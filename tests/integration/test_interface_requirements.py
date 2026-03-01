
import unittest
import os
import re

class TestInterfaceRequirements(unittest.TestCase):
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

    def test_basic_elements(self):
        self.assertIn('id="cast-input"', self.content)
        self.assertIn('without_genres', self.content)
        self.assertIn('watch_region', self.content)

if __name__ == "__main__":
    unittest.main()
