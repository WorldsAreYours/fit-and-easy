#!/usr/bin/env python3
"""
Demonstration script showing the enhanced querying capabilities
of the improved exercise data model.
"""

import sys
import os
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_v2 import get_database, create_tables
from models_v2 import Exercise, MuscleGroup, Equipment, Difficulty
from seed_data_v2 import main as seed_database


def demonstrate_queries():
    """Demonstrate various advanced query capabilities"""
    print("🔍 ENHANCED EXERCISE QUERYING DEMONSTRATION")
    print("=" * 60)
    
    # Get database session
    db = next(get_database())
    
    try:
        # Query 1: Find all chest exercises
        print("\n1️⃣  CHEST EXERCISES:")
        print("-" * 30)
        chest_exercises = db.query(Exercise).join(Exercise.muscle_groups).filter(
            MuscleGroup.name == "chest"
        ).all()
        
        for exercise in chest_exercises:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} ({exercise.primary_equipment.value}) - {', '.join(muscle_names)}")
        
        # Query 2: Find exercises by equipment
        print("\n2️⃣  BODYWEIGHT EXERCISES:")
        print("-" * 30)
        bodyweight_exercises = db.query(Exercise).filter(
            Exercise.primary_equipment == Equipment.BODYWEIGHT
        ).all()
        
        for exercise in bodyweight_exercises:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} ({exercise.difficulty.value}) - {', '.join(muscle_names)}")
        
        # Query 3: Find exercises by multiple muscle groups (OR logic)
        print("\n3️⃣  CHEST OR SHOULDER EXERCISES:")
        print("-" * 35)
        chest_or_shoulder = db.query(Exercise).join(Exercise.muscle_groups).filter(
            MuscleGroup.name.in_(["chest", "shoulders", "front_delts"])
        ).distinct().all()
        
        for exercise in chest_or_shoulder:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} - {', '.join(muscle_names)}")
        
        # Query 4: Find exercises by muscle category
        print("\n4️⃣  UPPER BODY EXERCISES:")
        print("-" * 30)
        upper_body_exercises = db.query(Exercise).join(Exercise.muscle_groups).filter(
            MuscleGroup.category == "upper_body"
        ).distinct().limit(5).all()
        
        for exercise in upper_body_exercises:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} - {', '.join(muscle_names)}")
        
        # Query 5: Find exercises by difficulty and equipment
        print("\n5️⃣  EASY DUMBBELL EXERCISES:")
        print("-" * 30)
        easy_dumbbell = db.query(Exercise).filter(
            Exercise.difficulty == Difficulty.EASY,
            Exercise.primary_equipment == Equipment.DUMBBELLS
        ).all()
        
        for exercise in easy_dumbbell:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} - {', '.join(muscle_names)}")
        
        # Query 6: Complex query - chest exercises that also work triceps
        print("\n6️⃣  CHEST + TRICEPS EXERCISES:")
        print("-" * 35)
        
        # Subquery to find exercises with both chest and triceps
        chest_triceps = db.query(Exercise).join(Exercise.muscle_groups).filter(
            MuscleGroup.name == "chest"
        ).intersect(
            db.query(Exercise).join(Exercise.muscle_groups).filter(
                MuscleGroup.name == "triceps"
            )
        ).all()
        
        for exercise in chest_triceps:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} - {', '.join(muscle_names)}")
        
        # Query 7: Equipment statistics
        print("\n7️⃣  EQUIPMENT USAGE STATISTICS:")
        print("-" * 35)
        
        equipment_counts = db.query(Exercise.primary_equipment, func.count(Exercise.id)).group_by(
            Exercise.primary_equipment
        ).order_by(func.count(Exercise.id).desc()).all()
        
        for equipment, count in equipment_counts:
            print(f"   • {equipment.value.replace('_', ' ').title()}: {count} exercises")
        
        # Query 8: Muscle group coverage
        print("\n8️⃣  MUSCLE GROUP COVERAGE:")
        print("-" * 30)
        
        muscle_coverage = db.query(MuscleGroup.name, func.count(Exercise.id)).join(
            Exercise.muscle_groups
        ).group_by(MuscleGroup.name).order_by(
            func.count(Exercise.id).desc()
        ).all()
        
        for muscle, count in muscle_coverage:
            print(f"   • {muscle.replace('_', ' ').title()}: {count} exercises")
        
        # Query 9: Find exercises suitable for home workout (bodyweight + dumbbells)
        print("\n9️⃣  HOME WORKOUT SUITABLE EXERCISES:")
        print("-" * 40)
        
        home_equipment = [Equipment.BODYWEIGHT, Equipment.DUMBBELLS]
        home_exercises = db.query(Exercise).filter(
            Exercise.primary_equipment.in_(home_equipment)
        ).limit(8).all()
        
        for exercise in home_exercises:
            muscle_names = [mg.name for mg in exercise.muscle_groups]
            print(f"   • {exercise.name} ({exercise.primary_equipment.value}) - {', '.join(muscle_names)}")
        
        # Query 10: Difficulty distribution
        print("\n🔟 DIFFICULTY DISTRIBUTION:")
        print("-" * 30)
        
        difficulty_counts = db.query(Exercise.difficulty, func.count(Exercise.id)).group_by(
            Exercise.difficulty
        ).all()
        
        total_exercises = sum(count for _, count in difficulty_counts)
        for difficulty, count in difficulty_counts:
            percentage = (count / total_exercises) * 100
            print(f"   • {difficulty.value.title()}: {count} exercises ({percentage:.1f}%)")
        
        print(f"\n📊 SUMMARY:")
        print(f"   • Total Exercises: {total_exercises}")
        print(f"   • Total Muscle Groups: {db.query(MuscleGroup).count()}")
        print(f"   • Equipment Types: {len(Equipment)}")
        
    finally:
        db.close()


def demonstrate_api_filtering():
    """Show examples of how the new API filtering would work"""
    print("\n🌐 API FILTERING EXAMPLES")
    print("=" * 40)
    
    examples = [
        {
            "description": "Find chest exercises using dumbbells",
            "endpoint": "GET /exercises",
            "params": "?muscle_groups=chest&equipment=dumbbells"
        },
        {
            "description": "Find all upper body exercises",
            "endpoint": "GET /exercises", 
            "params": "?muscle_categories=upper_body"
        },
        {
            "description": "Find easy bodyweight exercises",
            "endpoint": "GET /exercises",
            "params": "?equipment=bodyweight&difficulty=easy"
        },
        {
            "description": "Find exercises targeting chest AND triceps",
            "endpoint": "GET /exercises",
            "params": "?muscle_groups=chest,triceps&require_all_muscle_groups=true"
        },
        {
            "description": "Search exercises by name",
            "endpoint": "GET /exercises/search",
            "params": "?q=push"
        },
        {
            "description": "Get muscle groups by category",
            "endpoint": "GET /muscle-groups",
            "params": "?category=upper_body"
        },
        {
            "description": "Generate upper body workout",
            "endpoint": "POST /users/1/generate-workout",
            "params": "?workout_type=upper_body&available_equipment=dumbbells,bodyweight"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}️⃣  {example['description']}:")
        print(f"   {example['endpoint']}{example['params']}")


def compare_old_vs_new():
    """Compare old string-based vs new normalized approach"""
    print("\n⚖️  OLD vs NEW APPROACH COMPARISON")
    print("=" * 50)
    
    print("\n❌ OLD APPROACH (String-based):")
    print("   Exercise.muscle_groups = 'chest,triceps,front_delts'")
    print("   Exercise.equipment = 'dumbbells'")
    print("\n   Problems:")
    print("   • Hard to query specific muscle groups")
    print("   • Inconsistent equipment naming")
    print("   • No standardization")
    print("   • Difficult to do complex filters")
    print("   • No relationship management")
    
    print("\n✅ NEW APPROACH (Normalized):")
    print("   Exercise.muscle_groups = [MuscleGroup('chest'), MuscleGroup('triceps')]")
    print("   Exercise.primary_equipment = Equipment.DUMBBELLS")
    print("\n   Benefits:")
    print("   • Efficient database queries")
    print("   • Standardized equipment types")
    print("   • Proper relationships")
    print("   • Advanced filtering capabilities") 
    print("   • Better data integrity")
    print("   • Easier to extend")


def main():
    """Main demonstration function"""
    print("🏋️‍♂️ PERSONAL TRAINER APP - ENHANCED EXERCISE MODEL DEMO")
    print("=" * 70)
    
    # Ensure database is set up
    print("Setting up enhanced database...")
    seed_database()
    
    # Run demonstrations
    demonstrate_queries()
    demonstrate_api_filtering() 
    compare_old_vs_new()
    
    print("\n" + "=" * 70)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("\nThe enhanced model provides much more powerful and flexible")
    print("exercise querying capabilities for your personal trainer app!")


if __name__ == "__main__":
    main()