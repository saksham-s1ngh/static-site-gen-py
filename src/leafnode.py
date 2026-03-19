from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(
        self, 
        tag: str | None, 
        value: str | None, 
        props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value can't be none")
        if self.tag is None:
            return self.value

        props_list = [f' {k}="{v}"' for k, v in (self.props or {}).items()]
        attributes = "".join(props_list)
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
