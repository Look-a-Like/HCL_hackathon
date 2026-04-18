import json
from typing import Optional
from backend.graph.state import TravelState
from backend.tools.travel_data import get_destination_by_name


def itinerary_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    duration_days = state.get("duration_days")
    budget_breakdown = state.get("budget_breakdown", {})
    interests = state.get("interests", [])
    destination_info = state.get("destination_info", {})
    
    if not destination:
        state["errors"].append("No destination for itinerary")
        return state
    
    days = duration_days if duration_days else 3
    dest_data = get_destination_by_name(destination)
    attractions = dest_data.get("attractions", []) if dest_data else []
    
    per_day_food = budget_breakdown.get("per_day_breakdown", {}).get("food", 500)
    activities_budget = budget_breakdown.get("activities", 1000)
    activities_per_day = activities_budget // days if days > 0 else 0
    
    itinerary = _generate_itinerary(
        destination=destination,
        days=days,
        attractions=attractions,
        interests=interests,
        per_day_food=per_day_food,
        activities_per_day=activities_per_day
    )
    
    state["itinerary"] = itinerary
    return state


def _generate_itinerary(
    destination: str,
    days: int,
    attractions: list[dict],
    interests: list[str],
    per_day_food: int,
    activities_per_day: int
) -> list[dict]:
    itinerary = []
    
    if not attractions:
        attractions = [
            {"name": f"Explore {destination}", "type": "general", "description": "Discover the local area"}
        ]
    
    attractions_by_type = {}
    for attr in attractions:
        attr_type = attr.get("type", "general")
        if attr_type not in attractions_by_type:
            attractions_by_type[attr_type] = []
        attractions_by_type[attr_type].append(attr)
    
    day_分配 = ["morning", "afternoon", "evening"]
    
    for day_num in range(1, days + 1):
        day_activities = []
        day_cost = 0
        
        type_keys = list(attractions_by_type.keys())
        for i, time_slot in enumerate(day_分配):
            if i < len(type_keys) and type_keys[i] in attractions_by_type:
                attr_list = attractions_by_type[type_keys[i]]
                if attr_list:
                    attr = attr_list[i % len(attr_list)]
                    day_activities.append({
                        "time": time_slot,
                        "activity": attr.get("name"),
                        "description": attr.get("description"),
                        "type": attr.get("type")
                    })
                    day_cost += activities_per_day // 3 if activities_per_day > 0 else 0
        
        if not day_activities:
            day_activities.append({
                "time": "morning",
                "activity": f"Free time in {destination}",
                "description": "Relax and explore at your own pace",
                "type": "leisure"
            })
        
        meals = _get_meals_for_destination(destination, day_num)
        day_cost += sum(m.get("cost", 0) for m in meals)
        
        itinerary.append({
            "day_number": day_num,
            "title": f"Day {day_num} in {destination}",
            "activities": day_activities,
            "meals": meals,
            "estimated_cost": day_cost,
            "travel_tips": _get_travel_tip(destination, day_num)
        })
    
    return itinerary


def _get_meals_for_destination(destination: str, day_num: int) -> list[dict]:
    dest_lower = destination.lower()
    
    breakfast_options = {
        "goa": ["Prawn fry with bread", "Idli with coconut chutney"],
        "kerala": ["Appam with stew", "Puttu and kadala"],
        "manali": ["Paratha with aloo", "Maggi and chai"],
        "jaipur": ["Pyaaz kachori", "Lassi"],
        "default": ["Traditional breakfast", "Local specialties"]
    }
    
    lunch_options = {
        "goa": ["Fish curry with rice", "Seafood platter"],
        "kerala": ["Thali with fish fry", "Sadhya"],
        "manali": ["Rajma chawal", "Momos"],
        "jaipur": ["Daal baati churma", "Laal maas"],
        "default": ["Local thali", "Regional cuisine"]
    }
    
    dinner_options = {
        "goa": ["Beachside seafood dinner", "Feni and snacks"],
        "kerala": ["Kappa and fish curry", "Banana fritters"],
        "manali": ["Bonfire dinner", "Garhwali cuisine"],
        "jaipur": ["Ghewar", "Dal baati"],
        "default": ["Local dinner", "Night market visit"]
    }
    
    breakfast = breakfast_options.get(dest_lower, breakfast_options["default"])[0]
    lunch = lunch_options.get(dest_lower, lunch_options["default"])[0]
    dinner = dinner_options.get(dest_lower, dinner_options["default"])[0]
    
    return [
        {"meal": "breakfast", "description": breakfast, "cost": 150},
        {"meal": "lunch", "description": lunch, "cost": 300},
        {"meal": "dinner", "description": dinner, "cost": 400}
    ]


def _get_travel_tip(destination: str, day_num: int) -> str:
    tips = {
        "goa": "Rent a scooter for easy beach-to-beach travel. Start early to beat the heat.",
        "manali": "Carry warm clothes even in summer. Book Rohtang pass permits in advance.",
        "jaipur": "Visit Amber Fort early morning to avoid crowds. Don't miss the light show.",
        "kerala": "Start early for houseboat departure. Carry rain gear if visiting monsoons.",
        "rishikesh": "Book rafting in advance during peak season. Attend evening Ganga aarti.",
        "shimla": "Walk to Mall Road from your hotel. Visit Ridge in the evening.",
        "varanasi": "Hire a guide for ghats. Boat ride at sunrise is magical.",
        "darjeeling": "Book Toy Train tickets weeks in advance. Morning views are clearest.",
        "default": "Start early each day to make the most of your time. Stay hydrated!"
    }
    
    return tips.get(destination.lower(), tips["default"])