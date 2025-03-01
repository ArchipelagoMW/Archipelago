from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import TypedDict

from zilliandomizer.logic_components.items import (
    Item as ZzItem,
    KEYWORD,
    NORMAL,
    RESCUE,
    item_name_to_id as zz_item_name_to_zz_id,
    items as zz_items,
    item_name_to_item as zz_item_name_to_zz_item,
)
from zilliandomizer.logic_components.regions import RegionData
from zilliandomizer.low_resources.item_rooms import item_room_codes
from zilliandomizer.options import Chars
from zilliandomizer.utils.loc_name_maps import loc_to_id as pretty_loc_name_to_id
from zilliandomizer.utils import parse_loc_name, parse_reg_name
from zilliandomizer.zri.memory import RescueInfo

from .config import base_id as base_id

item_name_to_id = {
    "Apple": 0 + base_id,
    "Champ": 1 + base_id,
    "JJ": 2 + base_id,
    "Win": 3 + base_id,
    "Empty": 4 + base_id,
    "ID Card": 5 + base_id,
    "Red ID Card": 6 + base_id,
    "Floppy Disk": 7 + base_id,
    "Bread": 8 + base_id,
    "Opa-Opa": 9 + base_id,
    "Zillion": 10 + base_id,
    "Scope": 11 + base_id,
}


_zz_rescue_0 = zz_item_name_to_zz_item["rescue_0"]
_zz_rescue_1 = zz_item_name_to_zz_item["rescue_1"]
_zz_empty = zz_item_name_to_zz_item["empty"]


def make_id_to_others(start_char: Chars) -> tuple[
    dict[int, str], dict[int, int], dict[int, ZzItem]
]:
    """ returns id_to_name, id_to_zz_id, id_to_zz_item """
    id_to_name: dict[int, str] = {}
    id_to_zz_id: dict[int, int] = {}
    id_to_zz_item: dict[int, ZzItem] = {}

    if start_char == "JJ":
        name_to_zz_item = {
            "Apple": _zz_rescue_0,
            "Champ": _zz_rescue_1,
            "JJ": _zz_empty
        }
    elif start_char == "Apple":
        name_to_zz_item = {
            "Apple": _zz_empty,
            "Champ": _zz_rescue_1,
            "JJ": _zz_rescue_0
        }
    else:  # Champ
        name_to_zz_item = {
            "Apple": _zz_rescue_0,
            "Champ": _zz_empty,
            "JJ": _zz_rescue_1
        }

    for name, ap_id in item_name_to_id.items():
        id_to_name[ap_id] = name

        if ap_id >= 4 + base_id:
            index = ap_id - base_id
            zz_item = zz_items[index]
            assert zz_item.id == index and zz_item.name == name
        elif ap_id < 3 + base_id:
            # rescue
            assert name in {"Apple", "Champ", "JJ"}
            zz_item = name_to_zz_item[name]
        else:  # main
            zz_item = zz_item_name_to_zz_item["main"]

        id_to_zz_id[ap_id] = zz_item_name_to_zz_id[zz_item.debug_name]
        id_to_zz_item[ap_id] = zz_item

    return id_to_name, id_to_zz_id, id_to_zz_item


def make_room_name(row: int, col: int) -> str:
    return f"{chr(ord('A') + row - 1)}-{col + 1}"


loc_name_to_id: dict[str, int] = {
    name: id_ + base_id
    for name, id_ in pretty_loc_name_to_id.items()
}


def zz_reg_name_to_reg_name(zz_reg_name: str) -> str:
    if zz_reg_name[0] == "r" and zz_reg_name[3] == "c":
        row, col = parse_reg_name(zz_reg_name)
        end = zz_reg_name[5:]
        return f"{make_room_name(row, col)} {end.upper()}"
    return zz_reg_name


class ClientRescue(TypedDict):
    start_char: Chars
    room_code: int
    mask: int


class ZillionSlotInfo(TypedDict):
    start_char: Chars
    rescues: dict[str, ClientRescue]
    loc_mem_to_id: dict[int, int]
    """ memory location of canister to Archipelago location id number """


def get_slot_info(regions: Iterable[RegionData],
                  start_char: Chars,
                  loc_name_to_pretty: Mapping[str, str]) -> ZillionSlotInfo:
    items_placed_in_map_index: dict[int, int] = defaultdict(int)
    rescue_locations: dict[int, RescueInfo] = {}
    loc_memory_to_loc_id: dict[int, int] = {}
    for region in regions:
        for loc in region.locations:
            assert loc.item, ("There should be an item placed in every location before "
                              f"writing slot info. {loc.name} is missing item.")
            if loc.item.code in {KEYWORD, NORMAL, RESCUE}:
                row, col, _y, _x = parse_loc_name(loc.name)
                map_index = row * 8 + col
                item_no = items_placed_in_map_index[map_index]
                room_code = item_room_codes[map_index]

                r = room_code
                m = 1 << item_no
                if loc.item.code == RESCUE:
                    rescue_locations[loc.item.id] = RescueInfo(start_char, r, m)
                loc_memory = (r << 7) | m
                loc_memory_to_loc_id[loc_memory] = pretty_loc_name_to_id[loc_name_to_pretty[loc.name]]
                items_placed_in_map_index[map_index] += 1

    rescues: dict[str, ClientRescue] = {}
    for i in (0, 1):
        if i in rescue_locations:
            ri = rescue_locations[i]
            rescues[str(i)] = {
                "start_char": ri.start_char,
                "room_code": ri.room_code,
                "mask": ri.mask
            }
    return {
        "start_char": start_char,
        "rescues": rescues,
        "loc_mem_to_id": loc_memory_to_loc_id
    }
