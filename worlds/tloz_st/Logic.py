from BaseClasses import MultiWorld, Item
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import SpiritTracksOptions

#TODO change locations to ST
def make_overworld_logic(player: int, origin_name: str, options: SpiritTracksOptions):
    overworld_logic = [



        # ====== Mercay Island ==============

        #[region 1, region 2, two-directional, logic requirements],
        ["aboda village", "aboda village rocks", False, None],
        #["aboda village", "aboda village stamp book", False, None],
        ["aboda village", "aboda village stamp station", False, None],
        ["aboda village", "aboda village bees", False, None],
        ["aboda village", "goal", False, None],


        # # ======== Mountain Passage =========

        # ["mercay island", "mercay passage 1", False, lambda state:
        #     any([st_can_cut_small_trees(state, player),
        #         st_has_small_keys(state, player, "Mountain Passage", 3),
        #         st_option_glitched_logic(state, player)  # Savewarp in back entrance / reverse cuccoo jump
        #          ])],
        # ["mercay island", "mercay passage 2", False, lambda state: st_can_reach_MP2(state, player)],
        # ["mercay passage 2", "mercay passage rat", False, lambda state: st_mercay_passage_rat(state, player)],


        # # ========== TotOK ===================
        # ["totok", "totok 1f chart chest", False, lambda state: any([
        #     st_has_small_keys(state, player, "Temple of the Ocean King", 1),
        #     st_ut_small_key_vanilla_location(state, player),
        #     st_totok_b1_all_checks_ut(state, player)
        # ])],
        # # B1
        # ["totok", "totok b1", False, lambda state: st_has_spirit(state, player, "Power")],
        # ["totok b1", "totok b1 eye chest", False, lambda state: all([st_has_grapple(state, player),
        #                                                              st_has_bow(state, player)])],
        # ["totok b1", "totok b1 stantom chest", False, lambda state: st_can_kill_stantoms(state, player)],
        # ["totok b1", "totok b1 key", False, lambda state: any([st_has_explosives(state, player),
        #                                                        st_has_grapple(state, player),
        #                                                        st_has_boomerang(state, player)])],
        # ["totok b1 key", "totok b2", False, lambda state: any([
        #     st_ut_small_key_vanilla_location(state, player),
        #     st_totok_b1_all_checks_ut(state, player)
        # ])],
        # ["totok b1", "totok b2", False, lambda state: st_has_small_keys(state, player, "Temple of the Ocean King", 2)],
        # # B2
        # ["totok b2", "totok b2 key", False, lambda state: st_totok_b2_key(state, player)],
        # ["totok b2", "totok b2 bombchu chest", False, lambda state: all([st_can_hit_bombchu_switches(state, player),
        #                                                                  st_has_explosives(state, player)])],
        # ["totok b2", "totok b2 stantom chest", False, lambda state: all([st_has_stantom_sword(state, player),
        #                                                                  any([st_can_hit_tricky_switches(state, player),
        #                                                                       st_has_explosives(state, player)])])],
        # ["totok b2 key", "totok b3", False, lambda state: any([
        #     st_ut_small_key_vanilla_location(state, player),
        #     st_totok_b2_all_checks_ut(state, player)
        # ])],
        # ["totok b2", "totok b3", False, lambda state: st_has_small_keys(state, player, "Temple of the Ocean King", 3)],
        # # B3
        # ["totok b3", "totok b3 stantom chest", False, lambda state: all([st_can_kill_stantoms_traps(state, player),
        #                                                                  st_has_grapple(state, player)])],
        # ["totok b3", "totok b3 locked chest", False, lambda state: any([
        #         st_has_small_keys(state, player, "Temple of the Ocean King", 4),
        #         st_ut_small_key_vanilla_location(state, player)])],  # UT
        # ["totok b3 locked chest", "totok b3.5", False, lambda state: st_is_ut(state, player)],  # UT ignores force gems
        # ["totok b3", "totok b3 bow chest", False, lambda state: st_has_bow(state, player)],
        # ["totok b3", "totok b3.5", False, lambda state: st_totok_b4_access(state, player)],
        # ["totok b3.5", "totok b4", False, lambda state: all([st_has_spirit(state, player, "Wisdom"),
        #                                                      st_can_hit_tricky_switches(state, player)])],
        # # B4
        # ["totok b4", "totok b4 stantom chest", False, lambda state: st_has_stantom_sword(state, player)],
        # ["totok b4", "totok b4 key", False, lambda state: any([st_has_explosives(state, player),
        #                                                        st_can_boomerang_return(state, player)])],
        # ["totok b4", "totok b5", False, lambda state: st_totok_b5_key_logic(state, player)],
        # ["totok b5", "totok b5 chest", False, lambda state: st_totok_b5(state, player)],
        # ["totok b5 chest", "totok b6", False, None],
        # ["totok b4", "totok b5.5", False, lambda state: all([st_totok_b5_key_logic(state, player),
        #                                                      st_can_hit_bombchu_switches(state, player)])],
        # ["totok b5.5", "totok b5.5 chest", False, lambda state: st_has_shovel(state, player)],
        # ["totok b5.5", "totok b6", False, None],
        # # B6
        # ["totok b6", "totok b6 stantom chest", False, lambda state: st_has_stantom_sword(state, player)],
        # ["totok b6", "totok b6 bow chest", False, lambda state: st_has_bow(state, player)],
        # ["totok b6", "totok b6 cc", False, lambda state: st_has_sea_chart(state, player, "SW")],
        # ["totok b6", "totok midway", False, lambda state: st_has_triforce_crest(state, player)],

        # # ============ TotOK Part 2 =====================

        # # B7
        # ["totok midway", "totok b7", False, lambda state: st_has_spirit(state, player, "Courage")],
        # ["totok b7", "totok b8", False, None],
        # ["totok b7", "totok b7 east", False, lambda state: st_has_grapple(state, player)],
        # ["totok b7 east", "totok b7 peg", False, lambda state: st_has_range(state, player)],
        # ["totok b7", "totok b7 stantom", False, lambda state: st_can_kill_stantoms(state, player)],
        # # B8
        # ["totok b8", "totok b7 east", False, lambda state: st_can_hit_switches(state, player)],
        # ["totok b8", "totok b9 nw", False, lambda state: any([
        #     st_has_totok_crystal(state, player, "Round"),
        #     st_has_hammer(state, player)])],
        # ["totok b7 east", "totok b9 nw", False, lambda state: st_is_ut(state, player)],  # UT Bypass
        # ["totok b8", "totok b8 stantom", False, lambda state: st_can_kill_stantoms(state, player)],
        # ["totok b8", "totok b8 2 crystals", False, lambda state: st_totok_b8_2_crystals(state, player)],
        # ["totok b8", "totok b9", False, lambda state: st_totok_b9(state, player)],  # Includes UT
        # # B9
        # ["totok b9", "totok b9 ghosts", False, lambda state: st_can_hit_switches(state, player)],
        # ["totok b9", "totok b9 nw", False, lambda state: st_totok_b9_stantom_square(state, player)],
        # ["totok b9", "totok b9 stantom", False, lambda state: st_totok_b9_stantom_kill(state, player)],
        # ["totok b9", "totok b9.5", False, lambda state: st_totok_b95(state, player)],  # UT Crystals
        # ["totok b9.5", "totok b10", False, None],
        # # B10
        # ["totok b10", "totok b10 inner", False, lambda state: st_has_explosives(state, player)],
        # ["totok b10 inner", "totok b10 hammer", False, lambda state: st_has_hammer(state, player)],
        # ["totok b10 inner", "totok b10 stantom", False, lambda state: st_can_kill_stantoms_traps(state, player)],
        # ["totok b10 inner", "totok b10 stantom eyes", False, lambda state: st_has_grapple(state, player)],
        # ["totok b10 inner", "totok b11", False, lambda state: st_totok_b10_key_logic(state, player)],
        # # B11
        # ["totok b11", "totok b11 stantom", False, lambda state: st_has_stantom_sword(state, player)],
        # ["totok b11", "totok b12", False, lambda state: st_totok_b12(state, player)],
        # # B12
        # ["totok b12", "totok b12 hammer", False, lambda state: st_has_hammer(state, player)],
        # ["totok b12", "totok b12 stantom", False, lambda state: st_has_stantom_sword(state, player)],
        # ["totok b12", "totok b13", False, lambda state: st_totok_b12_force_gems(state, player)],  # UT Force gems

        # # B13
        # ["totok b13", "totok before bellum", False, lambda state: st_totok_b13_door(state, player)],
        # ["totok", "totok before bellum", False, lambda state: st_totok_blue_warp(state, player)],
        # # Bellum
        # ["totok", "bellum 1", False, lambda state: st_totok_bellum_staircase(state, player)],
        # ["bellum 1", "ghost ship fight", False, lambda state: st_can_beat_bellum(state, player)],
        # ["ghost ship fight", "bellumbeck", False, lambda state: st_can_beat_ghost_ship_fight(state, player)],


        # # ============ Shops ====================

        # ["mercay island", "shop power gem", False, lambda state: st_can_buy_gem(state, player)],
        # ["mercay island", "shop quiver", False, lambda state: st_can_buy_quiver(state, player)],
        # ["mercay island", "shop bombchu bag", False, lambda state: st_can_buy_chu_bag(state, player)],
        # ["mercay island", "shop heart container", False, lambda state: st_can_buy_heart(state, player)],

        # # ============ SW Ocean =================

        # ["mercay island", "sw ocean east", False, lambda state: st_boat_access(state, player)],
        # ["sw ocean east", "cannon island", False, None],
        # ["sw ocean east", "ember island", False, None],
        # ["sw ocean east", "sw ocean crest salvage", False, lambda state: st_salvage_courage_crest(state, player)],
        # ["sw ocean east", "sw ocean west", False, lambda state: st_can_enter_ocean_sw_west(state, player)],
        # ["sw ocean west", "molida island", False, None],
        # ["sw ocean west", "spirit island", False, None],
        # ["sw ocean west", "sw ocean nyave", False, lambda state: any([st_has_cave_damage(state, player),
        #                                                               st_clever_pots(state, player)])],
        # ["sw ocean nyave", "sw ocean nyave trade", False, lambda state: st_has_guard_notebook(state, player)],
        # ["sw ocean west", "sw ocean frog sti", False, lambda state: st_has_cannon(state, player)],
        # ["sw ocean east", "sw ocean frog x", False, lambda state: st_has_cannon(state, player)],

        # # ============ Cannon Island ===============

        # ["cannon island", "cannon island salvage arm", False, lambda state: st_has_courage_crest(state, player)],
        # ["cannon island", "cannon island dig", False, lambda state: st_has_shovel(state, player)],

        # # =============== Temple of Fire =================

        # ["tof 1f", "tof 1f keese", False, lambda state: st_can_kill_bat(state, player)],
        # ["tof 1f", "tof 1f maze", False, lambda state: any([
        #     st_has_small_keys(state, player, "Temple of Fire", 1),
        #     st_tof_1f_key_ut(state, player)])],
        # ["tof 1f maze", "tof 2f", False, lambda state: st_can_hit_spin_switches(state, player)],
        # # 2F
        # ["tof 2f", "tof 1f west", False, lambda state: st_has_short_range(state, player)],
        # ["tof 1f west", "tof 1f sw", False, lambda state: st_spiral_wall_switches(state, player)],
        # ["tof 1f sw", "tof 2f south", False, lambda state: st_can_kill_bubble(state, player)],
        # ["tof 2f south", "tof 3f", False, lambda state: st_tof_3f(state, player)],
        # # 3F
        # ["tof 3f", "tof 3f key drop", False, lambda state: st_has_boomerang(state, player)],
        # ["tof 3f key drop", "tof 3f boss key", False, lambda state:
        #     any([st_has_small_keys(state, player, "Temple of Fire", 3),
        #          st_ut_small_key_own_dungeon(state, player)])],  # All 3F checks need boomerang, UT included
        # ["tof 3f boss key", "tof blaaz", False, lambda state: all([
        #     st_has_sword(state, player),
        #     st_has_boss_key_simple(state, player, "Temple of Fire")])],  # Includes UT
        # ["tof blaaz", "post tof", False, None],

        # # =============== Temple of Courage ================

        # ["toc", "toc bomb alcove", False, lambda state: st_has_explosives(state, player)],
        # ["toc", "toc b1", False, lambda state: st_toc_key_door_1(state, player)],
        # ["toc", "toc hammer clips", False, lambda state: st_can_hammer_clip(state, player)],
        # ["toc b1", "toc b1 grapple", False, lambda state: any([st_has_grapple(state, player),
        #                                                        st_can_boomerang_return(state, player)])],
        # ["toc b1", "toc 1f west", False, lambda state: st_has_explosives(state, player)],
        # ["toc b1 grapple", "toc 1f west", False, lambda state: st_has_bow(state, player)],
        # ["toc hammer clips", "toc 1f west", False, None],
        # ["toc 1f west", "toc map room", False, lambda state: st_has_explosives(state, player)],
        # ["toc 1f west", "toc 2f beamos", False, lambda state: st_toc_key_door_2(state, player)],
        # ["toc 1f west", "toc b1 maze", False, lambda state:
        #     st_has_shape_crystal(state, player, "Temple of Courage", "Square")],
        # ["toc 2f beamos", "toc b1 maze", False, lambda state: st_is_ut(state, player)],  # UT Crystal
        # ["toc 2f beamos", "toc south 1f", False, lambda state: all([st_is_ut(state, player),
        #                                                             st_has_bow(state, player)])],
        # ["toc b1 grapple", "toc b1 maze", False, None],
        # ["toc b1 maze", "toc south 1f", False, lambda state: all([
        #     st_has_bow(state, player),
        #     st_has_shape_crystal(state, player, "Temple of Courage", "Square")])],

        # ["toc south 1f", "toc 2f spike corridor", False, lambda state: st_has_explosives(state, player)],
        # ["toc 2f spike corridor", "toc 2f platforms", False, lambda state: all([st_has_explosives(state, player),
        #                                                                         st_has_bow(state, player)])],
        # ["toc hammer clips", "toc 2f spike corridor", False, None],
        # ["toc south 1f", "toc 2f platforms", False, lambda state: st_has_bow(state, player)],
        # ["toc 2f spike corridor", "toc torches", False, lambda state: st_has_boomerang(state, player)],
        # ["toc torches", "toc torches chest", False, lambda state: st_has_bow(state, player)],
        # ["toc torches", "toc pols 2", False, lambda state: st_toc_final_switch_state(state, player)],
        # ["toc pols 2", "toc bk room", False, lambda state: st_toc_key_door_3(state, player)],
        # ["toc bk room", "toc bk chest", False, lambda state: st_has_bow(state, player)],
        # ["toc bk room", "toc before boss", False, lambda state: st_has_boss_key(state, player, "Temple of Courage")],
        # ["toc bk chest", "toc before boss", False, lambda state:
        #     st_has_boss_key_simple(state, player, "Temple of Courage")],
        # ["toc before boss", "toc before boss chest", False, lambda state: st_has_explosives(state, player)],
        # ["toc before boss", "toc crayk", False, lambda state: st_has_bow(state, player)],

        # # ============ Ocean NW ===============
        # ["sw ocean west", "nw ocean", False, lambda state: st_has_sea_chart(state, player, "NW")],
        # ["sw ocean east", "nw ocean", False, lambda state: st_has_frog_n(state, player)],
        # ["nw ocean", "nw ocean frog n", False, lambda state: st_has_cannon(state, player)],
        # ["nw ocean", "gust", False, None],
        # ["nw ocean", "bannan", False, None],
        # ["nw ocean", "zauz", False, None],
        # ["nw ocean", "uncharted", False, None],
        # ["nw ocean", "ghost ship", False, lambda state: st_has_ghost_ship_access(state, player)],
        # ["nw ocean", "porl", False, None],
        # ["porl", "porl item", False, lambda state: st_has_sword(state, player)],
        # ["porl", "porl trade", False, lambda state: st_has_heros_new_clothes(state, player)],

        # # ================= Temple of Wind ====================

        # ["tow", "tow b1", False, lambda state: any([
        #     st_can_hammer_clip(state, player),
        #     st_can_kill_bat(state, player)])],
        # ["tow b1", "tow b2", False, None],
        # ["tow b2", "tow b2 dig", False, lambda state: st_has_shovel(state, player)],
        # ["tow b2", "tow b2 bombs", False, lambda state: st_has_explosives(state, player)],
        # ["tow b2", "tow b2 key", False, lambda state: any([
        #     st_has_small_keys(state, player, "Temple of Wind"),
        #     st_wind_temple_key_ut(state, player)])],
        # ["tow b2", "tow bk chest", False, lambda state: st_has_bombs(state, player)],
        # ["tow", "tow cyclok", False, lambda state: all([
        #     st_has_bombs(state, player),
        #     st_has_boss_key_simple(state, player, "Temple of Wind")])],
        # ["tow cyclok", "post tow", False, None],


        # # ================= SE Ocean ====================

        # ["sw ocean", "se ocean", False, lambda state: all([
        #     st_has_sea_chart(state, player, "SE"),
        #     st_has_sea_chart(state, player, "SW")])],
        # ["se ocean", "se ocean frogs", False, lambda state: st_has_cannon(state, player)],
        # ["se ocean", "goron", False, lambda state: st_has_cannon(state, player)],
        # ["se ocean", "se ocean trade", False, lambda state: st_has_kaleidoscope(state, player)],
        # ["se ocean", "iof", False, lambda state: st_has_cannon(state, player)],
        # ["se ocean", "harrow", False, lambda state: st_has_sword(state, player)],
        # ["se ocean", "ds", False, None],
        # ["se ocean", "pirate ambush", False, lambda state: st_beat_ghost_ship(state, player)],

        # # ================= Goron Island ====================

        # ["goron", "goron chus", False, lambda state: st_goron_chus(state, player)],
        # ["goron", "goron grapple", False, lambda state: st_has_grapple(state, player)],
        # ["goron chus", "goron quiz", False, None],
        # ["goron", "goron north", False, None],
        # ["goron north", "goron north bombchu", False, lambda state: st_can_hit_bombchu_switches(state, player)],
        # ["goron north", "goron outside temple", False, lambda state: st_has_explosives(state, player)],
        # ["goron", "goron outside temple", False, lambda state: st_can_hammer_clip(state, player)],
        # ["goron outside temple", "goron north", False, lambda state: st_has_bombs(state, player)],
        # ["goron outside temple", "gt", False, lambda state: st_has_shovel(state, player)],
        # ["gt dongo", "goron chief 2", False, None],


        # # ================= Goron Temple ====================
        # ["gt", "gt bow", False, lambda state: st_has_bow(state, player)],
        # ["gt", "gt b1", False, lambda state: all([st_has_explosives(state, player),
        #                                           st_can_kill_eye_brute(state, player)])],
        # ["gt", "gt b2", False, lambda state: st_can_hit_bombchu_switches(state, player)],
        # ["gt b2", "gt b3", False, None],
        # ["gt b2", "gt b2 back", False, lambda state: any([
        #     st_has_explosives(state, player),
        #     st_has_boomerang(state, player)])],
        # ["gt b2 back", "gt bk chest", False, lambda state: st_has_chus(state, player)],
        # ["gt b2", "gt dongo", False, lambda state: all([
        #     st_has_chus(state, player),
        #     st_has_boss_key_simple(state, player, "Goron Temple")])],

        # # ================= Harrow Island ====================

        # ["harrow", "harrow dig", False, lambda state: st_has_shovel(state, player)],
        # ["harrow dig", "harrow dig 2", False, lambda state: st_has_sea_chart(state, player, "NE")],

        # # ================= Dee Ess Island ====================

        # ["ds", "ds dig", False, lambda state: st_has_shovel(state, player)],
        # ["ds", "ds combat", False, lambda state: st_can_kill_eye_brute(state, player)],
        # ["gt dongo", "ds race", False, None],

        # # ================= Isle of Frost ====================

        # ["iof", "iof grapple", False, lambda state: st_has_grapple(state, player)],
        # ["iof", "iof dig", False, lambda state: st_has_shovel(state, player)],
        # ["iof grapple", "iof grapple dig", False, lambda state: st_has_shovel(state, player)],
        # ["iof", "iof yook", False, lambda state: st_has_damage(state, player)],
        # ["iof yook", "toi", False, None],

        # # ================= Ice Temple ====================

        # ["toi", "toi 2f", False, lambda state: any([
        #     st_has_explosives(state, player),
        #     st_has_boomerang(state, player)])],
        # ["toi 2f", "toi 3f", False, lambda state: any([
        #     st_has_range(state, player),
        #     st_has_bombs(state, player)])],
        # ["toi 3f", "toi 3f switch", False, lambda state: st_has_explosives(state, player)],
        # ["toi 3f switch", "toi 3f boomerang", False, lambda state: st_toi_3f_boomerang(state, player)],
        # ["toi 3f boomerang", "toi 2f miniboss", False, lambda state: st_toi_key_door_1_ut(state, player)],
        # ["toi 3f", "toi 2f miniboss", False, lambda state: st_toi_key_doors(state, player, 3, 1)],
        # ["toi 2f miniboss", "toi side path", False, lambda state: st_has_grapple(state, player)],
        # ["toi", "toi side path", False, lambda state: all([
        #     st_can_hammer_clip(state, player),
        #     st_has_grapple(state, player)])],
        # ["toi side path", "toi b1", False, lambda state: any([
        #     st_has_explosives(state, player),
        #     st_has_hammer(state, player)
        # ])],
        # ["toi b1", "toi b1 2", False, lambda state: st_has_explosives(state, player)],
        # ["toi b1 2", "toi b1 key", False, lambda state: st_toi_key_door_2(state, player)],
        # ["toi b1 2", "toi b2", False, lambda state: st_toi_b2(state, player)],
        # ["toi b2", "toi bk chest", False, lambda state: st_can_hammer_clip(state, player)],
        # ["toi b2", "toi b2 key", False, lambda state: st_toi_key_door_3(state, player)],
        # ["toi b2 key", "toi bk chest", False, None],
        # ["toi bk chest", "toi gleeok", False, lambda state: st_is_ut(state, player)],
        # ["toi b2", "toi gleeok", False, lambda state: st_has_boss_key(state, player, "Temple of Ice")],

        # # ================= NE Ocean ====================

        # ["sw ocean", "ne ocean", False, lambda state: st_has_frog_square(state, player)],
        # ["se ocean", "ne ocean", False, lambda state: st_has_sea_chart(state, player, "NE")],
        # ["ne ocean", "ne ocean frog", False, lambda state: st_has_cannon(state, player)],
        # ["ne ocean", "ne ocean combat", False, lambda state: st_can_kill_blue_chu(state, player)],
        # ["ne ocean", "iotd", False, None],
        # ["ne ocean", "maze", False, lambda state: st_has_sword(state, player)],
        # ["ne ocean", "ruins", False, lambda state: all([st_has_regal_necklace(state, player),
        #                                                 st_has_cave_damage(state, player)])],
        # ["ne ocean", "pirate ambush", False, lambda state: st_beat_ghost_ship(state, player)],

        # # ================= IotD ====================

        # ["iotd", "iotd rupoor", False, lambda state: st_has_bombs(state, player)],
        # ["iotd", "iotd dig", False, lambda state: st_has_shovel(state, player)],
        # ["iotd dig", "iotd cave", False, lambda state: st_has_bombs(state, player)],

        # # ================= Isle of Ruins ====================

        # ["ruins", "ruins dig", False, lambda state: st_has_shovel(state, player)],
        # ["ruins", "ruins water", False, lambda state: st_has_kings_key(state, player)],
        # ["ruins water", "mutoh", False, None],

        # # ================= Mutoh's Temple ====================

        # ["mutoh", "mutoh hammer", False, lambda state: st_has_hammer(state, player)],
        # ["mutoh hammer", "mutoh water", False, lambda state: st_mutoh_water(state, player)],
        # ["mutoh water", "mutoh bk chest", False, lambda state: any([
        #     st_has_small_keys(state, player, "Mutoh's Temple", 2),
        #     st_ut_small_key_own_dungeon(state, player)])],
        # ["mutoh water", "mutoh eox", False, lambda state: st_has_boss_key(state, player, "Mutoh's Temple")],
        # ["mutoh bk chest", "mutoh eox", False, lambda state: st_is_ut(state, player)],


        # # ================= Maze Island ====================

        # ["maze", "maze east", False, lambda state: st_has_explosives(state, player)],
        # ["maze", "maze normal", False, lambda state: st_has_bow(state, player)],
        # ["maze normal", "maze expert", False, lambda state: st_has_grapple(state, player)],
        # ["maze", "maze dig", False, lambda state: st_has_shovel(state, player)],

        # # Goal stuff
        # ["mercay island", "beat required dungeons", False, lambda state: st_beat_required_dungeons(state, player)],
        # ["sw ocean east", "bellumbeck", False, lambda state: st_bellumbeck_quick_finish(state, player)],
        # ["bellumbeck", "beat bellumbeck", False, lambda state: st_can_beat_bellumbeck(state, player)],
        # ["beat bellumbeck", "goal", False, lambda state: st_option_goal_bellum(state, player)],
        # ["totok midway", "goal", False, lambda state: st_option_goal_midway(state, player)]

    ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name


def create_connections(multiworld: MultiWorld, player: int, origin_name: str, options):
    all_logic = [
        make_overworld_logic(player, origin_name, options)
    ]

    # Create connections
    for logic_array in all_logic:
        for entrance_desc in logic_array:
            region_1 = multiworld.get_region(entrance_desc[0], player)
            region_2 = multiworld.get_region(entrance_desc[1], player)
            is_two_way = entrance_desc[2]
            rule = entrance_desc[3]

            region_1.connect(region_2, None, rule)
            if is_two_way:
                region_2.connect(region_1, None, rule)
