"""
Enumeration classes for the application.
"""

import enum


class FitnessLevel(str, enum.Enum):
    """User fitness levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Difficulty(str, enum.Enum):
    """Exercise difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Equipment(str, enum.Enum):
    """Standardized equipment types for exercises."""
    BODYWEIGHT = "bodyweight"
    DUMBBELLS = "dumbbells"
    BARBELL = "barbell"
    KETTLEBELL = "kettlebell"
    RESISTANCE_BANDS = "resistance_bands"
    CABLE_MACHINE = "cable_machine"
    SMITH_MACHINE = "smith_machine"
    LEG_PRESS = "leg_press"
    LAT_PULLDOWN = "lat_pulldown"
    ROWING_MACHINE = "rowing_machine"
    PULL_UP_BAR = "pull_up_bar"
    BENCH = "bench"
    INCLINE_BENCH = "incline_bench"
    DECLINE_BENCH = "decline_bench"
    STABILITY_BALL = "stability_ball"
    MEDICINE_BALL = "medicine_ball"
    FOAM_ROLLER = "foam_roller"
    YOGA_MAT = "yoga_mat"
    CARDIO_MACHINE = "cardio_machine"