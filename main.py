"""
FastAPI Personal Trainer App Backend
Provides endpoints for user management, exercise library, and workout tracking.
Designed to be easily extensible with AI features in the future.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random

from database import get_database, create_tables
from models import User, Exercise, Workout, WorkoutExercise, FitnessLevel, Difficulty
from pydantic import BaseModel


# Pydantic models for request/response validation
class UserCreate(BaseModel):
    name: str
    email: str  # Changed from EmailStr to str for compatibility
    fitness_level: FitnessLevel = FitnessLevel.BEGINNER
    goals: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    fitness_level: str
    goals: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseCreate(BaseModel):
    name: str
    muscle_groups: str  # Comma-separated
    equipment: str
    difficulty: Difficulty = Difficulty.MEDIUM
    instructions: str


class ExerciseResponse(BaseModel):
    id: int
    name: str
    muscle_groups: str
    equipment: str
    difficulty: str
    instructions: str

    class Config:
        from_attributes = True


class WorkoutCreate(BaseModel):
    name: str
    date: Optional[datetime] = None
    notes: Optional[str] = None


class WorkoutExerciseCreate(BaseModel):
    exercise_id: int
    sets: int = 3
    reps: int = 10
    weight: Optional[float] = None
    rest_time: int = 60


class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    sets: int
    reps: int
    weight: Optional[float]
    rest_time: int
    exercise: ExerciseResponse

    class Config:
        from_attributes = True


class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    name: str
    date: datetime
    notes: Optional[str]
    created_at: datetime
    workout_exercises: List[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True


class GeneratedWorkout(BaseModel):
    """Response model for generated workouts"""
    workout_name: str
    exercises: List[WorkoutExerciseCreate]
    estimated_duration: int  # in minutes


# Initialize FastAPI app
app = FastAPI(
    title="Personal Trainer App API",
    description="Backend API for a personal trainer application with exercise library and workout tracking",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    create_tables()


# User endpoints
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_database)
):
    """Create a new user profile"""
    # Check if user with email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_database)
):
    """Get user profile by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Exercise endpoints
@app.post("/exercises", response_model=ExerciseResponse, status_code=201)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_database)
):
    """Create a new exercise"""
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@app.get("/exercises", response_model=List[ExerciseResponse])
def list_exercises(
    muscle_group: Optional[str] = Query(None, description="Filter by muscle group"),
    equipment: Optional[str] = Query(None, description="Filter by equipment"),
    difficulty: Optional[Difficulty] = Query(None, description="Filter by difficulty"),
    db: Session = Depends(get_database)
):
    """List exercises with optional filters"""
    query = db.query(Exercise)
    
    # Apply filters
    if muscle_group:
        query = query.filter(Exercise.muscle_groups.contains(muscle_group))
    if equipment:
        query = query.filter(Exercise.equipment.contains(equipment))
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    
    exercises = query.all()
    return exercises


# Workout endpoints
@app.post("/workouts", response_model=WorkoutResponse, status_code=201)
def create_workout(
    user_id: int,
    workout: WorkoutCreate,
    db: Session = Depends(get_database)
):
    """Create a new workout for a user"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    workout_data = workout.dict()
    workout_data["user_id"] = user_id
    if workout_data["date"] is None:
        workout_data["date"] = datetime.utcnow()
    
    db_workout = Workout(**workout_data)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@app.post("/workouts/{workout_id}/exercises", response_model=WorkoutExerciseResponse, status_code=201)
def add_exercise_to_workout(
    workout_id: int,
    workout_exercise: WorkoutExerciseCreate,
    db: Session = Depends(get_database)
):
    """Add an exercise to a workout"""
    # Verify workout exists
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Verify exercise exists
    exercise = db.query(Exercise).filter(Exercise.id == workout_exercise.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    workout_exercise_data = workout_exercise.dict()
    workout_exercise_data["workout_id"] = workout_id
    
    db_workout_exercise = WorkoutExercise(**workout_exercise_data)
    db.add(db_workout_exercise)
    db.commit()
    db.refresh(db_workout_exercise)
    
    # Load the exercise relationship for response
    workout_exercise_with_exercise = db.query(WorkoutExercise).filter(
        WorkoutExercise.id == db_workout_exercise.id
    ).join(Exercise).first()
    
    return workout_exercise_with_exercise


@app.get("/workouts/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_database)
):
    """Get workout details with exercises"""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    return workout


@app.get("/users/{user_id}/workouts", response_model=List[WorkoutResponse])
def get_user_workouts(
    user_id: int,
    db: Session = Depends(get_database)
):
    """Get all workouts for a user"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    workouts = db.query(Workout).filter(
        Workout.user_id == user_id
    ).order_by(Workout.date.desc()).all()
    return workouts


@app.post("/users/{user_id}/generate-workout", response_model=GeneratedWorkout)
def generate_workout(
    user_id: int,
    db: Session = Depends(get_database)
):
    """
    Generate a simple workout based on user's fitness level and goals.
    This is a basic implementation that can be enhanced with AI later.
    """
    # Verify user exists and get their profile
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all exercises
    all_exercises = db.query(Exercise).all()
    
    if not all_exercises:
        raise HTTPException(status_code=400, detail="No exercises available for workout generation")
    
    # Simple workout generation logic
    # This can be enhanced with AI/ML algorithms later
    
    # Filter exercises based on user's fitness level
    difficulty_mapping = {
        FitnessLevel.BEGINNER: [Difficulty.EASY, Difficulty.MEDIUM],
        FitnessLevel.INTERMEDIATE: [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD],
        FitnessLevel.ADVANCED: [Difficulty.MEDIUM, Difficulty.HARD]
    }
    
    suitable_exercises = [
        ex for ex in all_exercises 
        if ex.difficulty in difficulty_mapping.get(user.fitness_level, [Difficulty.MEDIUM])
    ]
    
    # Ensure we have a balanced workout with different muscle groups
    muscle_groups = ["chest", "back", "legs", "shoulders", "arms", "core"]
    selected_exercises = []
    
    # Try to get at least one exercise per major muscle group
    for muscle_group in muscle_groups:
        muscle_exercises = [
            ex for ex in suitable_exercises 
            if muscle_group in ex.muscle_groups.lower()
        ]
        if muscle_exercises:
            selected_exercises.append(random.choice(muscle_exercises))
    
    # If we don't have enough exercises, add more randomly
    while len(selected_exercises) < min(8, len(suitable_exercises)):
        remaining_exercises = [ex for ex in suitable_exercises if ex not in selected_exercises]
        if not remaining_exercises:
            break
        selected_exercises.append(random.choice(remaining_exercises))
    
    # Limit to 5-8 exercises
    selected_exercises = selected_exercises[:8]
    
    # Generate workout exercise parameters based on fitness level
    rep_ranges = {
        FitnessLevel.BEGINNER: (8, 12),
        FitnessLevel.INTERMEDIATE: (8, 15),
        FitnessLevel.ADVANCED: (6, 12)
    }
    
    set_counts = {
        FitnessLevel.BEGINNER: (2, 3),
        FitnessLevel.INTERMEDIATE: (3, 4),
        FitnessLevel.ADVANCED: (3, 5)
    }
    
    workout_exercises = []
    for exercise in selected_exercises:
        min_reps, max_reps = rep_ranges[user.fitness_level]
        min_sets, max_sets = set_counts[user.fitness_level]
        
        workout_exercise = WorkoutExerciseCreate(
            exercise_id=exercise.id,
            sets=random.randint(min_sets, max_sets),
            reps=random.randint(min_reps, max_reps),
            rest_time=random.randint(45, 90)  # 45-90 seconds rest
        )
        workout_exercises.append(workout_exercise)
    
    # Estimate workout duration (rough calculation)
    estimated_duration = sum(
        (we.sets * (we.reps * 3 + we.rest_time)) // 60  # 3 seconds per rep + rest time
        for we in workout_exercises
    )
    
    return GeneratedWorkout(
        workout_name=f"Generated Workout - {datetime.now().strftime('%Y-%m-%d')}",
        exercises=workout_exercises,
        estimated_duration=max(estimated_duration, 20)  # Minimum 20 minutes
    )


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)