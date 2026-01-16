"""
Database Reset Script
This script drops and recreates all database tables to accommodate schema changes.
Use this when you've made changes to the models that require table alterations.
"""
import sys
import os

# Add the project root to the path so we can import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import Base, get_db_connection

def reset_database():
    """Drop all tables and recreate them"""
    print("Getting database connection...")
    engine = get_db_connection()
    
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully!")
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
    
    print("\nDatabase reset completed!")

if __name__ == "__main__":
    print("WARNING: This script will DROP ALL DATA in the database!")
    print("This action cannot be undone.")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        reset_database()
    else:
        print("Operation cancelled.")