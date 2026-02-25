"""Career Recommender Agent"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base_agent import BaseAgent, AgentResponse
from app.agents.agent_tools import AgentTools


class CareerRecommenderAgent(BaseAgent):
    """Agent specialized in recommending career paths based on student profile"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize Career Recommender Agent"""
        super().__init__(
            name="Career Recommender",
            agent_type="career_recommender",
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
        Generate career recommendations for a student
        
        Args:
            student_id: ID of the student
            
        Returns:
            AgentResponse with career recommendations
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
            
            # Create prompt for LLM
            system_prompt = """You are an expert career counselor with deep knowledge of job markets, 
            career paths, and skill requirements. Analyze the student profile and recommend 
            suitable career paths with detailed reasoning."""
            
            user_prompt = f"""
            Based on this student profile, recommend top 3-5 career paths:
            
            Student Profile:
            - Name: {profile.get('name')}
            - Grade Level: {profile.get('grade_level')}
            - GPA: {profile.get('gpa')}
            
            Skills: {skills}
            Interests: {interests}
            Career Preferences: {preferences}
            
            Please provide:
            1. Top 3-5 recommended career paths
            2. Why each path is suitable
            3. Skills needed for each path
            4. Next steps to prepare
            5. Salary expectations
            """
            
            # Get LLM response
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            recommendation_text = response.content
            
            # Parse and structure recommendation
            recommendations = {
                "student_id": student_id,
                "student_name": profile.get('name'),
                "generated_at": datetime.now().isoformat(),
                "recommendation_text": recommendation_text,
                "skills_current": len(skills),
                "interests_count": len(interests)
            }
            
            # Add to history
            self.add_to_history("assistant", recommendation_text)
            
            return self._create_response(
                status="success",
                message="Career recommendations generated successfully",
                data=recommendations,
                reasoning="Analyzed student skills, interests, and preferences",
                confidence=0.9
            )
            
        except Exception as e:
            return self._create_response(
                status="error",
                message=f"Error generating recommendations: {str(e)}",
                data={},
                reasoning=str(e)
            )
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools for this agent"""
        return [
            {"name": "get_student_profile", "description": "Fetch student profile"},
            {"name": "get_student_skills", "description": "Get student skills"},
            {"name": "get_student_interests", "description": "Get student interests"},
            {"name": "get_career_preferences", "description": "Get career preferences"},
        ]
