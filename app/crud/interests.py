"""Interests CRUD Operations"""
from sqlalchemy.orm import Session
from app.models.interests import Interests
from app.schemas.interests import InterestsCreate, InterestsUpdate


def get_interest(db: Session, interest_id: int) -> Interests:
    """Get interest by ID"""
    return db.query(Interests).filter(Interests.id == interest_id).first()


def get_student_interests(db: Session, student_id: int) -> list[Interests]:
    """Get all interests for a student"""
    return db.query(Interests).filter(Interests.student_id == student_id).all()


def create_interest(db: Session, interest: InterestsCreate) -> Interests:
    """Create a new interest"""
    db_interest = Interests(**interest.dict())
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest


def update_interest(db: Session, interest_id: int, interest_update: InterestsUpdate) -> Interests:
    """Update interest"""
    db_interest = get_interest(db, interest_id)
    if db_interest:
        db_interest.interests = interest_update.interests
        db.add(db_interest)
        db.commit()
        db.refresh(db_interest)
    return db_interest


def delete_interest(db: Session, interest_id: int) -> bool:
    """Delete interest"""
    db_interest = get_interest(db, interest_id)
    if db_interest:
        db.delete(db_interest)
        db.commit()
        return True
    return False
