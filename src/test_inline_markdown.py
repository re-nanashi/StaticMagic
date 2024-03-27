import unittest

from inline_markdown import (
    split_nodes_delimiter,
)

from textnode import (
    TextNode, TextType
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word",
                        TextType.text_type_text)
        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.text_type_bold)
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
        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.text_type_bold)
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
        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.text_type_bold)
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
        node = TextNode("This is text with an *italic* word",
                        TextType.text_type_text)
        new_nodes = split_nodes_delimiter(
            [node], "*", TextType.text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_type_text),
                TextNode("italic", TextType.text_type_italic),
                TextNode(" word", TextType.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode(
            "This is text with a `code block` word", TextType.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text),
                TextNode("code block", TextType.text_type_code),
                TextNode(" word", TextType.text_type_text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
