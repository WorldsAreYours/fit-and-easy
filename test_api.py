"""
Simple test script to verify the API endpoints work correctly.
This creates a test database and performs basic CRUD operations.
"""

import requests
import json
from datetime import datetime


def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Personal Trainer App API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return False
    
    # Test creating a user
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "fitness_level": "beginner",
        "goals": "lose weight, build muscle"
    }
    
    response = requests.post(f"{base_url}/users", json=user_data)
    print(f"Create user: {response.status_code}")
    if response.status_code == 201:
        user = response.json()
        user_id = user["id"]
        print(f"Created user with ID: {user_id}")
    else:
        print(f"Failed to create user: {response.text}")
        return False
    
    # Test getting user
    response = requests.get(f"{base_url}/users/{user_id}")
    print(f"Get user: {response.status_code}")
    
    # Test listing exercises
    response = requests.get(f"{base_url}/exercises")
    print(f"List exercises: {response.status_code}")
    if response.status_code == 200:
        exercises = response.json()
        print(f"Found {len(exercises)} exercises")
        if exercises:
            exercise_id = exercises[0]["id"]
            print(f"Sample exercise: {exercises[0]['name']}")
    
    # Test creating a workout
    workout_data = {
        "name": "Morning Workout",
        "notes": "Quick morning routine"
    }
    
    response = requests.post(f"{base_url}/workouts?user_id={user_id}", json=workout_data)
    print(f"Create workout: {response.status_code}")
    if response.status_code == 201:
        workout = response.json()
        workout_id = workout["id"]
        print(f"Created workout with ID: {workout_id}")
    
    # Test adding exercise to workout
    if 'exercise_id' in locals():
        exercise_data = {
            "exercise_id": exercise_id,
            "sets": 3,
            "reps": 12,
            "rest_time": 60
        }
        
        response = requests.post(f"{base_url}/workouts/{workout_id}/exercises", json=exercise_data)
        print(f"Add exercise to workout: {response.status_code}")
    
    # Test getting workout with exercises
    response = requests.get(f"{base_url}/workouts/{workout_id}")
    print(f"Get workout details: {response.status_code}")
    
    # Test getting user's workouts
    response = requests.get(f"{base_url}/users/{user_id}/workouts")
    print(f"Get user workouts: {response.status_code}")
    
    # Test workout generation
    response = requests.post(f"{base_url}/users/{user_id}/generate-workout")
    print(f"Generate workout: {response.status_code}")
    if response.status_code == 200:
        generated = response.json()
        print(f"Generated workout with {len(generated['exercises'])} exercises")
        print(f"Estimated duration: {generated['estimated_duration']} minutes")
    
    print("\nAPI testing completed successfully!")
    return True


if __name__ == "__main__":
    test_api()