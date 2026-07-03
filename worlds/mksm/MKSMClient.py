"""
MKSMClient.py

Archipelago client for Mortal Kombat: Shaolin Monks.
Connects to a running PCSX2 instance via the PINE protocol and bridges
location checks to the Archipelago server.

Minimal scope for now: detects collected red koins only. Item granting
and other location categories come later.
"""

from __future__ import annotations

import asyncio
import copy
import logging
import sys
import typing
from collections import deque

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, get_base_parser, handle_url_arg, logger, \
    ClientCommandProcessor, gui_enabled

import Utils
from worlds.mksm.consts import GameState, DEFAULT_EVENT_ARRAY, EVENTS_TO_LOCATION_NAME

from .MKSMInterface import MKSMInterface
from .callbacks import game_watcher as run_callbacks

EMULATOR_RECONNECT_DELAY = 5  # seconds between PCSX2 connection attempts


class MKSMCommandProcessor(ClientCommandProcessor):
    ctx: MKSMContext

    # def _cmd_xp(self, value: str = "1000") -> bool:
    #     """Add given xp
    #     Usage: /xp   or   /xp 5000"""
    #     ctx: MKSMContext = self.ctx
    #     ctx.game_interface.add_xp(int(value))
    #     self.output(f"Added {value} XP")
    #     return True

    # def _cmd_health(self):
    #     """
    #     prints current health status
    #     """
    #     ctx: MKSMContext = self.ctx
    #     print(ctx.game_interface.health_status())
    #     return True

    def _cmd_events(self, n: str = "5") -> bool:
        """prints the current room and the last n events in the server's saved event log
        Usage: /events   or   /events 10"""
        ctx: MKSMContext = self.ctx
        current_events = list(ctx.stored_data.get("EVENT_ARRAY") or [])
        events = [tuple(current_events[i:i + 8]) for i in range(0, len(current_events), 8)]

        if not events:
            self.output("event log is empty")
            return True

        self.output(f"current room: {hex(events[-1][0])}")

        for event in events[-int(n):]:
            room, event_code = event[0], event[4]
            location_name = EVENTS_TO_LOCATION_NAME.get(event, "<unmapped>")
            self.output(f"room={hex(room)} event={hex(event_code)} ({location_name})")

        return True

    def _cmd_debug(self) -> bool:
        """
        Toggles whether the Debug menu replaces the options in the pause screen
        """
        ctx: MKSMContext = self.ctx
        if not ctx.game_interface.get_connection_state():
            self.output("can't toggle debug menu - not connected to the game.")
            return False

        is_debug = ctx.game_interface.toggle_debug_menu()

        if is_debug:
            self.output("Debug Menu turned ON")
        else:
            self.output("Debug Menu turned OFF")

        return True

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a MultiWorld Server"""
        ctx: MKSMContext = self.ctx
        if not ctx.ready_to_connect():
            self.output("can't connect - not at the main menu.")
            return False
        return super()._cmd_connect(address)

    async def _cmd_removeevent(self) -> bool:
        """removes all events from the room the last event happened in, use in cases of
        softlocks if exited at wrong times, use only on main menu"""
        ctx: MKSMContext = self.ctx
        if ctx.game_state != GameState.MAIN_MENU:
            self.output("only use /removeevents on main menu")
            return True

        current_events = ctx.stored_data.get("EVENT_ARRAY")

        if not current_events or current_events == DEFAULT_EVENT_ARRAY:
            self.output("no event to remove")
            return True

        events = [tuple(current_events[i:i + 8]) for i in range(0, len(current_events), 8)]
        last_room = events[-1][0]
        self.output(f"Removing events from last room: {hex(last_room)}")
        remaining_events = [event for event in events if event[0] != last_room]
        new_array = [byte for event in remaining_events for byte in event]

        await ctx.send_msgs([{"cmd": "Set",
                              "key": "EVENT_ARRAY",
                              "operations": [
                                  {
                                      "operation": "replace",
                                      "value": new_array
                                  }
                              ],
                              }])

        return True

    async def _cmd_default(self) -> bool:
        """adds the default event array's entries back into the current event array
        (without removing anything already there)"""
        ctx: MKSMContext = self.ctx

        current_events = list(ctx.stored_data.get("EVENT_ARRAY") or [])
        existing = {tuple(current_events[i:i + 8]) for i in range(0, len(current_events), 8)}
        default_events = [tuple(DEFAULT_EVENT_ARRAY[i:i + 8]) for i in range(0, len(DEFAULT_EVENT_ARRAY), 8)]

        missing_events = [event for event in default_events if event not in existing]
        new_array = current_events + [byte for event in missing_events for byte in event]

        ctx.game_interface.clear_event_log(bytes(new_array))

        await ctx.send_msgs([{"cmd": "Set",
                              "key": "EVENT_ARRAY",
                              "operations": [
                                  {
                                      "operation": "replace",
                                      "value": new_array
                                  }
                              ],
                              }])

        return True

    async def _cmd_deathlink(self):
        ctx: MKSMContext = self.ctx
        is_death_link = "DeathLink" in ctx.tags
        self.output(f"Setting Death Link: {not is_death_link}")
        await ctx.update_death_link(not is_death_link)


class MKSMContext(CommonContext):
    game = "Mortal Kombat: Shaolin Monks"
    items_handling = 0b111  # receive all items, even though we don't act on them yet
    want_slot_data = True
    command_processor = MKSMCommandProcessor
    game_interface: MKSMInterface
    game_state: GameState
    prev_state: GameState
    is_paused: bool
    set_upgrades_in_pause: bool = False
    health_upgrades: int = 0
    xp_items_given: int = 0
    first_loop: bool
    pending_server_address: str | None
    emulator_settled: bool
    was_dead: bool
    message_queue: deque
    currently_printing: bool = False
    print_start_time: float

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)
        self.is_paused = False
        self.game_interface = MKSMInterface(logger)
        self.synced_koins = False  # set True after the one-time on-connect memory sync
        self.game_state = GameState.BOOTING
        self.prev_state = GameState.BOOTING
        self.slot_data = None
        self.first_loop = True
        self.pending_server_address = None
        self.emulator_settled = False
        self.was_dead = False
        self.message_queue = deque()

    def ready_to_connect(self) -> bool:
        return self.emulator_settled and self.game_interface.get_game_state() == GameState.MAIN_MENU

    async def connect(self, address: str | None = None) -> None:
        # gates the GUI's Connect button too, since it calls ctx.connect() directly
        # rather than going through the command processor's _cmd_connect.
        if not self.ready_to_connect():
            logger.info("can't connect - not at the main menu.")
            return
        await super().connect(address)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        self.game_interface.kill_player()

    def on_print_json(self, args: dict):
        super().on_print_json(args)
        self.message_queue.append(
            self.rawjsontotextparser(copy.deepcopy(args["data"]))
        )


async def game_watcher(ctx: MKSMContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.01)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.game_interface.get_connection_state():
            ctx.synced_koins = False  # re-sync on the next successful (re)connect
            ctx.game_interface.connect_to_game()
            await asyncio.sleep(EMULATOR_RECONNECT_DELAY)
            continue

        if ctx.server is None or ctx.slot is None:
            # don't connect to the AP server until a settled read shows the game sitting at
            # the main menu - connecting while memory is still mid-boot/reset (and possibly
            # garbage) is exactly what's caused the reset-related corruption bugs elsewhere
            # in this client. "settled" just means we've already read game state once since
            # the emulator connection was (re)established - this loop's previous iteration.
            if (ctx.emulator_settled and ctx.pending_server_address
                    and ctx.game_interface.get_game_state() == GameState.MAIN_MENU):
                ctx.server_address = ctx.pending_server_address
                ctx.pending_server_address = None
                ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

            ctx.emulator_settled = True
            continue  # not connected to the AP server yet

        try:
            await run_callbacks(ctx)
        except Exception:
            # Without this, any exception raised anywhere in the callback chain
            # (a PINE read/write hiccup, a bad address, anything) kills this
            # task silently and for good - the watcher just stops ticking with
            # no visible error until the client process exits.
            logger.exception("Error while running MKSM game watcher callbacks")


async def main(args) -> None:
    ctx = MKSMContext(None, args.password)
    ctx.auth = args.name
    ctx.pending_server_address = args.connect  # held back until game_watcher's connect gate opens

    if gui_enabled:
        ctx.run_gui()
    else:
        ctx.run_cli()

    ctx.set_notify("EVENT_ARRAY")
    ctx.set_notify("CURRENT_XP")
    ctx.set_notify("XP_ITEMS_GIVEN")
    watcher_task = asyncio.create_task(game_watcher(ctx), name="MKSMGameWatcher")

    await ctx.exit_event.wait()

    ctx.game_interface.disconnect_from_game()
    await watcher_task
    await ctx.shutdown()


def launch(*launch_args: str) -> None:
    import colorama

    if not logging.getLogger().handlers:
        # Launched via the graphical Launcher's component click: this runs in a fresh
        # multiprocessing.Process with no console attached, and the __main__ guard below
        # never fires (we're called as an imported function, not as the main script), so
        # logging is otherwise never configured here - any startup exception would be
        # completely invisible (no console, no log file) without this.
        Utils.init_logging("MKSMClient", exception_logger="Client")

    parser = get_base_parser(description="Mortal Kombat: Shaolin Monks Archipelago Client")
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(launch_args)
    args = handle_url_arg(args, parser=parser)

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    Utils.init_logging("MKSMClient", exception_logger="Client")
    launch(*sys.argv[1:])
