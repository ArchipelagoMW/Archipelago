from dataclasses import fields
import enum
import logging

from typing import *
from math import floor, ceil
from dataclasses import dataclass
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import WebWorld, World
from . import ItemNames
from .Items import StarcraftItem, filler_items, get_full_item_list, \
    get_basic_units, ItemData, upgrade_included_names, progressive_if_nco, kerrigan_actives, kerrigan_passives, \
    kerrigan_only_passives, progressive_if_ext, not_balanced_starting_units, spear_of_adun_calldowns, \
    spear_of_adun_castable_passives, nova_equipment
from . import Items
from .ItemGroups import item_name_groups
from .Locations import get_locations, get_location_types, get_plando_locations
from .Regions import create_regions
from .Options import (get_option_value, LocationInclusion, KerriganLevelItemDistribution,
    KerriganPresence, KerriganPrimalStatus, RequiredTactics, kerrigan_unit_available, StarterUnit, SpearOfAdunPresence,
    get_enabled_campaigns, SpearOfAdunAutonomouslyCastAbilityPresence, Starcraft2Options, SpearOfAdunPresentInNoBuild
)
from .PoolFilter import filter_items, get_item_upgrades, get_used_races
from .MissionTables import (
    MissionInfo, SC2Campaign, lookup_name_to_mission, SC2Mission, SC2Race, MissionFlag
)

logger = logging.getLogger("Starcraft 2")


class ItemFilterFlags(enum.IntFlag):
    Available = 0
    Locked = enum.auto()
    StartInventory = enum.auto()
    NonLocal = enum.auto()
    Removed = enum.auto()
    Plando = enum.auto()
    Excluded = enum.auto()

    Unremovable = Locked|StartInventory|Plando


@dataclass
class FilterItem:
    name: str
    data: ItemData
    index: int = 0
    flags: ItemFilterFlags = ItemFilterFlags.Available


class Starcraft2WebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor", "Phaneros"]
    )

    tutorials = [setup]


class SC2World(World):
    """
    StarCraft II is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Play as one of three factions across four campaigns in a battle for supremacy of the Koprulu Sector.
    """

    game = "Starcraft 2"
    web = Starcraft2WebWorld()

    item_name_to_id = {name: data.code for name, data in get_full_item_list().items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None)}
    options_dataclass = Starcraft2Options
    options: Starcraft2Options

    item_name_groups = item_name_groups
    locked_locations: List[str]
    """Locations locked to contain specific items, such as victory events or forced resources"""
    location_cache: List[Location]
    mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]] = {}
    final_mission_id: int
    victory_item: str
    required_client_version = 0, 4, 5

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2World, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.mission_req_table, self.final_mission_id, self.victory_item = create_regions(
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
        flag_mission_based_item_excludes(self, item_list)
        flag_start_inventory(self, item_list)
        flag_unused_upgrade_types(self, item_list)
        flag_excluded_item_sets(self, item_list)
        flag_and_add_resource_locations(self, item_list)
        pool: List[Item] = prune_item_pool(self, item_list)
        pad_item_pool_with_filler(self, len(self.location_cache) - len(self.locked_locations) - len(pool), pool)

        # old
        # excluded_items = get_excluded_items(self)

        # starter_items = assign_starter_items(self, excluded_items, self.locked_locations, self.location_cache)

        # fill_resource_locations(self, self.locked_locations, self.location_cache)

        # pool = get_item_pool(self, self.mission_req_table, starter_items, excluded_items, self.location_cache)

        # fill_item_pool_with_dummy_items(self, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.victory_item, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in [field.name for field in fields(Starcraft2Options)]:
            option = get_option_value(self, option_name)
            if type(option) in {str, int}:
                slot_data[option_name] = int(option)
        slot_req_table = {}

        # Serialize data
        for campaign in self.mission_req_table:
            slot_req_table[campaign.id] = {}
            for mission in self.mission_req_table[campaign]:
                slot_req_table[campaign.id][mission] = self.mission_req_table[campaign][mission]._asdict()
                # Replace mission objects with mission IDs
                slot_req_table[campaign.id][mission]["mission"] = slot_req_table[campaign.id][mission]["mission"].id

                for index in range(len(slot_req_table[campaign.id][mission]["required_world"])):
                    # TODO this is a band-aid, sometimes the mission_req_table already contains dicts
                    # as far as I can tell it's related to having multiple vanilla mission orders
                    if not isinstance(slot_req_table[campaign.id][mission]["required_world"][index], dict):
                        slot_req_table[campaign.id][mission]["required_world"][index] = slot_req_table[campaign.id][mission]["required_world"][index]._asdict()

        enabled_campaigns = get_enabled_campaigns(self)
        slot_data["plando_locations"] = get_plando_locations(self)
        slot_data["nova_covert_ops_only"] = (enabled_campaigns == {SC2Campaign.NCO})
        slot_data["mission_req"] = slot_req_table
        slot_data["final_mission"] = self.final_mission_id
        slot_data["version"] = 3

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
    locked_items = world.options.locked_items
    start_inventory = world.options.start_inventory
    result: List[FilterItem] = []
    for item_name, item_data in Items.item_table.items():
        if not item_data.quantity:
            continue
        max_count = item_data.quantity
        excluded_count = excluded_items.get(item_name)
        locked_count = locked_items.get(item_name)
        start_count: Optional[int] = start_inventory.get(item_name)
        # specifying 0 in the yaml means exclude / lock all
        # start_inventory doesn't allow specifying 0
        # not specifying means don't exclude/lock/start
        if excluded_count == 0:
            excluded_count = max_count
        elif excluded_count is None:
            excluded_count = 0
        if locked_count == 0:
            locked_count = max_count
        elif locked_count is None:
            locked_count = 0
        if start_count is None:
            start_count = 0

        # Priority: start_inventory >> locked_items >> excluded_items >> unspecified
        if start_count > max_count:
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
        for index in range(max_count - excluded_count):
            result.append(FilterItem(item_name, item_data, index))
            if index < start_count:
                result[-1].flags |= ItemFilterFlags.StartInventory
            if index < locked_count + start_count:
                result[-1].flags |= ItemFilterFlags.Locked
            if item_name in world.options.non_local_items:
                result[-1].flags |= ItemFilterFlags.NonLocal
    return result


def flag_mission_based_item_excludes(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Excludes items based on mission / campaign presence. e.g. Nova Gear is excluded if there are no Nova missions.
    """
    missions: List[SC2Mission] = []
    for campaign in world.mission_req_table.values():
        missions.extend(mission_info.mission for _, mission_info in campaign.items())

    kerrigan_missions = len([mission for mission in missions if MissionFlag.Kerrigan in mission.flags]) > 0
    nova_missions = [mission for mission in missions if MissionFlag.Nova in mission.flags]

    kerrigan_is_present = kerrigan_missions and world.options.kerrigan_presence == KerriganPresence.option_vanilla

    # TvZ build missions -- check flags Terran and VsZerg are true and NoBuild is false
    tvz_build_mask = MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.NoBuild
    tvz_expect_value = MissionFlag.Terran|MissionFlag.VsZerg
    if world.options.take_over_ai_allies:
        tvz_build_mask |= MissionFlag.AiTerranAlly
        tvz_expect_value |= MissionFlag.AiTerranAlly
    tvz_build_missions = [mission for mission in missions if tvz_build_mask & mission.flags == tvz_expect_value]

    # Check if SOA actives should be present
    if world.options.spear_of_adun_presence == SpearOfAdunPresence.option_not_present:
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
    if world.options.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present:
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
        if not nova_missions and item.data.type == Items.ItemType.Nova_Gear:
            item.flags |= ItemFilterFlags.Excluded
        
        # Todo(mm): How should no-build only / grant_story_tech affect excluding Kerrigan items?
        # Exclude Primal form based on Kerrigan presence or primal form option
        if (item.data.type == Items.ItemType.Primal_Form
            and ((not kerrigan_is_present) or world.options.kerrigan_primal_status != KerriganPrimalStatus.option_item)
        ):
            item.flags |= ItemFilterFlags.Excluded
        
        # Remove Kerrigan abilities if there's no kerrigan
        if (item.data.type == Items.ItemType.Ability and not kerrigan_is_present):
            item.flags |= ItemFilterFlags.Excluded
        
        # Remove Spear of Adun if it's off
        if item.name in Items.spear_of_adun_calldowns and not soa_presence:
            item.flags |= ItemFilterFlags.Excluded

        # Remove Spear of Adun passives
        if item.name in Items.spear_of_adun_castable_passives and not soa_passive_presence:
            item.flags |= ItemFilterFlags.Excluded
        
        # Remove Psi Disrupter and Hive Mind Emulator if you never play a build TvZ
        if (item.name in (ItemNames.HIVE_MIND_EMULATOR, ItemNames.PSI_DISRUPTER)
            and not tvz_build_missions
        ):
            item.flags |= ItemFilterFlags.Excluded
    return


def flag_start_inventory(world: SC2World, item_list: List[FilterItem]) -> None:
    """Adds items to start_inventory based on first mission logic and options like `starter_unit` and `start_primary_abilities`"""
    first_mission_name = get_first_mission(world.mission_req_table).mission_name
    starter_unit = int(world.options.starter_unit)

    # If starter_unit is off and the first mission doesn't have a no-logic location, force starter_unit on
    if starter_unit == StarterUnit.option_off:
        start_collection_state = CollectionState(world.multiworld)
        starter_mission_locations = [location.name for location in world.location_cache
                                     if location.parent_region
                                     and location.parent_region.name == first_mission_name
                                     and location.access_rule(start_collection_state)]
        if not starter_mission_locations:
            # Force early unit if first mission is impossible without one
            starter_unit = StarterUnit.option_any_starter_unit

    if starter_unit != StarterUnit.option_off:
        resolve_start_unit(world, item_list, starter_unit)
    
    resolve_start_abilities(world, item_list)


def resolve_start_unit(world: SC2World, item_list: List[FilterItem], starter_unit: int) -> None:
    first_mission = get_first_mission(world.mission_req_table)
    first_race = first_mission.race

    if first_race == SC2Race.ANY:
        # If the first mission is a logic-less no-build
        races = get_used_races(world.mission_req_table, world)
        races.remove(SC2Race.ANY)
        if first_mission.race in races:
            # The campaign's race is in (At least one mission that's not logic-less no-build exists)
            first_race = first_mission.campaign.race
        elif len(races) > 0:
            # The campaign only has logic-less no-build missions. Find any other valid race
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
                {ItemNames.ZEALOT, ItemNames.CENTURION, ItemNames.SENTINEL, ItemNames.BLOOD_HUNTER,
                    ItemNames.AVENGER, ItemNames.IMMORTAL, ItemNames.ANNIHILATOR, ItemNames.VANGUARD})
        if first_mission == SC2Mission.SUDDEN_STRIKE:
            # Special case - cliffjumpers
            basic_units = {ItemNames.REAPER, ItemNames.GOLIATH, ItemNames.SIEGE_TANK, ItemNames.VIKING, ItemNames.BANSHEE}
        basic_unit_options = [
            item for item in possible_starter_items.values()
            if item.name in basic_units
            and ItemFilterFlags.StartInventory not in item.flags
        ]
        
        # For Sudden Strike, starter units need an upgrade to help them get around
        nco_support_items = {
            ItemNames.REAPER: ItemNames.REAPER_SPIDER_MINES,
            ItemNames.GOLIATH: ItemNames.GOLIATH_JUMP_JETS,
            ItemNames.SIEGE_TANK: ItemNames.SIEGE_TANK_JUMP_JETS,
            ItemNames.VIKING: ItemNames.VIKING_SMART_SERVOS,
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
            if ItemNames.NOVA_JUMP_SUIT_MODULE in possible_starter_items:
                possible_starter_items[ItemNames.NOVA_JUMP_SUIT_MODULE].flags |= ItemFilterFlags.StartInventory
        if MissionFlag.Nova in first_mission.flags:
            possible_starter_weapons = (
                ItemNames.NOVA_HELLFIRE_SHOTGUN,
                ItemNames.NOVA_PLASMA_RIFLE,
                ItemNames.NOVA_PULSE_GRENADES,
            )
            starter_weapon_options = [item for item in possible_starter_items.values() if item.name in possible_starter_weapons]
            starter_weapon = world.random.choice(starter_weapon_options)
            starter_weapon.flags |= ItemFilterFlags.StartInventory
        mission_count = sum(len(campaign) for campaign in world.mission_req_table.values())
        if mission_count <= 10 and world.final_mission_id == SC2Mission.END_GAME.id:
            if ItemNames.LIBERATOR_RAID_ARTILLERY in possible_starter_items:
                possible_starter_items[ItemNames.LIBERATOR_RAID_ARTILLERY].flags |= ItemFilterFlags.StartInventory
            else:
                logger.warning(f"Tried and failed to add {ItemNames.LIBERATOR_RAID_ARTILLERY} to the start inventory because it was excluded or plando'd")


def resolve_start_abilities(world: SC2World, item_list: List[FilterItem]) -> None:
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
    upgrade_items = world.options.generic_upgrade_items
    for item in item_list:
        if item.data.type == Items.ItemType.Upgrade:
            if not include_upgrades or (item.name not in upgrade_included_names[upgrade_items]):
                item.flags |= ItemFilterFlags.Excluded


def flag_excluded_item_sets(world: SC2World, item_list: List[FilterItem]) -> None:
    """Excludes items based on item set options (`nco_items`, `bw_items`, `ext_items`)"""
    # Note(mm): These options should just be removed in favour of better item sets and a single "vanilla only" switch
    item_sets = {'wol', 'hots', 'lotv'}
    if get_option_value(world, 'nco_items') or SC2Campaign.NCO in get_enabled_campaigns(world):
        item_sets.add('nco')
    if get_option_value(world, 'bw_items'):
        item_sets.add('bw')
    if get_option_value(world, 'ext_items'):
        item_sets.add('ext')

    def allowed_quantity(name: str, data: ItemData) -> int:
        if not data.origin.intersection(item_sets):
            return 0
        elif name in progressive_if_nco and 'nco' not in item_sets:
            return 1
        elif name in progressive_if_ext and 'ext' not in item_sets:
            return 1
        else:
            return data.quantity

    amounts: Dict[str, int] = {}
    for item in item_list:
        if ItemFilterFlags.Excluded in item.flags:
            continue
        max_quantity = allowed_quantity(item.name, item.data)
        amount_in_pool = amounts.get(item.name, 0)
        if max_quantity > amount_in_pool:
            amounts[item.name] = amount_in_pool + 1
        else:
            item.flags |= ItemFilterFlags.Excluded


def flag_and_add_resource_locations(world: SC2World, item_list: List[FilterItem]) -> None:
    """
    Filters the locations in the world using a trash or Nothing item
    :param world: The sc2 world object
    :param item_list: The current list of items to append to
    """
    open_locations = [location for location in world.location_cache if location.item is None]
    plando_locations = get_plando_locations(world)
    resource_location_types = get_location_types(world, LocationInclusion.option_resources)
    location_data = {sc2_location.name: sc2_location for sc2_location in get_locations(world)}
    for location in open_locations:
        # Go through the locations that aren't locked yet (early unit, etc)
        if location.name not in plando_locations:
            # The location is not plando'd
            sc2_location = location_data[location.name]
            if sc2_location.type in resource_location_types:
                item_name = world.random.choice(filler_items)
                item = create_item_with_correct_settings(world.player, item_name)
                location.place_locked_item(item)
                item_list.append(FilterItem(item_name, Items.item_table[item_name], 0, ItemFilterFlags.Plando|ItemFilterFlags.Locked))
                world.locked_locations.append(location.name)


def prune_item_pool(world: SC2World, item_list: List[FilterItem]) -> List[Item]:
    """Prunes the item pool size to be less than the number of available locations"""

    item_list = [item for item in item_list if ItemFilterFlags.Unremovable & item.flags or ItemFilterFlags.Excluded not in item.flags]
    num_items = len(item_list)
    last_num_items = -1
    while num_items != last_num_items:
        # Remove orphan items until there are no more being removed
        item_list = [item for item in item_list if ItemFilterFlags.Unremovable & item.flags or item_list_contains_parent(item.data, item_list)]
        last_num_items = num_items
        num_items = len(item_list)

    pool: List[Item] = []
    locked_items: List[Item] = []
    existing_items: List[Item] = []
    for item in item_list:
        ap_item = create_item_with_correct_settings(world.player, item.name)
        if ItemFilterFlags.StartInventory in item.flags:
            existing_items.append(ap_item)
        elif ItemFilterFlags.Locked in item.flags:
            locked_items.append(ap_item)
        else:
            pool.append(ap_item)

    fill_pool_with_kerrigan_levels(world, pool)
    filtered_pool = filter_items(world, world.mission_req_table, world.location_cache, pool, existing_items, locked_items)
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


def get_excluded_items(world: World) -> Set[str]:
    excluded_items: Set[str] = set(get_option_value(world, 'excluded_items'))
    for item in world.multiworld.precollected_items[world.player]:
        excluded_items.add(item.name)
    locked_items: Set[str] = set(get_option_value(world, 'locked_items'))
    # Starter items are also excluded items
    starter_items: Set[str] = set(get_option_value(world, 'start_inventory'))
    item_table = get_full_item_list()
    soa_presence = get_option_value(world, "spear_of_adun_presence")
    soa_autocast_presence = get_option_value(world, "spear_of_adun_autonomously_cast_ability_presence")
    enabled_campaigns = get_enabled_campaigns(world)

    # Ensure no item is both guaranteed and excluded
    invalid_items = excluded_items.intersection(locked_items)
    invalid_count = len(invalid_items)
    # Don't count starter items that can appear multiple times
    invalid_count -= len([item for item in starter_items.intersection(locked_items) if item_table[item].quantity != 1])
    if invalid_count > 0:
        raise Exception(f"{invalid_count} item{'s are' if invalid_count > 1 else ' is'} both locked and excluded from generation.  Please adjust your excluded items and locked items.")

    def smart_exclude(item_choices: Set[str], choices_to_keep: int):
        expected_choices = len(item_choices)
        if expected_choices == 0:
            return
        item_choices = set(item_choices)
        starter_choices = item_choices.intersection(starter_items)
        excluded_choices = item_choices.intersection(excluded_items)
        item_choices.difference_update(excluded_choices)
        item_choices.difference_update(locked_items)
        candidates = sorted(item_choices)
        exclude_amount = min(expected_choices - choices_to_keep - len(excluded_choices) + len(starter_choices), len(candidates))
        if exclude_amount > 0:
            excluded_items.update(world.random.sample(candidates, exclude_amount))

    # Nova gear exclusion if NCO not in campaigns
    if SC2Campaign.NCO not in enabled_campaigns:
        excluded_items = excluded_items.union(nova_equipment)

    kerrigan_presence = get_option_value(world, "kerrigan_presence")
    # Exclude Primal Form item if option is not set or Kerrigan is unavailable
    if get_option_value(world, "kerrigan_primal_status") != KerriganPrimalStatus.option_item or \
        (kerrigan_presence == KerriganPresence.option_not_present):
        excluded_items.add(ItemNames.KERRIGAN_PRIMAL_FORM)

    # no Kerrigan, but keep non-Kerrigan passives
    if kerrigan_presence == KerriganPresence.option_not_present:
        smart_exclude(kerrigan_only_passives, 0)
        for tier in range(7):
            smart_exclude(kerrigan_actives[tier], 0)

    # SOA exclusion, other cases are handled by generic race logic
    if (soa_presence == SpearOfAdunPresence.option_lotv_protoss and SC2Campaign.LOTV not in enabled_campaigns) \
            or soa_presence == SpearOfAdunPresence.option_not_present:
        excluded_items.update(spear_of_adun_calldowns)
    if (soa_autocast_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_lotv_protoss \
            and SC2Campaign.LOTV not in enabled_campaigns) \
            or soa_autocast_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present:
        excluded_items.update(spear_of_adun_castable_passives)

    return excluded_items


def assign_starter_items(world: SC2World, excluded_items: Set[str], locked_locations: List[str], location_cache: List[Location]) -> List[Item]:
    starter_items: List[Item] = []
    non_local_items = get_option_value(world, "non_local_items")
    starter_unit = get_option_value(world, "starter_unit")
    enabled_campaigns = get_enabled_campaigns(world)
    first_mission = get_first_mission(world.mission_req_table).mission_name
    # Ensuring that first mission is completable
    if starter_unit == StarterUnit.option_off:
        starter_mission_locations = [location.name for location in location_cache
                                     if location.parent_region.name == first_mission
                                     and location.access_rule == Location.access_rule]
        if not starter_mission_locations:
            # Force early unit if first mission is impossible without one
            starter_unit = StarterUnit.option_any_starter_unit

    if starter_unit != StarterUnit.option_off:
        first_race = lookup_name_to_mission[first_mission].race

        if first_race == SC2Race.ANY:
            # If the first mission is a logic-less no-build
            mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]] = world.mission_req_table
            races = get_used_races(mission_req_table, world)
            races.remove(SC2Race.ANY)
            if lookup_name_to_mission[first_mission].race in races:
                # The campaign's race is in (At least one mission that's not logic-less no-build exists)
                first_race = lookup_name_to_mission[first_mission].campaign.race
            elif len(races) > 0:
                # The campaign only has logic-less no-build missions. Find any other valid race
                first_race = world.random.choice(list(races))

        if first_race != SC2Race.ANY:
            # The race of the early unit has been chosen
            basic_units = get_basic_units(world, first_race)
            if starter_unit == StarterUnit.option_balanced:
                basic_units = basic_units.difference(not_balanced_starting_units)
            if first_mission == SC2Mission.DARK_WHISPERS.mission_name:
                # Special case - you don't have a logicless location but need an AA
                basic_units = basic_units.difference(
                    {ItemNames.ZEALOT, ItemNames.CENTURION, ItemNames.SENTINEL, ItemNames.BLOOD_HUNTER,
                     ItemNames.AVENGER, ItemNames.IMMORTAL, ItemNames.ANNIHILATOR, ItemNames.VANGUARD})
            if first_mission == SC2Mission.SUDDEN_STRIKE.mission_name:
                # Special case - cliffjumpers
                basic_units = {ItemNames.REAPER, ItemNames.GOLIATH, ItemNames.SIEGE_TANK, ItemNames.VIKING, ItemNames.BANSHEE}
            local_basic_unit = sorted(item for item in basic_units if item not in non_local_items and item not in excluded_items)
            if not local_basic_unit:
                # Drop non_local_items constraint
                local_basic_unit = sorted(item for item in basic_units if item not in excluded_items)
                if not local_basic_unit:
                    raise Exception("Early Unit: At least one basic unit must be included")

            unit: Item = add_starter_item(world, excluded_items, local_basic_unit)
            starter_items.append(unit)

            # NCO-only specific rules
            if first_mission == SC2Mission.SUDDEN_STRIKE.mission_name:
                support_item: Union[str, None] = None
                if unit.name == ItemNames.REAPER:
                    support_item = ItemNames.REAPER_SPIDER_MINES
                elif unit.name == ItemNames.GOLIATH:
                    support_item = ItemNames.GOLIATH_JUMP_JETS
                elif unit.name == ItemNames.SIEGE_TANK:
                    support_item = ItemNames.SIEGE_TANK_JUMP_JETS
                elif unit.name == ItemNames.VIKING:
                    support_item = ItemNames.VIKING_SMART_SERVOS
                if support_item is not None:
                    starter_items.append(add_starter_item(world, excluded_items, [support_item]))
                starter_items.append(add_starter_item(world, excluded_items, [ItemNames.NOVA_JUMP_SUIT_MODULE]))
                starter_items.append(
                    add_starter_item(world, excluded_items,
                                     [
                                         ItemNames.NOVA_HELLFIRE_SHOTGUN,
                                         ItemNames.NOVA_PLASMA_RIFLE,
                                         ItemNames.NOVA_PULSE_GRENADES
                                     ]))
            if enabled_campaigns == {SC2Campaign.NCO}:
                starter_items.append(add_starter_item(world, excluded_items, [ItemNames.LIBERATOR_RAID_ARTILLERY]))
    
    starter_abilities = get_option_value(world, 'start_primary_abilities')
    assert isinstance(starter_abilities, int)
    if starter_abilities:
        ability_count = starter_abilities
        ability_tiers = [0, 1, 3]
        world.random.shuffle(ability_tiers)
        if ability_count > 3:
            ability_tiers.append(6)
        for tier in ability_tiers:
            abilities = kerrigan_actives[tier].union(kerrigan_passives[tier]).difference(excluded_items, non_local_items)
            if not abilities:
                abilities = kerrigan_actives[tier].union(kerrigan_passives[tier]).difference(excluded_items)
            if abilities:
                ability_count -= 1
                starter_items.append(add_starter_item(world, excluded_items, list(abilities)))
                if ability_count == 0:
                    break

    return starter_items


def get_first_mission(mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]]) -> SC2Mission:
    # The first world should also be the starting world
    campaigns = mission_req_table.keys()
    lowest_id = min([campaign.id for campaign in campaigns])
    first_campaign = [campaign for campaign in campaigns if campaign.id == lowest_id][0]
    return list(mission_req_table[first_campaign].values())[0].mission


def add_starter_item(world: World, excluded_items: Set[str], item_list: Sequence[str]) -> Item:

    item_name = world.random.choice(sorted(item_list))

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(world.player, item_name)

    world.multiworld.push_precollected(item)

    return item


def get_item_pool(world: SC2World, mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]],
                  starter_items: List[Item], excluded_items: Set[str], location_cache: List[Location]) -> List[Item]:
    pool: List[Item] = []

    # For the future: goal items like Artifact Shards go here
    locked_items = []

    # YAML items
    yaml_locked_items = get_option_value(world, 'locked_items')
    assert not isinstance(yaml_locked_items, int)

    # Adjust generic upgrade availability based on options
    include_upgrades = get_option_value(world, 'generic_upgrade_missions') == 0
    upgrade_items = get_option_value(world, 'generic_upgrade_items')
    assert isinstance(upgrade_items, int)

    # Include items from outside main campaigns
    item_sets = {'wol', 'hots', 'lotv'}
    if get_option_value(world, 'nco_items') \
            or SC2Campaign.NCO in get_enabled_campaigns(world):
        item_sets.add('nco')
    if get_option_value(world, 'bw_items'):
        item_sets.add('bw')
    if get_option_value(world, 'ext_items'):
        item_sets.add('ext')

    def allowed_quantity(name: str, data: ItemData) -> int:
        if name in excluded_items \
                or data.type == "Upgrade" and (not include_upgrades or name not in upgrade_included_names[upgrade_items]) \
                or not data.origin.intersection(item_sets):
            return 0
        elif name in progressive_if_nco and 'nco' not in item_sets:
            return 1
        elif name in progressive_if_ext and 'ext' not in item_sets:
            return 1
        else:
            return data.quantity

    for name, data in Items.item_table.items():
        for index in range(allowed_quantity(name, data)):
            item = create_item_with_correct_settings(world.player, name)
            if name in yaml_locked_items:
                locked_items.append(item)
            else:
                pool.append(item)

    existing_items = starter_items + [item for item in world.multiworld.precollected_items[world.player] if item not in starter_items]
    existing_names = [item.name for item in existing_items]

    # Check the parent item integrity, exclude items
    pool[:] = [item for item in pool if pool_contains_parent(item, pool + locked_items + existing_items)]

    # Removing upgrades for excluded items
    for item_name in excluded_items:
        if item_name in existing_names:
            continue
        invalid_upgrades = get_item_upgrades(pool, item_name)
        for invalid_upgrade in invalid_upgrades:
            pool.remove(invalid_upgrade)

    fill_pool_with_kerrigan_levels(world, pool)
    filtered_pool = filter_items(world, mission_req_table, location_cache, pool, existing_items, locked_items)
    return filtered_pool


def fill_item_pool_with_dummy_items(self: SC2World, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(self.player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = Items.item_table[name]

    item = Item(name, data.classification, data.code, player)

    return item


def pool_contains_parent(item: Item, pool: Iterable[Item]):
    item_data = get_full_item_list().get(item.name)
    if item_data.parent_item is None:
        # The item has not associated parent, the item is valid
        return True
    parent_item = item_data.parent_item
    # Check if the pool contains the parent item
    return parent_item in [pool_item.name for pool_item in pool]


def fill_resource_locations(world: World, locked_locations: List[str], location_cache: List[Location]):
    """
    Filters the locations in the world using a trash or Nothing item
    :param multiworld:
    :param player:
    :param locked_locations:
    :param location_cache:
    :return:
    """
    open_locations = [location for location in location_cache if location.item is None]
    plando_locations = get_plando_locations(world)
    resource_location_types = get_location_types(world, LocationInclusion.option_resources)
    location_data = {sc2_location.name: sc2_location for sc2_location in get_locations(world)}
    for location in open_locations:
        # Go through the locations that aren't locked yet (early unit, etc)
        if location.name not in plando_locations:
            # The location is not plando'd
            sc2_location = location_data[location.name]
            if sc2_location.type in resource_location_types:
                item_name = world.random.choice(filler_items)
                item = create_item_with_correct_settings(world.player, item_name)
                location.place_locked_item(item)
                locked_locations.append(location.name)


def fill_pool_with_kerrigan_levels(world: World, item_pool: List[Item]):
    total_levels = get_option_value(world, "kerrigan_level_item_sum")
    if get_option_value(world, "kerrigan_presence") not in kerrigan_unit_available \
            or total_levels == 0 \
            or SC2Campaign.HOTS not in get_enabled_campaigns(world):
        return
    
    def add_kerrigan_level_items(level_amount: int, item_amount: int):
        name = f"{level_amount} Kerrigan Level"
        if level_amount > 1:
            name += "s"
        for _ in range(item_amount):
            item_pool.append(create_item_with_correct_settings(world.player, name))

    sizes = [70, 35, 14, 10, 7, 5, 2, 1]
    option = get_option_value(world, "kerrigan_level_item_distribution")

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
