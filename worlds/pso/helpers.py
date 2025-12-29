from typing import NamedTuple

class PSORamData(NamedTuple):
    """
    Keep our RAM data organized

    :param ram_addr: address in memory to be written to / read from
    :param bit_position: what position in ram_addr to start operations from
    :param ram_byte_size: how far the memory space extends for this object
    """
    ram_addr: int | None = None
    bit_position: int | None = None
    ram_byte_size: int | None = None
#    pointer_offset: int | None = None
#    item_count: int | None = None