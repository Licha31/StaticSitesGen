from shlex import split

from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            if delimiter in text:
                parts = text.split(delimiter)
                if len(parts) % 2 == 0:
                    raise Exception("Invalid Markdown syntax")
                else:
                    for i, part in enumerate(parts):
                        if i % 2 == 0 and part != "":
                            new_nodes.append(TextNode(part,TextType.TEXT))
                        elif i % 2 != 0 and part != "":
                            new_nodes.append(TextNode(part,text_type))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)
        if extracted:
            text = node.text
            for image in extracted:
                parts = text.split(f"![{image[0]}]({image[1]})", 1)
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text = parts[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted = extract_markdown_links(node.text)
        if extracted:
            text = node.text
            for link in extracted:
                parts = text.split(f"[{link[0]}]({link[1]})", 1)
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                text = parts[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n", markdown)
    return [block.strip() for block in blocks if block.strip()]

