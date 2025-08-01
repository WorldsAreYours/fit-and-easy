"""
Exercise-related Pydantic schemas.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import Equipment, Difficulty
from .common import MuscleGroupResponse


class ExerciseBase(BaseModel):
    """Base exercise schema with common fields."""
    name: str
    primary_equipment: Equipment
    secondary_equipment: Optional[Equipment] = None
    difficulty: Difficulty = Difficulty.MEDIUM
    instructions: str
    tips: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """Schema for creating a new exercise."""
    muscle_group_ids: List[int] = Field(..., min_items=1, description="List of muscle group IDs")


class ExerciseUpdate(BaseModel):
    """Schema for updating an exercise."""
    name: Optional[str] = None
    primary_equipment: Optional[Equipment] = None
    secondary_equipment: Optional[Equipment] = None
    difficulty: Optional[Difficulty] = None
    instructions: Optional[str] = None
    tips: Optional[str] = None
    muscle_group_ids: Optional[List[int]] = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise API responses."""
    id: int
    muscle_groups: List[MuscleGroupResponse]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ExerciseFilter(BaseModel):
    """Schema for exercise filtering parameters."""
    muscle_groups: Optional[List[str]] = Field(None, description="Filter by muscle group names")
    equipment: Optional[List[Equipment]] = Field(None, description="Filter by equipment types")
    difficulty: Optional[List[Difficulty]] = Field(None, description="Filter by difficulty levels")
    muscle_categories: Optional[List[str]] = Field(None, description="Filter by muscle categories")
    require_all_muscle_groups: bool = Field(False, description="Require ALL muscle groups (AND) vs ANY (OR)")
    search: Optional[str] = Field(None, description="Search in name and instructions")