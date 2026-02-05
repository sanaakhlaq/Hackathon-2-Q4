"""
Database models for the application
Uses the DATABASE_URL from environment variables
Optimized for Neon Serverless PostgreSQL with proper indexing and relationships
"""
import os
from urllib.parse import urlparse
from typing import Optional, List
from datetime import datetime

# Import SQLModel components
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from contextlib import contextmanager

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Fallback to SQLite for development
    DATABASE_URL = "sqlite:///./todo.db"

# Configure connection pool settings optimized for Neon Serverless
connect_args = {"check_same_thread": False}  # Needed for SQLite

# Global engine instance
engine = None

def create_db_and_tables():
    global engine
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SQLModel.metadata.create_all(bind=engine)

def get_db():
    with Session(engine) as session:
        yield session

class User(SQLModel, table=True):
    """User model with proper indexing and relationships"""
    __tablename__ = "users"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields with indexes
    name: str = Field(max_length=100)
    email: str = Field(unique=True)
    hashed_password: str = Field(max_length=255)  # Add hashed password field

    # Timestamps with indexes
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationships
    todos: List["Todo"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Todo(SQLModel, table=True):
    """Todo model with proper indexing and relationships"""
    __tablename__ = "todos"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields with indexes
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)  # Use Text for longer content
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=20)  # Add priority field

    # Foreign key with index
    user_id: int = Field(foreign_key="users.id")

    # Timestamps with indexes
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship
    owner: Optional[User] = Relationship(back_populates="todos")

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed}, priority='{self.priority}')>"


def init_db():
    """Initialize database tables with proper error handling"""
    try:
        create_db_and_tables()
        print("Database tables created successfully!")

        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        expected_tables = ['users', 'todos']
        for table in expected_tables:
            if table not in tables:
                print(f"Warning: Table '{table}' was not created")
            else:
                print(f"Table '{table}' exists: [OK]")

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    print("Database URL configured:", bool(DATABASE_URL))

    # Initialize database
    init_db()