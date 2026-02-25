"""Academic Profile CRUD Operations"""
from sqlalchemy.orm import Session
from app.models.academic_profile import StudentAcademicProfile, StudentSubjectMark
from app.schemas.academic_profile import StudentAcademicProfileCreate, StudentAcademicProfileUpdate


def create_academic_profile(
    db: Session, 
    student_id: int, 
    academic_profile: StudentAcademicProfileCreate
) -> StudentAcademicProfile:
    """Create a new academic profile with optional subjects"""
    db_profile = StudentAcademicProfile(
        student_id=student_id,
        stream=academic_profile.stream,
        current_class=academic_profile.current_class,
        result=academic_profile.result,
        strongest_subject=academic_profile.strongest_subject,
        weakest_subject=academic_profile.weakest_subject
    )
    db.add(db_profile)
    db.flush()  # Flush to get the profile ID for subject creation
    
    # Add subjects if provided
    if academic_profile.subjects:
        for subject_data in academic_profile.subjects:
            db_subject = StudentSubjectMark(
                academic_profile_id=db_profile.id,
                subject_name=subject_data.subject_name,
                marks=subject_data.marks
            )
            db.add(db_subject)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_academic_profile_by_id(db: Session, profile_id: int) -> StudentAcademicProfile:
    """Get academic profile by ID"""
    return db.query(StudentAcademicProfile).filter(StudentAcademicProfile.id == profile_id).first()


def get_academic_profile_by_student_id(db: Session, student_id: int) -> StudentAcademicProfile:
    """Get academic profile by student ID"""
    return db.query(StudentAcademicProfile).filter(StudentAcademicProfile.student_id == student_id).first()


def update_academic_profile(
    db: Session,
    profile_id: int,
    academic_profile: StudentAcademicProfileUpdate
) -> StudentAcademicProfile:
    """Update academic profile and subjects - replaces all subjects with new ones"""
    db_profile = db.query(StudentAcademicProfile).filter(StudentAcademicProfile.id == profile_id).first()
    if not db_profile:
        return None
    
    update_data = academic_profile.model_dump(exclude_unset=True)
    
    # Extract subjects from update_data if present
    subjects = update_data.pop('subjects', None)
    
    # Update profile fields
    for field, value in update_data.items():
        if value is not None:
            setattr(db_profile, field, value)
    
    # Always delete existing subjects first
    db.query(StudentSubjectMark).filter(StudentSubjectMark.academic_profile_id == profile_id).delete()
    
    # Add new subjects if provided
    if subjects:
        for subject_data in subjects:
            # Handle both dict and object inputs
            if isinstance(subject_data, dict):
                subject_name = subject_data.get('subject_name')
                marks = subject_data.get('marks')
            else:
                subject_name = subject_data.subject_name
                marks = subject_data.marks
            
            db_subject = StudentSubjectMark(
                academic_profile_id=db_profile.id,
                subject_name=subject_name,
                marks=marks
            )
            db.add(db_subject)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_academic_profile(db: Session, profile_id: int) -> bool:
    """Delete academic profile"""
    db_profile = db.query(StudentAcademicProfile).filter(StudentAcademicProfile.id == profile_id).first()
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True


def add_subject_mark(
    db: Session,
    profile_id: int,
    subject_name: str,
    marks: int
) -> StudentSubjectMark:
    """Add subject mark to academic profile"""
    db_mark = StudentSubjectMark(
        academic_profile_id=profile_id,
        subject_name=subject_name,
        marks=marks
    )
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


def get_subject_marks(db: Session, profile_id: int) -> list[StudentSubjectMark]:
    """Get all subject marks for a profile"""
    return db.query(StudentSubjectMark).filter(StudentSubjectMark.academic_profile_id == profile_id).all()


def delete_subject_mark(db: Session, mark_id: int) -> bool:
    """Delete subject mark"""
    db_mark = db.query(StudentSubjectMark).filter(StudentSubjectMark.id == mark_id).first()
    if not db_mark:
        return False
    
    db.delete(db_mark)
    db.commit()
    return True
