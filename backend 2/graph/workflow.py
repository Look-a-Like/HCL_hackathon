from langgraph.graph import StateGraph, END
from backend.graph.state import TravelState, create_initial_state
from backend.agents import (
    planner_agent,
    destination_agent,
    budget_agent,
    itinerary_agent,
    booking_agent,
    local_experience_agent,
)
from backend.graph.router import tracked, with_retry


def create_workflow() -> StateGraph:
    workflow = StateGraph(TravelState)
    
    workflow.add_node("planner", tracked(with_retry(planner_agent, "planner"), "planner"))
    workflow.add_node("destination", tracked(with_retry(destination_agent, "destination"), "destination"))
    workflow.add_node("budget", tracked(with_retry(budget_agent, "budget"), "budget"))
    workflow.add_node("itinerary", tracked(with_retry(itinerary_agent, "itinerary"), "itinerary"))
    workflow.add_node("booking", tracked(with_retry(booking_agent, "booking"), "booking"))
    workflow.add_node("local_experience", tracked(with_retry(local_experience_agent, "local_experience"), "local_experience"))
    
    workflow.set_entry_point("planner")
    
    workflow.add_edge("planner", "destination")
    workflow.add_edge("planner", "budget")
    
    workflow.add_edge("destination", "itinerary")
    workflow.add_edge("budget", "itinerary")
    
    workflow.add_edge("itinerary", "booking")
    workflow.add_edge("itinerary", "local_experience")
    
    workflow.add_edge("booking", END)
    workflow.add_edge("local_experience", END)
    
    return workflow


def compile_workflow():
    graph = create_workflow()
    return graph.compile()


langgraph_app = compile_workflow()


async def run_travel_planning(user_input: str):
    initial_state = create_initial_state(user_input)
    final_state = await langgraph_app.ainvoke(initial_state)
    return final_state