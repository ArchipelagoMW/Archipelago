import time
import struct
import typing
import asyncio
from socket import socket, AF_INET, SOCK_STREAM

import colorama

import Utils
from GameID import jak1_name
from .locs import CellLocations as Cells, ScoutLocations as Flies
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled


class JakAndDaxterClientCommandProcessor(ClientCommandProcessor):
    ctx: "JakAndDaxterContext"

    # TODO - Clean up commands related to the REPL, make them more user friendly.
    #  The REPL has a specific order of operations it needs to do in order to process our input:
    #  1. Connect (we need to open a socket connection on ip/port to the REPL).
    #  2. Listen (have the REPL compiler connect and listen on the game's REPL server's socket).
    #  3. Compile (have the REPL compiler compile the game into object code it can run).
    #  All 3 need to be done, and in this order, for this to work.


class JakAndDaxterReplClient:
    ip: str
    port: int
    socket: socket
    connected: bool = False
    listening: bool = False
    compiled: bool = False

    def __init__(self, ip: str = "127.0.0.1", port: int = 8181):
        self.ip = ip
        self.port = port
        self.connected = self.g_connect()
        if self.connected:
            self.listening = self.g_listen()
        if self.connected and self.listening:
            self.compiled = self.g_compile()

    # This helper function formats and sends `form` as a command to the REPL.
    # ALL commands to the REPL should be sent using this function.
    def send_form(self, form: str) -> None:
        header = struct.pack("<II", len(form), 10)
        self.socket.sendall(header + form.encode())
        logger.info("Sent Form: " + form)

    def g_connect(self) -> bool:
        if not self.ip or not self.port:
            return False

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        time.sleep(1)
        print(self.socket.recv(1024).decode())
        return True

    def g_listen(self) -> bool:
        self.send_form("(lt)")
        return True

    def g_compile(self) -> bool:
        # Show this visual cue when compilation is started.
        # It's the version number of the OpenGOAL Compiler.
        self.send_form("(set! *debug-segment* #t)")

        # Play this audio cue when compilation is started.
        # It's the sound you hear when you press START + CIRCLE to open the Options menu.
        self.send_form("(dotimes (i 1) "
                       "(sound-play-by-name "
                       "(static-sound-name \"start-options\") "
                       "(new-sound-id) 1024 0 0 (sound-group sfx) #t))")

        # Start compilation. This is blocking, so nothing will happen until the REPL is done.
        self.send_form("(mi)")

        # Play this audio cue when compilation is complete.
        # It's the sound you hear when you press START + START to close the Options menu.
        self.send_form("(dotimes (i 1) "
                       "(sound-play-by-name "
                       "(static-sound-name \"menu close\") "
                       "(new-sound-id) 1024 0 0 (sound-group sfx) #t))")

        # Disable cheat-mode and debug (close the visual cue).
        self.send_form("(set! *cheat-mode* #f)")
        self.send_form("(set! *debug-segment* #f)")
        return True

    def g_verify(self) -> bool:
        self.send_form("(dotimes (i 1) "
                       "(sound-play-by-name "
                       "(static-sound-name \"menu close\") "
                       "(new-sound-id) 1024 0 0 (sound-group sfx) #t))")
        return True

    # TODO - In ArchipelaGOAL, override the 'get-pickup event so that it doesn't give you the item,
    #  it just plays the victory animation. Then define a new event type like 'get-archipelago
    #  to actually give ourselves the item. See game-info.gc and target-handler.gc.

    def give_power_cell(self, ap_id: int) -> None:
        cell_id = Cells.to_game_id(ap_id)
        self.send_form("(send-event "
                       "*target* \'get-archipelago "
                       "(pickup-type fuel-cell) "
                       "(the float " + str(cell_id) + "))")

    def give_scout_fly(self, ap_id: int) -> None:
        fly_id = Flies.to_game_id(ap_id)
        self.send_form("(send-event "
                       "*target* \'get-archipelago "
                       "(pickup-type buzzer) "
                       "(the float " + str(fly_id) + "))")


class JakAndDaxterContext(CommonContext):
    tags = {"AP"}
    game = jak1_name
    items_handling = 0b111  # Full item handling
    command_processor = JakAndDaxterClientCommandProcessor
    repl: JakAndDaxterReplClient

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        self.repl = JakAndDaxterReplClient()
        super().__init__(server_address, password)

    def on_package(self, cmd: str, args: dict):
        if cmd == "":
            pass

    def run_gui(self):
        from kvui import GameManager

        class JakAndDaxterManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Jak and Daxter ArchipelaGOAL Client"

        self.ui = JakAndDaxterManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def run_game():
    pass


async def main():
    Utils.init_logging("JakAndDaxterClient", exception_logger="Client")

    ctx = JakAndDaxterContext(None, None)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    run_game()

    await ctx.exit_event.wait()
    await ctx.shutdown()


if __name__ == "__main__":
    colorama.init()
    asyncio.run(main())
    colorama.deinit()