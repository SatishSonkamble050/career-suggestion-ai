# Multi-Agent Career Guidance System

## Overview

This is a comprehensive multi-agent AI system built with **LangChain** and **LangGraph** for providing intelligent career guidance to students. The system uses multiple specialized AI agents that work together to provide holistic career counseling.

## Architecture

### Agent Types

The system includes 5 specialized agents:

1. **Career Recommender Agent** - Generates personalized career recommendations based on skills, interests, and preferences
2. **Skill Analyzer Agent** - Analyzes current skills and identifies gaps for target careers
3. **Interest Evaluator Agent** - Analyzes career interests and matches them with suitable fields
4. **Academic Counselor Agent** - Provides academic guidance and course recommendations
5. **Job Market Analyst Agent** - Analyzes job market trends and employment opportunities

### System Components

```
app/agents/
├── __init__.py
├── base_agent.py                  # Abstract base class for all agents
├── agent_tools.py                 # Shared tools and utilities
├── career_recommender_agent.py    # Career recommendation agent
├── skill_analyzer_agent.py        # Skill analysis agent
├── interest_evaluator_agent.py    # Interest evaluation agent
├── academic_counselor_agent.py    # Academic guidance agent
├── job_market_analyst_agent.py    # Job market analysis agent
└── agent_orchestrator.py          # Main orchestrator using LangGraph

app/api/routes/
└── agents.py                       # API endpoints for agent system
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies:
- `langchain==0.1.1` - LangChain framework
- `langchain-openai==0.0.5` - OpenAI integration
- `langgraph==0.0.23` - LangGraph for agent orchestration
- `openai==1.3.0` - OpenAI API client

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and set up your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key_here
DATABASE_URL=sqlite:///./career_guidance.db
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Agent Management

#### Get Available Agents
```
GET /api/agents/available
```

Returns list of all available agents with descriptions.

#### Execute Multiple Agents
```
POST /api/agents/execute
```

Request body:
```json
{
  "student_id": 1,
  "agent_types": ["career_recommender", "skill_analyzer", "interest_evaluator"],
  "context": {
    "target_career": "Software Engineer"
  },
  "conversation_id": "optional-uuid"
}
```

#### Execute Single Agent
```
POST /api/agents/execute/{agent_type}?student_id=1&target_career=Software Engineer
```

`agent_type` can be:
- `career_recommender`
- `skill_analyzer`
- `interest_evaluator`
- `academic_counselor`
- `job_market_analyst`

#### Get Comprehensive Career Guidance
```
POST /api/agents/career-guidance/{student_id}
```

Executes all agents in optimal sequence to provide comprehensive guidance.

#### View Conversation History
```
GET /api/agents/conversation/{conversation_id}
```

#### Clear Conversation History
```
DELETE /api/agents/conversation/{conversation_id}
```

## Usage Examples

### Example 1: Get Career Recommendations

```bash
curl -X POST "http://localhost:8000/api/agents/execute/career_recommender?student_id=1"
```

### Example 2: Analyze Skills Gaps

```bash
curl -X POST "http://localhost:8000/api/agents/execute/skill_analyzer?student_id=1&target_career=Data%20Scientist"
```

### Example 3: Comprehensive Guidance

```bash
curl -X POST "http://localhost:8000/api/agents/career-guidance/1"
```

### Example 4: Multi-Agent Execution

```bash
curl -X POST "http://localhost:8000/api/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "agent_types": ["skill_analyzer", "interest_evaluator", "career_recommender"],
    "context": {"target_career": "Software Engineer"}
  }'
```

## How Agents Work

### BaseAgent Class

All agents inherit from `BaseAgent` which provides:
- Standardized response format
- Conversation history management
- Tool access
- Error handling

### Agent Response Format

```json
{
  "agent_name": "Career Recommender",
  "agent_type": "career_recommender",
  "timestamp": "2024-02-21T10:30:00",
  "status": "success",
  "message": "Career recommendations generated successfully",
  "data": {
    "student_id": 1,
    "recommendations": "..."
  },
  "reasoning": "Analyzed student skills and interests",
  "confidence": 0.9
}
```

### Agent Orchestrator

The `AgentOrchestrator` manages:
- Agent instantiation and lifecycle
- Multi-agent task execution
- Result aggregation
- Summary generation using LLM
- Conversation history tracking

## Available Tools

Each agent has access to shared tools via `AgentTools`:

1. `get_student_profile()` - Fetch comprehensive student profile
2. `get_student_skills()` - Get student skills with proficiency levels
3. `get_student_interests()` - Get career interests
4. `get_career_preferences()` - Get career preferences
5. `analyze_skills_gaps()` - Analyze skills gaps for target career
6. `get_job_market_trends()` - Get industry job market data
7. `create_learning_path()` - Generate personalized learning paths

## Extending the System

### Adding a New Agent

1. Create a new agent class inheriting from `BaseAgent`:

```python
from app.agents.base_agent import BaseAgent, AgentResponse

class MyNewAgent(BaseAgent):
    def __init__(self, db: Session):
        super().__init__(
            name="My Agent",
            agent_type="my_agent",
            model_name="gpt-3.5-turbo"
        )
        self.db = db
    
    async def process(self, **kwargs) -> AgentResponse:
        # Implementation
        pass
    
    def get_tools(self) -> List[Dict[str, Any]]:
        # Return available tools
        pass
```

2. Add the agent to the orchestrator in `agent_orchestrator.py`
3. Register in API routes in `agents.py`

### Adding New Tools

1. Add methods to `AgentTools` class:

```python
def my_new_tool(self) -> Dict[str, Any]:
    # Implementation
    pass
```

2. Expose as LangGraph tool:

```python
def get_langgraph_tools(self) -> List[Tool]:
    tools.append(
        Tool(
            name="my_new_tool",
            func=self.my_new_tool,
            description="Description of what the tool does"
        )
    )
```

## Technologies Used

- **FastAPI** - Web framework
- **LangChain** - LLM framework and utilities
- **LangGraph** - Agent orchestration
- **OpenAI** - LLM provider (GPT-3.5-turbo)
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation

## Performance Considerations

1. **Agent Parallelization**: Agents can be executed in parallel for independent tasks
2. **Caching**: Implement caching for repeated student queries
3. **Token Optimization**: Use appropriate token limits in LLM calls
4. **Database Indexing**: Ensure proper database indexing for efficient queries

## Error Handling

The system includes:
- Try-catch blocks in all agents
- Validation of student IDs before processing
- Graceful error messages in responses
- Logging of errors for debugging

## Future Enhancements

1. **Real-time Job Market Data**: Integrate with LinkedIn/Indeed APIs
2. **Skill Assessment**: Add automated skill testing
3. **Interview Preparation**: Add interview prep agent
4. **Salary Negotiation**: Add salary guidance agent
5. **Network Building**: Add networking advisor agent
6. **Multi-language Support**: Support for multiple languages
7. **Custom Workflows**: Allow users to create custom agent workflows

## Troubleshooting

### Issue: OpenAI API Key Error
- Verify your OpenAI API key in `.env`
- Check that the key has proper permissions
- Ensure the key is not expired

### Issue: Database Connection Error
- Verify `DATABASE_URL` in `.env`
- Ensure database file has write permissions

### Issue: Agent Not Responding
- Check LangChain/OpenAI logs
- Verify student ID exists in database
- Check API rate limits

## License

MIT License

## Support

For issues or questions, please refer to the main project documentation.
