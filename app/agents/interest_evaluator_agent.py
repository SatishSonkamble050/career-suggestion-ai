"""Interest Evaluator Agent"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base_agent import BaseAgent, AgentResponse
from app.agents.agent_tools import AgentTools


class InterestEvaluatorAgent(BaseAgent):
    """Agent specialized in understanding and evaluating student interests"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize Interest Evaluator Agent"""
        super().__init__(
            name="Interest Evaluator",
            agent_type="interest_evaluator",
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
        Evaluate student interests and suggest matching careers
        
        Args:
            student_id: ID of the student
            
        Returns:
            AgentResponse with interest evaluation and career matches
        """
        try:
            # Get student data
            interests = self.tools.get_student_interests(student_id)
            profile = self.tools.get_student_profile(student_id)
            skills = self.tools.get_student_skills(student_id)
            
            if "error" in profile:
                return self._create_response(
                    status="error",
                    message="Student not found",
                    data={},
                    reasoning="Unable to fetch student profile"
                )
            
            # Create prompt for interest evaluation
            system_prompt = """You are a career interest assessment specialist. Analyze the student's 
            interests and match them with suitable careers and fields. Provide deep insights into 
            why these interests align with specific career paths."""
            
            user_prompt = f"""
            Evaluate the student's interests:
            
            Student: {profile.get('name')}
            Grade Level: {profile.get('grade_level')}
            
            Interests: {interests}
            Current Skills: {skills}
            
            Please provide:
            1. Analysis of interest patterns
            2. Top 5 matching career fields
            3. How interests align with each field
            4. Industries with growth potential
            5. Recommended exploration activities
            """
            
            # Get LLM evaluation
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            evaluation_text = response.content
            
            # Prepare evaluation data
            evaluation_data = {
                "student_id": student_id,
                "student_name": profile.get('name'),
                "interests": interests,
                "interest_count": len(interests),
                "evaluation_text": evaluation_text,
                "generated_at": datetime.now().isoformat(),
                "analysis_depth": "comprehensive"
            }
            
            # Add to history
            self.add_to_history("assistant", evaluation_text)
            
            return self._create_response(
                status="success",
                message="Interest evaluation completed successfully",
                data=evaluation_data,
                reasoning="Analyzed interests and identified matching career fields",
                confidence=0.88
            )
            
        except Exception as e:
            return self._create_response(
                status="error",
                message=f"Error evaluating interests: {str(e)}",
                data={},
                reasoning=str(e)
            )
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools for this agent"""
        return [
            {"name": "get_student_interests", "description": "Get student interests"},
            {"name": "get_student_profile", "description": "Get student profile"},
            {"name": "get_student_skills", "description": "Get student skills"},
        ]
