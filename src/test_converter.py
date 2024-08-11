import unittest
from textnode import TextNode, TextType
from converter import split_nodes_delimiter
import unittest
from converter import extract_markdown_images

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_valid_delimiter(self):
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.text_type_text)
        ]
        delimiter = "`"
        text_type = TextType.text_type_code
        expected_nodes = [
            TextNode("This is text with a ", TextType.text_type_text),
            TextNode("code block", TextType.text_type_code),
            TextNode(" word", TextType.text_type_text),
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_invalid_delimiter_amount(self):
        old_nodes = [
            TextNode("This is text with a `code block` `word", TextType.text_type_text)
        ]
        delimiter = "`"
        text_type = TextType.text_type_code
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_no_text_nodes(self):
        old_nodes = [
            TextNode("This is some code``", TextType.text_type_text)
        ]
        delimiter = "`"
        text_type = TextType.text_type_code
        expected_nodes = [
            TextNode("This is some code", TextType.text_type_text)
        ]
        print(split_nodes_delimiter(old_nodes, delimiter, text_type))
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_empty_nodes(self):
        old_nodes = []
        delimiter = ","
        text_type = TextType.text_type_code
        expected_nodes = []
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_no_images(self):
        text = "This is text without any images"
        expected_images = []
        self.assertEqual(extract_markdown_images(text), expected_images)

        
if __name__ == "__main__":
    unittest.main()