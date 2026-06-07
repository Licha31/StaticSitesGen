from unittest import TestCase
from page_gen import extract_title

class test_page_gen(TestCase):
    
    def test_extract_title(self):
        markdown = "# Hello\n"
        self.assertEqual(extract_title(markdown), "Hello")

