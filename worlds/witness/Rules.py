from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class WitnessLogic(LogicMixin):
    def _witness_has_lasers(self, player: int, amount: int) -> bool:    
        lasers = 0
        
        lasers += int(self.has("Symmetry Laser Activation", player))
        lasers += int(self.has("Desert Laser Activation", player) and self.has("Desert Laser Redirection", player))
        lasers += int(self.has("Town Laser Activation", player))
        lasers += int(self.has("Monastery Laser Activation", player))
        lasers += int(self.has("Keep Laser Hedges Activation", player) and self.has("Keep Laser Pressure Plates Activation", player))
        lasers += int(self.has("Quarry Laser Activation", player))
        lasers += int(self.has("Treehouse Laser Activation", player))
        lasers += int(self.has("Jungle Laser Activation", player))
        lasers += int(self.has("Bunker Laser Activation", player))
        lasers += int(self.has("Swamp Laser Activation", player))
        lasers += int(self.has("Shadows Laser Activation", player))
        
        return lasers >= amount
    
    def _can_solve_panel(self, panel, player):
        from .full_logic import CHECKS_BY_HEX, CHECKS_BY_NAME, NECESSARY_EVENT_PANELS, EVENT_ITEM_NAMES, ORIGINAL_EVENT_PANELS, EVENT_ITEM_PAIRS
        from .Locations import event_location_table, locations
                     
        
        panelObj = CHECKS_BY_HEX[panel] 
          
        if CHECKS_BY_HEX[panel]["checkName"] + " Solved" in event_location_table and not self.has(EVENT_ITEM_PAIRS[CHECKS_BY_HEX[panel]["checkName"] + " Solved"], player):
            return False
        if panel not in ORIGINAL_EVENT_PANELS and not self.can_reach(CHECKS_BY_HEX[panel]["checkName"], "Location", player):
            return False
        if panel in ORIGINAL_EVENT_PANELS and CHECKS_BY_HEX[panel]["checkName"] + " Solved" not in event_location_table and not self._safe_manual_panel_check(panel, player): 
            return False
        return True
    
    def _meets_item_requirements(self, panel, player):
        from .full_logic import CHECKS_BY_HEX, CHECKS_BY_NAME, NECESSARY_EVENT_PANELS, EVENT_ITEM_NAMES
        from .Locations import event_location_table, locations
        
        panelObj = CHECKS_BY_HEX[panel] 
        
        
        for option in panelObj["requirement"]:     
            if len(option) == 0:
                return True
        
            solvability = []
            
            for item in option:
                if item == "7 Lasers":
                    solvability.append(self._witness_has_lasers(player, 7))
                elif item == "11 Lasers":
                    solvability.append(self._witness_has_lasers(player, 11))
                elif item in NECESSARY_EVENT_PANELS:
                    if CHECKS_BY_HEX[item]["checkName"] + " Solved" in event_location_table:
                        solvability.append(self.has(EVENT_ITEM_NAMES[item], player))
                    else :
                        solvability.append(self.can_reach(CHECKS_BY_HEX[item]["checkName"], "Location", player))
                else:
                    solvability.append(self.has(item, player))
                               
            if all(solvability):          
                return True

        return False
      
    #nested can_reach can cause problems, but only if the region being checked is neither of the two original regions from the first can_reach.
    #a nested can_reach is okay here because the only panels this function is called on are panels that exist on either side of all connections they are required for.
    #the spoiler log looks so much nicer this way, it gets rid of a bunch of event items, only leaving a couple. :)
    def _safe_manual_panel_check(self, panel, player):
        from .full_logic import CHECKS_BY_HEX
        return self._meets_item_requirements(panel, player) and self.can_reach(CHECKS_BY_HEX[panel]["region"]["name"],"Region", player)

    def _can_solve_panels(self, panelHexToSolveSet, player):
        from .full_logic import CHECKS_BY_HEX, CHECKS_BY_NAME, ORIGINAL_EVENT_PANELS
        from .Locations import event_location_table
        
        for option in panelHexToSolveSet:    
            if len(option) == 0:
                return True
                                
            validOption = True
            
            for panel in option:     
                if not self._can_solve_panel(panel, player):
                    validOption = False
                    break
                
            if validOption:
                return True
        return False

def makeLambda(checkHex, player):
    return lambda state: state._meets_item_requirements(checkHex, player)

def set_rules(world: MultiWorld, player: int):
    from .full_logic import CHECKS_BY_NAME, CHECKS_BY_HEX
    from .Locations import location_table, event_location_table
    
    for location in location_table:
        real_location = location
    
        if location in event_location_table:
            real_location = location[:-7]

        panel = CHECKS_BY_NAME[real_location]
        checkHex = panel["checkHex"]

        rule = makeLambda(checkHex, player)

        set_rule(world.get_location(location, player), rule)

    if world.logic[player] != 'nologic':
        world.completion_condition[player] = lambda state: state.has('Victory', player)
        
    