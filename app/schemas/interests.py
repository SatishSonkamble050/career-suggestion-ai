"""Interests Schema"""
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class InterestsCreate(BaseModel):
    """Schema for creating interests"""
    student_id: int
    interests: Dict[str, Any]  # JSON object of interests


class InterestsUpdate(BaseModel):
    """Schema for updating interests"""
    interests: Dict[str, Any]  # JSON object of interests


class InterestsResponse(BaseModel):
    """Schema for interests response"""
    id: int
    student_id: int
    interests: Dict[str, Any]
    updated_at: datetime
    
    class Config:
        from_attributes = True
