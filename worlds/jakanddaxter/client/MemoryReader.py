import random
import typing
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound, ProcessError, MemoryReadError, WinAPIError
import json

from CommonClient import logger
from worlds.jakanddaxter.locs import CellLocations as Cells, ScoutLocations as Flies, SpecialLocations as Specials

# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1

next_cell_index_offset = 0  # Each of these is an uint64, so 8 bytes.
next_buzzer_index_offset = 8  # Each of these is an uint64, so 8 bytes.
next_special_index_offset = 16  # Each of these is an uint64, so 8 bytes.

cells_checked_offset = 24
buzzers_checked_offset = 428  # cells_checked_offset + (sizeof uint32 * 101 cells)
specials_checked_offset = 876  # buzzers_checked_offset + (sizeof uint32 * 112 buzzers)

buzzers_received_offset = 1004  # specials_checked_offset + (sizeof uint32 * 32 specials)
specials_received_offset = 1020  # buzzers_received_offset + (sizeof uint8 * 16 levels (for scout fly groups))

died_offset = 1052  # specials_received_offset + (sizeof uint8 * 32 specials)

deathlink_enabled_offset = 1053  # died_offset + sizeof uint8

end_marker_offset = 1054  # deathlink_enabled_offset + sizeof uint8


# "Jak" to be replaced by player name in the Client.
def autopsy(died: int) -> str:
    assert died > 0, f"Tried to find Jak's cause of death, but he's still alive!"
    if died in [1, 2, 3, 4]:
        return random.choice(["Jak said goodnight.",
                              "Jak stepped into the light.",
                              "Jak gave Daxter his insect collection.",
                              "Jak did not follow Step 1."])
    if died == 5:
        return "Jak fell into an endless pit."
    if died == 6:
        return "Jak drowned in the spicy water."
    if died == 7:
        return "Jak tried to tackle a Lurker Shark."
    if died == 8:
        return "Jak hit 500 degrees."
    if died == 9:
        return "Jak took a bath in a pool of dark eco."
    if died == 10:
        return "Jak got bombarded with flaming 30-ton boulders."
    if died == 11:
        return "Jak hit 800 degrees."
    if died == 12:
        return "Jak ceased to be."
    if died == 13:
        return "Jak got eaten by the dark eco plant."
    if died == 14:
        return "Jak burned up."
    if died == 15:
        return "Jak hit the ground hard."
    if died == 16:
        return "Jak crashed the zoomer."
    if died == 17:
        return "Jak got Flut Flut hurt."
    if died == 18:
        return "Jak poisoned the whole darn catch."

    return "Jak died."


class JakAndDaxterMemoryReader:
    marker: typing.ByteString
    goal_address = None
    connected: bool = False
    initiated_connect: bool = False

    # The memory reader just needs the game running.
    gk_process: pymem.process = None

    location_outbox = []
    outbox_index: int = 0
    finished_game: bool = False

    # Deathlink handling
    deathlink_enabled: bool = False
    send_deathlink: bool = False
    cause_of_death: str = ""

    def __init__(self, marker: typing.ByteString = b'UnLiStEdStRaTs_JaK1\x00'):
        self.marker = marker
        self.connect()

    async def main_tick(self,
                        location_callback: typing.Callable,
                        finish_callback: typing.Callable,
                        deathlink_callback: typing.Callable,
                        deathlink_toggle: typing.Callable):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)  # Ping to see if it's alive.
            except (ProcessError, MemoryReadError, WinAPIError):
                logger.error("The gk process has died. Restart the game and run \"/memr connect\" again.")
                self.connected = False
        else:
            return

        # Save some state variables temporarily.
        old_deathlink_enabled = self.deathlink_enabled

        # Read the memory address to check the state of the game.
        self.read_memory()

        # Checked Locations in game. Handle the entire outbox every tick until we're up to speed.
        if len(self.location_outbox) > self.outbox_index:
            location_callback(self.location_outbox)
            self.outbox_index += 1

        if self.finished_game:
            finish_callback()

        if old_deathlink_enabled != self.deathlink_enabled:
            deathlink_toggle()
            logger.debug("Toggled DeathLink " + ("ON" if self.deathlink_enabled else "OFF"))

        if self.send_deathlink:
            deathlink_callback()

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")  # The GOAL Kernel
            logger.info("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            logger.error("Could not find the gk process.")
            self.connected = False
            return

        # If we don't find the marker in the first loaded module, we've failed.
        modules = list(self.gk_process.list_modules())
        marker_address = pattern.pattern_scan_module(self.gk_process.process_handle, modules[0], self.marker)
        if marker_address:
            # At this address is another address that contains the struct we're looking for: the game's state.
            # From here we need to add the length in bytes for the marker and 4 bytes of padding,
            # and the struct address is 8 bytes long (it's a uint64).
            goal_pointer = marker_address + len(self.marker) + 4
            self.goal_address = int.from_bytes(self.gk_process.read_bytes(goal_pointer, sizeof_uint64),
                                               byteorder="little",
                                               signed=False)
            logger.info("Found the archipelago memory address: " + str(self.goal_address))
            self.connected = True
        else:
            logger.error("Could not find the archipelago memory address.")
            self.connected = False

        if self.connected:
            logger.info("The Memory Reader is ready!")

    def print_status(self):
        logger.info("Memory Reader Status:")
        logger.info("   Game process ID: " + (str(self.gk_process.process_id) if self.gk_process else "None"))
        logger.info("   Game state memory address: " + str(self.goal_address))
        logger.info("   Last location checked: " + (str(self.location_outbox[self.outbox_index])
                                                    if self.outbox_index else "None"))

    def read_memory(self) -> typing.List[int]:
        try:
            next_cell_index = int.from_bytes(
                self.gk_process.read_bytes(self.goal_address, sizeof_uint64),
                byteorder="little",
                signed=False)
            next_buzzer_index = int.from_bytes(
                self.gk_process.read_bytes(self.goal_address + next_buzzer_index_offset, sizeof_uint64),
                byteorder="little",
                signed=False)
            next_special_index = int.from_bytes(
                self.gk_process.read_bytes(self.goal_address + next_special_index_offset, sizeof_uint64),
                byteorder="little",
                signed=False)

            for k in range(0, next_cell_index):
                next_cell = int.from_bytes(
                    self.gk_process.read_bytes(
                        self.goal_address + cells_checked_offset + (k * sizeof_uint32),
                        sizeof_uint32),
                    byteorder="little",
                    signed=False)
                cell_ap_id = Cells.to_ap_id(next_cell)
                if cell_ap_id not in self.location_outbox:
                    self.location_outbox.append(cell_ap_id)
                    logger.debug("Checked power cell: " + str(next_cell))

            for k in range(0, next_buzzer_index):
                next_buzzer = int.from_bytes(
                    self.gk_process.read_bytes(
                        self.goal_address + buzzers_checked_offset + (k * sizeof_uint32),
                        sizeof_uint32),
                    byteorder="little",
                    signed=False)
                buzzer_ap_id = Flies.to_ap_id(next_buzzer)
                if buzzer_ap_id not in self.location_outbox:
                    self.location_outbox.append(buzzer_ap_id)
                    logger.debug("Checked scout fly: " + str(next_buzzer))

            for k in range(0, next_special_index):
                next_special = int.from_bytes(
                    self.gk_process.read_bytes(
                        self.goal_address + specials_checked_offset + (k * sizeof_uint32),
                        sizeof_uint32),
                    byteorder="little",
                    signed=False)

                # 112 is the game-task ID of `finalboss-movies`, which is written to this array when you grab
                # the white eco. This is our victory condition, so we need to catch it and act on it.
                if next_special == 112 and not self.finished_game:
                    self.finished_game = True
                    logger.info("Congratulations! You finished the game!")
                else:

                    # All other special checks handled as normal.
                    special_ap_id = Specials.to_ap_id(next_special)
                    if special_ap_id not in self.location_outbox:
                        self.location_outbox.append(special_ap_id)
                        logger.debug("Checked special: " + str(next_special))

            died = int.from_bytes(
                self.gk_process.read_bytes(self.goal_address + died_offset, sizeof_uint8),
                byteorder="little",
                signed=False)

            if died > 0:
                self.send_deathlink = True
                self.cause_of_death = autopsy(died)

            deathlink_flag = int.from_bytes(
                self.gk_process.read_bytes(self.goal_address + deathlink_enabled_offset, sizeof_uint8),
                byteorder="little",
                signed=False)

            # Listen for any changes to this setting.
            self.deathlink_enabled = bool(deathlink_flag)

        except (ProcessError, MemoryReadError, WinAPIError):
            logger.error("The gk process has died. Restart the game and run \"/memr connect\" again.")
            self.connected = False

        return self.location_outbox

    def save_data(self):
        with open("jakanddaxter_location_outbox.json", "w+") as f:
            dump = {
                "outbox_index": self.outbox_index,
                "location_outbox": self.location_outbox
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        try:
            with open("jakanddaxter_location_outbox.json", "r") as f:
                load = json.load(f)
                self.outbox_index = load["outbox_index"]
                self.location_outbox = load["location_outbox"]
        except FileNotFoundError:
            pass
