from typing import Callable, Dict, List, Set
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import item_table
from .MissionTables import no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list,\
    mission_orders, get_starting_mission_locations, MissionInfo, vanilla_mission_req_table, alt_final_mission_locations
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


def filter_missions(multiworld: MultiWorld, player: int) -> Dict[str, List[str]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    shuffle_protoss = get_option_value(multiworld, player, "shuffle_protoss")
    excluded_missions = set(get_option_set_value(multiworld, player, "excluded_missions"))
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
            "all_in": ["All-In"]
        }

    mission_pools = [
        [],
        easy_regions_list,
        medium_regions_list,
        hard_regions_list
    ]
    # Omitting Protoss missions if not shuffling protoss
    if not shuffle_protoss:
        excluded_missions = excluded_missions.union(PROTOSS_REGIONS)
    # Replacing All-In on low mission counts
    if mission_count < 14:
        final_mission = multiworld.random.choice([mission for mission in alt_final_mission_locations.keys() if mission not in excluded_missions])
        excluded_missions.add(final_mission)
    else:
        final_mission = 'All-In'
    # Yaml settings determine which missions can be placed in the first slot
    mission_pools[0] = [mission for mission in get_starting_mission_locations(multiworld, player).keys() if mission not in excluded_missions]
    # Removing the new no-build missions from their original sets
    for i in range(1, len(mission_pools)):
        mission_pools[i] = [mission for mission in mission_pools[i] if mission not in excluded_missions.union(mission_pools[0])]
    # If the first mission is a build mission, there may not be enough locations to reach Outbreak as a second mission
    if not get_option_value(multiworld, player, 'shuffle_no_build'):
        # Swapping Outbreak and The Great Train Robbery
        if "Outbreak" in mission_pools[1]:
            mission_pools[1].remove("Outbreak")
            mission_pools[2].append("Outbreak")
        if "The Great Train Robbery" in mission_pools[2]:
            mission_pools[2].remove("The Great Train Robbery")
            mission_pools[1].append("The Great Train Robbery")
    # Removing random missions from each difficulty set in a cycle
    set_cycle = 0
    current_count = sum(len(mission_pool) for mission_pool in mission_pools)

    if current_count < mission_count:
        raise Exception("Not enough missions available to fill the campaign on current settings.  Please exclude fewer missions.")
    while current_count > mission_count:
        if set_cycle == 4:
            set_cycle = 0
        # Must contain at least one mission per set
        mission_pool = mission_pools[set_cycle]
        if len(mission_pool) <= 1:
            if all(len(mission_pool) <= 1 for mission_pool in mission_pools):
                raise Exception("Not enough missions available to fill the campaign on current settings.  Please exclude fewer missions.")
        else:
            mission_pool.remove(multiworld.random.choice(mission_pool))
            current_count -= 1
        set_cycle += 1

    return {
        "no_build": mission_pools[0],
        "easy": mission_pools[1],
        "medium": mission_pools[2],
        "hard": mission_pools[3],
        "all_in": [final_mission]
    }


def get_item_upgrades(inventory: List[Item], parent_item: Item or str):
    item_name = parent_item.name if isinstance(parent_item, Item) else parent_item
    return [
        inv_item for inv_item in inventory
        if item_table[inv_item.name].parent_item == item_name
    ]


class ValidInventory:

    def has(self, item: str, player: int):
        return item in self.logical_inventory

    def has_any(self, items: Set[str], player: int):
        return any(item in self.logical_inventory for item in items)

    def has_all(self, items: Set[str], player: int):
        return all(item in self.logical_inventory for item in items)

    def has_units_per_structure(self) -> bool:
        return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(FACTORY_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(STARPORT_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure

    def generate_reduced_inventory(self, inventory_size: int, mission_requirements: List[Callable]) -> List[Item]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory = list(self.item_pool)
        locked_items = list(self.locked_items)
        self.logical_inventory = {
            item.name for item in inventory + locked_items + self.existing_items
            if item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing)
        }
        requirements = mission_requirements
        cascade_keys = self.cascade_removal_map.keys()
        units_always_have_upgrades = get_option_value(self.multiworld, self.player, "units_always_have_upgrades")
        if self.min_units_per_structure > 0:
            requirements.append(lambda state: state.has_units_per_structure())

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
            item = self.multiworld.random.choice(inventory)
            # Cascade removals to associated items
            if item in cascade_keys:
                items_to_remove = self.cascade_removal_map[item]
                transient_items = []
                cascade_failure = False
                while len(items_to_remove) > 0:
                    item_to_remove = items_to_remove.pop()
                    transient_items.append(item_to_remove)
                    if item_to_remove not in inventory:
                        if units_always_have_upgrades and item_to_remove in locked_items:
                            cascade_failure = True
                            break
                        else:
                            continue
                    success = attempt_removal(item_to_remove)
                    if not success and units_always_have_upgrades:
                        cascade_failure = True
                        transient_items += items_to_remove
                        break
                # Lock all associated items if any of them cannot be removed on Units Always Have Upgrades
                if cascade_failure:
                    for transient_item in transient_items:
                        if transient_item in inventory:
                            inventory.remove(transient_item)
                        if transient_item not in locked_items:
                            locked_items.append(transient_item)
                        if transient_item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing):
                            self.logical_inventory.add(transient_item.name)
            else:
                attempt_removal(item)

        return inventory + locked_items

    def _read_logic(self):
        self._sc2wol_has_common_unit = lambda world, player: SC2WoLLogic._sc2wol_has_common_unit(self, world, player)
        self._sc2wol_has_air = lambda world, player: SC2WoLLogic._sc2wol_has_air(self, world, player)
        self._sc2wol_has_air_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_air_anti_air(self, world, player)
        self._sc2wol_has_competent_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_competent_anti_air(self, world, player)
        self._sc2wol_has_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_anti_air(self, world, player)
        self._sc2wol_defense_rating = lambda world, player, zerg_enemy, air_enemy=False: SC2WoLLogic._sc2wol_defense_rating(self, world, player, zerg_enemy, air_enemy)
        self._sc2wol_has_competent_comp = lambda world, player: SC2WoLLogic._sc2wol_has_competent_comp(self, world, player)
        self._sc2wol_has_train_killers = lambda world, player: SC2WoLLogic._sc2wol_has_train_killers(self, world, player)
        self._sc2wol_able_to_rescue = lambda world, player: SC2WoLLogic._sc2wol_able_to_rescue(self, world, player)
        self._sc2wol_beats_protoss_deathball = lambda world, player: SC2WoLLogic._sc2wol_beats_protoss_deathball(self, world, player)
        self._sc2wol_survives_rip_field = lambda world, player: SC2WoLLogic._sc2wol_survives_rip_field(self, world, player)
        self._sc2wol_has_protoss_common_units = lambda world, player: SC2WoLLogic._sc2wol_has_protoss_common_units(self, world, player)
        self._sc2wol_has_protoss_medium_units = lambda world, player: SC2WoLLogic._sc2wol_has_protoss_medium_units(self, world, player)
        self._sc2wol_has_mm_upgrade = lambda world, player: SC2WoLLogic._sc2wol_has_mm_upgrade(self, world, player)
        self._sc2wol_final_mission_requirements = lambda world, player: SC2WoLLogic._sc2wol_final_mission_requirements(self, world, player)

    def __init__(self, multiworld: MultiWorld, player: int,
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item],
                 has_protoss: bool):
        self.multiworld = multiworld
        self.player = player
        self.logical_inventory = set()
        self.locked_items = locked_items[:]
        self.existing_items = existing_items
        self._read_logic()
        # Initial filter of item pool
        self.item_pool = []
        item_quantities: dict[str, int] = dict()
        # Inventory restrictiveness based on number of missions with checks
        mission_order_type = get_option_value(self.multiworld, self.player, "mission_order")
        mission_count = len(mission_orders[mission_order_type]) - 1
        self.min_units_per_structure = int(mission_count / 7)
        min_upgrades = 1 if mission_count < 10 else 2
        for item in item_pool:
            item_info = item_table[item.name]
            if item_info.type == "Upgrade":
                # Locking upgrades based on mission duration
                if item.name not in item_quantities:
                    item_quantities[item.name] = 0
                item_quantities[item.name] += 1
                if item_quantities[item.name] < min_upgrades:
                    self.locked_items.append(item)
                else:
                    self.item_pool.append(item)
            elif item_info.type == "Goal":
                locked_items.append(item)
            elif item_info.type != "Protoss" or has_protoss:
                self.item_pool.append(item)
        self.cascade_removal_map: Dict[Item, List[Item]] = dict()
        for item in self.item_pool + locked_items + existing_items:
            if item.name in UPGRADABLE_ITEMS:
                upgrades = get_item_upgrades(self.item_pool, item)
                associated_items = [*upgrades, item]
                self.cascade_removal_map[item] = associated_items
                if get_option_value(multiworld, player, "units_always_have_upgrades"):
                    for upgrade in upgrades:
                        self.cascade_removal_map[upgrade] = associated_items


def filter_items(multiworld: MultiWorld, player: int, mission_req_table: Dict[str, MissionInfo], location_cache: List[Location],
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item]) -> List[Item]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    has_protoss = bool(PROTOSS_REGIONS.intersection(mission_req_table.keys()))
    mission_requirements = [location.access_rule for location in location_cache]
    valid_inventory = ValidInventory(multiworld, player, item_pool, existing_items, locked_items, has_protoss)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items
