"""Pydantic Schemas for Career Report"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AvgSalary(BaseModel):
    min: int
    max: int
    experience: int

class TopCareer(BaseModel):
    id: str
    name: str
    matchPercentage: int
    description: str
    whyMatches: List[str]
    educationPath: str
    coursesNeeded: List[str]
    skillsNeeded: List[str]
    employmentRate: int
    avgSalary: AvgSalary
    growthRate: int
    jobsAvailable: int
    topCompanies: List[str]
    alternativeNames: List[str]
    relatedFields: List[str]

class CollegeSuggestion(BaseModel):
    id: str
    name: str
    state: str
    type: str
    ranking: int
    jeeAdvancedCutoff: Optional[int] = None
    relevantCourses: List[str]
    placementRate: float
    avgPackage: float

class SalaryPrediction(BaseModel):
    year: int
    salary: int
    role: str

class RoadmapStep(BaseModel):
    step: int
    timeline: str
    title: str
    description: str
    actions: List[str]
    achievements: List[str]

class FinalReport(BaseModel):
    studentName: Optional[str] = None
    testDate: Optional[str] = None
    topCareers: List[TopCareer]
    collegeSuggestions: List[CollegeSuggestion]
    salaryPrediction: List[SalaryPrediction]
    roadmap: List[RoadmapStep]
    backupOptions: List[Any]


class StudentInput(BaseModel):
    name: str
    date: str
    marks: Dict[str, int]
    skills: List[str]
    interests: List[str]
    preferences: Dict[str, Any]

class CareerResponse(BaseModel):
    studentName: str
    testDate: str
    topCareers: List[Dict]
    collegeSuggestions: List[Dict]
    salaryPrediction: List[Dict]
    roadmap: List[Dict]
    backupOptions: List[Dict]
