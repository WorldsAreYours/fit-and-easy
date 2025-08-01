"""
Common Pydantic schemas and base classes.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(20, ge=1, le=100, description="Number of items to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class MuscleGroupResponse(BaseModel):
    """Response schema for muscle groups."""
    id: int
    name: str
    category: str
    description: Optional[str]

    class Config:
        orm_mode = True