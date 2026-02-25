# Multi-Agent System Implementation Guide

## Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload
```

4. **Access API documentation:**
Open `http://localhost:8000/docs` in your browser

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────── Agent Orchestrator ────────────────┐   │
│  │                    (LangGraph)                         │   │
│  │                                                        │   │
│  │  ┌─────────────┬──────────────┬─────────────────┐    │   │
│  │  │   Career    │    Skill     │   Interest      │    │   │
│  │  │Recommender  │   Analyzer   │   Evaluator     │    │   │
│  │  │   Agent     │   Agent      │   Agent         │    │   │
│  │  └─────────────┴──────────────┴─────────────────┘    │   │
│  │                                                        │   │
│  │  ┌─────────────────────┬──────────────────────┐      │   │
│  │  │   Academic          │   Job Market         │      │   │
│  │  │   Counselor         │   Analyst            │      │   │
│  │  │   Agent             │   Agent              │      │   │
│  │  └─────────────────────┴──────────────────────┘      │   │
│  │                                                        │   │
│  │  ┌────────────────────────────────────────────┐      │   │
│  │  │         Agent Tools & Utilities            │      │   │
│  │  │  • Student Profile • Skills Analysis       │      │   │
│  │  │  • Interest Mapping • Market Trends        │      │   │
│  │  │  • Learning Paths  • Gap Analysis          │      │   │
│  │  └────────────────────────────────────────────┘      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌────────────────────── API Routes ──────────────────┐    │
│  │  POST /api/agents/execute                         │    │
│  │  POST /api/agents/career-guidance/{id}            │    │
│  │  GET  /api/agents/available                       │    │
│  │  GET  /api/agents/conversation/{id}               │    │
│  └───────────────────────────────────────────────────┘    │
│                                                               │
│  ┌────────────────────── Database ────────────────────┐    │
│  │  • Students • Skills • Interests • Preferences     │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Agents Overview

### 1. Career Recommender Agent

**Purpose:** Generate personalized career recommendations

**Input:**
- Student ID
- Student profile (skills, interests, GPA)
- Career preferences

**Process:**
- Analyzes skills and interests
- Matches with career requirements
- Considers market demand

**Output:**
- Top 3-5 recommended careers
- Alignment reasoning
- Required skills
- Salary expectations
- Next steps

**Example:**
```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1"
```

### 2. Skill Analyzer Agent

**Purpose:** Assess skills and identify development areas

**Input:**
- Student ID
- Target career (optional)

**Process:**
- Evaluates current skills
- Identifies skill gaps
- Prioritizes learning areas

**Output:**
- Skill proficiency report
- Gaps vs target career
- Development recommendations
- Priority ranking

**Example:**
```bash
curl -X POST "http://localhost:8000/api/agents/execute/skill_analyzer?student_id=1&target_career=Software%20Engineer"
```

### 3. Interest Evaluator Agent

**Purpose:** Match interests with suitable careers

**Input:**
- Student ID
- Current interests
- Skills

**Process:**
- Analyzes interest patterns
- Matches with career fields
- Identifies emerging opportunities

**Output:**
- Interest pattern analysis
- Matching career fields
- Exploration activities
- Industry growth trends

**Example:**
```bash
curl -X POST "http://localhost:8000/api/agents/execute/interest_evaluator?student_id=1"
```

### 4. Academic Counselor Agent

**Purpose:** Provide academic planning guidance

**Input:**
- Student ID
- Academic profile
- Career goals
- Current performance

**Process:**
- Analyzes academic record
- Recommends courses
- Plans academic milestone

**Output:**
- Performance assessment
- Course recommendations
- Study strategies
- Certification paths

**Example:**
```bash
curl -X POST "http://localhost:8000/api/agents/execute/academic_counselor?student_id=1"
```

### 5. Job Market Analyst Agent

**Purpose:** Provide employment market insights

**Input:**
- Student ID
- Target industries (optional)

**Process:**
- Analyzes market trends
- Evaluates demand for skills
- Projects growth

**Output:**
- Market trends analysis
- In-demand skills
- Salary outlook
- Job growth projections

**Example:**
```bash
curl -X POST "http://localhost:8000/api/agents/execute/job_market_analyst?student_id=1&industry=Technology"
```

## API Usage Patterns

### Pattern 1: Single Agent Execution

```python
import asyncio
import httpx

async def get_career_recommendations():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/execute/career_recommender",
            params={"student_id": 1}
        )
        return response.json()

# Run
result = asyncio.run(get_career_recommendations())
```

### Pattern 2: Multi-Agent Orchestration

```python
import asyncio
import httpx

async def get_comprehensive_guidance():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/execute",
            json={
                "student_id": 1,
                "agent_types": [
                    "career_recommender",
                    "skill_analyzer",
                    "interest_evaluator"
                ],
                "context": {"target_career": "Software Engineer"}
            }
        )
        return response.json()

# Run
result = asyncio.run(get_comprehensive_guidance())
```

### Pattern 3: Comprehensive Career Guidance

```python
import asyncio
import httpx

async def get_all_guidance():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/career-guidance/1"
        )
        return response.json()

# Run - executes all agents
result = asyncio.run(get_all_guidance())
```

## Configuration

### Environment Variables

```env
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# LangChain
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...

# Database
DATABASE_URL=sqlite:///./career_guidance.db

# Agent Settings
AGENT_TIMEOUT=30
AGENT_MAX_CONVERSATION_HISTORY=50
AGENT_ENABLE_AGENT_MEMORY=true
AGENT_PARALLEL_AGENT_EXECUTION=true
```

## Advanced Usage

### Custom Agent Creation

To add a new agent:

```python
from app.agents.base_agent import BaseAgent, AgentResponse
from sqlalchemy.orm import Session

class MyCustomAgent(BaseAgent):
    def __init__(self, db: Session):
        super().__init__(
            name="My Custom Agent",
            agent_type="my_custom_agent"
        )
        self.db = db
    
    async def process(self, **kwargs) -> AgentResponse:
        # Your implementation
        return self._create_response(
            status="success",
            message="Processing complete",
            data={"result": "..."},
            confidence=0.9
        )
    
    def get_tools(self):
        return []  # Define tools if needed
```

### Custom Tool Integration

Add tools to `AgentTools`:

```python
def my_custom_tool(self) -> dict:
    """Custom tool implementation"""
    return {"data": "..."}
```

Then register in `get_langgraph_tools()`:

```python
Tool(
    name="my_custom_tool",
    func=self.my_custom_tool,
    description="My custom tool description"
)
```

## Performance Optimization

### 1. Parallel Agent Execution

```python
# Orchestrator automatically parallelizes independent agents
request = OrchestrationRequest(
    student_id=1,
    agent_types=[
        AgentType.SKILL_ANALYZER,
        AgentType.INTEREST_EVALUATOR,
        AgentType.JOB_MARKET_ANALYST  # These 3 run in parallel
    ]
)
```

### 2. Caching Strategies

```python
# Implement caching for student profiles
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_student_profile(student_id: int):
    return get_student_profile(student_id)
```

### 3. Token Optimization

Agents use optimized prompts with limited token counts:
- Default max_tokens: 1500
- System prompt optimized for clarity
- Context limited to essential information

## Monitoring & Debugging

### Enable LangChain Tracing

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key
```

Visit LangSmith dashboard to view:
- Agent execution traces
- Token usage
- Response times
- Error logs

### View Conversation History

```bash
# Get conversation details
curl "http://localhost:8000/api/agents/conversation/{conversation_id}"
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=your_key
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Production Settings

```env
DEBUG=false
AGENT_PARALLEL_AGENT_EXECUTION=true
AGENT_MAX_PARALLEL_AGENTS=5
AGENT_TIMEOUT=60
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| OpenAI 401 Error | Check OPENAI_API_KEY is valid |
| Slow responses | Enable parallel execution, reduce token limits |
| Student not found | Verify student exists in database |
| Tool not found | Register tool in AgentTools class |
| LangGraph errors | Check langgraph library version |

## Testing

Run the example file:

```bash
python -m app.agents.examples
```

Or import and use in your tests:

```python
from app.agents.examples import example_orchestrator_multi_request
import asyncio

asyncio.run(example_orchestrator_multi_request(db, student_id=1))
```

## Next Steps

1. Set up your .env file with OpenAI API key
2. Test individual agents via API
3. Execute comprehensive guidance queries
4. Monitor and optimize response times
5. Customize prompts and tools for your needs
6. Deploy to production

## Support & Resources

- **API Documentation**: http://localhost:8000/docs
- **README**: AGENTS_README.md
- **Examples**: app/agents/examples.py
- **Configuration**: app/agents/config.py
