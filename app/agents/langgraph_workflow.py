"""LangGraph Workflow for Multi-Agent Career Guidance System"""
from typing import TypedDict, List, Optional, Any, Annotated
from datetime import datetime
from functools import reduce
import operator
from sqlalchemy.orm import Session

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel


class AgentState(TypedDict, total=False):
    """State passed through the multi-agent workflow"""
    # Student Information
    student_id: int
    student_name: str
    student_profile: dict
    
    # Messages and History
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Agent Execution State
    agents_to_execute: List[str]  # Queue of agents to execute
    executed_agents: List[str]  # Completed agents
    current_agent: Optional[str]  # Currently executing agent
    
    # Results and Data
    agent_results: dict  # Results from each agent {agent_name: result}
    combined_analysis: str  # Synthesized analysis from all agents
    student_data: dict  # Cached student data (skills, interests, etc.)
    
    # Execution Context
    context: dict  # Additional context for agents
    conversation_id: str  # Unique conversation identifier
    timestamp: datetime
    
    # Workflow Control
    next_agent: Optional[str]  # Next agent to execute
    should_continue: bool  # Whether to continue the workflow
    final_response: Optional[str]  # Final response to return


class AgentExecutionInfo(BaseModel):
    """Information about agent execution"""
    agent_name: str
    agent_type: str
    execution_time: float
    status: str  # success, error, skipped
    message: str
    confidence: float
    data_keys: List[str]


class WorkflowConfig(BaseModel):
    """Configuration for the workflow"""
    max_retries: int = 3
    agent_timeout: int = 30
    enable_parallel_execution: bool = True
    verbose_logging: bool = True
    collect_all_results: bool = True


class MultiAgentWorkflow:
    """Multi-agent workflow orchestrator using LangGraph"""
    
    def __init__(self, db: Session, config: Optional[WorkflowConfig] = None):
        """Initialize the multi-agent workflow"""
        self.db = db
        self.config = config or WorkflowConfig()
        self.graph = None
        self.agent_results_cache = {}
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Build the LangGraph StateGraph"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("input_processor", self._process_input)
        workflow.add_node("skill_analyzer", self._execute_skill_analyzer)
        workflow.add_node("interest_evaluator", self._execute_interest_evaluator)
        workflow.add_node("career_recommender", self._execute_career_recommender)
        workflow.add_node("academic_counselor", self._execute_academic_counselor)
        workflow.add_node("job_market_analyst", self._execute_job_market_analyst)
        workflow.add_node("synthesizer", self._synthesize_results)
        workflow.add_node("response_formatter", self._format_final_response)
        
        # Set entry point
        workflow.set_entry_point("input_processor")
        
        # Add conditional edges for routing
        workflow.add_conditional_edges(
            "input_processor",
            self._route_after_input,
            {
                "skill_analyzer": "skill_analyzer",
                "interest_evaluator": "interest_evaluator",
                "career_recommender": "career_recommender",
                "academic_counselor": "academic_counselor",
                "job_market_analyst": "job_market_analyst",
                "synthesizer": "synthesizer",
            }
        )
        
        # Connect agent nodes to next decision point
        for agent in ["skill_analyzer", "interest_evaluator", "career_recommender", 
                      "academic_counselor", "job_market_analyst"]:
            workflow.add_conditional_edges(
                agent,
                self._route_next_agent,
                {
                    "skill_analyzer": "skill_analyzer",
                    "interest_evaluator": "interest_evaluator",
                    "career_recommender": "career_recommender",
                    "academic_counselor": "academic_counselor",
                    "job_market_analyst": "job_market_analyst",
                    "synthesizer": "synthesizer",
                    "end": END,
                }
            )
        
        # Synthesizer to response formatter
        workflow.add_edge("synthesizer", "response_formatter")
        workflow.add_edge("response_formatter", END)
        
        # Compile the graph
        self.graph = workflow.compile()
    
    def _process_input(self, state: AgentState) -> AgentState:
        """Process input and initialize workflow state"""
        if self.config.verbose_logging:
            print(f"[INPUT PROCESSOR] Student ID: {state.get('student_id')}")
        
        # Load student data once
        from app.agents.agent_tools import AgentTools
        tools = AgentTools(self.db)
        
        student_data = {
            "profile": tools.get_student_profile(state["student_id"]),
            "skills": tools.get_student_skills(state["student_id"]),
            "interests": tools.get_student_interests(state["student_id"]),
            "preferences": tools.get_career_preferences(state["student_id"]),
        }
        
        state["student_data"] = student_data
        state["messages"] = [
            HumanMessage(content=f"Analyzing student {state['student_id']}")
        ]
        state["executed_agents"] = []
        state["agent_results"] = {}
        state["should_continue"] = True
        
        return state
    
    def _route_after_input(self, state: AgentState) -> str:
        """Route to first agent after input processing"""
        # Start with skill analyzer
        return "skill_analyzer"
    
    def _execute_skill_analyzer(self, state: AgentState) -> AgentState:
        """Execute skill analyzer agent"""
        return self._execute_agent(
            state=state,
            agent_name="Skill Analyzer",
            agent_type="skill_analyzer",
            target_career=state.get("context", {}).get("target_career")
        )
    
    def _execute_interest_evaluator(self, state: AgentState) -> AgentState:
        """Execute interest evaluator agent"""
        return self._execute_agent(
            state=state,
            agent_name="Interest Evaluator",
            agent_type="interest_evaluator"
        )
    
    def _execute_career_recommender(self, state: AgentState) -> AgentState:
        """Execute career recommender agent"""
        return self._execute_agent(
            state=state,
            agent_name="Career Recommender",
            agent_type="career_recommender"
        )
    
    def _execute_academic_counselor(self, state: AgentState) -> AgentState:
        """Execute academic counselor agent"""
        return self._execute_agent(
            state=state,
            agent_name="Academic Counselor",
            agent_type="academic_counselor"
        )
    
    def _execute_job_market_analyst(self, state: AgentState) -> AgentState:
        """Execute job market analyst agent"""
        return self._execute_agent(
            state=state,
            agent_name="Job Market Analyst",
            agent_type="job_market_analyst",
            industry=state.get("context", {}).get("industry")
        )
    
    def _execute_agent(
        self,
        state: AgentState,
        agent_name: str,
        agent_type: str,
        **kwargs
    ) -> AgentState:
        """Execute a single agent node"""
        import asyncio
        import time
        
        try:
            if self.config.verbose_logging:
                print(f"[{agent_type.upper()}] Executing agent: {agent_name}")
            
            start_time = time.time()
            
            # Import agent dynamically
            if agent_type == "skill_analyzer":
                from app.agents.skill_analyzer_agent import SkillAnalyzerAgent
                agent = SkillAnalyzerAgent(self.db)
                result = asyncio.run(agent.process(
                    student_id=state["student_id"],
                    **kwargs
                ))
            elif agent_type == "interest_evaluator":
                from app.agents.interest_evaluator_agent import InterestEvaluatorAgent
                agent = InterestEvaluatorAgent(self.db)
                result = asyncio.run(agent.process(student_id=state["student_id"]))
            elif agent_type == "career_recommender":
                from app.agents.career_recommender_agent import CareerRecommenderAgent
                agent = CareerRecommenderAgent(self.db)
                result = asyncio.run(agent.process(student_id=state["student_id"]))
            elif agent_type == "academic_counselor":
                from app.agents.academic_counselor_agent import AcademicCounselorAgent
                agent = AcademicCounselorAgent(self.db)
                result = asyncio.run(agent.process(student_id=state["student_id"]))
            elif agent_type == "job_market_analyst":
                from app.agents.job_market_analyst_agent import JobMarketAnalystAgent
                agent = JobMarketAnalystAgent(self.db)
                result = asyncio.run(agent.process(student_id=state["student_id"], **kwargs))
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            execution_time = time.time() - start_time
            
            # Store result
            state["agent_results"][agent_name] = {
                "status": result.status,
                "message": result.message,
                "data": result.data,
                "confidence": result.confidence,
                "execution_time": execution_time
            }
            
            state["executed_agents"].append(agent_name)
            
            if self.config.verbose_logging:
                print(f"[{agent_type.upper()}] Completed in {execution_time:.2f}s - Status: {result.status}")
            
            # Add to messages
            state["messages"].append(
                AIMessage(content=f"{agent_name}: {result.message}")
            )
            
        except Exception as e:
            if self.config.verbose_logging:
                print(f"[{agent_type.upper()}] Error: {str(e)}")
            
            state["agent_results"][agent_name] = {
                "status": "error",
                "message": f"Agent execution failed: {str(e)}",
                "data": {},
                "confidence": 0.0,
                "execution_time": 0
            }
            state["executed_agents"].append(agent_name)
        
        return state
    
    def _route_next_agent(self, state: AgentState) -> str:
        """Route to next agent or synthesizer"""
        agents_sequence = [
            "Skill Analyzer",
            "Interest Evaluator",
            "Career Recommender",
            "Academic Counselor",
            "Job Market Analyst"
        ]
        
        # Find next agent
        last_agent = state["executed_agents"][-1] if state["executed_agents"] else None
        
        if last_agent:
            try:
                current_index = agents_sequence.index(last_agent)
                if current_index < len(agents_sequence) - 1:
                    next_agent_name = agents_sequence[current_index + 1]
                    agent_type = next_agent_name.lower().replace(" ", "_")
                    if agent_type == "job_market_analyst":
                        return "job_market_analyst"
                    return next_agent_name.lower()
            except ValueError:
                pass
        
        # All agents executed, go to synthesizer
        return "synthesizer"
    
    def _synthesize_results(self, state: AgentState) -> AgentState:
        """Synthesize results from all agents"""
        if self.config.verbose_logging:
            print("[SYNTHESIZER] Synthesizing results from all agents")
        
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage as HumanMsg
        
        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
            
            # Prepare results summary
            results_summary = "\n\n".join([
                f"{agent}: {result['message']}\nData: {result['data']}"
                for agent, result in state["agent_results"].items()
            ])
            
            prompt = f"""
            Synthesize the following multi-agent analysis results:
            
            {results_summary}
            
            Provide a comprehensive, actionable summary that combines all insights.
            """
            
            messages = [
                SystemMessage(content="You are an expert at synthesizing AI agent outputs."),
                HumanMsg(content=prompt)
            ]
            
            response = llm.invoke(messages)
            state["combined_analysis"] = response.content
            
            state["messages"].append(
                AIMessage(content=f"Synthesizer: Analysis complete")
            )
            
        except Exception as e:
            if self.config.verbose_logging:
                print(f"[SYNTHESIZER] Error: {str(e)}")
            state["combined_analysis"] = f"Synthesis failed: {str(e)}"
        
        return state
    
    def _format_final_response(self, state: AgentState) -> AgentState:
        """Format final response"""
        if self.config.verbose_logging:
            print("[FORMATTER] Formatting final response")
        
        final_response = {
            "conversation_id": state.get("conversation_id"),
            "student_id": state["student_id"],
            "timestamp": state.get("timestamp", datetime.now()).isoformat(),
            "agents_executed": state["executed_agents"],
            "individual_results": state["agent_results"],
            "combined_analysis": state["combined_analysis"],
            "execution_complete": True
        }
        
        state["final_response"] = final_response
        
        return state
    
    async def execute_workflow(
        self,
        student_id: int,
        conversation_id: str,
        context: Optional[dict] = None
    ) -> dict:
        """Execute the complete workflow"""
        from uuid import uuid4
        
        initial_state: AgentState = {
            "student_id": student_id,
            "conversation_id": conversation_id or str(uuid4()),
            "messages": [],
            "agents_to_execute": [],
            "executed_agents": [],
            "agent_results": {},
            "combined_analysis": "",
            "student_data": {},
            "context": context or {},
            "timestamp": datetime.now(),
            "next_agent": None,
            "should_continue": True,
            "final_response": None,
        }
        
        if self.config.verbose_logging:
            print(f"\n{'='*60}")
            print(f"Starting Multi-Agent Workflow for Student {student_id}")
            print(f"Conversation ID: {initial_state['conversation_id']}")
            print(f"{'='*60}\n")
        
        try:
            # Execute the graph
            final_state = self.graph.invoke(initial_state)
            
            if self.config.verbose_logging:
                print(f"\n{'='*60}")
                print("Workflow Execution Complete")
                print(f"Agents Executed: {', '.join(final_state['executed_agents'])}")
                print(f"{'='*60}\n")
            
            return final_state["final_response"]
            
        except Exception as e:
            if self.config.verbose_logging:
                print(f"Workflow Error: {str(e)}")
            return {
                "conversation_id": initial_state["conversation_id"],
                "student_id": student_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "execution_complete": False
            }
    
    def get_graph_visualization(self) -> str:
        """Get ASCII representation of the workflow graph"""
        if not self.graph:
            return "Graph not initialized"
        
        # Get the underlying graph structure
        return str(self.graph)
