import re
from textnode import TextNode, TextType

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

def extract_markdown_images(text):
    markdown_text_and_img = re.findall(r"!\[(.*?)\]\(([^)\s]+)\)", text) 
    return markdown_text_and_img

def extract_markdown_links(text):
    markdown_text_and_url = re.findall(r"\[(.*?)\]\(([^)\s]+)\)", text)
    return markdown_text_and_url
