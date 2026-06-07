import pandas as pd
from textblob import TextBlob


def sentiment_score(text):

    try:

        return round(
            TextBlob(text)
            .sentiment
            .polarity,
            2
        )

    except Exception:

        return 0


def sentiment_label(score):

    if score > 0.1:
        return "Positive"

    elif score < -0.1:
        return "Negative"

    return "Neutral"


def source_statistics(
    articles
):

    stats = {}

    for article in articles:

        source = article.get(
            "source",
            {}
        )

        if isinstance(source, dict):
            source_name = source.get(
                "name",
                "Unknown"
            )
        
        elif isinstance(source, str):
            source_name = source

        else:
            source_name = (
                article.get(
                    "source_name"
                )
                or
                article.get(
                    "source_id"
                )
                or
                "Unknown"
            )

    return pd.DataFrame(
        {
            "Source": stats.keys(),
            "Count": stats.values()
        }
    )


def estimate_reading_time(
    text
):

    words = len(
        text.split()
    )

    return round(
        words / 200,
        1
    )