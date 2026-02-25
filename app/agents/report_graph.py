from langgraph.graph import StateGraph, END
from .state import CareerState
from .nodes import (
    academic_analyzer,
    skill_matcher,
    career_generator,
    college_recommender,
    salary_predictor,
    roadmap_planner,
    final_builder
)


def build_graph():
    builder = StateGraph(CareerState)

    # Add nodes
    builder.add_node("academic_analyzer", academic_analyzer)
    builder.add_node("skill_matcher", skill_matcher)
    builder.add_node("career_generator", career_generator)
    builder.add_node("college_recommender", college_recommender)
    builder.add_node("salary_predictor", salary_predictor)
    builder.add_node("roadmap_planner", roadmap_planner)
    builder.add_node("final_builder", final_builder)

    # Set entry point
    builder.set_entry_point("academic_analyzer")

    # Add edges to connect nodes
    builder.add_edge("academic_analyzer", "skill_matcher")
    builder.add_edge("skill_matcher", "career_generator")
    builder.add_edge("career_generator", "college_recommender")
    builder.add_edge("college_recommender", "salary_predictor")
    builder.add_edge("salary_predictor", "roadmap_planner")
    builder.add_edge("roadmap_planner", "final_builder")
    builder.add_edge("final_builder", END)

    # Compile graph
    graph = builder.compile()
    return graph