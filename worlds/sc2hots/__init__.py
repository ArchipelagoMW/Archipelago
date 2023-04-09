import typing

from typing import List, Set, Tuple, Dict
from math import floor, ceil
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import StarcraftHotSItem, item_table, filler_items, item_name_groups, get_full_item_list, \
    get_basic_units, upgrade_included_names, ItemData
from .Locations import get_locations
from .Regions import create_regions
from .Options import sc2hots_options, get_option_value
from .LogicMixin import SC2HotSLogic, KERRIGAN_ACTIVES, KERRIGAN_PASSIVES, KERRIGAN_ONLY_PASSIVES
from .PoolFilter import filter_missions, filter_items, get_item_upgrades, UPGRADABLE_ITEMS
from .MissionTables import starting_mission_locations, MissionInfo


class Starcraft2HotSWebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor"]
    )

    tutorials = [setup]


class SC2HotSWorld(World):
    """
    StarCraft II: Heart of the Swarm is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Command Raynor's Raiders in collecting pieces of the Keystone in order to stop the zerg threat posed by the Queen of Blades.
    """

    game = "Starcraft 2 Heart of the Swarm"
    web = Starcraft2HotSWebWorld()
    data_version = 3

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    option_definitions = sc2hots_options

    item_name_groups = item_name_groups
    locked_locations: typing.List[str]
    location_cache: typing.List[Location]
    mission_req_table = {}
    final_mission_id: int
    victory_item: str
    required_client_version = 0, 3, 6

    def __init__(self, multiworld: MultiWorld, player: int):
        super(SC2HotSWorld, self).__init__(multiworld, player)
        self.location_cache = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftHotSItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        self.mission_req_table, self.final_mission_id, self.victory_item = create_regions(
            self.multiworld, self.player, get_locations(self.multiworld, self.player), self.location_cache
        )

    def generate_basic(self):
        excluded_items = get_excluded_items(self.multiworld, self.player)

        starter_items = assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)

        pool = get_item_pool(self.multiworld, self.player, self.mission_req_table, starter_items, excluded_items, self.location_cache)

        fill_item_pool_with_dummy_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.victory_item, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in sc2hots_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        slot_req_table = {}
        for mission in self.mission_req_table:
            slot_req_table[mission] = self.mission_req_table[mission]._asdict()

        slot_data["mission_req"] = slot_req_table
        slot_data["final_mission"] = self.final_mission_id
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
    guaranteed_items = locked_items.union(starter_items)
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

    # Ensure no Kerrigan ability tier has two locked actives
    # Should only be called when actives are relevant to the player
    def test_kerrigan_actives(tier: int):
        actives_amount = len(guaranteed_items.intersection(KERRIGAN_ACTIVES[tier]))
        if actives_amount > 1:
            raise Exception(f"Kerrigan Ability Tier {tier + 1} has {actives_amount} guaranteed active abilities.  The maximum allowed is 1.  Please adjust your locked items and start inventory.")

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
            smart_exclude(KERRIGAN_ACTIVES[tier].union(KERRIGAN_PASSIVES[tier]), 0)
    else:
        # no Kerrigan, but keep non-Kerrigan passives
        if kerriganless == 1:
            smart_exclude(KERRIGAN_ONLY_PASSIVES, 0)
            for tier in range(7):
                smart_exclude(KERRIGAN_ACTIVES[tier], 0)
        # pick a random ability per tier and remove all others
        if get_option_value(multiworld, player, "include_all_kerrigan_abilities") == 0:
            for tier in range(7):
                # ignore active abilities if Kerrigan is off
                if kerriganless == 1:
                    smart_exclude(KERRIGAN_PASSIVES[tier], 0)
                else:
                    test_kerrigan_actives(tier)
                    smart_exclude(KERRIGAN_ACTIVES[tier].union(KERRIGAN_PASSIVES[tier]), 1)
            # ensure Kerrigan has an active T1 or T2 ability for no-build missions on Standard
            if get_option_value(multiworld, player, "required_tactics") == 0 and get_option_value(multiworld, player, "shuffle_no_build"):
                active_t1_t2 = KERRIGAN_ACTIVES[0].union(KERRIGAN_ACTIVES[1])
                if active_t1_t2.issubset(excluded_items):
                    # all T1 and T2 actives were excluded
                    tier = multiworld.random.choice([0, 1])
                    excluded_items.update(KERRIGAN_PASSIVES[tier])
                    active_ability = multiworld.random.choice(sorted(KERRIGAN_ACTIVES[tier]))
                    excluded_items.remove(active_ability)
        elif kerriganless == 0:  # if Kerrigan exists, pick a random active ability per tier and remove the other active abilities
            for tier in range(7):
                test_kerrigan_actives(tier)
                smart_exclude(KERRIGAN_ACTIVES[tier], 1)

    return excluded_items


def assign_starter_items(multiworld: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]) -> List[Item]:
    non_local_items = multiworld.non_local_items[player].value
    starter_items = []
    if get_option_value(multiworld, player, "early_unit"):
        local_basic_unit = sorted(item for item in get_basic_units(multiworld, player) if item not in non_local_items and item not in excluded_items)
        if not local_basic_unit:
            local_basic_unit = sorted(item for item in get_basic_units(multiworld, player) if item not in excluded_items)
            if not local_basic_unit:
                raise Exception("Early Unit: At least one basic unit must be included")

        # The first world should also be the starting world
        first_mission = list(multiworld.worlds[player].mission_req_table)[0]
        if first_mission in starting_mission_locations:
            first_location = starting_mission_locations[first_mission]
        # elif first_mission == "In Utter Darkness":
        #     first_location = first_mission + ": Defeat"
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
            abilities = KERRIGAN_ACTIVES[tier].union(KERRIGAN_PASSIVES[tier]).difference(excluded_items)
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


def get_item_pool(multiworld: MultiWorld, player: int, mission_req_table: Dict[str, MissionInfo],
                  starter_items: List[str], excluded_items: Set[str], location_cache: List[Location]) -> List[Item]:
    pool: List[Item] = []

    # For the future: goal items like Artifact Shards go here
    locked_items = []

    # YAML items
    yaml_locked_items = get_option_value(multiworld, player, 'locked_items')

    # Adjust generic upgrade availability based on options
    include_upgrades = get_option_value(multiworld, player, 'generic_upgrade_missions') == 0
    upgrade_items = get_option_value(multiworld, player, 'generic_upgrade_items')

    def item_allowed(name: str, data: ItemData) -> bool:
        return name not in excluded_items and \
            (data.type != "Upgrade" or (include_upgrades and \
            name in upgrade_included_names[upgrade_items]))

    for name, data in item_table.items():
        # if name not in excluded_items:
        if item_allowed(name, data):
            for _ in range(data.quantity):
                item = create_item_with_correct_settings(player, name)
                if name in yaml_locked_items:
                    locked_items.append(item)
                else:
                    pool.append(item)

    existing_items = starter_items + [item for item in multiworld.precollected_items[player]]
    existing_names = [item.name for item in existing_items]
    # Removing upgrades for excluded items
    for item_name in excluded_items:
        if item_name in existing_names:
            continue
        invalid_upgrades = get_item_upgrades(pool, item_name)
        for invalid_upgrade in invalid_upgrades:
            pool.remove(invalid_upgrade)
    
    fill_pool_with_kerrigan_levels(multiworld, player, pool)
    inventory_size = len([location for location in location_cache if location.item is None])
    trap_count = int(inventory_size * get_option_value(multiworld, player, "trap_percentage") / 100)
    inventory_size -= trap_count
    filtered_pool = filter_items(multiworld, player, mission_req_table, location_cache,
                                 pool, existing_items, locked_items, inventory_size)
    for _ in range(trap_count):
        filtered_pool.append(create_item_with_correct_settings(player, "Transmission Trap"))

    return filtered_pool


def fill_item_pool_with_dummy_items(self: SC2HotSWorld, multiworld: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = item_table[name]

    item = Item(name, data.classification, data.code, player)

    return item

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
