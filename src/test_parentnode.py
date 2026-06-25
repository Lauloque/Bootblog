import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_props_leading_spaces(self):
        node = ParentNode(
            tag="a",
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.props_to_html()[0], " ")

    def test_print_node(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            tag="a",
            children=[child_node],
            props={"href": "https://www.google.com"},
        )

        self.assertEqual(
            repr(parent_node),
            "HTMLNode(tag'a', value=None, children=[LeafNode(tag='span', value='child', props=None)], prop={'href': 'https://www.google.com'})",
        )

    def test_props_to_html(self):
        parent_node = ParentNode(
            "p",
            children=None,
            props={"href": "https://www.google.com"},
        )

        self.assertEqual(parent_node.props_to_html(), ' href="https://www.google.com"')


if __name__ == "__main__":
    unittest.main()
