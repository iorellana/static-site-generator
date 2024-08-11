import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", props={'class': 'container'})
        self.assertEqual(repr(node), "tag: div \nvalue: Hello, World! \nchildren: None \nprops: {'class': 'container'}")

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, World!", props={'class': 'container', 'id': 'main'})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph", props={'class': 'container'})
        self.assertEqual(node.to_html(), '<p class="container">This is a paragraph</p>')

    def test_to_html_no_tag(self):
        node = LeafNode(value="This is a paragraph", props={'class': 'container'})
        self.assertEqual(node.to_html(), 'This is a paragraph')

    def test_to_html_no_value(self):
        node = LeafNode("p", props={'class': 'container'})
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("div", children=[
            LeafNode("p", "This is a paragraph", props={'class': 'container'}),
            LeafNode("span", "This is a span", props={'class': 'highlight'}),
            LeafNode("a", "This is a link", props={'href': 'https://example.com'})
        ], props={'class': 'wrapper'})
        expected_html = '<div class="wrapper"><p class="container">This is a paragraph</p><span class="highlight">This is a span</span><a href="https://example.com">This is a link</a></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_tag(self):
        node = ParentNode(children=[
            LeafNode("p", "This is a paragraph", props={'class': 'container'}),
            LeafNode("span", "This is a span", props={'class': 'highlight'}),
            LeafNode("a", "This is a link", props={'href': 'https://example.com'})
        ], props={'class': 'wrapper'})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", props={'class': 'wrapper'})
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()