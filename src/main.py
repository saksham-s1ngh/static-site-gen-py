import os
import shutil
import sys

from copystatic import recursive_copy
from generate_page import generate_recursive

dir_path_docs = "./docs"
dir_path_static = "./static"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(
            dir_path_docs
        )  # delete all the contents of the destination directory

    # grab the first CLI arg (if exists), and save it to basepath
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print("Copying static files to docs...")
    recursive_copy(dir_path_static, dir_path_docs)

    dir_path_content = "./content/"
    template_path = "./template.html"
    generate_recursive(dir_path_content, template_path, dir_path_docs, basepath)


main()
