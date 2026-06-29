import unittest

from markdown_converters import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


class TestTextToTextnodes(unittest.TestCase):
    def test_one_for_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_only(self):
        text = "This is just some text"

        expected = [TextNode(text, TextType.TEXT)]

        self.assertListEqual(text_to_textnodes(text), expected)


class TestMarkdown2Blocks(unittest.TestCase):
    def test_all_in_one(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)

    def test_empty_blocks(self):
        md = """
This is a paragraph


This is another paragraph
"""

        expected = ["This is a paragraph", "This is another paragraph"]
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, expected)


class TestBlock2BlockType(unittest.TestCase):
    def test_valid_headings(self):
        headings = [
            "# text",
            "## text",
            "### text",
            "#### text",
            "##### text",
            "###### text",
        ]

        for heading in headings:
            with self.subTest(heading=heading):
                self.assertEqual(block_to_block_type(heading), BlockType.HEADING)

    def test_wrong_headings(self):
        headings = [
            "#text",
            "####### text",
            " text",
            "text",
        ]

        for heading in headings:
            with self.subTest(heading=heading):
                self.assertNotEqual(block_to_block_type(heading), BlockType.HEADING)

    def test_valid_codes(self):
        cases = [
            """```
some code
```""",
            """```
some code
on multiple lines
```""",
        ]

        for case in cases:
            with self.subTest(case=case):
                self.assertEqual(block_to_block_type(case), BlockType.CODE)

    def test_invalid_codes(self):
        cases = [
            """```python
some python code
```""",
            """```
some code that doesn't end
""",
            """some code that doesn't start
```""",
        ]

        for case in cases:
            with self.subTest(case=case):
                self.assertNotEqual(block_to_block_type(case), BlockType.CODE)

    def test_valid_quotes(self):
        text = "> some text\n> with line returns\n> and other things..."

        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_invalid_quotes(self):
        text = "> some text\nwith line returns\n> and other things..."

        self.assertNotEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_valid_unordered_list(self):
        text = "- some text\n- with line returns\n- and other things..."

        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        text = "- some text\nwith line returns\n- and other things..."

        self.assertNotEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_valid_ordered_list(self):
        text = "1. some text\n2. with line returns\n3. and other things..."

        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        cases = [
            "1. numbers \n3. unordered \n2. list",
            "1- wrong\n2- leading\n3- character",
            "1.simply\n2.no\n3.spaces",
        ]

        for case in cases:
            with self.subTest(case=case):
                self.assertNotEqual(block_to_block_type(case), BlockType.ORDERED_LIST)


class TestBlock2HTML(unittest.TestCase):
    def test_all(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

> This is a quote > with a `code` inline.

```
a code block
with line return
```

- unordered
- lis**ttt**

1. ordered
2. lis_ttt_

# heading

## heading

### heading

#### heading

##### heading

###### heading

####### fake heading
"""

        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><blockquote>This is a quote > with a <code>code</code> inline.</blockquote><pre><code>a code block\nwith line return\n</code></pre><ul><li>unordered</li><li>lis<b>ttt</b></li></ul><ol><li>ordered</li><li>lis<i>ttt</i></li></ol><h1>heading</h1><h2>heading</h2><h3>heading</h3><h4>heading</h4><h5>heading</h5><h6>heading</h6><p>####### fake heading</p></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected,
        )


if __name__ == "__main__":
    unittest.main()
