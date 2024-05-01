import time
import struct
from socket import socket, AF_INET, SOCK_STREAM
from CommonClient import logger
from worlds.jakanddaxter.locs import CellLocations as Cells, ScoutLocations as Flies, OrbLocations as Orbs
from worlds.jakanddaxter.GameID import jak1_id


class JakAndDaxterReplClient:
    ip: str
    port: int
    socket: socket
    connected: bool = False
    listening: bool = False
    compiled: bool = False

    item_inbox = {}
    inbox_index = 0

    def __init__(self, ip: str = "127.0.0.1", port: int = 8181):
        self.ip = ip
        self.port = port

    async def init(self):
        self.connected = self.connect()
        if self.connected:
            self.listening = self.listen()
        if self.connected and self.listening:
            self.compiled = self.compile()

    async def main_tick(self):

        # Receive Items from AP. Handle 1 item per tick.
        if len(self.item_inbox) > self.inbox_index:
            self.receive_item()
            self.inbox_index += 1

    # This helper function formats and sends `form` as a command to the REPL.
    # ALL commands to the REPL should be sent using this function.
    # TODO - this blocks on receiving an acknowledgement from the REPL server. But it doesn't print
    #  any log info in the meantime. Is that a problem?
    def send_form(self, form: str, print_ok: bool = True) -> bool:
        header = struct.pack("<II", len(form), 10)
        self.socket.sendall(header + form.encode())
        response = self.socket.recv(1024).decode()
        if "OK!" in response:
            if print_ok:
                logger.info(response)
            return True
        else:
            logger.error(f"Unexpected response from REPL: {response}")
            return False

    def connect(self) -> bool:
        logger.info("Connecting to the OpenGOAL REPL...")
        if not self.ip or not self.port:
            logger.error(f"Unable to connect: IP address \"{self.ip}\" or port \"{self.port}\" was not provided.")
            return False

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            time.sleep(1)
            welcome_message = self.socket.recv(1024).decode()

            # Should be the OpenGOAL welcome message (ignore version number).
            if "Connected to OpenGOAL" and "nREPL!" in welcome_message:
                logger.info(welcome_message)
                return True
            else:
                logger.error(f"Unable to connect: unexpected welcome message \"{welcome_message}\"")
                return False
        except ConnectionRefusedError as e:
            logger.error(f"Unable to connect: {e.strerror}")
            return False

    def listen(self) -> bool:
        logger.info("Listening for the game...")
        return self.send_form("(lt)")

    def compile(self) -> bool:
        logger.info("Compiling the game... Wait for the success sound before continuing!")
        ok_count = 0
        try:
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

            # Disable cheat-mode and debug (close the visual cue).
            # self.send_form("(set! *debug-segment* #f)")
            if self.send_form("(set! *cheat-mode* #f)"):
                ok_count += 1

        except:
            logger.error(f"Unable to compile: commands were not sent properly.")
            return False

        # Now wait until we see the success message... 5 times.
        return ok_count == 5

    def verify(self) -> bool:
        logger.info("Verifying compilation... if you don't hear the success sound, try listening and compiling again!")
        return self.send_form("(dotimes (i 1) "
                              "(sound-play-by-name "
                              "(static-sound-name \"menu-close\") "
                              "(new-sound-id) 1024 0 0 (sound-group sfx) #t))")

    def receive_item(self):
        ap_id = getattr(self.item_inbox[self.inbox_index], "item")

        # Determine the type of item to receive.
        if ap_id in range(jak1_id, jak1_id + Flies.fly_offset):
            self.receive_power_cell(ap_id)

        elif ap_id in range(jak1_id + Flies.fly_offset, jak1_id + Orbs.orb_offset):
            self.receive_scout_fly(ap_id)

        elif ap_id > jak1_id + Orbs.orb_offset:
            pass  # TODO

    def receive_power_cell(self, ap_id: int) -> bool:
        cell_id = Cells.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type fuel-cell) "
                            "(the float " + str(cell_id) + "))")
        if ok:
            logger.info(f"Received power cell {cell_id}!")
        else:
            logger.error(f"Unable to receive power cell {cell_id}!")
        return ok

    def receive_scout_fly(self, ap_id: int) -> bool:
        fly_id = Flies.to_game_id(ap_id)
        ok = self.send_form("(send-event "
                            "*target* \'get-archipelago "
                            "(pickup-type buzzer) "
                            "(the float " + str(fly_id) + "))")
        if ok:
            logger.info(f"Received scout fly {fly_id}!")
        else:
            logger.error(f"Unable to receive scout fly {fly_id}!")
        return ok
