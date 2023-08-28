from typing import List, Union
import unittest
import random
import sys

from BaseClasses import MultiWorld
from worlds.stardew_valley.test import setup_solo_multiworld
from worlds.stardew_valley.test.TestOptions import basic_checks, SVTestBase
from worlds.stardew_valley import options, locations, items, Group, ItemClassification, StardewOptions
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.regions import RandomizationFlag, create_final_connections, randomize_connections, create_final_regions
from worlds.stardew_valley.items import item_table, items_by_group
from worlds.stardew_valley.locations import location_table, LocationTags
from worlds.stardew_valley.options import stardew_valley_option_classes, Mods, EntranceRandomization

mod_list = ["DeepWoods", "Tractor Mod", "Bigger Backpack",
            "Luck Skill", "Magic", "Socializing Skill", "Archaeology",
            "Cooking Skill", "Binning Skill", "Juna - Roommate NPC",
            "Professor Jasper Thomas", "Alec Revisited", "Custom NPC - Yoba", "Custom NPC Eugene",
            "'Prophet' Wellwick", "Mister Ginger (cat npc)", "Shiko - New Custom NPC", "Delores - Custom NPC",
            "Ayeisha - The Postal Worker (Custom NPC)", "Custom NPC - Riley", "Skull Cavern Elevator"]


def check_stray_mod_items(chosen_mods: Union[List[str], str], tester: SVTestBase, multiworld: MultiWorld):
    if isinstance(chosen_mods, str):
        chosen_mods = [chosen_mods]
    for multiworld_item in multiworld.get_items():
        item = item_table[multiworld_item.name]
        tester.assertTrue(item.mod_name is None or item.mod_name in chosen_mods)
    for multiworld_location in multiworld.get_locations():
        if multiworld_location.event:
            continue
        location = location_table[multiworld_location.name]
        tester.assertTrue(location.mod_name is None or location.mod_name in chosen_mods)


class TestGenerateModsOptions(SVTestBase):

    def test_given_single_mods_when_generate_then_basic_checks(self):
        for mod in mod_list:
            with self.subTest(f"Mod: {mod}"):
                multi_world = setup_solo_multiworld({Mods: mod})
                basic_checks(self, multi_world)
                check_stray_mod_items(mod, self, multi_world)

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        num_mods = len(mod_list)
        for mod1_index in range(0, num_mods):
            for mod2_index in range(mod1_index + 1, num_mods):
                mod1 = mod_list[mod1_index]
                mod2 = mod_list[mod2_index]
                mods = (mod1, mod2)
                with self.subTest(f"Mods: {mods}"):
                    multiworld = setup_solo_multiworld({Mods: mods})
                    basic_checks(self, multiworld)
                    check_stray_mod_items(list(mods), self, multiworld)

    def test_given_mod_names_when_generate_paired_with_entrance_randomizer_then_basic_checks(self):
        for option in EntranceRandomization.options:
            for mod in mod_list:
                with self.subTest(f"entrance_randomization: {option}, Mod: {mod}"):
                    multiworld = setup_solo_multiworld({EntranceRandomization.internal_name: option, Mods: mod})
                    basic_checks(self, multiworld)
                    check_stray_mod_items(mod, self, multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        if self.skip_long_tests:
            return
        for option in stardew_valley_option_classes:
            if not option.options:
                continue
            for value in option.options:
                for mod in mod_list:
                    with self.subTest(f"{option.internal_name}: {value}, Mod: {mod}"):
                        multiworld = setup_solo_multiworld({option.internal_name: option.options[value], Mods: mod})
                        basic_checks(self, multiworld)
                        check_stray_mod_items(mod, self, multiworld)


class TestBaseItemGeneration(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.Mods.internal_name: mod_list
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(footwear.name for footwear in items.items_by_group[Group.FOOTWEAR])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression
                             and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)


class TestNoGingerIslandModItemGeneration(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Mods.internal_name: mod_list
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(footwear.name for footwear in items.items_by_group[Group.FOOTWEAR])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression
                             and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                if Group.GINGER_ISLAND in progression_item.groups:
                    self.assertNotIn(progression_item.name, all_created_items)
                else:
                    self.assertIn(progression_item.name, all_created_items)


class TestModEntranceRando(unittest.TestCase):

    def test_mod_entrance_randomization(self):

        for option, flag in [(options.EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (options.EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (options.EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
            with self.subTest(option=option, flag=flag):
                seed = random.randrange(sys.maxsize)
                rand = random.Random(seed)
                world_options = StardewOptions({options.EntranceRandomization.internal_name: option,
                                                options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
                                                options.Mods.internal_name: mod_list})
                final_regions = create_final_regions(world_options)
                final_connections = create_final_connections(world_options)

                regions_by_name = {region.name: region for region in final_regions}
                _, randomized_connections = randomize_connections(rand, world_options, regions_by_name)

                for connection in final_connections:
                    if flag in connection.flag:
                        connection_in_randomized = connection.name in randomized_connections
                        reverse_in_randomized = connection.reverse in randomized_connections
                        self.assertTrue(connection_in_randomized,
                                      f"Connection {connection.name} should be randomized but it is not in the output. Seed = {seed}")
                        self.assertTrue(reverse_in_randomized,
                                      f"Connection {connection.reverse} should be randomized but it is not in the output. Seed = {seed}")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization. Seed = {seed}")


class TestModTraps(SVTestBase):
    def test_given_traps_when_generate_then_all_traps_in_pool(self):
        trap_option = options.TrapItems
        for value in trap_option.options:
            if value == "no_traps":
                continue
            world_options = self.allsanity_options_without_mods()
            world_options.update({options.TrapItems.internal_name: trap_option.options[value], Mods: "Magic"})
            multi_world = setup_solo_multiworld(world_options)
            trap_items = [item_data.name for item_data in items_by_group[Group.TRAP] if Group.DEPRECATED not in item_data.groups]
            multiworld_items = [item.name for item in multi_world.get_items()]
            for item in trap_items:
                with self.subTest(f"Option: {value}, Item: {item}"):
                    self.assertIn(item, multiworld_items)
