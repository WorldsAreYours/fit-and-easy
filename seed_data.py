"""
Seed data script for populating the exercise database.
Contains 25+ exercises covering all major muscle groups with proper form instructions.
Run this script after setting up the database to populate initial exercise data.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models import Exercise, Difficulty


# Comprehensive exercise database covering all major muscle groups
EXERCISE_DATA = [
    # Chest Exercises
    {
        "name": "Push-ups",
        "muscle_groups": "chest,shoulders,triceps",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Start in plank position. Lower your body until chest nearly touches the floor. Push back up to starting position. Keep your core tight and maintain straight line from head to heels."
    },
    {
        "name": "Bench Press",
        "muscle_groups": "chest,shoulders,triceps",
        "equipment": "barbell,bench",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Lie on bench with feet flat on floor. Grip barbell with hands slightly wider than shoulders. Lower bar to chest, then press back up. Keep shoulder blades pulled back throughout movement."
    },
    {
        "name": "Dumbbell Flyes",
        "muscle_groups": "chest",
        "equipment": "dumbbells,bench",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Lie on bench holding dumbbells above chest. Lower weights in wide arc until you feel stretch in chest. Bring dumbbells back together above chest. Keep slight bend in elbows throughout."
    },
    
    # Back Exercises
    {
        "name": "Pull-ups",
        "muscle_groups": "back,biceps",
        "equipment": "pull-up bar",
        "difficulty": Difficulty.HARD,
        "instructions": "Hang from bar with hands shoulder-width apart. Pull your body up until chin clears the bar. Lower with control. Engage core and avoid swinging."
    },
    {
        "name": "Bent-over Rows",
        "muscle_groups": "back,biceps",
        "equipment": "barbell",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Hinge at hips, keep back straight. Pull barbell to lower chest/upper abdomen. Squeeze shoulder blades together. Lower with control. Keep core engaged throughout."
    },
    {
        "name": "Lat Pulldowns",
        "muscle_groups": "back,biceps",
        "equipment": "cable machine",
        "difficulty": Difficulty.EASY,
        "instructions": "Sit at lat pulldown machine. Grip bar wider than shoulders. Pull bar down to upper chest while leaning slightly back. Focus on squeezing shoulder blades together."
    },
    {
        "name": "Deadlifts",
        "muscle_groups": "back,glutes,hamstrings",
        "equipment": "barbell",
        "difficulty": Difficulty.HARD,
        "instructions": "Stand with feet hip-width apart, barbell over mid-foot. Hinge at hips, grab bar. Drive through heels to stand up straight. Keep back neutral and chest up throughout movement."
    },
    
    # Leg Exercises
    {
        "name": "Squats",
        "muscle_groups": "legs,glutes",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Stand with feet shoulder-width apart. Lower hips back and down as if sitting in chair. Go down until thighs parallel to floor. Drive through heels to return to standing."
    },
    {
        "name": "Barbell Back Squats",
        "muscle_groups": "legs,glutes",
        "equipment": "barbell,squat rack",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Position barbell on upper back. Stand with feet shoulder-width apart. Squat down keeping chest up and knees tracking over toes. Drive through heels to stand up."
    },
    {
        "name": "Lunges",
        "muscle_groups": "legs,glutes",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Step forward into lunge position. Lower back knee toward ground. Both knees should be at 90 degrees. Push off front foot to return to starting position. Alternate legs."
    },
    {
        "name": "Romanian Deadlifts",
        "muscle_groups": "hamstrings,glutes",
        "equipment": "dumbbells",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Hold dumbbells in front of thighs. Hinge at hips, pushing hips back. Lower weights while keeping legs relatively straight. Feel stretch in hamstrings, then return to standing."
    },
    {
        "name": "Calf Raises",
        "muscle_groups": "calves",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Stand tall with feet hip-width apart. Raise up onto toes as high as possible. Hold briefly, then lower slowly. Can be done on step for greater range of motion."
    },
    
    # Shoulder Exercises
    {
        "name": "Overhead Press",
        "muscle_groups": "shoulders,triceps",
        "equipment": "dumbbells",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Stand with dumbbells at shoulder level. Press weights straight overhead until arms are fully extended. Lower with control back to shoulder level. Keep core tight throughout."
    },
    {
        "name": "Lateral Raises",
        "muscle_groups": "shoulders",
        "equipment": "dumbbells",
        "difficulty": Difficulty.EASY,
        "instructions": "Hold dumbbells at sides. Raise arms out to sides until parallel to floor. Focus on leading with pinkies. Lower slowly. Keep slight bend in elbows throughout movement."
    },
    {
        "name": "Pike Push-ups",
        "muscle_groups": "shoulders,triceps",
        "equipment": "bodyweight",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Start in downward dog position. Lower head toward ground by bending elbows. Push back up to starting position. Keep hips high throughout movement."
    },
    
    # Arm Exercises
    {
        "name": "Bicep Curls",
        "muscle_groups": "biceps",
        "equipment": "dumbbells",
        "difficulty": Difficulty.EASY,
        "instructions": "Hold dumbbells at sides with palms facing forward. Curl weights up by flexing biceps. Keep elbows at sides. Lower slowly to starting position."
    },
    {
        "name": "Tricep Dips",
        "muscle_groups": "triceps",
        "equipment": "bodyweight,chair",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Sit on edge of chair, hands gripping edge. Slide forward off chair. Lower body by bending elbows. Push back up to starting position. Keep elbows close to body."
    },
    {
        "name": "Hammer Curls",
        "muscle_groups": "biceps,forearms",
        "equipment": "dumbbells",
        "difficulty": Difficulty.EASY,
        "instructions": "Hold dumbbells with neutral grip (palms facing each other). Curl weights up keeping wrists straight. Focus on squeezing biceps at top. Lower slowly."
    },
    {
        "name": "Close-grip Push-ups",
        "muscle_groups": "triceps,chest",
        "equipment": "bodyweight",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Start in push-up position with hands close together forming triangle. Lower body keeping elbows close to sides. Push back up focusing on tricep engagement."
    },
    
    # Core Exercises
    {
        "name": "Plank",
        "muscle_groups": "core",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Start in push-up position on forearms. Keep body in straight line from head to heels. Engage core and hold position. Breathe normally throughout hold."
    },
    {
        "name": "Crunches",
        "muscle_groups": "core",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Lie on back with knees bent, hands behind head. Lift shoulders off ground by contracting abs. Keep lower back pressed to floor. Lower slowly."
    },
    {
        "name": "Russian Twists",
        "muscle_groups": "core,obliques",
        "equipment": "bodyweight",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Sit with knees bent, lean back slightly. Lift feet off ground if possible. Rotate torso side to side, touching ground beside hips. Keep chest up throughout."
    },
    {
        "name": "Mountain Climbers",
        "muscle_groups": "core,cardio",
        "equipment": "bodyweight",
        "difficulty": Difficulty.MEDIUM,
        "instructions": "Start in plank position. Alternate bringing knees toward chest in running motion. Keep hips level and core engaged. Maintain fast pace for cardio benefit."
    },
    {
        "name": "Dead Bug",
        "muscle_groups": "core",
        "equipment": "bodyweight",
        "difficulty": Difficulty.EASY,
        "instructions": "Lie on back with arms up and knees bent at 90 degrees. Lower opposite arm and leg slowly. Return to start and repeat other side. Keep lower back pressed to floor."
    },
    
    # Full Body/Compound Exercises
    {
        "name": "Burpees",
        "muscle_groups": "full body,cardio",
        "equipment": "bodyweight",
        "difficulty": Difficulty.HARD,
        "instructions": "Start standing. Drop into squat, place hands on ground. Jump feet back to plank. Do push-up. Jump feet to squat. Jump up with arms overhead. Repeat quickly."
    },
    {
        "name": "Thrusters",
        "muscle_groups": "legs,shoulders,core",
        "equipment": "dumbbells",
        "difficulty": Difficulty.HARD,
        "instructions": "Hold dumbbells at shoulder level. Squat down keeping chest up. Drive up explosively while pressing weights overhead. Lower weights and repeat."
    },
    {
        "name": "Turkish Get-ups",
        "muscle_groups": "full body,core",
        "equipment": "kettlebell",
        "difficulty": Difficulty.HARD,
        "instructions": "Lie on back holding weight overhead. Follow specific sequence to stand up while keeping weight overhead. Reverse sequence to return to lying position. Complex movement requiring practice."
    }
]


def seed_exercises():
    """
    Populate the database with initial exercise data.
    This function will add all exercises if they don't already exist.
    """
    session = SessionLocal()
    try:
        # Check if exercises already exist
        existing_exercises = session.query(Exercise).all()
        
        if existing_exercises:
            print(f"Database already contains {len(existing_exercises)} exercises. Skipping seed.")
            return
        
        # Add all exercises
        exercises_added = 0
        for exercise_data in EXERCISE_DATA:
            exercise = Exercise(**exercise_data)
            session.add(exercise)
            exercises_added += 1
        
        session.commit()
        print(f"Successfully added {exercises_added} exercises to the database!")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding exercises: {e}")
        raise
    finally:
        session.close()


def main():
    """Main function to set up database and seed data"""
    print("Creating database tables...")
    create_tables()
    
    print("Seeding exercise data...")
    seed_exercises()
    
    print("Database setup complete!")


if __name__ == "__main__":
    main()