import json
from backend.graph.state import TravelState
from backend.tools.travel_data import get_destination_by_name


def budget_agent(state: TravelState) -> TravelState:
    budget = state.get("budget")
    destination = state.get("destination")
    duration_days = state.get("duration_days")
    interests = state.get("interests", [])
    
    if not budget:
        state["errors"].append("No budget specified")
        return state
    
    dest_data = get_destination_by_name(destination) if destination else None
    avg_daily_cost = dest_data.get("avg_daily_cost") if dest_data else 2500
    
    days = duration_days if duration_days else 3
    
    total_budget = budget
    
    if avg_daily_cost * days > total_budget:
        transport_ratio = 0.25
        hotel_ratio = 0.35
        food_ratio = 0.25
        activities_ratio = 0.10
        buffer_ratio = 0.05
    else:
        transport_ratio = 0.20
        hotel_ratio = 0.30
        food_ratio = 0.25
        activities_ratio = 0.15
        buffer_ratio = 0.10
    
    if "adventure" in interests or "party" in interests:
        activities_ratio += 0.05
        food_ratio -= 0.05
    
    transport = round(total_budget * transport_ratio)
    hotel = round(total_budget * hotel_ratio / days) if days > 0 else 0
    food = round(total_budget * food_ratio / days) if days > 0 else 0
    activities = round(total_budget * activities_ratio)
    buffer = round(total_budget * buffer_ratio)
    
    state["budget_breakdown"] = {
        "total": total_budget,
        "duration_days": days,
        "transport": transport,
        "hotel": hotel,
        "food": food,
        "activities": activities,
        "buffer": buffer,
        "per_day_breakdown": {
            "hotel": hotel,
            "food": food,
        },
        "currency": "INR",
        "tips": _generate_budget_tips(budget, destination, interests)
    }
    
    return state


def _generate_budget_tips(budget: float, destination: str, interests: list[str]) -> list[str]:
    tips = []
    per_day = budget / max(1, 3)
    
    if per_day < 1000:
        tips.append("Travel during off-season for better deals")
        tips.append("Use public transport instead of taxis")
        tips.append("Stay in budget hotels or hostels")
        tips.append("Eat at local restaurants instead of tourist spots")
    elif per_day < 3000:
        tips.append("Book accommodations in advance")
        tips.append("Look for combo packages for attractions")
        tips.append("Consider day trips to save on accommodation")
    else:
        tips.append("Consider premium experiences and guided tours")
        tips.append("Book directly with hotels for upgrades")
    
    if destination:
        dest_lower = destination.lower()
        if "goa" in dest_lower:
            tips.append("Visit in monsoon for cheap prices but check weather")
        elif "manali" in dest_lower or "shimla" in dest_lower:
            tips.append("Book ski packages if visiting in winter")
        elif "kerala" in dest_lower:
            tips.append("Try houseboat stays - they offer good value")
    
    return tips