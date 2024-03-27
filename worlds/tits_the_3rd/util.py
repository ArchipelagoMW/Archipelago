import datetime
import json
import os
import shutil

DEFAULT_DEV_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dev_util/dev_config.json")

def _raise_malformed_config_error(field: str):
    """
    Raise an error from the given field

    :str field: The field to raise the rror on
    """
    print(f"Error reading field {field} in dev_config.json. Pleae see readme.md for setup")
    raise ValueError(field)

def assert_path_exists(path: str):
    """
    Check if the provided directory exists. Raise an error otherwise.

    :str path: The path to check if it exists.

    Raises:
    :FileNotFoundError: If the path does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path '{path}' does not exist.")

def copy_contents(source: str, destination: str, only_copy: list[str] = None):
    """
    Copy the contents from the source directory into the destination directory.

    :str source: the source directory
    :str destination: the destination directory
    :list[str] (optional) only_copy: Only copy the specified files
    """
    items = os.listdir(source) if not only_copy else only_copy
    for item in items:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)

def delete_contents(directory: str):
    """
    Delete the contents of the provided directory

    :str directory: The directory in question.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def read_dev_config_and_assert_contents(config_path = DEFAULT_DEV_CONFIG_PATH) -> dict:
    """
    Reads the dev config for running development scripts and returns it as a dict.

    :str config_path: The path to the config.
    """
    config = None
    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
    except FileNotFoundError as err:
        print(f"Unable to find {config_path}.")
        raise err
    for field in ["gameDirectory", "lbARKDirectory"]:
        if field not in config:
            _raise_malformed_config_error(field)
    return config

def get_tooling_path(filename: str):
    """
    Get the path of a tool in the external_tools subdirectory

    :str filename: The name of the file to get in the external_tools subdirectory
    """
    patch_dir = os.path.dirname(os.path.realpath(__file__))
    tools_dir = os.path.join(patch_dir, "external_tools")
    tool_path = os.path.join(tools_dir, filename)
    assert_path_exists(tool_path)
    return tool_path

def move_contents_with_file_ending(source: str, destination: str, file_ending: str):
    """
    Move the contents of source which end in the file_ending extention into
    the destination directory

    :str source: the source directory
    :str destination: the destination directory
    :str file_ending: the file extention to match against
    """
    for root, _, files in os.walk(source):
        for file in files:
            if file.endswith(file_ending):
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(destination, file)
                shutil.move(src_file_path, dst_file_path)

def prompt_and_create_backup(backup_directory: str, copy_from_directory: str):
    """
    Prompt the user for a backup. If they answer yes,
    copy the contents from the copy_from directory into a backup created inside the backup_directory.

    :str backup_directory: The directory to create the backup in.
    :str copy_from_directory: The directory to copy the contents from.
    """
    response = None
    while not response or response.lower() not in ["yes", "y", "no", "n"]:
        response = input(f"The directory '{copy_from_directory}' already has contents. Do you want to make a backup up before overwriting? (y/n): ")
        if response.lower() in ("yes", "y"):
            backup_name = datetime.datetime.now().strftime("backup-%Y-%m-%d-%H-%M-%S")
            backup_path = os.path.join(backup_directory, backup_name)
            os.makedirs(backup_path)
            copy_contents(copy_from_directory, backup_path)
            print(f"created backup at directory {backup_path}")
        elif response.lower() not in ["no", "n"]:
            print("invalid response. Please enter y/n")
