from typing import NamedTuple, Optional


class LMRamData(NamedTuple):
    ram_addr: Optional[int] = None
    bit_flag: Optional[bool] = None
    bit_position: Optional[int] = None
    ram_byte_size: Optional[int] = None
    pointer_offset: Optional[int] = None
    in_game_room_id: Optional[int] = None