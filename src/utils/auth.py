import hashlib
from src.database.models import get_session, User

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email: str, username: str, password: str):
    session = get_session()
    try:
        if session.query(User).filter(User.email == email).first():
            return False, "Email already exists"
        if session.query(User).filter(User.username == username).first():
            return False, "Username already taken"
        
        hashed_pwd = hash_password(password)
        user = User(email=email, username=username, password_hash=hashed_pwd)
        session.add(user)
        session.commit()
        session.refresh(user)
        return True, user
    finally:
        session.close()

def authenticate_user(email: str, password: str):
    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user and user.password_hash == hash_password(password):
            return True, user
        return False, None
    finally:
        session.close()
