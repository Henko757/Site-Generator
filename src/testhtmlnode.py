import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_none(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_props_empty(self):
        node = HTMLNode(props={})

        self.assertEqual(node.props_to_html(), "")

    def test_single_property(self):
        node = HTMLNode(
            props={
                "class": "container"
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' class="container"'
        )


if __name__ == "__main__":
    unittest.main()