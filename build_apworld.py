import argparse
import importlib
import os
import sys
import zipfile
from pathlib import Path
from typing import Optional, Type, TypeAlias

import orjson

from worlds import AutoWorldRegister
from worlds.AutoWorld import World
from worlds.Files import APWorldContainer

StrPath: TypeAlias = str | os.PathLike[str]

MANIFEST_NAME = "archipelago.json"
ZIP_EXCLUDE = {
    ".DS_STORE",
    ".pytest_cache",
    "__MACOSX",
    "__pycache__"
}


def main(
    input_path: StrPath,
    output_path: StrPath = os.curdir,
    apworld_name: Optional[str] = None,
    world_type: Optional[Type[World]] = None
) -> str:
    """
    Creates an apworld file at output_path containing the directory at input_path.
    Note: some common dirs/files that should not be packaged are automatically excluded (see ZIP_EXCLUDE).

    The apworld spec can be found here: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld%20specification.md

    :param input_path: Path to the directory which will be used as the contents of the apworld
    :param output_path: Path to the directory into which the created apworld file will be put
    :param apworld_name: Name for the apworld file and its contained directory. Defaults to input_path directory name
    :param world_type: The worlds.AutoWorld.World type for this apworld. If omitted, it will be found/loaded automatically.
    (world_type's presence is an optimization in case the caller already has it)
    """

    if not isinstance(input_path, Path):
        input_path = Path(input_path)

    assert input_path.is_dir(), f"{input_path} is not a directory or does not exist"

    os.makedirs(output_path, exist_ok=True)

    if apworld_name is None:
        apworld_name = input_path.name

    if world_type:
        assert _is_world_type_from_path(world_type, input_path), \
            f"Expected {world_type} from {input_path}; was {world_type.__file__}"

        game_name = world_type.game
    else:
        game_name = _find_or_load_world_type(input_path).game

    zip_path = os.path.join(output_path, apworld_name + ".apworld")

    apworld = APWorldContainer(zip_path)
    apworld.game = game_name
    apworld.manifest_path = os.path.join(input_path, MANIFEST_NAME)

    if os.path.isfile(apworld.manifest_path):
        manifest = orjson.loads(open(apworld.manifest_path).read())
    else:
        manifest = {}

    manifest.update(apworld.get_manifest())

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED,
        compresslevel=9,
	    strict_timestamps=False
    ) as zf:
        for path in input_path.rglob("*"):
            excluded = False
            relative_path = Path(apworld_name, path.relative_to(input_path))

            for exclude in ZIP_EXCLUDE:
                if exclude in str(relative_path):
                    excluded = True
                    break

            if excluded:
                continue

            if not relative_path.name == MANIFEST_NAME:
                zf.write(path, relative_path)

        zf.writestr(os.path.join(apworld_name, MANIFEST_NAME), orjson.dumps(manifest))

    return zip_path


def _find_or_load_world_type(path: Path) -> Type[World]:
    world_type = _find_registered_world_type_for_path(path)

    if world_type is None:
        path_parent = str(Path(path.parent).resolve())

        if path_parent not in sys.path:
            sys.path.insert(0, path_parent)

        importlib.import_module(path.name)

        world_type = _find_registered_world_type_for_path(path)

    if world_type is None:
        raise KeyError(f"Module at {path} did not register a World type")

    return world_type


def _find_registered_world_type_for_path(path: Path) -> Optional[Type[World]]:
    return next(
        (
            # dicts keep insertion order, so if we just added a world, it'll be last, hence the reversed
            world_type for _, world_type in reversed(AutoWorldRegister.world_types.items())
            if _is_world_type_from_path(world_type, path)
        ),
        None
    )


def _is_world_type_from_path(world_type: Type[World], path: Path) -> bool:
    return Path(world_type.__file__).is_relative_to(path.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Path to the apworld dir")
    parser.add_argument("-n", "--apworld-name", default=None, help="Name of the built apworld")
    parser.add_argument("-o", "--output-path", default=os.curdir, help="Path to place the built apworld")

    args = parser.parse_args()

    main(
        apworld_name=args.apworld_name,
        input_path=args.input_path,
        output_path=args.output_path
    )
