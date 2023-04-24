import json
from pathlib import Path
from typing import Dict, List
from BaseClasses import MultiWorld, Region
from worlds.AutoWorld import LogicMixin


class LandstalkerLogic(LogicMixin):
    def _landstalker_has_items(self, player, items):
        for item in items:
            if not self.has(item, player):
                return False
        return True

    def _landstalker_has_visited_regions(self, player, regions):
        for region in regions:
            if not self.can_reach(region, None, player):
                return False
        return True


def create_rules(multiworld: MultiWorld, player: int, regions_table: Dict[str, Region], dark_region_ids: List[str]):
    # Item & exploration requirements to take paths
    add_path_requirements(multiworld, player, regions_table, dark_region_ids)
    add_specific_path_requirements(multiworld, player)

    # Location rules to forbid some item types depending on location types
    add_location_rules(multiworld, player)

    # Win condition
    multiworld.completion_condition[player] = lambda state: state.has("King Nole's Treasure", player)


def add_path_requirements(multiworld: MultiWorld, player: int, regions_table: Dict[str, Region],
                          dark_region_ids: List[str]):
    can_damage_boost = multiworld.handle_damage_boosting_in_logic[player].value

    script_folder = Path(__file__)
    with open((script_folder.parent / "data/world_path.json").resolve(), "r") as file:
        rules_data = json.load(file)
        for data in rules_data:
            name = data["fromId"] + " -> " + data["toId"]

            # Determine required items to reach this region
            required_items = data["requiredItems"] if "requiredItems" in data else []
            if "itemsPlacedWhenCrossing" in data:
                required_items += data["itemsPlacedWhenCrossing"]

            if data["toId"] in dark_region_ids:
                # Make Lantern required to reach the randomly selected dark regions
                required_items.append("Lantern")
            if can_damage_boost:
                # If damage boosting is handled in logic, remove all iron boots & fireproof requirements
                required_items = [item for item in required_items if item != "Iron Boots" and item != "Fireproof"]

            # Determine required other visited regions to reach this region
            required_region_ids = data["requiredNodes"] if "requiredNodes" in data else []
            required_regions = [regions_table[region_id] for region_id in required_region_ids]

            # Create the rule lambda using those requirements
            if len(required_items) == 0 and len(required_regions) == 0:
                continue

            access_rule = make_path_requirement_lambda(player, required_items, required_regions)
            multiworld.get_entrance(name, player).access_rule = access_rule

            # If two-way, also apply the rule to the opposite path
            if "twoWay" in data and data["twoWay"] is True:
                reverse_name = data["toId"] + " -> " + data["fromId"]
                multiworld.get_entrance(reverse_name, player).access_rule = access_rule


def add_specific_path_requirements(multiworld: MultiWorld, player: int):
    # Make the jewels required to reach Kazalt
    jewel_count = multiworld.jewel_count[player].value
    required_jewels = ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"]
    del required_jewels[jewel_count:]
    path_to_kazalt = multiworld.get_entrance("king_nole_cave -> kazalt", player)
    path_to_kazalt.access_rule = make_path_requirement_lambda(player, required_jewels, [])

    # If enemy jumping is enabled, Mir Tower sector first tree can be bypassed to reach the elevated ledge
    if multiworld.handle_enemy_jumping_in_logic[player].value == 1:
        remove_requirements_for(multiworld, "mir_tower_sector -> mir_tower_sector_tree_ledge", player)

    # Both trees in Mir Tower sector can be abused using tree cutting glitch
    if multiworld.handle_tree_cutting_glitch_in_logic[player].value == 1:
        remove_requirements_for(multiworld, "mir_tower_sector -> mir_tower_sector_tree_ledge", player)
        remove_requirements_for(multiworld, "mir_tower_sector -> mir_tower_sector_tree_coast", player)

    # If Whistle can be used from behind the trees, it adds a new path that requires the whistle as well
    if multiworld.allow_whistle_usage_behind_trees[player].value == 1:
        entrance = multiworld.get_entrance("greenmaze_post_whistle -> greenmaze_pre_whistle", player)
        entrance.access_rule = make_path_requirement_lambda(player, ["Einstein Whistle"], [])


def make_path_requirement_lambda(player, required_items, required_regions):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: \
        state._landstalker_has_items(player, required_items) \
        and state._landstalker_has_visited_regions(player, required_regions)


def remove_requirements_for(multiworld: MultiWorld, entrance_name: str, player: int):
    entrance = multiworld.get_entrance(entrance_name, player)
    entrance.access_rule = lambda state: True


def add_location_rules(multiworld: MultiWorld, player: int):
    for location in multiworld.get_locations(player):
        if location.type_string == "ground":
            location.item_rule = lambda item: not (item.player == player and ' Gold' in item.name)
        elif location.type_string == "shop":
            location.item_rule = lambda item: item.player == player and ' Gold' not in item.name
