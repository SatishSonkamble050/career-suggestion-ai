#!/usr/bin/env python3
"""
Initialize database with tables from models
"""
from app.core.database import Base, engine
from app.models import (
    student,
    academic_profile,
    interests,
    skills,
    career_preferences,
    career_report
)

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("Tables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")
