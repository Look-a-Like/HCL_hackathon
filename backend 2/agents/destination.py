import json
from backend.graph.state import TravelState
from backend.tools.travel_data import get_destination_by_name, get_all_destination_names
from backend.prompts.destination import DESTINATION_SYSTEM_PROMPT, DESTINATION_USER_PROMPT
from backend.tools.llm import get_llm_client, parse_json_response
from backend.tools.search import aserper_search


async def destination_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    interests = state.get("interests", [])
    
    if not destination:
        state["errors"].append("No destination specified")
        return state
    
    # Attempt to get data from mock DB first
    dest_data = get_destination_by_name(destination)
    
    search_context = ""
    if not dest_data:
        # Perform dynamic search if not in database
        search_results = await aserper_search(f"top attractions and best time to visit {destination}")
        search_context = json.dumps(search_results)
    else:
        # Use existing data as context for the LLM
        search_context = json.dumps(dest_data)
    
    client = get_llm_client()
    prompt = DESTINATION_USER_PROMPT.format(
        destination=destination,
        interests=", ".join(interests) if interests else "General travel"
    )
    
    # Enrich the prompt with search context
    full_prompt = f"{prompt}\n\nSearch Context/Existing Data:\n{search_context}"
    
    # Let with_retry handle exceptions from achat
    response = await client.achat(
        messages=[{"role": "user", "content": full_prompt}],
        system_prompt=DESTINATION_SYSTEM_PROMPT,
        max_tokens=800,
        temperature=0.3
    )
    extracted = parse_json_response(response)
    
    if extracted:
        state["destination_info"] = {
            "name": extracted.get("destination", destination),
            "description": extracted.get("description"),
            "best_season": extracted.get("best_season"),
            "attractions": extracted.get("attractions", []),
            "matched_interests": extracted.get("matching_interests", []),
            "avg_daily_cost": dest_data.get("avg_daily_cost") if dest_data else 3000
        }
        # Update canonical destination name if LLM provided a better one
        state["destination"] = extracted.get("destination", destination)
    else:
        raise ValueError("Failed to parse JSON response from LLM")
    
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
