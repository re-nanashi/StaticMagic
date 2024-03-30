import os
import shutil


def copy_files_r(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(source_dir_path):
        src_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path):
            try:
                shutil.copy(src_path, dest_path)
                print(
                    f"File({src_path}) was copied to {dest_path} successfully.")
            except shutil.SameFileError:
                raise Exception(
                    "Source and destination represents the same file.")
            except PermissionError:
                raise Exception("Permission denied.")
            except:
                raise Exception("Error occured while copying file.")
        else:
            copy_files_r(src_path, dest_path)
