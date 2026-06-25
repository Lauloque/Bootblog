from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode(terxt={self.text!r}, text_type={self.text_type.value!r}, url={self.url!r})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            # This should return a LeafNode with no tag, just a raw text value.
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            # This should return a LeafNode with a "b" tag and the text
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            # "i" tag, text
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            # "code" tag, text
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            # "a" tag, anchor text, and "href" prop
            if text_node.url is None:
                raise ValueError("LINK nodes require a URL")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            # "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
            if text_node.url is None:
                raise ValueError("IMAGE nodes require a URL")
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError(f"Unknown text_type '{text_node.text_type}'")
