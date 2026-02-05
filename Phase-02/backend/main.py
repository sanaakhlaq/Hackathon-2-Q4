import os
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- Imports ---
from auth import signup_user, login_user, verify_token, get_user_by_email
from models import init_db, User, Todo, get_db
from sqlmodel import Session, select

# Database initialization
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

app = FastAPI(title="Todo API", version="1.0.0")

# --- CORS Settings ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security_scheme = HTTPBearer()

# --- Request/Response Models ---
class UserSignupRequest(BaseModel):
    name: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Medium"

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    completed: bool
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Dependencies ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    try:
        token = credentials.credentials
        payload = verify_token(token)
        email = payload.get("sub")
        user = get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token or session expired")

# --- API Routes ---

@app.get("/")
def read_root():
    return {"message": "Backend is Running Successfully!", "port": "7860"}

@app.post("/signup", response_model=UserResponse)
def signup(user_data: UserSignupRequest):
    try:
        user_info = signup_user(user_data.name, user_data.email, user_data.password)
        return UserResponse(id=user_info["id"], name=user_info["name"], email=user_info["email"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=TokenResponse)
def login(user_data: UserLoginRequest):
    try:
        token = login_user(user_data.email, user_data.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return TokenResponse(access_token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/me", response_model=UserResponse)
def get_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"]
    )

# --- Todo Routes ---

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = db.exec(statement).all()
    return todos

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from models import Todo
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        user_id=current_user["id"],
        completed=False,
        created_at=datetime.utcnow()  # Date fix
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# --- DELETE ROUTE (ADDED) ---
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from models import Todo
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user["id"])
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(todo)
    db.commit()
    return {"message": "Task deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}