from backend.graph.state import TravelState
from backend.tools.ranking import enrich_experience_with_links

EXPERIENCES_DB: dict[str, dict[str, list[dict]]] = {
    "goa": {
        "food": [
            {"name": "Beach Shacks at Baga", "description": "Fresh seafood right on the beach", "cost_range": "₹300–500"},
            {"name": "Fisherman's Wharf", "description": "Authentic Goan seafood restaurant", "cost_range": "₹500–800"},
            {"name": "Hotel Terminal", "description": "Famous for prawns fry and local Goan thali", "cost_range": "₹400–600"},
        ],
        "hidden_gem": [
            {"name": "Tobacco Garden", "description": "Quiet hidden beach near Ashvem", "cost_range": "Free"},
            {"name": "Chorão Island", "description": "Quaint Portuguese heritage island", "cost_range": "₹200"},
            {"name": "Mangueshi Temple", "description": "Offbeat Goan cultural heritage site", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "St. Francis Xavier Church", "description": "Historical church in Old Goa (UNESCO)", "cost_range": "Free"},
            {"name": "Fontainhas Heritage Walk", "description": "Latin Quarter lanes with Portuguese-era houses", "cost_range": "₹100"},
            {"name": "Mandovi Sunset Cruise", "description": "Goan music and sunset over the river", "cost_range": "₹300–500"},
        ],
    },
    "manali": {
        "food": [
            {"name": "Johnson's Cafe", "description": "Famous for apple pie and trout fish", "cost_range": "₹200–400"},
            {"name": "Chicku Cafe", "description": "Local Himalayan cuisine with valley views", "cost_range": "₹150–300"},
            {"name": "Mountains Cafe", "description": "Cozy cafe with panoramic mountain views", "cost_range": "₹150–250"},
        ],
        "hidden_gem": [
            {"name": "Jana Falls", "description": "Lesser-known waterfall through pine forest", "cost_range": "Free"},
            {"name": "Naggar Castle", "description": "500-year-old stone castle above Kullu Valley", "cost_range": "₹100"},
            {"name": "Kashmiri Colony", "description": "Authentic Kashmiri crafts and culture", "cost_range": "Free"},
        ],
        "activity": [
            {"name": "Bhrigu Lake Trek", "description": "High-altitude lake trek with glacier views", "cost_range": "₹500"},
            {"name": "Paragliding at Solang Valley", "description": "Flying over Himalayan valleys", "cost_range": "₹1,500"},
            {"name": "Beas River Rafting", "description": "Grade III–IV white-water rapids", "cost_range": "₹600–1,000"},
        ],
    },
    "jaipur": {
        "food": [
            {"name": "Lassi Wala near Tripolia Gate", "description": "Famous thick creamy lassi served in earthen pots", "cost_range": "₹50"},
            {"name": "Pyaaz Kachori at Rawat Misthan Bhandar", "description": "Iconic spiced onion kachori shop", "cost_range": "₹50"},
            {"name": "LMB Restaurant", "description": "Traditional Rajasthani thali since 1954", "cost_range": "₹300–500"},
        ],
        "hidden_gem": [
            {"name": "Anokhi Museum of Hand Printing", "description": "Block printing museum in a restored haveli", "cost_range": "₹50"},
            {"name": "Jal Mahal Viewpoint", "description": "Water palace view from the roadside promenade", "cost_range": "Free"},
            {"name": "Pandit Kulfi near Hawa Mahal", "description": "Decades-old street stall serving dense kesar kulfi", "cost_range": "₹30"},
        ],
        "culture": [
            {"name": "Chand Baori Stepwell", "description": "Ancient stepwell with 3,500 steps in Abhaneri", "cost_range": "₹100"},
            {"name": "Hot Air Balloon Ride", "description": "Aerial view of the Pink City at sunrise", "cost_range": "₹3,000"},
            {"name": "Nahargarh Fort Sunset", "description": "Panoramic view of Jaipur from the hilltop fort", "cost_range": "₹50"},
        ],
    },
    "kerala": {
        "food": [
            {"name": "Kayees Biryani", "description": "Legendary Malabar biryani in Mattancherry", "cost_range": "₹150–250"},
            {"name": "Seafood at Kumarakom", "description": "Fresh daily catch at backwater restaurants", "cost_range": "₹300–500"},
            {"name": "Sadhya at a Local Home", "description": "Traditional 24-dish banana-leaf feast", "cost_range": "₹200–400"},
        ],
        "hidden_gem": [
            {"name": "Kumarakom Bird Sanctuary", "description": "Migratory birds over the Vembanad Lake", "cost_range": "₹50"},
            {"name": "Marari Beach", "description": "Quiet, unspoiled fishermen's beach", "cost_range": "Free"},
            {"name": "Jew Town Mattancherry", "description": "Antique shops and spice warehouses in Fort Kochi", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "Kathakali Show", "description": "Classical Keralan dance-drama with elaborate makeup", "cost_range": "₹200"},
            {"name": "Kalaripayattu Demonstration", "description": "World's oldest martial art performed live", "cost_range": "₹300"},
            {"name": "Spice Plantation Tour", "description": "Walk through cardamom and pepper plantations", "cost_range": "₹500"},
        ],
    },
    "rishikesh": {
        "food": [
            {"name": "Chotiwala Restaurant", "description": "Iconic vegetarian restaurant on the ghats since 1958", "cost_range": "₹200–400"},
            {"name": "German Bakery Rishikesh", "description": "Healthy organic meals with Ganga views", "cost_range": "₹150–300"},
            {"name": "Ramana's Garden Cafe", "description": "Organic garden-to-table vegetarian", "cost_range": "₹150–250"},
        ],
        "hidden_gem": [
            {"name": "Phool Chatti Waterfall", "description": "Secret waterfall 15 km upstream on the Ganga", "cost_range": "Free"},
            {"name": "Beatles Ashram (Chaurasi Kutia)", "description": "Abandoned ashram with surreal wall art", "cost_range": "₹50"},
            {"name": "Kunjapuri Temple at Sunrise", "description": "Hill temple with Himalayan panorama at dawn", "cost_range": "Free"},
        ],
        "activity": [
            {"name": "Sivananda Ashram Yoga", "description": "Traditional morning yoga and meditation sessions", "cost_range": "Free (donation)"},
            {"name": "Ganga Aarti at Triveni Ghat", "description": "Nightly fire ceremony on the holy river", "cost_range": "Free"},
            {"name": "White Water Rafting (Shivpuri)", "description": "Grade III–IV rapids on the Ganga", "cost_range": "₹600–1,200"},
        ],
    },
    "shimla": {
        "food": [
            {"name": "Cafe Simla Times", "description": "Heritage cafe with colonial-era decor", "cost_range": "₹200–400"},
            {"name": "Himachali Dham at a local dhaba", "description": "Traditional festive meal with rice, dal and mandyali", "cost_range": "₹150–250"},
        ],
        "hidden_gem": [
            {"name": "Chadwick Falls", "description": "Secluded waterfall inside Shimla forests", "cost_range": "Free"},
            {"name": "Jakhu Temple Trek", "description": "Sunrise hike to the highest peak in Shimla", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "Gaiety Heritage Theatre", "description": "Victorian-era theatre on the Mall Road", "cost_range": "₹100"},
            {"name": "Viceregal Lodge", "description": "British India summer capital now a museum", "cost_range": "₹50"},
        ],
    },
    "agra": {
        "food": [
            {"name": "Petha at Panchhi Sweets", "description": "Iconic translucent pumpkin sweet of Agra", "cost_range": "₹100–200"},
            {"name": "Dalmoth at Bhagwan Das", "description": "Crispy spiced lentil snack famous citywide", "cost_range": "₹100"},
        ],
        "hidden_gem": [
            {"name": "Mehtab Bagh at Sunset", "description": "Garden across the river with Taj Mahal silhouette", "cost_range": "₹200"},
            {"name": "Kinari Bazaar", "description": "Colourful narrow market for zari, saris and bridal wear", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "Fatehpur Sikri", "description": "Mughal ghost city 40 km from Agra", "cost_range": "₹300"},
            {"name": "Agra Fort Sound & Light Show", "description": "Mughal history narrated through lights at night", "cost_range": "₹200"},
        ],
    },
    "assam": {
        "food": [
            {"name": "Khorika at a Local Dhaba", "description": "Charcoal-grilled pork or fish, quintessential Assamese street food", "cost_range": "₹100–200"},
            {"name": "Masor Tenga", "description": "Sour fish curry cooked with tomatoes and lemon, served with red rice", "cost_range": "₹150–300"},
            {"name": "Pitha at Jorhat Market", "description": "Traditional rice cakes filled with coconut and sesame, made fresh in the morning", "cost_range": "₹30–80"},
        ],
        "hidden_gem": [
            {"name": "Majuli Island", "description": "World's largest river island with Vaishnavite monasteries and mask-making villages", "cost_range": "₹200"},
            {"name": "Haflong Blue Hill Lake", "description": "Serene lake in Assam's only hill station, largely off the tourist trail", "cost_range": "Free"},
            {"name": "Sualkuchi Silk Village", "description": "Village of weavers producing the famous Assam Muga and Pat silk on traditional looms", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "Kamakhya Temple", "description": "Shakti pilgrimage site atop Nilachal Hill with sweeping views of Guwahati", "cost_range": "Free"},
            {"name": "Bihu Dance Performance", "description": "Vibrant harvest festival dance — catch live performances at cultural centres", "cost_range": "₹100–200"},
            {"name": "Kaziranga National Park", "description": "UNESCO World Heritage Site, home to two-thirds of the world's one-horned rhinos", "cost_range": "₹500–1,500"},
        ],
        "activity": [
            {"name": "River Safari on the Brahmaputra", "description": "Boat cruise past sandbars and river dolphins at dawn", "cost_range": "₹300–600"},
            {"name": "Tea Garden Walk at Jorhat", "description": "Walking tour through 200-year-old tea estates with a tasting session", "cost_range": "₹200"},
        ],
    },
    "darjeeling": {
        "food": [
            {"name": "Glenary's Bakery", "description": "Colonial-era bakery on the Mall with legendary cinnamon rolls and Darjeeling tea", "cost_range": "₹100–300"},
            {"name": "Momos at Chowrasta", "description": "Steamed pork and vegetable dumplings from roadside stalls on the main square", "cost_range": "₹60–120"},
            {"name": "Nathmull's Tea Room", "description": "Family tea house sampling first-flush Darjeeling oolong since 1931", "cost_range": "₹100"},
        ],
        "hidden_gem": [
            {"name": "Batasia Loop", "description": "Spiral railway loop with a War Memorial and panoramic Kanchenjunga views", "cost_range": "₹50"},
            {"name": "Ghoom Monastery", "description": "Oldest Tibetan Buddhist monastery in Darjeeling, housing a 5m Maitreya statue", "cost_range": "Free"},
            {"name": "Mirik Lake", "description": "Quiet boating lake surrounded by cardamom and orange orchards, 50 km from Darjeeling", "cost_range": "₹100"},
        ],
        "activity": [
            {"name": "Sunrise at Tiger Hill", "description": "4am drive for the famous Everest and Kanchenjunga sunrise above the clouds", "cost_range": "₹200"},
            {"name": "Toy Train Ride (DHR)", "description": "UNESCO-listed narrow-gauge steam railway through tea gardens and mountain curves", "cost_range": "₹250–1,200"},
        ],
    },
    "varanasi": {
        "food": [
            {"name": "Kashi Chaat Bhandar", "description": "Famous for tamatar chaat and aloo tikki — a Varanasi street food institution", "cost_range": "₹50–100"},
            {"name": "Blue Lassi Shop", "description": "80-year-old clay-pot lassi shop near Vishwanath Gali with 60+ flavours", "cost_range": "₹60"},
            {"name": "Malaiyo at Godowlia", "description": "Cloud-light saffron-cream dessert only made in Varanasi winters", "cost_range": "₹30"},
        ],
        "hidden_gem": [
            {"name": "Nag Kuan Mosque Lane", "description": "Ancient neighbourhood where Hindu and Muslim artisans weave Banarasi silk side by side", "cost_range": "Free"},
            {"name": "Ramnagar Fort", "description": "18th-century Mughal-style fort across the Ganga, home to a vintage car museum", "cost_range": "₹100"},
            {"name": "Tulsi Manas Temple", "description": "White marble temple built on the site where Tulsidas composed the Ramcharitmanas", "cost_range": "Free"},
        ],
        "culture": [
            {"name": "Ganga Aarti at Dashashwamedh Ghat", "description": "Nightly fire ritual with synchronized priests — arrive early for a good spot", "cost_range": "Free"},
            {"name": "Dawn Boat Ride on the Ganga", "description": "Early morning row past the burning ghats and bathing pilgrims", "cost_range": "₹200–400"},
            {"name": "Sarnath", "description": "Site of Buddha's first sermon with a 3rd-century Ashoka Pillar and Dhamek Stupa", "cost_range": "₹100"},
        ],
    },
}

INTEREST_TO_TYPE = {
    "food": "food", "foodie": "food", "culinary": "food",
    "culture": "culture", "heritage": "culture", "historical": "culture",
    "adventure": "activity", "trek": "activity", "sports": "activity",
    "nature": "hidden_gem", "mountains": "hidden_gem", "beaches": "hidden_gem",
}


async def local_experience_agent(state: TravelState) -> TravelState:
    destination = state.get("destination") or ""
    interests = state.get("interests") or []

    if not destination:
        state["errors"].append("No destination specified for local experiences")
        state["local_experiences"] = []
        return state

    dest_key = destination.split(",")[0].strip().lower()
    dest_data = EXPERIENCES_DB.get(dest_key, {})

    if not dest_data:
        dest_data = {
            "food": [{"name": "Local Restaurants", "description": "Explore authentic local cuisine", "cost_range": "₹200–400"}],
            "hidden_gem": [{"name": "Hidden Local Spots", "description": "Ask locals for their favourite spots", "cost_range": "Free"}],
            "culture": [{"name": "Cultural Attractions", "description": "Visit historic and cultural sites", "cost_range": "Varies"}],
        }

    result = []
    seen = set()

    for interest in interests:
        exp_type = INTEREST_TO_TYPE.get(interest.lower())
        if exp_type and exp_type in dest_data:
            for exp in dest_data[exp_type]:
                if exp["name"] not in seen:
                    seen.add(exp["name"])
                    result.append({
                        "name": exp["name"],
                        "type": exp_type,
                        "description": exp["description"],
                        "estimated_cost": exp.get("cost_range", "Varies"),
                        "why_special": exp.get("why_special", ""),
                    })

    if not result:
        for exp_type, exps in dest_data.items():
            for exp in exps[:2]:
                if exp["name"] not in seen:
                    seen.add(exp["name"])
                    result.append({
                        "name": exp["name"],
                        "type": exp_type,
                        "description": exp["description"],
                        "estimated_cost": exp.get("cost_range", "Varies"),
                        "why_special": "",
                    })

    enriched = [enrich_experience_with_links(exp, destination) for exp in result[:8]]
    state["local_experiences"] = enriched
    return state
