import unittest
from typing import List, Union

from BaseClasses import MultiWorld
from worlds.stardew_valley.mods.mod_data import all_mods
from worlds.stardew_valley.test import setup_solo_multiworld
from worlds.stardew_valley.test.TestOptions import basic_checks, SVTestCase
from worlds.stardew_valley.items import item_table
from worlds.stardew_valley.locations import location_table
from worlds.stardew_valley.options import Mods
from .option_names import options_to_include


def check_stray_mod_items(chosen_mods: Union[List[str], str], tester: unittest.TestCase, multiworld: MultiWorld):
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


class TestGenerateModsOptions(SVTestCase):

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        mods = list(all_mods)
        num_mods = len(mods)
        for mod1_index in range(0, num_mods):
            for mod2_index in range(mod1_index + 1, num_mods):
                mod1 = mods[mod1_index]
                mod2 = mods[mod2_index]
                mod_pair = (mod1, mod2)
                with self.subTest(f"Mods: {mod_pair}"):
                    multiworld = setup_solo_multiworld({Mods: mod_pair})
                    basic_checks(self, multiworld)
                    check_stray_mod_items(list(mod_pair), self, multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        if self.skip_long_tests:
            return
        num_options = len(options_to_include)
        for option_index in range(0, num_options):
            option = options_to_include[option_index]
            if not option.options:
                continue
            for value in option.options:
                for mod in all_mods:
                    with self.subTest(f"{option.internal_name}: {value}, Mod: {mod}"):
                        multiworld = setup_solo_multiworld({option.internal_name: option.options[value], Mods: mod})
                        basic_checks(self, multiworld)
                        check_stray_mod_items(mod, self, multiworld)