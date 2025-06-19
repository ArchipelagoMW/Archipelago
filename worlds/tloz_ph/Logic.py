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
        ["mercay island", "sw ocean", False, lambda state: ph_has_sea_chart(state, player, "SW")],
        ["mercay island", "totok", False, None],
        ["mercay island", "mercay freedle island", False, lambda state: ph_has_explosives(state, player)],
        ["mercay freedle island", "mercay freedle tunnel chest", False, lambda state: ph_has_range(state, player)],
        ["mercay freedle island", "mercay freedle gift", False, lambda state: ph_has_sea_chart(state, player, "SE")],
        ["mercay island", "mercay yellow guy", False, lambda state: ph_has_courage_crest(state, player)],

        # ======== Mountain Passage =========

        ["mercay island", "mercay passage 1", False, lambda state:
        any([ph_can_cut_small_trees(state, player),
             ph_has_small_keys(state, player, "Mountain Passage", 3)])],
        ["mercay island", "mercay passage 2", False, lambda state: ph_can_reach_MP2(state, player)],

        # ========== TotOK ===================
        ["totok", "totok 1f chart chest", False, lambda state:
        ph_has_small_keys(state, player, "Temple of the Ocean King", 1)],
        # B1
        ["totok", "totok b1", False, lambda state: ph_has_spirit(state, player, "Power")],
        ["totok b1", "totok b1 eye chest", False, lambda state: all([ph_has_grapple(state, player),
                                                                     ph_has_bow(state, player)])],
        ["totok b1", "totok b1 phantom chest", False, lambda state: ph_can_kill_phantoms(state, player)],
        ["totok b1", "totok b1 key", False, lambda state: any([ph_has_explosives(state, player),
                                                               ph_has_grapple(state, player),
                                                               ph_has_boomerang(state, player)])],
        ["totok b1", "totok b2", False, lambda state: ph_has_small_keys(state, player, "Temple of the Ocean King", 2)],
        # B2
        ["totok b2", "totok b2 key", False, lambda state: ph_totok_b2_key(state, player)],
        ["totok b2", "totok b2 bombchu chest", False, lambda state: all([ph_can_hit_bombchu_switches(state, player),
                                                                         ph_has_explosives(state, player)])],
        ["totok b2", "totok b2 phantom chest", False, lambda state: all([ph_has_phantom_sword(state, player),
                                                                         any([ph_can_hit_tricky_switches(state, player),
                                                                              ph_has_explosives(state, player)])])],
        ["totok b2", "totok b3", False, lambda state: ph_has_small_keys(state, player, "Temple of the Ocean King", 3)],
        # B3
        ["totok b3", "totok b3 phantom chest", False, lambda state: all([ph_can_kill_phantoms_traps(state, player),
                                                                         ph_has_grapple(state, player)])],
        ["totok b3", "totok b3 locked chest", False, lambda state:
        ph_has_small_keys(state, player, "Temple of the Ocean King", 4)],
        ["totok b3", "totok b3 bow chest", False, lambda state: ph_has_bow(state, player)],
        ["totok b3", "totok b3.5", False, lambda state: any([ph_has_grapple(state, player),
                                                             ph_has_force_gems(state, player)])],
        ["totok b3.5", "totok b4", False, lambda state: all([ph_has_spirit(state, player, "Wisdom"),
                                                             ph_can_hit_tricky_switches(state, player)])],
        # B4
        ["totok b4", "totok b4 phantom chest", False, lambda state: ph_has_phantom_sword(state, player)],
        ["totok b4", "totok b4 key", False, lambda state: any([ph_has_explosives(state, player),
                                                               ph_can_boomerang_return(state, player)])],
        ["totok b4", "totok b5", False, lambda state: ph_totok_b5_key_logic(state, player)],
        ["totok b5", "totok b5 chest", False, lambda state: all([ph_can_kill_bubble(state, player),
                                                                 ph_has_mid_range(state, player)])],
        ["totok b5 chest", "totok b6", False, None],
        ["totok b4", "totok b5.5", False, lambda state: all([ph_totok_b5_key_logic(state, player),
                                                             ph_can_hit_bombchu_switches(state, player)])],
        ["totok b5.5", "totok b5.5 chest", False, lambda state: ph_has_shovel(state, player)],
        ["totok b5.5", "totok b6", False, None],
        # B6
        ["totok b6", "totok b6 phantom chest", False, lambda state: ph_has_phantom_sword(state, player)],
        ["totok b6", "totok b6 bow chest", False, lambda state: ph_has_bow(state, player)],
        ["totok b6", "totok midway", False, lambda state: ph_has_triforce_crest(state, player)],

        # ============ TotOK Part 2 =====================

        # B7
        ["totok midway", "totok b7", False, lambda state: ph_has_spirit(state, player, "Courage")],
        ["totok b7", "totok b8", False, None],
        ["totok b7", "totok b7 east", False, lambda state: ph_has_grapple(state, player)],
        ["totok b7 east", "totok b7 peg", False, lambda state: ph_has_range(state, player)],
        ["totok b7", "totok b7 phantom", False, lambda state: ph_can_kill_phantoms(state, player)],
        # B8
        ["totok b8", "totok b7 east", False, lambda state: ph_can_hit_switches(state, player)],
        ["totok b8", "totok b9 nw", False, lambda state: any([
            ph_has_totok_crystal(state, player, "Round"),
            ph_has_hammer(state, player)])],
        ["totok b8", "totok b8 phantom", False, lambda state: ph_can_kill_phantoms(state, player)],
        ["totok b8", "totok b8 2 crystals", False, lambda state: ph_totok_b8_2_crystals(state, player)],
        ["totok b8", "totok b9", False, lambda state: ph_totok_b9(state, player)],
        # B9
        ["totok b9", "totok b9 ghosts", False, lambda state: ph_can_hit_switches(state, player)],
        ["totok b9", "totok b9 nw", False, None],
        ["totok b9", "totok b9 phantom", False, lambda state: ph_totok_b9_phantom_kill(state, player)],
        ["totok b9", "totok b9.5", False, lambda state: all([ph_has_totok_crystal(state, player, "Round"),
                                                             ph_has_totok_crystal(state, player, "Triangle")])],
        ["totok b9.5", "totok b10", False, lambda state: ph_totok_b9_phantom_kill(state, player)],
        # B10
        ["totok b10", "totok b10 inner", False, lambda state: ph_has_explosives(state, player)],
        ["totok b10 inner", "totok b10 hammer", False, lambda state: ph_has_hammer(state, player)],
        ["totok b10 inner", "totok b10 phantom", False, lambda state: ph_can_kill_phantoms_traps(state, player)],
        ["totok b10 inner", "totok b10 phantom eyes", False, lambda state: ph_has_grapple(state, player)],
        ["totok b10 inner", "totok b11", False, lambda state: ph_totok_b10_key_logic(state, player)],
        # B11
        ["totok b11", "totok b11 phantom", False, lambda state: ph_has_phantom_sword(state, player)],
        ["totok b11", "totok b12", False, lambda state: ph_totok_b12(state, player)],
        # B12
        ["totok b12", "totok b12 hammer", False, lambda state: ph_has_hammer(state, player)],
        ["totok b12", "totok b12 phantom", False, lambda state: ph_has_phantom_sword(state, player)],
        ["totok b12", "totok b13", False, lambda state: ph_has_force_gems(state, player, 12, 2)],
        # B13
        ["totok b13", "totok before bellum", False, lambda state: ph_totok_b13_door(state, player)],
        ["totok", "totok before bellum", False, lambda state: ph_totok_blue_warp(state, player)],
        # Bellum
        ["totok", "bellum 1", False, lambda state: ph_totok_bellum_staircase(state, player)],
        ["bellum 1", "ghost ship fight", False, lambda state: ph_can_beat_bellum(state, player)],
        ["ghost ship fight", "bellumbeck", False, lambda state: ph_can_beat_ghost_ship_fight(state, player)],
        ["bellumbeck", "beat bellumbeck", False, lambda state: ph_can_beat_bellumbeck(state, player)],


        # ============ Shops ====================

        ["mercay island", "shop power gem", False, lambda state: ph_has_rupees(state, player, 500)],
        ["mercay island", "shop quiver", False, lambda state: ph_can_buy_quiver(state, player)],
        ["mercay island", "shop bombchu bag", False, lambda state: ph_can_buy_chu_bag(state, player)],
        ["mercay island", "shop heart container", False, lambda state: ph_can_buy_heart(state, player)],

        ["sw ocean east", "beedle gem", False, lambda state: ph_has_rupees(state, player, 500)],
        # TODO Calculate actual need
        ["sw ocean east", "beedle bomb bag", False, lambda state: all([ph_has_rupees(state, player, 1000),
                                                                       ph_has_bombs(state, player)])],

        # ============ SW Ocean =================

        ["mercay island", "sw ocean east", False, lambda state: ph_boat_access(state, player)],
        ["sw ocean east", "cannon island", False, None],
        ["sw ocean east", "ember island", False, None],
        ["sw ocean east", "sw ocean crest salvage", False, lambda state: ph_salvage_courage_crest(state, player)],
        ["sw ocean east", "sw ocean west", False, lambda state: ph_can_enter_ocean_sw_west(state, player)],
        ["sw ocean west", "molida island", False, None],
        ["sw ocean west", "spirit island", False, None],
        ["sw ocean west", "sw ocean nyave", False, lambda state: ph_has_cave_damage(state, player)],
        ["sw ocean west", "sw ocean frog phi", False, lambda state: ph_has_cannon(state, player)],
        ["sw ocean east", "sw ocean frog x", False, lambda state: ph_has_cannon(state, player)],

        # ============ Cannon Island ===============

        ["cannon island", "cannon island salvage arm", False, lambda state: ph_has_courage_crest(state, player)],
        ["cannon island", "cannon island dig", False, lambda state: ph_has_shovel(state, player)],

        # =============== Isle of Ember ================

        ["ember island", "ember island dig", False, lambda state: ph_has_shovel(state, player)],
        ["ember island", "ember island grapple", False, lambda state: ph_has_grapple(state, player)],
        ["ember island", "tof 1f", False, None],

        # =============== Temple of Fire =================

        ["tof 1f", "tof 1f keese", False, lambda state: ph_can_kill_bat(state, player)],
        ["tof 1f", "tof 1f maze", False, lambda state: ph_has_small_keys(state, player, "Temple of Fire", 1)],
        ["tof 1f maze", "tof 2f", False, lambda state: ph_can_hit_spin_switches(state, player)],
        # 2F
        ["tof 2f", "tof 1f west", False, lambda state: ph_has_short_range(state, player)],
        ["tof 1f west", "tof 1f sw", False, lambda state: ph_spiral_wall_switches(state, player)],
        ["tof 1f sw", "tof 2f south", False, lambda state: ph_can_kill_bubble(state, player)],
        ["tof 2f south", "tof 3f", False, lambda state: ph_tof_3f(state, player)],
        # 3F
        ["tof 3f", "tof 3f key drop", False, lambda state: ph_has_boomerang(state, player)],
        ["tof 3f key drop", "tof 3f boss key", False, lambda state:
        ph_has_small_keys(state, player, "Temple of Fire", 3)],  # All 3F checks need boomerang
        ["tof 3f boss key", "tof blaaz", False, lambda state: all([
            ph_has_sword(state, player),
            ph_has_boss_key(state, player, "Temple of Fire")])],
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
        ["toc crayk", "molida archery", False, None],

        # =============== Temple of Courage ================

        ["toc", "toc bomb alcove", False, lambda state: ph_has_explosives(state, player)],
        ["toc", "toc b1", False, lambda state: ph_toc_key_doors(state, player, 3, 1)],
        ["toc", "toc hammer clips", False, lambda state: ph_can_hammer_clip(state, player)],
        ["toc b1", "toc b1 grapple", False, lambda state: ph_has_grapple(state, player)],
        ["toc b1", "toc 1f west", False, lambda state: ph_has_explosives(state, player)],
        ["toc b1 grapple", "toc 1f west", False, lambda state: ph_has_bow(state, player)],
        ["toc hammer clips", "toc 1f west", False, None],
        ["toc 1f west", "toc map room", False, lambda state: ph_has_explosives(state, player)],
        ["toc 1f west", "toc 2f beamos", False, lambda state: ph_toc_key_doors(state, player, 3, 2)],
        ["toc 1f west", "toc b1 maze", False, lambda state:
        ph_has_shape_crystal(state, player, "Temple of Courage", "Square")],
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
        ["toc pols 2", "toc bk room", False, lambda state: ph_has_small_keys(state, player, "Temple of Courage", 3)],
        ["toc bk room", "toc bk chest", False, lambda state: ph_has_bow(state, player)],
        ["toc bk room", "toc before boss", False, lambda state: ph_has_boss_key(state, player, "Temple of Courage")],
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


        # Goal stuff
        ["sw ocean east", "beat required dungeons", False, lambda state: ph_beat_required_dungeons(state, player)],
        ["beat bellumbeck", "goal", False, None],

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
