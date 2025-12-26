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

def get_session():
    return SessionLocal()

# 🔥 THESE 4 FUNCTIONS WERE MISSING 🔥
def get_conversation_messages(conv_id):
    session = get_session()
    try:
        messages = (session.query(Message)
                   .filter(Message.conversation_id == conv_id)
                   .order_by(Message.timestamp)
                   .all())
        return [{"sender": m.sender, "content": m.content} for m in messages]
    finally:
        session.close()

def save_message(conv_id, sender, content):
    session = get_session()
    try:
        message = Message(conversation_id=conv_id, sender=sender, content=content)
        session.add(message)
        session.commit()
    finally:
        session.close()

def create_new_conversation(user_id):
    session = get_session()
    try:
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv.id
    finally:
        session.close()

def get_user_conversations(user_id):
    session = get_session()
    try:
        convs = (session.query(Conversation)
                .filter(Conversation.user_id == user_id)
                .order_by(Conversation.created_at.desc())
                .limit(10)
                .all())
        return [{"id": c.id, "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")} for c in convs]
    finally:
        session.close()
