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
        
        for index, split_node in enumerate(split_nodes):
            if split_node == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split_node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # skip processing non-text nodes (since they might already be processed)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        extracted_image_list = extract_markdown_images(node_text)
        # if there's no images, skip processing and append as-is
        if len(extracted_image_list) == 0:
            new_nodes.append(node)
            continue
        for ext_image in extracted_image_list:
            sections = node_text.split(f"![{ext_image[0]}]({ext_image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(ext_image[0], TextType.IMAGE, ext_image[1]))
            node_text = sections[1]
        if node_text != "": # for any trailing text nodes after image nodes
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # skip processing non-text nodes (since they might already be processed)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        extracted_url_list = extract_markdown_links(node_text)
        # if there's no urls, skip processing and append as-is
        if len(extracted_url_list) == 0:
            new_nodes.append(node)
            continue
        for ext_url in extracted_url_list:
            sections = node_text.split(f"[{ext_url[0]}]({ext_url[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            node_text = sections[1]
            new_nodes.append(TextNode(ext_url[0], TextType.LINK, ext_url[1]))
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    markdown_text_and_img = re.findall(r"!\[(.*?)\]\(([^)\s]+)\)", text) 
    return markdown_text_and_img

def extract_markdown_links(text):
    markdown_text_and_url = re.findall(r"\[(.*?)\]\(([^)\s]+)\)", text)
    return markdown_text_and_url

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

