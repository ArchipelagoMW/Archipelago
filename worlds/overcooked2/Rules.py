from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

class Overcooked2Logic(LogicMixin):
    # Defs here

    def rule(self, player: int):
        return True
    
def set_rules(world: MultiWorld, player: int):
    def reachable_locations(state):
        return [location for location in world.get_locations() if location.can_reach(state)]


