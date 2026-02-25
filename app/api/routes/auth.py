"""Authentication Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.crud import student
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new student"""
    # Check if email already exists
    existing_student = student.get_student_by_email(db, email=register_data.email)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(register_data.password)
    
    # Create student with hashed password
    from app.schemas.student import StudentCreate
    student_create = StudentCreate(
        name=register_data.name,
        email=register_data.email,
        password=hashed_password,
        grade_level=register_data.grade_level,
        gpa=register_data.gpa,
        state=register_data.state
    )
    
    db_student = student.create_student(db, student=student_create)
    
    # Create access token
    access_token = create_access_token(data={"sub": db_student.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=db_student.id,
        email=db_student.email,
        name=db_student.name
    )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login student"""
    # Find student by email
    db_student = student.get_student_by_email(db, email=login_data.email)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, db_student.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": db_student.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=db_student.id,
        email=db_student.email,
        name=db_student.name
    )
