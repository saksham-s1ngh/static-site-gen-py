import os

from markdown_blocks import (
    markdown_to_html_node,
)


def extract_title(markdown):
    # title = ""
    markdown_blocks = markdown.split("\n")
    for block in markdown_blocks:
        if block.startswith("# "):
            title = block[2:].strip()
            if title:
                # this case is for when '# ' is found, but it's empty after
                return title

    raise Exception("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        source_markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_file_from_source = markdown_to_html_node(source_markdown).to_html()
    source_title = extract_title(source_markdown)

    template = template.replace("{{ Title }}", source_title)
    template = template.replace("{{ Content }}", html_file_from_source)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as f:
        f.write(template)
