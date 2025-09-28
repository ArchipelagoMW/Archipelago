from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import add_locations, connect_regions

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
