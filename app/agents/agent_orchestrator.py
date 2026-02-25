"""Agent Orchestrator using LangGraph"""
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Session
# from langchain.agents import create_openai_functions_agent  # Deprecated in newer langchain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from app.agents.career_recommender_agent import CareerRecommenderAgent
from app.agents.skill_analyzer_agent import SkillAnalyzerAgent
from app.agents.interest_evaluator_agent import InterestEvaluatorAgent
from app.agents.academic_counselor_agent import AcademicCounselorAgent
from app.agents.job_market_analyst_agent import JobMarketAnalystAgent
from app.agents.base_agent import AgentResponse
try:
    from app.agents.langgraph_workflow import MultiAgentWorkflow, WorkflowConfig
except ImportError:
    MultiAgentWorkflow = None
    WorkflowConfig = None


class AgentType(str, Enum):
    """Available agent types"""
    CAREER_RECOMMENDER = "career_recommender"
    SKILL_ANALYZER = "skill_analyzer"
    INTEREST_EVALUATOR = "interest_evaluator"
    ACADEMIC_COUNSELOR = "academic_counselor"
    JOB_MARKET_ANALYST = "job_market_analyst"


class OrchestrationRequest(BaseModel):
    """Request for agent orchestration"""
    student_id: int
    agent_types: List[AgentType]
    context: Dict[str, Any] = {}
    conversation_id: Optional[str] = None


class OrchestrationResponse(BaseModel):
    """Response from agent orchestration"""
    conversation_id: str
    student_id: int
    timestamp: datetime
    agents_executed: List[str]
    results: List[AgentResponse]
    summary: str
    status: str


class AgentOrchestrator:
    """Main orchestrator for managing multiple AI agents using LangGraph"""
    
    def __init__(self, db: Session, model_name: str = "gpt-3.5-turbo"):
        """Initialize the agent orchestrator"""
        self.db = db
        self.model_name = model_name
        self.agents: Dict[AgentType, Any] = {}
        self._initialize_agents()
        self.conversation_history = {}
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Initialize LangGraph workflow
        self.workflow_config = WorkflowConfig(
            max_retries=3,
            agent_timeout=30,
            enable_parallel_execution=True,
            verbose_logging=True
        )
        self.langgraph_workflow = MultiAgentWorkflow(db, self.workflow_config)
    
    def _initialize_agents(self) -> None:
        """Initialize all available agents"""
        self.agents = {
            AgentType.CAREER_RECOMMENDER: CareerRecommenderAgent(self.db, self.model_name),
            AgentType.SKILL_ANALYZER: SkillAnalyzerAgent(self.db, self.model_name),
            AgentType.INTEREST_EVALUATOR: InterestEvaluatorAgent(self.db, self.model_name),
            AgentType.ACADEMIC_COUNSELOR: AcademicCounselorAgent(self.db, self.model_name),
            AgentType.JOB_MARKET_ANALYST: JobMarketAnalystAgent(self.db, self.model_name),
        }
    
    async def execute_agents(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """
        Execute multiple agents in orchestrated manner
        
        Args:
            request: OrchestrationRequest with student ID and agent types
            
        Returns:
            OrchestrationResponse with results from all agents
        """
        from uuid import uuid4
        
        conversation_id = request.conversation_id or str(uuid4())
        results: List[AgentResponse] = []
        agents_executed: List[str] = []
        
        try:
            # Execute each requested agent
            for agent_type in request.agent_types:
                if agent_type in self.agents:
                    agent = self.agents[agent_type]
                    response = await agent.process(
                        student_id=request.student_id,
                        **request.context
                    )
                    results.append(response)
                    agents_executed.append(agent.name)
            
            # Generate orchestration summary
            summary = await self._generate_summary(request.student_id, results)
            
            # Store conversation
            self.conversation_history[conversation_id] = {
                "student_id": request.student_id,
                "agents_executed": agents_executed,
                "results": results,
                "timestamp": datetime.now()
            }
            
            return OrchestrationResponse(
                conversation_id=conversation_id,
                student_id=request.student_id,
                timestamp=datetime.now(),
                agents_executed=agents_executed,
                results=results,
                summary=summary,
                status="success"
            )
            
        except Exception as e:
            return OrchestrationResponse(
                conversation_id=conversation_id,
                student_id=request.student_id,
                timestamp=datetime.now(),
                agents_executed=agents_executed,
                results=results,
                summary=f"Error during orchestration: {str(e)}",
                status="error"
            )
    
    async def execute_agent(
        self,
        student_id: int,
        agent_type: AgentType,
        **kwargs
    ) -> AgentResponse:
        """Execute a single agent"""
        if agent_type not in self.agents:
            return AgentResponse(
                agent_name="Unknown",
                agent_type=str(agent_type),
                timestamp=datetime.now(),
                status="error",
                message=f"Agent type {agent_type} not found",
                data={}
            )
        
        agent = self.agents[agent_type]
        return await agent.process(student_id=student_id, **kwargs)
    
    async def _generate_summary(self, student_id: int, results: List[AgentResponse]) -> str:
        """Generate orchestration summary using LLM"""
        try:
            results_text = "\n\n".join([
                f"{r.agent_name} ({r.agent_type}):\n{r.message}\nData: {r.data}"
                for r in results
            ])
            
            prompt = f"""
            Summarize the following multi-agent analysis results for student {student_id}:
            
            {results_text}
            
            Provide a concise, actionable summary combining insights from all agents.
            """
            
            messages = [
                SystemMessage(content="You are an expert at synthesizing multiple AI agent outputs."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def get_conversation_history(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve conversation history"""
        return self.conversation_history.get(conversation_id)
    
    def get_available_agents(self) -> List[Dict[str, str]]:
        """Get list of available agents"""
        return [
            {
                "type": str(agent_type),
                "name": agent.name,
                "description": f"Agent specialized in {agent.agent_type.replace('_', ' ')}"
            }
            for agent_type, agent in self.agents.items()
        ]
    
    def clear_conversation_history(self, conversation_id: str) -> bool:
        """Clear conversation history"""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
            return True
        return False
    
    # ============ LangGraph Workflow Methods ============
    
    async def execute_with_langgraph(
        self,
        student_id: int,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        enable_logging: bool = True
    ) -> Dict[str, Any]:
        """
        Execute multi-agent workflow using LangGraph
        
        This method uses the LangGraph StateGraph to manage agent execution
        with proper state management and routing.
        
        Args:
            student_id: Student ID
            conversation_id: Optional conversation ID
            context: Additional context for agents
            enable_logging: Enable verbose logging
            
        Returns:
            Complete workflow results
        """
        from uuid import uuid4
        
        conv_id = conversation_id or str(uuid4())
        
        # Update workflow config
        self.workflow_config.verbose_logging = enable_logging
        self.langgraph_workflow = MultiAgentWorkflow(self.db, self.workflow_config)
        
        # Execute workflow
        result = await self.langgraph_workflow.execute_workflow(
            student_id=student_id,
            conversation_id=conv_id,
            context=context
        )
        
        # Store in history
        self.conversation_history[conv_id] = {
            "student_id": student_id,
            "workflow_result": result,
            "timestamp": datetime.now(),
            "execution_method": "langgraph"
        }
        
        return result
    
    def get_workflow_graph_visualization(self) -> str:
        """Get ASCII visualization of the LangGraph workflow"""
        return self.langgraph_workflow.get_graph_visualization()
    
    async def execute_custom_workflow(
        self,
        student_id: int,
        agent_sequence: List[str],
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> OrchestrationResponse:
        """
        Execute agents in custom sequence using LangGraph state management
        
        Args:
            student_id: Student ID
            agent_sequence: List of agent types in execution order
            conversation_id: Optional conversation ID
            context: Additional context
            
        Returns:
            OrchestrationResponse with results
        """
        from uuid import uuid4
        
        conv_id = conversation_id or str(uuid4())
        results: List[AgentResponse] = []
        agents_executed: List[str] = []
        
        try:
            # Build custom workflow state
            state_data = {
                "student_id": student_id,
                "conversation_id": conv_id,
                "context": context or {},
                "executed_agents": [],
                "agent_results": {}
            }
            
            # Execute agents in sequence
            for agent_type_str in agent_sequence:
                try:
                    agent_type = AgentType[agent_type_str.upper().replace("-", "_")]
                    response = await self.execute_agent(
                        student_id=student_id,
                        agent_type=agent_type,
                        **context or {}
                    )
                    results.append(response)
                    agents_executed.append(response.agent_name)
                except (KeyError, ValueError) as e:
                    continue
            
            # Generate summary
            summary = await self._generate_summary(student_id, results)
            
            # Store conversation
            self.conversation_history[conv_id] = {
                "student_id": student_id,
                "agents_executed": agents_executed,
                "results": results,
                "timestamp": datetime.now(),
                "execution_method": "custom_sequence"
            }
            
            return OrchestrationResponse(
                conversation_id=conv_id,
                student_id=student_id,
                timestamp=datetime.now(),
                agents_executed=agents_executed,
                results=results,
                summary=summary,
                status="success"
            )
            
        except Exception as e:
            return OrchestrationResponse(
                conversation_id=conv_id,
                student_id=student_id,
                timestamp=datetime.now(),
                agents_executed=agents_executed,
                results=results,
                summary=f"Error in custom workflow: {str(e)}",
                status="error"
            )
    
    def get_workflow_execution_stats(self, conversation_id: str) -> Optional[Dict]:
        """Get execution statistics for a workflow"""
        conv_data = self.conversation_history.get(conversation_id)
        if not conv_data:
            return None
        
        stats = {
            "conversation_id": conversation_id,
            "student_id": conv_data.get("student_id"),
            "timestamp": conv_data.get("timestamp"),
            "execution_method": conv_data.get("execution_method", "unknown"),
            "agents_executed": len(conv_data.get("agents_executed", [])),
            "total_results": len(conv_data.get("results", [])),
        }
        
        # Calculate execution times if available
        if "results" in conv_data and conv_data["results"]:
            stats["agent_names"] = [r.agent_name for r in conv_data["results"]]
        
        return stats
    
    async def execute_parallel_agents(
        self,
        student_id: int,
        agent_types: List[AgentType],
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> OrchestrationResponse:
        """
        Execute multiple agents in parallel using LangGraph
        
        Args:
            student_id: Student ID
            agent_types: List of agent types to execute in parallel
            conversation_id: Optional conversation ID
            context: Additional context
            
        Returns:
            OrchestrationResponse with results
        """
        import asyncio
        from uuid import uuid4
        
        conv_id = conversation_id or str(uuid4())
        
        try:
            # Create tasks for parallel execution
            tasks = [
                self.execute_agent(student_id=student_id, agent_type=at, **context or {})
                for at in agent_types
            ]
            
            # Execute all agents in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            valid_results = [r for r in results if isinstance(r, AgentResponse)]
            agents_executed = [r.agent_name for r in valid_results]
            
            # Generate summary
            summary = await self._generate_summary(student_id, valid_results)
            
            # Store conversation
            self.conversation_history[conv_id] = {
                "student_id": student_id,
                "agents_executed": agents_executed,
                "results": valid_results,
                "timestamp": datetime.now(),
                "execution_method": "parallel"
            }
            
            return OrchestrationResponse(
                conversation_id=conv_id,
                student_id=student_id,
                timestamp=datetime.now(),
                agents_executed=agents_executed,
                results=valid_results,
                summary=summary,
                status="success"
            )
            
        except Exception as e:
            return OrchestrationResponse(
                conversation_id=conv_id,
                student_id=student_id,
                timestamp=datetime.now(),
                agents_executed=[],
                results=[],
                summary=f"Error in parallel execution: {str(e)}",
                status="error"
            )

