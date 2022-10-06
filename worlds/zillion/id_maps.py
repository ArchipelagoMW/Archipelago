from typing import Dict, Tuple
from zilliandomizer.logic_components.items import Item as ZzItem, \
    item_name_to_id as zz_item_name_to_zz_id, items as zz_items, \
    item_name_to_item as zz_item_name_to_zz_item
from zilliandomizer.options import Chars
from zilliandomizer.utils.loc_name_maps import loc_to_id as pretty_loc_name_to_id
from zilliandomizer.utils import parse_reg_name
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


def make_id_to_others(start_char: Chars) -> Tuple[
    Dict[int, str], Dict[int, int], Dict[int, ZzItem]
]:
    """ returns id_to_name, id_to_zz_id, id_to_zz_item """
    id_to_name: Dict[int, str] = {}
    id_to_zz_id: Dict[int, int] = {}
    id_to_zz_item: Dict[int, ZzItem] = {}

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


loc_name_to_id: Dict[str, int] = {
    name: id_ + base_id
    for name, id_ in pretty_loc_name_to_id.items()
}


def zz_reg_name_to_reg_name(zz_reg_name: str) -> str:
    if zz_reg_name[0] == 'r' and zz_reg_name[3] == 'c':
        row, col = parse_reg_name(zz_reg_name)
        end = zz_reg_name[5:]
        return f"{make_room_name(row, col)} {end.upper()}"
    return zz_reg_name
