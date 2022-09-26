import typing

from BaseClasses import Location
from .Names import LocationName


class YILocation(Location):
    game: str = "Yoshis Island"

    progress_byte: int = 0x000000
    progress_bit: int = 0

    def __init__(self, player: int, name: str = '', address: int = None, parent =None, prog_byte: int = None, prog_bit: int = None):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit = prog_bit


level_goal_table = {
    LocationName.W1_L1_flowers: 0x16000,
    LocationName.W1_L1_coins: 0x16001,
    LocationName.W1_L1_stars: 0x16002,
    LocationName.W1_L1_clear: 0x16003,

    LocationName.W6_L8_clear: 0x16004,
}


all_locations = {
    **level_goal_table,
}

location_table = {}

def setup_locations(world, player: int):
    location_table = {**level_goal_table}




lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}