import requests

from config.settings import (
    GUARDIAN_API_KEY
)
from news.gnews_client import _clean

print(
    "GUARDIAN KEY LOADED:",
    bool(GUARDIAN_API_KEY)
)

def fetch_guardian(
    query: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not GUARDIAN_API_KEY:
        return []

    url = "https://content.guardianapis.com/search"
    params = {
        "q":            query or "world",
        "from-date":    from_date,
        "to-date":      to_date,
        "page-size":    min(max_articles, 50),
        "api-key":      GUARDIAN_API_KEY,
        "show-fields":  "trailText,thumbnail",
        "order-by":     "relevance",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        items = data.get("response", {}).get("results", [])
        results = []
        for a in items:
            fields = a.get("fields", {})
            cleaned = _clean({
                "title":       a.get("webTitle", ""),
                "description": fields.get("trailText", a.get("webTitle", "")),
                "url":         a.get("webUrl", ""),
                "source_name": "The Guardian",
                "publishedAt": a.get("webPublicationDate", "")[:10],
                "urlToImage":  fields.get("thumbnail", ""),
            })
            if cleaned:
                results.append(cleaned)
        return results
    except Exception as e:
        print(f"[Guardian] Error: {e}")
        return []