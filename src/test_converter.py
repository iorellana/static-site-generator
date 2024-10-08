import unittest
from htmlnode import HTMLNode
from textnode import (TextNode, 
                      text_type_text, 
                      text_type_bold, 
                      text_type_italic, 
                      text_type_code, 
                      text_type_image, 
                      text_type_link)
import unittest
from converter import (extract_markdown_images, extract_markdown_links, extract_title,
                       markdown_to_html_node, 
                        split_nodes_delimiter, split_nodes_image, split_nodes_link,
                        text_to_textnodes,
                        markdown_to_blocks, block_type_header, block_type_code, block_type_quote, block_type_unordered_list, block_type_ordered_list, block_type_paragraph, block_to_block_type)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_valid_delimiter(self):
        old_nodes = [
            TextNode("This is text with a `code block` word", text_type_text)
        ]
        delimiter = "`"
        text_type = text_type_code
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_invalid_delimiter_amount(self):
        old_nodes = [
            TextNode("This is text with a `code block` `word", text_type_text)
        ]
        delimiter = "`"
        text_type = text_type_code
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_no_text_nodes(self):
        old_nodes = [
            TextNode("This is some code``", text_type_text)
        ]
        delimiter = "`"
        text_type = text_type_code
        expected_nodes = [
            TextNode("This is some code", text_type_text)
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_empty_nodes(self):
        old_nodes = []
        delimiter = ","
        text_type = text_type_code
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
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
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
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
        
class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is a single block"
        expected_blocks = ["This is a single block"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_blocks(self):
        markdown = "This is the first block\n\nThis is the second block\n\nThis is the third block"
        expected_blocks = ["This is the first block", "This is the second block", "This is the third block"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_empty_blocks(self):
        markdown = "\n\n\n"
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_blocks_with_spaces(self):
        markdown = "   This is the first block   \n\n   This is the second block   \n\n   This is the third block   "
        expected_blocks = ["This is the first block", "This is the second block", "This is the third block"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_header_block(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), block_type_header)

    def test_code_block(self):
        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_quote_block(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_ordered_list_block(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

    def test_paragraph_block(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

# PRE: Every to_html() has a initial div tag
class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_header(self):
        markdown = "# Hello world!"
        expected_html = "<div><h1>Hello world!</h1></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_code_block(self):
        markdown = "```python\nprint('Hello world!')\n```"
        expected_html = "<div><pre><code>python\nprint('Hello world!')\n</code></pre></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_quote(self):
        markdown = "> Hello world!"
        expected_html = "<div><blockquote>Hello world!</blockquote></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_unordered_list(self):
        markdown = "- item 1\n- item 2\n- item 3"
        expected_html = "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_ordered_list(self):
        markdown = "1. item 1\n2. item 2\n3. item 3"
        expected_html = "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_paragraph(self):
        markdown = "Hello world!"
        expected_html = "<div><p>Hello world!</p></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_empty(self):
        markdown = ""
        self.assertRaises(ValueError, markdown_to_html_node, markdown)

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = "# This is a valid title"
        expected_title = "This is a valid title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_no_title(self):
        markdown = "This is a paragraph without a title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_multiple_titles(self):
        markdown = "# Title 1\n\n# Title 2"
        expected_title = "Title 1"
        self.assertEqual(extract_title(markdown), expected_title)

if __name__ == "__main__":
    unittest.main()