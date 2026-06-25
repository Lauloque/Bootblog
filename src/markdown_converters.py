import re

from textnode import TextNode, TextType


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

        md_images = extract_markdown_images(node.text)
        if not md_images:
            new_nodes.append(node)
        temp_text = node.text
        for img in md_images:
            (img_alt, img_url) = img
            before, after = temp_text.split(f"![{img_alt}]({img_url})", 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            temp_text = after
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.LINK:
            new_nodes.append(node)
            continue

        md_links = extract_markdown_links(node.text)
        if not md_links:
            new_nodes.append(node)
        temp_text = node.text
        for link in md_links:
            (link_alt, link_url) = link
            before, after = temp_text.split(f"[{link_alt}]({link_url})", 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            temp_text = after
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
