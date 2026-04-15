from itertools import product
from math import sqrt
from typing import TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import PaintWorld


# There are only 512 (8**3) possible sets of arguments when each of r, g and b can be from 0 inclusive to 7 inclusive,
# so pre-calculate them.
def _make_single_pixel_score_lookup():
    """
    Create a lookup for the maximum possible score for a pixel in the worst case, for r, g and b color depth from 0-7
    inclusive.
    """
    # The color depth calculation is the same for r, g and b, so can be calculated once for each possible input value.
    color_depth = {i: (2 ** (7 - i) - 1) ** 2 for i in range(8)}
    return {
        (r, g, b): 1 - sqrt(
            (color_depth[r] + color_depth[g] + color_depth[b]) * 12
        ) / 765
        for r, g, b in product(range(8), repeat=3)
    }


SINGLE_PIXEL_SCORE_LOOKUP = _make_single_pixel_score_lookup()


def paint_percent_available(state: CollectionState, world: "PaintWorld", player: int) -> bool:
    if state.paint_percent_stale[player]:
        state.paint_percent_available[player] = calculate_paint_percent_available(state, world, player)
        state.paint_percent_stale[player] = False
    return state.paint_percent_available[player]


def calculate_paint_percent_available(state: CollectionState, world: "PaintWorld", player: int) -> float:
    p = state.has("Pick Color", player)
    r = state.count("Progressive Color Depth (Red)", player)
    g = state.count("Progressive Color Depth (Green)", player)
    b = state.count("Progressive Color Depth (Blue)", player)
    if not p:
        r = min(r, 2)
        g = min(g, 2)
        b = min(b, 2)
    else:
        r = min(r, 7)
        g = min(g, 7)
        b = min(b, 7)
    w = state.count("Progressive Canvas Width", player)
    h = state.count("Progressive Canvas Height", player)
    # This code calculates the total similarity in logic using the formula:
    # (expected score per pixel) * (pixels currently available) * (logic percent from options) / (total pixel count)
    # The expected score and logic percent per pixel are calculated elsewhere for efficiency.
    return (SINGLE_PIXEL_SCORE_LOOKUP[r, g, b] *
            min(world.final_width // 2 + w * world.options.canvas_width_increment.value, world.final_width) *
            min(world.final_height // 2 + h * world.options.canvas_height_increment.value, world.final_height) *
            world.per_pixel_logic_percent)


def set_completion_rules(world: "PaintWorld", player: int) -> None:
    goal_percent = min(world.options.logic_percent.value, world.options.goal_percent.value)
    world.multiworld.completion_condition[player] = \
        lambda state: paint_percent_available(state, world, player) >= goal_percent
