import json
import os
import sys
import random

# Ensure project root is in path if run directly
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.constants.tmdb import GENRES, CERTIFICATIONS
from src.services.tmdb_client import fetch_all

def get_user_input(prompt, default=None):
    if default is not None:
        user_in = input(f"{prompt} [{default}]: ").strip()
        return user_in if user_in else default
    return input(f"{prompt}: ").strip()


def collect_filters():
    """Gather all filter inputs from the user. Returns a dict."""

    print("\nAvailable Genres:", ", ".join(GENRES.keys()))
    genre_name = get_user_input("Include Genre (or leave empty)", "")
    genre_id = GENRES.get(genre_name) if genre_name in GENRES else ""

    exclude_genre_name = get_user_input("Exclude Genre (or leave empty)", "")
    exclude_genre_id = GENRES.get(exclude_genre_name) if exclude_genre_name in GENRES else ""
    if not exclude_genre_id and exclude_genre_name.isdigit():
        exclude_genre_id = exclude_genre_name

    cast_id = get_user_input("Cast Member ID (e.g. 287 for Brad Pitt) [Optional]", "")

    country = get_user_input("Origin Country Code (e.g., US, JP, FR) [Optional]", "")
    language = get_user_input("Language Code (e.g., en, ja, fr) [Optional]", "")
    keyword_id = get_user_input("Keyword ID (e.g., 9882 for Time Travel) [Optional]", "")
    exclude_keyword_id = get_user_input("Exclude Keyword ID [Optional]", "")
    min_votes = int(get_user_input("Minimum Votes (quality control)", "0"))
    watch_region = get_user_input("Watch Region (e.g. US, SE, GB)", "US")

    # Advanced Filters
    print("\n--- Advanced Filters ---")
    min_runtime = get_user_input("Min Runtime (minutes) [Optional]", "")
    max_runtime = get_user_input("Max Runtime (minutes) [Optional]", "")

    print("Providers: 8=Netflix, 337=Disney+, 9=Amazon Prime, 15=Hulu, "
          "1899=HBO Max, 350=Apple TV+, 531=Paramount+, 386=Peacock, 11=Mubi")
    provider_id = get_user_input("Provider ID [Optional]", "")

    crew_id = get_user_input("Crew/Director ID (e.g. 525 for Spielberg) [Optional]", "")
    company_id = get_user_input("Production Company ID (e.g. 420 for Marvel) [Optional]", "")

    # Certification
    print(f"\nCertifications: {', '.join(CERTIFICATIONS)}")
    cert_country = get_user_input("Certification Country (e.g. US) [Optional]", "")
    certification = get_user_input("Certification (e.g. PG-13) [Optional]", "") if cert_country else ""

    max_score = get_user_input("Max Score (e.g. 7.5 for hidden gems) [Optional]", "")

    start_year_input = get_user_input("Start Year", "1900")
    end_year_input = get_user_input("End Year", "2026")

    sort_order = get_user_input(
        "Sort Order (popularity.desc, vote_average.desc, revenue.desc, shuffle)",
        "popularity.desc"
    )

    return {
        "genre_id": genre_id,
        "exclude_genre_id": exclude_genre_id,
        "cast_id": cast_id,
        "country": country,
        "language": language,
        "keyword_id": keyword_id,
        "exclude_keyword_id": exclude_keyword_id,
        "min_votes": min_votes,
        "watch_region": watch_region,
        "min_runtime": min_runtime,
        "max_runtime": max_runtime,
        "provider_id": provider_id,
        "crew_id": crew_id,
        "company_id": company_id,
        "cert_country": cert_country,
        "certification": certification,
        "max_score": max_score,
        "start_year": int(start_year_input),
        "end_year": int(end_year_input),
        "sort_order": sort_order,
        "include_adult": False,
    }


def save_results(movies, sort_order):
    """Optionally shuffle, then save to JSON."""

    print("\n\nSaving database...")

    if sort_order == "shuffle":
        print("Shuffling results...")
        random.shuffle(movies)

    filename = f"deep_database_{len(movies)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)

    print(f"DONE! Saved {len(movies)} movies to '{filename}'")


def main():
    print("--- MovieWizard (Deep Search) ---")

    # 1. API Key Setup
    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        print("Hint: Get your free API key at https://www.themoviedb.org/settings/api")
        api_key = get_user_input("Enter TMDb API Key")

    if not api_key:
        print("Error: API Key is required.")
        return

    # 2. Collect all filters
    filters = collect_filters()

    # 3. Fetch movies
    all_movies = fetch_all(api_key, filters)

    # 4. Save results
    save_results(all_movies, filters["sort_order"])


if __name__ == "__main__":
    main()
