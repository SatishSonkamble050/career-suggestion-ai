"""API Router for Career Reports"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.career_report import CareerReportCreate, CareerReportResponse
from app.crud import career_report

router = APIRouter(prefix="/api/v1/career-reports", tags=["career_reports"])


@router.post("/", response_model=CareerReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: CareerReportCreate,
    db: Session = Depends(get_db)
):
    """Create a new career report"""
    return career_report.create_career_report(db, report_data)


@router.get("/{report_id}", response_model=CareerReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific report"""
    db_report = career_report.get_career_report(db, report_id)
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return db_report


@router.get("/student/{student_id}", response_model=List[CareerReportResponse])
async def get_student_reports(
    student_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all reports for a student (paginated)"""
    return career_report.get_student_reports(db, student_id, skip=skip, limit=limit)


@router.get("/student/{student_id}/latest", response_model=CareerReportResponse)
async def get_latest_report(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get the latest report for a student"""
    db_report = career_report.get_latest_report(db, student_id)
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reports found for this student"
        )
    return db_report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Delete a report"""
    success = career_report.delete_career_report(db, report_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )


@router.delete("/student/{student_id}/all", status_code=status.HTTP_200_OK)
async def delete_all_student_reports(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Delete all reports for a student"""
    count = career_report.delete_student_reports(db, student_id)
    return {"deleted_count": count}
