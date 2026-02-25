"""Student Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.crud import student

router = APIRouter(prefix="/api/v1/students", tags=["students"])


@router.get("/", response_model=list[StudentResponse])
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all students"""
    students = student.get_all_students(db, skip=skip, limit=limit)
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    """Get student by ID"""
    db_student = student.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student_endpoint(student_data: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    db_student = student.get_student_by_email(db, email=student_data.email)
    if db_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return student.create_student(db, student=student_data)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_endpoint(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    """Update student"""
    db_student = student.update_student(db, student_id, student_update)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """Delete student"""
    success = student.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return None
