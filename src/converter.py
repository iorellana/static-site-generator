from textnode import TextNode, TextType
import re

# Ignores the nodes that are not text text_type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        parts = text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid delimiter amount")
        for i in range(0, len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], node.text_type))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        parts = extract_markdown_images(text)
        if len(parts) == 0:
            new_nodes.append(node)
            continue
        for i in range(0, len(parts)):
            if i == 0:
                new_nodes.append(TextNode(parts[i][0], node.text_type))
            new_nodes.append(TextNode(parts[i][1], TextType.text_type_image))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches