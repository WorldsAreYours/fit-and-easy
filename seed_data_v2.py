"""
Enhanced seed script for populating the database with standardized exercise data.
Features proper muscle group categorization and equipment standardization.
"""

from sqlalchemy.orm import Session
from database_v2 import get_database, create_tables
from models_v2 import MuscleGroup, Exercise, Equipment, Difficulty

# Standardized muscle groups with categories
MUSCLE_GROUPS_DATA = [
    # Upper Body - Chest
    {"name": "chest", "category": "upper_body", "description": "Pectoral muscles"},
    {"name": "upper_chest", "category": "upper_body", "description": "Upper portion of pectoral muscles"},
    {"name": "lower_chest", "category": "upper_body", "description": "Lower portion of pectoral muscles"},
    
    # Upper Body - Back
    {"name": "back", "category": "upper_body", "description": "General back muscles"},
    {"name": "lats", "category": "upper_body", "description": "Latissimus dorsi"},
    {"name": "rhomboids", "category": "upper_body", "description": "Rhomboid muscles"},
    {"name": "traps", "category": "upper_body", "description": "Trapezius muscles"},
    {"name": "rear_delts", "category": "upper_body", "description": "Posterior deltoids"},
    {"name": "lower_back", "category": "upper_body", "description": "Erector spinae and lower back"},
    
    # Upper Body - Shoulders
    {"name": "shoulders", "category": "upper_body", "description": "General deltoid muscles"},
    {"name": "front_delts", "category": "upper_body", "description": "Anterior deltoids"},
    {"name": "side_delts", "category": "upper_body", "description": "Lateral deltoids"},
    
    # Upper Body - Arms
    {"name": "biceps", "category": "upper_body", "description": "Bicep muscles"},
    {"name": "triceps", "category": "upper_body", "description": "Tricep muscles"},
    {"name": "forearms", "category": "upper_body", "description": "Forearm muscles"},
    
    # Lower Body
    {"name": "quads", "category": "lower_body", "description": "Quadriceps muscles"},
    {"name": "hamstrings", "category": "lower_body", "description": "Hamstring muscles"},
    {"name": "glutes", "category": "lower_body", "description": "Gluteal muscles"},
    {"name": "calves", "category": "lower_body", "description": "Calf muscles"},
    {"name": "hip_flexors", "category": "lower_body", "description": "Hip flexor muscles"},
    {"name": "adductors", "category": "lower_body", "description": "Inner thigh muscles"},
    {"name": "abductors", "category": "lower_body", "description": "Outer thigh and glute muscles"},
    
    # Core
    {"name": "abs", "category": "core", "description": "Abdominal muscles"},
    {"name": "obliques", "category": "core", "description": "Side abdominal muscles"},
    {"name": "core", "category": "core", "description": "General core stabilizers"},
    
    # Full Body
    {"name": "full_body", "category": "full_body", "description": "Multiple muscle groups"},
    {"name": "cardio", "category": "cardio", "description": "Cardiovascular system"},
]

# Enhanced exercise data with proper categorization
EXERCISES_DATA = [
    # Chest Exercises
    {
        "name": "Push-ups",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["chest", "triceps", "front_delts", "core"],
        "instructions": "Start in plank position, lower body until chest nearly touches floor, push back up.",
        "tips": "Keep core tight and body in straight line. Modify on knees if needed."
    },
    {
        "name": "Bench Press",
        "primary_equipment": Equipment.BARBELL,
        "secondary_equipment": Equipment.BENCH,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["chest", "triceps", "front_delts"],
        "instructions": "Lie on bench, grip bar wider than shoulders, lower to chest, press up.",
        "tips": "Keep feet planted, shoulder blades pulled back, controlled movement."
    },
    {
        "name": "Dumbbell Flyes",
        "primary_equipment": Equipment.DUMBBELLS,
        "secondary_equipment": Equipment.BENCH,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["chest", "front_delts"],
        "instructions": "Lie on bench, arms extended with slight bend, lower weights to sides, squeeze chest to bring weights together.",
        "tips": "Focus on stretching the chest at bottom, don't lower too far to avoid shoulder strain."
    },
    {
        "name": "Incline Dumbbell Press",
        "primary_equipment": Equipment.DUMBBELLS,
        "secondary_equipment": Equipment.INCLINE_BENCH,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["upper_chest", "front_delts", "triceps"],
        "instructions": "Lie on incline bench, press dumbbells from chest level to above shoulders.",
        "tips": "Use 30-45 degree incline, control the weight on the way down."
    },
    
    # Back Exercises
    {
        "name": "Pull-ups",
        "primary_equipment": Equipment.PULL_UP_BAR,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["lats", "rhomboids", "biceps", "rear_delts"],
        "instructions": "Hang from bar, pull body up until chin clears bar, lower with control.",
        "tips": "Engage core, avoid swinging, use assistance if needed."
    },
    {
        "name": "Bent-over Rows",
        "primary_equipment": Equipment.BARBELL,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["lats", "rhomboids", "traps", "biceps"],
        "instructions": "Hinge at hips, keep back straight, pull bar to lower chest, squeeze shoulder blades.",
        "tips": "Keep core tight, don't round the back, pull elbows back."
    },
    {
        "name": "Lat Pulldowns",
        "primary_equipment": Equipment.LAT_PULLDOWN,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["lats", "rhomboids", "biceps"],
        "instructions": "Sit at machine, pull bar down to upper chest, squeeze shoulder blades together.",
        "tips": "Lean slightly back, don't pull behind neck, control the weight up."
    },
    {
        "name": "Deadlifts",
        "primary_equipment": Equipment.BARBELL,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["lower_back", "glutes", "hamstrings", "traps", "core"],
        "instructions": "Stand with bar over feet, hinge at hips, keep back straight, drive through heels to stand.",
        "tips": "Keep bar close to body, engage core, don't round back."
    },
    
    # Leg Exercises
    {
        "name": "Squats",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["quads", "glutes", "core"],
        "instructions": "Stand with feet shoulder-width apart, lower hips back and down, drive through heels to stand.",
        "tips": "Keep chest up, knees track over toes, full range of motion."
    },
    {
        "name": "Barbell Squats",
        "primary_equipment": Equipment.BARBELL,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["quads", "glutes", "core", "hamstrings"],
        "instructions": "Bar on upper back, squat down keeping knees aligned with toes, drive up through heels.",
        "tips": "Keep core tight, chest up, don't let knees cave inward."
    },
    {
        "name": "Lunges",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["quads", "glutes", "hamstrings", "core"],
        "instructions": "Step forward, lower back knee toward ground, push off front foot to return.",
        "tips": "Keep torso upright, front knee over ankle, equal weight distribution."
    },
    {
        "name": "Romanian Deadlifts",
        "primary_equipment": Equipment.DUMBBELLS,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["hamstrings", "glutes", "lower_back"],
        "instructions": "Hold weights, hinge at hips keeping legs slightly bent, lower weights toward floor, return to standing.",
        "tips": "Feel stretch in hamstrings, keep weights close to legs, don't round back."
    },
    
    # Shoulder Exercises
    {
        "name": "Overhead Press",
        "primary_equipment": Equipment.BARBELL,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["shoulders", "triceps", "core"],
        "instructions": "Stand with bar at shoulder level, press straight up overhead, lower with control.",
        "tips": "Keep core tight, don't arch back excessively, full overhead extension."
    },
    {
        "name": "Lateral Raises",
        "primary_equipment": Equipment.DUMBBELLS,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["side_delts"],
        "instructions": "Hold weights at sides, raise arms to sides until parallel to floor, lower slowly.",
        "tips": "Slight bend in elbows, don't swing weights, control the negative."
    },
    {
        "name": "Pike Push-ups",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["shoulders", "triceps", "core"],
        "instructions": "Start in downward dog position, lower head toward ground, push back up.",
        "tips": "Keep legs straight, form inverted V shape, gradually increase range of motion."
    },
    
    # Core Exercises
    {
        "name": "Plank",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["core", "abs", "shoulders"],
        "instructions": "Hold push-up position, keep body straight from head to heels.",
        "tips": "Don't let hips sag or pike up, breathe normally, start with shorter holds."
    },
    {
        "name": "Russian Twists",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.EASY,
        "muscle_groups": ["obliques", "abs", "core"],
        "instructions": "Sit with knees bent, lean back slightly, rotate torso side to side.",
        "tips": "Keep chest up, control the movement, can add weight for progression."
    },
    {
        "name": "Mountain Climbers",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.MEDIUM,
        "muscle_groups": ["core", "abs", "shoulders", "cardio"],
        "instructions": "Start in plank, alternate bringing knees to chest quickly.",
        "tips": "Keep hips level, maintain plank position, quick but controlled movement."
    },
    
    # Full Body Exercises
    {
        "name": "Burpees",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["full_body", "cardio", "chest", "quads", "core"],
        "instructions": "Squat down, jump feet back to plank, do push-up, jump feet forward, jump up.",
        "tips": "Move smoothly between positions, modify by removing push-up or jump if needed."
    },
    {
        "name": "Thrusters",
        "primary_equipment": Equipment.DUMBBELLS,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["shoulders", "quads", "glutes", "core", "full_body"],
        "instructions": "Hold weights at shoulders, squat down, drive up and press weights overhead.",
        "tips": "Use leg drive to help press, smooth transition from squat to press."
    },
    {
        "name": "Turkish Get-ups",
        "primary_equipment": Equipment.DUMBBELLS,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["core", "shoulders", "full_body"],
        "instructions": "Lie down holding weight up, use complex movement pattern to stand up while keeping weight overhead.",
        "tips": "Start light, learn the movement pattern first, very technical exercise."
    }
]


def seed_muscle_groups(db: Session):
    """Populate the database with standardized muscle groups"""
    print("Seeding muscle groups...")
    
    # Check if muscle groups already exist
    existing_count = db.query(MuscleGroup).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} muscle groups. Skipping seed.")
        return
    
    for group_data in MUSCLE_GROUPS_DATA:
        muscle_group = MuscleGroup(**group_data)
        db.add(muscle_group)
    
    db.commit()
    print(f"✓ Added {len(MUSCLE_GROUPS_DATA)} muscle groups")


def seed_exercises(db: Session):
    """Populate the database with exercises and their muscle group relationships"""
    print("Seeding exercises...")
    
    # Check if exercises already exist
    existing_count = db.query(Exercise).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} exercises. Skipping seed.")
        return
    
    # Create a mapping of muscle group names to objects
    muscle_groups_map = {mg.name: mg for mg in db.query(MuscleGroup).all()}
    
    for exercise_data in EXERCISES_DATA:
        # Extract muscle group names and get the actual objects
        muscle_group_names = exercise_data.pop("muscle_groups")
        muscle_group_objects = [muscle_groups_map[name] for name in muscle_group_names if name in muscle_groups_map]
        
        # Create exercise
        exercise = Exercise(**exercise_data)
        exercise.muscle_groups = muscle_group_objects
        
        db.add(exercise)
    
    db.commit()
    print(f"✓ Added {len(EXERCISES_DATA)} exercises with muscle group relationships")


def main():
    """Main function to run the seeding process"""
    print("Starting enhanced database setup...")
    
    # Create tables
    create_tables()
    print("✓ Database tables created")
    
    # Get database session
    db = next(get_database())
    
    try:
        # Seed data in order (muscle groups first, then exercises)
        seed_muscle_groups(db)
        seed_exercises(db)
        
        print("\n🎉 Enhanced database setup complete!")
        print("\nSummary:")
        print(f"  • Muscle Groups: {db.query(MuscleGroup).count()}")
        print(f"  • Exercises: {db.query(Exercise).count()}")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()