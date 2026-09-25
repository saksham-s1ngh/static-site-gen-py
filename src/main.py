import os
import shutil

from textnode import TextNode, TextType


def recursive_copy(source, dest):
    item_path, dest_path = "", ""
    source_items = os.listdir(source)
    for item in source_items:
        item_path = os.path.join(source, item)  # construct full path with the item
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest)
        else:  # if item is a directory
            # if the item is a dir, it will have to be a dir within public
            # so we the correct destination path which is : dest + sub_dir_name
            dest_path = os.path.join(dest, item)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            recursive_copy(
                item_path, dest_path
            )  # recurse through the item if it's a directory


def main():
    dummy_node = TextNode("This is img alt text", TextType.BOLD, "#dummy_url")
    print(dummy_node)

    dest = "public/"
    if os.path.exists(dest):
        shutil.rmtree(dest)  # delete all the contents of the destination directory
    os.mkdir(dest)

    source = "static/"
    recursive_copy(source, dest)


main()
