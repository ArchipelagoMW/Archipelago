
from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule

def set_rules(world: World):
    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.victory, world.player)