#!/usr/bin/env python3
"""
Migration script to convert from old exercise model to new normalized model.
Converts comma-separated muscle groups to proper relationships.
"""

import sys
import os
import re
from typing import List, Dict, Set
from sqlalchemy.orm import Session

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import both old and new models
from database import get_database, create_tables
from models import Exercise as OldExercise, Equipment as OldEquipment  # Old model
from models_v2 import Exercise, MuscleGroup, Equipment, Difficulty  # New model


# Mapping from old string-based equipment to new enum
EQUIPMENT_MAPPING = {
    "bodyweight": Equipment.BODYWEIGHT,
    "dumbbells": Equipment.DUMBBELLS, 
    "dumbbell": Equipment.DUMBBELLS,
    "barbell": Equipment.BARBELL,
    "kettlebell": Equipment.KETTLEBELL,
    "resistance bands": Equipment.RESISTANCE_BANDS,
    "bands": Equipment.RESISTANCE_BANDS,
    "cable": Equipment.CABLE_MACHINE,
    "cable machine": Equipment.CABLE_MACHINE,
    "smith machine": Equipment.SMITH_MACHINE,
    "leg press": Equipment.LEG_PRESS,
    "lat pulldown": Equipment.LAT_PULLDOWN,
    "pulldown": Equipment.LAT_PULLDOWN,
    "rowing machine": Equipment.ROWING_MACHINE,
    "pull-up bar": Equipment.PULL_UP_BAR,
    "pull up bar": Equipment.PULL_UP_BAR,
    "pullup bar": Equipment.PULL_UP_BAR,
    "bench": Equipment.BENCH,
    "incline bench": Equipment.INCLINE_BENCH,
    "decline bench": Equipment.DECLINE_BENCH,
    "stability ball": Equipment.STABILITY_BALL,
    "exercise ball": Equipment.STABILITY_BALL,
    "medicine ball": Equipment.MEDICINE_BALL,
    "foam roller": Equipment.FOAM_ROLLER,
    "yoga mat": Equipment.YOGA_MAT,
    "mat": Equipment.YOGA_MAT,
    "treadmill": Equipment.CARDIO_MACHINE,
    "cardio": Equipment.CARDIO_MACHINE,
}

# Mapping for normalizing muscle group names
MUSCLE_GROUP_MAPPING = {
    # Chest variants
    "chest": "chest",
    "pecs": "chest", 
    "pectoral": "chest",
    "pectorals": "chest",
    "upper chest": "upper_chest",
    "lower chest": "lower_chest",
    
    # Back variants
    "back": "back",
    "lats": "lats",
    "latissimus": "lats",
    "latissimus dorsi": "lats",
    "rhomboids": "rhomboids",
    "traps": "traps",
    "trapezius": "traps",
    "rear delts": "rear_delts",
    "rear deltoids": "rear_delts",
    "posterior deltoids": "rear_delts",
    "lower back": "lower_back",
    "erector spinae": "lower_back",
    
    # Shoulders
    "shoulders": "shoulders",
    "delts": "shoulders",
    "deltoids": "shoulders",
    "front delts": "front_delts",
    "anterior delts": "front_delts",
    "anterior deltoids": "front_delts",
    "side delts": "side_delts",
    "lateral delts": "side_delts",
    "lateral deltoids": "side_delts",
    
    # Arms
    "biceps": "biceps",
    "bicep": "biceps",
    "triceps": "triceps",
    "tricep": "triceps",
    "forearms": "forearms",
    "forearm": "forearms",
    
    # Legs
    "legs": "quads",  # Default to quads for generic "legs"
    "quads": "quads",
    "quadriceps": "quads",
    "hamstrings": "hamstrings",
    "hamstring": "hamstrings",
    "glutes": "glutes",
    "glute": "glutes",
    "gluteus": "glutes",
    "calves": "calves",
    "calf": "calves",
    "hip flexors": "hip_flexors",
    "adductors": "adductors",
    "inner thighs": "adductors",
    "abductors": "abductors",
    
    # Core
    "core": "core",
    "abs": "abs",
    "abdominals": "abs",
    "obliques": "obliques",
    "oblique": "obliques",
    
    # Full body
    "full body": "full_body",
    "cardio": "cardio",
    "cardiovascular": "cardio",
}


def parse_muscle_groups(muscle_groups_string: str) -> List[str]:
    """Parse comma-separated muscle groups string into list of normalized names"""
    if not muscle_groups_string:
        return []
    
    # Split by comma and clean up
    raw_groups = [group.strip().lower() for group in muscle_groups_string.split(',')]
    
    # Normalize each group
    normalized_groups = []
    for group in raw_groups:
        if group in MUSCLE_GROUP_MAPPING:
            normalized_name = MUSCLE_GROUP_MAPPING[group]
            if normalized_name not in normalized_groups:
                normalized_groups.append(normalized_name)
        else:
            print(f"⚠️  Unknown muscle group: '{group}' - skipping")
    
    return normalized_groups


def parse_equipment(equipment_string: str) -> Equipment:
    """Parse equipment string to Equipment enum"""
    if not equipment_string:
        return Equipment.BODYWEIGHT
    
    equipment_lower = equipment_string.strip().lower()
    
    if equipment_lower in EQUIPMENT_MAPPING:
        return EQUIPMENT_MAPPING[equipment_lower]
    
    # Try partial matches
    for key, value in EQUIPMENT_MAPPING.items():
        if key in equipment_lower:
            return value
    
    print(f"⚠️  Unknown equipment: '{equipment_string}' - defaulting to bodyweight")
    return Equipment.BODYWEIGHT


def migrate_exercises(db: Session) -> Dict[str, int]:
    """Migrate exercises from old format to new format"""
    print("🔄 Migrating exercises...")
    
    # This is a conceptual migration - in practice you'd read from the old database
    # For demo purposes, we'll use the old seed data format
    
    OLD_EXERCISE_DATA = [
        {
            "name": "Push-ups",
            "muscle_groups": "chest,triceps,shoulders",
            "equipment": "bodyweight",
            "difficulty": "easy",
            "instructions": "Start in plank position, lower body until chest nearly touches floor, push back up."
        },
        {
            "name": "Bench Press", 
            "muscle_groups": "chest,triceps,front delts",
            "equipment": "barbell",
            "difficulty": "medium",
            "instructions": "Lie on bench, grip bar wider than shoulders, lower to chest, press up."
        },
        {
            "name": "Squats",
            "muscle_groups": "quads,glutes,core",
            "equipment": "bodyweight", 
            "difficulty": "easy",
            "instructions": "Stand with feet shoulder-width apart, lower hips back and down, drive through heels."
        },
        {
            "name": "Pull-ups",
            "muscle_groups": "lats,biceps,rear delts",
            "equipment": "pull-up bar",
            "difficulty": "hard", 
            "instructions": "Hang from bar, pull body up until chin clears bar, lower with control."
        },
        {
            "name": "Deadlifts",
            "muscle_groups": "lower back,glutes,hamstrings,traps",
            "equipment": "barbell",
            "difficulty": "hard",
            "instructions": "Stand with bar over feet, hinge at hips, keep back straight, drive through heels."
        }
    ]
    
    stats = {
        "exercises_migrated": 0,
        "muscle_groups_created": 0,
        "relationships_created": 0,
        "errors": 0
    }
    
    # Get muscle groups mapping
    muscle_groups_map = {mg.name: mg for mg in db.query(MuscleGroup).all()}
    
    for old_exercise_data in OLD_EXERCISE_DATA:
        try:
            # Parse muscle groups
            muscle_group_names = parse_muscle_groups(old_exercise_data["muscle_groups"])
            muscle_group_objects = []
            
            for name in muscle_group_names:
                if name in muscle_groups_map:
                    muscle_group_objects.append(muscle_groups_map[name])
                else:
                    print(f"⚠️  Muscle group '{name}' not found in database")
            
            # Parse equipment
            primary_equipment = parse_equipment(old_exercise_data["equipment"])
            
            # Parse difficulty
            difficulty_map = {
                "easy": Difficulty.EASY,
                "medium": Difficulty.MEDIUM,
                "hard": Difficulty.HARD
            }
            difficulty = difficulty_map.get(old_exercise_data["difficulty"], Difficulty.MEDIUM)
            
            # Check if exercise already exists
            existing = db.query(Exercise).filter(Exercise.name == old_exercise_data["name"]).first()
            if existing:
                print(f"⚠️  Exercise '{old_exercise_data['name']}' already exists - skipping")
                continue
            
            # Create new exercise
            new_exercise = Exercise(
                name=old_exercise_data["name"],
                primary_equipment=primary_equipment,
                difficulty=difficulty,
                instructions=old_exercise_data["instructions"],
                muscle_groups=muscle_group_objects
            )
            
            db.add(new_exercise)
            db.commit()
            
            stats["exercises_migrated"] += 1
            stats["relationships_created"] += len(muscle_group_objects)
            
            print(f"✅ Migrated: {old_exercise_data['name']}")
            
        except Exception as e:
            print(f"❌ Error migrating {old_exercise_data['name']}: {e}")
            stats["errors"] += 1
            db.rollback()
    
    return stats


def validate_migration(db: Session):
    """Validate the migration results"""
    print("\n🔍 Validating migration...")
    
    # Check exercise count
    exercise_count = db.query(Exercise).count()
    print(f"✅ Total exercises: {exercise_count}")
    
    # Check muscle group relationships
    exercises_with_groups = db.query(Exercise).join(Exercise.muscle_groups).distinct().count()
    print(f"✅ Exercises with muscle groups: {exercises_with_groups}")
    
    # Check equipment distribution
    equipment_counts = db.query(Exercise.primary_equipment, db.func.count(Exercise.id)).group_by(
        Exercise.primary_equipment
    ).all()
    
    print("✅ Equipment distribution:")
    for equipment, count in equipment_counts:
        print(f"   • {equipment.value}: {count}")
    
    # Sample some exercises to verify
    print("\n📋 Sample migrated exercises:")
    sample_exercises = db.query(Exercise).limit(3).all()
    for exercise in sample_exercises:
        muscle_names = [mg.name for mg in exercise.muscle_groups]
        print(f"   • {exercise.name} ({exercise.primary_equipment.value}) - {', '.join(muscle_names)}")


def main():
    """Main migration function"""
    print("🔄 EXERCISE MODEL MIGRATION SCRIPT")
    print("=" * 50)
    
    db = next(get_database())
    
    try:
        # Ensure new tables exist
        print("Creating new database tables...")
        create_tables()
        
        # Check if muscle groups exist
        muscle_group_count = db.query(MuscleGroup).count()
        if muscle_group_count == 0:
            print("❌ No muscle groups found. Please run seed_data_v2.py first to populate muscle groups.")
            return
        
        print(f"✅ Found {muscle_group_count} muscle groups")
        
        # Run migration
        stats = migrate_exercises(db)
        
        # Validate results
        validate_migration(db)
        
        # Print summary
        print(f"\n📊 MIGRATION SUMMARY:")
        print(f"   • Exercises migrated: {stats['exercises_migrated']}")
        print(f"   • Relationships created: {stats['relationships_created']}")
        print(f"   • Errors: {stats['errors']}")
        
        if stats['errors'] == 0:
            print("\n🎉 Migration completed successfully!")
        else:
            print(f"\n⚠️  Migration completed with {stats['errors']} errors.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()