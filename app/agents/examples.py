"""
Example usage of the Multi-Agent Career Guidance System

This file demonstrates how to use the agent system with LangChain and LangGraph.
"""

import asyncio
from typing import Optional
from sqlalchemy.orm import Session

# Example 1: Using Individual Agents

async def example_career_recommender(db: Session, student_id: int):
    """Example: Get career recommendations from a single agent"""
    from app.agents.career_recommender_agent import CareerRecommenderAgent
    
    agent = CareerRecommenderAgent(db)
    response = await agent.process(student_id=student_id)
    
    print("Career Recommender Response:")
    print(f"Status: {response.status}")
    print(f"Message: {response.message}")
    print(f"Data: {response.data}")
    print(f"Confidence: {response.confidence}")
    

async def example_skill_analyzer(db: Session, student_id: int, target_career: str):
    """Example: Analyze skills for a target career"""
    from app.agents.skill_analyzer_agent import SkillAnalyzerAgent
    
    agent = SkillAnalyzerAgent(db)
    response = await agent.process(
        student_id=student_id,
        target_career=target_career
    )
    
    print("Skill Analyzer Response:")
    print(f"Status: {response.status}")
    print(f"Message: {response.message}")
    if response.status == "success":
        print(f"Skills Gap: {response.data.get('skill_gaps')}")


async def example_interest_evaluator(db: Session, student_id: int):
    """Example: Evaluate student interests"""
    from app.agents.interest_evaluator_agent import InterestEvaluatorAgent
    
    agent = InterestEvaluatorAgent(db)
    response = await agent.process(student_id=student_id)
    
    print("Interest Evaluator Response:")
    print(f"Status: {response.status}")
    print(f"Analysis: {response.data.get('evaluation_text')}")


async def example_academic_counselor(db: Session, student_id: int):
    """Example: Get academic guidance"""
    from app.agents.academic_counselor_agent import AcademicCounselorAgent
    
    agent = AcademicCounselorAgent(db)
    response = await agent.process(student_id=student_id)
    
    print("Academic Counselor Response:")
    print(f"Status: {response.status}")
    print(f"Guidance: {response.data.get('guidance_text')}")


async def example_job_market_analyst(
    db: Session,
    student_id: int,
    industry: Optional[str] = None
):
    """Example: Analyze job market trends"""
    from app.agents.job_market_analyst_agent import JobMarketAnalystAgent
    
    agent = JobMarketAnalystAgent(db)
    response = await agent.process(
        student_id=student_id,
        industry=industry
    )
    
    print("Job Market Analyst Response:")
    print(f"Status: {response.status}")
    print(f"Market Data: {response.data.get('market_data')}")
    print(f"Analysis: {response.data.get('analysis_text')}")


# Example 2: Using the Agent Orchestrator

async def example_orchestrator_single_request(db: Session, student_id: int):
    """Example: Execute single agent through orchestrator"""
    from app.agents.agent_orchestrator import (
        AgentOrchestrator,
        AgentType
    )
    
    orchestrator = AgentOrchestrator(db)
    
    response = await orchestrator.execute_agent(
        student_id=student_id,
        agent_type=AgentType.CAREER_RECOMMENDER
    )
    
    print("Orchestrator - Career Recommender:")
    print(f"Status: {response.status}")
    print(f"Message: {response.message}")


async def example_orchestrator_multi_request(db: Session, student_id: int):
    """Example: Execute multiple agents through orchestrator"""
    from app.agents.agent_orchestrator import (
        AgentOrchestrator,
        AgentType,
        OrchestrationRequest
    )
    
    orchestrator = AgentOrchestrator(db)
    
    # Create orchestration request
    request = OrchestrationRequest(
        student_id=student_id,
        agent_types=[
            AgentType.SKILL_ANALYZER,
            AgentType.INTEREST_EVALUATOR,
            AgentType.CAREER_RECOMMENDER,
        ],
        context={
            "target_career": "Software Engineer"
        }
    )
    
    # Execute orchestration
    response = await orchestrator.execute_agents(request)
    
    print("Orchestration Response:")
    print(f"Conversation ID: {response.conversation_id}")
    print(f"Status: {response.status}")
    print(f"Agents Executed: {response.agents_executed}")
    print(f"Summary: {response.summary}")
    print("\nIndividual Results:")
    for result in response.results:
        print(f"  - {result.agent_name}: {result.status}")


async def example_orchestrator_comprehensive(db: Session, student_id: int):
    """Example: Get comprehensive career guidance using all agents"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    # Get available agents
    available = orchestrator.get_available_agents()
    print("Available Agents:")
    for agent in available:
        print(f"  - {agent['name']} ({agent['type']})")
    
    print("\nGetting comprehensive guidance...")


async def example_agent_conversation_history(db: Session, student_id: int):
    """Example: Track agent conversation history"""
    from app.agents.career_recommender_agent import CareerRecommenderAgent
    
    agent = CareerRecommenderAgent(db)
    
    # Execute agent
    response1 = await agent.process(student_id=student_id)
    print("First response completed")
    
    # Get conversation history
    history = agent.get_history()
    print(f"Conversation history: {len(history)} messages")
    
    # Clear history
    agent.clear_history()
    print("History cleared")


# Example 3: Error Handling

async def example_error_handling(db: Session):
    """Example: Handle errors gracefully"""
    from app.agents.career_recommender_agent import CareerRecommenderAgent
    
    agent = CareerRecommenderAgent(db)
    
    # Try with non-existent student
    response = await agent.process(student_id=99999)
    
    print("Error Handling Example:")
    print(f"Status: {response.status}")
    print(f"Message: {response.message}")
    if response.status == "error":
        print(f"Error Details: {response.reasoning}")


# Example 4: Using with API

"""
These examples show how to use the agents via the FastAPI API:

1. Get Available Agents:
   GET /api/agents/available

2. Execute Single Agent:
   POST /api/agents/execute/career_recommender?student_id=1

3. Execute Multiple Agents:
   POST /api/agents/execute
   {
     "student_id": 1,
     "agent_types": ["career_recommender", "skill_analyzer"],
     "context": {"target_career": "Software Engineer"}
   }

4. Get Comprehensive Guidance:
   POST /api/agents/career-guidance/1

5. Get Conversation History:
   GET /api/agents/conversation/{conversation_id}

6. Clear Conversation:
   DELETE /api/agents/conversation/{conversation_id}
"""


# Main execution
async def run_examples(db: Session, student_id: int = 1):
    """Run all examples"""
    
    print("=" * 80)
    print("MULTI-AGENT CAREER GUIDANCE SYSTEM - EXAMPLES")
    print("=" * 80)
    
    try:
        print("\n1. Individual Agents Example")
        print("-" * 40)
        await example_career_recommender(db, student_id)
        
        print("\n2. Orchestrator Examples")
        print("-" * 40)
        await example_orchestrator_single_request(db, student_id)
        
        print("\n3. Multi-Agent Orchestration")
        print("-" * 40)
        await example_orchestrator_multi_request(
            db,
            student_id
        )
        
        print("\n4. Conversation History")
        print("-" * 40)
        await example_agent_conversation_history(db, student_id)
        
        print("\n" + "=" * 80)
        print("Examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    To run these examples:
    
    1. Set up your environment with proper database and OpenAI API key
    2. Run: python -m app.agents.examples
    
    Or integrate with your FastAPI app and call the required functions.
    """
    print("This module demonstrates agent usage. Import functions as needed.")
