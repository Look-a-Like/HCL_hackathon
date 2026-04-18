from typing import List


def rank_options(options: List[dict], budget: float, key: str, max_results: int = 3) -> List[dict]:
    if not options:
        return []
    
    ranked = sorted(options, key=lambda x: abs(x.get(key, 0) - budget))
    return ranked[:max_results]


def rank_hotels_by_budget(hotels: List[dict], budget_per_night: float, max_results: int = 3) -> List[dict]:
    return rank_options(hotels, budget_per_night, "price_per_night", max_results)


def rank_flights_by_budget(flights: List[dict], max_budget: float, max_results: int = 3) -> List[dict]:
    budget_per_ticket = max_budget
    return rank_options(flights, budget_per_ticket, "price", max_results)


def filter_by_tier(options: List[dict], tier: str) -> List[dict]:
    return [opt for opt in options if opt.get("tier", "").lower() == tier.lower()]


def rank_by_rating(options: List[dict], max_results: int = 5) -> List[dict]:
    if not options:
        return []
    return sorted(options, key=lambda x: x.get("rating", 0), reverse=True)[:max_results]