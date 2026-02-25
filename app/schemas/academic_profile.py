"""Academic Profile Schema"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StudentSubjectMarkCreate(BaseModel):
    """Schema for creating subject marks"""
    subject_name: str
    marks: int


class StudentSubjectMarkResponse(StudentSubjectMarkCreate):
    """Schema for subject marks response"""
    id: int
    academic_profile_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudentAcademicProfileCreate(BaseModel):
    """Schema for creating academic profile"""
    stream: str
    current_class: str
    result: str
    strongest_subject: str
    weakest_subject: str
    subjects: Optional[List[StudentSubjectMarkCreate]] = None


class StudentAcademicProfileCreateWithStudent(BaseModel):
    """Schema for creating academic profile with student_id"""
    student_id: int
    stream: str
    current_class: str
    result: str
    strongest_subject: str
    weakest_subject: str
    subjects: Optional[List[StudentSubjectMarkCreate]] = None


class StudentAcademicProfileUpdate(BaseModel):
    """Schema for updating academic profile"""
    stream: Optional[str] = None
    current_class: Optional[str] = None
    result: Optional[str] = None
    strongest_subject: Optional[str] = None
    weakest_subject: Optional[str] = None
    subjects: Optional[List[StudentSubjectMarkCreate]] = None


class StudentAcademicProfileResponse(BaseModel):
    """Schema for academic profile response"""
    id: int
    student_id: int
    stream: str
    current_class: str
    result: str
    strongest_subject: str
    weakest_subject: str
    created_at: datetime
    updated_at: datetime
    subjects: List[StudentSubjectMarkResponse] = []
    
    class Config:
        from_attributes = True
