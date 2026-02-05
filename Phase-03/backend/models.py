import os
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

# --- Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, echo=False)

# --- Models ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str

class Task(SQLModel, table=True): # Yahan Task rakha hai mcp_tools ke liye
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

# Agent.py ke liye alias (Taki ImportError na aaye)
Todo = Task 

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str 
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

# --- Database Initialization ---
def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session