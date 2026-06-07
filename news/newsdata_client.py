from plotly import data
import requests
from streamlit.config_util import _clean

from config.settings import (
    NEWSDATA_API_KEY
)


def fetch_newsdata(
    query: str,
    lang_code: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not NEWSDATA_API_KEY:
        return []

    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey":    NEWSDATA_API_KEY,
        "q":         query or "world",
        "language":  lang_code,
        "from_date": from_date,
        "to_date":   to_date,
        "size":      min(max_articles, 10),
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        raw  = data.get("results", [])
        results = []
        for a in raw:
            cleaned = _clean({
                "title":       a.get("title", ""),
                "description": a.get("description") or a.get("content") or "",
                "url":         a.get("link", ""),
                "source_name": a.get("source_id", "NewsData"),
                "publishedAt": (a.get("pubDate") or "")[:10],
                "urlToImage":  a.get("image_url") or "",
            })
            if cleaned:
                results.append(cleaned)
        return results
    except Exception as e:
        print(f"[NewsData] Error: {e}")
        return []