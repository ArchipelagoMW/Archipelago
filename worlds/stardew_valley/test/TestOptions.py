import itertools
import unittest
from typing import Dict

from BaseClasses import ItemClassification, MultiWorld
from Options import SpecialRange
from . import setup_solo_multiworld, SVTestBase
from .. import StardewItem, options, items_by_group, Group
from ..locations import locations_by_tag, LocationTags
from ..options import StardewOption, stardew_valley_option_classes

SEASONS = {"Spring", "Summer", "Fall", "Winter"}
TOOLS = {"Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can", "Fishing Rod"}


def assert_can_win(tester: SVTestBase, multiworld: MultiWorld):
    for item in multiworld.get_items():
        multiworld.state.collect(item)

    tester.assertTrue(multiworld.find_item("Victory", 1).can_reach(multiworld.state))


def basic_checks(tester: SVTestBase, multiworld: MultiWorld):
    tester.assertIn(StardewItem("Victory", ItemClassification.progression, None, 1), multiworld.get_items())
    assert_can_win(tester, multiworld)
    non_event_locations = [location for location in multiworld.get_locations() if not location.event]
    tester.assertEqual(len(multiworld.itempool), len(non_event_locations))


def check_no_ginger_island(tester: SVTestBase, multiworld: MultiWorld):
    ginger_island_items = [item_data.name for item_data in items_by_group[Group.GINGER_ISLAND]]
    ginger_island_locations = [location_data.name for location_data in locations_by_tag[LocationTags.GINGER_ISLAND]]
    for item in multiworld.get_items():
        tester.assertNotIn(item.name, ginger_island_items)
    for location in multiworld.get_locations():
        tester.assertNotIn(location.name, ginger_island_locations)


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, SpecialRange):
        return option.special_range_names
    elif option.options:
        return option.options
    return {}


class TestGenerateDynamicOptions(SVTestBase):
    def test_given_special_range_when_generate_then_basic_checks(self):
        for option in stardew_valley_option_classes:
            if not issubclass(option, SpecialRange):
                continue
            for value in option.special_range_names:
                with self.subTest(f"{option.internal_name}: {value}"):
                    choices = {option.internal_name: option.special_range_names[value]}
                    multiworld = setup_solo_multiworld(choices)
                    basic_checks(self, multiworld)

    def test_given_choice_when_generate_then_basic_checks(self):
        for option in stardew_valley_option_classes:
            if not option.options:
                continue
            for value in option.options:
                with self.subTest(f"{option.internal_name}: {value}"):
                    choices = {option.internal_name: option.options[value]}
                    multiworld = setup_solo_multiworld(choices)
                    basic_checks(self, multiworld)

    def test_given_option_pair_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        options_to_exclude = ["starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                              "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                              "quick_start", "gifting", "gift_tax"]
        options_to_include = [option_to_include for option_to_include in stardew_valley_option_classes
                              if option_to_include.internal_name not in options_to_exclude]
        num_options = len(options_to_include)
        for option1_index in range(0, num_options):
            for option2_index in range(option1_index + 1, num_options):
                option1 = options_to_include[option1_index]
                option2 = options_to_include[option2_index]
                option1_choices = get_option_choices(option1)
                option2_choices = get_option_choices(option2)
                for key1 in option1_choices:
                    for key2 in option2_choices:
                        with self.subTest(f"{option1.internal_name}: {key1}, {option2.internal_name}: {key2}"):
                            choices = {option1.internal_name: option1_choices[key1],
                                       option2.internal_name: option2_choices[key2]}
                            multiworld = setup_solo_multiworld(choices)
                            basic_checks(self, multiworld)


class TestGoal(SVTestBase):
    def test_given_goal_when_generate_then_victory_is_in_correct_location(self):
        for goal, location in [("community_center", "Complete Community Center"),
                               ("grandpa_evaluation", "Succeed Grandpa's Evaluation"),
                               ("bottom_of_the_mines", "Reach the Bottom of The Mines"),
                               ("cryptic_note", "Complete Quest Cryptic Note"),
                               ("master_angler", "Catch Every Fish")]:
            with self.subTest(msg=f"Goal: {goal}, Location: {location}"):
                world_options = {options.Goal.internal_name: options.Goal.options[goal]}
                multi_world = setup_solo_multiworld(world_options)
                victory = multi_world.find_item("Victory", 1)
                self.assertEqual(victory.name, location)


class TestSeasonRandomization(SVTestBase):
    def test_given_disabled_when_generate_then_all_seasons_are_precollected(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_disabled}
        multi_world = setup_solo_multiworld(world_options)

        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        self.assertTrue(all([season in precollected_items for season in SEASONS]))

    def test_given_randomized_when_generate_then_all_seasons_are_in_the_pool_or_precollected(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized}
        multi_world = setup_solo_multiworld(world_options)
        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        items = {item.name for item in multi_world.get_items()} | precollected_items
        self.assertTrue(all([season in items for season in SEASONS]))
        self.assertEqual(len(SEASONS.intersection(precollected_items)), 1)

    def test_given_progressive_when_generate_then_3_progressive_seasons_are_in_the_pool(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        items = [item.name for item in multi_world.get_items()]
        self.assertEqual(items.count("Progressive Season"), 3)


class TestBackpackProgression(SVTestBase):
    def test_given_vanilla_when_generate_then_no_backpack_in_pool(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla}
        multi_world = setup_solo_multiworld(world_options)

        assert "Progressive Backpack" not in {item.name for item in multi_world.get_items()}

    def test_given_progressive_when_generate_then_progressive_backpack_is_in_pool_two_times(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)
        items = [item.name for item in multi_world.get_items()]
        self.assertEqual(items.count("Progressive Backpack"), 2)

    def test_given_progressive_when_generate_then_backpack_upgrades_are_locations(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        locations = {locations.name for locations in multi_world.get_locations(1)}
        self.assertIn("Large Pack", locations)
        self.assertIn("Deluxe Pack", locations)

    def test_given_early_progressive_when_generate_then_progressive_backpack_is_in_early_pool(self):
        world_options = {
            options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive}
        multi_world = setup_solo_multiworld(world_options)

        self.assertIn("Progressive Backpack", multi_world.early_items[1])


class TestToolProgression(SVTestBase):
    def test_given_vanilla_when_generate_then_no_tool_in_pool(self):
        world_options = {options.ToolProgression.internal_name: options.ToolProgression.option_vanilla}
        multi_world = setup_solo_multiworld(world_options)

        items = {item.name for item in multi_world.get_items()}
        for tool in TOOLS:
            self.assertNotIn(tool, items)

    def test_given_progressive_when_generate_then_progressive_tool_of_each_is_in_pool_four_times(self):
        world_options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        items = [item.name for item in multi_world.get_items()]
        for tool in TOOLS:
            self.assertEqual(items.count("Progressive " + tool), 4)

    def test_given_progressive_when_generate_then_tool_upgrades_are_locations(self):
        world_options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        locations = {locations.name for locations in multi_world.get_locations(1)}
        for material, tool in itertools.product(["Copper", "Iron", "Gold", "Iridium"],
                                                ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]):
            self.assertIn(f"{material} {tool} Upgrade", locations)
        self.assertIn("Purchase Training Rod", locations)
        self.assertIn("Bamboo Pole Cutscene", locations)
        self.assertIn("Purchase Fiberglass Rod", locations)
        self.assertIn("Purchase Iridium Rod", locations)


class TestGenerateAllOptionsWithExcludeGingerIsland(SVTestBase):
    def test_given_special_range_when_generate_exclude_ginger_island(self):
        for option in stardew_valley_option_classes:
            if not issubclass(option,
                              SpecialRange) or option.internal_name == options.ExcludeGingerIsland.internal_name:
                continue
            for value in option.special_range_names:
                with self.subTest(f"{option.internal_name}: {value}"):
                    multiworld = setup_solo_multiworld(
                        {options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
                         option.internal_name: option.special_range_names[value]})
                    check_no_ginger_island(self, multiworld)

    def test_given_choice_when_generate_exclude_ginger_island(self):
        island_option = options.ExcludeGingerIsland
        for option in stardew_valley_option_classes:
            if not option.options or option.internal_name == island_option.internal_name:
                continue
            for value in option.options:
                with self.subTest(f"{option.internal_name}: {value}"):
                    multiworld = setup_solo_multiworld(
                        {island_option.internal_name: island_option.option_true,
                         option.internal_name: option.options[value]})
                    if multiworld.worlds[self.player].options[island_option.internal_name] != island_option.option_true:
                        continue
                    basic_checks(self, multiworld)
                    check_no_ginger_island(self, multiworld)

    def test_given_island_related_goal_then_override_exclude_ginger_island(self):
        island_goals = [value for value in options.Goal.options if value in ["greatest_walnut_hunter", "perfection"]]
        island_option = options.ExcludeGingerIsland
        for goal in island_goals:
            for value in island_option.options:
                with self.subTest(f"Goal: {goal}, {island_option.internal_name}: {value}"):
                    multiworld = setup_solo_multiworld(
                        {options.Goal.internal_name: options.Goal.options[goal],
                            island_option.internal_name: island_option.options[value]})
                    self.assertEqual(multiworld.worlds[self.player].options[island_option.internal_name], island_option.option_false)
                    basic_checks(self, multiworld)
