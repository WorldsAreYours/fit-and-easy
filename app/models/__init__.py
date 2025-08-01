"""
Database models package.

Imports all models for easy access and ensures proper model registration.
"""

from .base import BaseModel, TimestampMixin
from .enums import FitnessLevel, Difficulty, Equipment
from .user import User
from .exercise import Exercise, MuscleGroup, exercise_muscle_groups
from .workout import Workout, WorkoutExercise

__all__ = [
    "BaseModel",
    "TimestampMixin", 
    "FitnessLevel",
    "Difficulty",
    "Equipment",
    "User",
    "Exercise",
    "MuscleGroup", 
    "exercise_muscle_groups",
    "Workout",
    "WorkoutExercise",
]