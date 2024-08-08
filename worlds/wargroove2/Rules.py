from typing import List

from BaseClasses import Region, Location
from .Levels import Wargroove2Level
from worlds.AutoWorld import LogicMixin


class Wargroove2Logic(LogicMixin):
    pass


def set_rules(multiworld, level_list: [Wargroove2Level],
              first_level: Wargroove2Level,
              final_levels: [Wargroove2Level],
              player: int):
    # Level 0
    first_level.define_access_rules(multiworld)

    # Levels 1-28 (Top 28 of the list)
    for i in range(0, 28):
        level_list[i].define_access_rules(multiworld)

    # Final Levels (Top 4 of the list)
    final_levels[0].define_access_rules(multiworld, lambda state: state.has_all({"Final North", "Final Center"}, player))
    final_levels[1].define_access_rules(multiworld, lambda state: state.has_all({"Final East", "Final Center"}, player))
    final_levels[2].define_access_rules(multiworld, lambda state: state.has_all({"Final South", "Final Center"}, player))
    final_levels[3].define_access_rules(multiworld, lambda state: state.has_all({"Final West", "Final Center"}, player))

