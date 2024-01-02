from typing import List, TYPE_CHECKING

from BaseClasses import CollectionState
from .data.world_path import WORLD_PATHS_JSON
from .Locations import LandstalkerLocation
from .Regions import LandstalkerRegion

if TYPE_CHECKING:
    from . import LandstalkerWorld


def _landstalker_has_visited_regions(state: CollectionState, player: int, regions):
    return all([state.can_reach(region, None, player) for region in regions])


def _landstalker_has_health(state: CollectionState, player: int, health):
    return state.has("Life Stock", player, health)


# multiworld: MultiWorld, player: int, regions_table: Dict[str, Region], dark_region_ids: List[str]
def create_rules(world: "LandstalkerWorld"):
    # Item & exploration requirements to take paths
    add_path_requirements(world)
    add_specific_path_requirements(world)

    # Location rules to forbid some item types depending on location types
    add_location_rules(world)

    # Win condition
    world.multiworld.completion_condition[world.player] = lambda state: state.has("King Nole's Treasure", world.player)


# multiworld: MultiWorld, player: int, regions_table: Dict[str, Region],
#                           dark_region_ids: List[str]
def add_path_requirements(world: "LandstalkerWorld"):
    for data in WORLD_PATHS_JSON:
        name = data["fromId"] + " -> " + data["toId"]

        # Determine required items to reach this region
        required_items = data["requiredItems"] if "requiredItems" in data else []
        if "itemsPlacedWhenCrossing" in data:
            required_items += data["itemsPlacedWhenCrossing"]

        if data["toId"] in world.dark_region_ids:
            # Make Lantern required to reach the randomly selected dark regions
            required_items.append("Lantern")
        if world.options.handle_damage_boosting_in_logic:
            # If damage boosting is handled in logic, remove all iron boots & fireproof requirements
            required_items = [item for item in required_items if item != "Iron Boots" and item != "Fireproof"]

        # Determine required other visited regions to reach this region
        required_region_ids = data["requiredNodes"] if "requiredNodes" in data else []
        required_regions = [world.regions_table[region_id] for region_id in required_region_ids]

        if not (required_items or required_regions):
            continue

        # Create the rule lambda using those requirements
        access_rule = make_path_requirement_lambda(world.player, required_items, required_regions)
        world.multiworld.get_entrance(name, world.player).access_rule = access_rule

        # If two-way, also apply the rule to the opposite path
        if "twoWay" in data and data["twoWay"] is True:
            reverse_name = data["toId"] + " -> " + data["fromId"]
            world.multiworld.get_entrance(reverse_name, world.player).access_rule = access_rule


def add_specific_path_requirements(world: "LandstalkerWorld"):
    multiworld = world.multiworld
    player = world.player

    # Make the jewels required to reach Kazalt
    jewel_count = world.options.jewel_count.value
    path_to_kazalt = multiworld.get_entrance("king_nole_cave -> kazalt", player)
    if jewel_count < 6:
        # 5- jewels => the player needs to find as many uniquely named jewel items
        required_jewels = ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"]
        del required_jewels[jewel_count:]
        path_to_kazalt.access_rule = make_path_requirement_lambda(player, required_jewels, [])
    else:
        # 6+ jewels => the player needs to find as many "Kazalt Jewel" items
        path_to_kazalt.access_rule = lambda state: state.has("Kazalt Jewel", player, jewel_count)

    # If enemy jumping is enabled, Mir Tower sector first tree can be bypassed to reach the elevated ledge
    if world.options.handle_enemy_jumping_in_logic == 1:
        remove_requirements_for(world, "mir_tower_sector -> mir_tower_sector_tree_ledge")

    # Both trees in Mir Tower sector can be abused using tree cutting glitch
    if world.options.handle_tree_cutting_glitch_in_logic == 1:
        remove_requirements_for(world, "mir_tower_sector -> mir_tower_sector_tree_ledge")
        remove_requirements_for(world, "mir_tower_sector -> mir_tower_sector_tree_coast")

    # If Whistle can be used from behind the trees, it adds a new path that requires the whistle as well
    if world.options.allow_whistle_usage_behind_trees == 1:
        entrance = multiworld.get_entrance("greenmaze_post_whistle -> greenmaze_pre_whistle", player)
        entrance.access_rule = make_path_requirement_lambda(player, ["Einstein Whistle"], [])


def make_path_requirement_lambda(player: int, required_items: List[str], required_regions: List[LandstalkerRegion]):
    """
    Lambdas are created in a for loop, so values need to be captured
    """
    return lambda state: \
        state.has_all(set(required_items), player) and _landstalker_has_visited_regions(state, player, required_regions)


def make_shop_location_requirement_lambda(player: int, location: LandstalkerLocation):
    """
    Lambdas are created in a for loop, so values need to be captured
    """
    # Prevent local golds in shops, as well as duplicates
    other_locations_in_shop = [loc for loc in location.parent_region.locations if loc != location]
    return lambda item: \
        item.player != player \
        or (" Gold" not in item.name
            and item.name not in [loc.item.name for loc in other_locations_in_shop if loc.item is not None])


def remove_requirements_for(world: "LandstalkerWorld", entrance_name: str):
    entrance = world.multiworld.get_entrance(entrance_name, world.player)
    entrance.access_rule = lambda state: True


def add_location_rules(world: "LandstalkerWorld"):
    location: LandstalkerLocation
    for location in world.multiworld.get_locations(world.player):
        if location.type_string == "ground":
            location.item_rule = lambda item: not (item.player == world.player and " Gold" in item.name)
        elif location.type_string == "shop":
            location.item_rule = make_shop_location_requirement_lambda(world.player, location)

    # Add a special rule for Fahl
    fahl_location = world.multiworld.get_location("Mercator: Fahl's dojo challenge reward", world.player)
    fahl_location.access_rule = lambda state: _landstalker_has_health(state, world.player, 15)
