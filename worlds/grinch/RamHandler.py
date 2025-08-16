from typing import NamedTuple, Optional


class GrinchRamData(NamedTuple):
    ram_address: int
    value: Optional[int] = None #none is empty/null
    # Either set or add either hex or unsigned values through Client.py
    # Hex uses 0x00, unsigned are base whole numbers
    binary_bit_pos: Optional[int] = None
    bit_size: int = 1
    update_existing_value: bool = False
    max_count: int = 0