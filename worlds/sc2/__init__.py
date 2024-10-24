from dataclasses import fields
import enum
import logging

from typing import *
from math import floor, ceil
from dataclasses import dataclass
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification, CollectionState
from Options import Accessibility
from worlds.AutoWorld import WebWorld, World
from . import item_names
from .items import (
    StarcraftItem, filler_items, get_full_item_list, ProtossItemType,
    ItemData, kerrigan_actives, kerrigan_passives,
    not_balanced_starting_units,
)
from . import items
from . import item_groups
from . import location_groups
from .locations import get_locations, DEFAULT_LOCATION_LIST, get_location_types, get_location_flags, get_plando_locations
from .options import (
    get_option_value, LocationInclusion, KerriganLevelItemDistribution,
    KerriganPresence, KerriganPrimalStatus, kerrigan_unit_available, StarterUnit, SpearOfAdunPresence,
    get_enabled_campaigns, SpearOfAdunAutonomouslyCastAbilityPresence, Starcraft2Options,
    GrantStoryTech, GenericUpgradeResearch, GenericUpgradeItems, RequiredTactics,
    upgrade_included_names
)
from .rules import get_basic_units
from . import settings
from .pool_filter import filter_items
from .mission_tables import (
    SC2Campaign, SC2Mission, SC2Race, MissionFlag
)
from .regions import create_mission_order
from .mission_order.structs import SC2MissionOrder

logger = logging.getLogger("Starcraft 2")


class ItemFilterFlags(enum.IntFlag):
    Available = 0
    Locked = enum.auto()
    StartInventory = enum.auto()
    NonLocal = enum.auto()
    Removed = enum.auto()
    Plando = enum.auto()
    Excluded = enum.auto()
    AllowedOrphan = enum.auto()
    """Used to flag items that shouldn't be filtered out with their parents"""
    ForceProgression = enum.auto()
    """Used to flag items that aren't classified as progression by default"""
    Necessary = enum.auto()
    """Used to flag items that are never allowed to be culled.
    This differs from `Locked` in that locked items may still be culled if there's space issues or in some circumstances when a parent item is culled."""

    Unremovable = Locked|StartInventory|Plando|Necessary


@dataclass
class FilterItem:
    name: str
    data: ItemData
    index: int = 0
    flags: ItemFilterFlags = ItemFilterFlags.Available


class Starcraft2WebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor", "Phaneros"]
    )

    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Neocerber"]
    )

    custom_mission_orders_en = Tutorial(
        "Custom Mission Order Usage Guide",
        "Documentation for the `custom_mission_order` YAML option",
        "English",
        "en_Custom Mission Orders.md",
        "custom_mission_orders/en",
        ["Salzkorn"]
    )

    tutorials = [setup_en, setup_fr, custom_mission_orders_en]


class SC2World(World):
    """
    StarCraft II is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Play as one of three factions across four campaigns in a battle for supremacy of the Koprulu Sector.
    """

    game = "Starcraft 2"
    web = Starcraft2WebWorld()
    settings: ClassVar[settings.Starcraft2Settings]

    item_name_to_id = {name: data.code for name, data in get_full_item_list().items()}
    location_name_to_id = {location.name: location.code for location in DEFAULT_LOCATION_LIST}
    options_dataclass = Starcraft2Options
    options: Starcraft2Options

    item_name_groups = item_groups.item_name_groups
    location_name_groups = location_groups.get_location_groups()
    locked_locations: List[str]
    """Locations locked to contain specific items, such as victory events or forced resources"""
    location_cache: List[Location]
    final_missions: List[int]
    required_client_version = 0, 4, 5
    custom_mission_order: SC2MissionOrder
    has_barracks_unit: bool = True
    has_factory_unit: bool = True
    has_starport_unit: bool = True
    has_zerg_melee_unit: bool = True
    has_zerg_ranged_unit: bool = True
    has_zerg_air_unit: bool = True
    has_protoss_ground_unit: bool = True
    has_protoss_air_unit: bool = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2World, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.custom_mission_order = create_mission_order(
            self, get_locations(self), self.location_cache
        )

    def create_items(self):
        # Starcraft 2-specific item setup:
        # * Filter item pool based on player options
        # * Plando starter units
        # * Start-inventory units if necessary for logic
        # * Plando filler items based on location exclusions
        # * If the item pool is less than the location count, add some filler items

        setup_events(self.player, self.locked_locations, self.location_cache)

        item_list: List[FilterItem] = create_and_flag_explicit_item_locks_and_excludes(self)
        flag_excludes_by_faction_presence(self, item_list)
        flag_mission_based_item_excludes(self, item_list)
        flag_allowed_orphan_items(self, item_list)
        flag_start_inventory(self, item_list)
        flag_unused_upgrade_types(self, item_list)
        flag_user_excluded_item_sets(self, item_list)
        flag_war_council_items(self, item_list)
        flag_and_add_resource_locations(self, item_list)
        flag_mission_order_required_items(self, item_list)
        pool: List[Item] = prune_item_pool(self, item_list)
        pad_item_pool_with_filler(self, len(self.location_cache) - len(self.locked_locations) - len(pool), pool)

        push_precollected_items_to_multiworld(self, item_list)

        self.multiworld.itempool += pool

        # Tell the logic which unit classes are used for required W/A upgrades
        used_item_names: Set[str] = {item.name for item in item_list}
        used_item_names = used_item_names.union(item.name for item in self.multiworld.itempool if item.player == self.player)
        if used_item_names.isdisjoint(item_groups.barracks_units):
            self.has_barracks_unit = False
        if used_item_names.isdisjoint(item_groups.factory_units):
            self.has_factory_unit = False
        if used_item_names.isdisjoint(item_groups.starport_units):
            self.has_starport_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_melee_wa):
            self.has_zerg_melee_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_ranged_wa):
            self.has_zerg_ranged_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_air_units):
            self.has_zerg_air_unit = False
        if used_item_names.isdisjoint(item_groups.protoss_ground_wa):
            self.has_protoss_ground_unit = False
        if used_item_names.isdisjoint(item_groups.protoss_air_wa):
            self.has_protoss_air_unit = False

    def set_rules(self) -> None:
        if self.options.required_tactics == RequiredTactics.option_no_logic:
            # Forcing completed goal and minimal accessibility on no logic
            self.options.accessibility.value = Accessibility.option_minimal
            required_items = self.custom_mission_order.get_items_to_lock()
            self.multiworld.completion_condition[self.player] = lambda state, required_items=required_items: all(
                state.has(item, self.player, amount) for (item, amount) in required_items.items()
            )
        else:
            self.multiworld.completion_condition[self.player] = self.custom_mission_order.get_completion_condition(self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in [field.name for field in fields(Starcraft2Options)]:
            option = get_option_value(self, option_name)
            if type(option) in {str, int}:
                slot_data[option_name] = int(option)

        enabled_campaigns = get_enabled_campaigns(self)
        slot_data["plando_locations"] = get_plando_locations(self)
        slot_data["nova_covert_ops_only"] = (enabled_campaigns == {SC2Campaign.NCO})
        slot_data["final_mission_ids"] = self.custom_mission_order.get_final_mission_ids()
        slot_data["custom_mission_order"] = self.custom_mission_order.get_slot_data()
        slot_data["version"] = 4

        if SC2Campaign.HOTS not in enabled_campaigns:
            slot_data["kerrigan_presence"] = KerriganPresence.option_not_present
        return slot_data


def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address is None:
            item = Item(location.name, ItemClassification.progression, None, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def create_and_flag_explicit_item_locks_and_excludes(world: SC2World) -> List[FilterItem]:
    """
    Handles `excluded_items`, `locked_items`, and `start_inventory`
    Returns a list of all possible non-filler items that can be added, with an accompanying flags bitfield.
    """
    excluded_items = world.options.excluded_items
    unexcluded_items = world.options.unexcluded_items
    locked_items = world.options.locked_items
    start_inventory = world.options.start_inventory
    key_items = world.custom_mission_order.get_items_to_lock()

    def resolve_count(count: Optional[int], max_count: int) -> int:
        if count == 0:
            return max_count
        if count is None:
            return 0
        if max_count == 0:
            return count
        return min(count, max_count)

    result: List[FilterItem] = []
    for item_name, item_data in items.item_table.items():
        max_count = item_data.quantity
        excluded_count = excluded_items.get(item_name)
        unexcluded_count = unexcluded_items.get(item_name)
        locked_count = locked_items.get(item_name)
        start_count: Optional[int] = start_inventory.get(item_name)
        key_count = key_items.get(item_name, 0)
        # specifying 0 in the yaml means exclude / lock all
        # start_inventory doesn't allow specifying 0
        # not specifying means don't exclude/lock/start
        excluded_count = resolve_count(excluded_count, max_count)
        unexcluded_count = resolve_count(unexcluded_count, max_count)
        locked_count = resolve_count(locked_count, max_count)
        start_count = resolve_count(start_count, max_count)

        excluded_count = max(0, excluded_count - unexcluded_count)

        # Priority: start_inventory >> locked_items >> excluded_items >> unspecified
        if max_count == 0:
            if excluded_count:
                logger.warning(f"Item {item_name} was listed as excluded, but as a filler item, it cannot be explicitly excluded.")
            excluded_count = 0
            max_count = start_count + locked_count
        elif start_count > max_count:
            logger.warning(f"Item {item_name} had start amount greater than maximum amount ({start_count} > {max_count}). Capping start amount to max.")
            start_count = max_count
            locked_count = 0
            excluded_count = 0
        elif locked_count + start_count > max_count:
            logger.warning(f"Item {item_name} had locked + start amount greater than maximum amount "
                f"({locked_count} + {start_count} > {max_count}). Capping locked amount to max - start.")
            locked_count = max_count - start_count
            excluded_count = 0
        elif excluded_count + locked_count + start_count > max_count:
            logger.warning(f"Item {item_name} had excluded + locked + start amounts greater than maximum amount "
                f"({excluded_count} + {locked_count} + {start_count} > {max_count}). Decreasing excluded amount.")
            excluded_count = max_count - start_count - locked_count
        # Make sure the final count creates enough items to satisfy key requirements
        final_count = max(max_count - excluded_count, key_count)
        for index in range(final_count):
            result.append(FilterItem(item_name, item_data, index))
            if index < start_count:
                result[-1].flags |= ItemFilterFlags.StartInventory
            if index < locked_count + start_count:
                result[-1].flags |= ItemFilterFlags.Locked
            if item_name in world.options.non_local_items:
                result[-1].flags |= ItemFilterFlags.NonLocal
    return result


def flag_excludes_by_faction_presence(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes items based on if their faction has a mission present where they can be used"""
    missions = get_all_missions(world.custom_mission_order)
    if world.options.take_over_ai_allies.value:
        terran_missions = [mission for mission in missions if (MissionFlag.Terran|MissionFlag.AiTerranAlly) & mission.flags]
        zerg_missions = [mission for mission in missions if (MissionFlag.Zerg|MissionFlag.AiZergAlly) & mission.flags]
        protoss_missions = [mission for mission in missions if (MissionFlag.Protoss|MissionFlag.AiProtossAlly) & mission.flags]
    else:
        terran_missions = [mission for mission in missions if MissionFlag.Terran in mission.flags]
        zerg_missions = [mission for mission in missions if MissionFlag.Zerg in mission.flags]
        protoss_missions = [mission for mission in missions if MissionFlag.Protoss in mission.flags]
    terran_build_missions = [mission for mission in terran_missions if MissionFlag.NoBuild not in mission.flags]
    zerg_build_missions = [mission for mission in zerg_missions if MissionFlag.NoBuild not in mission.flags]
    protoss_build_missions = [mission for mission in protoss_missions if MissionFlag.NoBuild not in mission.flags]
    auto_upgrades_in_nobuilds = (
        world.options.generic_upgrade_research.value
        in (GenericUpgradeResearch.option_always_auto, GenericUpgradeResearch.option_auto_in_no_build)
    )

    for item in item_list:
        # Catch-all for all of a faction's items
        if (not terran_missions and item.data.race == SC2Race.TERRAN):
            item.flags |= ItemFilterFlags.Excluded
            continue
        if (not zerg_missions and item.data.race == SC2Race.ZERG):
            item.flags |= ItemFilterFlags.Excluded
            continue
        if (not protoss_missions and item.data.race == SC2Race.PROTOSS):
            if item.name not in item_groups.soa_items:
                item.flags |= ItemFilterFlags.Excluded
            continue
        
        # Faction units
        if (not terran_build_missions
            and item.data.type in (items.TerranItemType.Unit, items.TerranItemType.Building, items.TerranItemType.Mercenary)
        ):
            item.flags |= ItemFilterFlags.Excluded
        if (not zerg_build_missions
            and item.data.type in (items.ZergItemType.Unit, items.ZergItemType.Mercenary, items.ZergItemType.Evolution_Pit)
        ):
            if (SC2Mission.ENEMY_WITHIN not in missions
                or world.options.grant_story_tech.value == GrantStoryTech.option_true
                or item.name not in (item_names.ZERGLING, item_names.ROACH, item_names.HYDRALISK, item_names.INFESTOR)
            ):
                item.flags |= ItemFilterFlags.Excluded
        if (not protoss_build_missions
            and item.data.type in (
                items.ProtossItemType.Unit,
                items.ProtossItemType.Unit_2,
                items.ProtossItemType.Building,
            )
        ):
            # Note(mm): This doesn't exclude things like automated assimilators or warp gate improvements
            # because that item type is mixed in with e.g. Reconstruction Beam and Overwatch
            if (SC2Mission.TEMPLAR_S_RETURN not in missions
                or world.options.grant_story_tech.value == GrantStoryTech.option_true
                or item.name not in (
                    item_names.IMMORTAL, item_names.ANNIHILATOR,
                    item_names.COLOSSUS, item_names.VANGUARD, item_names.REAVER, item_names.DARK_TEMPLAR,
                    item_names.SENTRY, item_names.HIGH_TEMPLAR,
                )
            ):
                item.flags |= ItemFilterFlags.Excluded
        
        # Faction +attack/armour upgrades
        if (item.data.type == items.TerranItemType.Upgrade
            and not terran_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.Excluded
        if (item.data.type == items.ZergItemType.Upgrade
            and not zerg_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.Excluded
        if (item.data.type == items.ProtossItemType.Upgrade
            and not protoss_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.Excluded


def flag_mission_based_item_excludes(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Excludes items based on mission / campaign presence: Nova Gear, Kerrigan abilities, SOA
    """
    missions = get_all_missions(world.custom_mission_order)

    kerrigan_missions = [mission for mission in missions if MissionFlag.Kerrigan in mission.flags]
    kerrigan_build_missions = [mission for mission in kerrigan_missions if MissionFlag.NoBuild not in mission.flags]
    nova_missions = [mission for mission in missions if MissionFlag.Nova in mission.flags]

    kerrigan_is_present = len(kerrigan_missions) > 0 and world.options.kerrigan_presence == KerriganPresence.option_vanilla

    # TvZ build missions -- check flags Terran and VsZerg are true and NoBuild is false
    tvz_build_mask = MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.NoBuild
    tvz_expect_value = MissionFlag.Terran|MissionFlag.VsZerg
    if world.options.take_over_ai_allies:
        tvz_build_mask |= MissionFlag.AiTerranAlly
        tvz_expect_value |= MissionFlag.AiTerranAlly
    tvz_build_missions = [mission for mission in missions if tvz_build_mask & mission.flags == tvz_expect_value]

    # Check if SOA actives should be present
    if world.options.spear_of_adun_presence != SpearOfAdunPresence.option_not_present:
        soa_missions = missions
        if not world.options.spear_of_adun_present_in_no_build:
            soa_missions = [m for m in soa_missions if MissionFlag.NoBuild not in m.flags]
        if world.options.spear_of_adun_presence == SpearOfAdunPresence.option_lotv_protoss:
            soa_missions = [m for m in soa_missions if m.campaign == SC2Campaign.LOTV]
        elif world.options.spear_of_adun_presence == SpearOfAdunPresence.option_protoss:
            soa_missions = [m for m in soa_missions if MissionFlag.Protoss in m.flags]
        
        soa_presence = len(soa_missions) > 0
    else:
        soa_presence = False
    
    # Check if SOA passives should be present
    if world.options.spear_of_adun_autonomously_cast_ability_presence != SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present:
        soa_missions = missions
        if not world.options.spear_of_adun_autonomously_cast_present_in_no_build:
            soa_missions = [m for m in soa_missions if MissionFlag.NoBuild not in m.flags]
        if world.options.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_lotv_protoss:
            soa_missions = [m for m in soa_missions if m.campaign == SC2Campaign.LOTV]
        elif world.options.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_protoss:
            soa_missions = [m for m in soa_missions if MissionFlag.Protoss in m.flags]
        
        soa_passive_presence = len(soa_missions) > 0
    else:
        soa_passive_presence = False

    for item in item_list:
        # Filter Nova equipment if you never get Nova
        if not nova_missions and (item.name in item_groups.nova_equipment):
            item.flags |= ItemFilterFlags.Excluded
        
        # Todo(mm): How should no-build only / grant_story_tech affect excluding Kerrigan items?
        # Exclude Primal form based on Kerrigan presence or primal form option
        if (item.data.type == items.ZergItemType.Primal_Form
            and ((not kerrigan_is_present) or world.options.kerrigan_primal_status != KerriganPrimalStatus.option_item)
        ):
            item.flags |= ItemFilterFlags.Excluded
        
        # Remove Kerrigan abilities if there's no kerrigan
        if item.data.type == items.ZergItemType.Ability:
            if not kerrigan_is_present:
                item.flags |= ItemFilterFlags.Excluded
            elif world.options.grant_story_tech and not kerrigan_build_missions:
                item.flags |= ItemFilterFlags.Excluded
        
        # Remove Spear of Adun if it's off
        if item.name in items.spear_of_adun_calldowns and not soa_presence:
            item.flags |= ItemFilterFlags.Excluded

        # Remove Spear of Adun passives
        if item.name in items.spear_of_adun_castable_passives and not soa_passive_presence:
            item.flags |= ItemFilterFlags.Excluded
        
        # Remove Psi Disrupter and Hive Mind Emulator if you never play a build TvZ
        if (item.name in (item_names.HIVE_MIND_EMULATOR, item_names.PSI_DISRUPTER)
            and not tvz_build_missions
        ):
            item.flags |= ItemFilterFlags.Excluded
    return


def flag_allowed_orphan_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Adds the `Allowed_Orphan` flag to items that shouldn't be filtered with their parents, like combat shield"""
    missions = get_all_missions(world.custom_mission_order)
    terran_nobuild_missions = any((MissionFlag.Terran|MissionFlag.NoBuild) in  mission.flags for mission in missions)
    for item in item_list:
        if item.name in (
            item_names.MARINE_COMBAT_SHIELD, item_names.MARINE_PROGRESSIVE_STIMPACK, item_names.MARINE_MAGRAIL_MUNITIONS,
            item_names.MEDIC_STABILIZER_MEDPACKS, item_names.MEDIC_NANO_PROJECTOR,
        ) and terran_nobuild_missions:
            item.flags |= ItemFilterFlags.AllowedOrphan


def flag_start_inventory(world: SC2World, item_list: List[FilterItem]) -> None:
    """Adds items to start_inventory based on first mission logic and options like `starter_unit` and `start_primary_abilities`"""
    potential_starters = world.custom_mission_order.get_starting_missions()
    starter_mission_names = [mission.mission_name for mission in potential_starters]
    starter_unit = int(world.options.starter_unit)

    # If starter_unit is off and the first mission doesn't have a no-logic location, force starter_unit on
    if starter_unit == StarterUnit.option_off:
        start_collection_state = CollectionState(world.multiworld)
        starter_mission_locations = [location.name for location in world.location_cache
                                     if location.parent_region
                                     and location.parent_region.name in starter_mission_names
                                     and location.access_rule(start_collection_state)]
        if not starter_mission_locations:
            # Force early unit if first mission is impossible without one
            starter_unit = StarterUnit.option_any_starter_unit

    if starter_unit != StarterUnit.option_off:
        flag_start_unit(world, item_list, starter_unit)
    
    flag_start_abilities(world, item_list)


def flag_start_unit(world: SC2World, item_list: List[FilterItem], starter_unit: int) -> None:
    first_mission = get_first_mission(world, world.custom_mission_order)
    first_race = first_mission.race

    if first_race == SC2Race.ANY:
        # If the first mission is a logic-less no-build
        missions = get_all_missions(world.custom_mission_order)
        build_missions = [mission for mission in missions if MissionFlag.NoBuild not in mission.flags]
        races = {mission.race for mission in build_missions if mission.race != SC2Race.ANY}
        if races:
            first_race = world.random.choice(list(races))

    if first_race != SC2Race.ANY:
        possible_starter_items = {
            item.name: item for item in item_list if (ItemFilterFlags.Plando|ItemFilterFlags.Excluded) & item.flags == 0
        }

        # The race of the early unit has been chosen
        basic_units = get_basic_units(world, first_race)
        if starter_unit == StarterUnit.option_balanced:
            basic_units = basic_units.difference(not_balanced_starting_units)
        if first_mission == SC2Mission.DARK_WHISPERS:
            # Special case - you don't have a logicless location but need an AA
            basic_units = basic_units.difference(
                {item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL, item_names.BLOOD_HUNTER,
                    item_names.AVENGER, item_names.IMMORTAL, item_names.ANNIHILATOR, item_names.VANGUARD})
        if first_mission == SC2Mission.SUDDEN_STRIKE:
            # Special case - cliffjumpers
            basic_units = {item_names.REAPER, item_names.GOLIATH, item_names.SIEGE_TANK, item_names.VIKING, item_names.BANSHEE}
        basic_unit_options = [
            item for item in possible_starter_items.values()
            if item.name in basic_units
            and ItemFilterFlags.StartInventory not in item.flags
        ]
        
        # For Sudden Strike, starter units need an upgrade to help them get around
        nco_support_items = {
            item_names.REAPER: item_names.REAPER_SPIDER_MINES,
            item_names.GOLIATH: item_names.GOLIATH_JUMP_JETS,
            item_names.SIEGE_TANK: item_names.SIEGE_TANK_JUMP_JETS,
            item_names.VIKING: item_names.VIKING_SMART_SERVOS,
        }
        if first_mission == SC2Mission.SUDDEN_STRIKE:
            basic_unit_options = [
                item for item in basic_unit_options
                if item.name not in nco_support_items
                or nco_support_items[item.name] in possible_starter_items
                and ((ItemFilterFlags.Plando|ItemFilterFlags.Excluded) & possible_starter_items[nco_support_items[item.name]].flags) == 0
            ]
        if not basic_unit_options:
            raise Exception("Early Unit: At least one basic unit must be included")
        local_basic_unit = [item for item in basic_unit_options if ItemFilterFlags.NonLocal not in item.flags]
        if local_basic_unit:
            basic_unit_options = local_basic_unit
        
        unit = world.random.choice(basic_unit_options)
        unit.flags |= ItemFilterFlags.StartInventory

        # NCO-only specific rules
        if first_mission == SC2Mission.SUDDEN_STRIKE:
            if unit.name in nco_support_items:
                support_item = possible_starter_items[nco_support_items[unit.name]]
                support_item.flags |= ItemFilterFlags.StartInventory
            if item_names.NOVA_JUMP_SUIT_MODULE in possible_starter_items:
                possible_starter_items[item_names.NOVA_JUMP_SUIT_MODULE].flags |= ItemFilterFlags.StartInventory
        if MissionFlag.Nova in first_mission.flags:
            possible_starter_weapons = (
                item_names.NOVA_HELLFIRE_SHOTGUN,
                item_names.NOVA_PLASMA_RIFLE,
                item_names.NOVA_PULSE_GRENADES,
            )
            starter_weapon_options = [item for item in possible_starter_items.values() if item.name in possible_starter_weapons]
            starter_weapon = world.random.choice(starter_weapon_options)
            starter_weapon.flags |= ItemFilterFlags.StartInventory


def flag_start_abilities(world: SC2World, item_list: List[FilterItem]) -> None:
    starter_abilities = world.options.start_primary_abilities
    if not starter_abilities:
        return
    assert starter_abilities <= 4
    ability_count = int(starter_abilities)
    ability_tiers = [0, 1, 3]
    world.random.shuffle(ability_tiers)
    if ability_count >= 4:
        # Avoid picking an ultimate unless 4 starter abilities were asked for.
        # Without this check, it would be possible to pick an ultimate if a previous tier failed
        # to pick due to exclusions
        ability_tiers.append(6)
    for tier in ability_tiers:
        abilities_in_tier = kerrigan_actives[tier].union(kerrigan_passives[tier])
        potential_starter_abilities = [
            item for item in item_list 
            if item.name in abilities_in_tier
            and (ItemFilterFlags.Excluded|ItemFilterFlags.StartInventory|ItemFilterFlags.Plando) & item.flags == 0
        ]
        # Try to avoid giving non-local items unless there is no alternative
        abilities = [item for item in potential_starter_abilities if ItemFilterFlags.NonLocal not in item.flags]
        if not abilities:
            abilities = potential_starter_abilities
        if abilities:
            ability_count -= 1
            ability = world.random.choice(abilities)
            ability.flags |= ItemFilterFlags.StartInventory
            if ability_count <= 0:
                break


def flag_unused_upgrade_types(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes +armour/attack upgrades based on generic upgrade strategy."""
    include_upgrades = world.options.generic_upgrade_missions == 0
    upgrade_items: GenericUpgradeItems = world.options.generic_upgrade_items
    for item in item_list:
        if item.data.type in items.upgrade_item_types:
            if not include_upgrades or (item.name not in upgrade_included_names[upgrade_items]):
                item.flags |= ItemFilterFlags.Excluded


def flag_user_excluded_item_sets(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes items based on item set options (`only_vanilla_items`)"""
    if not world.options.vanilla_items_only.value:
        return

    vanilla_nonprogressive_count = {
        item_name: 0 for item_name in item_groups.terran_original_progressive_upgrades
    }
    vanilla_items = item_groups.vanilla_items + item_groups.nova_equipment
    for item in item_list:
        if ItemFilterFlags.Excluded in item.flags:
            continue
        if item.name not in vanilla_items:
            item.flags |= ItemFilterFlags.Excluded
        if item.name in item_groups.terran_original_progressive_upgrades:
            if vanilla_nonprogressive_count[item.name]:
                item.flags |= ItemFilterFlags.Excluded
            vanilla_nonprogressive_count[item.name] += 1

def flag_war_council_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes / start-inventories items based on `nerf_unit_baselines` option"""
    if world.options.nerf_unit_baselines:
        return

    for item in item_list:
        if item.data.type in (ProtossItemType.War_Council, ProtossItemType.War_Council_2):
            item.flags |= ItemFilterFlags.StartInventory


def flag_and_add_resource_locations(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Filters the locations in the world using a trash or Nothing item
    :param world: The sc2 world object
    :param item_list: The current list of items to append to
    """
    open_locations = [location for location in world.location_cache if location.item is None]
    plando_locations = get_plando_locations(world)
    resource_location_types = get_location_types(world, LocationInclusion.option_resources)
    resource_location_flags = get_location_flags(world, LocationInclusion.option_resources)
    location_data = {sc2_location.name: sc2_location for sc2_location in get_locations(world)}
    for location in open_locations:
        # Go through the locations that aren't locked yet (early unit, etc)
        if location.name not in plando_locations:
            # The location is not plando'd
            sc2_location = location_data[location.name]
            if (sc2_location.type in resource_location_types
                or (sc2_location.flags & resource_location_flags)
            ):
                item_name = world.random.choice(filler_items)
                item = create_item_with_correct_settings(world.player, item_name)
                location.place_locked_item(item)
                world.locked_locations.append(location.name)


def flag_mission_order_required_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Marks items that are necessary for item rules in the mission order and forces them to be progression."""
    locks_required = world.custom_mission_order.get_items_to_lock()
    locks_done = {item: 0 for item in locks_required}
    for item in item_list:
        if item.name in locks_required and locks_done[item.name] < locks_required[item.name]:
            item.flags |= ItemFilterFlags.Necessary
            item.flags |= ItemFilterFlags.ForceProgression
            locks_done[item.name] += 1


def prune_item_pool(world: SC2World, item_list: List[FilterItem]) -> List[Item]:
    """Prunes the item pool size to be less than the number of available locations"""

    item_list = [item for item in item_list if ItemFilterFlags.Unremovable & item.flags or ItemFilterFlags.Excluded not in item.flags]
    num_items = len(item_list)
    last_num_items = -1
    while num_items != last_num_items:
        # Remove orphan items until there are no more being removed
        item_list = [item for item in item_list
            if (ItemFilterFlags.Unremovable|ItemFilterFlags.AllowedOrphan) & item.flags
            or item_list_contains_parent(item.data, item_list)]
        last_num_items = num_items
        num_items = len(item_list)

    pool: List[Item] = []
    locked_items: List[Item] = []
    existing_items: List[Item] = []
    necessary_items: List[Item] = []
    for item in item_list:
        ap_item = create_item_with_correct_settings(world.player, item.name)
        if ItemFilterFlags.ForceProgression in item.flags:
            ap_item.classification = ItemClassification.progression
        if ItemFilterFlags.StartInventory in item.flags:
            existing_items.append(ap_item)
        elif ItemFilterFlags.Necessary in item.flags:
            necessary_items.append(ap_item)
        elif ItemFilterFlags.Locked in item.flags:
            locked_items.append(ap_item)
        else:
            pool.append(ap_item)

    fill_pool_with_kerrigan_levels(world, pool)
    filtered_pool = filter_items(world, world.location_cache, pool, existing_items, locked_items, necessary_items)
    return filtered_pool


def item_list_contains_parent(item_data: ItemData, item_list: List[FilterItem]) -> bool:
    if item_data.parent_item is None:
        # The item has no associated parent, the item is valid
        return True
    parent_item = item_data.parent_item
    # Check if the pool contains the parent item
    return parent_item in [item.name for item in item_list]


def pad_item_pool_with_filler(self: SC2World, num_items: int, pool: List[Item]):
    for _ in range(num_items):
        item = create_item_with_correct_settings(self.player, self.get_filler_item_name())
        pool.append(item)


def get_first_mission(world: SC2World, mission_order: SC2MissionOrder) -> SC2Mission:
    # Pick an arbitrary lowest-difficulty starer mission
    missions = mission_order.get_starting_missions()
    missions = [(mission_order.mission_pools.get_modified_mission_difficulty(mission), mission) for mission in missions]
    missions.sort(key = lambda difficulty_mission_tuple: difficulty_mission_tuple[0])
    (lowest_difficulty, _) = missions[0]
    missions = [mission for (difficulty, mission) in missions if difficulty == lowest_difficulty]
    return world.random.choice(missions)

def get_all_missions(mission_order: SC2MissionOrder) -> List[SC2Mission]:
    return mission_order.get_used_missions()


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = items.item_table[name]

    item = Item(name, data.classification, data.code, player)

    return item


def fill_pool_with_kerrigan_levels(world: SC2World, item_pool: List[Item]):
    total_levels = world.options.kerrigan_level_item_sum.value
    missions = get_all_missions(world.custom_mission_order)
    kerrigan_missions = [mission for mission in missions if MissionFlag.Kerrigan in mission.flags]
    kerrigan_build_missions = [mission for mission in kerrigan_missions if MissionFlag.NoBuild not in mission.flags]
    if (world.options.kerrigan_presence.value not in kerrigan_unit_available
        or total_levels == 0
        or not kerrigan_missions
        or (world.options.grant_story_levels and not kerrigan_build_missions)
    ):
        return
    
    def add_kerrigan_level_items(level_amount: int, item_amount: int):
        name = f"{level_amount} Kerrigan Level"
        if level_amount > 1:
            name += "s"
        for _ in range(item_amount):
            item_pool.append(create_item_with_correct_settings(world.player, name))

    sizes = [70, 35, 14, 10, 7, 5, 2, 1]
    option = world.options.kerrigan_level_item_distribution.value

    assert isinstance(option, int)
    assert isinstance(total_levels, int)

    if option in (KerriganLevelItemDistribution.option_vanilla, KerriganLevelItemDistribution.option_smooth):
        distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if option == KerriganLevelItemDistribution.option_vanilla:
            distribution = [32, 0, 0, 1, 3, 0, 0, 0, 1, 1]
        else: # Smooth
            distribution = [0, 0, 0, 1, 1, 2, 2, 2, 1, 1]
        for tier in range(len(distribution)):
            add_kerrigan_level_items(tier + 1, distribution[tier])
    else:
        size = sizes[option - 2]
        round_func: Callable[[float], int] = round
        if total_levels > 70:
            round_func = floor
        else:
            round_func = ceil
        add_kerrigan_level_items(size, round_func(float(total_levels) / size))

def push_precollected_items_to_multiworld(world: SC2World, item_list: List[FilterItem]) -> None:
    # world.multiworld.push_precollected() has side-effects, so we can't just clear
    # world.multiworld.precollected_items[world.player]
    precollected_amounts: Dict[str, int] = {}
    for ap_item in world.multiworld.precollected_items[world.player]:
        precollected_amounts[ap_item.name] = precollected_amounts.get(ap_item.name, 0) + 1
    for item in item_list:
        if ItemFilterFlags.StartInventory not in item.flags:
            continue
        if precollected_amounts.get(item.name, 0) <= 0:
            world.multiworld.push_precollected(create_item_with_correct_settings(world.player, item.name))
        else:
            precollected_amounts[item.name] -= 1
