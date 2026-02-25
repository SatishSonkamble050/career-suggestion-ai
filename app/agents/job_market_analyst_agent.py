"""Job Market Analyst Agent"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base_agent import BaseAgent, AgentResponse
from app.agents.agent_tools import AgentTools


class JobMarketAnalystAgent(BaseAgent):
    """Agent specialized in job market analysis and trends"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize Job Market Analyst Agent"""
        super().__init__(
            name="Job Market Analyst",
            agent_type="job_market_analyst",
            model_name=model_name
        )
        self.db = db
        self.tools = AgentTools(db)
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=1500
        )
    
    async def process(self, student_id: int, industry: Optional[str] = None, **kwargs) -> AgentResponse:
        """
        Analyze job market trends and opportunities
        
        Args:
            student_id: ID of the student
            industry: Optional specific industry to analyze
            
        Returns:
            AgentResponse with job market analysis
        """
        try:
            # Get student data
            profile = self.tools.get_student_profile(student_id)
            interests = self.tools.get_student_interests(student_id)
            preferences = self.tools.get_career_preferences(student_id)
            
            if "error" in profile:
                return self._create_response(
                    status="error",
                    message="Student not found",
                    data={},
                    reasoning="Unable to fetch student profile"
                )
            
            # Determine industries to analyze
            industries_to_analyze = [industry] if industry else ["Technology", "Healthcare", "Finance"]
            
            market_data = {}
            for ind in industries_to_analyze:
                market_data[ind] = self.tools.get_job_market_trends(ind)
            
            # Create prompt for market analysis
            system_prompt = """You are an expert job market analyst with knowledge of employment 
            trends, salary data, skill requirements, and career growth opportunities. Provide 
            detailed market insights and recommendations."""
            
            user_prompt = f"""
            Analyze job market opportunities for this student:
            
            Student: {profile.get('name')}
            Interests: {interests}
            Career Preferences: {preferences}
            
            Market Data:
            {market_data}
            
            Please provide:
            1. Current market trends analysis
            2. In-demand skills in relevant industries
            3. Salary outlook and compensation trends
            4. Job growth projections
            5. Emerging opportunities
            6. Competitive advantage strategies
            7. Timeline for career launch
            """
            
            # Get LLM analysis
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            analysis_text = response.content
            
            # Prepare analysis data
            analysis_data = {
                "student_id": student_id,
                "student_name": profile.get('name'),
                "market_data": market_data,
                "industries_analyzed": industries_to_analyze,
                "analysis_text": analysis_text,
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "job_market_trends"
            }
            
            # Add to history
            self.add_to_history("assistant", analysis_text)
            
            return self._create_response(
                status="success",
                message="Job market analysis completed successfully",
                data=analysis_data,
                reasoning="Analyzed market trends and opportunities",
                confidence=0.86
            )
            
        except Exception as e:
            return self._create_response(
                status="error",
                message=f"Error analyzing job market: {str(e)}",
                data={},
                reasoning=str(e)
            )
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools for this agent"""
        return [
            {"name": "get_job_market_trends", "description": "Get job market trends"},
            {"name": "get_student_interests", "description": "Get student interests"},
            {"name": "get_career_preferences", "description": "Get career preferences"},
        ]
