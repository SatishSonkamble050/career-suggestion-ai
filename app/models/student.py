"""Student Model"""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Student(Base):
    """Student database model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    grade_level = Column(Integer, nullable=True)
    gpa = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(String(50), nullable=True)  # active, inactive, deleted
    
    # Relationships
    skills = relationship("Skills", back_populates="student", cascade="all, delete-orphan")
    interests = relationship("Interests", back_populates="student", cascade="all, delete-orphan")
    career_preferences = relationship("CareerPreferences", back_populates="student", cascade="all, delete-orphan")
    academic_profile = relationship("StudentAcademicProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    career_reports = relationship("CareerReport", back_populates="student", cascade="all, delete-orphan")
