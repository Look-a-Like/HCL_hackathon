import json
from backend.graph.state import TravelState
from backend.tools.travel_data import get_destination_by_name


def local_experience_agent(state: TravelState) -> TravelState:
    destination = state.get("destination")
    interests = state.get("interests", [])
    
    if not destination:
        state["errors"].append("No destination for local experiences")
        state["local_experiences"] = []
        return state
    
    dest_data = get_destination_by_name(destination)
    experiences = _get_local_experiences(destination, interests, dest_data)
    
    state["local_experiences"] = experiences
    return state


def _get_local_experiences(destination: str, interests: list[str], dest_data: dict) -> list[dict]:
    experiences_db = {
        "goa": {
            "food": [
                {"name": "Beach Shacks at Baga", "description": "Fresh seafood right on the beach", "cost_range": "₹300-500"},
                {"name": "Fisherman's Wharf", "description": "Authentic Goan seafood", "cost_range": "₹500-800"},
                {"name": "Hotel Terminal", "description": "Famous for prawns fry", "cost_range": "₹400-600"}
            ],
            "hidden_gems": [
                {"name": "Tobacco Garden", "description": "Hidden beach near Ashvem", "cost_range": "Free"},
                {"name": "Chorão Island", "description": "Quaint Portuguese island", "cost_range": "₹200"},
                {"name": "Mangueshi Temple", "description": "Offbeat cultural site", "cost_range": "Free"}
            ],
            "culture": [
                {"name": "St. Francis Xavier Church", "description": "Historical church in Old Goa", "cost_range": "Free"},
                {"name": "Fontainhas Walk", "description": "Latin Quarter heritage walk", "cost_range": "₹100"},
                {"name": "Sunset Cruise", "description": "Mandovi river sunset", "cost_range": "₹300-500"}
            ]
        },
        "manali": {
            "food": [
                {"name": "Johnson's Cafe", "description": "Famous for apple pie", "cost_range": "₹200-400"},
                {"name": "Chicku", "description": "Local Himalayan cuisine", "cost_range": "₹150-300"},
                {"name": "Mountains Cafe", "description": "Cozy cafe with valley views", "cost_range": "₹150-250"}
            ],
            "hidden_gems": [
                {"name": "Jana Falls", "description": "Lesser known waterfall", "cost_range": "Free"},
                {"name": "Naggar Castle", "description": "500-year old castle", "cost_range": "₹100"},
                {"name": "Kashmiri Colony", "description": "Authentic Kashmiri culture", "cost_range": "Free"}
            ],
            "adventure": [
                {"name": "Bhrigu Lake Trek", "description": "High altitude lake trek", "cost_range": "₹500"},
                {"name": "Paragliding Solang", "description": "Flying over valleys", "cost_range": "₹1500"},
                {"name": "River Rafting", "description": "Beas river rapids", "cost_range": "₹600-1000"}
            ]
        },
        "jaipur": {
            "food": [
                {"name": "Lassi Wala", "description": "Famous creamy lassi", "cost_range": "₹50"},
                {"name": "Pyaaz Kachori at Rawat", "description": "Famous kachori shop", "cost_range": "₹50"},
                {"name": "Suvarna Jain", "description": "Traditional Rajasthani thali", "cost_range": "₹300-500"}
            ],
            "hidden_gems": [
                {"name": "Anokhi Museum", "description": "Block printing museum", "cost_range": "₹50"},
                {"name": "Jal Mahal View", "description": "Water palace from roadside", "cost_range": "Free"},
                {"name": "Baba Ramdev Temple", "description": "Offbeat cultural site", "cost_range": "Free"}
            ],
            "culture": [
                {"name": "Chand Baori", "description": "Stepwell in Abhaneri", "cost_range": "₹100"},
                {"name": "Elephant Festival", "description": "If visiting in Feb/March", "cost_range": "Varies"},
                {"name": "Hot Air Balloon", "description": "City aerial view", "cost_range": "₹3000"}
            ]
        },
        "kerala": {
            "food": [
                {"name": "Kadalundi", "description": "Seafood in Fort Kochi", "cost_range": "₹400-600"},
                {"name": "Maharaja", "description": "Traditional sadya", "cost_range": "₹200-400"},
                {"name": "Seafood at Kumarakom", "description": "Fresh catch daily", "cost_range": "₹300-500"}
            ],
            "hidden_gems": [
                {"name": "Kumarakom Bird Sanctuary", "description": "Migratory birds", "cost_range": "₹50"},
                {"name": "Kottayam", "description": "Offbeat backwater destination", "cost_range": "₹200"},
                {"name": "Marari Beach", "description": "Lesser known beach", "cost_range": "Free"}
            ],
            "culture": [
                {"name": "Kathakali Show", "description": "Traditional dance drama", "cost_range": "₹200"},
                {"name": "Kalaripayattu", "description": "Martial arts demonstration", "cost_range": "₹300"},
                {"name": "Spice Plantation Tour", "description": "Learn about spices", "cost_range": "₹500"}
            ]
        },
        "rishikesh": {
            "food": [
                {"name": "Chotiwala", "description": "Famous restaurant chain", "cost_range": "₹200-400"},
                {"name": "German Bakery", "description": "Healthy eats", "cost_range": "₹150-300"},
                {"name": "Ramana's", "description": "Organic café", "cost_range": "₹150-250"}
            ],
            "hidden_gems": [
                {"name": "Phool Chatti Waterfall", "description": "Secret waterfall", "cost_range": "Free"},
                {"name": "Beatles Ashram", "description": "Abandoned ashram", "cost_range": "₹50"},
                {"name": "Gurugram", "description": "Hidden spiritual spot", "cost_range": "Free"}
            ],
            "yoga": [
                {"name": "Sivananda Ashram", "description": "Traditional yoga", "cost_range": "Free donation"},
                {"name": "Art of Living", "description": "Meditation sessions", "cost_range": "₹500"},
                {"name": "Yoga on Ganga", "description": "Riverside sessions", "cost_range": "₹200"}
            ]
        }
    }
    
    dest_lower = destination.lower()
    dest_experiences = experiences_db.get(dest_lower, {})
    
    if not dest_experiences:
        dest_experiences = {
            "food": [{"name": "Local restaurants", "description": "Explore local cuisine", "cost_range": "₹200-400"}],
            "hidden_gems": [{"name": "Explore the area", "description": "Discover hidden spots", "cost_range": "Varies"}],
            "culture": [{"name": "Local attractions", "description": "Cultural sites", "cost_range": "Varies"}]
        }
    
    result = []
    
    interest_mapping = {
        "food": "food",
        "foodie": "food",
        "culture": "culture",
        "heritage": "culture",
        "adventure": "adventure",
        "mountains": "adventure",
        "nature": "hidden_gems"
    }
    
    for interest in interests:
        if interest in interest_mapping:
            exp_type = interest_mapping[interest]
            for exp in dest_experiences.get(exp_type, []):
                result.append({
                    "name": exp["name"],
                    "type": exp_type,
                    "description": exp["description"],
                    "estimated_cost": exp["cost_range"]
                })
    
    if not result:
        for exp_type, exps in dest_experiences.items():
            for exp in exps[:2]:
                result.append({
                    "name": exp["name"],
                    "type": exp_type,
                    "description": exp["description"],
                    "estimated_cost": exp["cost_range"]
                })
    
    return result[:10]