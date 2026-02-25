# All API Endpoints - Career Guidance App

## Base URL
```
http://localhost:8000
```

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [Student Management Endpoints](#student-management-endpoints)
3. [Skills Endpoints](#skills-endpoints)
4. [Interests Endpoints](#interests-endpoints)
5. [Career Preferences Endpoints](#career-preferences-endpoints)
6. [Academic Profile Endpoints](#academic-profile-endpoints)
7. [AI Agents Endpoints](#ai-agents-endpoints)
8. [Simple LangGraph Workflow Endpoints](#simple-langgraph-workflow-endpoints)
9. [System Endpoints](#system-endpoints)

---

## Authentication Endpoints

### 1. Register New Student
```http
POST /api/v1/auth/register
```
**Description**: Create a new student account

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "grade_level": 12,
  "gpa": 3.8
}
```

**Response** (201):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "john@example.com",
  "name": "John Doe"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "grade_level": 12,
    "gpa": 3.8
  }'
```

---

### 2. Login
```http
POST /api/v1/auth/login
```
**Description**: Login student account

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "john@example.com",
  "name": "John Doe"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'
```

---

## Student Management Endpoints

### 3. Get All Students
```http
GET /api/v1/students
```
**Description**: Get list of all students

**Query Parameters**:
| Parameter | Type | Default |
|-----------|------|---------|
| skip | integer | 0 |
| limit | integer | 100 |

**Response** (200):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "grade_level": 12,
    "gpa": 3.8,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

**cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/students?skip=0&limit=10"
```

---

### 4. Get Student by ID
```http
GET /api/v1/students/{student_id}
```
**Description**: Get specific student details

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "grade_level": 12,
  "gpa": 3.8,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/students/1
```

---

### 5. Create Student
```http
POST /api/v1/students
```
**Description**: Create a new student (alternative to register)

**Request Body**:
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "SecurePassword456",
  "grade_level": 11,
  "gpa": 3.5
}
```

**Response** (201):
```json
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "grade_level": 11,
  "gpa": 3.5
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "SecurePassword456",
    "grade_level": 11,
    "gpa": 3.5
  }'
```

---

### 6. Update Student
```http
PUT /api/v1/students/{student_id}
```
**Description**: Update student information

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Request Body**:
```json
{
  "name": "John Updated",
  "grade_level": 13,
  "gpa": 3.9
}
```

**Response** (200):
```json
{
  "id": 1,
  "name": "John Updated",
  "grade_level": 13,
  "gpa": 3.9
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "grade_level": 13,
    "gpa": 3.9
  }'
```

---

### 7. Delete Student
```http
DELETE /api/v1/students/{student_id}
```
**Description**: Delete a student

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (204 No Content)

**cURL**:
```bash
curl -X DELETE http://localhost:8000/api/v1/students/1
```

---

## Skills Endpoints

### 8. Get Student Skills
```http
GET /api/v1/skills/student/{student_id}
```
**Description**: Get all skills for a student

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (200):
```json
[
  {
    "id": 1,
    "student_id": 1,
    "skill_name": "Python",
    "proficiency_level": 95,
    "description": "Expert in Python programming"
  },
  {
    "id": 2,
    "student_id": 1,
    "skill_name": "JavaScript",
    "proficiency_level": 85,
    "description": "Advanced JavaScript developer"
  }
]
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/skills/student/1
```

---

### 9. Get Skill by ID
```http
GET /api/v1/skills/{skill_id}
```
**Description**: Get specific skill details

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| skill_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "skill_name": "Python",
  "proficiency_level": 95,
  "description": "Expert in Python programming"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/skills/1
```

---

### 10. Create Skill
```http
POST /api/v1/skills
```
**Description**: Add a new skill for student

**Request Body**:
```json
{
  "student_id": 1,
  "skill_name": "Machine Learning",
  "proficiency_level": 80,
  "description": "Advanced ML knowledge"
}
```

**Response** (201):
```json
{
  "id": 3,
  "student_id": 1,
  "skill_name": "Machine Learning",
  "proficiency_level": 80,
  "description": "Advanced ML knowledge"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/skills \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "skill_name": "Machine Learning",
    "proficiency_level": 80,
    "description": "Advanced ML knowledge"
  }'
```

---

### 11. Update Skill
```http
PUT /api/v1/skills/{skill_id}
```
**Description**: Update skill information

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| skill_id | integer |

**Request Body**:
```json
{
  "proficiency_level": 90,
  "description": "Expert level ML practitioner"
}
```

**Response** (200):
```json
{
  "id": 3,
  "student_id": 1,
  "skill_name": "Machine Learning",
  "proficiency_level": 90,
  "description": "Expert level ML practitioner"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/v1/skills/3 \
  -H "Content-Type: application/json" \
  -d '{
    "proficiency_level": 90,
    "description": "Expert level ML practitioner"
  }'
```

---

### 12. Delete Skill
```http
DELETE /api/v1/skills/{skill_id}
```
**Description**: Delete a skill

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| skill_id | integer |

**Response** (204 No Content)

**cURL**:
```bash
curl -X DELETE http://localhost:8000/api/v1/skills/1
```

---

## Interests Endpoints

### 13. Get Student Interests
```http
GET /api/v1/interests/student/{student_id}
```
**Description**: Get all interests for a student

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (200):
```json
[
  {
    "id": 1,
    "student_id": 1,
    "interest_area": "Artificial Intelligence",
    "intensity_level": 95,
    "description": "Passionate about AI research"
  }
]
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/interests/student/1
```

---

### 14. Get Interest by ID
```http
GET /api/v1/interests/{interest_id}
```
**Description**: Get specific interest details

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| interest_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "interest_area": "Artificial Intelligence",
  "intensity_level": 95,
  "description": "Passionate about AI research"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/interests/1
```

---

### 15. Create Interest
```http
POST /api/v1/interests
```
**Description**: Add a new interest for student

**Request Body**:
```json
{
  "student_id": 1,
  "interest_area": "Data Science",
  "intensity_level": 85,
  "description": "Strong interest in data analysis"
}
```

**Response** (201):
```json
{
  "id": 2,
  "student_id": 1,
  "interest_area": "Data Science",
  "intensity_level": 85,
  "description": "Strong interest in data analysis"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/interests \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "interest_area": "Data Science",
    "intensity_level": 85,
    "description": "Strong interest in data analysis"
  }'
```

---

### 16. Update Interest
```http
PUT /api/v1/interests/{interest_id}
```
**Description**: Update interest information

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| interest_id | integer |

**Request Body**:
```json
{
  "intensity_level": 90
}
```

**Response** (200):
```json
{
  "id": 2,
  "student_id": 1,
  "interest_area": "Data Science",
  "intensity_level": 90,
  "description": "Strong interest in data analysis"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/v1/interests/2 \
  -H "Content-Type: application/json" \
  -d '{"intensity_level": 90}'
```

---

### 17. Delete Interest
```http
DELETE /api/v1/interests/{interest_id}
```
**Description**: Delete an interest

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| interest_id | integer |

**Response** (204 No Content)

**cURL**:
```bash
curl -X DELETE http://localhost:8000/api/v1/interests/1
```

---

## Career Preferences Endpoints

### 18. Get Student Career Preferences
```http
GET /api/v1/career-preferences/student/{student_id}
```
**Description**: Get all career preferences for a student

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (200):
```json
[
  {
    "id": 1,
    "student_id": 1,
    "career_path": "Machine Learning Engineer",
    "match_score": 92,
    "reasoning": "Perfect fit for skills and interests"
  }
]
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/career-preferences/student/1
```

---

### 19. Get Career Preference by ID
```http
GET /api/v1/career-preferences/{preference_id}
```
**Description**: Get specific career preference details

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| preference_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "career_path": "Machine Learning Engineer",
  "match_score": 92,
  "reasoning": "Perfect fit for skills and interests"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/career-preferences/1
```

---

### 20. Create Career Preference
```http
POST /api/v1/career-preferences
```
**Description**: Add a new career preference

**Request Body**:
```json
{
  "student_id": 1,
  "career_path": "Data Scientist",
  "match_score": 88,
  "reasoning": "Great alignment with data interests"
}
```

**Response** (201):
```json
{
  "id": 2,
  "student_id": 1,
  "career_path": "Data Scientist",
  "match_score": 88,
  "reasoning": "Great alignment with data interests"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/career-preferences \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "career_path": "Data Scientist",
    "match_score": 88,
    "reasoning": "Great alignment with data interests"
  }'
```

---

### 21. Update Career Preference
```http
PUT /api/v1/career-preferences/{preference_id}
```
**Description**: Update career preference

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| preference_id | integer |

**Request Body**:
```json
{
  "match_score": 95,
  "reasoning": "Excellent fit"
}
```

**Response** (200):
```json
{
  "id": 2,
  "student_id": 1,
  "career_path": "Data Scientist",
  "match_score": 95,
  "reasoning": "Excellent fit"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/v1/career-preferences/2 \
  -H "Content-Type: application/json" \
  -d '{"match_score": 95, "reasoning": "Excellent fit"}'
```

---

### 22. Delete Career Preference
```http
DELETE /api/v1/career-preferences/{preference_id}
```
**Description**: Delete a career preference

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| preference_id | integer |

**Response** (204 No Content)

**cURL**:
```bash
curl -X DELETE http://localhost:8000/api/v1/career-preferences/1
```

---

## Academic Profile Endpoints

### 23. Create Academic Profile
```http
POST /api/v1/academic-profiles
```
**Description**: Create academic profile for student

**Request Body**:
```json
{
  "student_id": 1,
  "stream": "Science",
  "current_class": "12th",
  "result": "Pass",
  "strongest_subject": "Mathematics",
  "weakest_subject": "Physical Education",
  "subjects": [
    {
      "subject_name": "Mathematics",
      "marks": 95
    },
    {
      "subject_name": "Physics",
      "marks": 88
    },
    {
      "subject_name": "Chemistry",
      "marks": 90
    }
  ]
}
```

**Response** (201):
```json
{
  "id": 1,
  "student_id": 1,
  "stream": "Science",
  "current_class": "12th",
  "result": "Pass",
  "strongest_subject": "Mathematics",
  "weakest_subject": "Physical Education",
  "subjects": [...]
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/academic-profiles \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "stream": "Science",
    "current_class": "12th",
    "result": "Pass",
    "strongest_subject": "Mathematics",
    "weakest_subject": "Physical Education",
    "subjects": [
      {"subject_name": "Mathematics", "marks": 95}
    ]
  }'
```

---

### 24. Get Academic Profile by ID
```http
GET /api/v1/academic-profiles/{profile_id}
```
**Description**: Get academic profile details

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| profile_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "stream": "Science",
  "current_class": "12th",
  "result": "Pass",
  "strongest_subject": "Mathematics",
  "weakest_subject": "Physical Education"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/academic-profiles/1
```

---

### 25. Get Profile by Student ID
```http
GET /api/v1/academic-profiles/student/{student_id}
```
**Description**: Get academic profile for a student

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "stream": "Science",
  "current_class": "12th"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/v1/academic-profiles/student/1
```

---

### 26. Update Academic Profile
```http
PUT /api/v1/academic-profiles/{profile_id}
```
**Description**: Update academic profile

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| profile_id | integer |

**Request Body**:
```json
{
  "result": "Excellent",
  "strongest_subject": "Physics"
}
```

**Response** (200):
```json
{
  "id": 1,
  "student_id": 1,
  "stream": "Science",
  "result": "Excellent",
  "strongest_subject": "Physics"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/v1/academic-profiles/1 \
  -H "Content-Type: application/json" \
  -d '{"result": "Excellent", "strongest_subject": "Physics"}'
```

---

### 27. Delete Academic Profile
```http
DELETE /api/v1/academic-profiles/{profile_id}
```
**Description**: Delete academic profile

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| profile_id | integer |

**Response** (204 No Content)

**cURL**:
```bash
curl -X DELETE http://localhost:8000/api/v1/academic-profiles/1
```

---

### 28. Add Subject Mark
```http
POST /api/v1/academic-profiles/{profile_id}/subjects
```
**Description**: Add subject mark to profile

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| profile_id | integer |

**Request Body**:
```json
{
  "subject_name": "Computer Science",
  "marks": 92
}
```

**Response** (201):
```json
{
  "id": 4,
  "academic_profile_id": 1,
  "subject_name": "Computer Science",
  "marks": 92
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/academic-profiles/1/subjects \
  -H "Content-Type: application/json" \
  -d '{"subject_name": "Computer Science", "marks": 92}'
```

---

## AI Agents Endpoints

### 29. Get Available Agents
```http
GET /api/agents/available
```
**Description**: Get list of all available AI agents

**Response** (200):
```json
[
  {
    "type": "career_recommender",
    "name": "Career Recommender Agent",
    "description": "Recommends career paths"
  },
  {
    "type": "skill_analyzer",
    "name": "Skill Analyzer Agent",
    "description": "Analyzes student skills"
  },
  {
    "type": "interest_evaluator",
    "name": "Interest Evaluator Agent",
    "description": "Evaluates career interests"
  },
  {
    "type": "academic_counselor",
    "name": "Academic Counselor Agent",
    "description": "Provides academic guidance"
  },
  {
    "type": "job_market_analyst",
    "name": "Job Market Analyst Agent",
    "description": "Analyzes job market trends"
  }
]
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/agents/available
```

---

### 30. Execute Multiple Agents
```http
POST /api/agents/execute
```
**Description**: Execute multiple agents for complete analysis

**Request Body**:
```json
{
  "student_id": 1,
  "agents": [
    "career_recommender",
    "skill_analyzer",
    "interest_evaluator"
  ]
}
```

**Response** (200):
```json
{
  "student_id": 1,
  "agents_executed": 3,
  "results": [
    {
      "agent_type": "career_recommender",
      "response": "Based on your profile..."
    }
  ]
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "agents": ["career_recommender", "skill_analyzer"]
  }'
```

---

### 31. Execute Single Agent
```http
POST /api/agents/execute/{agent_type}
```
**Description**: Execute a single specific agent

**Path Parameters**:
| Parameter | Type | Options |
|-----------|------|---------|
| agent_type | string | career_recommender, skill_analyzer, interest_evaluator, academic_counselor, job_market_analyst |

**Query Parameters**:
| Parameter | Type | Required |
|-----------|------|----------|
| student_id | integer | Yes |
| target_career | string | No |
| industry | string | No |

**Response** (200):
```json
{
  "agent_type": "career_recommender",
  "student_id": 1,
  "response": "Detailed career analysis...",
  "confidence": 0.92
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1"
```

**With Optional Parameters**:
```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1&target_career=Engineer&industry=Tech"
```

---

### 32. Execute LangGraph Workflow
```http
POST /api/agents/langgraph/execute/{student_id}
```
**Description**: Execute advanced LangGraph workflow

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Request Body**:
```json
{
  "academic": {"gpa": 3.8},
  "skills": {"technical": ["Python"]},
  "interests": {"fields": ["AI"]},
  "preferences": {"salary_range": "100k-150k"}
}
```

**Response** (200):
```json
{
  "student_id": 1,
  "execution_status": "completed",
  "results": {...}
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/agents/langgraph/execute/1 \
  -H "Content-Type: application/json" \
  -d '{"academic":{"gpa":3.8}}'
```

---

### 33. Parallel Agent Execution
```http
POST /api/agents/langgraph/parallel/{student_id}
```
**Description**: Execute agents in parallel for faster results

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Request Body**:
```json
{
  "academic": {"gpa": 3.8},
  "skills": {"technical": ["Python"]},
  "interests": {"fields": ["AI"]},
  "preferences": {"salary_range": "100k-150k"}
}
```

**Response** (200):
```json
{
  "student_id": 1,
  "execution_time_seconds": 5.2,
  "agents_executed": 5,
  "results": {...}
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/agents/langgraph/parallel/1 \
  -H "Content-Type: application/json" \
  -d '{"academic":{"gpa":3.8}}'
```

---

## Simple LangGraph Workflow Endpoints

### 34. Health Check
```http
GET /api/agents/simple/health
```
**Description**: Check if workflow service is running

**Response** (200):
```json
{
  "status": "healthy",
  "service": "simple_langgraph"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/api/agents/simple/health
```

---

### 35. Career Guidance Workflow
```http
POST /api/agents/simple/career-guide/{student_id}
```
**Description**: Execute simplified LangGraph workflow for career guidance

**Path Parameters**:
| Parameter | Type |
|-----------|------|
| student_id | integer |

**Request Body** (Optional):
```json
{
  "academic": {
    "gpa": 3.8,
    "major": "Computer Science",
    "subjects": ["AI", "ML"],
    "strong_areas": ["Programming"],
    "weak_areas": ["Public Speaking"]
  },
  "skills": {
    "technical": ["Python", "JavaScript"],
    "soft": ["Leadership"],
    "certifications": ["AWS"]
  },
  "interests": {
    "fields": ["AI", "Data Science"],
    "activities": ["Kaggle"],
    "industries": ["Tech"]
  },
  "preferences": {
    "work_style": "Remote",
    "salary_range": "100k-150k",
    "location": "San Francisco",
    "career_growth": "Leadership",
    "impact": "Meaningful",
    "learning": "Cutting-edge"
  }
}
```

**Response** (200):
```json
{
  "student_id": 1,
  "academic_analysis": {...},
  "skill_analysis": {...},
  "interest_analysis": {...},
  "preference_analysis": {...},
  "market_analysis": {...},
  "final_report": "Comprehensive career guidance..."
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {"gpa": 3.8},
    "skills": {"technical": ["Python"]},
    "interests": {"fields": ["AI"]},
    "preferences": {"salary_range": "100k-150k"}
  }'
```

---

## System Endpoints

### 36. Health Check (App)
```http
GET /health
```
**Description**: Check if application is healthy

**Response** (200):
```json
{
  "status": "healthy"
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/health
```

---

### 37. API Documentation (Swagger UI)
```http
GET /docs
```
**Description**: Interactive API documentation

**Access**: Open `http://localhost:8000/docs` in browser

---

### 38. API Documentation (ReDoc)
```http
GET /redoc
```
**Description**: Alternative API documentation

**Access**: Open `http://localhost:8000/redoc` in browser

---

### 39. OpenAPI Schema
```http
GET /openapi.json
```
**Description**: Get OpenAPI specification

**Response** (200):
```json
{
  "openapi": "3.1.0",
  "info": {"title": "Career Guidance App", "version": "1.0.0"},
  "paths": {...}
}
```

**cURL**:
```bash
curl -X GET http://localhost:8000/openapi.json
```

---

## Status Codes Reference

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource successfully created |
| 204 | No Content | Request successful, no content |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Authentication required |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Invalid data |
| 500 | Server Error | Internal server error |

---

## Quick Testing Guide

### Using cURL
```bash
# Test health
curl http://localhost:8000/health

# Get all students
curl http://localhost:8000/api/v1/students

# Get student by ID
curl http://localhost:8000/api/v1/students/1

# Create student
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'
```

### Using Swagger UI
1. Open browser
2. Navigate to `http://localhost:8000/docs`
3. Click on endpoint
4. Click "Try it out"
5. Fill in parameters
6. Click "Execute"

### Using Python
```python
import requests

# Get students
response = requests.get("http://localhost:8000/api/v1/students")
print(response.json())

# Create student
data = {"name": "John", "email": "john@example.com", "password": "pass"}
response = requests.post("http://localhost:8000/api/v1/students", json=data)
print(response.json())
```

---

## Endpoint Summary Table

| # | Method | Endpoint | Description |
|----|--------|----------|-------------|
| 1 | POST | /api/v1/auth/register | Register student |
| 2 | POST | /api/v1/auth/login | Login student |
| 3 | GET | /api/v1/students | Get all students |
| 4 | GET | /api/v1/students/{id} | Get student by ID |
| 5 | POST | /api/v1/students | Create student |
| 6 | PUT | /api/v1/students/{id} | Update student |
| 7 | DELETE | /api/v1/students/{id} | Delete student |
| 8 | GET | /api/v1/skills/student/{id} | Get student skills |
| 9 | GET | /api/v1/skills/{id} | Get skill by ID |
| 10 | POST | /api/v1/skills | Create skill |
| 11 | PUT | /api/v1/skills/{id} | Update skill |
| 12 | DELETE | /api/v1/skills/{id} | Delete skill |
| 13 | GET | /api/v1/interests/student/{id} | Get student interests |
| 14 | GET | /api/v1/interests/{id} | Get interest by ID |
| 15 | POST | /api/v1/interests | Create interest |
| 16 | PUT | /api/v1/interests/{id} | Update interest |
| 17 | DELETE | /api/v1/interests/{id} | Delete interest |
| 18 | GET | /api/v1/career-preferences/student/{id} | Get preferences |
| 19 | GET | /api/v1/career-preferences/{id} | Get preference by ID |
| 20 | POST | /api/v1/career-preferences | Create preference |
| 21 | PUT | /api/v1/career-preferences/{id} | Update preference |
| 22 | DELETE | /api/v1/career-preferences/{id} | Delete preference |
| 23 | POST | /api/v1/academic-profiles | Create profile |
| 24 | GET | /api/v1/academic-profiles/{id} | Get profile by ID |
| 25 | GET | /api/v1/academic-profiles/student/{id} | Get profile by student |
| 26 | PUT | /api/v1/academic-profiles/{id} | Update profile |
| 27 | DELETE | /api/v1/academic-profiles/{id} | Delete profile |
| 28 | POST | /api/v1/academic-profiles/{id}/subjects | Add subject mark |
| 29 | GET | /api/agents/available | Get available agents |
| 30 | POST | /api/agents/execute | Execute multiple agents |
| 31 | POST | /api/agents/execute/{type} | Execute single agent |
| 32 | POST | /api/agents/langgraph/execute/{id} | Execute LangGraph |
| 33 | POST | /api/agents/langgraph/parallel/{id} | Parallel execution |
| 34 | GET | /api/agents/simple/health | Health check |
| 35 | POST | /api/agents/simple/career-guide/{id} | Career guidance |
| 36 | GET | /health | App health check |

---

**Total Endpoints**: 39+ endpoints

**Last Updated**: February 21, 2026
