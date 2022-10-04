from typing import Callable
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import item_table
from .MissionTables import no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list,\
    mission_orders, starting_mission_locations, MissionInfo
from .Options import get_option_value
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
MIN_UNITS_PER_STRUCTURE = [
    3,   # Vanilla
    3,   # Vanilla Shuffled
    2,   # Mini Shuffle
    0    # Gauntlet
]

PROTOSS_REGIONS = {"A Sinister Turn", "Echoes of the Future", "In Utter Darkness"}

ALWAYS_USEFUL_ARMORY = [
    "Combat Shield (Marine)", "Stabilizer Medpacks (Medic)"  # Needed for no-build logic
]


def filter_missions(world: MultiWorld, player: int) -> dict[str, list[str]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(world, player, "mission_order")
    shuffle_protoss = get_option_value(world, player, "shuffle_protoss")
    relegate_no_build = get_option_value(world, player, "relegate_no_build")

    # Vanilla and Vanilla Shuffled use the entire mission pool
    if mission_order_type in (0, 1):
        return {
            'no_build': no_build_regions_list[:],
            'easy': easy_regions_list[:],
            'medium': medium_regions_list[:],
            'hard': hard_regions_list[:]
        }

    mission_count = 0
    for mission in mission_orders[mission_order_type]:
        if mission is None:
            continue
        if mission.type == 'all_in':  # All-In is placed separately
            continue
        mission_count += 1

    mission_sets = [
        set(no_build_regions_list),
        set(easy_regions_list),
        set(medium_regions_list),
        set(hard_regions_list)
    ]
    # Omitting Protoss missions if not shuffling protoss
    if not shuffle_protoss:
        for mission_set in mission_sets:
            mission_set.difference_update(PROTOSS_REGIONS)
    # Omitting No Build missions if relegating no-build
    if relegate_no_build:
        # The build missions in starting_mission_locations become the new "no build missions"
        mission_sets[0] = set(starting_mission_locations.keys())
        mission_sets[0].difference_update(no_build_regions_list)
        # Future-proofing in case a non-Easy mission is placed in starting_mission_locations
        for mission_set in mission_sets[1:]:
            mission_set.difference_update(mission_sets[0])
    # Removing random missions from each difficulty set in a cycle
    set_cycle = 0
    mission_pools = [list(mission_set) for mission_set in mission_sets]
    current_count = sum(len(mission_pool) for mission_pool in mission_pools)
    if current_count < mission_count:
        raise Exception('Not enough missions available to fill the campaign on current settings.')
    while current_count > mission_count:
        if set_cycle == 4:
            set_cycle = 0
        # Must contain at least one mission per set
        mission_pool = mission_pools[set_cycle]
        set_cycle += 1
        if len(mission_pool) == 1:
            continue
        mission_pool.remove(world.random.choice(mission_pool))
        current_count -= 1
    return {
        'no_build': mission_pools[0],
        'easy': mission_pools[1],
        'medium': mission_pools[2],
        'hard': mission_pools[3]
    }


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
        inventory = list(self.item_pool)
        locked_items = list(self.locked_items)
        self.logical_inventory = {item.name for item in self.progression_items.union(self.locked_items)}
        requirements = mission_requirements
        mission_order_type = get_option_value(self.world, self.player, "mission_order")
        min_units_per_structure = MIN_UNITS_PER_STRUCTURE[mission_order_type]
        if min_units_per_structure > 0:
            requirements.append(lambda state: state.has_units_per_structure(min_units_per_structure))
        while len(inventory) + len(locked_items) > inventory_size:
            if len(inventory) == 0:
                raise Exception('Reduced item pool generation failed.')
            # Select random item from removable items
            item = self.world.random.choice(inventory)
            inventory.remove(item)
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if all(requirement(self) for requirement in requirements):
                    # If item can be removed and is a unit, remove armory upgrades
                    # Some armory upgrades are kept regardless, as they remain logically relevant
                    if item.name in UPGRADABLE_ITEMS:
                        inventory = [
                            inv_item for inv_item in inventory
                            if inv_item.name in ALWAYS_USEFUL_ARMORY or not inv_item.name.endswith('(' + item.name + ')')
                        ]
                else:
                    # If item cannot be removed, move it to locked items
                    self.logical_inventory.add(item.name)
                    locked_items.append(item)
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
        self._sc2wol_has_bunker_unit = lambda world, player: SC2WoLLogic._sc2wol_has_bunker_unit(self, world, player)

    def __init__(self, world: MultiWorld, player: int,
                 item_pool: list[Item], existing_items: list[Item], locked_items: list[Item],
                 has_protoss: bool):
        self.world = world
        self.player = player
        self.logical_inventory = set()
        self.progression_items = set()
        self.locked_items = locked_items[:]
        self.existing_items = existing_items
        self._read_logic()
        # Initial filter of item pool
        self.item_pool = []
        item_quantities: dict[str, int] = dict()
        for item in item_pool:
            item_info = item_table[item.name]
            if item.classification == ItemClassification.progression:
                self.progression_items.add(item)
            if item_info.type == 'Upgrade':
                # All Upgrades are locked except for the final tier
                if item.name not in item_quantities:
                    item_quantities[item.name] = 0
                item_quantities[item.name] += 1
                if item_quantities[item.name] < item_info.quantity:
                    self.locked_items.append(item)
                else:
                    self.item_pool.append(item)
            elif item_info.type == 'Goal':
                locked_items.append(item)
            elif item_info.type != 'Protoss' or has_protoss:
                self.item_pool.append(item)


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
