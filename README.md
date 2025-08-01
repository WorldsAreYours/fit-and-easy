# 🏋️ Personal Trainer App

A comprehensive fitness tracking and workout management API built with FastAPI, SQLAlchemy, and SQLite. Designed with a professional, scalable architecture for team development and future AI integration.

## 📁 Project Structure

```
fit-and-easy/
├── app/                          # 📦 Main application package
│   ├── core/                     # ⚙️ Core configuration and database
│   ├── models/                   # 🗃️ Database models (organized by domain)
│   ├── schemas/                  # 📋 Pydantic request/response models
│   ├── api/v1/                   # 🌐 Versioned API endpoints
│   ├── services/                 # 💼 Business logic layer
│   └── utils/                    # 🛠️ Utility functions
├── database/                     # 🗄️ Database utilities and migrations
│   ├── seeds/                    # 🌱 Seed data for development
│   └── migrations/               # 🔄 Database migration scripts
├── scripts/                      # 📜 Utility scripts and demos
├── tests/                        # 🧪 Test suite (organized by component)
├── docs/                         # 📚 Documentation and API specs
├── requirements/                 # 📋 Environment-specific dependencies
└── config/                       # ⚙️ Configuration files
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt
```

### 2. Initialize Database

```bash
# Setup database with seed data
python scripts/setup_database.py
```

### 3. Run the Application

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Explore the API

- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc  
- **Health Check**: http://localhost:8000/health

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `docs/RESTRUCTURE_SUMMARY.md` | Complete restructuring overview |
| `docs/ENHANCED_MODEL_SUMMARY.md` | Enhanced exercise model details |
| `docs/DATABASE_SETUP.md` | Database setup and management |
| `docs/api/` | OpenAPI specifications |

## 🏗️ Architecture Highlights

### **Professional Structure**
- ✅ **Separation of Concerns**: Models, services, API, and schemas in separate packages
- ✅ **Scalable Design**: Easy to add new features without touching existing code
- ✅ **Package Organization**: Clear Python package hierarchy with proper imports
- ✅ **Environment Configs**: Development, testing, and production ready

### **Database Design**
- 🗃️ **Normalized Models**: Proper relationships and standardized enums
- 🏋️ **Exercise System**: 27 muscle groups, equipment standardization, difficulty levels
- 💪 **Workout Management**: Complete workout planning and tracking
- 👤 **User Profiles**: Fitness levels, goals, and personalized recommendations

### **API Features**
- 🌐 **RESTful Design**: Resource-based endpoints with proper HTTP methods
- 📋 **Data Validation**: Pydantic schemas for request/response validation
- 🔍 **Advanced Filtering**: Search exercises by muscle groups, equipment, difficulty
- 📄 **Auto Documentation**: OpenAPI/Swagger integration
- ⚡ **Performance**: Efficient database queries and pagination

## 🎯 Key Features

### **Exercise Management**
- 📊 **15+ Exercises** with proper muscle group relationships
- 🏷️ **Equipment Standardization** (bodyweight, dumbbells, barbells, etc.)
- 🎚️ **Difficulty Levels** (easy, medium, hard)
- 🔍 **Advanced Search** and filtering capabilities

### **Workout Planning**
- 📝 **Custom Workouts** with sets, reps, weight tracking
- 🤖 **Workout Generator** based on user goals and fitness level
- ⏱️ **Rest Time Management** and exercise ordering
- 📈 **Progress Tracking** with workout history

### **User Management**
- 👤 **User Profiles** with fitness levels and goals
- 🎯 **Personalized Recommendations** based on user data
- 📊 **Workout History** and progress tracking

## 🛠️ Development

### **Environment Setup**
```bash
# Development dependencies
pip install -r requirements/development.txt

# Run tests
pytest

# Code formatting
black .

# Type checking
mypy app/
```

### **Database Management**
```bash
# Reset database
rm trainer_app_structured.db
python scripts/setup_database.py

# Run migration scripts
python database/migrations/migration_script.py
```

### **Demo Scripts**
```bash
# Demonstrate new structure
python scripts/demo_new_structure.py

# Show enhanced queries
python scripts/demo_enhanced_queries.py

# Test API endpoints
python tests/legacy/test_enhanced_api.py
```

## 🔮 Future Roadmap

### **Phase 1: Core Enhancement**
- 🔐 User authentication and authorization
- 📊 Exercise analytics and progress tracking
- 🎯 Advanced workout recommendations

### **Phase 2: AI Integration**
- 🤖 AI-powered workout generation
- 📈 Performance analysis and insights
- 🗣️ Natural language workout queries

### **Phase 3: Social Features**
- 👥 Social workout sharing
- 🏆 Achievement system
- 👨‍🏫 Trainer-client connections

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the structure**: Add code to appropriate packages
4. **Write tests**: Use the `tests/` directory structure
5. **Update documentation**: Keep docs up to date
6. **Submit pull request**: Clear description of changes

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🎉 Acknowledgments

- **FastAPI** for the excellent web framework
- **SQLAlchemy** for robust ORM capabilities  
- **Pydantic** for data validation and serialization
- **Uvicorn** for ASGI server implementation

---

**Ready to transform your fitness journey with professional-grade API architecture!** 🚀💪