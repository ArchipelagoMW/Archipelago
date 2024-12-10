import copy
import logging
from typing import Callable, Dict, List, Set, Union, Tuple, TYPE_CHECKING, Iterable

from BaseClasses import Item, Location
from .item import StarcraftItem, ItemFilterFlags, item_names, item_parents
from .item.item_tables import item_table, TerranItemType, ZergItemType, ProtossItemType
from .options import get_option_value, RequiredTactics

if TYPE_CHECKING:
    from . import SC2World


# Items that can be placed before resources if not already in
# General upgrades and Mercs
second_pass_placeable_items: Tuple[str, ...] = (
    # Global weapon/armor upgrades
    item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
    item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
    item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
    item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    item_names.PROGRESSIVE_PROTOSS_SHIELDS,
    # Terran Buildings without upgrades
    item_names.SENSOR_TOWER,
    item_names.HIVE_MIND_EMULATOR,
    item_names.PSI_DISRUPTER,
    item_names.PERDITION_TURRET,
    # General Terran upgrades without any dependencies
    item_names.SCV_ADVANCED_CONSTRUCTION,
    item_names.SCV_DUAL_FUSION_WELDERS,
    item_names.SCV_CONSTRUCTION_JUMP_JETS,
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    item_names.PROGRESSIVE_ORBITAL_COMMAND,
    item_names.ULTRA_CAPACITORS,
    item_names.VANADIUM_PLATING,
    item_names.ORBITAL_DEPOTS,
    item_names.MICRO_FILTERING,
    item_names.AUTOMATED_REFINERY,
    item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR,
    item_names.COMMAND_CENTER_SCANNER_SWEEP,
    item_names.COMMAND_CENTER_MULE,
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES,
    item_names.TECH_REACTOR,
    item_names.CELLULAR_REACTOR,
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL,  # Place only L1
    item_names.STRUCTURE_ARMOR,
    item_names.HI_SEC_AUTO_TRACKING,
    item_names.ADVANCED_OPTICS,
    item_names.ROGUE_FORCES,
    # Mercenaries (All races)
    *[item_name for item_name, item_data in item_table.items()
      if item_data.type in (TerranItemType.Mercenary, ZergItemType.Mercenary)],
    # Kerrigan and Nova levels, abilities and generally useful stuff
    *[item_name for item_name, item_data in item_table.items()
      if item_data.type in (
        ZergItemType.Level,
        ZergItemType.Ability,
        ZergItemType.Evolution_Pit,
        TerranItemType.Nova_Gear
        )],
    item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
    # Zerg static defenses
    item_names.SPORE_CRAWLER,
    item_names.SPINE_CRAWLER,
    # Overseer
    item_names.OVERLORD_OVERSEER_ASPECT,
    # Spear of Adun Abilities
    item_names.SOA_CHRONO_SURGE,
    item_names.SOA_PROGRESSIVE_PROXY_PYLON,
    item_names.SOA_PYLON_OVERCHARGE,
    item_names.SOA_ORBITAL_STRIKE,
    item_names.SOA_TEMPORAL_FIELD,
    item_names.SOA_SOLAR_LANCE,
    item_names.SOA_MASS_RECALL,
    item_names.SOA_SHIELD_OVERCHARGE,
    item_names.SOA_DEPLOY_FENIX,
    item_names.SOA_PURIFIER_BEAM,
    item_names.SOA_TIME_STOP,
    item_names.SOA_SOLAR_BOMBARDMENT,
    # Protoss generic upgrades
    item_names.MATRIX_OVERLOAD,
    item_names.QUATRO,
    item_names.NEXUS_OVERCHARGE,
    item_names.ORBITAL_ASSIMILATORS,
    item_names.WARP_HARMONIZATION,
    item_names.GUARDIAN_SHELL,
    item_names.RECONSTRUCTION_BEAM,
    item_names.OVERWATCH,
    item_names.SUPERIOR_WARP_GATES,
    item_names.KHALAI_INGENUITY,
    item_names.AMPLIFIED_ASSIMILATORS,
    # Protoss static defenses
    item_names.PHOTON_CANNON,
    item_names.KHAYDARIN_MONOLITH,
    item_names.SHIELD_BATTERY,
)


def copy_item(item: StarcraftItem) -> StarcraftItem:
    return StarcraftItem(item.name, item.classification, item.code, item.player, item.filter_flags)


class ValidInventory:
    def __init__(self, world: 'SC2World', item_pool: List[StarcraftItem]) -> None:
        self.multiworld = world.multiworld
        self.player = world.player
        self.world: 'SC2World' = world
        # Track all Progression items and those with complex rules for filtering
        self.logical_inventory: List[str] = [
            item.name for item in item_pool
            if item_table[item.name].is_important_for_filtering()
        ]
        self.item_pool = item_pool
        self.item_name_to_item: Dict[str, List[StarcraftItem]] = {}
        self.item_name_to_child_items: Dict[str, List[StarcraftItem]] = {}
        for item in item_pool:
            self.item_name_to_item.setdefault(item.name, []).append(item)
            for parent_item in item_parents.child_item_to_parent_items.get(item.name, []):
                self.item_name_to_child_items.setdefault(parent_item, []).append(item)

    def has(self, item: str, player: int):
        return item in self.logical_inventory

    def has_any(self, items: Set[str], player: int):
        return any(item in self.logical_inventory for item in items)

    def has_all(self, items: Set[str], player: int):
        return all(item in self.logical_inventory for item in items)

    def has_group(self, item_group: str, player: int, count: int = 1):
        return False  # Deliberately fails here, as item pooling is not aware about mission layout

    def count_group(self, item_name_group: str, player: int) -> int:
        return 0  # For item filtering assume no missions are beaten

    def count(self, item: str, player: int) -> int:
        return len([inventory_item for inventory_item in self.logical_inventory if inventory_item == item])

    def count_from_list(self, items: Iterable[str], player: int) -> int:
        return sum(self.count(item_name, player) for item_name in items)

    def generate_reduced_inventory(self, inventory_size: int, mission_requirements: List[Tuple[str, Callable]]) -> List[StarcraftItem]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory: List[StarcraftItem] = list(self.item_pool)
        # locked_items: List[StarcraftItem] = list(self.locked_items)
        # necessary_items: List[StarcraftItem] = list(self.necessary_items)
        requirements = mission_requirements
        min_upgrades_per_unit = self.world.options.min_number_of_upgrades.value
        max_upgrades_per_unit = self.world.options.max_number_of_upgrades.value
        if max_upgrades_per_unit > -1 and min_upgrades_per_unit > max_upgrades_per_unit:
            logging.getLogger("Starcraft 2").warning(
                f"min upgrades per unit is greater than max upgrades per unit ({min_upgrades_per_unit} > {max_upgrades_per_unit}). "
                f"Setting both to minimum value ({min_upgrades_per_unit})"
            )
            max_upgrades_per_unit = min_upgrades_per_unit

        def attempt_removal(
            item: StarcraftItem,
            remove_flag: ItemFilterFlags = ItemFilterFlags.FilterExcluded,
            lock_flag: ItemFilterFlags = ItemFilterFlags.Locked
        ) -> bool:
            """
            Returns true and applies `remove_flag` if the item is removable,
            else returns false and applies `lock_flag`
            """
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if not all(requirement(self) for (_, requirement) in mission_requirements):
                    # If item cannot be removed, lock or revert
                    self.logical_inventory.append(item.name)
                    # Note(mm): Be sure to re-add the _exact_ item we removed.
                    # Removing from `inventory` searches based on == checks, but AutoWorld.py
                    # checks using `is` to make sure there are no duplicate item objects in the pool.
                    # Hence, appending `item` could cause sporadic generation failures.
                    item.filter_flags |= lock_flag
                    return False
            item.filter_flags |= remove_flag
            return True
        
        def remove_child_items(
            parent_item: StarcraftItem,
            remove_flag: ItemFilterFlags = ItemFilterFlags.FilterExcluded,
            lock_flag: ItemFilterFlags = ItemFilterFlags.Locked
        ) -> None:
            child_items = self.item_name_to_child_items.get(parent_item.name, [])
            for child_item in child_items:
                if (ItemFilterFlags.AllowedOrphan|ItemFilterFlags.Unexcludable) & child_item.filter_flags:
                    continue
                parent_id = item_table[child_item.name].parent_item
                assert parent_id is not None
                if item_parents.parent_present[parent_id](self.logical_inventory, self.world.options):
                    continue
                if attempt_removal(child_item, remove_flag, lock_flag):
                    remove_child_items(child_item, remove_flag, lock_flag)

        # Process Excluded items, validate if the item can get actually excluded
        excluded_items: List[StarcraftItem] = [starcraft_item for starcraft_item in inventory if ItemFilterFlags.Excluded & starcraft_item.filter_flags]
        self.world.random.shuffle(excluded_items)
        for excluded_item in excluded_items:
            if ItemFilterFlags.Unexcludable & excluded_item.filter_flags:
                continue
            if not attempt_removal(excluded_item, remove_flag=ItemFilterFlags.Removed):
                if ItemFilterFlags.UserExcluded in excluded_item.filter_flags:
                    logging.getLogger("Starcraft 2").warning(
                        f"Cannot exclude item {excluded_item.name} as it would break a logic rule"
                    )
                else:
                    assert False, f"Item filtering excluded an item which is logically required: {excluded_item.name}"
                continue
            remove_child_items(excluded_item, remove_flag=ItemFilterFlags.Removed)
        inventory = [item for item in inventory if ItemFilterFlags.Removed not in item.filter_flags]

        # Clear excluded flags; all existing ones should be implemented or out-of-logic
        for item in inventory:
            item.filter_flags &= ~ItemFilterFlags.Excluded

        # Determine item groups to be constrained by min/max upgrades per unit
        group_to_item: Dict[str, List[StarcraftItem]] = {}
        for group, group_member_names in item_parents.item_upgrade_groups.items():
            group_to_item[group] = []
            for item_name in group_member_names:
                inventory_items = self.item_name_to_item.get(item_name, [])
                group_to_item[group].extend(item for item in inventory_items if ItemFilterFlags.Removed not in item.filter_flags)
            self.world.random.shuffle(group_to_item[group])

        # Limit the maximum number of upgrades
        if max_upgrades_per_unit != -1:
            for group_name, group_items in group_to_item.items():
                for item in group_items:
                    if len([x for x in group_items if ItemFilterFlags.Culled not in x.filter_flags]) <= max_upgrades_per_unit:
                        break
                    if ItemFilterFlags.Uncullable & item.filter_flags:
                        continue
                    attempt_removal(item, remove_flag=ItemFilterFlags.Culled)
                self.world.random.shuffle(group_items)
        
        # Requesting minimum upgrades for items that have already been locked/placed when minimum required
        if min_upgrades_per_unit != -1:
            for group_name, group_items in group_to_item.items():
                for item in group_items:
                    if len([x for x in group_items if ItemFilterFlags.RequestedOrBetter & x.filter_flags]) >= min_upgrades_per_unit:
                        break
                    if ItemFilterFlags.Culled & item.filter_flags:
                        continue
                    item.filter_flags |= ItemFilterFlags.Requested

        # Determining if the full-size inventory can complete campaign
        # Note(mm): Now that user excludes are checked against logic, this can probably never fail unless there's a bug.
        failed_locations: List[str] = [location for (location, requirement) in requirements if not requirement(self)]
        if len(failed_locations) > 0:
            raise Exception(f"Too many items excluded - couldn't satisfy access rules for the following locations:\n{failed_locations}")

        # Optionally locking generic items
        generic_items: List[StarcraftItem] = [starcraft_item for starcraft_item in inventory if starcraft_item.name in second_pass_placeable_items]
        reserved_generic_percent = self.world.options.ensure_generic_items.value / 100
        reserved_generic_amount = int(len(generic_items) * reserved_generic_percent)
        self.world.random.shuffle(generic_items)
        for starcraft_item in generic_items[:reserved_generic_amount]:
            starcraft_item.filter_flags |= ItemFilterFlags.Requested

        # Make an index from child to parent
        child_to_main_parent: Dict[str, StarcraftItem] = {}
        for item in inventory:
            parent_id = item_table[item.name].parent_item
            if parent_id is None:
                continue
            parent_item_name = item_parents.parent_present[parent_id].main_item
            if parent_item_name is None:
                continue
            parent_item = self.item_name_to_item.get(parent_item_name)
            if parent_item:
                child_to_main_parent[item.name] = parent_item[0]

        # Main cull process
        def remove_random_item(removable: List[StarcraftItem], remove_flag: ItemFilterFlags = ItemFilterFlags.Removed) -> bool:
            item = self.world.random.choice(removable)
            # Do not remove item if it would drop upgrades below minimum
            if min_upgrades_per_unit > 0:
                parent_item = child_to_main_parent.get(item.name)
                if parent_item is not None:
                    children = self.item_name_to_child_items.get(parent_item.name, [])
                    children = [x for x in children if not (ItemFilterFlags.CulledOrBetter & x.filter_flags)]
                    count = len(children)
                    if count <= min_upgrades_per_unit:
                        if parent_item in removable:
                            # Attempt to remove parent instead, if possible
                            item = parent_item
                        else:
                            # Lock remaining upgrades
                            for item in children:
                                item.filter_flags |= ItemFilterFlags.Locked
                            return False
            if attempt_removal(item, remove_flag):
                remove_child_items(item, remove_flag)
                return True
            return False

        def item_included(item: StarcraftItem) -> bool:
            return (
                ItemFilterFlags.Removed not in item.filter_flags
                or (ItemFilterFlags.Unexcludable & item.filter_flags)
                or (not (ItemFilterFlags.Excluded & item.filter_flags)
                    and (ItemFilterFlags.Requested & item.filter_flags)
                )
                or not (ItemFilterFlags.Culled & item.filter_flags)
            ) != 0

        # Part 1: Remove items that are not requested
        start_inventory_size = len([item for item in inventory if ItemFilterFlags.StartInventory in item.filter_flags])
        current_inventory_size = len([item for item in inventory if item_included(item)])
        while current_inventory_size - start_inventory_size > inventory_size:
            cullable_items = [item for item in inventory if not (ItemFilterFlags.Uncullable & item.filter_flags)]
            if len(cullable_items) == 0:
                break
            if remove_random_item(cullable_items):
                inventory = [item for item in inventory if ItemFilterFlags.Removed not in item.filter_flags]
                current_inventory_size = len([item for item in inventory if item_included(item)])
        
        # Handle too many requested
        if current_inventory_size - start_inventory_size > inventory_size:
            for item in inventory:
                item.filter_flags &= ~ItemFilterFlags.Requested

        # Part 2: If we need to remove more, allow removing requested items
        while current_inventory_size - start_inventory_size > inventory_size:
            excludable_items = [item for item in inventory if not (ItemFilterFlags.Unexcludable & item.filter_flags)]
            if len(excludable_items) == 0:
                break
            if remove_random_item(excludable_items):
                inventory = [item for item in inventory if ItemFilterFlags.Removed not in item.filter_flags]
                current_inventory_size = len([item for item in inventory if item_included(item)])

        # Part 3: If it still doesn't fit, move locked items to start inventory until it fits
        precollect_items = current_inventory_size - inventory_size - start_inventory_size
        if precollect_items > 0:
            items_to_start_inventory = self.world.random.choices(inventory, k=precollect_items, weights=[
                ItemFilterFlags.StartInventory not in item.filter_flags
                and ItemFilterFlags.Locked in item.filter_flags
                for item in inventory
            ])
            for item in items_to_start_inventory:
                item.filter_flags |= ItemFilterFlags.StartInventory
                start_inventory_size += 1

        assert current_inventory_size - start_inventory_size <= inventory_size
        inventory = [item for item in inventory if item_included(item)]

        # Removing extra dependencies
        # Transport Hook
        if item_names.MEDIVAC not in self.logical_inventory:
            # Don't allow L2 Siege Tank Transport Hook without Medivac
            inventory_transport_hooks = [item for item in inventory if item.name == item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK]
            if len(inventory_transport_hooks) > 1:
                inventory.remove(inventory_transport_hooks[0])

        return inventory


def filter_items(world: 'SC2World', location_cache: List[Location], item_pool: List[StarcraftItem]) -> List[StarcraftItem]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    if world.options.required_tactics.value == RequiredTactics.option_no_logic:
        mission_requirements = []
    else:
        mission_requirements = [(location.name, location.access_rule) for location in location_cache]
    valid_inventory = ValidInventory(world, item_pool)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items
