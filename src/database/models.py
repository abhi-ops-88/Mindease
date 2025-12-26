from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool  # 🔥 ADD THIS IMPORT
from datetime import datetime
import sqlite3

# ... your init_sqlite() function stays same ...

Base = declarative_base()
# 🔥 COMPLETE FIX - Handles ALL Streamlit Cloud issues
engine = create_engine(
    'sqlite:///mental_health.db',
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=NullPool  # No connection pooling conflicts
)
SessionLocal = sessionmaker(bind=engine)
