from unittest import TestCase

from BaseClasses import MultiWorld
from .option_assert import get_stardew_options
from ... import options, ExcludeGingerIsland


def is_goal(multiworld: MultiWorld, goal: int) -> bool:
    return get_stardew_options(multiworld).goal.value == goal


def is_bottom_mines(multiworld: MultiWorld) -> bool:
    return is_goal(multiworld, options.Goal.option_bottom_of_the_mines)


def is_not_bottom_mines(multiworld: MultiWorld) -> bool:
    return not is_bottom_mines(multiworld)


def is_walnut_hunter(multiworld: MultiWorld) -> bool:
    return is_goal(multiworld, options.Goal.option_greatest_walnut_hunter)


def is_not_walnut_hunter(multiworld: MultiWorld) -> bool:
    return not is_walnut_hunter(multiworld)


def is_perfection(multiworld: MultiWorld) -> bool:
    return is_goal(multiworld, options.Goal.option_perfection)


def is_not_perfection(multiworld: MultiWorld) -> bool:
    return not is_perfection(multiworld)


class GoalAssertMixin(TestCase):

    def assert_ginger_island_is_included(self, multiworld: MultiWorld):
        self.assertEqual(get_stardew_options(multiworld).exclude_ginger_island, ExcludeGingerIsland.option_false)

    def assert_walnut_hunter_world_is_valid(self, multiworld: MultiWorld):
        if is_not_walnut_hunter(multiworld):
            return

        self.assert_ginger_island_is_included(multiworld)

    def assert_perfection_world_is_valid(self, multiworld: MultiWorld):
        if is_not_perfection(multiworld):
            return

        self.assert_ginger_island_is_included(multiworld)

    def assert_goal_world_is_valid(self, multiworld: MultiWorld):
        self.assert_walnut_hunter_world_is_valid(multiworld)
        self.assert_perfection_world_is_valid(multiworld)
