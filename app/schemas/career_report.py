"""Career Report Schemas"""
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


class CareerReportCreate(BaseModel):
    """Schema for creating a new career report"""
    student_id: int
    final_report: Dict[str, Any] = Field(..., description="Complete career guidance report as JSON")


class CareerReportResponse(BaseModel):
    """Schema for career report response"""
    id: int
    student_id: int
    final_report: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
