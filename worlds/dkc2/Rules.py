
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC2World

from .Names import LocationName, ItemName, RegionName, EventName

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
        return state.has(ItemName.the_flying_krock, self.player)

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

        multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)
            

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
                lambda state: self.can_cling(state) and self.can_carry(state) and self.can_team_attack(state),
            LocationName.gangplank_galley_dk_coin:
                lambda state: self.can_cling(state) and (
                    self.can_hover(state) or self.can_cartwheel(state)
                ),
            LocationName.gangplank_galley_bonus_1:
                self.true,
            LocationName.gangplank_galley_bonus_2:
                self.true,

            LocationName.lockjaws_locker_clear:
                self.true,
            LocationName.lockjaws_locker_kong:
                self.true,
            LocationName.lockjaws_locker_dk_coin:
                self.true,
            LocationName.lockjaws_locker_bonus_1:
                self.true,

            LocationName.topsail_trouble_clear:
                self.true,
            LocationName.topsail_trouble_kong:
                self.true,
            LocationName.topsail_trouble_dk_coin:
                self.true,
            LocationName.topsail_trouble_bonus_1:
                self.true,
            LocationName.topsail_trouble_bonus_2:
                self.true,

            LocationName.krows_nest_clear:
                self.true,

            LocationName.hot_head_hop_clear:
                self.true,
            LocationName.hot_head_hop_kong:
                self.true,
            LocationName.hot_head_hop_dk_coin:
                self.true,
            LocationName.hot_head_hop_bonus_1:
                self.true,
            LocationName.hot_head_hop_bonus_2:
                self.true,
            LocationName.hot_head_hop_bonus_3:
                self.true,

            LocationName.kannons_klaim_clear:
                self.true,
            LocationName.kannons_klaim_kong:
                self.true,
            LocationName.kannons_klaim_dk_coin:
                self.true,
            LocationName.kannons_klaim_bonus_1:
                self.true,
            LocationName.kannons_klaim_bonus_2:
                self.true,
            LocationName.kannons_klaim_bonus_3:
                self.true,

            LocationName.lava_lagoon_clear:
                self.true,
            LocationName.lava_lagoon_kong:
                self.true,
            LocationName.lava_lagoon_dk_coin:
                self.true,
            LocationName.lava_lagoon_bonus_1:
                self.true,

            LocationName.red_hot_ride_clear:
                self.true,
            LocationName.red_hot_ride_kong:
                self.true,
            LocationName.red_hot_ride_dk_coin:
                self.true,
            LocationName.red_hot_ride_bonus_1:
                self.true,
            LocationName.red_hot_ride_bonus_2:
                self.true,

            LocationName.squawks_shaft_clear:
                self.true,
            LocationName.squawks_shaft_kong:
                self.true,
            LocationName.squawks_shaft_dk_coin:
                self.true,
            LocationName.squawks_shaft_bonus_1:
                self.true,
            LocationName.squawks_shaft_bonus_2:
                self.true,
            LocationName.squawks_shaft_bonus_3:
                self.true,

            LocationName.kleevers_kiln_clear:
                self.true,

            LocationName.barrel_bayou_clear:
                self.true,
            LocationName.barrel_bayou_kong:
                self.true,
            LocationName.barrel_bayou_dk_coin:
                self.true,
            LocationName.barrel_bayou_bonus_1:
                self.true,
            LocationName.barrel_bayou_bonus_2:
                self.true,

            LocationName.glimmers_galleon_clear:
                self.true,
            LocationName.glimmers_galleon_kong:
                self.true,
            LocationName.glimmers_galleon_dk_coin:
                self.true,
            LocationName.glimmers_galleon_bonus_1:
                self.true,
            LocationName.glimmers_galleon_bonus_2:
                self.true,

            LocationName.krockhead_klamber_clear:
                self.true,
            LocationName.krockhead_klamber_kong:
                self.true,
            LocationName.krockhead_klamber_dk_coin:
                self.true,
            LocationName.krockhead_klamber_bonus_1:
                self.true,

            LocationName.rattle_battle_clear:
                self.true,
            LocationName.rattle_battle_kong:
                self.true,
            LocationName.rattle_battle_dk_coin:
                self.true,
            LocationName.rattle_battle_bonus_1:
                self.true,
            LocationName.rattle_battle_bonus_2:
                self.true,
            LocationName.rattle_battle_bonus_3:
                self.true,

            LocationName.slime_climb_clear:
                self.true,
            LocationName.slime_climb_kong:
                self.true,
            LocationName.slime_climb_dk_coin:
                self.true,
            LocationName.slime_climb_bonus_1:
                self.true,
            LocationName.slime_climb_bonus_2:
                self.true,

            LocationName.bramble_blast_clear:
                self.true,
            LocationName.bramble_blast_kong:
                self.true,
            LocationName.bramble_blast_dk_coin:
                self.true,
            LocationName.bramble_blast_bonus_1:
                self.true,
            LocationName.bramble_blast_bonus_2:
                self.true,

            LocationName.kudgels_kontest_clear:
                self.true,

            LocationName.hornet_hole_clear:
                self.true,
            LocationName.hornet_hole_kong:
                self.true,
            LocationName.hornet_hole_dk_coin:
                self.true,
            LocationName.hornet_hole_bonus_1:
                self.true,
            LocationName.hornet_hole_bonus_2:
                self.true,
            LocationName.hornet_hole_bonus_3:
                self.true,

            LocationName.target_terror_clear:
                self.true,
            LocationName.target_terror_kong:
                self.true,
            LocationName.target_terror_dk_coin:
                self.true,
            LocationName.target_terror_bonus_1:
                self.true,
            LocationName.target_terror_bonus_2:
                self.true,

            LocationName.bramble_scramble_clear:
                self.true,
            LocationName.bramble_scramble_kong:
                self.true,
            LocationName.bramble_scramble_dk_coin:
                self.true,
            LocationName.bramble_scramble_bonus_1:
                self.true,

            LocationName.rickety_race_clear:
                self.true,
            LocationName.rickety_race_kong:
                self.true,
            LocationName.rickety_race_dk_coin:
                self.true,
            LocationName.rickety_race_bonus_1:
                self.true,

            LocationName.mudhole_marsh_clear:
                self.true,
            LocationName.mudhole_marsh_kong:
                self.true,
            LocationName.mudhole_marsh_dk_coin:
                self.true,
            LocationName.mudhole_marsh_bonus_1:
                self.true,
            LocationName.mudhole_marsh_bonus_2:
                self.true,

            LocationName.rambi_rumble_clear:
                self.true,
            LocationName.rambi_rumble_kong:
                self.true,
            LocationName.rambi_rumble_dk_coin:
                self.true,
            LocationName.rambi_rumble_bonus_1:
                self.true,
            LocationName.rambi_rumble_bonus_2:
                self.true,

            LocationName.king_zing_sting_clear:
                self.true,

            LocationName.ghostly_grove_clear:
                self.true,
            LocationName.ghostly_grove_kong:
                self.true,
            LocationName.ghostly_grove_dk_coin:
                self.true,
            LocationName.ghostly_grove_bonus_1:
                self.true,
            LocationName.ghostly_grove_bonus_2:
                self.true,

            LocationName.haunted_hall_clear:
                self.true,
            LocationName.haunted_hall_kong:
                self.true,
            LocationName.haunted_hall_dk_coin:
                self.true,
            LocationName.haunted_hall_bonus_1:
                self.true,
            LocationName.haunted_hall_bonus_2:
                self.true,
            LocationName.haunted_hall_bonus_3:
                self.true,

            LocationName.gusty_glade_clear:
                self.true,
            LocationName.gusty_glade_kong:
                self.true,
            LocationName.gusty_glade_dk_coin:
                self.true,
            LocationName.gusty_glade_bonus_1:
                self.true,
            LocationName.gusty_glade_bonus_2:
                self.true,

            LocationName.parrot_chute_panic_clear:
                self.true,
            LocationName.parrot_chute_panic_kong:
                self.true,
            LocationName.parrot_chute_panic_dk_coin:
                self.true,
            LocationName.parrot_chute_panic_bonus_1:
                self.true,
            LocationName.parrot_chute_panic_bonus_2:
                self.true,

            LocationName.web_woods_clear:
                self.true,
            LocationName.web_woods_kong:
                self.true,
            LocationName.web_woods_dk_coin:
                self.true,
            LocationName.web_woods_bonus_1:
                self.true,
            LocationName.web_woods_bonus_2:
                self.true,

            LocationName.kreepy_krow_clear:
                self.true,

            LocationName.arctic_abyss_clear:
                self.true,
            LocationName.arctic_abyss_kong:
                self.true,
            LocationName.arctic_abyss_dk_coin:
                self.true,
            LocationName.arctic_abyss_bonus_1:
                self.true,
            LocationName.arctic_abyss_bonus_2:
                self.true,

            LocationName.windy_well_clear:
                self.true,
            LocationName.windy_well_kong:
                self.true,
            LocationName.windy_well_dk_coin:
                self.true,
            LocationName.windy_well_bonus_1:
                self.true,
            LocationName.windy_well_bonus_2:
                self.true,

            LocationName.castle_crush_clear:
                self.true,
            LocationName.castle_crush_kong:
                self.true,
            LocationName.castle_crush_dk_coin:
                self.true,
            LocationName.castle_crush_bonus_1:
                self.true,
            LocationName.castle_crush_bonus_2:
                self.true,

            LocationName.clappers_cavern_clear:
                self.true,
            LocationName.clappers_cavern_kong:
                self.true,
            LocationName.clappers_cavern_dk_coin:
                self.true,
            LocationName.clappers_cavern_bonus_1:
                self.true,
            LocationName.clappers_cavern_bonus_2:
                self.true,

            LocationName.chain_link_chamber_clear:
                self.true,
            LocationName.chain_link_chamber_kong:
                self.true,
            LocationName.chain_link_chamber_dk_coin:
                self.true,
            LocationName.chain_link_chamber_bonus_1:
                self.true,
            LocationName.chain_link_chamber_bonus_2:
                self.true,

            LocationName.toxic_tower_clear:
                self.true,
            LocationName.toxic_tower_kong:
                self.true,
            LocationName.toxic_tower_dk_coin:
                self.true,
            LocationName.toxic_tower_bonus_1:
                self.true,

            LocationName.stronghold_showdown_clear:
                self.true,

            LocationName.screechs_sprint_clear:
                self.true,
            LocationName.screechs_sprint_kong:
                self.true,
            LocationName.screechs_sprint_dk_coin:
                self.true,
            LocationName.screechs_sprint_bonus_1:
                self.true,

            LocationName.k_rool_duel_clear:
                self.true,

            LocationName.jungle_jinx_clear:
                self.true,
            LocationName.jungle_jinx_kong:
                self.true,
            LocationName.jungle_jinx_dk_coin:
                self.true,

            LocationName.black_ice_battle_clear:
                self.true,
            LocationName.black_ice_battle_kong:
                self.true,
            LocationName.black_ice_battle_dk_coin:
                self.true,

            LocationName.klobber_karnage_clear:
                self.true,
            LocationName.klobber_karnage_kong:
                self.true,
            LocationName.klobber_karnage_dk_coin:
                self.true,

            LocationName.fiery_furnace_clear:
                self.true,
            LocationName.fiery_furnace_kong:
                self.true,
            LocationName.fiery_furnace_dk_coin:
                self.true,

            LocationName.animal_antics_clear:
                self.true,
            LocationName.animal_antics_kong:
                self.true,
            LocationName.animal_antics_dk_coin:
                self.true,

            LocationName.krocodile_core_clear:
                self.true,
        }

    def set_dkc2_rules(self) -> None:
        super().set_dkc2_rules()


class DKC2NormalRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                lambda state: self.can_carry(state) or self.has_rambi(state),

            LocationName.mainbrace_mayhem_clear:
                self.true,
            LocationName.mainbrace_mayhem_kong:
                self.true,
            LocationName.mainbrace_mayhem_dk_coin:
                self.true,
            LocationName.mainbrace_mayhem_bonus_1:
                self.true,
            LocationName.mainbrace_mayhem_bonus_2:
                self.true,
            LocationName.mainbrace_mayhem_bonus_3:
                self.true,

            LocationName.gangplank_galley_clear:
                self.true,
            LocationName.gangplank_galley_kong:
                self.true,
            LocationName.gangplank_galley_dk_coin:
                self.true,
            LocationName.gangplank_galley_bonus_1:
                self.true,
            LocationName.gangplank_galley_bonus_2:
                self.true,

            LocationName.lockjaws_locker_clear:
                self.true,
            LocationName.lockjaws_locker_kong:
                self.true,
            LocationName.lockjaws_locker_dk_coin:
                self.true,
            LocationName.lockjaws_locker_bonus_1:
                self.true,

            LocationName.topsail_trouble_clear:
                self.true,
            LocationName.topsail_trouble_kong:
                self.true,
            LocationName.topsail_trouble_dk_coin:
                self.true,
            LocationName.topsail_trouble_bonus_1:
                self.true,
            LocationName.topsail_trouble_bonus_2:
                self.true,

            LocationName.krows_nest_clear:
                self.true,

            LocationName.hot_head_hop_clear:
                self.true,
            LocationName.hot_head_hop_kong:
                self.true,
            LocationName.hot_head_hop_dk_coin:
                self.true,
            LocationName.hot_head_hop_bonus_1:
                self.true,
            LocationName.hot_head_hop_bonus_2:
                self.true,
            LocationName.hot_head_hop_bonus_3:
                self.true,

            LocationName.kannons_klaim_clear:
                self.true,
            LocationName.kannons_klaim_kong:
                self.true,
            LocationName.kannons_klaim_dk_coin:
                self.true,
            LocationName.kannons_klaim_bonus_1:
                self.true,
            LocationName.kannons_klaim_bonus_2:
                self.true,
            LocationName.kannons_klaim_bonus_3:
                self.true,

            LocationName.lava_lagoon_clear:
                self.true,
            LocationName.lava_lagoon_kong:
                self.true,
            LocationName.lava_lagoon_dk_coin:
                self.true,
            LocationName.lava_lagoon_bonus_1:
                self.true,

            LocationName.red_hot_ride_clear:
                self.true,
            LocationName.red_hot_ride_kong:
                self.true,
            LocationName.red_hot_ride_dk_coin:
                self.true,
            LocationName.red_hot_ride_bonus_1:
                self.true,
            LocationName.red_hot_ride_bonus_2:
                self.true,

            LocationName.squawks_shaft_clear:
                self.true,
            LocationName.squawks_shaft_kong:
                self.true,
            LocationName.squawks_shaft_dk_coin:
                self.true,
            LocationName.squawks_shaft_bonus_1:
                self.true,
            LocationName.squawks_shaft_bonus_2:
                self.true,
            LocationName.squawks_shaft_bonus_3:
                self.true,

            LocationName.kleevers_kiln_clear:
                self.true,

            LocationName.barrel_bayou_clear:
                self.true,
            LocationName.barrel_bayou_kong:
                self.true,
            LocationName.barrel_bayou_dk_coin:
                self.true,
            LocationName.barrel_bayou_bonus_1:
                self.true,
            LocationName.barrel_bayou_bonus_2:
                self.true,

            LocationName.glimmers_galleon_clear:
                self.true,
            LocationName.glimmers_galleon_kong:
                self.true,
            LocationName.glimmers_galleon_dk_coin:
                self.true,
            LocationName.glimmers_galleon_bonus_1:
                self.true,
            LocationName.glimmers_galleon_bonus_2:
                self.true,

            LocationName.krockhead_klamber_clear:
                self.true,
            LocationName.krockhead_klamber_kong:
                self.true,
            LocationName.krockhead_klamber_dk_coin:
                self.true,
            LocationName.krockhead_klamber_bonus_1:
                self.true,

            LocationName.rattle_battle_clear:
                self.true,
            LocationName.rattle_battle_kong:
                self.true,
            LocationName.rattle_battle_dk_coin:
                self.true,
            LocationName.rattle_battle_bonus_1:
                self.true,
            LocationName.rattle_battle_bonus_2:
                self.true,
            LocationName.rattle_battle_bonus_3:
                self.true,

            LocationName.slime_climb_clear:
                self.true,
            LocationName.slime_climb_kong:
                self.true,
            LocationName.slime_climb_dk_coin:
                self.true,
            LocationName.slime_climb_bonus_1:
                self.true,
            LocationName.slime_climb_bonus_2:
                self.true,

            LocationName.bramble_blast_clear:
                self.true,
            LocationName.bramble_blast_kong:
                self.true,
            LocationName.bramble_blast_dk_coin:
                self.true,
            LocationName.bramble_blast_bonus_1:
                self.true,
            LocationName.bramble_blast_bonus_2:
                self.true,

            LocationName.kudgels_kontest_clear:
                self.true,

            LocationName.hornet_hole_clear:
                self.true,
            LocationName.hornet_hole_kong:
                self.true,
            LocationName.hornet_hole_dk_coin:
                self.true,
            LocationName.hornet_hole_bonus_1:
                self.true,
            LocationName.hornet_hole_bonus_2:
                self.true,
            LocationName.hornet_hole_bonus_3:
                self.true,

            LocationName.target_terror_clear:
                self.true,
            LocationName.target_terror_kong:
                self.true,
            LocationName.target_terror_dk_coin:
                self.true,
            LocationName.target_terror_bonus_1:
                self.true,
            LocationName.target_terror_bonus_2:
                self.true,

            LocationName.bramble_scramble_clear:
                self.true,
            LocationName.bramble_scramble_kong:
                self.true,
            LocationName.bramble_scramble_dk_coin:
                self.true,
            LocationName.bramble_scramble_bonus_1:
                self.true,

            LocationName.rickety_race_clear:
                self.true,
            LocationName.rickety_race_kong:
                self.true,
            LocationName.rickety_race_dk_coin:
                self.true,
            LocationName.rickety_race_bonus_1:
                self.true,

            LocationName.mudhole_marsh_clear:
                self.true,
            LocationName.mudhole_marsh_kong:
                self.true,
            LocationName.mudhole_marsh_dk_coin:
                self.true,
            LocationName.mudhole_marsh_bonus_1:
                self.true,
            LocationName.mudhole_marsh_bonus_2:
                self.true,

            LocationName.rambi_rumble_clear:
                self.true,
            LocationName.rambi_rumble_kong:
                self.true,
            LocationName.rambi_rumble_dk_coin:
                self.true,
            LocationName.rambi_rumble_bonus_1:
                self.true,
            LocationName.rambi_rumble_bonus_2:
                self.true,

            LocationName.king_zing_sting_clear:
                self.true,

            LocationName.ghostly_grove_clear:
                self.true,
            LocationName.ghostly_grove_kong:
                self.true,
            LocationName.ghostly_grove_dk_coin:
                self.true,
            LocationName.ghostly_grove_bonus_1:
                self.true,
            LocationName.ghostly_grove_bonus_2:
                self.true,

            LocationName.haunted_hall_clear:
                self.true,
            LocationName.haunted_hall_kong:
                self.true,
            LocationName.haunted_hall_dk_coin:
                self.true,
            LocationName.haunted_hall_bonus_1:
                self.true,
            LocationName.haunted_hall_bonus_2:
                self.true,
            LocationName.haunted_hall_bonus_3:
                self.true,

            LocationName.gusty_glade_clear:
                self.true,
            LocationName.gusty_glade_kong:
                self.true,
            LocationName.gusty_glade_dk_coin:
                self.true,
            LocationName.gusty_glade_bonus_1:
                self.true,
            LocationName.gusty_glade_bonus_2:
                self.true,

            LocationName.parrot_chute_panic_clear:
                self.true,
            LocationName.parrot_chute_panic_kong:
                self.true,
            LocationName.parrot_chute_panic_dk_coin:
                self.true,
            LocationName.parrot_chute_panic_bonus_1:
                self.true,
            LocationName.parrot_chute_panic_bonus_2:
                self.true,

            LocationName.web_woods_clear:
                self.true,
            LocationName.web_woods_kong:
                self.true,
            LocationName.web_woods_dk_coin:
                self.true,
            LocationName.web_woods_bonus_1:
                self.true,
            LocationName.web_woods_bonus_2:
                self.true,

            LocationName.kreepy_krow_clear:
                self.true,

            LocationName.arctic_abyss_clear:
                self.true,
            LocationName.arctic_abyss_kong:
                self.true,
            LocationName.arctic_abyss_dk_coin:
                self.true,
            LocationName.arctic_abyss_bonus_1:
                self.true,
            LocationName.arctic_abyss_bonus_2:
                self.true,

            LocationName.windy_well_clear:
                self.true,
            LocationName.windy_well_kong:
                self.true,
            LocationName.windy_well_dk_coin:
                self.true,
            LocationName.windy_well_bonus_1:
                self.true,
            LocationName.windy_well_bonus_2:
                self.true,

            LocationName.castle_crush_clear:
                self.true,
            LocationName.castle_crush_kong:
                self.true,
            LocationName.castle_crush_dk_coin:
                self.true,
            LocationName.castle_crush_bonus_1:
                self.true,
            LocationName.castle_crush_bonus_2:
                self.true,

            LocationName.clappers_cavern_clear:
                self.true,
            LocationName.clappers_cavern_kong:
                self.true,
            LocationName.clappers_cavern_dk_coin:
                self.true,
            LocationName.clappers_cavern_bonus_1:
                self.true,
            LocationName.clappers_cavern_bonus_2:
                self.true,

            LocationName.chain_link_chamber_clear:
                self.true,
            LocationName.chain_link_chamber_kong:
                self.true,
            LocationName.chain_link_chamber_dk_coin:
                self.true,
            LocationName.chain_link_chamber_bonus_1:
                self.true,
            LocationName.chain_link_chamber_bonus_2:
                self.true,

            LocationName.toxic_tower_clear:
                self.true,
            LocationName.toxic_tower_kong:
                self.true,
            LocationName.toxic_tower_dk_coin:
                self.true,
            LocationName.toxic_tower_bonus_1:
                self.true,

            LocationName.stronghold_showdown_clear:
                self.true,

            LocationName.screechs_sprint_clear:
                self.true,
            LocationName.screechs_sprint_kong:
                self.true,
            LocationName.screechs_sprint_dk_coin:
                self.true,
            LocationName.screechs_sprint_bonus_1:
                self.true,

            LocationName.k_rool_duel_clear:
                self.true,

            LocationName.jungle_jinx_clear:
                self.true,
            LocationName.jungle_jinx_kong:
                self.true,
            LocationName.jungle_jinx_dk_coin:
                self.true,

            LocationName.black_ice_battle_clear:
                self.true,
            LocationName.black_ice_battle_kong:
                self.true,
            LocationName.black_ice_battle_dk_coin:
                self.true,

            LocationName.klobber_karnage_clear:
                self.true,
            LocationName.klobber_karnage_kong:
                self.true,
            LocationName.klobber_karnage_dk_coin:
                self.true,

            LocationName.fiery_furnace_clear:
                self.true,
            LocationName.fiery_furnace_kong:
                self.true,
            LocationName.fiery_furnace_dk_coin:
                self.true,

            LocationName.animal_antics_clear:
                self.true,
            LocationName.animal_antics_kong:
                self.true,
            LocationName.animal_antics_dk_coin:
                self.true,

            LocationName.krocodile_core_clear:
                self.true,
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
                self.true,
            LocationName.mainbrace_mayhem_kong:
                self.true,
            LocationName.mainbrace_mayhem_dk_coin:
                self.true,
            LocationName.mainbrace_mayhem_bonus_1:
                self.true,
            LocationName.mainbrace_mayhem_bonus_2:
                self.true,
            LocationName.mainbrace_mayhem_bonus_3:
                self.true,

            LocationName.gangplank_galley_clear:
                self.true,
            LocationName.gangplank_galley_kong:
                self.true,
            LocationName.gangplank_galley_dk_coin:
                self.true,
            LocationName.gangplank_galley_bonus_1:
                self.true,
            LocationName.gangplank_galley_bonus_2:
                self.true,

            LocationName.lockjaws_locker_clear:
                self.true,
            LocationName.lockjaws_locker_kong:
                self.true,
            LocationName.lockjaws_locker_dk_coin:
                self.true,
            LocationName.lockjaws_locker_bonus_1:
                self.true,

            LocationName.topsail_trouble_clear:
                self.true,
            LocationName.topsail_trouble_kong:
                self.true,
            LocationName.topsail_trouble_dk_coin:
                self.true,
            LocationName.topsail_trouble_bonus_1:
                self.true,
            LocationName.topsail_trouble_bonus_2:
                self.true,

            LocationName.krows_nest_clear:
                self.true,

            LocationName.hot_head_hop_clear:
                self.true,
            LocationName.hot_head_hop_kong:
                self.true,
            LocationName.hot_head_hop_dk_coin:
                self.true,
            LocationName.hot_head_hop_bonus_1:
                self.true,
            LocationName.hot_head_hop_bonus_2:
                self.true,
            LocationName.hot_head_hop_bonus_3:
                self.true,

            LocationName.kannons_klaim_clear:
                self.true,
            LocationName.kannons_klaim_kong:
                self.true,
            LocationName.kannons_klaim_dk_coin:
                self.true,
            LocationName.kannons_klaim_bonus_1:
                self.true,
            LocationName.kannons_klaim_bonus_2:
                self.true,
            LocationName.kannons_klaim_bonus_3:
                self.true,

            LocationName.lava_lagoon_clear:
                self.true,
            LocationName.lava_lagoon_kong:
                self.true,
            LocationName.lava_lagoon_dk_coin:
                self.true,
            LocationName.lava_lagoon_bonus_1:
                self.true,

            LocationName.red_hot_ride_clear:
                self.true,
            LocationName.red_hot_ride_kong:
                self.true,
            LocationName.red_hot_ride_dk_coin:
                self.true,
            LocationName.red_hot_ride_bonus_1:
                self.true,
            LocationName.red_hot_ride_bonus_2:
                self.true,

            LocationName.squawks_shaft_clear:
                self.true,
            LocationName.squawks_shaft_kong:
                self.true,
            LocationName.squawks_shaft_dk_coin:
                self.true,
            LocationName.squawks_shaft_bonus_1:
                self.true,
            LocationName.squawks_shaft_bonus_2:
                self.true,
            LocationName.squawks_shaft_bonus_3:
                self.true,

            LocationName.kleevers_kiln_clear:
                self.true,

            LocationName.barrel_bayou_clear:
                self.true,
            LocationName.barrel_bayou_kong:
                self.true,
            LocationName.barrel_bayou_dk_coin:
                self.true,
            LocationName.barrel_bayou_bonus_1:
                self.true,
            LocationName.barrel_bayou_bonus_2:
                self.true,

            LocationName.glimmers_galleon_clear:
                self.true,
            LocationName.glimmers_galleon_kong:
                self.true,
            LocationName.glimmers_galleon_dk_coin:
                self.true,
            LocationName.glimmers_galleon_bonus_1:
                self.true,
            LocationName.glimmers_galleon_bonus_2:
                self.true,

            LocationName.krockhead_klamber_clear:
                self.true,
            LocationName.krockhead_klamber_kong:
                self.true,
            LocationName.krockhead_klamber_dk_coin:
                self.true,
            LocationName.krockhead_klamber_bonus_1:
                self.true,

            LocationName.rattle_battle_clear:
                self.true,
            LocationName.rattle_battle_kong:
                self.true,
            LocationName.rattle_battle_dk_coin:
                self.true,
            LocationName.rattle_battle_bonus_1:
                self.true,
            LocationName.rattle_battle_bonus_2:
                self.true,
            LocationName.rattle_battle_bonus_3:
                self.true,

            LocationName.slime_climb_clear:
                self.true,
            LocationName.slime_climb_kong:
                self.true,
            LocationName.slime_climb_dk_coin:
                self.true,
            LocationName.slime_climb_bonus_1:
                self.true,
            LocationName.slime_climb_bonus_2:
                self.true,

            LocationName.bramble_blast_clear:
                self.true,
            LocationName.bramble_blast_kong:
                self.true,
            LocationName.bramble_blast_dk_coin:
                self.true,
            LocationName.bramble_blast_bonus_1:
                self.true,
            LocationName.bramble_blast_bonus_2:
                self.true,

            LocationName.kudgels_kontest_clear:
                self.true,

            LocationName.hornet_hole_clear:
                self.true,
            LocationName.hornet_hole_kong:
                self.true,
            LocationName.hornet_hole_dk_coin:
                self.true,
            LocationName.hornet_hole_bonus_1:
                self.true,
            LocationName.hornet_hole_bonus_2:
                self.true,
            LocationName.hornet_hole_bonus_3:
                self.true,

            LocationName.target_terror_clear:
                self.true,
            LocationName.target_terror_kong:
                self.true,
            LocationName.target_terror_dk_coin:
                self.true,
            LocationName.target_terror_bonus_1:
                self.true,
            LocationName.target_terror_bonus_2:
                self.true,

            LocationName.bramble_scramble_clear:
                self.true,
            LocationName.bramble_scramble_kong:
                self.true,
            LocationName.bramble_scramble_dk_coin:
                self.true,
            LocationName.bramble_scramble_bonus_1:
                self.true,

            LocationName.rickety_race_clear:
                self.true,
            LocationName.rickety_race_kong:
                self.true,
            LocationName.rickety_race_dk_coin:
                self.true,
            LocationName.rickety_race_bonus_1:
                self.true,

            LocationName.mudhole_marsh_clear:
                self.true,
            LocationName.mudhole_marsh_kong:
                self.true,
            LocationName.mudhole_marsh_dk_coin:
                self.true,
            LocationName.mudhole_marsh_bonus_1:
                self.true,
            LocationName.mudhole_marsh_bonus_2:
                self.true,

            LocationName.rambi_rumble_clear:
                self.true,
            LocationName.rambi_rumble_kong:
                self.true,
            LocationName.rambi_rumble_dk_coin:
                self.true,
            LocationName.rambi_rumble_bonus_1:
                self.true,
            LocationName.rambi_rumble_bonus_2:
                self.true,

            LocationName.king_zing_sting_clear:
                self.true,

            LocationName.ghostly_grove_clear:
                self.true,
            LocationName.ghostly_grove_kong:
                self.true,
            LocationName.ghostly_grove_dk_coin:
                self.true,
            LocationName.ghostly_grove_bonus_1:
                self.true,
            LocationName.ghostly_grove_bonus_2:
                self.true,

            LocationName.haunted_hall_clear:
                self.true,
            LocationName.haunted_hall_kong:
                self.true,
            LocationName.haunted_hall_dk_coin:
                self.true,
            LocationName.haunted_hall_bonus_1:
                self.true,
            LocationName.haunted_hall_bonus_2:
                self.true,
            LocationName.haunted_hall_bonus_3:
                self.true,

            LocationName.gusty_glade_clear:
                self.true,
            LocationName.gusty_glade_kong:
                self.true,
            LocationName.gusty_glade_dk_coin:
                self.true,
            LocationName.gusty_glade_bonus_1:
                self.true,
            LocationName.gusty_glade_bonus_2:
                self.true,

            LocationName.parrot_chute_panic_clear:
                self.true,
            LocationName.parrot_chute_panic_kong:
                self.true,
            LocationName.parrot_chute_panic_dk_coin:
                self.true,
            LocationName.parrot_chute_panic_bonus_1:
                self.true,
            LocationName.parrot_chute_panic_bonus_2:
                self.true,

            LocationName.web_woods_clear:
                self.true,
            LocationName.web_woods_kong:
                self.true,
            LocationName.web_woods_dk_coin:
                self.true,
            LocationName.web_woods_bonus_1:
                self.true,
            LocationName.web_woods_bonus_2:
                self.true,

            LocationName.kreepy_krow_clear:
                self.true,

            LocationName.arctic_abyss_clear:
                self.true,
            LocationName.arctic_abyss_kong:
                self.true,
            LocationName.arctic_abyss_dk_coin:
                self.true,
            LocationName.arctic_abyss_bonus_1:
                self.true,
            LocationName.arctic_abyss_bonus_2:
                self.true,

            LocationName.windy_well_clear:
                self.true,
            LocationName.windy_well_kong:
                self.true,
            LocationName.windy_well_dk_coin:
                self.true,
            LocationName.windy_well_bonus_1:
                self.true,
            LocationName.windy_well_bonus_2:
                self.true,

            LocationName.castle_crush_clear:
                self.true,
            LocationName.castle_crush_kong:
                self.true,
            LocationName.castle_crush_dk_coin:
                self.true,
            LocationName.castle_crush_bonus_1:
                self.true,
            LocationName.castle_crush_bonus_2:
                self.true,

            LocationName.clappers_cavern_clear:
                self.true,
            LocationName.clappers_cavern_kong:
                self.true,
            LocationName.clappers_cavern_dk_coin:
                self.true,
            LocationName.clappers_cavern_bonus_1:
                self.true,
            LocationName.clappers_cavern_bonus_2:
                self.true,

            LocationName.chain_link_chamber_clear:
                self.true,
            LocationName.chain_link_chamber_kong:
                self.true,
            LocationName.chain_link_chamber_dk_coin:
                self.true,
            LocationName.chain_link_chamber_bonus_1:
                self.true,
            LocationName.chain_link_chamber_bonus_2:
                self.true,

            LocationName.toxic_tower_clear:
                self.true,
            LocationName.toxic_tower_kong:
                self.true,
            LocationName.toxic_tower_dk_coin:
                self.true,
            LocationName.toxic_tower_bonus_1:
                self.true,

            LocationName.stronghold_showdown_clear:
                self.true,

            LocationName.screechs_sprint_clear:
                self.true,
            LocationName.screechs_sprint_kong:
                self.true,
            LocationName.screechs_sprint_dk_coin:
                self.true,
            LocationName.screechs_sprint_bonus_1:
                self.true,

            LocationName.k_rool_duel_clear:
                self.true,

            LocationName.jungle_jinx_clear:
                self.true,
            LocationName.jungle_jinx_kong:
                self.true,
            LocationName.jungle_jinx_dk_coin:
                self.true,

            LocationName.black_ice_battle_clear:
                self.true,
            LocationName.black_ice_battle_kong:
                self.true,
            LocationName.black_ice_battle_dk_coin:
                self.true,

            LocationName.klobber_karnage_clear:
                self.true,
            LocationName.klobber_karnage_kong:
                self.true,
            LocationName.klobber_karnage_dk_coin:
                self.true,

            LocationName.fiery_furnace_clear:
                self.true,
            LocationName.fiery_furnace_kong:
                self.true,
            LocationName.fiery_furnace_dk_coin:
                self.true,

            LocationName.animal_antics_clear:
                self.true,
            LocationName.animal_antics_kong:
                self.true,
            LocationName.animal_antics_dk_coin:
                self.true,

            LocationName.krocodile_core_clear:
                self.true,
        }

    def set_dkc2_rules(self) -> None:
        super().set_dkc2_rules()
