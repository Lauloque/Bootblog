import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_props_leading_spaces(self):
        node = LeafNode(
            tag="a",
            value="test",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.props_to_html()[0], " ")

    def test_print_node(self):
        node = LeafNode(
            tag="a",
            value="some text",
            props={"href": "https://www.google.com"},
        )

        expected = (
            "Current node: <a>\n"
            "        some text\n"
            "        Props:\n"
            '            href="https://www.google.com"\n'
        )
        self.assertEqual(repr(node), expected)

    def test_props_to_html(self):
        node = LeafNode(
            tag="a",
            value="some text",
            props={"href": "https://www.google.com", "target": "_blank"},
        )

        expected = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
