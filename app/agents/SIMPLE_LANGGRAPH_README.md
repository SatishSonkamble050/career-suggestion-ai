# Simple LangGraph Workflow - Complete Guide

## Overview

The Simple LangGraph Workflow is a clean, minimal implementation of multi-agent career guidance using LangGraph's StateGraph pattern. It provides sequential processing of student career data through 6 specialized agents that analyze different aspects of a student's profile.

## Architecture

```
CareerGuidanceState (TypedDict)
    ↓
Academic Agent → Skill Agent → Interest Agent → Preference Agent → Market Agent → Report Agent → END
    ↓
WorkflowResponse (Final Output)
```

### Quick Facts
- **Framework**: LangGraph + LangChain
- **Agents**: 6 specialized (Academic, Skill, Interest, Preference, Market, Report)
- **Execution**: Sequential with state accumulation
- **State Management**: TypedDict-based immutable state
- **LLM**: ChatOpenAI (configurable model, default: gpt-3.5-turbo)

---

## Quick Start

### 1. Health Check

```bash
curl -X GET http://localhost:8000/api/agents/simple/health
```

### 2. Basic Request

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

### 3. Python Usage

```python
from app.agents.simple_langgraph import SimpleLangGraphWorkflow
from app.core.database import SessionLocal

db = SessionLocal()
workflow = SimpleLangGraphWorkflow(db)

result = await workflow.execute(
    student_id=1,
    input_data={
        "academic": {"gpa": 3.8},
        "skills": {"technical": ["Python"]},
        "interests": {"fields": ["AI"]},
        "preferences": {"salary_range": "100k-150k"}
    }
)

print(result["final_report"])
```

---

## Detailed Usage

### API Endpoint

```
POST /api/agents/simple/career-guide/{student_id}
```

### Request Body

```json
{
  "academic": {
    "gpa": 3.8,
    "major": "Computer Science",
    "minor": "Mathematics",
    "subjects": ["AI", "ML", "Data Structures"],
    "strong_areas": ["Programming", "Math"],
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

**Note**: All fields are optional. Provide what data you have.

### Response Format

```json
{
  "student_id": 1,
  "academic_analysis": "Analysis of academic profile including GPA, major, and subjects...",
  "skill_analysis": "Assessment of technical and soft skills...",
  "interest_analysis": "Evaluation of career interests and fields...",
  "preference_analysis": "Review of career preferences and goals...",
  "market_analysis": "Analysis of job market opportunities...",
  "final_report": "Comprehensive career guidance report with specific recommendations and next steps..."
}
```

---

## Workflow Details

### State Management

The workflow uses `CareerGuidanceState` TypedDict:

```python
class CareerGuidanceState(TypedDict):
    student_id: int
    input_data: Dict[str, Any]
    academic_analysis: str
    skill_analysis: str
    interest_analysis: str
    preference_analysis: str
    market_analysis: str
    final_report: str
```

Each agent reads the current state and updates it with their analysis.

### Agent Sequence

#### 1. **Academic Agent**
- Analyzes GPA, major, subjects, and academic strengths/weaknesses
- Generates academic profile assessment
- Updates state with `academic_analysis`

#### 2. **Skill Agent**
- Evaluates technical and soft skills
- Assesses certifications and expertise level
- Updates state with `skill_analysis`
- Receives and builds on `academic_analysis`

#### 3. **Interest Agent**
- Assesses career field interests
- Evaluates industry preferences
- Identifies alignment with academic/skill profile
- Updates state with `interest_analysis`

#### 4. **Preference Agent**
- Reviews work style preferences
- Evaluates salary expectations
- Assesses career growth and impact goals
- Updates state with `preference_analysis`

#### 5. **Market Agent**
- Analyzes job market opportunities
- Identifies in-demand roles matching profile
- Evaluates market trends
- Updates state with `market_analysis`

#### 6. **Report Agent**
- Synthesizes all previous analyses
- Generates comprehensive career guidance
- Provides actionable recommendations
- Updates state with `final_report`

---

## Implementation Details

### File Structure

```
app/
├── agents/
│   ├── simple_langgraph.py           # Core workflow implementation
│   ├── simple_langgraph_examples.py  # Usage examples (5 examples)
│   └── SIMPLE_WORKFLOW_GUIDE.py      # Reference guide with cURL examples
├── api/
│   └── routes/
│       └── simple_langgraph.py       # FastAPI router and endpoints
└── core/
    └── database.py                   # Database connection
```

### Core Classes

#### SimpleLangGraphWorkflow

```python
class SimpleLangGraphWorkflow:
    def __init__(self, db: Session, model: str = "gpt-3.5-turbo"):
        """Initialize workflow with database and LLM model"""
    
    async def execute(self, student_id: int, input_data: Dict) -> Dict:
        """Execute the workflow and return results"""
    
    def _build_graph(self) -> Runnable:
        """Build the StateGraph with all nodes and edges"""
```

### LLM Configuration

- **Model**: Configurable (default: gpt-3.5-turbo)
- **Temperature**: 0.3 (factual, deterministic)
- **JSON Parsing**: Built-in with fallback to raw content

---

## Examples

### Example 1: Minimal Input

```python
workflow = SimpleLangGraphWorkflow(db)

result = await workflow.execute(
    student_id=1,
    input_data={
        "academic": {"gpa": 3.5, "major": "Engineering"},
        "skills": {"technical": ["Python", "CAD"]},
        "interests": {"fields": ["Robotics"]},
        "preferences": {"work_style": "Hands-on"}
    }
)

print(result["final_report"])
```

### Example 2: Comprehensive Profile

See `simple_langgraph_examples.py` for detailed example with full student profile.

### Example 3: Batch Processing

Process multiple students:

```python
students = [
    {"id": 1, "data": {...}},
    {"id": 2, "data": {...}}
]

for student in students:
    result = await workflow.execute(student["id"], student["data"])
    print(result["final_report"])
```

### Example 4: HTTP API

```bash
curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d @student_profile.json
```

---

## API Reference

### Endpoints

#### Health Check
```
GET /api/agents/simple/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Simple LangGraph workflow is running"
}
```

#### Execute Workflow
```
POST /api/agents/simple/career-guide/{student_id}
```

Query Parameters:
- `student_id` (path, required): Student ID

Request Body:
- All fields optional in CareerInput

Response:
```json
{
  "student_id": int,
  "academic_analysis": string,
  "skill_analysis": string,
  "interest_analysis": string,
  "preference_analysis": string,
  "market_analysis": string,
  "final_report": string
}
```

Errors:
- 404: Student not found
- 422: Invalid request data
- 500: Server error

---

## Best Practices

### Do's ✓
- Provide as much detail as possible for better recommendations
- Include both technical and soft skills for comprehensive analysis
- List specific subjects/areas for more targeted guidance
- Specify industries of interest for better market analysis
- Set clear preferences for personalized recommendations
- Run health check before making requests

### Don'ts ✗
- Don't use null values - just omit fields
- Don't include fields with empty arrays
- Don't worry about field order - any order works
- Don't assume all fields are required - they're optional

---

## Performance

### Execution Time
- **Average**: 10-15 seconds (depends on LLM response time)
- **Factors**: Model speed, API latency, complexity of analysis

### Token Usage
- **Per Request**: Varies by input size and analysis depth
- **Typical**: 2,000-4,000 tokens per full analysis

### Optimization Tips
- Use faster models (gpt-3.5-turbo) for real-time responses
- Use more capable models (gpt-4o-mini) for better analysis
- Cache results for same student_id to avoid duplicate processing

---

## Troubleshooting

### Issue: 404 Not Found
**Solution**: Ensure student exists in database or use valid student_id

### Issue: 422 Unprocessable Entity
**Solution**: Check JSON format and field names match CareerInput schema

### Issue: 500 Internal Server Error
**Solution**: 
- Check if OpenAI API key is configured
- Verify database connection
- Check logs for detailed error message

### Issue: Slow Response
**Solution**:
- Use faster model (gpt-3.5-turbo)
- Check OpenAI API status
- Reduce input data complexity

---

## Configuration

### Model Selection

```python
# Default (gpt-3.5-turbo)
workflow = SimpleLangGraphWorkflow(db)

# GPT-4 (slower but more accurate)
workflow = SimpleLangGraphWorkflow(db, model="gpt-4o-mini")

# Custom temperature (0-1, default 0.3)
# Edit simple_langgraph.py line: self.llm = ChatOpenAI(...)
```

### Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `DATABASE_URL`: Database connection string
- `OPENAI_MODEL`: Default LLM model

---

## Integration with Existing Systems

### With Basic Student Routes
```python
# Get student data
student = requests.get(f"http://localhost:8000/api/students/{student_id}")

# Use in workflow
result = await workflow.execute(student_id, {...})
```

### With FastAPI App
The router automatically registered in `app/main.py`:
```python
from app.api.routes import simple_langgraph
app.include_router(simple_langgraph.router)
```

### DataBase Integration
Uses existing SQLAlchemy ORM:
```python
db = SessionLocal()
workflow = SimpleLangGraphWorkflow(db)
```

---

## Files for Reference

1. **Core Implementation**: [app/agents/simple_langgraph.py](app/agents/simple_langgraph.py)
2. **API Routes**: [app/api/routes/simple_langgraph.py](app/api/routes/simple_langgraph.py)
3. **Examples**: [app/agents/simple_langgraph_examples.py](app/agents/simple_langgraph_examples.py)
4. **Reference Guide**: [app/agents/SIMPLE_WORKFLOW_GUIDE.py](app/agents/SIMPLE_WORKFLOW_GUIDE.py)

---

## Support & Debugging

### Enable Detailed Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### View Request/Response

```bash
curl -v -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### Test with Sample Data

See `SIMPLE_WORKFLOW_GUIDE.py` for sample JSON requests and cURL examples.

---

## Next Steps

1. ✅ Start with health check: `GET /api/agents/simple/health`
2. ✅ Try basic example with minimal data
3. ✅ Expand with comprehensive profile
4. ✅ Integrate with your UI/application
5. ✅ Monitor performance and optimize as needed

---

## Version Information

- **LangGraph**: 0.0.23+
- **LangChain**: 0.1.1+
- **OpenAI**: 1.3.0+
- **FastAPI**: 0.104.1+
- **Python**: 3.8+

---

## License

Same as parent project

---

## Questions?

Refer to:
- `SIMPLE_WORKFLOW_GUIDE.py` for cURL examples
- `simple_langgraph_examples.py` for Python examples
- Core implementation: `simple_langgraph.py`
- API routes: `app/api/routes/simple_langgraph.py`
