import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    markdown_blocks = markdown.split("\n")
    for block in markdown_blocks:
        if block.startswith("# "):
            title = block[2:].strip()
            if title:
                # this case is for when '# ' is found, but it's NOT empty after
                return title
    raise ValueError("No title found")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        source_markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_file_from_source = markdown_to_html_node(source_markdown).to_html()

    source_title = extract_title(source_markdown)
    template = template.replace("{{ Title }}", source_title)
    template = template.replace("{{ Content }}", html_file_from_source)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_recursive(
    source_dir_path: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, item)

        if os.path.isfile(source_path):
            new_filename = item.replace(".md", ".html")
            dest_file_path = os.path.join(dest_dir_path, new_filename)
            generate_page(source_path, template_path, dest_file_path, basepath)
        else:
            dest_sub_dir = os.path.join(dest_dir_path, item)
            if not os.path.exists(dest_sub_dir):
                os.mkdir(dest_sub_dir)
            generate_recursive(source_path, template_path, dest_sub_dir, basepath)
