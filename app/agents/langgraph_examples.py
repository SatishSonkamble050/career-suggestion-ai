"""LangGraph Workflow Examples and Usage Patterns"""

import asyncio
from typing import Optional
from sqlalchemy.orm import Session


# ============ Example 1: Basic LangGraph Workflow ============

async def example_langgraph_basic(db: Session, student_id: int):
    """Example: Execute basic multi-agent workflow with LangGraph"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    result = await orchestrator.execute_with_langgraph(
        student_id=student_id,
        enable_logging=True
    )
    
    print("LangGraph Workflow Results:")
    print(f"Conversation ID: {result['conversation_id']}")
    print(f"Agents Executed: {result['agents_executed']}")
    print(f"Combined Analysis: {result['combined_analysis'][:200]}...")


# ============ Example 2: Custom Agent Sequence with LangGraph ============

async def example_langgraph_custom_sequence(db: Session, student_id: int):
    """Example: Execute agents in custom sequence"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    # Define custom sequence
    agent_sequence = [
        "skill_analyzer",
        "interest_evaluator",
        "career_recommender"
    ]
    
    result = await orchestrator.execute_custom_workflow(
        student_id=student_id,
        agent_sequence=agent_sequence,
        context={"target_career": "Data Scientist"}
    )
    
    print("Custom Sequence Results:")
    print(f"Status: {result.status}")
    print(f"Agents: {result.agents_executed}")
    print(f"Summary: {result.summary}")


# ============ Example 3: Parallel Agent Execution ============

async def example_langgraph_parallel(db: Session, student_id: int):
    """Example: Execute multiple agents in parallel"""
    from app.agents.agent_orchestrator import AgentOrchestrator, AgentType
    
    orchestrator = AgentOrchestrator(db)
    
    # Parallel execution - these agents operate independently
    parallel_agents = [
        AgentType.SKILL_ANALYZER,
        AgentType.INTEREST_EVALUATOR,
        AgentType.JOB_MARKET_ANALYST
    ]
    
    result = await orchestrator.execute_parallel_agents(
        student_id=student_id,
        agent_types=parallel_agents
    )
    
    print("Parallel Execution Results:")
    print(f"Status: {result.status}")
    print(f"Agents Executed: {result.agents_executed}")
    print(f"Execution Summary: {result.summary}")


# ============ Example 4: Graph Visualization ============

def example_langgraph_visualization(db: Session):
    """Example: Get workflow graph visualization"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    visualization = orchestrator.get_workflow_graph_visualization()
    
    print("LangGraph Workflow Visualization:")
    print(visualization)


# ============ Example 5: Execution Statistics ============

async def example_langgraph_stats(db: Session, student_id: int):
    """Example: Get workflow execution statistics"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    # Execute workflow
    result = await orchestrator.execute_with_langgraph(
        student_id=student_id,
        enable_logging=False
    )
    
    conversation_id = result['conversation_id']
    
    # Get stats
    stats = orchestrator.get_workflow_execution_stats(conversation_id)
    
    print("Workflow Execution Statistics:")
    print(f"Conversation ID: {stats['conversation_id']}")
    print(f"Student ID: {stats['student_id']}")
    print(f"Agents Executed: {stats['agents_executed']}")
    print(f"Execution Method: {stats['execution_method']}")
    if 'agent_names' in stats:
        print(f"Agent Names: {stats['agent_names']}")


# ============ Example 6: Comprehensive State Management ============

async def example_langgraph_state_management(db: Session, student_id: int):
    """Example: Understanding LangGraph state flow"""
    from app.agents.langgraph_workflow import MultiAgentWorkflow, WorkflowConfig, AgentState
    from uuid import uuid4
    
    # Create workflow with custom config
    config = WorkflowConfig(
        max_retries=3,
        agent_timeout=30,
        enable_parallel_execution=True,
        verbose_logging=True,
        collect_all_results=True
    )
    
    workflow = MultiAgentWorkflow(db, config)
    
    # Execute workflow
    result = await workflow.execute_workflow(
        student_id=student_id,
        conversation_id=str(uuid4()),
        context={"target_career": "Software Engineer"}
    )
    
    print("LangGraph State Management Example:")
    print(f"Final Response Keys: {result.keys()}")
    print(f"Individual Results: {list(result['individual_results'].keys())}")


# ============ Example 7: Error Handling in Workflows ============

async def example_langgraph_error_handling(db: Session, student_id: int = 99999):
    """Example: Error handling in LangGraph workflows"""
    from app.agents.agent_orchestrator import AgentOrchestrator
    
    orchestrator = AgentOrchestrator(db)
    
    try:
        result = await orchestrator.execute_with_langgraph(
            student_id=student_id,  # Non-existent student
            enable_logging=False
        )
        
        if "error" in result:
            print(f"Workflow Error: {result['error']}")
        else:
            print("Workflow completed despite potential issues")
            
    except Exception as e:
        print(f"Exception caught: {str(e)}")


# ============ Example 8: HTTP Client Usage ============

"""
Using LangGraph endpoints via HTTP:

1. Basic LangGraph Execution:
   POST /api/agents/langgraph/execute/1
   Query params: enable_logging=true

2. Custom Sequence:
   POST /api/agents/langgraph/custom-sequence/1
   Body: {
     "agent_sequence": ["skill_analyzer", "career_recommender"],
     "context": {"target_career": "Data Scientist"}
   }

3. Parallel Execution:
   POST /api/agents/langgraph/parallel/1
   Body: {
     "agent_types": ["skill_analyzer", "interest_evaluator"],
     "context": {}
   }

4. Get Visualization:
   GET /api/agents/langgraph/graph-visualization

5. Get Statistics:
   GET /api/agents/langgraph/stats/{conversation_id}
"""

async def example_http_client():
    """Example: Using LangGraph endpoints via HTTP client"""
    import httpx
    
    async with httpx.AsyncClient() as client:
        # Execute with LangGraph
        response = await client.post(
            "http://localhost:8000/api/agents/langgraph/execute/1",
            params={"enable_logging": "true"}
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Result: {result}")
        
        # Get visualization
        viz_response = await client.get(
            "http://localhost:8000/api/agents/langgraph/graph-visualization"
        )
        print(f"Graph Visualization: {viz_response.json()}")


# ============ Example 9: Advanced Workflow Customization ============

async def example_advanced_workflow(db: Session, student_id: int):
    """Example: Advanced workflow with custom configurations"""
    from app.agents.langgraph_workflow import MultiAgentWorkflow, WorkflowConfig
    
    # Custom configuration
    config = WorkflowConfig(
        max_retries=5,
        agent_timeout=60,
        enable_parallel_execution=False,  # Sequential mode
        verbose_logging=True,
        collect_all_results=True
    )
    
    workflow = MultiAgentWorkflow(db, config)
    
    # Custom context for agents
    context = {
        "target_career": "Product Manager",
        "focus_area": "tech_startups",
        "timeline_months": 24,
        "budget_learning": 5000
    }
    
    result = await workflow.execute_workflow(
        student_id=student_id,
        context=context
    )
    
    print("Advanced Workflow Results:")
    print(f"Combined Analysis: {result['combined_analysis']}")
    print(f"Individual Results Count: {len(result['individual_results'])}")


# ============ Example 10: Workflow Chaining ============

async def example_workflow_chaining(db: Session, student_id: int):
    """Example: Chain multiple workflows for comprehensive analysis"""
    from app.agents.agent_orchestrator import AgentOrchestrator, AgentType
    
    orchestrator = AgentOrchestrator(db)
    
    print("Phase 1: Initial Analysis")
    phase1 = await orchestrator.execute_parallel_agents(
        student_id=student_id,
        agent_types=[AgentType.SKILL_ANALYZER, AgentType.INTEREST_EVALUATOR]
    )
    print(f"Phase 1 Results: {phase1.agents_executed}")
    
    print("\nPhase 2: Career Guidance")
    phase2 = await orchestrator.execute_with_langgraph(
        student_id=student_id,
        context={"phase": 2}
    )
    print(f"Phase 2 Completed: {phase2['execution_complete']}")


# ============ Main Execution ============

async def run_all_examples(db: Session, student_id: int = 1):
    """Run all LangGraph workflow examples"""
    
    print("=" * 80)
    print("LANGGRAPH MULTI-AGENT WORKFLOW EXAMPLES")
    print("=" * 80)
    
    try:
        print("\n1. Basic LangGraph Workflow")
        print("-" * 40)
        await example_langgraph_basic(db, student_id)
        
        print("\n2. Custom Agent Sequence")
        print("-" * 40)
        await example_langgraph_custom_sequence(db, student_id)
        
        print("\n3. Parallel Agent Execution")
        print("-" * 40)
        await example_langgraph_parallel(db, student_id)
        
        print("\n4. Graph Visualization")
        print("-" * 40)
        example_langgraph_visualization(db)
        
        print("\n5. Execution Statistics")
        print("-" * 40)
        await example_langgraph_stats(db, student_id)
        
        print("\n6. State Management")
        print("-" * 40)
        await example_langgraph_state_management(db, student_id)
        
        print("\n7. Error Handling")
        print("-" * 40)
        await example_langgraph_error_handling(db, student_id)
        
        print("\n8. Advanced Workflow")
        print("-" * 40)
        await example_advanced_workflow(db, student_id)
        
        print("\n9. Workflow Chaining")
        print("-" * 40)
        await example_workflow_chaining(db, student_id)
        
        print("\n" + "=" * 80)
        print("All LangGraph Examples Completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    To run these examples:
    
    1. From Python:
       python -m app.agents.langgraph_examples
    
    2. In your application:
       asyncio.run(run_all_examples(db))
    """
    print("This module contains LangGraph workflow examples.")
    print("Import and use the functions as needed.")
