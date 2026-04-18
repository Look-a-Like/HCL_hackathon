from typing import TypedDict, Optional


class TravelState(TypedDict):
    user_input: str
    conversation_history: list[str]

    budget: Optional[float]
    duration_days: Optional[int]
    destination: Optional[str]
    interests: Optional[list[str]]
    travel_dates: Optional[str]
    missing_fields: list[str]

    destination_info: Optional[dict]
    budget_breakdown: Optional[dict]
    itinerary: Optional[list[dict]]
    booking_options: Optional[dict]
    local_experiences: Optional[list[dict]]

    final_plan: Optional[dict]

    errors: list[str]
    retries: dict[str, int]

    metrics: dict


def create_initial_state(user_input: str) -> TravelState:
    return {
        "user_input": user_input,
        "conversation_history": [],
        "budget": None,
        "duration_days": None,
        "destination": None,
        "interests": None,
        "travel_dates": None,
        "missing_fields": [],
        "destination_info": None,
        "budget_breakdown": None,
        "itinerary": None,
        "booking_options": None,
        "local_experiences": None,
        "final_plan": None,
        "errors": [],
        "retries": {},
        "metrics": {"latency": {}, "cost": {}},
    }