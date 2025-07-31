"""
Database configuration and session management for the trainer app.
Uses SQLite with SQLAlchemy synchronous support for simplicity and compatibility.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database URL - using SQLite
DATABASE_URL = "sqlite:///./trainer_app.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_database():
    """
    Dependency function to get database session.
    Used for FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables (useful for testing/reset)"""
    Base.metadata.drop_all(bind=engine)