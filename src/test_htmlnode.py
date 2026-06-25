import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props_leading_spaces(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.props_to_html()[0], " ")

    def test_print_node(self):
        node = HTMLNode(
            tag="a",
            value="some text",
            props={"href": "https://www.google.com"},
        )

        self.assertEqual(
            repr(node),
            "HTMLNode(tag'a', value='some text', children=None, prop={'href': 'https://www.google.com'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="some text",
            props={"href": "https://www.google.com", "target": "_blank"},
        )

        expected = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
