from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool  # 🔥 STREAMLIT CLOUD FIX
from datetime import datetime
import sqlite3

# 🔥 FIX: Enable SQLite foreign keys
def init_sqlite():
    conn = sqlite3.connect('mental_health.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.commit()
    conn.close()

Base = declarative_base()

# 🔥 COMPLETE STREAMLIT CLOUD FIX - Handles ALL threading issues
engine = create_engine(
    'sqlite:///mental_health.db',
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=NullPool  # No connection pooling conflicts
)
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
    """Initialize database tables safely"""
    Base.metadata.create_all(engine, checkfirst=True)
    init_sqlite()  # Enable foreign keys

def get
