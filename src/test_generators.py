import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extra_spaces(self):
        case = "# My test title!\n# another title"
        expected = "My test title!"

        self.assertEqual(extract_title(case), expected)

    def test_extra_title(self):
        case = "# My test title!\n# another title"
        expected = "My test title!"

        self.assertEqual(extract_title(case), expected)

    def test_no_title(self):
        case = "no title"
        with self.assertRaises(Exception) as cm:
            extract_title(case)

        self.assertEqual(str(cm.exception), "No title in the provided markdown file.")
