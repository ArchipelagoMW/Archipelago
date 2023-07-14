import itertools
import unittest

from BaseClasses import ItemClassification, MultiWorld
from Options import SpecialRange
from . import setup_solo_multiworld, SVTestBase
from .. import StardewItem, options
from ..options import StardewOption, stardew_valley_option_classes

SEASONS = {"Spring", "Summer", "Fall", "Winter"}
TOOLS = {"Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can", "Fishing Rod"}


def assert_can_win(multiworld: MultiWorld):
    for item in multiworld.get_items():
        multiworld.state.collect(item)

    assert multiworld.find_item("Victory", 1).can_reach(multiworld.state)


def basic_checks(multiworld: MultiWorld):
    assert StardewItem("Victory", ItemClassification.progression, None, 1) in multiworld.get_items()
    assert_can_win(multiworld)
    assert len(multiworld.itempool) == len(
        [location for location in multiworld.get_locations() if not location.event])


class TestGenerateDynamicOptions(SVTestBase):
    def test_given_special_range_when_generate_then_basic_checks(self):
        for option in stardew_valley_option_classes:
            if not issubclass(option, SpecialRange):
                continue
            with self.subTest(msg=option.internal_name):
                for value in option.special_range_names:
                    multiworld = setup_solo_multiworld({option.internal_name: option.special_range_names[value]})
                    basic_checks(multiworld)

    def test_given_choice_when_generate_then_basic_checks(self):
        for option in stardew_valley_option_classes:
            if not option.options:
                continue
            with self.subTest(msg=option.internal_name):
                for value in option.options:
                    multiworld = setup_solo_multiworld({option.internal_name: option.options[value]})
                    basic_checks(multiworld)

    def test_given_option_combination_when_generate_then_basic_checks(self):
        option_combinations = [{options.Goal.internal_name: options.Goal.option_master_angler,
                               options.ToolProgression.internal_name: options.ToolProgression.option_vanilla}]
        ids = ["Master Angler + Vanilla tools"]

        for i in range(0, len(option_combinations)):
            option_combination = option_combinations[i]
            id = ids[i]
            with self.subTest(msg=f"{id}"):
                multi_world = setup_solo_multiworld(option_combination)
                basic_checks(multi_world)


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
                assert victory.name == location


class TestSeasonRandomization(SVTestBase):
    def test_given_disabled_when_generate_then_all_seasons_are_precollected(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_disabled}
        multi_world = setup_solo_multiworld(world_options)

        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        assert all([season in precollected_items for season in SEASONS])

    def test_given_randomized_when_generate_then_all_seasons_are_in_the_pool_or_precollected(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized}
        multi_world = setup_solo_multiworld(world_options)
        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        items = {item.name for item in multi_world.get_items()} | precollected_items
        assert all([season in items for season in SEASONS])
        assert len(SEASONS.intersection(precollected_items)) == 1

    def test_given_progressive_when_generate_then_3_progressive_seasons_are_in_the_pool(self):
        world_options = {options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        items = [item.name for item in multi_world.get_items()]
        assert items.count("Progressive Season") == 3


class TestBackpackProgression(SVTestBase):
    def test_given_vanilla_when_generate_then_no_backpack_in_pool(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla}
        multi_world = setup_solo_multiworld(world_options)

        assert "Progressive Backpack" not in {item.name for item in multi_world.get_items()}

    def test_given_progressive_when_generate_then_progressive_backpack_is_in_pool_two_times(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)
        items = [item.name for item in multi_world.get_items()]
        assert items.count("Progressive Backpack") == 2

    def test_given_progressive_when_generate_then_backpack_upgrades_are_locations(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        locations = {locations.name for locations in multi_world.get_locations(1)}
        assert "Large Pack" in locations
        assert "Deluxe Pack" in locations

    def test_given_early_progressive_when_generate_then_progressive_backpack_is_in_early_pool(self):
        world_options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive}
        multi_world = setup_solo_multiworld(world_options)

        assert "Progressive Backpack" in multi_world.early_items[1]


class TestToolProgression(SVTestBase):
    def test_given_vanilla_when_generate_then_no_tool_in_pool(self):
        world_options = {options.ToolProgression.internal_name: options.ToolProgression.option_vanilla}
        multi_world = setup_solo_multiworld(world_options)

        items = {item.name for item in multi_world.get_items()}
        for tool in TOOLS:
            assert tool not in items

    def test_given_progressive_when_generate_then_progressive_tool_of_each_is_in_pool_four_times(self):
        world_options = {options.ToolProgression.internal_name:options.ToolProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        items = [item.name for item in multi_world.get_items()]
        for tool in TOOLS:
            assert items.count("Progressive " + tool) == 4

    def test_given_progressive_when_generate_then_tool_upgrades_are_locations(self):
        world_options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive}
        multi_world = setup_solo_multiworld(world_options)

        locations = {locations.name for locations in multi_world.get_locations(1)}
        for material, tool in itertools.product(["Copper", "Iron", "Gold", "Iridium"],
                                                ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]):
            assert f"{material} {tool} Upgrade" in locations
        assert "Purchase Training Rod" in locations
        assert "Bamboo Pole Cutscene" in locations
        assert "Purchase Fiberglass Rod" in locations
        assert "Purchase Iridium Rod" in locations
