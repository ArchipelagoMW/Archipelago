from itertools import product
from math import sqrt

from BaseClasses import CollectionState
from . import PaintWorld


# There are only 512 (8**3) possible sets of arguments when each of r, g and b can be from 0 inclusive to 7 inclusive,
# so pre-calculate them.
def _make_single_pixel_score_lookup():
    """
    Create a lookup for the maximum possible score for a pixel in the worst case, for r, g and b from 0-7 inclusive.
    """
    rgb = [(2 ** (7 - i) - 1) ** 2 for i in range(8)]
    return {
        t: 1 - sqrt(
            (rgb[t[0]] + rgb[t[1]] + rgb[t[2]]) * 12
        ) / 765
        for t in product(range(8), repeat=3)
    }


SINGLE_PIXEL_SCORE_LOOKUP = _make_single_pixel_score_lookup()


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
    else:
        r = min(r, 7)
        g = min(g, 7)
        b = min(b, 7)
    w = state.count("Progressive Canvas Width", player)
    h = state.count("Progressive Canvas Height", player)
    # This code looks a little messy but it's a mathematical formula derived from the similarity calculations in the
    # client. The first line calculates the maximum score achievable for a single pixel with the current items in the
    # worst possible case. This per-pixel score is then multiplied by the number of pixels currently available (the
    # starting canvas is 400x300) over the total number of pixels with everything unlocked (800x600) to get the
    # total score achievable assuming the worst possible target image. Finally, this is multiplied by the logic percent
    # option which restricts the logic so as to not require pixel perfection.
    return (SINGLE_PIXEL_SCORE_LOOKUP[r, g, b] *
            min(400 + w * world.options.canvas_size_increment, 800) *
            min(300 + h * world.options.canvas_size_increment, 600) *
            world.options.logic_percent / 480000)


def set_completion_rules(world: PaintWorld, player: int) -> None:
    world.multiworld.completion_condition[player] = \
        lambda state: (paint_percent_available(state, world, player) >=
                       min(world.options.logic_percent, world.options.goal_percent))
