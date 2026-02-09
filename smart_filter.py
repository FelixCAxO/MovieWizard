import requests
import json
import time
import os
import sys
import random

# --- CONFIGURATION -----------------------------------------
# You can hardcode your key here or input it when running
DEFAULT_API_KEY = "" 

# GENRE MAPPING
GENRES = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
    "Mystery": 9648, "Romance": 10749, "Science Fiction": 878,
    "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37
}

# -----------------------------------------------------------

def get_user_input(prompt, default=None):
    if default:
        user_in = input(f"{prompt} [{default}]: ").strip()
        return user_in if user_in else default
    return input(f"{prompt}: ").strip()

def get_movies():
    print("--- MovieWizard (Deep Search) ---")
    
    # 1. API Key Setup
    api_key = DEFAULT_API_KEY
    if not api_key:
        api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        print("Hint: Get your free API key at https://www.themoviedb.org/settings/api")
        api_key = get_user_input("Enter TMDb API Key")
    
    if not api_key:
        print("Error: API Key is required.")
        return

    # 2. Filter Setup
    print("\nAvailable Genres:", ", ".join(GENRES.keys()))
    genre_name = get_user_input("Include Genre (or leave empty)", "")
    genre_id = GENRES.get(genre_name) if genre_name in GENRES else ""
    
    exclude_genre_name = get_user_input("Exclude Genre (or leave empty)", "")
    exclude_genre_id = GENRES.get(exclude_genre_name) if exclude_genre_name in GENRES else ""
    # Allow raw ID input for testing/advanced users
    if not exclude_genre_id and exclude_genre_name.isdigit():
        exclude_genre_id = exclude_genre_name

    cast_id = get_user_input("Cast Member ID (e.g. 287 for Brad Pitt) [Optional]", "")
    
    country = get_user_input("Origin Country Code (e.g., US, JP, FR) [Optional]", "")
    language = get_user_input("Language Code (e.g., en, ja, fr) [Optional]", "")
    keyword_id = get_user_input("Keyword ID (e.g., 9882 for Time Travel) [Optional]", "")
    min_votes = int(get_user_input("Minimum Votes (quality control)", "0"))
    watch_region = get_user_input("Watch Region (e.g. US, SE, GB)", "US")
    
    # EXCLUDE ADULT CONTENT
    include_adult = False
    
    # 3. Advanced Filters
    print("\n--- Advanced Filters ---")
    min_runtime = get_user_input("Min Runtime (minutes) [Optional]", "")
    max_runtime = get_user_input("Max Runtime (minutes) [Optional]", "")
    
    print("Providers: 8=Netflix, 337=Disney+, 9=Amazon Prime, 15=Hulu, 188=YouTube Premium")
    provider_id = get_user_input("Provider ID [Optional]", "")
    
    start_year_input = get_user_input("Start Year", "1900")
    end_year_input = get_user_input("End Year", "2026")
    
    sort_order = get_user_input("Sort Order (popularity.desc, vote_average.desc, shuffle)", "popularity.desc")

    
    # 3. Main Loop: Iterate by Year
    all_movies = []
    start_year = int(start_year_input)
    end_year = int(end_year_input)
    
    print(f"\nStarting Deep Search from {start_year} to {end_year}...")

    for year in range(start_year, end_year + 1):
        page = 1
        total_pages = 1
        year_movies_count = 0
        
        sys.stdout.write(f"\nScanning Year {year}...")

        while page <= total_pages:
            # Build URL with PRIMARY_RELEASE_YEAR
            # Note: For shuffle, we fetch popularity.desc usually, then shuffle locally, 
            # unless we randomise pages. Here we just fetch and shuffle result at the end.
            api_sort = sort_order if sort_order != "shuffle" else "popularity.desc"
            
            url = (
                   f"https://api.themoviedb.org/3/discover/movie?"
                   f"api_key={api_key}&sort_by={api_sort}"
                   f"&include_adult={str(include_adult).lower()}"
                   f"&include_video=false"
                   f"&primary_release_year={year}" 
                   f"&vote_count.gte={min_votes}&page={page}"
                  )
            
            # Apply Filters
            if genre_id: url += f"&with_genres={genre_id}"
            if exclude_genre_id: url += f"&without_genres={exclude_genre_id}"
            if cast_id: url += f"&with_cast={cast_id}"
            
            if language: url += f"&with_original_language={language}"
            if country:  url += f"&with_origin_country={country}"
            if keyword_id: url += f"&with_keywords={keyword_id}"
            
            if min_runtime: url += f"&with_runtime.gte={min_runtime}"
            if max_runtime: url += f"&with_runtime.lte={max_runtime}"
            
            if provider_id:
                url += f"&with_watch_providers={provider_id}"
            
            # Always append region if set (default US)
            if watch_region:
                url += f"&watch_region={watch_region}"

            try:
                res = requests.get(url)
                
                if res.status_code == 429:
                    time.sleep(1) # Short pause for rate limit
                    continue # Retry same page
                    
                data = res.json()
                results = data.get('results', [])
                
                # Update max pages for THIS YEAR only (capped at 500)
                total_pages = min(data.get('total_pages', 1), 500) 

                if not results:
                    break

                for m in results:
                    # Double check for adult content just in case
                    if not include_adult and m.get('adult'):
                        continue
                        
                    all_movies.append({
                        "id": m['id'],
                        "title": m['title'],
                        "year": year,
                        "rating": m.get('vote_average'),
                        "poster": m.get('poster_path'),
                        "overview": m.get('overview')
                    })
                    year_movies_count += 1

                # Visual Feedback
                sys.stdout.write(
                    f"\rYear {year}: Found {year_movies_count} movies (Total: {len(all_movies)})"
                )
                sys.stdout.flush()
                
                page += 1
                
            except Exception as e:
                print(f" Error: {e}")
                break
                
    # 4. Save Final File
    print("\n\nSaving database...")
    
    if sort_order == "shuffle":
        print("Shuffling results...")
        random.shuffle(all_movies)
        
    filename = f"deep_database_{len(all_movies)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, indent=2, ensure_ascii=False)
    
    print(f"DONE! Saved {len(all_movies)} movies to '{filename}'")

if __name__ == "__main__":
    get_movies()
