# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Location


class BumpStikLocation(Location):
    game = "Bumper Stickers"


offset = 595_000

location_table = {
    **{f"{(i + 1) * 500} Points": offset + i for i in range(0, 8)},
    **{f"Combo Clear {i + 4}": offset + 8 + i for i in range(0, 3)},
    **{f"Chain x{i + 2}": offset + 11 + i for i in range(0, 2)},
    "All Clear": offset + 13,
    **{f"Booster Bumper {i + 1}": offset + 14 + i for i in range(0, 5)},
    "Cleared All Hazards": offset + 19
}
