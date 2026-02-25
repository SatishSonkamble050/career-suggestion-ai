"""Academic Counselor Agent"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base_agent import BaseAgent, AgentResponse
from app.agents.agent_tools import AgentTools


class AcademicCounselorAgent(BaseAgent):
    """Agent specialized in academic guidance and planning"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize Academic Counselor Agent"""
        super().__init__(
            name="Academic Counselor",
            agent_type="academic_counselor",
            model_name=model_name
        )
        self.db = db
        self.tools = AgentTools(db)
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=1500
        )
    
    async def process(self, student_id: int, **kwargs) -> AgentResponse:
        """
        Provide academic guidance and planning recommendations
        
        Args:
            student_id: ID of the student
            
        Returns:
            AgentResponse with academic guidance
        """
        try:
            # Get student data
            profile = self.tools.get_student_profile(student_id)
            
            if "error" in profile:
                return self._create_response(
                    status="error",
                    message="Student not found",
                    data={},
                    reasoning="Unable to fetch student profile"
                )
            
            skills = self.tools.get_student_skills(student_id)
            interests = self.tools.get_student_interests(student_id)
            preferences = self.tools.get_career_preferences(student_id)
            
            # Create prompt for academic counseling
            system_prompt = """You are an experienced academic counselor. Provide comprehensive 
            academic guidance based on the student's profile, including course recommendations, 
            academic planning, and strategies for improvement."""
            
            user_prompt = f"""
            Provide academic guidance for this student:
            
            Student: {profile.get('name')}
            Grade Level: {profile.get('grade_level')}
            GPA: {profile.get('gpa')}
            Academic Profile: {profile.get('academic_profile')}
            
            Career Interests: {interests}
            Preferred Fields: {preferences}
            Current Skills: {skills}
            
            Please provide:
            1. Academic performance assessment
            2. Course recommendations aligned with career goals
            3. Study strategies and improvement areas
            4. Extracurricular activities to pursue
            5. Timeline for academic milestones
            6. Preparation for higher education/certifications
            """
            
            # Get LLM guidance
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            guidance_text = response.content
            
            # Prepare guidance data
            guidance_data = {
                "student_id": student_id,
                "student_name": profile.get('name'),
                "grade_level": profile.get('grade_level'),
                "current_gpa": profile.get('gpa'),
                "guidance_text": guidance_text,
                "generated_at": datetime.now().isoformat(),
                "guidance_type": "academic_planning"
            }
            
            # Add to history
            self.add_to_history("assistant", guidance_text)
            
            return self._create_response(
                status="success",
                message="Academic guidance generated successfully",
                data=guidance_data,
                reasoning="Analyzed academic profile and career goals",
                confidence=0.87
            )
            
        except Exception as e:
            return self._create_response(
                status="error",
                message=f"Error generating academic guidance: {str(e)}",
                data={},
                reasoning=str(e)
            )
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools for this agent"""
        return [
            {"name": "get_student_profile", "description": "Get student profile"},
            {"name": "get_student_skills", "description": "Get student skills"},
            {"name": "get_student_interests", "description": "Get student interests"},
            {"name": "create_learning_path", "description": "Create learning path"},
        ]
