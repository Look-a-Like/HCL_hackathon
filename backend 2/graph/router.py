import time
import asyncio
from typing import Callable, Any, Coroutine
from backend.graph.state import TravelState


MAX_RETRIES = 2


def with_retry(agent_fn: Callable[[TravelState], Coroutine[Any, Any, TravelState]], agent_name: str) -> Callable[[TravelState], Coroutine[Any, Any, TravelState]]:
    async def wrapper(state: TravelState) -> TravelState:
        for attempt in range(MAX_RETRIES + 1):
            try:
                # If the agent_fn returns a JSON string with an error, 
                # we should raise an exception so it can be caught by retry.
                # However, agents should handle their own errors.
                # Let's check if we should look for "error" in state["errors"].
                
                result = await agent_fn(state)
                # Some agents might add to state["errors"] instead of raising.
                # But here we only catch exceptions.
                return result
            except Exception as e:
                if attempt < MAX_RETRIES:
                    # Exponential backoff: 2s, 4s...
                    wait_time = (2 ** (attempt + 1))
                    await asyncio.sleep(wait_time)
                else:
                    state["errors"].append(f"{agent_name} failed after {MAX_RETRIES} retries: {str(e)}")
                    return apply_fallback(state, agent_name)
    return wrapper


def apply_fallback(state: TravelState, agent_name: str) -> TravelState:
    fallbacks = {
        "destination": lambda s: {"destination_info": {"error": "Fallback - destination unavailable"}},
        "budget": lambda s: {"budget_breakdown": {"error": "Fallback - budget calculation unavailable"}},
        "itinerary": lambda s: {"itinerary": []},
        "booking": lambda s: {"booking_options": {"hotels": [], "flights": []}},
        "local_experience": lambda s: {"local_experiences": []},
    }
    if agent_name in fallbacks:
        result = fallbacks[agent_name](state)
        for k, v in result.items():
            state[k] = v
    return state


def tracked(agent_fn: Callable[[TravelState], Coroutine[Any, Any, TravelState]], agent_name: str) -> Callable[[TravelState], Coroutine[Any, Any, TravelState]]:
    async def wrapper(state: TravelState) -> TravelState:
        start = time.time()
        state = await agent_fn(state)
        elapsed = round(time.time() - start, 2)
        
        # Ensure metrics is in state
        if "metrics" not in state:
            state["metrics"] = {"latency": {}, "cost": {}}
        if "latency" not in state["metrics"]:
            state["metrics"]["latency"] = {}
        
        state["metrics"]["latency"][agent_name] = elapsed
        return state
    return wrapper
