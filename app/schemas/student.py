"""Student Schema"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class StudentBase(BaseModel):
    """Base student schema"""
    name: str
    email: EmailStr
    grade_level: int
    gpa: Optional[float] = 0.0
    state: Optional[str] = None


class StudentCreate(StudentBase):
    """Schema for creating a student"""
    password: str


class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    name: Optional[str] = None
    grade_level: Optional[int] = None
    gpa: Optional[float] = None
    state: Optional[str] = None

class StudentResponse(StudentBase):
    """Schema for student response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
