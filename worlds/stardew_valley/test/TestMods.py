from typing import List, Union

from BaseClasses import MultiWorld
from . import setup_solo_multiworld
from .TestOptions import basic_checks, SVTestBase
from ..items import item_table
from ..locations import location_table
from ..options import stardew_valley_option_classes, Mods

mod_list = ["DeepWoods", "Tractor Mod", "Bigger Backpack",
            "Luck Skill", "Magic", "Socializing Skill", "Archaeology",
            "Cooking Skill", "Binning Skill", "Juna - Roommate NPC",
            "Professor Jasper Thomas", "Alec Revisited", "Custom NPC - Yoba", "Custom NPC Eugene",
            "'Prophet' Wellwick", "Mister Ginger (cat npc)", "Shiko - New Custom NPC", "Delores - Custom NPC",
            "Ayeisha - The Postal Worker (Custom NPC)"]


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
