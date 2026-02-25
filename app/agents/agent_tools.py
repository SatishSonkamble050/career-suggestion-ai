"""Tools and utilities for AI agents"""
from typing import Any, Callable, Dict, List, Optional
from langchain_core.tools import Tool
from sqlalchemy.orm import Session


class AgentTools:
    """Collection of tools available to agents"""
    
    def __init__(self, db: Session):
        """Initialize agent tools with database connection"""
        self.db = db
    
    def get_student_profile(self, student_id: int) -> Dict[str, Any]:
        """Get comprehensive student profile"""
        from app.crud.student import get_student
        from app.crud.academic_profile import get_student_academic_profile
        
        student = get_student(self.db, student_id)
        if not student:
            return {"error": "Student not found"}
        
        academic_profile = get_student_academic_profile(self.db, student_id)
        
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade_level": student.grade_level,
            "gpa": student.gpa,
            "academic_profile": academic_profile.dict() if academic_profile else None
        }
    
    def get_student_skills(self, student_id: int) -> List[Dict[str, Any]]:
        """Get student's skills and proficiency levels"""
        from app.crud.skills import get_student_skills
        
        skills = get_student_skills(self.db, student_id)
        return [{"skill": s.skill_name, "proficiency": s.proficiency_level} for s in skills]
    
    def get_student_interests(self, student_id: int) -> List[Dict[str, Any]]:
        """Get student's career interests"""
        from app.crud.interests import get_student_interests
        
        interests = get_student_interests(self.db, student_id)
        return [{"interest": i.interest_type, "level": i.interest_level} for i in interests]
    
    def get_career_preferences(self, student_id: int) -> Dict[str, Any]:
        """Get student's career preferences"""
        from app.crud.career_preferences import get_student_career_preferences
        
        prefs = get_student_career_preferences(self.db, student_id)
        if not prefs:
            return {}
        
        return {
            "preferred_industries": prefs.preferred_industries,
            "job_types": prefs.job_types,
            "work_environment": prefs.work_environment,
            "salary_expectations": prefs.salary_expectations
        }
    
    def analyze_skills_gaps(self, student_id: int, target_career: str) -> Dict[str, Any]:
        """Analyze skills gaps for target career"""
        current_skills = self.get_student_skills(student_id)
        
        # Career skill requirements mapping
        career_requirements = {
            "Software Engineer": ["Python", "JavaScript", "System Design", "Data Structures"],
            "Data Scientist": ["Python", "Statistics", "Machine Learning", "SQL"],
            "UI/UX Designer": ["Figma", "Design Thinking", "User Research", "Prototyping"],
            "Product Manager": ["Analytics", "Strategy", "Communication", "Technical Knowledge"],
            "Data Analyst": ["SQL", "Python", "Excel", "Tableau"]
        }
        
        required = career_requirements.get(target_career, [])
        current_skill_names = [s["skill"] for s in current_skills]
        
        gaps = [skill for skill in required if skill not in current_skill_names]
        
        return {
            "target_career": target_career,
            "required_skills": required,
            "current_skills": current_skill_names,
            "skill_gaps": gaps,
            "gap_count": len(gaps),
            "proficiency": len(required) - len(gaps)
        }
    
    def get_job_market_trends(self, industry: str) -> Dict[str, Any]:
        """Get job market trends for an industry"""
        # Simulated job market data
        market_trends = {
            "Technology": {
                "growth_rate": "15%",
                "top_skills": ["AI/ML", "Cloud Computing", "Cybersecurity"],
                "salary_range": "$80,000 - $200,000",
                "demand": "High",
                "opportunities": ["Startup", "Big Tech", "Startups"]
            },
            "Healthcare": {
                "growth_rate": "12%",
                "top_skills": ["Clinical Research", "Patient Care", "Medical Technology"],
                "salary_range": "$60,000 - $150,000",
                "demand": "High",
                "opportunities": ["Hospitals", "Clinics", "Research"]
            },
            "Finance": {
                "growth_rate": "8%",
                "top_skills": ["Financial Analysis", "Risk Management", "Programming"],
                "salary_range": "$70,000 - $180,000",
                "demand": "Medium",
                "opportunities": ["Banks", "Investment Firms", "Fintech"]
            }
        }
        
        return market_trends.get(industry, {"error": f"No data for {industry}"})
    
    def create_learning_path(self, student_id: int, target_skill: str, duration_weeks: int) -> Dict[str, Any]:
        """Create personalized learning path"""
        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "duration_weeks": duration_weeks,
            "learning_path": [
                {"week": i, "milestone": f"Master aspect {i} of {target_skill}"}
                for i in range(1, duration_weeks + 1)
            ],
            "resources": [
                "Online courses",
                "Hands-on projects",
                "Mentoring sessions",
                "Community participation"
            ]
        }
    
    def get_langgraph_tools(self) -> List[Tool]:
        """Get tools in LangGraph format"""
        tools = [
            Tool(
                name="get_student_profile",
                func=self.get_student_profile,
                description="Get comprehensive student profile including basic info and academic details"
            ),
            Tool(
                name="get_student_skills",
                func=self.get_student_skills,
                description="Get student's skills with proficiency levels"
            ),
            Tool(
                name="get_student_interests",
                func=self.get_student_interests,
                description="Get student's career interests"
            ),
            Tool(
                name="get_career_preferences",
                func=self.get_career_preferences,
                description="Get student's career preferences"
            ),
            Tool(
                name="analyze_skills_gaps",
                func=self.analyze_skills_gaps,
                description="Analyze skills gaps for a target career"
            ),
            Tool(
                name="get_job_market_trends",
                func=self.get_job_market_trends,
                description="Get job market trends for an industry"
            ),
            Tool(
                name="create_learning_path",
                func=self.create_learning_path,
                description="Create personalized learning path for a target skill"
            )
        ]
        return tools
