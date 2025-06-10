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
        ["mercay island", "sw ocean", False, lambda state: ph_has_sw_sea_chart(state, player)],
        ["mercay island", "totok", False, None],
        ["mercay island", "mercay freedle island", False, lambda state: ph_has_explosives(state, player)],
        ["mercay freedle island", "mercay freedle tunnel chest", False, lambda state: ph_has_range(state, player)],

        # ======== Mountain Passage =========

        ["mercay island", "mercay passage 1", False, lambda state:
            any([ph_can_cut_small_trees(state, player),
                ph_has_small_keys(state, player, "Mountain Passage", 3)])],
        ["mercay island", "mercay passage 2", False, lambda state: ph_can_reach_MP2(state, player)],


        # ========== TotOK ===================

        # ============ Shops ====================
        ["mercay island", "shop power gem", False, lambda state: ph_has_rupees(state, player, 500)],
        ["mercay island", "shop quiver", False, lambda state: ph_can_buy_quiver(state, player)],
        ["mercay island", "shop bombchu bag", False, lambda state: ph_can_buy_chu_bag(state, player)],
        ["mercay island", "shop heart container", False, lambda state: ph_can_buy_heart(state, player)],

        # ============ SW Ocean =================

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
