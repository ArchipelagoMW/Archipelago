from typing import Callable, Dict, List, Set
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import get_full_item_list, spider_mine_sources, second_pass_placeable_items, filler_items, \
    progressive_if_nco
from .MissionTables import no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list,\
    mission_orders, MissionInfo, alt_final_mission_locations, MissionPools
from .Options import get_option_value, MissionOrder, FinalMap, MissionProgressLocations, LocationInclusion
from .LogicMixin import SC2WoLLogic

# Items with associated upgrades
UPGRADABLE_ITEMS = [
    "Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre",
    "Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor", "Predator", "Widow Mine", "Cyclone",
    "Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser", "Raven", "Science Vessel", "Liberator", "Valkyrie",
    "Bunker", "Missile Turret"
]

BARRACKS_UNITS = {"Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre"}
FACTORY_UNITS = {"Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor", "Predator", "Widow Mine", "Cyclone"}
STARPORT_UNITS = {"Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser", "Hercules", "Science Vessel", "Raven", "Liberator", "Valkyrie"}

PROTOSS_REGIONS = {"A Sinister Turn", "Echoes of the Future", "In Utter Darkness"}


def filter_missions(multiworld: MultiWorld, player: int) -> Dict[int, List[str]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    shuffle_no_build = get_option_value(multiworld, player, "shuffle_no_build")
    shuffle_protoss = get_option_value(multiworld, player, "shuffle_protoss")
    excluded_missions = get_option_value(multiworld, player, "excluded_missions")
    final_map = get_option_value(multiworld, player, "final_map")
    mission_pools = {
        MissionPools.STARTER: no_build_regions_list[:],
        MissionPools.EASY: easy_regions_list[:],
        MissionPools.MEDIUM: medium_regions_list[:],
        MissionPools.HARD: hard_regions_list[:],
        MissionPools.FINAL: []
    }
    if mission_order_type == MissionOrder.option_vanilla:
        # Vanilla uses the entire mission pool
        mission_pools[MissionPools.FINAL] = ['All-In']
        return mission_pools
    # Omitting No-Build missions if not shuffling no-build
    if not shuffle_no_build:
        excluded_missions = excluded_missions.union(no_build_regions_list)
    # Omitting Protoss missions if not shuffling protoss
    if not shuffle_protoss:
        excluded_missions = excluded_missions.union(PROTOSS_REGIONS)
    # Replacing All-In with alternate ending depending on option
    if final_map == FinalMap.option_random_hard:
        final_mission = multiworld.random.choice([mission for mission in alt_final_mission_locations.keys() if mission not in excluded_missions])
        excluded_missions.add(final_mission)
    else:
        final_mission = 'All-In'
    # Excluding missions
    for difficulty, mission_pool in mission_pools.items():
        mission_pools[difficulty] = [mission for mission in mission_pool if mission not in excluded_missions]
    mission_pools[MissionPools.FINAL].append(final_mission)
    # Mission pool changes on Build-Only
    if not get_option_value(multiworld, player, 'shuffle_no_build'):
        def move_mission(mission_name, current_pool, new_pool):
            if mission_name in mission_pools[current_pool]:
                mission_pools[current_pool].remove(mission_name)
                mission_pools[new_pool].append(mission_name)
        # Replacing No Build missions with Easy missions
        move_mission("Zero Hour", MissionPools.EASY, MissionPools.STARTER)
        move_mission("Evacuation", MissionPools.EASY, MissionPools.STARTER)
        move_mission("Devil's Playground", MissionPools.EASY, MissionPools.STARTER)
        # Pushing Outbreak to Normal, as it cannot be placed as the second mission on Build-Only
        move_mission("Outbreak", MissionPools.EASY, MissionPools.MEDIUM)
        # Pushing extra Normal missions to Easy
        move_mission("The Great Train Robbery", MissionPools.MEDIUM, MissionPools.EASY)
        move_mission("Echoes of the Future", MissionPools.MEDIUM, MissionPools.EASY)
        move_mission("Cutthroat", MissionPools.MEDIUM, MissionPools.EASY)
        # Additional changes on Advanced Tactics
        if get_option_value(multiworld, player, "required_tactics") > 0:
            move_mission("The Great Train Robbery", MissionPools.EASY, MissionPools.STARTER)
            move_mission("Smash and Grab", MissionPools.EASY, MissionPools.STARTER)
            move_mission("Moebius Factor", MissionPools.MEDIUM, MissionPools.EASY)
            move_mission("Welcome to the Jungle", MissionPools.MEDIUM, MissionPools.EASY)
            move_mission("Engine of Destruction", MissionPools.HARD, MissionPools.MEDIUM)

    return mission_pools


def get_item_upgrades(inventory: List[Item], parent_item: Item or str):
    item_name = parent_item.name if isinstance(parent_item, Item) else parent_item
    return [
        inv_item for inv_item in inventory
        if get_full_item_list()[inv_item.name].parent_item == item_name
    ]


def get_item_quantity(item: Item, multiworld: MultiWorld, player: int):
    if (not get_option_value(multiworld, player, "nco_items")) \
            and item.name in progressive_if_nco:
        return 1
    return get_full_item_list()[item.name].quantity


def copy_item(item: Item):
    return Item(item.name, item.classification, item.code, item.player)


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

        def attempt_removal(item: Item) -> bool:
            # If item can be removed and has associated items, remove them as well
            inventory.remove(item)
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if not all(requirement(self) for requirement in requirements):
                    # If item cannot be removed, lock or revert
                    self.logical_inventory.add(item.name)
                    for _ in range(get_item_quantity(item, self.multiworld, self.player)):
                        locked_items.append(copy_item(item))
                    return False
            return True

        # Limit the maximum number of upgrades 
        maxUpgrad = get_option_value(self.multiworld, self.player,
                            "max_number_of_upgrades")
        if maxUpgrad != -1:
            unit_avail_upgrades = {}
            # Needed to take into account locked/existing items
            unit_nb_upgrades = {}
            for item in inventory:
                cItem = get_full_item_list()[item.name]
                if cItem.type in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
                    unit_avail_upgrades[item.name] = []
                    unit_nb_upgrades[item.name] = 0
                elif cItem.parent_item is not None:
                    if cItem.parent_item not in unit_avail_upgrades:
                        unit_avail_upgrades[cItem.parent_item] = [item]
                        unit_nb_upgrades[cItem.parent_item] = 1
                    else:
                        unit_avail_upgrades[cItem.parent_item].append(item)
                        unit_nb_upgrades[cItem.parent_item] += 1
            # For those two categories, we count them but dont include them in removal
            for item in locked_items + self.existing_items:
                cItem = get_full_item_list()[item.name]
                if cItem.type in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
                    unit_avail_upgrades[item.name] = []
                    unit_nb_upgrades[item.name] = 0
                elif cItem.parent_item is not None:
                    if cItem.parent_item not in unit_avail_upgrades:
                        unit_nb_upgrades[cItem.parent_item] = 1
                    else:
                        unit_nb_upgrades[cItem.parent_item] += 1
            # Making sure that the upgrades being removed is random 
            # Currently, only for combat shield vs Stabilizer Medpacks...
            shuffled_unit_upgrade_list = list(unit_avail_upgrades.keys())
            self.multiworld.random.shuffle(shuffled_unit_upgrade_list)
            for unit in shuffled_unit_upgrade_list:
                while (unit_nb_upgrades[unit] > maxUpgrad) \
                         and (len(unit_avail_upgrades[unit]) > 0):
                    itemCandidate = self.multiworld.random.choice(unit_avail_upgrades[unit])
                    _ = attempt_removal(itemCandidate)
                    # Whatever it succeed to remove the iventory or it fails and thus 
                    # lock it, the upgrade is no longer available for removal
                    unit_avail_upgrades[unit].remove(itemCandidate)
                    unit_nb_upgrades[unit] -= 1

        # Locking associated items for items that have already been placed when units_always_have_upgrades is on
        if units_always_have_upgrades:
            existing_items = set(self.existing_items[:] + locked_items)
            while existing_items:
                existing_item = existing_items.pop()
                items_to_lock = self.cascade_removal_map.get(existing_item, [existing_item])
                if get_full_item_list()[existing_item.name].type != "Upgrade":
                    # Don't process general upgrades, they may have been pre-locked per-level
                    for item in items_to_lock:
                        if item in inventory:
                            item_quantity = inventory.count(item)
                            # Unit upgrades, lock all levels
                            for _ in range(item_quantity):
                                inventory.remove(item)
                            if item not in locked_items:
                                # Lock all the associated items if not already locked
                                for _ in range(item_quantity):
                                    locked_items.append(copy_item(item))
                        if item in existing_items:
                            existing_items.remove(item)

        if self.min_units_per_structure > 0 and self.has_units_per_structure():
            requirements.append(lambda state: state.has_units_per_structure())

        # Determining if the full-size inventory can complete campaign
        if not all(requirement(self) for requirement in requirements):
            raise Exception("Too many items excluded - campaign is impossible to complete.")

        while len(inventory) + len(locked_items) > inventory_size:
            if len(inventory) == 0:
                # There are more items than locations and all of them are already locked due to YAML or logic.
                # Random items from locked ones will go to starting items
                self.multiworld.random.shuffle(locked_items)
                while len(locked_items) > inventory_size:
                    item: Item = locked_items.pop()
                    self.multiworld.push_precollected(item)
                break
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
                            for _ in range(inventory.count(transient_item)):
                                inventory.remove(transient_item)
                        if transient_item not in locked_items:
                            for _ in range(get_item_quantity(transient_item, self.multiworld, self.player)):
                                locked_items.append(copy_item(transient_item))
                        if transient_item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing):
                            self.logical_inventory.add(transient_item.name)
            else:
                attempt_removal(item)

        if not spider_mine_sources & self.logical_inventory:
            inventory = [item for item in inventory if not item.name.endswith("(Spider Mine)")]
        if not BARRACKS_UNITS & self.logical_inventory:
            inventory = [item for item in inventory if
                         not (item.name.startswith("Progressive Infantry") or item.name == "Orbital Strike")]
        if not FACTORY_UNITS & self.logical_inventory:
            inventory = [item for item in inventory if not item.name.startswith("Progressive Vehicle")]
        if not STARPORT_UNITS & self.logical_inventory:
            inventory = [item for item in inventory if not item.name.startswith("Progressive Ship")]

        # Cull finished, adding locked items back into inventory
        inventory += locked_items

        # Replacing empty space with generically useful items
        replacement_items = [item for item in self.item_pool
                             if (item not in inventory
                                 and item not in self.locked_items
                                 and item.name in second_pass_placeable_items)]
        self.multiworld.random.shuffle(replacement_items)
        while len(inventory) < inventory_size and len(replacement_items) > 0:
            item = replacement_items.pop()
            inventory.append(item)

        return inventory

    def _read_logic(self):
        self._sc2wol_has_common_unit = lambda world, player: SC2WoLLogic._sc2wol_has_common_unit(self, world, player)
        self._sc2wol_has_air = lambda world, player: SC2WoLLogic._sc2wol_has_air(self, world, player)
        self._sc2wol_has_air_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_air_anti_air(self, world, player)
        self._sc2wol_has_competent_anti_air = lambda world, player: SC2WoLLogic._sc2wol_has_competent_anti_air(self, world, player)
        self._sc2wol_has_competent_ground_to_air = lambda world, player: SC2WoLLogic._sc2wol_has_competent_ground_to_air(self, world, player)
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
        self._sc2wol_welcome_to_the_jungle_requirement = lambda world, player: SC2WoLLogic._sc2wol_welcome_to_the_jungle_requirement(self, world, player)
        self._sc2wol_can_respond_to_colony_infestations = lambda world, player: SC2WoLLogic._sc2wol_can_respond_to_colony_infestations(self, world, player)
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
            item_info = get_full_item_list()[item.name]
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
