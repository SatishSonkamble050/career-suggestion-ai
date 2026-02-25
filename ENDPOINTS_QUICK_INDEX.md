# Endpoints Quick Index

## 📋 All Endpoints at a Glance

### 🔐 Authentication (2)
- POST `/api/v1/auth/register` - Register
- POST `/api/v1/auth/login` - Login

### 👥 Students (5)
- GET `/api/v1/students` - List all
- GET `/api/v1/students/{id}` - Get one
- POST `/api/v1/students` - Create
- PUT `/api/v1/students/{id}` - Update
- DELETE `/api/v1/students/{id}` - Delete

### 💼 Skills (5)
- GET `/api/v1/skills/student/{id}` - Get student skills
- GET `/api/v1/skills/{id}` - Get one skill
- POST `/api/v1/skills` - Create
- PUT `/api/v1/skills/{id}` - Update
- DELETE `/api/v1/skills/{id}` - Delete

### 🎯 Interests (5)
- GET `/api/v1/interests/student/{id}` - Get student interests
- GET `/api/v1/interests/{id}` - Get one interest
- POST `/api/v1/interests` - Create
- PUT `/api/v1/interests/{id}` - Update
- DELETE `/api/v1/interests/{id}` - Delete

### 🚀 Career Preferences (5)
- GET `/api/v1/career-preferences/student/{id}` - Get student preferences
- GET `/api/v1/career-preferences/{id}` - Get one preference
- POST `/api/v1/career-preferences` - Create
- PUT `/api/v1/career-preferences/{id}` - Update
- DELETE `/api/v1/career-preferences/{id}` - Delete

### 📚 Academic Profiles (6)
- POST `/api/v1/academic-profiles` - Create
- GET `/api/v1/academic-profiles/{id}` - Get by ID
- GET `/api/v1/academic-profiles/student/{id}` - Get by student
- PUT `/api/v1/academic-profiles/{id}` - Update
- DELETE `/api/v1/academic-profiles/{id}` - Delete
- POST `/api/v1/academic-profiles/{id}/subjects` - Add subject

### 🤖 AI Agents (5)
- GET `/api/agents/available` - List agents
- POST `/api/agents/execute` - Multiple agents
- POST `/api/agents/execute/{type}` - Single agent
- POST `/api/agents/langgraph/execute/{id}` - LangGraph
- POST `/api/agents/langgraph/parallel/{id}` - Parallel

### 🎓 Simple LangGraph (2)
- GET `/api/agents/simple/health` - Health check
- POST `/api/agents/simple/career-guide/{id}` - Career guidance

### 🏥 System (3)
- GET `/health` - Health
- GET `/docs` - Swagger UI
- GET `/redoc` - ReDoc

---

## 🔍 Search by Use Case

### Create New Student Profile
```bash
# 1. Register/Create student
POST /api/v1/students
POST /api/v1/auth/register

# 2. Create academic profile
POST /api/v1/academic-profiles

# 3. Add skills
POST /api/v1/skills (multiple times)

# 4. Add interests
POST /api/v1/interests (multiple times)

# 5. Add career preferences
POST /api/v1/career-preferences (multiple times)
```

### Get Full Student Profile
```bash
# 1. Get student info
GET /api/v1/students/{student_id}

# 2. Get academic profile
GET /api/v1/academic-profiles/student/{student_id}

# 3. Get all skills
GET /api/v1/skills/student/{student_id}

# 4. Get all interests
GET /api/v1/interests/student/{student_id}

# 5. Get all preferences
GET /api/v1/career-preferences/student/{student_id}
```

### Generate Career Guidance
```bash
# Option 1: Simple LangGraph (Recommended)
POST /api/agents/simple/career-guide/{student_id}

# Option 2: Advanced LangGraph
POST /api/agents/langgraph/execute/{student_id}

# Option 3: Parallel Agents
POST /api/agents/langgraph/parallel/{student_id}

# Option 4: Individual Agents
POST /api/agents/execute/career_recommender?student_id={id}
POST /api/agents/execute/skill_analyzer?student_id={id}
POST /api/agents/execute/interest_evaluator?student_id={id}
POST /api/agents/execute/academic_counselor?student_id={id}
POST /api/agents/execute/job_market_analyst?student_id={id}
```

### Update Student Information
```bash
# 1. Update basic info
PUT /api/v1/students/{student_id}

# 2. Update academic profile
PUT /api/v1/academic-profiles/{profile_id}

# 3. Update a skill
PUT /api/v1/skills/{skill_id}

# 4. Update an interest
PUT /api/v1/interests/{interest_id}

# 5. Update a preference
PUT /api/v1/career-preferences/{preference_id}
```

### Delete Student Data
```bash
# 1. Delete specific skill
DELETE /api/v1/skills/{skill_id}

# 2. Delete specific interest
DELETE /api/v1/interests/{interest_id}

# 3. Delete specific preference
DELETE /api/v1/career-preferences/{preference_id}

# 4. Delete academic profile
DELETE /api/v1/academic-profiles/{profile_id}

# 5. Delete student (cascades all related data)
DELETE /api/v1/students/{student_id}
```

---

## 📊 Endpoint Statistics

| Category | Count | Total |
|----------|-------|-------|
| Auth | 2 | 2 |
| Students | 5 | 7 |
| Skills | 5 | 12 |
| Interests | 5 | 17 |
| Preferences | 5 | 22 |
| Academic | 6 | 28 |
| Agents | 5 | 33 |
| LangGraph | 2 | 35 |
| System | 3 | 38 |

**Total Active Endpoints**: 38+

---

## 🚀 Common Workflows

### Workflow 1: New Student Setup (10 requests)
```
1. POST /api/v1/auth/register        → Get student_id
2. POST /api/v1/academic-profiles    → Create profile
3. POST /api/v1/skills               → Add skill #1
4. POST /api/v1/skills               → Add skill #2
5. POST /api/v1/skills               → Add skill #3
6. POST /api/v1/interests            → Add interest #1
7. POST /api/v1/interests            → Add interest #2
8. POST /api/v1/career-preferences   → Add preference #1
9. POST /api/v1/career-preferences   → Add preference #2
10. POST /api/agents/simple/career-guide/{id} → Get guidance
```

### Workflow 2: Student Profile Review (5 requests)
```
1. GET /api/v1/students/{id}
2. GET /api/v1/academic-profiles/student/{id}
3. GET /api/v1/skills/student/{id}
4. GET /api/v1/interests/student/{id}
5. GET /api/v1/career-preferences/student/{id}
```

### Workflow 3: Career Analysis (3 requests)
```
1. PUT /api/v1/students/{id}                              → Update info
2. PUT /api/v1/academic-profiles/{profile_id}            → Update academics
3. POST /api/agents/simple/career-guide/{student_id}     → Get new guidance
```

---

## 🔗 Quick Links

- **Full Documentation**: [ALL_ENDPOINTS.md](ALL_ENDPOINTS.md)
- **API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Quick Reference**: [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)
- **Interactive Docs**: `http://localhost:8000/docs`

---

## 💡 Tips

### Fastest Setup
Use cURL with pre-saved JSON files:
```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d @student.json
```

### Testing Multiple Endpoints
Use Swagger UI at `http://localhost:8000/docs` - interactive and no CLI needed.

### Batch Operations
Process multiple students by storing student IDs and iterating:
```bash
for id in 1 2 3 4 5; do
  curl http://localhost:8000/api/v1/students/$id
done
```

### Error Debugging
Always check response status codes and error messages:
```bash
curl -i -X GET http://localhost:8000/api/v1/students/99999
# Look for 404 Not Found if student doesn't exist
```

---

**Version**: 1.0 | **Last Updated**: February 21, 2026
