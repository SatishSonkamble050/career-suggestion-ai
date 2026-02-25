"""API Routes for Multi-Agent System"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.agents.agent_orchestrator import (
    AgentOrchestrator, 
    AgentType, 
    OrchestrationRequest, 
    OrchestrationResponse
)
from app.agents.base_agent import AgentResponse

router = APIRouter(prefix="/api/agents", tags=["AI Agents"])


def get_orchestrator(db: Session = Depends(get_db)) -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    return AgentOrchestrator(db)


@router.get("/available", response_model=List[dict])
async def get_available_agents(orchestrator: AgentOrchestrator = Depends(get_orchestrator)):
    """Get list of available agents"""
    try:
        return orchestrator.get_available_agents()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching available agents: {str(e)}"
        )


@router.post("/execute", response_model=OrchestrationResponse)
async def execute_agents(
    request: OrchestrationRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Execute multiple agents"""
    try:
        response = await orchestrator.execute_agents(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing agents: {str(e)}"
        )


@router.post("/execute/{agent_type}", response_model=AgentResponse)
async def execute_single_agent(
    agent_type: str,
    student_id: int,
    target_career: Optional[str] = None,
    industry: Optional[str] = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Execute a single agent"""
    try:
        # Map string to AgentType
        agent_type_map = {
            "career_recommender": AgentType.CAREER_RECOMMENDER,
            "skill_analyzer": AgentType.SKILL_ANALYZER,
            "interest_evaluator": AgentType.INTEREST_EVALUATOR,
            "academic_counselor": AgentType.ACADEMIC_COUNSELOR,
            "job_market_analyst": AgentType.JOB_MARKET_ANALYST,
        }
        
        if agent_type not in agent_type_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid agent type: {agent_type}"
            )
        
        at = agent_type_map[agent_type]
        kwargs = {}
        
        if target_career:
            kwargs["target_career"] = target_career
        if industry:
            kwargs["industry"] = industry
        
        response = await orchestrator.execute_agent(
            student_id=student_id,
            agent_type=at,
            **kwargs
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing agent: {str(e)}"
        )


@router.post("/career-guidance/{student_id}", response_model=OrchestrationResponse)
async def get_comprehensive_career_guidance(
    student_id: int,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get comprehensive career guidance using all agents"""
    try:
        request = OrchestrationRequest(
            student_id=student_id,
            agent_types=[
                AgentType.SKILL_ANALYZER,
                AgentType.INTEREST_EVALUATOR,
                AgentType.CAREER_RECOMMENDER,
                AgentType.JOB_MARKET_ANALYST,
                AgentType.ACADEMIC_COUNSELOR,
            ]
        )
        response = await orchestrator.execute_agents(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating career guidance: {str(e)}"
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get conversation history"""
    try:
        history = orchestrator.get_conversation_history(conversation_id)
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation: {str(e)}"
        )


@router.delete("/conversation/{conversation_id}")
async def clear_conversation(
    conversation_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Clear conversation history"""
    try:
        success = orchestrator.clear_conversation_history(conversation_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return {"message": "Conversation cleared successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing conversation: {str(e)}"
        )


# ============ LangGraph Workflow Endpoints ============

@router.post("/langgraph/execute/{student_id}")
async def execute_with_langgraph(
    student_id: int,
    conversation_id: Optional[str] = None,
    enable_logging: bool = True,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """
    Execute multi-agent workflow using LangGraph StateGraph
    
    This endpoint uses LangGraph's state management and graph-based
    execution for coordinated multi-agent operations.
    """
    try:
        result = await orchestrator.execute_with_langgraph(
            student_id=student_id,
            conversation_id=conversation_id,
            enable_logging=enable_logging
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing LangGraph workflow: {str(e)}"
        )


@router.get("/langgraph/graph-visualization")
async def get_workflow_visualization(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get ASCII visualization of the LangGraph workflow"""
    try:
        visualization = orchestrator.get_workflow_graph_visualization()
        return {
            "visualization": visualization,
            "format": "ascii"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating visualization: {str(e)}"
        )


@router.post("/langgraph/custom-sequence/{student_id}")
async def execute_custom_sequence(
    student_id: int,
    agent_sequence: List[str],
    conversation_id: Optional[str] = None,
    context: Optional[dict] = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """
    Execute agents in a custom sequence using LangGraph state management
    
    Args:
        student_id: Student ID
        agent_sequence: List of agent types in order
        conversation_id: Optional conversation ID
        context: Additional context for agents
    
    Valid agent types:
    - skill_analyzer
    - interest_evaluator
    - career_recommender
    - academic_counselor
    - job_market_analyst
    """
    try:
        response = await orchestrator.execute_custom_workflow(
            student_id=student_id,
            agent_sequence=agent_sequence,
            conversation_id=conversation_id,
            context=context
        )
        return response.dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing custom sequence: {str(e)}"
        )


@router.post("/langgraph/parallel/{student_id}")
async def execute_parallel_agents(
    student_id: int,
    agent_types: List[str],
    conversation_id: Optional[str] = None,
    context: Optional[dict] = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """
    Execute multiple agents in parallel using LangGraph
    
    This is more efficient than sequential execution for independent agents.
    
    Args:
        student_id: Student ID
        agent_types: List of agent types to execute in parallel
        conversation_id: Optional conversation ID
        context: Additional context for agents
    """
    try:
        # Map string types to AgentType
        agent_type_map = {
            "career_recommender": AgentType.CAREER_RECOMMENDER,
            "skill_analyzer": AgentType.SKILL_ANALYZER,
            "interest_evaluator": AgentType.INTEREST_EVALUATOR,
            "academic_counselor": AgentType.ACADEMIC_COUNSELOR,
            "job_market_analyst": AgentType.JOB_MARKET_ANALYST,
        }
        
        agent_types_enum = []
        for at in agent_types:
            if at not in agent_type_map:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid agent type: {at}"
                )
            agent_types_enum.append(agent_type_map[at])
        
        response = await orchestrator.execute_parallel_agents(
            student_id=student_id,
            agent_types=agent_types_enum,
            conversation_id=conversation_id,
            context=context
        )
        return response.dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing parallel agents: {str(e)}"
        )


@router.get("/langgraph/stats/{conversation_id}")
async def get_workflow_stats(
    conversation_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get execution statistics for a workflow"""
    try:
        stats = orchestrator.get_workflow_execution_stats(conversation_id)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving stats: {str(e)}"
        )
