import json
from backend.graph.state import TravelState
from backend.tools.travel_data import get_destination_by_name, get_all_destination_names
from backend.prompts.destination import DESTINATION_SYSTEM_PROMPT, DESTINATION_USER_PROMPT


def get_anthropic_client():
    try:
        from anthropic import Anthropic
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            return Anthropic(api_key=api_key)
    except ImportError:
        pass
    return None


def destination_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    interests = state.get("interests", [])
    
    if not destination:
        state["errors"].append("No destination specified")
        return state
    
    dest_data = get_destination_by_name(destination)
    
    if dest_data:
        state["destination_info"] = {
            "name": dest_data.get("name"),
            "type": dest_data.get("type"),
            "state": dest_data.get("state"),
            "description": dest_data.get("description"),
            "best_season": dest_data.get("best_season"),
            "attractions": dest_data.get("attractions", []),
            "keywords": dest_data.get("keywords", []),
            "avg_daily_cost": dest_data.get("avg_daily_cost"),
            "matched_interests": _match_interests(dest_data, interests)
        }
    else:
        state["destination_info"] = {
            "name": destination,
            "error": "Destination not found in database",
            "available_destinations": get_all_destination_names()
        }
    
    return state


def _match_interests(dest_data: dict, user_interests: list[str]) -> list[str]:
    if not user_interests:
        return []
    
    keywords = [k.lower() for k in dest_data.get("keywords", [])]
    matched = []
    
    interest_keywords = {
        "beach": ["beach", "sea", "coast"],
        "mountains": ["mountain", "hill", "peak", "valley"],
        "adventure": ["adventure", "trek", "raft", "sports"],
        "food": ["food", "cuisine", "restaurant", "seafood"],
        "culture": ["heritage", "temple", "church", "museum", "palace"],
        "nature": ["nature", "wildlife", "park", "forest"],
        "party": ["party", "nightlife", "club"]
    }
    
    for interest in user_interests:
        if interest in interest_keywords:
            for kw in interest_keywords[interest]:
                if kw in keywords:
                    matched.append(interest)
                    break
    
    return list(set(matched))