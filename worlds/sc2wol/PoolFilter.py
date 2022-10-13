from typing import Callable
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import item_table
from .MissionTables import no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list,\
    mission_orders, get_starting_mission_locations, MissionInfo, vanilla_mission_req_table
from .Options import get_option_value, get_option_set_value
from .LogicMixin import SC2WoLLogic

# Items with associated upgrades
UPGRADABLE_ITEMS = [
    "Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre",
    "Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor",
    "Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser",
    "Bunker", "Missile Turret"
]

BARRACKS_UNITS = {"Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre"}
FACTORY_UNITS = {"Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor", "Predator"}
STARPORT_UNITS = {"Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser", "Hercules", "Science Vessel", "Raven"}

PROTOSS_REGIONS = {"A Sinister Turn", "Echoes of the Future", "In Utter Darkness"}


def filter_missions(world: MultiWorld, player: int) -> dict[str, list[str]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(world, player, "mission_order")
    shuffle_protoss = get_option_value(world, player, "shuffle_protoss")
    relegate_no_build = get_option_value(world, player, "relegate_no_build")
    excluded_missions: set[str] = get_option_set_value(world, player, "excluded_missions")
    invalid_mission_names = excluded_missions.difference(vanilla_mission_req_table.keys())
    if invalid_mission_names:
        raise Exception("Error in locked_missions - the following are not valid mission names: " + ", ".join(invalid_mission_names))
    mission_count = len(mission_orders[mission_order_type]) - 1
    # Vanilla and Vanilla Shuffled use the entire mission pool
    if mission_count == 28:
        return {
            "no_build": no_build_regions_list[:],
            "easy": easy_regions_list[:],
            "medium": medium_regions_list[:],
            "hard": hard_regions_list[:],
            "all_in": "all_in"
        }

    mission_sets = [
        set(no_build_regions_list),
        set(easy_regions_list),
        set(medium_regions_list),
        set(hard_regions_list)
    ]
    # Omitting No Build missions if relegating no-build
    if relegate_no_build:
        # The build missions in starting_mission_locations become the new "no build missions"
        mission_sets[0] = set(get_starting_mission_locations(world, player).keys())
        mission_sets[0].difference_update(no_build_regions_list)
        # Removing the new no-build missions from their original sets
        for mission_set in mission_sets[1:]:
            mission_set.difference_update(mission_sets[0])
    # Omitting Protoss missions if not shuffling protoss
    if not shuffle_protoss:
        excluded_missions = excluded_missions.union(PROTOSS_REGIONS)
    for mission_set in mission_sets:
        mission_set.difference_update(excluded_missions)
    # Removing random missions from each difficulty set in a cycle
    set_cycle = 0
    mission_pools = [list(mission_set) for mission_set in mission_sets]
    current_count = sum(len(mission_pool) for mission_pool in mission_pools)
    if current_count < mission_count:
        raise Exception("Not enough missions available to fill the campaign on current settings.  Please exclude fewer missions.")
    while current_count > mission_count:
        if set_cycle == 4:
            set_cycle = 0
        # Must contain at least one mission per set
        mission_pool = mission_pools[set_cycle]
        set_cycle += 1
        if len(mission_pool) == 1:
            if all(len(other_pool) == 1 for other_pool in mission_pools):
                raise Exception("Not enough missions available to fill the campaign on current settings.   Please exclude fewer missions.")
            continue
        mission_pool.remove(world.random.choice(mission_pool))
        current_count -= 1

    return {
        "no_build": mission_pools[0],
        "easy": mission_pools[1],
        "medium": mission_pools[2],
        "hard": mission_pools[3]
    }


def get_item_upgrades(inventory: list[Item], parent_item: Item or str):
    item_name = parent_item.name if isinstance(parent_item, Item) else parent_item
    return [
        inv_item for inv_item in inventory
        if item_table[inv_item.name].parent_item == item_name
    ]


class ValidInventory:

    def has(self, item: str, player: int):
        return item in self.logical_inventory

    def has_any(self, items: set[str], player: int):
        return any(item in self.logical_inventory for item in items)

    def has_all(self, items: set[str], player: int):
        return all(item in self.logical_inventory for item in items)

    def has_units_per_structure(self, min_units_per_structure) -> bool:
        return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > min_units_per_structure and \
            len(FACTORY_UNITS.intersection(self.logical_inventory)) > min_units_per_structure and \
            len(STARPORT_UNITS.intersection(self.logical_inventory)) > min_units_per_structure

    def generate_reduced_inventory(self, inventory_size: int, mission_requirements: list[Callable]) -> list[Item]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory = list(self.item_pool)
        locked_items = list(self.locked_items)
        self.logical_inventory = {
            item.name for item in inventory + locked_items
            if item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing)
        }
        requirements = mission_requirements
        cascade_keys = self.cascade_removal_map.keys()
        units_always_have_upgrades = get_option_value(self.world, self.player, "units_always_have_upgrades")
        # Inventory restrictiveness based on number of missions with checks
        mission_order_type = get_option_value(self.world, self.player, "mission_order")
        mission_count = len(mission_orders[mission_order_type]) - 1
        min_units_per_structure = int(mission_count / 7)
        if min_units_per_structure > 0:
            requirements.append(lambda state: state.has_units_per_structure(min_units_per_structure))

        def attempt_removal(item: Item) -> bool:
            # If item can be removed and has associated items, remove them as well
            inventory.remove(item)
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if not all(requirement(self) for requirement in requirements):
                    # If item cannot be removed, lock or revert
                    self.logical_inventory.add(item.name)
                    locked_items.append(item)
                    return False
            return True

        while len(inventory) + len(locked_items) > inventory_size:
            if len(inventory) == 0:
                raise Exception("Reduced item pool generation failed - not enough locations available to place items.")
            # Select random item from removable items
            item = self.world.random.choice(inventory)
            # Cascade removals to associated items
            if item in cascade_keys:
                items_to_remove = self.cascade_removal_map[item]
                transient_items = []
                while len(items_to_remove) > 0:
                    item_to_remove = items_to_remove.pop()
                    if item_to_remove not in inventory:
                        continue
                    success = attempt_removal(item_to_remove)
                    if success:
                        transient_items.append(item_to_remove)
                    elif units_always_have_upgrades:
                        # Lock all associated items if any of them cannot be removed
                        transient_items += items_to_remove
                        locked_items += transient_items
                        self.logical_inventory = self.logical_inventory.union({
                            transient_item.name for transient_item in transient_items
                            if item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing)
                        })
                        break
            else:
                attempt_removal(item)

        return inventory + locked_items

    def _read_logic(self):
        self._sc2wol_has_common_unit = lambda world, player: SC2WoLLogic._sc2wol_has_common_unit(self, world, player)
        self._sc2wol_has_air = lambda world, player: SC2WoLLogic._sc2wol_has_air(self, world, player)
        self._sc2wol_has_air_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_air_anti_air(self, world, player)
        self._sc2wol_has_competent_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_competent_anti_air(self, world, player)
        self._sc2wol_has_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_anti_air(self, world, player)
        self._sc2wol_has_heavy_defense = lambda world, player: SC2WoLLogic._sc2wol_has_heavy_defense(self, world, player)
        self._sc2wol_has_competent_comp = lambda world, player: SC2WoLLogic._sc2wol_has_competent_comp(self, world, player)
        self._sc2wol_has_train_killers = lambda world, player: SC2WoLLogic._sc2wol_has_train_killers(self, world, player)
        self._sc2wol_able_to_rescue = lambda world, player: SC2WoLLogic._sc2wol_able_to_rescue(self, world, player)
        self._sc2wol_beats_protoss_deathball = lambda world, player: SC2WoLLogic._sc2wol_beats_protoss_deathball(self, world, player)
        self._sc2wol_survives_rip_field = lambda world, player: SC2WoLLogic._sc2wol_survives_rip_field(self, world, player)
        self._sc2wol_has_protoss_common_units = lambda world, player: SC2WoLLogic._sc2wol_has_protoss_common_units(self, world, player)
        self._sc2wol_has_protoss_medium_units = lambda world, player: SC2WoLLogic._sc2wol_has_protoss_medium_units(self, world, player)
        self._sc2wol_has_mm_upgrade = lambda world, player: SC2WoLLogic._sc2wol_has_mm_upgrade(self, world, player)
        self._sc2wol_has_manned_bunkers = lambda world, player: SC2WoLLogic._sc2wol_has_manned_bunkers(self, world, player)
        self._sc2wol_final_mission_requirements = lambda world, player: SC2WoLLogic._sc2wol_final_mission_requirements(self, world, player)

    def __init__(self, world: MultiWorld, player: int,
                 item_pool: list[Item], existing_items: list[Item], locked_items: list[Item],
                 has_protoss: bool):
        self.world = world
        self.player = player
        self.logical_inventory = set()
        self.locked_items = locked_items[:]
        self.existing_items = existing_items
        self._read_logic()
        # Initial filter of item pool
        self.item_pool = []
        item_quantities: dict[str, int] = dict()
        for item in item_pool:
            item_info = item_table[item.name]
            if item_info.type == "Upgrade":
                # All Upgrades are locked except for the final tier
                if item.name not in item_quantities:
                    item_quantities[item.name] = 0
                item_quantities[item.name] += 1
                if item_quantities[item.name] < item_info.quantity:
                    self.locked_items.append(item)
                else:
                    self.item_pool.append(item)
            elif item_info.type == "Goal":
                locked_items.append(item)
            elif item_info.type != "Protoss" or has_protoss:
                self.item_pool.append(item)
        self.cascade_removal_map: dict[Item, list[Item]] = dict()
        for item in self.item_pool + locked_items + existing_items:
            if item.name in UPGRADABLE_ITEMS:
                upgrades = get_item_upgrades(self.item_pool, item)
                associated_items = [*upgrades, item]
                self.cascade_removal_map[item] = associated_items
                if get_option_value(world, player, "units_always_have_upgrades"):
                    for upgrade in upgrades:
                        self.cascade_removal_map[upgrade] = associated_items


def filter_items(world: MultiWorld, player: int, mission_req_table: dict[str, MissionInfo], location_cache: list[Location],
                 item_pool: list[Item], existing_items: list[Item], locked_items: list[Item]) -> list[Item]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    has_protoss = bool(PROTOSS_REGIONS.intersection(mission_req_table.keys()))
    mission_requirements = [location.access_rule for location in location_cache]
    valid_inventory = ValidInventory(world, player, item_pool, existing_items, locked_items, has_protoss)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items
