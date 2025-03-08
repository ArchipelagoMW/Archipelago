from worlds.pokepark.adresses import MemoryAddress, MemoryRange


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


def write_bit(dme,address: MemoryAddress, bit_mask: int, enable: bool = True):
    """
    Sets or clears bits according to a mask at a memory address, preserving all other bits.

    This function will only modify the bits specified in the bit_mask, leaving all other
    bits in their original state.

    :param dme: Dolphin Memory Engine
    :param address: MemoryAddress object with memory_range attribute
    :param bit_mask: Bit mask (e.g., 0b00010000 for bit 4)
    :param enable: True to set the bits, False to clear them
    """
    final_addr = address.final_address

    if address.memory_range == MemoryRange.BYTE:
        current_value = dme.read_byte(final_addr)
    elif address.memory_range == MemoryRange.HALFWORD:
        current_value = int.from_bytes(dme.read_bytes(final_addr, 2), byteorder='big')
    elif address.memory_range == MemoryRange.WORD:
        current_value = dme.read_word(final_addr)
    else:
        raise ValueError(f"Unknown memory range: {address.memory_range}")

    # Set or clear bits based on the mask
    if enable:
        new_value = current_value | bit_mask  # Set bits using bitwise OR
    else:
        new_value = current_value & ~bit_mask  # Clear bits using bitwise AND with inverted mask

    if new_value == current_value:
        return True

    if address.memory_range == MemoryRange.BYTE:
        dme.write_byte(final_addr, new_value)
    elif address.memory_range == MemoryRange.HALFWORD:
        dme.write_bytes(final_addr, new_value.to_bytes(2, byteorder='big'))
    elif address.memory_range == MemoryRange.WORD:
        dme.write_word(final_addr, new_value)