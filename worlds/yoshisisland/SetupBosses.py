from typing import Union
from BaseClasses import MultiWorld, CollectionState
from .Options import get_option_value

class BossReqs:
    player: int


    def __init__(self, multiworld, player: int):
        self.player = player

        
        if get_option_value(multiworld, player, "stage_logic") == 0:
            self.game_logic = "Easy"
        elif get_option_value(multiworld, player, "stage_logic") == 1:
            self.game_logic = "Normal"
        else:
            self.game_logic = "Hard"

        self.castle_unlock = multiworld.castle_open_condition[player].value
        self.boss_unlock = multiworld.castle_clear_condition[player].value

    def castle_access(self, state: CollectionState,) -> bool:
        return state.has('Boss Clear', self.player, self.castle_unlock)

    def castle_clear(self, state: CollectionState,) -> bool:
        return state.has('Boss Clear', self.player, self.boss_unlock)