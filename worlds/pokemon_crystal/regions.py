from BaseClasses import Location, Region, Item, ItemClassification
from typing import TYPE_CHECKING, Dict, List, Tuple

from .data import data
from .locations import PokemonCrystalLocation
from .items import PokemonCrystalItem

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


class RegionData:
    name: str
    exits: List[str]
    locations: List[str]


def create_regions(world: PokemonCrystalWorld) -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []

    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, world.player, world.multiworld)

        regions[region_name] = new_region

        for event_data in region_data.events:
            event = PokemonCrystalLocation(world.player, event_data.name, new_region)
            event.show_in_spoiler = False
            event.place_locked_item(PokemonCrystalItem(
                event_data.name, ItemClassification.progression, None, world.player))
            new_region.locations.append(event)

        for region_exit in region_data.exits:
            connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    for name, source, dest in connections:
        regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")

    return regions
