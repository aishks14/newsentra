from news.newsapi_client import fetch_newsapi
from news.gnews_client import fetch_gnews
from news.newsdata_client import fetch_newsdata
from news.guardian_client import fetch_guardian
from datetime import date, datetime


def fetch_all_news(
    query: str,
    lang_label: str,
    lang_code: str,
    gnews_lang: str,
    nd_lang: str,
    category_label: str,
    from_date: date,
    to_date: date,
    max_articles: int = 10,
    sort_by: str = "relevancy",
) -> tuple[list[dict], dict]:
    """
    Fetch from all 4 APIs, merge, deduplicate, return articles + source stats.
    Returns: (articles_list, source_counts_dict)
    """
    fd = from_date.strftime("%Y-%m-%d")
    td = to_date.strftime("%Y-%m-%d")

    # Fetch from each source
    newsapi_arts  = fetch_newsapi(query, lang_code, category_label, fd, td, max_articles, sort_by)
    gnews_arts    = fetch_gnews(query, gnews_lang, fd, td, max_articles)
    guardian_arts = fetch_guardian(query, fd, td, max_articles)
    newsdata_arts = fetch_newsdata(query, nd_lang, fd, td, max_articles)

    source_counts = {
        "NewsAPI":      len(newsapi_arts),
        "GNews":        len(gnews_arts),
        "The Guardian": len(guardian_arts),
        "NewsData.io":  len(newsdata_arts),
    }

    # Merge and deduplicate by URL
    all_arts: list[dict] = []
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()

    for art in newsapi_arts + gnews_arts + guardian_arts + newsdata_arts:
        url   = art["url"]
        title = art["title"].lower()[:80]
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        all_arts.append(art)

    return all_arts, source_counts