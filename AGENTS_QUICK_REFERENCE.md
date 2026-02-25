# Multi-Agent System - Quick Reference

## File Structure

```
app/agents/
├── __init__.py                      # Module exports
├── base_agent.py                    # Abstract base class & response model
├── agent_tools.py                   # Shared tools for agents
├── config.py                        # Configuration & settings
├── examples.py                      # Usage examples
├── career_recommender_agent.py      # Career recommendations
├── skill_analyzer_agent.py          # Skill analysis
├── interest_evaluator_agent.py      # Interest evaluation
├── academic_counselor_agent.py      # Academic guidance
├── job_market_analyst_agent.py      # Market analysis
└── agent_orchestrator.py            # Main orchestrator

app/api/routes/
└── agents.py                        # API endpoints
```

## API Quick Reference

### Base URL
```
http://localhost:8000/api/agents
```

### Endpoints

#### 1. Get Available Agents
```
GET /available
Response: List of available agents with descriptions
```

#### 2. Execute Single Agent
```
POST /execute/{agent_type}?student_id={id}
Query Parameters:
  - student_id (required): Student ID
  - target_career (optional): For skill analyzer
  - industry (optional): For job market analyst

Response: AgentResponse
```

Agent Types:
- `career_recommender`
- `skill_analyzer`
- `interest_evaluator`
- `academic_counselor`
- `job_market_analyst`

#### 3. Execute Multiple Agents
```
POST /execute
Request Body:
{
  "student_id": 1,
  "agent_types": ["career_recommender", "skill_analyzer"],
  "context": {"target_career": "Software Engineer"},
  "conversation_id": "optional-uuid"
}

Response: OrchestrationResponse
```

#### 4. Get Comprehensive Guidance
```
POST /career-guidance/{student_id}
Executes all agents in optimal sequence

Response: OrchestrationResponse
```

#### 5. Get Conversation History
```
GET /conversation/{conversation_id}

Response: Conversation history
```

#### 6. Clear Conversation
```
DELETE /conversation/{conversation_id}

Response: Success message
```

## Response Models

### AgentResponse
```json
{
  "agent_name": "Career Recommender",
  "agent_type": "career_recommender",
  "timestamp": "2024-02-21T10:30:00",
  "status": "success|error|pending",
  "message": "Human-readable message",
  "data": {
    "key": "value",
    "nested": {"data": "..."}
  },
  "reasoning": "Why this response was generated",
  "confidence": 0.9
}
```

### OrchestrationResponse
```json
{
  "conversation_id": "uuid",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00",
  "agents_executed": ["Career Recommender", "Skill Analyzer"],
  "results": [
    {
      "agent_name": "...",
      "agent_type": "...",
      ...
    }
  ],
  "summary": "Comprehensive summary from all agents",
  "status": "success|error"
}
```

## Available Tools

Each agent has access to these tools:

1. **get_student_profile**
   ```
   Returns: Complete student profile with academic details
   ```

2. **get_student_skills**
   ```
   Returns: List of skills with proficiency levels
   ```

3. **get_student_interests**
   ```
   Returns: List of career interests with levels
   ```

4. **get_career_preferences**
   ```
   Returns: Career preferences including industries and work environment
   ```

5. **analyze_skills_gaps**
   ```
   Params: target_career
   Returns: Skills needed vs current skills
   ```

6. **get_job_market_trends**
   ```
   Params: industry
   Returns: Market data including growth rate and salary range
   ```

7. **create_learning_path**
   ```
   Params: target_skill, duration_weeks
   Returns: Weekly learning milestones and resources
   ```

## Configuration

### Required Environment Variables
```env
OPENAI_API_KEY=sk-...  # OpenAI API key (required)
```

### Optional Environment Variables
```env
OPENAI_MODEL=gpt-3.5-turbo          # Default LLM model
LANGCHAIN_TRACING_V2=true           # Enable tracing
DATABASE_URL=sqlite:///./career_guidance.db
```

## Common Use Cases

### 1. Get Career Recommendations Only
```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1"
```

### 2. Analyze Skills for Target Career
```bash
curl -X POST "http://localhost:8000/api/agents/execute/skill_analyzer?student_id=1&target_career=Software%20Engineer"
```

### 3. Get Full Career Guidance
```bash
curl -X POST "http://localhost:8000/api/agents/career-guidance/1"
```

### 4. Execute Multiple Specific Agents
```bash
curl -X POST "http://localhost:8000/api/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "agent_types": ["skill_analyzer", "career_recommender"],
    "context": {"target_career": "Data Scientist"}
  }'
```

### 5. Market Analysis for Tech Industry
```bash
curl -X POST "http://localhost:8000/api/agents/execute/job_market_analyst?student_id=1&industry=Technology"
```

## Python Client Example

```python
import asyncio
import httpx

async def get_recommendations():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/execute/career_recommender",
            params={"student_id": 1}
        )
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Message: {data['message']}")
        print(f"Data: {data['data']}")
        return data

# Run
asyncio.run(get_recommendations())
```

## Status Codes

- **200**: Success
- **400**: Bad request (invalid student ID, agent type, etc.)
- **404**: Not found (student or conversation not found)
- **500**: Server error (API error, database error, etc.)

## Agent Execution Context

Agents can receive additional context:

```python
{
  "student_id": 1,
  "agent_types": ["skill_analyzer"],
  "context": {
    "target_career": "Software Engineer",
    "focus_area": "backend_development",
    "timeline_months": 12
  }
}
```

## Conversation Flow

```
1. User sends request → API Router
2. Router creates orchestrator instance
3. Orchestrator initializes agents
4. Agents execute in sequence/parallel
5. Results aggregated
6. LLM generates summary
7. Response returned to user
8. Conversation ID stored for history
```

## Performance Tips

1. **Use parallel execution**: Multiple independent agents run concurrently
2. **Cache student data**: Reduces database queries
3. **Limit token usage**: Each agent has max_tokens=1500
4. **Monitor confidence scores**: Lower scores may need validation

## Troubleshooting

### "Invalid agent type" error
- Check agent type spelling (use lowercase with underscores)
- Valid types: career_recommender, skill_analyzer, interest_evaluator, academic_counselor, job_market_analyst

### "Student not found" error
- Verify student exists in database
- Use correct student ID

### "OpenAI API error" 
- Check OPENAI_API_KEY is set
- Verify API key has sufficient credits
- Check rate limits

### Slow responses
- Enable parallel agent execution
- Reduce number of agents in single request
- Check OpenAI API status

## Next Steps

1. **Test Endpoints**: Use curl or Postman to test APIs
2. **Integrate with Frontend**: Build UI calling these endpoints
3. **Monitor Performance**: Enable LangChain tracing
4. **Customize Prompts**: Edit agent prompts in config.py
5. **Add Tools**: Extend AgentTools for custom functionality

## Documentation Files

- `AGENTS_README.md` - Comprehensive documentation
- `AGENTS_GUIDE.md` - Detailed implementation guide
- `app/agents/examples.py` - Python code examples
- `app/agents/config.py` - Configuration settings
