import json
import logging
import queue
import time
import struct
import random
from dataclasses import dataclass
from queue import Queue
from typing import Callable

from PyMemoryEditor import OpenProcess, PyMemoryEditorError

import asyncio
from asyncio import StreamReader, StreamWriter, Lock

from NetUtils import NetworkItem
from ..game_id import jak1_id, jak1_max, jak1_gk, jak1_goalc
from ..items import item_table, trap_item_table
from ..locs import (
    orb_locations as orbs,
    cell_locations as cells,
    scout_locations as flies,
    special_locations as specials,
    orb_cache_locations as caches)


logger = logging.getLogger("ReplClient")


@dataclass
class JsonMessageData:
    my_item_name: str | None = None
    my_item_finder: str | None = None
    their_item_name: str | None = None
    their_item_owner: str | None = None


ALLOWED_CHARACTERS = frozenset({
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
    "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z", " ", "!", ":", ",", ".", "/", "?", "-",
    "=", "+", "'", "(", ")", "\""
})


class JakAndDaxterReplClient:
    ip: str
    port: int
    reader: StreamReader
    writer: StreamWriter
    lock: Lock
    connected: bool = False
    initiated_connect: bool = False  # Signals when user tells us to try reconnecting.
    received_deathlink: bool = False
    balanced_orbs: bool = False

    # Variables to handle the title screen and initial game connection.
    initial_item_count = -1  # Brand new games have 0 items, so initialize this to -1.
    received_initial_items = False
    processed_initial_items = False

    # The REPL client needs the REPL/compiler process running, but that process
    # also needs the game running. Therefore, the REPL client needs both running.
    gk_process: OpenProcess | None = None
    goalc_process: OpenProcess | None = None

    item_inbox: list[NetworkItem] = []
    inbox_index = 0
    json_message_queue: Queue[JsonMessageData] = queue.Queue()

    # Logging callbacks
    # These will write to the provided logger, as well as the Client GUI with color markup.
    log_error: Callable    # Red
    log_warn: Callable     # Orange
    log_success: Callable  # Green
    log_info: Callable     # White (default)

    def __init__(self,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 ip: str = "127.0.0.1",
                 port: int = 8181):
        self.ip = ip
        self.port = port
        self.lock = asyncio.Lock()
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
                OpenProcess(name=jak1_gk)
            except PyMemoryEditorError as e:
                msg = (f"Error reading game memory! (Did the game crash?)\n"
                       f"Please close all open windows and reopen the Jak and Daxter Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak and Daxter Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                logger.error(e)
                self.connected = False
            try:
                OpenProcess(name=jak1_goalc)
            except PyMemoryEditorError as e:
                msg = (f"Error sending data to compiler! (Did the compiler crash?)\n"
                       f"Please close all open windows and reopen the Jak and Daxter Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak and Daxter > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak and Daxter Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                logger.error(e)
                self.connected = False
        else:
            return

        # When connecting the game to the AP server on the title screen, we may be processing items from starting
        # inventory or items received in an async game. Once we have caught up to the initial count, tell the player
        # that we are ready to start. New items may even come in during the title screen, so if we go over the count,
        # we should still send the ready signal.
        if not self.processed_initial_items:
            if self.inbox_index >= self.initial_item_count >= 0:
                self.processed_initial_items = True
                await self.send_connection_status("ready")

        # Receive Items from AP. receive_item() will update the inbox index
        if len(self.item_inbox) > self.inbox_index:
            await self.receive_item()
            await self.save_data()

        if self.received_deathlink:
            await self.receive_deathlink()
            self.received_deathlink = False

        # Progressively empty the queue during each tick
        # if text messages happen to be too slow we could pool dequeuing here,
        # but it'd slow down the ItemReceived message during release
        if not self.json_message_queue.empty():
            json_txt_data = self.json_message_queue.get_nowait()
            await self.write_game_text(json_txt_data)

    # This helper function formats and sends `form` as a command to the REPL.
    # ALL commands to the REPL should be sent using this function.
    async def send_form(self, form: str, print_ok: bool = True) -> bool:
        header = struct.pack("<II", len(form), 10)
        async with self.lock:
            self.writer.write(header + form.encode())
            await self.writer.drain()

            response_data = await self.reader.read(1024)
            response = response_data.decode()

            if "OK!" in response:
                if print_ok:
                    logger.debug(response)
                return True
            else:
                self.log_error(logger, f"Unexpected response from Compiler: {response}")
                return False

    async def connect(self):
        try:
            self.gk_process = OpenProcess(name=jak1_gk)  # The GOAL Kernel
            logger.debug("Found the gk process: " + str(self.gk_process.pid))
        except PyMemoryEditorError as e:
            self.log_error(logger, "Could not find the game process.")
            logger.error(e)
            return

        try:
            self.goalc_process = OpenProcess(name=jak1_goalc)  # The GOAL Compiler and REPL
            logger.debug("Found the goalc process: " + str(self.goalc_process.pid))
        except PyMemoryEditorError as e:
            self.log_error(logger, "Could not find the compiler process.")
            logger.error(e)
            return

        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            time.sleep(1)
            connect_data = await self.reader.read(1024)
            welcome_message = connect_data.decode()

            # Should be the OpenGOAL welcome message (ignore version number).
            if "Connected to OpenGOAL" and "nREPL!" in welcome_message:
                logger.debug(welcome_message)
            else:
                self.log_error(logger,
                               f"Unable to connect to Compiler websocket: unexpected welcome message "
                               f"\"{welcome_message}\"")
        except ConnectionRefusedError as e:
            self.log_error(logger, f"Unable to connect to Compiler websocket: {e.strerror}")
            return

        ok_count = 0
        if self.reader and self.writer:

            # Have the REPL listen to the game's internal websocket.
            if await self.send_form("(lt)", print_ok=False):
                ok_count += 1

            # Show this visual cue when compilation is started.
            # It's the version number of the OpenGOAL Compiler.
            if await self.send_form("(set! *debug-segment* #t)", print_ok=False):
                ok_count += 1

            # Start compilation. This is blocking, so nothing will happen until the REPL is done.
            if await self.send_form("(mi)", print_ok=False):
                ok_count += 1

            # Play this audio cue when compilation is complete.
            # It's the sound you hear when you press START + START to close the Options menu.
            if await self.send_form("(dotimes (i 1) "
                                    "(sound-play-by-name "
                                    "(static-sound-name \"menu-close\") "
                                    "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False):
                ok_count += 1

            # Disable cheat-mode and debug (close the visual cues).
            if await self.send_form("(set! *debug-segment* #f)", print_ok=False):
                ok_count += 1

            if await self.send_form("(set! *cheat-mode* #f)", print_ok=False):
                ok_count += 1

            # Run the retail game start sequence (while still connected with REPL).
            if await self.send_form("(start \'play (get-continue-by-name *game-info* \"title-start\"))"):
                ok_count += 1

            # Now wait until we see the success message... 7 times.
            if ok_count == 7:
                self.connected = True
            else:
                self.connected = False

        if self.connected:
            self.log_success(logger, "The Compiler is ready!")

    async def print_status(self):
        gc_proc_id = str(self.goalc_process.pid) if self.goalc_process else "None"
        gk_proc_id = str(self.gk_process.pid) if self.gk_process else "None"
        msg = (f"Compiler Status:\n"
               f"   Compiler process ID: {gc_proc_id}\n"
               f"   Game process ID: {gk_proc_id}\n")
        try:
            if self.reader and self.writer:
                addr = self.writer.get_extra_info("peername")
                addr = str(addr) if addr else "None"
                msg += f"   Game websocket: {addr}\n"
                await self.send_form("(dotimes (i 1) "
                                     "(sound-play-by-name "
                                     "(static-sound-name \"menu-close\") "
                                     "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False)
        except ConnectionResetError:
            msg += f"   Connection to the game was lost or reset!"
        last_item = str(getattr(self.item_inbox[self.inbox_index], "item")) if self.inbox_index else "None"
        msg += f"   Last item received: {last_item}\n"
        msg += f"   Did you hear the success audio cue?"
        self.log_info(logger, msg)

    # To properly display in-game text:
    # - It must be a valid character from the ALLOWED_CHARACTERS list.
    # - All lowercase letters must be uppercase.
    # - It must be wrapped in double quotes (for the REPL command).
    # - Apostrophes must be handled specially - GOAL uses invisible ASCII character 0x12.
    # I also only allotted 32 bytes to each string in OpenGOAL, so we must truncate.
    @staticmethod
    def sanitize_game_text(text: str) -> str:
        result = "".join([c if c in ALLOWED_CHARACTERS else "?" for c in text[:32]]).upper()
        result = result.replace("'", "\\c12")
        return f"\"{result}\""

    # Like sanitize_game_text, but the settings file will NOT allow any whitespace in the slot_name or slot_seed data.
    # And don't replace any chars with "?" for good measure.
    @staticmethod
    def sanitize_file_text(text: str) -> str:
        allowed_chars_no_extras = ALLOWED_CHARACTERS - {" ", "'", "(", ")", "\""}
        result = "".join([c if c in allowed_chars_no_extras else "" for c in text[:16]]).upper()
        return f"\"{result}\""

    # Pushes a JsonMessageData object to the json message queue to be processed during the repl main_tick
    def queue_game_text(self, my_item_name, my_item_finder, their_item_name, their_item_owner):
        self.json_message_queue.put(JsonMessageData(my_item_name, my_item_finder, their_item_name, their_item_owner))

    # OpenGOAL can handle both its own string datatype and C-like character pointers (charp).
    async def write_game_text(self, data: JsonMessageData):
        logger.debug(f"Sending info to the in-game messenger!")
        body = ""
        if data.my_item_name and data.my_item_finder:
            body += (f" (append-messages (-> *ap-messenger* 0) \'recv "
                     f" {self.sanitize_game_text(data.my_item_name)} "
                     f" {self.sanitize_game_text(data.my_item_finder)})")
        if data.their_item_name and data.their_item_owner:
            body += (f" (append-messages (-> *ap-messenger* 0) \'sent "
                     f" {self.sanitize_game_text(data.their_item_name)} "
                     f" {self.sanitize_game_text(data.their_item_owner)})")
        await self.send_form(f"(begin {body} (none))", print_ok=False)

    async def receive_item(self):
        # orbs and pills are just increment the in game counter, so just tally them up.
        # The rest are kept in an array to be fed in one big command.
        received_orbs = 0
        received_pills = 0
        received_cells = 0

        received_scout_flies = []
        received_special = []
        received_moves = []
        received_traps = []

        # an attempt to make the code easier to read
        fly_start = jak1_id + flies.fly_offset
        special_start = jak1_id + specials.special_offset
        cache_start = jak1_id + caches.orb_cache_offset
        orb_start = jak1_id + orbs.orb_offset
        trap_start = jak1_max - max(trap_item_table)

        for new_item in self.item_inbox[self.inbox_index:]:
            ap_id = new_item.item

            if ap_id < jak1_id or ap_id > jak1_max: # bail early instead of wasting time checking all of them
                self.log_error(logger, f"Tried to receive item with unknown AP ID {ap_id}!")
                continue

            # not bothering with array searches since >= and < are enough.
            # Since I checked if less than minimum I can remove all of the lower bound checks, elif already skips once range is found.
            if ap_id < fly_start:
                received_cells += 1

            elif ap_id < special_start:
                fly_id = flies.to_game_id(ap_id)
                received_scout_flies.append(str(fly_id))

            elif ap_id < cache_start:
                special_id = specials.to_game_id(ap_id)
                received_special.append(str(special_id))

            elif ap_id < orb_start:
                move_id = caches.to_game_id(ap_id)
                received_moves.append(str(move_id))

            elif ap_id < trap_start:
                orb_amount = orbs.to_game_id(ap_id)
                received_orbs += orb_amount

            elif ap_id < jak1_max:
                received_traps.append(str(ap_id))

            elif ap_id == jak1_max:
                received_pills += 1

            else:
                self.log_error(logger, f"Tried to receive item with unknown AP ID {ap_id}!")
                continue

        # Traps and pills are useless on the title screen so I don't bother sending them
        if received_cells > 0:
            await self.receive_item_amount("Power Cells", "fuel-cell", received_cells)
        if len(received_scout_flies) > 0:
            await self.receive_items("Scout Flies", "buzzer", received_scout_flies)
        if len(received_special) > 0:
            await self.receive_items("Special Unlocks", "ap-special", received_special)
        if len(received_moves) > 0:
            await self.receive_items("Moves", "ap-move", received_moves)
        if self.processed_initial_items and len(received_traps) > 0:
            await self.receive_items("Traps", "ap-trap", received_traps)
        if received_orbs > 0:
            await self.receive_item_amount("Precursor orbs", "money", received_orbs)
        if self.processed_initial_items and received_pills > 0:
            await self.receive_item_amount("Green Eco Pills", "eco-pill", received_pills, event="get-pickup")

        self.inbox_index = len(self.item_inbox)


    async def receive_items(self, pretty_name : str, pickup_type : str, items : list[str]):
        # An int array is created instead of floats because with highest move id it turns it into hex for some reason idky
        ok = await self.send_form(f"(let ((arr (new 'static 'array int {len(items)} {' '.join(items)})))"
                                  f"(dotimes (i {len(items)})"
                                   "(send-event "
                                   "*target* \'get-archipelago "
                                  f"(pickup-type {pickup_type}) "
                                   "(the float (-> arr i)) )))")
        if ok:
            logger.debug(f"Received {len(items)} {pretty_name}!")
        else:
            self.log_error(logger, f"Unable to receive {len(items)} {pretty_name}s!")
        return ok

    async def receive_item_amount(self, pretty_name : str, pickup_type : str, count : int, event : str = "get-archipelago"):
        ok = await self.send_form("(send-event "
                                 f"*target* \'{event} "
                                 f"(pickup-type {pickup_type})"
                                 f"(the float {count}))")
        if ok:
            logger.debug(f"Received {count} {pretty_name}!")
        else:
            self.log_error(logger, f"Unable to receive {count} {pretty_name}!")
        return ok

    async def receive_deathlink(self) -> bool:

        # Because it should at least be funny sometimes.
        death_types = ["\'death",
                       "\'death",
                       "\'death",
                       "\'death",
                       "\'endlessfall",
                       "\'drown-death",
                       "\'melt",
                       "\'dark-eco-pool"]
        chosen_death = random.choice(death_types)

        ok = await self.send_form("(ap-deathlink-received! " + chosen_death + ")")
        if ok:
            logger.debug(f"Received deathlink signal!")
        else:
            self.log_error(logger, f"Unable to receive deathlink signal!")
        return ok

    async def subtract_traded_orbs(self, orb_count: int) -> bool:

        # To protect against momentary server disconnects,
        # this should only be done once per client session.
        if not self.balanced_orbs:
            self.balanced_orbs = True

            ok = await self.send_form(f"(-! (-> *game-info* money) (the float {orb_count}))")
            if ok:
                logger.debug(f"Subtracting {orb_count} traded orbs!")
            else:
                self.log_error(logger, f"Unable to subtract {orb_count} traded orbs!")
            return ok

        return True

    # OpenGOAL has a limit of 8 parameters per function. We've already hit this limit. So, define a new datatype
    # in OpenGOAL that holds all these options, instantiate the type here, and have ap-setup-options! function take
    # that instance as input.
    async def setup_options(self,
                            os_option: int, os_bundle: int,
                            fc_count: int, mp_count: int,
                            lt_count: int, ct_amount: int,
                            ot_amount: int, trap_time: int,
                            goal_id: int, slot_name: str,
                            slot_seed: str) -> bool:
        sanitized_name = self.sanitize_file_text(slot_name)
        sanitized_seed = self.sanitize_file_text(slot_seed)

        # I didn't want to have to do this with floats but GOAL's compile-time vs runtime types leave me no choice.
        ok = await self.send_form(f"(ap-setup-options! (new 'static 'ap-seed-options "
                                  f":orbsanity-option {os_option} "
                                  f":orbsanity-bundle {os_bundle} "
                                  f":fire-canyon-unlock {fc_count}.0 "
                                  f":mountain-pass-unlock {mp_count}.0 "
                                  f":lava-tube-unlock {lt_count}.0 "
                                  f":citizen-orb-amount {ct_amount}.0 "
                                  f":oracle-orb-amount {ot_amount}.0 "
                                  f":trap-duration {trap_time}.0 "
                                  f":completion-goal {goal_id} "
                                  f":slot-name {sanitized_name} "
                                  f":slot-seed {sanitized_seed} ))")
        message = (f"Setting options: \n"
                   f"   orbsanity Option {os_option}, orbsanity Bundle {os_bundle}, \n"
                   f"   FC Cell Count {fc_count}, MP Cell Count {mp_count}, \n"
                   f"   LT Cell Count {lt_count}, Citizen Orb Amt {ct_amount}, \n"
                   f"   Oracle Orb Amt {ot_amount}, Trap Duration {trap_time}, \n"
                   f"   Completion GOAL {goal_id}, Slot Name {sanitized_name}, \n"
                   f"   Slot Seed {sanitized_seed}... ")
        if ok:
            logger.debug(message + "Success!")
        else:
            self.log_error(logger, message + "Failed!")

        return ok

    async def send_connection_status(self, status: str) -> bool:
        ok = await self.send_form(f"(ap-set-connection-status! (connection-status {status}))")
        if ok:
            logger.debug(f"Connection Status {status} set!")
        else:
            self.log_error(logger, f"Connection Status {status} failed to set!")

        return ok

    async def save_data(self):
        with open("jakanddaxter_item_inbox.json", "w+") as f:
            dump = {
                "inbox_index": self.inbox_index,
                "item_inbox": [{
                    "item": k.item,
                    "location": k.location,
                    "player": k.player,
                    "flags": k.flags
                    } for k in self.item_inbox
                ]
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        try:
            with open("jakanddaxter_item_inbox.json", "r") as f:
                load = json.load(f)
                self.inbox_index = load["inbox_index"]
                self.item_inbox = [NetworkItem(
                        item=load["item_inbox"][k]["item"],
                        location=load["item_inbox"][k]["location"],
                        player=load["item_inbox"][k]["player"],
                        flags=load["item_inbox"][k]["flags"]
                    ) for k in range(0, len(load["item_inbox"]))
                ]
        except FileNotFoundError:
            pass
