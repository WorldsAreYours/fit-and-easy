"""
SQLAlchemy models for the personal trainer app.
Defines the database schema for users, exercises, workouts, and their relationships.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum
from datetime import datetime


class FitnessLevel(str, enum.Enum):
    """Enumeration for user fitness levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Difficulty(str, enum.Enum):
    """Enumeration for exercise difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class User(Base):
    """
    User model representing app users with their fitness profiles.
    Central entity that owns workouts and has fitness preferences.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    fitness_level = Column(Enum(FitnessLevel), default=FitnessLevel.BEGINNER)
    goals = Column(Text)  # JSON string or comma-separated goals
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    """
    Exercise model representing individual exercises with their properties.
    Can be used across multiple workouts and users.
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    muscle_groups = Column(String(500))  # Comma-separated muscle groups
    equipment = Column(String(200))  # Equipment needed
    difficulty = Column(Enum(Difficulty), default=Difficulty.MEDIUM)
    instructions = Column(Text, nullable=False)

    # Relationships
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")


class Workout(Base):
    """
    Workout model representing a user's workout session.
    Contains metadata and links to exercises through WorkoutExercise.
    """
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(Base):
    """
    Association table linking workouts to exercises with specific parameters.
    Stores sets, reps, weight, and rest time for each exercise in a workout.
    """
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)  # Added primary key for easier querying
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    weight = Column(Float, nullable=True)  # Weight in kg, nullable for bodyweight exercises
    rest_time = Column(Integer, default=60)  # Rest time in seconds

    # Relationships
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")