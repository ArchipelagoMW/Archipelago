import json
import time
import struct
from typing import Dict, Callable
import random
from socket import socket, AF_INET, SOCK_STREAM

import pymem
from pymem.exception import ProcessNotFound, ProcessError

from CommonClient import logger
from NetUtils import NetworkItem
from ..GameID import jak1_id, jak1_max
from ..Items import item_table
from ..locs import (
    OrbLocations as Orbs,
    CellLocations as Cells,
    ScoutLocations as Flies,
    SpecialLocations as Specials,
    OrbCacheLocations as Caches)


class JakAndDaxterReplClient:
    ip: str
    port: int
    sock: socket
    connected: bool = False
    initiated_connect: bool = False  # Signals when user tells us to try reconnecting.
    received_deathlink: bool = False

    # The REPL client needs the REPL/compiler process running, but that process
    # also needs the game running. Therefore, the REPL client needs both running.
    gk_process: pymem.process = None
    goalc_process: pymem.process = None

    item_inbox: Dict[int, NetworkItem] = {}
    inbox_index = 0

    my_item_name: str = None
    my_item_finder: str = None
    their_item_name: str = None
    their_item_owner: str = None

    def __init__(self, ip: str = "127.0.0.1", port: int = 8181):
        self.ip = ip
        self.port = port
        self.connect()

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)  # Ping to see if it's alive.
            except ProcessError:
                logger.error("The gk process has died. Restart the game and run \"/repl connect\" again.")
                self.connected = False
            try:
                self.goalc_process.read_bool(self.goalc_process.base_address)  # Ping to see if it's alive.
            except ProcessError:
                logger.error("The goalc process has died. Restart the compiler and run \"/repl connect\" again.")
                self.connected = False
        else:
            return

        # Receive Items from AP. Handle 1 item per tick.
        if len(self.item_inbox) > self.inbox_index:
            self.receive_item()
            self.save_data()
            self.inbox_index += 1

        if self.received_deathlink:
            self.receive_deathlink()

            # Reset all flags.
            # As a precaution, we should reset our own deathlink flag as well.
            self.reset_deathlink()
            self.received_deathlink = False

    # This helper function formats and sends `form` as a command to the REPL.
    # ALL commands to the REPL should be sent using this function.
    # TODO - this blocks on receiving an acknowledgement from the REPL server. But it doesn't print
    #  any log info in the meantime. Is that a problem?
    def send_form(self, form: str, print_ok: bool = True) -> bool:
        header = struct.pack("<II", len(form), 10)
        self.sock.sendall(header + form.encode())
        response = self.sock.recv(1024).decode()
        if "OK!" in response:
            if print_ok:
                logger.debug(response)
            return True
        else:
            logger.error(f"Unexpected response from REPL: {response}")
            return False

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")  # The GOAL Kernel
            logger.info("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            logger.error("Could not find the gk process.")
            return

        try:
            self.goalc_process = pymem.Pymem("goalc.exe")  # The GOAL Compiler and REPL
            logger.info("Found the goalc process: " + str(self.goalc_process.process_id))
        except ProcessNotFound:
            logger.error("Could not find the goalc process.")
            return

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            time.sleep(1)
            welcome_message = self.sock.recv(1024).decode()

            # Should be the OpenGOAL welcome message (ignore version number).
            if "Connected to OpenGOAL" and "nREPL!" in welcome_message:
                logger.debug(welcome_message)
            else:
                logger.error(f"Unable to connect to REPL websocket: unexpected welcome message \"{welcome_message}\"")
        except ConnectionRefusedError as e:
            logger.error(f"Unable to connect to REPL websocket: {e.strerror}")
            return

        ok_count = 0
        if self.sock:

            # Have the REPL listen to the game's internal websocket.
            if self.send_form("(lt)", print_ok=False):
                ok_count += 1

            # Show this visual cue when compilation is started.
            # It's the version number of the OpenGOAL Compiler.
            if self.send_form("(set! *debug-segment* #t)", print_ok=False):
                ok_count += 1

            # Play this audio cue when compilation is started.
            # It's the sound you hear when you press START + CIRCLE to open the Options menu.
            if self.send_form("(dotimes (i 1) "
                              "(sound-play-by-name "
                              "(static-sound-name \"start-options\") "
                              "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False):
                ok_count += 1

            # Start compilation. This is blocking, so nothing will happen until the REPL is done.
            if self.send_form("(mi)", print_ok=False):
                ok_count += 1

            # Play this audio cue when compilation is complete.
            # It's the sound you hear when you press START + START to close the Options menu.
            if self.send_form("(dotimes (i 1) "
                              "(sound-play-by-name "
                              "(static-sound-name \"menu-close\") "
                              "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False):
                ok_count += 1

            # Disable cheat-mode and debug (close the visual cues).
            if self.send_form("(set! *debug-segment* #f)", print_ok=False):
                ok_count += 1

            if self.send_form("(set! *cheat-mode* #f)", print_ok=False):
                ok_count += 1

            # Run the retail game start sequence (while still in debug).
            if self.send_form("(start \'play (get-continue-by-name *game-info* \"title-start\"))"):
                ok_count += 1

            # Now wait until we see the success message... 8 times.
            if ok_count == 8:
                self.connected = True
            else:
                self.connected = False

        if self.connected:
            logger.info("The REPL is ready!")

    def print_status(self):
        logger.info("REPL Status:")
        logger.info("  REPL process ID: " + (str(self.goalc_process.process_id) if self.goalc_process else "None"))
        logger.info("  Game process ID: " + (str(self.gk_process.process_id) if self.gk_process else "None"))
        try:
            if self.sock:
                ip, port = self.sock.getpeername()
                logger.info("  Game websocket: " + (str(ip) + ", " + str(port) if ip else "None"))
                self.send_form("(dotimes (i 1) "
                               "(sound-play-by-name "
                               "(static-sound-name \"menu-close\") "
                               "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False)
        except:
            logger.warn("  Game websocket not found!")
        logger.info("  Did you hear the success audio cue?")
        logger.info("  Last item received: " + (str(getattr(self.item_inbox[self.inbox_index], "item"))
                                                if self.inbox_index else "None"))

    # To properly display in-game text, it must be alphanumeric and uppercase.
    # I also only allotted 32 bytes to each string in OpenGOAL, so we must truncate.
    @staticmethod
    def sanitize_game_text(text: str) -> str:
        if text is None:
            return "\"NONE\""

        result = "".join(c for c in text if (c in {"-", " "} or c.isalnum()))
        result = result[:32].upper()
        return f"\"{result}\""

    # OpenGOAL can handle both its own string datatype and C-like character pointers (charp).
    # So for the game to constantly display this information in the HUD, we have to write it
    # to a memory address as a char*.
    def write_game_text(self):
        logger.debug(f"Sending info to in-game display!")
        self.send_form(f"(charp<-string (-> *ap-info-jak1* my-item-name) "
                       f"{self.sanitize_game_text(self.my_item_name)})",
                       print_ok=False)
        self.send_form(f"(charp<-string (-> *ap-info-jak1* my-item-finder) "
                       f"{self.sanitize_game_text(self.my_item_finder)})",
                       print_ok=False)
        self.send_form(f"(charp<-string (-> *ap-info-jak1* their-item-name) "
                       f"{self.sanitize_game_text(self.their_item_name)})",
                       print_ok=False)
        self.send_form(f"(charp<-string (-> *ap-info-jak1* their-item-owner) "
                       f"{self.sanitize_game_text(self.their_item_owner)})",
                       print_ok=False)

    def receive_item(self):
        ap_id = getattr(self.item_inbox[self.inbox_index], "item")

        # Determine the type of item to receive.
        if ap_id in range(jak1_id, jak1_id + Flies.fly_offset):
            self.receive_power_cell(ap_id)
        elif ap_id in range(jak1_id + Flies.fly_offset, jak1_id + Specials.special_offset):
            self.receive_scout_fly(ap_id)
        elif ap_id in range(jak1_id + Specials.special_offset, jak1_id + Caches.orb_cache_offset):
            self.receive_special(ap_id)
        elif ap_id in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset):
            self.receive_move(ap_id)
        elif ap_id in range(jak1_id + Orbs.orb_offset, jak1_max):
            self.receive_precursor_orb(ap_id)  # Ponder the Orbs.
        elif ap_id == jak1_max:
            self.receive_green_eco()  # Ponder why I chose to do ID's this way.
        else:
            raise KeyError(f"Tried to receive item with unknown AP ID {ap_id}.")

    def receive_power_cell(self, ap_id: int) -> bool:
        cell_id = Cells.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type fuel-cell) "
                            "(the float " + str(cell_id) + "))")
        if ok:
            logger.debug(f"Received a Power Cell!")
        else:
            logger.error(f"Unable to receive a Power Cell!")
        return ok

    def receive_scout_fly(self, ap_id: int) -> bool:
        fly_id = Flies.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type buzzer) "
                            "(the float " + str(fly_id) + "))")
        if ok:
            logger.debug(f"Received a {item_table[ap_id]}!")
        else:
            logger.error(f"Unable to receive a {item_table[ap_id]}!")
        return ok

    def receive_special(self, ap_id: int) -> bool:
        special_id = Specials.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type ap-special) "
                            "(the float " + str(special_id) + "))")
        if ok:
            logger.debug(f"Received special unlock {item_table[ap_id]}!")
        else:
            logger.error(f"Unable to receive special unlock {item_table[ap_id]}!")
        return ok

    def receive_move(self, ap_id: int) -> bool:
        move_id = Caches.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type ap-move) "
                            "(the float " + str(move_id) + "))")
        if ok:
            logger.debug(f"Received the ability to {item_table[ap_id]}!")
        else:
            logger.error(f"Unable to receive the ability to {item_table[ap_id]}!")
        return ok

    def receive_precursor_orb(self, ap_id: int) -> bool:
        orb_amount = Orbs.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type money) "
                            "(the float " + str(orb_amount) + "))")
        if ok:
            logger.debug(f"Received {orb_amount} Precursor Orbs!")
        else:
            logger.error(f"Unable to receive {orb_amount} Precursor Orbs!")
        return ok

    # Green eco pills are our filler item. Use the get-pickup event instead to handle being full health.
    def receive_green_eco(self) -> bool:
        ok = self.send_form("(send-event "
                            "*target* \'get-pickup "
                            "(pickup-type eco-pill) "
                            "(the float 1))")
        if ok:
            logger.debug(f"Received a green eco pill!")
        else:
            logger.error(f"Unable to receive a green eco pill!")
        return ok

    def receive_deathlink(self) -> bool:

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

        ok = self.send_form("(ap-deathlink-received! " + chosen_death + ")")
        if ok:
            logger.debug(f"Received deathlink signal!")
        else:
            logger.error(f"Unable to receive deathlink signal!")
        return ok

    def reset_deathlink(self) -> bool:
        ok = self.send_form("(set! (-> *ap-info-jak1* died) 0)")
        if ok:
            logger.debug(f"Reset deathlink flag!")
        else:
            logger.error(f"Unable to reset deathlink flag!")
        return ok

    def subtract_traded_orbs(self, orb_count: int) -> bool:
        ok = self.send_form(f"(-! (-> *game-info* money) (the float {orb_count}))")
        if ok:
            logger.debug(f"Subtracting {orb_count} traded orbs!")
        else:
            logger.error(f"Unable to subtract {orb_count} traded orbs!")
        return ok

    def reset_orbsanity(self) -> bool:
        ok = self.send_form(f"(set! (-> *ap-info-jak1* collected-bundle-level) 0)")
        if ok:
            logger.debug(f"Reset level ID for collected orbsanity bundle!")
        else:
            logger.error(f"Unable to reset level ID for collected orbsanity bundle!")

        ok = self.send_form(f"(set! (-> *ap-info-jak1* collected-bundle-count) 0)")
        if ok:
            logger.debug(f"Reset orb count for collected orbsanity bundle!")
        else:
            logger.error(f"Unable to reset orb count for collected orbsanity bundle!")
        return ok

    def setup_options(self,
                      os_option: int, os_bundle: int,
                      fc_count: int, mp_count: int,
                      lt_count: int, goal_id: int) -> bool:
        ok = self.send_form(f"(ap-setup-options! "
                            f"(the uint {os_option}) (the uint {os_bundle}) "
                            f"(the float {fc_count}) (the float {mp_count}) "
                            f"(the float {lt_count}) (the uint {goal_id}))")
        message = (f"Setting options: \n"
                   f"    Orbsanity Option {os_option}, Orbsanity Bundle {os_bundle}, \n"
                   f"    FC Cell Count {fc_count}, MP Cell Count {mp_count}, \n"
                   f"    LT Cell Count {lt_count}, Completion GOAL {goal_id}... ")
        if ok:
            logger.debug(message + "Success!")
        else:
            logger.error(message + "Failed!")
        return ok

    def save_data(self):
        with open("jakanddaxter_item_inbox.json", "w+") as f:
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
        try:
            with open("jakanddaxter_item_inbox.json", "r") as f:
                load = json.load(f)
                self.inbox_index = load["inbox_index"]
                self.item_inbox = {k: NetworkItem(
                        item=load["item_inbox"][k]["item"],
                        location=load["item_inbox"][k]["location"],
                        player=load["item_inbox"][k]["player"],
                        flags=load["item_inbox"][k]["flags"]
                    ) for k in range(0, len(load["item_inbox"]))
                }
        except FileNotFoundError:
            pass
