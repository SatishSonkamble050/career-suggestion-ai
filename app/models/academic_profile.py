"""Student Academic Profile Models"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class StudentAcademicProfile(Base):
    """Student academic profile model"""
    __tablename__ = "student_academic_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    
    stream = Column(String(100), nullable=False)
    current_class = Column(String(50), nullable=False)
    result = Column(String(50), nullable=False)
    
    strongest_subject = Column(String(100), nullable=False)
    weakest_subject = Column(String(100), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="academic_profile")
    subjects = relationship("StudentSubjectMark", back_populates="academic_profile", cascade="all, delete-orphan")


class StudentSubjectMark(Base):
    """Student subject marks model"""
    __tablename__ = "student_subject_marks"

    id = Column(Integer, primary_key=True, index=True)
    academic_profile_id = Column(Integer, ForeignKey("student_academic_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    subject_name = Column(String(100), nullable=False)
    marks = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    academic_profile = relationship("StudentAcademicProfile", back_populates="subjects")
