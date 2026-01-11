from typing import Callable

from .. import WildAdjustmentData as WildAdjData


adjust_cache: dict[tuple[int, int, int, int], Callable[[int], int]] = {}


def adjust(old_min: int, old_max: int, new_min: int, new_max: int) -> Callable[[int], int]:
    a = (old_min, old_max, new_min, new_max)
    if a not in adjust_cache:
        if old_max == old_min:
            adjust_cache[a] = lambda level: (new_min + new_max) // 2
        else:
            adjust_cache[a] = lambda level: (level - old_min) * (new_max - new_min) // (old_max - old_min) + new_min
    return adjust_cache[a]


adjustments: list[WildAdjData] = [
    WildAdjData(adjust(5, 15, 8, 11), 0, 0, "surfing"),
    WildAdjData(adjust(5, 20, 10, 13), 0, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 8, 11), 0, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 13), 0, 0, "fishing rippling"),

    WildAdjData(adjust(35, 60, 20, 23), 1, 0, "fishing"),
    WildAdjData(adjust(35, 70, 23, 27), 1, 0, "fishing rippling"),

    WildAdjData(adjust(35, 55, 25, 35), 2, 0, "fishing"),
    WildAdjData(adjust(35, 70, 30, 40), 2, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 25, 35), 2, 1, "fishing"),
    WildAdjData(adjust(35, 70, 30, 40), 2, 1, "fishing rippling"),
    WildAdjData(adjust(35, 55, 25, 35), 2, 2, "fishing"),
    WildAdjData(adjust(35, 70, 30, 40), 2, 2, "fishing rippling"),
    WildAdjData(adjust(35, 55, 25, 35), 2, 3, "fishing"),
    WildAdjData(adjust(35, 70, 30, 40), 2, 3, "fishing rippling"),

    WildAdjData(adjust(47, 50, 10, 13), 3, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 10, 13), 4, 0, "dark grass"),

    WildAdjData(adjust(5, 20, 15, 18), 6, 0, "surfing"),
    WildAdjData(adjust(5, 20, 15, 20), 6, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 15, 18), 6, 0, "fishing"),
    WildAdjData(adjust(35, 70, 15, 20), 6, 0, "fishing rippling"),

    WildAdjData(adjust(34, 37, 20, 23), 11, 0, "grass"),
    WildAdjData(adjust(34, 37, 21, 24), 12, 0, "grass"),
    WildAdjData(adjust(34, 37, 22, 25), 13, 0, "grass"),
    WildAdjData(adjust(34, 37, 23, 26), 14, 0, "grass"),

    WildAdjData(adjust(35, 55, 15, 35), 49, 0, "fishing"),
    WildAdjData(adjust(35, 70, 15, 40), 49, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 15, 35), 49, 1, "fishing"),
    WildAdjData(adjust(35, 70, 15, 40), 49, 1, "fishing rippling"),
    WildAdjData(adjust(35, 55, 15, 35), 49, 2, "fishing"),
    WildAdjData(adjust(35, 70, 15, 40), 49, 2, "fishing rippling"),
    WildAdjData(adjust(35, 55, 15, 35), 49, 3, "fishing"),
    WildAdjData(adjust(35, 70, 15, 40), 49, 3, "fishing rippling"),

    WildAdjData(adjust(35, 55, 20, 45), 53, 0, "fishing"),
    WildAdjData(adjust(35, 70, 20, 50), 53, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 20, 45), 58, 0, "fishing"),
    WildAdjData(adjust(35, 70, 20, 50), 58, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 30, 33), 68, 0, "grass"),
    WildAdjData(adjust(57, 60, 34, 37), 68, 0, "dark grass"),
    WildAdjData(adjust(57, 60, 30, 35), 68, 0, "rustling grass"),
    WildAdjData(adjust(47, 50, 31, 34), 69, 0, "grass"),
    WildAdjData(adjust(47, 50, 31, 36), 69, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 25, 35), 69, 0, "surfing"),
    WildAdjData(adjust(25, 70, 25, 40), 69, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 25, 35), 69, 0, "fishing"),
    WildAdjData(adjust(35, 70, 25, 40), 69, 0, "fishing rippling"),
    WildAdjData(adjust(52, 55, 32, 35), 70, 0, "grass"),
    WildAdjData(adjust(62, 65, 36, 39), 70, 0, "dark grass"),
    WildAdjData(adjust(52, 55, 32, 37), 70, 0, "rustling grass"),
    WildAdjData(adjust(57, 60, 33, 36), 71, 0, "grass"),
    WildAdjData(adjust(57, 60, 37, 40), 71, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 25, 35), 71, 0, "surfing"),
    WildAdjData(adjust(25, 70, 25, 40), 71, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 25, 35), 71, 0, "fishing"),
    WildAdjData(adjust(35, 70, 25, 40), 71, 0, "fishing rippling"),

    WildAdjData(adjust(28, 31, 5, 8), 72, 0, "grass"),
    WildAdjData(adjust(28, 31, 6, 9), 72, 0, "rustling grass"),
    WildAdjData(adjust(5, 15, 5, 8), 72, 0, "surfing"),
    WildAdjData(adjust(5, 20, 6, 9), 72, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 5, 8), 72, 0, "fishing"),
    WildAdjData(adjust(35, 70, 6, 9), 72, 0, "fishing rippling"),

    WildAdjData(adjust(25, 55, 26, 29), 73, 0, "surfing"),
    WildAdjData(adjust(25, 70, 26, 30), 73, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 26, 29), 73, 0, "fishing"),
    WildAdjData(adjust(35, 70, 26, 30), 73, 0, "fishing rippling"),
    WildAdjData(adjust(25, 55, 26, 29), 73, 1, "surfing"),
    WildAdjData(adjust(25, 70, 26, 30), 73, 1, "surfing rippling"),
    WildAdjData(adjust(35, 55, 26, 29), 73, 1, "fishing"),
    WildAdjData(adjust(35, 70, 26, 30), 73, 1, "fishing rippling"),
    WildAdjData(adjust(25, 55, 26, 29), 73, 2, "surfing"),
    WildAdjData(adjust(25, 70, 26, 30), 73, 2, "surfing rippling"),
    WildAdjData(adjust(35, 55, 26, 29), 73, 2, "fishing"),
    WildAdjData(adjust(35, 70, 26, 30), 73, 2, "fishing rippling"),
    WildAdjData(adjust(25, 55, 26, 29), 73, 3, "surfing"),
    WildAdjData(adjust(25, 70, 26, 30), 73, 3, "surfing rippling"),
    WildAdjData(adjust(35, 55, 26, 29), 73, 3, "fishing"),
    WildAdjData(adjust(35, 70, 26, 30), 73, 3, "fishing rippling"),

    WildAdjData(adjust(47, 50, 31, 34), 75, 0, "grass"),
    WildAdjData(adjust(57, 60, 31, 39), 75, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 31, 34), 75, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 31, 34), 75, 0, "surfing"),
    WildAdjData(adjust(25, 70, 31, 39), 75, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 31, 34), 75, 0, "fishing"),
    WildAdjData(adjust(35, 70, 31, 39), 75, 0, "fishing rippling"),

    WildAdjData(adjust(32, 35, 8, 12), 77, 0, "dark grass"),
    WildAdjData(adjust(5, 15, 8, 11), 77, 0, "surfing"),
    WildAdjData(adjust(5, 20, 10, 13), 77, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 8, 11), 77, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 13), 77, 0, "fishing rippling"),

    WildAdjData(adjust(5, 15, 8, 11), 79, 0, "surfing"),
    WildAdjData(adjust(5, 20, 10, 13), 79, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 8, 11), 79, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 13), 79, 0, "fishing rippling"),

    WildAdjData(adjust(35, 55, 10, 15), 80, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 20), 80, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 10, 15), 81, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 20), 81, 0, "fishing rippling"),

    WildAdjData(adjust(35, 55, 15, 18), 82, 0, "fishing"),
    WildAdjData(adjust(35, 70, 17, 20), 82, 0, "fishing rippling"),

    WildAdjData(adjust(35, 55, 22, 25), 84, 0, "fishing"),
    WildAdjData(adjust(35, 70, 26, 29), 84, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 22, 25), 84, 1, "fishing"),
    WildAdjData(adjust(35, 70, 26, 29), 84, 1, "fishing rippling"),
    WildAdjData(adjust(35, 55, 22, 25), 84, 2, "fishing"),
    WildAdjData(adjust(35, 70, 26, 29), 84, 2, "fishing rippling"),
    WildAdjData(adjust(35, 55, 22, 25), 84, 3, "fishing"),
    WildAdjData(adjust(35, 70, 26, 29), 84, 3, "fishing rippling"),

    WildAdjData(adjust(35, 55, 30, 33), 93, 0, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 93, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 93, 1, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 93, 1, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 93, 2, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 93, 2, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 93, 3, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 93, 3, "fishing rippling"),

    WildAdjData(adjust(35, 55, 30, 33), 94, 0, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 94, 0, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 94, 1, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 94, 1, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 94, 2, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 94, 2, "fishing rippling"),
    WildAdjData(adjust(35, 55, 30, 33), 94, 3, "fishing"),
    WildAdjData(adjust(35, 70, 34, 37), 94, 3, "fishing rippling"),

    WildAdjData(adjust(47, 50, 33, 36), 96, 0, "grass"),
    WildAdjData(adjust(47, 50, 33, 36), 96, 0, "rustling grass"),
    WildAdjData(adjust(47, 50, 33, 36), 97, 0, "grass"),
    WildAdjData(adjust(47, 50, 33, 36), 97, 0, "rustling grass"),
    WildAdjData(adjust(47, 50, 33, 36), 98, 0, "grass"),
    WildAdjData(adjust(47, 50, 33, 36), 98, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 15, 35), 98, 0, "surfing"),
    WildAdjData(adjust(25, 70, 25, 40), 98, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 15, 35), 98, 0, "fishing"),
    WildAdjData(adjust(35, 70, 25, 40), 98, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 31, 34), 101, 0, "grass"),
    WildAdjData(adjust(57, 60, 31, 39), 101, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 31, 34), 101, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 31, 34), 101, 0, "surfing"),
    WildAdjData(adjust(25, 70, 31, 39), 101, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 31, 34), 101, 0, "fishing"),
    WildAdjData(adjust(35, 70, 31, 39), 101, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 30, 33), 102, 0, "grass"),
    WildAdjData(adjust(57, 60, 34, 37), 102, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 30, 33), 102, 0, "rustling grass"),

    WildAdjData(adjust(47, 50, 26, 29), 103, 0, "grass"),
    WildAdjData(adjust(57, 60, 30, 33), 103, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 26, 29), 103, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 26, 29), 103, 0, "surfing"),
    WildAdjData(adjust(25, 70, 30, 33), 103, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 26, 29), 103, 0, "fishing"),
    WildAdjData(adjust(35, 70, 30, 33), 103, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 22, 25), 104, 0, "grass"),
    WildAdjData(adjust(57, 60, 26, 29), 104, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 22, 25), 104, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 10, 25), 104, 0, "surfing"),
    WildAdjData(adjust(25, 70, 10, 30), 104, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 10, 25), 104, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 30), 104, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 28, 31), 105, 0, "grass"),
    WildAdjData(adjust(57, 60, 32, 35), 105, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 28, 31), 105, 0, "rustling grass"),
    WildAdjData(adjust(25, 55, 15, 30), 105, 0, "surfing"),
    WildAdjData(adjust(25, 70, 15, 35), 105, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 15, 30), 105, 0, "fishing"),
    WildAdjData(adjust(35, 70, 15, 35), 105, 0, "fishing rippling"),

    WildAdjData(adjust(47, 50, 22, 25), 106, 0, "grass"),
    WildAdjData(adjust(57, 60, 26, 29), 106, 0, "dark grass"),
    WildAdjData(adjust(47, 50, 22, 25), 106, 0, "rustling grass"),

    WildAdjData(adjust(35, 55, 5, 20), 108, 0, "fishing"),
    WildAdjData(adjust(35, 70, 5, 20), 108, 0, "fishing rippling"),

    WildAdjData(adjust(28, 32, 8, 11), 109, 0, "grass"),
    WildAdjData(adjust(32, 35, 8, 12), 109, 0, "dark grass"),
    WildAdjData(adjust(28, 31, 10, 13), 109, 0, "rustling grass"),
    WildAdjData(adjust(5, 15, 8, 11), 109, 0, "surfing"),
    WildAdjData(adjust(5, 20, 8, 12), 109, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 8, 13), 109, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 13), 109, 0, "fishing rippling"),

    WildAdjData(adjust(25, 55, 24, 27), 110, 0, "surfing"),
    WildAdjData(adjust(25, 70, 24, 28), 110, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 24, 27), 110, 0, "fishing"),
    WildAdjData(adjust(35, 70, 24, 28), 110, 0, "fishing rippling"),

    WildAdjData(adjust(5, 15, 8, 11), 111, 0, "surfing"),
    WildAdjData(adjust(5, 20, 8, 12), 111, 0, "surfing rippling"),
    WildAdjData(adjust(35, 55, 10, 13), 111, 0, "fishing"),
    WildAdjData(adjust(35, 70, 10, 14), 111, 0, "fishing rippling"),
]
