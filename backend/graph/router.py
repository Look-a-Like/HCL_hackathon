import time
from typing import Callable, Any
from backend.graph.state import TravelState


MAX_RETRIES = 2


def with_retry(agent_fn: Callable[[TravelState], TravelState], agent_name: str) -> Callable[[TravelState], TravelState]:
    def wrapper(state: TravelState) -> TravelState:
        retries = state["retries"].get(agent_name, 0)
        try:
            return agent_fn(state)
        except Exception as e:
            if retries < MAX_RETRIES:
                state["retries"][agent_name] = retries + 1
                return agent_fn(state)
            else:
                state["errors"].append(f"{agent_name} failed after {MAX_RETRIES} retries: {str(e)}")
                return apply_fallback(state, agent_name)
    return wrapper


def apply_fallback(state: TravelState, agent_name: str) -> TravelState:
    fallbacks = {
        "destination": lambda s: {**s, "destination_info": {"error": "Fallback - destination unavailable"}},
        "budget": lambda s: {**s, "budget_breakdown": {"error": "Fallback - budget calculation unavailable"}},
        "itinerary": lambda s: {**s, "itinerary": []},
        "booking": lambda s: {**s, "booking_options": {"hotels": [], "flights": []}},
        "local_experience": lambda s: {**s, "local_experiences": []},
    }
    if agent_name in fallbacks:
        result = fallbacks[agent_name](state)
        for k, v in result.items():
            state[k] = v
    return state


def tracked(agent_fn: Callable[[TravelState], TravelState], agent_name: str) -> Callable[[TravelState], TravelState]:
    def wrapper(state: TravelState) -> TravelState:
        start = time.time()
        state = agent_fn(state)
        elapsed = round(time.time() - start, 2)
        state["metrics"]["latency"][agent_name] = elapsed
        return state
    return wrapper