
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app import cli

def make_empty_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {"results": [], "total_pages": 1}
    return mock

def extract_url(mock_get, call_index=0):
    args, kwargs = mock_get.call_args_list[call_index]
    url = args[0]
    if 'params' in kwargs:
        import urllib.parse
        param_str = urllib.parse.urlencode(kwargs['params'])
        url += "?" + param_str
    return url

def base_inputs_no_cert(**overrides):
    defaults = {
        "api_key": "test_key", "genre_include": "", "genre_exclude": "", "cast_id": "",
        "country": "", "language": "", "keyword_id": "", "exclude_keyword_id": "",
        "min_votes": "0", "watch_region": "US", "min_runtime": "", "max_runtime": "",
        "provider_id": "", "crew_id": "", "company_id": "", "cert_country": "",
        "max_score": "", "start_year": "2024", "end_year": "2024", "sort_order": "popularity.desc",
    }
    defaults.update(overrides)
    return [
        defaults["api_key"], defaults["genre_include"], defaults["genre_exclude"], defaults["cast_id"],
        defaults["country"], defaults["language"], defaults["keyword_id"], defaults["exclude_keyword_id"],
        defaults["min_votes"], defaults["watch_region"], defaults["min_runtime"], defaults["max_runtime"],
        defaults["provider_id"], defaults["crew_id"], defaults["company_id"], defaults["cert_country"],
        defaults["max_score"], defaults["start_year"], defaults["end_year"], defaults["sort_order"],
    ]

class TestNewFilters(unittest.TestCase):

    @patch("builtins.input")
    @patch("requests.Session.get")
    @patch("sys.stdout")
    def test_all_new_filters_in_single_url(self, _stdout, mock_get, mock_input):
        mock_input.side_effect = base_inputs_no_cert(
            genre_include="Action", crew_id="525", company_id="420", max_score="8.0"
        )
        mock_get.return_value = make_empty_response()

        with patch("builtins.open", new_callable=MagicMock):
            cli.main()

        url = extract_url(mock_get)
        self.assertIn("with_genres=28", url)
        self.assertIn("with_crew=525", url)
        self.assertIn("with_companies=420", url)
        self.assertIn("vote_average.lte=8.0", url)

if __name__ == "__main__":
    unittest.main()
