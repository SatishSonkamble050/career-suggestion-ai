"""Career Guidance Engine Service"""
from sqlalchemy.orm import Session
from app.models.student import Student
from app.crud import skills, interests, career_preferences


class CareerEngine:
    """Service for providing career recommendations based on student profile"""
    
    def __init__(self, db: Session):
        """Initialize career engine with database session"""
        self.db = db
    
    def analyze_student(self, student_id: int) -> dict:
        """Analyze student's skills and interests to provide career guidance"""
        from app.crud.student import get_student
        
        student = get_student(self.db, student_id)
        if not student:
            return {"error": "Student not found"}
        
        student_skills = skills.get_student_skills(self.db, student_id)
        student_interests = interests.get_student_interests(self.db, student_id)
        
        return {
            "student_id": student.id,
            "name": student.name,
            "grade_level": student.grade_level,
            "gpa": student.gpa,
            "skills_count": len(student_skills),
            "interests_count": len(student_interests),
            "average_skill_level": self._calculate_average_skill_level(student_skills),
            "top_interests": self._get_top_interests(student_interests),
        }
    
    def generate_recommendations(self, student_id: int) -> list[dict]:
        """Generate career recommendations for a student"""
        from app.crud.student import get_student
        
        student = get_student(self.db, student_id)
        if not student:
            return []
        
        student_skills = skills.get_student_skills(self.db, student_id)
        student_interests = interests.get_student_interests(self.db, student_id)
        
        # Career mapping based on skills and interests
        career_map = {
            "Technology": ["Software Engineer", "Data Scientist", "Web Developer"],
            "Science": ["Researcher", "Biologist", "Chemist"],
            "Art": ["Designer", "Architect", "Artist"],
            "Business": ["Business Analyst", "Consultant", "Entrepreneur"],
        }
        
        recommendations = []
        for interest in student_interests:
            if interest.intensity_level > 50:  # High intensity
                careers = career_map.get(interest.interest_area, [])
                for career in careers:
                    recommendations.append({
                        "career_path": career,
                        "match_score": self._calculate_match_score(student_skills, interest),
                        "reasoning": f"Based on your interest in {interest.interest_area} and your skills"
                    })
        
        return sorted(recommendations, key=lambda x: x["match_score"], reverse=True)[:5]
    
    def _calculate_average_skill_level(self, student_skills: list) -> float:
        """Calculate average skill proficiency level"""
        if not student_skills:
            return 0.0
        return sum(skill.proficiency_level for skill in student_skills) / len(student_skills)
    
    def _get_top_interests(self, student_interests: list, limit: int = 3) -> list[str]:
        """Get top interests by intensity level"""
        sorted_interests = sorted(
            student_interests, 
            key=lambda x: x.intensity_level, 
            reverse=True
        )
        return [interest.interest_area for interest in sorted_interests[:limit]]
    
    def _calculate_match_score(self, student_skills: list, interest) -> float:
        """Calculate career match score based on skills and interests"""
        base_score = interest.intensity_level
        skill_bonus = self._calculate_average_skill_level(student_skills)
        match_score = min(100, (base_score + skill_bonus) / 2)
        return round(match_score, 2)
