import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///mental_health.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sender = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")

def init_db():
    Base.metadata.create_all(engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_conversations(user_id):
    from sqlalchemy.orm import Session
    db = SessionLocal()
    try:
        convs = db.query(Conversation).filter(Conversation.user_id == user_id)\
            .order_by(Conversation.created_at.desc()).limit(10).all()
        return [{"id": c.id, "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")} for c in convs]
    finally:
        db.close()
