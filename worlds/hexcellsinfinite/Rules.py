from worlds.generic.Rules import add_rule
from . import Options
from typing import TYPE_CHECKING
from .Items import HEXCELLS_LEVEL_ITEMS

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

# This is where you add rules for items or locations
# These are omega simplified rules
# There are a ton of different ways you can add rules, from amoount of items you need, to optional items
# There's also difficulty options and a bunch of others that aren't in this implementation
# I'd suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "HexcellsInfiniteWorld"):
    player = world.player
    if world.options.LevelUnlockType == Options.LevelUnlockType.option_vanilla :
        add_rule(world.multiworld.get_entrance("Level Group 1 -> Level Group 2", player), lambda state: state.has("Gem", player, 6))
        add_rule(world.multiworld.get_entrance("Level Group 2 -> Level Group 3", player), lambda state: state.has("Gem", player, 12))
        add_rule(world.multiworld.get_entrance("Level Group 3 -> Level Group 4", player), lambda state: state.has("Gem", player, 18))
        add_rule(world.multiworld.get_entrance("Level Group 4 -> Level Group 5", player), lambda state: state.has("Gem", player, 24))
        add_rule(world.multiworld.get_entrance("Level Group 5 -> Level Group 6", player), lambda state: state.has("Gem", player, 30))
    
        world.multiworld.completion_condition[player] = lambda state: state.has("Gem", player, 36)
    else:
        for worldNum in range(1, 7):
            for levelNum in range(1, 7):
                levelName = f"Hexcells {worldNum}-{levelNum}"
                regionName = f"Menu -> {worldNum}-{levelNum}"
                rule = lambda state, lamLevelName=levelName: state.has(lamLevelName, player, 1)
                add_rule(world.get_entrance(regionName), rule)
        world.multiworld.completion_condition[player] = lambda state: state.has_all(HEXCELLS_LEVEL_ITEMS,player)
        