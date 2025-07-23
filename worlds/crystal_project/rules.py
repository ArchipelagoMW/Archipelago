from .options import CrystalProjectOptions
from .constants.keys import *
from .constants.key_items import *
from .constants.mounts import *
from .constants.teleport_stones import *
from .constants.regions import *
from .constants.region_passes import *
from .constants.item_groups import *
from .items import singleton_keys
from BaseClasses import CollectionState

class CrystalProjectLogic:
    player: int
    options: CrystalProjectOptions

    def __init__(self, player: int, options: CrystalProjectOptions):
        self.player = player
        self.options = options

    def has_jobs(self, state: CollectionState, job_minimum: int) -> bool:
        return self.get_job_count(state) >= job_minimum
    
    def get_job_count(self, state: CollectionState) -> int:
        count = 0
        for job in state.multiworld.worlds[self.player].item_name_groups[JOB]:
            if state.has(job, self.player):
                count += 1

        #subtract starting jobs
        return count - self.get_starting_job_count()

    def get_starting_job_count(self):
        if self.options.jobRando.value == self.options.jobRando.option_full:
            return self.options.startingJobQuantity.value
        else:
            return 6

    def has_enough_clamshells(self, state: CollectionState):
        clamshell_quantity = 2
        if self.options.goal.value == self.options.goal.option_clamshells:
            clamshell_quantity = self.options.clamshellGoalQuantity.value
        return state.has(CLAMSHELL, self.player, clamshell_quantity)

    def has_rental_quintar(self, state: CollectionState, rental_region_name: str) -> bool:
        has_rental_quintar: bool = False
        
        #If you have Owl Drum or Quintar Flute you're just good to go
        if self.has_horizontal_movement(state):
            has_rental_quintar = True
        #If not we check for Quintar Pass and access to the rental location
        else:
            has_rental_quintar = state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player) or state.has(PROGRESSIVE_MOUNT, self.player)
            if self.options.regionsanity:
                if rental_region_name == ROLLING_QUINTAR_FIELDS and not state.has(ROLLING_QUINTAR_FIELDS_PASS, self.player):
                    has_rental_quintar = False
                if rental_region_name == SARA_SARA_BAZAAR and not state.has(SARA_SARA_BAZAAR_PASS, self.player):
                    has_rental_quintar = False

        return has_rental_quintar

    def has_horizontal_movement(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 2) or state.has(OWL_DRUM, self.player) or state.has(PROGRESSIVE_MOUNT, self.player, 2)

    def has_fast(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 2) or state.has(PROGRESSIVE_MOUNT, self.player, 2)

    def has_vertical_movement(self, state: CollectionState) -> bool:
        return state.has(IBEK_BELL, self.player) or state.has(PROGRESSIVE_MOUNT, self.player, 3)

    def has_glide(self, state: CollectionState) -> bool: 
        return state.has(OWL_DRUM, self.player) or state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3) or state.has(PROGRESSIVE_MOUNT, self.player, 4)

    def has_swimming(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_SALMON_VIOLA, self.player) or state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3)  or state.has(PROGRESSIVE_MOUNT, self.player, 5)

    def has_golden_quintar(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3) or state.has(PROGRESSIVE_MOUNT, self.player, 7)

    def new_world_requirements(self, state: CollectionState) -> bool:
        if self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley:
            return self.has_jobs(state, self.options.newWorldStoneJobQuantity.value)    
        else:
            return state.has(NEW_WORLD_STONE, self.player)

    def old_world_requirements(self, state: CollectionState) -> bool:
        if self.options.goal.value == self.options.goal.option_true_astley:
            return self.has_swimming(state) and state.has(DEITY_EYE, self.player, 4) and state.has(STEM_WARD, self.player)
        else:
            return state.has(OLD_WORLD_STONE, self.player)

    def is_area_in_level_range(self, state: CollectionState, min_level: int) -> bool:
        min_level = min_level + self.options.levelComparedToEnemies.value

        if min_level > self.options.maxLevel.value:
            min_level = self.options.maxLevel.value

        # Players start with 1 Progressive Level
        count = ((min_level - 1) // self.options.progressiveLevelSize.value) + 1

        if not self.options.levelGating.value == self.options.levelGating.option_none:
            return state.has(PROGRESSIVE_LEVEL, self.player, count)

        return True

    #has_key is for: Luxury Key, Gardeners Key, All Wing Keys, Cell Keys, Room One Key, Small Keys, Boss Key, Red Door Keys,
    #Ice Puzzle Keys, Rampart Key, Forgotten Key, Tram Key, Courtyard Key, Pyramid Key
    def has_key(self, state: CollectionState, key_name: str, count: int = 1) -> bool:
        if state.has(SKELETON_KEY, self.player):
            return True
        if (self.options.keyMode.value == self.options.keyMode.option_key_ring or
            self.options.keyMode.value == self.options.keyMode.option_key_ring_skelefree):
            return self.has_key_ring(state, key_name)
        return state.has(key_name, self.player, count)

    def has_key_ring(self, state: CollectionState, key_name: str) -> bool:
        if key_name in singleton_keys:
            return state.has(key_name, self.player)

        if (key_name == CELL_KEY
                or key_name == SOUTH_WING_KEY
                or key_name == EAST_WING_KEY
                or key_name == WEST_WING_KEY
                or key_name == DARK_WING_KEY):
            return state.has(PRISON_KEY_RING, self.player)

        if (key_name == BEAURIOR_BOSS_KEY
                or key_name == SMALL_KEY):
            return state.has(BEAURIOR_KEY_RING, self.player)

        if key_name == RED_DOOR_KEY:
            return state.has(SLIP_GLIDE_RIDE_KEY_RING, self.player)

        if key_name == ICE_PUZZLE_KEY:
            return state.has(ICE_PUZZLE_KEY_RING, self.player)

        if (key_name == FOLIAGE_KEY
                or key_name == CANOPY_KEY
                or key_name == CAVE_KEY):
            return state.has(JIDAMBA_KEY_RING, self.player)

        return False

    def has_jidamba_keys(self, state: CollectionState) -> bool:
        if self.has_key(state, FOLIAGE_KEY, 1) and self.has_key(state, CAVE_KEY, 1) and self.has_key(state, CANOPY_KEY,1):
            return True
        else:
            return False

    def can_earn_money(self, state: CollectionState, shop_region: str) -> bool:
        if shop_region == MERCURY_SHRINE:
            return True

        from .regions import region_levels_dictionary

        has_combat = False
        region_checked = 0
        shop_region_index = list(region_levels_dictionary.keys()).index(shop_region)

        for region in state.multiworld.worlds[self.player].get_regions():
            region_checked += 1
            #checking if the player has access to money-earning zones that are higher than 6 regions below the shop's region, to make sure they're not expected to grind Spawning Meadows enemies to buy something in Neptune Shrine
            if region_checked > (shop_region_index - 6) and region.can_reach(state) and region.name != MENU and region.name != MODDED_ZONE:
                enemy_level = region_levels_dictionary[region.name][0]
                if enemy_level > 0 or region.name == CAPITAL_SEQUOIA or region.name == QUINTAR_RESERVE:
                    has_combat = True
                    break

        return has_combat