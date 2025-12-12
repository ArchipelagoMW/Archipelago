from dataclasses import dataclass
from typing import Optional

from worlds.rac3.constants.data.position import RAC3POSITIONDATA
from worlds.rac3.constants.region import (PLANET_CHECKPOINT, PLANET_MENU_OFFSET, PLANET_NAME_FROM_ID, RAC3REGION,
                                          RESPAWN_COORDS_OFFSET)
from worlds.rac3.constants.status import RAC3STATUS


@dataclass
class RAC3REGIONDATA:
    ID: int = None
    SLOT_ADDRESS: Optional[int] = None
    CHECKPOINT: Optional[RAC3POSITIONDATA] = None
    PAUSE_ADDRESS: Optional[int] = None
    RESPAWN_COORDS_ADDRESS: Optional[int] = None

    def __init__(self,
                 idx: Optional[int] = None,
                 slot: Optional[int] = None,
                 checkpoint: Optional[RAC3POSITIONDATA] = None,
                 pause_address: Optional[int] = None,
                 respawn_coords_address: Optional[int] = None):
        self.ID: Optional[int] = idx
        self.SLOT_ADDRESS: Optional[int] = slot
        self.CHECKPOINT: Optional[RAC3POSITIONDATA] = checkpoint
        self.PAUSE_ADDRESS: Optional[int] = pause_address
        self.RESPAWN_COORDS_ADDRESS: Optional[int] = respawn_coords_address

    @staticmethod
    def construct_slot(slot: int):
        idx: int = slot + 1
        addr: int = 4 * slot + RAC3STATUS.PLANET_SLOT_ADDRESS
        return RAC3REGIONDATA(idx, addr)

    @staticmethod
    def construct_planet(idx: int):
        name = PLANET_NAME_FROM_ID[idx]
        planet_address = PLANET_MENU_OFFSET[name] + RAC3STATUS.PAUSE_BASE
        checkpoint = PLANET_CHECKPOINT.get(name, None)
        respawn_coords_address = RESPAWN_COORDS_OFFSET.get(name, None)
        if respawn_coords_address is not None:  # Not all planets should have respawn coords changed
            respawn_coords_address += RAC3STATUS.RESPAWN_BASE
        return RAC3REGIONDATA(idx, checkpoint=checkpoint, pause_address=planet_address,
                              respawn_coords_address=respawn_coords_address)


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
    RAC3REGION.PHOENIX_ASSAULT: RAC3REGIONDATA.construct_planet(0x06),
    RAC3REGION.UNUSED: RAC3REGIONDATA(0x0F),
    RAC3REGION.COMMAND_CENTER_2: RAC3REGIONDATA.construct_planet(0x14),
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK: RAC3REGIONDATA.construct_planet(0x17),
    RAC3REGION.UNUSED_2: RAC3REGIONDATA(0x19),
    RAC3REGION.METROPOLIS_RANGERS: RAC3REGIONDATA.construct_planet(0x1A),
    RAC3REGION.AQUATOS_BASE: RAC3REGIONDATA.construct_planet(0x1B),
    RAC3REGION.AQUATOS_SEWERS: RAC3REGIONDATA.construct_planet(0x1C),
    RAC3REGION.TYHRRANOSIS_RANGERS: RAC3REGIONDATA.construct_planet(0x1D),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_1: RAC3REGIONDATA(0x1E),
    RAC3REGION.QWARK_VID_COMIC_1: RAC3REGIONDATA(0x1F, pause_address=RAC3STATUS.VIDCOMIC_PAUSE),
    RAC3REGION.QWARK_VID_COMIC_4: RAC3REGIONDATA(0x20, pause_address=RAC3STATUS.VIDCOMIC_PAUSE),
    RAC3REGION.QWARK_VID_COMIC_2: RAC3REGIONDATA(0x21, pause_address=RAC3STATUS.VIDCOMIC_PAUSE),
    RAC3REGION.QWARK_VID_COMIC_3: RAC3REGIONDATA(0x22, pause_address=RAC3STATUS.VIDCOMIC_PAUSE),
    RAC3REGION.QWARK_VID_COMIC_5: RAC3REGIONDATA(0x23, pause_address=RAC3STATUS.VIDCOMIC_PAUSE),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_2: RAC3REGIONDATA(0x24),
    RAC3REGION.MENU: RAC3REGIONDATA(0xFF),
    RAC3REGION.SLOT_0: RAC3REGIONDATA.construct_slot(slot=0x00),
    RAC3REGION.SLOT_1: RAC3REGIONDATA.construct_slot(slot=0x01),
    RAC3REGION.SLOT_2: RAC3REGIONDATA.construct_slot(slot=0x02),
    RAC3REGION.SLOT_3: RAC3REGIONDATA.construct_slot(slot=0x03),
    RAC3REGION.SLOT_4: RAC3REGIONDATA.construct_slot(slot=0x04),
    RAC3REGION.SLOT_5: RAC3REGIONDATA.construct_slot(slot=0x05),
    RAC3REGION.SLOT_6: RAC3REGIONDATA.construct_slot(slot=0x06),
    RAC3REGION.SLOT_7: RAC3REGIONDATA.construct_slot(slot=0x07),
    RAC3REGION.SLOT_8: RAC3REGIONDATA.construct_slot(slot=0x08),
    RAC3REGION.SLOT_9: RAC3REGIONDATA.construct_slot(slot=0x09),
    RAC3REGION.SLOT_A: RAC3REGIONDATA.construct_slot(slot=0x0A),
    RAC3REGION.SLOT_B: RAC3REGIONDATA.construct_slot(slot=0x0B),
    RAC3REGION.SLOT_C: RAC3REGIONDATA.construct_slot(slot=0x0C),
    RAC3REGION.SLOT_D: RAC3REGIONDATA.construct_slot(slot=0x0D),
    RAC3REGION.SLOT_E: RAC3REGIONDATA.construct_slot(slot=0x0E),
    RAC3REGION.SLOT_F: RAC3REGIONDATA.construct_slot(slot=0x0F),
    RAC3REGION.SLOT_10: RAC3REGIONDATA.construct_slot(slot=0x10),
    RAC3REGION.SLOT_11: RAC3REGIONDATA.construct_slot(slot=0x11),
    RAC3REGION.SLOT_12: RAC3REGIONDATA.construct_slot(slot=0x12),
    RAC3REGION.SLOT_13: RAC3REGIONDATA.construct_slot(slot=0x13),
}
