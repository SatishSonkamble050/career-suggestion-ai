"""Base Agent Class for Career Guidance Agents"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Standard response model for all agents"""
    agent_name: str
    agent_type: str
    timestamp: datetime
    status: str  # success, error, pending
    message: str
    data: Dict[str, Any]
    reasoning: Optional[str] = None
    confidence: Optional[float] = None


class BaseAgent(ABC):
    """Abstract base class for all AI agents"""
    
    def __init__(self, name: str, agent_type: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize base agent
        
        Args:
            name: Agent display name
            agent_type: Type of agent (e.g., 'career_recommender', 'skill_analyzer')
            model_name: LLM model to use
        """
        self.name = name
        self.agent_type = agent_type
        self.model_name = model_name
        self.conversation_history = []
        self.tools = []
        
    @abstractmethod
    async def process(self, **kwargs) -> AgentResponse:
        """Process input and return response"""
        pass
    
    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools available to this agent"""
        pass
    
    def add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def _create_response(
        self,
        status: str,
        message: str,
        data: Dict[str, Any],
        reasoning: Optional[str] = None,
        confidence: Optional[float] = None
    ) -> AgentResponse:
        """Helper method to create agent response"""
        return AgentResponse(
            agent_name=self.name,
            agent_type=self.agent_type,
            timestamp=datetime.now(),
            status=status,
            message=message,
            data=data,
            reasoning=reasoning,
            confidence=confidence
        )
