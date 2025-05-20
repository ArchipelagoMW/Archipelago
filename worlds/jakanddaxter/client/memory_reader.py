import logging
import random
import struct
from typing import ByteString, Callable
import json
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound, ProcessError, MemoryReadError, WinAPIError
from dataclasses import dataclass

from ..locs import (orb_locations as orbs,
                    cell_locations as cells,
                    scout_locations as flies,
                    special_locations as specials,
                    orb_cache_locations as caches)


logger = logging.getLogger("MemoryReader")


# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1
sizeof_float = 4


# *****************************************************************************
# **** This number must match (-> *ap-info-jak1* version) in ap-struct.gc! ****
# *****************************************************************************
expected_memory_version = 5


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
death_count_offset = offsets.define(sizeof_uint32)
death_cause_offset = offsets.define(sizeof_uint8)
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
citizen_orb_amount_offset = offsets.define(sizeof_float)
oracle_orb_amount_offset = offsets.define(sizeof_float)
completion_goal_offset = offsets.define(sizeof_uint8)
completed_offset = offsets.define(sizeof_uint8)

# Text to display in the HUD (32 char max per string).
their_item_name_offset = offsets.define(sizeof_uint8, 32)
their_item_owner_offset = offsets.define(sizeof_uint8, 32)
my_item_name_offset = offsets.define(sizeof_uint8, 32)
my_item_finder_offset = offsets.define(sizeof_uint8, 32)

# Version of the memory struct, to cut down on mod/apworld version mismatches.
memory_version_offset = offsets.define(sizeof_uint32)

# Connection status to AP server (not the game!)
server_connection_offset = offsets.define(sizeof_uint8)
slot_name_offset = offsets.define(sizeof_uint8, 16)
slot_seed_offset = offsets.define(sizeof_uint8, 8)

# Trap information.
trap_duration_offset = offsets.define(sizeof_float)

# The End.
end_marker_offset = offsets.define(sizeof_uint8, 4)


# Can't believe this is easier to do in GOAL than Python but that's how it be sometimes.
def as_float(value: int) -> int:
    return int(struct.unpack('f', value.to_bytes(sizeof_float, "little"))[0])


# "Jak" to be replaced by player name in the Client.
def autopsy(cause: int) -> str:
    if cause in [1, 2, 3, 4]:
        return random.choice(["Jak said goodnight.",
                              "Jak stepped into the light.",
                              "Jak gave Daxter his insect collection.",
                              "Jak did not follow Step 1."])
    if cause == 5:
        return "Jak fell into an endless pit."
    if cause == 6:
        return "Jak drowned in the spicy water."
    if cause == 7:
        return "Jak tried to tackle a Lurker Shark."
    if cause == 8:
        return "Jak hit 500 degrees."
    if cause == 9:
        return "Jak took a bath in a pool of dark eco."
    if cause == 10:
        return "Jak got bombarded with flaming 30-ton boulders."
    if cause == 11:
        return "Jak hit 800 degrees."
    if cause == 12:
        return "Jak ceased to be."
    if cause == 13:
        return "Jak got eaten by the dark eco plant."
    if cause == 14:
        return "Jak burned up."
    if cause == 15:
        return "Jak hit the ground hard."
    if cause == 16:
        return "Jak crashed the zoomer."
    if cause == 17:
        return "Jak got Flut Flut hurt."
    if cause == 18:
        return "Jak poisoned the whole darn catch."
    if cause == 19:
        return "Jak collided with too many obstacles."
    return "Jak died."


class JakAndDaxterMemoryReader:
    marker: ByteString
    goal_address: int | None = None
    connected: bool = False
    initiated_connect: bool = False

    # The memory reader just needs the game running.
    gk_process: pymem.process = None

    location_outbox: list[int] = []
    outbox_index: int = 0
    finished_game: bool = False

    # Deathlink handling
    deathlink_enabled: bool = False
    send_deathlink: bool = False
    cause_of_death: str = ""
    death_count: int = 0

    # Orbsanity handling
    orbsanity_enabled: bool = False
    orbs_paid: int = 0

    # Game-related callbacks (inform the AP server of changes to game state)
    inform_checked_location: Callable
    inform_finished_game: Callable
    inform_died: Callable
    inform_toggled_deathlink: Callable
    inform_traded_orbs: Callable

    # Logging callbacks
    # These will write to the provided logger, as well as the Client GUI with color markup.
    log_error: Callable    # Red
    log_warn: Callable     # Orange
    log_success: Callable  # Green
    log_info: Callable     # White (default)

    def __init__(self,
                 location_check_callback: Callable,
                 finish_game_callback: Callable,
                 send_deathlink_callback: Callable,
                 toggle_deathlink_callback: Callable,
                 orb_trade_callback: Callable,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 marker: ByteString = b'UnLiStEdStRaTs_JaK1\x00'):
        self.marker = marker

        self.inform_checked_location = location_check_callback
        self.inform_finished_game = finish_game_callback
        self.inform_died = send_deathlink_callback
        self.inform_toggled_deathlink = toggle_deathlink_callback
        self.inform_traded_orbs = orb_trade_callback

        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)  # Ping to see if it's alive.
            except (ProcessError, MemoryReadError, WinAPIError):
                msg = (f"Error reading game memory! (Did the game crash?)\n"
                       f"Please close all open windows and reopen the Jak and Daxter Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak and Daxter Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                self.connected = False
        else:
            return

        if self.connected:

            # Save some state variables temporarily.
            old_deathlink_enabled = self.deathlink_enabled

            # Read the memory address to check the state of the game.
            self.read_memory()

            # Checked Locations in game. Handle the entire outbox every tick until we're up to speed.
            if len(self.location_outbox) > self.outbox_index:
                self.inform_checked_location(self.location_outbox)
                self.save_data()
                self.outbox_index += 1

            if self.finished_game:
                self.inform_finished_game()

            if old_deathlink_enabled != self.deathlink_enabled:
                self.inform_toggled_deathlink()
                logger.debug("Toggled DeathLink " + ("ON" if self.deathlink_enabled else "OFF"))

            if self.send_deathlink:
                self.inform_died()

            if self.orbs_paid > 0:
                self.inform_traded_orbs(self.orbs_paid)
                self.orbs_paid = 0

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")  # The GOAL Kernel
            logger.debug("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            self.log_error(logger, "Could not find the game process.")
            self.connected = False
            return

        # If we don't find the marker in the first loaded module, we've failed.
        modules = list(self.gk_process.list_modules())
        marker_address = pattern.pattern_scan_module(self.gk_process.process_handle, modules[0], self.marker)
        if marker_address:
            # At this address is another address that contains the struct we're looking for: the game's state.
            # From here we need to add the length in bytes for the marker and 4 bytes of padding,
            # and the struct address is 8 bytes long (it's an uint64).
            goal_pointer = marker_address + len(self.marker) + 4
            self.goal_address = int.from_bytes(self.gk_process.read_bytes(goal_pointer, sizeof_uint64),
                                               byteorder="little",
                                               signed=False)
            logger.debug("Found the archipelago memory address: " + str(self.goal_address))
            await self.verify_memory_version()
        else:
            self.log_error(logger, "Could not find the Archipelago marker address!")
            self.connected = False

    async def verify_memory_version(self):
        if self.goal_address is None:
            self.log_error(logger, "Could not find the Archipelago memory address!")
            self.connected = False
            return

        memory_version: int | None = None
        try:
            memory_version = self.read_goal_address(memory_version_offset, sizeof_uint32)
            if memory_version == expected_memory_version:
                self.log_success(logger, "The Memory Reader is ready!")
                self.connected = True
            else:
                raise MemoryReadError(memory_version_offset, sizeof_uint32)
        except (ProcessError, MemoryReadError, WinAPIError):
            if memory_version is None:
                msg = (f"Could not find a version number in the OpenGOAL memory structure!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   If the game is running, try entering '/memr connect' in the client.\n"
                       f"   You should see 'The Memory Reader is ready!'\n"
                       f"   If that did not work, or the game is not running, run the OpenGOAL Launcher.\n"
                       f"   Click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Try entering '/memr connect' in the client again.")
            else:
                msg = (f"The OpenGOAL memory structure is incompatible with the current Archipelago client!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                       f"   Click Update (if one is available).\n"
                       f"   Click Advanced > Compile. When this is done, click Continue.\n"
                       f"   Click Versions and verify the latest version is marked 'Active'.\n"
                       f"   Close all launchers, games, clients, and console windows, then restart Archipelago.")
            self.log_error(logger, msg)
            self.connected = False

    async def print_status(self):
        proc_id = str(self.gk_process.process_id) if self.gk_process else "None"
        last_loc = str(self.location_outbox[self.outbox_index - 1] if self.outbox_index else "None")
        msg = (f"Memory Reader Status:\n"
               f"   Game process ID: {proc_id}\n"
               f"   Game state memory address: {str(self.goal_address)}\n"
               f"   Last location checked: {last_loc}")
        await self.verify_memory_version()
        self.log_info(logger, msg)

    def read_memory(self) -> list[int]:
        try:
            # Need to grab these first and convert to floats, see below.
            citizen_orb_amount = self.read_goal_address(citizen_orb_amount_offset, sizeof_float)
            oracle_orb_amount = self.read_goal_address(oracle_orb_amount_offset, sizeof_float)

            next_cell_index = self.read_goal_address(next_cell_index_offset, sizeof_uint64)
            for k in range(0, next_cell_index):
                next_cell = self.read_goal_address(cells_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                cell_ap_id = cells.to_ap_id(next_cell)
                if cell_ap_id not in self.location_outbox:
                    self.location_outbox.append(cell_ap_id)
                    logger.debug("Checked power cell: " + str(next_cell))

                    # If orbsanity is ON and next_cell is one of the traders or oracles, then run a callback
                    # to add their amount to the DataStorage value holding our current orb trade total.
                    if next_cell in {11, 12, 31, 32, 33, 96, 97, 98, 99}:
                        citizen_orb_amount = as_float(citizen_orb_amount)
                        self.orbs_paid += citizen_orb_amount
                        logger.debug(f"Traded {citizen_orb_amount} orbs!")

                    if next_cell in {13, 14, 34, 35, 100, 101}:
                        oracle_orb_amount = as_float(oracle_orb_amount)
                        self.orbs_paid += oracle_orb_amount
                        logger.debug(f"Traded {oracle_orb_amount} orbs!")

            next_buzzer_index = self.read_goal_address(next_buzzer_index_offset, sizeof_uint64)
            for k in range(0, next_buzzer_index):
                next_buzzer = self.read_goal_address(buzzers_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                buzzer_ap_id = flies.to_ap_id(next_buzzer)
                if buzzer_ap_id not in self.location_outbox:
                    self.location_outbox.append(buzzer_ap_id)
                    logger.debug("Checked scout fly: " + str(next_buzzer))

            next_special_index = self.read_goal_address(next_special_index_offset, sizeof_uint64)
            for k in range(0, next_special_index):
                next_special = self.read_goal_address(specials_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                special_ap_id = specials.to_ap_id(next_special)
                if special_ap_id not in self.location_outbox:
                    self.location_outbox.append(special_ap_id)
                    logger.debug("Checked special: " + str(next_special))

            death_count = self.read_goal_address(death_count_offset, sizeof_uint32)
            death_cause = self.read_goal_address(death_cause_offset, sizeof_uint8)
            if death_count > self.death_count:
                self.cause_of_death = autopsy(death_cause)  # The way he names his variables? Wack!
                self.send_deathlink = True
                self.death_count += 1

            # Listen for any changes to this setting.
            deathlink_flag = self.read_goal_address(deathlink_enabled_offset, sizeof_uint8)
            self.deathlink_enabled = bool(deathlink_flag)

            next_cache_index = self.read_goal_address(next_orb_cache_index_offset, sizeof_uint64)
            for k in range(0, next_cache_index):
                next_cache = self.read_goal_address(orb_caches_checked_offset + (k * sizeof_uint32), sizeof_uint32)
                cache_ap_id = caches.to_ap_id(next_cache)
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

                            bundle_ap_id = orbs.to_ap_id(orbs.find_address(level, bundle, bundle_size))
                            if bundle_ap_id not in self.location_outbox:
                                self.location_outbox.append(bundle_ap_id)
                                logger.debug(f"Checked orb bundle: L{level} {bundle}")

            # Global Orbsanity option. Index 16 refers to all orbs found regardless of level.
            if orbsanity_option == 2:
                collected_bundles = self.read_goal_address(collected_bundle_offset + (16 * sizeof_uint32),
                                                           sizeof_uint32)
                if collected_bundles > 0:
                    for bundle in range(bundle_size,
                                        bundle_size + collected_bundles,  # Range max is non-inclusive.
                                        bundle_size):

                        bundle_ap_id = orbs.to_ap_id(orbs.find_address(16, bundle, bundle_size))
                        if bundle_ap_id not in self.location_outbox:
                            self.location_outbox.append(bundle_ap_id)
                            logger.debug(f"Checked orb bundle: G {bundle}")

            completed = self.read_goal_address(completed_offset, sizeof_uint8)
            if completed > 0 and not self.finished_game:
                self.finished_game = True
                self.log_success(logger, "Congratulations! You finished the game!")

        except (ProcessError, MemoryReadError, WinAPIError):
            msg = (f"Error reading game memory! (Did the game crash?)\n"
                   f"Please close all open windows and reopen the Jak and Daxter Client "
                   f"from the Archipelago Launcher.\n"
                   f"If the game and compiler do not restart automatically, please follow these steps:\n"
                   f"   Run the OpenGOAL Launcher, click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                   f"   Then click Advanced > Play in Debug Mode.\n"
                   f"   Then click Advanced > Open REPL.\n"
                   f"   Then close and reopen the Jak and Daxter Client from the Archipelago Launcher.")
            self.log_error(logger, msg)
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
