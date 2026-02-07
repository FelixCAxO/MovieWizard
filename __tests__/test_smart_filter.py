import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import smart_filter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smart_filter

class TestSmartFilter(unittest.TestCase):

    @patch('builtins.input')
    @patch('smart_filter.requests.get')
    @patch('smart_filter.sys.stdout')
    def test_get_movies_iterates_all_years_with_advanced_filters(self, mock_stdout, mock_get, mock_input):
        # Setup mocks
        # Inputs: 
        # 1. API Key: "test_key"
        # 2. Genre: "" (All)
        # 3. Country: ""
        # 4. Language: ""
        # 5. Keyword: "9882"
        # 6. Min Votes: "0"
        # 7. Min Runtime: "90"
        # 8. Max Runtime: "180"
        # 9. Provider: "8" (Netflix)
        
        mock_input.side_effect = [
            "test_key",  # API Key
            "",          # Genre Include
            "",          # Genre Exclude
            "",          # Cast ID
            "",          # Country
            "",          # Language
            "9882",      # Keyword
            "0",         # Min Votes
            "US",        # Watch Region
            "90",        # Min Runtime
            "180",       # Max Runtime
            "8",         # Provider
            "1900",      # Start Year
            "2026",      # End Year
            "popularity.desc" # Sort Order
        ]
        
        # API Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [],
            "total_pages": 1
        }
        mock_get.return_value = mock_response

        # Run the function
        with patch('builtins.open', new_callable=MagicMock):
            smart_filter.get_movies()

        # Verification
        # 1. Check Year Loop
        expected_calls = 2026 - 1900 + 1
        self.assertEqual(mock_get.call_count, expected_calls, f"Expected {expected_calls} API calls (one per year)")
        
        # 2. Check URL Parameters for new filters
        first_call_args = mock_get.call_args_list[0][0][0]
        
        self.assertIn("with_runtime.gte=90", first_call_args)
        self.assertIn("with_runtime.lte=180", first_call_args)
        self.assertIn("with_keywords=9882", first_call_args)
        self.assertIn("with_watch_providers=8", first_call_args)
        self.assertIn("watch_region=US", first_call_args)

    @patch('builtins.input')
    @patch('smart_filter.requests.get')
    @patch('smart_filter.sys.stdout')
    def test_new_features_inputs_and_url_construction(self, mock_stdout, mock_get, mock_input):
        inputs = [
            "test_key",       # API Key
            "",               # Genre Include
            "27",             # Genre Exclude (Horror)
            "287",            # Cast ID (Brad Pitt)
            "",               # Country
            "",               # Language
            "",               # Keyword
            "100",            # Min Votes
            "US",             # Watch Region
            "",               # Min Runtime
            "",               # Max Runtime
            "",               # Provider
            "2020",           # Start Year
            "2022",           # End Year
            "shuffle"         # Sort order
        ]
        
        mock_input.side_effect = inputs
        
        # Mock Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": 1, "title": "Movie A", "vote_average": 8.0, "release_date": "2020-01-01"},
                {"id": 2, "title": "Movie B", "vote_average": 7.0, "release_date": "2021-01-01"}
            ],
            "total_pages": 1
        }
        mock_get.return_value = mock_response

        # Run
        with patch('builtins.open', new_callable=MagicMock):
            smart_filter.get_movies()
            
        # Verify URL construction
        # We expect calls for years 2020, 2021, 2022 (3 years)
        self.assertEqual(mock_get.call_count, 3)
        
        args = mock_get.call_args_list[0][0][0]
        
        # Check parameters
        self.assertIn("without_genres=27", args)
        self.assertIn("with_cast=287", args)
        self.assertIn("watch_region=US", args)
        self.assertIn("primary_release_year=2020", args)
        
        # Check last call
        last_args = mock_get.call_args_list[-1][0][0]
        self.assertIn("primary_release_year=2022", last_args)

if __name__ == '__main__':
    unittest.main()