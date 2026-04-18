from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging

from backend.middleware.rate_limit import limiter
from backend.graph.workflow import langgraph_app
from backend.graph.state import create_initial_state
from backend.middleware.guard import is_injection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Travel Planning API")
    yield
    logger.info("Shutting down Travel Planning API")


app = FastAPI(title="Travel Planning API", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter.limit

app.add_exception_handler(Exception, lambda req, exc: {"error": str(exc)})


class PlanRequest(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Travel Planning API", "version": "1.0.0", "endpoints": ["/plan", "/health"]}


@app.get("/health")
async def health():
    return {"status": "healthy"}


async def generate_events(user_input: str):
    initial_state = create_initial_state(user_input)
    
    yield f"data: {json.dumps({'agent': 'planner', 'status': 'started', 'message': 'Processing your request...'})}\n\n"
    
    try:
        if is_injection(user_input):
            yield f"data: {json.dumps({'agent': 'error', 'status': 'error', 'message': 'Invalid input detected'})}\n\n"
            return
        
        result = initial_state
        for step in langgraph_app.stream(initial_state):
            for agent_name, output in step.items():
                result[agent_name] = output
                yield f"data: {json.dumps({'agent': agent_name, 'status': 'completed', 'output': output})}\n\n"
        
        final_plan = {
            "summary": f"{result.get('duration_days', 'N/A')}-day trip to {result.get('destination', 'Unknown')}",
            "destination": result.get("destination"),
            "budget": result.get("budget"),
            "duration_days": result.get("duration_days"),
            "budget_breakdown": result.get("budget_breakdown"),
            "itinerary": result.get("itinerary"),
            "booking_options": result.get("booking_options"),
            "local_experiences": result.get("local_experiences"),
            "metrics": result.get("metrics"),
            "errors": result.get("errors", [])
        }
        
        yield f"data: {json.dumps({'agent': 'final', 'status': 'complete', 'output': final_plan})}\n\n"
        
    except Exception as e:
        logger.error(f"Error in travel planning: {str(e)}")
        yield f"data: {json.dumps({'agent': 'error', 'status': 'error', 'message': str(e)})}\n\n"


@app.post("/plan")
@limiter.limit("5/minute")
async def plan(request: Request, body: PlanRequest):
    return StreamingResponse(
        generate_events(body.query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/plan/sync")
async def plan_sync(body: PlanRequest):
    if is_injection(body.query):
        return {"error": "Invalid input detected"}
    
    initial_state = create_initial_state(body.query)
    
    try:
        result = langgraph_app.invoke(initial_state)
        
        final_plan = {
            "summary": f"{result.get('duration_days', 'N/A')}-day trip to {result.get('destination', 'Unknown')}",
            "destination": result.get("destination"),
            "budget": result.get("budget"),
            "duration_days": result.get("duration_days"),
            "budget_breakdown": result.get("budget_breakdown"),
            "itinerary": result.get("itinerary"),
            "booking_options": result.get("booking_options"),
            "local_experiences": result.get("local_experiences"),
            "metrics": result.get("metrics"),
            "errors": result.get("errors", [])
        }
        
        return final_plan
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}