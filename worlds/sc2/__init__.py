import typing
from dataclasses import fields

from typing import List, Set, Iterable, Sequence, Dict, Callable, Union
from math import floor, ceil
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from . import ItemNames
from .Items import StarcraftItem, filler_items, get_item_table, get_full_item_list, \
    get_basic_units, ItemData, upgrade_included_names, progressive_if_nco, kerrigan_actives, kerrigan_passives, \
    kerrigan_only_passives, progressive_if_ext, not_balanced_starting_units, spear_of_adun_calldowns, \
    spear_of_adun_castable_passives, nova_equipment
from .ItemGroups import item_name_groups
from .Locations import get_locations, LocationType, get_location_types, get_plando_locations
from .Regions import create_regions
from .Options import get_option_value, LocationInclusion, KerriganLevelItemDistribution, \
    KerriganPresence, KerriganPrimalStatus, RequiredTactics, kerrigan_unit_available, StarterUnit, SpearOfAdunPresence, \
    get_enabled_campaigns, SpearOfAdunAutonomouslyCastAbilityPresence, Starcraft2Options
from .PoolFilter import filter_items, get_item_upgrades, UPGRADABLE_ITEMS, missions_in_mission_table, get_used_races
from .MissionTables import MissionInfo, SC2Campaign, lookup_name_to_mission, SC2Mission, \
    SC2Race


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

    tutorials = [setup_en, setup_fr]
    game_info_languages = ["en", "fr"]


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
    locked_locations: typing.List[str]
    location_cache: typing.List[Location]
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
        setup_events(self.player, self.locked_locations, self.location_cache)

        excluded_items = get_excluded_items(self)

        starter_items = assign_starter_items(self, excluded_items, self.locked_locations, self.location_cache)

        fill_resource_locations(self, self.locked_locations, self.location_cache)

        pool = get_item_pool(self, self.mission_req_table, starter_items, excluded_items, self.location_cache)

        fill_item_pool_with_dummy_items(self, self.locked_locations, self.location_cache, pool)

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


def setup_events(player: int, locked_locations: typing.List[str], location_cache: typing.List[Location]):
    for location in location_cache:
        if location.address is None:
            item = Item(location.name, ItemClassification.progression, None, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


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
        (kerrigan_presence in {KerriganPresence.option_not_present, KerriganPresence.option_not_present_and_no_passives}):
        excluded_items.add(ItemNames.KERRIGAN_PRIMAL_FORM)

    # no Kerrigan & remove all passives => remove all abilities
    if kerrigan_presence == KerriganPresence.option_not_present_and_no_passives:
        for tier in range(7):
            smart_exclude(kerrigan_actives[tier].union(kerrigan_passives[tier]), 0)
    else:
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


def assign_starter_items(world: World, excluded_items: Set[str], locked_locations: List[str], location_cache: typing.List[Location]) -> List[Item]:
    starter_items: List[Item] = []
    non_local_items = get_option_value(world, "non_local_items")
    starter_unit = get_option_value(world, "starter_unit")
    enabled_campaigns = get_enabled_campaigns(world)
    first_mission = get_first_mission(world.mission_req_table)
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


def get_first_mission(mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]]) -> str:
    # The first world should also be the starting world
    campaigns = mission_req_table.keys()
    lowest_id = min([campaign.id for campaign in campaigns])
    first_campaign = [campaign for campaign in campaigns if campaign.id == lowest_id][0]
    first_mission = list(mission_req_table[first_campaign])[0]
    return first_mission


def add_starter_item(world: World, excluded_items: Set[str], item_list: Sequence[str]) -> Item:

    item_name = world.random.choice(sorted(item_list))

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(world.player, item_name)

    world.multiworld.push_precollected(item)

    return item


def get_item_pool(world: World, mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]],
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

    for name, data in get_item_table().items():
        for _ in range(allowed_quantity(name, data)):
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
    data = get_full_item_list()[name]

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


def place_exclusion_item(item_name, location, locked_locations, player):
    item = create_item_with_correct_settings(player, item_name)
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
