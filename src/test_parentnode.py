import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " Normal "),
                LeafNode("i", "Italic"),
            ]
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> Normal <i>Italic</i></p>"
        )

    def test_missing_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Hello")
            ]
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_missing_children(self):
        node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children(self):
        node = ParentNode("div", [])

        self.assertEqual(
            node.to_html(),
            "<div></div>"
        )

    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Hello")
            ],
            {
                "class": "container"
            }
        )

        self.assertEqual(
            node.to_html(),
            '<div class="container">Hello</div>'
        )

    def test_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Hello")
                            ]
                        )
                    ]
                )
            ]
        )

        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>Hello</b></p></section></div>"
        )


if __name__ == "__main__":
    unittest.main()