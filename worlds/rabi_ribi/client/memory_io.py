"""
This module defines a class RabiRibiMemoryIO, which attaches
itself to an open Rabi Ribi process and reads/writes memory
in realtime. This is used to:
 - Recognize when a player gets an item
 - Write items to the player's inventory
 - Handle in game flags when a player recieves an AP item.
 - Modify map data loaded into memory.
 - etc... 
"""
import struct

from pymem import pymem

from CommonClient import logger

offset_player_x = int(0x0103469C)
offset_player_y = int(0x013AFDB4)
tile_length = 64

class RabiRibiMemoryIO():
    def __init__(self):
        try:
            self.rr_mem = pymem.Pymem("rabiribi.exe")
        except pymem.exception.ProcessNotFound as err:
            logger.error("Unable to find Rabi Ribi game process. Is the game open?")
            logger.error(str(err))
            raise err # TODO: handle me when this isnt just a POC
    
    def _read_word(self, offset):
        """
        Read 4 bytes of data at <base_process_address> + offset and return it.

        offset (int): the offset to read data from.
        """
        data = self.rr_mem.read_bytes(self.rr_mem.base_address + offset, 4)
        return data
    
    def _read_float(self, offset):
        """
        Read a word at the specified offset, and intepret it as a float.

        offset (int): the offset to read data from.
        """
        data = self._read_byte(offset)
        return struct.unpack("f", data)[0]
    
    def read_player_tile_position(self):
        """
        Read the player (x,y) and convert it to tile (x,y).
        """
        player_x = self._read_float(offset_player_x)
        player_y = self._read_float(offset_player_y)
        return (int(player_x // tile_length), int(player_y // tile_length))
