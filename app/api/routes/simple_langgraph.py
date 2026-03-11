"""API Router for Simplified LangGraph Workflow"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.schemas.report import FinalReport
from app.crud.career_report import create_career_report
from app.schemas.career_report import CareerReportCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.agents.simple_langgraph import SimpleLangGraphWorkflow, CareerGuidanceState
from app.agents.report_graph import build_graph
from app.agents.state import CareerState

router = APIRouter(prefix="/api/agents/simple", tags=["Simple LangGraph"])


class CareerInput(BaseModel):
    """Input data for career guidance workflow"""
    academic: Optional[Dict[str, Any]] = {}
    skills: Optional[Dict[str, Any]] = {}
    interests: Optional[Dict[str, Any]] = {}
    preferences: Optional[Dict[str, Any]] = {}


class StudentInput(BaseModel):
    """Input data for student career queries"""
    student_id: int
    state: Optional[str] = None
    country_name: Optional[str] = None
    academic: Optional[Dict[str, Any]] = {}
    skills: Optional[Dict[str, Any]] = {}
    interests: Optional[Dict[str, Any]] = {}
    preferences: Optional[Dict[str, Any]] = {}


class CareerResponse(FinalReport):
    """Response for career suggestions - extends FinalReport"""
    pass


def get_workflow(db: Session = Depends(get_db)) -> SimpleLangGraphWorkflow:
    """Get workflow instance"""
    return SimpleLangGraphWorkflow(db)


@router.post("/career-guide/{student_id}", response_model=FinalReport)
async def get_career_guidance(
    student_id: int,
    data: CareerInput,
    db: Session = Depends(get_db),
    workflow: SimpleLangGraphWorkflow = Depends(get_workflow)
) -> FinalReport:
    """
    Execute simplified LangGraph workflow for career guidance
    
    Args:
        student_id: Student ID
        data: Career input data (academic, skills, interests, preferences)
    
    Returns:
        Complete career guidance with all analyses and final report
    """
    try:
        input_data = data.dict()
        result = await workflow.execute(student_id, input_data)
        
        # Create a CareerReportCreate object and save to database
        report_data = CareerReportCreate(
            student_id=student_id,
            final_report=result["final_report"]
        )
        db_report = create_career_report(db, report_data)
        
        # Return the final report part of the result
        return result["final_report"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing workflow: {str(e)}"
        )


@router.post("/career/suggest", response_model=CareerResponse)
async def suggest_career(
    data: StudentInput,
    db: Session = Depends(get_db)
) -> CareerResponse:
    """
    Suggest careers using the report graph workflow.
    
    Args:
        data: Student input with academic, skills, interests, preferences
        db: Database session
    
    Returns:
        Career suggestions and guidance with detailed analysis
    """
    try:
        import traceback
        import logging
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        
        logger = logging.getLogger(__name__)
        
        # Prepare initial state
        initial_state: CareerState = {
            "student_id": data.student_id,
            "state_name" : data.state,
            "country_name": data.country_name,

            "input_data": {
                "academic": data.academic or {},
                "skills": data.skills or {},
                "interests": data.interests or {},
                "preferences": data.preferences or {}
            },
            "academic_analysis": None,
            "skill_analysis": None,
            "career_analysis": None,
            "college_analysis": None,
            "salary_analysis": None,
            "roadmap_analysis": None,
            "final_report": None
        }
        
        # Execute workflow in thread pool to avoid blocking
        def run_workflow():
            try:
                graph = build_graph()
                result = graph.invoke(initial_state)
                return result
            except Exception as e:
                logger.error(f"Workflow execution error: {str(e)}")
                logger.error(traceback.format_exc())
                raise
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_workflow)
        
        # Extract final report
        final_report = result.get("final_report", {})
        
        # Save to database
        report_data = CareerReportCreate(
            student_id=data.student_id,
            final_report=final_report
        )
        db_report = create_career_report(db, report_data)
        
        # Return the final report as CareerResponse
        return final_report
    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Career suggestion endpoint error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating career suggestions: {str(e)}"
        )



@router.get("/health")
async def health_check():
    """Check if workflow service is healthy"""
    return {"status": "healthy", "service": "simple_langgraph"}
