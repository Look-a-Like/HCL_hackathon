from backend.graph.state import TravelState
from backend.tools.travel_data import get_hotels_for_destination, get_flights_to_destination
from backend.tools.ranking import rank_hotels_by_budget, rank_flights_by_budget, filter_by_tier


def booking_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    budget_breakdown = state.get("budget_breakdown", {})
    
    if not destination:
        state["errors"].append("No destination for booking")
        state["booking_options"] = {"hotels": [], "flights": []}
        return state
    
    hotels = get_hotels_for_destination(destination)
    flights = get_flights_to_destination(destination)
    
    hotel_budget = budget_breakdown.get("hotel", state.get("budget", 5000) * 0.4)
    transport_budget = budget_breakdown.get("transport", state.get("budget", 5000) * 0.25)
    
    ranked_hotels = rank_hotels_by_budget(hotels, hotel_budget, max_results=3)
    ranked_flights = rank_flights_by_budget(flights, transport_budget, max_results=3)
    
    state["booking_options"] = {
        "hotels": ranked_hotels,
        "flights": ranked_flights,
        "booking_tips": _generate_booking_tips(destination, budget_breakdown)
    }
    
    return state


def _generate_booking_tips(destination: str, budget_breakdown: dict) -> list[str]:
    tips = []
    
    hotel_budget = budget_breakdown.get("hotel", 0)
    if hotel_budget < 1000:
        tips.append("Consider budget hotels or hostels - many offer great value")
        tips.append("Book with free cancellation to be flexible")
    elif hotel_budget < 3000:
        tips.append("Mid-range hotels often have good deals on booking sites")
        tips.append("Look for breakfast included packages")
    else:
        tips.append("Luxury hotels offer premium amenities and experiences")
        tips.append("Check for package deals combining multiple nights")
    
    transport_budget = budget_breakdown.get("transport", 0)
    if transport_budget < 3000:
        tips.append("Train travel is often cheaper and more scenic than flights")
        tips.append("Book AC or sleeper class for long distances")
    else:
        tips.append("Direct flights save time - check for deals")
        tips.append("Consider business class for longer flights")
    
    return tips