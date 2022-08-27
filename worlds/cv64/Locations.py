import typing

from BaseClasses import Location
from .Names import LocationName


class CV64Location(Location):
    game: str = "Castlevania 64"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    rom_offset: int

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None,
                 prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit = prog_bit
        self.inverted_bit = invert


forest_location_table = {
    LocationName.forest_pillars_right:  0xC64001,
    LocationName.forest_pillars_top:  0xC64002,
    LocationName.forest_bone_mom:  0xC64003,
    LocationName.forest_lgaz_in:  0xC64004,
    LocationName.forest_lgaz_top:  0xC64005,
    LocationName.forest_hgaz_in:  0xC64006,
    LocationName.forest_hgaz_top:  0xC64007,
    LocationName.forest_weretiger_sw:  0xC64008,
    LocationName.forest_weretiger_gate:  0xC64009,
    LocationName.forest_dirge_tomb: 0xC6400A,
    LocationName.forest_corpse_save: 0xC6400B,
    LocationName.forest_dbridge_wall: 0xC6400C,
    LocationName.forest_dbridge_sw: 0xC6400D,
    LocationName.forest_dbridge_gate_r: 0xC6400E,
    LocationName.forest_dbridge_tomb: 0xC6400F,
    LocationName.forest_bface_tomb: 0xC64010,
    LocationName.forest_ibridge: 0xC64011,
    LocationName.forest_werewolf_tomb: 0xC64012,
    LocationName.forest_werewolf_tree: 0xC64013,
    LocationName.forest_final_sw: 0xC64014,
}

cw_location_table = {
    LocationName.cw_bottom_middle: 0xC64015,
    LocationName.cw_rrampart: 0xC64016,
    LocationName.cw_lrampart: 0xC64017,
    LocationName.cw_dragon_sw: 0xC64018,
    LocationName.cw_drac_sw: 0xC64019,
    LocationName.cwr_bottom: 0xC6401A,
    LocationName.cwl_bottom: 0xC6401B,
    LocationName.cwl_bridge: 0xC6401C,
    LocationName.the_end: 0xC64000
}

all_locations = {
    **forest_location_table,
    **cw_location_table,
}

location_table = {}


def setup_locations(world, player: int):
    location_table = {**forest_location_table, **cw_location_table}

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
