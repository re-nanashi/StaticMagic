from enum import Enum

from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


class TextType(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"


"""
text_type_text: This should become a LeafNode with no tag, just a raw text value.
text_type_bold: This should become a LeafNode with a "b" tag and the text
text_type_italic: "i" tag, text
text_type_code: "code" tag, text
text_type_link: "a" tag, anchor text, and "href" prop
text_type_image: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""


def text_node_to_html_node(textnode):
    match textnode.text:
        case TextType.text_type_text:
            return LeafNode(None, textnode.text)
        case TextType.text_type_bold:
            return LeafNode("b", textnode.text)
        case TextType.text_type_italic:
            return LeafNode("i", textnode.text)
        case TextType.text_type_code:
            return LeafNode("code", textnode.text)
        case TextType.text_type_link:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.text_type_image:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise Exception(f"Invalid text type: {textnode.text_type}")
