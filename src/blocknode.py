import re
from enum import Enum

from leafnode import LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text: str) -> BlockType:
    if re.search(r"^(#{1,6}\s)", text):
        return BlockType.HEADING

    if re.search(r"^```\n[\s\S]*?\n```$", text):
        return BlockType.CODE

    lines = text.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST
