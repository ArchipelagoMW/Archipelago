import typing

from BaseClasses import CollectionRule
from worlds.generic.Rules import add_rule, forbid_item

from .Data import difficulty_lambda, level_locations, obelisks, boss_regions, excluded_levels, spawner_trap_ids, \
    difficulty_lambda_no_portal
from .Items import items_by_id
from .Locations import get_locations_by_tags
from .Options import Goal

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def set_rules(world: "GauntletLegendsWorld"):
    for location in get_locations_by_tags("no_obelisks") + (get_locations_by_tags("obelisk") if world.options.obelisks else []):
        for item in obelisks:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item, world.player)

    for location in get_locations_by_tags("no_spawner"):
        for item in spawner_trap_ids:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), items_by_id[item].item_name, world.player)

    if not world.options.instant_max:
        for level_id, locations in level_locations.items():
            for location in locations:
                if location.difficulty > 1:
                    if location.name not in world.disabled_locations:
                        if location.name not in world.disabled_locations:
                            level_id_ = level_id >> 4
                            difficulty = location.difficulty - 1
                            if world.options.portals:
                                expected_count = difficulty_lambda[level_id_][difficulty] - (
                                            len(world.excluded_regions) * 4)
                            else:
                                expected_count = difficulty_lambda_no_portal[level_id_][difficulty] - (
                                        len(world.excluded_regions) * 4)
                            expected_count = max(expected_count, 0)
                            add_rule(
                                world.get_location(location.name),
                                lambda state, expected_count_=expected_count: state.has("progression", world.player,
                                                                                        expected_count)
                            )


def goal_conditions(world: "GauntletLegendsWorld") -> CollectionRule:
    if world.options.goal == Goal.option_defeat_skorne:
        return lambda state: state.can_reach("Gates of the Underworld", "Region", world.player)

    eligible_boss_regions = [
        boss for boss in boss_regions
        if boss not in [
            level for region, levels in excluded_levels.items()
            if region in world.excluded_regions for level in levels
        ]
    ]
    needed_boss_count = world.options.boss_goal_count.value

    return lambda state: sum(state.can_reach_region(boss, world.player) for boss in eligible_boss_regions) >= needed_boss_count
