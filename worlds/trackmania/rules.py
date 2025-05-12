from typing import TYPE_CHECKING
from .items import get_progression_medal
from .locations import get_series_name
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import TrackmaniaWorld

def set_rules(world: "TrackmaniaWorld"):
    medal_total: int = world.series_data[0]["MedalTotal"]
    for i in range(1,world.options.series_number):
        set_series_rules(world, i, medal_total)
        medal_total += world.series_data[i]["MedalTotal"]

    final_medal_requirement: int = medal_total

    set_rule(world.multiworld.get_entrance("Victory!", world.player),
             lambda state: state.has(get_progression_medal(world), world.player, final_medal_requirement))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory!", world.player)

def set_series_rules(world: "TrackmaniaWorld", series_index : int, medal_total: int):
    entrance_name: str = f"{get_series_name(series_index - 1)} -> {get_series_name(series_index)}"
    set_rule(world.multiworld.get_entrance(entrance_name, world.player),
             lambda state: state.has(get_progression_medal(world), world.player, medal_total))