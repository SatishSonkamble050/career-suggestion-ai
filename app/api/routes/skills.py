"""Skills Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.skills import SkillsCreate, SkillsUpdate, SkillsResponse
from app.crud import skills

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])


@router.get("/student/{student_id}", response_model=list[SkillsResponse])
async def get_student_skills(student_id: int, db: Session = Depends(get_db)):
    """Get all skills for a student"""
    student_skills = skills.get_student_skills(db, student_id)
    return student_skills


@router.get("/{skill_id}", response_model=SkillsResponse)
async def get_skill_by_id(skill_id: int, db: Session = Depends(get_db)):
    """Get skill by ID"""
    db_skill = skills.get_skill(db, skill_id)
    if not db_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return db_skill


@router.post("/", response_model=SkillsResponse, status_code=status.HTTP_201_CREATED)
async def create_skill_endpoint(skill_data: SkillsCreate, db: Session = Depends(get_db)):
    """Create a new skill - updates if student already has skills record"""
    print(f"Received skill data: {skill_data}")
    existing_skills = skills.get_student_skills(db, skill_data.student_id)
    if existing_skills:
        # Update existing skills record (merges skills)
        skill_update = SkillsUpdate(skills=skill_data.skills)
        return skills.update_skill(db, existing_skills[0].id, skill_update)
    # Create new skills record
    print(f"Creating new skill record: {skill_data}")
    return skills.create_skill(db, skill=skill_data)


@router.put("/{skill_id}", response_model=SkillsResponse)
async def update_skill_endpoint(skill_id: int, skill_update: SkillsUpdate, db: Session = Depends(get_db)):
    """Update skill"""
    db_skill = skills.update_skill(db, skill_id, skill_update)
    if not db_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return db_skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill_endpoint(skill_id: int, db: Session = Depends(get_db)):
    """Delete skill"""
    success = skills.delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return None
