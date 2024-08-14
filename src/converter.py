from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from functools import reduce
import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

block_type_header = "header"
block_type_code = "code"
block_type_quote = "quote"
block_type_list = "list"
block_type_ordered_list = "ordered_list"
block_type_unordered_list = "unordered_list"
block_type_paragraph = "paragraph"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    # use regex to get two newlines with any number of spaces between them
    blocks = re.split(r"\n\s*\n", markdown)
    curated_blocks = []
    for block in blocks:
        if block == "":
            continue
        curated_blocks.append(block.strip())
    return curated_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return block_type_header
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if reduce(lambda a, v: a and v.startswith(">"), block.split("\n"), True):
        return block_type_quote
    if reduce(lambda a, v: a and (v.startswith("* ") or v.startswith("- ")), block.split("\n"), True):
        return block_type_unordered_list
    
    is_ordered_list = True
    for i in enumerate(block.split("\n")):
        if not i[1].startswith(f"{i[0]+1}. "):
            is_ordered_list = False
    if is_ordered_list and block.count("\n") > 0:
        return block_type_ordered_list

    return block_type_paragraph

def text_to_html_nodes(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = ParentNode("div")
    if blocks == []:
        raise ValueError("No markdown to convert")
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_header:
            html.children.append(
                ParentNode(f"h{block.count('#')}", children=text_to_html_nodes(block[2:])))
        elif block_type == block_type_code:
            html.children.append(
                ParentNode("pre", children=[ParentNode("code", children=text_to_html_nodes(block[3:-3]))]))
        elif block_type == block_type_quote:
            html.children.append(
                ParentNode("blockquote", children=text_to_html_nodes(block[1:].strip())))
        elif block_type == block_type_unordered_list:
            html.children.append(
                ParentNode("ul", children=[ParentNode("li", text_to_html_nodes(line[2:])) for line in block.split("\n")]))
        elif block_type == block_type_ordered_list:
            html.children.append(
                ParentNode("ol", children=[ParentNode("li", text_to_html_nodes(line[3:])) for line in block.split("\n")]))
        elif block_type == block_type_paragraph:
            html.children.append(
                ParentNode("p", children=text_to_html_nodes(block)))
    return html

def extract_title(markdown):
    title = list(filter(lambda x: x.startswith("# "), markdown.split("\n")))
    if len(title) == 0:
        raise ValueError("No title found")
    return title[0][2:]

