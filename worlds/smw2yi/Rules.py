import math

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule, set_rule

def set_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.has(ItemName.victory, player)