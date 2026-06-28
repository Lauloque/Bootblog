import unittest
from re import L

from blocknode import (
    BlockType,
    block_to_block_type,
)


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
