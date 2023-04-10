from typing import Callable, Dict, List, Set
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import item_table
from .MissionTables import no_build_regions_list, starter_regions_list, easy_regions_list, medium_regions_list, hard_regions_list,\
    mission_orders, MissionInfo, alt_final_mission_locations, MissionPools
from .Options import get_option_value
from .LogicMixin import SC2HotSLogic

# Items with associated upgrades
# UPGRADABLE_ITEMS = [
#     "Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre",
#     "Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor",
#     "Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser",
#     "Bunker", "Missile Turret"
# ]
UPGRADABLE_ITEMS = [
    "Zergling", "Roach", "Hydralisk", "Baneling", "Mutalisk", "Swarm Host", "Ultralisk"
]

# BARRACKS_UNITS = {"Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre"}
# FACTORY_UNITS = {"Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor", "Predator"}
# STARPORT_UNITS = {"Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser", "Hercules", "Science Vessel", "Raven"}

# PROTOSS_REGIONS = {"A Sinister Turn", "Echoes of the Future", "In Utter Darkness"}


def filter_missions(multiworld: MultiWorld, player: int) -> Dict[int, List[str]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    shuffle_no_build = get_option_value(multiworld, player, "shuffle_no_build")
    kerriganless = get_option_value(multiworld, player, "kerriganless") > 0
    logic_level = get_option_value(multiworld, player, "required_tactics")
    # shuffle_protoss = get_option_value(multiworld, player, "shuffle_protoss")
    excluded_missions = get_option_value(multiworld, player, "excluded_missions")
    mission_count = len(mission_orders[mission_order_type]) - 1
    mission_pools = {
        MissionPools.STARTER: starter_regions_list[:],
        MissionPools.EASY: easy_regions_list[:],
        MissionPools.MEDIUM: medium_regions_list[:],
        MissionPools.HARD: hard_regions_list[:],
        MissionPools.FINAL: []
    }
    if mission_order_type == 0:
        # Vanilla uses the entire mission pool
        mission_pools[MissionPools.FINAL] = ['The Reckoning']
        # mission_pools[MissionPools.FINAL] = ['All-In']
        return mission_pools
    elif mission_order_type == 1:
        # Vanilla Shuffled ignores the player-provided excluded missions
        excluded_missions = set()
    # Omitting No-Build missions if not shuffling no-build
    if not shuffle_no_build:
        excluded_missions = excluded_missions.union(no_build_regions_list)
    # Omitting Protoss missions if not shuffling protoss
    # if not shuffle_protoss:
    #     excluded_missions = excluded_missions.union(PROTOSS_REGIONS)
    # Replacing The Reckoning on low mission counts
    if mission_count < 13:
        final_mission = multiworld.random.choice([mission for mission in alt_final_mission_locations.keys() if mission not in excluded_missions])
        excluded_missions.add(final_mission)
    else:
        final_mission = 'The Reckoning'
    # Excluding missions
    for difficulty, mission_pool in mission_pools.items():
        mission_pools[difficulty] = [mission for mission in mission_pool if mission not in excluded_missions]
    mission_pools[MissionPools.FINAL].append(final_mission)
    # Mission pool changes
    def move_mission(mission_name, current_pool, new_pool):
        if mission_name in mission_pools[current_pool]:
            mission_pools[current_pool].remove(mission_name)
            mission_pools[new_pool].append(mission_name)
    if len(mission_pools[MissionPools.STARTER]) < 2 and not kerriganless or logic_level > 0:
        # Conditionally moving Easy missions to Starter
        move_mission("Harvest of Screams", MissionPools.EASY, MissionPools.STARTER)
        move_mission("Domination", MissionPools.EASY, MissionPools.STARTER)
    if logic_level > 0:
        # Medium -> Easy
        for mission in ("Fire in the Sky", "Waking the Ancient", "Conviction"):
            move_mission(mission, MissionPools.MEDIUM, MissionPools.EASY)
        # Hard -> Medium
        move_mission("Phantoms of the Void", MissionPools.HARD, MissionPools.MEDIUM)
        if not kerriganless:
            # Additional starter mission assuming player starts with minimal anti-air
            move_mission("Waking the Ancient", MissionPools.EASY, MissionPools.STARTER)

    return mission_pools


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

    # def has_units_per_structure(self) -> bool:
    #     return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
    #         len(FACTORY_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
    #         len(STARPORT_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure

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

        # Locking associated items for items that have already been placed when units_always_have_upgrades is on
        if units_always_have_upgrades:
            existing_items = self.existing_items[:]
            while existing_items:
                existing_item = existing_items.pop()
                items_to_lock = self.cascade_removal_map.get(existing_item, [existing_item])
                for item in items_to_lock:
                    if item in inventory:
                        inventory.remove(item)
                        locked_items.append(item)
                    if item in existing_items:
                        existing_items.remove(item)

        # if self.min_units_per_structure > 0 and self.has_units_per_structure():
        #     requirements.append(lambda state: state.has_units_per_structure())

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

        # Determining if the full-size inventory can complete campaign
        if not all(requirement(self) for requirement in requirements):
            raise Exception("Too many items excluded - campaign is impossible to complete.")

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
        # Removing extra dependencies (HotS)
        if "Baneling" in self.logical_inventory and\
           "Zergling" not in self.logical_inventory and\
           "Spawn Banelings (Kerrigan Tier 4)" not in self.logical_inventory:
            inventory = [item for item in inventory if "Baneling" not in item.name]
        if "Mutalisk" not in self.logical_inventory:
            inventory = [item for item in inventory if not item.name.startswith("Progressive Flyer")]
            locked_items = [item for item in locked_items if not item.name.startswith("Progressive Flyer")]

        # Cull finished, adding locked items back into inventory
        inventory += locked_items

        # Replacing empty space with generically useful items
        replacement_items = [item for item in self.item_pool
                             if item not in inventory and
                             item not in self.locked_items and
                             item_table[item.name].type in ("Ability", "Level")]
        self.multiworld.random.shuffle(replacement_items)
        while len(inventory) < inventory_size and len(replacement_items) > 0:
            item = replacement_items.pop()
            inventory.append(item)

        return inventory

    def _read_logic(self):
        self._sc2hots_has_common_unit = lambda world, player: SC2HotSLogic._sc2hots_has_common_unit(self, world, player)
        self._sc2hots_has_good_antiair = lambda world, player: SC2HotSLogic._sc2hots_has_good_antiair(self, world, player)
        self._sc2hots_has_minimal_antiair = lambda world, player: SC2HotSLogic._sc2hots_has_minimal_antiair(self, world, player)
        self._sc2hots_has_brood_lord = lambda world, player: SC2HotSLogic._sc2hots_has_brood_lord(self, world, player)
        self._sc2hots_has_viper = lambda world, player: SC2HotSLogic._sc2hots_has_viper(self, world, player)
        self._sc2hots_has_impaler_or_lurker = lambda world, player: SC2HotSLogic._sc2hots_has_impaler_or_lurker(self, world, player)
        self._sc2hots_has_competent_comp = lambda world, player: SC2HotSLogic._sc2hots_has_competent_comp(self, world, player)
        self._sc2hots_has_basic_comp = lambda world, player: SC2HotSLogic._sc2hots_has_basic_comp(self, world, player)
        # self._sc2wol_has_train_killers = lambda world, player: SC2HotSLogic._sc2wol_has_train_killers(self, world, player)
        self._sc2hots_can_spread_creep = lambda world, player: SC2HotSLogic._sc2hots_can_spread_creep(self, world, player)
        self._sc2hots_has_competent_defense = lambda world, player: SC2HotSLogic._sc2hots_has_competent_defense(self, world, player)
        # self._sc2wol_survives_rip_field = lambda world, player: SC2HotSLogic._sc2wol_survives_rip_field(self, world, player)
        # self._sc2wol_has_protoss_common_units = lambda world, player: SC2HotSLogic._sc2wol_has_protoss_common_units(self, world, player)
        # self._sc2wol_has_protoss_medium_units = lambda world, player: SC2HotSLogic._sc2wol_has_protoss_medium_units(self, world, player)
        # self._sc2wol_has_mm_upgrade = lambda world, player: SC2HotSLogic._sc2wol_has_mm_upgrade(self, world, player)
        self._sc2hots_has_basic_kerrigan = lambda world, player: SC2HotSLogic._sc2hots_has_basic_kerrigan(self, world, player)
        self._sc2hots_has_two_kerrigan_actives = lambda world, player: SC2HotSLogic._sc2hots_has_two_kerrigan_actives(self, world, player)
        self._sc2hots_has_low_tech = lambda world, player: SC2HotSLogic._sc2hots_has_low_tech(self, world, player)
        self._sc2hots_cleared_missions = lambda world, player, number: SC2HotSLogic._sc2hots_cleared_missions(self, world, player, number)

    def __init__(self, multiworld: MultiWorld, player: int, item_pool: List[Item],
                 existing_items: List[Item], locked_items: List[Item]):
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
        # self.min_units_per_structure = int(mission_count / 7)
        min_upgrades = 1 if mission_count < 7 else 2
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
            # elif item_info.type != "Protoss" or has_protoss:
            else:
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
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item], inventory_size: int) -> List[Item]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    # has_protoss = bool(PROTOSS_REGIONS.intersection(mission_req_table.keys()))
    mission_requirements = [location.access_rule for location in location_cache]
    valid_inventory = ValidInventory(multiworld, player, item_pool, existing_items, locked_items)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items
