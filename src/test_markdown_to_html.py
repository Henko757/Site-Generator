import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        # Using a clean string to avoid accidental empty text block generation
        md = (
            "This is **bolded** paragraph\ntext in a p\ntag here\n\n"
            "This is another paragraph with _italic_ text and `code` here"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        # Code blocks preserve internal formatting and newlines
        md = "```\ndef hello():\n    print('world')\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>def hello():\n    print('world')\n</code></pre></div>"
        )


if __name__ == "__main__":
    unittest.main()