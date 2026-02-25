"""Models Package"""
from app.models.student import Student
from app.models.skills import Skills
from app.models.interests import Interests
from app.models.career_preferences import CareerPreferences

__all__ = ["Student", "Skills", "Interests", "CareerPreferences"]
