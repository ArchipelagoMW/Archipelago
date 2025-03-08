import datetime
from io import BufferedReader
import json
import os
import pkgutil
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

def parse_string(fp: BufferedReader, delimiter: str = b'\x00') -> str:
    """
    Read a string starting at the file pointer up until the first x00 byte delimiter.
    The result will be decoded in utf-8 format.

    Args:
        fp (BufferedReader): The file pointer to start reading at.
        delimiter (str): A 1 character byte string to use as a delimiter.
    Raises:
        IOError: Error during read.
    """
    string = b""
    while True:
        byte = fp.read(1)
        if byte == delimiter:
            break
        string += byte
    return string.decode("utf-8")

def write_item_id_to_desc(ittxt_path: str, output_path: str) -> None:
    """
    This method is used to read the state of t_ittxt._dt / t_ittxt2._dt
    to parse the items to a specified file for debugging purposes.

    Args:
        ittxt_path (str): The path to t_ittxt._dt / t_ittxt2._dt
        output_path (str): The path to write the contents to
    """
    offsets = []
    items = []
    with open (ittxt_path, "rb") as fp:
        with open (output_path, "w", encoding="utf-8") as item_id_to_name_fp:
            first_item_addr = int.from_bytes(fp.read(2), byteorder="little")
            fp.seek(0)
            while fp.tell() < first_item_addr:
                item_offset = int.from_bytes(fp.read(2), byteorder="little")
                offsets.append(item_offset)
            for idx in range(len(offsets)):  # pylint: disable=consider-using-enumerate
                fp.seek(offsets[idx])
                item_id = int.from_bytes(fp.read(4), byteorder="little")
                fp.seek(offsets[idx] + 8)
                try:
                    name = parse_string(fp)
                    desc = parse_string(fp)
                except Exception:
                    pass
                item_id_to_name_fp.write(f"{item_id} {name} {desc}\n")
    return items


def load_file(path):
    data = pkgutil.get_data(__name__, path)
    if data is None:
        raise FileNotFoundError(f"{path!r} not found in {__name__}")
    return data
