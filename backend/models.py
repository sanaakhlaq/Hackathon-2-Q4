"""
Database models for the application
Uses the DATABASE_URL from environment variables
Optimized for Neon Serverless PostgreSQL with proper indexing and relationships
"""
import os
from urllib.parse import urlparse
from typing import Optional, List
from datetime import datetime

# Import SQLAlchemy components for proper model definitions
try:
    from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Index, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    from sqlalchemy.pool import QueuePool
except ImportError:
    print("SQLAlchemy is required. Please install with: pip install sqlalchemy psycopg2-binary")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Basic database configuration
DB_CONFIG = {
    'host': None,
    'port': None,
    'database': None,
    'username': None,
    'password': None,
    'scheme': None,
}

if DATABASE_URL:
    # Parse the database URL to extract connection details
    db_url = urlparse(DATABASE_URL)

    # Update database configuration
    DB_CONFIG = {
        'host': db_url.hostname,
        'port': db_url.port,
        'database': db_url.path[1:],  # Remove leading slash
        'username': db_url.username,
        'password': db_url.password,
        'scheme': db_url.scheme,
    }

# Create base class for all models
Base = declarative_base()

# Configure connection pool settings optimized for Neon Serverless
POOL_SETTINGS = {
    "poolclass": QueuePool,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_pre_ping": True,  # Verify connections before use
    "pool_recycle": 300,    # Recycle connections every 5 minutes
    "echo": False           # Set to True for SQL query logging
}


class DatabaseManager:
    """Manages database connections and sessions for Neon Serverless"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def initialize_engine(self):
        """Initialize database engine with Neon-optimized settings"""
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable not set")

        self.engine = create_engine(
            DATABASE_URL,
            **POOL_SETTINGS
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self.engine

    def get_session(self):
        """Get a database session"""
        if self.SessionLocal is None:
            self.initialize_engine()
        return self.SessionLocal()


# Global database manager instance
db_manager = DatabaseManager()


class User(Base):
    """User model with proper indexing and relationships"""
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core fields with indexes
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)  # Add hashed password field

    # Timestamps with indexes
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationships
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Todo(Base):
    """Todo model with proper indexing and relationships"""
    __tablename__ = "todos"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core fields with indexes
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)  # Use Text for longer content
    completed = Column(Boolean, default=False, index=True)
    priority = Column(String(20), default='medium', index=True)  # Add priority field

    # Foreign key with index
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Timestamps with indexes
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationship
    owner = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed}, priority='{self.priority}')>"


# Define indexes for better query performance
Index('idx_users_email', User.email)  # Already defined with unique constraint
Index('idx_users_created_at', User.created_at)
Index('idx_todos_user_id', Todo.user_id)
Index('idx_todos_completed', Todo.completed)
Index('idx_todos_created_at', Todo.created_at)


def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable not set")

        engine = db_manager.initialize_engine()
        return engine
    except Exception as e:
        print(f"Error establishing database connection: {e}")
        raise


def init_db():
    """Initialize database tables with proper error handling"""
    try:
        engine = get_db_connection()
        # Create all tables
        Base.metadata.create_all(bind=engine)
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
    print("Database connection details:", DB_CONFIG)

    # Initialize database
    init_db()