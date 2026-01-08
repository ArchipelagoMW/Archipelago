# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/rules.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from typing import Tuple
from BaseClasses import CollectionState
from collections.abc import Callable, Mapping, MutableMapping
from . import Hm, items, locations, species
from ..options import PokemonPlatinumOptions

Rule = Callable[[CollectionState], bool]

def always_true(*args, **kwargs) -> bool:
    return True

def create_hm_badge_rule(hm: Hm, player: int) -> Rule:
    badge_item = hm.badge_item()
    if badge_item is not None:
        def hm_badge_rule(state: CollectionState) -> bool:
            return state.has(badge_item, player)
    else:
        def hm_badge_rule(state: CollectionState) -> bool:
            return True
    return hm_badge_rule

class Rules:
    exit_rules: Mapping[Tuple[str, str], Rule]
    location_rules: Mapping[str, Rule]
    encounter_type_rules: Mapping[str, Rule]
    location_type_rules: Mapping[str, Rule]
    common_rules: MutableMapping[str, Callable]
    opts: PokemonPlatinumOptions
    
    def __init__(self, player: int, common_rules: MutableMapping[str, Callable], opts: PokemonPlatinumOptions):
        self.player = player
        self.opts = opts
        self.common_rules = common_rules
        self.common_rules.update({ hm.name.lower():self.create_hm_rule(hm, player) for hm in Hm })
        def regional_mons(n: int) -> Rule:
            mons = [f"mon_{spec}" for spec in species.regional_mons]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(mons, player, n)
            return rule
        def mons(n: int) -> Rule:
            mons = [f"mon_{spec}" for spec in species.species.keys()]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(mons, player, n)
            return rule
        def badges(n: int) -> Rule:
            badges = [items.items[loc.original_item].label
                for loc in locations.locations.values() if loc.type == "badge"]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(badges, player, n)
            return rule
        self.common_rules["regional_mons"] = regional_mons
        self.common_rules["mons"] = mons
        self.common_rules["badges"] = badges

    def fill_rules(self):
        self.common_rules.update({
            "national_dex": (lambda state : state.has("Upgradable Pokédex", self.player, 3)),
            "dowsingmachine_if_opt": (lambda state : state.has_all(["DOWSING MACHINE", "Pokétch"], self.player)) if self.opts.dowsing_machine_logic.value != 0 else always_true,
            "defog_if_opt": (self.common_rules["defog"]) if self.opts.visibility_hm_logic.value != 0 else always_true,
            "flash_if_opt": (self.common_rules["flash"]) if self.opts.visibility_hm_logic.value != 0 else always_true,
            "poketch_req": (lambda state : state.has_all(["Parcel", "Coupon 2", "Coupon 1", "Coupon 3"], self.player)),
        })
        self.exit_rules = {
            ("valor_lakefront", "lake_valor_drained"): (lambda state : state.has("event_lake_explosion", self.player)),
            ("valor_lakefront", "route_222"): (lambda state : state.has("event_distortion_world", self.player)) if self.opts.early_sunyshore.value == 0 else always_true,
            ("valor_lakefront", "lake_valor"): (lambda state : state.has("event_distortion_world", self.player)),
            ("verity_lakefront", "lake_verity"): (lambda state : state.has("event_lake_valor_defeat_saturn", self.player)),
            ("acuity_lakefront", "lake_acuity"): (lambda state : state.has("event_lake_verity_defeat_mars", self.player) and self.common_rules["rock_climb"](state)),
            ("acuity_lakefront", "lake_acuity_low_water"): (self.common_rules["rock_climb"]),
            ("route_219", "route_220"): (self.common_rules["surf"]),
            ("route_221", "pal_park_lobby"): (self.common_rules["national_dex"]),
            ("jubilife_city", "route_203"): (self.common_rules["poketch_req"]) if self.opts.parcel_coupons_route_203.value != 0 else always_true,
            ("jubilife_city", "jubilife_tv_1f"): (lambda state : state.has("event_coal_badge", self.player)),
            ("oreburgh_gate_1f", "oreburgh_gate_b1f"): (self.common_rules["rock_smash"]),
            ("route_207_south", "route_207"): (lambda state : state.has("Bicycle", self.player)),
            ("ravaged_path", "route_204_north"): (self.common_rules["rock_smash"]),
            ("floaroma_town", "route_205_south"): (lambda state : state.has("Works Key", self.player) or self.common_rules["surf"](state)),
            ("route_205_south", "fuego_ironworks_outside"): (self.common_rules["surf"]),
            ("route_205_south", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("route_205_north", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("eterna_forest", "old_chateau"): (self.common_rules["cut"]),
            ("eterna_city", "team_galactic_eterna_building_1f"): (self.common_rules["cut"]),
            ("mt_coronet_1f_north_room_1_left", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["rock_smash"]),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_left"): (lambda state : self.common_rules["rock_smash"](state) or self.common_rules["strength"](state)),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_top"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_b1f"): (lambda state : self.common_rules["defog_if_opt"](state) and self.common_rules["fly"](state)) if self.opts.north_sinnoh_fly.value != 0 else (self.common_rules["defog_if_opt"]),
            ("mt_coronet_1f_north_room_1_bottom", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("route_206_cycling_road_north_gate", "cycling_road"): (lambda state : state.has("Bicycle", self.player)),
            ("route_206_cycling_road_south_gate", "cycling_road"): (lambda state : state.has("Bicycle", self.player)),
            ("route_206", "route_206_upper"): (self.common_rules["cut"]),
            ("route_206_upper", "wayward_cave_1f"): (self.common_rules["flash_if_opt"]),
            ("mt_coronet_1f_south", "mt_coronet_2f_right"): (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["surf"](state)),
            ("mt_coronet_2f_right", "mt_coronet_2f_left"): (self.common_rules["strength"]),
            ("route_209_lost_tower_2f", "route_209_lost_tower_3f"): (self.common_rules["defog_if_opt"]),
            ("maniac_tunnel", "solaceon_ruins_maniac_tunnel_room"): (lambda state : state.has("event_solaceon_ruins", self.player)) if self.opts.unown_option.value == self.opts.unown_option.option_vanilla else (lambda state : state.has("Unown File", self.player, 26)) if self.opts.unown_option.value == self.opts.unown_option.option_item else always_true,
            ("route_210_south", "route_210_south_upper"): (lambda state : state.has("SecretPotion", self.player)),
            ("route_210_south_upper", "route_210_south"): (lambda state : state.has("SecretPotion", self.player)),
            ("route_210_south_upper", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("route_210_north", "route_210_grandma_wilma_house"): (self.common_rules["rock_climb"]),
            ("celestic_town", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("galactic_hq_wo_key", "veilstone_city_galactic_warehouse"): (lambda state : state.has_any(["event_lake_acuity_meet_jupiter", "Storage Key"], self.player)),
            ("veilstone_city_galactic_warehouse", "galactic_hq_wo_key"): (lambda state : state.has_any(["event_lake_acuity_meet_jupiter", "Storage Key"], self.player)),
            ("veilstone_city", "galactic_hq_w_key"): (lambda state : state.has("Galactic Key", self.player)),
            ("route_214", "spring_path"): (lambda state : state.has("event_distortion_world", self.player)),
            ("route_214", "route_214_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("sendoff_spring", "turnback_cave_entrance"): (self.common_rules["defog_if_opt"]),
            ("route_213", "grand_lake_route_213_northeast_house"): (self.common_rules["rock_climb"]),
            ("route_218", "route_218_gate_to_canalave_city"): (self.common_rules["surf"]),
            ("canalave_city", "fullmoon_island"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("mt_coronet_1f_tunnel_room", "mt_coronet_1f_tunnel_room_base"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_tunnel_room_base", "mt_coronet_1f_tunnel_room"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_north_room_2", "mt_coronet_b1f"): (self.common_rules["defog_if_opt"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_north_plat"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_south_entrance"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_north_plat", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south_entrance", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2_lower", "mt_coronet_4f_rooms_1_and_2"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2", "mt_coronet_4f_rooms_1_and_2_lower"): (self.common_rules["rock_climb"]),
            ("mt_coronet_2f_left", "mt_coronet_3f"): (lambda state : state.has("event_galactic_hq_defeat_cyrus", self.player)),
            ("snowpoint_city", "fight_area"): (lambda state : state.has_any(["S.S. Ticket", "event_beat_cynthia"], self.player)),
            ("snowpoint_city", "snowpoint_temple_1f"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("victory_road_1f", "victory_road_1f_room_1"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("route_223", "pokemon_league_south_south"): (self.common_rules["surf"]),
            ("pokemon_league_south_south", "pokemon_league_south"): (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            ("pokemon_league_north_pokecenter_1f", "pokemon_league_elevator_to_aaron_room"): (self.common_rules["badges"](8)),
            ("victory_road_1f_entrance", "victory_road_2f_entrance"): (self.common_rules["rock_climb"]),
            ("victory_road_2f_entrance", "victory_road_2f"): (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["strength"](state)),
            ("pastoria_city_observatory_gate_1f", "virt_great_marsh"): (lambda state : state.has("Marsh Pass", self.player)) if self.opts.marsh_pass.value != 0 else always_true,
            ("route_212_north_top", "route_212_north"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("route_212_north", "route_212_north_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("route_214_top", "route_214"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("fight_area", "route_225_gate_to_fight_area"): (self.common_rules["national_dex"]),
            ("fight_area", "route_230"): (self.common_rules["national_dex"]),
            ("route_230", "route_229"): (self.common_rules["surf"]),
            ("route_230", "fight_area"): (lambda state : self.common_rules["national_dex"](state) and self.common_rules["surf"](state)),
            ("route_228", "route_228_rock_peak_ruins"): (lambda state : state.has("Bicycle", self.player) or self.common_rules["fly"](state)),
            ("route_226_east", "route_226_mid"): (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["surf"](state)),
            ("route_226_mid", "route_226_east"): (self.common_rules["surf"]),
            ("route_226_west", "route_226_mid"): (self.common_rules["rock_climb"]),
            ("route_227_lower", "route_227"): (lambda state : state.has("Bicycle", self.player)),
            ("stark_mountain_room_1_entrance", "stark_mountain_room_1"): (self.common_rules["strength"]),
            ("stark_mountain_room_1", "stark_mountain_room_2"): (self.common_rules["rock_smash"]),
            ("sunyshore_city", "sunyshore_city_east_house"): (self.common_rules["rock_climb"]),
            ("ravaged_path", "ravaged_path_old_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_good_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_super_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_surf"): (self.common_rules["rock_smash"]),
            ("route_218", "route_218_land"): (self.common_rules["surf"]),
            ("route_230", "route_230_land"): (self.common_rules["surf"]),
        }
        self.location_rules = {
            "Twinleaf Town - Hidden Item in Pond": (self.common_rules["surf"]),
            "Lake Verity - Item in Southwest Grass Patch": (self.common_rules["surf"]),
            "Sandgem Town Pokemon Research Lab - National Pokédex from Prof Oak": (self.common_rules["regional_mons"](self.opts.regional_dex_goal.value)),
            "Sandgem Town Pokemon Research Lab - Poké Radar from Rowan": (self.common_rules["regional_mons"](self.opts.regional_dex_goal.value)),
            "Jubilife Trainers' School - Town Map from Rival": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon from East Clown": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon from Clown in front of Poketch HQ": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon from Clown in front of Jubilife TV": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Poketch from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Calculator App from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Pedometer App from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Party Status App from CEO": (self.common_rules["poketch_req"]),
            "Oreburgh Gate B1F - Item After Ramps": (lambda state : state.has("Bicycle", self.player) or self.common_rules["surf"](state)),
            "Oreburgh Gate B1F - Item in Pit North": (lambda state : self.common_rules["surf"](state) and self.common_rules["strength"](state)),
            "Oreburgh Gate B1F - Item in Pit South": (lambda state : self.common_rules["surf"](state) and self.common_rules["strength"](state)),
            "Oreburgh City - Gift from Overalls Man for Showing Geodude in North House": (lambda state : state.has("mon_geodude", self.player)),
            "Jubilife City - Fashion Case from Overalls Man After Grunts Battle After Oreburgh Gym": (lambda state : state.has("event_coal_badge", self.player)),
            "Route 204 - Item Behind Southwest Pond": (self.common_rules["surf"]),
            "Route 204 - Item Behind Eastern Pond": (self.common_rules["surf"]),
            "Ravaged Path - Item Left of Breakable Rocks": (self.common_rules["rock_smash"]),
            "Ravaged Path - Item at Water's End": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Ravaged Path - Item Behind Long Boulder Trail": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Upper Route 204 - Woman Behind Cut Tree": (self.common_rules["cut"]),
            "Valley Windworks - Item Behind Windworks": (self.common_rules["surf"]),
            "Valley Windworks - Item Beyond Fence": (self.common_rules["surf"]),
            "Valley Windworks - Hidden Item Beyond Fence": (self.common_rules["surf"]),
            "Eterna Forest - Hidden Item Next to Old Chateau": (self.common_rules["cut"]),
            "Eterna Forest - Item Next to Old Chateau": (self.common_rules["cut"]),
            "Eterna City - Item Behind Fence": (self.common_rules["cut"]),
            "Eterna City - Bike from Rad Rickshaw": (lambda state : state.has("event_eterna_defeat_team_galactic", self.player)),
            "Eterna City - Hidden Item Above Pond": (self.common_rules["surf"]),
            "Eterna City - Up-Grade from Prof Oak": (lambda state : state.has("event_met_oak_pal_park", self.player)),
            "Route 206 North Gate - Reward For 35 Pokemon Seen": (self.common_rules["mons"](35)),
            "Route 211 West - Item Under Bridge": (self.common_rules["rock_smash"]),
            "Mt. Coronet (Route 211 Tunnel Room) - Item Behind Two Breakable Rocks": (self.common_rules["rock_smash"]),
            "Mt. Coronet (Route 211 Tunnel Room) - Item in Corner Above Ledge": (self.common_rules["strength"]),
            "Wayward Cave - Item in Southwest Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave - Item in Northwest Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave - Item Next to Five Rocks": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Rock Next to Mira": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Rock Below Picnicker on East Side": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Center Boulder": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Corner With Breakable Rock": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Southeast Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave Secret Basement - Item in Final Room": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave Secret Basement - Item Between Bike Bridges": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave Secret Basement - Item After Four Bike Jumps": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave Secret Basement - Item Next to Bike Ramp on Ledges": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave Secret Basement - Hidden Item Against Northwest Wall": (lambda state : state.has("Bicycle", self.player)),
            "Route 207 - Item Below Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Mt. Coronet (Routes 207-208 Room) - Item Across Upper Pond": (self.common_rules["surf"]),
            "Mt. Coronet (Routes 207-208 Room) - Item Across Lower Pond": (self.common_rules["surf"]),
            "Route 208 - Hidden Item Above Rock Climb Slope": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 208 - Item Above Waterfall": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Route 208 - Item Behind Breakable Rocks": (self.common_rules["rock_smash"]),
            "Route 209 - Item Down River in Southeast": (self.common_rules["surf"]),
            "Route 209 - Item in Corner Past West Mud Slide Pit": (lambda state : state.has("Bicycle", self.player)),
            "Route 209 - Item Behind Cut Tree": (self.common_rules["cut"]),
            "Lost Tower 5F - Gift from Old Woman on Right": (self.common_rules["defog"]),
            "Lost Tower 5F - Gift from Old Woman on Left": (self.common_rules["defog"]),
            "Solaceon Town - Pokémon History App from Ruin Maniac": (self.common_rules["regional_mons"](50)),
            "Solaceon Ruins B2F - Gift for Lending Defog to Hiker": (lambda state : state.has("HM05 Defog", self.player)),
            "Route 210 South - Item in Northwest Corner": (lambda state : state.has_all(["Bag", "Bicycle"], self.player)),
            "Route 210 North - Item Behind Breakable Rocks": (lambda state : state.has("Bicycle", self.player) and self.common_rules["rock_smash"](state)),
            "Route 210 North - Hidden Item on Ledge in Pit": (self.common_rules["rock_climb"]),
            "Route 210 North - Hidden Item up East Waterfall": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Route 210 North - Item Under West Bridge": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Route 210 North - Item on Ledge Below Move Tutor": (self.common_rules["rock_climb"]),
            "Celestic Town Cave - HM03 from Cynthia's Grandmother": (lambda state : state.has("Old Charm", self.player)),
            "Celestic Town - Item Below Shrine Right Stairs": (lambda state : state.has("Old Charm", self.player)),
            "Celestic Town - Hidden Item Above Shrine Left Stairs": (lambda state : state.has("Old Charm", self.player)),
            "Route 211 East - Hidden Item Up Rock Climb Slope": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 211 East - Item Up Rock Climb Slope": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 215 - Item Next to Black Belt Behind Cut Tree": (self.common_rules["cut"]),
            "Route 215 - Item Behind Cut Trees Below Northeast Grass Patch": (self.common_rules["cut"]),
            "Veilstone City - Item on Rock Climb Platform": (self.common_rules["rock_climb"]),
            "Galactic Warehouse - Item in Many Generators Room": (lambda state : state.has("Galactic Key", self.player)),
            "Route 214 - Item Across Pond": (self.common_rules["surf"]),
            "Valor Lakefront - SecretPotion from Cynthia": (lambda state : state.has("event_fen_badge", self.player)),
            "Valor Lakefront - Hidden Item After Rock Climbing From Route 213": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Item After Rock Climb Ledges 2": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Item After Rock Climb Ledges 1": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Gift from Locked Out Woman": (lambda state : state.has("Suite Key", self.player)),
            "Route 213 - Hidden Item Next to Honey Tree": (self.common_rules["rock_smash"]),
            "Route 213 - Hidden Suite Key By Reception": (self.common_rules["dowsingmachine_if_opt"]),
            "Route 213 - Item on Sandy Island": (self.common_rules["surf"]),
            "Route 213 - Item Down East Rock Climb Slopes": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden Item in Grass After Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden Item on Sandy Island": (self.common_rules["surf"]),
            "Route 213 - Hidden Item on Southeast White Rock": (self.common_rules["surf"]),
            "Route 213 - Item on Small Island Above Swimmers": (self.common_rules["surf"]),
            "Route 213 - Item By Grass After Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Route 213 - Item Behind Breakable Rock on Beach": (self.common_rules["rock_smash"]),
            "Pastoria City - Item in Trees Above Boats": (self.common_rules["surf"]),
            "Route 212 South - Item By Grass Patch in Water": (self.common_rules["surf"]),
            "Route 212 South - Hidden Item Below Two Trees on Corner": (self.common_rules["surf"]),
            "Route 212 South - Item Near Scientist Between Cut Trees": (self.common_rules["cut"]),
            "Route 212 South - Item on Ledge Above Move Tutor": (self.common_rules["cut"]),
            "Route 212 North - Item on West Ledge": (lambda state : self.common_rules["cut"](state) or self.common_rules["surf"](state)),
            "Route 212 North - Item in Flower Patch": (self.common_rules["surf"]),
            "Route 212 North - Item Next to North Pond": (self.common_rules["surf"]),
            "Route 212 South - Hidden Item on SW Bike Bridge Island": (lambda state : state.has("Bicycle", self.player) and self.common_rules["cut"](state)),
            "Route 212 South - Item on Northeast Island Past Bike Bridge": (lambda state : state.has_all(["Bag", "Bicycle"], self.player)) if self.opts.pastoria_barriers.value != 0 else (lambda state : state.has("Bicycle", self.player)),
            "Route 218 - Item in Northeast Corner": (self.common_rules["surf"]),
            "Route 218 - Item Below Fisherman": (self.common_rules["surf"]),
            "Canalave City - Item in Trees South of Canal": (self.common_rules["surf"]),
            "Iron Island - Metal Coat from Byron": (self.common_rules["national_dex"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item on Corner White Rock Before Exit": (self.common_rules["rock_smash"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item Above Big White Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item Behind Breakable Rock on Left": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Mt. Coronet Tunnel to 1F - Hidden Item in White Rock on South Ledge": (self.common_rules["rock_climb"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item on Right Path": (self.common_rules["rock_climb"]),
            "Mt. Coronet B1F - Item in SW Corner": (self.common_rules["rock_smash"]),
            "Mt. Coronet B1F - Item Behind West Boulder": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["strength"](state)),
            "Mt. Coronet B1F - Hidden Item Behind Breakable Rock West of Lake": (self.common_rules["rock_smash"]),
            "Mt. Coronet B1F - Item in Middle of Lake": (self.common_rules["surf"]),
            "Mt. Coronet B1F - Item in Northeast Corner of Lake": (lambda state : self.common_rules["surf"](state) or self.common_rules["rock_smash"](state)),
            "Mt. Coronet B1F - Item Behind Boulder": (self.common_rules["strength"]),
            "Mt. Coronet B1F - Item Against East Wall": (self.common_rules["rock_smash"]),
            "Mt. Coronet Outside 1 - Hidden Item Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Left - Hidden Item Behind NW Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Right - Hidden Item on Wall Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Right - Hidden Item in Corner Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Room Above Waterfall - Item 1": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Mt. Coronet 4F Room Above Waterfall - Item 2": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Mt. Coronet 4F Room Above Waterfall - Hidden Item in Rock": (lambda state : self.common_rules["waterfall"](state) and self.common_rules["surf"](state)),
            "Route 216 - Right Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Bottom Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Top Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Left Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 217 - Gift from Hiker": (lambda state : state.has("HM08 Rock Climb", self.player)),
            "Acuity Lakefront - Item East of Lake Entrance": (self.common_rules["rock_climb"]),
            "Snowpoint Temple B4F - Item Past Ice Tile": (self.common_rules["strength"]),
            "Route 222 - Hidden Item in Grass Below Fence 1": (lambda state : self.common_rules["rock_smash"](state) or self.common_rules["surf"](state)),
            "Route 222 - Item Behind Cut Tree": (self.common_rules["cut"]),
            "Route 222 - Item in Grass Below Fence": (lambda state : self.common_rules["rock_smash"](state) or self.common_rules["surf"](state)),
            "Route 222 - Hidden Item in Grass Below Fence 2": (lambda state : self.common_rules["rock_smash"](state) or self.common_rules["surf"](state)),
            "Route 222 - Hidden Item in Grass Below SE Fence": (self.common_rules["surf"]),
            "Sunyshore City - HM07 from Jasmine": (lambda state : state.has("event_beacon_badge", self.player)),
            "Pokétch Company - Memo Pad App": (lambda state : state.has_all(["Parcel", "Coupon 2", "Coupon 1", "Coupon 3"], self.player) and self.common_rules["badges"](1)(state)),
            "Pokétch Company - Marking Map App": (lambda state : state.has_all(["Parcel", "Coupon 2", "Coupon 1", "Coupon 3"], self.player) and self.common_rules["badges"](3)(state)),
            "Pokétch Company - Link Searcher App": (lambda state : state.has_all(["Parcel", "Coupon 2", "Coupon 1", "Coupon 3"], self.player) and self.common_rules["badges"](5)(state)),
            "Pokétch Company - Move Tester App": (lambda state : state.has_all(["Parcel", "Coupon 2", "Coupon 1", "Coupon 3"], self.player) and self.common_rules["badges"](7)(state)),
            "Route 223 - Item Surrounded by West Rocks": (self.common_rules["surf"]),
            "Route 223 - Item Behind Sailor": (self.common_rules["surf"]),
            "Route 223 - Northwest Item": (self.common_rules["surf"]),
            "Route 223 - Northeast Item": (self.common_rules["surf"]),
            "Route 223 - Hidden Item on First Islet": (self.common_rules["surf"]),
            "Route 223 - Hidden Item to Left of Sailor": (self.common_rules["surf"]),
            "Victory Road 2F - Item in NE": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road 2F - Item Above Ledge": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road 2F - NW Item": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road 1F - First Item on Left": (self.common_rules["rock_climb"]),
            "Victory Road 1F - Hidden Item Before First Staircase to 2F": (self.common_rules["rock_climb"]),
            "Great Marsh - Matchup Checker App from Cowgirl": (lambda state : state.has("Marsh Pass", self.player)) if self.opts.marsh_pass.value != 0 else always_true,
            "Route 210 South - Old Charm from Cynthia": (lambda state : state.has("SecretPotion", self.player)),
            "Fight Area - Super Rod from Fisherman": (self.common_rules["national_dex"]),
            "Route 230 - Item on Island East Side": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Route 230 - Hidden Item on Island East Side Behind Breakable Rock": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Route 230 - Item on Island West Side": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Route 230 - Hidden Island on Island North Side": (lambda state : self.common_rules["rock_smash"](state) and self.common_rules["surf"](state)),
            "Route 229 - Item in Center Behind Cut Tree": (self.common_rules["cut"]),
            "Route 229 - Item Northeast of Pond": (self.common_rules["cut"]),
            "Route 229 - Hidden Item Southwest of Pond": (lambda state : self.common_rules["cut"](state) and self.common_rules["surf"](state)),
            "Resort Area - Item Across Pond": (self.common_rules["surf"]),
            "Route 228 - Item in Northernmost Pit": (lambda state : state.has("Bicycle", self.player) or self.common_rules["fly"](state)),
            "Route 228 - Item Behind Breakable Rocks": (self.common_rules["rock_smash"]),
            "Route 228 - Item Across Bike Rail Above Vents": (lambda state : state.has("Bicycle", self.player)),
            "Route 228 - Hidden Item in SE Corner by Rock": (lambda state : state.has("Bicycle", self.player)),
            "Route 228 - Hidden Item in SW Grass": (lambda state : state.has("Bicycle", self.player)),
            "Route 226 - Hidden Item in Tree Gap North of Meister's House": (self.common_rules["surf"]),
            "Route 226 - Hidden Item on Beach Below Rock Climb Area": (self.common_rules["surf"]),
            "Survival Area - Item to Left of Move Tutor's House": (self.common_rules["rock_climb"]),
            "Route 225 - Item on SW Hill": (self.common_rules["rock_climb"]),
            "Route 225 - Item Behind Cut Trees Near Trainer Trio": (self.common_rules["cut"]),
            "Route 225 - Item Behind Cut Trees Next to House": (self.common_rules["cut"]),
            "Route 225 - Item Across Lake Above House": (self.common_rules["surf"]),
            "Route 225 - Item on Northern Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 227 - Hidden Item Northeast of West Pond": (self.common_rules["rock_climb"]),
            "Route 227 - Item Next to East Pond": (self.common_rules["rock_climb"]),
            "Stark Mountain Exterior - Item on Southwest Hill": (self.common_rules["rock_climb"]),
            "Stark Mountain First Room - NE Item": (self.common_rules["rock_smash"]),
            "Stark Mountain First Room - Hidden Item Behind NE Item": (self.common_rules["rock_smash"]),
            "Stark Mountain Cavern - Item on Top of Central Rock Climb Hill": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Hidden Item Down SW Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Item in East Pit": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Item in NE Corner": (self.common_rules["rock_climb"]),
            "event_lake_explosion": (lambda state : state.has_all(["event_mine_badge", "HM04 Strength"], self.player)),
        }
        self.location_type_rules = {
            "hidden": (self.common_rules["dowsingmachine_if_opt"]),
            "uunown": (self.common_rules["dowsingmachine_if_opt"]),
        }
        self.encounter_type_rules = {
            "surf": (self.common_rules["surf"]),
            "good_rod": (lambda state : state.has_all(["Good Rod", "Bag"], self.player)),
            "super_rod": (lambda state : state.has_all(["Bag", "Super Rod"], self.player)),
            "old_rod": (lambda state : state.has_all(["Old Rod", "Bag"], self.player)),
        }

    def create_hm_rule(self, hm: Hm, player: int) -> Rule:
        mons = set()
        item_evols = []
        for name, spec in species.species.items():
            if hm not in spec.hms:
                continue
            mons.add(f"mon_{name}")
            while spec.pre_evolution:
                new_spec = species.species[spec.pre_evolution.species]
                if hm in new_spec.hms:
                    break
                if spec.pre_evolution.item:
                    item_evols.append([f"mon_{spec.pre_evolution.species}", spec.pre_evolution.item])
                else:
                    mons.add(f"mon_{spec.pre_evolution.species}")
                spec = new_spec
        bag = items.items["bag"].label
        def hm_rule(state: CollectionState) -> bool:
            if not (state.has_all([hm, bag], player) and self.common_rules[f"{hm.name.lower()}_badge"](state)):
                return False
            if state.has_any(mons, player):
                return True
            for item_evol in item_evols:
                if state.has_all(item_evol, player):
                    return True
            return False

        return hm_rule
