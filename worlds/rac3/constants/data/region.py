"""This module contains the dataclass for levels in the game and exportable constants"""
from dataclasses import dataclass

from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.region import (PLANET_LOAD_OFFSET, PLANET_MENU_OFFSET, PLANET_NAME_FROM_ID,
                                          PLANET_SPECIAL_OFFSET, PLANET_VENDOR_OFFSET, RAC3REGION,
                                          RESPAWN_COORDS_OFFSET)
from worlds.rac3.constants.status import RAC3STATUS


@dataclass
class RAC3REGIONDATA:
    """Data class for each level of the game"""
    ID: int
    PLANET_TO_LOAD: int
    PAUSE_ADDRESS: int
    PLANET_SPECIAL_OFFSET: int
    RESPAWN_COORDS_ADDRESS: int | None
    VENDOR_OFFSET: int | None
    VISIT_ADDRESS: int
    ACCESS_ADDRESS: int

    def __init__(self,
                 idx: int,
                 planet_to_load_address: int = 0,
                 pause_address: int = 0,
                 planet_special_offset: int = 0,
                 respawn_coords_address: int | None = None,
                 vendor_offset: int | None = 0):
        self.ID: int = idx
        self.PLANET_TO_LOAD: int = planet_to_load_address
        self.PAUSE_ADDRESS: int = pause_address
        self.PLANET_SPECIAL_OFFSET: int = planet_special_offset
        self.RESPAWN_COORDS_ADDRESS: int | None = respawn_coords_address
        self.VENDOR_OFFSET: int | None = vendor_offset
        self.VISIT_ADDRESS: int = RAC3STATUS.VISITED_BASE + idx
        self.ACCESS_ADDRESS: int = RAC3STATUS.INFOBOT_BASE + idx

    @staticmethod
    def construct_planet(idx: int):
        """
        Generic planet constructor, makes each planet into region data given the data in the RAC3_REGION_DATA_TABLE
        """
        name = PLANET_NAME_FROM_ID[idx]
        pause = PLANET_MENU_OFFSET[name] + RAC3STATUS.PAUSE_BASE
        load = PLANET_LOAD_OFFSET[name] + RAC3STATUS.PLANET_LOAD_BASE
        offset = PLANET_SPECIAL_OFFSET.get(name, 0)
        respawn_coords_address = RESPAWN_COORDS_OFFSET.get(name, None)
        if respawn_coords_address is not None:  # Not all planets should have respawn coords changed
            respawn_coords_address += RAC3STATUS.RESPAWN_BASE
        vendor_offset = PLANET_VENDOR_OFFSET.get(name, None)
        if vendor_offset is not None:
            vendor_offset += RAC3STATUS.VENDOR_BASE
        return RAC3REGIONDATA(idx, load, pause, offset, respawn_coords_address, vendor_offset)


RAC3_REGION_DATA_TABLE: dict[str, RAC3REGIONDATA] = {
    # Regions
    RAC3REGION.VELDIN: RAC3REGIONDATA.construct_planet(0x01),
    RAC3REGION.FLORANA: RAC3REGIONDATA.construct_planet(0x02),
    RAC3REGION.STARSHIP_PHOENIX: RAC3REGIONDATA.construct_planet(0x03),
    RAC3REGION.MARCADIA: RAC3REGIONDATA.construct_planet(0x04),
    RAC3REGION.DAXX: RAC3REGIONDATA.construct_planet(0x05),
    RAC3REGION.ANNIHILATION_NATION: RAC3REGIONDATA.construct_planet(0x07),
    RAC3REGION.AQUATOS: RAC3REGIONDATA.construct_planet(0x08),
    RAC3REGION.TYHRRANOSIS: RAC3REGIONDATA.construct_planet(0x09),
    RAC3REGION.ZELDRIN_STARPORT: RAC3REGIONDATA.construct_planet(0x0A),
    RAC3REGION.OBANI_GEMINI: RAC3REGIONDATA.construct_planet(0x0B),
    RAC3REGION.BLACKWATER_CITY: RAC3REGIONDATA.construct_planet(0x0C),
    RAC3REGION.HOLOSTAR_STUDIOS: RAC3REGIONDATA.construct_planet(0x0D),
    RAC3REGION.KOROS: RAC3REGIONDATA.construct_planet(0x0E),
    RAC3REGION.METROPOLIS: RAC3REGIONDATA.construct_planet(0x10),
    RAC3REGION.CRASH_SITE: RAC3REGIONDATA.construct_planet(0x11),
    RAC3REGION.ARIDIA: RAC3REGIONDATA.construct_planet(0x12),
    RAC3REGION.QWARKS_HIDEOUT: RAC3REGIONDATA.construct_planet(0x13),
    RAC3REGION.OBANI_DRACO: RAC3REGIONDATA.construct_planet(0x15),
    RAC3REGION.COMMAND_CENTER: RAC3REGIONDATA.construct_planet(0x16),
    RAC3REGION.MUSEUM: RAC3REGIONDATA.construct_planet(0x18),
    RAC3REGION.GALAXY: RAC3REGIONDATA(0x00),
    RAC3REGION.SKIDD_CUTSCENE: RAC3REGIONDATA(0x00),
    RAC3REGION.NANOTECH: RAC3REGIONDATA(0x00),
    RAC3REGION.NGPLUS: RAC3REGIONDATA(0x00),
    RAC3REGION.UPGRADES: RAC3REGIONDATA(0x00),
    # Do not contain locations
    RAC3REGION.PHOENIX_ASSAULT: RAC3REGIONDATA.construct_planet(0x06),
    RAC3REGION.UNUSED: RAC3REGIONDATA(0x0F),
    RAC3REGION.COMMAND_CENTER_2: RAC3REGIONDATA.construct_planet(0x14),
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK: RAC3REGIONDATA.construct_planet(0x17),
    RAC3REGION.UNUSED_2: RAC3REGIONDATA(0x19),
    RAC3REGION.METROPOLIS_RANGERS: RAC3REGIONDATA.construct_planet(0x1A),
    RAC3REGION.AQUATOS_BASE: RAC3REGIONDATA.construct_planet(0x1B),
    RAC3REGION.AQUATOS_SEWERS: RAC3REGIONDATA.construct_planet(0x1C),
    RAC3REGION.TYHRRANOSIS_RANGERS: RAC3REGIONDATA.construct_planet(0x1D),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_1: RAC3REGIONDATA(0x1E, PLANET_LOAD_OFFSET[
        RAC3REGION.QWARK_VID_COMIC_UNUSED_1] + RAC3STATUS.PLANET_LOAD_BASE),
    RAC3REGION.QWARK_VID_COMIC_1: RAC3REGIONDATA.construct_planet(0x1F),
    RAC3REGION.QWARK_VID_COMIC_4: RAC3REGIONDATA.construct_planet(0x20),
    RAC3REGION.QWARK_VID_COMIC_2: RAC3REGIONDATA.construct_planet(0x21),
    RAC3REGION.QWARK_VID_COMIC_3: RAC3REGIONDATA.construct_planet(0x22),
    RAC3REGION.QWARK_VID_COMIC_5: RAC3REGIONDATA.construct_planet(0x23),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_2: RAC3REGIONDATA(0x24, PLANET_LOAD_OFFSET[
        RAC3REGION.QWARK_VID_COMIC_UNUSED_2] + RAC3STATUS.PLANET_LOAD_BASE),
    RAC3REGION.MENU: RAC3REGIONDATA(0xFF),
}
PLANET_FROM_INFOBOT: dict[str, str] = {
    RAC3ITEM.VELDIN: RAC3REGION.VELDIN,
    RAC3ITEM.FLORANA: RAC3REGION.FLORANA,
    RAC3ITEM.STARSHIP_PHOENIX: RAC3REGION.STARSHIP_PHOENIX,
    RAC3ITEM.MARCADIA: RAC3REGION.MARCADIA,
    RAC3ITEM.ANNIHILATION_NATION: RAC3REGION.ANNIHILATION_NATION,
    RAC3ITEM.AQUATOS: RAC3REGION.AQUATOS,
    RAC3ITEM.TYHRRANOSIS: RAC3REGION.TYHRRANOSIS,
    RAC3ITEM.DAXX: RAC3REGION.DAXX,
    RAC3ITEM.OBANI_GEMINI: RAC3REGION.OBANI_GEMINI,
    RAC3ITEM.BLACKWATER_CITY: RAC3REGION.BLACKWATER_CITY,
    RAC3ITEM.HOLOSTAR_STUDIOS: RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3ITEM.OBANI_DRACO: RAC3REGION.OBANI_DRACO,
    RAC3ITEM.ZELDRIN_STARPORT: RAC3REGION.ZELDRIN_STARPORT,
    RAC3ITEM.METROPOLIS: RAC3REGION.METROPOLIS,
    RAC3ITEM.CRASH_SITE: RAC3REGION.CRASH_SITE,
    RAC3ITEM.ARIDIA: RAC3REGION.ARIDIA,
    RAC3ITEM.QWARKS_HIDEOUT: RAC3REGION.QWARKS_HIDEOUT,
    RAC3ITEM.KOROS: RAC3REGION.KOROS,
    RAC3ITEM.COMMAND_CENTER: RAC3REGION.COMMAND_CENTER,
    RAC3ITEM.MUSEUM: RAC3REGION.MUSEUM,
}
INFOBOT_FROM_PLANET: dict[str, str] = {v: k for k, v in PLANET_FROM_INFOBOT.items()}
SHORTCUT_FROM_PLANET: dict[str, list[str]] = {
    RAC3REGION.VELDIN: [],
}
