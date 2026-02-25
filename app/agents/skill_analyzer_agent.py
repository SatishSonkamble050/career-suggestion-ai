"""Skill Analyzer Agent"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base_agent import BaseAgent, AgentResponse
from app.agents.agent_tools import AgentTools


class SkillAnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing and evaluating student skills"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize Skill Analyzer Agent"""
        super().__init__(
            name="Skill Analyzer",
            agent_type="skill_analyzer",
            model_name=model_name
        )
        self.db = db
        self.tools = AgentTools(db)
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=1500
        )
    
    async def process(self, student_id: int, target_career: Optional[str] = None, **kwargs) -> AgentResponse:
        """
        Analyze student skills and identify gaps
        
        Args:
            student_id: ID of the student
            target_career: Optional target career to analyze gaps for
            
        Returns:
            AgentResponse with skill analysis
        """
        try:
            # Get student skills
            skills = self.tools.get_student_skills(student_id)
            profile = self.tools.get_student_profile(student_id)
            
            if "error" in profile:
                return self._create_response(
                    status="error",
                    message="Student not found",
                    data={},
                    reasoning="Unable to fetch student profile"
                )
            
            # Analyze skills gaps if target career provided
            gaps_analysis = None
            if target_career:
                gaps_analysis = self.tools.analyze_skills_gaps(student_id, target_career)
            
            # Create prompt for skill analysis
            system_prompt = """You are an expert skill assessment coach. Analyze the student's 
            current skills and provide detailed feedback on strengths, weaknesses, and recommendations 
            for skill development."""
            
            user_prompt = f"""
            Analyze the student's skills:
            
            Student: {profile.get('name')}
            Grade Level: {profile.get('grade_level')}
            Current Skills: {skills}
            """
            
            if gaps_analysis:
                user_prompt += f"\nTarget Career: {target_career}\nSkill Gaps Analysis: {gaps_analysis}"
            
            user_prompt += "\n\nProvide:\n1. Strength assessment\n2. Weakness identification\n3. Development recommendations"
            
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
                "current_skills": skills,
                "skills_count": len(skills),
                "analysis_text": analysis_text,
                "target_career": target_career,
                "generated_at": datetime.now().isoformat()
            }
            
            if gaps_analysis:
                analysis_data["skill_gaps"] = gaps_analysis
            
            # Add to history
            self.add_to_history("assistant", analysis_text)
            
            return self._create_response(
                status="success",
                message="Skill analysis completed successfully",
                data=analysis_data,
                reasoning="Analyzed current skills and identified development areas",
                confidence=0.85
            )
            
        except Exception as e:
            return self._create_response(
                status="error",
                message=f"Error analyzing skills: {str(e)}",
                data={},
                reasoning=str(e)
            )
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools for this agent"""
        return [
            {"name": "get_student_skills", "description": "Get student skills"},
            {"name": "analyze_skills_gaps", "description": "Analyze skills gaps"},
            {"name": "get_student_profile", "description": "Get student profile"},
        ]
