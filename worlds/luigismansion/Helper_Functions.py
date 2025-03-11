from typing import NamedTuple, Optional


class LMRamData(NamedTuple):
    ram_addr: int = None
    bit_flag: bool = None
    bit_position: int = None
    ram_byte_size: int = None
    pointer_offset: Optional[int] = None
    in_game_room_id: Optional[int] = None