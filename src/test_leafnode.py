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

        self.assertEqual(
            repr(node),
            "LeafNode(tag='a', value='some text', props={'href': 'https://www.google.com'})",
        )

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
