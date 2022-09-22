from typing import Dict
from zilliandomizer.logic_components.items import Item as ZzItem, \
    id_to_item as useful_id_to_zz_item
from zilliandomizer.low_resources.loc_id_maps import loc_to_id as zz_loc_name_to_id
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


_weird_locations = {
    "r04c1y80x20": ("mid-bottom", "left-left"),
    "r04c1y18x58": ("top", "center-left-center"),
    "r10c5y98x18": ("bottom", "left corner"),
    "r16c2y60x80": ("mid-bottom", "center"),
}


def loc_zz_name_to_name(zz_name: str) -> str:
    row, col, y, x = parse_loc_name(zz_name)
    vertical = "top" if y <= 0x20 \
        else "top-mid" if y <= 0x40 \
        else "mid" if y <= 0x60 \
        else "bottom-mid" if y <= 0x80 \
        else "bottom"
    horizontal = horizontals[x >> 4]
    if zz_name in _weird_locations:
        vertical, horizontal = _weird_locations[zz_name]
    return f"{make_room_name(row, col)} {vertical} {horizontal}"


loc_name_to_id: Dict[str, int] = {
    loc_zz_name_to_name(zz_name): id_ + base_id
    for zz_name, id_ in zz_loc_name_to_id.items()
}
assert len(loc_name_to_id) == len(zz_loc_name_to_id), f"{len(loc_name_to_id)} == {len(zz_loc_name_to_id)}"


def zz_reg_name_to_reg_name(zz_reg_name: str) -> str:
    if zz_reg_name[0] == 'r' and zz_reg_name[3] == 'c':
        row, col = parse_reg_name(zz_reg_name)
        end = zz_reg_name[5:]
        return f"{make_room_name(row, col)} {end.upper()}"
    return zz_reg_name
