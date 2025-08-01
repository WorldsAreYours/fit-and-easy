"""
Exercise and muscle group models.
"""

from sqlalchemy import Column, String, Text, Enum, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel, TimestampMixin
from .enums import Difficulty, Equipment


# Association table for many-to-many relationship between exercises and muscle groups
exercise_muscle_groups = Table(
    'exercise_muscle_groups',
    BaseModel.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('muscle_group_id', Integer, ForeignKey('muscle_groups.id'), primary_key=True)
)


class MuscleGroup(BaseModel):
    """
    Standardized muscle groups for precise exercise categorization.
    Allows for efficient querying and filtering by specific muscle groups.
    """
    __tablename__ = "muscle_groups"

    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # e.g., "upper_body", "lower_body", "core"
    description = Column(Text)

    # Relationships
    exercises = relationship("Exercise", secondary=exercise_muscle_groups, back_populates="muscle_groups")


class Exercise(BaseModel, TimestampMixin):
    """
    Exercise model with proper normalization.
    Features many-to-many relationship with muscle groups and standardized equipment.
    """
    __tablename__ = "exercises"

    name = Column(String(200), nullable=False, index=True)
    primary_equipment = Column(Enum(Equipment), nullable=False, index=True)
    secondary_equipment = Column(Enum(Equipment), nullable=True)  # Optional secondary equipment
    difficulty = Column(Enum(Difficulty), default=Difficulty.MEDIUM, index=True)
    instructions = Column(Text, nullable=False)
    tips = Column(Text)  # Additional form tips or variations

    # Relationships
    muscle_groups = relationship("MuscleGroup", secondary=exercise_muscle_groups, back_populates="exercises")
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")