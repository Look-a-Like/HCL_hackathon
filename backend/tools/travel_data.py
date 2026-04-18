import os
import json
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"

_destinations_cache = None
_hotels_cache = None
_flights_cache = None


def load_destinations() -> list[dict]:
    global _destinations_cache
    if _destinations_cache is None:
        with open(DATA_DIR / "destinations.json", "r") as f:
            data = json.load(f)
            _destinations_cache = data.get("destinations", [])
    return _destinations_cache


def load_hotels() -> list[dict]:
    global _hotels_cache
    if _hotels_cache is None:
        with open(DATA_DIR / "hotels.json", "r") as f:
            data = json.load(f)
            _hotels_cache = data.get("hotels", [])
    return _hotels_cache


def load_flights() -> list[dict]:
    global _flights_cache
    if _flights_cache is None:
        with open(DATA_DIR / "flights.json", "r") as f:
            data = json.load(f)
            _flights_cache = data.get("flights", [])
    return _flights_cache


def get_destination_by_name(name: str) -> dict | None:
    destinations = load_destinations()
    name_lower = name.lower()
    for dest in destinations:
        if dest["name"].lower() == name_lower:
            return dest
    for dest in destinations:
        if name_lower in dest["name"].lower() or name_lower in dest.get("keywords", []):
            return dest
    return None


def get_hotels_for_destination(destination: str) -> list[dict]:
    hotels = load_hotels()
    for dest_hotels in hotels:
        if dest_hotels["destination"].lower() == destination.lower():
            return dest_hotels.get("hotels", [])
    return []


def get_flights_to_destination(destination: str) -> list[dict]:
    flights = load_flights()
    dest_lower = destination.lower()
    matching_flights = []
    for flight in flights:
        if dest_lower in flight["to"].lower():
            matching_flights.append(flight)
    return matching_flights


def search_destinations(query: str) -> list[dict]:
    destinations = load_destinations()
    query_lower = query.lower()
    results = []
    for dest in destinations:
        score = 0
        if query_lower in dest["name"].lower():
            score += 10
        if query_lower in dest.get("type", "").lower():
            score += 5
        if query_lower in dest.get("state", "").lower():
            score += 3
        if any(query_lower in k.lower() for k in dest.get("keywords", [])):
            score += 7
        if any(query_lower in a["name"].lower() for a in dest.get("attractions", [])):
            score += 4
        if score > 0:
            results.append((score, dest))
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]


def get_all_destination_names() -> list[str]:
    destinations = load_destinations()
    return [d["name"] for d in destinations]


def get_tier_for_budget(budget_per_day: float) -> str:
    if budget_per_day < 1000:
        return "budget"
    elif budget_per_day < 3000:
        return "mid"
    else:
        return "luxury"