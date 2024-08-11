import unittest
from enum import Enum
from textnode import TextNode, text_node_to_html_node, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode("Hello, World!", TextType.text_type_text)
        expected_node = LeafNode(value="Hello, World!")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_text_type_bold(self):
        text_node = TextNode("Hello, World!", TextType.text_type_bold)
        expected_node = LeafNode(tag="b", value="Hello, World!")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_text_type_italic(self):
        text_node = TextNode("Hello, World!", TextType.text_type_italic)
        expected_node = LeafNode(tag="i", value="Hello, World!")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_text_type_code(self):
        text_node = TextNode("print('Hello, World!')", TextType.text_type_code)
        expected_node = LeafNode(tag="code", value="print('Hello, World!')")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_text_type_link(self):
        text_node = TextNode("GitHub", TextType.text_type_link, url="https://github.com")
        expected_node = LeafNode(tag="a", value="GitHub", props={"href": "https://github.com"})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_text_type_image(self):
        text_node = TextNode("Logo", TextType.text_type_image, url="https://example.com/logo.png")
        expected_node = LeafNode(tag="img", value="", props={"src": "https://example.com/logo.png", "alt": "Logo"})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), expected_node.to_html())

    def test_invalid_text_type(self):
        text_node = TextNode("Hello, World!", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()