# API Endpoints Command Reference

Copy and paste ready commands for all endpoints.

---

## Authentication Commands

### Register Student
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "grade_level": 12,
    "gpa": 3.8
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

---

## Student Management Commands

### Get All Students
```bash
curl -X GET "http://localhost:8000/api/v1/students?skip=0&limit=10"
```

### Get Student by ID
```bash
curl -X GET http://localhost:8000/api/v1/students/1
```

### Create Student
```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "SecurePass456",
    "grade_level": 11,
    "gpa": 3.5
  }'
```

### Update Student
```bash
curl -X PUT http://localhost:8000/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "grade_level": 13,
    "gpa": 3.9
  }'
```

### Delete Student
```bash
curl -X DELETE http://localhost:8000/api/v1/students/1
```

---

## Skills Commands

### Get Student Skills
```bash
curl -X GET http://localhost:8000/api/v1/skills/student/1
```

### Get Skill by ID
```bash
curl -X GET http://localhost:8000/api/v1/skills/1
```

### Create Skill
```bash
curl -X POST http://localhost:8000/api/v1/skills \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "skill_name": "Python",
    "proficiency_level": 95,
    "description": "Expert level programmer"
  }'
```

### Update Skill
```bash
curl -X PUT http://localhost:8000/api/v1/skills/1 \
  -H "Content-Type: application/json" \
  -d '{
    "proficiency_level": 98,
    "description": "Master level Python developer"
  }'
```

### Delete Skill
```bash
curl -X DELETE http://localhost:8000/api/v1/skills/1
```

---

## Interests Commands

### Get Student Interests
```bash
curl -X GET http://localhost:8000/api/v1/interests/student/1
```

### Get Interest by ID
```bash
curl -X GET http://localhost:8000/api/v1/interests/1
```

### Create Interest
```bash
curl -X POST http://localhost:8000/api/v1/interests \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "interest_area": "Artificial Intelligence",
    "intensity_level": 95,
    "description": "Passionate about AI research"
  }'
```

### Update Interest
```bash
curl -X PUT http://localhost:8000/api/v1/interests/1 \
  -H "Content-Type: application/json" \
  -d '{
    "intensity_level": 90,
    "description": "Very interested in ML applications"
  }'
```

### Delete Interest
```bash
curl -X DELETE http://localhost:8000/api/v1/interests/1
```

---

## Career Preferences Commands

### Get Student Preferences
```bash
curl -X GET http://localhost:8000/api/v1/career-preferences/student/1
```

### Get Preference by ID
```bash
curl -X GET http://localhost:8000/api/v1/career-preferences/1
```

### Create Preference
```bash
curl -X POST http://localhost:8000/api/v1/career-preferences \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "career_path": "Machine Learning Engineer",
    "match_score": 92,
    "reasoning": "Perfect fit based on skills and interests"
  }'
```

### Update Preference
```bash
curl -X PUT http://localhost:8000/api/v1/career-preferences/1 \
  -H "Content-Type: application/json" \
  -d '{
    "match_score": 95,
    "reasoning": "Excellent career fit"
  }'
```

### Delete Preference
```bash
curl -X DELETE http://localhost:8000/api/v1/career-preferences/1
```

---

## Academic Profile Commands

### Create Academic Profile
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
      {"subject_name": "Mathematics", "marks": 95},
      {"subject_name": "Physics", "marks": 88},
      {"subject_name": "Chemistry", "marks": 90}
    ]
  }'
```

### Get Academic Profile by ID
```bash
curl -X GET http://localhost:8000/api/v1/academic-profiles/1
```

### Get Profile by Student ID
```bash
curl -X GET http://localhost:8000/api/v1/academic-profiles/student/1
```

### Update Academic Profile
```bash
curl -X PUT http://localhost:8000/api/v1/academic-profiles/1 \
  -H "Content-Type: application/json" \
  -d '{
    "result": "Excellent",
    "strongest_subject": "Physics"
  }'
```

### Delete Academic Profile
```bash
curl -X DELETE http://localhost:8000/api/v1/academic-profiles/1
```

### Add Subject Mark
```bash
curl -X POST http://localhost:8000/api/v1/academic-profiles/1/subjects \
  -H "Content-Type: application/json" \
  -d '{
    "subject_name": "Computer Science",
    "marks": 92
  }'
```

---

## AI Agents Commands

### Get Available Agents
```bash
curl -X GET http://localhost:8000/api/agents/available
```

### Execute Multiple Agents
```bash
curl -X POST http://localhost:8000/api/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "agents": [
      "career_recommender",
      "skill_analyzer",
      "interest_evaluator"
    ]
  }'
```

### Execute Career Recommender Agent
```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1"
```

### Execute Skill Analyzer Agent
```bash
curl -X POST "http://localhost:8000/api/agents/execute/skill_analyzer?student_id=1"
```

### Execute Interest Evaluator Agent
```bash
curl -X POST "http://localhost:8000/api/agents/execute/interest_evaluator?student_id=1"
```

### Execute Academic Counselor Agent
```bash
curl -X POST "http://localhost:8000/api/agents/execute/academic_counselor?student_id=1"
```

### Execute Job Market Analyst Agent
```bash
curl -X POST "http://localhost:8000/api/agents/execute/job_market_analyst?student_id=1"
```

---

## LangGraph Workflow Commands

### Execute LangGraph Workflow
```bash
curl -X POST http://localhost:8000/api/agents/langgraph/execute/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {
      "gpa": 3.8,
      "major": "Computer Science",
      "subjects": ["AI", "ML"]
    },
    "skills": {
      "technical": ["Python", "JavaScript"]
    },
    "interests": {
      "fields": ["AI", "Data Science"]
    },
    "preferences": {
      "work_style": "Remote",
      "salary_range": "100k-150k"
    }
  }'
```

### Execute Parallel Workflow
```bash
curl -X POST http://localhost:8000/api/agents/langgraph/parallel/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {"gpa": 3.8},
    "skills": {"technical": ["Python"]},
    "interests": {"fields": ["AI"]},
    "preferences": {"salary_range": "100k-150k"}
  }'
```

---

## Simple LangGraph Workflow Commands

### Health Check
```bash
curl -X GET http://localhost:8000/api/agents/simple/health
```

### Career Guidance - Minimal Request
```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {"gpa": 3.8}
  }'
```

### Career Guidance - Full Request
```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {
      "gpa": 3.9,
      "major": "Data Science",
      "subjects": ["ML", "Statistics"],
      "strong_areas": ["Math"],
      "weak_areas": ["Speaking"]
    },
    "skills": {
      "technical": ["Python", "R", "SQL"],
      "soft": ["Communication"],
      "certifications": ["AWS ML"]
    },
    "interests": {
      "fields": ["AI", "Data Science"],
      "activities": ["Kaggle", "Research"],
      "industries": ["Tech", "Finance"]
    },
    "preferences": {
      "work_style": "Remote",
      "salary_range": "120k-200k",
      "location": "San Francisco",
      "career_growth": "Leadership",
      "impact": "Meaningful work",
      "learning": "Cutting-edge tech"
    }
  }'
```

---

## System Commands

### App Health Check
```bash
curl -X GET http://localhost:8000/health
```

### Get OpenAPI Schema
```bash
curl -X GET http://localhost:8000/openapi.json
```

### Open Swagger UI
```bash
# Open in browser
http://localhost:8000/docs
```

### Open ReDoc
```bash
# Open in browser
http://localhost:8000/redoc
```

---

## Useful Bash Scripts

### Create Complete Student Profile
```bash
#!/bin/bash

STUDENT_ID=1
NAME="John Doe"
EMAIL="john@example.com"
PASSWORD="SecurePass123"

# Register student
echo "Creating student..."
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'$NAME'",
    "email": "'$EMAIL'",
    "password": "'$PASSWORD'",
    "grade_level": 12,
    "gpa": 3.8
  }'

echo "\nCreating academic profile..."
curl -X POST http://localhost:8000/api/v1/academic-profiles \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": '$STUDENT_ID',
    "stream": "Science",
    "current_class": "12th",
    "result": "Pass",
    "strongest_subject": "Math",
    "weakest_subject": "PE"
  }'

echo "\nAdding skills..."
curl -X POST http://localhost:8000/api/v1/skills \
  -H "Content-Type: application/json" \
  -d '{"student_id": '$STUDENT_ID', "skill_name": "Python", "proficiency_level": 95}'

echo "\nAdding interests..."
curl -X POST http://localhost:8000/api/v1/interests \
  -H "Content-Type: application/json" \
  -d '{"student_id": '$STUDENT_ID', "interest_area": "AI", "intensity_level": 95}'

echo "\nGetting career guidance..."
curl -X POST http://localhost:8000/api/agents/simple/career-guide/$STUDENT_ID \
  -H "Content-Type: application/json" \
  -d '{"academic": {"gpa": 3.8}}'
```

### Get Full Student Data
```bash
#!/bin/bash

STUDENT_ID=1

echo "Getting student info..."
curl -X GET http://localhost:8000/api/v1/students/$STUDENT_ID

echo "\n\nGetting academic profile..."
curl -X GET http://localhost:8000/api/v1/academic-profiles/student/$STUDENT_ID

echo "\n\nGetting skills..."
curl -X GET http://localhost:8000/api/v1/skills/student/$STUDENT_ID

echo "\n\nGetting interests..."
curl -X GET http://localhost:8000/api/v1/interests/student/$STUDENT_ID

echo "\n\nGetting preferences..."
curl -X GET http://localhost:8000/api/v1/career-preferences/student/$STUDENT_ID
```

### Test All Endpoints
```bash
#!/bin/bash

echo "=== Testing All Endpoints ==="

echo "\n1. Health Check"
curl -s http://localhost:8000/health | jq .

echo "\n2. Available Agents"
curl -s http://localhost:8000/api/agents/available | jq .

echo "\n3. Get All Students"
curl -s http://localhost:8000/api/v1/students | jq .

echo "\n4. Simple LangGraph Health"
curl -s http://localhost:8000/api/agents/simple/health | jq .

echo "\n=== Done ==="
```

---

## Using with Postman/Thunder Client

### Import as Environment Variable
```json
{
  "base_url": "http://localhost:8000",
  "student_id": "1"
}
```

### Save Requests Template
```
{{base_url}}/api/v1/students/{{student_id}}
{{base_url}}/api/v1/skills/student/{{student_id}}
{{base_url}}/api/agents/simple/career-guide/{{student_id}}
```

---

## Python HTTPx Examples

### Install
```bash
pip install httpx
```

### Async Example
```python
import httpx
import asyncio

async def test_endpoints():
    async with httpx.AsyncClient() as client:
        # Register student
        r = await client.post(
            "http://localhost:8000/api/v1/auth/register",
            json={
                "name": "John",
                "email": "john@example.com",
                "password": "pass",
                "grade_level": 12,
                "gpa": 3.8
            }
        )
        print("Register:", r.status_code)
        
        # Get all students
        r = await client.get("http://localhost:8000/api/v1/students")
        print("Students:", r.json())
        
        # Career guidance
        r = await client.post(
            "http://localhost:8000/api/agents/simple/career-guide/1",
            json={"academic": {"gpa": 3.8}}
        )
        print("Guidance:", r.json()["final_report"][:100] + "...")

asyncio.run(test_endpoints())
```

---

## Important Notes

1. **Replace Port**: If using different port, replace `8000` with your port
2. **Replace Host**: If deployed, replace `localhost` with your server IP/domain
3. **Replace IDs**: Replace `1` with actual student IDs
4. **Add Headers**: Some endpoints may require authentication headers
5. **JSON Format**: Always include `-H "Content-Type: application/json"`

---

**Version**: 1.0 | **Last Updated**: February 21, 2026
