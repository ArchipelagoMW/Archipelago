from BaseClasses import MultiWorld, Item
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import SpiritTracksOptions


def make_overworld_logic(player: int, origin_name: str, options: SpiritTracksOptions):
    overworld_logic = [



        # ====== Aboda Village ==============

        #[region 1, region 2, two-directional, logic requirements],
        ["aboda village", "aboda village rocks", False, None],
        #["aboda village", "aboda village stamp book", False, None],
        ["aboda village", "aboda village stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["aboda village", "aboda village bees", False, None],
        ["aboda village", "forest realm", False, None],

        # # ======== Castle Town =========

        ["forest realm", "castle town", False, None],
        ["castle town", "castle town stamp station", True, lambda state: st_has_stamp_book(state, player)],

        # # ========== ToS ===================

        ["forest realm", "tos", False, None],
        ["tos", "goal", False, lambda state: st_has_sword(state, player)],

        # # ============ Shops ====================

        # ["mercay island", "shop power gem", False, lambda state: st_can_buy_gem(state, player)],
        # ["mercay island", "shop quiver", False, lambda state: st_can_buy_quiver(state, player)],
        # ["mercay island", "shop bombchu bag", False, lambda state: st_can_buy_chu_bag(state, player)],
        # ["mercay island", "shop heart container", False, lambda state: st_can_buy_heart(state, player)],

        # # ============ SW Ocean =================


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
