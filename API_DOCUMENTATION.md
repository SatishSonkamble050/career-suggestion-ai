# Career Guidance App - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
5. [Request/Response Models](#requestresponse-models)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Rate Limiting](#rate-limiting)

---

## Overview

The Career Guidance App API provides endpoints for managing student profiles and generating personalized career guidance using AI-powered multi-agent workflows.

**API Version**: 1.0.0  
**Framework**: FastAPI  
**Documentation URL**: `http://localhost:8000/docs` (Swagger UI)  
**ReDoc URL**: `http://localhost:8000/redoc` (ReDoc)

---

## Base URL

```
http://localhost:8000
```

For production, replace `localhost:8000` with your deployment server URL.

---

## Authentication

Currently, the API does not require authentication. In production, implement JWT or OAuth2.

Future versions will include:
- JWT Bearer tokens
- API key authentication
- Role-based access control

---

## Endpoints

### Simple LangGraph Workflow (Main Career Guidance)

#### 1. Health Check
```http
GET /api/agents/simple/health
```

**Description**: Verify the workflow service is running.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "simple_langgraph"
}
```

**Example**:
```bash
curl -X GET http://localhost:8000/api/agents/simple/health
```

---

#### 2. Execute Career Guidance Workflow
```http
POST /api/agents/simple/career-guide/{student_id}
```

**Description**: Generate comprehensive career guidance for a student.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `student_id` | integer | Unique student identifier |

**Request Body** (application/json):
```json
{
  "academic": {
    "gpa": 3.8,
    "major": "Computer Science",
    "minor": "Mathematics",
    "subjects": ["AI", "ML", "Data Structures"],
    "strong_areas": ["Programming", "Mathematics"],
    "weak_areas": ["Public Speaking"]
  },
  "skills": {
    "technical": ["Python", "JavaScript", "SQL"],
    "soft": ["Leadership", "Communication"],
    "certifications": ["AWS Developer"]
  },
  "interests": {
    "fields": ["AI", "Data Science"],
    "activities": ["Kaggle", "Open source"],
    "industries": ["Tech", "Finance"]
  },
  "preferences": {
    "work_style": "Remote with flexibility",
    "salary_range": "100k-150k",
    "location": "San Francisco",
    "career_growth": "Fast-paced learning",
    "impact": "Meaningful work",
    "learning": "Cutting-edge tech"
  }
}
```

**Response** (200 OK):
```json
{
  "student_id": 1,
  "academic_analysis": {
    "strengths": ["Strong in mathematics", "Excellent programming skills"],
    "areas_for_improvement": ["Presentation skills"],
    "gpa_analysis": "3.8 GPA indicates excellent academic performance",
    "subject_recommendations": ["Advanced ML", "Distributed Systems"]
  },
  "skill_analysis": {
    "current_skills": ["Python (Expert)", "JavaScript (Advanced)"],
    "proficiency_level": "Advanced",
    "skill_gaps": ["DevOps", "System Design"],
    "in_demand_skills": ["Docker", "Kubernetes", "Cloud Architecture"]
  },
  "interest_analysis": {
    "interest_clusters": ["AI/ML", "Data Science"],
    "preferred_industries": ["Tech", "Finance"],
    "career_directions": ["ML Engineer", "Data Scientist", "AI Research"],
    "passion_areas": ["Solving complex problems", "Cutting-edge technology"]
  },
  "preference_analysis": {
    "work_environment": "Remote with flexibility",
    "salary_expectations": "100k-150k",
    "work_life_balance": "Flexible schedule",
    "career_growth": "Fast-track to leadership",
    "location_preferences": "San Francisco Bay Area"
  },
  "market_analysis": {
    "in_demand_roles": ["ML Engineer", "Data Scientist", "AI Specialist"],
    "emerging_fields": ["Large Language Models", "Computer Vision"],
    "salary_outlook": "ML Engineers: $150k-250k average",
    "growth_trends": ["AI adoption", "Remote work increase"],
    "timing_recommendation": "Excellent time to specialize in AI/ML"
  },
  "final_report": "Based on your academic excellence (3.8 GPA), strong technical foundation, and passion for AI/ML, a career as a Machine Learning Engineer is highly recommended. [Full detailed report...]"
}
```

**Status Codes**:
| Code | Description |
|------|-------------|
| 200 | Success - Career guidance generated |
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Student not found |
| 422 | Validation Error - Invalid request format |
| 500 | Server Error - Workflow execution failed |

**Example cURL**:
```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {"gpa": 3.8, "major": "Computer Science"},
    "skills": {"technical": ["Python", "JavaScript"]},
    "interests": {"fields": ["AI", "Data Science"]},
    "preferences": {"work_style": "Remote", "salary_range": "100k-150k"}
  }'
```

**Example Python (httpx async)**:
```python
import httpx
import asyncio

async def get_guidance():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/simple/career-guide/1",
            json={
                "academic": {"gpa": 3.8, "major": "CS"},
                "skills": {"technical": ["Python"]},
                "interests": {"fields": ["AI"]},
                "preferences": {"salary_range": "100k-150k"}
            }
        )
        return response.json()

result = asyncio.run(get_guidance())
print(result["final_report"])
```

**Example Python (requests sync)**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/agents/simple/career-guide/1",
    json={
        "academic": {"gpa": 3.8},
        "skills": {"technical": ["Python"]},
        "interests": {"fields": ["AI"]},
        "preferences": {"salary_range": "100k-150k"}
    }
)
guidance = response.json()
print(guidance["final_report"])
```

---

## Request/Response Models

### CareerInput

Request model for career guidance workflow.

```python
class CareerInput(BaseModel):
    academic: Optional[Dict[str, Any]] = {}
    skills: Optional[Dict[str, Any]] = {}
    interests: Optional[Dict[str, Any]] = {}
    preferences: Optional[Dict[str, Any]] = {}
```

**Fields**:

#### academic (optional)
```json
{
  "gpa": 3.8,
  "major": "Computer Science",
  "minor": "Mathematics",
  "subjects": ["AI", "ML"],
  "strong_areas": ["Programming"],
  "weak_areas": ["Public Speaking"]
}
```

#### skills (optional)
```json
{
  "technical": ["Python", "JavaScript"],
  "soft": ["Leadership", "Communication"],
  "certifications": ["AWS Developer"]
}
```

#### interests (optional)
```json
{
  "fields": ["AI", "Data Science"],
  "activities": ["Kaggle", "Open source"],
  "industries": ["Tech", "Finance"]
}
```

#### preferences (optional)
```json
{
  "work_style": "Remote",
  "salary_range": "100k-150k",
  "location": "San Francisco",
  "career_growth": "Leadership",
  "impact": "Meaningful work",
  "learning": "Cutting-edge tech"
}
```

### WorkflowResponse

Response model from career guidance workflow.

```python
class WorkflowResponse(BaseModel):
    student_id: int
    academic_analysis: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    interest_analysis: Dict[str, Any]
    preference_analysis: Dict[str, Any]
    market_analysis: Dict[str, Any]
    final_report: str
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error description message"
}
```

### Common Error Codes

#### 400 Bad Request
Occurs when request data is invalid or malformed.

```json
{
  "detail": "Invalid request format"
}
```

#### 404 Not Found
Occurs when student doesn't exist in database.

```json
{
  "detail": "Student not found"
}
```

#### 422 Unprocessable Entity
Occurs when request validation fails.

```json
{
  "detail": "1 validation error for CareerInput\nfield (type_error.dict)"
}
```

#### 500 Internal Server Error
Occurs during workflow execution.

```json
{
  "detail": "Error executing workflow: OpenAI API rate limited"
}
```

---

## Examples

### Example 1: Minimal Request

```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {"gpa": 3.5}
  }'
```

Response (200):
```json
{
  "student_id": 1,
  "academic_analysis": {...},
  "skill_analysis": {...},
  "interest_analysis": {...},
  "preference_analysis": {...},
  "market_analysis": {...},
  "final_report": "Based on your profile..."
}
```

### Example 2: Comprehensive Profile

```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/2 \
  -H "Content-Type: application/json" \
  -d @profile.json
```

Where `profile.json` contains:
```json
{
  "academic": {
    "gpa": 3.9,
    "major": "Data Science",
    "minor": "Economics",
    "subjects": ["Machine Learning", "Statistics", "Deep Learning"],
    "strong_areas": ["Mathematics", "Programming"],
    "weak_areas": ["Networking"]
  },
  "skills": {
    "technical": ["Python (Expert)", "R (Advanced)", "SQL (Advanced)"],
    "soft": ["Problem Solving", "Communication"],
    "certifications": ["AWS ML", "Google Analytics"]
  },
  "interests": {
    "fields": ["AI", "Data Science", "Finance"],
    "activities": ["Kaggle", "Research"],
    "industries": ["Tech", "Finance", "Healthcare"]
  },
  "preferences": {
    "work_style": "Flexible remote",
    "salary_range": "120k-200k",
    "location": "San Francisco",
    "career_growth": "Leadership track",
    "impact": "Meaningful problems",
    "learning": "Cutting-edge AI"
  }
}
```

### Example 3: Error Handling

```bash
# Invalid JSON
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Response (400):
# {
#   "detail": "Invalid request format"
# }
```

```bash
# Student not found
curl -X POST http://localhost:8000/api/agents/simple/career-guide/99999 \
  -H "Content-Type: application/json" \
  -d '{}'

# Response (404):
# {
#   "detail": "Student not found"
# }
```

---

## Rate Limiting

**Current Status**: No rate limiting applied.

**Future Implementation**:
- 100 requests per minute per IP
- 1000 requests per hour per API key
- Retry-After headers on 429 responses

---

## Testing

### Using Swagger UI
Navigate to: `http://localhost:8000/docs`

All endpoints are interactive and can be tested directly from the browser.

### Using ReDoc
Navigate to: `http://localhost:8000/redoc`

Full API reference documentation.

### Using Postman
1. Import collection from `/postman_collection.json`
2. Set `base_url` variable to `http://localhost:8000`
3. Run requests individually or create test suite

### Using cURL
```bash
# Test health
curl http://localhost:8000/api/agents/simple/health

# Test full workflow
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{"academic":{"gpa":3.8}}'
```

---

## Performance

### Response Times
- Health Check: < 100ms
- Full Workflow: 10-20 seconds (depends on LLM)

### Token Usage
- Per Request: 2,000-4,000 tokens
- Cost: ~$0.01-0.10 per request (with gpt-3.5-turbo)

### Scalability
- Current: Single instance
- Recommended Load: < 100 concurrent requests
- Limitation: OpenAI API rate limits

---

## Best Practices

#### Request Format
✅ **DO**: Provide as much data as possible for better analysis
✅ **DO**: Use specific field names matching the model
✅ **DO**: Send valid JSON

❌ **DON'T**: Use null values - omit fields instead
❌ **DON'T**: Send empty arrays
❌ **DON'T**: Include sensitive information (passwords, SSNs)

#### Error Handling
✅ **DO**: Implement retry logic with exponential backoff
✅ **DO**: Check HTTP status codes
✅ **DO**: Log error responses

❌ **DON'T**: Ignore 5xx errors
❌ **DON'T**: Assume success without checking status
❌ **DON'T**: Make too many rapid requests

---

## Troubleshooting

### API Not Responding
```bash
# Check if server is running
curl http://localhost:8000/api/agents/simple/health

# Check logs for errors
# Windows: Check terminal output where you ran uvicorn
```

### 500 Error on Workflow Request
**Possible causes**:
1. OpenAI API key not configured
2. Student ID doesn't exist in database
3. OpenAI API rate limited
4. Database connection issue

**Fix**:
```bash
# Verify .env configuration
# Check OPENAI_API_KEY is set
# Check database connection
# Check database contains student record
```

### Slow Response Times
**Possible causes**:
1. Using slower LLM model (gpt-4)
2. Large input data
3. OpenAI API latency
4. Network issues

**Fix**:
1. Use faster model: `gpt-3.5-turbo`
2. Reduce input data complexity
3. Check network connectivity
4. Implement caching for repeated requests

---

## Support

For issues, questions, or feedback:
1. Check API logs: `uvicorn main:app --log-level debug`
2. Visit Swagger docs: `http://localhost:8000/docs`
3. Review error messages carefully
4. Check configuration in `.env`

---

## Changelog

### v1.0.0 (Current)
- ✅ Simple LangGraph workflow
- ✅ Career guidance endpoint
- ✅ Health check endpoint
- ✅ Error handling
- ✅ Async execution

### v1.1.0 (Planned)
- 🔄 Authentication (JWT)
- 🔄 Rate limiting
- 🔄 Request caching
- 🔄 Batch processing
- 🔄 Webhook notifications

---

## License

Same as parent project

---

**Last Updated**: February 21, 2026  
**Status**: Production Ready ✅
