from typing import List
from urllib.parse import quote_plus


def _make_hotel_link(hotel_name: str, destination: str) -> str:
    query = quote_plus(f"{hotel_name} {destination}")
    return f"https://www.makemytrip.com/hotels/hotel-listing/?city={quote_plus(destination)}&searchText={query}"


def _make_flight_link(from_city: str, to_city: str) -> str:
    query = quote_plus(f"flights from {from_city} to {to_city}")
    return f"https://www.google.com/travel/flights?q={query}"


def _make_experience_link(experience_name: str, destination: str) -> str:
    query = quote_plus(f"{experience_name} {destination}")
    return f"https://www.google.com/maps/search/{query}"


def _make_tripadvisor_link(experience_name: str, destination: str) -> str:
    query = quote_plus(f"{experience_name} {destination}")
    return f"https://www.tripadvisor.com/Search?q={query}"


def rank_options(options: List[dict], budget: float, key: str, max_results: int = 3) -> List[dict]:
    if not options:
        return []
    ranked = sorted(options, key=lambda x: abs(x.get(key, 0) - budget))
    return ranked[:max_results]


def rank_hotels_by_budget(hotels: List[dict], budget_per_night: float, max_results: int = 3, destination: str = "") -> List[dict]:
    ranked = rank_options(hotels, budget_per_night, "price_per_night", max_results)
    for hotel in ranked:
        hotel["book_url"] = _make_hotel_link(hotel.get("name", ""), destination)
        hotel["maps_url"] = f"https://www.google.com/maps/search/{quote_plus(hotel.get('name', '') + ' ' + destination)}"
    return ranked


def rank_flights_by_budget(flights: List[dict], max_budget: float, max_results: int = 3) -> List[dict]:
    ranked = rank_options(flights, max_budget, "price", max_results)
    for flight in ranked:
        flight["book_url"] = _make_flight_link(flight.get("from", ""), flight.get("to", ""))
        flight["search_url"] = f"https://www.skyscanner.co.in/transport/flights/{quote_plus(flight.get('from',''))}/{quote_plus(flight.get('to',''))}/"
    return ranked


def filter_by_tier(options: List[dict], tier: str) -> List[dict]:
    return [opt for opt in options if opt.get("tier", "").lower() == tier.lower()]


def rank_by_rating(options: List[dict], max_results: int = 5) -> List[dict]:
    if not options:
        return []
    return sorted(options, key=lambda x: x.get("rating", 0), reverse=True)[:max_results]


def enrich_experience_with_links(experience: dict, destination: str) -> dict:
    name = experience.get("name", "")
    experience["maps_url"] = _make_experience_link(name, destination)
    experience["tripadvisor_url"] = _make_tripadvisor_link(name, destination)
    return experience
