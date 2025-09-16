from worlds.generic.Rules import add_rule
from .options import LevelUnlockType
from typing import TYPE_CHECKING
from .items import HEXCELLS_LEVEL_ITEMS

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

def set_rules(world: "HexcellsInfiniteWorld"):
    player = world.player
    if world.options.LevelUnlockType == LevelUnlockType.option_vanilla :
        add_rule(world.get_entrance("Level Group 1 -> Level Group 2"), lambda state: state.has("Gem", player, 6))
        add_rule(world.get_entrance("Level Group 2 -> Level Group 3"), lambda state: state.has("Gem", player, 12))
        add_rule(world.get_entrance("Level Group 3 -> Level Group 4"), lambda state: state.has("Gem", player, 18))
        add_rule(world.get_entrance("Level Group 4 -> Level Group 5"), lambda state: state.has("Gem", player, 24))
        add_rule(world.get_entrance("Level Group 5 -> Level Group 6"), lambda state: state.has("Gem", player, 30))
    
        world.multiworld.completion_condition[player] = lambda state: state.has("Gem", player, 36)
    else:
        for worldNum in range(1, 7):
            for levelNum in range(1, 7):
                levelName = f"Hexcells {worldNum}-{levelNum}"
                regionName = f"Menu -> {worldNum}-{levelNum}"
                rule = lambda state, lamLevelName=levelName: state.has(lamLevelName, player, 1)
                add_rule(world.get_entrance(regionName), rule)
        world.multiworld.completion_condition[player] = lambda state: state.has_all(HEXCELLS_LEVEL_ITEMS,player)
