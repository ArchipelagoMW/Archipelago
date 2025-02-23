from worlds.pokepark_1.adresses import MemoryAddress, MemoryRange


def read_memory(dme,mem: MemoryAddress) -> int:
    if mem.memory_range == MemoryRange.WORD:
        return dme.read_word(mem.final_address)
    if mem.memory_range == MemoryRange.HALFWORD:
        return int.from_bytes(dme.read_bytes(mem.final_address, 2), byteorder='big')
    if mem.memory_range == MemoryRange.BYTE:
        return dme.read_byte(mem.final_address)
    raise ValueError(f"Unknown MemoryRange: {mem.memory_range}")

def write_memory(dme,mem: MemoryAddress, value: int):
    if mem.memory_range == MemoryRange.WORD:
        dme.write_word(mem.final_address, value)
    if mem.memory_range == MemoryRange.HALFWORD:
        dme.write_bytes(mem.final_address, value.to_bytes(2, byteorder='big'))
    if mem.memory_range == MemoryRange.BYTE:
        dme.write_byte(mem.final_address, value)