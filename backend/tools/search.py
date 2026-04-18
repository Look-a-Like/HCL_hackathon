import requests
from typing import Optional


def duckduckgo_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if "Text" in topic and "FirstURL" in topic:
                    results.append({
                        "title": topic.get("Text", "").split(" - ")[0] if " - " in topic.get("Text", "") else topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", "")
                    })
            return results
    except Exception as e:
        return [{"error": str(e)}]
    return []


def enrich_destination_info(destination_name: str, interests: list[str]) -> dict:
    search_queries = [
        f"best things to do in {destination_name}",
        f"{destination_name} local food restaurants",
        f"best time to visit {destination_name}",
    ]
    
    enriched = {
        "destination": destination_name,
        "web_insights": [],
        "local_tips": []
    }
    
    for query in search_queries[:2]:
        results = duckduckgo_search(query, max_results=3)
        enriched["web_insights"].extend(results)
    
    return enriched