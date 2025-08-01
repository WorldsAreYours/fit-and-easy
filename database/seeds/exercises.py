"""
Exercise seed data.
"""

from typing import List, Dict, Any
from app.models.enums import Equipment, Difficulty

# Enhanced exercise data with proper categorization
EXERCISES_DATA: List[Dict[str, Any]] = [
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
    
    # Full Body Exercises
    {
        "name": "Burpees",
        "primary_equipment": Equipment.BODYWEIGHT,
        "difficulty": Difficulty.HARD,
        "muscle_groups": ["full_body", "cardio", "chest", "quads", "core"],
        "instructions": "Squat down, jump feet back to plank, do push-up, jump feet forward, jump up.",
        "tips": "Move smoothly between positions, modify by removing push-up or jump if needed."
    },
]