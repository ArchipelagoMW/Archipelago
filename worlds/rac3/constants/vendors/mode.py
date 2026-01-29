"""This module provides an enum of the different weapon vendor modes"""


from enum import Enum


class RAC3VENDORMODE(Enum):
    """Enum for each mode the weapon vendor can be in"""
    CLOSED = 0
    GADGETRON = 1
    SLIMCOGNITO = 2