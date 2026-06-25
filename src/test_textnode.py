import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        image_node = TextNode(
            "This is an image node",
            TextType.IMAGE,
            url="https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ",
        )
        html_node = text_node_to_html_node(image_node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props["src"], "https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ"
        )
        self.assertEqual(html_node.props["alt"], "This is an image node")


if __name__ == "__main__":
    unittest.main()
