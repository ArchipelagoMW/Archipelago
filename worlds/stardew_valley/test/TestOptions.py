import itertools
import unittest
from random import random
from typing import Dict

from BaseClasses import ItemClassification, MultiWorld
from Options import SpecialRange, OptionSet
from . import setup_solo_multiworld, SVTestBase
from .. import StardewItem, options, items_by_group, Group
from ..locations import locations_by_tag, LocationTags, location_table
from ..options import StardewOption, stardew_valley_option_classes, Mods
from ..strings.goal_names import Goal
from ..strings.season_names import Season
from ..strings.special_order_names import SpecialOrder
from ..strings.tool_names import ToolMaterial, Tool

SEASONS = {Season.spring, Season.summer, Season.fall, Season.winter}
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
        seed = int(random() * pow(10, 18) - 1)
        for option in stardew_valley_option_classes:
            if not option.options:
                continue
            for value in option.options:
                with self.subTest(f"{option.internal_name}: {value} [Seed: {seed}]"):
                    world_options = {option.internal_name: option.options[value]}
                    multiworld = setup_solo_multiworld(world_options, seed)
                    basic_checks(self, multiworld)


class TestGoal(SVTestBase):
    def test_given_goal_when_generate_then_victory_is_in_correct_location(self):
        for goal, location in [("community_center", Goal.community_center),
                               ("grandpa_evaluation", Goal.grandpa_evaluation),
                               ("bottom_of_the_mines", Goal.bottom_of_the_mines),
                               ("cryptic_note", Goal.cryptic_note),
                               ("master_angler", Goal.master_angler),
                               ("complete_collection", Goal.complete_museum),
                               ("full_house", Goal.full_house),
                               ("perfection", Goal.perfection)]:
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
        self.assertEqual(items.count(Season.progressive), 3)


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
        for material, tool in itertools.product(ToolMaterial.tiers.values(),
                                                [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.trash_can]):
            if material == ToolMaterial.basic:
                continue
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
        seed = int(random() * pow(10, 18) - 1)
        island_option = options.ExcludeGingerIsland
        for option in stardew_valley_option_classes:
            if not option.options or option.internal_name == island_option.internal_name:
                continue
            for value in option.options:
                with self.subTest(f"{option.internal_name}: {value} [Seed: {seed}]"):
                    multiworld = setup_solo_multiworld(
                        {island_option.internal_name: island_option.option_true,
                         option.internal_name: option.options[value]}, seed)
                    if multiworld.worlds[self.player].options[island_option.internal_name] != island_option.option_true:
                        continue
                    basic_checks(self, multiworld)
                    check_no_ginger_island(self, multiworld)

    def test_given_island_related_goal_then_override_exclude_ginger_island(self):
        island_goals = [value for value in options.Goal.options if value in ["walnut_hunter", "perfection"]]
        island_option = options.ExcludeGingerIsland
        for goal in island_goals:
            for value in island_option.options:
                with self.subTest(f"Goal: {goal}, {island_option.internal_name}: {value}"):
                    multiworld = setup_solo_multiworld(
                        {options.Goal.internal_name: options.Goal.options[goal],
                            island_option.internal_name: island_option.options[value]})
                    self.assertEqual(multiworld.worlds[self.player].options[island_option.internal_name], island_option.option_false)
                    basic_checks(self, multiworld)


class TestTraps(SVTestBase):
    def test_given_no_traps_when_generate_then_no_trap_in_pool(self):
        world_options = self.allsanity_options_without_mods()
        world_options.update({options.TrapItems.internal_name: options.TrapItems.option_no_traps})
        multi_world = setup_solo_multiworld(world_options)

        trap_items = [item_data.name for item_data in items_by_group[Group.TRAP]]
        multiworld_items = [item.name for item in multi_world.get_items()]

        for item in trap_items:
            with self.subTest(f"{item}"):
                self.assertNotIn(item, multiworld_items)

    def test_given_traps_when_generate_then_all_traps_in_pool(self):
        trap_option = options.TrapItems
        for value in trap_option.options:
            if value == "no_traps":
                continue
            world_options = self.allsanity_options_with_mods()
            world_options.update({options.TrapItems.internal_name: trap_option.options[value]})
            multi_world = setup_solo_multiworld(world_options)
            trap_items = [item_data.name for item_data in items_by_group[Group.TRAP] if Group.DEPRECATED not in item_data.groups and item_data.mod_name is None]
            multiworld_items = [item.name for item in multi_world.get_items()]
            for item in trap_items:
                with self.subTest(f"Option: {value}, Item: {item}"):
                    self.assertIn(item, multiworld_items)


class TestSpecialOrders(SVTestBase):
    def test_given_disabled_then_no_order_in_pool(self):
        world_options = {options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_disabled}
        multi_world = setup_solo_multiworld(world_options)

        locations_in_pool = {location.name for location in multi_world.get_locations() if location.name in location_table}
        for location_name in locations_in_pool:
            location = location_table[location_name]
            self.assertNotIn(LocationTags.SPECIAL_ORDER_BOARD, location.tags)
            self.assertNotIn(LocationTags.SPECIAL_ORDER_QI, location.tags)

    def test_given_board_only_then_no_qi_order_in_pool(self):
        world_options = {options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_only}
        multi_world = setup_solo_multiworld(world_options)

        locations_in_pool = {location.name for location in multi_world.get_locations() if location.name in location_table}
        for location_name in locations_in_pool:
            location = location_table[location_name]
            self.assertNotIn(LocationTags.SPECIAL_ORDER_QI, location.tags)

        for board_location in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
            if board_location.mod_name:
                continue
            self.assertIn(board_location.name, locations_in_pool)

    def test_given_board_and_qi_then_all_orders_in_pool(self):
        world_options = {options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
                         options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_victories}
        multi_world = setup_solo_multiworld(world_options)

        locations_in_pool = {location.name for location in multi_world.get_locations()}
        for qi_location in locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
            if qi_location.mod_name:
                continue
            self.assertIn(qi_location.name, locations_in_pool)

        for board_location in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
            if board_location.mod_name:
                continue
            self.assertIn(board_location.name, locations_in_pool)

    def test_given_board_and_qi_without_arcade_machines_then_lets_play_a_game_not_in_pool(self):
        world_options = {options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
                         options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled}
        multi_world = setup_solo_multiworld(world_options)

        locations_in_pool = {location.name for location in multi_world.get_locations()}
        self.assertNotIn(SpecialOrder.lets_play_a_game, locations_in_pool)
