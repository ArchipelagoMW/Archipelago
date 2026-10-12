import json
import logging
import queue
import time
import struct
import random
from dataclasses import dataclass
from queue import Queue
from typing import Callable

from PyMemoryEditor import OpenProcess, ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess

import asyncio
from asyncio import StreamReader, StreamWriter, Lock

from NetUtils import NetworkItem
from ..items import item_table, Jak3ItemData, TRAP_ID_START, TRAP_ID_END, ITEM_ID_FILLER_START, ITEM_ID_FILLER_END
from ..game_id import jak3_gk, jak3_goalc

logger = logging.getLogger("Jak3ReplClient")


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


class Jak3ReplClient:
    ip: str
    port: int
    reader: StreamReader
    writer: StreamWriter
    lock: Lock
    connected: bool = False
    initiated_connect: bool = False
    received_deathlink: bool = False

    initial_item_count = -1
    received_initial_items = False
    processed_initial_items = False

    waiting_for_compile: bool = False
    compile_ready_time: float = 0.0

    gk_process: OpenProcess | None = None
    goalc_process: OpenProcess | None = None

    item_inbox: dict[int, NetworkItem] = {}
    inbox_index = 0
    json_message_queue: Queue[JsonMessageData] = queue.Queue()

    slot_seed: str = ""

    log_error: Callable
    log_warn: Callable
    log_success: Callable
    log_info: Callable

    def __init__(self,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 memr,
                 ip: str = "127.0.0.1",
                 port: int = 8181):
        self.ip = ip
        self.port = port
        self.lock = asyncio.Lock()
        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback
        self.memr = memr

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        # Handle compile wait without blocking the event loop
        if self.waiting_for_compile:
            if asyncio.get_event_loop().time() >= self.compile_ready_time:
                self.waiting_for_compile = False
                self.log_info(logger, "[4/5] Set cheat mode to off...")
                await asyncio.sleep(0.5)
                await self.send_form("(set! *cheat-mode* #f)", print_ok=False)
                await asyncio.sleep(0.5)
                self.log_info(logger, "[5/5] Run the title screen...")
                await self.send_form("(start 'play (get-continue-by-name *game-info* \"title-start\"))")
                self.log_success(logger, "The REPL is ready!")
                self.connected = True
            return

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
            try:
                OpenProcess(name=jak3_gk)
            except (ProcessNotFoundError, ProcessIDNotExistsError, ClosedProcess):
                msg = (f"Error sending data to compiler! (Did the compiler crash?)\n"
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

        if not self.processed_initial_items:
            if self.inbox_index >= self.initial_item_count >= 0:
                self.processed_initial_items = True
                await self.send_form("(set! *ap-suppress-initial-talkers?* #f)", print_ok=False)
                await self.send_connection_status("ready")


        if len(self.item_inbox) > self.inbox_index:
            ok = await self.receive_item()
            if ok:
                await self.save_data()
                self.inbox_index += 1


        if self.received_deathlink:
            await self.receive_deathlink()
            self.received_deathlink = False

        if not self.json_message_queue.empty():
            json_txt_data = self.json_message_queue.get_nowait()
            await self.write_game_text(json_txt_data)

    async def send_form(self, form: str, print_ok: bool = True) -> bool:
        header = struct.pack("<II", len(form), 10)
        async with self.lock:
            self.writer.write(header + form.encode())
            await self.writer.drain()

            try:
                response_data = await asyncio.wait_for(self.reader.read(8192), timeout=120.0)
                response = response_data.decode()
            except asyncio.TimeoutError:
                self.log_error(logger, f"Timed out waiting for a response to: {form!r}")
                return False

            if response and len(response.strip()) > 0:
                if print_ok:
                    logger.debug(response)
                return True
            else:
                self.log_error(logger, f"Got empty/whitespace-only response for: {form!r}")
                return False

    async def connect(self):
        try:
            self.gk_process = OpenProcess(name=jak3_gk)
            logger.debug("Found the gk process: " + str(self.gk_process.pid))
        except ProcessNotFoundError:
            self.log_error(logger, "Could not find the game process.")
            return

        try:
            self.goalc_process = OpenProcess(name=jak3_goalc)
            logger.debug("Found the goalc process: " + str(self.goalc_process.pid))
        except ProcessNotFoundError:
            self.log_error(logger, "Could not find the compiler process.")
            return

        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            await asyncio.sleep(1)
            connect_data = await self.reader.read(8192)
            welcome_message = connect_data.decode()

            if "Connected to OpenGOAL" and "nREPL!" in welcome_message:
                logger.debug(welcome_message)
            else:
                self.log_error(logger,
                               f"Unable to connect to REPL websocket: unexpected welcome message \"{welcome_message}\"")
        except ConnectionRefusedError as e:
            self.log_error(logger, f"Unable to connect to REPL websocket: {e.strerror}")
            return

        if self.reader and self.writer:
            self.log_info(logger, "[1/5] Listen on the game's port...")
            await asyncio.sleep(0.5)
            if not await self.send_form("(lt)", print_ok=False):
                self.log_error(logger, "Failed to start listening on the game's port (lt).")
                return

            self.log_info(logger, "[2/5] Set debug flag to on...")
            await asyncio.sleep(0.5)
            if not await self.send_form("(set! *debug-segment* #t)", print_ok=False):
                self.log_error(logger, "Failed to set debug flag.")
                return

            self.log_info(logger, "[3/5] Compile the game...")
            await asyncio.sleep(0.5)
            if not await self.send_form("(mi)", print_ok=False):
                self.log_error(logger, "Failed to start compilation.")
                return

            self.log_info(logger, "[4/5] Set cheat mode to off...")
            await asyncio.sleep(0.5)
            if not await self.send_form("(set! *cheat-mode* #f)", print_ok=False):
                self.log_error(logger, "Failed to disable cheat mode.")
                return

            await asyncio.sleep(0.5)
            if not await self.send_form("(set! *debug-segment* #f)", print_ok=False):
                self.log_error(logger, "Failed to disable the debug flag.")
                return

            self.log_info(logger, "[5/5] Run the title screen...")
            if not await self.send_form("(start 'play (get-continue-by-name *game-info* \"title-start\"))"):
                self.log_error(logger, "Failed to run title screen.")
                return

            self.log_success(logger, "The REPL is ready!")
            self.connected = True

    @staticmethod
    def sanitize_game_text(text: str) -> str:
        result = "".join([c if c in ALLOWED_CHARACTERS else "?" for c in text[:32]]).upper()
        result = result.replace("'", "\\c12")
        return f"\"{result}\""

    @staticmethod
    def sanitize_file_text(text: str) -> str:
        allowed_chars_no_extras = ALLOWED_CHARACTERS - {" ", "'", "(", ")", "\""}
        result = "".join([c if c in allowed_chars_no_extras else "" for c in text[:16]]).upper()
        return f"\"{result}\""

    @staticmethod
    def sanitize_seed_text(text: str) -> str:
        allowed_chars_no_extras = ALLOWED_CHARACTERS - {" ", "'", "(", ")", "\""}
        result = "".join([c if c in allowed_chars_no_extras else "" for c in text[:7]]).upper()
        return f"\"{result}\""

    def queue_game_text(self, my_item_name, my_item_finder, their_item_name, their_item_owner):
        self.json_message_queue.put(JsonMessageData(my_item_name, my_item_finder, their_item_name, their_item_owner))

    async def write_game_text(self, data: JsonMessageData):
        logger.debug(f"Sending info to the in-game messenger!")
        body = ""
        if data.my_item_name and data.my_item_finder:
            is_trap = "Trap" in data.my_item_name
            is_filler = any(f in data.my_item_name for f in ("Pill", "Ammo", "Gems", "Health Pack"))
            if is_trap and data.my_item_finder != "MYSELF":
                direction = "'trap"
            elif data.my_item_finder == "MYSELF":
                direction = "'found"
            else:
                direction = "'recv"
            body += (f" (let ((m (the ap-messenger (process-by-name \"ap-messenger\" *active-pool*)))) "
                     f" (when m (append-messages m {direction} "
                     f" {self.sanitize_game_text(data.my_item_name)} "
                     f" {self.sanitize_game_text(data.my_item_finder)} "
                     f" {'#t' if is_filler else '#f'})))")
        if data.their_item_name and data.their_item_owner:
            is_filler_theirs = any(f in data.their_item_name for f in ("Pill", "Ammo", "Gems", "Health Pack"))
            if data.their_item_owner == "MYSELF":
                direction = "'found"
            else:
                direction = "'sent"
            body += (f" (let ((m (the ap-messenger (process-by-name \"ap-messenger\" *active-pool*)))) "
                     f" (when m (append-messages m {direction} "
                     f" {self.sanitize_game_text(data.their_item_name)} "
                     f" {self.sanitize_game_text(data.their_item_owner)} "
                     f" {'#t' if is_filler_theirs else '#f'})))")
        await self.send_form(f"(begin {body} (none))", print_ok=False)

    async def receive_item(self):
        item_obj = self.item_inbox[self.inbox_index]
        item = getattr(item_obj, "item")

        if item not in item_table:
            self.log_error(logger, f"Tried to receive item with unknown AP ID {item}!")
            return False

        item_data: Jak3ItemData = item_table[item]
        item_name: str = item_data.name
        item_symbol: str = item_data.symbol


        if TRAP_ID_START <= item <= TRAP_ID_END:
            ok = await self.send_form(f"(ap-trap-received! '{item_symbol})", print_ok=False)
            logger.debug(f"Sent trap {item_name}!")
            return ok  # removed queue_game_text, handled by json_to_game_text now

        ok = await self.send_form(f"(ap-item-received! '{item_symbol})", print_ok=False)
        if ok:
            logger.debug(f"Sent item {item_name}!")
        return ok

    async def receive_deathlink(self) -> bool:
        # Because it should at least be funny sometimes.
        death_types = ["'death",
                       "'death",
                       "'death",
                       "'death",
                       "'endlessfall",
                       "'drown-death",
                       "'lava",
                       "'dark-eco-pool",
                       "'crush",
                       "'smush",
                       "'grenade",
                       "'explode"]
        chosen_death = random.choice(death_types)

        ok = await self.send_form(f"(ap-deathlink-received! {chosen_death})", print_ok=False)
        if ok:
            logger.debug(f"Received deathlink signal!")
        else:
            self.log_error(logger, f"Unable to receive deathlink signal!")
        return ok

    async def acknowledge_orb_spend(self, amount: int) -> bool:
        logger.debug(f"Player spent {amount} orbs.")
        return True

    async def acknowledge_gem_spend(self, amount: int) -> bool:
        logger.debug(f"Player spent {amount} gems.")
        return True

    async def setup_options(self,
                            slot_name: str,
                            slot_seed: str,
                            trap_time: int,
                            completion_type: int,
                            specific_mission_value: int,
                            mission_count_value: int,
                            jak_is_jak2: int = 0,
                            randomize_bbush: int = 0,
                            bbush_cost_get_to: int = 4,
                            bbush_cost_race: int = 8,
                            bbush_cost_other: int = 12,
                            minigame_medal_checks: int = 0,
                            orbsanity: int = 0,
                            orbs_per_bundle: int = 20) -> bool:
        sanitized_name = self.sanitize_file_text(slot_name)
        sanitized_seed = self.sanitize_seed_text(slot_seed)

        ok = await self.send_form(f"(ap-setup-options! (new 'static 'ap-seed-options "
                                  f":slot-name {sanitized_name} "
                                  f":slot-seed {sanitized_seed} "
                                  f":trap-duration {trap_time}.0 "
                                  f":completion-type {completion_type} "
                                  f":completion-value {specific_mission_value} "
                                  f":completion-mission-count {mission_count_value} "
                                  f":jak-is-jak2 {jak_is_jak2} "
                                  f":randomize-bbush {randomize_bbush} "
                                  f":bbush-cost-get-to {bbush_cost_get_to}.0 "
                                  f":bbush-cost-race {bbush_cost_race}.0 "
                                  f":bbush-cost-other {bbush_cost_other}.0 "
                                  f":minigame-medal-checks {minigame_medal_checks} "
                                  f":orbsanity {orbsanity} "
                                  f":orbs-per-bundle {orbs_per_bundle} ))", print_ok=False)
        message = (f"Setting options: \n"
                   f"   Slot Name {sanitized_name}, \n"
                   f"   Slot Seed {sanitized_seed}, \n"
                   f"   Trap Duration {trap_time}, \n"
                   f"   Goal Type {completion_type}, \n"
                   f"   Specific Mission Value {specific_mission_value}, \n"
                   f"   Mission Count Value {mission_count_value}, \n"
                   f"   Jak is Jak 2: {jak_is_jak2}, \n"
                   f"   Randomize BBush: {randomize_bbush}, \n"
                   f"   BBush Cost Get-To: {bbush_cost_get_to}, \n"
                   f"   BBush Cost Race: {bbush_cost_race}, \n"
                   f"   BBush Cost Other: {bbush_cost_other}, \n"
                   f"   Minigame Medal Checks: {minigame_medal_checks}, \n"
                   f"   Orbsanity: {orbsanity}, \n"
                   f"   Orbs Per Bundle: {orbs_per_bundle}... ")
        if ok:
            logger.debug(message + "Sent!")
        else:
            self.log_error(logger, message + "Failed!")
        return ok

    async def send_connection_status(self, status: str) -> bool:
        ok = await self.send_form(f"(ap-set-connection-status! (ap-connection-status {status}))", print_ok=False)
        logger.debug(f"Connection Status {status} sent!")
        return ok

    async def save_data(self):
        filename = f"jak3_item_inbox_{self.slot_seed}.json" if self.slot_seed else "jak3_item_inbox.json"
        with open(filename, "w+") as f:
            dump = {
                "inbox_index": self.inbox_index,
                "item_inbox": [{
                    "item": self.item_inbox[k].item,
                    "location": self.item_inbox[k].location,
                    "player": self.item_inbox[k].player,
                    "flags": self.item_inbox[k].flags
                    } for k in self.item_inbox
                ]
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        self.inbox_index = 0
        self.item_inbox = {}