"""Reads a JSONC file and generates classes or dictionaries based on the data."""

import json
import re
import os
from js import getStringFile
from enum import IntEnum, auto
import pathlib


def remove_comments(jsonc_str):
    """Remove comments from a JSONC string."""
    # Remove single-line comments (//)
    jsonc_str = re.sub(r"//.*", "", jsonc_str)
    # Remove multi-line comments (/* ... */)
    jsonc_str = re.sub(r"/\*.*?\*/", "", jsonc_str, flags=re.DOTALL)
    return jsonc_str


def load_jsonc(filename):
    """Load a JSONC file, remove comments, and parse it into a dictionary."""
    jsonc_str = filename

    # Remove comments
    json_str = remove_comments(jsonc_str)

    # Parse JSON
    return json.loads(json_str)


def create_enum_class(name, values):
    """Dynamically create an Enum or IntEnum class based on the JSON data.

    If values are integers, an IntEnum is created, otherwise we process strings as objects.
    :param name: Name of the enum class
    :param values: Dictionary of enum members
    :return: Enum class or dict
    """
    enum_members = {key: auto() if value == "auto" else value for key, value in values.items()}

    # Check if all members are integers for IntEnum, or handle string eval for others
    if all(isinstance(value, int) for value in enum_members.values()):
        return IntEnum(name, enum_members)
    else:
        for key, value in enum_members.items():
            # Evaluate the string directly into an object reference
            if isinstance(value, str):
                enum_members[key] = eval(value, globals(), locals())
        return enum_members


def process_value(value):
    """Process a value that might contain a dictionary with an 'obj' key.

    If so, evaluate the 'obj' value into an object reference.
    """
    if isinstance(value, dict) and "obj" in value:
        return eval(value["obj"], globals(), locals())
    return value


def set_nested_dict(d, keys, value):
    """Recursively create nested dictionaries for keys containing periods.

    :param d: Dictionary to update
    :param keys: List of keys after splitting on period
    :param value: The value to set at the final nested key
    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def process_keys_with_period(data):
    """Recursively process a dictionary and handle keys with periods by creating nested dictionaries.

    Additionally, evaluate keys that are object references like SettingsStringEnum.blocker_0.
    :param data: The dictionary with keys to process
    :return: Processed dictionary with nested structures for keys containing periods
    """
    processed_data = {}

    for key, value in data.items():
        # Check if the key is an object reference, and evaluate it if so
        if is_object_reference(key):
            # Evaluate the key to turn it into an actual object reference
            evaluated_key = eval(key, globals(), locals())
            processed_data[evaluated_key] = value
        elif "." in key:
            keys = key.split(".")
            set_nested_dict(processed_data, keys, value)
        else:
            processed_data[key] = value

    return processed_data


def is_object_reference(key):
    """Determine if the key is an object reference (contains an enum or similar object reference).

    For simplicity, assume keys starting with 'SettingsStringEnum' are object references.
    :param key: Key to evaluate
    :return: True if the key should be treated as an object reference, False otherwise
    """
    # This can be extended with more logic to detect object references
    return key.startswith("SettingsStringEnum")


def generate_globals(path):
    """Load a JSONC file, process the data, and dynamically create classes or dictionaries.

    Handles nested keys and object references.
    :param path: Path to the JSONC file
    """
    # Replace the current path to find the JSONC file
    path = pathlib.Path(path).name
    path = "randomizer/Enums/" + path
    root, ext = os.path.splitext(path)
    # Handle case of cx_freeze turning jsonc into jsoncc
    if ext in (".py", ".pyc"):
        path = root + ".jsonc"

    # If the path starts with a slash, remove it
    if "\\" in path:
        path = path.replace("\\", "/")
    if path.startswith("/"):
        path = path[1:]
        # Verify the first character is not a slash
        if path.startswith("/"):
            path = path[1:]
    # Open and load the JSONC file
    f = getStringFile(path)
    enums_data = load_jsonc(f)

    new_globals = {}

    for enum_name, enum_values in enums_data.items():
        # Process the enum values to handle dicts with 'obj' keys
        processed_values = {key: process_value(value) for key, value in enum_values.items()}

        # Handle period in keys to convert them to nested objects
        processed_values = process_keys_with_period(processed_values)

        # Dynamically create the enum class or dictionary
        new_globals[enum_name] = create_enum_class(enum_name, processed_values)

        # Update globals with the new classes or objects
        globals().update(new_globals)

    return new_globals
