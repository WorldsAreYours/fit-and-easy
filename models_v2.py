"""
Improved SQLAlchemy models for the personal trainer app.
Features proper normalization for muscle groups and standardized equipment.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database_v2 import Base
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


class Equipment(str, enum.Enum):
    """Standardized equipment types for exercises"""
    BODYWEIGHT = "bodyweight"
    DUMBBELLS = "dumbbells"
    BARBELL = "barbell"
    KETTLEBELL = "kettlebell"
    RESISTANCE_BANDS = "resistance_bands"
    CABLE_MACHINE = "cable_machine"
    SMITH_MACHINE = "smith_machine"
    LEG_PRESS = "leg_press"
    LAT_PULLDOWN = "lat_pulldown"
    ROWING_MACHINE = "rowing_machine"
    PULL_UP_BAR = "pull_up_bar"
    BENCH = "bench"
    INCLINE_BENCH = "incline_bench"
    DECLINE_BENCH = "decline_bench"
    STABILITY_BALL = "stability_ball"
    MEDICINE_BALL = "medicine_ball"
    FOAM_ROLLER = "foam_roller"
    YOGA_MAT = "yoga_mat"
    CARDIO_MACHINE = "cardio_machine"


# Association table for many-to-many relationship between exercises and muscle groups
exercise_muscle_groups = Table(
    'exercise_muscle_groups',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('muscle_group_id', Integer, ForeignKey('muscle_groups.id'), primary_key=True)
)


class MuscleGroup(Base):
    """
    Standardized muscle groups for precise exercise categorization.
    Allows for efficient querying and filtering by specific muscle groups.
    """
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # e.g., "upper_body", "lower_body", "core"
    description = Column(Text)

    # Relationships
    exercises = relationship("Exercise", secondary=exercise_muscle_groups, back_populates="muscle_groups")


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
    Improved exercise model with proper normalization.
    Features many-to-many relationship with muscle groups and standardized equipment.
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    primary_equipment = Column(Enum(Equipment), nullable=False, index=True)
    secondary_equipment = Column(Enum(Equipment), nullable=True)  # Optional secondary equipment
    difficulty = Column(Enum(Difficulty), default=Difficulty.MEDIUM, index=True)
    instructions = Column(Text, nullable=False)
    tips = Column(Text)  # Additional form tips or variations
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    muscle_groups = relationship("MuscleGroup", secondary=exercise_muscle_groups, back_populates="exercises")
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

    id = Column(Integer, primary_key=True, index=True)
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