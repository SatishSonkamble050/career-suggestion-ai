"""FastAPI Application Factory for Career Guidance App"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import student, skills, interests, career_preferences, auth, academic_profile, agents, simple_langgraph, career_reports
from app.core.database import engine, Base

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    app = FastAPI(
        title="Career Guidance App",
        description="An intelligent career guidance application for students",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    # Include routers
    app.include_router(auth.router)
    app.include_router(student.router)
    app.include_router(academic_profile.router)
    app.include_router(skills.router)
    app.include_router(interests.router)
    app.include_router(career_preferences.router)
    app.include_router(career_reports.router)
    app.include_router(agents.router)
    app.include_router(simple_langgraph.router)
    
    return app

app = create_app()
