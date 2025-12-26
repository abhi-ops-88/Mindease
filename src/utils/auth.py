import hashlib
from src.utils.database import create_user, get_user

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, username, password):
    password_hash = hash_password(password)
    success = create_user(email, username, password_hash)
    return success, "Email/username exists" if not success else "Success"

def login_user(email, password):
    password_hash = hash_password(password)
    username = get_user(email, password_hash)
    return username is not None, username
