"""Interests Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.interests import InterestsCreate, InterestsUpdate, InterestsResponse
from app.crud import interests

router = APIRouter(prefix="/api/v1/interests", tags=["interests"])


@router.get("/student/{student_id}", response_model=list[InterestsResponse])
async def get_student_interests(student_id: int, db: Session = Depends(get_db)):
    """Get all interests for a student"""
    student_interests = interests.get_student_interests(db, student_id)
    return student_interests


@router.get("/{interest_id}", response_model=InterestsResponse)
async def get_interest_by_id(interest_id: int, db: Session = Depends(get_db)):
    """Get interest by ID"""
    db_interest = interests.get_interest(db, interest_id)
    if not db_interest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interest not found")
    return db_interest


@router.post("/", response_model=InterestsResponse, status_code=status.HTTP_201_CREATED)
async def create_interest_endpoint(interest_data: InterestsCreate, db: Session = Depends(get_db)):
    """Create a new interest - updates if student already has interests record"""
    print(f"Received interest data: {interest_data}")
    existing_interests = interests.get_student_interests(db, interest_data.student_id)
    if existing_interests:
        # Update existing interests record (merges interests)
        interest_update = InterestsUpdate(interests=interest_data.interests)
        return interests.update_interest(db, existing_interests[0].id, interest_update)
    # Create new interests record
    print(f"Creating new interest record: {interest_data}")
    return interests.create_interest(db, interest=interest_data)


@router.put("/{interest_id}", response_model=InterestsResponse)
async def update_interest_endpoint(interest_id: int, interest_update: InterestsUpdate, db: Session = Depends(get_db)):
    """Update interest"""
    db_interest = interests.update_interest(db, interest_id, interest_update)
    if not db_interest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interest not found")
    return db_interest


@router.delete("/{interest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interest_endpoint(interest_id: int, db: Session = Depends(get_db)):
    """Delete interest"""
    success = interests.delete_interest(db, interest_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interest not found")
    return None
