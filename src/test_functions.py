import unittest

from textnode import TextType, TextNode
from text_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes
from block_functions import markdown_to_blocks, block_to_block_type, Blocktype, markdown_to_html_code


class function_testings(unittest.TestCase):
    def test_bold_split(self):
        nodes_list = []
        node = TextNode("This is a *bold* text test",TextType.TEXT)
        nodes_list.append(node)
        result = split_nodes_delimiter(nodes_list,"*",TextType.BOLD)
        self.assertEqual(result,[
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text test", TextType.TEXT)
        ])

    def test_wrong_split(self):
        nodes_list = []
        node = TextNode("This is a *bold text test",TextType.TEXT)
        nodes_list.append(node)
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes_list,"*",TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second image", "https://i.imgur.com/3elNhQu.png")], matches)

    def test_markdown_extract_link_only(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.com/second)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://example.com/second"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph
    
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
    
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), Blocktype.HEADING)

    def test_code(self):
        block = "```this is COOOODE```"
        self.assertEqual(block_to_block_type(block), Blocktype.CODE)

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), Blocktype.QUOTE)

    def test_ordered_list(self):
        block = "1. This is an ordered list"
        self.assertEqual(block_to_block_type(block), Blocktype.ORDERED_LIST)

    def test_unordered_list(self):
        block = "- This is an unordered list"
        self.assertEqual(block_to_block_type(block), Blocktype.UNORDERED_LIST)

    def test_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), Blocktype.PARAGRAPH)

    def test_multilist(self):
        block = "- This is an unordered list\n- with multiple items 1. testing no ordered list appearance"
        self.assertEqual(block_to_block_type(block), Blocktype.UNORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_code(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_code(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        