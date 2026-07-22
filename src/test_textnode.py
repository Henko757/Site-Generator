import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):

    # ---------- TextNode equality tests ----------

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Goodbye", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode(
            "Google",
            TextType.LINK,
            "https://google.com",
        )

        node2 = TextNode(
            "Google",
            TextType.LINK,
            "https://youtube.com",
        )

        self.assertNotEqual(node, node2)

    def test_equal_none_url(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)

        self.assertEqual(node, node2)

    # ---------- text_node_to_html_node() tests ----------

    def test_text(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode(
            "Bold text",
            TextType.BOLD,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode(
            "Italic text",
            TextType.ITALIC,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode(
            "print('Hello')",
            TextType.CODE,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode(
            "Google",
            TextType.LINK,
            "https://www.google.com",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(
            html_node.props,
            {
                "href": "https://www.google.com",
            },
        )

    def test_image(self):
        node = TextNode(
            "An image",
            TextType.IMAGE,
            "image.png",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "image.png",
                "alt": "An image",
            },
        )

    def test_invalid_text_type(self):
        node = TextNode(
            "Invalid",
            "INVALID_TYPE",
        )

        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()