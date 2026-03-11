"""State definition for Career Graph"""
from typing import TypedDict, Dict, Any


class CareerState(TypedDict, total=False):
    """State for career guidance graph with all fields optional"""
    student_id: Any
    state_name : Any
    country_name : Any
    input_data: Any
    academic_analysis: Any
    skill_analysis: Any
    career_analysis: Any
    college_analysis: Any
    salary_analysis: Any
    roadmap_analysis: Any
    final_report: Any
