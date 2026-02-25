# LangGraph API Quick Reference

## Base URL
```
http://localhost:8000/api/agents
```

## Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/langgraph/execute/{id}` | Execute full workflow |
| POST | `/langgraph/custom-sequence/{id}` | Custom agent sequence |
| POST | `/langgraph/parallel/{id}` | Parallel agents |
| GET | `/langgraph/graph-visualization` | View workflow graph |
| GET | `/langgraph/stats/{id}` | Execution statistics |

---

## 1. Execute Full Workflow

**Endpoint:**
```
POST /langgraph/execute/{student_id}
```

**Parameters:**
```
Query Parameters:
  - conversation_id (optional): UUID for this conversation
  - enable_logging (optional, default=true): Enable verbose logging
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/agents/langgraph/execute/1?enable_logging=true"
```

**Response:**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00.123456",
  "agents_executed": [
    "Skill Analyzer",
    "Interest Evaluator",
    "Career Recommender",
    "Academic Counselor",
    "Job Market Analyst"
  ],
  "individual_results": {
    "Skill Analyzer": {
      "status": "success",
      "message": "Skill analysis completed",
      "data": {...},
      "confidence": 0.9
    },
    ...
  },
  "combined_analysis": "Comprehensive analysis combining all insights...",
  "execution_complete": true
}
```

**Time:** ~14 seconds (sequential execution)

---

## 2. Execute Custom Sequence

**Endpoint:**
```
POST /langgraph/custom-sequence/{student_id}
```

**Body:**
```json
{
  "agent_sequence": ["skill_analyzer", "career_recommender"],
  "conversation_id": "optional-uuid",
  "context": {
    "target_career": "Software Engineer"
  }
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/agents/langgraph/custom-sequence/1" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_sequence": ["skill_analyzer", "career_recommender"],
    "context": {"target_career": "Software Engineer"}
  }'
```

**Valid Agent Types:**
- `skill_analyzer`
- `interest_evaluator`
- `career_recommender`
- `academic_counselor`
- `job_market_analyst`

**Response:**
```json
{
  "conversation_id": "uuid",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00",
  "agents_executed": ["Skill Analyzer", "Career Recommender"],
  "results": [...],
  "summary": "Analysis summary...",
  "status": "success"
}
```

**Time:** ~5-7 seconds (2 agents)

---

## 3. Execute Parallel Agents

**Endpoint:**
```
POST /langgraph/parallel/{student_id}
```

**Body:**
```json
{
  "agent_types": ["skill_analyzer", "interest_evaluator", "job_market_analyst"],
  "conversation_id": "optional-uuid",
  "context": {}
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/agents/langgraph/parallel/1" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_types": ["skill_analyzer", "interest_evaluator", "job_market_analyst"]
  }'
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00",
  "agents_executed": [
    "Skill Analyzer",
    "Interest Evaluator",
    "Job Market Analyst"
  ],
  "results": [...],
  "summary": "Parallel analysis complete...",
  "status": "success"
}
```

**Time:** ~3 seconds (3 agents in parallel)
**Speedup:** 4.7x vs sequential

---

## 4. Get Graph Visualization

**Endpoint:**
```
GET /langgraph/graph-visualization
```

**Example Request:**
```bash
curl "http://localhost:8000/api/agents/langgraph/graph-visualization"
```

**Response:**
```json
{
  "visualization": "ASCII graph representation of the workflow",
  "format": "ascii"
}
```

**Example Output:**
```
INPUT_PROCESSOR
    ↓
    ├→ SKILL_ANALYZER
    ├→ INTEREST_EVALUATOR
    ├→ CAREER_RECOMMENDER
    ├→ ACADEMIC_COUNSELOR
    ├→ JOB_MARKET_ANALYST
    ↓
SYNTHESIZER
    ↓
RESPONSE_FORMATTER
    ↓
END
```

---

## 5. Get Execution Statistics

**Endpoint:**
```
GET /langgraph/stats/{conversation_id}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/agents/langgraph/stats/f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

**Response:**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00",
  "execution_method": "langgraph|custom_sequence|parallel",
  "agents_executed": 5,
  "total_results": 5,
  "agent_names": [
    "Skill Analyzer",
    "Interest Evaluator",
    "Career Recommender",
    "Academic Counselor",
    "Job Market Analyst"
  ]
}
```

---

## Python Client Examples

### Example 1: Basic Execution
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/langgraph/execute/1",
            params={"enable_logging": "true"}
        )
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Agents: {data['agents_executed']}")

asyncio.run(main())
```

### Example 2: Parallel Execution
```python
async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/langgraph/parallel/1",
            json={
                "agent_types": [
                    "skill_analyzer",
                    "interest_evaluator",
                    "job_market_analyst"
                ]
            }
        )
        data = response.json()
        print(f"Results: {data['agents_executed']}")

asyncio.run(main())
```

### Example 3: Custom Sequence
```python
async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agents/langgraph/custom-sequence/1",
            json={
                "agent_sequence": [
                    "skill_analyzer",
                    "career_recommender"
                ],
                "context": {
                    "target_career": "Data Scientist"
                }
            }
        )
        data = response.json()
        print(data["summary"])

asyncio.run(main())
```

### Example 4: Get Statistics
```python
async def main():
    async with httpx.AsyncClient() as client:
        # First execute
        exec_response = await client.post(
            "http://localhost:8000/api/agents/langgraph/execute/1"
        )
        exec_data = exec_response.json()
        conv_id = exec_data["conversation_id"]
        
        # Then get stats
        stats_response = await client.get(
            f"http://localhost:8000/api/agents/langgraph/stats/{conv_id}"
        )
        stats = stats_response.json()
        print(f"Method: {stats['execution_method']}")
        print(f"Agents: {stats['agent_names']}")

asyncio.run(main())
```

---

## JavaScript/TypeScript Examples

### Example 1: Fetch API
```javascript
async function executeWorkflow() {
  const response = await fetch(
    'http://localhost:8000/api/agents/langgraph/execute/1?enable_logging=true',
    { method: 'POST' }
  );
  const data = await response.json();
  console.log('Agents executed:', data.agents_executed);
  console.log('Analysis:', data.combined_analysis);
}

executeWorkflow();
```

### Example 2: Axios
```javascript
const axios = require('axios');

async function executeParallel() {
  const response = await axios.post(
    'http://localhost:8000/api/agents/langgraph/parallel/1',
    {
      agent_types: ['skill_analyzer', 'interest_evaluator']
    }
  );
  console.log('Results:', response.data.agents_executed);
}

executeParallel();
```

### Example 3: React Hook
```javascript
import { useState, useEffect } from 'react';

function WorkflowResults({ studentId }) {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const runWorkflow = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/agents/langgraph/execute/${studentId}`,
        { method: 'POST' }
      );
      const data = await response.json();
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={runWorkflow}>Run Workflow</button>
      {loading && <p>Loading...</p>}
      {results && (
        <div>
          <h2>Analysis Results</h2>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

---

## Performance Comparison

| Operation | Time | Notes |
|-----------|------|-------|
| Sequential (5 agents) | ~14s | All agents sequential |
| Parallel (5 agents) | ~3s | 4.7x faster |
| Custom (2 agents) | ~5-7s | Only specified agents |
| Visualization | <1s | ASCII only |
| Statistics | <1s | Cached data |

---

## Error Handling

### Invalid Agent Type
```json
{
  "status": "error",
  "detail": "Invalid agent type: invalid_agent"
}
```

### Student Not Found
```json
{
  "status": "error",
  "detail": "Student not found"
}
```

### Conversation Not Found
```json
{
  "status": "error",
  "detail": "Conversation not found"
}
```

### API Error
```json
{
  "status": "error",
  "detail": "Error executing workflow: ..."
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | Not found (student or conversation) |
| 500 | Server error (API or database error) |

---

## Request/Response Models

### AgentResponse
```json
{
  "agent_name": "Skill Analyzer",
  "agent_type": "skill_analyzer",
  "timestamp": "2024-02-21T10:30:00",
  "status": "success",
  "message": "Skill analysis completed",
  "data": {...},
  "confidence": 0.9
}
```

### OrchestrationResponse
```json
{
  "conversation_id": "uuid",
  "student_id": 1,
  "timestamp": "2024-02-21T10:30:00",
  "agents_executed": [...],
  "results": [...],
  "summary": "...",
  "status": "success"
}
```

---

## Tips & Tricks

### 1. Save Conversation ID
```bash
# Save the conversation ID for later retrieval
CONV_ID=$(curl -s -X POST "http://localhost:8000/api/agents/langgraph/execute/1" | jq -r '.conversation_id')
echo "Conversation: $CONV_ID"
```

### 2. Chain Requests
```bash
# Execute workflow
curl -X POST "http://localhost:8000/api/agents/langgraph/execute/1" | \
  jq '.conversation_id' | \
  xargs -I {} curl "http://localhost:8000/api/agents/langgraph/stats/{}"
```

### 3. Batch Processing
```python
import asyncio

async def process_students(student_ids):
    tasks = [
        execute_workflow(student_id)
        for student_id in student_ids
    ]
    return await asyncio.gather(*tasks)
```

### 4. Compare Execution Methods
```bash
# Sequential
time curl -X POST "http://localhost:8000/api/agents/langgraph/execute/1"

# Parallel
time curl -X POST "http://localhost:8000/api/agents/langgraph/parallel/1" \
  -d '{"agent_types":["skill_analyzer","interest_evaluator"]}'
```

---

## Related Documentation

- [LANGGRAPH_GUIDE.md](LANGGRAPH_GUIDE.md) - Comprehensive guide
- [LANGGRAPH_IMPLEMENTATION_SUMMARY.md](LANGGRAPH_IMPLEMENTATION_SUMMARY.md) - Implementation details
- [AGENTS_QUICK_REFERENCE.md](AGENTS_QUICK_REFERENCE.md) - General agent API reference

---

## Support

For issues or questions:
1. Check response status codes
2. Review error messages
3. Verify agent types are valid
4. Check student ID exists
5. See LANGGRAPH_GUIDE.md for detailed examples
