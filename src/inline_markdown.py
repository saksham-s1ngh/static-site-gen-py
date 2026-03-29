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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        extracted_image_list = extract_markdown_images(node_text)

        for ext_image in extracted_image_list:
            sections = node_text.split(f"![{ext_image[0]}]({ext_image[1]})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            node_text = sections[1]
            new_nodes.append(TextNode(ext_image[0], TextType.IMAGE, ext_image[1]))

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        extracted_url_list = extract_markdown_links(node_text)

        for ext_url in extracted_url_list:
            sections = node_text.split(f"[{ext_url[0]}]({ext_url[1]})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            node_text = sections[1]
            new_nodes.append(TextNode(ext_url[0], TextType.LINK, ext_url[1]))

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    markdown_text_and_img = re.findall(r"!\[(.*?)\]\(([^)\s]+)\)", text) 
    return markdown_text_and_img

def extract_markdown_links(text):
    markdown_text_and_url = re.findall(r"\[(.*?)\]\(([^)\s]+)\)", text)
    return markdown_text_and_url
