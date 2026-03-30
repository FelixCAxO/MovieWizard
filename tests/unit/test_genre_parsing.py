import unittest
from src.constants.tmdb import GENRES

def parse_genre_input(user_input):
    if not user_input:
        return ""
    
    parts = [p.strip() for p in user_input.replace("+", ",").split(",")]
    ids = []
    for part in parts:
        if part in GENRES:
            ids.append(str(GENRES[part]))
        elif part.isdigit():
            ids.append(part)
    
    return ",".join(ids)

class TestGenreParsing(unittest.TestCase):
    def test_single_genre(self):
        self.assertEqual(parse_genre_input("Action"), "28")
    
    def test_combined_genre_plus(self):
        # Romance is 10749, Comedy is 35
        self.assertEqual(parse_genre_input("Romance + Comedy"), "10749,35")
    
    def test_combined_genre_comma(self):
        self.assertEqual(parse_genre_input("Action, Drama"), "28,18")
    
    def test_empty_input(self):
        self.assertEqual(parse_genre_input(""), "")
    
    def test_invalid_genre(self):
        self.assertEqual(parse_genre_input("Unknown"), "")
    
    def test_mixed_valid_invalid(self):
        self.assertEqual(parse_genre_input("Action + Unknown"), "28")

if __name__ == "__main__":
    unittest.main()
