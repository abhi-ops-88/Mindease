# -*- coding: utf-8 -*-

import hashlib
from sqlalchemy.exc import IntegrityError
from src.database.models import get_session, User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(email: str, username: str, password: str):
    session = get_session()
    try:
        if session.query(User).filter(User.email == email).first():
            return None
        if session.query(User).filter(User.username == username).first():
            return None

        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def authenticate_user(email: str, password: str):
    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user and user.password_hash == hash_password(password):
            return user
        return None
    finally:
        session.close()
