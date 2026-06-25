from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        props = self.props_to_html() if self.props else "No props"

        return (
            f"Current node: <{self.tag}>\n"
            f"        {self.value if self.value else 'No value'}\n"
            f"        Props:\n"
            f"           {props}\n"
        )
