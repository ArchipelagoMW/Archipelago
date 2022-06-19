from typing import Dict
from zilliandomizer.logic_components.items import Item as ZzItem, \
    id_to_item as useful_id_to_zz_item
from zilliandomizer.low_resources.loc_id_maps import loc_to_id as zz_loc_name_to_useful_id
from zilliandomizer.utils import parse_loc_name, parse_reg_name
from .config import base_id


item_useful_id_to_pretty_id: Dict[int, int] = {
    u_i: p_i
    for p_i, u_i in enumerate(useful_id_to_zz_item)
}

item_pretty_id_to_useful_id: Dict[int, int] = {
    p_i: u_i
    for u_i, p_i in item_useful_id_to_pretty_id.items()
}

item_id_to_zz_item: Dict[int, ZzItem] = {
    item_useful_id_to_pretty_id[i] + base_id: item
    for i, item in useful_id_to_zz_item.items()
}

item_name_to_id = {
    z.debug_name: i
    for i, z in item_id_to_zz_item.items()
}


horizontals = [
    "in left wall",
    "far left",
    "left-left",
    "left",
    "left-left-center",  # in split rooms, this col is often occupied by a wall
    "left-center",
    "center-left",  # surprisingly few
    "center",  # more of these
    "center-r",  # than these
    "center-right",   # also few
    "right-center",
    "right-right-center",
    "right",
    "right-right",
    "far right",
    "in right wall",
]


def make_room_name(row: int, col: int) -> str:
    return f"{chr(ord('A') + row - 1)}-{col + 1}"


def loc_zz_name_to_name(zz_name: str) -> str:
    row, col, y, x = parse_loc_name(zz_name)
    vertical = "top" if y <= 0x20 \
        else "top-mid" if y <= 0x40 \
        else "mid" if y <= 0x60 \
        else "bottom-mid" if y <= 0x80 \
        else "bottom"
    horizontal = horizontals[x >> 4]
    return f"{make_room_name(row, col)} {vertical} {horizontal}"


loc_useful_id_to_pretty_id: Dict[int, int] = {
    u_i: p_i
    for p_i, u_i in enumerate(zz_loc_name_to_useful_id.values())
}

loc_name_to_id: Dict[str, int] = {
    loc_zz_name_to_name(zz_name): loc_useful_id_to_pretty_id[u_i] + base_id
    for zz_name, u_i in zz_loc_name_to_useful_id.items()
}


def zz_reg_name_to_reg_name(zz_reg_name: str) -> str:
    if zz_reg_name[0] == 'r' and zz_reg_name[3] == 'c':
        row, col = parse_reg_name(zz_reg_name)
        end = zz_reg_name[5:]
        return f"{make_room_name(row, col)} {end.upper()}"
    return zz_reg_name
