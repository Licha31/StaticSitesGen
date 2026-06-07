import unittest

from htmlnode import LeafNode

class test_LeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_LeafNode_eq(self):
        node = LeafNode("p", "Trying test with no help!")
        node2 = LeafNode("p", "Trying test with no help!")
        self.assertEqual(node.to_html(), node2.to_html())
        
    def test_LeafNode_dif(self):
        node = LeafNode("p2", "This is a node")
        node2 = LeafNode("p3", "This is a different node")
        self.assertNotEqual(node.to_html(),node2.to_html())
    
