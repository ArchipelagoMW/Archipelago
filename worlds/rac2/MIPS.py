
def jal(addr: int) -> bytes:
    if addr is None:
        # If address is None (which can happen in some cases with lists where an address is unspecified for a given
        # planet), put a nop instruction instead to avoid putting a jal that would always crash
        return nop()

    shifted_addr = (addr >> 2) & 0x03FFFFFF
    instruction = 0x0C000000 | shifted_addr
    return instruction.to_bytes(4, 'little')


def jr_ra() -> bytes:
    return bytes([0x08, 0x00, 0xE0, 0x03])


def nop() -> bytes:
    return bytes([0x00, 0x00, 0x00, 0x00])


def get_address_halves(addr: int) -> (bytes, bytes):
    lower_half = addr & 0xFFFF
    upper_half = (addr >> 16) & 0xFFFF
    if lower_half >= 0x8000:
        upper_half += 1
    uhb = upper_half.to_bytes(2, 'little')
    lhb = lower_half.to_bytes(2, 'little')
    return uhb, lhb
