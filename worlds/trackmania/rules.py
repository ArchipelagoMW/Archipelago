from typing import TYPE_CHECKING
from .items import get_progression_medal
from .locations import get_series_name
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import TrackmaniaWorld

def set_rules(world: "TrackmaniaWorld"):
    for i in range(1,world.options.series_number):
        set_map_rules(world, i)

    final_medal_requirement :int = world.options.series_number * world.options.medal_requirement
    set_rule(world.multiworld.get_entrance("Victory!", world.player),
             lambda state: state.has(get_progression_medal(world), world.player, final_medal_requirement))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory!", world.player)

def set_map_rules(world: "TrackmaniaWorld", map_index : int):
    entrance_name: str = f"{get_series_name(map_index - 1)} -> {get_series_name(map_index)}"
    medal_requirement: int = map_index * world.options.medal_requirement
    print(f"{entrance_name} {medal_requirement}")
    set_rule(world.multiworld.get_entrance(entrance_name, world.player),
             lambda state: state.has(get_progression_medal(world), world.player, medal_requirement))