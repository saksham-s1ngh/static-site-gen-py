from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    for block in block_strings:
        block = block.strip()
        if block == "":
            del block
    return block_strings

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    if markdown_block.startswith(("###### ","##### ","#### ","### ","## ","# ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```\n") and markdown_block.endswith("\n```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif markdown_block.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else :
        return BlockType.PARAGRAPH

