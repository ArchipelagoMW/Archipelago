from worlds.rac3.constants.locations.Rac3Tags import RAC3TAG
from Options import ExcludeLocations


class RAC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({RAC3TAG.UNSTABLE, RAC3TAG.LONG_TROPHY})
