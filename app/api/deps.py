"""
FastAPI dependencies.
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import get_database


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    yield from get_database()