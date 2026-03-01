import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.services import tmdb_client

class TestCliReliability(unittest.TestCase):

    @patch("requests.Session.get")
    def test_fetch_all_uses_timeout(self, mock_get):
        """Verify requests.get is called with a timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "total_pages": 1}
        mock_get.return_value = mock_response

        filters = {"sort_order": "popularity.desc"}
        
        tmdb_client.fetch_all("test_key", filters)
        
        for call in mock_get.call_args_list:
            args, kwargs = call
            self.assertIn("timeout", kwargs)

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_fetch_all_retries_on_429(self, mock_get, mock_sleep):
        """Verify retry logic for 429 status code."""
        mock_429 = MagicMock()
        mock_429.status_code = 429
        
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"results": [], "total_pages": 1}
        
        mock_get.side_effect = [mock_429, mock_429, mock_200]
        
        filters = {"sort_order": "popularity.desc", "start_year": 2024, "end_year": 2024}
        tmdb_client.fetch_all("test_key", filters)
        
        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("requests.Session.get")
    def test_fetch_all_uses_params_dict(self, mock_get):
        """Verify that URL parameters are passed as a dictionary."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "total_pages": 1}
        mock_get.return_value = mock_response

        filters = {
            "sort_order": "popularity.desc",
            "min_votes": 100,
            "genre_id": "28"
        }
        
        tmdb_client.fetch_all("test_key", filters)
        
        for call in mock_get.call_args_list:
            args, kwargs = call
            self.assertIn("params", kwargs)
            params = kwargs["params"]
            self.assertEqual(params.get("api_key"), "test_key")
            self.assertEqual(params.get("with_genres"), "28")

if __name__ == "__main__":
    unittest.main()
