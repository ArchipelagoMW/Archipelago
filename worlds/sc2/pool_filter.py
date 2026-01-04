import logging
from typing import Callable, Dict, List, Set, Tuple, TYPE_CHECKING, Iterable

from BaseClasses import Location, ItemClassification
from .item import StarcraftItem, ItemFilterFlags, item_names, item_parents, item_groups
from .item.item_tables import item_table, TerranItemType, ZergItemType, spear_of_adun_calldowns
from .options import RequiredTactics

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
        self.logical_inventory: Dict[str, int] = {}
        for item in item_pool:
            if not item_table[item.name].is_important_for_filtering():
                continue
            self.logical_inventory.setdefault(item.name, 0)
            self.logical_inventory[item.name] += 1
        self.item_pool = item_pool
        self.item_name_to_item: Dict[str, List[StarcraftItem]] = {}
        self.item_name_to_child_items: Dict[str, List[StarcraftItem]] = {}
        for item in item_pool:
            self.item_name_to_item.setdefault(item.name, []).append(item)
            for parent_item in item_parents.child_item_to_parent_items.get(item.name, []):
                self.item_name_to_child_items.setdefault(parent_item, []).append(item)

    def has(self, item: str, player: int, count: int = 1) -> bool:
        return self.logical_inventory.get(item, 0) >= count

    def has_any(self, items: Set[str], player: int) -> bool:
        return any(self.logical_inventory.get(item) for item in items)

    def has_all(self, items: Set[str], player: int) -> bool:
        return all(self.logical_inventory.get(item) for item in items)

    def has_group(self, item_group: str, player: int, count: int = 1) -> bool:
        return False  # Deliberately fails here, as item pooling is not aware about mission layout

    def count_group(self, item_name_group: str, player: int) -> int:
        return 0  # For item filtering assume no missions are beaten

    def count(self, item: str, player: int) -> int:
        return self.logical_inventory.get(item, 0)

    def count_from_list(self, items: Iterable[str], player: int) -> int:
        return sum(self.logical_inventory.get(item, 0) for item in items)

    def count_from_list_unique(self, items: Iterable[str], player: int) -> int:
        return sum(item in self.logical_inventory for item in items)

    def generate_reduced_inventory(self, inventory_size: int, filler_amount: int, mission_requirements: List[Tuple[str, Callable]]) -> List[StarcraftItem]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory: List[StarcraftItem] = list(self.item_pool)
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
        ) -> str:
            """
            Returns empty string and applies `remove_flag` if the item is removable,
            else returns a string containing failed locations and applies ItemFilterFlags.LogicLocked
            """
            # Only run logic checks when removing logic items
            if self.logical_inventory.get(item.name, 0) > 0:
                self.logical_inventory[item.name] -= 1
                failed_rules = [name for name, requirement in mission_requirements if not requirement(self)]
                if failed_rules:
                    # If item cannot be removed, lock and revert
                    self.logical_inventory[item.name] += 1
                    item.filter_flags |= ItemFilterFlags.LogicLocked
                    return f"{len(failed_rules)} rules starting with \"{failed_rules[0]}\""
                if not self.logical_inventory[item.name]:
                    del self.logical_inventory[item.name]
            item.filter_flags |= remove_flag
            return ""
        
        def remove_child_items(
            parent_item: StarcraftItem,
            remove_flag: ItemFilterFlags = ItemFilterFlags.FilterExcluded,
        ) -> None:
            child_items = self.item_name_to_child_items.get(parent_item.name, [])
            for child_item in child_items:
                if (ItemFilterFlags.AllowedOrphan|ItemFilterFlags.Unexcludable) & child_item.filter_flags:
                    continue
                parent_id = item_table[child_item.name].parent
                assert parent_id is not None
                if item_parents.parent_present[parent_id](self.logical_inventory, self.world.options):
                    continue
                if not attempt_removal(child_item, remove_flag):
                    remove_child_items(child_item, remove_flag)

        def cull_items_over_maximum(group: List[StarcraftItem], allowed_max: int) -> None:
            for item in group:
                if len([x for x in group if ItemFilterFlags.Culled not in x.filter_flags]) <= allowed_max:
                    break
                if ItemFilterFlags.Uncullable & item.filter_flags:
                    continue
                attempt_removal(item, remove_flag=ItemFilterFlags.Culled)

        def request_minimum_items(group: List[StarcraftItem], requested_minimum) -> None:
            for item in group:
                if len([x for x in group if ItemFilterFlags.RequestedOrBetter & x.filter_flags]) >= requested_minimum:
                    break
                if ItemFilterFlags.Culled & item.filter_flags:
                    continue
                item.filter_flags |= ItemFilterFlags.Requested

        # Process Excluded items, validate if the item can get actually excluded
        excluded_items: List[StarcraftItem] = [starcraft_item for starcraft_item in inventory if ItemFilterFlags.Excluded & starcraft_item.filter_flags]
        self.world.random.shuffle(excluded_items)
        for excluded_item in excluded_items:
            if ItemFilterFlags.Unexcludable & excluded_item.filter_flags:
                continue
            removal_failed = attempt_removal(excluded_item, remove_flag=ItemFilterFlags.Removed)
            if removal_failed:
                if ItemFilterFlags.UserExcluded in excluded_item.filter_flags:
                    logging.getLogger("Starcraft 2").warning(
                        f"Cannot exclude item {excluded_item.name} as it would break {removal_failed}"
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
        group: str = ""
        for group, group_member_names in item_parents.item_upgrade_groups.items():
            group_to_item[group] = []
            for item_name in group_member_names:
                inventory_items = self.item_name_to_item.get(item_name, [])
                group_to_item[group].extend(item for item in inventory_items if ItemFilterFlags.Removed not in item.filter_flags)

        # Limit the maximum number of upgrades
        if max_upgrades_per_unit != -1:
            for group_name, group_items in group_to_item.items():
                self.world.random.shuffle(group_to_item[group])
                cull_items_over_maximum(group_items, max_upgrades_per_unit)
        
        # Requesting minimum upgrades for items that have already been locked/placed when minimum required
        if min_upgrades_per_unit != -1:
            for group_name, group_items in group_to_item.items():
                self.world.random.shuffle(group_items)
                request_minimum_items(group_items, min_upgrades_per_unit)

        # Kerrigan max abilities
        kerrigan_actives = [item for item in inventory if item.name in item_groups.kerrigan_active_abilities]
        self.world.random.shuffle(kerrigan_actives)
        cull_items_over_maximum(kerrigan_actives, self.world.options.kerrigan_max_active_abilities.value)

        kerrigan_passives = [item for item in inventory if item.name in item_groups.kerrigan_passives]
        self.world.random.shuffle(kerrigan_passives)
        cull_items_over_maximum(kerrigan_passives, self.world.options.kerrigan_max_passive_abilities.value)

        # Spear of Adun max abilities
        spear_of_adun_actives = [item for item in inventory if item.name in spear_of_adun_calldowns]
        self.world.random.shuffle(spear_of_adun_actives)
        cull_items_over_maximum(spear_of_adun_actives, self.world.options.spear_of_adun_max_active_abilities.value)

        spear_of_adun_autocasts = [item for item in inventory if item.name in item_groups.spear_of_adun_passives]
        self.world.random.shuffle(spear_of_adun_autocasts)
        cull_items_over_maximum(spear_of_adun_autocasts, self.world.options.spear_of_adun_max_passive_abilities.value)

        # Nova items
        nova_weapon_items = [item for item in inventory if item.name in item_groups.nova_weapons]
        self.world.random.shuffle(nova_weapon_items)
        cull_items_over_maximum(nova_weapon_items, self.world.options.nova_max_weapons.value)

        nova_gadget_items = [item for item in inventory if item.name in item_groups.nova_gadgets]
        self.world.random.shuffle(nova_gadget_items)
        cull_items_over_maximum(nova_gadget_items, self.world.options.nova_max_gadgets.value)

        # Determining if the full-size inventory can complete campaign
        # Note(mm): Now that user excludes are checked against logic, this can probably never fail unless there's a bug.
        failed_locations: List[str] = [location for (location, requirement) in requirements if not requirement(self)]
        if len(failed_locations) > 0:
            raise Exception(f"Too many items excluded - couldn't satisfy access rules for the following locations:\n{failed_locations}")

        # Optionally locking generic items
        generic_items: List[StarcraftItem] = [
            starcraft_item for starcraft_item in inventory
            if starcraft_item.name in second_pass_placeable_items
               and (
                       not ItemFilterFlags.CulledOrBetter & starcraft_item.filter_flags
                       or ItemFilterFlags.RequestedOrBetter & starcraft_item.filter_flags
               )
        ]
        reserved_generic_percent = self.world.options.ensure_generic_items.value / 100
        reserved_generic_amount = int(len(generic_items) * reserved_generic_percent)
        self.world.random.shuffle(generic_items)
        for starcraft_item in generic_items[:reserved_generic_amount]:
            starcraft_item.filter_flags |= ItemFilterFlags.Requested

        # Main cull process
        def remove_random_item(
            removable: List[StarcraftItem],
            dont_remove_flags: ItemFilterFlags,
            remove_flag: ItemFilterFlags = ItemFilterFlags.Removed,
        ) -> bool:
            if len(removable) == 0:
                return False
            item = self.world.random.choice(removable)
            # Do not remove item if it would drop upgrades below minimum
            if min_upgrades_per_unit > 0:
                group_name = None
                parent = item_table[item.name].parent
                if parent is not None:
                    group_name = item_parents.parent_present[parent].constraint_group
                if group_name is not None:
                    children = group_to_item.get(group_name, [])
                    children = [x for x in children if not (ItemFilterFlags.CulledOrBetter & x.filter_flags)]
                    if len(children) <= min_upgrades_per_unit:
                        # Attempt to remove a parent instead, if possible
                        dont_remove = ItemFilterFlags.Removed|dont_remove_flags
                        parent_items = [
                            parent_item
                            for parent_name in item_parents.child_item_to_parent_items[item.name]
                            for parent_item in self.item_name_to_item.get(parent_name, [])
                            if not (dont_remove & parent_item.filter_flags)
                        ]
                        if parent_items:
                            item = self.world.random.choice(parent_items)
                        else:
                            # Lock remaining upgrades
                            for item in children:
                                item.filter_flags |= ItemFilterFlags.Locked
                            return False
            if not attempt_removal(item, remove_flag):
                remove_child_items(item, remove_flag)
                return True
            return False

        def item_included(item: StarcraftItem) -> bool:
            return bool(
                ItemFilterFlags.Removed not in item.filter_flags
                and ((ItemFilterFlags.Unexcludable|ItemFilterFlags.Excluded) & item.filter_flags) != ItemFilterFlags.Excluded
            )
        
        # Actually remove culled items; we won't re-add them
        inventory = [
            item for item in inventory
            if (((ItemFilterFlags.Uncullable|ItemFilterFlags.Culled) & item.filter_flags) != ItemFilterFlags.Culled)
        ]

        # Part 1: Remove items that are not requested
        start_inventory_size = len([item for item in inventory if ItemFilterFlags.StartInventory in item.filter_flags])
        current_inventory_size = len([item for item in inventory if item_included(item)])
        cullable_items = [item for item in inventory if not (ItemFilterFlags.Uncullable & item.filter_flags)]
        while current_inventory_size - start_inventory_size > inventory_size - filler_amount:
            if len(cullable_items) == 0:
                if filler_amount > 0:
                    filler_amount -= 1
                else:
                    break
            if remove_random_item(cullable_items, ItemFilterFlags.Uncullable):
                inventory = [item for item in inventory if ItemFilterFlags.Removed not in item.filter_flags]
                current_inventory_size = len([item for item in inventory if item_included(item)])
            cullable_items = [
                item for item in cullable_items
                if not ((ItemFilterFlags.Removed|ItemFilterFlags.Uncullable) & item.filter_flags)
            ]
        
        # Handle too many requested
        if current_inventory_size - start_inventory_size > inventory_size - filler_amount:
            for item in inventory:
                item.filter_flags &= ~ItemFilterFlags.Requested

        # Part 2: If we need to remove more, allow removing requested items
        excludable_items = [item for item in inventory if not (ItemFilterFlags.Unexcludable & item.filter_flags)]
        while current_inventory_size - start_inventory_size > inventory_size - filler_amount:
            if len(excludable_items) == 0:
                break
            if remove_random_item(excludable_items, ItemFilterFlags.Unexcludable):
                inventory = [item for item in inventory if ItemFilterFlags.Removed not in item.filter_flags]
                current_inventory_size = len([item for item in inventory if item_included(item)])
            excludable_items = [
                item for item in inventory
                if not ((ItemFilterFlags.Removed|ItemFilterFlags.Unexcludable) & item.filter_flags)
            ]

        # Part 3: If it still doesn't fit, move locked items to start inventory until it fits
        precollect_items = current_inventory_size - inventory_size - start_inventory_size - filler_amount
        if precollect_items > 0:
            promotable = [
                item
                for item in inventory
                if ItemFilterFlags.StartInventory not in item.filter_flags
                and ItemFilterFlags.Locked in item.filter_flags
            ]
            self.world.random.shuffle(promotable)
            for item in promotable[:precollect_items]:
                item.filter_flags |= ItemFilterFlags.StartInventory
                start_inventory_size += 1

        # Removing extra dependencies
        # Transport Hook
        if not self.logical_inventory.get(item_names.MEDIVAC):
            # Don't allow L2 Siege Tank Transport Hook without Medivac
            inventory_transport_hooks = [item for item in inventory if item.name == item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK]
            removable_transport_hooks = [item for item in inventory_transport_hooks if not (ItemFilterFlags.Unexcludable & item.filter_flags)]
            if len(inventory_transport_hooks) > 1 and removable_transport_hooks:
                inventory.remove(removable_transport_hooks[0])
        
        # Weapon/Armour upgrades
        def exclude_wa(prefix: str) -> List[StarcraftItem]:
            return [
                item for item in inventory
                if (ItemFilterFlags.UnexcludableUpgrade & item.filter_flags)
                or not item.name.startswith(prefix)
            ]
        used_item_names: Set[str] = {item.name for item in inventory}
        if used_item_names.isdisjoint(item_groups.barracks_wa_group):
            inventory = exclude_wa(item_names.TERRAN_INFANTRY_UPGRADE_PREFIX)
        if used_item_names.isdisjoint(item_groups.factory_wa_group):
            inventory = exclude_wa(item_names.TERRAN_VEHICLE_UPGRADE_PREFIX)
        if used_item_names.isdisjoint(item_groups.starport_wa_group):
            inventory = exclude_wa(item_names.TERRAN_SHIP_UPGRADE_PREFIX)
        if used_item_names.isdisjoint(item_groups.zerg_melee_wa):
            inventory = exclude_wa(item_names.PROGRESSIVE_ZERG_MELEE_ATTACK)
        if used_item_names.isdisjoint(item_groups.zerg_ranged_wa):
            inventory = exclude_wa(item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK)
        if used_item_names.isdisjoint(item_groups.zerg_air_units):
            inventory = exclude_wa(item_names.ZERG_FLYER_UPGRADE_PREFIX)
        if used_item_names.isdisjoint(item_groups.protoss_ground_wa):
            inventory = exclude_wa(item_names.PROTOSS_GROUND_UPGRADE_PREFIX)
        if used_item_names.isdisjoint(item_groups.protoss_air_wa):
            inventory = exclude_wa(item_names.PROTOSS_AIR_UPGRADE_PREFIX)
        
        # Part 4: Last-ditch effort to reduce inventory size; upgrades can go in start inventory
        current_inventory_size = len(inventory)
        precollect_items = current_inventory_size - inventory_size - start_inventory_size - filler_amount
        if precollect_items > 0:
            promotable = [
                item
                for item in inventory
                if ItemFilterFlags.StartInventory not in item.filter_flags
            ]
            self.world.random.shuffle(promotable)
            for item in promotable[:precollect_items]:
                item.filter_flags |= ItemFilterFlags.StartInventory
                start_inventory_size += 1
        
        assert current_inventory_size - start_inventory_size <= inventory_size - filler_amount, (
            f"Couldn't reduce inventory to fit. target={inventory_size}, poolsize={current_inventory_size}, "
            f"start_inventory={starcraft_item}, filler_amount={filler_amount}"
        )

        return inventory


def filter_items(world: 'SC2World', location_cache: List[Location], item_pool: List[StarcraftItem]) -> List[StarcraftItem]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    # Most of the excluded locations get actually removed but Victory ones are mandatory in order to allow the game
    # to progress normally. Since regular items aren't flagged as filler, we need to generate enough filler for those
    # locations as we need to have something that can be actually placed there.
    # Therefore, we reserve those to be filler.
    excluded_locations = [location for location in open_locations if location.name in world.options.exclude_locations.value]
    reserved_filler_count = len(excluded_locations)
    target_nonfiller_item_count = inventory_size - reserved_filler_count
    filler_amount = (inventory_size * world.options.filler_percentage) // 100
    if world.options.required_tactics.value == RequiredTactics.option_no_logic:
        mission_requirements = []
    else:
        mission_requirements = [(location.name, location.access_rule) for location in location_cache]
    valid_inventory = ValidInventory(world, item_pool)

    valid_items = valid_inventory.generate_reduced_inventory(target_nonfiller_item_count, filler_amount, mission_requirements)
    for _ in range(reserved_filler_count):
        filler_item = world.create_item(world.get_filler_item_name())
        if filler_item.classification & ItemClassification.progression:
            filler_item.classification = ItemClassification.filler # Must be flagged as Filler, even if it's a Kerrigan level
        valid_items.append(filler_item)
    return valid_items
