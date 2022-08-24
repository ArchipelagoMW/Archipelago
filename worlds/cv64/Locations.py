import typing

from BaseClasses import Location
from .Names import LocationName


class CV64Location(Location):
    game: str = "Castlevania 64"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None, prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit  = prog_bit
        self.inverted_bit  = invert


forest_location_table = {
    LocationName.forest_main_torch1:  0xC64001,
    LocationName.forest_main_torch2:  0xC64002,
    LocationName.forest_main_torch3:  0xC64003,
    LocationName.forest_main_torch4:  0xC64004,
    LocationName.forest_main_torch5:  0xC64005,
    LocationName.forest_main_torch6:  0xC64006,
    LocationName.forest_main_torch7:  0xC64007,
    LocationName.forest_main_torch8:  0xC64008,
    LocationName.forest_main_torch9:  0xC64009,
    LocationName.forest_main_torch10: 0xC6400A,
    LocationName.forest_main_torch11: 0xC6400B,
    LocationName.forest_main_torch12: 0xC6400C,
    LocationName.forest_main_torch13: 0xC6400D,
    LocationName.forest_main_torch14: 0xC6400E,
    LocationName.forest_main_torch15: 0xC6400F,
    LocationName.forest_main_torch16: 0xC64010,
    LocationName.forest_main_torch17: 0xC64011,
    LocationName.forest_main_torch18: 0xC64012,
    LocationName.forest_main_torch19: 0xC64013,
    LocationName.forest_main_torch20: 0xC64014,
}

cw_location_table = {
    LocationName.cw_main_torch1: 0xC64015,
    LocationName.cw_main_torch2: 0xC64016,
    LocationName.cw_main_torch3: 0xC64017,
    LocationName.cw_main_torch4: 0xC64018,
    LocationName.cw_main_torch5: 0xC64019,
    LocationName.cw_main_torch6: 0xC6401A,
    LocationName.cw_main_torch7: 0xC6401B,
    LocationName.cw_main_torch8: 0xC6401C,
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
