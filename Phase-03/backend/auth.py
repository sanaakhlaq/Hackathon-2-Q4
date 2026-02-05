import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from sqlmodel import Session, select
from models import User, engine

SECRET_KEY = os.getenv('BETTER_AUTH_SECRET', 'fallback_secret_123')
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain, hashed) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

def signup_user(name, email, password):
    with Session(engine) as session:
        statement = select(User).where(User.email == email.lower())
        if session.exec(statement).first():
            raise Exception("Email already exists")
        db_user = User(name=name, email=email.lower(), hashed_password=hash_password(password))
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

def get_user_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email.lower())).first()