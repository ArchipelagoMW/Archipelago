from logging import Logger
import dolphin_memory_engine


GC_GAME_ID_ADDRESS = 0x80000000


class DolphinException(Exception):
    pass


class DolphinClient:
    dolphin: dolphin_memory_engine
    logger: Logger

    def __init__(self, logger):
        self.dolphin = dolphin_memory_engine
        self.logger = logger

    def is_connected(self):
        try:
            self.__assert_connected()
            return True
        except Exception:
            return False

    def connect(self):
        if not self.dolphin.is_hooked():
            self.dolphin.hook()
        if not self.dolphin.is_hooked():
            raise DolphinException(
                "Could not connect to Dolphin, verify that you have a game running in the emulator")

    def disconnect(self):
        if self.dolphin.is_hooked():
            self.dolphin.un_hook()

    def __assert_connected(self):
        """Custom assert function that returns a DolphinException instead of a generic RuntimeError if the connection is lost"""
        try:
            self.dolphin.assert_hooked()
            # For some reason the dolphin_memory_engine.is_hooked() function doesn't recognize when the game is closed, checking if memory is available will assert the connection is alive
            self.dolphin.read_bytes(GC_GAME_ID_ADDRESS, 1)
        except RuntimeError as e:
            self.disconnect()
            raise DolphinException(e)

    def verify_target_address(self, target_address: int, read_size: int):
        """Ensures that the target address is within the valid range for GC memory"""
        if target_address < 0x80000000 or target_address + read_size > 0x81800000:
            raise DolphinException(
                f"{target_address:x} -> {target_address + read_size:x} is not a valid for GC memory"
            )

    def read_pointer(self, pointer, offset, byte_count):
        self.__assert_connected()

        address = None
        try:
            address = self.dolphin.follow_pointers(pointer, [0])
        except RuntimeError:
            self.logger.debug(f"Could not read pointer at {pointer:x}")
            return None

        if not self.dolphin.is_hooked():
            raise DolphinException("Dolphin no longer connected")

        address += offset
        return self.read_address(address, byte_count)

    def read_address(self, address, bytes_to_read):
        self.__assert_connected()
        self.verify_target_address(address, bytes_to_read)
        result = self.dolphin.read_bytes(address, bytes_to_read)
        return result

    def write_pointer(self, pointer, offset, data):
        self.__assert_connected()
        address = None
        try:
            address = self.dolphin.follow_pointers(pointer, [0])
        except RuntimeError:
            self.logger.debug(f"Could not read pointer at {pointer:x}")
            return None

        if not self.dolphin.is_hooked():
            raise DolphinException("Dolphin no longer connected")

        address += offset
        return self.write_address(address, data)

    def write_address(self, address, data):
        self.__assert_connected()
        result = self.dolphin.write_bytes(address, data)
        return result
