from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amoount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "HexcellsInfiniteWorld"):
    player = world.player
    options = world.options
    if(HexcellsInfiniteWorld.options.LevelUnlockType == Options.LevelUnlockType.option_vanilla):
        add_rule(world.multiworld.get_entrance("Level Group 1 -> Level Group 2", player), lambda state: state.has("Gem", player, 6))
        add_rule(world.multiworld.get_entrance("Level Group 2 -> Level Group 3", player), lambda state: state.has("Gem", player, 12))
        add_rule(world.multiworld.get_entrance("Level Group 3 -> Level Group 4", player), lambda state: state.has("Gem", player, 18))
        add_rule(world.multiworld.get_entrance("Level Group 4 -> Level Group 5", player), lambda state: state.has("Gem", player, 24))
        add_rule(world.multiworld.get_entrance("Level Group 5 -> Level Group 6", player), lambda state: state.has("Gem", player, 30))
    
        world.multiworld.completion_condition[player] = lambda state: state.has("Gem", player, 36)
    else:
        world.multiworld.completion_condition[player] = lambda state: state.has_all({
            "1-1","1-2","1-3","1-4","1-5","1-6",
            "2-1","2-2","2-3","2-4","2-5","2-6",
            "3-1","3-2","3-3","3-4","3-5","3-6",
            "4-1","4-2","4-3","4-4","4-5","4-6",
            "5-1","5-2","5-3","5-4","5-5","5-6",
            "6-1","6-2","6-3","6-4","6-5","6-6"},player)
        


