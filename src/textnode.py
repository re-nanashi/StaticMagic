from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


"""
text_type_text: This should become a LeafNode with no tag, just a raw text value.
text_type_bold: This should become a LeafNode with a "b" tag and the text
text_type_italic: "i" tag, text
text_type_code: "code" tag, text
text_type_link: "a" tag, anchor text, and "href" prop
text_type_image: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""


def text_node_to_html_node(text_node):
    match text_node.text:
        case TextType.text_type_text:
            return LeafNode(None, text_node.text)
        case TextType.text_type_bold:
            return LeafNode("b", text_node.text)
        case TextType.text_type_italic:
            return LeafNode("i", text_node.text)
        case TextType.text_type_code:
            return LeafNode("code", text_node.text)
        case TextType.text_type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.text_type_image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid text type: {text_node.text_type}")


"""
node = TextNode("This is text with a `code block` word", text_type_text)
new_nodes = split_nodes_delimiter([node], "`", text_type_code)

It returns:
[
    TextNode("This is text with a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" word", text_type_text),
"""


def split_nodes_delimiter(old_nodes, delimiter, text_type_code):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(new_nodes)
        res_node = []
        split_text_str = node.text.split(delimiter)
        if len(split_text_str) != 3:
            raise Exception(
                "Invalid markdown syntax: matching closing delimiter not found")
        res_node.append(TextNode(split_text_str[0], TextType.text_type_text))
        res_node.append(TextNode(split_text_str[1], text_type_code))
        res_node.append(TextNode(split_text_str[2], TextType.text_type_text))
        new_nodes.extend(res_node)
    return new_nodes
