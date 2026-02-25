from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.academic_profile import StudentAcademicProfile, StudentSubjectMark
from app.models.skills import Skills
from app.models.interests import Interests
from app.models.career_preferences import CareerPreferences


def load_student_full_profile(db: Session, student_id: int):
    """Load complete student profile from database"""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise Exception("Student not found")

    # Load academic profile
    academic = (
        db.query(StudentAcademicProfile)
        .filter(StudentAcademicProfile.student_id == student_id)
        .first()
    )

    subjects = []
    if academic:
        subject_rows = (
            db.query(StudentSubjectMark)
            .filter(StudentSubjectMark.academic_profile_id == academic.id)
            .all()
        )
        subjects = [
            {"subject_name": s.subject_name, "marks": s.marks}
            for s in subject_rows
        ]

    # Load skills (multiple records)
    skills_rows = (
        db.query(Skills)
        .filter(Skills.student_id == student_id)
        .all()
    )
    skills = [
        {
            "id": s.id,
            "skill_name": s.skill_name,
            "proficiency_level": s.proficiency_level,
            "description": s.description
        }
        for s in skills_rows
    ]

    # Load interests (multiple records)
    interests_rows = (
        db.query(Interests)
        .filter(Interests.student_id == student_id)
        .all()
    )
    interests = [
        {
            "id": i.id,
            "interest_area": i.interest_area,
            "intensity_level": i.intensity_level,
            "description": i.description
        }
        for i in interests_rows
    ]

    # Load career preferences (multiple records)
    preferences_rows = (
        db.query(CareerPreferences)
        .filter(CareerPreferences.student_id == student_id)
        .all()
    )
    preferences = [
        {
            "id": p.id,
            "career_path": p.career_path,
            "match_score": p.match_score,
            "reasoning": p.reasoning
        }
        for p in preferences_rows
    ]

    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade_level": student.grade_level,
            "gpa": student.gpa
        },
        "academic": {
            "stream": academic.stream if academic else None,
            "current_class": academic.current_class if academic else None,
            "result": academic.result if academic else None,
            "strongest_subject": academic.strongest_subject if academic else None,
            "weakest_subject": academic.weakest_subject if academic else None,
            "subjects": subjects
        },
        "skills": skills,
        "interests": interests,
        "preferences": preferences,
    }