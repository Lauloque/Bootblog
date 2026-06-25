from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list["HTMLNode"] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("No value provided to parent node")
        if not self.children:
            raise ValueError("No children provided to parent node")
        children_str = ""
        for child in self.children:
            children_str += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
