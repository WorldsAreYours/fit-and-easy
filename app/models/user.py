"""
User model and related classes.
"""

from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel, TimestampMixin
from .enums import FitnessLevel


class User(BaseModel, TimestampMixin):
    """
    User model representing app users with their fitness profiles.
    Central entity that owns workouts and has fitness preferences.
    """
    __tablename__ = "users"

    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    fitness_level = Column(Enum(FitnessLevel), default=FitnessLevel.BEGINNER)
    goals = Column(Text)  # JSON string or comma-separated goals

    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")