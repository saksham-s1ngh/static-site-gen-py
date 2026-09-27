import os
import shutil

from copystatic import recursive_copy
from textnode import TextNode, TextType

dir_path_public = "./public"
dir_path_static = "./static"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(
            dir_path_public
        )  # delete all the contents of the destination directory

    print("Copying static files to public...")
    recursive_copy(dir_path_static, dir_path_public)


main()
