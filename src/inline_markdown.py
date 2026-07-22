import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: missing closing '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(
        r"!\[(.*?)\]\((.*?)\)",
        text,
    )


def extract_markdown_links(text):
    return re.findall(
        r"\[(.*?)\]\((.*?)\)",
        text,
    )


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt_text, url in images:
            markdown = f"![{alt_text}]({url})"

            sections = remaining_text.split(markdown, 1)

            if len(sections) != 2:
                raise Exception("Invalid markdown image")

            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT,
                    )
                )

            new_nodes.append(
                TextNode(
                    alt_text,
                    TextType.IMAGE,
                    url,
                )
            )

            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(
                    remaining_text,
                    TextType.TEXT,
                )
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for text, url in links:
            markdown = f"[{text}]({url})"

            sections = remaining_text.split(markdown, 1)

            if len(sections) != 2:
                raise Exception("Invalid markdown link")

            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT,
                    )
                )

            new_nodes.append(
                TextNode(
                    text,
                    TextType.LINK,
                    url,
                )
            )

            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(
                    remaining_text,
                    TextType.TEXT,
                )
            )

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(
        nodes,
        "`",
        TextType.CODE,
    )

    nodes = split_nodes_delimiter(
        nodes,
        "**",
        TextType.BOLD,
    )

    nodes = split_nodes_delimiter(
        nodes,
        "_",
        TextType.ITALIC,
    )

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes