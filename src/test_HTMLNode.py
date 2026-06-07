import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "https://google.com", None, {"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')
    def test_props_is_None(self):
        node = HTMLNode("a", "https://google.com", None, None)
        self.assertEqual(node.props_to_html(), '')
    def test_props_equal(self):
        node = HTMLNode("a", "https://google.com", None, {"href": "https://google.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')