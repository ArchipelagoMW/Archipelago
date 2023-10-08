from typing import List, Union
import unittest
import random
import sys

from BaseClasses import MultiWorld
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.test import setup_solo_multiworld
from worlds.stardew_valley.test.TestOptions import basic_checks, SVTestBase
from worlds.stardew_valley import items, Group, ItemClassification
from worlds.stardew_valley.regions import RandomizationFlag, create_final_connections, randomize_connections, create_final_regions
from worlds.stardew_valley.items import item_table, items_by_group
from worlds.stardew_valley.locations import location_table
from worlds.stardew_valley.options import stardew_valley_option_classes, Mods, EntranceRandomization, Friendsanity, SeasonRandomization, SpecialOrderLocations, \
    ExcludeGingerIsland, TrapItems

all_mods = frozenset({ModNames.deepwoods, ModNames.tractor, ModNames.big_backpack,
                      ModNames.luck_skill, ModNames.magic, ModNames.socializing_skill, ModNames.archaeology,
                      ModNames.cooking_skill, ModNames.binning_skill, ModNames.juna,
                      ModNames.jasper, ModNames.alec, ModNames.yoba, ModNames.eugene,
                      ModNames.wellwick, ModNames.ginger, ModNames.shiko, ModNames.delores,
                      ModNames.ayeisha, ModNames.riley, ModNames.skull_cavern_elevator})


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
        for mod in all_mods:
            with self.subTest(f"Mod: {mod}"):
                multi_world = setup_solo_multiworld({Mods: mod})
                basic_checks(self, multi_world)
                check_stray_mod_items(mod, self, multi_world)

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        num_mods = len(all_mods)
        for mod1_index in range(0, num_mods):
            for mod2_index in range(mod1_index + 1, num_mods):
                mod1 = all_mods[mod1_index]
                mod2 = all_mods[mod2_index]
                mods = (mod1, mod2)
                with self.subTest(f"Mods: {mods}"):
                    multiworld = setup_solo_multiworld({Mods: mods})
                    basic_checks(self, multiworld)
                    check_stray_mod_items(list(mods), self, multiworld)

    def test_given_mod_names_when_generate_paired_with_entrance_randomizer_then_basic_checks(self):
        for option in EntranceRandomization.options:
            for mod in all_mods:
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
                for mod in all_mods:
                    with self.subTest(f"{option.internal_name}: {value}, Mod: {mod}"):
                        multiworld = setup_solo_multiworld({option.internal_name: option.options[value], Mods: mod})
                        basic_checks(self, multiworld)
                        check_stray_mod_items(mod, self, multiworld)


class TestBaseItemGeneration(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        Mods.internal_name: all_mods
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
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
        Mods.internal_name: all_mods
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

        for option, flag in [(EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
            with self.subTest(option=option, flag=flag):
                seed = random.randrange(sys.maxsize)
                rand = random.Random(seed)
                world_options = {EntranceRandomization.internal_name: option,
                                 ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
                                 Mods.internal_name: all_mods}
                multiworld = setup_solo_multiworld(world_options)
                world = multiworld.worlds[1]
                final_regions = create_final_regions(world.options)
                final_connections = create_final_connections(world.options)

                regions_by_name = {region.name: region for region in final_regions}
                _, randomized_connections = randomize_connections(rand, world.options, regions_by_name)

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
        for value in TrapItems.options:
            if value == "no_traps":
                continue
            world_options = self.allsanity_options_without_mods()
            world_options.update({TrapItems.internal_name: TrapItems.options[value], Mods: "Magic"})
            multi_world = setup_solo_multiworld(world_options)
            trap_items = [item_data.name for item_data in items_by_group[Group.TRAP] if Group.DEPRECATED not in item_data.groups]
            multiworld_items = [item.name for item in multi_world.get_items()]
            for item in trap_items:
                with self.subTest(f"Option: {value}, Item: {item}"):
                    self.assertIn(item, multiworld_items)
