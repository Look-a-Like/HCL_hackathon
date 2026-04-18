import json
from backend.graph.state import TravelState
from backend.prompts.itinerary import ITINERARY_SYSTEM_PROMPT, ITINERARY_USER_PROMPT
from backend.tools.llm import get_llm_client, parse_json_response


async def itinerary_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    duration_days = state.get("duration_days") or 3
    budget_breakdown = state.get("budget_breakdown", {})
    interests = state.get("interests", [])
    destination_info = state.get("destination_info", {})
    
    if not destination:
        state["errors"].append("No destination specified for itinerary")
        return state
    
    client = get_llm_client()
    prompt = ITINERARY_USER_PROMPT.format(
        destination=destination,
        days=duration_days,
        budget=json.dumps(budget_breakdown),
        interests=", ".join(interests) if interests else "General travel",
        destination_info=json.dumps(destination_info)
    )
    
    response = await client.achat(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=ITINERARY_SYSTEM_PROMPT,
        max_tokens=2000,
        temperature=0.3
    )
    
    try:
        extracted = parse_json_response(response)
        
        itinerary = []
        if isinstance(extracted, list):
            itinerary = extracted
        elif isinstance(extracted, dict):
            # Try common keys
            itinerary = extracted.get("itinerary", extracted.get("days", []))
            if not itinerary:
                # Last ditch: look for any list
                for val in extracted.values():
                    if isinstance(val, list):
                        itinerary = val
                        break
        
        if not itinerary:
            raise ValueError("Could not extract itinerary list from LLM response")
            
        state["itinerary"] = itinerary
        
    except Exception as e:
        state["errors"].append(f"Itinerary parsing error: {str(e)}")
        # Simple fallback itinerary
        state["itinerary"] = [
            {
                "day_number": i + 1,
                "title": f"Day {i+1} in {destination}",
                "activities": [
                    {"time": "Morning", "activity": "General Exploration", "description": "Explore the local area and landmarks."}
                ],
                "meals": [{"name": "Local Cuisine", "cost": 500}],
                "estimated_cost": 1000
            } for i in range(duration_days)
        ]
    
    return state
