from sqlmodel import create_engine, Session
from models import SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not set")
    print("Please make sure your .env file is configured correctly")
    exit(1)

# Configure engine with Neon-optimized settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use (essential for serverless)
    pool_recycle=300,    # Recycle connections every 5 minutes to handle serverless timeouts
    echo=False,          # Set to True for SQL query logging during development
    connect_args={
        "connect_timeout": 10,  # Timeout for establishing connections
    }
)

def get_session():
    """Generator that yields database sessions"""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables using SQLModel msg_metadata"""
    SQLModel.metadata.create_all(engine)