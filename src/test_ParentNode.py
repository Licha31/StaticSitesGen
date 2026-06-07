from multiprocessing import Value
from multiprocessing.process import parent_process
import unittest

from htmlnode import ParentNode
from htmlnode import LeafNode

class test_ParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_tag_None(self):
        parent_Node = ParentNode(None, "this is a test for None tag")
        with self.assertRaises(ValueError):
            parent_Node.to_html()

    def test_children_empty(self):
        parent_Node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            parent_Node.to_html()