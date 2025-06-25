"""
This module defines a class TitsTheThirdMemoryIO, which attaches
itself to an open Trails in the Sky the 3rd process and
reads/writes memory in realtime. This is used to:
 - Recognize when a player gets an item
 - Write items / abilities to the player's inventory
 - Handle in game flags when a player recieves an AP item.
 - Activate certain in game events.
 - etc...
"""

import asyncio
from dataclasses import dataclass
import json
import os
import struct
from typing import Any, Dict, List, Literal, Optional

from pymem import pymem

from CommonClient import logger
from worlds.tits_the_3rd import TitsThe3rdWorld
from worlds.tits_the_3rd.util import load_file

# TODO:
# - Writes require adding the base address, while reads do not. Make this consistent.

@dataclass
class ScenaFunction():
    """
    Python representation of a scena function used by Trails in the Sky the 3rd.
    """
    # The number used to import the scena file in the scp statement.
    #   eg. scp X
    import_number: int

    # The offset of the function within the scena file.
    offset: int

    # The name of the function for documentation purposes. Must be unique.
    #   Scena functions will be called through their designated function name
    #   in this module.
    function_name: str


class TitsThe3rdMemoryIO():
    """
    TitsThe3rdMemoryIO serves as an interface for interfacing with the Trails in the Sky
    the 3rd game instance. It does this by reading / writing memory to and from the game
    instance, as well as starting threads to activate certain game functionalities.
    """

    OFFSET_FLAG_0: int = 0x2AD491C
    OFFSET_WPID: int = OFFSET_FLAG_0 + (9504 // 8) # Flag 9504 - 9536
    FLAG_SHOULD_WRITE_WPID: int = 9496
    OFFSET_ITEMS_RECEIVED_INDEX = OFFSET_FLAG_0 + (1024 // 8)
    CHARACTER_ID_TO_NAME = {
        0: "estelle",
        1: "joshua",
        2: "scherazard",
        3: "olivier",
        4: "kloe",
        5: "agate",
        6: "tita",
        7: "zin",
        8: "kevin",
        9: "anelace",
        10: "josette",
        11: "richard",
        12: "mueller",
        13: "julia",
        14: "ries",
        15: "renne",
    }
    RECIPE_ID_TO_NAME = {1: "easy_paella"}

    def __init__(self, exit_event: asyncio.Event):
        self.tits_the_3rd_mem: pymem.Pymem = None
        self.tits_the_3rd_pid: int = None
        self.exit_event = exit_event
        self.scena_functions: Dict[str, ScenaFunction] = self._read_custom_scena_functions()
        self.scena_offsets: Dict[bytes, int] = dict()

        # Used for starting threads at the start of scena functions for starting events in game.
        self.scena_caller_alloc: Any = None

    def __del__(self):
        if self.is_connected() and self.scena_caller_alloc:
            self.tits_the_3rd_mem.free(self.scena_caller_alloc)

    def _get_scena_folder(self) -> str:
        """
        Returns the folder the game's patched scena files are located in.

        Returns (str): The path to the AP instance's scena directory.
        """
        # TODO: Custom path dependant on game instance.
        path = os.path.join(TitsThe3rdWorld.settings.game_installation_path, "data", "ED6_DT21")
        if not os.path.exists(path):
            raise ValueError(f"Unable to locate scena directory {path}")
        return path

    def _read_custom_scena_functions(self) -> Dict[str, ScenaFunction]:
        """
        Populate our custom scena function table, which will be used to interface with the game.

        Returns (Dict[str, ScenaFunction]): A mapping of function names to ScenaFunction data structs.
        """
        scena_folder = self._get_scena_folder()
        scena_functions = {}
        scena_table = json.loads(load_file("data/scena_table.json"))
        for file in scena_table:
            scena_file_path = os.path.join(scena_folder, file)
            import_number = scena_table[file]["importNumber"]
            function_offsets = self._get_scena_file_offsets(scena_file_path)
            for function in scena_table[file]["functions"]:
                function_name = function["functionName"]
                if function_name in scena_functions:
                    raise ValueError(f"Duplicate scena function name: {function_name}")
                scena = ScenaFunction(
                    import_number=import_number,
                    offset=function_offsets[function["functionNumber"]],
                    function_name=function_name
                )
                scena_functions[function_name] = scena
        return scena_functions

    def _get_scena_file_offsets(self, scena_file_path: str) -> List[int]:
        function_offsets = []
        function_table_pointer_offset = 0x60
        try:
            with open(scena_file_path, "rb") as fp:
                fp.seek(function_table_pointer_offset)
                function_table_offset = int.from_bytes(fp.read(2), byteorder="little")
                num_functions = int.from_bytes(fp.read(2), byteorder="little") // 2
                fp.seek(function_table_offset)
                for _ in range(num_functions):
                    function_offsets.append(int.from_bytes(fp.read(2), byteorder="little"))
        except FileNotFoundError as err:
            logger.info("Unable to find %s", scena_file_path)
            raise err
        return function_offsets

    def _read_bytes(self, offset, length):
        """
        Read length byte of data at <base_process_address> + offset and return it.

        offset (int): the offset to read data from.
        returns: The data represented as a byte string
        """
        data = self.tits_the_3rd_mem.read_bytes(self.tits_the_3rd_mem.base_address + offset, length)
        return data

    def _read_int(self, offset, byteorder: Literal["little", "big"] = "big", signed: bool = False):
        """
        Read 4 bytes at the specified offset, and interpret it as an int.

        offset (int): the offset to read data from.
        returns: The data represented as a float.
        """
        data = self._read_bytes(offset, 4)
        return int.from_bytes(data, byteorder, signed=signed)

    def _read_short(self, offset, byteorder: Literal["little", "big"] = "big", signed: bool = False):
        """
        Read 2 bytes at the specified offset, and interpret it as an int.

        offset (int): the offset to read data from.
        returns: The data represented as a float.
        """
        data = self._read_bytes(offset, 2)
        return int.from_bytes(data, byteorder, signed=signed)

    def _read_byte(self, offset, byteorder: Literal["little", "big"] = "big", signed: bool = False):
        """
        Read 1 byte at the specified offset, and interpret it as an int.

        offset (int): the offset to read data from.
        returns: The data represented as a float.
        """
        data =self._read_bytes(offset, 1)
        return int.from_bytes(data, byteorder, signed=signed)

    def is_connected(self):
        """Returns True if the class instance is currently connected to the game."""
        if self.tits_the_3rd_mem is None:
            return False

        # confirm the process is still running
        try:
            self._read_int(0)
        except pymem.exception.ProcessError:
            logger.info("Lost connection with Trails in the Sky the 3rd game instance.")
            self.tits_the_3rd_pid = None
            self.tits_the_3rd_mem = None
            return False
        return True

    def is_in_event(self):
        """Returns True if player is current in an event or text box"""
        EVENT_OFFSET = 0x02AD48A4
        return self._read_int(EVENT_OFFSET) != 0x0000FF00

    def is_in_battle(self):
        """Returns True if player is currently in battle"""
        BATTLE_OFFSET = 0x67D644
        return self._read_short(BATTLE_OFFSET, "little") != 0

    def is_valid_to_receive_item(self):
        """Returns True if the player is not currently in an event or battle"""
        return not self.is_in_event() and not self.is_in_battle()

    async def connect(self):
        """
        Connect is a blocking method which waits until it finds a
        Trails in the Sky the 3rd game instance. This can be used
        to wait until the user opens the game.

        Args:
            exit_event (asyncio.Event): The AP client exit event, signaling the
                                        player has closed the client.
        """
        logger.info("Waiting for connection to Trails in the Sky the 3rd game instance...")
        while not self.exit_event.is_set():
            try:
                self.tits_the_3rd_mem = pymem.Pymem("ed6_win3_DX9.exe")
                self.tits_the_3rd_pid = self.tits_the_3rd_mem.process_id
                self.allocate()
                logger.info("Successfully connected to Trails in the Sky the 3rd Game.")
                return
            except pymem.exception.ProcessNotFound:
                await asyncio.sleep(3)

    def call_scena(self, scena: ScenaFunction):
        """
        This function calls a scena function in game.
        This should be used to start custom behaviour in the game.

        Args:
            scena (ScenaFunction): The scena function to be called.
        """
        # Typically, we would want to use something like keystone for building our assembly code.
        #   But at the time of writing AP doesn't currently support adding new libraries for unmerged integrations.
        #   So build the assembly code manually instead.

        # from keystone import keystone
        # architecture = keystone.KS_ARCH_X86
        # mode = keystone.KS_MODE_32
        # endianess = keystone.KS_MODE_LITTLE_ENDIAN
        # ks = keystone.Ks(architecture, mode | endianess)
        # text_message_injection_ks = \
        #     f"mov dword ptr [{self.tits_the_3rd_mem.base_address + int(0x2AD48AA)}],{(0xFFFF << 16 | scena.offset)};" +\
        #     f"mov dword ptr [{self.tits_the_3rd_mem.base_address + int(0x2AD48A4)}],{hex(scena.import_number << 16 | 0x001B)};" +\
        #     "ret;"
        # text_message_injection_ks = text_message_injection_ks.encode()
        # text_message_injection_ks, _ = ks.asm(text_message_injection_ks)
        # text_message_injection_ks = bytes(text_message_injection_ks)

        def convert_le(val) -> list[bytes]:
            # Return the little endian representation of val, as a list of bytes, intepreted as an unsigned integer.
            return list(struct.pack('<I', val))

        # Statements in order:
        # - mov dword ptr [address], value
        # - mov dword ptr [address], value
        # - ret
        text_message_injection =\
            [0xC7, 0x05] +\
            convert_le(self.tits_the_3rd_mem.base_address + int(0x2AD48AA)) +\
            convert_le(0xFFFF << 16 | scena.offset)
        text_message_injection +=\
            [0xC7, 0x05] +\
            convert_le(self.tits_the_3rd_mem.base_address + int(0x2AD48A4)) +\
            convert_le(scena.import_number << 16 | 0x001B)
        text_message_injection += [0xC3]
        text_message_injection = bytes(text_message_injection)

        self.tits_the_3rd_mem.write_bytes(
            self.scena_caller_alloc,
            text_message_injection,
            len(text_message_injection)
        )
        self.tits_the_3rd_mem.start_thread(self.scena_caller_alloc)

    def allocate(self):
        """Allocate memory on the game process which we want to write to later."""
        self.scena_caller_alloc = self.tits_the_3rd_mem.allocate(150)

    def read_flag(self, flag_number: int) -> bool:
        """
        Read a provided flag value.
        In the scena file, this is refered to as flag[X] where X is the flag number.

        Args:
            flag_number (int): The number of the flag to read.

        Returns:
            bool: The value of the flag. True if the flag is set, False otherwise.
        """
        flag_byte_offset = self.OFFSET_FLAG_0 + (flag_number // 8)
        flag_bit = flag_number % 8
        data = self._read_byte(flag_byte_offset)
        flag_value = (data >> flag_bit) & 1
        return bool(flag_value)

    def write_flag(self, flag_number: int, value: bool) -> bool:
        """
        Write a provided flag value.
        In the scena file, this is refered to as flag[X] where X is the flag number.

        Args:
            flag_number (int): The number of the flag to write.

        Returns:
           bool: True if the flag was written successfully, False otherwise.
        """
        flag_byte_offset = self.OFFSET_FLAG_0 + (flag_number // 8)
        flag_bit = flag_number % 8
        byte_data = self._read_byte(flag_byte_offset)
        mask = 1 << flag_bit
        if value:
            # Set the bit to 1
            byte_data = byte_data | mask
        else:
            # Set the bit to 0
            byte_data = byte_data & (~mask)
        byte_data = byte_data.to_bytes(1, "little")
        self.tits_the_3rd_mem.write_bytes(self.tits_the_3rd_mem.base_address + flag_byte_offset, byte_data, 1)
        return self.read_flag(flag_number) == value

    def write_world_player_identifier(self, wpid: bytes) -> bool:
        """
        This identifier is used to validate that the player is
        loaded into the correct save. It is written on new-game,
        and must match in order for items to be sent or received.

        Args:
            wpid (bytes): The per-world player identifier to write.
                          Must be 4 bytes long

        Returns:
            bool: True if the per-world player identifier was written successfully, False otherwise.
        """
        if len(wpid) != 4:
            raise ValueError("wpid must be 4 bytes long")
        self.tits_the_3rd_mem.write_bytes(self.tits_the_3rd_mem.base_address + self.OFFSET_WPID, wpid, 4)
        self.write_last_item_receive_index(-1)
        if not self.read_world_player_identifier() == wpid:
            logger.info(f"Failed to write world player identifier: {self.read_world_player_identifier()} != {wpid}")
            logger.error("Failed to write world player identifier")
            return False
        return self.write_flag(self.FLAG_SHOULD_WRITE_WPID, False)

    def read_world_player_identifier(self) -> bytes:
        """
        Read the per-world player identifier from the game process.

        Returns:
            bytes: The per-world player identifier.
        """
        return self._read_bytes(self.OFFSET_WPID, 4)

    def read_last_item_receive_index(self) -> int:
        return self._read_short(self.OFFSET_ITEMS_RECEIVED_INDEX, "little", signed=True)

    def write_last_item_receive_index(self, index: int):
        self.tits_the_3rd_mem.write_bytes(self.tits_the_3rd_mem.base_address + self.OFFSET_ITEMS_RECEIVED_INDEX, index.to_bytes(2, "little", signed=True), 2)

    def should_write_world_player_identifier(self) -> bool:
        """
        Returns True if the per-world player identifier should be written.
        This is a custom flag set on new game, which is wiped when we write the identifier to memory.
        """
        return self.read_flag(self.FLAG_SHOULD_WRITE_WPID)

    def should_send_and_recieve_items(self, wpid: bytes) -> bool:
        """
        Returns True if the player should send or recieve items.
        This is a santiy check to ensure the player is on the correct save, which started from a new game for the AP.
        If this is the case, the correct world player identifier will be in the flag data.

        Args:
            wpid (bytes): The per-world player identifier to check.

        Returns:
            bool: True if the player should send or recieve items, False otherwise.
        """
        return self.read_world_player_identifier() == wpid

    def get_scena_offset(self, scena_id: bytes) -> Optional[int]:
        """Get and verify a cached scena offset. Find and cache if it does not exist"""
        if scena_id not in self.scena_offsets:
            address = self.tits_the_3rd_mem.pattern_scan_all(scena_id)
            if not address:
                logger.error(f"Could not find signature {scena_id.decode()}. Is the game running?")
                return None
            self.scena_offsets[scena_id] = address

        if self.tits_the_3rd_mem.read_bytes(self.scena_offsets[scena_id], len(scena_id)) != scena_id:
            del self.scena_offsets[scena_id]
            address = self.tits_the_3rd_mem.pattern_scan_all(scena_id)
            if not address:
                logger.error(f"Could not find signature {scena_id.decode()}. Is the game running?")
                return None
            self.scena_offsets[scena_id] = address

        return self.scena_offsets[scena_id]

    def give_item(self, item_id: int, amount: int):
        """Function to give an item to the player in game"""
        address = self.get_scena_offset(b"AP Item Receive Notification")
        if address is None:
            return False
        self.tits_the_3rd_mem.write_bytes(address + 30, item_id.to_bytes(2, "little"), 2)
        self.tits_the_3rd_mem.write_bytes(address + 32, amount.to_bytes(2, "little"), 2)
        self.tits_the_3rd_mem.write_bytes(address + 45, item_id.to_bytes(2, "little"), 2)
        self.tits_the_3rd_mem.write_bytes(address + 48, bytes(f"{amount:02d}", encoding="utf8"), 2)
        self.call_scena(self.scena_functions["give_item"])
        return True

    def give_mira(self, amount: int):
        """Function to give mira to the player in game"""
        address: int = self.get_scena_offset(b"AP Mira Receive Notification")
        if not address:
            return False
        self.tits_the_3rd_mem.write_bytes(address + 30, amount.to_bytes(2, "little"), 2)
        self.tits_the_3rd_mem.write_bytes(address + 50, bytes(f"{amount:05d}", encoding="utf8"), 5)
        self.call_scena(self.scena_functions["give_mira"])
        return True

    def give_low_sepith(self, amount: int):
        """Function to give low element sepith to the player in game"""
        address: int = self.get_scena_offset(b"AP Low Sepith Receive Notification")
        if not address:
            return False
        amount_in_bytes = amount.to_bytes(2, "little")
        self.tits_the_3rd_mem.write_bytes(address + 37, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 41, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 45, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 49, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 81, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 103, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 124, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 145, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.call_scena(self.scena_functions["give_low_sepith"])
        return True

    def give_high_sepith(self, amount: int):
        """Function to give high element sepith to the player in game"""
        address: int = self.get_scena_offset(b"AP High Sepith Receive Notification")
        if not address:
            return False
        amount_in_bytes = amount.to_bytes(2, "little")
        self.tits_the_3rd_mem.write_bytes(address + 38, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 42, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 46, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 77, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 99, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 122, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.call_scena(self.scena_functions["give_high_sepith"])
        return True

    def give_all_sepith(self, amount: int):
        """Function to give all types of sepith to the player in game"""
        address: int = self.get_scena_offset(b"AP All Sepith Receive Notification")
        if not address:
            return False
        amount_in_bytes = amount.to_bytes(2, "little")
        self.tits_the_3rd_mem.write_bytes(address + 37, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 41, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 45, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 49, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 53, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 57, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 61, amount_in_bytes, 2)
        self.tits_the_3rd_mem.write_bytes(address + 93, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 115, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 136, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 157, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 178, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 200, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.tits_the_3rd_mem.write_bytes(address + 223, bytes(f"{amount:03d}", encoding="utf8"), 3)
        self.call_scena(self.scena_functions["give_all_sepith"])
        return True

    def send_item(self, item_id: int):
        address: int = self.get_scena_offset(b"AP Item Send Notification")
        if not address:
            return False
        logger.info(f"Sending Item {item_id}")
        self.tits_the_3rd_mem.write_bytes(address + 36, item_id.to_bytes(2, "little"), 2)
        self.call_scena(self.scena_functions["send_item"])
        return True

    def unlock_area(self, area_flag: int):
        if self.write_flag(area_flag, True):
            self.call_scena(self.scena_functions["unlock_area"])
            return True
        return False

    def unlock_character(self, character_id: int):
        character_name = self.CHARACTER_ID_TO_NAME[character_id]
        self.call_scena(self.scena_functions[f"unlock_{character_name}"])
        return True

    def give_recipe(self, recipe_id: int):
        character_name = self.RECIPE_ID_TO_NAME[recipe_id]
        self.call_scena(self.scena_functions[f"unlock_{character_name}"])
        return True
