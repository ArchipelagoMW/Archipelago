# TODO: handle data
# TODO: handle clients
# TODO: handle yaml templates

import json
import os.path
import platform
import sys
import zipfile
from pathlib import Path
from .AutoWorld import World

METADATA_KEYS = [
    "game",
    "file_types",
    # license
    # description
    # maintainers
]

VERSION_KEYS = [
    "world_version",
    "min_generator_version",
    "max_generator_version",
]


def create_world_meta(world_key, world_type, is_frozen):
    metadata = {}
    for key in METADATA_KEYS:
        if getattr(world_type, key, None):  # avoid writing optional keys if they aren't set
            metadata[key] = getattr(world_type, key)
    for key in VERSION_KEYS:
        if getattr(world_type, key, None):  # avoid writing optional keys if they aren't set
            metadata[key] = getattr(world_type, key).as_simple_string()
    if world_type.__doc__ != World.__doc__:
        metadata["description"] = world_type.__doc__.strip()
    metadata["game_id"] = world_key
    metadata["frozen"] = is_frozen
    if is_frozen:
        metadata["arch"] = platform.machine()
        metadata["os"] = platform.system()  # TODO: linux
        metadata["pyversion"] = f"{sys.version_info[0]}.{sys.version_info[1]}"
    else:
        metadata["arch"] = "any"
        metadata["os"] = "any"
        metadata["pyversion"] = "any"
    return metadata


def export_world(libfolder, world_type, output_dir, is_frozen):
    world_key = os.path.split(os.path.dirname(world_type.__file__))[1]
    world_directory = libfolder / "worlds" / world_key

    metadata = create_world_meta(world_key, world_type, is_frozen)

    arch = metadata["arch"]
    os_type = metadata["os"]
    base_file_name = f"{world_key}"
    parts = [base_file_name]
    if arch != "any":
        parts.append(arch)
    if os_type != "any":
        parts.append(os_type)
    if metadata['pyversion'] != "any":
        parts.append(f"py{metadata['pyversion']}")
    if metadata["world_version"] != "0.0.0":
        parts.append(metadata["world_version"])
    world_file_name = f"{'-'.join(parts)}.apworld"

    output_name = output_dir / world_file_name
    with zipfile.ZipFile(output_name, "x", zipfile.ZIP_DEFLATED,
                         compresslevel=9) as zf:
        for path in world_directory.rglob("*.*"):
            relative_path = os.path.join(*path.parts[path.parts.index("worlds") + 1:])
            if any(part.startswith(".") or part == "__pycache__" for part in Path(relative_path).parts):
                continue
            zf.write(path, relative_path)
        zf.writestr(os.path.join(world_key, "metadata.json"), json.dumps(metadata, indent=4))
        zf.close()
    return output_name

