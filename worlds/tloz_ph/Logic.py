from BaseClasses import MultiWorld, Item
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import PhantomHourglassOptions


def make_overworld_logic(player: int, origin_name: str, options: PhantomHourglassOptions):
    overworld_logic = [

        ["totok b6", "goal", False, lambda state: ph_has_spirit(state, player, "Courage")],

        # ====== Mercay Island ==============

        ["mercay island", "mercay dig spot", False, lambda state: ph_has_shovel(state, player)],
        ["mercay island", "mercay zora cave", False, lambda state: ph_has_explosives(state, player)],
        ["mercay zora cave", "mercay zora cave south", False, lambda state: ph_has_bow(state, player)],
        ["mercay island", "sw ocean", False, lambda state: ph_has_sw_sea_chart(state, player)],
        ["mercay island", "totok", False, None],
        ["mercay island", "mercay freedle island", False, lambda state: ph_has_explosives(state, player)],
        ["mercay freedle island", "mercay freedle tunnel chest", False, lambda state: ph_has_range(state, player)],
        ["mercay freedle island", "mercay freedle gift", False, lambda state: ph_has_se_sea_chart(state, player)],
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
        ["totok b2", "totok b2 key", False, lambda state: ph_can_hit_tricky_switches(state, player)],
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
        ["totok b4", "totok b5.5", False, lambda state: all([ph_totok_b5_key_logic(state, player),
                                                             ph_can_hit_bombchu_switches(state, player)])],
        ["totok b5.5", "totok b5.5 chest", False, lambda state: ph_has_shovel(state, player)],
        ["totok b4", "totok b6", False, lambda state: ph_totok_b6(state, player)],
        # B6
        ["totok b6", "totok b6 phantom chest", False, lambda state: ph_has_phantom_sword(state, player)],
        ["totok b6", "totok b6 bow chest", False, lambda state: ph_has_bow(state, player)],

        # ============ TotOK Part 2 =====================



        # ============ Shops ====================
        ["mercay island", "shop power gem", False, lambda state: ph_has_rupees(state, player, 500)],
        ["mercay island", "shop quiver", False, lambda state: ph_can_buy_quiver(state, player)],
        ["mercay island", "shop bombchu bag", False, lambda state: ph_can_buy_chu_bag(state, player)],

        ["mercay island", "shop heart container", False, lambda state: ph_can_buy_heart(state, player)],

        # ============ SW Ocean =================

        ["mercay island", "sw ocean east", False, lambda state: ph_has_sw_sea_chart(state, player)],
        ["sw ocean east", "cannon island", False, None],
        ["sw ocean east", "ember island", False, None],
        ["sw ocean east", "sw ocean crest salvage", False, lambda state: ph_salvage_courage_crest(state, player)],

        # ============ Cannon Island ===============

        ["cannon island", "cannon island salvage arm", False, lambda state: ph_has_courage_crest(state, player)],

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
