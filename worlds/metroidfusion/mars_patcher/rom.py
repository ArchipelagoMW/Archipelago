import pkgutil
from enum import Enum
from os import PathLike

from .mf.constants.reserved_space import ReservedConstantsMF
from .zm.constants.reserved_space import ReservedConstantsZM

BytesLike = bytes | bytearray

SIZE_8MB = 0x800000
ROM_OFFSET = 0x8000000


class Game(Enum):
    """The possible GBA games."""

    MF = 1
    """Metroid Fusion"""
    ZM = 2
    """Zero Mission"""


class Region(Enum):
    """The possible regions."""

    U = 1
    """USA"""
    E = 2
    """European"""
    J = 3
    """Japanese"""
    C = 4
    """Chinese"""


class Rom:
    """
    A class dealing with ROM operations, like loading and saving the ROM, or
    reading and writing bytes.

    Attributes:
        game: An enum indicating the current game that is loaded.
        region: An enum indicating the region of the currently loaded game.
        data: A bytearray containing the data from a loaded game.
        free_space_addr: An integer keeping track of the current known address where free space in
                         the game is contained.
    """

    _title_to_game = {
        # Fusion
        "METROID4USA\0AMTE": {
            "game": Game.MF,
            "region": Region.U,
        },
        "METROID4EUR\0AMTP": {
            "game": Game.MF,
            "region": Region.E,
        },
        "METROID4JPN\0AMTJ": {
            "game": Game.MF,
            "region": Region.J,
        },
        "METFUSIONCHNAMTC": {
            "game": Game.MF,
            "region": Region.C,
        },
        # Zero Mission
        "ZEROMISSIONEBMXE": {
            "game": Game.ZM,
            "region": Region.U,
        },
        "ZEROMISSIONPBMXP": {
            "game": Game.ZM,
            "region": Region.E,
        },
        "ZEROMISSIONJBMXJ": {
            "game": Game.ZM,
            "region": Region.J,
        },
        "ZEROMISSIONCBMXC": {
            "game": Game.ZM,
            "region": Region.C,
        },
    }

    def __init__(self, path: str | PathLike[str]):
        # Read file
        with open(path, "rb") as f:
            self.data = bytearray(f.read())
        # Check length
        if len(self.data) != SIZE_8MB:
            raise ValueError("ROM should be 8MB")
        # Check title and code
        title = self.read_ascii(0xA0, 0x10)
        if title not in self._title_to_game:
            raise ValueError("Not a valid GBA Metroid ROM")

        game = self._title_to_game[title]["game"]
        region = self._title_to_game[title]["region"]
        assert isinstance(game, Game)
        assert isinstance(region, Region)
        self.game = game
        self.region = region

        # For now we only allow MF U
        if self.game == Game.ZM:
            raise ValueError("Not compatible with Metroid Zero Mission")
        if self.region != Region.U:
            raise ValueError("Only compatible with the North American (U) version")
        # Set free space address
        if self.is_mf():
            self.free_space_addr = ReservedConstantsMF.PATCHER_FREE_SPACE_ADDR
        elif self.is_zm():
            self.free_space_addr = ReservedConstantsZM.PATCHER_FREE_SPACE_ADDR

    def is_mf(self) -> bool:
        """Returns true when the currently loaded game is Metroid Fusion."""
        return self.game == Game.MF

    def is_zm(self) -> bool:
        """Returns true when the currently loaded game is Metroid Zero Mission."""
        return self.game == Game.ZM

    def read_8(self, addr: int) -> int:
        """Reads one byte from the specified address, and returns the read value."""
        return self.data[addr]

    def read_16(self, addr: int) -> int:
        """Reads two bytes from the specified address, and returns the read value."""
        return self.data[addr] | (self.data[addr + 1] << 8)

    def read_32(self, addr: int) -> int:
        """Reads four bytes from the specified address, and returns the read value."""
        return (
            self.data[addr]
            | (self.data[addr + 1] << 8)
            | (self.data[addr + 2] << 16)
            | (self.data[addr + 3] << 24)
        )

    def read_ptr(self, addr: int) -> int:
        """
        Reads a pointer (four bytes) from the specified address, and returns the read address.
        The return value is adjusted to be used right away, by subtracting the offset on where
        the ROM is loaded in the GBA.

        Raises:
            ValueError: If the pointer that was read does not point to the region where
                        the GBA loads ROMs.
        """
        val = self.read_32(addr)
        if val < ROM_OFFSET:
            raise ValueError(f"Invalid pointer {val:X} at {addr:X}")
        return val - ROM_OFFSET

    def read_bytes(self, addr: int, size: int) -> bytearray:
        """
        Reads a specified amount of bytes from a given address, and returns
        the read values as a bytearray.
        """
        end = addr + size
        return self.data[addr:end]

    def read_ascii(self, addr: int, size: int) -> str:
        """
        Reads a specified amount of bytes from a given addres, and returns
        the read values interpreted as an ASCII string
        """
        return self.read_bytes(addr, size).decode("ascii")

    def write_8(self, addr: int, val: int) -> None:
        """Writes a number as a byte to a specified address."""
        self.data[addr] = val & 0xFF

    def write_16(self, addr: int, val: int) -> None:
        """Writes a number as two bytes (short) to a specified address."""
        val &= 0xFFFF
        self.data[addr] = val & 0xFF
        self.data[addr + 1] = val >> 8

    def write_32(self, addr: int, val: int) -> None:
        """Writes a number as four bytes (int) to a specified address."""
        val &= 0xFFFFFFFF
        self.data[addr] = val & 0xFF
        self.data[addr + 1] = (val >> 8) & 0xFF
        self.data[addr + 2] = (val >> 16) & 0xFF
        self.data[addr + 3] = val >> 24

    def write_ptr(self, addr: int, val: int) -> None:
        """
        Writes a pointer to a specified address. The pointer needs to be less than
        the offset where the ROM is loaded in the GBA.
        """
        assert val < ROM_OFFSET, f"Pointer should be less than {ROM_OFFSET:X} but is {val:X}"
        self.write_32(addr, val + ROM_OFFSET)

    def write_bytes(
        self, data_addr: int, vals: BytesLike, val_addr: int = 0, size: int | None = None
    ) -> None:
        """
        Writes a bytes like object either in full or partially to a specified address.

        Args:
            data_addr: Where to write in the ROM data.
            vals: A bytes like object that should get written.
            val_addr: An index from where vals should begin to start writing. 0 by default.
            size: How many bytes should be written to the ROM. If None is specified,
                  then that means the full length of vals. None by default.
        """
        if size is None:
            size = len(vals) - val_addr
        data_end = data_addr + size
        val_end = val_addr + size
        self.data[data_addr:data_end] = vals[val_addr:val_end]

    def write_16_list(self, addr: int, vals: list[int]) -> int:
        """Writes a list of numbers as 16-bit integers. Does not check if the
        values are within 16-bit range. Returns the ending address."""
        for val in vals:
            self.write_16(addr, val)
            addr += 2
        return addr

    def copy_bytes(self, src_addr: int, dst_addr: int, size: int) -> None:
        """Copies a specified amount of bytes from the source address to the destination address."""
        self.write_bytes(dst_addr, self.data, src_addr, size)

    def reserve_free_space(self, size: int) -> int:
        """
        Returns an address that is able to fit in a specified size.
        Alignment is always 4.
        """
        remain = self.free_space_addr % 4
        if remain != 0:
            self.free_space_addr += 4 - remain
        addr = self.free_space_addr
        self.free_space_addr += size
        # Check if past end of reserved space
        if self.is_mf():
            free_space_end = ReservedConstantsMF.PATCHER_FREE_SPACE_END
        elif self.is_zm():
            free_space_end = ReservedConstantsZM.PATCHER_FREE_SPACE_END
        else:
            raise ValueError(self.game)
        if self.free_space_addr > free_space_end:
            raise RuntimeError("Ran out of reserved free space")
        return addr

    def save(self, path: str | PathLike[str]) -> None:
        """Saves the currently loaded data to a specified path."""
        with open(path, "wb") as f:
            f.write(self.data)
