def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    for block in block_strings:
        block = block.strip()

        if block == "":
            del block

    return block_strings
