from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text;
        self.text_type = text_type;
        self.url = url;

    def __eq__(self, other):
        return ( 
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, text_node.url)
    elif text_node.text_type == TextType.IMAGE:
        prop_dict = {
            "src" : text_node.url,
            "alt" : text_node.text,
        }
        return LeafNode("img", "", prop_dict)
    else:
        raise NameError("Incorrect text type name")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise Exception("Closing delimiter not found")
        
        for index, splits in enumerate(split_nodes):
            if splits == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(splits, TextType.TEXT))
            else:
                new_nodes.append(TextNode(splits, text_type))
    return new_nodes

