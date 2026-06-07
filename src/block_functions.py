from random import choice
import re
from enum import Enum
from text_functions import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n", markdown)
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return Blocktype.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return Blocktype.CODE
    elif all([line.startswith(">") for line in lines]):
        return Blocktype.QUOTE
    elif all([line.startswith("- ") for line in lines]):
        return Blocktype.UNORDERED_LIST
    elif all([line.startswith(f"{i}. ") for i, line in enumerate(lines, 1)]):
        return Blocktype.ORDERED_LIST
    else:
        return Blocktype.PARAGRAPH

def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children

def markdown_to_html_code(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == Blocktype.HEADING:
            heading_level = len(block.split(" ",1)[0])
            child = ParentNode(f"h{heading_level}", text_to_children(block.split(" ", 1)[1]))
            children.append(child)
        elif block_type == Blocktype.CODE:
            child = ParentNode("pre", [LeafNode("code", block[4:-3])])
            children.append(child)
        elif block_type == Blocktype.QUOTE:
            blockquote = []
            for quote in block.split("\n"):
                blockquote.append(quote.strip("> "))
            children.append(ParentNode("blockquote", text_to_children("\n".join(blockquote))))
        elif block_type == Blocktype.UNORDERED_LIST:
            child = ParentNode("ul", [ParentNode("li", text_to_children(item.strip("- "))) for item in block.split("\n")])
            children.append(child)
        elif block_type == Blocktype.ORDERED_LIST:
            child = ParentNode("ol", [ParentNode("li", text_to_children(item.split(". ")[1])) for item in block.split("\n")])
            children.append(child)
        else:
            child = ParentNode("p", text_to_children(block.replace("\n", " ")))
            children.append(child)
    return ParentNode("div", children)
