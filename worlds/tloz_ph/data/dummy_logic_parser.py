from worlds.tloz_ph.data.LogicPredicates import *
from BaseClasses import CollectionState
import inspect


# This file is for reformatting logic data

player = 0

overworld_logic = [
# ====== Mercay Island ==============

    ['mercay island', 'mercay dig spot', False, "ph_has_shovel(state, player)"],
    ['mercay island', 'mercay zora cave', False, "ph_has_explosives(state, player)"],
    ['mercay zora cave', 'mercay zora cave south', False, "ph_has_bow(state, player)"],
    ['mercay island', 'mercay zora cave south', False, "ph_can_sword_scroll_clip(state, player)"],
    ['mercay island', 'totok', False, None],
    ['mercay island', 'mercay freedle island', False, "ph_has_explosives(state, player)"],
    ['mercay freedle island', 'mercay freedle tunnel chest', False, "ph_has_range(state, player)"],
    ['mercay freedle island', 'mercay freedle gift', False, "ph_has_sea_chart(state, player, 'SE')"],
    ['mercay island', 'mercay yellow guy', False, "ph_has_courage_crest(state, player)"],
    ['post tow', 'mercay oshus gem', False, None],
    ['mercay island', 'mercay oshus phantom blade', False, "ph_has_phantom_blade(state, player)"],
    ['mercay oshus phantom blade', 'mercay oshus gem', False, None],
    ['mercay island', 'sw ocean', False, "ph_has_sea_chart(state, player, 'SW')"],

    # ======== Mountain Passage =========

    ['mercay island', 'mercay passage 1', False, "any([ph_can_cut_small_trees(state, player), ph_has_small_keys(state, player, 'Mountain Passage', 3),ph_option_glitched_logic(state, player)])"],
    ['mercay island', 'mercay passage 2', False, "ph_can_reach_MP2(state, player)"],
    ['mercay passage 2', 'mercay passage rat', False, "ph_mercay_passage_rat(state, player)"],

    # ========== TotOK ===================
    ['totok', 'totok 1f chart chest', False, "any([ph_has_small_keys(state, player, 'Temple of the Ocean King', 1),ph_ut_small_key_vanilla_location(state, player),ph_totok_b1_all_checks_ut(state, player)])"],
    # B1
    ['totok', 'totok b1', False, "ph_has_spirit(state, player, 'Power')"],
    ['totok b1', 'totok b1 eye chest', False, "all([ph_has_grapple(state, player),ph_has_bow(state, player)])"],
    ['totok b1', 'totok b1 phantom chest', False, "ph_can_kill_phantoms(state, player)"],
    ['totok b1', 'totok b1 key', False, "any([ph_has_explosives(state, player),ph_has_grapple(state, player),ph_has_boomerang(state, player)])"],
    ['totok b1 key', 'totok b2', False, "any([ph_ut_small_key_vanilla_location(state, player),ph_totok_b1_all_checks_ut(state, player)])"],
    ['totok b1', 'totok b2', False, "ph_has_small_keys(state, player, 'Temple of the Ocean King', 2)"],
    # B2
    ['totok b2', 'totok b2 key', False, "ph_totok_b2_key(state, player)"],
    ['totok b2', 'totok b2 bombchu chest', False, "all([ph_can_hit_bombchu_switches(state, player),ph_has_explosives(state, player)])"],
    ['totok b2', 'totok b2 phantom chest', False, "all([ph_has_phantom_sword(state, player),any([ph_can_hit_tricky_switches(state, player),ph_has_explosives(state, player)])])"],
    ['totok b2 key', 'totok b3', False, "any([ph_ut_small_key_vanilla_location(state, player),ph_totok_b2_all_checks_ut(state, player)])"],
    ['totok b2', 'totok b3', False, "ph_has_small_keys(state, player, 'Temple of the Ocean King', 3)"],
    # B3
    ['totok b3', 'totok b3 phantom chest', False, "all([ph_can_kill_phantoms_traps(state, player),ph_has_grapple(state, player)])"],
    ['totok b3', 'totok b3 locked chest', False, "any([ph_has_small_keys(state, player, 'Temple of the Ocean King', 4),ph_ut_small_key_vanilla_location(state, player)])"],  # UT
    ['totok b3 locked chest', 'totok b3.5', False, "ph_is_ut(state, player)"],  # UT ignores force gems
    ['totok b3', 'totok b3 bow chest', False, "ph_has_bow(state, player)"],
    ['totok b3', 'totok b3.5', False, "ph_totok_b4_access(state, player)"],
    ['totok b3.5', 'totok b4', False, "all([ph_has_spirit(state, player, 'Wisdom'),ph_can_hit_tricky_switches(state, player)])"],
    # B4
    ['totok b4', 'totok b4 phantom chest', False, "ph_has_phantom_sword(state, player)"],
    ['totok b4', 'totok b4 key', False, "any([ph_has_explosives(state, player),ph_can_boomerang_return(state, player)])"],
    ['totok b4', 'totok b5', False, "ph_totok_b5_key_logic(state, player)"],
    ['totok b5', 'totok b5 chest', False, "ph_totok_b5(state, player)"],
    ['totok b5 chest', 'totok b6', False, None],
    ['totok b4', 'totok b5.5', False, "all([ph_totok_b5_key_logic(state, player),ph_can_hit_bombchu_switches(state, player)])"],
    ['totok b5.5', 'totok b5.5 chest', False, "ph_has_shovel(state, player)"],
    ['totok b5.5', 'totok b6', False, None],
    # B6
    ['totok b6', 'totok b6 phantom chest', False, "ph_has_phantom_sword(state, player)"],
    ['totok b6', 'totok b6 bow chest', False, "ph_has_bow(state, player)"],
    ['totok b6', 'totok b6 cc', False, "ph_has_sea_chart(state, player, 'SW')"],
    ['totok b6', 'totok midway', False, "ph_has_triforce_crest(state, player)"],

    # ============ TotOK Part 2 =====================

    # B7
    ['totok midway', 'totok b7', False, "ph_has_spirit(state, player, 'Courage')"],
    ['totok b7', 'totok b8', False, None],
    ['totok b7', 'totok b7 east', False, "ph_has_grapple(state, player)"],
    ['totok b7 east', 'totok b7 peg', False, "ph_has_range(state, player)"],
    ['totok b7', 'totok b7 phantom', False, "ph_can_kill_phantoms(state, player)"],
    # B8
    ['totok b8', 'totok b7 east', False, "ph_can_hit_switches(state, player)"],
    ['totok b8', 'totok b9 nw', False, "any([ph_has_totok_crystal(state, player, 'Round'),ph_has_hammer(state, player)])"],
    ['totok b7 east', 'totok b9 nw', False, "ph_is_ut(state, player)"],  # UT Bypass
    ['totok b8', 'totok b8 phantom', False, "ph_can_kill_phantoms(state, player)"],
    ['totok b8', 'totok b8 2 crystals', False, "ph_totok_b8_2_crystals(state, player)"],
    ['totok b8', 'totok b9', False, "ph_totok_b9(state, player)"],  # Includes UT
    # B9
    ['totok b9', 'totok b9 ghosts', False, "ph_can_hit_switches(state, player)"],
    ['totok b9', 'totok b9 nw', False, "ph_totok_b9_phantom_square(state, player)"],
    ['totok b9', 'totok b9 phantom', False, "ph_totok_b9_phantom_kill(state, player)"],
    ['totok b9', 'totok b9.5', False, "ph_totok_b95(state, player)"],  # UT Crystals
    ['totok b9.5', 'totok b10', False, None],
    # B10
    ['totok b10', 'totok b10 inner', False, "ph_has_explosives(state, player)"],
    ['totok b10 inner', 'totok b10 hammer', False, "ph_has_hammer(state, player)"],
    ['totok b10 inner', 'totok b10 phantom', False, "ph_can_kill_phantoms_traps(state, player)"],
    ['totok b10 inner', 'totok b10 phantom eyes', False, "ph_has_grapple(state, player)"],
    ['totok b10 inner', 'totok b11', False, "ph_totok_b10_key_logic(state, player)"],
    # B11
    ['totok b11', 'totok b11 phantom', False, "ph_has_phantom_sword(state, player)"],
    ['totok b11', 'totok b12', False, "ph_totok_b12(state, player)"],
    # B12
    ['totok b12', 'totok b12 hammer', False, "ph_has_hammer(state, player)"],
    ['totok b12', 'totok b12 phantom', False, "ph_has_phantom_sword(state, player)"],
    ['totok b12', 'totok b13', False, "ph_totok_b12_force_gems(state, player)"],  # UT Force gems

    # B13
    ['totok b13', 'totok before bellum', False, "ph_totok_b13_door(state, player)"],
    ['totok', 'totok before bellum', False, "ph_totok_blue_warp(state, player)"],
    # Bellum
    ['totok', 'bellum 1', False, "ph_totok_bellum_staircase(state, player)"],
    ['bellum 1', 'ghost ship fight', False, "ph_can_beat_bellum(state, player)"],
    ['ghost ship fight', 'bellumbeck', False, "ph_can_beat_ghost_ship_fight(state, player)"],

    # ============ Shops ====================

    ['mercay island', 'shop power gem', False, "ph_can_buy_gem(state, player)"],
    ['mercay island', 'shop quiver', False, "ph_can_buy_quiver(state, player)"],
    ['mercay island', 'shop bombchu bag', False, "ph_can_buy_chu_bag(state, player)"],
    ['mercay island', 'shop heart container', False, "ph_can_buy_heart(state, player)"],

    ['sw ocean east', 'beedle gem', False, "ph_beedle_shop(state, player, 500)"],
    ['sw ocean east', 'beedle bomb bag', False, "all([ph_beedle_shop(state, player, 500),ph_has_bombs(state, player)])"],
    ['sw ocean east', 'masked ship gem', False, "ph_beedle_shop(state, player, 500)"],
    ['sw ocean east', 'masked ship hc', False, "ph_beedle_shop(state, player, 500)"],

    # ============ SW Ocean =================

    ['mercay island', 'sw ocean east', False, "ph_boat_access(state, player)"],
    ['sw ocean east', 'cannon island', False, None],
    ['sw ocean east', 'ember island', False, None],
    ['sw ocean east', 'sw ocean crest salvage', False, "ph_salvage_courage_crest(state, player)"],
    ['sw ocean east', 'sw ocean west', False, "ph_can_enter_ocean_sw_west(state, player)"],
    ['sw ocean west', 'molida island', False, None],
    ['sw ocean west', 'spirit island', False, None],
    ['sw ocean west', 'sw ocean nyave', False, "ph_has_cave_damage(state, player)"],
    ['sw ocean nyave', 'sw ocean nyave trade', False, "ph_has_guard_notebook(state, player)"],
    ['sw ocean west', 'sw ocean frog phi', False, "ph_has_cannon(state, player)"],
    ['sw ocean east', 'sw ocean frog x', False, "ph_has_cannon(state, player)"],

    # ============ Cannon Island ===============

    ['cannon island', 'cannon island salvage arm', False, "ph_has_courage_crest(state, player)"],
    ['cannon island', 'cannon island dig', False, "ph_has_shovel(state, player)"],

    # =============== Isle of Ember ================

    ['ember island', 'ember island dig', False, "ph_has_shovel(state, player)"],
    ['ember island', 'ember island grapple', False, "any([ph_has_grapple(state, player),ph_can_sword_glitch(state, player)])"],
    ['ember island', 'tof 1f', False, None],

    # =============== Temple of Fire =================

    ['tof 1f', 'tof 1f keese', False, "ph_can_kill_bat(state, player)"],
    ['tof 1f', 'tof 1f maze', False, "any([ph_has_small_keys(state, player, 'Temple of Fire', 1),ph_tof_1f_key_ut(state, player)])"],
    ['tof 1f maze', 'tof 2f', False, "ph_can_hit_spin_switches(state, player)"],
    # 2F
    ['tof 2f', 'tof 1f west', False, "ph_has_short_range(state, player)"],
    ['tof 1f west', 'tof 1f sw', False, "ph_spiral_wall_switches(state, player)"],
    ['tof 1f sw', 'tof 2f south', False, "ph_can_kill_bubble(state, player)"],
    ['tof 2f south', 'tof 3f', False, "ph_tof_3f(state, player)"],
    # 3F
    ['tof 3f', 'tof 3f key drop', False, "ph_has_boomerang(state, player)"],
    ['tof 3f key drop', 'tof 3f boss key', False, "any([ph_has_small_keys(state, player, 'Temple of Fire', 3),ph_ut_small_key_own_dungeon(state, player)])"],  # All 3F checks need boomerang, UT included
    ['tof 3f boss key', 'tof blaaz', False, "all([ph_has_sword(state, player),ph_has_boss_key_simple(state, player, 'Temple of Fire')])"],  # Includes UT
    ['tof blaaz', 'post tof', False, None],

    # =========== Molida Island ===============

    ['molida island', 'molida dig', False, "ph_has_shovel(state, player)"],
    ['molida island', 'molida grapple', False, "ph_has_grapple(state, player)"],
    ['molida island', 'molida cave back', False, "ph_has_cave_damage(state, player)"],
    ['molida cave back', 'molida cave back dig', False, "ph_has_shovel(state, player)"],
    ['molida cave back dig', 'molida cuccoo dig', False, "ph_has_grapple(state, player)"],
    ['molida dig', 'molida north', False, "ph_has_sun_key(state, player)"],
    ['molida north', 'molida north grapple', False, "ph_has_grapple(state, player)"],
    ['molida north', 'toc', False, "ph_can_enter_toc(state, player)"],
    ['toc crayk', 'post toc', False, None],
    ['post toc', 'molida archery', False, None],

    # =============== Temple of Courage ================

    ['toc', 'toc bomb alcove', False, "ph_has_explosives(state, player)"],
    ['toc', 'toc b1', False, "ph_toc_key_door_1(state, player)"],
    ['toc', 'toc hammer clips', False, "ph_can_hammer_clip(state, player)"],
    ['toc b1', 'toc b1 grapple', False, "any([ph_has_grapple(state, player),ph_can_boomerang_return(state, player)])"],
    ['toc b1', 'toc 1f west', False, "ph_has_explosives(state, player)"],
    ['toc b1 grapple', 'toc 1f west', False, "ph_has_bow(state, player)"],
    ['toc hammer clips', 'toc 1f west', False, None],
    ['toc 1f west', 'toc map room', False, "ph_has_explosives(state, player)"],
    ['toc 1f west', 'toc 2f beamos', False, "ph_toc_key_door_2(state, player)"],
    ['toc 1f west', 'toc b1 maze', False, "ph_has_shape_crystal(state, player, 'Temple of Courage', 'Square')"],
    ['toc 2f beamos', 'toc b1 maze', False, "ph_is_ut(state, player)"],  # UT Crystal
    ['toc 2f beamos', 'toc south 1f', False, "all([ph_is_ut(state, player),ph_has_bow(state, player)])"],
    ['toc b1 grapple', 'toc b1 maze', False, None],
    ['toc b1 maze', 'toc south 1f', False, "all([ph_has_bow(state, player),ph_has_shape_crystal(state, player, 'Temple of Courage', 'Square')])"],

    ['toc south 1f', 'toc 2f spike corridor', False, "ph_has_explosives(state, player)"],
    ['toc 2f spike corridor', 'toc 2f platforms', False, "all([ph_has_explosives(state, player),ph_has_bow(state, player)])"],
    ['toc hammer clips', 'toc 2f spike corridor', False, None],
    ['toc south 1f', 'toc 2f platforms', False, "ph_has_bow(state, player)"],
    ['toc 2f spike corridor', 'toc torches', False, "ph_has_boomerang(state, player)"],
    ['toc torches', 'toc torches chest', False, "ph_has_bow(state, player)"],
    ['toc torches', 'toc pols 2', False, "ph_toc_final_switch_state(state, player)"],
    ['toc pols 2', 'toc bk room', False, "ph_toc_key_door_3(state, player)"],
    ['toc bk room', 'toc bk chest', False, "ph_has_bow(state, player)"],
    ['toc bk room', 'toc before boss', False, "ph_has_boss_key(state, player, 'Temple of Courage')"],
    ['toc bk chest', 'toc before boss', False, "ph_has_boss_key_simple(state, player, 'Temple of Courage')"],
    ['toc before boss', 'toc before boss chest', False, "ph_has_explosives(state, player)"],
    ['toc before boss', 'toc crayk', False, "ph_has_bow(state, player)"],

    # ================ Spirit Island =====================

    ['spirit island', 'spirit island gauntlet', False, "ph_has_grapple(state, player)"],
    ['spirit island', 'spirit power 1', False, "ph_has_spirit_gems(state, player, 'Power', 10)"],
    ['spirit island', 'spirit power 2', False, "ph_has_spirit_gems(state, player, 'Power', 20)"],
    ['spirit island', 'spirit wisdom 1', False, "ph_has_spirit_gems(state, player, 'Wisdom', 10)"],
    ['spirit island', 'spirit wisdom 2', False, "ph_has_spirit_gems(state, player, 'Wisdom', 20)"],
    ['spirit island', 'spirit courage 1', False, "ph_has_spirit_gems(state, player, 'Courage', 10)"],
    ['spirit island', 'spirit courage 2', False, "ph_has_spirit_gems(state, player, 'Courage', 20)"],

    # ============ Ocean NW ===============
    ['sw ocean west', 'nw ocean', False, "ph_has_sea_chart(state, player, 'NW')"],
    ['sw ocean east', 'nw ocean', False, "ph_has_frog_n(state, player)"],
    ['nw ocean', 'nw ocean frog n', False, "ph_has_cannon(state, player)"],
    ['nw ocean', 'gust', False, None],
    ['nw ocean', 'bannan', False, None],
    ['nw ocean', 'zauz', False, None],
    ['nw ocean', 'uncharted', False, None],
    ['nw ocean', 'ghost ship', False, "ph_has_ghost_ship_access(state, player)"],
    ['nw ocean', 'porl', False, None],
    ['porl', 'porl item', False, "ph_has_sword(state, player)"],
    ['porl', 'porl trade', False, "ph_has_heros_new_clothes(state, player)"],

    # ================= Isle of Gust ====================

    ['gust', 'gust combat', False, "ph_has_cave_damage(state, player)"],
    ['gust', 'gust dig', False, "ph_has_shovel(state, player)"],
    ['gust dig', 'tow', False, None],

    # ================= Temple of Wind ====================

    ['tow', 'tow b1', False, "any([ph_can_hammer_clip(state, player),ph_can_kill_bat(state, player)])"],
    ['tow b1', 'tow b2', False, None],
    ['tow b2', 'tow b2 dig', False, "ph_has_shovel(state, player)"],
    ['tow b2', 'tow b2 bombs', False, "ph_has_explosives(state, player)"],
    ['tow b2', 'tow b2 key', False, "any([ph_has_small_keys(state, player, 'Temple of Wind'),ph_wind_temple_key_ut(state, player)])"],
    ['tow b2', 'tow bk chest', False, "ph_has_bombs(state, player)"],
    ['tow', 'tow cyclok', False, "all([ph_has_bombs(state, player),ph_has_boss_key_simple(state, player, 'Temple of Wind')])"],
    ['tow cyclok', 'post tow', False, None],

    # ================= Bannan Island ====================

    ['bannan', 'bannan grapple', False, "ph_has_grapple(state, player)"],
    ['bannan', 'bannan dig', False, "ph_has_shovel(state, player)"],
    ['bannan', 'bannan east', False, "ph_has_bombs(state, player)"],
    ['bannan east', 'bannan east grapple', False, "ph_has_grapple(state, player)"],
    ['bannan east grapple', 'bannan east grapple dig', False, "ph_has_shovel(state, player)"],
    ['bannan east', 'bannan cannon game', False, "ph_has_cannon(state, player)"],
    ['bannan', 'bannan scroll', False, "ph_bannan_scroll(state, player)"],

    # ================= Zauz's Island ====================

    ['zauz', 'zauz dig', False, "ph_has_shovel(state, player)"],
    ['zauz', 'zauz blade', False, None],
    ['ghost ship tetra', 'zauz crest', False, None],

    # ================= Uncharted Island ====================

    ['uncharted', 'uncharted dig', False, "ph_has_shovel(state, player)"],
    ['uncharted', 'uncharted cave', False, "ph_has_sword(state, player)"],
    ['uncharted cave', 'uncharted grapple', False, "ph_has_grapple(state, player)"],

    # ================= Ghost Ship ====================

    ['ghost ship', 'ghost ship barrel', False, "ph_ghost_ship_barrel(state, player)"],
    ['ghost ship barrel', 'ghost ship b2', False, "any([ph_has_shape_crystal(state, player, 'Ghost Ship', 'Triangle'),ph_is_ut(state, player)])"],
    ['ghost ship b2', 'ghost ship b3', False, None],
    ['ghost ship b3', 'ghost ship cubus', False, "ph_has_sword(state, player)"],
    ['ghost ship b2', 'ghost ship tetra', False, "ph_has_ghost_key(state, player)"],
    ['ghost ship tetra', 'spawn pirate ambush', False, None],

    # ================= SE Ocean ====================

    ['sw ocean', 'se ocean', False, "all([ph_has_sea_chart(state, player, 'SE'),ph_has_sea_chart(state, player, 'SW')])"],
    ['se ocean', 'se ocean frogs', False, "ph_has_cannon(state, player)"],
    ['se ocean', 'goron', False, "ph_has_cannon(state, player)"],
    ['se ocean', 'se ocean trade', False, "ph_has_kaleidoscope(state, player)"],
    ['se ocean', 'iof', False, "ph_has_cannon(state, player)"],
    ['se ocean', 'harrow', False, "ph_has_sword(state, player)"],
    ['se ocean', 'ds', False, None],
    ['se ocean', 'pirate ambush', False, "ph_beat_ghost_ship(state, player)"],

    # ================= Goron Island ====================

    ['goron', 'goron chus', False, "ph_goron_chus(state, player)"],
    ['goron', 'goron grapple', False, "ph_has_grapple(state, player)"],
    ['goron chus', 'goron quiz', False, None],
    ['goron', 'goron north', False, None],
    ['goron north', 'goron north bombchu', False, "ph_can_hit_bombchu_switches(state, player)"],
    ['goron north', 'goron outside temple', False, "ph_has_explosives(state, player)"],
    ['goron', 'goron outside temple', False, "ph_can_hammer_clip(state, player)"],
    ['goron outside temple', 'goron north', False, "ph_has_bombs(state, player)"],
    ['goron outside temple', 'gt', False, "ph_has_shovel(state, player)"],
    ['gt dongo', 'goron chief 2', False, None],

    # ================= Goron Temple ====================
    ['gt', 'gt bow', False, "ph_has_bow(state, player)"],
    ['gt', 'gt b1', False, "all([ph_has_explosives(state, player),ph_can_kill_eye_brute(state, player)])"],
    ['gt', 'gt b2', False, "ph_can_hit_bombchu_switches(state, player)"],
    ['gt b2', 'gt b3', False, None],
    ['gt b2', 'gt b2 back', False, "any([ph_has_explosives(state, player),ph_has_boomerang(state, player)])"],
    ['gt b2 back', 'gt bk chest', False, "ph_has_chus(state, player)"],
    ['gt b2', 'gt dongo', False, "all([ph_has_chus(state, player),ph_has_boss_key_simple(state, player, 'Goron Temple')])"],

    # ================= Harrow Island ====================

    ['harrow', 'harrow dig', False, "ph_has_shovel(state, player)"],
    ['harrow dig', 'harrow dig 2', False, "ph_has_sea_chart(state, player, 'NE')"],

    # ================= Dee Ess Island ====================

    ['ds', 'ds dig', False, "ph_has_shovel(state, player)"],
    ['ds', 'ds combat', False, "ph_can_kill_eye_brute(state, player)"],
    ['gt dongo', 'ds race', False, None],

    # ================= Isle of Frost ====================

    ['iof', 'iof grapple', False, "ph_has_grapple(state, player)"],
    ['iof', 'iof dig', False, "ph_has_shovel(state, player)"],
    ['iof grapple', 'iof grapple dig', False, "ph_has_shovel(state, player)"],
    ['iof', 'iof yook', False, "ph_has_damage(state, player)"],
    ['iof yook', 'toi', False, None],

    # ================= Ice Temple ====================

    ['toi', 'toi 2f', False, "any([ph_has_explosives(state, player),ph_has_boomerang(state, player)])"],
    ['toi 2f', 'toi 3f', False, "any([ph_has_range(state, player),ph_has_bombs(state, player)])"],
    ['toi 3f', 'toi 3f switch', False, "ph_has_explosives(state, player)"],
    ['toi 3f switch', 'toi 3f boomerang', False, "ph_toi_3f_boomerang(state, player)"],
    ['toi 3f boomerang', 'toi 2f miniboss', False, "ph_toi_key_door_1_ut(state, player)"],
    ['toi 3f', 'toi 2f miniboss', False, "ph_toi_key_doors(state, player, 3, 1)"],
    ['toi 2f miniboss', 'toi side path', False, "ph_has_grapple(state, player)"],
    ['toi', 'toi side path', False, "all([ph_can_hammer_clip(state, player),ph_has_grapple(state, player)])"],
    ['toi side path', 'toi b1', False, "any([ph_has_explosives(state, player),ph_has_hammer(state, player)])"],
    ['toi b1', 'toi b1 2', False, "ph_has_explosives(state, player)"],
    ['toi b1 2', 'toi b1 key', False, "ph_toi_key_door_2(state, player)"],
    ['toi b1 2', 'toi b2', False, "ph_toi_b2(state, player)"],
    ['toi b2', 'toi bk chest', False, "ph_can_hammer_clip(state, player)"],
    ['toi b2', 'toi b2 key', False, "ph_toi_key_door_3(state, player)"],
    ['toi b2 key', 'toi bk chest', False, None],
    ['toi bk chest', 'toi gleeok', False, "ph_is_ut(state, player)"],
    ['toi b2', 'toi gleeok', False, "ph_has_boss_key(state, player, 'Temple of Ice')"],

    # ================= NE Ocean ====================

    ['sw ocean', 'ne ocean', False, "ph_has_frog_square(state, player)"],
    ['se ocean', 'ne ocean', False, "ph_has_sea_chart(state, player, 'NE')"],
    ['ne ocean', 'ne ocean frog', False, "ph_has_cannon(state, player)"],
    ['ne ocean', 'ne ocean combat', False, "ph_can_kill_blue_chu(state, player)"],
    ['ne ocean', 'iotd', False, None],
    ['ne ocean', 'maze', False, "ph_has_sword(state, player)"],
    ['ne ocean', 'ruins', False, "all([ph_has_regal_necklace(state, player),ph_has_cave_damage(state, player)])"],
    ['ne ocean', 'pirate ambush', False, "ph_beat_ghost_ship(state, player)"],

    # ================= IotD ====================

    ['iotd', 'iotd rupoor', False, "ph_has_bombs(state, player)"],
    ['iotd', 'iotd dig', False, "ph_has_shovel(state, player)"],
    ['iotd dig', 'iotd cave', False, "ph_has_bombs(state, player)"],

    # ================= Isle of Ruins ====================

    ['ruins', 'ruins dig', False, "ph_has_shovel(state, player)"],
    ['ruins', 'ruins water', False, "ph_has_kings_key(state, player)"],
    ['ruins water', 'mutoh', False, None],

    # ================= Mutoh's Temple ====================

    ['mutoh', 'mutoh hammer', False, "ph_has_hammer(state, player)"],
    ['mutoh hammer', 'mutoh water', False, "ph_mutoh_water(state, player)"],
    ['mutoh water', 'mutoh bk chest', False, "any([ph_has_small_keys(state, player, 'Mutoh's Temple', 2),ph_ut_small_key_own_dungeon(state, player)])"],
    ['mutoh water', 'mutoh eox', False, "ph_has_boss_key(state, player, 'Mutoh's Temple')"],
    ['mutoh bk chest', 'mutoh eox', False, "ph_is_ut(state, player)"],

    # ================= Maze Island ====================

    ['maze', 'maze east', False, "ph_has_explosives(state, player)"],
    ['maze', 'maze normal', False, "ph_has_bow(state, player)"],
    ['maze normal', 'maze expert', False, "ph_has_grapple(state, player)"],

    # Goal stuff
    ['mercay island', 'beat required dungeons', False, "ph_beat_required_dungeons(state, player)"],
    ['sw ocean east', 'bellumbeck', False, "ph_bellumbeck_quick_finish(state, player)"],
    ['bellumbeck', 'beat bellumbeck', False, "ph_can_beat_bellumbeck(state, player)"],
    ['beat bellumbeck', 'goal', False, "ph_option_goal_bellum(state, player)"],
    ['totok midway', 'goal', False, "ph_option_goal_midway(state, player)"]
]

# New format : dict of region -> dict of connection + requirements
new_logic: dict[str, dict[str, str]] = {}
for reg1, reg2, _, logic in overworld_logic:
    new_logic.setdefault(reg1, {})
    new_logic[reg1][reg2] = logic

for reg1, data in new_logic.items():
    print(f"{reg1} has exit to:")
    for reg2, logic in data.items():
        if logic is None:
            print(f"\t- {reg2}")
        else:
            print(f"\t- {reg2}, {logic}")
