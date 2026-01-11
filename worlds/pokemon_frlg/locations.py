from typing import TYPE_CHECKING, Dict, List, Set
from BaseClasses import CollectionState, Location, LocationProgressType, Region, ItemClassification
from Fill import FillError, fill_restrictive
from .data import data, LocationCategory, fly_blacklist_map, TRAINER_REMATCH_MAP
from .groups import location_groups
from .items import PokemonFRLGItem, get_random_item, update_renewable_to_progression
from .options import (CardKey, Dexsanity, Goal, IslandPasses, ShuffleFlyUnlocks, ShuffleHiddenItems, ShufflePokedex,
                      ShuffleRunningShoes, Trainersanity)

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
    "Viridian City (South)": "ITEM_FLY_VIRIDIAN",
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
    "Three Island Town (South)": "ITEM_FLY_THREE_ISLAND",
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
    location_id: str | None
    scaling_ids: List[str] | None
    spoiler_name: str
    encounter_key: str
    hint_entrances: List[str]

    def __init__(
            self,
            player: int,
            name: str,
            address: int | None,
            category: LocationCategory,
            parent: Region | None = None,
            item_address: Dict[str, int | List[int]] | None = None,
            default_item_id: int | None = None,
            location_id: str | None = None,
            scaling_ids: List[str] | None = None,
            spoiler_name: str | None = None,
            encounter_key: str | None = None) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = default_item_id
        self.item_address = item_address
        self.category = category
        self.location_id = location_id
        self.scaling_ids = scaling_ids
        self.spoiler_name = spoiler_name if spoiler_name is not None else name
        self.encounter_key = encounter_key


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


def create_locations(world: "PokemonFRLGWorld", regions: Dict[str, Region]) -> None:
    """
    Iterates through region data and adds locations to the multiworld if
    those locations are included in the given categories.
    """
    def create_location(location_id: str) -> PokemonFRLGLocation:
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
            default_item,
            location_id
        )

        return location

    def exclude_location(location_id: str) -> bool:
        sevii_required_locations = [
            "NPC_GIFT_GOT_ONE_PASS", "TRAINER_ELITE_FOUR_LORELEI_2_REWARD", "TRAINER_ELITE_FOUR_BRUNO_2_REWARD",
            "TRAINER_ELITE_FOUR_AGATHA_2_REWARD", "TRAINER_ELITE_FOUR_LANCE_2_REWARD",
            "TRAINER_CHAMPION_REMATCH_BULBASAUR_REWARD"
        ]

        post_champion_locations = [
            "TRAINER_ELITE_FOUR_LORELEI_2_REWARD", "TRAINER_ELITE_FOUR_BRUNO_2_REWARD",
            "TRAINER_ELITE_FOUR_AGATHA_2_REWARD", "TRAINER_ELITE_FOUR_LANCE_2_REWARD",
            "TRAINER_CHAMPION_REMATCH_BULBASAUR_REWARD", "FAME_CHECKER_BRUNO_5"
        ]

        post_champion_gossiper_locations = [
            "FAME_CHECKER_DAISY_1", "FAME_CHECKER_OAK_6", "FAME_CHECKER_MISTY_6", "FAME_CHECKER_DAISY_2",
            "FAME_CHECKER_MRFUJI_4", "FAME_CHECKER_DAISY_5", "FAME_CHECKER_LANCE_4", "FAME_CHECKER_KOGA_4",
            "FAME_CHECKER_BRUNO_3", "FAME_CHECKER_LANCE_3", "FAME_CHECKER_MRFUJI_6", "FAME_CHECKER_AGATHA_2",
            "FAME_CHECKER_AGATHA_3", "FAME_CHECKER_LANCE_5", "FAME_CHECKER_LANCE_6", "FAME_CHECKER_BRUNO_4",
            "FAME_CHECKER_LORELEI_4", "FAME_CHECKER_AGATHA_4"
        ]

        if world.options.kanto_only and location_id in sevii_required_locations:
            return True
        if not world.options.post_goal_locations and world.options.goal == Goal.option_champion:
            if location_id in post_champion_locations:
                return True
            if ("Early Gossipers" not in world.options.modify_world_state.value and
                    location_id in post_champion_gossiper_locations):
                return True
        return False

    included_types: Set[str] = set()
    if world.options.shuffle_hidden == ShuffleHiddenItems.option_all:
        included_types.add("Hidden Items")
        included_types.add("Recurring Hidden Items")
    elif world.options.shuffle_hidden == ShuffleHiddenItems.option_nonrecurring:
        included_types.add("Hidden Items")
    if world.options.extra_key_items:
        included_types.add("Extra Key Items")
    if world.options.trainersanity != Trainersanity.special_range_names["none"]:
        included_types.add("Trainersanity")
        if world.options.rematchsanity:
            included_types.add("Rematchsanity")
    if world.options.dexsanity != Dexsanity.special_range_names["none"]:
        included_types.add("Dexsanity")
    if world.options.famesanity:
        included_types.add("Famesanity")
    if world.options.pokemon_request_locations:
        included_types.add("Pokemon Requests")
    if world.options.card_key != CardKey.option_vanilla:
        included_types.add("Split Card Key")
    if world.options.island_passes in (IslandPasses.option_split, IslandPasses.option_progressive_split):
        included_types.add("Split Island Passes")
    if world.options.split_teas:
        included_types.add("Split Teas")
    if world.options.gym_keys:
        included_types.add("Gym Keys")

    for region_data in data.regions.values():
        if region_data.name not in regions:
            continue

        region = regions[region_data.name]
        included_locations = [loc for loc in region_data.locations
                              if data.locations[loc].include.issubset(included_types)]

        for location_id in included_locations:
            if exclude_location(location_id):
                continue
            if world.is_universal_tracker:
                location = data.locations[location_id]
                if ((location.category == LocationCategory.TRAINER
                        or location.category == LocationCategory.TRAINER_REMATCH)
                        and location.flag not in world.ut_slot_data["trainersanity_locations"]):
                    continue
                elif (location.category == LocationCategory.POKEDEX
                      and location.flag not in world.ut_slot_data["dexsanity_locations"]):
                    continue
            region.locations.append(create_location(location_id))

    # Remove trainersanity locations if there are more than the amount specified in the settings
    if world.options.trainersanity != Trainersanity.special_range_names["none"] and not world.is_universal_tracker:
        locations: List[PokemonFRLGLocation] = world.get_locations()
        trainer_locations = [loc for loc in locations if loc.category == LocationCategory.TRAINER]
        locs_to_remove = len(trainer_locations) - world.options.trainersanity.value
        if locs_to_remove > 0:
            rematchsanity = world.options.rematchsanity
            priority_trainer_locations = [loc for loc in trainer_locations
                                          if loc.name in world.options.priority_locations.value]
            non_priority_trainer_locations = [loc for loc in trainer_locations
                                              if loc.name not in world.options.priority_locations.value]
            world.random.shuffle(priority_trainer_locations)
            world.random.shuffle(non_priority_trainer_locations)
            trainer_locations = non_priority_trainer_locations + priority_trainer_locations
            for location in trainer_locations:
                region = location.parent_region
                region.locations.remove(location)
                if rematchsanity and location.location_id in TRAINER_REMATCH_MAP:
                    for location_id in TRAINER_REMATCH_MAP[location.location_id]:
                        region.locations.remove(world.get_location(data.locations[location_id].name))
                locs_to_remove -= 1
                if locs_to_remove <= 0:
                    break


def place_unrandomized_items(world: "PokemonFRLGWorld") -> None:
    def fill_unrandomized_location(location: Location,
                                            as_event: bool) -> None:
        item = world.create_item_by_id(location.default_item_id)
        if as_event:
            item.code = None
            location.address = None
            location.show_in_spoiler = False
        location.place_locked_item(item)
        location.progress_type = LocationProgressType.DEFAULT
        world.itempool.remove(item)

    if world.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_off:
        fly_locations = [loc for loc in world.get_locations() if loc.name in location_groups["Town Visits"]]
        for location in fly_locations:
            fill_unrandomized_location(location, True)
    elif world.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_exclude_indigo:
        fill_unrandomized_location(world.get_location("Indigo Plateau - Unlock Fly Destination"), False)

    shop_locations = []
    if world.options.shopsanity:
        shop_locations.extend([loc for loc in world.get_locations() if "Held Shop Item" in loc.name])
        if not world.options.post_goal_locations and world.options.goal == Goal.option_champion:
            shop_locations.extend([loc for loc in world.get_locations() if
                                   loc.name in location_groups["Market Stall"] and
                                   int(loc.name[-1]) in (3, 4, 5, 8, 9)])
    else:
        shop_locations.extend([loc for loc in world.get_locations() if loc.name in location_groups["Shops"]])
    if not world.options.vending_machines:
        shop_locations.extend([loc for loc in world.get_locations() if loc.name in location_groups["Vending Machines"]])
    if not world.options.prizesanity:
        shop_locations.extend([loc for loc in world.get_locations() if loc.name in location_groups["Prizes"]])
    for location in shop_locations:
        fill_unrandomized_location(location, True)
        update_renewable_to_progression(location.item)

    if world.options.shuffle_pokedex == ShufflePokedex.option_vanilla:
        fill_unrandomized_location(world.get_location("Professor Oak's Lab - Oak Gift 1 (Deliver Parcel)"), False)

    if world.options.shuffle_running_shoes == ShuffleRunningShoes.option_vanilla:
        fill_unrandomized_location(world.get_location("Pewter City - Gift from Mom"), False)


def place_shop_items(world: "PokemonFRLGWorld") -> None:
    if (not world.options.shopsanity and not world.options.vending_machines) or world.is_universal_tracker:
        return

    shop_locations = [loc for loc in world.get_locations() if
                      (loc.name in location_groups["Shops"] or
                       loc.name in location_groups["Vending Machines"] or
                       loc.name in location_groups["Prizes"]) and
                      not loc.is_event]
    shop_items = [world.create_item_by_id(loc.default_item_id) for loc in shop_locations]
    non_progression_shop_locations = [loc for loc in shop_locations if
                                      loc.name not in location_groups["Market Stall"] and
                                      loc.name not in location_groups["Vending Machines"] and
                                      loc.name not in location_groups["Prizes"] and
                                      int(loc.name[-1]) > world.options.shop_slots.value]
    world.random.shuffle(shop_items)

    if not world.options.kanto_only:
        two_island_shop_location_ids = ["SHOP_TWO_ISLAND_1", "SHOP_TWO_ISLAND_7", "SHOP_TWO_ISLAND_2",
                                        "SHOP_TWO_ISLAND_6", "SHOP_TWO_ISLAND_5", "SHOP_TWO_ISLAND_8",
                                        "SHOP_TWO_ISLAND_3", "SHOP_TWO_ISLAND_4", "SHOP_TWO_ISLAND_9"]
        for index, location_id in enumerate(two_island_shop_location_ids):
            if (index >= world.options.shop_slots.value and
                    not world.get_location(data.locations[location_id].name).is_event):
                non_progression_shop_locations.append(world.get_location(data.locations[location_id].name))


    renewable_items = []
    if world.options.vending_machines:
        renewable_items.extend(["Fresh Water", "Soda Pop", "Lemonade"])
    elif (world.options.shopsanity and
          not world.options.kanto_only and
          (world.options.post_goal_locations or world.options.goal != Goal.option_champion)):
        renewable_items.append("Lemonade")
    if renewable_items:
        renewable_locations = [loc for loc in shop_locations if
                               loc.progress_type != LocationProgressType.EXCLUDED and
                               loc not in non_progression_shop_locations]
        if len(renewable_locations) == 0:
            renewable_locations = [loc for loc in shop_locations if
                                   loc not in non_progression_shop_locations]
        if len(renewable_locations) == 0:
            renewable_locations = [loc for loc in shop_locations]
        world.random.shuffle(renewable_locations)
        for item_name in renewable_items:
            renewable_location = renewable_locations.pop()
            item = world.create_item(item_name)
            item.classification = ItemClassification.progression
            renewable_location.place_locked_item(item)
            world.itempool.remove(item)
            shop_items.remove(item)

    for location in non_progression_shop_locations:
        if location.locked:
            continue
        item = shop_items.pop()
        location.place_locked_item(item)
        world.itempool.remove(item)


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
        if not world.is_universal_tracker:
            free_fly_location_id = world.random.choice(free_fly_list)
        else:
            fly_map_lookup = {v: k for k, v in fly_item_id_map.items()}
            free_fly_location_id = fly_map_lookup[world.ut_slot_data["free_fly_location_id"]]
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
        if not world.is_universal_tracker:
            town_map_fly_location_id = world.random.choice(town_map_fly_list)
        else:
            fly_map_lookup = {v: k for k, v in fly_item_id_map.items()}
            town_map_fly_location_id = fly_map_lookup[world.ut_slot_data["town_map_fly_location_id"]]
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

def shuffle_badges(world: "PokemonFRLGWorld") -> None:
    if world.is_universal_tracker:
        return

    badge_items = []
    badge_items.extend(world.get_pre_fill_items())
    world.pre_fill_items.clear()
    locations: List[PokemonFRLGLocation] = world.get_locations()
    for attempt in range(5):
        badge_locations: List[PokemonFRLGLocation] = [
            loc for loc in locations if loc.name in location_groups["Gym Prizes"] and loc.item is None
        ]
        state = world.get_world_collection_state()
        # Try to place badges with current Pokemon and HM access
        # If it can't, try with guaranteed HM access and fix it later
        if attempt > 1:
            world.logic.guaranteed_hm_access = True
        state.sweep_for_advancements()
        world.random.shuffle(badge_items)
        world.random.shuffle(badge_locations)
        fill_restrictive(world.multiworld, state, badge_locations.copy(), badge_items,
                         single_player_placement=True, lock=True, allow_partial=True, allow_excluded=True)
        if len(badge_items) > 8 - len(badge_locations):
            for location in badge_locations:
                if location.item:
                    badge_items.append(location.item)
                    location.item = None
            continue
        else:
            break
    else:
        raise FillError(f"Failed to place badges for player {world.player}")
    world.logic.guaranteed_hm_access = False
