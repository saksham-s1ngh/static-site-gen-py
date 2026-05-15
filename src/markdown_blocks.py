from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    filtered = []
    for block in block_strings:
        block = block.strip()
        if block == "":
            continue
        filtered.append(block)
    return filtered

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    if markdown_block.startswith(("###### ","##### ","#### ","### ","## ","# ")):
        return BlockType.HEADING
    if markdown_block.startswith("```\n") and markdown_block.endswith("\n```") and len(lines) > 1:
        return BlockType.CODE
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if markdown_block.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [] 
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    raise ValueError("invalid block type")
"""
Paragraph: join the lines with spaces (markdown often wraps a paragraph across multiple lines, but <p> should be one continuous string).

Heading: count the leading #s to pick h1–h6, then strip the #s and the space.

Code: strip the surrounding triple backticks, wrap a TextNode in a <code>, then wrap that in a <pre>. Don't run inline parsing here.

Quote: strip the > (and optional space) from each line, then join with spaces or newlines.

Unordered list: split on newlines, strip the - from each line, wrap each in <li>, wrap them all in <ul>.

Ordered list: same as ul, but strip the N. prefix and use <ol>.
"""

def paragraph_to_html_node(block):
    lines = block.split("\n") # split the string by \n
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
    
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```\n") or not block.endswith("\n```"):
        raise ValueError("invalid code block")
    code_block = block[4:-3] # slicing is cleaner than using strip("```\n")
    raw_text_node = TextNode(code_block, TextType.TEXT)
    code_child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [code_child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children) 

def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            raise ValueError("invalid ordered list block")
        text = line[len(f"{i+1}. "):]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def ulist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("invalid unordered list block")
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
