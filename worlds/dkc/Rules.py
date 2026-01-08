from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKCWorld

from .Names import LocationName, ItemName, RegionName, EventName

from worlds.generic.Rules import CollectionRule, add_rule
from BaseClasses import CollectionState
  
class DKCRules:
    player: int
    world: "DKCWorld"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "DKCWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.dk_isle} -> {RegionName.kongo_jungle}":
                self.can_access_jungle,
            f"{RegionName.dk_isle} -> {RegionName.monkey_mines}":
                self.can_access_mines,
            f"{RegionName.dk_isle} -> {RegionName.vine_valley}":
                self.can_access_valley,
            f"{RegionName.dk_isle} -> {RegionName.gorilla_glacier}":
                self.can_access_glacier,
            f"{RegionName.dk_isle} -> {RegionName.kremkroc_industries}":
                self.can_access_industries,
            f"{RegionName.dk_isle} -> {RegionName.chimp_caverns}":
                self.can_access_caverns,
            f"{RegionName.dk_isle} -> {RegionName.gangplank_galleon}":
                self.can_access_ship,
            f"{RegionName.kongo_jungle} -> {RegionName.very_gnawty_lair_map}":
                self.can_access_very_gnawty,
            f"{RegionName.monkey_mines} -> {RegionName.necky_nuts_map}":
                self.can_access_master_necky,
            f"{RegionName.vine_valley} -> {RegionName.bumble_b_rumble_map}":
                self.can_access_queen_b,
            f"{RegionName.gorilla_glacier} -> {RegionName.really_gnawty_rampage_map}":
                self.can_access_really_gnawty,
            f"{RegionName.kremkroc_industries} -> {RegionName.boss_dumb_drum_map}":
                self.can_access_dumb_drum,
            f"{RegionName.chimp_caverns} -> {RegionName.necky_revenge_map}":
                self.can_access_master_necky_snr,
        }

    def can_access_jungle(self, state: CollectionState) -> bool:
        return state.has(ItemName.kongo_jungle, self.player)
        
    def can_access_mines(self, state: CollectionState) -> bool:
        return state.has(ItemName.monkey_mines, self.player)

    def can_access_valley(self, state: CollectionState) -> bool:
        return state.has(ItemName.vine_valley, self.player)

    def can_access_glacier(self, state: CollectionState) -> bool:
        return state.has(ItemName.gorilla_glacier, self.player)

    def can_access_industries(self, state: CollectionState) -> bool:
        return state.has(ItemName.kremkroc_industries, self.player)

    def can_access_caverns(self, state: CollectionState) -> bool:
        return state.has(ItemName.chimp_caverns, self.player)
        
    def can_access_ship(self, state: CollectionState) -> bool:
        return state.has(ItemName.boss_token, self.player, self.world.options.gangplank_tokens.value)
    

    def can_access_jungle_glitched(self, state: CollectionState) -> bool:
        return self.can_access_jungle(state) or (
                self.can_access_valley_glitched(state) and self.has_both_kongs(state) and self.can_carry(state) and (
                self.has_expresso(state) or self.can_roll(state))
            )
    
    def can_access_mines_glitched(self, state: CollectionState) -> bool:
        return self.can_access_mines(state) or (
                self.has_both_kongs(state) and self.can_carry(state) and (
                self.can_access_caverns_glitched(state) or (self.can_access_valley_glitched(state) and self.has_expresso(state)))
            )
    
    def can_access_valley_glitched(self, state: CollectionState) -> bool:
        return self.can_access_valley(state) or self.can_access_jungle(state)

    def can_access_glacier_glitched(self, state: CollectionState) -> bool:
        return self.can_access_glacier(state) or (
                self.can_carry(state) and ((
                    self.can_access_jungle_glitched(state) and self.has_donkey(state)) or (
                    self.can_access_caverns_glitched(state) and self.has_both_kongs(state)) or (
                    self.can_access_valley_glitched(state) and self.has_both_kongs(state) and self.has_expresso(state))
                )
            )
    
    def can_access_industries_glitched(self, state: CollectionState) -> bool:
        return self.can_access_industries(state) or (
                self.can_access_valley_glitched(state) and self.has_both_kongs(state) and self.can_carry(state) and self.has_expresso(state)
            )

    def can_access_caverns_glitched(self, state: CollectionState) -> bool:
        return self.can_access_caverns(state) or (
                self.can_access_valley_glitched(state) and self.has_both_kongs(state) and self.can_carry(state) and self.has_expresso(state)
            )

    def can_access_very_gnawty(self, state: CollectionState) -> bool:
        return state.has(EventName.jungle_level, self.player, self.world.options.required_jungle_levels.value)
    
    def can_access_master_necky(self, state: CollectionState) -> bool:
        return state.has(EventName.mines_level, self.player, self.world.options.required_mines_levels.value)
    
    def can_access_queen_b(self, state: CollectionState) -> bool:
        return state.has(EventName.valley_level, self.player, self.world.options.required_valley_levels.value)
    
    def can_access_really_gnawty(self, state: CollectionState) -> bool:
        return state.has(EventName.glacier_level, self.player, self.world.options.required_glacier_levels.value)
    
    def can_access_dumb_drum(self, state: CollectionState) -> bool:
        return state.has(EventName.industries_level, self.player, self.world.options.required_industries_levels.value)
    
    def can_access_master_necky_snr(self, state: CollectionState) -> bool:
        return state.has(EventName.caverns_level, self.player, self.world.options.required_caverns_levels.value)

    def has_donkey(self, state: CollectionState) -> bool:
        return state.has(ItemName.donkey, self.player)

    def has_diddy(self, state: CollectionState) -> bool:
        return state.has(ItemName.diddy, self.player)
    
    def has_both_kongs(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.donkey, ItemName.diddy}, self.player)
    
    def can_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.carry, self.player)
    
    def can_swim(self, state: CollectionState) -> bool:
        return state.has(ItemName.swim, self.player)
    
    def can_roll(self, state: CollectionState) -> bool:
        return state.has(ItemName.roll, self.player)
    
    def can_climb(self, state: CollectionState) -> bool:
        return state.has(ItemName.climb, self.player)
    
    def can_slap(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.donkey, ItemName.slap}, self.player)
    
    def has_kannons(self, state: CollectionState) -> bool:
        return state.has(ItemName.kannons, self.player)
    
    def has_switches(self, state: CollectionState) -> bool:
        return state.has(ItemName.switches, self.player)
    
    def has_minecart(self, state: CollectionState) -> bool:
        return state.has(ItemName.minecart, self.player)
    
    def has_winky(self, state: CollectionState) -> bool:
        return state.has(ItemName.winky, self.player)
    
    def has_expresso(self, state: CollectionState) -> bool:
        return state.has(ItemName.expresso, self.player)
    
    def has_rambi(self, state: CollectionState) -> bool:
        return state.has(ItemName.rambi, self.player)
    
    def has_enguarde(self, state: CollectionState) -> bool:
        return state.has(ItemName.enguarde, self.player)
    
    def has_squawks(self, state: CollectionState) -> bool:
        return state.has(ItemName.squawks, self.player)
    
    def has_tires(self, state: CollectionState) -> bool:
        return state.has(ItemName.tires, self.player)
    
    def has_platforms(self, state: CollectionState) -> bool:
        return state.has(ItemName.platforms, self.player)
    
    def true(self, state: CollectionState) -> bool:
        return True
    
    def set_dkc_rules(self) -> None:
        multiworld = self.world.multiworld

        if self.world.options.glitched_world_access:
            self.connection_rules.update(
                {
                    f"{RegionName.dk_isle} -> {RegionName.kongo_jungle}":
                        self.can_access_jungle_glitched,
                    f"{RegionName.dk_isle} -> {RegionName.monkey_mines}":
                        self.can_access_mines_glitched,
                    f"{RegionName.dk_isle} -> {RegionName.vine_valley}":
                        self.can_access_valley_glitched,
                    f"{RegionName.dk_isle} -> {RegionName.gorilla_glacier}":
                        self.can_access_glacier_glitched,
                    f"{RegionName.dk_isle} -> {RegionName.kremkroc_industries}":
                        self.can_access_industries_glitched,
                    f"{RegionName.dk_isle} -> {RegionName.chimp_caverns}":
                        self.can_access_caverns_glitched,
                }
            )

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
            
        multiworld.completion_condition[self.player] = lambda state: state.has(EventName.k_rool, self.player)
        
    # Universal Tracker: Append the next logic level rule that has UT's glitched item to the actual logic rule
    def set_dkc_glitched_rules(self) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                glitched_rule = lambda state, rule=self.location_rules[loc.name]: state.has(ItemName.glitched, self.player) and rule(state)
                add_rule(loc, glitched_rule, combine="or")
 

class DKCStrictRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_bonus_2:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.has_tires,
            LocationName.jungle_hijinxs_bunch_1:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_2:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_3:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_4:
                self.can_roll,
            LocationName.jungle_hijinxs_bunch_5:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_6:
                lambda state: self.can_slap(state) and self.can_roll(state),
            LocationName.jungle_hijinxs_balloon_2:
                self.can_roll,
            LocationName.jungle_hijinxs_bunch_7:
                lambda state: self.can_slap(state) and self.can_roll(state),
            LocationName.jungle_hijinxs_bunch_8:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_9:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_10:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_11:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                lambda state: self.can_roll(state) and self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_13:
                lambda state: self.can_roll(state) and self.can_slap(state) and self.has_diddy(state),
            LocationName.jungle_hijinxs_balloon_4:
                lambda state: self.can_roll(state) and self.has_diddy(state),
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_15:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_18:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                lambda state: self.has_rambi(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.jungle_hijinxs_balloon_6:
                lambda state: self.has_rambi(state) and self.has_tires(state) and self.has_kannons(state),

            LocationName.ropey_rampage_clear:
                self.can_climb,
            EventName.ropey_rampage_clear:
                self.can_climb,
            LocationName.ropey_rampage_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_bonus_2:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_kong:
                lambda state: self.can_climb(state),
            LocationName.ropey_rampage_bunch_1:
                self.can_roll,
            LocationName.ropey_rampage_bunch_2:
                self.can_roll,
            LocationName.ropey_rampage_bunch_3:
                self.can_roll,
            LocationName.ropey_rampage_bunch_4:
                self.can_slap,
            LocationName.ropey_rampage_bunch_5:
                self.can_slap,
            LocationName.ropey_rampage_bunch_6:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_7:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_8:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_9:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_token_1:
                self.can_climb,
            LocationName.ropey_rampage_bunch_10:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_11:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_12:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_13:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_14:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_15:
                lambda state: self.can_slap(state) and self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_token_2:
                lambda state: self.has_tires(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_16:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_17:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_18:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_19:
                lambda state: self.can_slap(state) and self.can_climb(state),

            LocationName.reptile_rumble_clear:
                self.has_tires,
            EventName.reptile_rumble_clear:
                self.has_tires,
            LocationName.reptile_rumble_bonus_1:
                self.can_carry,
            LocationName.reptile_rumble_bonus_2:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            LocationName.reptile_rumble_bonus_3:
                lambda state: self.can_carry(state) and self.has_tires(state),
            LocationName.reptile_rumble_kong:
                self.has_tires,
            LocationName.reptile_rumble_bunch_1:
                self.can_slap,
            LocationName.reptile_rumble_bunch_2:
                self.can_slap,
            LocationName.reptile_rumble_bunch_3:
                self.can_slap,
            LocationName.reptile_rumble_bunch_4:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_6:
                self.has_tires,
            LocationName.reptile_rumble_bunch_7:
                self.has_tires,
            LocationName.reptile_rumble_bunch_8:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state) and self.can_carry(state),
            LocationName.reptile_rumble_bunch_10:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_token_1:
                self.has_tires,
            LocationName.reptile_rumble_bunch_11:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_12:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_13:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_14:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.coral_capers_clear:
                self.can_swim,
            EventName.coral_capers_clear:
                self.can_swim,
            LocationName.coral_capers_kong:
                self.can_swim,
            LocationName.coral_capers_bunch_1:
                self.can_swim,
            LocationName.coral_capers_balloon_1:
                self.can_swim,
            LocationName.coral_capers_bunch_2:
                self.can_swim,
            LocationName.coral_capers_token_1:
                self.can_swim,

            LocationName.barrel_cannon_canyon_clear:
                self.has_kannons,
            EventName.barrel_cannon_canyon_clear:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_kong:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_token_1:
                lambda state: self.has_diddy(state) and self.can_roll(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_1:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_2:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_3:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_4:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_token_2:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_6:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_7:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_8:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_9:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_10:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_11:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_12:
                lambda state: self.can_slap(state) and self.has_kannons(state),

            LocationName.very_gnawty_lair_clear:
                self.has_both_kongs,
            LocationName.defeated_gnawty_1:
                self.has_both_kongs,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.has_kannons,
            LocationName.winky_walkway_kong:
                lambda state: self.has_kannons(state) and self.has_winky(state),
            LocationName.winky_walkway_bunch_1:
                self.can_slap,
            LocationName.winky_walkway_bunch_2:
                self.can_slap,
            LocationName.winky_walkway_bunch_3:
                self.can_slap,
            LocationName.winky_walkway_bunch_4:
                self.can_slap,
            LocationName.winky_walkway_token_1:
                self.has_winky,
            LocationName.winky_walkway_bunch_5:
                self.can_slap,

            LocationName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            EventName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_kong:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_1:
                self.can_slap,
            LocationName.mine_cart_carnage_bunch_2:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_token_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_3:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_balloon_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),

            LocationName.bouncy_bonanza_clear:
                self.has_tires,
            EventName.bouncy_bonanza_clear:
                self.has_tires,
            LocationName.bouncy_bonanza_bonus_1:
                self.can_carry,
            LocationName.bouncy_bonanza_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.bouncy_bonanza_kong:
                self.has_tires,
            LocationName.bouncy_bonanza_token_1:
                self.has_tires,
            LocationName.bouncy_bonanza_bunch_1:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_2:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_3:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_4:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_7:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_8:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_10:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.stop_go_station_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            EventName.stop_go_station_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            LocationName.stop_go_station_bonus_1:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_carry(state),
            LocationName.stop_go_station_bonus_2:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.stop_go_station_kong:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_roll(state),
            LocationName.stop_go_station_bunch_1:
                self.can_slap,
            LocationName.stop_go_station_bunch_2:
                lambda state: self.has_switches(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_3:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_token_1:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_roll(state),
            LocationName.stop_go_station_bunch_4:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_5:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_6:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_7:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),

            LocationName.millstone_mayhem_clear:
                lambda state: self.has_tires(state) and (self.can_roll(state) or self.has_winky(state)),
            EventName.millstone_mayhem_clear:
                lambda state: self.has_tires(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bonus_1:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bonus_3:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.millstone_mayhem_kong:
                lambda state: self.has_tires(state) and self.has_kannons(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_1:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_2:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_3:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_4:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_7:
                lambda state: self.has_tires(state) and self.can_slap(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_8:
                lambda state: self.has_tires(state) and self.can_slap(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state) and (self.can_roll(state) or self.has_winky(state)),

            LocationName.necky_nuts_clear:
                lambda state: self.has_both_kongs(state) and self.has_tires(state),
            LocationName.defeated_necky_1:
                lambda state: self.has_both_kongs(state) and self.has_tires(state),

            LocationName.vulture_culture_clear:
                self.has_kannons,
            EventName.vulture_culture_clear:
                self.has_kannons,
            LocationName.vulture_culture_bonus_1:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            LocationName.vulture_culture_bonus_2:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_bonus_3:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_kong:
                lambda state: self.has_kannons(state) and self.has_tires(state) and self.can_carry(state),
            LocationName.vulture_culture_bunch_1:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_4:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_5:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_6:
                lambda state: self.has_kannons(state) and self.can_slap(state),

            LocationName.tree_top_town_clear:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            EventName.tree_top_town_clear:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            LocationName.tree_top_town_bonus_1:
                self.has_kannons,
            LocationName.tree_top_town_bonus_2:
                self.has_kannons,
            LocationName.tree_top_town_kong:
                self.has_kannons,
            LocationName.tree_top_town_bunch_1:
                self.can_slap,
            LocationName.tree_top_town_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.tree_top_town_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.tree_top_town_bunch_4:
                lambda state: self.has_kannons(state) and self.can_slap(state) and self.has_tires(state),
            LocationName.tree_top_town_token_1:
                lambda state: self.has_kannons(state) and self.can_roll(state) and self.has_tires(state),

            LocationName.forest_frenzy_clear:
                self.can_climb,
            EventName.forest_frenzy_clear:
                self.can_climb,
            LocationName.forest_frenzy_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.forest_frenzy_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.forest_frenzy_kong:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.forest_frenzy_bunch_1:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_3:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_4:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_5:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_balloon_1:
                self.can_climb,

            LocationName.temple_tempest_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            EventName.temple_tempest_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.temple_tempest_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.temple_tempest_bonus_2:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.temple_tempest_kong:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.temple_tempest_token_1:
                self.has_diddy,
            LocationName.temple_tempest_bunch_1:
                self.can_slap,
            LocationName.temple_tempest_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_3:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_4:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_5:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_6:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_7:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.temple_tempest_bunch_8:
                lambda state: self.can_climb(state) and self.has_tires(state),

            LocationName.orang_utan_gang_clear:
                lambda state: self.can_carry(state) or self.has_expresso(state) or self.can_roll(state) or self.has_both_kongs(state),
            EventName.orang_utan_gang_clear:
                lambda state: self.can_carry(state) or self.has_expresso(state) or self.can_roll(state) or self.has_both_kongs(state),
            LocationName.orang_utan_gang_bonus_1:
                self.has_expresso,
            LocationName.orang_utan_gang_bonus_2:
                lambda state: self.can_carry(state) and self.has_expresso(state),
            LocationName.orang_utan_gang_bonus_3:
                self.can_carry,
            LocationName.orang_utan_gang_bonus_4:
                self.can_carry,
            LocationName.orang_utan_gang_bonus_5:
                self.can_carry,
            LocationName.orang_utan_gang_kong:
                lambda state: self.can_carry(state) and self.can_roll(state) and self.has_tires(state),
            LocationName.orang_utan_gang_bunch_1:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_2:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_3:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_4:
                self.can_roll,
            LocationName.orang_utan_gang_bunch_5:
                lambda state: self.can_slap(state) and (self.can_carry(state) or self.has_expresso(state) or self.can_roll(state) or self.has_diddy(state)),
            LocationName.orang_utan_gang_bunch_6:
                self.has_expresso,
            LocationName.orang_utan_gang_token_1:
                lambda state: self.has_tires(state) and self.has_expresso(state),
            LocationName.orang_utan_gang_bunch_7:
                lambda state: self.can_slap(state) and (self.can_carry(state) or self.has_expresso(state) or self.can_roll(state) or self.has_diddy(state)),
            LocationName.orang_utan_gang_bunch_8:
                self.has_expresso,
            LocationName.orang_utan_gang_bunch_9:
                self.has_expresso,

            LocationName.clam_city_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            EventName.clam_city_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.clam_city_kong:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.clam_city_bunch_1:
                self.can_swim,
            LocationName.clam_city_bunch_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.clam_city_token_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.bumble_b_rumble_clear:
                lambda state: self.has_both_kongs(state) and self.can_carry(state),
            LocationName.defeated_bumble_b:
                lambda state: self.has_both_kongs(state) and self.can_carry(state),

            LocationName.snow_barrel_blast_clear:
                self.has_kannons,
            EventName.snow_barrel_blast_clear:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_3:
                self.has_kannons,
            LocationName.snow_barrel_blast_kong:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_1:
                self.can_slap,
            LocationName.snow_barrel_blast_balloon_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.snow_barrel_blast_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.snow_barrel_blast_token_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_balloon_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_4:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_5:
                lambda state: self.has_kannons(state) and self.can_slap(state),

            LocationName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            EventName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.slipslide_ride_bunch_1:
                self.can_climb,
            LocationName.slipslide_ride_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.slipslide_ride_bunch_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_4:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_5:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_6:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.slipslide_ride_bunch_7:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_carry(state),
            LocationName.slipslide_ride_bunch_8:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_slap(state),
            LocationName.slipslide_ride_bunch_9:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_slap(state),
            LocationName.slipslide_ride_token_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),

            LocationName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            EventName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            LocationName.ice_age_alley_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ice_age_alley_bonus_2:
                lambda state: self.has_expresso(state) and self.has_kannons(state),
            LocationName.ice_age_alley_kong:
                lambda state: self.can_roll(state) and self.has_expresso(state),
            LocationName.ice_age_alley_bunch_1:
                self.can_slap,
            LocationName.ice_age_alley_bunch_2:
                lambda state: ((self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state)) and self.can_slap(state),
            LocationName.ice_age_alley_bunch_3:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),

            LocationName.croctopus_chase_clear:
                self.can_swim,
            EventName.croctopus_chase_clear:
                self.can_swim,
            LocationName.croctopus_chase_kong:
                self.can_swim,
            LocationName.croctopus_chase_bunch_1:
                self.can_swim,
            LocationName.croctopus_chase_token_1:
                self.can_swim,
            LocationName.croctopus_chase_token_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_3:
                self.can_swim,
            LocationName.croctopus_chase_bunch_4:
                self.can_swim,
            LocationName.croctopus_chase_bunch_5:
                self.can_swim,
            LocationName.croctopus_chase_balloon_1:
                self.can_swim,

            LocationName.torchlight_trouble_clear:
                lambda state: self.has_donkey(state) and self.has_squawks(state),
            EventName.torchlight_trouble_clear:
                lambda state: self.has_donkey(state) and self.has_squawks(state),
            LocationName.torchlight_trouble_bonus_1:
                lambda state: self.has_donkey(state) and self.has_squawks(state) and self.can_carry(state),
            LocationName.torchlight_trouble_bonus_2:
                lambda state: self.has_donkey(state) and self.has_squawks(state) and self.can_carry(state),
            LocationName.torchlight_trouble_kong:
                lambda state: self.has_donkey(state) and self.has_squawks(state) and self.can_carry(state) and self.can_roll(state) and self.has_tires(state),
            LocationName.torchlight_trouble_bunch_1:
                lambda state: self.has_donkey(state) and self.has_squawks(state) and self.can_slap(state),

            LocationName.rope_bridge_rumble_clear:
                self.has_tires,
            EventName.rope_bridge_rumble_clear:
                self.has_tires,
            LocationName.rope_bridge_rumble_bonus_1:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.rope_bridge_rumble_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.rope_bridge_rumble_kong:
                lambda state: self.has_tires(state) and self.can_roll(state),
            LocationName.rope_bridge_rumble_bunch_1:
                lambda state: self.has_tires(state) and self.can_roll(state),

            LocationName.really_gnawty_rampage_clear:
                self.has_both_kongs,
            LocationName.defeated_gnawty_2:
                self.has_both_kongs,

            LocationName.oil_drum_alley_clear:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            EventName.oil_drum_alley_clear:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bonus_2:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.oil_drum_alley_bonus_3:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.oil_drum_alley_bonus_4:
                lambda state: self.has_tires(state) and (self.can_carry(state) or self.has_rambi(state)) and self.has_kannons(state),
            LocationName.oil_drum_alley_kong:
                lambda state: self.has_tires(state) and self.can_roll(state) and self.has_kannons(state) and (self.can_carry(state) and self.has_rambi(state)),
            LocationName.oil_drum_alley_bunch_1:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bunch_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),

            LocationName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            EventName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state) and self.can_roll(state),
            LocationName.trick_track_trek_bonus_2:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.trick_track_trek_bonus_3:
                lambda state: self.has_platforms(state) and self.has_kannons(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_kong:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_bunch_1:
                self.has_platforms,
            LocationName.trick_track_trek_token_1:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),

            LocationName.elevator_antics_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            EventName.elevator_antics_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.elevator_antics_bonus_1:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.elevator_antics_bonus_2:
                self.can_climb,
            LocationName.elevator_antics_bonus_3:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.elevator_antics_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.can_climb,
            LocationName.elevator_antics_bunch_3:
                self.can_climb,

            LocationName.poison_pond_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            EventName.poison_pond_clear:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_kong:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_3:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_4:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_5:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_token_1:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_token_2:
                lambda state: self.can_swim(state) and self.has_enguarde(state),
            LocationName.poison_pond_bunch_6:
                lambda state: self.can_swim(state) and self.has_enguarde(state),

            LocationName.mine_cart_madness_clear:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            EventName.mine_cart_madness_clear:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            LocationName.mine_cart_madness_bonus_1:
                lambda state: self.has_minecart(state) and self.can_climb(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_2:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_3:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_kong:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            LocationName.mine_cart_madness_token_1:
                self.has_minecart,
            LocationName.mine_cart_madness_bunch_1:
                lambda state: self.has_minecart(state) and self.has_tires(state),

            LocationName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            EventName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            LocationName.blackout_basement_bonus_1:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_bonus_2:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.blackout_basement_kong:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_token_1:
                self.can_roll,
            LocationName.blackout_basement_bunch_1:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),

            LocationName.boss_dumb_drum_clear:
                self.has_both_kongs,
            LocationName.defeated_boss_dumb_drum:
                self.has_both_kongs,

            LocationName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            EventName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_kong:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_1:
                self.has_platforms,
            LocationName.tanked_up_trouble_bunch_2:
                self.has_platforms,
            LocationName.tanked_up_trouble_token_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_3:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_4:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),

            LocationName.manic_mincers_clear:
                lambda state: (self.has_both_kongs(state) or self.has_rambi(state)) and self.has_tires(state),
            EventName.manic_mincers_clear:
                lambda state: (self.has_both_kongs(state) or self.has_rambi(state)) and self.has_tires(state),
            LocationName.manic_mincers_bonus_1:
                lambda state: (self.has_both_kongs(state) and self.can_carry(state)) or self.has_rambi(state),
            LocationName.manic_mincers_bonus_2:
                lambda state: (self.has_both_kongs(state) and self.can_carry(state)) or self.has_rambi(state),
            LocationName.manic_mincers_kong:
                lambda state: self.has_both_kongs(state) or self.has_rambi(state),
            LocationName.manic_mincers_bunch_1:
                lambda state: self.has_both_kongs(state) or self.has_rambi(state),
            LocationName.manic_mincers_bunch_2:
                lambda state: self.has_both_kongs(state) or self.has_rambi(state),
            LocationName.manic_mincers_token_1:
                lambda state: self.has_both_kongs(state) or self.has_rambi(state),

            LocationName.misty_mine_clear:
                self.can_climb,
            EventName.misty_mine_clear:
                self.can_climb,
            LocationName.misty_mine_bonus_1:
                self.can_climb,
            LocationName.misty_mine_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.misty_mine_kong:
                self.can_climb,
            LocationName.misty_mine_token_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.misty_mine_bunch_1:
                self.can_carry,
            LocationName.misty_mine_bunch_2:
                self.can_climb,
            LocationName.misty_mine_token_2:
                lambda state: self.can_climb(state) and self.has_expresso(state),

            LocationName.loopy_lights_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            EventName.loopy_lights_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            LocationName.loopy_lights_bonus_1:
                lambda state: self.has_switches(state) and self.has_kannons(state),
            LocationName.loopy_lights_bonus_2:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_carry(state),
            LocationName.loopy_lights_kong:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.has_kannons(state) and self.can_roll(state) and self.can_carry(state),
            LocationName.loopy_lights_bunch_1:
                lambda state: self.has_switches(state) and self.has_tires(state),
            LocationName.loopy_lights_bunch_2:
                lambda state: self.has_switches(state) and self.has_tires(state),

            LocationName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            EventName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            LocationName.platform_perils_bonus_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.platform_perils_bonus_2:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state) and self.has_kannons(state),
            LocationName.platform_perils_kong:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            LocationName.platform_perils_token_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)),
            LocationName.platform_perils_bunch_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and self.has_tires(state),

            LocationName.necky_revenge_clear:
                lambda state: self.has_both_kongs(state) and self.has_tires(state),
            LocationName.defeated_necky_2:
                lambda state: self.has_both_kongs(state) and self.has_tires(state),
        }

class DKCLooseRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_bonus_2:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.has_tires,
            LocationName.jungle_hijinxs_bunch_1:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_2:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_3:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_4:
                lambda state: self.has_rambi(state) or self.can_roll(state),
            LocationName.jungle_hijinxs_bunch_5:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_6:
                self.can_slap,
            LocationName.jungle_hijinxs_balloon_2:
                self.can_roll,
            LocationName.jungle_hijinxs_bunch_7:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_8:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_9:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_10:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_11:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                lambda state: self.can_roll(state) and self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_13:
                lambda state: self.can_roll(state) and self.can_slap(state),
            LocationName.jungle_hijinxs_balloon_4:
                lambda state: self.can_roll(state) and self.has_diddy(state),
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_15:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_18:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                lambda state: self.has_rambi(state) and self.has_tires(state),
            LocationName.jungle_hijinxs_balloon_6:
                lambda state: self.has_rambi(state) and self.has_tires(state),

            LocationName.ropey_rampage_clear:
                self.can_climb,
            EventName.ropey_rampage_clear:
                self.can_climb,
            LocationName.ropey_rampage_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_bonus_2:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_kong:
                lambda state: self.can_climb(state),
            LocationName.ropey_rampage_bunch_1:
                self.true,
            LocationName.ropey_rampage_bunch_2:
                self.true,
            LocationName.ropey_rampage_bunch_3:
                self.true,
            LocationName.ropey_rampage_bunch_4:
                self.can_slap,
            LocationName.ropey_rampage_bunch_5:
                self.can_slap,
            LocationName.ropey_rampage_bunch_6:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_7:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_8:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_9:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_token_1:
                self.can_climb,
            LocationName.ropey_rampage_bunch_10:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_11:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_12:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_13:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_14:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_15:
                lambda state: self.can_slap(state) and self.can_climb(state) and (self.can_roll(state) or self.has_diddy(state)),
            LocationName.ropey_rampage_token_2:
                lambda state: self.has_tires(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_16:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_17:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_18:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_19:
                lambda state: self.can_slap(state) and self.can_climb(state),

            LocationName.reptile_rumble_clear:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            EventName.reptile_rumble_clear:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bonus_1:
                self.can_carry,
            LocationName.reptile_rumble_bonus_2:
                lambda state: self.has_kannons(state) and (self.has_tires(state) or self.has_diddy(state)),
            LocationName.reptile_rumble_bonus_3:
                lambda state: self.can_carry(state) and self.has_tires(state),
            LocationName.reptile_rumble_kong:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_1:
                self.can_slap,
            LocationName.reptile_rumble_bunch_2:
                self.can_slap,
            LocationName.reptile_rumble_bunch_3:
                self.can_slap,
            LocationName.reptile_rumble_bunch_4:
                lambda state: (self.has_tires(state) or self.has_diddy(state)) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_5:
                lambda state: (self.has_tires(state) or self.has_diddy(state)) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_6:
                self.has_tires,
            LocationName.reptile_rumble_bunch_7:
                self.has_tires,
            LocationName.reptile_rumble_bunch_8:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_10:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_token_1:
                self.has_tires,
            LocationName.reptile_rumble_bunch_11:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_12:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_13:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_14:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.coral_capers_clear:
                self.can_swim,
            EventName.coral_capers_clear:
                self.can_swim,
            LocationName.coral_capers_kong:
                self.can_swim,
            LocationName.coral_capers_bunch_1:
                self.can_swim,
            LocationName.coral_capers_balloon_1:
                self.can_swim,
            LocationName.coral_capers_bunch_2:
                self.can_swim,
            LocationName.coral_capers_token_1:
                self.can_swim,

            LocationName.barrel_cannon_canyon_clear:
                self.has_kannons,
            EventName.barrel_cannon_canyon_clear:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_kong:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_token_1:
                lambda state: self.can_roll(state) and (self.has_diddy(state) or (self.has_kannons(state) and self.has_donkey(state))),
            LocationName.barrel_cannon_canyon_bunch_1:
                lambda state: self.can_slap(state) and (self.has_kannons(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_2:
                lambda state: self.can_slap(state) and (self.has_kannons(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.barrel_cannon_canyon_bunch_3:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_4:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_token_2:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_6:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_7:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_8:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_9:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_10:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_11:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_12:
                lambda state: self.can_slap(state) and self.has_kannons(state),

            LocationName.very_gnawty_lair_clear:
                self.true,
            LocationName.defeated_gnawty_1:
                self.true,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.has_kannons,
            LocationName.winky_walkway_kong:
                self.has_kannons,
            LocationName.winky_walkway_bunch_1:
                self.can_slap,
            LocationName.winky_walkway_bunch_2:
                self.can_slap,
            LocationName.winky_walkway_bunch_3:
                self.can_slap,
            LocationName.winky_walkway_bunch_4:
                self.can_slap,
            LocationName.winky_walkway_token_1:
                self.has_winky,
            LocationName.winky_walkway_bunch_5:
                self.can_slap,

            LocationName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            EventName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_kong:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_1:
                self.can_slap,
            LocationName.mine_cart_carnage_bunch_2:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_token_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_3:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_balloon_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),

            LocationName.bouncy_bonanza_clear:
                self.has_tires,
            EventName.bouncy_bonanza_clear:
                self.has_tires,
            LocationName.bouncy_bonanza_bonus_1:
                self.can_carry,
            LocationName.bouncy_bonanza_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.bouncy_bonanza_kong:
                self.has_tires,
            LocationName.bouncy_bonanza_token_1:
                self.has_tires,
            LocationName.bouncy_bonanza_bunch_1:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_2:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_3:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_4:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_7:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_8:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_10:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.stop_go_station_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            EventName.stop_go_station_clear:
                lambda state: self.has_switches(state) and self.has_tires(state),
            LocationName.stop_go_station_bonus_1:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_carry(state),
            LocationName.stop_go_station_bonus_2:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.stop_go_station_kong:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_roll(state),
            LocationName.stop_go_station_bunch_1:
                self.can_slap,
            LocationName.stop_go_station_bunch_2:
                lambda state: self.has_switches(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_3:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_token_1:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_roll(state),
            LocationName.stop_go_station_bunch_4:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_5:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_6:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.stop_go_station_bunch_7:
                lambda state: self.has_switches(state) and self.has_tires(state) and self.can_slap(state),

            LocationName.millstone_mayhem_clear:
                self.has_tires,
            EventName.millstone_mayhem_clear:
                self.has_tires,
            LocationName.millstone_mayhem_bonus_1:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bonus_3:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.millstone_mayhem_kong:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bunch_1:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_2:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_3:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_4:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.millstone_mayhem_bunch_7:
                lambda state: self.has_tires(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_8:
                lambda state: self.has_tires(state) and (self.can_roll(state) or self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_9:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.necky_nuts_clear:
                self.has_tires,
            LocationName.defeated_necky_1:
                self.has_tires,

            LocationName.vulture_culture_clear:
                self.has_kannons,
            EventName.vulture_culture_clear:
                self.has_kannons,
            LocationName.vulture_culture_bonus_1:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            LocationName.vulture_culture_bonus_2:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_bonus_3:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_kong:
                lambda state: self.has_kannons(state) and self.has_tires(state) and self.can_carry(state),
            LocationName.vulture_culture_bunch_1:
                lambda state: (self.has_kannons(state) or self.has_diddy(state)) and self.can_slap(state),
            LocationName.vulture_culture_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_4:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_5:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_6:
                lambda state: self.has_kannons(state) and self.can_slap(state),

            LocationName.tree_top_town_clear:
                lambda state: self.has_kannons(state) and self.has_diddy(state),
            EventName.tree_top_town_clear:
                lambda state: self.has_kannons(state) and self.has_diddy(state),
            LocationName.tree_top_town_bonus_1:
                self.has_kannons,
            LocationName.tree_top_town_bonus_2:
                self.has_kannons,
            LocationName.tree_top_town_kong:
                self.has_kannons,
            LocationName.tree_top_town_bunch_1:
                self.can_slap,
            LocationName.tree_top_town_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.tree_top_town_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.tree_top_town_bunch_4:
                lambda state: self.has_kannons(state) and self.can_slap(state) and self.has_tires(state),
            LocationName.tree_top_town_token_1:
                lambda state: self.has_kannons(state) and self.can_roll(state) and self.has_tires(state),

            LocationName.forest_frenzy_clear:
                self.can_climb,
            EventName.forest_frenzy_clear:
                self.can_climb,
            LocationName.forest_frenzy_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.forest_frenzy_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.forest_frenzy_kong:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.forest_frenzy_bunch_1:
                lambda state: (self.can_climb(state) or (self.has_diddy(state) and self.can_roll(state))) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_3:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_4:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_bunch_5:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_balloon_1:
                self.can_climb,

            LocationName.temple_tempest_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            EventName.temple_tempest_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.temple_tempest_bonus_1:
                lambda state: (self.can_climb(state) or (self.has_diddy(state) and self.can_roll(state))) and self.can_carry(state),
            LocationName.temple_tempest_bonus_2:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.temple_tempest_kong:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.temple_tempest_token_1:
                self.true,
            LocationName.temple_tempest_bunch_1:
                self.can_slap,
            LocationName.temple_tempest_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_3:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_4:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_5:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_6:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.can_slap(state),
            LocationName.temple_tempest_bunch_7:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.temple_tempest_bunch_8:
                lambda state: self.can_climb(state) and self.has_tires(state),

            LocationName.orang_utan_gang_clear:
                self.true,
            EventName.orang_utan_gang_clear:
                self.true,
            LocationName.orang_utan_gang_bonus_1:
                self.has_expresso,
            LocationName.orang_utan_gang_bonus_2:
                lambda state: self.can_carry(state) and (self.has_expresso(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.orang_utan_gang_bonus_3:
                self.can_carry,
            LocationName.orang_utan_gang_bonus_4:
                self.can_carry,
            LocationName.orang_utan_gang_bonus_5:
                self.true,
            LocationName.orang_utan_gang_kong:
                lambda state: self.can_carry(state) and self.can_roll(state) and self.has_tires(state),
            LocationName.orang_utan_gang_bunch_1:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_2:
                lambda state: self.can_carry(state) or self.can_slap(state),
            LocationName.orang_utan_gang_bunch_3:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_4:
                self.can_roll,
            LocationName.orang_utan_gang_bunch_5:
                lambda state: self.can_slap(state) and (self.can_carry(state) or self.has_expresso(state)),
            LocationName.orang_utan_gang_bunch_6:
                lambda state: self.has_expresso(state) or (self.has_diddy(state) and self.can_roll(state)),
            LocationName.orang_utan_gang_token_1:
                lambda state: self.has_tires(state) and self.has_expresso(state),
            LocationName.orang_utan_gang_bunch_7:
                lambda state: self.can_slap(state) and (self.can_carry(state) or self.has_expresso(state)),
            LocationName.orang_utan_gang_bunch_8:
                self.true,
            LocationName.orang_utan_gang_bunch_9:
                self.true,

            LocationName.clam_city_clear:
                self.can_swim,
            EventName.clam_city_clear:
                self.can_swim,
            LocationName.clam_city_kong:
                self.can_swim,
            LocationName.clam_city_bunch_1:
                self.can_swim,
            LocationName.clam_city_bunch_2:
                self.can_swim,
            LocationName.clam_city_token_1:
                self.can_swim,

            LocationName.bumble_b_rumble_clear:
                self.can_carry,
            LocationName.defeated_bumble_b:
                self.can_carry,

            LocationName.snow_barrel_blast_clear:
                self.has_kannons,
            EventName.snow_barrel_blast_clear:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_3:
                self.has_kannons,
            LocationName.snow_barrel_blast_kong:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_1:
                lambda state: self.has_kannons(state) or self.can_slap(state),
            LocationName.snow_barrel_blast_balloon_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.snow_barrel_blast_bunch_3:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.snow_barrel_blast_token_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_balloon_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_4:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_5:
                lambda state: self.has_kannons(state) and self.can_slap(state),

            LocationName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            EventName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_1:
                self.can_climb,
            LocationName.slipslide_ride_bunch_2:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.slipslide_ride_bunch_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_4:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_5:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_6:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_7:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_8:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_slap(state),
            LocationName.slipslide_ride_bunch_9:
                lambda state: self.can_climb(state) and self.has_kannons(state) and self.can_slap(state),
            LocationName.slipslide_ride_token_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),

            LocationName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            EventName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            LocationName.ice_age_alley_bonus_1:
                lambda state: (self.can_climb(state) or self.has_expresso(state)) and self.has_kannons(state),
            LocationName.ice_age_alley_bonus_2:
                lambda state: self.has_expresso(state) and self.has_kannons(state),
            LocationName.ice_age_alley_kong:
                lambda state: self.can_roll(state) and self.has_expresso(state),
            LocationName.ice_age_alley_bunch_1:
                self.can_slap,
            LocationName.ice_age_alley_bunch_2:
                lambda state: ((self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state)) and self.can_slap(state),
            LocationName.ice_age_alley_bunch_3:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),

            LocationName.croctopus_chase_clear:
                self.can_swim,
            EventName.croctopus_chase_clear:
                self.can_swim,
            LocationName.croctopus_chase_kong:
                self.can_swim,
            LocationName.croctopus_chase_bunch_1:
                self.can_swim,
            LocationName.croctopus_chase_token_1:
                self.can_swim,
            LocationName.croctopus_chase_token_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_3:
                self.can_swim,
            LocationName.croctopus_chase_bunch_4:
                self.can_swim,
            LocationName.croctopus_chase_bunch_5:
                self.can_swim,
            LocationName.croctopus_chase_balloon_1:
                self.can_swim,

            LocationName.torchlight_trouble_clear:
                self.true,
            EventName.torchlight_trouble_clear:
                self.true,
            LocationName.torchlight_trouble_bonus_1:
                self.can_carry,
            LocationName.torchlight_trouble_bonus_2:
                self.can_carry,
            LocationName.torchlight_trouble_kong:
                lambda state: self.can_carry(state) and self.can_roll(state),
            LocationName.torchlight_trouble_bunch_1:
                self.can_slap,

            LocationName.rope_bridge_rumble_clear:
                self.has_tires,
            EventName.rope_bridge_rumble_clear:
                self.has_tires,
            LocationName.rope_bridge_rumble_bonus_1:
                self.has_kannons,
            LocationName.rope_bridge_rumble_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.rope_bridge_rumble_kong:
                lambda state: self.has_tires(state) and self.can_roll(state),
            LocationName.rope_bridge_rumble_bunch_1:
                lambda state: self.has_tires(state) and self.can_roll(state),

            LocationName.really_gnawty_rampage_clear:
                self.true,
            LocationName.defeated_gnawty_2:
                self.true,

            LocationName.oil_drum_alley_clear:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            EventName.oil_drum_alley_clear:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bonus_2:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.oil_drum_alley_bonus_3:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.oil_drum_alley_bonus_4:
                lambda state: (
                              (
                              (self.has_tires(state) and self.has_rambi(state)) or
                              (self.has_tires(state) and self.can_carry(state)) or
                              (self.can_roll(state) and self.can_carry(state))
                              )
                              and self.has_kannons(state)),
            LocationName.oil_drum_alley_kong:
                lambda state: self.has_tires(state) and self.can_roll(state) and self.has_kannons(state) and (self.can_carry(state) or self.has_rambi(state)),
            LocationName.oil_drum_alley_bunch_1:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bunch_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),

            LocationName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            EventName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state) and self.can_roll(state),
            LocationName.trick_track_trek_bonus_2:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.trick_track_trek_bonus_3:
                lambda state: self.has_platforms(state) and self.has_kannons(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_kong:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.trick_track_trek_bunch_1:
                self.has_platforms,
            LocationName.trick_track_trek_token_1:
                lambda state: self.has_platforms(state) and (self.has_donkey(state) or (self.has_diddy(state) and self.can_roll(state))),

            LocationName.elevator_antics_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            EventName.elevator_antics_clear:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.elevator_antics_bonus_1:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.elevator_antics_bonus_2:
                self.can_climb,
            LocationName.elevator_antics_bonus_3:
                lambda state: self.can_climb(state) and self.has_tires(state),
            LocationName.elevator_antics_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.can_climb,
            LocationName.elevator_antics_bunch_3:
                self.can_climb,

            LocationName.poison_pond_clear:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            EventName.poison_pond_clear:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_kong:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_1:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_2:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_3:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_4:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_5:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_token_1:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_token_2:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_6:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),

            LocationName.mine_cart_madness_clear:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            EventName.mine_cart_madness_clear:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            LocationName.mine_cart_madness_bonus_1:
                lambda state: self.has_minecart(state) and self.can_climb(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_2:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_3:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_kong:
                lambda state: self.has_minecart(state) and self.has_tires(state),
            LocationName.mine_cart_madness_token_1:
                self.has_minecart,
            LocationName.mine_cart_madness_bunch_1:
                lambda state: self.has_minecart(state) and self.has_tires(state),

            LocationName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            EventName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            LocationName.blackout_basement_bonus_1:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_bonus_2:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.blackout_basement_kong:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_token_1:
                self.can_roll,
            LocationName.blackout_basement_bunch_1:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),

            LocationName.boss_dumb_drum_clear:
                lambda state: (self.has_diddy(state) and self.can_roll(state)) or self.has_donkey(state),
            LocationName.defeated_boss_dumb_drum:
                lambda state: (self.has_diddy(state) and self.can_roll(state)) or self.has_donkey(state),

            LocationName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            EventName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_kong:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_1:
                self.has_platforms,
            LocationName.tanked_up_trouble_bunch_2:
                self.has_platforms,
            LocationName.tanked_up_trouble_token_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_3:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_bunch_4:
                lambda state: self.has_platforms(state) and self.has_tires(state) and self.has_kannons(state),

            LocationName.manic_mincers_clear:
                self.has_tires,
            EventName.manic_mincers_clear:
                self.has_tires,
            LocationName.manic_mincers_bonus_1:
                lambda state: (self.has_both_kongs(state) and self.can_carry(state)) or self.has_rambi(state),
            LocationName.manic_mincers_bonus_2:
                lambda state: (self.has_both_kongs(state) and self.can_carry(state)) or self.has_rambi(state),
            LocationName.manic_mincers_kong:
                self.true,
            LocationName.manic_mincers_bunch_1:
                self.true,
            LocationName.manic_mincers_bunch_2:
                self.true,
            LocationName.manic_mincers_token_1:
                self.true,

            LocationName.misty_mine_clear:
                self.can_climb,
            EventName.misty_mine_clear:
                self.can_climb,
            LocationName.misty_mine_bonus_1:
                self.can_climb,
            LocationName.misty_mine_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.misty_mine_kong:
                self.can_climb,
            LocationName.misty_mine_token_1:
                self.can_carry,
            LocationName.misty_mine_bunch_1:
                self.can_carry,
            LocationName.misty_mine_bunch_2:
                self.can_climb,
            LocationName.misty_mine_token_2:
                lambda state: self.can_climb(state) and (self.has_expresso(state) or self.can_roll(state)),

            LocationName.loopy_lights_clear:
                self.has_tires,
            EventName.loopy_lights_clear:
                self.has_tires,
            LocationName.loopy_lights_bonus_1:
                self.has_kannons,
            LocationName.loopy_lights_bonus_2:
                lambda state: self.has_tires(state) and self.can_carry(state),
            LocationName.loopy_lights_kong:
                lambda state: self.has_tires(state) and self.has_kannons(state) and self.can_roll(state) and self.can_carry(state),
            LocationName.loopy_lights_bunch_1:
                self.has_tires,
            LocationName.loopy_lights_bunch_2:
                self.has_tires,

            LocationName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            EventName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            LocationName.platform_perils_bonus_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.platform_perils_bonus_2:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state) and self.has_kannons(state),
            LocationName.platform_perils_kong:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)) and self.has_tires(state),
            LocationName.platform_perils_token_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and (self.has_donkey(state) or self.can_roll(state)),
            LocationName.platform_perils_bunch_1:
                lambda state: self.has_platforms(state) and self.can_carry(state) and self.has_tires(state),

            LocationName.necky_revenge_clear:
                self.has_tires,
            LocationName.defeated_necky_2:
                self.has_tires,
        }

    def set_dkc_rules(self) -> None:
        super().set_dkc_rules()


class DKCExpertRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

      
        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_bonus_2:
                lambda state: self.has_rambi(state) or self.can_carry(state),
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.has_tires,
            LocationName.jungle_hijinxs_bunch_1:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_2:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_3:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_4:
                self.true,
            LocationName.jungle_hijinxs_bunch_5:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_6:
                self.can_slap,
            LocationName.jungle_hijinxs_balloon_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_7:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_8:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_9:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_10:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_11:
                self.can_slap,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                lambda state: (self.can_roll(state) and self.has_diddy(state)) or self.has_rambi(state),
            LocationName.jungle_hijinxs_bunch_13:
                lambda state: self.can_roll(state) and self.can_slap(state),
            LocationName.jungle_hijinxs_balloon_4:
                lambda state: (self.can_roll(state) and self.has_diddy(state)) or self.has_rambi(state),
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_15:
                lambda state: self.has_rambi(state) or self.can_slap(state),
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_18:
                lambda state: self.has_rambi(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                lambda state: self.has_rambi(state) and self.has_tires(state),
            LocationName.jungle_hijinxs_balloon_6:
                lambda state: self.has_rambi(state) and self.has_tires(state),

            LocationName.ropey_rampage_clear:
                self.can_climb,
            EventName.ropey_rampage_clear:
                self.can_climb,
            LocationName.ropey_rampage_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_bonus_2:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.ropey_rampage_kong:
                lambda state: self.can_climb(state),
            LocationName.ropey_rampage_bunch_1:
                self.true,
            LocationName.ropey_rampage_bunch_2:
                self.true,
            LocationName.ropey_rampage_bunch_3:
                self.true,
            LocationName.ropey_rampage_bunch_4:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.ropey_rampage_bunch_5:
                self.can_slap,
            LocationName.ropey_rampage_bunch_6:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_7:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_8:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_9:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_token_1:
                lambda state: (self.can_climb(state) or self.has_both_kongs(state)) or (self.has_diddy(state) and self.can_roll(state)),
            LocationName.ropey_rampage_bunch_10:
                lambda state: (self.can_slap(state) and self.can_climb(state)) or self.has_both_kongs(state),
            LocationName.ropey_rampage_bunch_11:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_12:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_13:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.ropey_rampage_bunch_14:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.ropey_rampage_bunch_15:
                lambda state: self.can_slap(state) and self.can_climb(state) and (self.can_roll(state) or self.has_diddy(state)),
            LocationName.ropey_rampage_token_2:
                self.can_climb,
            LocationName.ropey_rampage_bunch_16:
                lambda state: self.can_slap(state) and self.can_climb(state),
            LocationName.ropey_rampage_bunch_17:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_18:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.ropey_rampage_bunch_19:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),

            LocationName.reptile_rumble_clear:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            EventName.reptile_rumble_clear:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bonus_1:
                self.can_carry,
            LocationName.reptile_rumble_bonus_2:
                self.has_kannons,
            LocationName.reptile_rumble_bonus_3:
                lambda state: self.can_carry(state) and self.has_tires(state),
            LocationName.reptile_rumble_kong:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_2:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_3:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_4:
                self.can_slap,
            LocationName.reptile_rumble_bunch_5:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_6:
                self.true,
            LocationName.reptile_rumble_bunch_7:
                self.true,
            LocationName.reptile_rumble_bunch_8:
                lambda state: (self.has_tires(state) or self.has_diddy(state)) and self.can_slap(state),
            LocationName.reptile_rumble_bunch_9:
                lambda state: self.can_slap(state) or (self.has_diddy(state) and self.can_roll(state)),
            LocationName.reptile_rumble_bunch_10:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.reptile_rumble_token_1:
                lambda state: self.has_tires(state) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_11:
                lambda state: (self.has_tires(state) and self.can_slap(state)) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_12:
                lambda state: (self.has_tires(state) and self.can_slap(state)) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_13:
                lambda state: (self.has_tires(state) and self.can_slap(state)) or self.has_diddy(state),
            LocationName.reptile_rumble_bunch_14:
                lambda state: self.has_tires(state) and self.can_slap(state),

            LocationName.coral_capers_clear:
                self.can_swim,
            EventName.coral_capers_clear:
                self.can_swim,
            LocationName.coral_capers_kong:
                self.can_swim,
            LocationName.coral_capers_bunch_1:
                self.can_swim,
            LocationName.coral_capers_balloon_1:
                self.can_swim,
            LocationName.coral_capers_bunch_2:
                self.can_swim,
            LocationName.coral_capers_token_1:
                self.can_swim,

            LocationName.barrel_cannon_canyon_clear:
                self.has_kannons,
            EventName.barrel_cannon_canyon_clear:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_kong:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_token_1:
                self.can_roll,
            LocationName.barrel_cannon_canyon_bunch_1:
                self.can_slap,
            LocationName.barrel_cannon_canyon_bunch_2:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.barrel_cannon_canyon_bunch_3:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_4:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_token_2:
                self.has_kannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_6:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_7:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_8:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.barrel_cannon_canyon_bunch_9:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_10:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_11:
                lambda state: self.can_slap(state) and self.has_kannons(state),
            LocationName.barrel_cannon_canyon_bunch_12:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),

            LocationName.very_gnawty_lair_clear:
                self.true,
            LocationName.defeated_gnawty_1:
                self.true,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.has_kannons,
            LocationName.winky_walkway_kong:
                self.has_kannons,
            LocationName.winky_walkway_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.winky_walkway_bunch_2:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.winky_walkway_bunch_3:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.winky_walkway_bunch_4:
                lambda state: self.can_slap(state) or (self.has_diddy(state) and self.has_winky(state)),
            LocationName.winky_walkway_token_1:
                lambda state: self.has_winky(state) or self.has_donkey(state) or self.has_both_kongs(state),
            LocationName.winky_walkway_bunch_5:
                lambda state: self.can_slap(state) or self.has_diddy(state),

            LocationName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            EventName.mine_cart_carnage_clear:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_kong:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_1:
                self.can_slap,
            LocationName.mine_cart_carnage_bunch_2:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_token_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_bunch_3:
                lambda state: self.has_kannons(state) and self.has_minecart(state),
            LocationName.mine_cart_carnage_balloon_1:
                lambda state: self.has_kannons(state) and self.has_minecart(state),

            LocationName.bouncy_bonanza_clear:
                self.has_tires,
            EventName.bouncy_bonanza_clear:
                self.has_tires,
            LocationName.bouncy_bonanza_bonus_1:
                self.can_carry,
            LocationName.bouncy_bonanza_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.bouncy_bonanza_kong:
                self.has_tires,
            LocationName.bouncy_bonanza_token_1:
                self.has_tires,
            LocationName.bouncy_bonanza_bunch_1:
                self.can_slap,
            LocationName.bouncy_bonanza_bunch_2:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.bouncy_bonanza_bunch_3:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.bouncy_bonanza_bunch_4:
                lambda state: (self.can_slap(state) and (
                    self.has_tires(state) or self.can_carry(state))) or (
                        self.has_diddy(state) and self.can_roll(state)
                    ) ,
            LocationName.bouncy_bonanza_bunch_5:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_7:
                lambda state: self.has_tires(state) and self.can_slap(state),
            LocationName.bouncy_bonanza_bunch_8:
                lambda state: self.has_tires(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.bouncy_bonanza_bunch_9:
                lambda state: self.has_tires(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.bouncy_bonanza_bunch_10:
                lambda state: self.has_tires(state) and (self.can_slap(state) or self.has_diddy(state)),

            LocationName.stop_go_station_clear:
                self.true,
            EventName.stop_go_station_clear:
                self.true,
            LocationName.stop_go_station_bonus_1:
                self.can_carry,
            LocationName.stop_go_station_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.stop_go_station_kong:
                self.can_roll,
            LocationName.stop_go_station_bunch_1:
                self.can_slap,
            LocationName.stop_go_station_bunch_2:
                self.can_slap,
            LocationName.stop_go_station_bunch_3:
                lambda state: self.can_slap(state) and (self.has_switches(state) or self.has_both_kongs(state)),
            LocationName.stop_go_station_token_1:
                self.true,
            LocationName.stop_go_station_bunch_4:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.stop_go_station_bunch_5:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.stop_go_station_bunch_6:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.stop_go_station_bunch_7:
                lambda state: self.can_slap(state),

            LocationName.millstone_mayhem_clear:
                lambda state: self.has_donkey(state) or self.has_tires(state),
            EventName.millstone_mayhem_clear:
                lambda state: self.has_donkey(state) or self.has_tires(state),
            LocationName.millstone_mayhem_bonus_1:
                lambda state: self.has_kannons(state) and (self.has_tires(state) or self.has_donkey(state)),
            LocationName.millstone_mayhem_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.millstone_mayhem_bonus_3:
                lambda state: self.can_carry(state) and (self.has_tires(state) or self.has_donkey(state)),
            LocationName.millstone_mayhem_kong:
                lambda state: self.has_kannons(state) and (self.has_tires(state) or self.has_donkey(state)),
            LocationName.millstone_mayhem_bunch_1:
                lambda state: self.can_slap(state) or (
                    self.has_tires(state) and self.has_diddy(state) and self.has_kannons(state)),
            LocationName.millstone_mayhem_bunch_2:
                lambda state: self.can_slap(state) or (self.has_tires(state) and self.has_diddy(state)),
            LocationName.millstone_mayhem_bunch_3:
                lambda state: self.can_slap(state) or (self.has_tires(state) and self.has_diddy(state)),
            LocationName.millstone_mayhem_bunch_4:
                lambda state: self.can_slap(state) or (
                    self.has_tires(state) and self.has_diddy(state) and self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_5:
                lambda state: self.can_slap(state) or (
                    self.has_tires(state) and self.has_diddy(state) and self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_6:
                lambda state: self.can_slap(state) or (
                    self.has_tires(state) and self.has_diddy(state) and self.has_winky(state)),
            LocationName.millstone_mayhem_bunch_7:
                lambda state: self.has_donkey(state) or self.has_tires(state),
            LocationName.millstone_mayhem_bunch_8:
                lambda state: self.has_donkey(state) or self.has_tires(state),
            LocationName.millstone_mayhem_bunch_9:
                lambda state: self.can_slap(state) or (
                    self.has_tires(state) and self.has_diddy(state) and self.has_winky(state)),

            LocationName.necky_nuts_clear:
                self.true,
            LocationName.defeated_necky_1:
                self.true,

            LocationName.vulture_culture_clear:
                self.has_kannons,
            EventName.vulture_culture_clear:
                self.has_kannons,
            LocationName.vulture_culture_bonus_1:
                lambda state: self.has_kannons(state) and self.has_tires(state),
            LocationName.vulture_culture_bonus_2:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_bonus_3:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_kong:
                lambda state: self.has_kannons(state) and self.can_carry(state),
            LocationName.vulture_culture_bunch_1:
                self.can_slap,
            LocationName.vulture_culture_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_3:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_both_kongs(state)),
            LocationName.vulture_culture_bunch_4:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.vulture_culture_bunch_5:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.vulture_culture_bunch_6:
                lambda state: self.has_kannons(state) and self.can_slap(state),

            LocationName.tree_top_town_clear:
                self.has_kannons,
            EventName.tree_top_town_clear:
                self.has_kannons,
            LocationName.tree_top_town_bonus_1:
                self.has_kannons,
            LocationName.tree_top_town_bonus_2:
                self.has_kannons,
            LocationName.tree_top_town_kong:
                self.has_kannons,
            LocationName.tree_top_town_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.tree_top_town_bunch_2:
                lambda state: self.has_kannons(state) and self.can_slap(state),
            LocationName.tree_top_town_bunch_3:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.tree_top_town_bunch_4:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.tree_top_town_token_1:
                self.has_kannons,

            LocationName.forest_frenzy_clear:
                self.can_climb,
            EventName.forest_frenzy_clear:
                self.can_climb,
            LocationName.forest_frenzy_bonus_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.forest_frenzy_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.forest_frenzy_kong:
                lambda state: self.can_climb(state) and self.can_roll(state),
            LocationName.forest_frenzy_bunch_1:
                lambda state: (self.can_slap(state) and self.can_climb(state)) or 
                    (self.has_diddy(state) and (self.can_climb(state) or self.can_roll(state))),
            LocationName.forest_frenzy_bunch_2:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.forest_frenzy_bunch_3:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.forest_frenzy_bunch_4:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.forest_frenzy_bunch_5:
                lambda state: self.can_climb(state) and self.can_slap(state),
            LocationName.forest_frenzy_balloon_1:
                self.can_climb,

            LocationName.temple_tempest_clear:
                lambda state: (self.can_climb(state) or (self.has_diddy(state) and self.can_roll(state))) and 
                    (self.has_tires(state) or (self.can_carry(state) and self.has_expresso(state))),
            EventName.temple_tempest_clear:
                lambda state: (self.can_climb(state) or (self.has_diddy(state) and self.can_roll(state))) and 
                    (self.has_tires(state) or (self.can_carry(state) and self.has_expresso(state))),
            LocationName.temple_tempest_bonus_1:
                lambda state: (self.can_climb(state) or (self.has_diddy(state) and self.can_roll(state))) and self.can_carry(state),
            LocationName.temple_tempest_bonus_2:
                lambda state: self.has_kannons(state) and (self.can_climb(state) or 
                    (self.can_carry(state) and self.has_expresso(state) and self.has_diddy(state))),
            LocationName.temple_tempest_kong:
                lambda state: (self.can_climb(state) and self.has_tires(state)) or 
                    (self.can_carry(state) and self.has_expresso(state) and self.has_diddy(state)),
            LocationName.temple_tempest_token_1:
                self.true,
            LocationName.temple_tempest_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.temple_tempest_bunch_2:
                lambda state: (self.can_slap(state) and self.can_climb(state)) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state)),
            LocationName.temple_tempest_bunch_3:
                lambda state: self.can_slap(state) and (self.can_climb(state) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state))),
            LocationName.temple_tempest_bunch_4:
                lambda state: (self.can_slap(state) and self.can_climb(state)) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state)),
            LocationName.temple_tempest_bunch_5:
                lambda state: (self.can_slap(state) and self.can_climb(state)) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state)),
            LocationName.temple_tempest_bunch_6:
                lambda state: self.has_tires(state) and self.can_slap(state) and (self.can_climb(state) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state))),
            LocationName.temple_tempest_bunch_7:
                lambda state: (self.can_climb(state) and self.has_tires(state)) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state)),
            LocationName.temple_tempest_bunch_8:
                lambda state: (self.can_climb(state) and self.has_tires(state)) or 
                    (self.has_diddy(state) and self.can_roll(state) and self.has_expresso(state)),

            LocationName.orang_utan_gang_clear:
                self.true,
            EventName.orang_utan_gang_clear:
                self.true,
            LocationName.orang_utan_gang_bonus_1:
                self.has_expresso,
            LocationName.orang_utan_gang_bonus_2:
                lambda state: self.can_carry(state) and (self.has_expresso(state) or (self.has_diddy(state) and self.can_roll(state))),
            LocationName.orang_utan_gang_bonus_3:
                lambda state: self.can_carry or self.has_expresso(state),
            LocationName.orang_utan_gang_bonus_4:
                lambda state: self.can_carry or self.has_expresso(state),
            LocationName.orang_utan_gang_bonus_5:
                self.true,
            LocationName.orang_utan_gang_kong:
                lambda state: self.can_carry(state) and self.has_tires(state) and 
                    (self.can_roll(state) or self.has_expresso(state)) ,
            LocationName.orang_utan_gang_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.orang_utan_gang_bunch_2:
                lambda state: self.can_carry(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.orang_utan_gang_bunch_3:
                self.can_slap,
            LocationName.orang_utan_gang_bunch_4:
                lambda state: self.can_roll(state) or self.has_expresso(state),
            LocationName.orang_utan_gang_bunch_5:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.orang_utan_gang_bunch_6:
                lambda state: self.has_expresso(state) or (self.has_diddy(state) and self.can_roll(state)),
            LocationName.orang_utan_gang_token_1:
                self.has_expresso,
            LocationName.orang_utan_gang_bunch_7:
                lambda state: self.can_slap(state) or self.has_diddy(state),
            LocationName.orang_utan_gang_bunch_8:
                self.true,
            LocationName.orang_utan_gang_bunch_9:
                self.true,

            LocationName.clam_city_clear:
                self.can_swim,
            EventName.clam_city_clear:
                self.can_swim,
            LocationName.clam_city_kong:
                self.can_swim,
            LocationName.clam_city_bunch_1:
                self.true,
            LocationName.clam_city_bunch_2:
                self.can_swim,
            LocationName.clam_city_token_1:
                self.can_swim,

            LocationName.bumble_b_rumble_clear:
                self.can_carry,
            LocationName.defeated_bumble_b:
                self.can_carry,

            LocationName.snow_barrel_blast_clear:
                self.has_kannons,
            EventName.snow_barrel_blast_clear:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bonus_3:
                self.has_kannons,
            LocationName.snow_barrel_blast_kong:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_1:
                lambda state: self.has_kannons(state) or self.can_slap(state) or self.has_diddy(state),
            LocationName.snow_barrel_blast_balloon_1:
                lambda state: self.has_kannons(state) or self.has_diddy(state),
            LocationName.snow_barrel_blast_bunch_2:
                lambda state: (self.has_kannons(state) and 
                    (self.can_slap(state) or self.has_diddy(state))) or self.has_both_kongs(state),
            LocationName.snow_barrel_blast_bunch_3:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.snow_barrel_blast_token_1:
                self.has_kannons,
            LocationName.snow_barrel_blast_balloon_2:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_4:
                self.has_kannons,
            LocationName.snow_barrel_blast_bunch_5:
                lambda state: self.has_kannons(state) and (self.can_slap(state) or self.has_diddy(state)),

            LocationName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            EventName.slipslide_ride_clear:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bonus_1:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_2:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.slipslide_ride_bonus_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_1:
                self.can_climb,
            LocationName.slipslide_ride_bunch_2:
                lambda state: self.can_climb(state) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.slipslide_ride_bunch_3:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_4:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_5:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_6:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_7:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.slipslide_ride_bunch_8:
                lambda state: self.can_climb(state) and self.has_kannons(state) and 
                    (self.can_slap(state) or self.has_diddy(state)),
            LocationName.slipslide_ride_bunch_9:
                lambda state: self.can_climb(state) and self.has_kannons(state) and 
                    (self.can_slap(state) or self.has_diddy(state)),
            LocationName.slipslide_ride_token_1:
                lambda state: self.can_climb(state) and self.has_kannons(state),

            LocationName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            EventName.ice_age_alley_clear:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),
            LocationName.ice_age_alley_bonus_1:
                lambda state: (self.can_climb(state) or self.has_expresso(state)) and self.has_kannons(state),
            LocationName.ice_age_alley_bonus_2:
                lambda state: self.has_expresso(state) and self.has_kannons(state),
            LocationName.ice_age_alley_kong:
                self.has_expresso,
            LocationName.ice_age_alley_bunch_1:
                lambda state: self.can_slap(state) or (self.has_expresso(state) and self.has_diddy(state)),
            LocationName.ice_age_alley_bunch_2:
                lambda state: ((self.can_climb(state) and self.has_kannons(state)) or 
                    self.has_expresso(state)) and (self.can_slap(state) or self.has_diddy(state)),
            LocationName.ice_age_alley_bunch_3:
                lambda state: (self.can_climb(state) and self.has_kannons(state)) or self.has_expresso(state),

            LocationName.croctopus_chase_clear:
                self.can_swim,
            EventName.croctopus_chase_clear:
                self.can_swim,
            LocationName.croctopus_chase_kong:
                self.can_swim,
            LocationName.croctopus_chase_bunch_1:
                self.can_swim,
            LocationName.croctopus_chase_token_1:
                self.can_swim,
            LocationName.croctopus_chase_token_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_2:
                self.can_swim,
            LocationName.croctopus_chase_bunch_3:
                self.can_swim,
            LocationName.croctopus_chase_bunch_4:
                self.can_swim,
            LocationName.croctopus_chase_bunch_5:
                self.can_swim,
            LocationName.croctopus_chase_balloon_1:
                self.can_swim,

            LocationName.torchlight_trouble_clear:
                self.true,
            EventName.torchlight_trouble_clear:
                self.true,
            LocationName.torchlight_trouble_bonus_1:
                self.can_carry,
            LocationName.torchlight_trouble_bonus_2:
                self.can_carry,
            LocationName.torchlight_trouble_kong:
                lambda state: self.can_carry(state) and self.can_roll(state),
            LocationName.torchlight_trouble_bunch_1:
                lambda state: self.can_slap(state) or self.has_diddy(state),

            LocationName.rope_bridge_rumble_clear:
                self.has_tires,
            EventName.rope_bridge_rumble_clear:
                self.has_tires,
            LocationName.rope_bridge_rumble_bonus_1:
                self.has_kannons,
            LocationName.rope_bridge_rumble_bonus_2:
                lambda state: self.has_tires(state) and self.has_kannons(state),
            LocationName.rope_bridge_rumble_kong:
                lambda state: self.has_tires(state) and self.can_roll(state),
            LocationName.rope_bridge_rumble_bunch_1:
                lambda state: self.has_tires(state) and self.can_roll(state),

            LocationName.really_gnawty_rampage_clear:
                self.true,
            LocationName.defeated_gnawty_2:
                self.true,

            LocationName.oil_drum_alley_clear:
                lambda state: self.has_kannons(state) and 
                    (self.has_tires(state) or (self.has_diddy(state) and 
                         (self.has_rambi(state) or self.can_roll(state)))),
            EventName.oil_drum_alley_clear:
                lambda state: self.has_kannons(state) and 
                    (self.has_tires(state) or (self.has_diddy(state) and 
                         (self.has_rambi(state) or self.can_roll(state)))),
            LocationName.oil_drum_alley_bonus_1:
                lambda state: self.can_carry(state) and self.has_kannons(state),
            LocationName.oil_drum_alley_bonus_2:
                self.can_carry,
            LocationName.oil_drum_alley_bonus_3:
                self.can_carry,
            LocationName.oil_drum_alley_bonus_4:
                self.has_kannons,
            LocationName.oil_drum_alley_kong:
                lambda state: self.has_kannons(state) and 
                    (self.has_tires(state) or (self.has_diddy(state) and 
                         (self.has_rambi(state) or self.can_roll(state)))),
            LocationName.oil_drum_alley_bunch_1:
                self.has_kannons,
            LocationName.oil_drum_alley_bunch_2:
                self.has_kannons,

            LocationName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) or (self.can_roll(state) and self.has_kannons(state)),
            EventName.trick_track_trek_clear:
                lambda state: self.has_platforms(state) or (self.can_roll(state) and self.has_kannons(state)),
            LocationName.trick_track_trek_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state) and self.can_roll(state),
            LocationName.trick_track_trek_bonus_2:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.trick_track_trek_bonus_3:
                lambda state: self.has_platforms(state) or (self.can_roll(state) and self.has_kannons(state)),
            LocationName.trick_track_trek_kong:
                self.has_platforms,
            LocationName.trick_track_trek_bunch_1:
                self.has_platforms,
            LocationName.trick_track_trek_token_1:
                lambda state: self.has_platforms(state) or (self.can_roll(state) and self.has_kannons(state)),

            LocationName.elevator_antics_clear:
                self.can_climb,
            EventName.elevator_antics_clear:
                self.can_climb,
            LocationName.elevator_antics_bonus_1:
                lambda state: self.can_climb(state) and (self.can_roll(state) or self.has_diddy(state)),
            LocationName.elevator_antics_bonus_2:
                self.can_climb,
            LocationName.elevator_antics_bonus_3:
                self.can_climb,
            LocationName.elevator_antics_kong:
                lambda state: self.can_climb(state) and self.has_kannons(state),
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.can_climb,
            LocationName.elevator_antics_bunch_3:
                self.can_climb,

            LocationName.poison_pond_clear:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            EventName.poison_pond_clear:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_kong:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_1:
                self.true,
            LocationName.poison_pond_bunch_2:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_3:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_4:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_5:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_token_1:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_token_2:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),
            LocationName.poison_pond_bunch_6:
                lambda state: self.can_swim(state) and (self.has_enguarde(state) or self.has_both_kongs(state)),

            LocationName.mine_cart_madness_clear:
                self.has_minecart,
            EventName.mine_cart_madness_clear:
                self.has_minecart,
            LocationName.mine_cart_madness_bonus_1:
                lambda state: self.has_minecart(state) and self.can_climb(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_2:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_bonus_3:
                lambda state: self.has_minecart(state) and self.has_tires(state) and self.has_kannons(state),
            LocationName.mine_cart_madness_kong:
                lambda state: self.has_minecart(state) and (self.has_tires(state) or self.has_donkey(state)),
            LocationName.mine_cart_madness_token_1:
                self.has_minecart,
            LocationName.mine_cart_madness_bunch_1:
                self.has_minecart,

            LocationName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            EventName.blackout_basement_clear:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state),
            LocationName.blackout_basement_bonus_1:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_bonus_2:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.can_carry(state) and self.has_kannons(state),
            LocationName.blackout_basement_kong:
                lambda state: self.can_climb(state) and self.has_tires(state) and self.has_platforms(state) and self.has_kannons(state),
            LocationName.blackout_basement_token_1:
                self.true,
            LocationName.blackout_basement_bunch_1:
                lambda state: self.can_climb(state) and self.has_tires(state),

            LocationName.boss_dumb_drum_clear:
                lambda state: (self.has_diddy(state) and self.can_roll(state)) or self.has_donkey(state),
            LocationName.defeated_boss_dumb_drum:
                lambda state: (self.has_diddy(state) and self.can_roll(state)) or self.has_donkey(state),

            LocationName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state),
            EventName.tanked_up_trouble_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state),
            LocationName.tanked_up_trouble_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.tanked_up_trouble_kong:
                lambda state: self.has_platforms(state) and self.has_tires(state),
            LocationName.tanked_up_trouble_bunch_1:
                self.has_platforms,
            LocationName.tanked_up_trouble_bunch_2:
                self.has_platforms,
            LocationName.tanked_up_trouble_token_1:
                self.has_platforms,
            LocationName.tanked_up_trouble_bunch_3:
                lambda state: self.has_platforms(state) and self.has_tires(state),
            LocationName.tanked_up_trouble_bunch_4:
                lambda state: self.has_platforms(state) and self.has_tires(state),

            LocationName.manic_mincers_clear:
                lambda state: self.has_tires(state) or self.can_carry(state) or 
                    self.has_rambi(state) or self.has_both_kongs(state),
            EventName.manic_mincers_clear:
                lambda state: self.has_tires(state) or self.can_carry(state) or 
                    self.has_rambi(state) or self.has_both_kongs(state),
            LocationName.manic_mincers_bonus_1:
                lambda state: self.can_carry(state) or self.has_rambi(state),
            LocationName.manic_mincers_bonus_2:
                lambda state: self.can_carry(state) or self.has_rambi(state),
            LocationName.manic_mincers_kong:
                self.true,
            LocationName.manic_mincers_bunch_1:
                self.true,
            LocationName.manic_mincers_bunch_2:
                self.true,
            LocationName.manic_mincers_token_1:
                self.true,

            LocationName.misty_mine_clear:
                self.can_climb,
            EventName.misty_mine_clear:
                self.can_climb,
            LocationName.misty_mine_bonus_1:
                self.can_climb,
            LocationName.misty_mine_bonus_2:
                lambda state: self.can_climb(state) and (self.can_carry(state) or self.has_expresso(state)),
            LocationName.misty_mine_kong:
                self.can_climb,
            LocationName.misty_mine_token_1:
                self.can_carry,
            LocationName.misty_mine_bunch_1:
                self.can_carry,
            LocationName.misty_mine_bunch_2:
                self.true,
            LocationName.misty_mine_token_2:
                lambda state: self.can_climb(state) and (self.has_expresso(state) or self.can_roll(state)),

            LocationName.loopy_lights_clear:
                self.has_tires,
            EventName.loopy_lights_clear:
                self.has_tires,
            LocationName.loopy_lights_bonus_1:
                self.has_kannons,
            LocationName.loopy_lights_bonus_2:
                lambda state: self.can_carry(state) and (self.has_tires(state) or self.can_roll(state)),
            LocationName.loopy_lights_kong:
                lambda state: self.has_tires(state) and self.has_kannons(state) and self.can_roll(state) and self.can_carry(state),
            LocationName.loopy_lights_bunch_1:
                lambda state: self.has_tires(state) or self.can_roll(state),
            LocationName.loopy_lights_bunch_2:
                self.has_tires,

            LocationName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and 
                    (self.has_both_kongs(state) or self.can_roll(state) or self.can_carry(state)),
            EventName.platform_perils_clear:
                lambda state: self.has_platforms(state) and self.has_tires(state) and 
                    (self.has_both_kongs(state) or self.can_roll(state) or self.can_carry(state)),
            LocationName.platform_perils_bonus_1:
                lambda state: self.has_platforms(state) and self.has_kannons(state),
            LocationName.platform_perils_bonus_2:
                lambda state: self.has_platforms(state) and 
                    self.has_tires(state) and self.has_kannons(state) and 
                    (self.has_both_kongs(state) or self.can_roll(state) or self.can_carry(state)),
            LocationName.platform_perils_kong:
                lambda state: self.has_platforms(state) and self.has_tires(state) and 
                    (self.has_both_kongs(state) or self.can_roll(state) or self.can_carry(state)),
            LocationName.platform_perils_token_1:
                self.has_platforms,
            LocationName.platform_perils_bunch_1:
                lambda state: self.has_platforms(state) and self.can_carry(state),

            LocationName.necky_revenge_clear:
                self.true,
            LocationName.defeated_necky_2:
                self.true,
        }



    def set_dkc_rules(self) -> None:
        super().set_dkc_rules()
