from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from .SetRequiredBosses import load_req_bosses

from .Options import get_option_value

import random
import pdb

class LogicComplex(LogicMixin):

    def castle_door(self, world: MultiWorld, player: int) -> bool: #This will check for what door mode 6-8 uses, depending on settings and return logic correctly.
        if get_option_value(world, player, "castle_door_choice") == 1:
            return self.has('! Switch', player)

        elif get_option_value(world, player, "castle_door_choice") == 2:
            return self.has('Egg Capacity Upgrade', player, 2) and self.has('Key', player)

        elif get_option_value(world, player, "castle_door_choice") > 2:
            return True

    def castle_unlock_con(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "castle_open_condition") == 0:
            return True
        elif get_option_value(world, player, "castle_open_condition") == 1:
            return self.has("World Flag", player, world.flags_for_castle_open[player].value)
        elif get_option_value(world, player, "castle_open_condition") == 2:
            return load_req_bosses(world, player)



    def lots_of_stars(self, world: MultiWorld, player: int) -> bool: #This is a check for middle rings or tulips
        return self.has_any({'Middle Ring', 'Tulip'}, player)


    #def castle_clear()

    #def bosses_killed()

    #def can_carry_2_eggs()

    #def can_carry_3_eggs()

    #def can_carry_4_eggs()

    #def can_carry_5_eggs()

    #def can_carry_6_eggs()

    def can_see_hidden_objects(self, world: MultiWorld, player: int) -> bool: #Determine if the player is on Strict logic, and if consumables are on, return magnifying glass access and secret lens if not
        if get_option_value(world, player, "stage_logic") == 0:
            if get_option_value(world, player, "hidden_object_visibility") > 1:
                return True
            elif get_option_value(world, player, "item_logic") == True:
                return self.can_grind_overworld_panels(world, player) or self.has('Secret Lens', player)
            else:
                return self.has('Secret Lens', player)
        else:
            return True
            

    def world_1_keys(self, world: MultiWorld, player: int) -> bool:
        return self.has('Key', player) or self.has('World 1 Key', player, 4)
    
    def world_2_keys(self, world: MultiWorld, player: int) -> bool:
        return self.has('Key', player) or self.has('World 2 Key', player, 8)
    
    def world_3_keys(self, world: MultiWorld, player: int) -> bool:
        return self.has('Key', player) or self.has('World 3 Key', player, 3)

    def world_4_keys(self, world: MultiWorld, player: int) -> bool:
        return self.has('Key', player) or self.has('World 4 Key', player, 8)

    def world_5_keys(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "extras_enabled") == False:
            return self.has('Key', player) or self.has('World 2 Key', player, 1) #1 if Extras disabled
        else:
            return self.has('Key', player) or self.has('World 2 Key', player, 2)

    def world_6_keys(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "extras_enabled") == False:
            return self.has('Key', player) or self.has('World 6 Key', player, 6) #6 if castle is set to door 2
        else:
            return self.has('Key', player) or self.has('World 6 Key', player, 5)
    
    
    def logic_easy(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "stage_logic") == 0:
            return True

    def logic_normal(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "stage_logic") == 1:
            return True

    def logic_hard(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "stage_logic") == 2:
            return True

    
    def can_grind_melons(self, world: MultiWorld, player: int) -> bool:
        if self.can_grind_overworld_panels(world, player):
            return True
        else:
            return self.can_grind_bandit_melons(world, player)

    def can_grind_bandit_melons(self, world: MultiWorld, player: int) -> bool:
        if self.can_reach('The Cave Of The Mystery Maze', 'Region', player):
            return self.has('Large Spring Ball', player) and self.world_2_keys(world, player)


    def can_grind_overworld_panels(self, world: MultiWorld, player: int) -> bool:
        if self.can_reach('Flip Cards', 'Region', player) or self.can_reach('Drawing Lots', 'Region', player) or self.can_reach('Match Cards', 'Region', player):
            return False

    
    def can_melt_ice(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "item_logic") == True:
            return self.has('Fire Melons', player) or self.can_grind_melons(world, player)
        else:
            return self.has('Fire Melons', player)

    def castle_clear_logic(self, world: MultiWorld, player: int) -> bool:
        if get_option_value(world, player, "flags_for_castle_open") == world.flags_for_castle_clear[player].value:
            return True


        


    #def can_grind_bandit_games



    #Seed Spitting Contest:
        #Pocket Melon, Pocket Fire Melon, Ice Melon can melt ice or kill enemies.

    #Collect Coins:
        #Winged Cloud, FULL Eggs, 

    #def inventory_can_screen_clear #Pow, Clouds, Super Melon, Ice Melon, Fire Melon

    #def can_grind_melons