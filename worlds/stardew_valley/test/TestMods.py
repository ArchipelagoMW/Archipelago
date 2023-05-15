from worlds.stardew_valley.test import setup_solo_multiworld
from worlds.stardew_valley.test.TestOptions import basic_checks, SVTestBase
from worlds.stardew_valley.options import stardew_valley_option_classes, Mods

mod_list = ["DeepWoods", "Tractor Mod", "Bigger Backpack",
            "Luck Skill", "Magic", "Socializing Skill", "Archaeology",
            "Cooking Skill", "Binning Skill", "Juna - Roommate NPC",
            "Professor Jasper Thomas", "Alec Revisited", "Custom NPC - Yoba", "Custom NPC Eugene",
            "'Prophet' Wellwick", "Mister Ginger (cat npc)", "Shiko - New Custom NPC", "Delores - Custom NPC",
            "Ayeisha - The Postal Worker (Custom NPC)"]


# Stealing from OptionSet in order to actually use it for tests.


class TestGenerateModsOptions(SVTestBase):

    def test_given_mod_names_when_generate_then_basic_checks(self):
        for mod in mod_list:
            multi_world = setup_solo_multiworld({Mods: mod})
            basic_checks(self, multi_world)

    def test_given_mod_names_when_generate_in_pairs_then_basic_checks(self):
        num_options = len(mod_list)
        for option1_index in range(0, num_options):
            for option2_index in range(option1_index + 1, num_options):
                option1 = mod_list[option1_index]
                option2 = mod_list[option2_index]
                multiworld = setup_solo_multiworld({Mods: (option1, option2)})
                basic_checks(self, multiworld)

    def test_given_mod_names_when_generate_paired_with_base_then_basic_checks(self):
        for option in stardew_valley_option_classes:
            if not option.options:
                continue
            with self.subTest(msg=option.internal_name):
                for value in option.options:
                    for mod in mod_list:
                        multi_world = setup_solo_multiworld({option.internal_name: option.options[value], Mods: mod})
                        basic_checks(self, multi_world)
