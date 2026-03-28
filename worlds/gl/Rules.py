import typing

from worlds.generic.Rules import add_rule, forbid_item

from .Data import difficulty_lambda, level_locations, obelisks, boss_regions, excluded_levels
from .Locations import get_locations_by_tags
from .Options import Goal

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld

def set_rules(world: "GauntletLegendsWorld"):
    for location in get_locations_by_tags("no_obelisks") + (get_locations_by_tags("obelisk") if world.options.obelisks else []):
        for item in obelisks:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item, world.player)

    if not world.options.instant_max:
        for level_id, locations in level_locations.items():
            for location in locations:
                if location.difficulty > 1:
                    if location.name not in world.disabled_locations:
                        add_rule(
                            world.get_location(location.name),
                            lambda state, level_id_=level_id >> 4, difficulty=location.difficulty - 1:
                            state.has("progression", world.player, max(difficulty_lambda[level_id_][difficulty] - (len(world.excluded_regions) * 4), 0))
                            )

def goal_conditions(state, world: "GauntletLegendsWorld") -> bool:
    return state.can_reach("Gates of the Underworld", "Region", world.player) \
                            if world.options.goal == Goal.option_defeat_skorne else \
                            (sum(state.can_reach(boss, "Region", world.player)
                                for boss in boss_regions if boss not in
                                [level for region, levels in excluded_levels.items() if region in world.excluded_regions for level in levels])
                                >= world.options.boss_goal_count.value)
