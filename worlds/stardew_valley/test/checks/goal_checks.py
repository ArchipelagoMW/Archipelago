from BaseClasses import MultiWorld
from .option_checks import is_setting, assert_is_setting
from ... import options
from .. import SVTestBase


def is_goal(multiworld: MultiWorld, goal: int) -> bool:
    return is_setting(multiworld, options.Goal.internal_name, goal)


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


def assert_ginger_island_is_included(tester: SVTestBase, multiworld: MultiWorld):
    assert_is_setting(tester, multiworld, options.ExcludeGingerIsland.internal_name, options.ExcludeGingerIsland.option_false)


def assert_walnut_hunter_world_is_valid(tester: SVTestBase, multiworld: MultiWorld):
    if is_not_walnut_hunter(multiworld):
        return

    assert_ginger_island_is_included(tester, multiworld)


def assert_perfection_world_is_valid(tester: SVTestBase, multiworld: MultiWorld):
    if is_not_perfection(multiworld):
        return

    assert_ginger_island_is_included(tester, multiworld)


def assert_goal_world_is_valid(tester: SVTestBase, multiworld: MultiWorld):
    assert_walnut_hunter_world_is_valid(tester, multiworld)
    assert_perfection_world_is_valid(tester, multiworld)
