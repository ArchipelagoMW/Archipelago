"""This module provides an enum of the different types a vendor can have"""
from enum import IntEnum


class RAC3VENDORTYPE(IntEnum):
    """Enum of the different types a vendor can have"""
    WEAPON = 0
    MOD = 1  # Unused from RaC2
    SHIP = 2
    ARMOR = 3
    SKIN = 5
