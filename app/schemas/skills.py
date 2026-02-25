"""Skills Schema"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SkillsCreate(BaseModel):
    """Schema for creating a skill"""
    student_id: int
    skills: Dict[str, Any]  # JSON object of skills


class SkillsUpdate(BaseModel):
    """Schema for updating a skill"""
    skills: Dict[str, Any]  # JSON object of skills


class SkillsResponse(BaseModel):
    """Schema for skills response"""
    id: int
    student_id: int
    skills: Dict[str, Any]
    updated_at: datetime
    
    class Config:
        from_attributes = True
