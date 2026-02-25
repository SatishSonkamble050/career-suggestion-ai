"""Quick Reference Guide for Simple LangGraph Workflow"""

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    SIMPLE LANGGRAPH WORKFLOW REFERENCE                     ║
╚════════════════════════════════════════════════════════════════════════════╝

This guide shows how to use the simplified LangGraph workflow for career guidance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check if the workflow service is running:

  curl -X GET http://localhost:8000/api/agents/simple/health

Response (200):
  {"status": "healthy", "message": "Simple LangGraph workflow is running"}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. BASIC CAREER GUIDANCE REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Minimal example - just GPA and field of study:

  curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
    -H "Content-Type: application/json" \
    -d '{
      "academic": {
        "gpa": 3.8,
        "major": "Computer Science"
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


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. COMPREHENSIVE PROFILE WITH DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete profile for detailed analysis:

  curl -X POST http://localhost:8000/api/agents/simple/career-guide/2 \
    -H "Content-Type: application/json" \
    -d '{
      "academic": {
        "gpa": 3.9,
        "major": "Data Science",
        "subjects": ["Machine Learning", "Statistics", "Deep Learning"],
        "strong_areas": ["Mathematics", "Programming"],
        "weak_areas": ["Public Speaking"]
      },
      "skills": {
        "technical": [
          "Python (Expert)",
          "R (Advanced)",
          "SQL (Advanced)",
          "TensorFlow (Advanced)"
        ],
        "soft": ["Problem Solving", "Communication", "Leadership"],
        "certifications": ["AWS ML", "Google Analytics"]
      },
      "interests": {
        "fields": ["AI", "Data Science", "Finance"],
        "activities": ["Kaggle", "Research", "Open source"],
        "industries": ["Tech", "Finance", "Healthcare"]
      },
      "preferences": {
        "work_style": "Flexible remote with office days",
        "salary_range": "120k-200k",
        "location": "San Francisco Bay Area",
        "career_growth": "Fast-track to leadership",
        "impact": "Meaningful work on real problems",
        "learning": "Cutting-edge technology"
      }
    }'


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. REQUEST FORMAT & FIELDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Endpoint: POST /api/agents/simple/career-guide/{student_id}

All fields are OPTIONAL. Provide what data you have:

CareerInput JSON Schema:
{
  "academic": {
    "gpa": float,                    # e.g., 3.8
    "major": string,                 # e.g., "Computer Science"
    "minor": string,                 # e.g., "Mathematics"
    "subjects": [string],            # e.g., ["AI", "ML", "NLP"]
    "strong_areas": [string],        # e.g., ["Math", "Programming"]
    "weak_areas": [string]           # e.g., ["Public Speaking"]
  },
  "skills": {
    "technical": [string],           # e.g., ["Python", "JavaScript"]
    "soft": [string],                # e.g., ["Leadership", "Communication"]
    "certifications": [string]       # e.g., ["AWS Developer"]
  },
  "interests": {
    "fields": [string],              # e.g., ["AI", "Data Science"]
    "activities": [string],          # e.g., ["Kaggle", "Open source"]
    "industries": [string]           # e.g., ["Tech", "Finance"]
  },
  "preferences": {
    "work_style": string,            # e.g., "Remote"
    "salary_range": string,          # e.g., "100k-150k"
    "location": string,              # e.g., "Silicon Valley"
    "career_growth": string,         # e.g., "Fast learning"
    "impact": string,                # e.g., "Meaningful work"
    "learning": string               # e.g., "Cutting-edge tech"
  }
}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. RESPONSE FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WorkflowResponse (200 OK):
{
  "student_id": 1,
  "academic_analysis": "Text analysis of academic profile",
  "skill_analysis": "Text analysis of skills and certifications",
  "interest_analysis": "Text analysis of interests and fields",
  "preference_analysis": "Text analysis of career preferences",
  "market_analysis": "Text analysis of job market opportunities",
  "final_report": "Comprehensive career guidance report with recommendations"
}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. ERROR HANDLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error responses (400, 500):
{
  "detail": "Error message describing what went wrong"
}

Common errors:
- Student not found: 404 Not Found
- Invalid JSON: 422 Unprocessable Entity
- Server error: 500 Internal Server Error


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. PYTHON USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using httpx (async):
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
        result = response.json()
        print(result["final_report"])

asyncio.run(get_guidance())


Using requests (sync):
import requests

response = requests.post(
    "http://localhost:8000/api/agents/simple/career-guide/1",
    json={"academic": {"gpa": 3.8}}
)
print(response.json()["final_report"])


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. WORKFLOW EXECUTION STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The workflow executes 6 agents in sequence:

  1. Academic Agent      → Analyzes GPA, Major, Subjects
  2. Skill Agent         → Evaluates Technical & Soft Skills
  3. Interest Agent      → Assesses Career Interests & Fields
  4. Preference Agent    → Reviews Career Preferences & Goals
  5. Market Agent        → Analyzes Job Market & Opportunities
  6. Report Agent        → Generates Final Comprehensive Report

Each agent processes the previous results and enriches the analysis.
Final report includes career recommendations with concrete paths.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. TIPS & BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Provide as much detail as possible for better recommendations
✓ Include both technical and soft skills for comprehensive analysis
✓ List specific subjects/areas for more targeted guidance
✓ Specify industries of interest for market analysis
✓ Set clear preferences for personalized recommendations

✗ Don't use null values - just omit the field
✗ Don't include fields with empty arrays
✗ Don't worry about field order - all orders supported


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. DEBUGGING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Enable logging in your Python code:

  import logging
  logging.basicConfig(level=logging.DEBUG)

Check API running:
  curl -X GET http://localhost:8000/api/agents/simple/health

Test connectivity:
  curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
    -H "Content-Type: application/json" \
    -d '{"academic": {"gpa": 3.5}}'

View full request/response with verbose curl:
  curl -v -X POST http://localhost:8000/api/agents/simple/career-guide/1 \
    -H "Content-Type: application/json" \
    -d '{...}'

"""

# Example JSON files for saving

MINIMAL_INPUT = """
{
  "academic": {
    "gpa": 3.8,
    "major": "Computer Science"
  },
  "skills": {
    "technical": ["Python", "JavaScript"]
  },
  "interests": {
    "fields": ["AI", "Web Development"]
  },
  "preferences": {
    "work_style": "Remote",
    "salary_range": "100k-150k"
  }
}
"""

DETAILED_INPUT = """
{
  "academic": {
    "gpa": 3.9,
    "major": "Data Science",
    "minor": "Economics",
    "subjects": [
      "Machine Learning",
      "Statistics",
      "Linear Algebra",
      "Deep Learning",
      "Natural Language Processing"
    ],
    "strong_areas": ["Mathematics", "Programming", "Statistical Analysis"],
    "weak_areas": ["Public Speaking", "Networking"]
  },
  "skills": {
    "technical": [
      "Python (Expert)",
      "R (Advanced)",
      "SQL (Advanced)",
      "TensorFlow (Advanced)",
      "Pandas (Expert)",
      "Scikit-learn (Advanced)",
      "AWS (Intermediate)",
      "Docker (Intermediate)"
    ],
    "soft": [
      "Problem Solving",
      "Communication",
      "Teamwork - Experience",
      "Project Leadership"
    ],
    "certifications": [
      "AWS Certified ML Specialist",
      "Google Data Analytics Professional"
    ]
  },
  "interests": {
    "fields": [
      "Machine Learning",
      "Data Science",
      "Artificial Intelligence",
      "Quantitative Finance",
      "Healthcare Analytics"
    ],
    "activities": [
      "Kaggle competitions",
      "Research projects",
      "Open source contributions",
      "Teaching & mentoring"
    ],
    "industries": [
      "Technology",
      "Finance",
      "Healthcare",
      "E-commerce",
      "Startups"
    ]
  },
  "preferences": {
    "work_style": "Collaborative with flexible remote",
    "salary_range": "120k-200k",
    "location": "San Francisco Bay Area or New York",
    "career_growth": "Fast-track to leadership",
    "impact": "Meaningful work solving real problems",
    "learning": "Cutting-edge technology and research"
  }
}
"""

if __name__ == "__main__":
    print(__doc__)
