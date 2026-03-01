def build_params(filters, year, page):
    """Construct a TMDb /discover/movie parameter dictionary from the filter dict."""

    api_sort = filters["sort_order"]
    if api_sort == "shuffle":
        api_sort = "popularity.desc"

    params = {
        "sort_by": api_sort,
        "include_adult": str(filters.get('include_adult', False)).lower(),
        "include_video": "false",
        "primary_release_year": year,
        "vote_count.gte": filters.get('min_votes', 0),
        "page": page
    }

    # Genre
    if filters.get("genre_id"):
        params["with_genres"] = filters["genre_id"]
    if filters.get("exclude_genre_id"):
        params["without_genres"] = filters["exclude_genre_id"]

    # People
    if filters.get("cast_id"):
        params["with_cast"] = filters["cast_id"]
    if filters.get("crew_id"):
        params["with_crew"] = filters["crew_id"]

    # Content
    if filters.get("language"):
        params["with_original_language"] = filters["language"]
    if filters.get("country"):
        params["with_origin_country"] = filters["country"]
    if filters.get("keyword_id"):
        params["with_keywords"] = filters["keyword_id"]
    if filters.get("exclude_keyword_id"):
        params["without_keywords"] = filters["exclude_keyword_id"]

    # Runtime
    if filters.get("min_runtime"):
        params["with_runtime.gte"] = filters["min_runtime"]
    if filters.get("max_runtime"):
        params["with_runtime.lte"] = filters["max_runtime"]

    # Provider
    if filters.get("provider_id"):
        params["with_watch_providers"] = filters["provider_id"]

    # Region
    if filters.get("watch_region"):
        params["watch_region"] = filters["watch_region"]

    # Company
    if filters.get("company_id"):
        params["with_companies"] = filters["company_id"]

    # Certification
    if filters.get("cert_country") and filters.get("certification"):
        params["certification_country"] = filters["cert_country"]
        params["certification"] = filters["certification"]

    # Score ceiling
    if filters.get("max_score"):
        params["vote_average.lte"] = filters["max_score"]

    return params
