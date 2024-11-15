import os
from dataclasses import fields
from itertools import count
from typing import Dict, ClassVar

import yaml

from BaseClasses import Tutorial, Item, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .Items import ITEM_TABLE, LMItem, get_item_names_per_category, filler_items, ALL_ITEMS_TABLE
from .Locations import *
from .Options import LMOptions
from .Regions import *


def run_client():
    print("Running LM Client")
    from .LMClient import main  # lazy import

    launch_subprocess(main, name="LuigiMansionClient")


components.append(
    Component("LM Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apLM"))
)


class LMWeb(WebWorld):
    theme = "stone"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Luigi's Mansion randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["BootsinSoots"],
        )
    ]


class LMWorld(World):
    """
    Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi.
    Luigi has won a strange mansion but on arriving, he discovers it's full of ghosts!
    Armed with the mysterious Poltergust 3000, Luigi will need to overcome his fears to kick the ghosts out
    before he can move in. Wait! Is that Mario?
    """

    game: ClassVar[str] = "Luigi's Mansion"
    options_dataclass = LMOptions
    options: LMOptions

    topology_present = True
    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: LMItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[Dict[str, int]] = {
        name: LMLocation.get_apid(data.code) for name, data in ALL_LOCATION_TABLE.items() if data.code is not None
    }

    item_name_groups = get_item_names_per_category()
    required_client_version = (0, 5, 1)
    web = LMWeb()
    ghost_affected_regions = {
        "Anteroom": "No Element",
        "Wardrobe": "No Element",
        "Laundry Room": "No Element",
        "Hidden Room": "Ice",
        "Mirror Room": "No Element",
        "Storage Room": "No Element",
        "Kitchen": "Ice",
        "1F Bathroom": "No Element",
        "Courtyard": "No Element",
        "Tea Room": "No Element",
        "2F Washroom": "Fire",
        "Projection Room": "No Element",
        "Safari Room": "Water",
        "Cellar": "No Element",
        "Roof": "No Element",
        "Sealed Room": "No Element",
        "Armory": "No Element",
        "Pipe Room": "No Element"
    }

    def __init__(self, *args, **kwargs):
        self.itempool: list[LMItem] = []
        self.pre_fill_items: list[LMItem] = []

        # self.vanilla_dungeon_item_names: set[str] = set()
        # self.own_dungeon_item_names: set[str] = set()
        # self.any_dungeon_item_names: set[str] = set()

        # self.island_number_to_chart_name = ISLAND_NUMBER_TO_CHART_NAME.copy()

        # self.required_boss_item_locations: list[str] = []
        # self.required_dungeons: list[str] = []
        # self.banned_dungeons: list[str] = []
        super(LMWorld, self).__init__(*args, **kwargs)

    # def _get_access_rule(self, region):
    #   snake_case_region = region.lower().replace("'", "").replace(" ", "_")
    #   return f"can_access_{snake_case_region}"

    # def _get_dungeon_locations(self):
    #    dungeon_regions = DUNGEON_EXITS.copy()#

    # If miniboss entrances are not shuffled, include miniboss arenas as a dungeon regions
    #    if not self.options.randomize_miniboss_entrances:
    #        dungeon_regions += [
    #            "Forbidden Woods Miniboss Arena",
    #            "Tower of the Gods Miniboss Arena",
    #            "Earth Temple Miniboss Arena",
    #            "Wind Temple Miniboss Arena",
    #        ]

    # Forsaken Fortress is an odd dungeon as it exists on the Great Sea
    # Simply keep a list of all locations in the dungeon, except the boss Heart Container
    #    ff_dungeon_locations = [
    #        "Forsaken Fortress - Phantom Ganon",
    #        "Forsaken Fortress - Chest Outside Upper Jail Cell",
    #        "Forsaken Fortress - Chest Inside Lower Jail Cell",
    #        "Forsaken Fortress - Chest Guarded By Bokoblin",
    #        "Forsaken Fortress - Chest on Bed",
    #    ]

    #   return [
    #        location
    #        for location in self.multiworld.get_locations(self.player)
    #        if location.name in ff_dungeon_locations or location.region in dungeon_regions
    #    ]

    #    def _randomize_required_bosses(self):
    #        dungeon_names = set(DUNGEON_NAMES)
    #
    #        # Assert that the user is not including and excluding a dungeon at the same time
    #        if len(self.options.included_dungeons.value & self.options.excluded_dungeons.value) != 0:
    #            raise RuntimeError("Conflict found in the lists of required and banned dungeons for required bosses mode")

    #        # If the user enforces a dungeon location to be priority, consider that when selecting required bosses
    #        required_dungeons = self.options.included_dungeons.value
    #        for location_name in self.options.priority_locations.value:
    #            dungeon_name, _ = split_location_name_by_zone(location_name)
    #            if dungeon_name in dungeon_names:
    #                required_dungeons.add(dungeon_name)
    #
    #        # Ensure that we aren't prioritizing more dungeon locations than requested number of required bosses
    #        num_required_bosses = self.options.num_required_bosses
    #        if len(required_dungeons) > num_required_bosses:
    #            raise RuntimeError("Could not select required bosses to satisfy options set by user")

    # Ensure that after removing excluded dungeons that we still have enough dungeons to satisfy user options
    #        num_remaining = num_required_bosses - len(required_dungeons)
    #        remaining_dungeon_options = dungeon_names - required_dungeons - self.options.excluded_dungeons.value
    #        if len(remaining_dungeon_options) < num_remaining:
    #            raise RuntimeError("Could not select required bosses to satisfy options set by user")

    # Finish selecting required bosses
    #       required_dungeons.update(self.multiworld.random.sample(list(remaining_dungeon_options), num_remaining))
    #
    #        # Exclude locations which are not in the dungeon of a required boss
    #        banned_dungeons = dungeon_names - required_dungeons
    #        for location_name, _ in LOCATION_TABLE.items():
    #            dungeon_name, _ = split_location_name_by_zone(location_name)
    #            if dungeon_name in banned_dungeons:
    #                self.multiworld.get_location(location_name, self.player).progress_type = LocationProgressType.EXCLUDED

    # Exclude mail related to banned dungeons
    #        if "Forbidden Woods" in banned_dungeons:
    #            self.multiworld.get_location("Mailbox - Letter from Orca", self.player).progress_type = (
    #                LocationProgressType.EXCLUDED
    #            )
    #        if "Forsaken Fortress" in banned_dungeons:
    #            self.multiworld.get_location("Mailbox - Letter from Aryll", self.player).progress_type = (
    #                LocationProgressType.EXCLUDED
    #            )
    #            self.multiworld.get_location("Mailbox - Letter from Tingle", self.player).progress_type = (
    #                LocationProgressType.EXCLUDED
    #            )
    #        if "Earth Temple" in banned_dungeons:
    #            self.multiworld.get_location("Mailbox - Letter from Baito", self.player).progress_type = (
    #                LocationProgressType.EXCLUDED
    #            )

    # Record the item location names for required bosses
    #        possible_boss_item_locations = [loc for loc, data in LOCATION_TABLE.items() if LMFlag.BOSS in data.flags]
    #        self.required_boss_item_locations = [
    #            loc for loc in possible_boss_item_locations if split_location_name_by_zone(loc)[0] in required_dungeons
    #        ]
    #        self.required_dungeons = list(required_dungeons)
    #        self.banned_dungeons = list(banned_dungeons)

    #    def _randomize_entrances(self):
    #        # Copy over the lists of entrances by type
    #        entrances = [
    #            DUNGEON_ENTRANCES.copy(),
    #            MINIBOSS_ENTRANCES.copy(),
    #            BOSS_ENTRANCES.copy(),
    #            SECRET_CAVES_ENTRANCES.copy(),
    #            SECRET_CAVES_INNER_ENTRANCES.copy(),
    #            FAIRY_FOUNTAIN_ENTRANCES.copy(),
    #        ]
    #        exits = [
    #           DUNGEON_EXITS.copy(),
    #   MINIBOSS_EXITS.copy(),
    #   BOSS_EXITS.copy(),
    #   SECRET_CAVES_EXITS.copy(),
    #   SECRET_CAVES_INNER_EXITS.copy(),
    #   FAIRY_FOUNTAIN_EXITS.copy(),
    # ]

    # Retrieve the entrance randomization option
    # options = [
    #   self.options.randomize_dungeon_entrances,
    #   self.options.randomize_miniboss_entrances,
    #   self.options.randomize_boss_entrances,
    #   self.options.randomize_secret_cave_entrances,
    #   self.options.randomize_secret_cave_inner_entrances,
    #   self.options.randomize_fairy_fountain_entrances,
    # ]

    # entrance_exit_pairs: list[tuple[Region, Region]] = []
    #
    # Force miniboss doors to be vanilla in nonrequired dungeons
    # for miniboss_entrance, miniboss_exit in zip(entrances[1], exits[1]):
    #   assert miniboss_entrance.startswith("Miniboss Entrance in ")
    #   dungeon_name = miniboss_entrance[len("Miniboss Entrance in ") :]
    #   if dungeon_name in self.banned_dungeons:
    #       entrances[1].remove(miniboss_entrance)
    #       entrance_region = self.multiworld.get_region(miniboss_entrance, self.player)
    #       exits[1].remove(miniboss_exit)
    #       exit_region = self.multiworld.get_region(miniboss_exit, self.player)
    #       entrance_exit_pairs.append((entrance_region, exit_region))

    # Force boss doors to be vanilla in nonrequired dungeons
    # for boss_entrance, boss_exit in zip(entrances[2], exits[2]):
    #   assert boss_entrance.startswith("Boss Entrance in ")
    #   dungeon_name = boss_entrance[len("Boss Entrance in ") :]
    #   if dungeon_name in self.banned_dungeons:
    #       entrances[2].remove(boss_entrance)
    #       entrance_region = self.multiworld.get_region(boss_entrance, self.player)
    #       exits[2].remove(boss_exit)
    #       exit_region = self.multiworld.get_region(boss_exit, self.player)
    #       entrance_exit_pairs.append((entrance_region, exit_region))
    #
    # if self.options.mix_entrances == "separate_pools":
    #   # Connect entrances to exits of the same type
    #   for option, entrance_group, exit_group in zip(options, entrances, exits):
    #       # If the entrance group is randomized, shuffle their order
    #       if option:
    #           self.multiworld.random.shuffle(entrance_group)
    #           self.multiworld.random.shuffle(exit_group)
    #
    #       for entrance_name, exit_name in zip(entrance_group, exit_group):
    #           entrance_region = self.multiworld.get_region(entrance_name, self.player)
    #           exit_region = self.multiworld.get_region(exit_name, self.player)
    #           entrance_exit_pairs.append((entrance_region, exit_region))
    # elif self.options.mix_entrances == "mix_pools":
    #   # We do a bit of extra work here in order to prevent unreachable "islands" of regions.
    #   # For example, DRC boss door leading to DRC. This will cause generation failures.

    # Gather all the entrances and exits for selected randomization pools
    #   randomized_entrances: list[str] = []
    #   randomized_exits: list[str] = []
    #   non_randomized_exits: list[str] = ["The Great Sea"]
    #   for option, entrance_group, exit_group in zip(options, entrances, exits):
    #       if option:
    #           randomized_entrances += entrance_group
    #           randomized_exits += exit_group
    #       else:
    #           # If not randomized, then just connect the entrance-exit pairs now
    #           for entrance_name, exit_name in zip(entrance_group, exit_group):
    #               non_randomized_exits.append(exit_name)
    #               entrance_region = self.multiworld.get_region(entrance_name, self.player)
    #               exit_region = self.multiworld.get_region(exit_name, self.player)
    #               entrance_exit_pairs.append((entrance_region, exit_region))

    # Build a list of accessible randomized entrances, assuming the player has all items
    #   accessible_entrances: list[str] = []
    #   for exit_name, entrances in ENTRANCE_ACCESSIBILITY.items():
    #       if exit_name in non_randomized_exits:
    #           accessible_entrances += [
    #               entrance_name for entrance_name in entrances if entrance_name in randomized_entrances
    #           ]
    #   non_accessible_entrances: list[str] = [
    #       entrance_name for entrance_name in randomized_entrances if entrance_name not in accessible_entrances
    #   ]

    # Priotize exits that lead to more entrances first
    #   priority_exits: list[str] = []
    #   for exit_name, entrances in ENTRANCE_ACCESSIBILITY.items():
    #       if exit_name == "The Great Sea":
    #           continue
    #       if exit_name in randomized_exits and any(
    #           entrance_name in randomized_entrances for entrance_name in entrances
    #       ):
    #           priority_exits.append(exit_name)

    # Assign each priority exit to an accessible entrance
    #   for exit_name in priority_exits:
    #       # Choose an accessible entrance at random
    #       self.multiworld.random.shuffle(accessible_entrances)
    #       entrance_name = accessible_entrances.pop()
    #
    # Connect the pair
    #       entrance_region = self.multiworld.get_region(entrance_name, self.player)
    #       exit_region = self.multiworld.get_region(exit_name, self.player)
    #       entrance_exit_pairs.append((entrance_region, exit_region))
    #
    #       # Remove the pair from the list of entrance/exits to be connected
    #       randomized_entrances.remove(entrance_name)
    #       randomized_exits.remove(exit_name)
    #
    # Consider entrances in that exit as accessible now
    #       for newly_accessible_entrance in ENTRANCE_ACCESSIBILITY[exit_name]:
    #           if newly_accessible_entrance in non_accessible_entrances:
    #               accessible_entrances.append(newly_accessible_entrance)
    #               non_accessible_entrances.remove(newly_accessible_entrance)
    #
    # With all entrances either assigned or accessible, we should have an equal number of unassigned entrances
    # and exits to pair
    #   assert len(randomized_entrances) == len(randomized_exits)
    #
    # Join the remaining entrance/exits randomly
    #   self.multiworld.random.shuffle(randomized_entrances)
    #   self.multiworld.random.shuffle(randomized_exits)
    #   for entrance_name, exit_name in zip(randomized_entrances, randomized_exits):
    #       entrance_region = self.multiworld.get_region(entrance_name, self.player)
    #       exit_region = self.multiworld.get_region(exit_name, self.player)
    #       entrance_exit_pairs.append((entrance_region, exit_region))
    # else:
    #   raise Exception(f"Invalid entrance randomization option: {self.options.mix_entrances}")
    #
    # return entrance_exit_pairs

    def _set_optional_locations(self):

        # Set the flags for progression location by checking player's settings
        if self.options.plantsanity:
            for location, data in PLANT_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    # if entry.code == 70:     # Placed here for eventual Huge Flower Support
                    #    add_rule(entry,
                    #             lambda state: state.has("Progressive Flower", self.player, 4))
                    # else:
                    for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        if self.options.knocksanity:
            for location, data in FURNITURE_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        if self.options.speedy_spirits:
            for location, data in SPEEDY_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        if self.options.portrait_ghosts:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    if entry.code == 624:
                        add_rule(entry, lambda state: state.has_group("Medal", self.player))
                    elif entry.code == 627:
                        add_rule(entry,
                                 lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
                    else:
                        for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        if self.options.boosanity:
            for location, data in BOO_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Boo Radar", self.player))
                if len(entry.access) != 0:
                    if entry.code == 675:
                        add_rule(entry, lambda state: state.has_group("Medal", self.player))
                    elif entry.code == 679:
                        add_rule(entry,
                                 lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
                    else:
                        for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        else:
            for location, data in BOO_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.code = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                add_rule(entry, lambda state: state.has("Boo Radar", self.player))
                if len(entry.access) != 0:
                    if entry.code == 675:
                        add_rule(entry, lambda state: state.has_group("Medal", self.player))
                    elif entry.code == 679:
                        add_rule(entry,
                                 lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
                    else:
                        for item in entry.access: add_rule(entry, lambda state: state.has(item, self.player))
                region.locations.append(entry)
        if self.options.goal == 1:
            rankcalc = 0
            if self.options.rank_requirement < 3:
                rankcalc = 1
            elif self.options.rank_requirement == 3:
                rankcalc = 2
            elif 3 < self.options.rank_requirement < 5:
                rankcalc = 3
            elif self.options.rank_requirement == 6:
                rankcalc = 4
            else:
                rankcalc = 5
            loc = self.multiworld.get_location("King Boo", self.player)
            add_rule(loc, lambda state: state.has("Gold Diamond", self.player, rankcalc))

    def generate_early(self):
        if self.options.enemizer:
            set_ghost_type(self.multiworld, self.ghost_affected_regions)

        # If sword mode is Start with Hero's Sword, then send the player a starting sword
        if self.options.boo_radar:
            self.options.start_inventory.value["Boo Radar"] = (
                    self.options.start_inventory.value.get("Boo Radar", 0) + 1
            )
        if not self.options.knocksanity:
            self.multiworld.push_precollected(self.create_item("Heart Key"))

        if self.options.good_vacuum == 0:
            self.options.start_inventory.value["Poltergust 4000"] = (
                    self.options.start_inventory.value.get("Poltergust 4000", 0) + 1
            )
        if self.options.boosanity == 0 and self.options.balcony_boo_count > 30:
            self.options.balcony_boo_count = 30

    def create_regions(self):
        # "Menu" is the required starting point
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add all randomizable regions
        for region_name in REGION_LIST:
            if region_name in self.multiworld.regions.region_cache[self.player]:
                continue
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        # Assign each location to their region
        for location, data in BASE_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
            entry = LMLocation(self.player, location, region, data)
            if len(entry.access) != 0:
                for item in entry.access:
                    add_rule(entry, lambda state: state.has(item, self.player))
            if entry.code is None:
                entry.place_locked_item(Item(entry.locked_item, ItemClassification.progression, None, self.player))
            region.locations.append(entry)
        for location, data in ENEMIZER_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
            entry = LMLocation(self.player, location, region, data)
            if len(entry.access) != 0:
                for item in entry.access:
                    add_rule(entry, lambda state: state.has(item, self.player))
            region.locations.append(entry)
        for location, data in CLEAR_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
            entry = LMLocation(self.player, location, region, data)
            if entry.code == 5:
                add_rule(entry, lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
            elif entry.code == 25:
                add_rule(entry, lambda state: state.has_group("Medal", self.player))
            else:
                for item in entry.access:
                    add_rule(entry, lambda state: state.has(item, self.player))
        self._set_optional_locations()
        connect_regions(self.multiworld, self.player)

    def create_item(self, item: str) -> LMItem:
        # TODO: calculate nonprogress items dynamically
        set_non_progress = False

        if item in ALL_ITEMS_TABLE:
            if item == "Gold Diamond":
                if self.options.goal == 1:
                    return LMItem(item, self.player, ITEM_TABLE[item], False)
                else:
                    return LMItem(item, self.player, ITEM_TABLE[item], True)
            else:
                if item in ALL_ITEMS_TABLE:
                    return LMItem(item, self.player, ALL_ITEMS_TABLE[item], set_non_progress)
        raise Exception(f"Invalid item name: {item}")

    def pre_fill(self):  # TODO use for forced early options (AKA Parlor/Heart/2FFHallway Key)
        pass

    #    @classmethod
    #    def stage_pre_fill(cls, multiworld: MultiWorld):
    # Reference: `fill_dungeons_restrictive()` from ALTTP
    #            dungeon_shortnames: dict[str, str] = {
    #            "Dragon Roost Cavern": "DRC",
    #            "Forbidden Woods": "FW",
    #            "Tower of the Gods": "TotG",
    #            "Forsaken Fortress": "FF",
    #            "Earth Temple": "ET",
    #            "Wind Temple": "WT",
    #        }

    #        in_dungeon_items: list[LMItem] = []
    #        own_dungeon_items: set[tuple[int, str]] = set()
    #        for subworld in multiworld.get_game_worlds("The Wind Waker"):
    #            player = subworld.player
    #            if player not in multiworld.groups:
    #                in_dungeon_items += [item for item in subworld.pre_fill_items]
    #                own_dungeon_items |= {(player, item_name) for item_name in subworld.own_dungeon_item_names}

    #        if in_dungeon_items:
    #            locations: list[LMLocation] = [
    #                location
    #                for world in multiworld.get_game_worlds("The Wind Waker")
    #                for location in world._get_dungeon_locations()
    #                if not location.item
    #            ]

    #            if own_dungeon_items:
    #                for location in locations:
    #                    dungeon = location.name.split(" - ")[0]
    #                    orig_rule = location.item_rule
    #                    location.item_rule = lambda item, dungeon=dungeon, orig_rule=orig_rule: (
    #                        not (item.player, item.name) in own_dungeon_items
    #                        or item.name.startswith(dungeon_shortnames[dungeon])
    #                    ) and orig_rule(item)

    #            multiworld.random.shuffle(locations)
    # Dungeon-locked items have to be placed first, to not run out of spaces for dungeon-locked items
    # subsort in the order Big Key, Small Key, Other before placing dungeon items

    #            sort_order = {"BKey": 3, "SKey": 2}
    #            in_dungeon_items.sort(
    #                key=lambda item: sort_order.get(item.type, 1)
    #                + (5 if (item.player, item.name) in own_dungeon_items else 0)
    #            )

    # Construct a partial all_state which contains only the items from get_pre_fill_items,
    # which aren't in_dungeon
    #            in_dungeon_player_ids = {item.player for item in in_dungeon_items}
    #            all_state_base = CollectionState(multiworld)
    #            for item in multiworld.itempool:
    #                multiworld.worlds[item.player].collect(all_state_base, item)
    #            pre_fill_items = []
    #            for player in in_dungeon_player_ids:
    #                pre_fill_items += multiworld.worlds[player].get_pre_fill_items()
    #            for item in in_dungeon_items:
    #                try:
    #                     pre_fill_items.remove(item)
    #                 except ValueError:
    #                     # pre_fill_items should be a subset of in_dungeon_items, but just in case
    #                     pass
    #             for item in pre_fill_items:
    #                 multiworld.worlds[item.player].collect(all_state_base, item)
    #             all_state_base.sweep_for_events()
    #
    #             # Remove completion condition so that minimal-accessibility worlds place keys properly
    #             for player in {item.player for item in in_dungeon_items}:
    #                 if all_state_base.has("Victory", player):
    #                     all_state_base.remove(multiworld.worlds[player].create_item("Victory"))
    #
    #             fill_restrictive(
    #                 multiworld,
    #                 all_state_base,
    #                 locations,
    #                 in_dungeon_items,
    #                 single_player_placement=True,
    #                 lock=True,
    #                 allow_excluded=True,
    #                 name="LM Dungeon Items",
    #             )

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        if not self.options.boosanity:
            for _ in range(35):
                exclude += ["Boo"]
        if self.options.good_vacuum == 2:
            exclude += ["Poltergust 4000"]
        for item, data in ITEM_TABLE.items():
            copies_to_place = data.quantity - exclude.count(item)
            for _ in range(copies_to_place):
                self.itempool.append(self.create_item(item))
        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        n_items = len(self.pre_fill_items) + len(self.itempool)
        n_filler_items = n_locations - n_items

        # Add filler items to the item pool.
        for _ in range(n_filler_items):
            self.itempool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += self.itempool

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice([item_name for item_name in filler_items])

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    # TODO: UPDATE FOR LM
    def generate_output(self, output_directory: str):
        # Output seed name and slot number to seed RNG in randomizer client
        output_data = {
            "Seed": self.multiworld.seed_name,
            "Slot": self.player,
            "Name": self.multiworld.get_player_name(self.player),
            "Options": {},
            "Locations": {},
            "Entrances": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        # Output which item has been placed at each location
        locations = self.multiworld.get_locations(self.player)
        for location in locations:
            if location.address is not None:
                if location.item:
                    item_info = {
                        "player": location.item.player,
                        "name": location.item.name,
                        "game": location.item.game,
                        "classification": location.item.classification.name,
                    }
                else:
                    item_info = {"name": "Nothing", "game": "Luigi's Mansion", "classification": "filler"}
                output_data["Locations"][location.name] = item_info

        # # Output the mapping of entrances to exits
        # entrances = self.multiworld.get_entrances(self.player)
        # for entrance in entrances:
        #     if entrance.parent_region.name in ALL_ENTRANCES:
        #         output_data["Entrances"][entrance.parent_region.name] = entrance.connected_region.name

        # Output the plando details to file
        file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.apLM")
        with open(file_path, "w") as f:
            f.write(yaml.dump(output_data, sort_keys=False))

    # TODO: UPDATE FOR LM IF NEEDED
    def fill_slot_data(self):
        # return {
        #     "progression_dungeons": self.options.progression_dungeons.value,
        #     "progression_tingle_chests": self.options.progression_tingle_chests.value,
        #     "progression_dungeon_secrets": self.options.progression_dungeon_secrets.value,
        #     "progression_puzzle_secret_caves": self.options.progression_puzzle_secret_caves.value,
        #     "progression_combat_secret_caves": self.options.progression_combat_secret_caves.value,
        #     "progression_savage_labyrinth": self.options.progression_savage_labyrinth.value,
        #     "progression_great_fairies": self.options.progression_great_fairies.value,
        #     "progression_short_sidequests": self.options.progression_short_sidequests.value,
        #     "progression_long_sidequests": self.options.progression_long_sidequests.value,
        #     "progression_spoils_trading": self.options.progression_spoils_trading.value,
        #     "progression_minigames": self.options.progression_minigames.value,
        #     "progression_battlesquid": self.options.progression_battlesquid.value,
        #     "progression_free_gifts": self.options.progression_free_gifts.value,
        #     "progression_mail": self.options.progression_mail.value,
        #     "progression_platforms_rafts": self.options.progression_platforms_rafts.value,
        #     "progression_submarines": self.options.progression_submarines.value,
        #     "progression_eye_reef_chests": self.options.progression_eye_reef_chests.value,
        #     "progression_big_octos_gunboats": self.options.progression_big_octos_gunboats.value,
        #     "progression_triforce_charts": self.options.progression_triforce_charts.value,
        #     "progression_treasure_charts": self.options.progression_treasure_charts.value,
        #     "progression_expensive_purchases": self.options.progression_expensive_purchases.value,
        #     "progression_island_puzzles": self.options.progression_island_puzzles.value,
        #     "progression_misc": self.options.progression_misc.value,
        #     "randomize_mapcompass": self.options.randomize_mapcompass.value,
        #     "randomize_smallkeys": self.options.randomize_smallkeys.value,
        #     "randomize_bigkeys": self.options.randomize_bigkeys.value,
        #     "sword_mode": self.options.sword_mode.value,
        #     "required_bosses": self.options.required_bosses.value,
        #     "num_required_bosses": self.options.num_required_bosses.value,
        #     "chest_type_matches_contents": self.options.chest_type_matches_contents.value,
        #     "included_dungeons": self.options.included_dungeons.value,
        #     "excluded_dungeons": self.options.excluded_dungeons.value,
        #     # "trap_chests": self.options.trap_chests.value,
        #     "hero_mode": self.options.hero_mode.value,
        #     "logic_obscurity": self.options.logic_obscurity.value,
        #     "logic_precision": self.options.logic_precision.value,
        #     "enable_tuner_logic": self.options.enable_tuner_logic.value,
        #     "randomize_dungeon_entrances": self.options.randomize_dungeon_entrances.value,
        #     "randomize_secret_cave_entrances": self.options.randomize_secret_cave_entrances.value,
        #     "randomize_miniboss_entrances": self.options.randomize_miniboss_entrances.value,
        #     "randomize_boss_entrances": self.options.randomize_boss_entrances.value,
        #     "randomize_secret_cave_inner_entrances": self.options.randomize_secret_cave_inner_entrances.value,
        #     "randomize_fairy_fountain_entrances": self.options.randomize_fairy_fountain_entrances.value,
        #     "mix_entrances": self.options.mix_entrances.value,
        #     "randomize_enemies": self.options.randomize_enemies.value,
        #     # "randomize_music": self.options.randomize_music.value,
        #     "randomize_starting_island": self.options.randomize_starting_island.value,
        #     "randomize_charts": self.options.randomize_charts.value,
        #     # "hoho_hints": self.options.hoho_hints.value,
        #     # "fishmen_hints": self.options.fishmen_hints.value,
        #     # "korl_hints": self.options.korl_hints.value,
        #     # "num_item_hints": self.options.num_item_hints.value,
        #     # "num_location_hints": self.options.num_location_hints.value,
        #     # "num_barren_hints": self.options.num_barren_hints.value,
        #     # "num_path_hints": self.options.num_path_hints.value,
        #     # "prioritize_remote_hints": self.options.prioritize_remote_hints.value,
        #     "swift_sail": self.options.swift_sail.value,
        #     "instant_text_boxes": self.options.instant_text_boxes.value,
        #     "reveal_full_sea_chart": self.options.reveal_full_sea_chart.value,
        #     "add_shortcut_warps_between_dungeons": self.options.add_shortcut_warps_between_dungeons.value,
        #     "skip_rematch_bosses": self.options.skip_rematch_bosses.value,
        #     "remove_music": self.options.remove_music.value,
        #     "death_link": self.options.death_link.value,
        # }
        pass
