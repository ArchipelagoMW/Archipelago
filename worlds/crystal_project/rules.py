from .Options import CrystalProjectOptions
from worlds.generic.Rules import set_rule, forbid_items_for_player, add_rule
from BaseClasses import CollectionState
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from . import CrystalProjectWorld
from .Keys import *

class CrystalProjectLogic:
    player: int
    options: CrystalProjectOptions

    def __init__(self, player: Optional[int], options: Optional[CrystalProjectOptions]):
        self.player = player
        self.options = options

    def has_jobs(self, state: CollectionState, job_minimum: int) -> bool:
        return self.get_job_count(state) >= job_minimum
    
    def get_job_count(self, state: CollectionState) -> int:
        count = 0
        if state.has("Job - Warrior", self.player):
            count += 1
        if state.has("Job - Monk", self.player):
            count += 1
        if state.has("Job - Rogue", self.player):
            count += 1
        if state.has("Job - Cleric", self.player):
            count += 1
        if state.has("Job - Wizard", self.player):
            count += 1
        if state.has("Job - Warlock", self.player):
            count += 1
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

        #subtract starting jobs
        return count - self.get_starting_job_count()

    def get_starting_job_count(self):
        if self.options.jobRando.value == self.options.jobRando.option_full:
            return self.options.startingJobQuantity.value
        else:
            return 6

    def has_enough_clamshells(self, state: CollectionState):
        return state.has("Item - Clamshell", self.player, self.options.clamshellsQuantity)

    def has_rental_quintar(self, state: CollectionState) -> bool:
        return state.has_any({"Item - Progressive Quintar Flute"}, self.player) or state.has("Item - Owl Drum", self.player)

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
        if self.options.goal.value == self.options.goal.option_astley:
            return self.has_jobs(state, self.options.newWorldStoneJobQuantity.value)    
        else:
            return state.has("Item - New World Stone", self.player)

    def is_area_in_level_range(self, state: CollectionState, count: int) -> bool:
        if self.options.levelGating:
            return state.has("Item - Progressive Level Cap", self.player, count)
        return True

    #has_key is for: Luxury Key, Gardeners Key, All Wing Keys, Cell Keys, Room One Key, Small Keys, Boss Key, Red Door Keys,
    #Ice Puzzle Keys, Rampart Key, Forgotten Key, Tram Key, Courtyard Key, Pyramid Key
    def has_key(self, state: CollectionState, key_name: str, count: int = 1) -> bool:
        return state.has(key_name, self.player, count) or state.has(SKELETON_KEY, self.player)

    def has_jidamba_keys(self, state: CollectionState) -> bool:
        if state.has(SKELETON_KEY, self.player):
            return True
        elif state.has(FOLIAGE_KEY, self.player) and state.has(CAVE_KEY, self.player) and state.has(CANOPY_KEY, self.player):
            return True
        else:
            return False