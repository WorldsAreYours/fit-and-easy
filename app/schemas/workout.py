"""
Workout-related Pydantic schemas.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .exercise import ExerciseResponse


class WorkoutBase(BaseModel):
    """Base workout schema with common fields."""
    name: str
    date: Optional[datetime] = None
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    """Schema for creating a new workout."""
    pass


class WorkoutUpdate(BaseModel):
    """Schema for updating a workout."""
    name: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class WorkoutExerciseBase(BaseModel):
    """Base workout exercise schema."""
    exercise_id: int
    sets: int = Field(3, ge=1, le=20)
    reps: int = Field(10, ge=1, le=100)
    weight: Optional[float] = Field(None, ge=0, description="Weight in kg")
    rest_time: int = Field(60, ge=0, le=600, description="Rest time in seconds")
    order: int = Field(1, ge=1, description="Exercise order in workout")


class WorkoutExerciseCreate(WorkoutExerciseBase):
    """Schema for adding an exercise to a workout."""
    pass


class WorkoutExerciseUpdate(BaseModel):
    """Schema for updating a workout exercise."""
    sets: Optional[int] = Field(None, ge=1, le=20)
    reps: Optional[int] = Field(None, ge=1, le=100)
    weight: Optional[float] = Field(None, ge=0)
    rest_time: Optional[int] = Field(None, ge=0, le=600)
    order: Optional[int] = Field(None, ge=1)


class WorkoutExerciseResponse(WorkoutExerciseBase):
    """Schema for workout exercise API responses."""
    id: int
    exercise: ExerciseResponse

    class Config:
        orm_mode = True


class WorkoutResponse(WorkoutBase):
    """Schema for workout API responses."""
    id: int
    user_id: int
    workout_exercises: List[WorkoutExerciseResponse] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class GeneratedWorkout(BaseModel):
    """Schema for generated workout responses."""
    name: str
    exercises: List[ExerciseResponse]
    estimated_duration: int = Field(..., description="Estimated duration in minutes")
    target_muscle_groups: List[str]
    difficulty_level: str