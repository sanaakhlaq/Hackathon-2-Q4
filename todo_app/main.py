from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from models import init_db, Todo, engine
from auth import signup_user, create_access_token, verify_token, get_user_by_email, verify_password
from pydantic import BaseModel
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Todo API",
    lifespan=lifespan
)

# Using Starlette's Middleware class approach to avoid unpacking errors
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Apply middleware to the app
for middleware_item in middleware:
    app.add_middleware(middleware_item.__class__, **middleware_item.options)

security = HTTPBearer()

# Pydantic Models
class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TodoCreate(BaseModel):
    title: str
    description: str = None


def get_db():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def get_current_user(
    res: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(res.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/")
def home():
    return {"message": "Server is running!", "docs": "/docs"}


@app.post("/signup")
def signup(data: UserSignup):
    try:
        user = signup_user(data.name, data.email, data.password)
        return {"id": user.id, "name": user.name, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
def login(data: UserLogin):
    user = get_user_by_email(data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/todos", response_model=List[Todo])
def list_todos(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statement = select(Todo).where(Todo.user_id == user.id)
    return db.exec(statement).all()


@app.post("/todos", response_model=Todo)
def add_todo(
    data: TodoCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_todo = Todo(title=data.title, description=data.description, user_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo