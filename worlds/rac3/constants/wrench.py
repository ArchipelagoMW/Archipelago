"""This module provides constant address offsets, for use when reading data regarding the OmniWrench"""

from worlds.rac3.constants.region import WRENCH_FUNCTION_OFFSET
from worlds.rac3.constants.status import RAC3STATUS


class RAC3WRENCH:
    """Base struct for the Wrench function data, containing common address offsets"""
    NANOTECH_THRESHOLD_OFFSET: int = 0x2B0 # Contains the instruction that holds the Nanotech required to reach a certain upgrade.
    NANOTECH_DIFFERENCE_CHECK_OFFSET: int = 0x2B4 # Example: For V2, this address contains the decimal number 25. 25 + 15 = 40, OmniWrench V3.
    UPGRADE_ID_OFFSET: int = 0x2BC # Contains the ID that will be written to the BASE_ITEM_ID.
    BASE_ITEM_ID_OFFSET: int = 0x350 # Contains the item ID that the function will write to. If 00 or 01, the OmniWrench is decoupled from Nanotech
                                     # and the function will write there instead.
    PER_LEVEL_OFFSET: int = 0x18 # Starting at WRENCH_FUNCTION_BASE + NANOTECH_THRESHOLD_OFFSET, 
                                 # every +0x18 will contain an upgrade. +0x90 directly jumps from V2 to V8.  

    @staticmethod
    def get_wrench_property_address(planet: str) -> int:
        """Provides the wrench property address for reading data"""
        addr = RAC3STATUS.WRENCH_FUNCTION_BASE + WRENCH_FUNCTION_OFFSET[planet]
        return addr