from parentnode import ParentNode
from leafnode import LeafNode
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)
from inline_markdown import text_to_textnodes
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


def text_to_children(text):
    """
    Convert inline markdown text into HTMLNodes.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def paragraph_to_html_node(block):
    """
    Convert a paragraph block into a ParentNode.
    """
    text = " ".join(block.split("\n"))
    return ParentNode(
        "p",
        text_to_children(text),
    )


def heading_to_html_node(block):
    """
    Convert a markdown heading to an h1-h6 node safely.
    """
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1

    # Safe stripping handling whether space is present or missing
    text = block[level:]
    if text.startswith(" "):
        text = text[1:]

    return ParentNode(
        f"h{level}",
        text_to_children(text),
    )


def quote_to_html_node(block):
    """
    Convert a markdown quote block into a blockquote node.
    """
    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        if line.startswith(">"):
            line = line[1:]
        if line.startswith(" "):
            line = line[1:]
        cleaned_lines.append(line)

    text = " ".join(cleaned_lines)
    return ParentNode(
        "blockquote",
        text_to_children(text),
    )


def unordered_list_to_html_node(block):
    """
    Convert a markdown unordered list into a <ul>.
    """
    items = []
    for line in block.split("\n"):
        text = line[2:] if len(line) > 2 else ""
        items.append(
            ParentNode(
                "li",
                text_to_children(text),
            )
        )
    return ParentNode(
        "ul",
        items,
    )


def ordered_list_to_html_node(block):
    """
    Convert a markdown ordered list into an <ol>.
    """
    items = []
    for line in block.split("\n"):
        # Isolate the list marker boundary (e.g., "1. ")
        parts = line.split(".", 1)
        text = parts[1].strip() if len(parts) > 1 else line
        items.append(
            ParentNode(
                "li",
                text_to_children(text),
            )
        )
    return ParentNode(
        "ol",
        items,
    )


def code_to_html_node(block):
    """
    Convert a markdown code block into <pre><code>...</code></pre>
    """
    lines = block.split("\n")
    # Check if code block contains explicit newline fences
    if len(lines) > 1:
        code = "\n".join(lines[1:-1]) + "\n"
    else:
        code = block.strip("`")

    code_leaf = text_node_to_html_node(
        TextNode(code, TextType.TEXT)
    )

    code_node = ParentNode(
        "code",
        [code_leaf],
    )

    return ParentNode(
        "pre",
        [code_node],
    )


def block_to_html_node(block):
    """
    Convert a markdown block into the appropriate HTML node.
    """
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    """
    Convert an entire markdown document into a single HTML tree.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode(
        "div",
        children,
    )