import unittest

from htmlnode import (HTMLNode, LeafNode, ParentNode)


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), repr(node2))

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

    def test_parentnode_class(self):
        parentnode = ParentNode("p", [LeafNode("b", "Bold text")])

        self.assertEqual(parentnode.to_html(), "<p><b>Bold text</b></p>")

    def test_pnode_(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(
            None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])

        self.assertEqual(node.to_html(
        ), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

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

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.to_html(),
            '<h2 class="greeting" href="https://boot.dev"><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>',
        )


if __name__ == "__main__":
    unittest.main()
