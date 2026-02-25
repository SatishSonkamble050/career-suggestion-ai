"""Career Preferences Schema"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CareerPreferencesBase(BaseModel):
    """Base career preferences schema"""
    career_path: str
    match_score: Optional[float] = Field(0.0, ge=0, le=100)
    reasoning: Optional[str] = None
    prefer_government_job: Optional[bool] = False
    willing_to_relocate: Optional[bool] = False
    income_expectation: Optional[int] = None
    work_life_balance: Optional[str] = "medium"
    study_abroad: Optional[bool] = False
    entrepreneurship: Optional[bool] = False


class CareerPreferencesCreate(CareerPreferencesBase):
    """Schema for creating career preferences"""
    student_id: int


class CareerPreferencesUpdate(BaseModel):
    """Schema for updating career preferences"""
    career_path: Optional[str] = None
    match_score: Optional[float] = Field(None, ge=0, le=100)
    reasoning: Optional[str] = None
    prefer_government_job: Optional[bool] = None
    willing_to_relocate: Optional[bool] = None
    income_expectation: Optional[int] = None
    work_life_balance: Optional[str] = None
    study_abroad: Optional[bool] = None
    entrepreneurship: Optional[bool] = None


class CareerPreferencesResponse(CareerPreferencesBase):
    """Schema for career preferences response"""
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
