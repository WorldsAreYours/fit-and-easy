"""
User-related Pydantic schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.enums import FitnessLevel


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str
    email: str
    fitness_level: FitnessLevel = FitnessLevel.BEGINNER
    goals: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str] = None
    email: Optional[str] = None
    fitness_level: Optional[FitnessLevel] = None
    goals: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user API responses."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True