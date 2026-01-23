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
            "test_key", 
            "", 
            "", 
            "", 
            "9882",
            "0", 
            "90", 
            "180", 
            "8"
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

if __name__ == '__main__':
    unittest.main()