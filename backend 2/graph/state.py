from typing import TypedDict, Optional, Annotated, Any
import operator


def last_value(old: Any, new: Any) -> Any:
    """Reducer that picks the new value, but keeps old if new is None."""
    return new if new is not None else old


def merge_dicts(old: dict, new: dict) -> dict:
    """Reducer that merges two dictionaries."""
    return {**(old or {}), **(new or {})}


def merge_lists(old: list, new: list) -> list:
    """Reducer that merges two lists, attempting to avoid duplicates if they are identical."""
    if old is new:
        return old
    
    # If nodes return the full list, we only want to add what's truly new.
    # But detecting "truly new" is hard without knowing the previous state.
    # For now, let's just return the new one if it's a super-set, 
    # or combine them if they are different.
    if not old: return new
    if not new: return old
    
    # Simple heuristic: if new is longer and starts with old, it's a full state return
    if len(new) >= len(old) and new[:len(old)] == old:
        return new
    
    return old + new


class TravelState(TypedDict):
    user_input: Annotated[str, last_value]
    conversation_history: Annotated[list[str], merge_lists]

    budget: Annotated[Optional[float], last_value]
    duration_days: Annotated[Optional[int], last_value]
    destination: Annotated[Optional[str], last_value]
    interests: Annotated[Optional[list[str]], last_value]
    travel_dates: Annotated[Optional[str], last_value]
    missing_fields: Annotated[list[str], merge_lists]

    destination_info: Annotated[Optional[dict], last_value]
    budget_breakdown: Annotated[Optional[dict], last_value]
    itinerary: Annotated[Optional[list[dict]], last_value]
    booking_options: Annotated[Optional[dict], last_value]
    local_experiences: Annotated[Optional[list[dict]], last_value]

    final_plan: Annotated[Optional[dict], last_value]

    errors: Annotated[list[str], merge_lists]
    retries: Annotated[dict[str, int], merge_dicts]

    metrics: Annotated[dict, merge_dicts]


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
