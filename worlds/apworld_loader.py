"""
Load world modules from .apworld zip files. Uses a custom meta path finder so that
import worlds.<name> can resolve to code inside a zip that is not on sys.path.
"""
from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import logging
import sys
import zipimport
from pathlib import Path
from types import ModuleType
from typing import Sequence

from Utils import version_tuple, messagebox
from zipfile import BadZipFile


# Module specs for apworld modules; the finder returns these so import finds the zip.
_module_specs: dict[str, importlib.machinery.ModuleSpec] = {}
_finder_inserted = False


class _APWorldModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(
        self,
        fullname: str,
        _path: Sequence[str] | None,
        _target: ModuleType = None,
    ) -> importlib.machinery.ModuleSpec | None:
        return _module_specs.get(fullname)


def load_apworld_by_path(path: str, failed_world_loads: list[str]) -> bool:
    """Load an apworld from the given path. Returns True if the world module was loaded."""
    global _finder_inserted
    from .Files import APWorldContainer, InvalidDataError
    from .AutoWorld import AutoWorldRegister

    if not _finder_inserted:
        sys.meta_path.insert(0, _APWorldModuleFinder())
        _finder_inserted = True

    try:
        apworld = APWorldContainer(path)
        apworld.read()
    except InvalidDataError as e:
        if version_tuple < (0, 7, 0):
            logging.error(
                f"Invalid or missing manifest file for {path}. "
                "This apworld will stop working with Archipelago 0.7.0."
            )
            logging.error(e)
            return False
        raise
    except BadZipFile as e:
        err_message = (
            f"The world source {path} is not a valid zip. "
            "It is likely either corrupted, or was packaged incorrectly."
        )
        if sys.stdout:
            raise RuntimeError(err_message) from e
        messagebox("Couldn't load worlds", err_message, error=True)
        sys.exit(1)

    if apworld.minimum_ap_version and apworld.minimum_ap_version > version_tuple:
        logging.warning(
            f"Did not load {path} as its minimum core version {apworld.minimum_ap_version} "
            f"is higher than current core version {version_tuple}."
        )
        failed_world_loads.append(apworld.game or path)
        return False
    if apworld.maximum_ap_version and apworld.maximum_ap_version < version_tuple:
        logging.warning(
            f"Did not load {path} as its maximum core version {apworld.maximum_ap_version} "
            f"is lower than current core version {version_tuple}."
        )
        failed_world_loads.append(apworld.game or path)
        return False
    if apworld.game and AutoWorldRegister.world_types.get(apworld.game) is not None:
        logging.warning(
            f"Did not load {path} as its game {apworld.game} is already loaded."
        )
        return False

    importer = zipimport.zipimporter(path)
    world_name = Path(path).stem
    spec = importer.find_spec(f"worlds.{world_name}")
    if spec is None:
        logging.warning(f"Could not find spec for worlds.{world_name} in {path}")
        return False
    _module_specs[f"worlds.{world_name}"] = spec
    try:
        importlib.import_module(f"worlds.{world_name}")
    except Exception:
        import traceback
        import io
        file_like = io.StringIO()
        print(f"Could not load apworld at {path}:", file=file_like)
        traceback.print_exc(file=file_like)
        file_like.seek(0)
        logging.exception(file_like.read())
        failed_world_loads.append(apworld.game or world_name)
        return False
    if apworld.game and apworld.world_version:
        cls = AutoWorldRegister.world_types.get(apworld.game)
        if cls is not None:
            cls.world_version = apworld.world_version
    return True


def forget_module(module_name: str) -> None:
    """Remove the module from the apworld finder and sys.modules so it can be loaded again.
    Call this when unloading a world that was loaded from an apworld."""
    _module_specs.pop(module_name, None)
    sys.modules.pop(module_name, None)
