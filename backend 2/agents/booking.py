from backend.graph.state import TravelState
from backend.tools.travel_data import get_hotels_for_destination, get_flights_to_destination
from backend.tools.ranking import rank_hotels_by_budget, rank_flights_by_budget


async def booking_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    budget_breakdown = state.get("budget_breakdown") or {}

    if not destination:
        state["errors"].append("No destination specified for booking")
        state["booking_options"] = {"hotels": [], "flights": []}
        return state

    hotels = get_hotels_for_destination(destination)
    flights = get_flights_to_destination(destination)

    total_budget = state.get("budget") or 5000
    hotel_budget = budget_breakdown.get("hotel") or (total_budget * 0.4)
    transport_budget = budget_breakdown.get("transport") or (total_budget * 0.25)

    ranked_hotels = rank_hotels_by_budget(hotels, hotel_budget, max_results=3, destination=destination)
    ranked_flights = rank_flights_by_budget(flights, transport_budget, max_results=3)

    state["booking_options"] = {
        "hotels": ranked_hotels,
        "flights": ranked_flights,
        "booking_tips": _booking_tips(budget_breakdown),
    }

    return state


def _booking_tips(budget_breakdown: dict) -> list[str]:
    tips = []
    hotel_budget = budget_breakdown.get("hotel", 0)
    transport_budget = budget_breakdown.get("transport", 0)

    if hotel_budget < 1000:
        tips += ["Consider budget hotels or hostels for great value", "Book with free cancellation to stay flexible"]
    elif hotel_budget < 3000:
        tips += ["Mid-range hotels often have good deals on booking sites", "Look for breakfast-included packages"]
    else:
        tips += ["Luxury hotels offer premium amenities", "Check package deals for multi-night stays"]

    if transport_budget < 3000:
        tips += ["Train travel is cheaper and more scenic than flights", "Book AC sleeper class for long routes"]
    else:
        tips += ["Direct flights save time — check for early deals", "Book 4–6 weeks ahead for best fares"]

    return tips
