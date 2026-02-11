import logging
import re
from typing import Any

from BaseClasses import CollectionState, Item, ItemClassification, LocationProgressType, MultiWorld
from Options import OptionError
from worlds.AutoWorld import World

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import get_option_value, is_option_enabled

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem, item_name_to_item
from ..Locations import ManualLocation, location_name_to_location, victory_names
from .Data import CASTER, DOH, HEALERS, MELEE, RANGED, TANKS, WORLD_BOSSES, categorizedLocationNames
from .Helpers import get_int_value
from .Options import LevelCap

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################


def get_duty_count(duty_type: str, duty_diff: int, multiworld: MultiWorld, player: int) -> int | None:
    if duty_type == "Dungeon":
        return get_int_value(multiworld, player, "dungeon_count")
    if duty_type == "Variant Dungeon":
        return get_int_value(multiworld, player, "variant_dungeon_count")
    if duty_type == "Trial":
        if duty_diff == 1:  # Normal
            return get_int_value(multiworld, player, "trial_count")
        if duty_diff == 2:  # Extreme
            return get_int_value(multiworld, player, "extreme_trial_count")
        if duty_diff == 4:  # Endgame
            return get_int_value(multiworld, player, "endgame_trial_count")
    if duty_type in ["Raid", "Normal Raid", "Savage Raid", "Endgame Raid"]:
        if duty_diff == 1:  # Normal
            return get_int_value(multiworld, player, "normal_raid_count")
        if duty_diff == 3:  # Savage
            return get_int_value(multiworld, player, "savage_raid_count")
        if duty_diff == 4:  # Endgame
            return get_int_value(multiworld, player, "endgame_raid_count")
    if duty_type == "Alliance Raid":
        return get_int_value(multiworld, player, "alliance_raid_count")
    if duty_type == "Ultimate":
        return get_int_value(multiworld, player, "ultimate_count")
    if duty_type == "Guildhest":
        return None
    if duty_type == "PvP":
        return None
    raise ValueError(f"Unknown duty type {duty_type}")

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    world.skipped_duties: set[str] = set()
    if not getattr(multiworld, 'generation_is_fake', False):
        for category, names in categorizedLocationNames.items():
            dutyType, _dutyExpansion, dutyDifficulty = category
            count = get_duty_count(dutyType, dutyDifficulty, multiworld, player)
            if count is None:
                continue
            count = min(len(names), count)
            used_names = world.random.sample(names, count)
            for name in names:
                if name not in used_names:
                    world.skipped_duties.add(name)

    tanks = TANKS.copy()
    healers = HEALERS.copy()
    melee = MELEE.copy()
    caster = CASTER.copy()
    ranged = RANGED.copy()
    doh = DOH.copy()

    world.random.shuffle(tanks)
    world.random.shuffle(healers)
    world.random.shuffle(melee)
    world.random.shuffle(caster)
    world.random.shuffle(ranged)
    world.random.shuffle(doh)
    force_jobs = sorted(get_option_value(multiworld, player, "force_jobs"))
    level_cap = get_option_value(multiworld, player, "level_cap") or LevelCap.range_end
    if force_jobs:
        if len(force_jobs) > 5:
            world.random.shuffle(force_jobs)
            force_jobs = force_jobs[:5]
        prog_classes = force_jobs
    else:
        prog_classes = [tanks[0], healers[0], melee[0], caster[0], ranged[0]]
    world.prog_classes = prog_classes
    world.prog_levels = [f"5 {job} Levels" for job in world.prog_classes]
    world.prog_doh = doh[0]

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    locationNamesToRemove = []
    locationNamesToExclude = []
    if not is_option_enabled(multiworld, player, "include_unreasonable_fates"):
        locationNamesToRemove.extend(WORLD_BOSSES)


    include_dungeons = get_option_value(multiworld, player, "include_dungeons")
    level_cap = get_option_value(multiworld, player, "level_cap") or LevelCap.range_end

    if not is_option_enabled(multiworld, player, "allow_main_scenario_duties"):
        locationNamesToRemove.extend(["The Porta Decumana", "Castrum Meridianum", "The Praetorium"])

    for location in location_table:
        if not include_dungeons and location.get("is_dungeon"):
            # print(f"Removing {location['name']} from {player}'s world")
            locationNamesToRemove.append(location["name"])
            continue

    # Find all region access items.
    access_items = {item['name']: item for item in item_table if item['name'].endswith(" Access")}

    for region in multiworld.regions:
        # Get the item required to access the region to determine the level requirement of the region.
        access_item_name = region.name + " Access"
        access_item = access_items.get(access_item_name)
        # If there is an item for this region and the level requirement is above the level cap, remove all the locations
        # in the region.
        if access_item is not None and access_item.get("level", 0) > level_cap:
            # print(f"Removing all locations in region {region.name} from {player}'s world")
            for location in list(region.locations):
                # print(f"  Removing {location.name}")
                region.locations.remove(location)
        # Remove/exclude locations in `locationNamesToRemove`/`locationNamesToExclude`.
        elif region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    # print(f"Removing {location.name} from {player}'s pool")
                    region.locations.remove(location)
                elif location.name in locationNamesToExclude:
                    location.progress_type = LocationProgressType.EXCLUDED
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool


# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(
    item_pool: list[ManualItem], world: World, multiworld: MultiWorld, player: int
) -> list:
    prog_levels = world.prog_levels
    start_class = world.random.choice(prog_levels)
    prog_doh = f"5 {world.prog_doh} Levels"
    level_cap = get_option_value(multiworld, player, "level_cap") or LevelCap.range_end

    seen_levels = {}

    reduced_item_pool = []
    for item in item_pool:
        if item.name in prog_levels:
            item.classification = ItemClassification.progression
        if prog_doh and item.name == prog_doh:
            item.classification = ItemClassification.progression
            prog_doh = ""

        if "Levels" in item.name:
            # Add the levels from this item, always 5 currently.
            seen_levels[item.name] = seen_levels.get(item.name, 0) + 5
            if seen_levels[item.name] > level_cap:
                # Do not add the item to the item pool if the total seen levels is now above the level cap.
                continue
            # If it is the first levels for the starting class, add the item to starting inventory.
            if item.name == start_class and seen_levels[item.name] <= 10:
                # Added to starting inventory instead of the item pool.
                multiworld.push_precollected(item)
                continue
        if item_name_to_item[item.name].get("level", 0) > level_cap:
            # Do not add the item to the item pool if the level requirement is above the level cap.
            continue

        reduced_item_pool.append(item)

    return reduced_item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)


# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list[ManualItem], world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called before the victory location has the victory event placed and locked
def before_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called after the victory location has the victory event placed and locked
def after_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    if getattr(multiworld, 'generation_is_fake', False):
        if "Levels" in item.name:
            item.classification = ItemClassification.progression
    elif item.name in getattr(world, "prog_levels", []) or item.name in ["5 FSH Levels", "5 BLU Levels"]:
        item.classification = ItemClassification.progression
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> None:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    slot_data["prog_classes"] = world.prog_classes
    slot_data["mcguffins_needed"] = get_option_value(multiworld, player, "mcguffins_needed") or 30
    slot_data["skipped_duties"] = list(world.skipped_duties)
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass


def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    This is the earliest hook called during generation, before anything else is done.
    Use it to check or modify incompatible options, or to set up variables for later use.
    """

    goal = victory_names[get_option_value(multiworld, player, 'goal')]  # type: ignore
    goal_location = next(loc for loc in location_table if loc.get('victory') and loc['name'] == goal)
    level_cap = get_option_value(multiworld, player, 'level_cap')
    goal_level = goal_location.get('level', 0)

    if goal_level and goal_level < level_cap:
        raise OptionError(f"The selected goal '{goal}' requires level {goal_location.get('level')}, which exceeds the level cap of {level_cap}.")

    if not get_option_value(multiworld, player, 'fatesanity') and is_option_enabled(multiworld, player, 'fates_per_zone') == 0 \
        and not is_option_enabled(multiworld, player, 'include_dungeons') and not is_option_enabled(multiworld, player, 'fishsanity'):
        raise OptionError("You can't disable everything.")


def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    """
        Called when Universal Tracker wants to perform a fake generation
        Use this if you want to use or modify the slot_data for passed into re_gen_passthrough
    """
    return slot_data
