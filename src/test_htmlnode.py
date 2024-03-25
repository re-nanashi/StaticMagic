import unittest

from htmlnode import (HTMLNode, LeafNode)


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), repr(node2))

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_prop_conversion(self):
        node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        html_attr_str = node.props_to_html()
        self.assertEqual(
            html_attr_str, ' href="https://www.google.com" target="_blank"')

    def test_prop_conversion2(self):
        node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        html_attr_str = node.props_to_html()
        self.assertNotEqual(
            html_attr_str, ' href="https://www.boot.dev" target="_blank"')

    def test_repr(self):
        node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            "HTMLNode(None, None, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    def test_leafnode_conversion(self):
        leafnode = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(leafnode.to_html(),
                         "<p>This is a paragraph of text.</p>")

    def test_leafnode_conversion2(self):
        leafnode = LeafNode("a", "Click me!", {
            "href": "https://www.google.com"})
        self.assertEqual(
            leafnode.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leafnode_props_to_html(self):
        leafnode = LeafNode("a", "Click me!", {
                            "href": "https://www.google.com"})
        self.assertEqual(leafnode.props_to_html(),
                         ' href="https://www.google.com"')
