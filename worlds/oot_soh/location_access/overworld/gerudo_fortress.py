from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (add_locations, connect_regions)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
