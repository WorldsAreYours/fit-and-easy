# Personal Trainer App Backend

A FastAPI-based backend for a personal trainer application that provides exercise management, workout tracking, and basic workout generation capabilities.

## Features

- **User Management**: Create and manage user profiles with fitness levels and goals
- **Exercise Library**: Comprehensive database of 27+ exercises across all major muscle groups
- **Workout Tracking**: Create workouts and track exercises with sets, reps, and weights
- **Workout Generation**: Simple algorithm to generate workouts based on user fitness level
- **RESTful API**: Well-designed endpoints with proper HTTP status codes and validation
- **Database**: SQLite database with SQLAlchemy ORM
- **Documentation**: Automatic API documentation with FastAPI/Swagger

## Project Structure

```
fit-and-easy/
├── main.py              # FastAPI application with all endpoints
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration and session management
├── seed_data.py         # Script to populate exercise database
├── test_api.py          # API testing script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Database Schema

### Users
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `fitness_level`: beginner/intermediate/advanced
- `goals`: Text description of fitness goals
- `created_at`: Timestamp

### Exercises
- `id`: Primary key
- `name`: Exercise name
- `muscle_groups`: Comma-separated muscle groups
- `equipment`: Required equipment
- `difficulty`: easy/medium/hard
- `instructions`: Detailed form instructions

### Workouts
- `id`: Primary key
- `user_id`: Foreign key to users
- `name`: Workout name
- `date`: Workout date
- `notes`: Optional notes
- `created_at`: Timestamp

### Workout Exercises
- `id`: Primary key
- `workout_id`: Foreign key to workouts
- `exercise_id`: Foreign key to exercises
- `sets`: Number of sets
- `reps`: Number of repetitions
- `weight`: Weight used (optional)
- `rest_time`: Rest time in seconds

## API Endpoints

### Users
- `POST /users` - Create a new user
- `GET /users/{user_id}` - Get user profile

### Exercises
- `POST /exercises` - Create a new exercise
- `GET /exercises` - List exercises (with optional filters for muscle group, equipment, difficulty)

### Workouts
- `POST /workouts?user_id={user_id}` - Create a new workout
- `POST /workouts/{workout_id}/exercises` - Add exercise to workout
- `GET /workouts/{workout_id}` - Get workout details
- `GET /users/{user_id}/workouts` - Get user's workouts

### Workout Generation
- `POST /users/{user_id}/generate-workout` - Generate a workout based on user's fitness level

### Health
- `GET /health` - Health check endpoint

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database and Seed Data**
   ```bash
   python seed_data.py
   ```

3. **Start the Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

5. **Run Tests**
   ```bash
   python test_api.py
   ```

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "fitness_level": "beginner",
    "goals": "lose weight, build muscle"
  }'
```

### List Exercises
```bash
curl "http://localhost:8000/exercises?muscle_group=chest&difficulty=easy"
```

### Create a Workout
```bash
curl -X POST "http://localhost:8000/workouts?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Workout",
    "notes": "Quick morning routine"
  }'
```

### Generate a Workout
```bash
curl -X POST "http://localhost:8000/users/1/generate-workout"
```

## Technical Decisions

### Framework Choice
- **FastAPI**: Chosen for automatic API documentation, type hints, async support, and excellent performance
- **SQLAlchemy**: Robust ORM with good migration support for future database changes
- **SQLite**: Simple file-based database perfect for development and small-scale deployment

### Architecture
- **Synchronous Design**: Used synchronous SQLAlchemy for Python 3.7 compatibility and simplicity
- **Separation of Concerns**: Clear separation between database models, API endpoints, and business logic
- **Pydantic Models**: Strong typing and validation for API requests/responses

### Future AI Integration
The codebase is designed to easily accommodate AI features:
- Workout generation logic is abstracted and can be replaced with ML models
- Exercise data includes detailed instructions suitable for training AI models
- User goals and fitness levels provide rich context for personalized recommendations
- API design allows for adding new endpoints for AI-powered features

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sqlalchemy**: ORM and database toolkit
- **pydantic**: Data validation and settings management
- **python-multipart**: Form data parsing
- **aiosqlite**: Async SQLite driver
- **python-dateutil**: Date/time utilities
- **email-validator**: Email validation

## Development Notes

- The application uses synchronous SQLAlchemy for Python 3.7 compatibility
- All endpoints include proper error handling and HTTP status codes
- Database relationships are properly configured with foreign keys
- The workout generator uses a simple algorithm that can be enhanced with AI/ML
- CORS is enabled for future frontend integration

## Next Steps

1. Add user authentication and authorization
2. Implement progress tracking and analytics
3. Add AI-powered workout recommendations
4. Create a frontend application
5. Add image/video support for exercises
6. Implement workout templates and programs
7. Add social features (sharing workouts, following users)
8. Mobile app development