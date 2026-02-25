"""Career Preferences CRUD Operations"""
from sqlalchemy.orm import Session
from app.models.career_preferences import CareerPreferences
from app.schemas.career_preferences import CareerPreferencesCreate, CareerPreferencesUpdate


def get_career_preference(db: Session, preference_id: int) -> CareerPreferences:
    """Get career preference by ID"""
    return db.query(CareerPreferences).filter(CareerPreferences.id == preference_id).first()


def get_student_career_preferences(db: Session, student_id: int) -> list[CareerPreferences]:
    """Get all career preferences for a student"""
    return db.query(CareerPreferences).filter(CareerPreferences.student_id == student_id).all()


def create_career_preference(db: Session, preference: CareerPreferencesCreate) -> CareerPreferences:
    """Create a new career preference"""
    db_preference = CareerPreferences(**preference.dict())
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference


def update_career_preference(db: Session, preference_id: int, preference_update: CareerPreferencesUpdate) -> CareerPreferences:
    """Update career preference"""
    db_preference = get_career_preference(db, preference_id)
    if db_preference:
        update_data = preference_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_preference, key, value)
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
    return db_preference


def delete_career_preference(db: Session, preference_id: int) -> bool:
    """Delete career preference"""
    db_preference = get_career_preference(db, preference_id)
    if db_preference:
        db.delete(db_preference)
        db.commit()
        return True
    return False
