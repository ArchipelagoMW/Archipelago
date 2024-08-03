import random
from typing import ByteString, List, Callable
import json
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound, ProcessError, MemoryReadError, WinAPIError
from dataclasses import dataclass

from CommonClient import logger
from ..locs import (OrbLocations as Orbs,
                    CellLocations as Cells,
                    ScoutLocations as Flies,
                    SpecialLocations as Specials,
                    OrbCacheLocations as Caches)

# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1
sizeof_float = 4


# IMPORTANT: OpenGOAL memory structures are particular about the alignment, in memory, of member elements according to
# their size in bits. The address for an N-bit field must be divisible by N. Use this class to define the memory offsets
# of important values in the struct. It will also do the byte alignment properly for you.
# See https://opengoal.dev/docs/reference/type_system/#arrays
@dataclass
class OffsetFactory:
    current_offset: int = 0

    def define(self, size: int, length: int = 1) -> int:

        # If necessary, align current_offset to the current size first.
        bytes_to_alignment = self.current_offset % size
        if bytes_to_alignment != 0:
            self.current_offset += (size - bytes_to_alignment)

        # Increment current_offset so the next definition can be made.
        offset_to_use = self.current_offset
        self.current_offset += (size * length)
        return offset_to_use


# Start defining important memory address offsets here. They must be in the same order, have the same sizes, and have
# the same lengths, as defined in `ap-info-jak1`.
offsets = OffsetFactory()

# Cell, Buzzer, and Special information.
next_cell_index_offset = offsets.define(sizeof_uint64)
next_buzzer_index_offset = offsets.define(sizeof_uint64)
next_special_index_offset = offsets.define(sizeof_uint64)

cells_checked_offset = offsets.define(sizeof_uint32, 101)
buzzers_checked_offset = offsets.define(sizeof_uint32, 112)
specials_checked_offset = offsets.define(sizeof_uint32, 32)

buzzers_received_offset = offsets.define(sizeof_uint8, 16)
specials_received_offset = offsets.define(sizeof_uint8, 32)

# Deathlink information.
died_offset = offsets.define(sizeof_uint8)
deathlink_enabled_offset = offsets.define(sizeof_uint8)

# Move Rando information.
next_orb_cache_index_offset = offsets.define(sizeof_uint64)
orb_caches_checked_offset = offsets.define(sizeof_uint32, 16)
moves_received_offset = offsets.define(sizeof_uint8, 16)
moverando_enabled_offset = offsets.define(sizeof_uint8)

# Orbsanity information.
orbsanity_option_offset = offsets.define(sizeof_uint8)
orbsanity_bundle_offset = offsets.define(sizeof_uint32)
collected_bundle_offset = offsets.define(sizeof_uint32, 17)

# Progression and Completion information.
fire_canyon_unlock_offset = offsets.define(sizeof_float)
mountain_pass_unlock_offset = offsets.define(sizeof_float)
lava_tube_unlock_offset = offsets.define(sizeof_float)
completion_goal_offset = offsets.define(sizeof_uint8)
completed_offset = offsets.define(sizeof_uint8)

# Text to display in the HUD (32 char max per string).
their_item_name_offset = offsets.define(sizeof_uint8, 32)
their_item_owner_offset = offsets.define(sizeof_uint8, 32)
my_item_name_offset = offsets.define(sizeof_uint8, 32)
my_item_finder_offset = offsets.define(sizeof_uint8, 32)

# The End.
end_marker_offset = offsets.define(sizeof_uint8, 4)


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
    if died == 19:
        return "Jak collided with too many obstacles."
    return "Jak died."


class JakAndDaxterMemoryReader:
    marker: ByteString
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

    # Orbsanity handling
    orbsanity_enabled: bool = False
    orbs_paid: int = 0

    def __init__(self, marker: ByteString = b'UnLiStEdStRaTs_JaK1\x00'):
        self.marker = marker
        self.connect()

    async def main_tick(self,
                        location_callback: Callable,
                        finish_callback: Callable,
                        deathlink_callback: Callable,
                        deathlink_toggle: Callable,
                        paid_orbs_callback: Callable):
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
            self.save_data()
            self.outbox_index += 1

        if self.finished_game:
            finish_callback()

        if old_deathlink_enabled != self.deathlink_enabled:
            deathlink_toggle()
            logger.debug("Toggled DeathLink " + ("ON" if self.deathlink_enabled else "OFF"))

        if self.send_deathlink:
            deathlink_callback()

        if self.orbs_paid > 0:
            paid_orbs_callback(self.orbs_paid)
            self.orbs_paid = 0

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
        logger.info("   Last location checked: " + (str(self.location_outbox[self.outbox_index - 1])
                                                    if self.outbox_index else "None"))

    def read_memory(self) -> List[int]:
        try:
            next_cell_index = self.read_goal_address(0, sizeof_uint64)
            next_buzzer_index = self.read_goal_address(next_buzzer_index_offset, sizeof_uint64)
            next_special_index = self.read_goal_address(next_special_index_offset, sizeof_uint64)

            for k in range(0, next_cell_index):
                next_cell = self.read_goal_address(cells_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                cell_ap_id = Cells.to_ap_id(next_cell)
                if cell_ap_id not in self.location_outbox:
                    self.location_outbox.append(cell_ap_id)
                    logger.debug("Checked power cell: " + str(next_cell))

                    # If orbsanity is ON and next_cell is one of the traders or oracles, then run a callback
                    # to add their amount to the DataStorage value holding our current orb trade total.
                    if next_cell in {11, 12, 31, 32, 33, 96, 97, 98, 99}:
                        self.orbs_paid += 90
                        logger.debug("Traded 90 orbs!")

                    if next_cell in {13, 14, 34, 35, 100, 101}:
                        self.orbs_paid += 120
                        logger.debug("Traded 120 orbs!")

            for k in range(0, next_buzzer_index):
                next_buzzer = self.read_goal_address(buzzers_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                buzzer_ap_id = Flies.to_ap_id(next_buzzer)
                if buzzer_ap_id not in self.location_outbox:
                    self.location_outbox.append(buzzer_ap_id)
                    logger.debug("Checked scout fly: " + str(next_buzzer))

            for k in range(0, next_special_index):
                next_special = self.read_goal_address(specials_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                special_ap_id = Specials.to_ap_id(next_special)
                if special_ap_id not in self.location_outbox:
                    self.location_outbox.append(special_ap_id)
                    logger.debug("Checked special: " + str(next_special))

            died = self.read_goal_address(died_offset, sizeof_uint8)
            if died > 0:
                self.send_deathlink = True
                self.cause_of_death = autopsy(died)

            # Listen for any changes to this setting.
            deathlink_flag = self.read_goal_address(deathlink_enabled_offset, sizeof_uint8)
            self.deathlink_enabled = bool(deathlink_flag)

            next_cache_index = self.read_goal_address(next_orb_cache_index_offset, sizeof_uint64)

            for k in range(0, next_cache_index):
                next_cache = self.read_goal_address(orb_caches_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                cache_ap_id = Caches.to_ap_id(next_cache)
                if cache_ap_id not in self.location_outbox:
                    self.location_outbox.append(cache_ap_id)
                    logger.debug("Checked orb cache: " + str(next_cache))

            # Listen for any changes to this setting.
            # moverando_flag = self.read_goal_address(moverando_enabled_offset, sizeof_uint8)
            # self.moverando_enabled = bool(moverando_flag)

            orbsanity_option = self.read_goal_address(orbsanity_option_offset, sizeof_uint8)
            bundle_size = self.read_goal_address(orbsanity_bundle_offset, sizeof_uint32)
            self.orbsanity_enabled = orbsanity_option > 0

            # Per Level Orbsanity option. Only need to do this loop if we chose this setting.
            if orbsanity_option == 1:
                for level in range(0, 16):
                    collected_bundles = self.read_goal_address(collected_bundle_offset + (level * sizeof_uint32),
                                                               sizeof_uint32)

                    # Count up from the first bundle, by bundle size, until you reach the latest collected bundle.
                    # e.g. {25, 50, 75, 100, 125...}
                    if collected_bundles > 0:
                        for bundle in range(bundle_size,
                                            bundle_size + collected_bundles,  # Range max is non-inclusive.
                                            bundle_size):

                            bundle_ap_id = Orbs.to_ap_id(Orbs.find_address(level, bundle, bundle_size))
                            if bundle_ap_id not in self.location_outbox:
                                self.location_outbox.append(bundle_ap_id)
                                logger.debug("Checked orb bundle: " + str(bundle_ap_id))

            # Global Orbsanity option. Index 16 refers to all orbs found regardless of level.
            if orbsanity_option == 2:
                collected_bundles = self.read_goal_address(collected_bundle_offset + (16 * sizeof_uint32),
                                                           sizeof_uint32)
                if collected_bundles > 0:
                    for bundle in range(bundle_size,
                                        bundle_size + collected_bundles,  # Range max is non-inclusive.
                                        bundle_size):

                        bundle_ap_id = Orbs.to_ap_id(Orbs.find_address(16, bundle, bundle_size))
                        if bundle_ap_id not in self.location_outbox:
                            self.location_outbox.append(bundle_ap_id)
                            logger.debug("Checked orb bundle: " + str(bundle_ap_id))

            completed = self.read_goal_address(completed_offset, sizeof_uint8)
            if completed > 0 and not self.finished_game:
                self.finished_game = True
                logger.info("Congratulations! You finished the game!")

        except (ProcessError, MemoryReadError, WinAPIError):
            logger.error("The gk process has died. Restart the game and run \"/memr connect\" again.")
            self.connected = False

        return self.location_outbox

    def read_goal_address(self, offset: int, length: int) -> int:
        return int.from_bytes(
            self.gk_process.read_bytes(self.goal_address + offset, length),
            byteorder="little",
            signed=False)

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
