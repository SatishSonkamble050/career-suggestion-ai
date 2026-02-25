# API Quick Reference

## Health Check
```
GET /api/agents/simple/health
```
**Quick test**: `curl http://localhost:8000/api/agents/simple/health`

---

## Career Guidance Workflow
```
POST /api/agents/simple/career-guide/{student_id}
```

### Minimal Example
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

### Full Example
```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{
    "academic": {
      "gpa": 3.8,
      "major": "Computer Science",
      "subjects": ["AI", "ML"],
      "strong_areas": ["Programming"],
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
      "work_style": "Remote",
      "salary_range": "100k-150k",
      "location": "San Francisco",
      "career_growth": "Leadership",
      "impact": "Meaningful work",
      "learning": "Cutting-edge tech"
    }
  }'
```

---

## Response Format

```json
{
  "student_id": 1,
  "final_report": "Comprehensive career guidance..."
}
```

---

## Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Parse response |
| 400 | Bad Request | Check JSON format |
| 404 | Not Found | Verify student_id exists |
| 422 | Invalid Data | Check field names |
| 500 | Server Error | Check logs, retry |

---

## Python Examples

### Async (httpx)
```python
import httpx
import asyncio

async def get_guidance():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/simple/career-guide/1",
            json={
                "academic": {"gpa": 3.8},
                "skills": {"technical": ["Python"]},
                "interests": {"fields": ["AI"]},
                "preferences": {"salary_range": "100k-150k"}
            }
        )
        result = response.json()
        print(result["final_report"])

asyncio.run(get_guidance())
```

### Sync (requests)
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

result = response.json()
print(result["final_report"])
```

### With Error Handling
```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/agents/simple/career-guide/1",
        json={"academic": {"gpa": 3.8}},
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code} - {e.response.text}")
except requests.exceptions.ConnectionError:
    print("Connection failed - is the server running?")
except requests.exceptions.Timeout:
    print("Request timed out")
```

---

## Field Reference

### Academic
```json
{
  "gpa": 3.8,                      // GPA (0-4.0)
  "major": "Computer Science",     // Major name
  "minor": "Mathematics",          // Minor name (optional)
  "subjects": ["AI", "ML"],        // List of subjects
  "strong_areas": ["Programming"], // Strong areas
  "weak_areas": ["Public Speaking"] // Areas to improve
}
```

### Skills
```json
{
  "technical": ["Python", "JavaScript"], // Technical skills
  "soft": ["Leadership"],                 // Soft skills
  "certifications": ["AWS Developer"]     // Certifications
}
```

### Interests
```json
{
  "fields": ["AI", "Data Science"],      // Career fields
  "activities": ["Kaggle"],              // Activities
  "industries": ["Tech", "Finance"]      // Industries
}
```

### Preferences
```json
{
  "work_style": "Remote",           // Work environment
  "salary_range": "100k-150k",      // Salary expectation
  "location": "San Francisco",      // Location
  "career_growth": "Leadership",    // Growth goals
  "impact": "Meaningful work",      // Impact goals
  "learning": "Cutting-edge tech"   // Learning goals
}
```

---

## Testing Tools

### Browser
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Command Line
```bash
# Check if running
curl http://localhost:8000/api/agents/simple/health

# Full request
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{"academic":{"gpa":3.8}}'

# Save response to file
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d @request.json > response.json
```

### Postman
1. `POST` → `http://localhost:8000/api/agents/simple/career-guide/1`
2. Headers: `Content-Type: application/json`
3. Body (raw JSON): Copy from examples
4. Click Send

---

## Common Issues

| Issue | Solution |
|-------|----------|
| 404 Not Found | Student doesn't exist, check student_id |
| 422 Validation Error | Check JSON field names and types |
| 500 Server Error | Check .env (OPENAI_API_KEY), check logs |
| Slow response | Workflow takes 10-20s, that's normal |
| No API response | Server not running, check port 8000 |

---

## Performance Tips

1. **Response Time**: ~10-20 seconds per request
2. **Token Cost**: ~$0.01-0.10 per request
3. **Caching**: Cache responses for same student_id
4. **Batch**: Process multiple students sequentially
5. **Parallel**: Max ~5-10 concurrent requests

---

## Environment Setup

Required in `.env`:
```
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=sqlite:///./career_guidance.db
```

---

**Access full docs**: See `API_DOCUMENTATION.md`
