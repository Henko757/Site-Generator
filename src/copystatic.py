import os
import shutil


def copy_static(source, destination):
    """
    Recursively copy all files and folders from the source
    directory to the destination directory.

    If the destination already exists, it is deleted first
    to ensure a clean copy.
    """

    # Delete the destination directory if it already exists
    if os.path.exists(destination):
        print(f"Deleting directory: {destination}")
        shutil.rmtree(destination)

    # Create the destination directory
    print(f"Creating directory: {destination}")
    os.mkdir(destination)

    # Begin recursive copy
    copy_directory(source, destination)


def copy_directory(source, destination):
    """
    Recursively copy the contents of one directory into another.
    """

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)

        else:
            print(f"Creating directory: {destination_path}")
            os.mkdir(destination_path)

            copy_directory(source_path, destination_path)