"""Simple LangGraph Workflow Examples"""

import asyncio
from typing import Dict, Any
from sqlalchemy.orm import Session


# ============ Example 1: Basic Usage ============

async def example_basic_workflow(db: Session):
    """Example: Basic workflow execution"""
    from app.agents.simple_langgraph import SimpleLangGraphWorkflow
    
    workflow = SimpleLangGraphWorkflow(db)
    
    # Input data
    input_data = {
        "academic": {
            "gpa": 3.8,
            "major": "Computer Science",
            "subjects": ["Data Structures", "Algorithms", "Machine Learning"],
            "weak_areas": ["Public Speaking"]
        },
        "skills": {
            "technical": ["Python", "JavaScript", "SQL"],
            "soft": ["Leadership", "Communication"],
            "certifications": ["AWS Developer"]
        },
        "interests": {
            "fields": ["AI", "Data Science", "Cloud Computing"],
            "activities": ["Building projects", "Learning new tech"]
        },
        "preferences": {
            "work_style": "Remote with flexibility",
            "salary_range": "100k-150k",
            "location": "Tech hub",
            "growth": "Fast-paced learning environment"
        }
    }
    
    # Execute workflow
    result = await workflow.execute(student_id=1, input_data=input_data)
    
    print("=== Career Guidance Results ===\n")
    print(f"Academic Analysis: {result['academic_analysis']}\n")
    print(f"Skill Analysis: {result['skill_analysis']}\n")
    print(f"Interest Analysis: {result['interest_analysis']}\n")
    print(f"Preference Analysis: {result['preference_analysis']}\n")
    print(f"Market Analysis: {result['market_analysis']}\n")
    print(f"Final Report:\n{result['final_report']}")


# ============ Example 2: Via HTTP API ============

async def example_http_api():
    """Example: Using the HTTP API"""
    import httpx
    
    async with httpx.AsyncClient() as client:
        # Send request
        response = await client.post(
            "http://localhost:8000/api/agents/simple/career-guide/1",
            json={
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
            }
        )
        
        result = response.json()
        print("Career Guidance Results:")
        print(result["final_report"])


# ============ Example 3: Minimal Input ============

async def example_minimal(db: Session):
    """Example: Minimal input data"""
    from app.agents.simple_langgraph import SimpleLangGraphWorkflow
    
    workflow = SimpleLangGraphWorkflow(db)
    
    # Just the essentials
    input_data = {
        "academic": {"gpa": 3.5, "major": "Engineering"},
        "skills": {"technical": ["Python", "CAD"]},
        "interests": {"fields": ["Robotics"]},
        "preferences": {"work_style": "Hands-on"}
    }
    
    result = await workflow.execute(student_id=2, input_data=input_data)
    print(result["final_report"])


# ============ Example 4: Detailed Profile ============

async def example_detailed(db: Session):
    """Example: Detailed student profile"""
    from app.agents.simple_langgraph import SimpleLangGraphWorkflow
    
    workflow = SimpleLangGraphWorkflow(db)
    
    # Comprehensive profile
    input_data = {
        "academic": {
            "gpa": 3.9,
            "major": "Data Science",
            "minor": "Economics",
            "subjects": [
                "Machine Learning",
                "Statistics",
                "Linear Algebra",
                "Deep Learning",
                "NLP"
            ],
            "strong_areas": ["Mathematics", "Programming"],
            "weak_areas": ["Networking"]
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
                "Teamwork",
                "Leadership"
            ],
            "certifications": [
                "AWS ML Specialist",
                "Google Data Analytics"
            ]
        },
        "interests": {
            "fields": [
                "Machine Learning",
                "Data Science",
                "AI Research",
                "Quantitative Finance",
                "Healthcare Analytics"
            ],
            "activities": [
                "Kaggle competitions",
                "Research projects",
                "Open source contribution",
                "Teaching others"
            ],
            "industries": [
                "Tech",
                "Finance",
                "Healthcare",
                "Startups"
            ]
        },
        "preferences": {
            "work_style": "Collaborative mixed remote",
            "salary_range": "120k-200k",
            "location": "San Francisco Bay Area or New York",
            "career_growth": "Fast-track to leadership",
            "impact": "Meaningful work",
            "learning": "Cutting-edge tech"
        }
    }
    
    result = await workflow.execute(student_id=3, input_data=input_data)
    print("=== Comprehensive Career Analysis ===\n")
    print(result["final_report"])


# ============ Example 5: Multiple Students ============

async def example_batch_processing(db: Session):
    """Example: Process multiple students"""
    from app.agents.simple_langgraph import SimpleLangGraphWorkflow
    
    workflow = SimpleLangGraphWorkflow(db)
    
    students_data = [
        {
            "id": 1,
            "data": {
                "academic": {"gpa": 3.8},
                "skills": {"technical": ["Python"]},
                "interests": {"fields": ["AI"]},
                "preferences": {"salary_range": "100k-150k"}
            }
        },
        {
            "id": 2,
            "data": {
                "academic": {"gpa": 3.5},
                "skills": {"technical": ["JavaScript"]},
                "interests": {"fields": ["Web Development"]},
                "preferences": {"salary_range": "80k-120k"}
            }
        }
    ]
    
    print("Processing multiple students...\n")
    for student_info in students_data:
        print(f"Student {student_info['id']}:")
        result = await workflow.execute(
            student_id=student_info["id"],
            input_data=student_info["data"]
        )
        print(f"Final Recommendation:\n{result['final_report'][:200]}...\n")


# ============ Main ============

async def run_all_examples(db: Session):
    """Run all examples"""
    print("=" * 80)
    print("SIMPLE LANGGRAPH WORKFLOW EXAMPLES")
    print("=" * 80)
    
    try:
        print("\n1. Basic Workflow")
        print("-" * 40)
        await example_basic_workflow(db)
        
        print("\n2. Minimal Input")
        print("-" * 40)
        await example_minimal(db)
        
        print("\n3. Detailed Profile")
        print("-" * 40)
        await example_detailed(db)
        
        print("\n4. Batch Processing")
        print("-" * 40)
        await example_batch_processing(db)
        
        print("\n" + "=" * 80)
        print("All examples completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Simple LangGraph examples module.")
    print("\nTo run example via HTTP API:")
    print("  curl -X POST http://localhost:8000/api/agents/simple/career-guide/1 \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"academic\":{\"gpa\":3.8},\"skills\":{\"technical\":[\"Python\"]}}'")
