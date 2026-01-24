import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import smart_filter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smart_filter

class TestSmartFilterV2(unittest.TestCase):

    @patch('builtins.input')
    @patch('smart_filter.requests.get')
    @patch('smart_filter.sys.stdout')
    def test_new_features_inputs_and_url_construction(self, mock_stdout, mock_get, mock_input):
        # We need to mock all inputs in sequence.
        # Current inputs:
        # 1. API Key
        # 2. Genre (Include)
        # 3. Country
        # 4. Language
        # 5. Keyword
        # 6. Min Votes
        # 7. Min Runtime
        # 8. Max Runtime
        # 9. Provider
        
        # NEW EXPECTED inputs based on requirements:
        # - Cast (Person ID)
        # - Exclude Genre
        # - Watch Region
        # - Start Year
        # - End Year
        # - Sort Order (Shuffle?)
        
        # Let's assume we append them or integrate them. 
        # I will refactor the script to ask for these.
        
        inputs = [
            "test_key",       # API Key
            "",               # Genre Include
            "27",             # Genre Exclude (Horror) - NEW
            "287",            # Cast ID (Brad Pitt) - NEW
            "",               # Country
            "",               # Language
            "",               # Keyword
            "100",            # Min Votes
            "US",             # Watch Region - NEW (was hardcoded)
            "",               # Min Runtime
            "",               # Max Runtime
            "",               # Provider
            "2020",           # Start Year - NEW (was hardcoded 1900)
            "2022",           # End Year - NEW (was hardcoded 2026)
            "shuffle"         # Sort order - NEW
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
        
        # Check NEW parameters
        self.assertIn("without_genres=27", args)
        self.assertIn("with_cast=287", args)
        self.assertIn("watch_region=US", args)
        
        # Check if Start/End year logic works (The first call should be for 2020)
        self.assertIn("primary_release_year=2020", args)
        
        # Check last call
        last_args = mock_get.call_args_list[-1][0][0]
        self.assertIn("primary_release_year=2022", last_args)

if __name__ == '__main__':
    unittest.main()
