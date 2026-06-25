import unittest

from markdown_converters import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter_single(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a *bold* word", TextType.TEXT)

        result = split_nodes_delimiter([node], "*", TextType.BOLD)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_occurrences(self):
        node = TextNode("This is *one* and *two* examples", TextType.TEXT)

        result = split_nodes_delimiter([node], "*", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" examples", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_non_text_nodes_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)

        result = split_nodes_delimiter([node], "*", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("normal *bold*", TextType.TEXT),
            TextNode("skip me", TextType.BOLD),
        ]

        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)

        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("skip me", TextType.BOLD),
        ]

        self.assertEqual(result, expected)


class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_link_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"

        self.assertEqual(
            extract_markdown_links(text), [("to boot dev", "https://www.boot.dev")]
        )

    def test_extract_link_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_img_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
        )

    def test_extract_img_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )


class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_no_link(self):
        node = TextNode("Some text", TextType.TEXT)

        self.assertListEqual(split_nodes_link([node]), [node])

    def test_split_no_image(self):
        node = TextNode("Some text", TextType.TEXT)

        self.assertListEqual(split_nodes_image([node]), [node])


if __name__ == "__main__":
    unittest.main()
