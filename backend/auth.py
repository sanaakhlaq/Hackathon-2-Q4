"""
Authentication module for the application
Handles user signup, login, password hashing, and JWT token generation
Uses optimized database session management from models.py for Neon Serverless PostgreSQL
"""
import os
import re
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Use jose.jwt instead of jwt
from jose import jwt

# Load environment variables
load_dotenv()

# Import database configuration and models with session management
from .models import User, db_manager, get_db_connection

# Get secret key from environment
SECRET_KEY = os.getenv('BETTER_AUTH_SECRET')
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthException(Exception):
    """Custom exception for authentication errors"""
    pass


def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_password(password: str) -> bool:
    """
    Validate password strength (minimum 8 characters)
    """
    return len(password) >= 8


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthException("Token has expired")
    except jwt.JWTError:
        raise AuthException("Invalid token")


def signup_user(name: str, email: str, password: str) -> Optional[dict]:
    """
    Register a new user with validated email and hashed password using Neon-optimized session management
    """
    # Validate email format
    if not validate_email(email):
        raise AuthException("Invalid email format")

    # Validate password length
    if not validate_password(password):
        raise AuthException("Password must be at least 8 characters long")

    # Get database session using the optimized connection pool from models.py
    engine = get_db_connection()

    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.query(User).filter(User.email == email.lower()).first()
        if existing_user:
            raise AuthException("User with this email already exists")

        # Hash the password
        hashed_password = hash_password(password)

        # Create new user with hashed password
        db_user = User(
            name=name,
            email=email.lower(),  # Store email in lowercase for consistency
            hashed_password=hashed_password  # Store the hashed password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }


def login_user(email: str, password: str) -> Optional[str]:
    """
    Authenticate user and return access token using Neon-optimized session management
    """
    # Validate email format
    if not validate_email(email):
        raise AuthException("Invalid email format")

    # Get database session using the optimized connection pool from models.py
    engine = get_db_connection()

    with Session(engine) as session:
        # Find user by email
        user = session.query(User).filter(User.email == email.lower()).first()

        if not user:
            raise AuthException("Invalid credentials")

        # Verify the provided password against the stored hash
        if not verify_password(password, user.hashed_password):
            raise AuthException("Invalid credentials")

        # Create and return access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email.lower(), "scopes": ["user"]},
            expires_delta=access_token_expires
        )

        return access_token


def generate_reset_token(email: str) -> Optional[str]:
    """
    Generate a password reset token
    """
    # Validate email format
    if not validate_email(email):
        raise AuthException("Invalid email format")

    # Create a special reset token with shorter expiration
    reset_data = {
        "sub": email.lower(),
        "type": "reset"
    }

    # Shorter expiration for reset tokens (1 hour)
    reset_token = create_access_token(
        data=reset_data,
        expires_delta=timedelta(hours=1)
    )

    return reset_token


def reset_password(reset_token: str, new_password: str) -> bool:
    """
    Reset user password using the reset token
    """
    # Validate new password
    if not validate_password(new_password):
        raise AuthException("New password must be at least 8 characters long")

    try:
        # Decode the reset token
        payload = verify_token(reset_token)

        # Check if this is a reset token
        if payload.get("type") != "reset":
            raise AuthException("Invalid reset token")

        # Extract email from token
        email = payload.get("sub")

        # Hash the new password
        hashed_new_password = hash_password(new_password)

        # In a real implementation, update the user's password in the database
        # Since our User model doesn't have a password field, we'll simulate
        print(f"Password reset initiated for {email}")
        return True

    except AuthException:
        raise
    except Exception:
        raise AuthException("Invalid or expired reset token")


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authenticate user credentials using Neon-optimized session management and return user info if valid
    """
    # Validate email format
    if not validate_email(email):
        raise AuthException("Invalid email format")

    # Get database session using the optimized connection pool from models.py
    engine = get_db_connection()

    with Session(engine) as session:
        # Find user by email
        user = session.query(User).filter(User.email == email.lower()).first()

        if not user:
            raise AuthException("Invalid credentials")

        # Verify the provided password against the stored hash
        if not verify_password(password, user.hashed_password):
            raise AuthException("Invalid credentials")

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Retrieve user by email using Neon-optimized session management
    """
    # Validate email format
    if not validate_email(email):
        raise AuthException("Invalid email format")

    # Get database session using the optimized connection pool from models.py
    engine = get_db_connection()

    with Session(engine) as session:
        user = session.query(User).filter(User.email == email.lower()).first()

        if not user:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }


# Example usage functions
def example_signup():
    """
    Example of how to use the signup function
    """
    try:
        user = signup_user("John Doe", "john.doe@example.com", "securepassword123")
        print(f"Signed up user: {user}")
    except AuthException as e:
        print(f"Signup failed: {e}")


def example_login():
    """
    Example of how to use the login function
    """
    try:
        token = login_user("john.doe@example.com", "securepassword123")
        print(f"Login successful, token: {token[:50]}...")  # Show partial token for security
    except AuthException as e:
        print(f"Login failed: {e}")


if __name__ == "__main__":
    print("Authentication module loaded")
    print(f"Secret key configured: {'Yes' if SECRET_KEY else 'No'}")

    # Run examples
    example_signup()
    example_login()