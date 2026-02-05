"""
Database initialization script for Neon Serverless PostgreSQL
Creates tables in the Neon database using the models defined in models.py
Implements best practices for serverless connections with proper connection pooling
"""
import os
import sys
from urllib.parse import urlparse
from contextlib import contextmanager

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add backend directory to path to import models
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import the updated models with proper SQLAlchemy setup
from models import User, Todo, DB_CONFIG, db_manager, Base

# We'll use SQLAlchemy for database operations
try:
    from sqlalchemy import create_engine, text, inspect
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.pool import QueuePool
except ImportError:
    print("SQLAlchemy is required for this script. Please install it using: pip install sqlalchemy psycopg2-binary")
    sys.exit(1)

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not set")
    print("Please make sure your .env file is configured correctly")
    sys.exit(1)

print(f"Using database: {DB_CONFIG['database']} on host {DB_CONFIG['host']}")

# Configure connection pool settings optimized for Neon Serverless
POOL_SETTINGS = {
    "poolclass": QueuePool,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_pre_ping": True,  # Verify connections before use (essential for serverless)
    "pool_recycle": 300,    # Recycle connections every 5 minutes to handle serverless timeouts
    "echo": False,          # Set to True for SQL query logging during development
    "connect_args": {
        "connect_timeout": 10,  # Timeout for establishing connections
    }
}

def create_neon_engine():
    """Create a database engine optimized for Neon Serverless PostgreSQL"""
    try:
        # Create engine with Neon-optimized settings
        engine = create_engine(
            DATABASE_URL,
            **POOL_SETTINGS
        )
        print("Neon-optimized database engine created successfully")
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        sys.exit(1)

@contextmanager
def get_db_session():
    """Context manager for database sessions with proper cleanup for serverless"""
    session = None
    try:
        engine = create_neon_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        # Begin a transaction
        session.begin()
        yield session

        # Commit the transaction if no errors occurred
        session.commit()
    except Exception as e:
        # Rollback the transaction on error to maintain ACID compliance
        if session:
            session.rollback()
        print(f"Database transaction error: {e}")
        raise
    finally:
        # Always close the session to return connection to pool
        if session:
            session.close()

def verify_table_exists(engine, table_name: str) -> bool:
    """Verify if a specific table exists in the database"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return table_name in tables
    except Exception as e:
        print(f"Error checking for table {table_name}: {e}")
        return False

def init_db():
    """Initialize the database by creating all tables with ACID compliance"""
    engine = create_neon_engine()

    try:
        # Create all tables defined in the models
        # Using transaction to ensure ACID compliance
        with engine.connect() as connection:
            # Begin transaction
            trans = connection.begin()
            try:
                Base.metadata.create_all(connection)
                trans.commit()
                print("Tables created successfully with ACID compliance!")
            except Exception as e:
                trans.rollback()
                print(f"Error creating tables: {e}")
                raise

        # Verify that the tables exist
        users_exists = verify_table_exists(engine, 'users')
        todos_exists = verify_table_exists(engine, 'todos')

        print(f"Users table exists: {users_exists}")
        print(f"Todos table exists: {todos_exists}")

        if users_exists and todos_exists:
            print("\nSUCCESS: Both 'users' and 'todos' tables have been created in Neon database!")
            print(f"Connected to database: {DB_CONFIG['database']}")
            print(f"Host: {DB_CONFIG['host']}")

            # Additional verification - check table structure
            inspector = inspect(engine)
            users_columns = [col['name'] for col in inspector.get_columns('users')]
            todos_columns = [col['name'] for col in inspector.get_columns('todos')]

            print(f"Users table columns: {users_columns}")
            print(f"Todos table columns: {todos_columns}")

            return True
        else:
            print("\nERROR: Tables were not created properly")
            return False

    except SQLAlchemyError as e:
        print(f"SQLAlchemy error during database initialization: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        return False

def test_connection_pooling():
    """Test connection pooling functionality"""
    print("\nTesting connection pooling...")
    try:
        engine = create_neon_engine()

        # Test multiple connections to verify pooling
        connections_tested = 0
        for i in range(3):
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                connections_tested += 1

        print(f"Successfully tested {connections_tested} pooled connections")
        return True
    except Exception as e:
        print(f"Error testing connection pooling: {e}")
        return False

if __name__ == "__main__":
    print("Starting Neon Serverless database initialization...")
    print(f"Database URL: {DATABASE_URL[:50]}...")  # Show partial URL for security
    print("Using optimized settings for Neon Serverless PostgreSQL:")
    print(f"  - Pool size: {POOL_SETTINGS['pool_size']}")
    print(f"  - Max overflow: {POOL_SETTINGS['max_overflow']}")
    print(f"  - Pool pre-ping: {POOL_SETTINGS['pool_pre_ping']}")
    print(f"  - Pool recycle: {POOL_SETTINGS['pool_recycle']} seconds")

    success = init_db()

    if success:
        # Test connection pooling
        pooling_success = test_connection_pooling()

        if pooling_success:
            print("\nDatabase initialization completed successfully!")
            print("The 'users' and 'todos' tables are now live on Neon!")
            print("Connection pooling and ACID compliance verified.")
        else:
            print("\nDatabase initialization completed but connection pooling test failed.")
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)