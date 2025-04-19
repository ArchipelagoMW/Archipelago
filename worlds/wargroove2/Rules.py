from typing import TYPE_CHECKING
from .Levels import first_level
if TYPE_CHECKING:
    from . import Wargroove2World


def set_rules(world: "Wargroove2World") -> None:
    level_list = world.level_list
    final_levels = world.final_levels
    player = world.player

    # Level 0
    first_level.define_access_rules(world, player)

    # Levels 1-28 (Top 28 of the list)
    for i in range(0, 28):
        level_list[i].define_access_rules(world, player)

    # Final Levels (Top 4 of the list)
    final_levels[0].define_access_rules(world, player,
                                        lambda state: state.has_all(["Final North", "Final Center"], player))
    final_levels[1].define_access_rules(world, player,
                                        lambda state: state.has_all(["Final East", "Final Center"], player))
    final_levels[2].define_access_rules(world, player,
                                        lambda state: state.has_all(["Final South", "Final Center"], player))
    final_levels[3].define_access_rules(world, player,
                                        lambda state: state.has_all(["Final West", "Final Center"], player))
