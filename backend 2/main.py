from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from backend.middleware.rate_limit import limiter
from backend.graph.workflow import langgraph_app
from backend.graph.state import create_initial_state
from backend.middleware.guard import is_injection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Cartographer AI API")
    yield
    logger.info("Shutting down Cartographer AI API")


app = FastAPI(title="Cartographer AI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter.limit
app.add_exception_handler(Exception, lambda req, exc: {"error": str(exc)})


class PlanRequest(BaseModel):
    query: str


def transform_final_plan(result: dict) -> dict:
    """Transform LangGraph state into the frontend's FinalPlan structure."""
    bb = result.get("budget_breakdown") or {}
    budget_breakdown = {
        "flights": bb.get("transport", 0),
        "hotel": bb.get("hotel", 0),
        "activities": bb.get("activities", 0),
        "food": bb.get("food", 0),
        "transport": bb.get("transport", 0),
        "misc": bb.get("buffer", 0),
        "total": bb.get("total") or result.get("budget") or 0,
        "currency": bb.get("currency", "INR"),
    }

    raw_itinerary = result.get("itinerary") or []
    itinerary = []
    for i, day in enumerate(raw_itinerary):
        day_num = day.get("day_number") or day.get("day") or (i + 1)
        theme = day.get("title") or day.get("theme") or f"Day {day_num}"

        morning_default = "Explore the local area"
        afternoon_default = "Visit key attractions"
        evening_default = "Dinner and leisure"

        # Direct fields (new prompt format)
        morning = day.get("morning") or morning_default
        afternoon = day.get("afternoon") or afternoon_default
        evening = day.get("evening") or evening_default

        # Fallback: activities array (old format)
        if morning == morning_default and afternoon == afternoon_default:
            activities = day.get("activities", [])
            if isinstance(activities, list):
                for act in activities:
                    time_slot = str(act.get("time", "")).lower()
                    desc = act.get("description") or act.get("activity") or ""
                    if "morning" in time_slot:
                        morning = desc or morning
                    elif "afternoon" in time_slot or "midday" in time_slot or "noon" in time_slot:
                        afternoon = desc or afternoon
                    elif "evening" in time_slot or "night" in time_slot:
                        evening = desc or evening

        raw_meals = day.get("meals", [])
        meals = {}
        if isinstance(raw_meals, list):
            for m in raw_meals:
                name = str(m.get("name", "")).lower()
                if "break" in name:
                    meals["breakfast"] = m.get("name", "Local breakfast")
                elif "lunch" in name:
                    meals["lunch"] = m.get("name", "Local lunch")
                elif "dinner" in name or "supper" in name:
                    meals["dinner"] = m.get("name", "Local dinner")
                else:
                    meals.setdefault("lunch", m.get("name", "Local meal"))
        elif isinstance(raw_meals, dict):
            meals = raw_meals

        itinerary.append({
            "day": day_num,
            "theme": theme,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "meals": meals,
            "estimated_cost": day.get("estimated_cost", 0),
        })

    raw_gems = result.get("local_experiences") or []
    local_gems = [
        {
            "name": gem.get("name", "Local Gem"),
            "type": gem.get("type", "experience"),
            "description": gem.get("description", ""),
            "tip": gem.get("why_special") or gem.get("tip") or gem.get("note"),
            "maps_url": gem.get("maps_url"),
            "tripadvisor_url": gem.get("tripadvisor_url"),
            "estimated_cost": gem.get("estimated_cost"),
        }
        for gem in raw_gems
    ]

    raw_booking = result.get("booking_options") or {}
    hotels = raw_booking.get("hotels", [])
    flights = raw_booking.get("flights", [])

    formatted_hotels = [
        {
            "name": h.get("name", "Hotel"),
            "price": h.get("price_per_night", 0),
            "rating": h.get("rating"),
            "notes": ", ".join(h.get("amenities", [])) if h.get("amenities") else None,
            "book_url": h.get("book_url"),
            "maps_url": h.get("maps_url"),
        }
        for h in hotels
    ]
    formatted_flights = [
        {
            "name": f.get("airline", "Flight"),
            "price": f.get("price", 0),
            "route": f.get("route"),
            "duration": f.get("duration"),
            "notes": f.get("stops"),
            "book_url": f.get("book_url"),
            "search_url": f.get("search_url"),
        }
        for f in flights
    ]

    duration_days = result.get("duration_days") or len(itinerary) or 3
    interests = result.get("interests") or []
    destination = result.get("destination") or "Your Destination"
    budget = result.get("budget") or 0

    return {
        "destination": destination,
        "trip_duration": f"{duration_days} days",
        "travel_style": ", ".join(interests) if interests else "Flexible",
        "budget_breakdown": budget_breakdown,
        "itinerary": itinerary,
        "booking_options": {
            "flights": formatted_flights,
            "hotels": formatted_hotels,
        },
        "local_gems": local_gems,
        "summary": f"A {duration_days}-day trip to {destination} optimized for ₹{budget:,.0f}.",
        "metrics": result.get("metrics"),
    }


@app.get("/")
async def root():
    return {"message": "Cartographer AI API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


async def generate_events(user_input: str):
    yield f"data: {json.dumps({'type': 'agent_start', 'agent': 'planner'})}\n\n"

    if is_injection(user_input):
        yield f"data: {json.dumps({'type': 'error', 'error': 'Invalid input detected'})}\n\n"
        return

    initial_state = create_initial_state(user_input)

    try:
        result = dict(initial_state)
        async for step in langgraph_app.astream(initial_state):
            for agent_name, output in step.items():
                yield f"data: {json.dumps({'type': 'agent_start', 'agent': agent_name})}\n\n"
                result.update(output)
                yield f"data: {json.dumps({'type': 'agent_done', 'agent': agent_name, 'data': None})}\n\n"

        final_plan = transform_final_plan(result)
        yield f"data: {json.dumps({'type': 'final_plan', 'data': final_plan})}\n\n"

    except Exception as e:
        logger.error(f"Error in travel planning: {str(e)}", exc_info=True)
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"


@app.post("/plan")
@limiter.limit("5/minute")
async def plan(request: Request, body: PlanRequest):
    return StreamingResponse(
        generate_events(body.query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/plan/sync")
async def plan_sync(body: PlanRequest):
    if is_injection(body.query):
        return {"error": "Invalid input detected"}

    initial_state = create_initial_state(body.query)

    try:
        result = await langgraph_app.ainvoke(initial_state)
        return transform_final_plan(result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}
