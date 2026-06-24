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

        expected = (
            "Current node: <a>\n"
            "        some text\n"
            "        Children:\n"
            "            No children\n"
            "        Props:\n"
            '            href="https://www.google.com"\n'
        )
        self.assertEqual(repr(node), expected)

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
