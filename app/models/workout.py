"""
Workout and workout exercise models.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel, TimestampMixin


class Workout(BaseModel, TimestampMixin):
    """
    Workout model representing a user's workout session.
    Contains metadata and links to exercises through WorkoutExercise.
    """
    __tablename__ = "workouts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(BaseModel):
    """
    Association table linking workouts to exercises with specific parameters.
    Stores sets, reps, weight, and rest time for each exercise in a workout.
    """
    __tablename__ = "workout_exercises"

    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    weight = Column(Float, nullable=True)  # Weight in kg, nullable for bodyweight exercises
    rest_time = Column(Integer, default=60)  # Rest time in seconds
    order = Column(Integer, default=1)  # Exercise order in workout

    # Relationships
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")