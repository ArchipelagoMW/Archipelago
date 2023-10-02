import typing

from typing import List, Set, Tuple, Dict
from math import floor, ceil
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import StarcraftWoLItem, filler_items, item_name_groups, get_item_table, get_full_item_list, \
    get_basic_units, ItemData, upgrade_included_names, progressive_if_nco, kerrigan_actives, kerrigan_passives, kerrigan_only_passives
from .Locations import get_locations, LocationType
from .Regions import create_regions
from .Options import sc2wol_options, get_option_value, LocationInclusion
from .LogicMixin import SC2WoLLogic
from .PoolFilter import filter_missions, filter_items, get_item_upgrades, UPGRADABLE_ITEMS
from .MissionTables import starting_mission_locations, MissionInfo, SC2Campaign, lookup_name_to_mission


class Starcraft2WoLWebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor"]
    )

    tutorials = [setup]


class SC2WoLWorld(World):
    """
    StarCraft II: Wings of Liberty is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Command Raynor's Raiders in collecting pieces of the Keystone in order to stop the zerg threat posed by the Queen of Blades.
    """

    game = "Starcraft 2 Wings of Liberty"
    web = Starcraft2WoLWebWorld()
    data_version = 4

    item_name_to_id = {name: data.code for name, data in get_full_item_list().items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    option_definitions = sc2wol_options

    item_name_groups = item_name_groups
    locked_locations: typing.List[str]
    location_cache: typing.List[Location]
    mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]] = {}
    final_mission_id: int
    victory_item: str
    required_client_version = 0, 3, 6

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2WoLWorld, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftWoLItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.mission_req_table, self.final_mission_id, self.victory_item = create_regions(
            self.multiworld, self.player, get_locations(self.multiworld, self.player), self.location_cache
        )

    def create_items(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        excluded_items = get_excluded_items(self.multiworld, self.player)

        starter_items = assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)

        filter_locations(self.multiworld, self.player, self.locked_locations, self.location_cache)

        pool = get_item_pool(self.multiworld, self.player, self.mission_req_table, starter_items, excluded_items, self.location_cache)

        fill_item_pool_with_dummy_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.victory_item, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in sc2wol_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
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

        slot_data["mission_req"] = slot_req_table
        slot_data["final_mission"] = self.final_mission_id
        slot_data["version"] = 3
        return slot_data


def setup_events(player: int, locked_locations: typing.List[str], location_cache: typing.List[Location]):
    for location in location_cache:
        if location.address is None:
            item = Item(location.name, ItemClassification.progression, None, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_excluded_items(multiworld: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set(get_option_value(multiworld, player, 'excluded_items'))
    for item in multiworld.precollected_items[player]:
        excluded_items.add(item.name)
    locked_items: Set[str] = set(get_option_value(multiworld, player, 'locked_items'))
    # Starter items are also excluded items
    starter_items: Set[str] = set(get_option_value(multiworld, player, 'start_inventory'))
    item_table = get_full_item_list()
    mutation_count = get_option_value(multiworld, player, "include_mutations")
    strain_count = get_option_value(multiworld, player, "include_strains")

    # Exclude Primal Form item if option is not set
    if get_option_value(multiworld, player, "kerrigan_primal_status") != 5:
        excluded_items.add("Primal Form (Kerrigan)")

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
            excluded_items.update(multiworld.random.sample(candidates, exclude_amount))

    # pick a random mutation & strain for each unit and exclude the rest
    for name in UPGRADABLE_ITEMS:
        mutations = {child_name for child_name, item in item_table.items()
                   if item.parent_item == name and item.type == "Mutation"}
        smart_exclude(mutations, mutation_count)
        strains = {child_name for child_name, item in item_table.items()
                   if item.parent_item == name and item.type == "Strain" and child_name not in excluded_items}
        smart_exclude(strains, strain_count)

    kerriganless = get_option_value(multiworld, player, "kerriganless")
    # no Kerrigan & remove all passives => remove all abilities
    if kerriganless == 2:
        for tier in range(7):
            smart_exclude(kerrigan_actives[tier].union(kerrigan_passives[tier]), 0)
    else:
        # no Kerrigan, but keep non-Kerrigan passives
        if kerriganless == 1:
            smart_exclude(kerrigan_only_passives, 0)
            for tier in range(7):
                smart_exclude(kerrigan_actives[tier], 0)
        # pick a random ability per tier and remove all others
        if get_option_value(multiworld, player, "include_all_kerrigan_abilities") == 0:
            for tier in range(7):
                # ignore active abilities if Kerrigan is off
                if kerriganless == 1:
                    smart_exclude(kerrigan_passives[tier], 0)
                else:
                    smart_exclude(kerrigan_actives[tier].union(kerrigan_passives[tier]), 1)
            # ensure Kerrigan has an active T1 or T2 ability for no-build missions on Standard
            if get_option_value(multiworld, player, "required_tactics") == 0 and get_option_value(multiworld, player, "shuffle_no_build"):
                active_t1_t2 = kerrigan_actives[0].union(kerrigan_actives[1])
                if active_t1_t2.issubset(excluded_items):
                    # all T1 and T2 actives were excluded
                    tier = multiworld.random.choice([0, 1])
                    excluded_items.update(kerrigan_passives[tier])
                    active_ability = multiworld.random.choice(sorted(kerrigan_actives[tier]))
                    excluded_items.remove(active_ability)
    # if Kerrigan exists and all abilities are included,
    # no ability needs to be excluded

    return excluded_items


def assign_starter_items(multiworld: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]) -> List[Item]:
    starter_items = []
    non_local_items = multiworld.non_local_items[player].value
    if get_option_value(multiworld, player, "early_unit"):
        # The first world should also be the starting world
        campaigns = multiworld.worlds[player].mission_req_table.keys()
        lowest_id = min([campaign.id for campaign in campaigns])
        first_campaign = [campaign for campaign in campaigns if campaign.id == lowest_id][0]
        first_mission = list(multiworld.worlds[player].mission_req_table[first_campaign])[0]
        first_race = lookup_name_to_mission[first_mission].race

        local_basic_unit = sorted(item for item in get_basic_units(multiworld, player, first_race) if item not in non_local_items and item not in excluded_items)
        if not local_basic_unit:
            local_basic_unit = sorted(item for item in get_basic_units(multiworld, player, first_race) if item not in excluded_items)
            if not local_basic_unit:
                raise Exception("Early Unit: At least one basic unit must be included")

        if first_mission in starting_mission_locations:
            first_location = starting_mission_locations[first_mission]
        elif first_mission == "In Utter Darkness":
            first_location = first_mission + ": Defeat"
        else:
            first_location = first_mission + ": Victory"

        starter_items.append(assign_starter_item(multiworld, player, excluded_items, locked_locations, first_location, local_basic_unit))
    
    starter_abilities = get_option_value(multiworld, player, 'start_primary_abilities')
    if starter_abilities:
        ability_count = starter_abilities
        ability_tiers = [0, 1, 3]
        multiworld.random.shuffle(ability_tiers)
        if ability_count > 3:
            ability_tiers.append(6)
        for tier in ability_tiers:
            abilities = kerrigan_actives[tier].union(kerrigan_passives[tier]).difference(excluded_items, non_local_items)
            if not abilities:
                abilities = kerrigan_actives[tier].union(kerrigan_passives[tier]).difference(excluded_items)
            if abilities:
                ability_count -= 1
                ability = multiworld.random.choice(sorted(abilities))
                ability_item = create_item_with_correct_settings(player, ability)
                multiworld.push_precollected(ability_item)
                excluded_items.add(ability)
                starter_items.append(ability_item)
                if ability_count == 0:
                    break

    return starter_items


def assign_starter_item(multiworld: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str],
                        location: str, item_list: Tuple[str, ...]) -> Item:

    item_name = multiworld.random.choice(item_list)

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(player, item_name)

    multiworld.get_location(location, player).place_locked_item(item)

    locked_locations.append(location)

    return item


def get_item_pool(multiworld: MultiWorld, player: int, mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]],
                  starter_items: List[Item], excluded_items: Set[str], location_cache: List[Location]) -> List[Item]:
    pool: List[Item] = []

    # For the future: goal items like Artifact Shards go here
    locked_items = []

    # YAML items
    yaml_locked_items = get_option_value(multiworld, player, 'locked_items')

    # Adjust generic upgrade availability based on options
    include_upgrades = get_option_value(multiworld, player, 'generic_upgrade_missions') == 0
    upgrade_items = get_option_value(multiworld, player, 'generic_upgrade_items')

    # Include items from outside Wings of Liberty
    # TODO should this be more sophisticated?
    item_sets = {'wol', 'hots'}
    if get_option_value(multiworld, player, 'nco_items'):
        item_sets.add('nco')
    if get_option_value(multiworld, player, 'bw_items'):
        item_sets.add('bw')
    if get_option_value(multiworld, player, 'ext_items'):
        item_sets.add('ext')

    def allowed_quantity(name: str, data: ItemData) -> int:
        if name in excluded_items \
                or data.type == "Upgrade" and (not include_upgrades or name not in upgrade_included_names[upgrade_items]) \
                or not data.origin.intersection(item_sets):
            return 0
        elif name in progressive_if_nco and 'nco' not in item_sets:
            return 1
        else:
            return data.quantity

    for name, data in get_item_table(multiworld, player).items():
        for i in range(allowed_quantity(name, data)):
            item = create_item_with_correct_settings(player, name)
            if name in yaml_locked_items:
                locked_items.append(item)
            else:
                pool.append(item)

    existing_items = starter_items + [item for item in multiworld.precollected_items[player]]
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

    fill_pool_with_kerrigan_levels(multiworld, player, pool)
    filtered_pool = filter_items(multiworld, player, mission_req_table, location_cache, pool, existing_items, locked_items)
    return filtered_pool


def fill_item_pool_with_dummy_items(self: SC2WoLWorld, multiworld: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = get_full_item_list()[name]

    item = Item(name, data.classification, data.code, player)

    return item


def pool_contains_parent(item: Item, pool: [Item]):
    item_data = get_full_item_list().get(item.name)
    if item_data.parent_item is None:
        # The item has not associated parent, the item is valid
        return True
    parent_item = item_data.parent_item
    # Check if the pool contains the parent item
    return parent_item in [pool_item.name for pool_item in pool]


def filter_locations(multiworld: MultiWorld, player, locked_locations: List[str], location_cache: List[Location]):
    """
    Filters the locations in the world using a trash or Nothing item
    :param multiworld:
    :param player:
    :param locked_locations:
    :param location_cache:
    :return:
    """
    open_locations = [location for location in location_cache if location.item is None]
    plando_locations = get_plando_locations(multiworld, player)
    mission_progress_locations = get_option_value(multiworld, player, "mission_progress_locations")
    bonus_locations = get_option_value(multiworld, player, "bonus_locations")
    challenge_locations = get_option_value(multiworld, player, "challenge_locations")
    optional_boss_locations = get_option_value(multiworld, player, "optional_boss_locations")
    location_data = get_locations(multiworld, player)
    for location in open_locations:
        # Go through the locations that aren't locked yet (early unit, etc)
        if location.name not in plando_locations:
            # The location is not plando'd
            sc2_location = [sc2_location for sc2_location in location_data if sc2_location.name == location.name][0]
            location_type = sc2_location.type

            if location_type == LocationType.MISSION_PROGRESS \
                    and mission_progress_locations != LocationInclusion.option_enabled:
                item_name = get_exclusion_item(multiworld, mission_progress_locations)
                place_exclusion_item(item_name, location, locked_locations, player)

            if location_type == LocationType.BONUS \
                    and bonus_locations != LocationInclusion.option_enabled:
                item_name = get_exclusion_item(multiworld, bonus_locations)
                place_exclusion_item(item_name, location, locked_locations, player)

            if location_type == LocationType.CHALLENGE \
                    and challenge_locations != LocationInclusion.option_enabled:
                item_name = get_exclusion_item(multiworld, challenge_locations)
                place_exclusion_item(item_name, location, locked_locations, player)

            if location_type == LocationType.OPTIONAL_BOSS \
                    and optional_boss_locations != LocationInclusion.option_enabled:
                item_name = get_exclusion_item(multiworld, optional_boss_locations)
                place_exclusion_item(item_name, location, locked_locations, player)


def place_exclusion_item(item_name, location, locked_locations, player):
    item = create_item_with_correct_settings(player, item_name)
    location.place_locked_item(item)
    locked_locations.append(location.name)


def get_exclusion_item(multiworld: MultiWorld, option) -> str:
    """
    Gets the exclusion item according to settings (trash/nothing)
    :param multiworld:
    :param option:
    :return: Item used for location exclusion
    """
    if option == LocationInclusion.option_nothing:
        return "Nothing"
    elif option == LocationInclusion.option_trash:
        item = multiworld.random.choice(filler_items)
        return item
    raise Exception(f"Unsupported option type: {option}")


def get_plando_locations(multiworld: MultiWorld, player) -> List[str]:
    """

    :param multiworld:
    :param player:
    :return: A list of locations affected by a plando in a world
    """
    plando_locations = []
    for plando_setting in multiworld.plando_items[player]:
        plando_locations += plando_setting.get("locations", [])
        plando_setting_location = plando_setting.get("location", None)
        if plando_setting_location is not None:
            plando_locations.append(plando_setting_location)

    return plando_locations

def fill_pool_with_kerrigan_levels(multiworld: MultiWorld, player: int, item_pool: List[Item]):
    total_levels = get_option_value(multiworld, player, "kerrigan_level_item_sum")
    if get_option_value(multiworld, player, "kerriganless") > 0 \
        or total_levels == 0:
        return
    
    def add_kerrigan_level_items(level_amount: int, item_amount: int):
        name = f"{level_amount} Kerrigan Level"
        if level_amount > 1:
            name += "s"
        for _ in range(item_amount):
            item_pool.append(create_item_with_correct_settings(player, name))

    sizes = [70, 35, 14, 10, 7, 5, 2, 1]
    option = get_option_value(multiworld, player, "kerrigan_level_item_distribution")
    if option < 2:
        distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if option == 0: # vanilla
            distribution = [32, 0, 0, 1, 3, 0, 0, 0, 1, 1]
        elif option == 1: # smooth
            distribution = [0, 0, 0, 1, 1, 2, 2, 2, 1, 1]
        for tier in range(len(distribution)):
            add_kerrigan_level_items(tier + 1, distribution[tier])
    else:
        size = sizes[option - 2]
        round_func = round
        if total_levels > 70:
            round_func = floor
        else:
            round_func = ceil
        add_kerrigan_level_items(size, round_func(float(total_levels) / size))
