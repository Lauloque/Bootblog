import re
from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        for i, part in enumerate(parts):
            if part == "":
                continue
            new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.IMAGE:
            new_nodes.append(node)
            continue

        temp_text = node.text
        md_images = extract_markdown_images(temp_text)
        if not md_images:
            new_nodes.append(node)
            continue
        for img in md_images:
            (img_alt, img_url) = img
            before, after = temp_text.split(f"![{img_alt}]({img_url})", 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            temp_text = after
        if temp_text:
            new_nodes.append(TextNode(temp_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.LINK:
            new_nodes.append(node)
            continue

        temp_text = node.text
        md_links = extract_markdown_links(temp_text)
        if not md_links:
            new_nodes.append(node)
            continue
        for link in md_links:
            (link_alt, link_url) = link
            before, after = temp_text.split(f"[{link_alt}]({link_url})", 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            temp_text = after
        if temp_text:
            new_nodes.append(TextNode(temp_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_children(text: str) -> list[LeafNode]:
    textnode_list = text_to_textnodes(text)

    htmlnode_list = [text_node_to_html_node(textnode) for textnode in textnode_list]

    return htmlnode_list


def markdown_to_blocks(text: str) -> list[str]:
    blocks = []

    for block in text.split("\n\n"):
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                html_nodes_list = text_to_children(block) or None
                block_nodes.append(
                    ParentNode(
                        "p",
                        children=(html_nodes_list),
                    )
                )

            case BlockType.HEADING:
                heading_level = re.search(r"^(#{1,6})", block)
                assert heading_level is not None, "Expected a heading block"

                block = re.sub(r"^\#+\s", "", block, flags=re.MULTILINE)
                html_nodes_list = text_to_children(block) or None
                block_nodes.append(
                    ParentNode(
                        f"h{len(heading_level.group(1))}",
                        children=(html_nodes_list),
                    )
                )

            case BlockType.CODE:
                block = re.sub(r"^```\n?", "", block, flags=re.MULTILINE)
                block_nodes.append(
                    ParentNode("pre", [ParentNode("code", [LeafNode(None, block)])])
                )

            case BlockType.QUOTE:
                block = re.sub(r"^> ?", "", block, flags=re.MULTILINE)
                block = block.replace("\n", " ")
                html_nodes_list = text_to_children(block) or None
                block_nodes.append(
                    ParentNode(
                        "blockquote",
                        children=(html_nodes_list),
                    )
                )

            case BlockType.UNORDERED_LIST:
                block = re.sub(r"^- ", "", block, flags=re.MULTILINE)
                children_text = block.split("\n")
                children_nodes = []
                for child in children_text:
                    grandchildren = text_to_children(child) or None
                    children_nodes.append(ParentNode("li", grandchildren))
                block_nodes.append(ParentNode("ul", children_nodes))

            case BlockType.ORDERED_LIST:
                block = re.sub(r"^\d+\. ", "", block, flags=re.MULTILINE)
                children_text = block.split("\n")
                children_nodes = []
                for child in children_text:
                    grandchildren = text_to_children(child) or None
                    children_nodes.append(ParentNode("li", grandchildren))
                block_nodes.append(ParentNode("ol", children_nodes))

    return ParentNode(tag="div", children=block_nodes)
