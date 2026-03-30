from src.constants.tmdb import GENRES

def parse_genre_input(user_input):
    """
    Parses a string of genre names (e.g., 'Action + Drama' or 'Action, Drama')
    into a comma-separated list of TMDB genre IDs.
    """
    if not user_input:
        return ""
    
    # Split by + or , and strip whitespace
    parts = [p.strip() for p in user_input.replace("+", ",").split(",")]
    ids = []
    for part in parts:
        # Check if it's a known genre name (case-sensitive as per GENRES keys)
        if part in GENRES:
            ids.append(str(GENRES[part]))
        # Also allow raw IDs
        elif part.isdigit():
            ids.append(part)
    
    return ",".join(ids)
