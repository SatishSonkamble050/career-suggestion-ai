"""Career Preferences Model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CareerPreferences(Base):
    """Career Preferences database model"""
    __tablename__ = "career_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    career_path = Column(String(100), nullable=False)
    match_score = Column(Float, default=0.0)  # 0-100
    reasoning = Column(String(500), nullable=True)
    prefer_government_job = Column(Boolean, default=False)
    willing_to_relocate = Column(Boolean, default=False)
    income_expectation = Column(Integer, nullable=True)  # in thousands
    work_life_balance = Column(String(20), default="medium")  # low, medium, high
    study_abroad = Column(Boolean, default=False)
    entrepreneurship = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="career_preferences")
