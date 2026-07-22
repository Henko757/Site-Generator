import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_heading_six_hashes(self):
        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )

    def test_invalid_heading(self):
        self.assertEqual(
            block_to_block_type("####### Too many"),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote(self):
        block = "> Quote\n> Another quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        block = "- One\n- Two\n- Three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        block = "1. One\n2. Two\n3. Three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_list(self):
        block = "1. One\n3. Three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is just a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()