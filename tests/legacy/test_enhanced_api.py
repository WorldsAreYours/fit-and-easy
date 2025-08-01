#!/usr/bin/env python3
"""
Quick test script for the enhanced API endpoints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import time
from subprocess import Popen, DEVNULL

def start_server():
    """Start the enhanced API server"""
    print("🚀 Starting enhanced API server...")
    proc = Popen([
        "python", "-m", "uvicorn", "main_v2:app", 
        "--host", "127.0.0.1", "--port", "8001"
    ], stdout=DEVNULL, stderr=DEVNULL)
    
    # Wait for server to start
    time.sleep(3)
    return proc

def test_enhanced_endpoints():
    """Test the enhanced API endpoints"""
    base_url = "http://127.0.0.1:8001"
    
    print("🧪 Testing Enhanced API Endpoints")
    print("=" * 40)
    
    try:
        # Test 1: Health check
        print("\n1️⃣  Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"   ✅ Health check: {response.json()['status']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Get muscle groups
        print("\n2️⃣  Testing muscle groups endpoint...")
        response = requests.get(f"{base_url}/muscle-groups")
        if response.status_code == 200:
            muscle_groups = response.json()
            print(f"   ✅ Found {len(muscle_groups)} muscle groups")
            print(f"   📋 Sample: {muscle_groups[0]['name']}, {muscle_groups[1]['name']}, {muscle_groups[2]['name']}")
        else:
            print(f"   ❌ Muscle groups failed: {response.status_code}")
        
        # Test 3: Get muscle categories
        print("\n3️⃣  Testing muscle categories endpoint...")
        response = requests.get(f"{base_url}/muscle-groups/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"   ✅ Categories: {', '.join(categories['categories'])}")
        else:
            print(f"   ❌ Categories failed: {response.status_code}")
        
        # Test 4: Get all exercises
        print("\n4️⃣  Testing exercises endpoint...")
        response = requests.get(f"{base_url}/exercises")
        if response.status_code == 200:
            exercises = response.json()
            print(f"   ✅ Found {len(exercises)} exercises")
            
            # Show sample exercise
            if exercises:
                ex = exercises[0]
                muscle_names = [mg['name'] for mg in ex['muscle_groups']]
                print(f"   📋 Sample: {ex['name']} ({ex['primary_equipment']}) - {', '.join(muscle_names)}")
        else:
            print(f"   ❌ Exercises failed: {response.status_code}")
        
        # Test 5: Filter by muscle group
        print("\n5️⃣  Testing muscle group filtering...")
        response = requests.get(f"{base_url}/exercises?muscle_groups=chest")
        if response.status_code == 200:
            chest_exercises = response.json()
            print(f"   ✅ Found {len(chest_exercises)} chest exercises")
            for ex in chest_exercises[:3]:  # Show first 3
                muscle_names = [mg['name'] for mg in ex['muscle_groups']]
                print(f"      • {ex['name']} - {', '.join(muscle_names)}")
        else:
            print(f"   ❌ Chest exercises filter failed: {response.status_code}")
        
        # Test 6: Filter by equipment
        print("\n6️⃣  Testing equipment filtering...")
        response = requests.get(f"{base_url}/exercises?equipment=bodyweight")
        if response.status_code == 200:
            bodyweight_exercises = response.json()
            print(f"   ✅ Found {len(bodyweight_exercises)} bodyweight exercises")
            for ex in bodyweight_exercises[:3]:  # Show first 3
                print(f"      • {ex['name']} ({ex['difficulty']})")
        else:
            print(f"   ❌ Bodyweight exercises filter failed: {response.status_code}")
        
        # Test 7: Get equipment list
        print("\n7️⃣  Testing equipment endpoint...")
        response = requests.get(f"{base_url}/equipment")
        if response.status_code == 200:
            equipment = response.json()
            print(f"   ✅ Available equipment: {len(equipment['equipment'])} types")
            print(f"   📋 Sample: {', '.join(equipment['equipment'][:5])}...")
        else:
            print(f"   ❌ Equipment endpoint failed: {response.status_code}")
        
        # Test 8: Search exercises
        print("\n8️⃣  Testing exercise search...")
        response = requests.get(f"{base_url}/exercises/search?q=push")
        if response.status_code == 200:
            search_results = response.json()
            print(f"   ✅ Found {len(search_results)} exercises matching 'push'")
            for ex in search_results[:2]:  # Show first 2
                print(f"      • {ex['name']}")
        else:
            print(f"   ❌ Exercise search failed: {response.status_code}")
        
        # Test 9: Create a user (for workout generation)
        print("\n9️⃣  Testing user creation...")
        user_data = {
            "name": "Enhanced Test User",
            "email": "enhanced@example.com",
            "fitness_level": "intermediate",
            "goals": "Build strength with enhanced model"
        }
        response = requests.post(f"{base_url}/users", json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"   ✅ Created user: {user['name']} (ID: {user['id']})")
            
            # Test 10: Generate workout
            print("\n🔟 Testing enhanced workout generation...")
            workout_params = {
                "workout_type": "upper_body",
                "duration_minutes": 30,
                "available_equipment": ["bodyweight", "dumbbells"]
            }
            response = requests.post(
                f"{base_url}/users/{user['id']}/generate-workout",
                params=workout_params
            )
            if response.status_code == 200:
                workout = response.json()
                print(f"   ✅ Generated workout: {workout['name']}")
                print(f"   📊 {len(workout['exercises'])} exercises, {workout['estimated_duration']} min")
                print(f"   🎯 Target muscles: {', '.join(workout['target_muscle_groups'][:5])}...")
                
                # Show exercises
                for ex in workout['exercises'][:3]:  # Show first 3
                    muscle_names = [mg['name'] for mg in ex['muscle_groups']]
                    print(f"      • {ex['name']} ({ex['primary_equipment']}) - {', '.join(muscle_names)}")
            else:
                print(f"   ❌ Workout generation failed: {response.status_code}")
                if response.text:
                    print(f"      Error: {response.text}")
        else:
            print(f"   ❌ User creation failed: {response.status_code}")
            if response.text:
                print(f"      Error: {response.text}")
        
        print(f"\n🎉 Enhanced API testing complete!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8001.")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 ENHANCED API TESTING SCRIPT")
    print("=" * 50)
    
    # Start server
    server_proc = None
    try:
        server_proc = start_server()
        
        # Run tests
        success = test_enhanced_endpoints()
        
        if success:
            print("\n✅ All enhanced API tests passed!")
        else:
            print("\n❌ Some tests failed.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted")
    finally:
        # Clean up server
        if server_proc:
            print("\n🛑 Stopping server...")
            server_proc.terminate()
            server_proc.wait()

if __name__ == "__main__":
    main()