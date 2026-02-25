"""Skills Model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# class Skills(Base):
#     """Skills database model"""
#     __tablename__ = "skills"
    
#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
#     skill_name = Column(String(100), nullable=False)
#     proficiency_level = Column(Float, default=0.0)  # 0-100
#     description = Column(String(500), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     student = relationship("Student", back_populates="skills")

class Skills(Base):
    """Skills database model"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    # skill_name = Column(String(100), nullable=False)
    # proficiency_level = Column(Float, default=0.0)  # 0-100
    # description = Column(String(500), nullable=True)
    # created_at = Column(DateTime, default=datetime.utcnow)
    skills = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="skills")
