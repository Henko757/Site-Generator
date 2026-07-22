import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    # ---------- split_nodes_delimiter ----------

    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    # ---------- extract_markdown_images ----------

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertEqual(
            matches,
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
        )

    # ---------- extract_markdown_links ----------

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://boot.dev)"
        )

        self.assertEqual(
            matches,
            [("Boot.dev", "https://boot.dev")],
        )

    # ---------- split_nodes_image ----------

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(
                    " and another ",
                    TextType.TEXT,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
        )

    # ---------- split_nodes_link ----------

    def test_split_links(self):
        node = TextNode(
            "Visit [Boot.dev](https://boot.dev) today!",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode(
                    "Visit ",
                    TextType.TEXT,
                ),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
                TextNode(
                    " today!",
                    TextType.TEXT,
                ),
            ],
        )

    # ---------- text_to_textnodes ----------

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word "
            "and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
        )

    def test_text_only(self):
        self.assertEqual(
            text_to_textnodes("Hello world"),
            [
                TextNode(
                    "Hello world",
                    TextType.TEXT,
                )
            ],
        )

    def test_only_bold(self):
        self.assertEqual(
            text_to_textnodes("**Hello**"),
            [
                TextNode(
                    "Hello",
                    TextType.BOLD,
                )
            ],
        )

    def test_only_italic(self):
        self.assertEqual(
            text_to_textnodes("_Hello_"),
            [
                TextNode(
                    "Hello",
                    TextType.ITALIC,
                )
            ],
        )

    def test_only_code(self):
        self.assertEqual(
            text_to_textnodes("`print('Hello')`"),
            [
                TextNode(
                    "print('Hello')",
                    TextType.CODE,
                )
            ],
        )

    def test_only_image(self):
        self.assertEqual(
            text_to_textnodes(
                "![cat](cat.png)"
            ),
            [
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                )
            ],
        )

    def test_only_link(self):
        self.assertEqual(
            text_to_textnodes(
                "[Boot.dev](https://boot.dev)"
            ),
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()