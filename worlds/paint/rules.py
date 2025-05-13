from math import sqrt

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule
from . import PaintWorld, location_exists_with_options


def paint_percent_available(state: CollectionState, world: PaintWorld, player: int) -> bool:
    if state.paint_percent_stale[player]:
        state.paint_percent_available[player] = calculate_paint_percent_available(state, world, player)
        state.paint_percent_stale[player] = False
    return state.paint_percent_available[player]


def calculate_paint_percent_available(state: CollectionState, world: PaintWorld, player: int) -> float:
    p = state.has("Pick Color", player)
    r = state.count("Progressive Color Depth (Red)", player)
    g = state.count("Progressive Color Depth (Green)", player)
    b = state.count("Progressive Color Depth (Blue)", player)
    if not p:
        r = min(r, 2)
        g = min(g, 2)
        b = min(b, 2)
    w = state.count("Progressive Canvas Width", player)
    h = state.count("Progressive Canvas Height", player)
    return ((1 - ((sqrt(((2 ** (7 - r) - 1) ** 2 + (2 ** (7 - g) - 1) ** 2 + (2 ** (7 - b) - 1) ** 2) * 12)) / 765)) *
            (400 + w * world.options.canvas_size_increment) * (300 + h * world.options.canvas_size_increment) *
            world.options.logic_percent / 480000)


def set_single_rule(world: PaintWorld, player: int, i: int) -> None:
    set_rule(world.multiworld.get_location(f"Similarity: {i/4}%", player),
             lambda state: paint_percent_available(state, world, player) >= i/4)


def set_rules(world: PaintWorld, player: int) -> None:
    for i in range(1, world.options.logic_percent * 4 + 1):
        if location_exists_with_options(world, i):
            set_single_rule(world, player, i)


def set_completion_rules(world: PaintWorld, player: int) -> None:
    world.multiworld.completion_condition[player] = \
        lambda state: (paint_percent_available(state, world, player) >=
                       min(world.options.logic_percent, world.options.goal_percent))
