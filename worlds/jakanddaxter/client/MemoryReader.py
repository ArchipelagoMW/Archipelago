import typing
import subprocess
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound


class JakAndDaxterMemoryReader:
    marker: typing.ByteString
    connected: bool = False
    marked: bool = False

    process = None
    marker_address = None
    goal_address = None

    location_outbox = {}
    outbox_index = 0

    def __init__(self, marker: typing.ByteString = b'UnLiStEdStRaTs_JaK1\x00'):
        self.marker = marker
        self.connected = self.connect()
        if self.connected and self.marker:
            self.marked = self.find_marker()
        pass

    async def main_tick(self, location_callback: typing.Callable):
        self.read_memory()

        # Checked Locations in game. Handle 1 location per tick.
        if len(self.location_outbox) > self.outbox_index:
            await location_callback(self.location_outbox[self.outbox_index])
            self.outbox_index += 1

    def connect(self) -> bool:
        try:
            self.process = pymem.Pymem("gk.exe")  # The GOAL Kernel
            return True
        except ProcessNotFound:
            return False

    def find_marker(self) -> bool:

        # If we don't find the marker in the first module's worth of memory, we've failed.
        modules = list(self.process.list_modules())
        self.marker_address = pattern.pattern_scan_module(self.process.process_handle, modules[0], self.marker)
        if self.marker_address:
            # At this address is another address that contains the struct we're looking for: the game's state.
            # From here we need to add the length in bytes for the marker and 4 bytes of padding,
            # and the struct address is 8 bytes long (it's u64).
            goal_pointer = self.marker_address + len(self.marker) + 4
            self.goal_address = int.from_bytes(self.process.read_bytes(goal_pointer, 8),
                                               byteorder="little",
                                               signed=False)
            return True
        return False

    def read_memory(self) -> typing.Dict:
        pass
