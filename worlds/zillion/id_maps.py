from typing import Dict
from zilliandomizer.logic_components.items import Item as ZzItem, \
    id_to_item as useful_id_to_zz_item
from zilliandomizer.utils.loc_name_maps import loc_to_id as pretty_loc_name_to_id
from zilliandomizer.utils import parse_reg_name
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
