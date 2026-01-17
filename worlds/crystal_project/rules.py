from BaseClasses import CollectionState
from .constants.display_regions import *
from .constants.item_groups import *
from .constants.jobs import SCHOLAR_JOB
from .constants.key_items import *
from .constants.keys import *
from .constants.level_requirements import *
from .constants.mounts import *
from .constants.region_passes import *
from .constants.scholar_abilities import REVERSE_POLARITY
from .constants.teleport_stones import *
from .items import singleton_keys
from .options import CrystalProjectOptions


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
        if self.options.job_rando.value == self.options.job_rando.option_full:
            return self.options.starting_job_quantity.value
        else:
            return 6

    def has_enough_clamshells(self, state: CollectionState):
        clamshell_quantity = 2
        if self.options.goal.value == self.options.goal.option_clamshells:
            clamshell_quantity = self.options.clamshell_goal_quantity.value
        return state.has(CLAMSHELL, self.player, clamshell_quantity)

    def has_rental_quintar(self, state: CollectionState, rental_display_region_name: str) -> bool:
        #Using the display region for this check bc it's least likely to change and equivalent in function in this case

        #If you have Owl Drum or Quintar Flute you're just good to go
        if self.has_horizontal_movement(state):
            has_rental_quintar = True
        #If not we check for Quintar Pass and access to the rental location
        else:
            has_rental_quintar = state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player) or state.has(PROGRESSIVE_MOUNT, self.player)
            if not self.is_regionsanity_disabled():
                if rental_display_region_name == ROLLING_QUINTAR_FIELDS_DISPLAY_NAME and not state.has(ROLLING_QUINTAR_FIELDS_PASS, self.player):
                    has_rental_quintar = False
                if rental_display_region_name == SARA_SARA_BAZAAR_DISPLAY_NAME and not state.has(SARA_SARA_BAZAAR_PASS, self.player):
                    has_rental_quintar = False

        return has_rental_quintar

    def has_horizontal_movement(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 2) or state.has(OWL_DRUM, self.player) or state.has(PROGRESSIVE_MOUNT, self.player, 2)

    def has_fast(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 2) or state.has(PROGRESSIVE_MOUNT, self.player, 2)

    def has_vertical_movement(self, state: CollectionState) -> bool:
        return state.has(IBEK_BELL, self.player) or state.has(PROGRESSIVE_MOUNT, self.player, 3)

    def can_push_ice_block_and_goat(self, state: CollectionState, region_pass: str) -> bool:
        return self.has_vertical_movement(state) and (state.has(region_pass, self.player, 1) or self.options.regionsanity.value == self.options.regionsanity.option_disabled)

    def has_glide(self, state: CollectionState) -> bool: 
        return state.has(OWL_DRUM, self.player) or state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3) or state.has(PROGRESSIVE_MOUNT, self.player, 4)

    def has_rental_salmon(self, state: CollectionState) -> bool:
        return self.has_swimming(state) or state.has(SALMON_RIVER_PASS, self.player) or self.options.regionsanity.value == self.options.regionsanity.option_disabled

    def has_swimming(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_SALMON_VIOLA, self.player) or state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3)  or state.has(PROGRESSIVE_MOUNT, self.player, 5)

    def fish_race_requirements(self, state: CollectionState, is_rental_salmon_enough: bool = False) -> bool:
        if is_rental_salmon_enough:
            return state.has(SALMON_RIVER_PASS, self.player) or self.options.regionsanity.value == self.options.regionsanity.option_disabled
        else:
            return (state.has(PROGRESSIVE_SALMON_VIOLA, self.player) or state.has(PROGRESSIVE_MOUNT, self.player, 5)) and (state.has(SALMON_RIVER_PASS, self.player) or self.options.regionsanity.value == self.options.regionsanity.option_disabled)

    def has_golden_quintar(self, state: CollectionState) -> bool:
        return state.has(PROGRESSIVE_QUINTAR_WOODWIND, self.player, 3) or state.has(PROGRESSIVE_MOUNT, self.player, 7)

    def obscure_routes_on(self) -> bool:
        return self.options.obscure_routes.value == self.options.obscure_routes.option_true

    def is_hop_to_it_at_least_fancy_footwork(self) -> bool:
        return self.options.hop_to_it.value >= self.options.hop_to_it.option_fancy_footwork

    def is_hop_to_it_at_least_one_hop_beyond(self) -> bool:
        return self.options.hop_to_it.value >= self.options.hop_to_it.option_one_hop_beyond

    def is_hop_to_it_pray(self) -> bool:
        return self.options.hop_to_it.value == self.options.hop_to_it.option_pray

    def is_regionsanity_disabled(self) -> bool:
        return self.options.regionsanity.value == self.options.regionsanity.option_disabled

    def is_regionsanity_extreme(self) -> bool:
        return self.options.regionsanity.value == self.options.regionsanity.option_extreme

    def old_world_requirements(self, state: CollectionState) -> bool:
        if self.options.goal.value == self.options.goal.option_true_astley:
            return self.has_swimming(state) and state.has(DEITY_EYE, self.player, 4) and state.has(STEM_WARD, self.player) and state.can_reach(THE_DEPTHS_AP_REGION, player=self.player)
        else:
            return state.has(OLD_WORLD_STONE, self.player)

    def get_progressive_level_count(self, expected_level: int) -> int:
        expected_level += self.options.level_compared_to_enemies.value

        if expected_level > self.options.max_level.value:
            expected_level = self.options.max_level.value

        expected_level -= self.options.starting_level.value

        count = ((expected_level - 1) // self.options.progressive_level_size.value) + 1
        return count

    def is_area_in_level_range(self, state: CollectionState, level: int) -> bool:
        if not self.options.level_gating.value == self.options.level_gating.option_none:
            return state.has(PROGRESSIVE_LEVEL, self.player, self.get_progressive_level_count(level))

        return True

    #has_key is for: Luxury Key, Gardeners Key, All Wing Keys, Cell Keys, Room One Key, Small Keys, Boss Key, Red Door Keys,
    #Ice Puzzle Keys, Rampart Key, Forgotten Key, Tram Key, Courtyard Key, Pyramid Key
    def has_key(self, state: CollectionState, key_name: str, count: int = 1) -> bool:
        if state.has(SKELETON_KEY, self.player):
            return True
        if (self.options.key_mode.value == self.options.key_mode.option_key_ring or
            self.options.key_mode.value == self.options.key_mode.option_key_ring_skelefree):
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
        if state.has(SKELETON_KEY, self.player) or (self.has_key(state, FOLIAGE_KEY, 1) and self.has_key(state, CAVE_KEY, 1) and self.has_key(state, CANOPY_KEY,1)):
            return True
        else:
            return False

    ap_regions_that_cant_earn_money: list[str] = [MENU_AP_REGION, SARA_SARA_BEACH_EAST_AP_REGION, IBEK_CAVE_MOUTH_AP_REGION, BELOW_IBEK_CAVE_MOUTH_AP_REGION, BELOW_IBEK_CAVE_EAST_AP_REGION,
                                                  BELOW_IBEK_CAVE_WEST_AP_REGION, MODDED_ZONE_AP_REGION]

    def can_earn_money(self, state: CollectionState, shop_ap_region: str) -> bool:
        #Note: this rule is also used for the Sara Sara Bazaar innkeeper bc he charges money
        if shop_ap_region == MERCURY_SHRINE_AP_REGION:
            return True

        from .regions import display_region_levels_dictionary
        from .regions import ap_region_to_display_region_dictionary

        has_combat = False

        #This is getting the order of the Display Region that the shop is in; higher order means more difficult zones
        # (if the shop has no combat in its region, then we can't exactly do a compare on enemy levels directly)
        shop_region_index = list(display_region_levels_dictionary.keys()).index(ap_region_to_display_region_dictionary[shop_ap_region])

        for ap_region in state.multiworld.worlds[self.player].get_regions():
            current_display_region_index = list(display_region_levels_dictionary.keys()).index(ap_region_to_display_region_dictionary[ap_region.name])

            #checking if the player has access to money-earning zones that are higher than 6 regions below the shop's region, to make sure they're not expected to grind Spawning Meadows enemies
            #to buy something in Neptune Shrine
            if current_display_region_index > (shop_region_index - 6) and ap_region.can_reach(state) and ap_region.name not in self.ap_regions_that_cant_earn_money:
                enemy_level = display_region_levels_dictionary[ap_region_to_display_region_dictionary[ap_region.name]][0]
                if (enemy_level > 0 or (ap_region.name == CAPITAL_SEQUOIA_AP_REGION and self.is_area_in_level_range(state, CAPITAL_SEQUOIA_ENEMY_LEVEL)) or
                        (ap_region.name == QUINTAR_RESERVE_AP_REGION and self.is_area_in_level_range(state, QUINTAR_RESERVE_ENEMY_LEVEL))):
                    has_combat = True
                    break

        return has_combat

    def can_fight_gran(self, state: CollectionState) -> bool:
        return (state.has(SCHOLAR_JOB, self.player) and state.has(REVERSE_POLARITY, self.player)) or self.is_area_in_level_range(state, GRAN_FIGHT_LEVEL)