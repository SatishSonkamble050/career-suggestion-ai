# Career Guidance App

A comprehensive FastAPI-based backend application for providing intelligent career guidance to students based on their skills, interests, and academic performance.

## Project Structure

```
career_guidance_app/
└── app/
    ├── main.py                          # FastAPI app factory
    ├── core/
    │   ├── __init__.py
    │   └── database.py                  # Database configuration
    ├── models/
    │   ├── __init__.py
    │   ├── student.py                   # Student model
    │   ├── skills.py                    # Skills model
    │   ├── interests.py                 # Interests model
    │   └── career_preferences.py        # Career preferences model
    ├── schemas/
    │   ├── __init__.py
    │   ├── student.py                   # Student Pydantic schema
    │   ├── skills.py                    # Skills Pydantic schema
    │   ├── interests.py                 # Interests Pydantic schema
    │   └── career_preferences.py        # Career preferences Pydantic schema
    ├── crud/
    │   ├── __init__.py
    │   ├── student.py                   # Student CRUD operations
    │   ├── skills.py                    # Skills CRUD operations
    │   ├── interests.py                 # Interests CRUD operations
    │   └── career_preferences.py        # Career preferences CRUD operations
    ├── api/
    │   ├── __init__.py
    │   └── routes/
    │       ├── __init__.py
    │       ├── student.py               # Student API endpoints
    │       ├── skills.py                # Skills API endpoints
    │       ├── interests.py             # Interests API endpoints
    │       └── career_preferences.py    # Career preferences API endpoints
    └── services/
        ├── __init__.py
        └── career_engine.py             # Career recommendation engine
```

## Features

- ✅ Student profile management
- ✅ Skills tracking
- ✅ Interest assessment
- ✅ Career preferences management
- ✅ Career recommendation engine
- ✅ SQLAlchemy ORM with relationships
- ✅ Pydantic data validation
- ✅ RESTful API with FastAPI
- ✅ CORS middleware
- ✅ Database migrations ready
- ✅ Auto-generated API documentation

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

```bash
cd career_guidance_app
uvicorn app.main:app --reload
```

The application will start at `http://localhost:8000`

## API Documentation

Once the server is running, access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### Students
- `GET /api/v1/students/` - Get all students
- `GET /api/v1/students/{student_id}` - Get student by ID
- `POST /api/v1/students/` - Create new student
- `PUT /api/v1/students/{student_id}` - Update student
- `DELETE /api/v1/students/{student_id}` - Delete student

### Skills
- `GET /api/v1/skills/student/{student_id}` - Get student's skills
- `GET /api/v1/skills/{skill_id}` - Get skill by ID
- `POST /api/v1/skills/` - Create new skill
- `PUT /api/v1/skills/{skill_id}` - Update skill
- `DELETE /api/v1/skills/{skill_id}` - Delete skill

### Interests
- `GET /api/v1/interests/student/{student_id}` - Get student's interests
- `GET /api/v1/interests/{interest_id}` - Get interest by ID
- `POST /api/v1/interests/` - Create new interest
- `PUT /api/v1/interests/{interest_id}` - Update interest
- `DELETE /api/v1/interests/{interest_id}` - Delete interest

### Career Preferences
- `GET /api/v1/career-preferences/student/{student_id}` - Get student's career preferences
- `GET /api/v1/career-preferences/{preference_id}` - Get career preference by ID
- `POST /api/v1/career-preferences/` - Create new career preference
- `PUT /api/v1/career-preferences/{preference_id}` - Update career preference
- `DELETE /api/v1/career-preferences/{preference_id}` - Delete career preference

## Database Models

### Student
- `id` (Integer, Primary Key)
- `name` (String)
- `email` (String, Unique)
- `grade_level` (Integer)
- `gpa` (Float)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Skills
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key)
- `skill_name` (String)
- `proficiency_level` (Float: 0-100)
- `description` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Interests
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key)
- `interest_area` (String)
- `intensity_level` (Float: 0-100)
- `description` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Career Preferences
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key)
- `career_path` (String)
- `match_score` (Float: 0-100)
- `reasoning` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Services

### CareerEngine
The `CareerEngine` service provides:
- `analyze_student(student_id)` - Analyze student profile
- `generate_recommendations(student_id)` - Generate career recommendations
- `_calculate_match_score()` - Calculate skill-career match score

## Running Tests

```bash
pytest
```

## Configuration

Update the `.env` file to configure:

```
DATABASE_URL=sqlite:///./career_guidance.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## Development Workflow

1. Define models in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Implement CRUD operations in `app/crud/`
4. Create API routes in `app/api/routes/`
5. Add business logic in `app/services/`
6. Test endpoints using Swagger UI

## Next Steps

- [ ] Create database initialization script
- [ ] Implement authentication and authorization
- [ ] Add career recommendation algorithm
- [ ] Create comprehensive test suite
- [ ] Add API logging
- [ ] Deploy to production
- [ ] Create frontend integration

## License

MIT
