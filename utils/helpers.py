from datetime import datetime

def filter_articles_by_date(
    articles,
    from_date,
    to_date
):

    filtered = []

    for article in articles:

        date_str = (
            article.get("publishedAt")
            or article.get("pubDate")
        )

        if not date_str:
            continue

        try:

            article_date = datetime.fromisoformat(
                date_str.replace(
                    "Z",
                    "+00:00"
                )
            ).date()

            if isinstance(
                from_date,
                str
            ):
                from_date = datetime.fromisoformat(
                    from_date
                ).date()

            if isinstance(
                to_date,
                str
            ):
                to_date = datetime.fromisoformat(
                    to_date
                ).date()

            if (
                from_date
                <= article_date
                <= to_date
            ):
                filtered.append(
                    article
                )

        except Exception:
            continue

    return filtered

def filter_relevant_articles(
    articles,
    query
):

    keywords = [

        word.lower()

        for word in query.split()

        if len(word) > 2
    ]

    filtered = []

    for article in articles:

        title = str(
            article.get(
                "title",
                ""
            )
        ).lower()

        description = str(
            article.get(
                "description",
                ""
            )
        ).lower()

        text = (
            title
            + " "
            + description
        )

        matches = 0

        for keyword in keywords:

            if keyword in text:
                matches += 1

        if matches >= len(keywords):

            filtered.append(
                article
            )

    return filtered