import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment variables."""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    logger.info("Database URL loaded from environment variables")
    return database_url

# Get the database URL from environment variables
DATABASE_URL = get_database_url()

# Example: Create a database engine (uncomment if you're using SQLAlchemy)
# engine = create_engine(DATABASE_URL)

# Your application code here
# Example usage of DATABASE_URL:
print(f"Database URL: {DATABASE_URL}")

# If you're building a Gradio app (common for Hugging Face Spaces)
if __name__ == "__main__":
    # Import and run your main application
    # For example, if using Gradio:
    # import gradio as gr
    # gr.Interface(...).launch(server_port=7860)
    
    # Or if it's a Flask/FastAPI app:
    # from your_app import app
    # app.run(host='0.0.0.0', port=7860)
    
    logger.info("Application running on port 7860")
    logger.info(f"Using database: {DATABASE_URL.split('@')[0] if '@' in DATABASE_URL else DATABASE_URL}")