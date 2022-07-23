# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Location


class BumpStikLocation(Location):
    game = "Bumper Stickers"


offset = 595_000

location_table = {
    **{f"{(i * 500) + 250} Points": offset + (i * 2) for i in range(0, 8)},
    **{f"{(i + 1) * 500} Points": offset + (i * 2) + 1 for i in range(0, 8)},
    **{f"Combo Clear {i + 4}": offset + 16 + i for i in range(0, 3)},
    **{f"Chain x{i + 2}": offset + 19 + i for i in range(0, 2)},
    "All Clear": offset + 21,
    **{f"Booster Bumper {i + 1}": offset + 22 + i for i in range(0, 5)},
    "Cleared All Hazards": offset + 27
}
