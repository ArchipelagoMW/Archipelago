from typing import TYPE_CHECKING, Dict, List, Tuple

from BaseClasses import Region, ItemClassification, Entrance
from .data import data
from .items import PokemonCrystalItem
from .locations import PokemonCrystalLocation
from .options import FreeFlyLocation
from .rules import can_map_card_fly

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


class RegionData:
    name: str
    exits: List[str]
    locations: List[str]


FLY_REGIONS = {22: "REGION_ECRUTEAK_CITY",
               21: "REGION_OLIVINE_CITY",
               19: "REGION_CIANWOOD_CITY",
               23: "REGION_MAHOGANY_TOWN",
               25: "REGION_BLACKTHORN_CITY",
               3: "REGION_VIRIDIAN_CITY",
               4: "REGION_PEWTER_CITY",
               5: "REGION_CERULEAN_CITY",
               7: "REGION_VERMILION_CITY",
               8: "REGION_LAVENDER_TOWN",
               10: "REGION_CELADON_CITY",
               9: "REGION_SAFFRON_CITY",
               11: "REGION_FUCHSIA_CITY"}


def create_regions(world: PokemonCrystalWorld) -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    johto_only = world.options.johto_only.value

    for region_name, region_data in data.regions.items():
        if region_data.johto or not johto_only or (region_data.silver_cave and johto_only == 2):
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
        src_ok = data.regions[source].johto or (data.regions[source].silver_cave and johto_only > 1) or not johto_only
        dest_ok = data.regions[dest].johto or (data.regions[dest].silver_cave and johto_only > 1) or not johto_only
        if src_ok and dest_ok:
            regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")
    regions["Menu"].connect(regions["REGION_FLY"], "Fly")

    return regions


def setup_free_fly(world: PokemonCrystalWorld):
    fly = world.get_region("REGION_FLY")
    free_fly_location = FLY_REGIONS[world.free_fly_location]
    fly_region = world.get_region(free_fly_location)
    connection = Entrance(
        world.player,
        f"REGION_FLY -> {free_fly_location}",
        fly
    )
    fly.exits.append(connection)
    connection.connect(fly_region)

    if world.options.free_fly_location == FreeFlyLocation.option_free_fly_and_map_card:
        map_card_fly_location = FLY_REGIONS[world.map_card_fly_location]
        map_card_region = world.get_region(map_card_fly_location)
        connection = Entrance(
            world.player,
            f"REGION_FLY -> {map_card_fly_location}",
            fly
        )
        connection.access_rule = lambda state: can_map_card_fly(state, world)
        fly.exits.append(connection)
        connection.connect(map_card_region)
