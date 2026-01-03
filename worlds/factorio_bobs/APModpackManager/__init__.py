import logging
from pathlib import Path

from .BaseModpack import BaseModpack
from .ItemLocations import items_to_id, locations_to_id

logger = logging.getLogger(f"APModpackManager - factorio with modpacks")


modpack_directories: list[Path] = [Path(__file__).parent.parent / "InternalPacks"]
"""
all paths that should be checked for modpacks should be in modpack_directories
relative paths should be relative to ap root but should not be within an ap world
"""
modpacks: dict[str, BaseModpack] = {}
"""
all the initializes modpacks
"""
modpackType: type[BaseModpack] = BaseModpack
"""
should be set to a child of `BaseModpack` before initialising
"""

def init_modpacks() -> None:
    """
    This initializes all mod packs it can find
    it checks all locations found in modpack_directories

    This should be run after modpackType is set by the apworld
    """
    logger.debug("Initializing modpack manager")
    for directory in modpack_directories:
        logger.debug(f"Looking for modpacks in {directory.resolve()}")
        for modpack_header in directory.glob("*/header.json"):
            modpackPath: Path = modpack_header.parent
            logger.debug(f"Found modpack in: {modpackPath}")
            modpack = modpackType(modpackPath)
            if modpack.packName in modpacks:
                raise Exception(f"Modpack already initialized: {modpack.packName}")
            modpacks[modpack.packName] = modpack

def get_items() -> dict[str, int]:
    if items_to_id:
        return items_to_id
    if not modpacks:
        raise Exception("No modpacks found, ensure modpacks exist and that packs are initialized before calling get_items()")
    for modpack in modpacks.values():
        modpack.init_items()
    return items_to_id

def get_locations() -> dict[str, int]:
    if locations_to_id:
        return locations_to_id
    if not modpacks:
        raise Exception("No modpacks found, ensure modpacks exist and that packs are initialized before calling get_locations()")
    for modpack in modpacks.values():
        modpack.init_locations()
    return locations_to_id
