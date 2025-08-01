# 📚 API Documentation Guide

Your Personal Trainer App now has comprehensive API documentation available in multiple formats!

## 🎯 Quick Access

### Interactive Documentation (Recommended)
Start your server and visit these URLs:

```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Then visit:
# 🌟 Swagger UI (Interactive):  http://localhost:8000/docs
# 📖 ReDoc (Clean):           http://localhost:8000/redoc
```

### Static Files
- `openapi.json` - OpenAPI 3.0 specification in JSON format
- `openapi.yaml` - OpenAPI 3.0 specification in YAML format

## 🚀 Features of the Generated Documentation

### ✅ What's Included:
- **All 10 endpoints** with detailed descriptions
- **Request/Response schemas** with validation rules
- **Interactive testing** - try endpoints directly from Swagger UI
- **Authentication schemes** (ready for future auth implementation)
- **Error responses** and status codes
- **Example requests and responses**

### 📋 All Documented Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user profile |
| GET | `/users/{user_id}` | Get user profile by ID |
| POST | `/exercises` | Create a new exercise |
| GET | `/exercises` | List exercises with filters |
| POST | `/workouts` | Create a new workout |
| POST | `/workouts/{workout_id}/exercises` | Add exercise to workout |
| GET | `/workouts/{workout_id}` | Get workout details |
| GET | `/users/{user_id}/workouts` | Get user's workouts |
| POST | `/users/{user_id}/generate-workout` | Generate AI workout |
| GET | `/health` | Health check endpoint |

## 🔧 How to Regenerate Documentation

```bash
# Simple way - just run the generator
python generate_docs.py

# Or get it directly from the running server
curl http://localhost:8000/openapi.json > openapi.json
```

## 🌐 Sharing Your API

You can share the documentation in several ways:

1. **Share the files**: Send `openapi.json` or `openapi.yaml` to developers
2. **Host the docs**: Deploy your app and share the `/docs` URL
3. **Import to tools**: Load the spec into Postman, Insomnia, or other API tools
4. **Generate client code**: Use OpenAPI generators to create client SDKs

## 🎨 Customization Options

The documentation can be enhanced by adding more details to your FastAPI decorators:

```python
@app.post("/users", 
    response_model=UserResponse, 
    status_code=201,
    summary="Create User Account",
    description="Creates a new user profile with fitness level and goals",
    response_description="User successfully created with assigned ID",
    tags=["User Management"]
)
```

## 📱 Testing with Swagger UI

1. Visit `http://localhost:8000/docs`
2. Click on any endpoint to expand it
3. Click "Try it out" 
4. Fill in parameters/request body
5. Click "Execute" to test the API
6. View the response directly in the browser

The interactive documentation makes it easy to test your API without writing any code!