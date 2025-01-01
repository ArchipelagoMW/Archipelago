
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC2World

from .Names import LocationName, ItemName, RegionName, EventName

from worlds.generic.Rules import CollectionRule
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
        return state.has_any_count({ItemName.the_flying_krock: 1, ItemName.boss_token: self.world.options.krock_boss_tokens.value}, self.player)
    
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
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
                
        if self.world.options.goal.value == 0x01:
            multiworld.completion_condition[self.player] = lambda state: state.has(EventName.k_rool_duel_clear, self.player)
            
        elif self.world.options.goal.value == 0x02:
            multiworld.completion_condition[self.player] = lambda state: state.has(EventName.krocodile_core_clear, self.player)
        
        else:
            multiworld.completion_condition[self.player] = lambda state: (
                state.has(EventName.k_rool_duel_clear, self.player) and
                state.has(EventName.krocodile_core_clear, self.player)
            )
            

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
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.kannons_klaim_kong:
                lambda state: self.can_carry(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.kannons_klaim_dk_coin:
                lambda state: self.can_hover(state) and self.can_cartwheel(state),
            LocationName.kannons_klaim_bonus_1:
                lambda state: self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and
                    self.can_hover(state),
            LocationName.kannons_klaim_bonus_2:
                lambda state: self.can_carry(state) and self.can_team_attack(state) and self.has_kannons(state) and self.can_hover(state),
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
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state) and
                    self.has_kannons(state),
            LocationName.barrel_bayou_kong:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state) and
                    self.has_kannons(state) and self.can_cartwheel(state),
            LocationName.barrel_bayou_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_bonus_1:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state) and
                    self.can_carry(state),
            LocationName.barrel_bayou_bonus_2:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state) and
                    self.has_kannons(state) and self.can_team_attack(state),

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
                lambda state: self.has_kannons(state) and self.can_team_attack(state) and self.can_hover(state),
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
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_carry(state) and
                    self.can_cartwheel(state),
            LocationName.gusty_glade_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_hover(state),
            LocationName.gusty_glade_bonus_1:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
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
                self.can_cling,
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
                lambda state: self.has_clapper(state) and self.can_cling(state) and self.can_cartwheel(state) and
                    self.can_team_attack(state),
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
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_cartwheel(state) and 
                    self.has_squawks(state),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_cartwheel(state) and 
                    self.has_squawks(state),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.can_cartwheel(state) and 
                    self.has_squawks(state),
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
                lambda state: self.can_carry(state) and self.can_hover(state) and self.has_diddy(state),
        }

    def set_dkc2_rules(self) -> None:
        super().set_dkc2_rules()


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
                lambda state: self.has_squitter(state) and self.has_kannons(state),

            LocationName.kannons_klaim_clear:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.kannons_klaim_kong:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.kannons_klaim_dk_coin:
                lambda state: self.can_hover(state) or self.can_cartwheel(state),
            LocationName.kannons_klaim_bonus_1:
                lambda state: self.can_use_diddy_barrels(state) and self.can_use_dixie_barrels(state) and
                    self.can_hover(state),
            LocationName.kannons_klaim_bonus_2:
                lambda state: self.can_carry(state) and self.can_team_attack(state) and self.has_kannons(state),
            LocationName.kannons_klaim_bonus_3:
                lambda state: self.can_carry(state) and self.has_kannons(state),

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
                lambda state: self.has_kannons(state) and self.can_team_attack(state) and
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
                lambda state: self.can_cling(state) and self.has_squitter(state) and self.can_team_attack(state),
            LocationName.hornet_hole_kong:
                lambda state: self.can_cling(state) and self.has_squitter(state) and self.can_team_attack(state),
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
                lambda state: self.can_cling(state) and self.can_team_attack(state),
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
                lambda state: self.has_squawks(state) and self.can_cartwheel(state) and self.can_carry(state),

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
                self.can_team_attack,
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
                lambda state: self.can_climb(state) and self.can_cartwheel(state) and self.has_squawks(state),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.can_cartwheel(state) and self.has_squawks(state),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.can_cartwheel(state) and self.has_squawks(state),
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
        }

    def set_dkc2_rules(self) -> None:
        super().set_dkc2_rules()


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
                lambda state: self.can_carry(state) or self.has_both_kongs(state),
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
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),
            LocationName.barrel_bayou_kong:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state)
                ),
            LocationName.barrel_bayou_dk_coin:
                lambda state: self.has_controllable_barrels(state) and self.has_rambi(state),
            LocationName.barrel_bayou_bonus_1:
                lambda state: self.has_controllable_barrels(state) and self.can_carry(state),
            LocationName.barrel_bayou_bonus_2:
                lambda state: self.has_controllable_barrels(state) and self.has_kannons(state),

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
                lambda state: self.has_kannons(state) and self.can_hover(state) and self.can_team_attack(state) and 
                self.can_cartwheel(state),
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
                self.can_cling,
            LocationName.hornet_hole_kong:
                self.can_cling,
            LocationName.hornet_hole_dk_coin:
                lambda state: self.can_cling(state) and 
                    self.can_team_attack(state) and 
                    self.has_squitter(state),
            LocationName.hornet_hole_bonus_1:
                lambda state: self.can_cling(state) and 
                    self.can_team_attack(state) and 
                    self.can_carry(state),
            LocationName.hornet_hole_bonus_2:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
            LocationName.hornet_hole_bonus_3:
                lambda state: self.can_cling(state) and 
                    self.can_team_attack(state) and 
                    self.has_squitter(state),

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
                    self.has_squitter(state) and self.has_squawks(state),
            LocationName.bramble_scramble_bonus_1:
                lambda state: self.can_climb(state) and self.has_squawks(state) and ((
                    self.can_team_attack(state) and self.has_invincibility(state)
                    ) or (
                    self.can_hover(state) and self.has_kannons(state) and self.has_diddy(state) and
                    self.has_dixie(state)
                    )
                ),

            LocationName.rickety_race_clear:
                self.has_skull_kart,
            LocationName.rickety_race_kong:
                self.has_skull_kart,
            LocationName.rickety_race_dk_coin:
                self.has_skull_kart,
            LocationName.rickety_race_bonus_1:
                lambda state: self.has_skull_kart and 
                    self.can_team_attack(state) 
                    and self.can_hover(state),

            LocationName.mudhole_marsh_clear:
                lambda state: self.can_cling(state) and (
                    self.can_climb(state) or self.can_hover(state)
                ),
            LocationName.mudhole_marsh_kong:
                lambda state: self.can_cling(state) and self.can_carry(state) and (
                    self.can_climb(state) or self.can_hover(state)
                ),
            LocationName.mudhole_marsh_dk_coin:
                lambda state: self.can_cling(state) and (
                    self.can_climb(state) or self.can_hover(state)
                ),
            LocationName.mudhole_marsh_bonus_1:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
            LocationName.mudhole_marsh_bonus_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and (
                    self.can_climb(state) or self.can_hover(state)
                ),

            LocationName.rambi_rumble_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state),
            LocationName.rambi_rumble_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state) and ( 
                    self.can_cartwheel(state) or self.can_team_attack(state)),
            LocationName.rambi_rumble_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.rambi_rumble_bonus_1:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.rambi_rumble_bonus_2:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.has_rambi(state),

            LocationName.king_zing_sting_clear:
                self.has_squawks,
            LocationName.king_zing_defeated:
                self.has_squawks,

             LocationName.ghostly_grove_clear:
                self.can_climb,
            LocationName.ghostly_grove_kong:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.ghostly_grove_dk_coin:
                lambda state:  self.can_climb(state) and self.can_team_attack(state) and (
                    self.can_hover(state) or (self.can_cartwheel(state) and self.has_diddy(state))
                ),
            LocationName.ghostly_grove_bonus_1:
            lambda state: self.can_carry(state) and (
                    self.can_climb(state) and self.can_team_attack(state)
                ),
            LocationName.ghostly_grove_bonus_2:
                self.can_climb,

            LocationName.haunted_hall_clear:
                self.has_skull_kart,
            LocationName.haunted_hall_kong:
                self.has_skull_kart,
            LocationName.haunted_hall_dk_coin:
                self.has_skull_kart,
            LocationName.haunted_hall_bonus_1:
                self.has_skull_kart,
            LocationName.haunted_hall_bonus_2:
                self.has_skull_kart,
            LocationName.haunted_hall_bonus_3:
                self.has_skull_kart,

            LocationName.gusty_glade_clear:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_kong:
                lambda state: self.can_cling(state) and self.has_kannons(state) and self.can_carry(state) and
                    self.can_cartwheel(state),
            LocationName.gusty_glade_dk_coin:
                lambda state: self.can_cling(state) and self.has_kannons(state),
            LocationName.gusty_glade_bonus_1:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
            LocationName.gusty_glade_bonus_2:
                lambda state: self.can_cling(state) and self.can_carry(state) and self.has_kannons(state),

            LocationName.parrot_chute_panic_clear:
                lambda state: self.can_hover(state) or self.has_squawks(state),
            LocationName.parrot_chute_panic_kong:
                lambda state: self.can_hover(state) or self.has_squawks(state),
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
                        self.can_cartwheel(state) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_kong:
                lambda state: (
                    (self.can_swim(state) or self.has_enguarde(state)) and
                    (self.can_cartwheel(state) or self.can_hover(state))
                ),
            LocationName.arctic_abyss_dk_coin:
                lambda state: self.can_swim(state) or (
                    self.has_enguarde(state) and (
                        self.can_cartwheel(state) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_bonus_1:
                lambda state: self.has_enguarde(state) and ( 
                    self.can_swim(state) or (
                        self.can_cartwheel(state) or self.can_hover(state)
                    )
                ),
            LocationName.arctic_abyss_bonus_2:
                
                lambda state: self.can_carry(state) and (
                    self.can_swim(state) or (
                        self.has_enguarde(state) and (
                            self.can_cartwheel(state) or self.can_hover(state)
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
                lambda state: (self.can_hover or self.can_cartwheel(state)) or self.has_both_kongs(state),
            LocationName.castle_crush_kong:
                lambda state: self.can_hover or (self.can_cartwheel(state) or self.has_both_kongs(state)),
            LocationName.castle_crush_dk_coin:
                lambda state: self.has_squawks(state) and (
                    self.can_hover or (self.can_cartwheel(state) or self.has_both_kongs(state)),
                ),
            LocationName.castle_crush_bonus_1:
                lambda state: self.has_rambi(state) and self.has_both_kongs(state) and  self.can_carry(state),
            LocationName.castle_crush_bonus_2:
                lambda state: self.can_carry(state) and self.has_squawks(state) and (
                    self.has_both_kongs(state) or 
                    (self.can_hover or self.can_cartwheel(state))
                ),

            LocationName.clappers_cavern_clear:
                lambda state: self.has_clapper(state) and self.has_kannons(state) and ((
                    self.can_cling(state) and 
                        (self.has_enguarde(state) or self.can_swim(state))
                    ) or (
                        self.can_swim(state) and self.has_invincibility(state)
                    )
                ),
            LocationName.clappers_cavern_kong:
                lambda state: self.has_clapper(state) and self.has_kannons(state) and ((
                    self.can_cling(state) and 
                        (self.has_enguarde(state) or self.can_swim(state))
                    ) or (
                        self.can_swim(state) and self.has_invincibility(state) and self.can_team_attack(state)
                    )
                ),
            LocationName.clappers_cavern_dk_coin:
                self.can_team_attack,
            LocationName.clappers_cavern_bonus_1:
                lambda state: self.can_cling(state) and self.can_team_attack(state),
            LocationName.clappers_cavern_bonus_2:
                lambda state: self.has_clapper(state) and self.has_kannons(state) and self.has_enguarde(state),

            LocationName.chain_link_chamber_clear:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or self.has_kannons(state)
                ),
            LocationName.chain_link_chamber_kong:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or self.has_kannons(state)
                ),
            LocationName.chain_link_chamber_dk_coin:
                lambda state: self.can_climb(state) and (
                    self.can_cling(state) or self.has_kannons(state)
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
                    self.can_team_attack(state) or self.can_cartwheel(state)
                ),
            LocationName.screechs_sprint_kong:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state)
                ),
            LocationName.screechs_sprint_dk_coin:
                lambda state: self.can_climb(state) and self.has_squawks(state) and (
                    self.can_team_attack(state) or self.can_cartwheel(state)
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
            LocationName.jungle_jinx_kong:
                lambda state: self.can_cartwheel(state) and (
                    self.has_kannons(state) or self.can_hover(state)) and (
                    self.can_carry(state) or self.has_both_kongs(state) 
                ), 
            LocationName.jungle_jinx_dk_coin:
                lambda state: self.can_team_attack(state)  and (
                    self.can_cartwheel(state) or self.can_hover(state)
                ), 

            LocationName.black_ice_battle_kong:
                self.can_carry,
            LocationName.black_ice_battle_dk_coin:
                self.can_carry,

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
                lambda state: self.can_swim(state) and self.has_kannons(state) and
                    self.has_squitter and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_kong:
                lambda state: self.can_swim(state) and self.has_kannons(state) and
                    self.has_squitter and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),
            LocationName.animal_antics_dk_coin:
                lambda state: self.can_swim(state) and self.has_kannons(state) and
                    self.has_squitter and self.has_enguarde(state) and (
                        self.has_rambi(state) or (
                            self.can_hover(state) and self.can_team_attack(state)
                        )
                    ),

            LocationName.krocodile_core_clear:
                self.can_carry,
        }

    def set_dkc2_rules(self) -> None:
        super().set_dkc2_rules()
