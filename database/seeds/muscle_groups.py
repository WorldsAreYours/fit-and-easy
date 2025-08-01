"""
Muscle group seed data.
"""

from typing import List, Dict

# Standardized muscle groups with categories
MUSCLE_GROUPS_DATA: List[Dict[str, str]] = [
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