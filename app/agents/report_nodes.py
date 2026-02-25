import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def academic_analyzer(state):
    prompt = f"""
    Analyze marks: {state['student_input']['marks']}
    Give strengths and recommended stream.
    Return JSON.
    """
    response = llm([HumanMessage(content=prompt)])
    state["academic_analysis"] = json.loads(response.content)
    return state


def skill_matcher(state):
    prompt = f"""
    Skills: {state['student_input']['skills']}
    Interests: {state['student_input']['interests']}
    Match career domains.
    Return JSON.
    """
    response = llm([HumanMessage(content=prompt)])
    state["skill_analysis"] = json.loads(response.content)
    return state


def career_generator(state):
    prompt = f"""
    Based on academic: {state['academic_analysis']}
    and skills: {state['skill_analysis']}

    Generate 5 detailed career suggestions.
    Return JSON array.
    """
    response = llm([HumanMessage(content=prompt)])
    state["career_suggestions"] = json.loads(response.content)
    return state


def college_recommender(state):
    prompt = f"""
    Suggest Indian colleges for careers:
    {state['career_suggestions']}

    Return JSON array.
    """
    response = llm([HumanMessage(content=prompt)])
    state["college_suggestions"] = json.loads(response.content)
    return state


def salary_predictor(state):
    prompt = f"""
    Predict 10-year salary growth for:
    {state['career_suggestions'][0]['name']}

    Return JSON array.
    """
    response = llm([HumanMessage(content=prompt)])
    state["salary_prediction"] = json.loads(response.content)
    return state


def roadmap_planner(state):
    prompt = f"""
    Create 4-step roadmap for:
    {state['career_suggestions'][0]['name']}

    Return JSON array.
    """
    response = llm([HumanMessage(content=prompt)])
    state["roadmap"] = json.loads(response.content)
    return state


def final_builder(state):
    state["final_report"] = {
        "studentName": state["student_input"]["name"],
        "testDate": state["student_input"]["date"],
        "topCareers": state["career_suggestions"],
        "collegeSuggestions": state["college_suggestions"],
        "salaryPrediction": state["salary_prediction"],
        "roadmap": state["roadmap"],
        "backupOptions": []
    }
    return state