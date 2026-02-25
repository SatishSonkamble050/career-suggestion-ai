"""Career Report Agent"""
import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent, AgentResponse
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class CareerReportAgent(BaseAgent):
    """Agent that generates a comprehensive career report."""

    def __init__(self):
        super().__init__(name="Career Report Agent", agent_type="report_generator")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
        self.prompt_template = """
You are a career report generator. Your task is to compile the analysis from different agents into a single, comprehensive JSON report.

IMPORTANT: Return ONLY valid JSON, no other text before or after.

The report must follow this exact structure:
{{
    "studentName": "Student",
    "testDate": "2026-02-22",
    "topCareers": [
        {{
            "id": "career-id",
            "name": "Career Name",
            "matchPercentage": 80,
            "description": "Description",
            "whyMatches": ["reason1", "reason2"],
            "educationPath": "Education path",
            "coursesNeeded": ["course1", "course2"],
            "skillsNeeded": ["skill1", "skill2"],
            "employmentRate": 92,
            "avgSalary": {{"min": 5, "max": 30, "experience": 5}},
            "growthRate": 22,
            "jobsAvailable": 450000,
            "topCompanies": ["company1", "company2"],
            "alternativeNames": ["alt1"],
            "relatedFields": ["field1"]
        }}
    ],
    "collegeSuggestions": [
        {{
            "id": "college-id",
            "name": "College Name",
            "state": "State",
            "type": "Government",
            "ranking": 3,
            "jeeAdvancedCutoff": 45,
            "relevantCourses": ["course1"],
            "placementRate": 99.2,
            "avgPackage": 28
        }}
    ],
    "salaryPrediction": [
        {{"year": 0, "salary": 6, "role": "Junior Developer"}},
        {{"year": 1, "salary": 8, "role": "Junior Developer"}}
    ],
    "roadmap": [
        {{
            "step": 1,
            "timeline": "Next 6 Months",
            "title": "Foundation",
            "description": "Description",
            "actions": ["action1"],
            "achievements": ["achievement1"]
        }}
    ],
    "backupOptions": []
}}

Here is the data from the other agents:
- Academic Analysis: {academic_analysis}
- Skill Analysis: {skill_analysis}
- Interest Analysis: {interest_analysis}
- Preference Analysis: {preference_analysis}
- Market Analysis: {market_analysis}

Generate a comprehensive JSON report without any markdown formatting or explanations. Return only the raw JSON object.
"""

    async def process(self, **kwargs) -> AgentResponse:
        """
        Executes the agent to generate the career report.

        Args:
            **kwargs: A dictionary containing the analysis from other agents.

        Returns:
            An AgentResponse containing the generated final report.
        """
        prompt = self.prompt_template.format(
            academic_analysis=json.dumps(kwargs.get("academic_analysis", {})),
            skill_analysis=json.dumps(kwargs.get("skill_analysis", {})),
            interest_analysis=json.dumps(kwargs.get("interest_analysis", {})),
            preference_analysis=json.dumps(kwargs.get("preference_analysis", {})),
            market_analysis=json.dumps(kwargs.get("market_analysis", {}))
        )
        response_text = self.llm.invoke([HumanMessage(content=prompt)]).content
        
        try:
            # Clean the response - remove markdown code blocks and extra whitespace
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Try to find JSON object in the response
            if not cleaned_response.startswith("{"):
                # Try to find the first { and last }
                start_idx = cleaned_response.find("{")
                end_idx = cleaned_response.rfind("}") + 1
                if start_idx != -1 and end_idx > start_idx:
                    cleaned_response = cleaned_response[start_idx:end_idx]
            
            # The response from the LLM should be a JSON string.
            report = json.loads(cleaned_response)
            return AgentResponse(
                agent_name=self.name,
                agent_type=self.agent_type,
                timestamp=datetime.utcnow(),
                status="success",
                message="Successfully generated career report.",
                data={"final_report": report}
            )
        except json.JSONDecodeError as e:
            # Handle cases where the LLM response is not valid JSON
            return AgentResponse(
                agent_name=self.name,
                agent_type=self.agent_type,
                timestamp=datetime.utcnow(),
                status="error",
                message=f"Failed to generate valid JSON report: {str(e)}",
                data={"raw_response": response_text, "cleaned_response": cleaned_response if 'cleaned_response' in locals() else None}
            )

    def get_tools(self) -> list:
        """This agent does not use any tools."""
        return []

    async def execute(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent to generate the career report.

        Args:
            agent_input: A dictionary containing the analysis from other agents.

        Returns:
            A dictionary containing the generated final report.
        """
        response = await self.process(**agent_input)
        return response.data

