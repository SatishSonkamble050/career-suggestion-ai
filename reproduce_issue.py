import json
import os
from dotenv import load_dotenv
from app.agents.report_graph import build_graph
from app.agents.state import CareerState
from unittest.mock import MagicMock, patch

load_dotenv()

def mock_llm_invoke(*args, **kwargs):
    content = json.dumps({
        "mock": "response", 
        "strengths": [], 
        "areas_for_improvement": [], 
        "gpa_analysis": "Good", 
        "subject_recommendations": [],
        "matched_careers": [{"title": "Software Engineer", "match_score": 0.9}],
        "skills_gap": [],
        "suggested_career": {"title": "Full Stack Dev", "description": "Good choice"},
        "roadmap": [],
        "salary_trend": [],
        "colleges": []
    })
    return MagicMock(content=content)

def reproduction():
    with patch("app.agents.nodes.get_llm") as mock_get_llm:
        print("Mocking LLM")
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = mock_llm_invoke
        mock_get_llm.return_value = mock_llm
        
        # Also patch _get_llm directly just in case provided one is used
        with patch("app.agents.nodes._get_llm", return_value=mock_llm):
            try:
                print("Building graph...")
                graph = build_graph()
                print("Graph built.")
                
                initial_state = {
                    "student_id": 1,
                    "input_data": {
                        "academic": {},
                        "skills": {},
                        "interests": {},
                        "preferences": {}
                    },
                    "academic_analysis": None,
                    "skill_analysis": None,
                    "career_analysis": None,
                    "college_analysis": None,
                    "salary_analysis": None,
                    "roadmap_analysis": None,
                    "final_report": None
                }
                
                print("Invoking graph...")
                result = graph.invoke(initial_state)
                print("Graph invoked successfully.")
                print(result.keys())
                
            except Exception as e:
                print(f"Caught exception: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    reproduction()
