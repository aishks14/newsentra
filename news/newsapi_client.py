from sre_constants import CATEGORY

from newsapi import NewsApiClient
from config.categories import CATEGORIES, CATEGORY_KEYWORDS
from config.language_config import NEWSAPI_SUPPORTED
from config.settings import NEWS_API_KEY
from news.gnews_client import _clean

client = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_newsapi(
    query: str,
    lang_code: str,
    category_label: str,
    from_date: str,
    to_date: str,
    max_articles: int,
    sort_by: str = "relevancy",
) -> list[dict]:
    if not NEWS_API_KEY:
        return []

    lang = lang_code if lang_code in NEWSAPI_SUPPORTED else "en"
    cat  = CATEGORIES.get(category_label, "")
    kw   = CATEGORY_KEYWORDS.get(category_label, "")
    full_query = f"{query} {kw}".strip() if kw else query

    try:
        client = NewsApiClient(api_key=NEWS_API_KEY)

        if cat and not full_query:
            # Category browse (top-headlines)
            resp = client.get_top_headlines(
                category=cat, language=lang, page_size=max_articles
            )
        elif cat:
            resp = client.get_everything(
                q=full_query, language=lang,
                from_param=from_date, to=to_date,
                sort_by=sort_by, page_size=max_articles,
            )
        else:
            resp = client.get_everything(
                q=full_query, language=lang,
                from_param=from_date, to=to_date,
                sort_by=sort_by, page_size=max_articles,
            )

        raw = resp.get("articles", [])
        results = [_clean(a) for a in raw]
        return [r for r in results if r]
    except Exception as e:
        print(f"[NewsAPI] Error: {e}")
        return []