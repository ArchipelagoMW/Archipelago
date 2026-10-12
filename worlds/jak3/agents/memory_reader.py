import logging
import struct
from typing import ByteString, Callable
import json
from PyMemoryEditor import OpenProcess, ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess
from dataclasses import dataclass

from worlds.jak3.locs.mission_locations import (main_tasks_to_missions, side_tasks_to_missions,
                                                  get_location_id, get_dual_checks_for_mission,
                                                  DUAL_CHECK_SLOT_OFFSET,
                                                  medal_ids_to_medals, secret_ids_to_secrets,
                                                  get_orb_bundle_location_id)

from ..game_id import jak3_gk

logger = logging.getLogger("Jak3MemoryReader")




# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1
sizeof_float = 4


# *****************************************************************************
# **** This number must match (-> *ap-info-jak3* version) in ap-struct.gc! ****
# *****************************************************************************
expected_memory_version = 9


@dataclass
class OffsetFactory:
    current_offset: int = 0

    def define(self, size: int, length: int = 1) -> int:
        bytes_to_alignment = self.current_offset % size
        if bytes_to_alignment != 0:
            self.current_offset += (size - bytes_to_alignment)
        offset_to_use = self.current_offset
        self.current_offset += (size * length)
        return offset_to_use


offsets = OffsetFactory()

memory_version_offset = offsets.define(sizeof_uint32)
next_mission_index_offset = offsets.define(sizeof_uint64)
next_side_mission_index_offset = offsets.define(sizeof_uint64)
missions_checked_offset = offsets.define(sizeof_uint32, 75)
side_missions_checked_offset = offsets.define(sizeof_uint32, 75)
connection_status_offset = offsets.define(sizeof_uint32)
slot_name_offset = offsets.define(sizeof_uint8, 16)
slot_seed_offset = offsets.define(sizeof_uint8, 8)
completion_goal_offset = offsets.define(sizeof_uint8)
completion_goal_type_offset = offsets.define(sizeof_uint32)
completion_goal_value_offset = offsets.define(sizeof_uint32)
completed_offset = offsets.define(sizeof_uint8)
death_count_offset = offsets.define(sizeof_uint32)
cause_of_death_offset = offsets.define(sizeof_uint8)
deathlink_enabled_offset = offsets.define(sizeof_uint8)
trap_duration_offset = offsets.define(sizeof_float)
next_medal_index_offset = offsets.define(sizeof_uint64)
medals_checked_offset = offsets.define(sizeof_uint32, 30)
next_secret_index_offset = offsets.define(sizeof_uint64)
secrets_checked_offset = offsets.define(sizeof_uint32, 40)
orbs_found_offset = offsets.define(sizeof_uint32)
next_orb_bundle_index_offset = offsets.define(sizeof_uint64)
orb_bundles_checked_offset = offsets.define(sizeof_uint32, 600)
orbs_spent_offset = offsets.define(sizeof_uint32)
gems_spent_offset = offsets.define(sizeof_uint32)
end_marker_offset = offsets.define(sizeof_uint8, 4)


def as_float(value: int) -> int:
    return int(struct.unpack('f', value.to_bytes(sizeof_float, "little"))[0])

# "Jak" to be replaced by player name in the Client.
def autopsy(cause: int) -> str:
    if cause == 5:
        return "Jak got taken out by a bot."
    if cause == 6:
        return "Jak got stung by a centipede."
    if cause == 7:
        return "Jak fell into an endless pit."
    if cause == 8:
        return "Jak instantly perished."
    if cause == 9:
        return "Jak took a swim in molten lava."
    if cause == 10:
        return "Jak melted away."
    if cause == 11:
        return "Jak went out with a bang."
    if cause == 12:
        return "Jak was caught in a massive explosion."
    if cause == 13:
        return "Jak died in the turret."
    if cause == 14:
        return "Jak got smushed."
    if cause == 15:
        return "Jak was struck down in an attack."
    if cause == 16:
        return "Jak got shocked."
    if cause == 17:
        return "Jak got crushed."
    if cause == 18:
        return "Jak died."
    if cause == 19:
        return "Jak got blown up by a grenade."
    if cause == 20:
        return "Jak drowned."
    if cause == 21:
        return "Jak got burned."
    if cause == 22:
        return "Jak burned up."
    if cause == 23:
        return "Jak failed to continue."
    if cause == 24:
        return "Jak got grabbed by a tentacle."
    if cause == 25:
        return "Daxter was struck down in combat."
    return "Jak died."

class Jak3MemoryReader:
    marker: ByteString
    goal_address: int | None = None
    connected: bool = False
    initiated_connect: bool = False

    gk_process: OpenProcess | None = None

    location_outbox: list[int] = []
    outbox_index: int = 0
    finished_game: bool = False
    checks_per_mission: int = 1
    location_check_mode: int = 1  # 1 = single check per mission, 2 = dual checks
    slot_seed: str = ""

    # Number of orb bundle locations the generator created for this seed (from slot data).
    # Bundles above this number are ignored. Default = max, i.e. no filtering until set.
    orb_bundle_count: int = 600
    orb_bundle_size: int = 0   # orbs per bundle (0 = orbsanity off)

    # Deathlink handling
    deathlink_enabled: bool = False
    send_deathlink: bool = False
    cause_of_death: int = 0
    death_count: int = 0

    # Spend tracking (orbs/gems)
    last_orbs_spent: int = 0
    last_gems_spent: int = 0
    orbs_paid: int = 0
    gems_paid: int = 0

    inform_checked_location: Callable
    inform_finished_game: Callable
    inform_died: Callable
    inform_toggled_deathlink: Callable
    inform_orb_spend: Callable
    inform_gem_spend: Callable

    log_error: Callable
    log_warn: Callable
    log_success: Callable
    log_info: Callable

    def __init__(self,
                 location_check_callback: Callable,
                 finish_game_callback: Callable,
                 send_deathlink_callback: Callable,
                 toggle_deathlink_callback: Callable,
                 orb_spend_callback: Callable,
                 gem_spend_callback: Callable,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 marker: ByteString = b'ArChIpElAgO_JaK3\x00'):
        self.marker = marker

        self.inform_checked_location = location_check_callback
        self.inform_finished_game = finish_game_callback
        self.inform_died = send_deathlink_callback
        self.inform_toggled_deathlink = toggle_deathlink_callback
        self.inform_orb_spend = orb_spend_callback
        self.inform_gem_spend = gem_spend_callback

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
                OpenProcess(name=jak3_gk)
            except (ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess):
                msg = (f"Error reading game memory! (Did the game crash?)\n"
                       f"Please close all open windows and reopen the Jak 3 Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak 3 Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                self.connected = False
        else:
            return

        if self.connected:
            old_deathlink_enabled = self.deathlink_enabled

            self.read_memory()

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
                self.inform_orb_spend(self.orbs_paid)
                self.orbs_paid = 0

            if self.gems_paid > 0:
                self.inform_gem_spend(self.gems_paid)
                self.gems_paid = 0

    async def connect(self):
        try:
            self.gk_process = OpenProcess(name=jak3_gk)
            if self.gk_process:
                logger.debug("Found the gk process: " + str(self.gk_process.pid))
            else:
                return
        except ProcessNotFoundError:
            self.log_error(logger, "Could not find the game process.")
            self.connected = False
            return

        marker_addresses = list(self.gk_process.search_by_value(bytes, len(self.marker), self.marker,
                                                                writeable_only=True) if self.gk_process else [])
        if len(marker_addresses) > 0:
            goal_pointer = marker_addresses[0] + len(self.marker) + 7
            self.goal_address = int.from_bytes(
                self.gk_process.read_process_memory(goal_pointer, bytes, sizeof_uint64),
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
                raise Exception(memory_version_offset, sizeof_uint32)
        except (ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess):
            if memory_version is None:
                msg = (f"Could not find a version number in the OpenGOAL memory structure!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   If the game is running, try entering '/memr connect' in the client.\n"
                       f"   You should see 'The Memory Reader is ready!'\n"
                       f"   If that did not work, or the game is not running, run the OpenGOAL Launcher.\n"
                       f"   Click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Try entering '/memr connect' in the client again.")
            else:
                msg = (f"The OpenGOAL memory structure is incompatible with the current Archipelago client!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Click Update (if one is available).\n"
                       f"   Click Advanced > Compile. When this is done, click Continue.\n"
                       f"   Click Versions and verify the latest version is marked 'Active'.\n"
                       f"   Close all launchers, games, clients, and console windows, then restart Archipelago.")
            self.log_error(logger, msg)
            self.connected = False

    async def print_status(self):
        proc_id = str(self.gk_process.pid) if self.gk_process else "None"
        last_loc = str(self.location_outbox[self.outbox_index - 1] if self.outbox_index else "None")
        msg = (f"Memory Reader Status:\n"
               f"   Game process ID: {proc_id}\n"
               f"   Game state memory address: {str(self.goal_address) if self.goal_address else 'null'}\n"
               f"   Last location checked: {last_loc}\n"
               f"   Checks per mission: {self.checks_per_mission}\n"
               f"   Location check mode: {self.location_check_mode}")
        await self.verify_memory_version()
        self.log_info(logger, msg)

    def read_memory(self) -> list[int]:
        try:
            next_mission_idx = self.read_goal_address(next_mission_index_offset, sizeof_uint64)
            for i in range(int(next_mission_idx)):
                raw_main_task_id = self.read_goal_address(missions_checked_offset + (i * sizeof_uint32),
                                                          sizeof_uint32)

                if raw_main_task_id in main_tasks_to_missions:
                    main_mission_id = main_tasks_to_missions[raw_main_task_id].mission_id
                    mission_name = main_tasks_to_missions[raw_main_task_id].name

                    checks = (get_dual_checks_for_mission(main_mission_id)
                              if self.location_check_mode == 2
                              else self.checks_per_mission)

                    for check in range(1, checks + 1):
                        loc_id = get_location_id(main_mission_id,
                                                  DUAL_CHECK_SLOT_OFFSET + check - 1 if self.location_check_mode == 2 else check)
                        if loc_id not in self.location_outbox:
                            self.location_outbox.append(loc_id)
                            logger.debug(f"Mission completed! Raw game-task: {raw_main_task_id}"
                                         f" -> Mission ID: {main_mission_id}"
                                         f" -> Check {check}"
                                         f" -> Location ID: {loc_id}"
                                         f" -> '{mission_name}'")

            next_side_mission_idx = self.read_goal_address(next_side_mission_index_offset, sizeof_uint64)
            for i in range(int(next_side_mission_idx)):
                raw_side_task_id = self.read_goal_address(side_missions_checked_offset + (i * sizeof_uint32),
                                                          sizeof_uint32)

                if raw_side_task_id in side_tasks_to_missions:
                    side_mission_id = side_tasks_to_missions[raw_side_task_id].mission_id
                    side_mission_name = side_tasks_to_missions[raw_side_task_id].name

                    # Side missions always have exactly 1 check in dual-check mode.
                    checks = 1 if self.location_check_mode == 2 else self.checks_per_mission

                    for check in range(1, checks + 1):
                        loc_id = get_location_id(side_mission_id,
                                                  DUAL_CHECK_SLOT_OFFSET + check - 1 if self.location_check_mode == 2 else check)
                        if loc_id not in self.location_outbox:
                            self.location_outbox.append(loc_id)
                            logger.debug(f"Side mission completed! Raw game-task: {raw_side_task_id}"
                                         f" -> Mission ID: {side_mission_id}"
                                         f" -> Check {check}"
                                         f" -> Location ID: {loc_id}"
                                         f" -> '{side_mission_name}'")

            next_medal_idx = self.read_goal_address(next_medal_index_offset, sizeof_uint64)
            for i in range(int(next_medal_idx)):
                raw_medal_id = self.read_goal_address(medals_checked_offset + (i * sizeof_uint32),
                                                      sizeof_uint32)

                if raw_medal_id in medal_ids_to_medals:
                    medal = medal_ids_to_medals[raw_medal_id]
                    loc_id = medal.location_id
                    if loc_id not in self.location_outbox:
                        self.location_outbox.append(loc_id)
                        logger.debug(f"Medal earned! Medal ID: {raw_medal_id}"
                                     f" -> Location ID: {loc_id}"
                                     f" -> '{medal.name}'")

            next_secret_idx = self.read_goal_address(next_secret_index_offset, sizeof_uint64)
            for i in range(int(next_secret_idx)):
                raw_secret_id = self.read_goal_address(secrets_checked_offset + (i * sizeof_uint32),
                                                       sizeof_uint32)

                if raw_secret_id in secret_ids_to_secrets:
                    secret = secret_ids_to_secrets[raw_secret_id]
                    loc_id = secret.location_id
                    if loc_id not in self.location_outbox:
                        self.location_outbox.append(loc_id)
                        logger.debug(f"Secret bought! Secret ID: {raw_secret_id}"
                                     f" -> Location ID: {loc_id}"
                                     f" -> '{secret.name}'")

            completed = self.read_goal_address(completed_offset, sizeof_uint8)
            if completed > 0 and not self.finished_game:
                self.finished_game = True
                self.log_success(logger, "Congratulations! You finished the game!")


            next_orb_bundle_idx = self.read_goal_address(next_orb_bundle_index_offset, sizeof_uint64)
            for i in range(int(next_orb_bundle_idx)):
                raw_bundle_id = self.read_goal_address(orb_bundles_checked_offset + (i * sizeof_uint32),
                                                       sizeof_uint32)

                # Ignore bundles the generator didn't create a location for in this seed.
                if raw_bundle_id > self.orb_bundle_count:
                    continue

                loc_id = get_orb_bundle_location_id(raw_bundle_id)
                if loc_id not in self.location_outbox:
                    self.location_outbox.append(loc_id)
                    logger.debug(f"Orb bundle checked! Bundle ID: {raw_bundle_id}"
                                 f" -> Location ID: {loc_id}")

            # Catch up any bundles the game skipped (e.g. when several orbs are
            # awarded at once and the running total jumps past a multiple).
            if self.orb_bundle_size > 0:
                orbs_found = self.read_goal_address(orbs_found_offset, sizeof_uint32)
                bundles_earned = min(orbs_found // self.orb_bundle_size, self.orb_bundle_count)
                for bundle_id in range(1, bundles_earned + 1):
                    loc_id = get_orb_bundle_location_id(bundle_id)
                    if loc_id not in self.location_outbox:
                        self.location_outbox.append(loc_id)
                        logger.debug(f"Orb bundle caught up! Bundle ID: {bundle_id}"
                                     f" -> Location ID: {loc_id}")

            # Deathlink handling
            death_count = self.read_goal_address(death_count_offset, sizeof_uint32)
            cause_of_death = self.read_goal_address(cause_of_death_offset, sizeof_uint8)
            if death_count > self.death_count:
                self.cause_of_death = cause_of_death
                self.send_deathlink = True
                self.death_count = death_count

            # Listen for any changes to this setting.
            deathlink_flag = self.read_goal_address(deathlink_enabled_offset, sizeof_uint8)
            self.deathlink_enabled = bool(deathlink_flag)

            # Spend tracking: GOAL increments these monotonic counters the instant a spend happens.
            orbs_spent = self.read_goal_address(orbs_spent_offset, sizeof_uint32)
            if orbs_spent > self.last_orbs_spent:
                self.orbs_paid += (orbs_spent - self.last_orbs_spent)
                self.last_orbs_spent = orbs_spent

            gems_spent = self.read_goal_address(gems_spent_offset, sizeof_uint32)
            if gems_spent > self.last_gems_spent:
                self.gems_paid += (gems_spent - self.last_gems_spent)
                self.last_gems_spent = gems_spent

        except (ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess):
            msg = (f"Error reading game memory! (Did the game crash?)\n"
                   f"Please close all open windows and reopen the Jak 3 Client "
                   f"from the Archipelago Launcher.\n"
                   f"If the game and compiler do not restart automatically, please follow these steps:\n"
                   f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                   f"   Then click Advanced > Play in Debug Mode.\n"
                   f"   Then click Advanced > Open REPL.\n"
                   f"   Then close and reopen the Jak 3 Client from the Archipelago Launcher.")
            self.log_error(logger, msg)
            self.connected = False

        return self.location_outbox

    def read_goal_address(self, offset: int, length: int) -> int:
        if not (self.gk_process and self.goal_address):
            raise Exception(memory_version_offset, sizeof_uint32)

        return int.from_bytes(
            self.gk_process.read_process_memory(self.goal_address + offset, bytes, length),
            byteorder="little",
            signed=False)

    def save_data(self):
        filename = f"jak3_location_outbox_{self.slot_seed}.json" if self.slot_seed else "jak3_location_outbox.json"
        with open(filename, "w+") as f:
            dump = {
                "outbox_index": self.outbox_index,
                "location_outbox": self.location_outbox
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        self.outbox_index = 0
        self.location_outbox = []
        filename = f"jak3_location_outbox_{self.slot_seed}.json" if self.slot_seed else "jak3_location_outbox.json"
        try:
            with open(filename, "r") as f:
                load = json.load(f)
                self.outbox_index = load["outbox_index"]
                self.location_outbox = load["location_outbox"]
        except FileNotFoundError:
            pass