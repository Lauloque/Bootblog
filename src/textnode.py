from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain_text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "code-text"
    LINK = "link"


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"
