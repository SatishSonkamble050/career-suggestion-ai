"""Node implementations for Career Graph"""
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .state import CareerState

# Load environment variables
load_dotenv()

# Initialize LLM with error handling
def get_llm():
    """Get LLM instance, initializing only when needed"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, api_key=api_key)

llm = None

def _get_llm():
    """Lazy load LLM"""
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def academic_analyzer(state: CareerState) -> Dict[str, Any]:
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
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        analysis = json.loads(response.content)
    except:
        analysis = {"raw_analysis": response.content}
    
    return {"academic_analysis": analysis}


def skill_matcher(state: CareerState) -> Dict[str, Any]:
    """Match skills with career opportunities"""
    skills_data = state["input_data"].get("skills", {})
    academic_analysis = state.get("academic_analysis", {})
    
    prompt = f"""
    Based on academic analysis and skills, match skills with careers.
    Academic: {json.dumps(academic_analysis)}
    Skills: {json.dumps(skills_data)}
    
    Return JSON with:
    - current_skills (list)
    - proficiency_level (string)
    - skill_gaps (list)
    - in_demand_skills (list)
    - recommended_skill_development (list)
    """
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        analysis = json.loads(response.content)
    except:
        analysis = {"raw_analysis": response.content}
    
    return {"skill_analysis": analysis}


def career_generator(state: CareerState) -> Dict[str, Any]:
    """Generate career recommendations"""
    academic = state.get("academic_analysis", {})
    skills = state.get("skill_analysis", {})
    interests = state["input_data"].get("interests", {})
    preferences = state["input_data"].get("preferences", {})
    
    prompt = f"""
    Generate top 5 career recommendations based on:
    Academic: {json.dumps(academic)}
    Skills: {json.dumps(skills)}
    Interests: {json.dumps(interests)}
    Preferences: {json.dumps(preferences)}
    
    Return ONLY a JSON array (not wrapped in any key) of top 5 career objects.
    Each career object must have exactly these fields:
    - id: string (unique identifier)
    - name: string (career name)
    - matchPercentage: integer (0-100)
    - description: string (brief description)
    - whyMatches: array of strings (reasons why this matches)
    - educationPath: string (required education)
    - coursesNeeded: array of strings
    - skillsNeeded: array of strings
    - employmentRate: integer (percentage 0-100)
    - avgSalary: object with min (integer), max (integer), experience (integer years)
    - growthRate: integer (percentage 0-100)
    - jobsAvailable: integer
    - topCompanies: array of strings
    - alternativeNames: array of strings
    - relatedFields: array of strings
    
    Example format: [{{id: "1", name: "...", matchPercentage: 90, ...}}, ...]
    """
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        # Extract JSON from response
        response_text = response.content.strip()
        
        # Remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parse the JSON
        parsed = json.loads(response_text)
        
        # If wrapped in a "careers" key, unwrap it
        if isinstance(parsed, dict) and "careers" in parsed:
            careers = parsed["careers"]
        elif isinstance(parsed, list):
            careers = parsed
        else:
            careers = [parsed] if parsed else []
        
        # Ensure all careers have proper structure and fix field names
        for career in careers:
            if "avgSalary" in career and isinstance(career["avgSalary"], dict):
                # Fix field name from experienceYears to experience
                if "experienceYears" in career["avgSalary"]:
                    career["avgSalary"]["experience"] = career["avgSalary"].pop("experienceYears")
    except Exception as e:
        careers = []
    
    return {"career_analysis": {"top_careers": careers if isinstance(careers, list) else []}}


def college_recommender(state: CareerState) -> Dict[str, Any]:
    """Recommend colleges based on profile"""
    academic = state.get("academic_analysis", {})
    careers = state.get("career_analysis", {}).get("top_careers", [])
    
    prompt = f"""
    Recommend 6 suitable colleges based on academic profile and top career choices.
    Academic Analysis: {json.dumps(academic)}
    Top Careers: {json.dumps(careers[:3])}
    
    Return ONLY a JSON array (not wrapped in any key) of 6 college objects.
    Each college must have exactly these fields:
    - id: string (unique identifier)
    - name: string (college name)
    - state: string (state/region)
    - type: string (Government or Private)
    - ranking: integer (national ranking)
    - jeeAdvancedCutoff: integer or null (if applicable)
    - relevantCourses: array of strings (program names)
    - placementRate: number (percentage 0-100)
    - avgPackage: number (salary in lakhs)
    
    Example format: [{{id: "1", name: "...", state: "...", type: "...", ...}}, ...]
    """
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        response_text = response.content.strip()
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(response_text)
        
        # If wrapped in a "colleges" key, unwrap it
        if isinstance(parsed, dict) and "colleges" in parsed:
            colleges = parsed["colleges"]
        elif isinstance(parsed, list):
            colleges = parsed
        else:
            colleges = [parsed] if parsed else []
    except:
        colleges = []
    
    return {"college_analysis": {"colleges": colleges if isinstance(colleges, list) else []}}


def salary_predictor(state: CareerState) -> Dict[str, Any]:
    """Predict salary trajectory"""
    top_career = state.get("career_analysis", {}).get("top_careers", [{}])[0]
    
    prompt = f"""
    Based on the top career choice, predict salary progression over 10 years.
    Top Career: {json.dumps(top_career)}
    
    Return ONLY a JSON array (not wrapped in any key) of salary prediction objects for years 0-10.
    Each prediction object must have:
    - year: integer (0 to 10)
    - salary: integer (in thousands, not lakhs)
    - role: string (job title at that level)
    
    Example format: [{{year: 0, salary: 300000, role: "Entry Level"}}, ...]
    """
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        response_text = response.content.strip()
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(response_text)
        
        # If wrapped in a "predictions" key, unwrap it
        if isinstance(parsed, dict) and "predictions" in parsed:
            salary_data = parsed["predictions"]
        elif isinstance(parsed, list):
            salary_data = parsed
        else:
            salary_data = [parsed] if parsed else []
    except:
        salary_data = []
    
    return {"salary_analysis": {"predictions": salary_data if isinstance(salary_data, list) else []}}


def roadmap_planner(state: CareerState) -> Dict[str, Any]:
    """Create career roadmap"""
    top_career = state.get("career_analysis", {}).get("top_careers", [{}])[0]
    skills = state.get("skill_analysis", {})
    
    prompt = f"""
    Create a detailed 18-month career roadmap for reaching the top career choice.
    Career: {json.dumps(top_career)}
    Current Skills: {json.dumps(skills)}
    
    Return ONLY a JSON array (not wrapped in any key) of 4 roadmap step objects.
    Each step must have exactly these fields:
    - step: integer (1 to 4)
    - timeline: string (duration like "0-3 months")
    - title: string (phase name)
    - description: string (what to do in this phase)
    - actions: array of strings (specific actions to take)
    - achievements: array of strings (expected milestones/achievements)
    
    Example format: [{{step: 1, timeline: "0-3 months", title: "...", description: "...", actions: [...], achievements: [...]}}, ...]
    """
    
    response = _get_llm().invoke([HumanMessage(content=prompt)])
    
    try:
        response_text = response.content.strip()
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(response_text)
        
        # If wrapped in a "steps" key, unwrap it
        if isinstance(parsed, dict) and "steps" in parsed:
            roadmap = parsed["steps"]
        elif isinstance(parsed, list):
            roadmap = parsed
        else:
            roadmap = [parsed] if parsed else []
    except:
        roadmap = []
    
    return {"roadmap_analysis": {"steps": roadmap if isinstance(roadmap, list) else []}}


def final_builder(state: CareerState) -> Dict[str, Any]:
    """Build final comprehensive report"""
    from datetime import datetime
    
    # Get data from state
    career_data = state.get("career_analysis", {})
    college_data = state.get("college_analysis", {})
    salary_data = state.get("salary_analysis", {})
    roadmap_data = state.get("roadmap_analysis", {})
    
    # Extract lists and handle wrapping
    careers = career_data.get("top_careers", [])
    if isinstance(careers, dict) and "careers" in careers:
        careers = careers["careers"]
    careers = careers if isinstance(careers, list) else []
    
    colleges = college_data.get("colleges", [])
    if isinstance(colleges, dict) and "colleges" in colleges:
        colleges = colleges["colleges"]
    colleges = colleges if isinstance(colleges, list) else []
    
    salary = salary_data.get("predictions", [])
    if isinstance(salary, dict) and "predictions" in salary:
        salary = salary["predictions"]
    salary = salary if isinstance(salary, list) else []
    
    roadmap = roadmap_data.get("steps", [])
    if isinstance(roadmap, dict) and "steps" in roadmap:
        roadmap = roadmap["steps"]
    roadmap = roadmap if isinstance(roadmap, list) else []
    
    final_report = {
        "studentName": "Student",
        "testDate": datetime.now().strftime("%Y-%m-%d"),
        "topCareers": careers,
        "collegeSuggestions": colleges,
        "salaryPrediction": salary,
        "roadmap": roadmap,
        "backupOptions": []
    }
    
    return {"final_report": final_report}
