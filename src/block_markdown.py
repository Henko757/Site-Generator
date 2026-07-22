from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    cleaned_blocks = []

    for block in blocks:
        block = block.strip()

        if block != "":
            cleaned_blocks.append(block)

    return cleaned_blocks


def block_to_block_type(block: str) -> BlockType:
    # Heading
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered List
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered List
    ordered = True

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break

    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH