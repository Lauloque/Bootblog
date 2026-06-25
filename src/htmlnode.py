class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def __repr__(self) -> str:
        return f"HTMLNode(tag{self.tag!r}, value={self.value!r}, children={self.children!r}, prop={self.props!r})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        string = ""
        if self.props:
            for key, value in self.props.items():
                string += f' {key}="{value}"'
        return string
