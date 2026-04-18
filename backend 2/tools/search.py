import os
import httpx
from typing import Optional


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
JINA_BASE_URL = "https://r.jina.ai"


def serper_search(query: str, max_results: int = 5) -> list[dict]:
    if not SERPER_API_KEY:
        return [{"error": "SERPER_API_KEY not configured"}]
    
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": max_results,
    }
    headers = {
        "X-API-Key": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("organic", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]


async def aserper_search(query: str, max_results: int = 5) -> list[dict]:
    if not SERPER_API_KEY:
        return [{"error": "SERPER_API_KEY not configured"}]
    
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": max_results,
    }
    headers = {
        "X-API-Key": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("organic", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]


def serper_image_search(query: str, max_results: int = 5) -> list[dict]:
    if not SERPER_API_KEY:
        return [{"error": "SERPER_API_KEY not configured"}]
    
    url = "https://google.serper.dev/images"
    payload = {
        "q": query,
        "num": max_results,
    }
    headers = {
        "X-API-Key": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("images", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("imageUrl", ""),
                    "thumbnail": item.get("thumbnailUrl", ""),
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]


def fetch_page(url: str) -> dict:
    headers = {
        "X-Engine": "cf-browser-rendering",
        "X-Keep-Img-Data-Url": "true",
        "X-Token-Budget": "20000",
        "X-With-Generated-Alt": "true",
        "X-With-Images-Summary": "all",
        "X-With-Links-Summary": "all",
        "Accept": "application/json"
    }
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"
    
    fetch_url = f"{JINA_BASE_URL}/{url}"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(fetch_url, headers=headers)
            response.raise_for_status()
            return {
                "url": url,
                "content": response.text,
                "status": "success"
            }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "status": "error"
        }


async def afetch_page(url: str) -> dict:
    headers = {
        "X-Engine": "cf-browser-rendering",
        "X-Keep-Img-Data-Url": "true",
        "X-Token-Budget": "20000",
        "X-With-Generated-Alt": "true",
        "X-With-Images-Summary": "all",
        "X-With-Links-Summary": "all",
        "Accept": "application/json"
    }
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"
    
    fetch_url = f"{JINA_BASE_URL}/{url}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(fetch_url, headers=headers)
            response.raise_for_status()
            return {
                "url": url,
                "content": response.text,
                "status": "success"
            }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "status": "error"
        }


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
        results = serper_search(query, max_results=3)
        enriched["web_insights"].extend(results)
    
    return enriched
