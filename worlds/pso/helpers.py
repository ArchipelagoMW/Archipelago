from typing import NamedTuple

from dolphin_memory_engine import read_byte, read_bytes, write_byte, write_bytes

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


def read_short(console_address: int) -> int:
    """
    Read a 2-byte short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(read_bytes(console_address, 2), byteorder="big")


def write_short(console_address: int, value: int) -> None:
    """
    Write a 2-byte short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    write_bytes(console_address, value.to_bytes(2, byteorder="big"))


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()

def set_bit(value, bit):
    """
    Set the specified bit to 1
    """
    # Make the correct value by using Left Shift on 1 until it's in the correct bit position,
    # Ensure it's set to 1 by comparing with OR
    return value | (1 << bit)


def clear_bit(value, bit):
    """
    Set the specified bit to 0
    """
    # Make the correct value by using Left Shift on 1 until it's in the correct bit position,
    # Flip those bits with NOT, and then compare using AND to ensure the specified bit is 0
    return value & ~(1 << bit)


def write_bit(console_address: int, bit_position: int, value: int) -> None:
    """
    Write to a single bit to a specific position in a byte of Dolphin memory.

    :param console_address: Address to write to.
    :param bit_position: Position of the bit in the Dolphin memory.
    :param value: Value to write – 0 or 1
    """
    # If we don't get a binary value, throw an error
    if not value in {0, 1}:
        raise ValueError(f"write_bit only accepts integer values of 0 or 1; got {value}")

    # Grab the current full 8-bit value
    byte_value = read_byte(console_address)

    # Either clear the bit (0) or set the bit (1)
    if value == 0:
        byte_value = clear_bit(byte_value, bit_position)
    else:
        byte_value = set_bit(byte_value, bit_position)

    # Write the new value back to the original address
    write_byte(console_address, byte_value)