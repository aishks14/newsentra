import requests
from config.settings import GNEWS_API_KEY

def _clean(art: dict) -> dict | None:
    """Normalize a raw article dict. Returns None for junk entries."""
    title = (art.get("title") or "").strip()
    desc  = (art.get("description") or art.get("content") or "").strip()
    url   = (art.get("url") or "").strip()
    if not title or not desc or "[Removed]" in title or not url:
        return None
    return {
        "title":       title[:200],
        "description": desc[:600],
        "url":         url,
        "source":      art.get("source_name") or art.get("source", {}).get("name", "Unknown"),
        "published":   (art.get("publishedAt") or art.get("published_at") or
                        art.get("pubDate") or "")[:10],
        "image":       art.get("urlToImage") or art.get("image") or "",
    }

def fetch_gnews(
    query: str,
    lang_code: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not GNEWS_API_KEY:
        return []

    kw = query or "world news"
    url = "https://gnews.io/api/v4/search"
    params = {
        "q":        kw,
        "lang":     lang_code,
        "from":     f"{from_date}T00:00:00Z",
        "to":       f"{to_date}T23:59:59Z",
        "max":      min(max_articles, 10),
        "apikey":   GNEWS_API_KEY,
        "sortby":   "relevance",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        raw  = data.get("articles", [])
        cleaned = []
        for a in raw:
            src = a.get("source", {}).get("name", "GNews")
            cleaned.append(_clean({**a, "source_name": src}))
        return [r for r in cleaned if r]
    except Exception as e:
        print(f"[GNews] Error: {e}")
        return []