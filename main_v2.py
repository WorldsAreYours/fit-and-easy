"""
Enhanced FastAPI Personal Trainer App Backend
Features improved exercise data model with proper normalization and advanced filtering.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional, Set
from datetime import datetime
import random

from database_v2 import get_database, create_tables
from models_v2 import (
    User, Exercise, Workout, WorkoutExercise, MuscleGroup, 
    FitnessLevel, Difficulty, Equipment
)
from pydantic import BaseModel


# Enhanced Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    fitness_level: FitnessLevel = FitnessLevel.BEGINNER
    goals: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    fitness_level: FitnessLevel
    goals: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class MuscleGroupResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]

    class Config:
        orm_mode = True


class ExerciseCreate(BaseModel):
    name: str
    primary_equipment: Equipment
    secondary_equipment: Optional[Equipment] = None
    difficulty: Difficulty = Difficulty.MEDIUM
    instructions: str
    tips: Optional[str] = None
    muscle_group_ids: List[int]  # List of muscle group IDs


class ExerciseResponse(BaseModel):
    id: int
    name: str
    primary_equipment: Equipment
    secondary_equipment: Optional[Equipment]
    difficulty: Difficulty
    instructions: str
    tips: Optional[str]
    muscle_groups: List[MuscleGroupResponse]
    created_at: datetime

    class Config:
        orm_mode = True


class ExerciseSearchFilters(BaseModel):
    """Advanced search filters for exercises"""
    muscle_groups: Optional[List[str]] = None  # Muscle group names
    equipment: Optional[List[Equipment]] = None  # Equipment types
    difficulty: Optional[List[Difficulty]] = None  # Difficulty levels
    muscle_categories: Optional[List[str]] = None  # Muscle categories (upper_body, lower_body, etc.)
    require_all_muscle_groups: bool = False  # AND vs OR for muscle groups


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
    order: int = 1


class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    sets: int
    reps: int
    weight: Optional[float]
    rest_time: int
    order: int
    exercise: ExerciseResponse

    class Config:
        orm_mode = True


class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    name: str
    date: datetime
    notes: Optional[str]
    created_at: datetime
    workout_exercises: List[WorkoutExerciseResponse] = []

    class Config:
        orm_mode = True


class GeneratedWorkout(BaseModel):
    """Response model for generated workouts"""
    name: str
    exercises: List[ExerciseResponse]
    estimated_duration: int  # minutes
    target_muscle_groups: List[str]
    difficulty_level: str


# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Personal Trainer API",
    description="Fitness app backend with advanced exercise filtering and muscle group management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    create_tables()


# Health check endpoint
@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


# User endpoints (unchanged from v1)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_database)
):
    """Create a new user profile"""
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


# Enhanced muscle group endpoints
@app.get("/muscle-groups", response_model=List[MuscleGroupResponse])
def list_muscle_groups(
    category: Optional[str] = Query(None, description="Filter by category (upper_body, lower_body, core, etc.)"),
    db: Session = Depends(get_database)
):
    """List all muscle groups, optionally filtered by category"""
    query = db.query(MuscleGroup)
    
    if category:
        query = query.filter(MuscleGroup.category == category)
    
    muscle_groups = query.order_by(MuscleGroup.category, MuscleGroup.name).all()
    return muscle_groups


@app.get("/muscle-groups/categories")
def list_muscle_categories(db: Session = Depends(get_database)):
    """Get all unique muscle group categories"""
    categories = db.query(MuscleGroup.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}


# Enhanced exercise endpoints
@app.post("/exercises", response_model=ExerciseResponse, status_code=201)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_database)
):
    """Create a new exercise with muscle group relationships"""
    # Verify muscle groups exist
    muscle_groups = db.query(MuscleGroup).filter(MuscleGroup.id.in_(exercise.muscle_group_ids)).all()
    if len(muscle_groups) != len(exercise.muscle_group_ids):
        raise HTTPException(status_code=400, detail="One or more muscle group IDs are invalid")
    
    # Create exercise (exclude muscle_group_ids from dict)
    exercise_data = exercise.dict()
    muscle_group_ids = exercise_data.pop("muscle_group_ids")
    
    db_exercise = Exercise(**exercise_data)
    db_exercise.muscle_groups = muscle_groups
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@app.get("/exercises", response_model=List[ExerciseResponse])
def list_exercises(
    muscle_groups: Optional[List[str]] = Query(None, description="Filter by muscle group names"),
    equipment: Optional[List[Equipment]] = Query(None, description="Filter by equipment types"),
    difficulty: Optional[List[Difficulty]] = Query(None, description="Filter by difficulty levels"),
    muscle_categories: Optional[List[str]] = Query(None, description="Filter by muscle categories"),
    require_all_muscle_groups: bool = Query(False, description="Require ALL muscle groups (AND) vs ANY (OR)"),
    limit: int = Query(50, description="Maximum number of exercises to return", le=100),
    db: Session = Depends(get_database)
):
    """List exercises with advanced filtering capabilities"""
    
    # Start with base query, eager load muscle groups
    query = db.query(Exercise).options(joinedload(Exercise.muscle_groups))
    
    # Apply equipment filter
    if equipment:
        equipment_conditions = [Exercise.primary_equipment.in_(equipment)]
        # Also check secondary equipment
        equipment_conditions.append(Exercise.secondary_equipment.in_(equipment))
        query = query.filter(or_(*equipment_conditions))
    
    # Apply difficulty filter
    if difficulty:
        query = query.filter(Exercise.difficulty.in_(difficulty))
    
    # Apply muscle group filters
    if muscle_groups or muscle_categories:
        # Join with muscle groups for filtering
        query = query.join(Exercise.muscle_groups)
        
        conditions = []
        
        if muscle_groups:
            conditions.append(MuscleGroup.name.in_(muscle_groups))
        
        if muscle_categories:
            conditions.append(MuscleGroup.category.in_(muscle_categories))
        
        if conditions:
            if require_all_muscle_groups:
                # For AND logic, we need to count matching muscle groups
                query = query.filter(or_(*conditions))
                if muscle_groups:
                    # Group by exercise and count matching muscle groups
                    query = query.group_by(Exercise.id).having(
                        db.func.count(MuscleGroup.id) >= len(muscle_groups)
                    )
            else:
                # For OR logic, any matching muscle group is fine
                query = query.filter(or_(*conditions))
    
    # Apply limit and get results
    exercises = query.distinct().limit(limit).all()
    return exercises


@app.get("/exercises/search", response_model=List[ExerciseResponse])
def search_exercises(
    q: str = Query(..., description="Search term for exercise name or instructions"),
    db: Session = Depends(get_database)
):
    """Search exercises by name or instructions"""
    query = db.query(Exercise).options(joinedload(Exercise.muscle_groups))
    
    # Search in name and instructions
    search_filter = or_(
        Exercise.name.ilike(f"%{q}%"),
        Exercise.instructions.ilike(f"%{q}%"),
        Exercise.tips.ilike(f"%{q}%")
    )
    
    exercises = query.filter(search_filter).limit(20).all()
    return exercises


@app.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_database)
):
    """Get detailed exercise information"""
    exercise = db.query(Exercise).options(joinedload(Exercise.muscle_groups)).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


# Equipment endpoint
@app.get("/equipment")
def list_equipment():
    """Get all available equipment types"""
    return {"equipment": [eq.value for eq in Equipment]}


# Enhanced workout generation
@app.post("/users/{user_id}/generate-workout", response_model=GeneratedWorkout)
def generate_workout(
    user_id: int,
    target_muscle_groups: Optional[List[str]] = Query(None, description="Target specific muscle groups"),
    workout_type: str = Query("balanced", description="Workout type: balanced, upper_body, lower_body, cardio"),
    duration_minutes: int = Query(45, description="Target workout duration in minutes", ge=15, le=120),
    available_equipment: Optional[List[Equipment]] = Query(None, description="Available equipment"),
    db: Session = Depends(get_database)
):
    """Generate a personalized workout with enhanced muscle group targeting"""
    
    # Get user to determine fitness level
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build exercise query
    query = db.query(Exercise).options(joinedload(Exercise.muscle_groups))
    
    # Filter by available equipment
    if available_equipment:
        equipment_conditions = [Exercise.primary_equipment.in_(available_equipment)]
        equipment_conditions.append(Exercise.secondary_equipment.in_(available_equipment))
        equipment_conditions.append(Exercise.secondary_equipment.is_(None))  # Include bodyweight
        query = query.filter(or_(*equipment_conditions))
    
    # Filter by workout type and target muscle groups
    if workout_type != "balanced":
        if workout_type == "upper_body":
            target_categories = ["upper_body"]
        elif workout_type == "lower_body":
            target_categories = ["lower_body"]
        elif workout_type == "core":
            target_categories = ["core"]
        elif workout_type == "cardio":
            target_categories = ["cardio", "full_body"]
        else:
            target_categories = ["upper_body", "lower_body", "core"]
        
        query = query.join(Exercise.muscle_groups).filter(
            MuscleGroup.category.in_(target_categories)
        )
    
    if target_muscle_groups:
        query = query.join(Exercise.muscle_groups).filter(
            MuscleGroup.name.in_(target_muscle_groups)
        )
    
    # Adjust difficulty based on user fitness level
    if user.fitness_level == FitnessLevel.BEGINNER:
        difficulty_filter = [Difficulty.EASY, Difficulty.MEDIUM]
    elif user.fitness_level == FitnessLevel.INTERMEDIATE:
        difficulty_filter = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
    else:  # ADVANCED
        difficulty_filter = [Difficulty.MEDIUM, Difficulty.HARD]
    
    query = query.filter(Exercise.difficulty.in_(difficulty_filter))
    
    # Get exercises and select a balanced set
    available_exercises = query.distinct().all()
    
    if not available_exercises:
        raise HTTPException(status_code=404, detail="No exercises found matching the criteria")
    
    # Calculate number of exercises based on duration
    exercises_count = min(max(duration_minutes // 8, 3), len(available_exercises), 8)
    
    # Select diverse exercises
    selected_exercises = random.sample(available_exercises, exercises_count)
    
    # Get target muscle groups from selected exercises
    target_groups = set()
    for exercise in selected_exercises:
        target_groups.update([mg.name for mg in exercise.muscle_groups])
    
    # Estimate duration (8 minutes per exercise on average)
    estimated_duration = len(selected_exercises) * 8
    
    return GeneratedWorkout(
        name=f"{workout_type.replace('_', ' ').title()} Workout",
        exercises=selected_exercises,
        estimated_duration=estimated_duration,
        target_muscle_groups=list(target_groups),
        difficulty_level=user.fitness_level.value
    )


# Workout endpoints (similar to v1 but with enhanced queries)
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
    
    # Set date to now if not provided
    if not workout.date:
        workout.date = datetime.now()
    
    db_workout = Workout(user_id=user_id, **workout.dict())
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
    """Add an exercise to a workout with specific parameters"""
    # Verify workout and exercise exist
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    exercise = db.query(Exercise).filter(Exercise.id == workout_exercise.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db_workout_exercise = WorkoutExercise(workout_id=workout_id, **workout_exercise.dict())
    db.add(db_workout_exercise)
    db.commit()
    db.refresh(db_workout_exercise)
    return db_workout_exercise


@app.get("/workouts/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_database)
):
    """Get workout details with all exercises"""
    workout = db.query(Workout).options(
        joinedload(Workout.workout_exercises).joinedload(WorkoutExercise.exercise).joinedload(Exercise.muscle_groups)
    ).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    return workout


@app.get("/users/{user_id}/workouts", response_model=List[WorkoutResponse])
def get_user_workouts(
    user_id: int,
    limit: int = Query(10, description="Number of workouts to return", le=50),
    db: Session = Depends(get_database)
):
    """Get user's workout history"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    workouts = db.query(Workout).options(
        joinedload(Workout.workout_exercises).joinedload(WorkoutExercise.exercise).joinedload(Exercise.muscle_groups)
    ).filter(Workout.user_id == user_id).order_by(Workout.date.desc()).limit(limit).all()
    
    return workouts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)