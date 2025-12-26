from sqlalchemy import (
    create_engine, Column, Integer, String,
    Text, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.pool import NullPool
from datetime import datetime
import sqlite3

DATABASE_URL = "sqlite:///mental_health.db"

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)

SessionLocal = sessionmaker(bind=engine)

def init_sqlite():
    conn = sqlite3.connect("mental_health.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.close()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

def init_db():
    Base.metadata.create_all(engine)
    init_sqlite()

def get_session():
    return SessionLocal()

# ===== Chat helpers =====

def create_new_conversation(user_id):
    session = get_session()
    conv = Conversation(user_id=user_id)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    session.close()
    return conv.id

def get_user_conversations(user_id):
    session = get_session()
    convs = (
        session.query(Conversation)
        .filter_by(user_id=user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
    session.close()
    return convs

def get_conversation_messages(conv_id):
    session = get_session()
    msgs = (
        session.query(Message)
        .filter_by(conversation_id=conv_id)
        .order_by(Message.timestamp)
        .all()
    )
    session.close()
    return msgs

def save_message(conv_id, sender, content):
    session = get_session()
    msg = Message(
        conversation_id=conv_id,
        sender=sender,
        content=content
    )
    session.add(msg)
    session.commit()
    session.close()
