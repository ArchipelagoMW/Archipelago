from BaseClasses import MultiWorld, Item
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import PhantomHourglassOptions


def make_overworld_logic(player: int, origin_name: str, options: PhantomHourglassOptions):
    overworld_logic = [

        # ====== Mercay Island ==============

        ["mercay island", "mercay dig spot", False, lambda state: ph_has_shovel(state, player)],
        ["mercay island", "mercay zora cave", False, lambda state: ph_has_explosives(state, player)],
        ["mercay zora cave", "mercay zora cave south", False, lambda state: ph_has_bow(state, player)],
        ["mercay island", "mercay zora cave south", False, lambda state: ph_can_sword_scroll_clip(state, player)],
        ["mercay island", "totok", False, None],
        ["mercay island", "mercay freedle island", False, lambda state: ph_has_explosives(state, player)],
        ["mercay freedle island", "mercay freedle tunnel chest", False, lambda state: ph_has_range(state, player)],
        ["mercay freedle island", "mercay freedle gift", False, lambda state: ph_has_sea_chart(state, player, "SE")],
        ["mercay island", "mercay yellow guy", False, lambda state: ph_has_courage_crest(state, player)],
        ["post tow", "mercay oshus gem", False, None],
        ["mercay island", "mercay oshus phantom blade", False, lambda state: ph_has_phantom_blade(state, player)],
        ["mercay oshus phantom blade", "mercay oshus gem", False, None],
        ["mercay island", "sw ocean", False, lambda state: ph_has_sea_chart(state, player, "SW")],

        # ======== Mountain Passage =========

        ["mercay island", "mercay passage 1", False, lambda state:
        any([ph_can_cut_small_trees(state, player),
             ph_has_small_keys(state, player, "Mountain Passage", 3),
             ph_option_glitched_logic(state, player)  # Savewarp in back entrance / reverse cuccoo jump
             ])],
        ["mercay island", "mercay passage 2", False, lambda state: ph_can_reach_MP2(state, player)],
        ["mercay passage 2", "mercay passage rat", False, lambda state: ph_mercay_passage_rat(state, player)],

        # ========== TotOK ===================
        ["totok", "totok 1f", False, lambda state: ph_totok_1f(state, player)],

        ["totok 1f", "totok 1f chest", False, lambda state: ph_totok_1f_chest(state, player)],
        ["totok 1f", "totok 1f chart", False, lambda state: ph_totok_1f_chart(state, player)],
        ["totok 1f", "totok b1", False, lambda state: ph_totok_b1(state, player)],

        ["totok b1", "totok b1 key", False, lambda state: ph_totok_b1_key(state, player)],
        ["totok b1", "totok b1 phantom", False, lambda state: ph_totok_b1_phantom(state, player)],
        ["totok b1", "totok b1 bow", False, lambda state: ph_totok_b1_bow(state, player)],
        ["totok b1", "totok b2", False, lambda state: ph_totok_b2(state, player)],

        ["totok b2", "totok b2 key", False, lambda state: ph_totok_b2_key(state, player)],
        ["totok b2", "totok b2 phantom", False, lambda state: ph_totok_b2_phantom(state, player)],
        ["totok b2", "totok b2 chu", False, lambda state: ph_totok_b2_chu(state, player)],
        ["totok b2", "totok b3", False, lambda state: ph_totok_b3(state, player)],

        ["totok b3", "totok b3 nw", False, lambda state: ph_totok_b3_nw(state, player)],
        ["totok b3", "totok b3 se", False, lambda state: ph_totok_b3_se(state, player)],
        ["totok b3", "totok b3 sw", False, lambda state: ph_totok_b3_sw(state, player)],
        ["totok b3", "totok b3 bow", False, lambda state: ph_totok_b3_bow(state, player)],
        ["totok b3", "totok b3 key", False, lambda state: ph_totok_b3_key(state, player)],
        ["totok b3", "totok b3 phantom", False, lambda state: ph_totok_b3_phantom(state, player)],
        ["totok b3", "totok b35", False, lambda state: ph_totok_b35(state, player)],

        ["totok b35", "totok b4", False, lambda state: ph_totok_b4(state, player)],
        ["totok b4", "totok b4 key", False, lambda state: ph_totok_b4_key(state, player)],
        ["totok b4", "totok b4 eyes", False, lambda state: ph_totok_b4_eyes(state, player)],
        ["totok b4", "totok b4 phantom", False, lambda state: ph_totok_b4_phantom(state, player)],
        ["totok b4", "totok b5", False, lambda state: ph_totok_b5(state, player)],
        ["totok b4", "totok b5 alt", False, lambda state: ph_totok_b5_alt(state, player)],

        ["totok b5", "totok b5 chest", False, lambda state: ph_totok_b5_chest(state, player)],
        ["totok b5", "totok b6", False, lambda state: ph_totok_b6(state, player)],
        ["totok b5 alt", "totok b5 alt chest", False, lambda state: ph_totok_b5_alt_chest(state, player)],
        ["totok b5 alt", "totok b6", False, lambda state: ph_totok_b6(state, player)],

        ["totok b6", "totok b6 bow", False, lambda state: ph_totok_b6_bow(state, player)],
        ["totok b6", "totok b6 phantom", False, lambda state: ph_totok_b6_phantom(state, player)],
        ["totok b6", "totok b6 crest", False, lambda state: ph_totok_b6_crest(state, player)],
        ["totok b6", "totok midway", False, lambda state: ph_totok_b7(state, player)],
        ["totok midway", "totok b7", False, lambda state: ph_has_spirit(state, player, "Courage")],

        ["totok b7", "totok b7 crystal", False, lambda state: ph_totok_b7_crystal(state, player)],
        ["totok b7", "totok b7 switch", False, lambda state: ph_totok_b7_switch_chest(state, player)],
        ["totok b7", "totok b8", False, lambda state: ph_totok_b8(state, player)],

        ["totok b8", "totok b8 phantom", False, lambda state: ph_totok_b8_phantom(state, player)],
        ["totok b8", "totok b9", False, lambda state: ph_totok_b9(state, player)],
        ["totok b8", "totok b8 2c chest", False, lambda state: ph_totok_b8_2_crystal_chest(state, player)],
        ["totok b8", "totok b7 phantom", False, lambda state: ph_totok_b7_phantom(state, player)],
        ["totok b8", "totok b9 corner chest", False, lambda state: ph_totok_b9_corner_chest(state, player)],

        ["totok b9", "totok b9 phantom", False, lambda state: ph_totok_b9_phantom(state, player)],
        ["totok b9", "totok b9 ghosts", False, lambda state: ph_totok_b9_ghosts(state, player)],

        ["totok b9", "totok b10", False, lambda state: ph_totok_b10(state, player)],

        ["totok b10", "totok b10 key", False, lambda state: ph_totok_b10_key(state, player)],
        ["totok b10", "totok b10 phantom", False, lambda state: ph_totok_b10_phantom(state, player)],
        ["totok b10", "totok b10 eye", False, lambda state: ph_totok_b10_eye(state, player)],
        ["totok b10", "totok b10 hammer", False, lambda state: ph_totok_b10_hammer(state, player)],
        ["totok b10", "totok b11", False, lambda state: ph_totok_b11(state, player)],

        ["totok b11", "totok b11 phantom", False, lambda state: ph_totok_b11_phantom(state, player)],
        ["totok b11", "totok b11 eyes", False, lambda state: ph_totok_b11_eyes(state, player)],
        ["totok b11", "totok b12", False, lambda state: ph_totok_b12(state, player)],

        ["totok b12", "totok b12 nw", False, lambda state: ph_totok_b12_nw(state, player)],
        ["totok b12", "totok b12 ne", False, lambda state: ph_totok_b12_ne(state, player)],
        ["totok b12", "totok b12 phantom", False, lambda state: ph_totok_b12_phantom(state, player)],
        ["totok b12", "totok b12 ghost", False, lambda state: ph_totok_b12_ghost(state, player)],
        ["totok b12", "totok b12 hammer", False, lambda state: ph_totok_b12_hammer(state, player)],
        ["totok b12", "totok b13", False, lambda state: ph_totok_b13(state, player)],

        ["totok b13", "totok b13 chest", False, lambda state: ph_totok_b13_chest(state, player)],
        ["totok b13", "totok before bellum", False, lambda state: ph_totok_b13_door(state, player)],
        ["totok", "totok before bellum", False, lambda state: ph_totok_blue_warp(state, player)],
        # Bellum
        ["totok before bellum", "bellum 1", False, lambda state: ph_totok_bellum_staircase(state, player)],
        ["bellum 1", "ghost ship fight", False, lambda state: ph_can_beat_bellum(state, player)],
        ["ghost ship fight", "bellumbeck", False, lambda state: ph_can_beat_ghost_ship_fight(state, player)],

        # ============ Shops ====================

        ["mercay island", "shop power gem", False, lambda state: ph_can_buy_gem(state, player)],
        ["mercay island", "shop quiver", False, lambda state: ph_can_buy_quiver(state, player)],
        ["mercay island", "shop bombchu bag", False, lambda state: ph_can_buy_chu_bag(state, player)],
        ["mercay island", "shop heart container", False, lambda state: ph_can_buy_heart(state, player)],

        ["sw ocean east", "beedle", False, None],
        ["beedle", "beedle gem", False, lambda state: ph_beedle_shop(state, player, 500)],
        ["beedle", "beedle bomb bag", False, lambda state: all([ph_beedle_shop(state, player, 500),
                                                                ph_has_bombs(state, player)])],
        ["beedle", "masked ship gem", False, lambda state: ph_beedle_shop(state, player, 500)],
        ["beedle", "masked ship hc", False, lambda state: ph_beedle_shop(state, player, 500)],

        ["beedle", "beedle bronze", False, lambda state: any([ph_has_rupees(state, player, 80),
                                                              ph_has_beedle_points(state, player, 1)])],
        ["beedle", "beedle silver", False, lambda state: ph_has_beedle_points(state, player, 20)],
        ["beedle", "beedle gold", False, lambda state: ph_has_beedle_points(state, player, 50)],
        ["beedle", "beedle plat", False, lambda state: ph_has_beedle_points(state, player, 100)],
        ["beedle", "beedle vip", False, lambda state: ph_has_beedle_points(state, player, 200)],


        # ============ SW Ocean =================

        ["mercay island", "sw ocean east", False, lambda state: ph_boat_access(state, player)],
        ["sw ocean east", "cannon island", False, None],
        ["sw ocean east", "ember island", False, None],
        ["sw ocean east", "sw ocean crest salvage", False, lambda state: ph_salvage_courage_crest(state, player)],
        ["sw ocean east", "sw ocean west", False, lambda state: ph_can_enter_ocean_sw_west(state, player)],
        ["sw ocean west", "molida island", False, None],
        ["sw ocean west", "spirit island", False, None],
        ["sw ocean west", "sw ocean nyave", False, lambda state: any([ph_has_cave_damage(state, player),
                                                                      ph_clever_pots(state, player)])],
        ["sw ocean nyave", "sw ocean nyave trade", False, lambda state: ph_has_guard_notebook(state, player)],
        ["sw ocean west", "sw ocean frog phi", False, lambda state: ph_has_cannon(state, player)],
        ["sw ocean east", "sw ocean frog x", False, lambda state: ph_has_cannon(state, player)],

        # ============ Cannon Island ===============

        ["cannon island", "cannon island salvage arm", False, lambda state: ph_has_courage_crest(state, player)],
        ["cannon island", "cannon island dig", False, lambda state: ph_has_shovel(state, player)],

        # =============== Isle of Ember ================

        ["ember island", "ember island dig", False, lambda state: ph_has_shovel(state, player)],
        ["ember island", "ember island grapple", False, lambda state: any([
            ph_has_grapple(state, player),
            ph_can_sword_glitch(state, player)])],
        ["ember island", "tof 1f", False, None],

        # =============== Temple of Fire =================

        ["tof 1f", "tof 1f keese", False, lambda state: ph_can_kill_bat(state, player)],
        ["tof 1f", "tof 1f maze", False, lambda state: any([
            ph_has_small_keys(state, player, "Temple of Fire", 1),
            ph_tof_1f_key_ut(state, player)])],
        ["tof 1f maze", "tof 2f", False, lambda state: ph_can_hit_spin_switches(state, player)],
        # 2F
        ["tof 2f", "tof 1f west", False, lambda state: ph_has_short_range(state, player)],
        ["tof 1f west", "tof 1f sw", False, lambda state: ph_spiral_wall_switches(state, player)],
        ["tof 1f sw", "tof 2f south", False, lambda state: ph_can_kill_bubble(state, player)],
        ["tof 2f south", "tof 3f", False, lambda state: ph_tof_3f(state, player)],
        # 3F
        ["tof 3f", "tof 3f key drop", False, lambda state: ph_has_boomerang(state, player)],
        ["tof 3f key drop", "tof 3f boss key", False, lambda state:
        any([ph_has_small_keys(state, player, "Temple of Fire", 3),
             ph_ut_small_key_own_dungeon(state, player)])],  # All 3F checks need boomerang, UT included
        ["tof 3f boss key", "tof blaaz", False, lambda state: all([
            ph_has_sword(state, player),
            ph_has_boss_key_simple(state, player, "Temple of Fire")])],  # Includes UT
        ["tof blaaz", "post tof", False, None],

        # =========== Molida Island ===============

        ["molida island", "molida dig", False, lambda state: ph_has_shovel(state, player)],
        ["molida island", "molida grapple", False, lambda state: ph_has_grapple(state, player)],
        ["molida island", "molida cave back", False, lambda state: ph_has_cave_damage(state, player)],
        ["molida cave back", "molida cave back dig", False, lambda state: ph_has_shovel(state, player)],
        ["molida cave back dig", "molida cuccoo dig", False, lambda state: ph_has_grapple(state, player)],
        ["molida dig", "molida north", False, lambda state: ph_has_sun_key(state, player)],
        ["molida north", "molida north grapple", False, lambda state: ph_has_grapple(state, player)],
        ["molida north", "toc", False, lambda state: ph_can_enter_toc(state, player)],
        ["toc crayk", "post toc", False, None],
        ["post toc", "molida archery", False, None],

        # =============== Temple of Courage ================

        ["toc", "toc bomb alcove", False, lambda state: ph_has_explosives(state, player)],
        ["toc", "toc b1", False, lambda state: ph_toc_key_door_1(state, player)],
        ["toc", "toc hammer clips", False, lambda state: ph_can_hammer_clip(state, player)],
        ["toc b1", "toc b1 grapple", False, lambda state: any([ph_has_grapple(state, player),
                                                               ph_can_boomerang_return(state, player)])],
        ["toc b1", "toc 1f west", False, lambda state: ph_has_explosives(state, player)],
        ["toc b1 grapple", "toc 1f west", False, lambda state: ph_has_bow(state, player)],
        ["toc hammer clips", "toc 1f west", False, None],
        ["toc 1f west", "toc map room", False, lambda state: ph_has_explosives(state, player)],
        ["toc 1f west", "toc 2f beamos", False, lambda state: ph_toc_key_door_2(state, player)],
        ["toc 1f west", "toc b1 maze", False, lambda state:
        ph_has_shape_crystal(state, player, "Temple of Courage", "Square")],
        ["toc 2f beamos", "toc b1 maze", False, lambda state: ph_is_ut(state, player)],  # UT Crystal
        ["toc 2f beamos", "toc south 1f", False, lambda state: all([ph_is_ut(state, player),
                                                                    ph_has_bow(state, player)])],
        ["toc b1 grapple", "toc b1 maze", False, None],
        ["toc b1 maze", "toc south 1f", False, lambda state: all([
            ph_has_bow(state, player),
            ph_has_shape_crystal(state, player, "Temple of Courage", "Square")])],

        ["toc south 1f", "toc 2f spike corridor", False, lambda state: ph_has_explosives(state, player)],
        ["toc 2f spike corridor", "toc 2f platforms", False, lambda state: all([ph_has_explosives(state, player),
                                                                                ph_has_bow(state, player)])],
        ["toc hammer clips", "toc 2f spike corridor", False, None],
        ["toc south 1f", "toc 2f platforms", False, lambda state: ph_has_bow(state, player)],
        ["toc 2f spike corridor", "toc torches", False, lambda state: ph_has_boomerang(state, player)],
        ["toc torches", "toc torches chest", False, lambda state: ph_has_bow(state, player)],
        ["toc torches", "toc pols 2", False, lambda state: ph_toc_final_switch_state(state, player)],
        ["toc pols 2", "toc bk room", False, lambda state: ph_toc_key_door_3(state, player)],
        ["toc bk room", "toc bk chest", False, lambda state: ph_has_bow(state, player)],
        ["toc bk room", "toc before boss", False, lambda state: ph_has_boss_key(state, player, "Temple of Courage")],
        ["toc bk chest", "toc before boss", False, lambda state:
        ph_has_boss_key_simple(state, player, "Temple of Courage")],
        ["toc before boss", "toc before boss chest", False, lambda state: ph_has_explosives(state, player)],
        ["toc before boss", "toc crayk", False, lambda state: ph_has_bow(state, player)],

        # ================ Spirit Island =====================

        ["spirit island", "spirit island gauntlet", False, lambda state: ph_has_grapple(state, player)],
        ["spirit island", "spirit power 1", False, lambda state: ph_has_spirit_gems(state, player, "Power", 10)],
        ["spirit island", "spirit power 2", False, lambda state: ph_has_spirit_gems(state, player, "Power", 20)],
        ["spirit island", "spirit wisdom 1", False, lambda state: ph_has_spirit_gems(state, player, "Wisdom", 10)],
        ["spirit island", "spirit wisdom 2", False, lambda state: ph_has_spirit_gems(state, player, "Wisdom", 20)],
        ["spirit island", "spirit courage 1", False, lambda state: ph_has_spirit_gems(state, player, "Courage", 10)],
        ["spirit island", "spirit courage 2", False, lambda state: ph_has_spirit_gems(state, player, "Courage", 20)],

        # ============ Ocean NW ===============
        ["sw ocean west", "nw ocean", False, lambda state: ph_has_sea_chart(state, player, "NW")],
        ["sw ocean east", "nw ocean", False, lambda state: ph_has_frog_n(state, player)],
        ["nw ocean", "nw ocean frog n", False, lambda state: ph_has_cannon(state, player)],
        ["nw ocean", "gust", False, None],
        ["nw ocean", "bannan", False, None],
        ["nw ocean", "zauz", False, None],
        ["nw ocean", "uncharted", False, None],
        ["nw ocean", "ghost ship", False, lambda state: ph_has_ghost_ship_access(state, player)],
        ["nw ocean", "porl", False, None],
        ["porl", "porl item", False, lambda state: ph_has_sword(state, player)],
        ["porl", "porl trade", False, lambda state: ph_has_heros_new_clothes(state, player)],

        # ================= Isle of Gust ====================

        ["gust", "gust combat", False, lambda state: ph_has_cave_damage(state, player)],
        ["gust", "gust dig", False, lambda state: ph_has_shovel(state, player)],
        ["gust dig", "tow", False, None],

        # ================= Temple of Wind ====================

        ["tow", "tow b1", False, lambda state: any([
            ph_can_hammer_clip(state, player),
            ph_can_kill_bat(state, player)])],
        ["tow b1", "tow b2", False, None],
        ["tow b2", "tow b2 dig", False, lambda state: ph_has_shovel(state, player)],
        ["tow b2", "tow b2 bombs", False, lambda state: ph_has_explosives(state, player)],
        ["tow b2", "tow b2 key", False, lambda state: any([
            ph_has_small_keys(state, player, "Temple of Wind"),
            ph_wind_temple_key_ut(state, player)])],
        ["tow b2", "tow bk chest", False, lambda state: ph_has_bombs(state, player)],
        ["tow", "tow cyclok", False, lambda state: all([
            ph_has_bombs(state, player),
            ph_has_boss_key_simple(state, player, "Temple of Wind")])],
        ["tow cyclok", "post tow", False, None],

        # ================= Bannan Island ====================

        ["bannan", "bannan grapple", False, lambda state: ph_has_grapple(state, player)],
        ["bannan", "bannan dig", False, lambda state: ph_has_shovel(state, player)],
        ["bannan", "bannan east", False, lambda state: ph_has_bombs(state, player)],
        ["bannan east", "bannan east grapple", False, lambda state: ph_has_grapple(state, player)],
        ["bannan east grapple", "bannan east grapple dig", False, lambda state: ph_has_shovel(state, player)],
        ["bannan east", "bannan cannon game", False, lambda state: ph_has_cannon(state, player)],
        ["bannan", "bannan scroll", False, lambda state: ph_bannan_scroll(state, player)],
        ["bannan", "bannan loovar", False, lambda state: ph_has_loovar(state, player)],
        ["bannan", "bannan rsf", False, lambda state: ph_has_rsf(state, player)],
        ["bannan", "bannan neptoona", False, lambda state: ph_has_neptoona(state, player)],
        ["bannan", "bannan stowfish", False, lambda state: ph_has_stowfish(state, player)],
        ["bannan", "bannan letter", False, lambda state: ph_has_jolene_letter(state, player)],

        # ================= Zauz's Island ====================

        ["zauz", "zauz dig", False, lambda state: ph_has_shovel(state, player)],
        ["zauz", "zauz blade", False, lambda state: ph_zauz_required_metals(state, player)],
        ["ghost ship tetra", "zauz crest", False, None],

        # ================= Uncharted Island ====================

        ["uncharted", "uncharted dig", False, lambda state: ph_has_shovel(state, player)],
        ["uncharted", "uncharted cave", False, lambda state: ph_has_sword(state, player)],
        ["uncharted cave", "uncharted grapple", False, lambda state: ph_has_grapple(state, player)],

        # ================= Ghost Ship ====================

        ["ghost ship", "ghost ship barrel", False, lambda state: ph_ghost_ship_barrel(state, player)],
        ["ghost ship barrel", "ghost ship b2", False, lambda state:
        any([ph_has_shape_crystal(state, player, "Ghost Ship", "Triangle"),
             ph_is_ut(state, player)])],
        ["ghost ship b2", "ghost ship b3", False, None],
        ["ghost ship b3", "ghost ship cubus", False, lambda state: ph_has_sword(state, player)],
        ["ghost ship b2", "ghost ship tetra", False, lambda state: ph_has_ghost_key(state, player)],
        ["ghost ship tetra", "spawn pirate ambush", False, None],

        # ================= SE Ocean ====================

        ["sw ocean", "se ocean", False, lambda state: all([
            ph_has_sea_chart(state, player, "SE"),
            ph_has_sea_chart(state, player, "SW")])],
        ["se ocean", "se ocean frogs", False, lambda state: ph_has_cannon(state, player)],
        ["se ocean", "goron", False, lambda state: ph_can_pass_sea_monsters(state, player)],
        ["se ocean", "se ocean trade", False, lambda state: ph_has_kaleidoscope(state, player)],
        ["se ocean", "iof", False, lambda state: ph_can_pass_sea_monsters(state, player)],
        ["se ocean", "harrow", False, lambda state: ph_has_sword(state, player)],
        ["se ocean", "ds", False, None],
        ["se ocean", "pirate ambush", False, lambda state: ph_beat_ghost_ship(state, player)],

        # ================= Goron Island ====================

        ["goron", "goron chus", False, lambda state: ph_goron_chus(state, player)],
        ["goron", "goron grapple", False, lambda state: ph_has_grapple(state, player)],
        ["goron chus", "goron quiz", False, None],
        ["goron", "goron north", False, None],
        ["goron north", "goron north bombchu", False, lambda state: ph_can_hit_bombchu_switches(state, player)],
        ["goron north", "goron outside temple", False, lambda state: ph_has_explosives(state, player)],
        ["goron", "goron outside temple", False, lambda state: ph_can_hammer_clip(state, player)],
        ["goron outside temple", "goron north", False, lambda state: ph_has_bombs(state, player)],
        ["goron outside temple", "gt", False, lambda state: ph_has_shovel(state, player)],
        ["gt dongo", "goron chief 2", False, lambda state: ph_goron_chus(state, player)],

        # ================= Goron Temple ====================
        ["gt", "gt bow", False, lambda state: ph_has_bow(state, player)],
        ["gt", "gt b1", False, lambda state: all([ph_has_explosives(state, player),
                                                  ph_can_kill_eye_brute(state, player),
                                                  ph_has_sword(state, player)])],
        ["gt b1", "gt b2", False, lambda state: ph_can_hit_bombchu_switches(state, player)],
        ["gt b2", "gt b3", False, None],
        ["gt b2", "gt b2 back", False, lambda state: any([
            ph_has_explosives(state, player),
            ph_has_boomerang(state, player)])],
        ["gt b2 back", "gt bk chest", False, lambda state: ph_has_chus(state, player)],
        ["gt b2", "gt dongo", False, lambda state: all([
            ph_has_chus(state, player),
            ph_has_boss_key_simple(state, player, "Goron Temple")])],

        # ================= Harrow Island ====================

        ["harrow", "harrow dig", False, lambda state: ph_has_shovel(state, player)],
        ["harrow dig", "harrow dig 2", False, lambda state: ph_has_sea_chart(state, player, "NE")],

        # ================= Dee Ess Island ====================

        ["ds", "ds dig", False, lambda state: ph_has_shovel(state, player)],
        ["ds", "ds combat", False, lambda state: ph_can_kill_eye_brute(state, player)],
        ["gt dongo", "ds race", False, None],

        # ================= Isle of Frost ====================

        ["iof", "iof grapple", False, lambda state: ph_has_grapple(state, player)],
        ["iof", "iof dig", False, lambda state: ph_has_shovel(state, player)],
        ["iof grapple", "iof grapple dig", False, lambda state: ph_has_shovel(state, player)],
        ["iof", "iof yook", False, lambda state: ph_has_damage(state, player)],
        ["iof yook", "toi", False, None],

        # ================= Ice Temple ====================

        ["toi", "toi 2f", False, lambda state: any([
            ph_has_explosives(state, player),
            ph_has_boomerang(state, player)])],
        ["toi 2f", "toi 3f", False, lambda state: any([
            ph_has_range(state, player),
            ph_has_bombs(state, player)])],
        ["toi 3f", "toi 3f switch", False, lambda state: any([ph_has_bombs(state, player),
                                                              all([
                                                                  ph_option_hard_logic(state, player),
                                                                  ph_has_chus(state, player)
                                                              ])])],
        ["toi 3f switch", "toi 3f boomerang", False, lambda state: ph_toi_3f_boomerang(state, player)],
        ["toi 3f boomerang", "toi 2f miniboss", False, lambda state: ph_toi_key_door_1_ut(state, player)],
        ["toi 3f", "toi 2f miniboss", False, lambda state: ph_toi_key_doors(state, player, 3, 1)],
        ["toi 2f miniboss", "toi side path", False, lambda state: ph_has_grapple(state, player)],
        ["toi", "toi side path", False, lambda state: all([
            ph_can_hammer_clip(state, player),
            ph_has_grapple(state, player)])],
        ["toi side path", "toi b1", False, lambda state: any([
            ph_has_explosives(state, player),
            ph_has_hammer(state, player)
        ])],
        ["toi b1", "toi b1 2", False, lambda state: ph_has_explosives(state, player)],
        ["toi b1 2", "toi b1 key", False, lambda state: ph_toi_key_door_2(state, player)],
        ["toi b1 2", "toi b2", False, lambda state: ph_toi_b2(state, player)],
        ["toi b2", "toi bk chest", False, lambda state: ph_can_hammer_clip(state, player)],
        ["toi b2", "toi b2 key", False, lambda state: ph_toi_key_door_3(state, player)],
        ["toi b2 key", "toi bk chest", False, None],
        ["toi bk chest", "toi gleeok", False, lambda state: ph_is_ut(state, player)],
        ["toi b2", "toi gleeok", False, lambda state: ph_has_boss_key(state, player, "Temple of Ice")],

        # ================= NE Ocean ====================

        ["sw ocean", "ne ocean", False, lambda state: ph_has_frog_square(state, player)],
        ["se ocean", "ne ocean", False, lambda state: ph_has_sea_chart(state, player, "NE")],
        ["ne ocean", "ne ocean frog", False, lambda state: ph_has_cannon(state, player)],
        ["ne ocean", "ne ocean combat", False, lambda state: ph_can_kill_blue_chu(state, player)],
        ["ne ocean", "iotd", False, None],
        ["ne ocean", "maze", False, lambda state: ph_has_sword(state, player)],
        ["ne ocean", "ruins", False, lambda state: all([ph_has_regal_necklace(state, player),
                                                        ph_has_cave_damage(state, player)])],
        ["ne ocean", "pirate ambush", False, lambda state: ph_beat_ghost_ship(state, player)],

        # ================= IotD ====================

        ["iotd", "iotd rupoor", False, lambda state: ph_has_bombs(state, player)],
        ["iotd", "iotd dig", False, lambda state: ph_has_shovel(state, player)],
        ["iotd dig", "iotd cave", False, lambda state: ph_has_bombs(state, player)],

        # ================= Isle of Ruins ====================

        ["ruins", "ruins dig", False, lambda state: ph_has_shovel(state, player)],
        ["ruins", "ruins water", False, lambda state: ph_has_kings_key(state, player)],
        ["ruins water", "mutoh", False, None],

        # ================= Mutoh's Temple ====================

        ["mutoh", "mutoh hammer", False, lambda state: ph_has_hammer(state, player)],
        ["mutoh hammer", "mutoh water", False, lambda state: ph_mutoh_water(state, player)],
        ["mutoh water", "mutoh bk chest", False, lambda state: any([
            ph_has_small_keys(state, player, "Mutoh's Temple", 2),
            ph_ut_small_key_own_dungeon(state, player)])],
        ["mutoh water", "mutoh eox", False, lambda state: ph_has_boss_key(state, player, "Mutoh's Temple")],
        ["mutoh bk chest", "mutoh eox", False, lambda state: ph_is_ut(state, player)],

        # ================= Maze Island ====================

        ["maze", "maze east", False, lambda state: ph_has_explosives(state, player)],
        ["maze", "maze normal", False, lambda state: ph_has_bow(state, player)],
        ["maze normal", "maze expert", False, lambda state: ph_has_grapple(state, player)],
        ["maze", "maze dig", False, lambda state: ph_has_shovel(state, player)],

        # ========== Fishing ====================

        ["sw ocean", "fishing", False, lambda state: ph_has_fishing_rod(state, player)],
        ["fishing", "fishing bcl", False, lambda state: ph_has_big_catch_lure(state, player)],
        ["fishing", "fishing rsf", False, lambda state: ph_can_catch_rsf(state, player)],
        ["fishing", "fishing shadows", False, lambda state: ph_has_swordfish_shadows(state, player)],
        ["fishing", "fishing stowfish", False, lambda state: ph_ut_can_stowfish(state, player)],

        # ========== Salvage ==============

        ["sw ocean west", "sw ocean west salvage", False, lambda state: ph_has_salvage(state, player)],
        ["sw ocean east", "sw ocean east salvage", False, lambda state: ph_has_salvage(state, player)],
        ["nw ocean", "nw ocean salvage", False, lambda state: ph_has_salvage(state, player)],
        ["se ocean", "se ocean salvage", False, lambda state: ph_has_salvage(state, player)],
        ["ne ocean", "ne ocean salvage", False, lambda state: ph_has_salvage(state, player)],
        ["ne ocean", "ne ocean inner", False, lambda state: ph_has_regal_necklace(state, player)],
        ["ne ocean inner", "ne ocean salvage inner", False, lambda state: ph_has_salvage(state, player)],
        ["ne ocean", "nw ocean corner salvage", False, lambda state: all([
            ph_has_salvage(state, player),
            ph_has_sea_chart(state, player, "NW")])],

        ["sw ocean west salvage", "salvage 1", False, lambda state: ph_has_treasure_map(state, player, 1)],
        ["sw ocean east salvage", "salvage 2", False, lambda state: ph_has_treasure_map(state, player, 2)],
        ["nw ocean salvage", "salvage 3", False, lambda state: ph_has_treasure_map(state, player, 3)],
        ["nw ocean corner salvage", "salvage 4", False, lambda state: ph_has_treasure_map(state, player, 4)],
        ["sw ocean west salvage", "salvage 5", False, lambda state: ph_has_treasure_map(state, player, 5)],
        ["nw ocean salvage", "salvage 6", False, lambda state: ph_has_treasure_map(state, player, 6)],
        ["nw ocean salvage", "salvage 7", False, lambda state: ph_has_treasure_map(state, player, 7)],
        ["sw ocean east salvage", "salvage 8", False, lambda state: ph_has_treasure_map(state, player, 8)],
        ["sw ocean east salvage", "salvage 9", False, lambda state: ph_has_treasure_map(state, player, 9)],
        ["nw ocean salvage", "salvage 10", False, lambda state: ph_has_treasure_map(state, player, 10)],
        ["nw ocean salvage", "salvage 11", False, lambda state: ph_has_treasure_map(state, player, 11)],
        ["se ocean salvage", "salvage 12", False, lambda state: ph_has_treasure_map(state, player, 12)],
        ["se ocean salvage", "salvage 13", False, lambda state: ph_has_treasure_map(state, player, 13)],
        ["se ocean salvage", "salvage 14", False, lambda state: ph_has_treasure_map(state, player, 14)],
        ["se ocean salvage", "salvage 15", False, lambda state: ph_has_treasure_map(state, player, 15)],
        ["se ocean salvage", "salvage 16", False, lambda state: ph_has_treasure_map(state, player, 16)],
        ["se ocean salvage", "salvage 17", False, lambda state: ph_has_treasure_map(state, player, 17)],
        ["sw ocean east salvage", "salvage 18", False, lambda state: ph_has_treasure_map(state, player, 18)],
        ["nw ocean salvage", "salvage 19", False, lambda state: ph_has_treasure_map(state, player, 19)],
        ["nw ocean corner salvage", "salvage 20", False, lambda state: ph_has_treasure_map(state, player, 20)],
        ["sw ocean west salvage", "salvage 21", False, lambda state: ph_has_treasure_map(state, player, 21)],
        ["se ocean salvage", "salvage 22", False, lambda state: ph_has_treasure_map(state, player, 22)],
        ["se ocean salvage", "salvage 23", False, lambda state: ph_has_treasure_map(state, player, 23)],
        ["ne ocean salvage", "salvage 24", False, lambda state: ph_has_treasure_map(state, player, 24)],
        ["ne ocean salvage", "salvage 25", False, lambda state: ph_has_treasure_map(state, player, 25)],
        ["ne ocean salvage inner", "salvage 26", False, lambda state: ph_has_treasure_map(state, player, 26)],
        ["ne ocean salvage", "salvage 27", False, lambda state: ph_has_treasure_map(state, player, 27)],
        ["ne ocean salvage inner", "salvage 28", False, lambda state: ph_has_treasure_map(state, player, 28)],
        ["ne ocean salvage", "salvage 29", False, lambda state: ph_has_treasure_map(state, player, 29)],
        ["ne ocean salvage", "salvage 30", False, lambda state: ph_has_treasure_map(state, player, 30)],
        ["ne ocean salvage", "salvage 31", False, lambda state: ph_has_treasure_map(state, player, 31)],

        # Goal stuff
        ["sw ocean east", "bellumbeck", False, lambda state: ph_bellumbeck_quick_finish(state, player)],
        ["bellumbeck", "beat bellumbeck", False, lambda state: ph_can_beat_bellumbeck(state, player)],
        ["beat bellumbeck", "goal", False, None],
        ["totok midway", "goal", False, lambda state: ph_option_goal_midway(state, player)],
        ["mercay island", "goal", False, lambda state: ph_win_on_metals(state, player)],

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
