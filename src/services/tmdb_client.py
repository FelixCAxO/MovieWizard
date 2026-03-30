import requests
import time
import sys
from src.domain.filters import build_params

def fetch_all(api_key, filters):
    """Iterate year-by-year, paginating each, and collect all movies."""

    all_movies = []
    start = filters.get("start_year", 1900)
    end = filters.get("end_year", 2026)

    print(f"\nStarting Deep Search from {start} to {end}...")

    # Using a Session for connection reuse
    session = requests.Session()
    base_url = "https://api.themoviedb.org/3/discover/movie"

    for year in range(start, end + 1):
        page = 1
        total_pages = 1
        year_count = 0

        sys.stdout.write(f"\nScanning Year {year}...")

        while page <= total_pages:
            params = build_params(filters, year, page)
            params["api_key"] = api_key

            max_retries = 5
            retry_count = 0
            res = None
            
            while retry_count < max_retries:
                try:
                    res = session.get(base_url, params=params, timeout=(5, 20))

                    if res.status_code == 429:
                        retry_count += 1
                        retry_after = int(res.headers.get("Retry-After", 2 ** retry_count))
                        time.sleep(retry_after)
                        continue
                    
                    res.raise_for_status()
                    break # Success, break retry loop

                except (requests.exceptions.RequestException, Exception) as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f" Error: {e}")
                        return all_movies
                    time.sleep(2 ** retry_count)
            
            if not res or res.status_code != 200:
                break # Exit page loop if we failed after max retries

            data = res.json()
            results = data.get("results", [])
            total_pages = min(data.get("total_pages", 1), 500)

            if not results:
                break

            for m in results:
                if not filters.get("include_adult", False) and m.get("adult"):
                    continue

                all_movies.append({
                    "id": m["id"],
                    "title": m["title"],
                    "year": year,
                    "rating": m.get("vote_average"),
                    "popularity": m.get("popularity"),
                    "vote_count": m.get("vote_count"),
                    "poster": m.get("poster_path"),
                    "overview": m.get("overview"),
                })
                year_count += 1

            sys.stdout.write(
                f"\rYear {year}: Found {year_count} movies "
                f"(Total: {len(all_movies)})"
            )
            sys.stdout.flush()

            page += 1

    return all_movies
