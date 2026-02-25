"""Simplified LangGraph Workflow for Multi-Agent Career Guidance"""

from app.agents.career_report_agent import CareerReportAgent
from typing import TypedDict, Dict, Any
from app.services.data_loader import load_student_full_profile
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
import json
from sqlalchemy.orm import Session


class CareerGuidanceState(TypedDict):
    """State for career guidance workflow"""
    student_id: int
    input_data: Dict[str, Any]
    
    # Individual analyses
    academic_analysis: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    interest_analysis: Dict[str, Any]
    preference_analysis: Dict[str, Any]
    market_analysis: Dict[str, Any]
    
    # Final output
    final_report: Dict[str, Any]


class SimpleLangGraphWorkflow:
    """Simplified LangGraph workflow for career guidance"""
    
    def __init__(self, db: Session, model: str = "gpt-3.5-turbo"):
        """Initialize workflow with database and LLM"""
        self.db = db
        self.llm = ChatOpenAI(model_name=model, temperature=0.3)
        self.career_report_agent = CareerReportAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        graph = StateGraph(CareerGuidanceState)
        
        # Add nodes
        graph.add_node("academic", self.academic_agent)
        graph.add_node("skills", self.skill_agent)
        graph.add_node("interests", self.interest_agent)
        graph.add_node("preferences", self.preference_agent)
        graph.add_node("market", self.market_agent)
        graph.add_node("report", self.compile_report)
        
        # Set entry point
        graph.set_entry_point("academic")
        
        # Add edges (sequential flow)
        graph.add_edge("academic", "skills")
        graph.add_edge("skills", "interests")
        graph.add_edge("interests", "preferences")
        graph.add_edge("preferences", "market")
        graph.add_edge("market", "report")
        graph.add_edge("report", END)
        
        # Compile graph
        return graph.compile()
    
    async def academic_agent(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Analyze academic profile"""
        academic_data = state["input_data"].get("academic", {})
        
        prompt = f"""
        Analyze this academic profile and return JSON:
        {json.dumps(academic_data)}
        
        Return JSON with:
        - strengths (list of strong areas)
        - areas_for_improvement (list)
        - gpa_analysis (string)
        - subject_recommendations (list)
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"raw_analysis": response.content}
        
        return {"academic_analysis": analysis}
    
    async def skill_agent(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Analyze skills profile"""
        skills_data = state["input_data"].get("skills", {})
        
        prompt = f"""
        Analyze this skills profile and return JSON:
        {json.dumps(skills_data)}
        
        Return JSON with:
        - current_skills (list)
        - proficiency_level (string)
        - skill_gaps (list)
        - in_demand_skills (list)
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"raw_analysis": response.content}
        
        return {"skill_analysis": analysis}
    
    async def interest_agent(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Analyze career interests"""
        interests_data = state["input_data"].get("interests", {})
        
        prompt = f"""
        Analyze these career interests and return JSON:
        {json.dumps(interests_data)}
        
        Return JSON with:
        - interest_clusters (list)
        - preferred_industries (list)
        - career_directions (list)
        - passion_areas (list)
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"raw_analysis": response.content}
        
        return {"interest_analysis": analysis}
    
    async def preference_agent(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Analyze career preferences"""
        preferences_data = state["input_data"].get("preferences", {})
        
        prompt = f"""
        Analyze these career preferences and return JSON:
        {json.dumps(preferences_data)}
        
        Return JSON with:
        - work_environment (string)
        - salary_expectations (string)
        - work_life_balance (string)
        - career_growth (string)
        - location_preferences (string)
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"raw_analysis": response.content}
        
        return {"preference_analysis": analysis}
    
    async def market_agent(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Analyze job market context"""
        prompt = f"""
        Based on the student profile analysis, analyze current job market:
        
        Academic: {json.dumps(state['academic_analysis'])}
        Skills: {json.dumps(state['skill_analysis'])}
        Interests: {json.dumps(state['interest_analysis'])}
        
        Return JSON with:
        - in_demand_roles (list)
        - emerging_fields (list)
        - salary_outlook (string)
        - growth_trends (list)
        - timing_recommendation (string)
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"raw_analysis": response.content}
        
        return {"market_analysis": analysis}
    
    async def compile_report(self, state: CareerGuidanceState) -> Dict[str, Any]:
        """Compile all analyses into a final report."""
        report_input = {
            "academic_analysis": state.get("academic_analysis", {}),
            "skill_analysis": state.get("skill_analysis", {}),
            "interest_analysis": state.get("interest_analysis", {}),
            "preference_analysis": state.get("preference_analysis", {}),
            "market_analysis": state.get("market_analysis", {}),
        }
        
        print("Compiling report with input:", report_input)  # Debugging statement
        report_output = await self.career_report_agent.execute(report_input)
        
        return {"final_report": report_output.get("final_report")}
    
    async def execute(
        self,
        student_id: int,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the workflow
        
        Args:
            student_id: Student ID
            input_data: Dict with keys: academic, skills, interests, preferences
            
        Returns:
            Complete workflow results
        """
        # Initial state
        initial_state: CareerGuidanceState = {
            "student_id": student_id,
            "input_data": input_data,
            "academic_analysis": {},
            "skill_analysis": {},
            "interest_analysis": {},
            "preference_analysis": {},
            "market_analysis": {},
            "final_report": {}
        }
        
        # Execute workflow
        result = await self.graph.ainvoke(initial_state)
        
        return {
            "student_id": result["student_id"],
            "academic_analysis": result["academic_analysis"],
            "skill_analysis": result["skill_analysis"],
            "interest_analysis": result["interest_analysis"],
            "preference_analysis": result["preference_analysis"],
            "market_analysis": result["market_analysis"],
            "final_report": result["final_report"]
        }
