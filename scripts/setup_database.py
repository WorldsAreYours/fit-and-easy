#!/usr/bin/env python3
"""
Database setup script.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import create_tables, get_database
from app.models import MuscleGroup, Exercise
from database.seeds.muscle_groups import MUSCLE_GROUPS_DATA
from database.seeds.exercises import EXERCISES_DATA


def seed_muscle_groups(db: Session) -> None:
    """Populate the database with standardized muscle groups."""
    print("🏋️  Seeding muscle groups...")
    
    # Check if muscle groups already exist
    existing_count = db.query(MuscleGroup).count()
    if existing_count > 0:
        print(f"   ✅ Database already contains {existing_count} muscle groups. Skipping seed.")
        return
    
    for group_data in MUSCLE_GROUPS_DATA:
        muscle_group = MuscleGroup(**group_data)
        db.add(muscle_group)
    
    db.commit()
    print(f"   ✅ Added {len(MUSCLE_GROUPS_DATA)} muscle groups")


def seed_exercises(db: Session) -> None:
    """Populate the database with exercises and their muscle group relationships."""
    print("💪 Seeding exercises...")
    
    # Check if exercises already exist
    existing_count = db.query(Exercise).count()
    if existing_count > 0:
        print(f"   ✅ Database already contains {existing_count} exercises. Skipping seed.")
        return
    
    # Create a mapping of muscle group names to objects
    muscle_groups_map = {mg.name: mg for mg in db.query(MuscleGroup).all()}
    
    for exercise_data in EXERCISES_DATA:
        # Extract muscle group names and get the actual objects
        muscle_group_names = exercise_data.pop("muscle_groups")
        muscle_group_objects = [
            muscle_groups_map[name] 
            for name in muscle_group_names 
            if name in muscle_groups_map
        ]
        
        # Create exercise
        exercise = Exercise(**exercise_data)
        exercise.muscle_groups = muscle_group_objects
        
        db.add(exercise)
    
    db.commit()
    print(f"   ✅ Added {len(EXERCISES_DATA)} exercises with muscle group relationships")


def main():
    """Main setup function."""
    print("🚀 Setting up Personal Trainer Database")
    print("=" * 50)
    
    # Create tables
    print("📋 Creating database tables...")
    create_tables()
    print("   ✅ Tables created successfully")
    
    # Get database session
    db = next(get_database())
    
    try:
        # Seed data in order (muscle groups first, then exercises)
        seed_muscle_groups(db)
        seed_exercises(db)
        
        # Print summary
        muscle_group_count = db.query(MuscleGroup).count()
        exercise_count = db.query(Exercise).count()
        
        print(f"\n🎉 Database setup complete!")
        print(f"   📊 Summary:")
        print(f"      • Muscle Groups: {muscle_group_count}")
        print(f"      • Exercises: {exercise_count}")
        print(f"\n🏃‍♂️ Ready to start your fitness journey!")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()