# Proposed Project Structure

## Current Issues
❌ **Everything in root directory**
❌ **models_v2.py has too many models** 
❌ **No logical separation of concerns**
❌ **Scripts mixed with application code**
❌ **No clear package structure**

## Proposed Structure

```
fit-and-easy/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app setup and configuration
│   ├── core/                     # Core configuration and setup
│   │   ├── __init__.py
│   │   ├── config.py             # App configuration
│   │   ├── database.py           # Database connection and setup
│   │   └── security.py           # Security utilities (future)
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model and common mixins
│   │   ├── user.py               # User model
│   │   ├── exercise.py           # Exercise and MuscleGroup models
│   │   ├── workout.py            # Workout and WorkoutExercise models
│   │   └── enums.py              # All enums (FitnessLevel, Difficulty, Equipment)
│   ├── schemas/                  # Pydantic models for API
│   │   ├── __init__.py
│   │   ├── user.py               # User request/response schemas
│   │   ├── exercise.py           # Exercise schemas
│   │   ├── workout.py            # Workout schemas
│   │   └── common.py             # Common schemas and base classes
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependencies (database session, etc.)
│   │   ├── router.py             # Main API router
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── users.py          # User endpoints
│   │       ├── exercises.py      # Exercise endpoints
│   │       ├── workouts.py       # Workout endpoints
│   │       └── muscle_groups.py  # Muscle group endpoints
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py       # User business logic
│   │   ├── exercise_service.py   # Exercise filtering and search
│   │   ├── workout_service.py    # Workout generation and management
│   │   └── recommendation_service.py  # Exercise recommendations (future)
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── database_utils.py     # Database helpers
│       ├── exercise_utils.py     # Exercise parsing and validation
│       └── filters.py            # Query filtering utilities
├── database/                     # Database related files
│   ├── __init__.py
│   ├── migrations/               # Database migrations
│   │   ├── __init__.py
│   │   └── migrate_v1_to_v2.py   # Migration from old to new structure
│   └── seeds/                    # Seed data
│       ├── __init__.py
│       ├── muscle_groups.py      # Muscle group seed data
│       └── exercises.py          # Exercise seed data
├── scripts/                      # Utility scripts
│   ├── setup_database.py         # Database setup script
│   ├── demo_queries.py           # Query demonstration
│   └── import_exercises.py       # Exercise import utilities
├── tests/                        # Test files
│   ├── __init__.py
│   ├── conftest.py               # Test configuration
│   ├── test_api/                 # API tests
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_exercises.py
│   │   └── test_workouts.py
│   ├── test_models/              # Model tests
│   │   ├── __init__.py
│   │   ├── test_user.py
│   │   └── test_exercise.py
│   └── test_services/            # Service tests
│       ├── __init__.py
│       └── test_workout_service.py
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   │   ├── openapi.json
│   │   └── openapi.yaml
│   ├── ENHANCED_MODEL_SUMMARY.md
│   └── DEVELOPMENT.md
├── config/                       # Configuration files
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── requirements/                 # Requirements files
│   ├── base.txt                  # Base requirements
│   ├── development.txt           # Development requirements
│   └── production.txt            # Production requirements
├── .env.example                  # Environment variables template
├── .gitignore
├── README.md
├── pyproject.toml               # Modern Python project config
└── Dockerfile                   # Docker configuration (future)
```

## Benefits of This Structure

### 1. **Separation of Concerns**
- **Models**: Each model in its own file
- **API**: Endpoints grouped by resource
- **Services**: Business logic separated from API
- **Schemas**: Request/response models separate from database models

### 2. **Scalability**
- Easy to add new features
- Clear where new code should go
- Testable architecture
- Package-based imports

### 3. **Maintainability**
- Small, focused files
- Clear dependencies
- Easy to navigate
- Standard Python project structure

### 4. **Developer Experience**
- IDE auto-completion works better
- Easy to find specific functionality
- Clear import paths
- Testing is straightforward

## Migration Plan

1. **Create new directory structure**
2. **Split models_v2.py into focused files**
3. **Separate API endpoints into resource-based files**
4. **Extract business logic into services**
5. **Move utility scripts to scripts/ directory**
6. **Update imports and dependencies**
7. **Add proper __init__.py files for packages**
8. **Update documentation and README**