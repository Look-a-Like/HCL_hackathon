import json
from backend.graph.state import TravelState
from backend.prompts.local_experience import LOCAL_EXPERIENCE_SYSTEM_PROMPT, LOCAL_EXPERIENCE_USER_PROMPT
from backend.tools.llm import get_llm_client, parse_json_response
from backend.tools.search import aserper_search


async def local_experience_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    interests = state.get("interests", [])
    
    if not destination:
        state["errors"].append("No destination specified for local experiences")
        return state
    
    # Dynamic search for local experiences
    search_context = ""
    try:
        search_results = await aserper_search(f"local food, hidden gems, and authentic experiences in {destination}")
        search_context = json.dumps(search_results)
    except Exception as e:
        search_context = f"Search failed: {str(e)}"
    
    client = get_llm_client()
    prompt = LOCAL_EXPERIENCE_USER_PROMPT.format(
        destination=destination,
        interests=", ".join(interests) if interests else "General travel"
    )
    
    # Combine user prompt with search context
    full_prompt = f"{prompt}\n\nSearch context:\n{search_context}"
    
    response = await client.achat(
        messages=[{"role": "user", "content": full_prompt}],
        system_prompt=LOCAL_EXPERIENCE_SYSTEM_PROMPT,
        max_tokens=1000,
        temperature=0.4
    )
    
    try:
        extracted = parse_json_response(response)
        
        experiences = []
        if isinstance(extracted, list):
            experiences = extracted
        elif isinstance(extracted, dict):
            experiences = extracted.get("experiences", extracted.get("recommendations", []))
            if not experiences:
                # Look for any list
                for val in extracted.values():
                    if isinstance(val, list):
                        experiences = val
                        break
        
        if not experiences:
            raise ValueError("Could not extract local experiences list from LLM response")
            
        state["local_experiences"] = experiences
        
    except Exception as e:
        state["errors"].append(f"Local experience parsing error: {str(e)}")
        # Fallback empty list
        state["local_experiences"] = [
            {
                "name": "Local Street Food Tour",
                "type": "food",
                "description": "Explore the authentic flavors of the city at a local market.",
                "estimated_cost": "500-1000 INR",
                "why_special": "Experience the true local taste and culture."
            }
        ]
    
    return state
