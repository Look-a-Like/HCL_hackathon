import json
from backend.graph.state import TravelState
from backend.tools.travel_data import get_hotels_for_destination, get_flights_to_destination
from backend.tools.ranking import rank_hotels_by_budget, rank_flights_by_budget
from backend.tools.llm import get_llm_client, parse_json_response


async def booking_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    budget_breakdown = state.get("budget_breakdown", {})
    
    if not destination:
        state["errors"].append("No destination specified for booking")
        state["booking_options"] = {"hotels": [], "flights": []}
        return state
    
    # We use curated mock data for the actual listings as live APIs are restricted
    hotels = get_hotels_for_destination(destination)
    flights = get_flights_to_destination(destination)
    
    hotel_budget = budget_breakdown.get("hotel", state.get("budget", 5000) * 0.4)
    transport_budget = budget_breakdown.get("transport", state.get("budget", 5000) * 0.25)
    
    ranked_hotels = rank_hotels_by_budget(hotels, hotel_budget, max_results=3)
    ranked_flights = rank_flights_by_budget(flights, transport_budget, max_results=3)
    
    # Use LLM to generate dynamic, personalized booking tips
    client = get_llm_client()
    tip_prompt = f"Provide 3-5 specific, practical booking tips for a trip to {destination} with a total budget of {state.get('budget')} INR. Focus on hotel and transport savings."
    
    response = await client.achat(
        messages=[{"role": "user", "content": tip_prompt}],
        system_prompt="You are a travel booking expert. Provide concise, numbered or bulleted tips for the given destination and budget. Return as a JSON list of strings.",
        temperature=0.3
    )
    
    try:
        tips = parse_json_response(response)
        if not isinstance(tips, list):
             # Try to extract bullet points from text if not JSON
             tips = [line.strip("- 123456789. ") for line in response.split("\n") if line.strip() and (line.strip().startswith("-") or line.strip()[0].isdigit())]
             if not tips:
                 tips = [response.strip()]
    except Exception:
        tips = [
            "Book at least 3-4 weeks in advance for better hotel rates.",
            "Consider public transport or shared cabs to save on local travel.",
            "Look for accommodations slightly outside the city center for better value."
        ]
    
    state["booking_options"] = {
        "hotels": ranked_hotels,
        "flights": ranked_flights,
        "booking_tips": tips[:5]
    }
    
    return state
