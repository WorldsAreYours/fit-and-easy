"""
Application configuration management.
"""

import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database
    database_url: str = "sqlite:///./trainer_app_structured.db"
    
    # API
    api_title: str = "Personal Trainer API"
    api_description: str = "Comprehensive fitness tracking and workout management API"
    api_version: str = "2.0.0"
    debug: bool = True  # Default to True for development
    
    # CORS
    cors_origins: List[str] = ["*"]  # Configure for production
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Workout Generation
    default_workout_duration: int = 45  # minutes
    min_workout_exercises: int = 3
    max_workout_exercises: int = 8
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()