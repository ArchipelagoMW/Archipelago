import logging
from pathlib import Path
from typing import TypeVar
from zipfile import ZipFile, Path as ZipPath

from . import BaseModpack

logger = logging.getLogger(f"APModpackManager - factorio with modpacks: PackLoader")

U = TypeVar('U', bound=BaseModpack)
modpacks: dict[str, U] = {}
"""
all the initializes modpacks
"""
def init_modpacks(modpackType: type[U]) -> None:
    """
    This initializes all mod packs it can find
    it checks all locations found in modpack_directories

    This should be run after modpackType is set by the apworld
    """
    modpack_directories = modpackType.modpack_directories
    logger.debug("Initializing modpack manager")
    for directory, filesystems in modpack_directories:
        logger.debug(f"Looking for modpacks in {directory}")
        for modpack_header in directory.glob("*/header.json"):
            modpackPath: Path = modpack_header.parent
            logger.debug(f"Found modpack in: {modpackPath}")
            modpack = modpackType(modpackPath, filesystems=filesystems)
            if modpack.packName in modpacks:
                raise Exception(f"Modpack already initialized: {modpack.packName}")
            modpacks[modpack.packName] = modpack
        for zip_path in directory.glob("*.zip"):
            zip_filesystem = ZipFile(zip_path)
            filesystems_copy = filesystems.copy()
            filesystems_copy.append(zip_filesystem)
            root = ZipPath(zip_filesystem)
            if not (root / "header.json").exists():
                zip_filesystem.close()
                continue
            logger.debug(f"Found zip modpack in: {zip_path.resolve()}")
            modpack = modpackType(root, filesystem=filesystems_copy)
            if modpack.packName in modpacks:
                raise Exception(f"Modpack already initialized: {modpack.packName}")
            modpacks[modpack.packName] = modpack