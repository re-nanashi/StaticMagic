import os
import shutil

from copystatic import copy_files_r
from gencontent import generate_pages_r


def copy_static_files():
    dir_path_static = "./static"
    dir_path_public = "./public"
    if not os.path.exists(dir_path_static):
        # Raise an exception if no folder to copy
        raise Exception("Directory does not exist: static. Exiting program...")
    if not os.path.exists(dir_path_public):
        # Create new dir if public directory does not exist
        os.mkdir("../public")
    # Delete the public dir's content
    shutil.rmtree(dir_path_public)
    # Copy the files from static to public
    copy_files_r(dir_path_static, dir_path_public)
    print("Success: All files from the static directory has been copied to the public directory.")


def main():
    copy_static_files()
    generate_pages_r("./content", "./template.html",
                     "./public")


main()
