"""Configuration for Agent System"""
from pydantic_settings import BaseSettings
from typing import Optional


class AgentSettings(BaseSettings):
    """Agent system configuration"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1500
    
    # LangChain Configuration
    langchain_tracing: bool = False
    langchain_api_key: Optional[str] = None
    
    # Agent Configuration
    agent_timeout: int = 30  # seconds
    max_conversation_history: int = 50
    enable_agent_memory: bool = True
    
    # Performance Configuration
    parallel_agent_execution: bool = True
    max_parallel_agents: int = 3
    
    class Config:
        env_prefix = "AGENT_"
        case_sensitive = False


class AgentPrompts:
    """Predefined prompts for agents"""
    
    CAREER_RECOMMENDER_SYSTEM = """You are an expert career counselor with deep knowledge of job markets, 
    career paths, and skill requirements. Analyze the student profile and recommend 
    suitable career paths with detailed reasoning."""
    
    SKILL_ANALYZER_SYSTEM = """You are an expert skill assessment coach. Analyze the student's 
    current skills and provide detailed feedback on strengths, weaknesses, and recommendations 
    for skill development."""
    
    INTEREST_EVALUATOR_SYSTEM = """You are a career interest assessment specialist. Analyze the student's 
    interests and match them with suitable careers and fields. Provide deep insights into 
    why these interests align with specific career paths."""
    
    ACADEMIC_COUNSELOR_SYSTEM = """You are an experienced academic counselor. Provide comprehensive 
    academic guidance based on the student's profile, including course recommendations, 
    academic planning, and strategies for improvement."""
    
    JOB_MARKET_ANALYST_SYSTEM = """You are an expert job market analyst with knowledge of employment 
    trends, salary data, skill requirements, and career growth opportunities. Provide 
    detailed market insights and recommendations."""
    
    ORCHESTRATOR_SUMMARY = """You are an expert at synthesizing multiple AI agent outputs. 
    Combine insights from all agents to provide actionable career guidance."""


class CareerMappings:
    """Career-to-skills mappings and market data"""
    
    CAREER_SKILLS_MAP = {
        "Software Engineer": ["Python", "JavaScript", "System Design", "Data Structures"],
        "Data Scientist": ["Python", "Statistics", "Machine Learning", "SQL"],
        "UI/UX Designer": ["Figma", "Design Thinking", "User Research", "Prototyping"],
        "Product Manager": ["Analytics", "Strategy", "Communication", "Technical Knowledge"],
        "Data Analyst": ["SQL", "Python", "Excel", "Tableau"],
        "DevOps Engineer": ["Docker", "Kubernetes", "Linux", "CI/CD"],
        "Security Engineer": ["Cybersecurity", "Network Security", "Cryptography", "Penetration Testing"],
        "Machine Learning Engineer": ["Python", "TensorFlow", "Machine Learning", "Deep Learning"],
    }
    
    MARKET_TRENDS = {
        "Technology": {
            "growth_rate": "15%",
            "top_skills": ["AI/ML", "Cloud Computing", "Cybersecurity"],
            "salary_range": "$80,000 - $200,000",
            "demand": "High",
        },
        "Healthcare": {
            "growth_rate": "12%",
            "top_skills": ["Clinical Research", "Patient Care", "Medical Technology"],
            "salary_range": "$60,000 - $150,000",
            "demand": "High",
        },
        "Finance": {
            "growth_rate": "8%",
            "top_skills": ["Financial Analysis", "Risk Management", "Programming"],
            "salary_range": "$70,000 - $180,000",
            "demand": "Medium",
        },
    }
    
    INTERESTS_TO_CAREERS = {
        "Problem Solving": ["Software Engineer", "Data Scientist", "Researcher"],
        "Creative": ["UI/UX Designer", "Product Designer", "Marketing Manager"],
        "Leadership": ["Product Manager", "Project Manager", "Engineering Manager"],
        "Analysis": ["Data Analyst", "Business Analyst", "Financial Analyst"],
        "Research": ["Researcher", "Data Scientist", "Scientist"],
    }


# Global settings instance
agent_settings = AgentSettings()
