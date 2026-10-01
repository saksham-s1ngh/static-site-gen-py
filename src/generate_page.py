def extract_title(markdown):
    # title = ""
    markdown_blocks = markdown.split("\n")
    for block in markdown_blocks:
        if block.startswith("# "):
            # title = block[2:].strip()
            return block[2:].strip()

    # if not title:
    raise Exception("No title found")
