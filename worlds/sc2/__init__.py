from dataclasses import fields
import logging

from typing import *
from math import floor, ceil
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification, CollectionState
from Options import Accessibility, OptionError
from worlds.AutoWorld import WebWorld, World
from . import location_groups
from .item.item_groups import unreleased_items, war_council_upgrades
from .item.item_tables import (
    get_full_item_list,
    not_balanced_starting_units, WEAPON_ARMOR_UPGRADE_MAX_LEVEL,
)
from .item import FilterItem, ItemFilterFlags, StarcraftItem, item_groups, item_names, item_tables, item_parents, \
    ZergItemType, ProtossItemType, ItemData
from .locations import (
	get_locations, DEFAULT_LOCATION_LIST, get_location_types, get_location_flags,
    get_plando_locations, LocationType, lookup_location_id_to_type
)
from .mission_order.layout_types import Gauntlet
from .options import (
    get_option_value, LocationInclusion, KerriganLevelItemDistribution,
    KerriganPresence, KerriganPrimalStatus, kerrigan_unit_available, StarterUnit, SpearOfAdunPresence,
    get_enabled_campaigns, SpearOfAdunPassiveAbilityPresence, Starcraft2Options,
    GrantStoryTech, GenericUpgradeResearch, RequiredTactics,
    upgrade_included_names, EnableVoidTrade, FillerItemsDistribution, MissionOrderScouting, option_groups,
    NovaGhostOfAChanceVariant, MissionOrder, VanillaItemsOnly, ExcludeOverpoweredItems,
    is_mission_in_soa_presence,
)
from .rules import get_basic_units, SC2Logic
from . import settings
from .pool_filter import filter_items
from .mission_tables import SC2Campaign, SC2Mission, SC2Race, MissionFlag
from .regions import create_mission_order
from .mission_order import SC2MissionOrder
from worlds.LauncherComponents import components, Component, launch as launch_component
from .mission_order.presets import sc2_options_presets

logger = logging.getLogger("Starcraft 2")
VICTORY_MODULO = 100

def launch_client(*args: str):
    from .client import launch
    launch_component(launch, name="Starcraft 2 Client", args=args)

components.append(Component('Starcraft 2 Client', func=launch_client, game_name='Starcraft 2', supports_uri=True))

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
        "Documentation for the custom_mission_order YAML option",
        "English",
        "custom_mission_orders_en.md",
        "custom_mission_orders/en",
        ["Salzkorn"]
    )

    tutorials = [setup_en, setup_fr, custom_mission_orders_en]
    game_info_languages = ["en", "fr"]
    options_presets = sc2_options_presets
    option_groups = option_groups


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

    item_name_groups = item_groups.item_name_groups  # type: ignore
    location_name_groups = location_groups.get_location_groups()
    locked_locations: List[str]
    """Locations locked to contain specific items, such as victory events or forced resources"""
    location_cache: List[Location]
    final_missions: List[int]
    required_client_version = 0, 6, 4
    custom_mission_order: SC2MissionOrder
    logic: Optional['SC2Logic']
    filler_items_distribution: Dict[str, int]

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2World, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []
        self.filler_items_distribution = FillerItemsDistribution.default
        self.logic = None

    def create_item(self, name: str) -> StarcraftItem:
        data = get_full_item_list()[name]
        return StarcraftItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.logic = SC2Logic(self)
        self.custom_mission_order = create_mission_order(
            self, get_locations(self), self.location_cache
        )
        self.logic.nova_used = (
                MissionFlag.Nova in self.custom_mission_order.get_used_flags()
                or (
                        MissionFlag.WoLNova in self.custom_mission_order.get_used_flags()
                        and self.options.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_nco
                )
        )

    def create_items(self) -> None:
        # Starcraft 2-specific item setup:
        # * Filter item pool based on player options
        # * Plando starter units
        # * Start-inventory units if necessary for logic
        # * Plando filler items based on location exclusions
        # * If the item pool is less than the location count, add some filler items

        setup_events(self.player, self.locked_locations, self.location_cache)
        set_up_filler_items_distribution(self)

        item_list: List[FilterItem] = create_and_flag_explicit_item_locks_and_excludes(self)
        flag_excludes_by_faction_presence(self, item_list)
        flag_mission_based_item_excludes(self, item_list)
        flag_allowed_orphan_items(self, item_list)
        flag_start_inventory(self, item_list)
        flag_unused_upgrade_types(self, item_list)
        flag_unreleased_items(item_list)
        flag_user_excluded_item_sets(self, item_list)
        flag_war_council_items(self, item_list)
        flag_and_add_resource_locations(self, item_list)
        flag_mission_order_required_items(self, item_list)
        pruned_items: List[StarcraftItem] = prune_item_pool(self, item_list)

        start_inventory = [item for item in pruned_items if ItemFilterFlags.StartInventory in item.filter_flags]
        pool = [item for item in pruned_items if ItemFilterFlags.StartInventory not in item.filter_flags]

        # Tell the logic which unit classes are used for required W/A upgrades
        used_item_names: Set[str] = {item.name for item in pruned_items}
        used_item_names = used_item_names.union(item.name for item in self.multiworld.itempool if item.player == self.player)
        assert self.logic is not None
        if used_item_names.isdisjoint(item_groups.barracks_wa_group):
            self.logic.has_barracks_unit = False
        if used_item_names.isdisjoint(item_groups.factory_wa_group):
            self.logic.has_factory_unit = False
        if used_item_names.isdisjoint(item_groups.starport_wa_group):
            self.logic.has_starport_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_melee_wa):
            self.logic.has_zerg_melee_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_ranged_wa):
            self.logic.has_zerg_ranged_unit = False
        if used_item_names.isdisjoint(item_groups.zerg_air_units):
            self.logic.has_zerg_air_unit = False
        if used_item_names.isdisjoint(item_groups.protoss_ground_wa):
            self.logic.has_protoss_ground_unit = False
        if used_item_names.isdisjoint(item_groups.protoss_air_wa):
            self.logic.has_protoss_air_unit = False

        pad_item_pool_with_filler(self, len(self.location_cache) - len(self.locked_locations) - len(pool), pool)

        push_precollected_items_to_multiworld(self, start_inventory)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        if self.options.required_tactics == RequiredTactics.option_no_logic:
            # Forcing completed goal and minimal accessibility on no logic
            self.options.accessibility.value = Accessibility.option_minimal
            required_items = self.custom_mission_order.get_items_to_lock()
            self.multiworld.completion_condition[self.player] = lambda state, required_items=required_items: all(  # type: ignore
                state.has(item, self.player, amount) for (item, amount) in required_items.items()
            )
        else:
            self.multiworld.completion_condition[self.player] = self.custom_mission_order.get_completion_condition(self.player)

    def get_filler_item_name(self) -> str:
        # Assume `self.filler_items_distribution` is validated and has at least one non-zero entry
        return self.random.choices(tuple(self.filler_items_distribution), weights=self.filler_items_distribution.values())[0]  # type: ignore

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data: Dict[str, Any] = {}
        for option_name in [field.name for field in fields(Starcraft2Options)]:
            option = get_option_value(self, option_name)
            if type(option) in {str, int}:
                slot_data[option_name] = int(option)

        enabled_campaigns = get_enabled_campaigns(self)
        slot_data["plando_locations"] = get_plando_locations(self)
        slot_data["use_nova_nco_fallback"] = (
                enabled_campaigns == {SC2Campaign.NCO}
                and self.options.mission_order == MissionOrder.option_vanilla
        )
        if (self.options.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_nco
                or (
                        self.options.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_auto
                        and MissionFlag.Nova in self.custom_mission_order.get_used_flags().keys()
                )
        ):
            slot_data["use_nova_wol_fallback"] = False
        else:
            slot_data["use_nova_wol_fallback"] = True
        slot_data["final_mission_ids"] = self.custom_mission_order.get_final_mission_ids()
        slot_data["custom_mission_order"] = self.custom_mission_order.get_slot_data()
        slot_data["version"] = 4

        if SC2Campaign.HOTS not in enabled_campaigns:
            slot_data["kerrigan_presence"] = KerriganPresence.option_not_present

        if self.options.mission_order_scouting != MissionOrderScouting.option_none:
            mission_item_classification: Dict[str, int] = {}
            for location in self.multiworld.get_locations(self.player):
                # Event do not hold items
                if not location.is_event:
                    assert location.address is not None
                    assert location.item is not None
                    if lookup_location_id_to_type[location.address] == LocationType.VICTORY_CACHE:
                        # Ensure that if there are multiple items given for finishing a mission and that at least
                        # one is progressive, the flag kept is progressive.
                        location_name = self.location_id_to_name[(location.address // VICTORY_MODULO) * VICTORY_MODULO]
                        old_classification = mission_item_classification.get(location_name, 0)
                        mission_item_classification[location_name] = old_classification | location.item.classification.as_flag()
                    else:
                        mission_item_classification[location.name] = location.item.classification.as_flag()
            slot_data["mission_item_classification"] = mission_item_classification

        # Disable trade if there is no trade partner
        traders = [
            world
            for world in self.multiworld.worlds.values()
            if world.game == self.game and world.options.enable_void_trade == EnableVoidTrade.option_true  # type: ignore
        ]
        if len(traders) < 2:
            slot_data["enable_void_trade"] = EnableVoidTrade.option_false

        return slot_data

    def pre_fill(self) -> None:
        assert self.logic is not None
        self.logic.total_mission_count = self.custom_mission_order.get_mission_count()
        if (
                self.options.generic_upgrade_missions > 0
                and self.options.required_tactics != RequiredTactics.option_no_logic
        ):
            # Attempt to resolve a situation when the option is too high for the mission order rolled
            weapon_armor_item_names = [
                item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
                item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
                item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE
            ]
            def state_with_kerrigan_levels() -> CollectionState:
                state: CollectionState = self.multiworld.get_all_state(False)
                # Ignore dead ends caused by Kerrigan -> solve those in the next stage
                state.collect(self.create_item(item_names.KERRIGAN_LEVELS_70))
                state.update_reachable_regions(self.player)
                return state

            self._fill_needed_items(state_with_kerrigan_levels, weapon_armor_item_names, WEAPON_ARMOR_UPGRADE_MAX_LEVEL)
        if (
                self.options.kerrigan_levels_per_mission_completed > 0
                and self.options.required_tactics != RequiredTactics.option_no_logic
        ):
            # Attempt to solve being locked by Kerrigan level requirements
            self._fill_needed_items(lambda: self.multiworld.get_all_state(False), [item_names.KERRIGAN_LEVELS_1], 70)


    def _fill_needed_items(self, all_state_getter: Callable[[],CollectionState], items_to_use: List[str], max_attempts: int) -> None:
        """
        Helper for pre-fill, seeks if the world is actually solvable and inserts items to start inventory if necessary.
        :param all_state_getter:
        :param items_to_use:
        :param max_attempts:
        :return:
        """
        for attempt in range(0, max_attempts):
            all_state: CollectionState = all_state_getter()
            location_failed = False
            for location in self.location_cache:
                if not (all_state.can_reach_location(location.name, self.player)
                        and all_state.can_reach_region(location.parent_region.name, self.player)):
                    location_failed = True
                    break
            if location_failed:
                for item_name in items_to_use:
                    item = self.multiworld.create_item(item_name, self.player)
                    self.multiworld.push_precollected(item)
            else:
                return


    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        """
        Generate information to hint where each mission is actually located in the mission order
        :param hint_data:
        """
        hint_data[self.player] = {}
        for campaign in self.custom_mission_order.mission_order_node.campaigns:
            for layout in campaign.layouts:
                columns = layout.layout_type.get_visual_layout()
                is_single_row_layout = max([len(column) for column in columns]) == 1
                for column_index, column in enumerate(columns):
                    for row_index, layout_mission in enumerate(column):
                        slot = layout.missions[layout_mission]
                        if hasattr(slot, "mission") and slot.mission is not None:
                            mission = slot.mission
                            campaign_name = campaign.get_visual_name()
                            layout_name = layout.get_visual_name()
                            if isinstance(layout.layout_type, Gauntlet):
                                # Linearize Gauntlet
                                column_name = str(
                                    layout_mission + 1
                                    if layout_mission >= 0
                                    else layout.layout_type.size + layout_mission + 1
                                )
                                row_name = ""
                            else:
                                column_name = "" if len(columns) == 1 else _get_column_display(column_index, is_single_row_layout)
                                row_name = "" if is_single_row_layout else str(1 + row_index)
                            mission_position_name: str = campaign_name + " " + layout_name + " " + column_name + row_name
                            mission_position_name = mission_position_name.strip().replace("  ", " ")
                            if mission_position_name != "":
                                for location in self.get_region(mission.mission_name).get_locations():
                                    if location.address is not None:
                                        hint_data[self.player][location.address] = mission_position_name


def _get_column_display(index: int, single_row_layout: bool) -> str:
    """
    Helper function to display column name
    :param index:
    :param single_row_layout:
    :return:
    """
    if single_row_layout:
        return str(index + 1)
    else:
        # Convert column name to a letter, from Z continue with AA and so on
        f: Callable[[int], str] = lambda x: "" if x == 0 else f((x - 1) // 26) + chr((x - 1) % 26 + ord("A"))
        return f(index + 1)


def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]) -> None:
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
    
    auto_excludes = {item_name: 1 for item_name in item_groups.legacy_items}
    if world.options.exclude_overpowered_items.value == ExcludeOverpoweredItems.option_true:
        for item_name in item_groups.overpowered_items:
            auto_excludes[item_name] = 1

    result: List[FilterItem] = []
    for item_name, item_data in item_tables.item_table.items():
        max_count = item_data.quantity
        auto_excluded_count = auto_excludes.get(item_name)
        excluded_count = excluded_items.get(item_name, auto_excluded_count)
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
        final_count = max(max_count, key_count)
        for index in range(final_count):
            result.append(FilterItem(item_name, item_data, index))
            if index < start_count:
                result[-1].flags |= ItemFilterFlags.StartInventory
            if index < locked_count + start_count:
                result[-1].flags |= ItemFilterFlags.Locked
            if item_name in world.options.non_local_items:
                result[-1].flags |= ItemFilterFlags.NonLocal
            if index >= max(max_count - excluded_count, key_count):
                result[-1].flags |= ItemFilterFlags.UserExcluded
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
        # Unit upgrades required for no-builds will get the FilterExcluded lifted when flagging AllowedOrphan
        if not terran_build_missions and item.data.race == SC2Race.TERRAN:
            if item.name not in item_groups.nova_equipment:
                item.flags |= ItemFilterFlags.FilterExcluded
                continue
        if not zerg_missions and item.data.race == SC2Race.ZERG:
            if item.data.type != item_tables.ZergItemType.Ability \
                    and item.data.type != ZergItemType.Level:
                item.flags |= ItemFilterFlags.FilterExcluded
                continue
        if not protoss_missions and item.data.race == SC2Race.PROTOSS:
            if item.name not in item_groups.soa_items:
                item.flags |= ItemFilterFlags.FilterExcluded
            continue

        # Faction units
        if (not zerg_build_missions
            and item.data.type in (item_tables.ZergItemType.Unit, item_tables.ZergItemType.Mercenary, item_tables.ZergItemType.Evolution_Pit)
        ):
            if (SC2Mission.ENEMY_WITHIN not in missions
                or world.options.grant_story_tech.value == GrantStoryTech.option_grant
                or item.name not in (item_names.ZERGLING, item_names.ROACH, item_names.HYDRALISK, item_names.INFESTOR)
            ):
                item.flags |= ItemFilterFlags.FilterExcluded
        if (not protoss_build_missions
            and item.data.type in (
                        item_tables.ProtossItemType.Unit,
                        item_tables.ProtossItemType.Unit_2,
                        item_tables.ProtossItemType.Building,
            )
        ):
            # Note(mm): This doesn't exclude things like automated assimilators or warp gate improvements
            # because that item type is mixed in with e.g. Reconstruction Beam and Overwatch
            if (SC2Mission.TEMPLAR_S_RETURN not in missions
                or world.options.grant_story_tech.value == GrantStoryTech.option_grant
                or item.name not in (
                            item_names.IMMORTAL, item_names.ANNIHILATOR,
                            item_names.COLOSSUS, item_names.VANGUARD, item_names.REAVER, item_names.DARK_TEMPLAR,
                            item_names.SENTRY, item_names.HIGH_TEMPLAR,
                )
            ):
                item.flags |= ItemFilterFlags.FilterExcluded

        # Faction +attack/armour upgrades
        if (item.data.type == item_tables.TerranItemType.Upgrade
            and not terran_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.FilterExcluded
        if (item.data.type == item_tables.ZergItemType.Upgrade
            and not zerg_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.FilterExcluded
        if (item.data.type == item_tables.ProtossItemType.Upgrade
            and not protoss_build_missions
            and not auto_upgrades_in_nobuilds
        ):
            item.flags |= ItemFilterFlags.FilterExcluded


def flag_mission_based_item_excludes(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Excludes items based on mission / campaign presence: Nova Gear, Kerrigan abilities, SOA
    """
    missions = get_all_missions(world.custom_mission_order)

    kerrigan_missions = [mission for mission in missions if MissionFlag.Kerrigan in mission.flags]
    kerrigan_build_missions = [mission for mission in kerrigan_missions if MissionFlag.NoBuild not in mission.flags]
    nova_missions = [
        mission for mission in missions
        if MissionFlag.Nova in mission.flags
           or (
                   world.options.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_nco
                   and MissionFlag.WoLNova in mission.flags
           )
    ]

    kerrigan_is_present = (
            len(kerrigan_missions) > 0
            and world.options.kerrigan_presence in kerrigan_unit_available
            and SC2Campaign.HOTS in get_enabled_campaigns(world) # TODO: Kerrigan available all Zerg/Everywhere
    )

    # TvX build missions -- check flags
    if world.options.take_over_ai_allies:
        terran_build_missions = [mission for mission in missions if (
            (MissionFlag.Terran in mission.flags or MissionFlag.AiTerranAlly in mission.flags)
            and MissionFlag.NoBuild not in mission.flags
        )]
    else:
        terran_build_missions = [mission for mission in missions if (
            MissionFlag.Terran in mission.flags
            and MissionFlag.NoBuild not in mission.flags
        )]
    tvz_build_missions = [mission for mission in terran_build_missions if MissionFlag.VsZerg in mission.flags]
    tvp_build_missions = [mission for mission in terran_build_missions if MissionFlag.VsProtoss in mission.flags]
    tvt_build_missions = [mission for mission in terran_build_missions if MissionFlag.VsTerran in mission.flags]

    # Check if SOA actives should be present
    if world.options.spear_of_adun_presence != SpearOfAdunPresence.option_not_present:
        soa_missions = missions
        soa_missions = [
            m for m in soa_missions
            if is_mission_in_soa_presence(world.options.spear_of_adun_presence.value, m)
        ]
        if not world.options.spear_of_adun_present_in_no_build:
            soa_missions = [m for m in soa_missions if MissionFlag.NoBuild not in m.flags]
        soa_presence = len(soa_missions) > 0
    else:
        soa_presence = False

    # Check if SOA passives should be present
    if world.options.spear_of_adun_passive_ability_presence != SpearOfAdunPassiveAbilityPresence.option_not_present:
        soa_missions = missions
        soa_missions = [
            m for m in soa_missions
            if is_mission_in_soa_presence(
                world.options.spear_of_adun_passive_ability_presence.value,
                m,
                SpearOfAdunPassiveAbilityPresence
            )
        ]
        if not world.options.spear_of_adun_passive_present_in_no_build:
            soa_missions = [m for m in soa_missions if MissionFlag.NoBuild not in m.flags]
        soa_passive_presence = len(soa_missions) > 0
    else:
        soa_passive_presence = False

    remove_kerrigan_abils = (
        # TODO: Kerrigan presence Zerg/Everywhere
        not kerrigan_is_present
        or (world.options.grant_story_tech.value == GrantStoryTech.option_grant and not kerrigan_build_missions)
        or (
            world.options.grant_story_tech.value == GrantStoryTech.option_allow_substitutes
            and len(kerrigan_missions) == 1
            and kerrigan_missions[0] == SC2Mission.SUPREME
        )
    )

    for item in item_list:
        # Filter Nova equipment if you never get Nova
        if not nova_missions and (item.name in item_groups.nova_equipment):
            item.flags |= ItemFilterFlags.FilterExcluded

        # Todo(mm): How should no-build only / grant_story_tech affect excluding Kerrigan items?
        # Exclude Primal form based on Kerrigan presence or primal form option
        if (item.data.type == item_tables.ZergItemType.Primal_Form
            and ((not kerrigan_is_present) or world.options.kerrigan_primal_status != KerriganPrimalStatus.option_item)
        ):
            item.flags |= ItemFilterFlags.FilterExcluded

        # Remove Kerrigan abilities if there's no kerrigan
        if item.data.type == item_tables.ZergItemType.Ability and remove_kerrigan_abils:
            item.flags |= ItemFilterFlags.FilterExcluded

        # Remove Spear of Adun if it's off
        if item.name in item_tables.spear_of_adun_calldowns and not soa_presence:
            item.flags |= ItemFilterFlags.FilterExcluded

        # Remove Spear of Adun passives
        if item.name in item_tables.spear_of_adun_castable_passives and not soa_passive_presence:
            item.flags |= ItemFilterFlags.FilterExcluded

        # Remove matchup-specific items if you don't play that matchup
        if (item.name in (item_names.HIVE_MIND_EMULATOR, item_names.PSI_DISRUPTER)
            and not tvz_build_missions
        ):
            item.flags |= ItemFilterFlags.FilterExcluded
        if (item.name in (item_names.PSI_INDOCTRINATOR, item_names.SONIC_DISRUPTER)
            and not tvt_build_missions
        ):
            item.flags |= ItemFilterFlags.FilterExcluded
        if (item.name in (item_names.PSI_SCREEN, item_names.ARGUS_AMPLIFIER)
            and not tvp_build_missions
        ):
            item.flags |= ItemFilterFlags.FilterExcluded
    return


def flag_allowed_orphan_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Adds the `Allowed_Orphan` flag to items that shouldn't be filtered with their parents, like combat shield"""
    missions = get_all_missions(world.custom_mission_order)
    if SC2Mission.PIERCING_OF_THE_SHROUD in missions:
        for item in item_list:
            if item.name in (
                    item_names.MARINE_COMBAT_SHIELD, item_names.MARINE_PROGRESSIVE_STIMPACK, item_names.MARINE_MAGRAIL_MUNITIONS,
                    item_names.MEDIC_STABILIZER_MEDPACKS, item_names.MARINE_LASER_TARGETING_SYSTEM,
            ):
                item.flags |= ItemFilterFlags.AllowedOrphan
                item.flags &= ~ItemFilterFlags.FilterExcluded
    # These rules only trigger on Standard tactics
    if SC2Mission.BELLY_OF_THE_BEAST in missions and world.options.required_tactics == RequiredTactics.option_standard:
        for item in item_list:
            if item.name in (
                    item_names.MARINE_COMBAT_SHIELD, item_names.MARINE_PROGRESSIVE_STIMPACK, item_names.MARINE_MAGRAIL_MUNITIONS,
                    item_names.MEDIC_STABILIZER_MEDPACKS, item_names.MARINE_LASER_TARGETING_SYSTEM,
                    item_names.FIREBAT_NANO_PROJECTORS, item_names.FIREBAT_JUGGERNAUT_PLATING, item_names.FIREBAT_PROGRESSIVE_STIMPACK
            ):
                item.flags |= ItemFilterFlags.AllowedOrphan
                item.flags &= ~ItemFilterFlags.FilterExcluded
    if SC2Mission.EVIL_AWOKEN in missions and world.options.required_tactics == RequiredTactics.option_standard:
        for item in item_list:
            if item.name in (item_names.STALKER_PHASE_REACTOR, item_names.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES, item_names.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION):
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
    first_mission = get_random_first_mission(world, world.custom_mission_order)
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
            item.name: item for item in item_list if (ItemFilterFlags.Plando|ItemFilterFlags.UserExcluded|ItemFilterFlags.FilterExcluded) & item.flags == 0
        }

        # The race of the early unit has been chosen
        basic_units = get_basic_units(world.options.required_tactics.value, first_race)
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
                and ((ItemFilterFlags.Plando|ItemFilterFlags.UserExcluded|ItemFilterFlags.FilterExcluded) & possible_starter_items[nco_support_items[item.name]].flags) == 0
            ]
        if not basic_unit_options:
            raise OptionError("Early Unit: At least one basic unit must be included")
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
    available_abilities = item_groups.kerrigan_non_ulimates
    for i in range(ability_count):
        potential_starter_abilities = [
            item for item in item_list
            if item.name in available_abilities
            and (ItemFilterFlags.UserExcluded|ItemFilterFlags.StartInventory|ItemFilterFlags.Plando) & item.flags == 0
        ]
        if len(potential_starter_abilities) == 0 or i >= 3:
            # Avoid picking an ultimate unless 4 starter abilities were asked for.
            # Without this check, it would be possible to pick an ultimate if a previous tier failed
            # to pick due to exclusions
            available_abilities = item_groups.kerrigan_abilities
            potential_starter_abilities = [
                item for item in item_list
                if item.name in available_abilities
                   and (ItemFilterFlags.UserExcluded|ItemFilterFlags.StartInventory|ItemFilterFlags.Plando) & item.flags == 0
            ]
        # Try to avoid giving non-local items unless there is no alternative
        abilities = [item for item in potential_starter_abilities if ItemFilterFlags.NonLocal not in item.flags]
        if not abilities:
            abilities = potential_starter_abilities
        if abilities:
            ability = world.random.choice(abilities)
            ability.flags |= ItemFilterFlags.StartInventory


def flag_unused_upgrade_types(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes +armour/attack upgrades based on generic upgrade strategy.
    Caps upgrade items based on `max_upgrade_level`."""
    include_upgrades = world.options.generic_upgrade_missions == 0
    upgrade_items = world.options.generic_upgrade_items.value
    upgrade_included_counts: Dict[str, int] = {}
    for item in item_list:
        if item.data.type in item_tables.upgrade_item_types:
            if not include_upgrades or (item.name not in upgrade_included_names[upgrade_items]):
                item.flags |= ItemFilterFlags.Removed
            else:
                included = upgrade_included_counts.get(item.name, 0)
                if (
                    included >= world.options.max_upgrade_level
                    and not (ItemFilterFlags.Locked|ItemFilterFlags.StartInventory) & item.flags
                ):
                    item.flags |= ItemFilterFlags.FilterExcluded
                elif ItemFilterFlags.UserExcluded not in item.flags:
                    upgrade_included_counts[item.name] = included + 1

def flag_unreleased_items(item_list: List[FilterItem]) -> None:
    """Remove all unreleased items unless they're explicitly locked"""
    for item in item_list:
        if (item.name in unreleased_items
                and not (ItemFilterFlags.Locked|ItemFilterFlags.StartInventory) & item.flags):
            item.flags |= ItemFilterFlags.Removed


def flag_user_excluded_item_sets(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes items based on item set options (`only_vanilla_items`)"""
    vanilla_nonprogressive_count = {
        item_name: 0 for item_name in item_groups.terran_original_progressive_upgrades
    }
    if world.options.vanilla_items_only.value == VanillaItemsOnly.option_true:
        vanilla_items = item_groups.vanilla_items + item_groups.nova_equipment
        for item in item_list:
            if ItemFilterFlags.UserExcluded in item.flags:
                continue
            if item.name not in vanilla_items:
                item.flags |= ItemFilterFlags.UserExcluded
            if item.name in item_groups.terran_original_progressive_upgrades:
                if vanilla_nonprogressive_count[item.name]:
                    item.flags |= ItemFilterFlags.UserExcluded
                vanilla_nonprogressive_count[item.name] += 1

    excluded_count: Dict[str, int] = dict()


def flag_war_council_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes / start-inventories items based on `nerf_unit_baselines` option.
    Will skip items that are excluded by other sources."""
    if world.options.war_council_nerfs:
        return

    flagged_item_names = []
    for item in item_list:
        if (
            item.name in war_council_upgrades
            and not ItemFilterFlags.Excluded & item.flags
            and item.name not in flagged_item_names
        ):
            flagged_item_names.append(item.name)
            item.flags |= ItemFilterFlags.StartInventory


def flag_and_add_resource_locations(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Filters the locations in the world using a trash or Nothing item
    :param world: The sc2 world object
    :param item_list: The current list of items to append to
    """
    open_locations = [location for location in world.location_cache if location.item is None]
    plando_locations = get_plando_locations(world)
    filler_location_types = get_location_types(world, LocationInclusion.option_filler)
    filler_location_flags = get_location_flags(world, LocationInclusion.option_filler)
    location_data = {sc2_location.name: sc2_location for sc2_location in DEFAULT_LOCATION_LIST}
    for location in open_locations:
        # Go through the locations that aren't locked yet (early unit, etc)
        if location.name not in plando_locations:
            # The location is not plando'd
            sc2_location = location_data[location.name]
            if (sc2_location.type in filler_location_types
                or (sc2_location.flags & filler_location_flags)
            ):
                item_name = world.get_filler_item_name()
                item = create_item_with_correct_settings(world.player, item_name)
                if item.classification & ItemClassification.progression:
                    # Scouting shall show Filler (or a trap)
                    item.classification = ItemClassification.filler
                location.place_locked_item(item)
                world.locked_locations.append(location.name)


def flag_mission_order_required_items(world: SC2World, item_list: List[FilterItem]) -> None:
    """Marks items that are necessary for item rules in the mission order and forces them to be progression."""
    locks_required = world.custom_mission_order.get_items_to_lock()
    locks_done = {item: 0 for item in locks_required}
    for item in item_list:
        if item.name in locks_required and locks_done[item.name] < locks_required[item.name]:
            item.flags |= ItemFilterFlags.Locked
            item.flags |= ItemFilterFlags.ForceProgression
            locks_done[item.name] += 1


def prune_item_pool(world: SC2World, item_list: List[FilterItem]) -> List[StarcraftItem]:
    """Prunes the item pool size to be less than the number of available locations"""

    item_list = [
        item for item in item_list
        if (ItemFilterFlags.Removed not in item.flags)
        and (ItemFilterFlags.Unexcludable & item.flags or ItemFilterFlags.FilterExcluded not in item.flags)
    ]
    num_items = len(item_list)
    last_num_items = -1
    while num_items != last_num_items:
        # Remove orphan items until there are no more being removed
        item_name_list = [item.name for item in item_list]
        item_list = [item for item in item_list
            if (ItemFilterFlags.Unexcludable|ItemFilterFlags.AllowedOrphan) & item.flags
            or item_list_contains_parent(world, item.data, item_name_list)]
        last_num_items = num_items
        num_items = len(item_list)

    pool: List[StarcraftItem] = []
    for item in item_list:
        ap_item = create_item_with_correct_settings(world.player, item.name, item.flags)
        if ItemFilterFlags.ForceProgression in item.flags:
            ap_item.classification = ItemClassification.progression
        pool.append(ap_item)

    fill_pool_with_kerrigan_levels(world, pool)
    filtered_pool = filter_items(world, world.location_cache, pool)
    return filtered_pool


def item_list_contains_parent(world: SC2World, item_data: ItemData, item_name_list: List[str]) -> bool:
    if item_data.parent is None:
        # The item has no associated parent, the item is valid
        return True
    return item_parents.parent_present[item_data.parent](item_name_list, world.options)


def pad_item_pool_with_filler(world: SC2World, num_items: int, pool: List[StarcraftItem]):
    for _ in range(num_items):
        item = create_item_with_correct_settings(world.player, world.get_filler_item_name())
        pool.append(item)


def set_up_filler_items_distribution(world: SC2World) -> None:
    world.filler_items_distribution = world.options.filler_items_distribution.value.copy()

    prune_fillers(world)
    if sum(world.filler_items_distribution.values()) == 0:
        world.filler_items_distribution = FillerItemsDistribution.default.copy()
    prune_fillers(world)


def prune_fillers(world):
    mission_flags = world.custom_mission_order.get_used_flags()
    include_protoss = (
            MissionFlag.Protoss in mission_flags
            or (world.options.take_over_ai_allies and (MissionFlag.AiProtossAlly in mission_flags))
    )
    include_kerrigan = (
            MissionFlag.Kerrigan in mission_flags
            and world.options.kerrigan_presence in kerrigan_unit_available
    )
    generic_upgrade_research = world.options.generic_upgrade_research
    if not include_protoss:
        world.filler_items_distribution.pop(item_names.SHIELD_REGENERATION, 0)
    if not include_kerrigan:
        world.filler_items_distribution.pop(item_names.KERRIGAN_LEVELS_1, 0)
    if (generic_upgrade_research in
            [
                GenericUpgradeResearch.option_always_auto,
                GenericUpgradeResearch.option_auto_in_build
            ]
    ):
        world.filler_items_distribution.pop(item_names.UPGRADE_RESEARCH_SPEED, 0)
        world.filler_items_distribution.pop(item_names.UPGRADE_RESEARCH_COST, 0)


def get_random_first_mission(world: SC2World, mission_order: SC2MissionOrder) -> SC2Mission:
    # Pick an arbitrary lowest-difficulty starer mission
    starting_missions = mission_order.get_starting_missions()
    mission_difficulties = [
        (mission_order.mission_pools.get_modified_mission_difficulty(mission), mission)
        for mission in starting_missions
    ]
    mission_difficulties.sort(key = lambda difficulty_mission_tuple: difficulty_mission_tuple[0])
    (lowest_difficulty, _) = mission_difficulties[0]
    first_mission_candidates = [mission for (difficulty, mission) in mission_difficulties if difficulty == lowest_difficulty]
    return world.random.choice(first_mission_candidates)


def get_all_missions(mission_order: SC2MissionOrder) -> List[SC2Mission]:
    return mission_order.get_used_missions()


def create_item_with_correct_settings(player: int, name: str, filter_flags: ItemFilterFlags = ItemFilterFlags.Available) -> StarcraftItem:
    data = item_tables.item_table[name]

    item = StarcraftItem(name, data.classification, data.code, player, filter_flags)
    if ItemFilterFlags.ForceProgression & filter_flags:
        item.classification = ItemClassification.progression

    return item


def fill_pool_with_kerrigan_levels(world: SC2World, item_pool: List[StarcraftItem]):
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


def push_precollected_items_to_multiworld(world: SC2World, item_list: List[StarcraftItem]) -> None:
    # Clear the pre-collected items, as AP will try to do this for us,
    # and we want to be able to filer out precollected items in the case of upgrade packages.
    auto_precollected_items = world.multiworld.precollected_items[world.player].copy()
    world.multiworld.precollected_items[world.player].clear()
    for item in auto_precollected_items:
        world.multiworld.state.remove(item)

    for item in item_list:
        if ItemFilterFlags.StartInventory not in item.filter_flags:
            continue
        world.multiworld.push_precollected(create_item_with_correct_settings(world.player, item.name, item.filter_flags))
