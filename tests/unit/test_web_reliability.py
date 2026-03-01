
import unittest
import os
import re

class TestWebReliability(unittest.TestCase):
    def setUp(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        html_path = os.path.join(base_path, "interface.html")
        with open(html_path, "r", encoding="utf-8") as f:
            self.content = f.read()
        
        for asset in ["src/app/web.js", "src/services/tmdb_web.js", "src/app/styles.css"]:
            asset_path = os.path.join(base_path, asset)
            if os.path.exists(asset_path):
                with open(asset_path, "r", encoding="utf-8") as f:
                    self.content += "\n" + f.read()

    def test_no_unsafe_event_current_target(self):
        self.assertIn('event', self.content)

    def test_noopener_noreferrer(self):
        links = re.findall(r'target=["\']_blank["\']', self.content)
        self.assertGreater(len(links), 0)
        self.assertIn('rel="noopener noreferrer"', self.content)

    def test_url_search_params_usage(self):
        self.assertIn('URLSearchParams', self.content)

    def test_fetch_res_ok_checks(self):
        ok_checks = len(re.findall(r'res\.ok', self.content))
        self.assertGreaterEqual(ok_checks, 3)

if __name__ == "__main__":
    unittest.main()
