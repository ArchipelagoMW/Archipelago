from typing import TYPE_CHECKING, Dict, List, Set
from BaseClasses import CollectionState, Location, LocationProgressType, Region, ItemClassification
from .data import data, LocationCategory, fly_blacklist_map
from .groups import location_groups
from .items import PokemonFRLGItem, get_random_item
from .options import ShuffleFlyUnlocks, ViridianCityRoadblock

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

fly_item_id_map = {
    "ITEM_FLY_NONE": 0,
    "ITEM_FLY_PALLET": 1,
    "ITEM_FLY_VIRIDIAN": 2,
    "ITEM_FLY_PEWTER": 3,
    "ITEM_FLY_CERULEAN": 4,
    "ITEM_FLY_LAVENDER": 5,
    "ITEM_FLY_VERMILION": 6,
    "ITEM_FLY_CELADON": 7,
    "ITEM_FLY_FUCHSIA": 8,
    "ITEM_FLY_CINNABAR": 9,
    "ITEM_FLY_INDIGO": 10,
    "ITEM_FLY_SAFFRON": 11,
    "ITEM_FLY_ONE_ISLAND": 12,
    "ITEM_FLY_TWO_ISLAND": 13,
    "ITEM_FLY_THREE_ISLAND": 14,
    "ITEM_FLY_FOUR_ISLAND": 15,
    "ITEM_FLY_FIVE_ISLAND": 16,
    "ITEM_FLY_SEVEN_ISLAND": 17,
    "ITEM_FLY_SIX_ISLAND": 18,
    "ITEM_FLY_ROUTE4": 19,
    "ITEM_FLY_ROUTE10": 20
}

fly_item_map = {
    "Pallet Town": "ITEM_FLY_PALLET",
    "Viridian City South": "ITEM_FLY_VIRIDIAN",
    "Pewter City": "ITEM_FLY_PEWTER",
    "Cerulean City": "ITEM_FLY_CERULEAN",
    "Lavender Town": "ITEM_FLY_LAVENDER",
    "Vermilion City": "ITEM_FLY_VERMILION",
    "Celadon City": "ITEM_FLY_CELADON",
    "Fuchsia City": "ITEM_FLY_FUCHSIA",
    "Cinnabar Island": "ITEM_FLY_CINNABAR",
    "Indigo Plateau": "ITEM_FLY_INDIGO",
    "Saffron City": "ITEM_FLY_SAFFRON",
    "One Island Town": "ITEM_FLY_ONE_ISLAND",
    "Two Island Town": "ITEM_FLY_TWO_ISLAND",
    "Three Island Town South": "ITEM_FLY_THREE_ISLAND",
    "Four Island Town": "ITEM_FLY_FOUR_ISLAND",
    "Five Island Town": "ITEM_FLY_FIVE_ISLAND",
    "Six Island Town": "ITEM_FLY_SIX_ISLAND",
    "Seven Island Town": "ITEM_FLY_SEVEN_ISLAND",
    "Route 4 Pokemon Center 1F": "ITEM_FLY_ROUTE4",
    "Route 10 Pokemon Center 1F": "ITEM_FLY_ROUTE10"
}


class PokemonFRLGLocation(Location):
    game: str = "Pokemon FireRed and LeafGreen"
    item_address = Dict[str, int | List[int]] | None
    default_item_id: int | None
    category: LocationCategory
    data_ids: List[str] | None
    spoiler_name: str

    def __init__(
            self,
            player: int,
            name: str,
            address: int | None,
            category: LocationCategory,
            parent: Region | None = None,
            item_address: Dict[str, int | List[int]] | None = None,
            default_item_id: int | None = None,
            data_ids: List[str] | None = None,
            spoiler_name: str | None = None) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = default_item_id
        self.item_address = item_address
        self.category = category
        self.data_ids = data_ids
        self.spoiler_name = spoiler_name if spoiler_name is not None else name


def create_location_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location names to their AP location ID (address)
    """
    name_to_id_mapping: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_id in region_data.locations:
            location_data = data.locations[location_id]
            name_to_id_mapping[location_data.name] = location_data.flag

    return name_to_id_mapping


def create_locations_from_categories(world: "PokemonFRLGWorld",
                                     regions: Dict[str, Region],
                                     categories: Set[LocationCategory]) -> None:
    def exclude_location(location_id: str):
        sevii_required_locations = [
            "NPC_GIFT_GOT_ONE_PASS", "TRAINER_ELITE_FOUR_LORELEI_2_REWARD", "TRAINER_ELITE_FOUR_BRUNO_2_REWARD",
            "TRAINER_ELITE_FOUR_AGATHA_2_REWARD", "TRAINER_ELITE_FOUR_LANCE_2_REWARD",
            "TRAINER_CHAMPION_REMATCH_BULBASAUR_REWARD"
        ]

        if world.options.kanto_only and location_id in sevii_required_locations:
            return True
        return False

    """
    Iterates through region data and adds locations to the multiworld if
    those locations are included in the given categories.
    """
    for region_data in data.regions.values():
        if region_data.name not in regions:
            continue

        region = regions[region_data.name]
        included_locations = [loc for loc in region_data.locations if data.locations[loc].category in categories]

        for location_id in included_locations:
            if exclude_location(location_id):
                continue

            location_data = data.locations[location_id]

            if location_data.default_item == data.constants["ITEM_NONE"]:
                default_item = world.item_name_to_id[get_random_item(world, ItemClassification.filler)]
            else:
                default_item = location_data.default_item

            location = PokemonFRLGLocation(
                world.player,
                location_data.name,
                location_data.flag,
                location_data.category,
                region,
                location_data.address,
                default_item
            )
            region.locations.append(location)


def fill_unrandomized_locations(world: "PokemonFRLGWorld") -> None:
    def create_events_for_unrandomized_items(locations: Set[PokemonFRLGLocation]) -> None:
        for location in locations:
            location.place_locked_item(PokemonFRLGItem(world.item_id_to_name[location.default_item_id],
                                                       ItemClassification.progression,
                                                       None,
                                                       world.player))
            location.progress_type = LocationProgressType.DEFAULT
            location.address = None
            location.show_in_spoiler = False

    unrandomized_progression_locations = set()

    if world.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_off:
        fly_locations = [loc for loc in world.get_locations() if loc.name in location_groups["Town Visits"]]
        unrandomized_progression_locations.update(fly_locations)
    elif world.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_exclude_indigo:
        unrandomized_progression_locations.add(world.get_location("Indigo Plateau - Unlock Fly Destination"))

    if not world.options.shuffle_berry_pouch:
        unrandomized_progression_locations.add(world.get_location("Title Screen - Starting Item 1"))
    if not world.options.shuffle_tm_case:
        unrandomized_progression_locations.add(world.get_location("Title Screen - Starting Item 2"))

    create_events_for_unrandomized_items(unrandomized_progression_locations)


def set_free_fly(world: "PokemonFRLGWorld") -> None:
    # Set our free fly location
    world.free_fly_location_id = fly_item_id_map["ITEM_FLY_NONE"]
    world.town_map_fly_location_id = fly_item_id_map["ITEM_FLY_NONE"]

    if not world.options.free_fly_location and not world.options.town_map_fly_location:
        return

    state = CollectionState(world.multiworld, True)
    forbidden_fly_list = list()

    if world.options.kanto_only:
        forbidden_fly_list = ["ITEM_FLY_ONE_ISLAND", "ITEM_FLY_TWO_ISLAND", "ITEM_FLY_THREE_ISLAND",
                              "ITEM_FLY_FOUR_ISLAND", "ITEM_FLY_FIVE_ISLAND", "ITEM_FLY_SIX_ISLAND",
                              "ITEM_FLY_SEVEN_ISLAND"]

    if (not world.options.randomize_fly_destinations and
            world.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_off):
        flys_to_remove = []
        locations = world.get_locations()

        for item_name in world.multiworld.local_early_items[world.player].keys():
            item = world.create_item(item_name)
            state.collect(item, True)

        state.sweep_for_advancements(locations)
        reachable_regions = state.reachable_regions[world.player]

        for region in reachable_regions:
            if region.name in fly_item_map.keys():
                flys_to_remove.append(fly_item_map[region.name])

        forbidden_fly_list.extend(flys_to_remove)

    blacklisted_free_fly_locations = [v for k, v in fly_blacklist_map.items()
                                      if k in world.options.free_fly_blacklist.value]
    blacklisted_town_map_fly_locations = [v for k, v in fly_blacklist_map.items()
                                          if k in world.options.town_map_fly_blacklist.value]
    free_fly_list = [fly for fly in fly_item_map.values()
                     if fly not in forbidden_fly_list and fly not in blacklisted_free_fly_locations]
    town_map_fly_list = [fly for fly in fly_item_map.values()
                         if fly not in forbidden_fly_list and fly not in blacklisted_town_map_fly_locations]
    if len(free_fly_list) == 0:
        free_fly_list = [fly for fly in fly_item_map.values() if fly not in forbidden_fly_list]
    if len(town_map_fly_list) == 0:
        town_map_fly_list = [fly for fly in fly_item_map.values() if fly not in forbidden_fly_list]

    if world.options.free_fly_location:
        free_fly_location_id = world.random.choice(free_fly_list)
        world.free_fly_location_id = fly_item_id_map[free_fly_location_id]

        if free_fly_location_id in town_map_fly_list and len(town_map_fly_list) > 1:
            town_map_fly_list.remove(free_fly_location_id)

        start_region = world.multiworld.get_region("Title Screen", world.player)
        free_fly_location = PokemonFRLGLocation(
            world.player,
            "Free Fly Location",
            None,
            LocationCategory.EVENT,
            start_region,
            None,
            None
        )
        item_id = data.constants[free_fly_location_id]
        free_fly_location.place_locked_item(PokemonFRLGItem(data.items[item_id].name,
                                                            ItemClassification.progression,
                                                            None,
                                                            world.player))
        free_fly_location.show_in_spoiler = False
        start_region.locations.append(free_fly_location)

    if world.options.town_map_fly_location:
        town_map_fly_location_id = world.random.choice(town_map_fly_list)
        world.town_map_fly_location_id = fly_item_id_map[town_map_fly_location_id]

        start_region = world.multiworld.get_region("Title Screen", world.player)
        town_map_fly_location = PokemonFRLGLocation(
            world.player,
            "Town Map Fly Location",
            None,
            LocationCategory.EVENT,
            start_region,
            None,
            None
        )
        item_id = data.constants[town_map_fly_location_id]
        town_map_fly_location.place_locked_item(PokemonFRLGItem(data.items[item_id].name,
                                                                 ItemClassification.progression,
                                                                 None,
                                                                 world.player))
        town_map_fly_location.access_rule = lambda state: state.has("Town Map", world.player)
        town_map_fly_location.show_in_spoiler = False
        start_region.locations.append(town_map_fly_location)
