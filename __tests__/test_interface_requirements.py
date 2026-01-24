import unittest
import os
import re

class TestInterfaceContent(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'interface.html')
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def test_cast_input_exists(self):
        # Search for an input or section related to Cast/People
        # We expect an ID or label for "Cast" or "Person"
        self.assertTrue(re.search(r'id=["\"]cast-input["\"]', self.content) or re.search(r'Cast', self.content), 
                        "Interface must have a Cast/Person search input")

    def test_exclude_genre_logic(self):
        # Look for logic handling exclusion or UI for it
        self.assertTrue(re.search(r'without_genres', self.content) or re.search(r'exclude', self.content, re.IGNORECASE),
                        "Interface must handle genre exclusion (without_genres)")

    def test_watch_region_selector(self):
        # Look for a region selector
        self.assertTrue(re.search(r'watch_region', self.content), 
                        "Interface must include watch_region parameter in API call")
        self.assertTrue(re.search(r'<select.*id=["\"]region-select["\"]', self.content) or re.search(r'Region', self.content),
                        "Interface must have a Region selector in UI")

    def test_vote_count_slider(self):
        # Look for vote count slider
        self.assertTrue(re.search(r'vote_count.gte', self.content), 
                        "Interface must include vote_count.gte parameter")
        self.assertTrue(re.search(r'min-votes', self.content) or re.search(r'Vote Count', self.content),
                        "Interface must have UI for Minimum Votes")

    def test_shuffle_sort(self):
        # Look for shuffle option
        self.assertTrue(re.search(r'shuffle', self.content, re.IGNORECASE), 
                        "Interface must include a Shuffle/Random sort option")

    def test_date_range_inputs(self):
        # Look for date inputs beyond just "Era"
        self.assertTrue(re.search(r'primary_release_date.gte', self.content), 
                        "Interface must support primary_release_date.gte")
        self.assertTrue(re.search(r'primary_release_date.lte', self.content), 
                        "Interface must support primary_release_date.lte")

if __name__ == '__main__':
    unittest.main()