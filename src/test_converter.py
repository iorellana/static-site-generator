import unittest
from textnode import TextNode, TextType
from converter import split_nodes_delimiter
import unittest
from converter import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link

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

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("bolded", TextType.text_type_bold),
                TextNode(" word", TextType.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("bolded", TextType.text_type_bold),
                TextNode(" word and ", TextType.text_type_text),
                TextNode("another", TextType.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("bolded word", TextType.text_type_bold),
                TextNode(" and ", TextType.text_type_text),
                TextNode("another", TextType.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_type_text),
                TextNode("italic", TextType.text_type_italic),
                TextNode(" word", TextType.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("code block", TextType.text_type_code),
                TextNode(" word", TextType.text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_type_text),
                TextNode("image", TextType.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_type_text),
                TextNode("image", TextType.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text_type_text),
                TextNode(
                    "second image", TextType.text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("link", TextType.text_type_link, "https://boot.dev"),
                TextNode(" and ", TextType.text_type_text),
                TextNode("another link", TextType.text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.text_type_text),
            ],
            new_nodes,
        )
        
if __name__ == "__main__":
    unittest.main()