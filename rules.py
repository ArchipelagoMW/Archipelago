from ..generic.Rules import add_rule
from BaseClasses import MultiWorld
from .locations import *
from .names import ItemName

def set_rules(world: MultiWorld, player: int):
	add_rule(world.get_location(LocationName.golden_diva), lambda _: True)

	world.completion_condition[player] = lambda state: state.has(ItemName.victory, player)