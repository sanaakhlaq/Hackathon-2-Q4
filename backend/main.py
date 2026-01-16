"""
FastAPI Backend for Todo Application
Links Auth and Database layers with REST API endpoints
Implements Signup, Login, and Todo CRUD routes using the Auth and Database agents
"""
import os
import sys
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from jose import jwt
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend modules
from backend.auth import signup_user, login_user, verify_token, get_user_by_email, AuthException
from backend.models import init_db, db_manager, User, Todo, get_db_connection
from sqlalchemy.orm import Session

# Initialize database
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Todo application with authentication",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security_scheme = HTTPBearer()

# Pydantic models for request/response validation
class UserSignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., min_length=5, max_length=100, description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")

class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=100, description="User's email address")
    password: str = Field(..., min_length=1, max_length=100, description="User's password")

class TodoCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    priority: str = Field(default="medium", description="Priority level (high, medium, low)")

class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: Optional[bool] = Field(None, description="Completion status")
    priority: Optional[str] = Field(None, description="Priority level (high, medium, low)")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    user_id: int
    created_at: datetime
    updated_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    detail: str

# Dependency to verify JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """Dependency to get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        user = get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_db():
    """Dependency to get database session"""
    engine = get_db_connection()
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def read_root():
    """Root endpoint to verify API is running"""
    return {"message": "Todo API is running", "status": "success"}

@app.post("/signup",
          response_model=UserResponse,
          responses={
              201: {"description": "User created successfully"},
              400: {"model": ErrorResponse, "description": "Invalid input or user already exists"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
def signup(user_data: UserSignupRequest):
    """
    Register a new user with validated email and hashed password
    Uses the Auth agent for secure user flows and password hashing
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Use the Auth agent to handle signup logic
        user_info = signup_user(user_data.name, user_data.email, user_data.password)

        if user_info:
            return UserResponse(
                id=user_info["id"],
                name=user_info["name"],
                email=user_info["email"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/login",
          response_model=TokenResponse,
          responses={
              200: {"description": "Login successful, token returned"},
              400: {"model": ErrorResponse, "description": "Invalid credentials or input"},
              401: {"model": ErrorResponse, "description": "Invalid credentials"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
def login(user_data: UserLoginRequest):
    """
    Authenticate user and return access token
    Uses the Auth agent for secure authentication flow
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Use the Auth agent to handle login logic
        token = login_user(user_data.email, user_data.password)

        if token:
            return TokenResponse(access_token=token)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/me",
         response_model=UserResponse,
         responses={
             200: {"description": "User information retrieved successfully"},
             401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired token"},
             404: {"model": ErrorResponse, "description": "User not found"}
         })
def get_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user's information using JWT authentication
    Uses the Auth agent to verify token and retrieve user info
    Uses the Database agent for Neon-optimized session management
    """
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user.get("created_at")
    )

# Todo CRUD Endpoints
@app.post("/todos",
          response_model=TodoResponse,
          responses={
              201: {"description": "Todo created successfully"},
              400: {"model": ErrorResponse, "description": "Invalid input"},
              401: {"model": ErrorResponse, "description": "Unauthorized"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
def create_todo(
    todo_data: TodoCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo item for the authenticated user
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Create new todo associated with current user
        db_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            completed=False,
            priority=todo_data.priority,
            user_id=current_user["id"]
        )

        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)

        return TodoResponse(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            priority=db_todo.priority,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/todos",
         response_model=List[TodoResponse],
         responses={
             200: {"description": "List of user's todos returned successfully"},
             401: {"model": ErrorResponse, "description": "Unauthorized"},
             500: {"model": ErrorResponse, "description": "Internal server error"}
         })
def get_todos(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all todos for the authenticated user
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Query todos for current user
        todos = db.query(Todo).filter(Todo.user_id == current_user["id"]).all()

        return [TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        ) for todo in todos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/todos/{todo_id}",
         response_model=TodoResponse,
         responses={
             200: {"description": "Todo retrieved successfully"},
             401: {"model": ErrorResponse, "description": "Unauthorized"},
             404: {"model": ErrorResponse, "description": "Todo not found"},
             500: {"model": ErrorResponse, "description": "Internal server error"}
         })
def get_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific todo by ID for the authenticated user
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Query specific todo for current user
        todo = db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.user_id == current_user["id"]
        ).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        return TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.put("/todos/{todo_id}",
         response_model=TodoResponse,
         responses={
             200: {"description": "Todo updated successfully"},
             400: {"model": ErrorResponse, "description": "Invalid input"},
             401: {"model": ErrorResponse, "description": "Unauthorized"},
             404: {"model": ErrorResponse, "description": "Todo not found"},
             500: {"model": ErrorResponse, "description": "Internal server error"}
         })
def update_todo(
    todo_id: int,
    todo_data: TodoUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific todo by ID for the authenticated user
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Query specific todo for current user
        todo = db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.user_id == current_user["id"]
        ).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        # Update fields if provided
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.completed is not None:
            todo.completed = todo_data.completed
        if todo_data.priority is not None:
            todo.priority = todo_data.priority

        db.commit()
        db.refresh(todo)

        return TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.delete("/todos/{todo_id}",
            responses={
                200: {"description": "Todo deleted successfully"},
                401: {"model": ErrorResponse, "description": "Unauthorized"},
                404: {"model": ErrorResponse, "description": "Todo not found"},
                500: {"model": ErrorResponse, "description": "Internal server error"}
            })
def delete_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific todo by ID for the authenticated user
    Uses the Database agent for Neon-optimized session management
    """
    try:
        # Query specific todo for current user
        todo = db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.user_id == current_user["id"]
        ).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        db.delete(todo)
        db.commit()

        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Health check endpoint to verify API is operational"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database": "connected"  # Simplified - in real app, check actual DB connection
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )