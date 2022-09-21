# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Location


class BumpStikLocation(Location):
    game = "Bumper Stickers"


offset = 595_000

level1_locs = [f"{(i + 1) * 250} Points" for i in range(4)] + \
    [f"{(i + 1) * 500} Total Points" for i in range(4)] + \
    ["Combo 5"]

level2_locs = [f"{(i + 1) * 500} Points" for i in range(4)] + \
    [f"{(i + 3) * 1000} Total Points" for i in range(4)] + \
    ["Combo 5"] + ["Chain x2"]

level3_locs = ["99999 Points (dummy goal)"]

level4_locs = ["99999 Points (dummy goal)"]

level5_locs = ["Cleared all Hazards"]

for x, list in enumerate([level1_locs, level2_locs, level3_locs, level4_locs, level5_locs]):
    for y, loc in enumerate(list):
        list[y] = f"Level {x + 1} - {loc}"

extra_locs = [f"Bonus Booster {i+1}" for i in range(5)] + \
    [f"Treasure Bumper {i+1}" for i in range(32)]

all_locs = level1_locs + level2_locs + level3_locs + level4_locs + level5_locs + extra_locs

location_table = {
    loc: offset + i for i, loc in enumerate(all_locs)
}
