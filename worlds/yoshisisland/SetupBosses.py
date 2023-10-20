from typing import Union
from BaseClasses import MultiWorld, CollectionState

class BossReqs:
    player: int


    def __init__(self, multiworld, player: int):
        self.player = player
        self.castle_unlock = multiworld.castle_open_condition[player].value
        self.boss_unlock = multiworld.castle_clear_condition[player].value

    def castle_access(self, state: CollectionState,) -> bool:
        return state.has('Boss Clear', self.player, self.castle_unlock)

    def castle_clear(self, state: CollectionState,) -> bool:
        return state.has('Boss Clear', self.player, self.boss_unlock)