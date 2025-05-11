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

        #subtract 6 to account for starting jobs
        return count - 6

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

    def has_luxury_key(self, state: CollectionState) -> bool:
        return state.has("Item - Luxury Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_gardeners_key(self, state: CollectionState) -> bool:
        return state.has("Item - Gardeners Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_south_wing_key(self, state: CollectionState) -> bool:
        return state.has("Item - South Wing Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_west_wing_key(self, state: CollectionState) -> bool:
        return state.has("Item - West Wing Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_east_wing_key(self, state: CollectionState) -> bool:
        return state.has("Item - East Wing Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_dark_wing_key(self, state: CollectionState) -> bool:
        return state.has("Item - Dark Wing Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_cell_key(self, state: CollectionState, count: int) -> bool:
        return state.has("Item - Cell Key", self.player, count) or state.has("Item - Skeleton Key", self.player)

    def has_room_one_key(self, state: CollectionState) -> bool:
        return state.has("Item - Room 1 Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_small_key(self, state: CollectionState, count: int) -> bool:
        return state.has("Item - Small Key", self.player, count) or state.has("Item - Skeleton Key", self.player)

    def has_boss_key(self, state: CollectionState) -> bool:
        return state.has("Item - Boss Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_red_door_key(self, state: CollectionState, count: int) -> bool:
        return state.has("Item - Red Door Key", self.player, count) or state.has("Item - Skeleton Key", self.player)

    def has_ice_puzzle_key(self, state: CollectionState, count: int) -> bool:
        return state.has("Item - Ice Puzzle Key", self.player, count) or state.has("Item - Skeleton Key", self.player)

    def has_rampart_key(self, state: CollectionState) -> bool:
        return state.has("Item - Rampart Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_forgotten_key(self, state: CollectionState) -> bool:
        return state.has("Item - Forgotten Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_tram_key(self, state: CollectionState) -> bool:
        return state.has("Item - Tram Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_courtyard_key(self, state: CollectionState) -> bool:
        return state.has("Item - Courtyard Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_pyramid_key(self, state: CollectionState) -> bool:
        return state.has("Item - Pyramid Key", self.player) or state.has("Item - Skeleton Key", self.player)

    def has_jidamba_keys(self, state: CollectionState) -> bool:
        if state.has("Item - Skeleton Key", self.player):
            return True
        elif state.has("Item - Foliage Key", self.player) and state.has("Item - Cave Key", self.player) and state.has("Item - Canopy Key", self.player):
            return True
        else:
            return False