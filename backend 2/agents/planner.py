import os
import json
import re
from typing import Optional
from backend.graph.state import TravelState
from backend.middleware.guard import is_injection, sanitize_input
from backend.prompts.planner import PLANNER_SYSTEM_PROMPT, PLANNER_USER_PROMPT, REFINEMENT_PROMPT
from backend.tools.llm import get_llm_client, parse_json_response


async def planner_agent(state: TravelState) -> TravelState:
    user_input = sanitize_input(state["user_input"])
    
    if is_injection(user_input):
        state["errors"].append("Invalid input detected")
        state["missing_fields"] = ["invalid input"]
        return state
    
    client = get_llm_client()
    
    if state["conversation_history"]:
        prompt = REFINEMENT_PROMPT.format(
            history=state["conversation_history"][-1],
            user_input=user_input
        )
    else:
        prompt = PLANNER_USER_PROMPT.format(user_input=user_input)
    
    # Let with_retry handle exceptions from achat
    result_text = await client.achat(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=PLANNER_SYSTEM_PROMPT,
        max_tokens=500,
        temperature=0.3
    )
    extracted = parse_json_response(result_text)
    
    if not extracted:
        # If parsing fails, use fallback parsing
        extracted = _fallback_parse(user_input)
    
    if extracted:
        state["destination"] = extracted.get("destination")
        state["budget"] = extracted.get("budget")
        state["duration_days"] = extracted.get("duration_days")
        state["travel_dates"] = extracted.get("travel_dates")
        state["interests"] = extracted.get("interests", [])
        state["missing_fields"] = extracted.get("missing_fields", [])
    
    state["conversation_history"].append(user_input)
    
    return state


def _fallback_parse(user_input: str) -> dict:
    user_lower = user_input.lower()
    
    destination = None
    destinations = [
        "goa", "manali", "jaipur", "kerala", "shimla", "agra", "rishikesh",
        "darjeeling", "varanasi", "ooty", "mysore", "leh", "ladakh",
        "assam", "guwahati", "kaziranga", "majuli",
        "meghalaya", "shillong", "cherrapunji",
        "sikkim", "gangtok", "andaman", "port blair",
        "coorg", "hampi", "gokarna", "munnar", "alleppey", "kovalam",
        "pondicherry", "mahabalipuram", "rameswaram", "madurai",
        "kolkata", "delhi", "mumbai", "pune", "bangalore", "hyderabad",
        "udaipur", "jodhpur", "jaisalmer", "pushkar",
        "nainital", "mussoorie", "haridwar", "auli",
        "srinagar", "pahalgam", "gulmarg",
    ]
    for dest in destinations:
        if dest in user_lower:
            destination = dest.title()
            break
    
    budget_match = re.search(r'(?:₹|rs\.?|inr)\s*([\d,]+)|([\d,]+)\s*(?:₹|rs\.?|inr)', user_lower)
    budget = None
    if budget_match:
        num_str = budget_match.group(1) or budget_match.group(2)
        budget = int(num_str.replace(",", ""))
    
    days_match = re.search(r'(\d+)\s*(?:day|days|night|nights)', user_lower)
    duration_days = int(days_match.group(1)) if days_match else 3  # default 3 days
    
    interests = []
    interest_keywords = {
        "beach": ["beach", "beaches"],
        "mountains": ["mountain", "mountains", "hill station"],
        "adventure": ["adventure", "trek", "rafting"],
        "food": ["food", "foodie", "culinary", "cuisine"],
        "culture": ["culture", "heritage", "historical", "temple"],
        "nature": ["nature", "wildlife", "safari"],
        "party": ["party", "nightlife"],
    }
    for interest, keywords in interest_keywords.items():
        if any(kw in user_lower for kw in keywords):
            interests.append(interest)
    
    missing = []
    if not destination:
        missing.append("destination")
    if not budget:
        missing.append("budget")
    if not duration_days:
        missing.append("duration")
    
    return {
        "destination": destination,
        "budget": budget,
        "duration_days": duration_days,
        "travel_dates": None,
        "interests": interests,
        "missing_fields": missing
    }