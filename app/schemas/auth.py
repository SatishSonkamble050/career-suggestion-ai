"""Authentication Schema"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    """Schema for user registration"""
    name: str
    email: EmailStr
    password: str
    grade_level: int
    gpa: Optional[float] = 0.0
    state: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str
    user_id: int
    email: str
    name: str


class TokenData(BaseModel):
    """Schema for token data"""
    email: Optional[str] = None
