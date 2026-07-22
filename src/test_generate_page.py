import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_single_h1(self):
        md = "# Hello World"

        self.assertEqual(
            extract_title(md),
            "Hello World",
        )

    def test_h1_with_whitespace(self):
        md = "#     Hello Boot.dev     "

        self.assertEqual(
            extract_title(md),
            "Hello Boot.dev",
        )

    def test_h1_after_other_text(self):
        md = """
Some introductory text.

# My Awesome Page

More text here.
"""

        self.assertEqual(
            extract_title(md),
            "My Awesome Page",
        )

    def test_multiple_headings(self):
        md = """
# First Heading

## Second Heading

### Third Heading
"""

        self.assertEqual(
            extract_title(md),
            "First Heading",
        )

    def test_no_h1(self):
        md = """
## Heading Two

Some paragraph text.

### Heading Three
"""

        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_markdown(self):
        md = ""

        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()