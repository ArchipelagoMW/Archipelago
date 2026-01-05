from pathlib import Path

from . import logger, BaseModpack

modpacks: dict[str, BaseModpack] = {}
"""
all the initializes modpacks
"""

def init_modpacks(modpackType: type[BaseModpack]) -> None:
    """
    This initializes all mod packs it can find
    it checks all locations found in modpack_directories

    This should be run after modpackType is set by the apworld
    """
    modpack_directories = modpackType.modpack_directories
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