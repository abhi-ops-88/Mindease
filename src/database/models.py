from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool
from datetime import datetime
import sqlite3

# =========================================================
# DATABASE CONFIG (STREAMLIT CLOUD SAFE)
# =========================================================

DATABASE_URL = "sqlite:///mental_health.db"

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,  # 🔥 avoids threading issues
)

SessionLocal = sessionmaker(bind=engine)


# =========================================================
# SQLITE FOREIGN KEY SUPPORT
# =========================================================

def init_sqlite():
    conn = sqlite3.connect("mental_health.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()


# =========================================================
# MODELS
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(
        Integer, ForeignKey("conversations.id"), nullable=False
    )
    sender = Column(String(10), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


# =========================================================
# DB INITIALIZATION
# =========================================================

def init_db():
    """Create tables safely (idempotent)"""
    Base.metadata.create_all(engine, checkfirst=True)
    init_sqlite()


# =========================================================
# SESSION HELPER
# =========================================================

def get_session():
    return SessionLocal()


# =========================================================
# CHAT HELPERS (USED BY ChatInterface)
# =========================================================

def get_user_conversations(user_id: int):
    session = get_session()
    try:
        conversations = (
            session.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

        return [
            {
                "id": c.id,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for c in conversations
        ]
    finally:
        session.close()


def get_conversation_messages(conversation_id: int):
    if not conversation_id:
        return []

    session = get_session()
    try:
        messages = (
            session.query(Message)
            .filter(Message.conversation_id == int(conversation_id))
            .order_by(Message.timestamp)
            .all()
        )

        return [
            {
                "sender": m.sender,
                "content": m.content,
                "timestamp": m.timestamp,
            }
            for m in messages
        ]
    finally:
        session.close()


def create_new_conversation(user_id: int):
    session = get_session()
    try:
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv.id  # 🔥 IMPORTANT: return INT, not ORM
    finally:
        session.close()


def save_message(conversation_id: int, sender: str, content: str):
    session = get_session()
    try:
        msg = Message(
            conversation_id=int(conversation_id),
            sender=sender,
            content=content,
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return msg.id
    finally:
        session.close()
