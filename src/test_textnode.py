import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is link", TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode("This is link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is an unspecified link url", TextType.LINK)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
