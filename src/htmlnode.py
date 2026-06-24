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
        self.props = props

    def __repr__(self) -> str:
        children = (
            "\n".join(f"            {child}" for child in self.children)
            if self.children
            else "            No children"
        )
        props = self.props_to_html() if self.props else "No props"

        return (
            f"Current node: <{self.tag}>\n"
            f"        {self.value if self.value else 'No value'}\n"
            f"        Children:\n"
            f"{children}\n"
            f"        Props:\n"
            f"           {props}\n"
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        string = ""
        if self.props:
            for key, value in self.props.items():
                string += f' {key}="{value}"'
        return string
