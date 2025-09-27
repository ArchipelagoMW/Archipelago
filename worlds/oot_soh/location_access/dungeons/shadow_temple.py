from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from ...Regions import double_link_regions
from ...Items import SohItem
from ...Locations import SohLocation, SohLocationData
from ...Enums import *
from ...LogicHelpers import add_locations, connect_regions

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    
}


def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_rules(world)

def set_rules(world: "SohWorld") -> None:
    player = world.player
    
