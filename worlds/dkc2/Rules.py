
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC2World
    from BaseClasses import Location

from .Names import LocationName, ItemName, RegionName, EventName
from .Options import Goal

from worlds.generic.Rules import CollectionRule, add_rule
from BaseClasses import CollectionState
  
class DKC2Rules:
    player: int
    world: "DKC2World"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "DKC2World") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.crocodile_isle} -> {RegionName.gangplank_galleon}":
                self.can_access_galleon,
            f"{RegionName.crocodile_isle} -> {RegionName.crocodile_cauldron}":
                self.can_access_cauldron,
            f"{RegionName.crocodile_isle} -> {RegionName.krem_quay}":
                self.can_access_quay,
            f"{RegionName.crocodile_isle} -> {RegionName.krazy_kremland}":
                self.can_access_kremland,
            f"{RegionName.crocodile_isle} -> {RegionName.gloomy_gulch}":
                self.can_access_gulch,
            f"{RegionName.crocodile_isle} -> {RegionName.krools_keep}":
                self.can_access_keep,
            f"{RegionName.crocodile_isle} -> {RegionName.the_flying_krock}":
                self.can_access_krock,
            f"{RegionName.crocodile_cauldron} -> {RegionName.lost_world_cauldron}":
                self.can_access_lost_world_cauldron,
            f"{RegionName.krem_quay} -> {RegionName.lost_world_quay}":
                self.can_access_lost_world_quay,
            f"{RegionName.krazy_kremland} -> {RegionName.lost_world_kremland}":
                self.can_access_lost_world_kremland,
            f"{RegionName.gloomy_gulch} -> {RegionName.lost_world_gulch}":
                self.can_access_lost_world_gulch,
            f"{RegionName.krools_keep} -> {RegionName.lost_world_keep}":
                self.can_access_lost_world_keep,
            f"{RegionName.gangplank_galleon} -> {RegionName.krows_nest_map}":
                self.can_access_nest,
            f"{RegionName.crocodile_cauldron} -> {RegionName.kleevers_kiln_map}":
                self.can_access_kiln,
            f"{RegionName.krem_quay} -> {RegionName.kudgels_kontest_map}":
                self.can_access_kontest,
            f"{RegionName.krazy_kremland} -> {RegionName.king_zing_sting_map}":
                self.can_access_king,
            f"{RegionName.gloomy_gulch} -> {RegionName.kreepy_krow_map}":
                self.can_access_kreepy,
            f"{RegionName.krools_keep} -> {RegionName.stronghold_showdown_map}":
                self.can_access_showdown,
            f"{RegionName.the_flying_krock} -> {RegionName.k_rool_duel_map}":
                self.can_access_duel,
        }

        if world.options.goal != Goal.option_flying_krock:
            self.connection_rules.update(
                {
                    f"{RegionName.lost_world_cauldron} -> {RegionName.krocodile_core_map}":
                        self.can_access_kore,
                    f"{RegionName.lost_world_quay} -> {RegionName.krocodile_core_map}":
                        self.can_access_kore,
                    f"{RegionName.lost_world_kremland} -> {RegionName.krocodile_core_map}":
                        self.can_access_kore,
                    f"{RegionName.lost_world_gulch} -> {RegionName.krocodile_core_map}":
                        self.can_access_kore,
                    f"{RegionName.lost_world_keep} -> {RegionName.krocodile_core_map}":
                        self.can_access_kore,
                }
            )

    def can_access_galleon(self, state: CollectionState) -> bool:
        return state.has(ItemName.gangplank_galleon, self.player)
    
    def can_access_cauldron(self, state: CollectionState) -> bool:
        return state.has(ItemName.crocodile_cauldron, self.player)
    
    def can_access_quay(self, state: CollectionState) -> bool:
        return state.has(ItemName.krem_quay, self.player)
    
    def can_access_kremland(self, state: CollectionState) -> bool:
        return state.has(ItemName.krazy_kremland, self.player)
    
    def can_access_gulch(self, state: CollectionState) -> bool:
        return state.has(ItemName.gloomy_gulch, self.player)
    
    def can_access_keep(self, state: CollectionState) -> bool:
        return state.has(ItemName.krools_keep, self.player)
    
    def can_access_krock(self, state: CollectionState) -> bool:
        if self.world.options.krock_boss_tokens.value == 0:
            return state.has(ItemName.the_flying_krock, self.player)
        else:
            return state.has(ItemName.boss_token, self.player, self.world.options.krock_boss_tokens.value)
    
    def can_access_lost_world_cauldron(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_cauldron, self.player)
    
    def can_access_lost_world_quay(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_quay, self.player)
    
    def can_access_lost_world_kremland(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_kremland, self.player)
    
    def can_access_lost_world_gulch(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_gulch, self.player)
    
    def can_access_lost_world_keep(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_keep, self.player)
    
    def can_access_kore(self, state: CollectionState) -> bool:
        return state.has(ItemName.lost_world_rock, self.player, self.world.options.lost_world_rocks.value)
    
    def can_access_nest(self, state: CollectionState) -> bool:
        return state.has(EventName.galleon_level, self.player, self.world.options.required_galleon_levels.value)
    
    def can_access_kiln(self, state: CollectionState) -> bool:
        return state.has(EventName.cauldron_level, self.player, self.world.options.required_cauldron_levels.value)
    
    def can_access_kontest(self, state: CollectionState) -> bool:
        return state.has(EventName.quay_level, self.player, self.world.options.required_quay_levels.value)
    
    def can_access_king(self, state: CollectionState) -> bool:
        return state.has(EventName.kremland_level, self.player, self.world.options.required_kremland_levels.value)
    
    def can_access_kreepy(self, state: CollectionState) -> bool:
        return state.has(EventName.gulch_level, self.player, self.world.options.required_gulch_levels.value)
    
    def can_access_showdown(self, state: CollectionState) -> bool:
        return state.has(EventName.keep_level, self.player, self.world.options.required_keep_levels.value)
    
    def can_access_duel(self, state: CollectionState) -> bool:
        return state.has(EventName.krock_level, self.player, self.world.options.required_krock_levels.value)

    def has_diddy(self, state: CollectionState) -> bool:
        return state.has(ItemName.diddy, self.player)

    def has_dixie(self, state: CollectionState) -> bool:
        return state.has(ItemName.dixie, self.player)
    
    def has_both_kongs(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.diddy, ItemName.dixie}, self.player)
    
    def can_climb(self, state: CollectionState) -> bool:
        return state.has(ItemName.climb, self.player)
    
    def can_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.carry, self.player)
    
    def can_cling(self, state: CollectionState) -> bool:
        return state.has(ItemName.cling, self.player)
    
    def can_cartwheel(self, state: CollectionState) -> bool:
        return state.has(ItemName.cartwheel, self.player)
    
    def can_swim(self, state: CollectionState) -> bool:
        return state.has(ItemName.swim, self.player)
    
    def can_team_attack(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.diddy, ItemName.dixie, ItemName.team_attack}, self.player)
    
    def can_hover(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.dixie, ItemName.helicopter_spin}, self.player)
    
    def has_rambi(self, state: CollectionState) -> bool:
        return state.has(ItemName.rambi, self.player)
    
    def has_squawks(self, state: CollectionState) -> bool:
        return state.has(ItemName.squawks, self.player)
    
    def has_enguarde(self, state: CollectionState) -> bool:
        return state.has(ItemName.enguarde, self.player)
    
    def has_squitter(self, state: CollectionState) -> bool:
        return state.has(ItemName.squitter, self.player)
    
    def has_rattly(self, state: CollectionState) -> bool:
        return state.has(ItemName.rattly, self.player)
    
    def has_clapper(self, state: CollectionState) -> bool:
        return state.has(ItemName.clapper, self.player)
    
    def has_glimmer(self, state: CollectionState) -> bool:
        return state.has(ItemName.glimmer, self.player)
    
    def has_skull_kart(self, state: CollectionState) -> bool:
        return state.has(ItemName.skull_kart, self.player)
    
    def has_kannons(self, state: CollectionState) -> bool:
        return state.has(ItemName.barrel_kannons, self.player)
    
    def has_invincibility(self, state: CollectionState) -> bool:
        return state.has(ItemName.barrel_exclamation, self.player)
    
    def can_use_diddy_barrels(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.diddy, ItemName.barrel_kong}, self.player)
    
    def can_use_dixie_barrels(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.dixie, ItemName.barrel_kong}, self.player)
    
    def has_controllable_barrels(self, state: CollectionState) -> bool:
        return state.has(ItemName.barrel_control, self.player)
    
    def has_warp_barrels(self, state: CollectionState) -> bool:
        return state.has(ItemName.barrel_warp, self.player)
    
    def true(self, state: CollectionState) -> bool:
        return True
    
    def set_dkc2_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = multiworld.get_entrance(entrance_name, self.player)
                entrance.access_rule = rule
            except KeyError:
                continue

        for loc in multiworld.get_locations(self.player):
            # Skip events so we don't have to type duplicate entries...
            if "(Map Event)" in loc.name:
                continue
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        map_event.access_rule = loc.access_rule
                    except KeyError:
                        # Filter out missing locations
                        continue
                
        if self.world.options.goal == Goal.option_flying_krock:
            multiworld.completion_condition[self.player] = lambda state: state.has(EventName.k_rool_duel_clear, self.player)
            
        elif self.world.options.goal.value == Goal.option_lost_world:
            multiworld.completion_condition[self.player] = lambda state: state.has(EventName.krocodile_core_clear, self.player)
        
        else:
            multiworld.completion_condition[self.player] = lambda state: (
                state.has(EventName.k_rool_duel_clear, self.player) and
                state.has(EventName.krocodile_core_clear, self.player)
            )

    # Universal Tracker: Append the next logic level rule that has UT's glitched item to the actual logic rule
    def set_dkc2_glitched_rules(self) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            # Skip events so we don't have to type duplicate entries...
            if "(Map Event)" in loc.name:
                continue
            if loc.name in self.location_rules:
                glitched_rule = lambda state, rule=self.location_rules[loc.name]: state.has(ItemName.glitched, self.player) and rule(state)
                add_rule(loc, glitched_rule, combine="or")
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        add_rule(map_event, glitched_rule, combine="or")
                    except KeyError:
                        # Filter out missing locations
                        continue
            

class DKC2StrictRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                lambda state: self.can_carry(state) or self.has_rambi(state),

            LocationName.mainbrace_mayhem_clear:
                self.can_climb,
            LocationName.mainbrace_mayhem_kong:
                self.can_climb,
            LocationName.mainbrace_mayhem_dk_coin:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_bonus_1:
                lambda state: self.can_climb(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.mainbrace_mayhem_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.mainbrace_mayhem_bonus_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_clear:
                self.can_cling,
            LocationName.gangplank_galley_kong:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and
                    self.has_kannons(state),
            LocationName.gangplank_galley_dk_coin:
                lambda state: self.can_cling(state) and (
                    self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state))
                ),
            LocationName.gangplank_galley_bonus_1:
                self.can_carry,
            LocationName.gangplank_galley_bonus_2:
                lambda state: self.can_cling(state) and self.has_invincibility(state),

            LocationName.lockjaws_locker_clear:
                self.can_swim,
            LocationName.lockjaws_locker_kong:
                self.can_swim,
            LocationName.lockjaws_locker_dk_coin:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.lockjaws_locker_bonus_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.topsail_trouble_clear:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_kong:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_dk_coin:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_bonus_1:
                lambda state: self.has_rattly(state) or (
                    self.can_team_attack(state) and self.can_cling(state)
                ),
            LocationName.topsail_trouble_bonus_2:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),

            LocationName.krows_nest_clear:
                lambda state: self.can_carry(state) and self.has_both_kongs(state),
            LocationName.krow_defeated:
                lambda state: self.can_carry(state) and self.has_both_kongs(state),

            LocationName.hot_head_hop_clear:
                self.has_kannons,
            LocationName.hot_head_hop_kong:
                lambda state: self.can_carry(state) and (
                    self.can_team_attack(state) or
                    self.has_squitter(state)
                ),
            LocationName.hot_head_hop_dk_coin:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_1:
                self.can_carry,
            LocationName.hot_head_hop_bonus_2:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_3:
                lambda state: self.has_squitter(state) and self.has_kannons(state),

            LocationName.kannons_klaim_clear:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.kannons_klaim_kong:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.kannons_klaim_dk_coin:
                lambda state: self.can_hover(state),
            LocationName.kannons_klaim_bonus_1:
                lambda state: self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and
                    self.can_hover(state),
            LocationName.kannons_klaim_bonus_2:
                lambda state: self.can_carry(state) and self.can_team_attack(state) and self.has_kannons(state),
            LocationName.kannons_klaim_bonus_3:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.can_hover(state),

            LocationName.lava_lagoon_clear:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_invincibility(state) and
                    self.has_kannons(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_kong:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_invincibility(state) and
                    self.has_kannons(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_dk_coin:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_invincibility(state) and
                    self.has_kannons(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_bonus_1:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_invincibility(state) and
                    self.has_kannons(state) and self.has_enguarde(state) and self.can_carry(state),

            LocationName.red_hot_ride_clear:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_kong:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_dk_coin:
                lambda state: self.can_carry(state) and self.has_rambi(state) and self.can_team_attack(state),
            LocationName.red_hot_ride_bonus_1:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_bonus_2:
                lambda state: self.can_carry(state) and self.has_rambi(state),

            LocationName.squawks_shaft_clear:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state) and self.has_squawks(state),
            LocationName.squawks_shaft_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_bonus_1:
                lambda state: self.has_kannons(state) and self.can_carry(state) and (
                    self.can_cartwheel(state) or 
                    self.can_hover(state)
                ),
            LocationName.squawks_shaft_bonus_2:
                lambda state: self.has_kannons(state) and self.can_team_attack(state),
            LocationName.squawks_shaft_bonus_3:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kleevers_kiln_clear:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_both_kongs(state),
            LocationName.kleever_defeated:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_both_kongs(state),

            LocationName.barrel_bayou_clear:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),
            LocationName.barrel_bayou_kong:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and self.can_cartwheel(state),
            LocationName.barrel_bayou_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_bonus_1:
                lambda state: self.has_controllable_barrels(state) and self.can_carry(state),
            LocationName.barrel_bayou_bonus_2:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and self.can_team_attack(state),

            LocationName.glimmers_galleon_clear:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_kong:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_dk_coin:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_bonus_1:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_bonus_2:
                lambda state: self.can_swim(state) and self.has_glimmer(state),

            LocationName.krockhead_klamber_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.krockhead_klamber_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.krockhead_klamber_dk_coin:
                lambda state: self.can_team_attack(state) and self.can_carry(state) and self.can_cartwheel(state),
            LocationName.krockhead_klamber_bonus_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.has_kannons(state) and 
                    self.has_squitter(state),

            LocationName.rattle_battle_clear:
                self.has_rattly,
            LocationName.rattle_battle_kong:
                self.has_rattly,
            LocationName.rattle_battle_dk_coin:
                lambda state: self.has_rattly(state) and self.has_kannons(state),
            LocationName.rattle_battle_bonus_1:
                lambda state: self.can_team_attack(state) and self.can_hover(state),
            LocationName.rattle_battle_bonus_2:
                self.has_rattly,
            LocationName.rattle_battle_bonus_3:
                self.has_rattly,

            LocationName.slime_climb_clear:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state) and 
                    self.has_kannons(state) and self.can_hover(state),
            LocationName.slime_climb_kong:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),
            LocationName.slime_climb_dk_coin:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state) and 
                    self.can_team_attack(state) and self.has_invincibility(state) and self.can_hover(state),
            LocationName.slime_climb_bonus_1:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state) and 
                    self.has_invincibility(state) and self.can_cling(state) and self.can_cartwheel(state) and self.can_hover(state),
            LocationName.slime_climb_bonus_2:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state) and self.can_hover(state),

            LocationName.bramble_blast_clear:
                self.has_kannons,
            LocationName.bramble_blast_kong:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_bonus_1:
                self.has_kannons,
            LocationName.bramble_blast_bonus_2:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kudgels_kontest_clear:
                lambda state: self.can_carry(state) and self.can_cartwheel(state) and self.can_hover(state) and self.has_diddy(state),
            LocationName.kudgel_defeated:
                lambda state: self.can_carry(state) and self.can_cartwheel(state) and self.can_hover(state) and self.has_diddy(state),

            LocationName.hornet_hole_clear:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_kong:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_dk_coin:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_bonus_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.hornet_hole_bonus_2:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_bonus_3:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),

            LocationName.target_terror_clear:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_kong:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_dk_coin:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_bonus_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_bonus_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_clear:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_kong:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_dk_coin:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_bonus_1:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state) and self.has_squawks(state),

            LocationName.rickety_race_clear:
                self.has_skull_kart,
            LocationName.rickety_race_kong:
                self.has_skull_kart,
            LocationName.rickety_race_dk_coin:
                self.has_skull_kart,
            LocationName.rickety_race_bonus_1:
                lambda state: self.has_skull_kart(state) and self.can_team_attack(state) and self.can_hover(state),

            LocationName.mudhole_marsh_clear:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_invincibility(state),
            LocationName.mudhole_marsh_kong:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_invincibility(state) and
                    self.can_carry(state) and self.can_team_attack(state),
            LocationName.mudhole_marsh_dk_coin:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_invincibility(state) and
                    self.can_hover(state),
            LocationName.mudhole_marsh_bonus_1:
                lambda state: self.can_cling(state) and self.has_invincibility(state) and
                    self.can_carry(state) and self.can_team_attack(state),
            LocationName.mudhole_marsh_bonus_2:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_invincibility(state) and
                    self.can_carry(state),

            LocationName.rambi_rumble_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state) and self.can_hover(state),
            LocationName.rambi_rumble_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),
            LocationName.rambi_rumble_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.rambi_rumble_bonus_1:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_team_attack(state) and self.can_hover(state),
            LocationName.rambi_rumble_bonus_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state) and self.can_hover(state),

            LocationName.king_zing_sting_clear:
                lambda state: self.has_squawks(state) and self.has_both_kongs(state),
            LocationName.king_zing_defeated:
                lambda state: self.has_squawks(state) and self.has_both_kongs(state),

            LocationName.ghostly_grove_clear:
                self.can_climb,
            LocationName.ghostly_grove_kong:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.can_carry(state),
            LocationName.ghostly_grove_dk_coin:
                lambda state: self.can_climb(state) and self.has_kannons(state) and (
                    self.can_cartwheel(state) or self.can_hover(state)
                ),
            LocationName.ghostly_grove_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.ghostly_grove_bonus_2:
                self.can_climb,

            LocationName.haunted_hall_clear:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_kong:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_dk_coin:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_bonus_1:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_bonus_2:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_bonus_3:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),

            LocationName.gusty_glade_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_cartwheel(state),
            LocationName.gusty_glade_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_carry(state) and
                    self.can_cartwheel(state),
            LocationName.gusty_glade_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.gusty_glade_bonus_1:
                lambda state: self.can_team_attack(state) and (self.can_cling(state) or self.has_rattly(state)),
            LocationName.gusty_glade_bonus_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_kannons(state),

            LocationName.parrot_chute_panic_clear:
                self.has_squawks,
            LocationName.parrot_chute_panic_kong:
                self.has_squawks,
            LocationName.parrot_chute_panic_dk_coin:
                self.can_hover,
            LocationName.parrot_chute_panic_bonus_1:
                self.has_squawks,
            LocationName.parrot_chute_panic_bonus_2:
                lambda state: self.has_squawks(state) and self.can_hover(state) and self.can_carry(state),

            LocationName.web_woods_clear:
                self.has_squitter,
            LocationName.web_woods_kong:
                lambda state: self.has_squitter(state) and self.can_team_attack(state),
            LocationName.web_woods_dk_coin:
                lambda state: self.has_squitter(state) and self.has_kannons(state),
            LocationName.web_woods_bonus_1:
                self.has_squitter,
            LocationName.web_woods_bonus_2:
                self.has_squitter,

            LocationName.kreepy_krow_clear:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state) and self.has_both_kongs(state),
            LocationName.kreepy_krow_defeated:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state) and self.has_both_kongs(state),

            LocationName.arctic_abyss_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_kong:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.arctic_abyss_dk_coin:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_bonus_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_bonus_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and self.can_carry(state),

            LocationName.windy_well_clear:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.has_both_kongs(state) and self.can_carry(state),
            LocationName.windy_well_kong:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.has_both_kongs(state) and self.can_carry(state),
            LocationName.windy_well_dk_coin:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.has_both_kongs(state) and self.can_carry(state),
            LocationName.windy_well_bonus_1:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_bonus_2:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.has_squawks(state) and self.has_both_kongs(state),

            LocationName.castle_crush_clear:
                lambda state: self.has_rambi(state) and self.can_cartwheel(state) and self.can_carry(state) and self.has_both_kongs(state),
            LocationName.castle_crush_kong:
                lambda state: self.has_rambi(state) and self.can_cartwheel(state) and self.can_carry(state) and self.has_both_kongs(state),
            LocationName.castle_crush_dk_coin:
                lambda state: self.has_rambi(state) and self.can_cartwheel(state) and self.can_carry(state) and
                    self.has_squawks(state) and self.has_both_kongs(state),
            LocationName.castle_crush_bonus_1:
                lambda state: self.has_rambi(state) and self.can_carry(state) and self.has_both_kongs(state),
            LocationName.castle_crush_bonus_2:
                lambda state: self.has_rambi(state) and self.can_cartwheel(state) and self.can_carry(state) and
                    self.has_squawks(state) and self.has_both_kongs(state),

            LocationName.clappers_cavern_clear:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.clappers_cavern_kong:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.can_team_attack(state) and self.can_hover(state),
            LocationName.clappers_cavern_dk_coin:
                lambda state: self.can_team_attack(state) and self.can_cling(state) and self.can_cartwheel(state),
            LocationName.clappers_cavern_bonus_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state) and self.can_cartwheel(state),
            LocationName.clappers_cavern_bonus_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),

            LocationName.chain_link_chamber_clear:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_kong:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_dk_coin:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_bonus_1:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.chain_link_chamber_bonus_2:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state) and self.can_cartwheel(state),

            LocationName.toxic_tower_clear:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),
            LocationName.toxic_tower_kong:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),
            LocationName.toxic_tower_dk_coin:
                lambda state: self.has_rattly(state) and self.has_kannons(state),
            LocationName.toxic_tower_bonus_1:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),

            LocationName.stronghold_showdown_clear:
                self.true,

            LocationName.screechs_sprint_clear:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_bonus_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.can_carry(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),

            LocationName.k_rool_duel_clear:
                lambda state: self.can_carry(state) and self.can_hover(state) and self.has_diddy(state),

            LocationName.jungle_jinx_clear:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),
            LocationName.jungle_jinx_kong:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.jungle_jinx_dk_coin:
                lambda state: self.can_cartwheel(state) and self.can_team_attack(state),

            LocationName.black_ice_battle_clear:
                self.can_carry,
            LocationName.black_ice_battle_kong:
                self.can_carry,
            LocationName.black_ice_battle_dk_coin:
                lambda state: self.can_carry(state) and self.can_team_attack(state),

            LocationName.klobber_karnage_clear:
                lambda state: self.can_carry(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state),
            LocationName.klobber_karnage_kong:
                lambda state: self.can_carry(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state),
            LocationName.klobber_karnage_dk_coin:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.has_invincibility(state) and 
                    self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and 
                    self.has_controllable_barrels(state),

            LocationName.fiery_furnace_clear:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state)
                    and self.can_team_attack(state),
            LocationName.fiery_furnace_kong:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state)
                    and self.can_team_attack(state),
            LocationName.fiery_furnace_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state)
                    and self.can_team_attack(state),

            LocationName.animal_antics_clear:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_rattly(state) and self.can_swim(state) and 
                    self.has_kannons(state),
            LocationName.animal_antics_kong:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_rattly(state) and self.can_swim(state) and 
                    self.has_kannons(state),
            LocationName.animal_antics_dk_coin:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.can_swim(state),

            LocationName.krocodile_core_clear:
                lambda state: self.can_carry(state) and self.can_hover(state) and self.has_diddy(state),
                
            LocationName.pirate_panic_banana_coin_1:
                self.can_team_attack,
            LocationName.pirate_panic_banana_bunch_1:
                self.true,
            LocationName.pirate_panic_red_balloon:
                self.true,
            LocationName.pirate_panic_banana_coin_2:
                self.can_team_attack,
            LocationName.pirate_panic_banana_coin_3:
                self.true,
            LocationName.pirate_panic_green_balloon:
                self.has_rambi,

            LocationName.mainbrace_mayhem_banana_bunch_1:
                lambda state: self.can_climb(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.mainbrace_mayhem_banana_coin_1:
                self.can_climb,
            LocationName.mainbrace_mayhem_banana_coin_2:
                self.can_climb,
            LocationName.mainbrace_mayhem_green_balloon:
                self.can_climb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_banana_bunch_1:
                lambda state: self.can_cling(state) and (
                    self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state))
                ),
            LocationName.gangplank_galley_banana_bunch_2:
                self.can_carry,
            LocationName.gangplank_galley_red_balloon_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_3:
                lambda state: self.can_cling(state) and self.can_team_attack(state) and self.has_kannons(state),
            LocationName.gangplank_galley_banana_coin_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_4:
                lambda state: self.can_cling(state) and self.has_kannons(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.gangplank_galley_banana_coin_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.gangplank_galley_banana_bunch_5:
                lambda state: self.can_cling(state) and self.has_kannons(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.gangplank_galley_banana_bunch_6:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.gangplank_galley_banana_bunch_7:
                self.can_cling,
            LocationName.gangplank_galley_red_balloon_2:
                 lambda state: self.can_cling(state) and self.has_invincibility(state) and self.can_carry(state),

            LocationName.lockjaws_locker_banana_coin_1:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_1:
                self.true,
            LocationName.lockjaws_locker_banana_coin_2:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_2:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_3:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_4:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_5:
                self.can_swim,
            LocationName.lockjaws_locker_banana_bunch_3:
                self.can_swim,
            LocationName.lockjaws_locker_red_balloon:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.lockjaws_locker_banana_coin_6:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.lockjaws_locker_banana_coin_7:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.lockjaws_locker_banana_coin_8:
                self.can_swim,
            LocationName.lockjaws_locker_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.topsail_trouble_red_balloon_1:
                lambda state: self.has_rattly(state) or (self.can_team_attack(state) and self.can_cling(state)),
            LocationName.topsail_trouble_red_balloon_2:
                lambda state: self.can_carry(state) and (self.has_rattly(state) or (self.can_team_attack(state) and self.can_cling(state))),
            LocationName.topsail_trouble_banana_bunch_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_banana_bunch_2:
                lambda state: self.has_rattly(state) or (self.can_team_attack(state) and self.can_cling(state)),
            LocationName.topsail_trouble_banana_coin_1:
                lambda state: self.has_rattly(state) or (self.can_team_attack(state) and self.can_cling(state)),
            LocationName.topsail_trouble_banana_coin_2:
                self.has_rattly,
            LocationName.topsail_trouble_banana_bunch_3:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_banana_coin_3:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_banana_coin_4:
                lambda state: self.can_climb(state) and self.can_carry(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_blue_balloon:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.krows_nest_banana_coin_1:
                self.can_team_attack,
            LocationName.krows_nest_banana_coin_2:
                self.can_team_attack,

            LocationName.hot_head_hop_green_balloon:
                lambda state: self.can_carry(state) and self.can_team_attack(state),
            LocationName.hot_head_hop_banana_coin_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_bunch_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_coin_2:
                lambda state: self.has_squitter(state) or self.can_team_attack(state),
            LocationName.hot_head_hop_banana_bunch_2:
                self.has_squitter,
            LocationName.hot_head_hop_banana_bunch_3:
                self.has_squitter,
            LocationName.hot_head_hop_banana_coin_3:
                self.has_squitter,
            LocationName.hot_head_hop_banana_coin_4:
                self.has_squitter,
            LocationName.hot_head_hop_red_balloon:
                lambda state: self.has_squitter(state) and self.has_kannons(state),

            LocationName.kannons_klaim_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_hover(state),
            LocationName.kannons_klaim_banana_coin_1:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.kannons_klaim_banana_coin_2:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.kannons_klaim_banana_coin_3:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.can_use_diddy_barrels(state),

            LocationName.lava_lagoon_banana_coin_1:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_bunch_1:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_bunch_2:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_clapper(state) and 
                    self.has_kannons(state) and self.has_invincibility(state),
            LocationName.lava_lagoon_banana_bunch_3:
                lambda state: self.can_swim(state) and self.has_clapper(state) and 
                    self.has_kannons(state) and self.has_invincibility(state),
            LocationName.lava_lagoon_banana_coin_6:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_coin_7:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_red_balloon_1:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state) and self.can_carry(state),
            LocationName.lava_lagoon_banana_bunch_5:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_coin_8:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_coin_9:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_coin_10:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_invincibility(state) and self.has_enguarde(state) and self.can_team_attack(state),

            LocationName.red_hot_ride_banana_bunch_1:
                self.true,
            LocationName.red_hot_ride_banana_coin_1:
                self.can_team_attack,
            LocationName.red_hot_ride_banana_coin_2:
                self.can_team_attack,
            LocationName.red_hot_ride_banana_bunch_2:
                self.can_carry,
            LocationName.red_hot_ride_banana_coin_3:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_bunch_3:
                lambda state: (self.can_carry(state) or self.can_team_attack(state)) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_coin_4:
                lambda state: (self.can_carry(state) or self.can_team_attack(state)) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_coin_5:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_coin_6:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_bunch_4:
                lambda state: self.can_carry(state) and self.has_rambi(state),

            LocationName.squawks_shaft_banana_coin_1:
                self.can_cartwheel,
            LocationName.squawks_shaft_banana_bunch_1:
                self.has_kannons,
            LocationName.squawks_shaft_banana_coin_2:
                lambda state: self.has_kannons(state) and self.can_carry(state) and (
                    self.can_cartwheel(state) or 
                    self.can_hover(state)
                ),
            LocationName.squawks_shaft_banana_bunch_2:
                self.has_kannons,
            LocationName.squawks_shaft_red_balloon_1:
                lambda state: self.has_kannons(state) and self.can_carry(state) and self.can_cartwheel(state), 
            LocationName.squawks_shaft_banana_coin_3:
                lambda state: self.has_kannons(state) and self.can_use_dixie_barrels(state),
            LocationName.squawks_shaft_banana_coin_4:
                lambda state: self.has_kannons(state) and self.can_use_dixie_barrels(state),
            LocationName.squawks_shaft_banana_coin_5:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_coin_6:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_coin_7:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_bunch_3:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_bunch_4:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kleevers_kiln_banana_coin_1:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_both_kongs(state) and 
                    self.can_hover(state),
            LocationName.kleevers_kiln_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_both_kongs(state) and 
                    self.can_hover(state),

            LocationName.barrel_bayou_banana_bunch_1:
                self.can_team_attack,
            LocationName.barrel_bayou_banana_coin_1:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_banana_bunch_2:
                self.has_controllable_barrels,
            LocationName.barrel_bayou_green_balloon:
                lambda state: self.has_controllable_barrels(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.barrel_bayou_banana_coin_2:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),
            LocationName.barrel_bayou_banana_bunch_3:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and self.can_team_attack(state),

            LocationName.glimmers_galleon_banana_coin_1:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_1:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_2:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_3:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_red_balloon:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_5:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_6:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_7:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_8:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_6:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_9:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_10:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_11:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_12:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_7:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_8:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_13:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_9:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_bunch_14:
                lambda state: self.can_swim(state) and self.has_glimmer(state),
            LocationName.glimmers_galleon_banana_coin_10:
                lambda state: self.can_swim(state) and self.has_glimmer(state),

            LocationName.krockhead_klamber_red_balloon_1:
                lambda state: self.can_team_attack(state) and self.can_carry(state),
            LocationName.krockhead_klamber_banana_coin_1:
                lambda state: self.can_team_attack(state) and self.can_cartwheel(state),
            LocationName.krockhead_klamber_banana_coin_2:
                self.can_climb,
            LocationName.krockhead_klamber_red_balloon_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.has_kannons(state) and 
                    self.has_squitter(state),
            LocationName.krockhead_klamber_banana_coin_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),

            LocationName.rattle_battle_banana_coin_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_4:
                self.has_rattly,

            LocationName.slime_climb_banana_coin_1:
                self.can_cartwheel,
            LocationName.slime_climb_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state),
            LocationName.slime_climb_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),
            LocationName.slime_climb_banana_bunch_4:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_swim(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),

            LocationName.bramble_blast_banana_bunch_1:
                self.can_team_attack,
            LocationName.bramble_blast_banana_bunch_2:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_3:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_1:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_4:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_5:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_2:
                self.has_kannons,
            LocationName.bramble_blast_red_balloon:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_6:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_7:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_8:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_9:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.hornet_hole_banana_bunch_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_coin_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_2:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_coin_2:
                self.true,
            LocationName.hornet_hole_green_balloon_1:
                self.can_carry,
            LocationName.hornet_hole_banana_coin_3:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_3:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_coin_4:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_4:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_5:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),
            LocationName.hornet_hole_red_balloon_1:
                lambda state: self.can_hover(state) and self.can_team_attack(state) and self.has_squitter(state) and 
                    self.has_kannons(state) and self.can_cling(state),

            LocationName.target_terror_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_banana_bunch_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_red_balloon:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_banana_bunch_1:
                self.has_kannons,
            LocationName.bramble_scramble_banana_bunch_2:
                 lambda state: self.can_carry(state) and self.has_both_kongs(state) and self.can_climb(state),
            LocationName.bramble_scramble_banana_coin_1:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state),
            LocationName.bramble_scramble_banana_coin_2:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_3:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_3:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_4:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_4:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_5:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_5:
                lambda state: self.can_hover(state) and self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_6:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_banana_coin_7:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_banana_coin_8:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_blue_balloon:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_red_balloon:
                lambda state: self.can_hover(state) and self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),

            LocationName.rickety_race_banana_coin:
                self.has_skull_kart,

            LocationName.mudhole_marsh_banana_coin_1:
                self.true,
            LocationName.mudhole_marsh_banana_bunch_1:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.mudhole_marsh_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state),
            LocationName.mudhole_marsh_banana_coin_3:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state) and self.can_climb(state),
            LocationName.mudhole_marsh_banana_coin_4:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state) and self.can_climb(state) and self.can_cartwheel(state),
            LocationName.mudhole_marsh_banana_coin_5:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state) and self.can_climb(state),

            LocationName.rambi_rumble_banana_coin_1:
                self.can_hover,
            LocationName.rambi_rumble_banana_bunch_1:
                self.can_hover,
            LocationName.rambi_rumble_banana_bunch_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and 
                    self.can_hover(state),
            LocationName.rambi_rumble_banana_coin_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and 
                    self.can_hover(state) and self.can_team_attack(state),
            LocationName.rambi_rumble_banana_bunch_3:
                lambda state: self.can_cling(state) and self.has_kannons(state) and 
                    self.can_hover(state) and self.has_rambi(state),

            LocationName.king_zing_sting_banana_coin_1:
                self.true,
            LocationName.king_zing_sting_banana_coin_2:
                self.true,

            LocationName.ghostly_grove_banana_bunch_1:
                self.true,
            LocationName.ghostly_grove_red_balloon:
                self.can_carry,
            LocationName.ghostly_grove_banana_bunch_2:
                self.true,
            LocationName.ghostly_grove_banana_coin_1:
                lambda state: self.can_climb(state) and self.can_cartwheel(state),
            LocationName.ghostly_grove_banana_bunch_3:
                self.can_climb,
            LocationName.ghostly_grove_banana_bunch_4:
                self.can_climb,
            LocationName.ghostly_grove_banana_coin_2:
                self.can_climb,

            LocationName.haunted_hall_banana_bunch_1:
                self.true,
            LocationName.haunted_hall_banana_bunch_2:
                self.true,
            LocationName.haunted_hall_banana_coin_1:
                self.can_cartwheel,
            LocationName.haunted_hall_banana_coin_2:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),
            LocationName.haunted_hall_banana_coin_3:
                lambda state: self.can_cling(state) and self.has_skull_kart(state),

            LocationName.gusty_glade_banana_coin_1:
                self.can_team_attack,
            LocationName.gusty_glade_banana_coin_2:
                self.can_cartwheel,
            LocationName.gusty_glade_blue_balloon:
                lambda state: self.can_team_attack(state) and self.has_rattly(state),
            LocationName.gusty_glade_banana_coin_3:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_cartwheel(state),

            LocationName.parrot_chute_panic_banana_coin_1:
                lambda state: self.has_squawks(state) and self.can_carry(state),
            LocationName.parrot_chute_panic_banana_coin_2:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_bunch_1:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_3:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_bunch_2:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_4:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_5:
                lambda state: self.has_squawks(state) and self.has_controllable_barrels(state) and self.can_team_attack(state),

            LocationName.web_woods_banana_coin_1:
                self.can_team_attack,
            LocationName.web_woods_banana_coin_2:
                lambda state: self.can_team_attack(state) and self.can_carry(state),
            LocationName.web_woods_green_balloon_1:
                lambda state: self.can_team_attack(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.web_woods_banana_bunch_1:
                self.can_cartwheel,
            LocationName.web_woods_banana_bunch_2:
                self.can_carry,
            LocationName.web_woods_banana_bunch_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_4:
                self.has_squitter,
            LocationName.web_woods_banana_coin_5:
                self.has_squitter,
            LocationName.web_woods_green_balloon_2:
                lambda state: self.has_squitter(state) and self.can_team_attack(state),

            LocationName.kreepy_krow_banana_coin_1:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state) and self.has_both_kongs(state),
            LocationName.kreepy_krow_banana_coin_2:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state) and self.has_both_kongs(state),

            LocationName.arctic_abyss_banana_coin_1:
                lambda state: self.can_team_attack(state) and (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_1:
                lambda state: self.can_team_attack(state) and (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_2:
                lambda state: self.can_team_attack(state) and (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_3:
                lambda state: self.can_team_attack(state) and (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_4:
                self.can_swim,
            LocationName.arctic_abyss_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_5:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_6:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_7:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_red_balloon_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_red_balloon_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.windy_well_banana_coin_1:
                self.can_carry,
            LocationName.windy_well_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_coin_3:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.can_cartwheel(state),
            LocationName.windy_well_banana_bunch_2:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.can_cartwheel(state),
            LocationName.windy_well_banana_coin_4:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_bunch_3:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_red_balloon:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.windy_well_banana_bunch_4:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.has_both_kongs(state) and self.has_squawks(state),

            LocationName.castle_crush_banana_coin_1:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_1:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_2:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_coin_2:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_3:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_4:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_5:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state) and self.can_cartwheel(state) and self.has_squawks(state),
            LocationName.castle_crush_banana_coin_3:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state) and self.can_cartwheel(state),
            LocationName.castle_crush_banana_bunch_6:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state) and self.can_cartwheel(state),

            LocationName.clappers_cavern_banana_coin_1:
                self.has_clapper,
            LocationName.clappers_cavern_banana_bunch_1:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_bunch_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_bunch_3:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_coin_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_bunch_4:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_coin_3:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_team_attack(state) and self.has_invincibility(state),
            LocationName.clappers_cavern_banana_coin_4:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_team_attack(state) and self.has_invincibility(state),
            LocationName.clappers_cavern_banana_coin_5:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_team_attack(state) and self.has_invincibility(state),

            LocationName.chain_link_chamber_banana_coin_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_2:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.chain_link_chamber_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_banana_bunch_4:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),
            LocationName.chain_link_chamber_banana_coin_4:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.has_kannons(state) and 
                    self.has_controllable_barrels(state) and self.has_invincibility(state),

            LocationName.toxic_tower_banana_bunch_1:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_2:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_3:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_4:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_5:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_6:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_7:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_1:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_2:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_3:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_4:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.toxic_tower_banana_coin_5:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.toxic_tower_banana_bunch_8:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.toxic_tower_banana_bunch_9:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.toxic_tower_green_balloon:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_kannons(state) and self.has_squitter(state),

            LocationName.stronghold_showdown_banana_coin_1:
                self.can_team_attack,
            LocationName.stronghold_showdown_red_balloon:
                self.can_team_attack,
            LocationName.stronghold_showdown_banana_coin_2:
                self.can_team_attack,

            LocationName.screechs_sprint_banana_coin_1:
                self.can_cartwheel,
            LocationName.screechs_sprint_banana_bunch_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_carry(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_red_balloon:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_4:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_5:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_6:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_7:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_coin_8:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_bunch_4:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_bunch_5:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.screechs_sprint_banana_bunch_6:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_squawks(state) and (self.has_diddy(state) and self.can_cartwheel(state)),

            LocationName.jungle_jinx_banana_bunch_1:
                self.true,
            LocationName.jungle_jinx_banana_bunch_2:
                self.true,
            LocationName.jungle_jinx_banana_coin_1:
                self.can_hover,
            LocationName.jungle_jinx_banana_coin_2:
                self.can_cartwheel,
            LocationName.jungle_jinx_banana_coin_3:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),
            LocationName.jungle_jinx_banana_coin_4:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state) and self.can_team_attack(state),
            LocationName.jungle_jinx_banana_coin_5:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),

            LocationName.black_ice_battle_banana_bunch_1:
                lambda state: self.can_carry(state) and self.can_cartwheel(state),
            LocationName.black_ice_battle_red_balloon_1:
                self.can_carry,
            LocationName.black_ice_battle_red_balloon_2:
                self.can_carry,
            LocationName.black_ice_battle_red_balloon_3:
                self.can_carry,
            LocationName.black_ice_battle_banana_bunch_2:
                self.can_carry,
            LocationName.black_ice_battle_banana_coin_1:
                self.can_carry,
            LocationName.black_ice_battle_banana_bunch_3:
                lambda state: self.can_carry(state) and self.can_team_attack(state),

            LocationName.klobber_karnage_banana_coin_1:
                self.true,
            LocationName.klobber_karnage_banana_bunch_1:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_bunch_2:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_coin_2:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_bunch_3:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_coin_3:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.has_controllable_barrels(state),
            LocationName.klobber_karnage_banana_bunch_4:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state),
            LocationName.klobber_karnage_banana_bunch_5:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_banana_bunch_6:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_banana_bunch_7:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_banana_coin_4:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_red_balloon:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),

            LocationName.fiery_furnace_banana_bunch_1:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_2:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_3:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_4:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state),
            LocationName.fiery_furnace_banana_coin_1:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),
            LocationName.fiery_furnace_banana_coin_2:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),
            LocationName.fiery_furnace_banana_bunch_5:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),

            LocationName.animal_antics_banana_bunch_1:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state),
            LocationName.animal_antics_banana_bunch_2:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state),
            LocationName.animal_antics_banana_coin_1:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state),
            LocationName.animal_antics_banana_coin_2:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_bunch_3:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_bunch_4:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_3:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_4:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_red_balloon:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_5:
                lambda state: self.has_both_kongs(state) and self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state)  and self.has_kannons(state) and self.has_rattly(state),
        }



class DKC2LooseRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                lambda state: self.can_carry(state) or self.has_rambi(state),

            LocationName.mainbrace_mayhem_clear:
                self.can_climb,
            LocationName.mainbrace_mayhem_kong:
                self.can_climb,
            LocationName.mainbrace_mayhem_dk_coin:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_bonus_1:
                lambda state: self.can_climb(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.mainbrace_mayhem_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.mainbrace_mayhem_bonus_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_clear:
                self.can_cling,
            LocationName.gangplank_galley_kong:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state),
            LocationName.gangplank_galley_dk_coin:
                lambda state: self.can_cling(state) and (
                    self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state))
                ),
            LocationName.gangplank_galley_bonus_1:
                self.can_carry,
            LocationName.gangplank_galley_bonus_2:
                lambda state: self.can_cling(state) and self.has_invincibility(state),

            LocationName.lockjaws_locker_clear:
                self.can_swim,
            LocationName.lockjaws_locker_kong:
                self.can_swim,
            LocationName.lockjaws_locker_dk_coin:
                self.can_swim,
            LocationName.lockjaws_locker_bonus_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.topsail_trouble_clear:
                lambda state: self.can_climb(state) and (
                    (self.can_team_attack(state) or self.has_rattly(state))
                ),
            LocationName.topsail_trouble_kong:
                lambda state: self.can_climb(state) and (
                    (self.can_team_attack(state) or self.has_rattly(state))
                ),
            LocationName.topsail_trouble_dk_coin:
                lambda state: self.can_climb(state) and (
                    (self.can_team_attack(state) or self.has_rattly(state))
                ),
            LocationName.topsail_trouble_bonus_1:
                lambda state: self.can_team_attack(state) or self.has_rattly(state),
            LocationName.topsail_trouble_bonus_2:
                lambda state: self.can_climb(state) and (
                    (self.can_team_attack(state) or self.has_rattly(state))
                ),

            LocationName.krows_nest_clear:
                self.can_carry,
            LocationName.krow_defeated:
                self.can_carry,

            LocationName.hot_head_hop_clear:
                lambda state: self.has_kannons(state) or self.has_squitter(state),
            LocationName.hot_head_hop_kong:
                lambda state: self.can_carry(state) and (
                    self.can_team_attack(state) or
                    self.has_squitter(state)
                ),
            LocationName.hot_head_hop_dk_coin:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_1:
                self.can_carry,
            LocationName.hot_head_hop_bonus_2:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_3:
                self.has_squitter,

            LocationName.kannons_klaim_clear:
                self.has_kannons,
            LocationName.kannons_klaim_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.kannons_klaim_dk_coin:
                lambda state: self.can_hover(state) or self.can_cartwheel(state),
            LocationName.kannons_klaim_bonus_1:
                lambda state: self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.kannons_klaim_bonus_2:
                self.has_kannons,
            LocationName.kannons_klaim_bonus_3:
                self.has_kannons,

            LocationName.lava_lagoon_clear:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.lava_lagoon_kong:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.lava_lagoon_dk_coin:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.lava_lagoon_bonus_1:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.has_enguarde(state) and self.can_carry(state),

            LocationName.red_hot_ride_clear:
                self.true,
            LocationName.red_hot_ride_kong:
                self.can_carry,
            LocationName.red_hot_ride_dk_coin:
                lambda state: self.can_carry(state) and self.can_team_attack(state),
            LocationName.red_hot_ride_bonus_1:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_bonus_2:
                self.true,

            LocationName.squawks_shaft_clear:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state) and self.has_squawks(state),
            LocationName.squawks_shaft_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_bonus_1:
                lambda state: self.has_kannons(state) and self.can_carry(state) and (
                    self.can_cartwheel(state) or 
                    self.can_hover(state)
                ),
            LocationName.squawks_shaft_bonus_2:
                lambda state: self.has_kannons(state) and self.can_team_attack(state),
            LocationName.squawks_shaft_bonus_3:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kleevers_kiln_clear:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.kleever_defeated:
                lambda state: self.can_cling(state) and self.can_carry(state),

            LocationName.barrel_bayou_clear:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),
            LocationName.barrel_bayou_kong:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and 
                    self.can_cartwheel(state),
            LocationName.barrel_bayou_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_bonus_1:
                lambda state: self.has_controllable_barrels(state) and self.can_carry(state),
            LocationName.barrel_bayou_bonus_2:
                lambda state: self.has_controllable_barrels(state) and
                    self.has_kannons(state) and self.can_team_attack(state),

            LocationName.glimmers_galleon_clear:
                self.can_swim,
            LocationName.glimmers_galleon_kong:
                self.can_swim,
            LocationName.glimmers_galleon_dk_coin:
                self.can_swim,
            LocationName.glimmers_galleon_bonus_1:
                self.can_swim,
            LocationName.glimmers_galleon_bonus_2:
                self.can_swim,

            LocationName.krockhead_klamber_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.krockhead_klamber_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.krockhead_klamber_dk_coin:
                lambda state: self.can_team_attack(state) and self.can_carry(state) and self.can_cartwheel(state),
            LocationName.krockhead_klamber_bonus_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.has_squitter(state),

            LocationName.rattle_battle_clear:
                self.has_rattly,
            LocationName.rattle_battle_kong:
                self.has_rattly,
            LocationName.rattle_battle_dk_coin:
                lambda state: self.has_rattly(state) and self.has_kannons(state),
            LocationName.rattle_battle_bonus_1:
                lambda state: self.can_team_attack(state) and
                    (self.can_hover(state) or self.can_cartwheel(state)),
            LocationName.rattle_battle_bonus_2:
                self.has_rattly,
            LocationName.rattle_battle_bonus_3:
                self.has_rattly,

            LocationName.slime_climb_clear:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.has_kannons(state),
            LocationName.slime_climb_kong:
                lambda state: self.can_climb(state) and self.can_swim(state) and  
                    (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.slime_climb_dk_coin:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state),
            LocationName.slime_climb_bonus_1:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.has_invincibility(state) and 
                    self.can_cling(state) and self.can_cartwheel(state),
            LocationName.slime_climb_bonus_2:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.can_carry(state),

            LocationName.bramble_blast_clear:
                self.has_kannons,
            LocationName.bramble_blast_kong:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_bonus_1:
                self.has_kannons,
            LocationName.bramble_blast_bonus_2:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kudgels_kontest_clear:
                self.can_carry,
            LocationName.kudgel_defeated:
                self.can_carry,

            LocationName.hornet_hole_clear:
                self.can_cling,
            LocationName.hornet_hole_kong:
                self.can_cling,
            LocationName.hornet_hole_dk_coin:
                lambda state: self.can_cling(state) and self.has_squitter(state) and self.can_team_attack(state),
            LocationName.hornet_hole_bonus_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.hornet_hole_bonus_2:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_bonus_3:
                lambda state: self.can_cling(state) and self.has_squitter(state) and self.can_team_attack(state),

            LocationName.target_terror_clear:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_kong:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_dk_coin:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_bonus_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_bonus_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_clear:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_kong:
                lambda state: self.can_climb(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_dk_coin:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_bonus_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state) and self.has_squawks(state),

            LocationName.rickety_race_clear:
                self.has_skull_kart,
            LocationName.rickety_race_kong:
                self.has_skull_kart,
            LocationName.rickety_race_dk_coin:
                self.has_skull_kart,
            LocationName.rickety_race_bonus_1:
                lambda state: self.has_skull_kart(state) and self.can_team_attack(state) and (
                    self.can_hover(state) or 
                    (self.has_diddy(state) and self.can_cartwheel(state))
                ),

            LocationName.mudhole_marsh_clear:
                lambda state: self.can_climb(state) and self.can_cling(state),
            LocationName.mudhole_marsh_kong:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.can_team_attack(state),
            LocationName.mudhole_marsh_dk_coin:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_hover(state),
            LocationName.mudhole_marsh_bonus_1:
                lambda state: self.can_cling(state) and self.can_carry(state) and 
                    self.can_team_attack(state),
            LocationName.mudhole_marsh_bonus_2:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_carry(state),

            LocationName.rambi_rumble_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state),
            LocationName.rambi_rumble_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state) and 
                    self.can_cartwheel(state),
            LocationName.rambi_rumble_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.rambi_rumble_bonus_1:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_team_attack(state),
            LocationName.rambi_rumble_bonus_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state),

            LocationName.king_zing_sting_clear:
                self.has_squawks,
            LocationName.king_zing_defeated:
                self.has_squawks,

            LocationName.ghostly_grove_clear:
                self.can_climb,
            LocationName.ghostly_grove_kong:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.can_carry(state),
            LocationName.ghostly_grove_dk_coin:
                lambda state: self.can_climb(state) and self.has_kannons(state) and (
                    self.can_cartwheel(state) or self.can_hover(state)
                ),
            LocationName.ghostly_grove_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.ghostly_grove_bonus_2:
                self.can_climb,

            LocationName.haunted_hall_clear:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_kong:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_dk_coin:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_bonus_1:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_bonus_2:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_bonus_3:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),

            LocationName.gusty_glade_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_carry(state) and
                    self.can_cartwheel(state),
            LocationName.gusty_glade_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.gusty_glade_bonus_1:
                lambda state: self.can_team_attack(state) and (self.can_cling(state) or self.has_rattly(state)),
            LocationName.gusty_glade_bonus_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_kannons(state),

            LocationName.parrot_chute_panic_clear:
                self.has_squawks,
            LocationName.parrot_chute_panic_kong:
                self.has_squawks,
            LocationName.parrot_chute_panic_dk_coin:
                lambda state: self.can_cartwheel(state) or self.can_hover(state),
            LocationName.parrot_chute_panic_bonus_1:
                self.has_squawks,
            LocationName.parrot_chute_panic_bonus_2:
                lambda state: self.has_squawks(state) and self.can_cartwheel(state) and self.can_carry(state),

            LocationName.web_woods_clear:
                self.has_squitter,
            LocationName.web_woods_kong:
                lambda state: self.has_squitter(state) and self.can_team_attack(state),
            LocationName.web_woods_dk_coin:
                lambda state: self.has_squitter(state) and (self.can_team_attack(state) or self.has_kannons(state)),
            LocationName.web_woods_bonus_1:
                self.has_squitter,
            LocationName.web_woods_bonus_2:
                self.has_squitter,

            LocationName.kreepy_krow_clear:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),
            LocationName.kreepy_krow_defeated:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),

            LocationName.arctic_abyss_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_kong:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and (
                    self.can_cartwheel(state) or self.can_hover(state)
                ),
            LocationName.arctic_abyss_dk_coin:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_bonus_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_bonus_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and self.can_carry(state),

            LocationName.windy_well_clear:
                lambda state: self.has_kannons(state) and self.can_cling(state),
            LocationName.windy_well_kong:
                lambda state: self.has_kannons(state) and self.can_cling(state),
            LocationName.windy_well_dk_coin:
                lambda state: self.has_kannons(state) and self.can_cling(state),
            LocationName.windy_well_bonus_1:
                self.can_cling,
            LocationName.windy_well_bonus_2:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state) and 
                    self.has_squawks(state),

            LocationName.castle_crush_clear:
                lambda state: self.can_cartwheel(state) or (self.has_rambi(state) and self.can_carry(state) and self.has_both_kongs(state)),
            LocationName.castle_crush_kong:
                lambda state: self.can_cartwheel(state) or (self.has_rambi(state) and self.can_carry(state) and self.has_both_kongs(state)),
            LocationName.castle_crush_dk_coin:
                lambda state: self.can_cartwheel(state) and self.has_squawks(state),
            LocationName.castle_crush_bonus_1:
                lambda state: self.has_rambi(state) and self.can_carry(state) and self.has_both_kongs(state),
            LocationName.castle_crush_bonus_2:
                lambda state: self.can_cartwheel(state) and self.can_carry(state) and self.has_squawks(state) and self.has_both_kongs(state),

            LocationName.clappers_cavern_clear:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.can_cling(state),
            LocationName.clappers_cavern_kong:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.can_cling(state),
            LocationName.clappers_cavern_dk_coin:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.clappers_cavern_bonus_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.clappers_cavern_bonus_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),

            LocationName.chain_link_chamber_clear:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or 
                    (self.has_controllable_barrels(state) and self.has_kannons(state))
                ),
            LocationName.chain_link_chamber_kong:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or 
                    (self.has_controllable_barrels(state) and self.has_kannons(state))
                ),
            LocationName.chain_link_chamber_dk_coin:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or 
                    (self.has_controllable_barrels(state) and self.has_kannons(state))
                ),
            LocationName.chain_link_chamber_bonus_1:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.chain_link_chamber_bonus_2:
                lambda state: self.can_climb(state) and self.has_controllable_barrels(state) and (
                    (self.can_cling(state) or self.has_kannons(state)) and 
                    (self.can_cartwheel(state) or self.can_team_attack(state))
                ),

            LocationName.toxic_tower_clear:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),
            LocationName.toxic_tower_kong:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),
            LocationName.toxic_tower_dk_coin:
                lambda state: self.has_rattly(state) and self.has_kannons(state),
            LocationName.toxic_tower_bonus_1:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and self.has_squitter(state) and 
                    self.has_kannons(state),

            LocationName.stronghold_showdown_clear:
                self.true,

            LocationName.screechs_sprint_clear:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_bonus_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.can_carry(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),

            LocationName.k_rool_duel_clear:
                self.can_carry,

            LocationName.jungle_jinx_clear:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),
            LocationName.jungle_jinx_kong:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.jungle_jinx_dk_coin:
                lambda state: self.can_cartwheel(state) and self.can_team_attack(state),

            LocationName.black_ice_battle_kong:
                self.can_carry,
            LocationName.black_ice_battle_dk_coin:
                self.can_carry,

            LocationName.klobber_karnage_clear:
                lambda state: self.can_carry(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state),
            LocationName.klobber_karnage_kong:
                lambda state: self.can_carry(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state),
            LocationName.klobber_karnage_dk_coin:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.has_invincibility(state) and 
                    self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and 
                    self.has_controllable_barrels(state),

            LocationName.fiery_furnace_clear:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state),
            LocationName.fiery_furnace_kong:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state)
                    and self.can_team_attack(state),
            LocationName.fiery_furnace_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.can_cartwheel(state)
                    and self.can_team_attack(state),

            LocationName.animal_antics_clear:
                lambda state: self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_rattly(state) and self.can_swim(state) and 
                    self.has_kannons(state),
            LocationName.animal_antics_kong:
                lambda state: self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_rattly(state) and self.can_swim(state) and 
                    self.has_kannons(state),
            LocationName.animal_antics_dk_coin:
                lambda state: self.has_rambi(state) and self.has_enguarde(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.can_swim(state),

            LocationName.krocodile_core_clear:
                self.can_carry,
                
            LocationName.pirate_panic_banana_coin_1:
                self.can_team_attack,
            LocationName.pirate_panic_banana_bunch_1:
                self.true,
            LocationName.pirate_panic_red_balloon:
                self.true,
            LocationName.pirate_panic_banana_coin_2:
                self.can_team_attack,
            LocationName.pirate_panic_banana_coin_3:
                self.true,
            LocationName.pirate_panic_green_balloon:
                self.has_rambi,

            LocationName.mainbrace_mayhem_banana_bunch_1:
                lambda state: self.can_climb(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.mainbrace_mayhem_banana_coin_1:
                self.can_climb,
            LocationName.mainbrace_mayhem_banana_coin_2:
                self.can_climb,
            LocationName.mainbrace_mayhem_green_balloon: 
                self.can_climb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_banana_bunch_1:
                lambda state: self.can_cling(state) and (
                    self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state))
                ),
            LocationName.gangplank_galley_banana_bunch_2:
                self.can_carry,
            LocationName.gangplank_galley_red_balloon_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_3:
                lambda state: self.can_team_attack(state) and self.has_kannons(state),
            LocationName.gangplank_galley_banana_coin_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_4:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gangplank_galley_banana_coin_2:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gangplank_galley_banana_bunch_5:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gangplank_galley_banana_bunch_6:
                lambda state: self.can_carry(state) and (self.can_cling(state) or self.can_hover(state) or self.can_cartwheel(state)) ,
            LocationName.gangplank_galley_banana_bunch_7:
                lambda state: self.can_hover(state) or self.can_cling(state),
            LocationName.gangplank_galley_red_balloon_2:
                 lambda state: self.can_cling(state) and self.can_carry(state) and (self.can_team_attack(state) or self.has_invincibility(state)) ,

            LocationName.lockjaws_locker_banana_coin_1:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_1:
                self.true,
            LocationName.lockjaws_locker_banana_coin_2:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_2:
                lambda state: self.can_swim(state) or self.can_hover(state) or self.can_cartwheel(state),
            LocationName.lockjaws_locker_banana_coin_3:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_4:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_5:
                self.can_swim,
            LocationName.lockjaws_locker_banana_bunch_3:
                self.can_swim,
            LocationName.lockjaws_locker_red_balloon:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.lockjaws_locker_banana_coin_6:
                lambda state: self.can_swim(state),
            LocationName.lockjaws_locker_banana_coin_7:
                lambda state: self.can_swim(state),
            LocationName.lockjaws_locker_banana_coin_8:
                self.can_swim,
            LocationName.lockjaws_locker_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.topsail_trouble_red_balloon_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state) or self.can_cling(state),
            LocationName.topsail_trouble_red_balloon_2:
                lambda state: self.can_carry(state) and (
                    self.has_rattly(state) or self.can_team_attack(state) or self.can_cling(state)
                ),
            LocationName.topsail_trouble_banana_bunch_1:
                lambda state: self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ,
            LocationName.topsail_trouble_banana_bunch_2:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.topsail_trouble_banana_coin_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.topsail_trouble_banana_coin_2:
                self.has_rattly,
            LocationName.topsail_trouble_banana_bunch_3:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_banana_coin_3:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_banana_coin_4:
                lambda state: self.can_climb(state) and self.can_carry(state) and (
                    self.can_team_attack(state) or
                    self.has_rattly(state) or 
                    (self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_blue_balloon:
                lambda state: self.can_climb(state) and self.can_team_attack(state) ,

            LocationName.krows_nest_banana_coin_1:
                self.can_team_attack,
            LocationName.krows_nest_banana_coin_2:
                self.can_team_attack,

            LocationName.hot_head_hop_green_balloon:
                lambda state: self.can_carry(state) and self.can_team_attack(state),
            LocationName.hot_head_hop_banana_coin_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_bunch_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_coin_2:
                lambda state: self.has_squitter(state) or self.can_team_attack(state),
            LocationName.hot_head_hop_banana_bunch_2:
                self.has_squitter,
            LocationName.hot_head_hop_banana_bunch_3:
                self.has_squitter,
            LocationName.hot_head_hop_banana_coin_3:
                self.has_squitter,
            LocationName.hot_head_hop_banana_coin_4:
                self.has_squitter,
            LocationName.hot_head_hop_red_balloon:
                self.has_squitter,

            LocationName.kannons_klaim_banana_bunch_1:
                lambda state: self.has_kannons(state) or self.can_team_attack(state),
            LocationName.kannons_klaim_banana_coin_1:
                lambda state: self.has_kannons(state),
            LocationName.kannons_klaim_banana_coin_2:
                lambda state: self.has_kannons(state) and (self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.kannons_klaim_banana_coin_3:
                lambda state: self.has_kannons(state) and self.can_use_diddy_barrels(state),

            LocationName.lava_lagoon_banana_coin_1:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_bunch_1:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_bunch_2:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_clapper(state) and 
                    self.has_kannons(state) and self.has_invincibility(state),
            LocationName.lava_lagoon_banana_bunch_3:
                lambda state: self.can_swim(state) and self.has_clapper(state) and 
                    self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_6:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_7:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_red_balloon_1:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and self.can_carry(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_bunch_5:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_8:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_9:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state),
            LocationName.lava_lagoon_banana_coin_10:
                lambda state: self.can_swim(state) and self.has_clapper(state) and self.has_kannons(state) and 
                    self.can_team_attack(state),

            LocationName.red_hot_ride_banana_bunch_1:
                self.true,
            LocationName.red_hot_ride_banana_coin_1:
                self.true,
            LocationName.red_hot_ride_banana_coin_2:
                self.true,
            LocationName.red_hot_ride_banana_bunch_2:
                self.can_carry,
            LocationName.red_hot_ride_banana_coin_3:
                lambda state: self.can_carry(state) or self.has_rambi(state),
            LocationName.red_hot_ride_banana_bunch_3:
                self.true,
            LocationName.red_hot_ride_banana_coin_4:
                self.true,
            LocationName.red_hot_ride_banana_coin_5:
                lambda state: self.can_carry(state) and self.has_rambi(state),
            LocationName.red_hot_ride_banana_coin_6:
                lambda state: self.can_carry(state),
            LocationName.red_hot_ride_banana_bunch_4:
                self.true,

            LocationName.squawks_shaft_banana_coin_1:
                self.can_cartwheel,
            LocationName.squawks_shaft_banana_bunch_1:
                self.has_kannons,
            LocationName.squawks_shaft_banana_coin_2:
                lambda state: self.has_kannons(state) and self.can_carry(state) and (
                    self.can_cartwheel(state) or 
                    self.can_hover(state)
                ),
            LocationName.squawks_shaft_banana_bunch_2:
                self.has_kannons,
            LocationName.squawks_shaft_red_balloon_1:
                lambda state: self.has_kannons(state) and self.can_carry(state) and self.can_cartwheel(state), 
            LocationName.squawks_shaft_banana_coin_3:
                lambda state: self.has_kannons(state) and self.can_use_dixie_barrels(state),
            LocationName.squawks_shaft_banana_coin_4:
                lambda state: self.has_kannons(state) and self.can_use_dixie_barrels(state),
            LocationName.squawks_shaft_banana_coin_5:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_coin_6:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_coin_7:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_bunch_3:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_banana_bunch_4:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kleevers_kiln_banana_coin_1:
                lambda state: self.can_cling(state) and self.can_carry(state) and 
                    self.can_hover(state),
            LocationName.kleevers_kiln_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and 
                    self.can_hover(state),

            LocationName.barrel_bayou_banana_bunch_1:
                self.can_team_attack,
            LocationName.barrel_bayou_banana_coin_1:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_banana_bunch_2:
                self.has_controllable_barrels,
            LocationName.barrel_bayou_green_balloon:
                lambda state: self.has_controllable_barrels(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.barrel_bayou_banana_coin_2:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),
            LocationName.barrel_bayou_banana_bunch_3:
                lambda state: self.has_controllable_barrels(state) and 
                    self.has_kannons(state) and self.can_team_attack(state),

            LocationName.glimmers_galleon_banana_coin_1:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_2:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_1:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_2:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_3:
                self.can_swim,
            LocationName.glimmers_galleon_red_balloon:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_4:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_3:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_5:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_4:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_6:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_7:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_5:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_8:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_6:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_9:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_10:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_11:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_12:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_7:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_8:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_13:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_9:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_14:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_10:
                self.can_swim,

            LocationName.krockhead_klamber_red_balloon_1:
                lambda state: self.can_team_attack(state) and self.can_carry(state),
            LocationName.krockhead_klamber_banana_coin_1:
                lambda state: self.can_team_attack(state) and self.can_cartwheel(state),
            LocationName.krockhead_klamber_banana_coin_2:
                self.can_climb,
            LocationName.krockhead_klamber_red_balloon_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.has_squitter(state),
            LocationName.krockhead_klamber_banana_coin_3:
                self.can_climb,

            LocationName.rattle_battle_banana_coin_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_4:
                self.has_rattly,

            LocationName.slime_climb_banana_coin_1:
                self.can_cartwheel,
            LocationName.slime_climb_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_1:
                lambda state: self.can_climb(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_swim(state),
            LocationName.slime_climb_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_swim(state) and 
                    self.can_cartwheel(state),
            LocationName.slime_climb_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_swim(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),
            LocationName.slime_climb_banana_bunch_4:
                lambda state: self.can_climb(state) and self.can_swim(state) and 
                    self.can_cartwheel(state) and self.can_hover(state),

            LocationName.bramble_blast_banana_bunch_1:
                self.can_team_attack,
            LocationName.bramble_blast_banana_bunch_2:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_3:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_1:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_4:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_5:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_2:
                self.has_kannons,
            LocationName.bramble_blast_red_balloon:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_6:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_7:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_8:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_9:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.hornet_hole_banana_bunch_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_coin_1:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_2:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_banana_coin_2:
                self.true,
            LocationName.hornet_hole_green_balloon_1:
                self.can_carry,
            LocationName.hornet_hole_banana_coin_3:
                self.true,
            LocationName.hornet_hole_banana_bunch_3:
                lambda state: self.can_team_attack(state) and self.has_squitter(state) and 
                    self.can_cling(state),
            LocationName.hornet_hole_banana_coin_4:
                lambda state: self.can_team_attack(state) and self.has_squitter(state) and 
                    self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_4:
                lambda state: self.can_team_attack(state) and self.has_squitter(state) and 
                    self.can_cling(state),
            LocationName.hornet_hole_banana_bunch_5:
                lambda state: self.can_team_attack(state) and self.can_cling(state),
            LocationName.hornet_hole_red_balloon_1:
                lambda state: self.can_team_attack(state) and self.has_squitter(state) and 
                    self.can_cling(state),

            LocationName.target_terror_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_banana_bunch_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_red_balloon:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_banana_bunch_1:
                self.true,
            LocationName.bramble_scramble_banana_bunch_2:
                lambda state: self.can_carry(state) and self.has_both_kongs(state) and self.can_climb(state),
            LocationName.bramble_scramble_banana_coin_1:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state),
            LocationName.bramble_scramble_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and
                    self.has_invincibility(state) and self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_3:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_3:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_4:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_4:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_5:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_5:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_6:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_7:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_8:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state),
            LocationName.bramble_scramble_blue_balloon:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state),
            LocationName.bramble_scramble_red_balloon:
                lambda state: self.can_cartwheel(state) and self.can_climb(state) and 
                    self.has_squitter(state) and self.has_squawks(state),

            LocationName.rickety_race_banana_coin:
                self.has_skull_kart,

            LocationName.mudhole_marsh_banana_coin_1:
                self.true,
            LocationName.mudhole_marsh_banana_bunch_1:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.mudhole_marsh_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.has_invincibility(state),
            LocationName.mudhole_marsh_banana_coin_3:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.can_climb(state),
            LocationName.mudhole_marsh_banana_coin_4:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.can_climb(state) and self.can_cartwheel(state),
            LocationName.mudhole_marsh_banana_coin_5:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state) and 
                    self.can_climb(state),

            LocationName.rambi_rumble_banana_coin_1:
                self.true,
            LocationName.rambi_rumble_banana_bunch_1:
                lambda state: self.can_hover(state) or self.can_cartwheel(state),
            LocationName.rambi_rumble_banana_bunch_2:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.rambi_rumble_banana_coin_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_team_attack(state),
            LocationName.rambi_rumble_banana_bunch_3:
                lambda state: self.can_cling(state) and self.has_kannons(state) and 
                    self.has_rambi(state),

            LocationName.king_zing_sting_banana_coin_1:
                self.true,
            LocationName.king_zing_sting_banana_coin_2:
                self.true,

            LocationName.ghostly_grove_banana_bunch_1:
                self.true,
            LocationName.ghostly_grove_red_balloon:
                self.can_carry,
            LocationName.ghostly_grove_banana_bunch_2:
                self.true,
            LocationName.ghostly_grove_banana_coin_1:
                lambda state: self.can_climb(state) and self.can_cartwheel(state),
            LocationName.ghostly_grove_banana_bunch_3:
                self.can_climb,
            LocationName.ghostly_grove_banana_bunch_4:
                self.can_climb,
            LocationName.ghostly_grove_banana_coin_2:
                self.can_climb,

            LocationName.haunted_hall_banana_bunch_1:
                self.true,
            LocationName.haunted_hall_banana_bunch_2:
                self.true,
            LocationName.haunted_hall_banana_coin_1:
                self.can_cartwheel,
            LocationName.haunted_hall_banana_coin_2:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),
            LocationName.haunted_hall_banana_coin_3:
                lambda state: self.has_skull_kart(state) and (
                    self.can_cartwheel(state) or self.can_hover(state) or self.can_cling(state) or 
                    self.can_team_attack(state)
                ),

            LocationName.gusty_glade_banana_coin_1:
                self.can_team_attack,
            LocationName.gusty_glade_banana_coin_2:
                self.can_cartwheel,
            LocationName.gusty_glade_blue_balloon:
                lambda state: self.can_team_attack(state) and self.has_rattly(state),
            LocationName.gusty_glade_banana_coin_3:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_cartwheel(state),

            LocationName.parrot_chute_panic_banana_coin_1:
                lambda state: self.has_squawks(state) and self.can_carry(state),
            LocationName.parrot_chute_panic_banana_coin_2:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_bunch_1:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_3:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_bunch_2:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_4:
                self.has_squawks,
            LocationName.parrot_chute_panic_banana_coin_5:
                lambda state: self.has_squawks(state) and self.has_controllable_barrels(state)
                    and (self.can_team_attack(state) or self.can_cartwheel(state)),

            LocationName.web_woods_banana_coin_1:
                self.can_team_attack,
            LocationName.web_woods_banana_coin_2:
                lambda state: self.can_team_attack(state) and self.can_carry(state),
            LocationName.web_woods_green_balloon_1:
                lambda state: self.can_team_attack(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.web_woods_banana_bunch_1:
                lambda state: self.can_team_attack(state) or self.can_cartwheel(state),
            LocationName.web_woods_banana_bunch_2:
                self.can_carry,
            LocationName.web_woods_banana_bunch_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_4:
                self.has_squitter,
            LocationName.web_woods_banana_coin_5:
                self.has_squitter,
            LocationName.web_woods_green_balloon_2:
                lambda state: self.has_squitter(state) and self.can_team_attack(state),

            LocationName.kreepy_krow_banana_coin_1:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),
            LocationName.kreepy_krow_banana_coin_2:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),

            LocationName.arctic_abyss_banana_coin_1:
                lambda state: self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.arctic_abyss_banana_bunch_1:
                lambda state: self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.arctic_abyss_banana_bunch_2:
                lambda state: self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.arctic_abyss_banana_bunch_3:
                lambda state: self.can_hover(state) or (self.has_diddy(state) and self.can_cartwheel(state)),
            LocationName.arctic_abyss_banana_bunch_4:
                self.can_swim,
            LocationName.arctic_abyss_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_5:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_6:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_banana_bunch_7:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_red_balloon_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.arctic_abyss_red_balloon_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.windy_well_banana_coin_1:
                self.true,
            LocationName.windy_well_banana_coin_2:
                self.can_cling,
            LocationName.windy_well_banana_coin_3:
                self.can_cling,
            LocationName.windy_well_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_bunch_2:
                lambda state: self.has_kannons(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_coin_4:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_bunch_3:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_red_balloon:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.windy_well_banana_bunch_4:
                lambda state: self.can_cling(state) and self.can_carry(state) and 
                    self.has_squawks(state),

            LocationName.castle_crush_banana_coin_1:
                self.true,
            LocationName.castle_crush_banana_bunch_1:
                self.true,
            LocationName.castle_crush_banana_bunch_2:
                self.true,
            LocationName.castle_crush_banana_coin_2:
                self.true,
            LocationName.castle_crush_banana_bunch_3:
                lambda state: self.has_rambi(state) and self.can_carry(state) and 
                    self.has_both_kongs(state),
            LocationName.castle_crush_banana_bunch_4:
                self.true,
            LocationName.castle_crush_banana_bunch_5:
                lambda state: self.can_cartwheel(state) and self.has_squawks(state),
            LocationName.castle_crush_banana_coin_3:
                lambda state: self.can_carry(state) and 
                    self.has_both_kongs(state) and self.can_cartwheel(state),
            LocationName.castle_crush_banana_bunch_6:
                lambda state: self.can_carry(state) and 
                    self.has_both_kongs(state) and self.can_cartwheel(state),

            LocationName.clappers_cavern_banana_coin_1:
                self.has_clapper,
            LocationName.clappers_cavern_banana_bunch_1:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state),
            LocationName.clappers_cavern_banana_bunch_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state),
            LocationName.clappers_cavern_banana_bunch_3:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state),
            LocationName.clappers_cavern_banana_coin_2:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state),
            LocationName.clappers_cavern_banana_bunch_4:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.has_enguarde(state),
            LocationName.clappers_cavern_banana_coin_3:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.can_team_attack(state) and self.has_invincibility(state),
            LocationName.clappers_cavern_banana_coin_4:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.can_team_attack(state) and self.has_invincibility(state),
            LocationName.clappers_cavern_banana_coin_5:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_kannons(state) and 
                    self.can_team_attack(state) and self.has_invincibility(state),

            LocationName.chain_link_chamber_banana_coin_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_2:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.chain_link_chamber_banana_coin_2:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_bunch_4:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_coin_3:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_coin_4:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            
            LocationName.toxic_tower_banana_bunch_1:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_2:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_3:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_4:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_5:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_6:
                self.has_rattly,
            LocationName.toxic_tower_banana_bunch_7:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_1:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_2:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_3:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_4:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_coin_5:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_bunch_8:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_bunch_9:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_green_balloon:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and (self.has_diddy(state) or self.can_climb(state)),

            LocationName.stronghold_showdown_banana_coin_1:
                self.can_team_attack,
            LocationName.stronghold_showdown_red_balloon:
                self.can_team_attack,
            LocationName.stronghold_showdown_banana_coin_2:
                self.can_team_attack,

            LocationName.screechs_sprint_banana_coin_1:
                self.can_cartwheel,
            LocationName.screechs_sprint_banana_bunch_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_cartwheel(state),
            LocationName.screechs_sprint_banana_coin_2:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_cartwheel(state),
            LocationName.screechs_sprint_banana_coin_3:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_red_balloon:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_bunch_2:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_bunch_3:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_coin_4:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_coin_5:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_coin_6:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_coin_7:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_coin_8:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_bunch_4:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_bunch_5:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),
            LocationName.screechs_sprint_banana_bunch_6:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                ),

            LocationName.jungle_jinx_banana_bunch_1:
                self.true,
            LocationName.jungle_jinx_banana_bunch_2:
                self.true,
            LocationName.jungle_jinx_banana_coin_1:
                self.can_hover,
            LocationName.jungle_jinx_banana_coin_2:
                self.can_cartwheel,
            LocationName.jungle_jinx_banana_coin_3:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),
            LocationName.jungle_jinx_banana_coin_4:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state) and self.can_team_attack(state),
            LocationName.jungle_jinx_banana_coin_5:
                lambda state: self.can_cartwheel(state) and self.has_kannons(state),

            LocationName.black_ice_battle_banana_bunch_1:
                lambda state: self.can_carry(state) and self.can_cartwheel(state),
            LocationName.black_ice_battle_red_balloon_1:
                self.true,
            LocationName.black_ice_battle_red_balloon_2:
                self.true,
            LocationName.black_ice_battle_red_balloon_3:
                self.can_carry,
            LocationName.black_ice_battle_banana_bunch_2:
                self.true,
            LocationName.black_ice_battle_banana_coin_1:
                self.true,
            LocationName.black_ice_battle_banana_bunch_3:
                self.can_carry,

            LocationName.klobber_karnage_banana_coin_1:
                self.true,
            LocationName.klobber_karnage_banana_bunch_1:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_bunch_2:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_coin_2:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_bunch_3:
                self.can_cartwheel,
            LocationName.klobber_karnage_banana_coin_3:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.has_controllable_barrels(state),
            LocationName.klobber_karnage_banana_bunch_4:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state) or self.can_hover(state)),
            LocationName.klobber_karnage_banana_bunch_5:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state) or self.can_hover(state) and self.has_kannons(state)),
            LocationName.klobber_karnage_banana_bunch_6:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_banana_bunch_7:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_banana_coin_4:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),
            LocationName.klobber_karnage_red_balloon:
                lambda state: self.can_cartwheel(state) and self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and self.has_controllable_barrels(state) and 
                    self.has_kannons(state),

            LocationName.fiery_furnace_banana_bunch_1:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_2:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_3:
                self.can_team_attack,
            LocationName.fiery_furnace_banana_bunch_4:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state),
            LocationName.fiery_furnace_banana_coin_1:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),
            LocationName.fiery_furnace_banana_coin_2:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),
            LocationName.fiery_furnace_banana_bunch_5:
                lambda state: self.has_controllable_barrels(state) and self.can_team_attack(state) and 
                    self.can_cartwheel(state),

            LocationName.animal_antics_banana_bunch_1:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state),
            LocationName.animal_antics_banana_bunch_2:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state),
            LocationName.animal_antics_banana_coin_1:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state),
            LocationName.animal_antics_banana_coin_2:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_bunch_3:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_bunch_4:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_3:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_4:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_red_balloon:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state) and self.has_kannons(state),
            LocationName.animal_antics_banana_coin_5:
                lambda state: self.has_rambi(state) and 
                    self.has_enguarde(state) and self.can_swim(state) and self.has_squitter(state) and 
                    self.has_squawks(state)  and self.has_kannons(state) and self.has_rattly(state),
        }


class DKC2ExpertRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                lambda state: self.can_carry(state) or self.has_rambi(state),

            LocationName.mainbrace_mayhem_clear:
                self.can_climb,
            LocationName.mainbrace_mayhem_kong:
                self.can_climb,
            LocationName.mainbrace_mayhem_dk_coin:
                lambda state: self.can_climb(state) and self.can_team_attack(state
                ), 
            LocationName.mainbrace_mayhem_bonus_1:
                lambda state: self.can_climb(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)),
            LocationName.mainbrace_mayhem_bonus_2:
                lambda state: self.can_carry(state) and self.can_climb(state),
            LocationName.mainbrace_mayhem_bonus_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_clear:
                lambda state: self.can_cling(state) or (
                    self.can_team_attack(state) and self.can_hover(state)
                    ),
            LocationName.gangplank_galley_kong:
                lambda state: self.can_carry(state) and self.can_team_attack(state) and (
                    self.can_cling(state) or self.can_hover(state)
                ),
            LocationName.gangplank_galley_dk_coin:
                lambda state: self.can_cartwheel(state) and (
                    self.can_cling(state) or self.can_hover(state)
                    ) or (self.can_team_attack(state) and self.can_cling(state)
                ),
            LocationName.gangplank_galley_bonus_1:
                self.can_carry,
            LocationName.gangplank_galley_bonus_2:
                self.can_cling,

            LocationName.lockjaws_locker_clear:
                self.can_swim,
            LocationName.lockjaws_locker_kong:
                self.can_swim,
            LocationName.lockjaws_locker_dk_coin:
                self.can_swim,
            LocationName.lockjaws_locker_bonus_1:
                lambda state: self.has_enguarde(state) and (self.can_swim(state) 
                    or (self.can_team_attack(state) and self.can_hover(state))),

            LocationName.topsail_trouble_clear:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or 
                     self.has_rattly(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_kong:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or 
                     self.has_rattly(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_dk_coin:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or 
                     self.has_rattly(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                ),
            LocationName.topsail_trouble_bonus_1:
                lambda state: self.can_team_attack(state) or self.has_rattly(state),

            LocationName.topsail_trouble_bonus_2:
                lambda state: self.can_climb(state) and (
                    self.can_team_attack(state) or 
                     self.has_rattly(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                ),

            LocationName.krows_nest_clear:
                self.can_carry,
            LocationName.krow_defeated:
                self.can_carry,

            LocationName.hot_head_hop_clear:
                lambda state: self.has_kannons(state) or self.has_squitter(state) or (
                        self.can_team_attack(state) and self.can_hover(state)
                    ),
            LocationName.hot_head_hop_kong:
                self.can_carry,
            LocationName.hot_head_hop_dk_coin:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_1:
                self.can_carry,
            LocationName.hot_head_hop_bonus_2:
                self.has_squitter,
            LocationName.hot_head_hop_bonus_3:
                self.has_squitter,

            LocationName.kannons_klaim_clear:
                self.has_kannons,
            LocationName.kannons_klaim_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.kannons_klaim_dk_coin:
                lambda state: self.can_hover(state) or self.can_cartwheel(state),
            LocationName.kannons_klaim_bonus_1:
                lambda state: self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.kannons_klaim_bonus_2:
                self.has_kannons,
            LocationName.kannons_klaim_bonus_3:
                self.has_kannons,

            LocationName.lava_lagoon_clear:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_kong:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_dk_coin:
                lambda state: self.can_swim(state) and self.has_clapper(state),
            LocationName.lava_lagoon_bonus_1:
                lambda state: self.can_swim(state) and 
                    self.has_clapper(state) and 
                    self.can_carry(state) and
                    self.has_enguarde(state),

            
            LocationName.red_hot_ride_kong:
                lambda state: self.can_carry(state) or self.has_both_kongs(state),
            LocationName.red_hot_ride_dk_coin:
                lambda state: self.has_both_kongs(state) or (self.can_carry(state) and self.has_diddy(state)),
            LocationName.red_hot_ride_bonus_1:
                lambda state: self.can_carry(state) or self.has_rambi(state),

            LocationName.squawks_shaft_clear:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state) and self.has_squawks(state),
            LocationName.squawks_shaft_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.squawks_shaft_bonus_1:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.squawks_shaft_bonus_2:
                lambda state: self.has_kannons(state) and (
                    self.can_team_attack(state) or  (
                        self.can_cartwheel(state) or self.can_hover(state)
                    )
                ),
            LocationName.squawks_shaft_bonus_3:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kleevers_kiln_clear:
                lambda state: self.can_cling(state) and self.can_carry(state),
            LocationName.kleever_defeated:
                lambda state: self.can_cling(state) and self.can_carry(state),

            LocationName.barrel_bayou_clear:
                lambda state: (self.has_controllable_barrels(state) or (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state))) 
                    and (self.has_kannons(state) or (self.can_hover(state) and self.can_team_attack(state))
                ),
            LocationName.barrel_bayou_kong:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state)
                ),
            LocationName.barrel_bayou_dk_coin:
                lambda state: self.has_rambi(state) and self.has_controllable_barrels(state),
            LocationName.barrel_bayou_bonus_1:
                lambda state: self.can_carry(state) and (
                    self.has_controllable_barrels(state) or (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state))
                ),
            LocationName.barrel_bayou_bonus_2:
                lambda state: self.has_controllable_barrels(state) and 
                    (self.has_kannons(state) or (self.can_hover(state) and self.can_team_attack(state))
                ),

            LocationName.glimmers_galleon_clear:
                self.can_swim,
            LocationName.glimmers_galleon_kong:
                self.can_swim,
            LocationName.glimmers_galleon_dk_coin:
                self.can_swim,
            LocationName.glimmers_galleon_bonus_1:
                self.can_swim,
            LocationName.glimmers_galleon_bonus_2:
                self.can_swim,

            LocationName.krockhead_klamber_clear:
                self.can_climb,
            LocationName.krockhead_klamber_kong:
                self.can_climb,
            LocationName.krockhead_klamber_dk_coin:
                lambda state: self.can_carry(state) and self.can_cartwheel(state) and self.has_both_kongs(state),
            LocationName.krockhead_klamber_bonus_1:
                lambda state: self.can_climb(state) and 
                self.can_team_attack(state) and 
                self.has_squitter(state),

            LocationName.rattle_battle_clear:
                self.has_rattly,
            LocationName.rattle_battle_kong:
                self.has_rattly,
            LocationName.rattle_battle_dk_coin:
                lambda state: self.has_rattly(state) and self.has_kannons(state),
            LocationName.rattle_battle_bonus_1:
                lambda state: self.can_team_attack(state) and (self.can_hover(state) or self.can_cartwheel(state)),
            LocationName.rattle_battle_bonus_2:
                self.has_rattly,
            LocationName.rattle_battle_bonus_3:
                self.has_rattly,

            LocationName.slime_climb_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slime_climb_kong:
                lambda state: self.can_climb(state) and self.can_swim(state),
            LocationName.slime_climb_dk_coin:
                lambda state: self.can_climb(state) and self.can_swim(state) and self.has_both_kongs(state),
            LocationName.slime_climb_bonus_1:
                self.can_climb,
            LocationName.slime_climb_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),

            LocationName.bramble_blast_clear:
                self.has_kannons,
            LocationName.bramble_blast_kong:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_dk_coin:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_bonus_1:
                self.has_kannons,
            LocationName.bramble_blast_bonus_2:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.kudgels_kontest_clear:
                self.can_carry,
            LocationName.kudgel_defeated:
                self.can_carry,

            LocationName.hornet_hole_clear:
                lambda state: self.can_cling(state) or (self.can_team_attack(state) and self.has_squitter(state)),
            LocationName.hornet_hole_kong:
                lambda state: self.can_cling(state) or (self.can_team_attack(state) and self.has_squitter(state)),
            LocationName.hornet_hole_dk_coin:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),
            LocationName.hornet_hole_bonus_1:
                lambda state: self.can_carry(state) and ((self.can_team_attack(state) and self.can_cling(state)) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)))
                ),
            LocationName.hornet_hole_bonus_2:
                lambda state: (self.can_team_attack(state) and self.can_cling(state)) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state))
                    ),
            LocationName.hornet_hole_bonus_3:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),

            LocationName.target_terror_clear:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_kong:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_dk_coin:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_bonus_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_bonus_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_clear:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_kong:
                lambda state: self.can_climb(state) and self.has_squawks(state) and self.has_kannons(state),
            LocationName.bramble_scramble_dk_coin:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),
            LocationName.bramble_scramble_bonus_1:
                lambda state: self.can_climb(state) and self.has_squawks(state) and ((
                    self.can_team_attack(state) and self.has_invincibility(state)
                    ) or (
                    self.can_hover(state) and self.has_kannons(state) and self.has_both_kongs(state)
                    )
                ),

            LocationName.rickety_race_clear:
                self.has_skull_kart,
            LocationName.rickety_race_kong:
                self.has_skull_kart,
            LocationName.rickety_race_dk_coin:
                self.has_skull_kart,
            LocationName.rickety_race_bonus_1:
                lambda state: self.has_skull_kart(state) and 
                    self.can_team_attack(state) 
                    and self.can_hover(state),

            LocationName.mudhole_marsh_clear:
                lambda state: (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state)
                        and self.has_both_kongs(state) and self.can_cartwheel(state)
                ),
            LocationName.mudhole_marsh_kong:
                lambda state: self.can_carry(state) and (
                    (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state)
                        and self.has_both_kongs(state) and self.can_cartwheel(state))
                ),
            LocationName.mudhole_marsh_dk_coin:
                lambda state: (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state)
                        and self.has_both_kongs(state) and self.can_cartwheel(state)
                ),
            LocationName.mudhole_marsh_bonus_1:
                lambda state: self.can_team_attack(state) and ((self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.has_both_kongs(state) and self.can_cartwheel(state))
                ),
            LocationName.mudhole_marsh_bonus_2:
                lambda state: self.can_carry(state) and (
                    (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state)
                        and self.has_both_kongs(state) and self.can_cartwheel(state))
                ),

            LocationName.rambi_rumble_clear:
                lambda state: (self.can_cling(state) or (self.has_diddy(state) and self.can_cartwheel(state)))  and self.has_kannons(state) and self.has_rambi(state),
            LocationName.rambi_rumble_kong:
                lambda state: (self.can_cling(state) or (self.has_diddy(state) and self.can_cartwheel(state))) and self.has_kannons(state) and self.has_rambi(state) and ( 
                    self.can_cartwheel(state) or self.can_team_attack(state)),
            LocationName.rambi_rumble_dk_coin:
                lambda state: self.has_kannons(state) and (self.can_cling(state) or self.can_team_attack(state)),
            LocationName.rambi_rumble_bonus_1:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.rambi_rumble_bonus_2:
                lambda state: (self.can_cling(state) or (self.has_diddy(state) and self.can_cartwheel(state))) and self.has_kannons(state) and self.has_rambi(state),

            LocationName.king_zing_sting_clear:
                self.has_squawks,
            LocationName.king_zing_defeated:
                self.has_squawks,

             LocationName.ghostly_grove_clear:
                self.can_climb,
            LocationName.ghostly_grove_kong:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.ghostly_grove_dk_coin:
                lambda state:  (self.can_climb(state) and (
                    (self.can_cartwheel(state) and self.has_diddy(state)) or self.can_hover(state))
                    ) or ((self.can_team_attack(state) or self.has_both_kongs(state)) and self.can_hover(state)
                ),
            LocationName.ghostly_grove_bonus_1:
            lambda state: self.can_carry(state) and 
                    (self.can_climb(state) or ((self.can_team_attack(state) or self.has_both_kongs(state)) and self.can_hover(state))
                ),
            LocationName.ghostly_grove_bonus_2:
                self.can_climb,

            LocationName.haunted_hall_clear:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_kong:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_dk_coin:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_bonus_1:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_bonus_2:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_bonus_3:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),

            LocationName.gusty_glade_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_carry(state) and
                    self.can_cartwheel(state),
            LocationName.gusty_glade_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_bonus_1:
                lambda state: self.can_team_attack(state) and (self.can_cling(state) or self.has_rattly(state)),
            LocationName.gusty_glade_bonus_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_kannons(state),

            LocationName.parrot_chute_panic_clear:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_kong:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_dk_coin:
                lambda state: self.can_hover(state) or self.has_diddy(state),
            LocationName.parrot_chute_panic_bonus_1:
                lambda state: self.has_squawks(state) or (
                    self.can_team_attack(state) and self.can_hover(state)),
            LocationName.parrot_chute_panic_bonus_2:
                lambda state: self.has_squawks(state) and (
                    self.can_cartwheel(state) or 
                    self.can_hover(state) or
                    self.has_both_kongs(state)
                ),

            LocationName.web_woods_clear:
                self.has_squitter,
            LocationName.web_woods_kong:
                lambda state: self.has_squitter(state) and (
                    self.can_team_attack(state) or (self.can_hover(state) or (
                        self.can_cartwheel(state) and self.has_diddy(state))
                    )),
            LocationName.web_woods_dk_coin:
                self.has_squitter,
            LocationName.web_woods_bonus_1:
                self.has_squitter,
            LocationName.web_woods_bonus_2:
                self.has_squitter,

            LocationName.kreepy_krow_clear:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),
            LocationName.kreepy_krow_defeated:
                lambda state: self.has_kannons(state) and self.can_climb(state) and self.can_cling(state) and 
                    self.can_carry(state),

            LocationName.arctic_abyss_clear:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and (
                        (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_kong:
                lambda state: (
                    (self.can_swim(state) or self.has_enguarde(state)) and
                    ( (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state))
                ),
            LocationName.arctic_abyss_dk_coin:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and (
                         (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_bonus_1:
                lambda state: self.has_enguarde(state) and ( 
                    self.can_swim(state) or (
                         (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_bonus_2:
                
                lambda state: self.can_carry(state) and (
                    self.can_swim(state) or (
                        self.has_enguarde(state) and (
                             (self.has_diddy(state) and self.can_cartwheel(state)) or self.can_hover(state)
                        )
                    )
                ),

            LocationName.windy_well_clear:
                self.can_cling,
            LocationName.windy_well_kong:
                lambda state: self.has_kannons(state) and self.can_cling(state),
            LocationName.windy_well_dk_coin:
                self.can_cling,
            LocationName.windy_well_bonus_1:
                self.can_cling,
            LocationName.windy_well_bonus_2:
                lambda state: self.can_carry(state) and self.can_cling(state) and self.has_squawks(state),

            LocationName.castle_crush_clear:
                lambda state: (self.can_hover(state) or self.can_cartwheel(state)) or self.has_both_kongs(state),
            LocationName.castle_crush_kong:
                lambda state: self.can_hover(state) or (self.can_cartwheel(state) or self.has_both_kongs(state)),
            LocationName.castle_crush_dk_coin:
                lambda state: self.has_squawks(state) and (
                    self.can_hover(state) or (self.can_cartwheel(state) or self.has_both_kongs(state)),
                ),
            LocationName.castle_crush_bonus_1:
                lambda state: self.has_rambi(state) and (self.has_both_kongs(state) or self.can_team_attack(state)),
            LocationName.castle_crush_bonus_2:
                lambda state: self.can_carry(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or 
                    (self.can_hover(state) or self.can_cartwheel(state))
                ),

            LocationName.clappers_cavern_clear:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state) and self.has_both_kongs(state))) and ((
                    self.can_cling(state) and 
                        (self.has_enguarde(state) or self.can_swim(state))
                    ) or (
                        self.can_swim(state) and self.has_invincibility(state)
                    )
                ),
            LocationName.clappers_cavern_kong:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state) and self.has_both_kongs(state))) and ((
                    self.can_cling(state) and 
                        (self.has_enguarde(state) or self.can_swim(state))
                    ) or (
                        self.can_swim(state) and self.has_invincibility(state) and self.can_team_attack(state)
                    )
                ),
            LocationName.clappers_cavern_dk_coin:
                lambda state: self.can_team_attack(state) and 
                    (self.can_cling(state) or self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))),
            LocationName.clappers_cavern_bonus_1:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
            LocationName.clappers_cavern_bonus_2:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and self.has_enguarde(state),

            LocationName.chain_link_chamber_clear:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or (self.has_kannons(state) and self.has_controllable_barrels(state))
                ),
            LocationName.chain_link_chamber_kong:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or (self.has_kannons(state) and self.has_controllable_barrels(state))
                ),
            LocationName.chain_link_chamber_dk_coin:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or (self.has_kannons(state) and self.has_controllable_barrels(state))
                ),
            LocationName.chain_link_chamber_bonus_1:
                lambda state: self.can_climb(state) and self.can_cling(state) and self.can_carry(state),
            LocationName.chain_link_chamber_bonus_2:
                lambda state: self.can_climb(state) and 
                self.has_controllable_barrels(state) and (
                    self.can_cling(state) or self.has_kannons(state)
                ) and (
                    self.can_cartwheel(state) or self.can_team_attack(state) or self.has_both_kongs(state)
                ),

            LocationName.toxic_tower_clear:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_kong:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_dk_coin:
                self.has_rattly,
            LocationName.toxic_tower_bonus_1:
                lambda state: self.has_rattly(state) and self.has_squawks(state),

            LocationName.screechs_sprint_clear:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_bonus_1:
                lambda state: self.can_climb(state) and 
                    self.can_team_attack(state) and 
                    self.can_cartwheel(state) and
                    self.can_carry(state)
                ,

            LocationName.k_rool_duel_clear:
                self.can_carry,

            LocationName.jungle_jinx_clear:
                lambda state: self.has_kannons(state) or self.can_hover(state), 
            
            LocationName.jungle_jinx_kong:
                lambda state: (self.can_hover(state) or (self.can_cartwheel(state) and self.has_kannons(state))) and (
                    self.can_carry(state) or self.has_both_kongs(state) 
                ), 
            LocationName.jungle_jinx_dk_coin:
                lambda state: self.can_team_attack(state)  and (
                    self.can_cartwheel(state) or self.can_hover(state)
                ), 

            LocationName.black_ice_battle_kong:
                lambda state: self.can_carry(state) or self.has_both_kongs(state),
            LocationName.black_ice_battle_dk_coin:
                lambda state: self.can_carry(state) or self.has_both_kongs(state),

            LocationName.klobber_karnage_clear:
                lambda state: self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and
                    self.has_controllable_barrels(state) and
                    self.has_kannons(state) and (
                        self.can_carry(state) or self.can_team_attack(state)
                    ),
            LocationName.klobber_karnage_kong:
                lambda state: self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and
                    self.has_controllable_barrels(state) and
                    self.has_kannons(state) and (
                        self.can_carry(state) or self.can_team_attack(state)
                    ),
            LocationName.klobber_karnage_dk_coin:
                lambda state: self.has_invincibility(state) and
                    self.can_use_diddy_barrels(state) and 
                    self.can_use_dixie_barrels(state) and
                    self.has_controllable_barrels(state) and
                    self.has_kannons(state) and (
                        self.can_carry(state) or self.can_team_attack(state)
                    ),

            LocationName.fiery_furnace_clear:
                lambda state: (
                    self.has_controllable_barrels(state) and (
                        self.can_cartwheel(state) or
                        self.has_both_kongs(state)
                    )
                ),
            LocationName.fiery_furnace_kong:
                lambda state: (
                    self.has_controllable_barrels(state) and (
                        self.can_cartwheel(state) or
                        self.has_both_kongs(state)
                    )
                ),
            LocationName.fiery_furnace_dk_coin:
                lambda state: (
                    self.has_controllable_barrels(state) and (
                        self.can_cartwheel(state) or
                        self.has_both_kongs(state)
                    )
                ),

            LocationName.animal_antics_clear:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_kong:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_dk_coin:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),

            LocationName.krocodile_core_clear:
                self.can_carry,
                
            LocationName.pirate_panic_banana_coin_1:
                self.can_team_attack,
            LocationName.pirate_panic_banana_bunch_1:
                self.true,
            LocationName.pirate_panic_red_balloon:
                self.true,
            LocationName.pirate_panic_banana_coin_2:
                lambda state: self.can_team_attack(state) or self.can_carry(state) or self.has_rambi(state),
            LocationName.pirate_panic_banana_coin_3:
                self.true,
            LocationName.pirate_panic_green_balloon:
                self.has_rambi,

            LocationName.mainbrace_mayhem_banana_bunch_1:
                self.can_cartwheel,
            LocationName.mainbrace_mayhem_banana_coin_1:
                lambda state: self.can_climb(state) or self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_coin_2:
                lambda state: self.can_climb(state) or self.can_team_attack(state),
            LocationName.mainbrace_mayhem_green_balloon:
                self.can_climb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_coin_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),
            LocationName.mainbrace_mayhem_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_team_attack(state),

            LocationName.gangplank_galley_banana_bunch_1:
                lambda state: self.can_hover(state) or (
                    self.can_cling(state) and (
                        (self.has_diddy(state) and self.can_cartwheel(state)) 
                        or self.can_team_attack(state))
                    ),
            LocationName.gangplank_galley_banana_bunch_2:
                self.can_carry,
            LocationName.gangplank_galley_red_balloon_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_3:
                self.can_team_attack,
            LocationName.gangplank_galley_banana_coin_1:
                self.can_carry,
            LocationName.gangplank_galley_banana_bunch_4:
                lambda state: self.can_hover(state) or self.has_kannons(state),
            LocationName.gangplank_galley_banana_coin_2:
                self.has_kannons,
            LocationName.gangplank_galley_banana_bunch_5:
                lambda state: self.can_hover(state) or self.has_kannons(state),
            LocationName.gangplank_galley_banana_bunch_6:
                lambda state: self.can_carry(state) and (self.can_hover(state) or self.can_cartwheel(state) or self.can_cling(state)),
            LocationName.gangplank_galley_banana_bunch_7:
                lambda state: self.can_hover(state) or self.can_cling(state),
            LocationName.gangplank_galley_red_balloon_2:
                lambda state: self.can_carry(state) and (self.can_hover(state) or self.can_cling(state)),


            LocationName.lockjaws_locker_banana_coin_1:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_1:
                self.true,
            LocationName.lockjaws_locker_banana_coin_2:
                self.true,
            LocationName.lockjaws_locker_banana_bunch_2:
                lambda state: self.can_swim(state) or self.can_hover(state) or self.can_cartwheel(state),
            LocationName.lockjaws_locker_banana_coin_3:
                lambda state: self.can_swim(state) or self.can_team_attack(state),
            LocationName.lockjaws_locker_banana_coin_4:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and self.can_team_attack(state) and self.can_hover(state)
                ),
            LocationName.lockjaws_locker_banana_coin_5:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and self.can_team_attack(state) and self.can_hover(state)
                ),
            LocationName.lockjaws_locker_banana_bunch_3:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and self.can_team_attack(state) and self.can_hover(state)
                ),
            LocationName.lockjaws_locker_red_balloon:
                lambda state: self.has_enguarde(state) and (
                    self.can_swim(state) or (self.can_team_attack(state) and self.can_hover(state))
                ),
            LocationName.lockjaws_locker_banana_coin_6:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_7:
                self.can_swim,
            LocationName.lockjaws_locker_banana_coin_8:
                self.can_swim,
            LocationName.lockjaws_locker_banana_bunch_4:
                lambda state: self.has_enguarde(state) and self.can_swim(state),

            LocationName.topsail_trouble_red_balloon_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state) or self.can_cling(state),
            LocationName.topsail_trouble_red_balloon_2:
                lambda state: self.can_carry(state) and (
                    self.has_rattly(state) or self.can_team_attack(state) or self.can_cling(state)
                ),
            LocationName.topsail_trouble_banana_bunch_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state) or (
                    self.can_cling(state) and self.has_kannons(state)
                ),
            LocationName.topsail_trouble_banana_bunch_2:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.topsail_trouble_banana_coin_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.topsail_trouble_banana_coin_2:
                self.has_rattly,
            LocationName.topsail_trouble_banana_bunch_3:
                lambda state: self.can_climb(state) and (
                    self.has_rattly(state) or self.can_team_attack(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                    ),
            LocationName.topsail_trouble_banana_coin_3:
                lambda state: self.can_climb(state) and (
                    self.has_rattly(state) or self.can_team_attack(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                    ),
            LocationName.topsail_trouble_banana_coin_4:
                lambda state: self.can_climb(state) and (
                    self.has_rattly(state) or self.can_team_attack(state) or (
                        self.can_cling(state) and self.has_kannons(state))
                    ),
            LocationName.topsail_trouble_blue_balloon:
                lambda state: self.can_climb(state) and (self.can_team_attack(state) or 
                    (self.has_both_kongs(state) and self.can_hover(state) and 
                        (self.has_rattly(state) or (self.can_cling(state) and self.has_kannons(state))))
                    ),

            LocationName.krows_nest_banana_coin_1:
                self.true,
            LocationName.krows_nest_banana_coin_2:
                self.true,

            LocationName.hot_head_hop_green_balloon:
                self.can_carry,
            LocationName.hot_head_hop_banana_coin_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_bunch_1:
                self.can_carry,
            LocationName.hot_head_hop_banana_coin_2:
                lambda state: self.has_squitter(state) or self.can_team_attack(state) or self.can_carry(state),
            LocationName.hot_head_hop_banana_bunch_2:
                self.has_squitter,
            LocationName.hot_head_hop_banana_bunch_3:
                self.has_squitter,
            LocationName.hot_head_hop_banana_coin_3:
                lambda state: self.has_squitter(state) or self.can_hover(state) or self.has_both_kongs(state),
            LocationName.hot_head_hop_banana_coin_4:
                lambda state: self.has_squitter(state) or self.can_hover(state) or (
                    self.has_kannons(state) and (self.has_both_kongs(state) or self.can_cartwheel(state))),
            LocationName.hot_head_hop_red_balloon:
                self.has_squitter,

            LocationName.kannons_klaim_banana_bunch_1:
                lambda state: self.has_kannons(state) or self.can_team_attack(state),
            LocationName.kannons_klaim_banana_coin_1:
                self.has_kannons,
            LocationName.kannons_klaim_banana_coin_2:
                lambda state: self.has_kannons(state) and (self.can_team_attack(state) or self.can_cartwheel(state)),
            LocationName.kannons_klaim_banana_coin_3:
                self.has_kannons,

            LocationName.lava_lagoon_banana_coin_1:
                lambda state: self.has_clapper(state) or self.has_both_kongs(state),
            LocationName.lava_lagoon_banana_coin_2:
                lambda state: self.has_clapper(state) or self.has_both_kongs(state),
            LocationName.lava_lagoon_banana_bunch_1:
                lambda state: self.has_clapper(state) or self.has_both_kongs(state),
            LocationName.lava_lagoon_banana_coin_3:
                lambda state: self.has_clapper(state) and (self.can_swim(state) or self.has_both_kongs(state)),
            LocationName.lava_lagoon_banana_bunch_2:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_4:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_5:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_bunch_3:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_6:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_7:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_red_balloon_1:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_enguarde(state),
            LocationName.lava_lagoon_banana_bunch_4:
                lambda state: self.has_clapper(state) and self.can_swim(state) and self.has_enguarde(state) and self.can_carry(state),
            LocationName.lava_lagoon_banana_bunch_5:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_8:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_9:
                lambda state: self.has_clapper(state) and self.can_swim(state),
            LocationName.lava_lagoon_banana_coin_10:
                lambda state: self.has_clapper(state) and self.can_swim(state),

            LocationName.red_hot_ride_banana_bunch_1:
                self.true,
            LocationName.red_hot_ride_banana_coin_1:
                self.true,
            LocationName.red_hot_ride_banana_coin_2:
                self.true,
            LocationName.red_hot_ride_banana_bunch_2:
                self.true,
            LocationName.red_hot_ride_banana_coin_3:
                self.true,
            LocationName.red_hot_ride_banana_bunch_3:
                self.true,
            LocationName.red_hot_ride_banana_coin_4:
                self.true,
            LocationName.red_hot_ride_banana_coin_5:
                self.has_rambi,
            LocationName.red_hot_ride_banana_coin_6:
                self.true,
            LocationName.red_hot_ride_banana_bunch_4:
                self.true,

            LocationName.squawks_shaft_banana_coin_1:
                self.true,
            LocationName.squawks_shaft_banana_bunch_1:
                lambda state: self.can_team_attack(state) or self.has_kannons(state),
            LocationName.squawks_shaft_banana_coin_2:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_bunch_2:
                self.has_kannons,
            LocationName.squawks_shaft_red_balloon_1:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_coin_3:
                self.has_kannons,
            LocationName.squawks_shaft_banana_coin_4:
                self.has_kannons,
            LocationName.squawks_shaft_banana_coin_5:
                lambda state: self.has_squawks(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_coin_6:
                lambda state: self.has_squawks(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_coin_7:
                lambda state: self.has_squawks(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_bunch_3:
                lambda state: self.has_squawks(state) and self.has_kannons(state),
            LocationName.squawks_shaft_banana_bunch_4:
                lambda state: self.has_squawks(state) and self.has_kannons(state),

            LocationName.kleevers_kiln_banana_coin_1:
                lambda state: self.can_cling(state) and self.can_hover(state) and self.can_carry(state),
            LocationName.kleevers_kiln_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_hover(state) and self.can_carry(state),

            LocationName.barrel_bayou_banana_bunch_1:
                lambda state: self.can_team_attack(state) or self.has_both_kongs(state),
            LocationName.barrel_bayou_banana_coin_1:
                lambda state: self.has_controllable_barrels(state) or 
                    (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state)
                ),
            LocationName.barrel_bayou_banana_bunch_2:
                lambda state: self.has_controllable_barrels(state) or 
                    (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state)
                ),
            LocationName.barrel_bayou_green_balloon:
                lambda state: (self.has_controllable_barrels(state) or (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state)))
                    and self.can_carry(state) and (
                    self.has_kannons(state) or self.can_hover(state)
                ),
            LocationName.barrel_bayou_banana_coin_2:
                lambda state: (self.has_controllable_barrels(state) or (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state))) 
                    and (self.has_kannons(state) or (self.can_hover(state) and self.can_team_attack(state))
                ),
            LocationName.barrel_bayou_banana_bunch_3:
                lambda state: (self.has_controllable_barrels(state) or (self.can_hover(state) and self.can_cartwheel(state) and self.has_rambi(state))) 
                    and (self.has_kannons(state) or (self.can_hover(state) and self.can_team_attack(state))
                ),

            LocationName.glimmers_galleon_banana_coin_1:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_2:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_1:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_2:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_3:
                self.can_swim,
            LocationName.glimmers_galleon_red_balloon:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_4:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_3:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_5:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_4:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_6:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_7:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_5:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_8:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_6:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_9:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_10:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_11:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_12:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_7:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_8:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_13:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_9:
                self.can_swim,
            LocationName.glimmers_galleon_banana_bunch_14:
                self.can_swim,
            LocationName.glimmers_galleon_banana_coin_10:
                self.can_swim,
                
            LocationName.krockhead_klamber_red_balloon_1:
                lambda state: self.has_both_kongs(state) and self.can_carry(state),
            LocationName.krockhead_klamber_banana_coin_1:
                lambda state: self.can_carry(state) and self.can_cartwheel(state) and self.has_both_kongs(state),
            LocationName.krockhead_klamber_banana_coin_2:
                lambda state: (self.can_cartwheel(state) and self.can_hover(state) and self.has_both_kongs(state)) or self.can_climb(state),
            LocationName.krockhead_klamber_red_balloon_2:
                lambda state: self.can_climb(state) and self.can_team_attack(state) and self.has_squitter(state),
            LocationName.krockhead_klamber_banana_coin_3:
                self.can_climb,

            LocationName.rattle_battle_banana_coin_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_1:
                self.true,
            LocationName.rattle_battle_banana_bunch_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_2:
                self.has_rattly,
            LocationName.rattle_battle_banana_coin_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_3:
                self.has_rattly,
            LocationName.rattle_battle_banana_bunch_4:
                self.has_rattly,

            LocationName.slime_climb_banana_coin_1:
                self.true,
            LocationName.slime_climb_banana_coin_2:
                self.can_climb,
            LocationName.slime_climb_banana_bunch_1:
                self.can_climb,
            LocationName.slime_climb_banana_bunch_2:
                self.can_climb,
            LocationName.slime_climb_banana_coin_3:
                self.can_climb,
            LocationName.slime_climb_banana_bunch_3:
                lambda state: self.can_climb(state) and (self.has_both_kongs(state) or self.can_swim(state)),
            LocationName.slime_climb_banana_bunch_4:
                lambda state: self.can_climb(state) and (self.has_both_kongs(state) or self.can_swim(state)),

            LocationName.bramble_blast_banana_bunch_1:
                self.can_team_attack,
            LocationName.bramble_blast_banana_bunch_2:
                lambda state: self.has_both_kongs(state) or self.has_kannons(state),
            LocationName.bramble_blast_banana_bunch_3:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_1:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_4:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_5:
                self.has_kannons,
            LocationName.bramble_blast_banana_coin_2:
                self.has_kannons,
            LocationName.bramble_blast_red_balloon:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_6:
                self.has_kannons,
            LocationName.bramble_blast_banana_bunch_7:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_8:
                lambda state: self.has_kannons(state) and self.has_squawks(state),
            LocationName.bramble_blast_banana_bunch_9:
                lambda state: self.has_kannons(state) and self.has_squawks(state),

            LocationName.hornet_hole_banana_bunch_1:
                lambda state: (self.can_team_attack(state) and self.can_cling(state)) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state))
                    ),
            LocationName.hornet_hole_banana_coin_1:
                lambda state: (self.can_team_attack(state) and self.can_cling(state)) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state))
                    ),
            LocationName.hornet_hole_banana_bunch_2:
                lambda state: (self.can_team_attack(state) and self.can_cling(state)) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state))
                    ),
            LocationName.hornet_hole_banana_coin_2:
                self.true,
            LocationName.hornet_hole_green_balloon_1:
                self.can_carry,
            LocationName.hornet_hole_banana_coin_3:
                self.true,
            LocationName.hornet_hole_banana_bunch_3:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),
            LocationName.hornet_hole_banana_coin_4:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),
            LocationName.hornet_hole_banana_bunch_4:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),
            LocationName.hornet_hole_banana_bunch_5:
                lambda state: self.can_team_attack(state) or self.has_both_kongs(state) or (self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)))
                    ),
            LocationName.hornet_hole_red_balloon_1:
                lambda state: self.has_squitter(state) and (
                    (self.has_both_kongs(state) and self.can_cling(state)) or self.can_team_attack(state)
                    ),

            LocationName.target_terror_banana_bunch_1:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),
            LocationName.target_terror_banana_bunch_2:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state) and self.has_squawks(state),
            LocationName.target_terror_red_balloon:
                lambda state: self.has_kannons(state) and self.has_skull_kart(state),

            LocationName.bramble_scramble_banana_bunch_1:
                self.true,
            LocationName.bramble_scramble_banana_bunch_2:
                self.has_both_kongs,
            LocationName.bramble_scramble_banana_coin_1:
                lambda state: self.can_climb(state) and self.has_kannons(state) and ((
                    self.can_team_attack(state) and self.has_invincibility(state)
                    ) or (
                    (self.can_hover(state) or self.can_cartwheel(state)) and self.has_both_kongs(state)
                    )
                ),
            LocationName.bramble_scramble_banana_coin_2:
                lambda state: self.can_climb(state) and self.has_squawks(state) and ((
                    self.can_team_attack(state) and self.has_invincibility(state)
                    ) or (
                    (self.can_hover(state) or self.can_cartwheel(state)) and self.has_kannons(state) and self.has_both_kongs(state)
                    )
                ),
            LocationName.bramble_scramble_banana_coin_3:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_3:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_4:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_4:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_5:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_bunch_5:
                lambda state: self.can_climb(state) and self.has_squawks(state),
            LocationName.bramble_scramble_banana_coin_6:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),
            LocationName.bramble_scramble_banana_coin_7:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),
            LocationName.bramble_scramble_banana_coin_8:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),
            LocationName.bramble_scramble_blue_balloon:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),
            LocationName.bramble_scramble_red_balloon:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or (self.can_cartwheel(state) and self.has_squitter(state))
                ),

            LocationName.rickety_race_banana_coin:
                self.has_skull_kart,

            LocationName.mudhole_marsh_banana_coin_1:
                self.true,
            LocationName.mudhole_marsh_banana_bunch_1:
                lambda state: self.can_carry(state) and (
                    (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state) and self.has_both_kongs(state))
                ),
            LocationName.mudhole_marsh_banana_coin_2:
                lambda state: self.can_carry(state) and (
                    (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state)
                        and self.has_both_kongs(state) and self.can_cartwheel(state))
                ),
            LocationName.mudhole_marsh_banana_coin_3:
                 lambda state: (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state) 
                        and self.has_both_kongs(state) and self.can_cartwheel(state)
                ),
            LocationName.mudhole_marsh_banana_coin_4:
                lambda state: (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state) 
                        and self.has_both_kongs(state) and self.can_cartwheel(state)
                ),
            LocationName.mudhole_marsh_banana_coin_5:
                lambda state: (self.can_cling(state) and 
                    (self.can_climb(state) or self.can_hover(state)))
                    or (self.can_hover(state) and self.can_team_attack(state) 
                        and self.has_both_kongs(state) and self.can_cartwheel(state)
                ),

            LocationName.rambi_rumble_banana_coin_1:
                self.true,
            LocationName.rambi_rumble_banana_bunch_1:
                self.true,
            LocationName.rambi_rumble_banana_bunch_2:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state)) or (self.can_cling(state) and self.has_kannons(state)),
            LocationName.rambi_rumble_banana_coin_2:
                lambda state: self.has_kannons(state) and (
                        self.can_cling(state) or (self.has_diddy(state) and self.can_cartwheel(state) and self.can_hover(state))
                    ),
            LocationName.rambi_rumble_banana_bunch_3:
                lambda state: (self.can_cling(state) or (self.has_diddy(state) and self.can_cartwheel(state))) and self.has_kannons(state) and self.has_rambi(state),

            LocationName.king_zing_sting_banana_coin_1:
                self.true,
            LocationName.king_zing_sting_banana_coin_2:
                self.true,

            LocationName.ghostly_grove_banana_bunch_1:
                self.true,
            LocationName.ghostly_grove_red_balloon:
                self.can_carry,
            LocationName.ghostly_grove_banana_bunch_2:
                self.true,
            LocationName.ghostly_grove_banana_coin_1:
                lambda state: (self.can_climb(state) or (
                    (self.can_team_attack(state) or self.has_both_kongs(state)) and self.can_hover(state))
                ),
            LocationName.ghostly_grove_banana_bunch_3:
                self.can_climb,
            LocationName.ghostly_grove_banana_bunch_4:
                lambda state: self.can_climb(state) or (
                    self.can_team_attack(state) and self.can_hover(state)
                ),
            LocationName.ghostly_grove_banana_coin_2:
                self.can_climb,

            LocationName.haunted_hall_banana_bunch_1:
                self.true,
            LocationName.haunted_hall_banana_bunch_2:
                self.true,
            LocationName.haunted_hall_banana_coin_1:
                self.true,
            LocationName.haunted_hall_banana_coin_2:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),
            LocationName.haunted_hall_banana_coin_3:
                lambda state: self.has_skull_kart(state) and (
                    self.has_diddy(state) or (self.has_dixie(state) 
                        and (self.can_hover(state) or self.can_cartwheel(state))
                        )),

            LocationName.gusty_glade_banana_coin_1:
                self.can_team_attack,
            LocationName.gusty_glade_banana_coin_2:
                self.true,
            LocationName.gusty_glade_blue_balloon:
                lambda state: self.can_team_attack(state) and self.has_rattly(state),
            LocationName.gusty_glade_banana_coin_3:
                lambda state: self.can_cling(state) and self.has_kannons(state),

            LocationName.parrot_chute_panic_banana_coin_1:
                lambda state: self.can_carry(state) or self.can_team_attack(state),
            LocationName.parrot_chute_panic_banana_coin_2:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_banana_bunch_1:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_banana_coin_3:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_banana_bunch_2:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_banana_coin_4:
                lambda state: (self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state),
            LocationName.parrot_chute_panic_banana_coin_5:
                lambda state: ((self.has_both_kongs(state) and self.can_hover(state) and self.can_carry(state)) or self.has_squawks(state)) 
                and self.has_controllable_barrels(state)
                    and (self.can_team_attack(state) or self.can_cartwheel(state)),

            LocationName.web_woods_banana_coin_1:
                lambda state: self.can_team_attack(state) or 
                    (self.has_diddy(state) and self.can_cartwheel(state)) or
                    (self.has_dixie(state) and self.can_hover(state)),
            LocationName.web_woods_banana_coin_2:
                lambda state: self.can_carry(state) and 
                    (self.can_team_attack(state) or 
                    (self.has_diddy(state) and self.can_cartwheel(state)) or
                    (self.has_dixie(state) and self.can_hover(state))
                ),
            LocationName.web_woods_green_balloon_1:
                lambda state: self.can_carry(state) and (self.can_team_attack(state) or self.has_kannons(state)),
            LocationName.web_woods_banana_bunch_1:
                self.true,
            LocationName.web_woods_banana_bunch_2:
                self.true,
            LocationName.web_woods_banana_bunch_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_3:
                self.has_squitter,
            LocationName.web_woods_banana_coin_4:
                self.has_squitter,
            LocationName.web_woods_banana_coin_5:
                self.has_squitter,
            LocationName.web_woods_green_balloon_2:
                lambda state: self.has_squitter(state) and self.can_team_attack(state),

            LocationName.kreepy_krow_banana_coin_1:
                lambda state: self.can_cling(state) and self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.kreepy_krow_banana_coin_2:
                lambda state: self.can_cling(state) and self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),

            LocationName.arctic_abyss_banana_coin_1:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state)) or 
                    (self.has_dixie(state) and self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_1:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state)) or 
                    (self.has_dixie(state) and self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_2:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state)) or 
                    (self.has_dixie(state) and self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_3:
                lambda state: (self.has_diddy(state) and self.can_cartwheel(state)) or 
                    (self.has_dixie(state) and self.can_hover(state)),
            LocationName.arctic_abyss_banana_bunch_4:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_coin_2:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_coin_3:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_coin_4:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_bunch_5:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_coin_5:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_bunch_6:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_banana_bunch_7:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),
            LocationName.arctic_abyss_red_balloon_1:
                lambda state: self.has_enguarde(state) and 
                    (self.can_swim(state) or (
                        (self.has_diddy(state) and self.can_cartwheel(state)) or 
                            (self.has_dixie(state) and self.can_hover(state))
                        )
                    ),
            LocationName.arctic_abyss_red_balloon_2:
                lambda state: self.can_swim(state) or 
                    (self.has_enguarde(state) and 
                        ((self.has_diddy(state) and self.can_cartwheel(state)) or 
                        (self.has_dixie(state) and self.can_hover(state)))
                    ),

            LocationName.windy_well_banana_coin_1:
                self.true,
            LocationName.windy_well_banana_coin_2:
                self.can_cling,
            LocationName.windy_well_banana_coin_3:
                self.can_cling,
            LocationName.windy_well_banana_bunch_1:
                lambda state: self.can_cling(state) and 
                    (self.has_kannons(state) or self.can_team_attack(state)),
            LocationName.windy_well_banana_bunch_2:
                lambda state: self.can_cling(state) and 
                    (self.has_kannons(state) or self.can_team_attack(state)),
            LocationName.windy_well_banana_coin_4:
                self.can_cling,
            LocationName.windy_well_banana_bunch_3:
                self.can_cling,
            LocationName.windy_well_red_balloon:
                self.can_cling,
            LocationName.windy_well_banana_bunch_4:
                lambda state: self.can_cling(state) and self.has_squawks(state) and self.can_carry(state),

            LocationName.castle_crush_banana_coin_1:
                self.true,
            LocationName.castle_crush_banana_bunch_1:
                self.true,
            LocationName.castle_crush_banana_bunch_2:
                self.true,
            LocationName.castle_crush_banana_coin_2:
                self.true,
            LocationName.castle_crush_banana_bunch_3:
                lambda state: self.has_rambi(state) and self.has_both_kongs(state) and  self.can_carry(state),
            LocationName.castle_crush_banana_bunch_4:
                self.true,
            LocationName.castle_crush_banana_bunch_5:
                lambda state: self.has_both_kongs(state) or 
                    (self.can_hover(state) or self.can_cartwheel(state)),
            LocationName.castle_crush_banana_coin_3:
                lambda state: self.can_carry(state) and (
                    self.has_both_kongs(state) or 
                        (self.can_hover(state) or self.can_cartwheel(state))
                    ),
            LocationName.castle_crush_banana_bunch_6:
                lambda state: self.can_carry(state) and (
                    self.has_both_kongs(state) or 
                        (self.can_hover(state) or self.can_cartwheel(state))
                    ),

            LocationName.clappers_cavern_banana_coin_1:
                lambda state: self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state)),
            LocationName.clappers_cavern_banana_bunch_1:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and 
                    (self.can_swim(state) or self.has_enguarde(state)),
            LocationName.clappers_cavern_banana_bunch_2:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and 
                    (self.can_swim(state) or self.has_enguarde(state)),
            LocationName.clappers_cavern_banana_bunch_3:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and 
                    (self.can_swim(state) or self.has_enguarde(state)),
            LocationName.clappers_cavern_banana_coin_2:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and 
                    (self.can_swim(state) or self.has_enguarde(state)),
            LocationName.clappers_cavern_banana_bunch_4:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and self.has_enguarde(state),
            LocationName.clappers_cavern_banana_coin_3:
                lambda state: self.has_kannons(state) and (self.has_clapper(state) or (self.can_hover(state) and self.can_swim(state))) and 
                    (self.can_swim(state) or self.has_enguarde(state)) and (
                        (self.can_team_attack(state) and self.has_invincibility(state)) or self.has_both_kongs(state)),
            LocationName.clappers_cavern_banana_coin_4:
                lambda state: self.has_kannons(state) and self.has_clapper(state) and 
                    (self.can_swim(state) or self.has_enguarde(state)) and (
                        (self.can_team_attack(state) and self.has_invincibility(state)) or self.has_both_kongs(state)),
            LocationName.clappers_cavern_banana_coin_5:
                lambda state: self.has_kannons(state) and self.has_clapper(state) and 
                    (self.can_swim(state) or self.has_enguarde(state)) and (
                        (self.can_team_attack(state) and self.has_invincibility(state)) or self.has_both_kongs(state)),

            LocationName.chain_link_chamber_banana_coin_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_1:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_2:
                self.can_climb,
            LocationName.chain_link_chamber_banana_bunch_3:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.chain_link_chamber_banana_coin_2:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_bunch_4:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_coin_3:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),
            LocationName.chain_link_chamber_banana_coin_4:
                lambda state: self.can_climb(state) and 
                    (self.can_cling(state) or (self.has_kannons(state) and 
                    self.has_controllable_barrels(state))),

            LocationName.toxic_tower_banana_bunch_1:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_2:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_3:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_4:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_5:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_6:
                lambda state: self.has_rattly(state) or self.can_team_attack(state),
            LocationName.toxic_tower_banana_bunch_7:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_1:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_2:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_3:
                self.has_rattly,
            LocationName.toxic_tower_banana_coin_4:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_coin_5:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_bunch_8:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_banana_bunch_9:
                lambda state: self.has_rattly(state) and self.has_squawks(state),
            LocationName.toxic_tower_green_balloon:
                lambda state: self.has_rattly(state) and self.has_squawks(state) and (self.has_diddy(state) or self.can_climb(state)),

            LocationName.stronghold_showdown_banana_coin_1:
                self.can_team_attack,
            LocationName.stronghold_showdown_red_balloon:
                self.can_team_attack,
            LocationName.stronghold_showdown_banana_coin_2:
                self.can_team_attack,

            LocationName.screechs_sprint_banana_coin_1:
                self.true,
            LocationName.screechs_sprint_banana_bunch_1:
                self.can_carry,
            LocationName.screechs_sprint_banana_coin_2:
                self.can_climb,
            LocationName.screechs_sprint_banana_coin_3:
                lambda state: self.can_climb(state) and (
                    ((self.has_squawks(state) or self.has_both_kongs(state)) and (
                    self.can_hover(state) or self.can_cartwheel(state))
                    ) or self.can_team_attack(state)
                ),
            LocationName.screechs_sprint_red_balloon:
                lambda state: self.can_climb(state) and (
                    ((self.has_squawks(state) or self.has_both_kongs(state)) and (
                    self.can_hover(state) or self.can_cartwheel(state))
                    ) or self.can_team_attack(state)
                ),
            LocationName.screechs_sprint_banana_bunch_2:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_bunch_3:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_coin_4:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_coin_5:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_coin_6:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_coin_7:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_coin_8:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_bunch_4:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_bunch_5:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),
            LocationName.screechs_sprint_banana_bunch_6:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state) or self.can_hover(state) or self.has_both_kongs(state)
                ),

            LocationName.jungle_jinx_banana_bunch_1:
                self.true,
            LocationName.jungle_jinx_banana_bunch_2:
                self.true,
            LocationName.jungle_jinx_banana_coin_1:
                self.true,
            LocationName.jungle_jinx_banana_coin_2:
                self.true,
            LocationName.jungle_jinx_banana_coin_3:
                lambda state: self.can_hover(state) or self.has_kannons(state),
            LocationName.jungle_jinx_banana_coin_4:
                lambda state: self.can_hover(state) or self.has_kannons(state),
            LocationName.jungle_jinx_banana_coin_5:
                lambda state: self.can_hover(state) or self.has_kannons(state),

            LocationName.black_ice_battle_banana_bunch_1:
                lambda state: self.can_hover(state) or self.has_both_kongs(state) or self.can_carry(state) or self.can_cartwheel(state),
            LocationName.black_ice_battle_red_balloon_1:
                self.true,
            LocationName.black_ice_battle_red_balloon_2:
                self.true,
            LocationName.black_ice_battle_red_balloon_3:
                self.can_carry,
            LocationName.black_ice_battle_banana_bunch_2:
                self.true,
            LocationName.black_ice_battle_banana_coin_1:
                self.true,
            LocationName.black_ice_battle_banana_bunch_3:
                lambda state: self.can_carry(state) or self.has_both_kongs(state),

            LocationName.klobber_karnage_banana_coin_1:
                self.true,
            LocationName.klobber_karnage_banana_bunch_1:
                self.true,
            LocationName.klobber_karnage_banana_bunch_2:
                self.true,
            LocationName.klobber_karnage_banana_coin_2:
                self.true,
            LocationName.klobber_karnage_banana_bunch_3:
                self.true,
            LocationName.klobber_karnage_banana_coin_3:
                lambda state: (self.has_diddy(state) and (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state)))
                               or (self.can_team_attack(state) and self.has_controllable_barrels(state)
                ),
            LocationName.klobber_karnage_banana_bunch_4:
                self.has_controllable_barrels,
            LocationName.klobber_karnage_banana_bunch_5:
                lambda state: self.has_controllable_barrels(state) and 
                    (self.has_both_kongs(state) or (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state))
                ),
            LocationName.klobber_karnage_banana_bunch_6:
                lambda state: self.has_controllable_barrels(state) and 
                    (self.has_both_kongs(state) or (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state))
                ),
            LocationName.klobber_karnage_banana_bunch_7:
                lambda state: self.has_controllable_barrels(state) and 
                    (self.has_both_kongs(state) or (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state))
                ),
            LocationName.klobber_karnage_banana_coin_4:
                lambda state: self.has_controllable_barrels(state) and 
                    (self.has_both_kongs(state) or (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state))
                ),
            LocationName.klobber_karnage_red_balloon:
                lambda state: self.has_controllable_barrels(state) and (self.can_cartwheel(state) or self.can_hover(state)) and
                    (self.has_both_kongs(state) or (self.can_use_dixie_barrels(state) and self.can_use_diddy_barrels(state))
                ),

            LocationName.fiery_furnace_banana_bunch_1:
                lambda state: self.can_team_attack(state) or (self.can_cartwheel(state) and self.can_hover(state)),
            LocationName.fiery_furnace_banana_bunch_2:
                lambda state: self.can_team_attack(state) or (self.can_cartwheel(state) and self.can_hover(state)),
            LocationName.fiery_furnace_banana_bunch_3:
                lambda state: self.can_team_attack(state) or (self.can_cartwheel(state) and self.can_hover(state)),
            LocationName.fiery_furnace_banana_bunch_4:
                lambda state: self.can_cartwheel(state) or self.can_hover(state) or self.has_controllable_barrels(state),
            LocationName.fiery_furnace_banana_coin_1:
                self.has_controllable_barrels,
            LocationName.fiery_furnace_banana_coin_2:
                self.has_controllable_barrels,
            LocationName.fiery_furnace_banana_bunch_5:
                lambda state: self.has_controllable_barrels(state) and (self.can_cartwheel(state) or self.can_hover(state)),

            LocationName.animal_antics_banana_bunch_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_bunch_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_coin_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_coin_2:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_bunch_3:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_bunch_4:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_coin_3:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_coin_4:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_red_balloon:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_banana_coin_5:
                lambda state: self.can_swim(state) and self.has_kannons(state) and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),

        }
