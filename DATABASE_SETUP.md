# Database Setup Guide

## Overview
This project uses SQLite with a seeded exercise database. The database file is not tracked in git to prevent conflicts and protect user data.

## Setting Up the Database

### First Time Setup
```bash
# Create and populate the database with exercises
python seed_data.py
```

This will:
- Create `trainer_app.db` with all necessary tables
- Populate the database with 27 pre-defined exercises
- Set up the schema for users, workouts, and workout exercises

### Resetting the Database
If you need to reset the database to its initial state:

```bash
# Delete the existing database
rm trainer_app.db

# Recreate with seed data
python seed_data.py
```

## Database Contents

### Exercises (27 total)
The seed script includes exercises covering:
- **Chest**: Push-ups, Bench Press, Dumbbell Flyes
- **Back**: Pull-ups, Bent-over Rows, Lat Pulldowns, Deadlifts
- **Legs**: Squats, Lunges, Romanian Deadlifts, Calf Raises
- **Shoulders**: Overhead Press, Lateral Raises, Pike Push-ups
- **Arms**: Bicep Curls, Tricep Dips, Hammer Curls, Close-grip Push-ups
- **Core**: Plank, Crunches, Russian Twists, Mountain Climbers, Dead Bug
- **Full Body**: Burpees, Thrusters, Turkish Get-ups

### Exercise Properties
Each exercise includes:
- Name and detailed instructions
- Target muscle groups
- Required equipment
- Difficulty level (easy/medium/hard)

## Development Notes

### Why Database is Not Tracked
- **Size**: Database files can grow large with user data
- **Conflicts**: Multiple developers would create merge conflicts
- **Security**: Prevents accidental commit of sensitive user data
- **Environment**: Each environment should have its own database

### Database Schema
The database includes these tables:
- `users` - User profiles and fitness information
- `exercises` - Exercise library with instructions
- `workouts` - User workout sessions
- `workout_exercises` - Linking table with sets/reps/weight data

### Migrations
For now, schema changes require:
1. Update models in `models.py`
2. Delete and recreate database with `python seed_data.py`
3. Future: Add proper migration system for production

## Troubleshooting

### "No such file" Error
If you get database errors, the database file might be missing:
```bash
python seed_data.py
```

### "Table doesn't exist" Error
The database schema might be outdated:
```bash
rm trainer_app.db
python seed_data.py
```

### Permission Errors
Ensure the directory is writable:
```bash
chmod 755 .
python seed_data.py
```

## Production Considerations

For production deployment:
- Use PostgreSQL or MySQL instead of SQLite
- Set up proper database migrations
- Configure backup procedures
- Use environment variables for database connection
- Implement database connection pooling