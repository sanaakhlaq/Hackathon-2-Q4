from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your database initialization function here
# from your_database_module import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    Runs startup and shutdown events.
    """
    logger.info("Starting up...")
    # Initialize database connection
    # await init_db()
    
    yield  # Application runs here
    
    # Cleanup on shutdown
    logger.info("Shutting down...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Secure API",
    description="A secure API with authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP Bearer token for authentication
security = HTTPBearer()


@app.get("/")
async def root():
    return {"message": "Welcome to the Secure API!"}


# Example Signup route
@app.post("/signup")
async def signup(username: str, password: str, email: str = None):
    """
    User signup endpoint
    """
    # Add your signup logic here
    return {
        "message": "User registered successfully",
        "username": username,
        "email": email
    }


# Example Login route
@app.post("/login")
async def login(username: str, password: str):
    """
    User login endpoint
    """
    # Add your login logic here
    # This is just a placeholder implementation
    if username and password:
        return {
            "message": "Login successful",
            "username": username,
            "access_token": f"fake_token_for_{username}"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )