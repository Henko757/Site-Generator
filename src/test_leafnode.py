import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>"
        )

    def test_leaf_to_html_link(self):
        node = LeafNode(
            "a",
            "Click me!",
            {
                "href": "https://www.google.com"
            }
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_raw_text(self):
        node = LeafNode(None, "Plain text")

        self.assertEqual(
            node.to_html(),
            "Plain text"
        )

    def test_leaf_bold(self):
        node = LeafNode("b", "Important")

        self.assertEqual(
            node.to_html(),
            "<b>Important</b>"
        )

    def test_leaf_no_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()