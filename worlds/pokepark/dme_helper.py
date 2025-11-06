from worlds.pokepark.adresses import MemoryAddress, MemoryRange


def read_memory(dme, mem: MemoryAddress) -> int:
    final_address = mem.final_address
    if mem.memory_range == MemoryRange.WORD:
        return dme.read_word(final_address)
    if mem.memory_range == MemoryRange.HALFWORD:
        return int.from_bytes(dme.read_bytes(final_address, 2), byteorder='big')
    if mem.memory_range == MemoryRange.BYTE:
        return dme.read_byte(final_address)
    raise ValueError(f"Unknown MemoryRange: {mem.memory_range}")


def write_memory(dme, mem: MemoryAddress, value: int):
    final_address = mem.final_address
    if mem.memory_range == MemoryRange.WORD:
        dme.write_word(final_address, value)
    if mem.memory_range == MemoryRange.HALFWORD:
        dme.write_bytes(final_address, value.to_bytes(2, byteorder='big'))
    if mem.memory_range == MemoryRange.BYTE:
        dme.write_byte(final_address, value)
