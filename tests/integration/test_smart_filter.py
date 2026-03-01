
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import urllib.parse

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app import cli

def extract_url(mock_get, call_index=0):
    args, kwargs = mock_get.call_args_list[call_index]
    url = args[0]
    if 'params' in kwargs:
        param_str = urllib.parse.urlencode(kwargs['params'])
        url += "?" + param_str
    return url

class TestSmartFilterIntegration(unittest.TestCase):

    @patch("builtins.input")
    @patch("requests.Session.get")
    @patch("sys.stdout")
    def test_get_movies_iterates_all_years(self, _stdout, mock_get, mock_input):
        mock_input.side_effect = [
            "test_key", "", "", "", "", "", "9882", "", "0", "US", "90", "180", "8", "", "", "", "", "2020", "2022", "popularity.desc"
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "total_pages": 1}
        mock_get.return_value = mock_response

        with patch("builtins.open", new_callable=MagicMock):
            cli.main()

        self.assertEqual(mock_get.call_count, 3) # 2020, 2021, 2022

if __name__ == "__main__":
    unittest.main()
