"""Academic Profile Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.academic_profile import (
    StudentAcademicProfileCreate,
    StudentAcademicProfileCreateWithStudent,
    StudentAcademicProfileUpdate,
    StudentAcademicProfileResponse,
    StudentSubjectMarkCreate,
    StudentSubjectMarkResponse
)
from app.crud import academic_profile

router = APIRouter(prefix="/api/v1/academic-profiles", tags=["academic_profiles"])


@router.post("", response_model=StudentAcademicProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile_with_student_id(
    profile_data: StudentAcademicProfileCreateWithStudent,
    db: Session = Depends(get_db)
):
    """Create academic profile with student_id in payload"""
    existing_profile = academic_profile.get_academic_profile_by_student_id(db, profile_data.student_id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already has an academic profile"
        )
    
    # Convert to StudentAcademicProfileCreate (without student_id)
    profile_create = StudentAcademicProfileCreate(
        stream=profile_data.stream,
        current_class=profile_data.current_class,
        result=profile_data.result,
        strongest_subject=profile_data.strongest_subject,
        weakest_subject=profile_data.weakest_subject,
        subjects=profile_data.subjects
    )
    
    return academic_profile.create_academic_profile(db, profile_data.student_id, profile_create)


@router.get("/{profile_id}", response_model=StudentAcademicProfileResponse)
async def get_academic_profile_endpoint(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get academic profile by ID"""
    db_profile = academic_profile.get_academic_profile_by_id(db, profile_id)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found"
        )
    return db_profile




@router.post("/student/{student_id}", response_model=StudentAcademicProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_academic_profile_endpoint(
    student_id: int,
    profile_data: StudentAcademicProfileCreate,
    db: Session = Depends(get_db)
):
    """Create academic profile for a student - updates if already exists"""
    existing_profile = academic_profile.get_academic_profile_by_student_id(db, student_id)
    if existing_profile:
        # Update existing profile
        return academic_profile.update_academic_profile(
            db=db,
            profile_id=existing_profile.id,
            academic_profile=StudentAcademicProfileUpdate(**profile_data.dict())
        )
    
    # Create new profile
    return academic_profile.create_academic_profile(db, student_id, profile_data)



@router.get("/student/{student_id}", response_model=StudentAcademicProfileResponse)
async def get_profile_by_student_endpoint(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get academic profile by student ID"""
    db_profile = academic_profile.get_academic_profile_by_student_id(db, student_id)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found for this student"
        )
    return db_profile


@router.put("/{profile_id}", response_model=StudentAcademicProfileResponse)
async def update_academic_profile_endpoint(
    profile_id: int,
    profile_update: StudentAcademicProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update academic profile"""
    db_profile = academic_profile.update_academic_profile(db, profile_id, profile_update)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found"
        )
    return db_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_academic_profile_endpoint(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Delete academic profile"""
    success = academic_profile.delete_academic_profile(db, profile_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found"
        )


@router.post("/{profile_id}/subjects", response_model=StudentSubjectMarkResponse, status_code=status.HTTP_201_CREATED)
async def add_subject_mark_endpoint(
    profile_id: int,
    mark_data: StudentSubjectMarkCreate,
    db: Session = Depends(get_db)
):
    """Add subject mark to academic profile"""
    db_profile = academic_profile.get_academic_profile_by_id(db, profile_id)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found"
        )
    
    return academic_profile.add_subject_mark(
        db,
        profile_id,
        mark_data.subject_name,
        mark_data.marks
    )


@router.get("/{profile_id}/subjects", response_model=list[StudentSubjectMarkResponse])
async def get_subject_marks_endpoint(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get all subject marks for a profile"""
    db_profile = academic_profile.get_academic_profile_by_id(db, profile_id)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic profile not found"
        )
    
    return academic_profile.get_subject_marks(db, profile_id)


@router.delete("/subjects/{mark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject_mark_endpoint(
    mark_id: int,
    db: Session = Depends(get_db)
):
    """Delete subject mark"""
    success = academic_profile.delete_subject_mark(db, mark_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject mark not found"
        )
