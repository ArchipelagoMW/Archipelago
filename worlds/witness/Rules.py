from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class WitnessLogic(LogicMixin):
    def _witness_has_lasers(self, player: int, amount: int) -> bool:
        lasers = 0
        
        lasers += int(self._witness_can_beat_symmetry_laser(player))
        lasers += int(self._witness_can_beat_desert_laser(player))
        lasers += int(self._witness_can_beat_shadows_laser(player))
        lasers += int(self._witness_can_beat_quarry_laser(player))
        lasers += int(self._witness_can_beat_keep_laser(player))
        lasers += int(self._witness_can_beat_monastery_laser(player))
        lasers += int(self._witness_can_beat_jungle_laser(player))
        lasers += int(self._witness_can_beat_town_laser(player))
        lasers += int(self._witness_can_beat_bunker_laser(player))
        lasers += int(self._witness_can_beat_treehouse_laser(player))
        lasers += int(self._witness_can_beat_swamp_laser(player))
        
        return lasers >= amount

    def _witness_can_beat_symmetry_laser(self, player: int) -> bool:
        return self.has('Symmetry Island Door 1', player) and self.has('Symmetry Island Door 2', player)
        
    def _witness_can_beat_desert_laser(self, player: int) -> bool:
        return self.has('Desert Surface Door', player) and self.has('Desert Pond Exit Door', player)
        
    def _witness_can_beat_shadows_laser(self, player: int) -> bool:
        return self.has('Shadows Outer Door Control', player)
        
    def _witness_can_beat_quarry_laser(self, player: int) -> bool:
        return self.has('Mill Entry Door Left', player) and (self.has('Shadows Outer Door Control', player) or self.has('Quarry Entry Gate 1', player))

    def _witness_can_beat_keep_laser(self, player: int) -> bool:
        return True
        
    def _witness_can_beat_monastery_laser(self, player: int) -> bool:
        return self.has('Monastery Left Door', player) and self.has('Monastery Right Door', player)
        
    def _witness_can_beat_jungle_laser(self, player: int) -> bool:
        return self.has('Jungle Pop-up Wall', player)
        
    def _witness_can_beat_town_laser(self, player: int) -> bool:
        #this might need some more logic... think about it later :)
        return self.has('Town Yellow Door', player) and self.has('Town Church Stars', player)
        
    def _witness_can_beat_bunker_laser(self, player: int) -> bool:
        return self.has('Bunker Entry Door', player)
        
    def _witness_can_beat_treehouse_laser(self, player: int) -> bool:
        return self.has('Boat Access', player) and self.has('Treehouse Doors 1&2', player) and self.has('Treehouse Door 3', player) and self.has('Treehouse Exterior Door Control', player)
        
    def _witness_can_beat_swamp_laser(self, player: int) -> bool:
        return self.has('Swamp Entry', player)

def set_rules(world: MultiWorld, player: int):
    if world.logic[player] != 'nologic':
        world.completion_condition[player] = lambda state: state.has('Victory', player)
        
    # Tutorial Checks
    set_rule(world.get_location("Tutorial Gate Open", player), lambda state: True)
    set_rule(world.get_location("Outside Tutorial Dots Tutorial 5", player), lambda state: True)
    set_rule(world.get_location("Outside Tutorial Stones Tutorial 9", player), lambda state: True)
    set_rule(world.get_location("Tutorial Patio floor", player), lambda state: True)
    set_rule(world.get_location("Orchard Apple Tree 5", player), lambda state: True)
    
    # Symmetry Checks
    set_rule(world.get_location("Glass Factory Vertical Symmetry 4", player), lambda state: state.has('Glass Factory Entry', player))
    set_rule(world.get_location("Glass Factory Rotational Symmetry 3", player), lambda state: state.has('Glass Factory Entry', player))
    set_rule(world.get_location("Glass Factory Melting 3", player), lambda state: state.has('Glass Factory Entry', player))
    
    set_rule(world.get_location("Symmetry Island Black Dots 5", player), lambda state: state.has('Symmetry Island Door 1', player))
    set_rule(world.get_location("Symmetry Island Colored Dots 6", player), lambda state: state.has('Symmetry Island Door 1', player))
    set_rule(world.get_location("Symmetry Island Fading Lines 7", player), lambda state: state.has('Symmetry Island Door 1', player))
    set_rule(world.get_location("Symmetry Island Transparent 5", player), lambda state: state.has('Symmetry Island Door 1', player))
    set_rule(world.get_location("Symmetry Island Laser Yellow 3", player), lambda state: state.has('Symmetry Island Door 1', player) and state.has('Symmetry Island Door 2', player))
    set_rule(world.get_location("Symmetry Island Laser Blue 3", player), lambda state: state.has('Symmetry Island Door 1', player) and state.has('Symmetry Island Door 2', player))
    set_rule(world.get_location("Symmetry Laser", player), lambda state: state.has('Symmetry Island Door 1', player) and state.has('Symmetry Island Door 2', player))
    
    # Desert Checks
    set_rule(world.get_location("Desert Surface 8", player), lambda state: True)
    set_rule(world.get_location("Desert Light 3", player), lambda state: state.has('Desert Surface Door', player))
    set_rule(world.get_location("Desert Pond 5", player), lambda state: state.has('Desert Surface Door', player))
    set_rule(world.get_location("Desert Flood 5", player), lambda state: state._witness_can_beat_desert_laser(player))
    set_rule(world.get_location("Desert Laser", player), lambda state: state._witness_can_beat_desert_laser(player))
    
    # Quarry Checks
    set_rule(world.get_location("Mill Lower Row 6", player), lambda state: state.has('Mill Entry Door Left', player) and (state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player)))
    set_rule(world.get_location("Mill Upper Row 8", player), lambda state: state.has('Mill Entry Door Left', player) and (state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player)))
    set_rule(world.get_location("Mill Control Room 2", player), lambda state: state.has('Mill Entry Door Left', player) and (state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player)))
    
    set_rule(world.get_location("Boathouse Erasers and Shapers 5", player), lambda state: state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player))
    set_rule(world.get_location("Boathouse Erasers and Stars 7", player), lambda state: state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player))
    set_rule(world.get_location("Boathouse Erasers Shapers and Stars 5", player), lambda state: state.has('Shadows Outer Door Control', player) or state.has('Quarry Entry Gate 1', player))
    
    #Treehouse Checks
    set_rule(world.get_location("Treehouse Yellow 9", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player))
    set_rule(world.get_location("Treehouse First Purple 5", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player) and state.has('Treehouse Door 3', player))
    set_rule(world.get_location("Treehouse Second Purple 7", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player) and state.has('Treehouse Door 3', player))
    set_rule(world.get_location("Treehouse Left Orange 15", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player) and state.has('Treehouse Door 3', player))
    set_rule(world.get_location("Treehouse Right Orange 12", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player) and state.has('Treehouse Door 3', player))
    set_rule(world.get_location("Treehouse Green 7", player), lambda state: state.has('Boat Access', player) and state.has('Treehouse Doors 1&2', player) and state.has('Treehouse Door 3', player))
    set_rule(world.get_location("Treehouse Laser", player), lambda state: state._witness_can_beat_treehouse_laser(player))
    
    #Shadows Checks
    set_rule(world.get_location("Shadows Tutorial 8", player), lambda state: state.has('Shadows Outer Door Control', player))
    set_rule(world.get_location("Shadows Avoid 8", player), lambda state: state.has('Shadows Outer Door Control', player))
    set_rule(world.get_location("Shadows Follow 5", player), lambda state: state.has('Shadows Outer Door Control', player))
    set_rule(world.get_location("Shadows Laser", player), lambda state: state.has('Shadows Outer Door Control', player)) 

    #Monastery Checks
    set_rule(world.get_location("Monastery Exterior 3", player), lambda state: state._witness_can_beat_monastery_laser(player))
    set_rule(world.get_location("Monastery Interior 4", player), lambda state: state._witness_can_beat_monastery_laser(player))
    set_rule(world.get_location("Monastery Laser", player), lambda state: state._witness_can_beat_monastery_laser(player))
    
    #Keep Checks
    set_rule(world.get_location("Keep Hedges 4", player), lambda state: True)
    set_rule(world.get_location("Keep Blue Pressure Plates", player), lambda state: True)
    set_rule(world.get_location("Keep Front Laser", player), lambda state: True)
    set_rule(world.get_location("Keep Back Laser", player), lambda state: True)    
    
    #Town Checks
    set_rule(world.get_location("Town Eraser", player), lambda state: True)
    set_rule(world.get_location("Town Blue 5", player), lambda state: True)
    set_rule(world.get_location("Town Red Hexagonal", player), lambda state: True)
    set_rule(world.get_location("Town Lattice", player), lambda state: state._witness_can_beat_town_laser(player))    
    set_rule(world.get_location("Town Laser", player), lambda state: True)    
    
    #Swamp Checks
    #This might need some more fiddling too? I'm not sure
    set_rule(world.get_location("Swamp Tutorial 6", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Tutorial 14", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Red 4", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Discontinuous 4", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Rotation Tutorial 4", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Rotation Advanced 4", player), lambda state: state.has('Swamp Entry', player))
    set_rule(world.get_location("Swamp Blue Underwater 5", player), lambda state: state.has('Swamp Entry', player)) 
    set_rule(world.get_location("Swamp Teal Underwater 5", player), lambda state: state.has('Swamp Entry', player))        
    set_rule(world.get_location("Swamp Red Underwater 4", player), lambda state: state.has('Swamp Entry', player))  
    set_rule(world.get_location("Swamp Purple Tetris", player), lambda state: state.has('Swamp Entry', player)) 
    set_rule(world.get_location("Swamp Laser", player), lambda state: state.has('Swamp Entry', player))     
    
    #Bunker Checks
    set_rule(world.get_location("Swamp Tutorial 6", player), lambda state: state.has('Bunker Entry Door', player))
    set_rule(world.get_location("Bunker Advanced 4", player), lambda state: state.has('Bunker Entry Door', player))
    set_rule(world.get_location("Bunker Glass 3", player), lambda state: state.has('Bunker Entry Door', player))
    set_rule(world.get_location("Bunker Ultraviolet 2", player), lambda state: state.has('Bunker Entry Door', player))    
    set_rule(world.get_location("Bunker Laser", player), lambda state: state.has('Bunker Entry Door', player)) 

    #Jungle Checks
    set_rule(world.get_location("Jungle Waves 3", player), lambda state: True)
    set_rule(world.get_location("Jungle Waves 7", player), lambda state: True)
    set_rule(world.get_location("Jungle Dots 6", player), lambda state: state.has('Jungle Pop-up Wall', player)) 
    set_rule(world.get_location("Jungle Laser", player), lambda state: state.has('Jungle Pop-up Wall', player))   

    #Mountaintop Checks
    set_rule(world.get_location("Mountaintop River", player), lambda state: True)
    
    #Mountain Inside Checks
    set_rule(world.get_location("Mountain 1 Orange 7", player), lambda state: state._witness_has_lasers(player, 7))
    set_rule(world.get_location("Mountain 1 Purple 2", player), lambda state: state._witness_has_lasers(player, 7))
    set_rule(world.get_location("Mountain 1 Green 5", player), lambda state: state._witness_has_lasers(player, 7))
    set_rule(world.get_location("Mountain 2 Rainbow 4", player), lambda state: state._witness_has_lasers(player, 7))
    set_rule(world.get_location("Mountain 2 Rainbow 4", player), lambda state: state._witness_has_lasers(player, 7))
    set_rule(world.get_location("Final Elevator Control", player), lambda state: state._witness_has_lasers(player, 7))