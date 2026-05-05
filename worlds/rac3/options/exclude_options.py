"""This module provides a list of Excluded locations for the Rac3 apworld"""

from Options import ExcludeLocations
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.vendors import RAC3VENDORLOCATION


class RAC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({RAC3TAG.UNSTABLE, RAC3VENDORLOCATION.NGPLUS_RY3N0})
