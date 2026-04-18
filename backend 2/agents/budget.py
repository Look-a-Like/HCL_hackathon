import json
from backend.graph.state import TravelState
from backend.prompts.budget import BUDGET_SYSTEM_PROMPT, BUDGET_USER_PROMPT
from backend.tools.llm import get_llm_client, parse_json_response


async def budget_agent(state: TravelState) -> TravelState:
    budget = state.get("budget")
    destination = state.get("destination")
    duration_days = state.get("duration_days") or 3
    interests = state.get("interests", [])
    
    if not budget:
        budget = 50000  # default ₹50,000 when not specified
        state["budget"] = budget
    
    client = get_llm_client()
    prompt = BUDGET_USER_PROMPT.format(
        budget=budget,
        destination=destination or "Unknown",
        days=duration_days,
        interests=", ".join(interests) if interests else "General travel"
    )
    
    response = await client.achat(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=BUDGET_SYSTEM_PROMPT,
        max_tokens=800,
        temperature=0.3
    )
    
    try:
        extracted = parse_json_response(response)
        
        if extracted:
            state["budget_breakdown"] = {
                "total": extracted.get("total", budget),
                "duration_days": duration_days,
                "transport": extracted.get("transport", 0),
                "hotel": extracted.get("hotel", 0),
                "food": extracted.get("food", 0),
                "activities": extracted.get("activities", 0),
                "buffer": extracted.get("buffer", 0),
                "per_day_breakdown": {
                    "hotel": extracted.get("hotel", 0),
                    "food": extracted.get("food", 0),
                },
                "currency": extracted.get("currency", "INR"),
                "tips": extracted.get("tips", [])
            }
        else:
            raise ValueError("Failed to parse JSON response from LLM")
            
    except Exception as e:
        state["errors"].append(f"Budget parsing error: {str(e)}")
        # Simple fallback calculation
        total_budget = budget
        transport = round(total_budget * 0.25)
        hotel = round(total_budget * 0.35 / max(1, duration_days))
        food = round(total_budget * 0.25 / max(1, duration_days))
        activities = round(total_budget * 0.10)
        buffer = round(total_budget * 0.05)
        
        state["budget_breakdown"] = {
            "total": total_budget,
            "duration_days": duration_days,
            "transport": transport,
            "hotel": hotel,
            "food": food,
            "activities": activities,
            "buffer": buffer,
            "per_day_breakdown": {"hotel": hotel, "food": food},
            "currency": "INR",
            "tips": ["Fallback budget calculated due to parsing error."]
        }
    
    return state
