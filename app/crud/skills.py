"""Skills CRUD Operations"""
from sqlalchemy.orm import Session
from app.models.skills import Skills
from app.schemas.skills import SkillsCreate, SkillsUpdate


def get_skill(db: Session, skill_id: int) -> Skills:
    """Get skill by ID"""
    return db.query(Skills).filter(Skills.id == skill_id).first()


def get_student_skills(db: Session, student_id: int) -> list[Skills]:
    """Get all skills for a student"""
    return db.query(Skills).filter(Skills.student_id == student_id).all()


def create_skill(db: Session, skill: SkillsCreate) -> Skills:
    """Create a new skill"""
    db_skill = Skills(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def update_skill(db: Session, skill_id: int, skill_update: SkillsUpdate) -> Skills:
    """Update skill - merges new skills with existing ones"""
    db_skill = get_skill(db, skill_id)
    if db_skill:
        # Merge new skills with existing skills
        existing_skills = db_skill.skills or {}
        merged_skills = {**existing_skills, **skill_update.skills}
        db_skill.skills = merged_skills
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
    return db_skill


def delete_skill(db: Session, skill_id: int) -> bool:
    """Delete skill"""
    db_skill = get_skill(db, skill_id)
    if db_skill:
        db.delete(db_skill)
        db.commit()
        return True
    return False
