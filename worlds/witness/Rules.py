from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class WitnessLogic(LogicMixin):
    def _witness_has_lasers(self, player: int, amount: int) -> bool:    
        lasers = 0
        
        lasers += int(self.can_reach("Symmetry Island Laser", "Location", player))
        lasers += int(self.can_reach("Desert Laser", "Location", player))
        lasers += int(self.can_reach("Town Laser", "Location", player))
        lasers += int(self.can_reach("Quarry Laser", "Location", player))
        lasers += int(self.can_reach("Shadows Laser", "Location", player))
        lasers += int(self.can_reach("Keep Laser Hedges", "Location", player) and self.can_reach("Keep Laser Pressure Plates", "Location", player))
        lasers += int(self.can_reach("Jungle Laser", "Location", player))
        lasers += int(self.can_reach("Swamp Laser", "Location", player))
        lasers += int(self.can_reach("Treehouse Laser", "Location", player))
        lasers += int(self.can_reach("Bunker Laser", "Location", player))
        lasers += int(self.can_reach("Monastery Laser", "Location", player))
        
        
        return lasers >= amount

def makeLambda(checkHex, player):
    from .FullLogic import can_solve_panel
    return lambda state: can_solve_panel(checkHex, state, player)

def set_rules(world: MultiWorld, player: int):
    from .FullLogic import checksByName, checksByHex, can_solve_panel
    from .Locations import location_table, event_location_table
    
    for location in location_table:
        real_location = location
    
        if location in event_location_table:
            real_location = location[:-6]

        panel = checksByName[real_location]
        checkHex = panel["checkHex"]

        rule = makeLambda(checkHex, player)

        set_rule(world.get_location(location, player), rule)

    if world.logic[player] != 'nologic':
        world.completion_condition[player] = lambda state: state.has('Victory', player)
        
    