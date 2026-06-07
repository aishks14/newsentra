from functools import lru_cache


@lru_cache(maxsize=100)
def cached_key(
    query,
    from_date,
    to_date,
    language
):
    return (
        query,
        from_date,
        to_date,
        language
    )