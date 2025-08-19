from math import sqrt

from BaseClasses import CollectionState
from . import PaintWorld


def paint_percent_available(state: CollectionState, world: PaintWorld, player: int) -> bool:
    if state.paint_percent_stale[player]:
        state.paint_percent_available[player] = calculate_paint_percent_available(state, world, player)
        state.paint_percent_stale[player] = False
    return state.paint_percent_available[player]


def calculate_paint_percent_available(state: CollectionState, world: PaintWorld, player: int) -> float:
    p = state.has("Pick Color", player)
    r = min(state.count("Progressive Color Depth (Red)", player), 7)
    g = min(state.count("Progressive Color Depth (Green)", player), 7)
    b = min(state.count("Progressive Color Depth (Blue)", player), 7)
    if not p:
        r = min(r, 2)
        g = min(g, 2)
        b = min(b, 2)
    w = state.count("Progressive Canvas Width", player)
    h = state.count("Progressive Canvas Height", player)
    # This code looks a little messy but it's a mathematical formula derived from the similarity calculations in the
    # client. The first line calculates the maximum score achievable for a single pixel with the current items in the
    # worst possible case. This per-pixel score is then multiplied by the number of pixels currently available (the
    # starting canvas is 400x300) over the total number of pixels with everything unlocked (800x600) to get the
    # total score achievable assuming the worst possible target image. Finally, this is multiplied by the logic percent
    # option which restricts the logic so as to not require pixel perfection.
    return ((1 - ((sqrt(((2 ** (7 - r) - 1) ** 2 + (2 ** (7 - g) - 1) ** 2 + (2 ** (7 - b) - 1) ** 2) * 12)) / 765)) *
            min(400 + w * world.options.canvas_size_increment, 800) *
            min(300 + h * world.options.canvas_size_increment, 600) *
            world.options.logic_percent / 480000)


def set_completion_rules(world: PaintWorld, player: int) -> None:
    world.multiworld.completion_condition[player] = \
        lambda state: (paint_percent_available(state, world, player) >=
                       min(world.options.logic_percent, world.options.goal_percent))
