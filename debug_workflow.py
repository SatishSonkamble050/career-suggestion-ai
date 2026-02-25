#!/usr/bin/env python3
"""
Debug script to test the career suggestion workflow
"""
import json
import traceback
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from app.agents.report_graph import build_graph
from app.agents.state import CareerState

def test_career_workflow():
    """Test the career suggestion workflow"""
    try:
        print("1. Building graph...")
        graph = build_graph()
        print("   ✓ Graph built successfully")
        
        print("\n2. Creating initial state...")
        initial_state: CareerState = {
            "student_id": 1,
            "input_data": {
                "academic": {"gpa": 3.8, "strengths": ["Math", "Science"]},
                "skills": {"programming": 8, "communication": 7},
                "interests": {"technology": "high", "business": "medium"},
                "preferences": {"location": "metro", "salary_priority": True}
            },
            "academic_analysis": None,
            "skill_analysis": None,
            "career_analysis": None,
            "college_analysis": None,
            "salary_analysis": None,
            "roadmap_analysis": None,
            "final_report": None
        }
        print("   ✓ Initial state created")
        print(f"   State keys: {list(initial_state.keys())}")
        
        print("\n3. Invoking graph...")
        # Try different invocation methods
        try:
            result = graph.invoke(initial_state)
            print("   ✓ graph.invoke() worked!")
        except AttributeError as e:
            print(f"   ✗ graph.invoke() failed: {e}")
            print("   Trying alternative methods...")
            
            # Try other methods
            if hasattr(graph, '__call__'):
                print("   Trying graph() direct call...")
                result = graph(initial_state)
                print("   ✓ Direct call worked!")
            elif hasattr(graph, 'run'):
                print("   Trying graph.run()...")
                result = graph.run(initial_state)
                print("   ✓ graph.run() worked!")
            else:
                print(f"   Available methods: {[m for m in dir(graph) if not m.startswith('_')]}")
                raise
        
        print("\n4. Result:")
        print(f"   Final report keys: {list(result.get('final_report', {}).keys()) if result.get('final_report') else 'None'}")
        print("   ✓ Workflow completed!")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print(f"\nTraceback:")
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = test_career_workflow()
    if result:
        print("\n✓ Workflow test successful!")
    else:
        print("\n✗ Workflow test failed!")
