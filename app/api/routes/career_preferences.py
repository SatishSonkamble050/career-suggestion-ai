"""Career Preferences Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.career_preferences import CareerPreferencesCreate, CareerPreferencesUpdate, CareerPreferencesResponse
from app.crud import career_preferences

router = APIRouter(prefix="/api/v1/career-preferences", tags=["career_preferences"])


@router.get("/student/{student_id}", response_model=list[CareerPreferencesResponse])
async def get_student_career_preferences(student_id: int, db: Session = Depends(get_db)):
    """Get all career preferences for a student"""
    preferences = career_preferences.get_student_career_preferences(db, student_id)
    return preferences


@router.get("/{preference_id}", response_model=CareerPreferencesResponse)
async def get_career_preference_by_id(preference_id: int, db: Session = Depends(get_db)):
    """Get career preference by ID"""
    db_preference = career_preferences.get_career_preference(db, preference_id)
    if not db_preference:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Career preference not found")
    return db_preference


@router.post("/", response_model=CareerPreferencesResponse, status_code=status.HTTP_201_CREATED)
async def create_career_preference_endpoint(preference_data: CareerPreferencesCreate, db: Session = Depends(get_db)):
    """Create a new career preference or update existing"""
    # Check if student already has career preferences
    existing_preferences = career_preferences.get_student_career_preferences(db, preference_data.student_id)
    print(f"Received career preference data: {existing_preferences}")
    if existing_preferences:
        # Update existing preference (use the first one)
        return await update_career_preference_endpoint(
            preference_id=existing_preferences[0].id, 
            preference_update=CareerPreferencesUpdate(**preference_data.dict()), 
            db=db
        )
    # Create new preference
    return career_preferences.create_career_preference(db, preference=preference_data)


@router.put("/{preference_id}", response_model=CareerPreferencesResponse)
async def update_career_preference_endpoint(preference_id: int, preference_update: CareerPreferencesUpdate, db: Session = Depends(get_db)):
    """Update career preference"""
    db_preference = career_preferences.update_career_preference(db, preference_id, preference_update)
    if not db_preference:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Career preference not found")
    return db_preference


@router.delete("/{preference_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_career_preference_endpoint(preference_id: int, db: Session = Depends(get_db)):
    """Delete career preference"""
    success = career_preferences.delete_career_preference(db, preference_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Career preference not found")
    return None
