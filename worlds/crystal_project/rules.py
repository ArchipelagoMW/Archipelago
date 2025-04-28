from .Options import CrystalProjectOptions
from worlds.generic.Rules import set_rule, forbid_items_for_player, add_rule
from BaseClasses import CollectionState
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from . import CrystalProjectWorld

class CrystalProjectLogic:
    player: int
    options: CrystalProjectOptions

    def __init__(self, player: Optional[int], options: Optional[CrystalProjectOptions]):
        self.player = player
        self.options = options

    def has_jobs(self, state:CollectionState, jobMinimum:int) -> bool:
        return self.get_job_count(state) >= jobMinimum
    
    def get_job_count(self, state: CollectionState) -> int:
        count = 0
        if state.has("Job - Fencer", self.player):
            count += 1
        if state.has("Job - Shaman", self.player):
            count += 1
        if state.has("Job - Scholar", self.player):
            count += 1
        if state.has("Job - Aegis", self.player):
            count += 1
        if state.has("Job - Hunter", self.player):
            count += 1
        if state.has("Job - Chemist", self.player):
            count += 1
        if state.has("Job - Reaper", self.player):
            count += 1
        if state.has("Job - Ninja", self.player):
            count += 1
        if state.has("Job - Nomad", self.player):
            count += 1
        if state.has("Job - Dervish", self.player):
            count += 1
        if state.has("Job - Beatsmith", self.player):
            count += 1
        if state.has("Job - Samurai", self.player):
            count += 1
        if state.has("Job - Assassin", self.player):
            count += 1
        if state.has("Job - Valkyrie", self.player):
            count += 1
        if state.has("Job - Summoner", self.player):
            count += 1
        if state.has("Job - Beastmaster", self.player):
            count += 1
        if state.has("Job - Weaver", self.player):
            count += 1
        if state.has("Job - Mimic", self.player):
            count += 1

        return count

    def has_enough_clamshells(self, state: CollectionState):
        clamshellsRequired = 13
        if (self.options.goal.value == self.options.goal.option_clamshells):
            clamshellsRequired = self.options.clamshellsQuantity

        return state.has("Item - Clamshell", self.player, clamshellsRequired)

    def has_rental_quintar(self, state: CollectionState) -> bool:
        return state.has_any({"Item - Progressive Quintar Flute"}, self.player)

    def has_horizontal_movement(self, state: CollectionState) -> bool:
        return state.has("Item - Progressive Quintar Flute", self.player, 2) or state.has("Item - Owl Drum", self.player)

    def has_vertical_movement(self, state: CollectionState) -> bool:
        return state.has("Item - Ibek Bell", self.player)

    def has_glide(self, state: CollectionState) -> bool: 
        return state.has("Item - Owl Drum", self.player) or state.has("Item - Progressive Quintar Flute", self.player, 3)

    def has_swimming(self, state: CollectionState) -> bool:
        return state.has_any({"Item - Progressive Salmon Violin"}, self.player) or state.has("Item - Progressive Quintar Flute", self.player, 3)

    def has_golden_quintar(self, state: CollectionState) -> bool:
        return state.has("Item - Progressive Quintar Flute", self.player, 3)

    def new_world_requirements(self, state: CollectionState) -> bool:
        if (self.options.goal.value == self.options.goal.option_astley):
            return self.has_jobs(state, self.options.newWorldStoneJobQuantity.value)    
        else:
            return state.has("Item - New World Stone", self.player)