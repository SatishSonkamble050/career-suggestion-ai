"""CRUD operations for Career Reports"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.career_report import CareerReport
from app.schemas.career_report import CareerReportCreate


def create_career_report(db: Session, report: CareerReportCreate) -> CareerReport:
    """Create a new career report"""
    db_report = CareerReport(
        student_id=report.student_id,
        final_report=report.final_report
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_career_report(db: Session, report_id: int) -> Optional[CareerReport]:
    """Get a career report by ID"""
    return db.query(CareerReport).filter(CareerReport.id == report_id).first()


def get_student_reports(
    db: Session, 
    student_id: int,
    skip: int = 0,
    limit: int = 10
) -> List[CareerReport]:
    """Get all reports for a student"""
    return db.query(CareerReport)\
        .filter(CareerReport.student_id == student_id)\
        .order_by(desc(CareerReport.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_latest_report(db: Session, student_id: int) -> Optional[CareerReport]:
    """Get the latest report for a student"""
    return db.query(CareerReport)\
        .filter(CareerReport.student_id == student_id)\
        .order_by(desc(CareerReport.created_at))\
        .first()


def delete_career_report(db: Session, report_id: int) -> bool:
    """Delete a career report"""
    db_report = get_career_report(db, report_id)
    if not db_report:
        return False
    
    db.delete(db_report)
    db.commit()
    return True


def delete_student_reports(db: Session, student_id: int) -> int:
    """Delete all reports for a student"""
    count = db.query(CareerReport).filter(CareerReport.student_id == student_id).count()
    db.query(CareerReport).filter(CareerReport.student_id == student_id).delete()
    db.commit()
    return count
