# Common import
import asyncio
import multiprocessing
import traceback
from typing import Optional

import Utils
from CommonClient import get_base_parser, gui_enabled, logger, server_loop

# Load Universal Tracker modules with aliases
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (TrackerCommandProcessor as ClientCommandProcessor,
                                              TrackerGameContext as CommonContext, UT_VERSION)

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext

    print("ERROR: Universal Tracker is not loaded")

# Game title dedicated
from . import Locations
# from .data.Constants import EPISODES
from .Rac3Interface import Rac3Interface
from .Rac3Callbacks import init, update
from .Rac3Options import GAME_TITLE, GAME_TITLE_FULL

CLIENT_INIT_LOG = f"{GAME_TITLE}_Client"
CLIENT_VERSION = "0.1.0"


class CommandProcessor(ClientCommandProcessor):
    # This is not mandatory for the game. Just a client command implementation.
    # def _cmd_kill(self):
    #     """Kill the game."""
    #     if isinstance(self.ctx, Rac3Context):
    #         self.ctx.game_interface.kill_player()
    def _cmd_weapon_exp_test(self):
        """Give weapon exp for testing purposes."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.received_others(50000092)

    def _cmd_bolt_test(self):
        """Give bolts for testing purposes."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.received_others(50000091)

    def _cmd_rac3_info(self):
        """Dump Rac3 info for debugging purposes."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.dump_info(self.ctx.current_planet, self.ctx.slot_data)

    def _cmd_force_update(self):
        """Force an update to the game state by running all update cycle methods."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.update()


class Rac3Context(CommonContext):
    # Client variables
    command_processor = CommandProcessor
    game_interface: Rac3Interface
    game = f"{GAME_TITLE_FULL}"
    pcsx2_sync_task: Optional[asyncio.Task] = None
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    slot_data: Optional[dict[str, Utils.Any]] = None
    last_error_message: Optional[str] = None
    notification_queue: list[str] = []
    notification_timestamp: float = 0
    showing_notification: bool = False
    deathlink_timestamp: float = 0
    death_link_enabled = False
    queued_deaths: int = 0
    current_planet: str = 'Galaxy'
    main_menu: bool = True

    items_handling = 0b111  # This is mandatory

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = Rac3Interface(logger)

    def notification(self, text: str):
        self.notification_queue.append(text)

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        if self.death_link_enabled:
            self.queued_deaths += 1
            cause = data.get("cause", "")
            if cause:
                self.notification(f"DeathLink: {cause}")
            else:
                self.notification(f"DeathLink: Received from {data['source']}")

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"{GAME_TITLE} Client v{CLIENT_VERSION}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"

        # AP version is added behind this automatically
        ui.base_title += " | Archipelago"
        return ui

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(Rac3Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            # logger.info(f"Received data: {args}")
            self.game_interface.proc_option(self.slot_data)

            # Set death link tag if it was requested in options
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))
                Utils.async_start(self.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": [
                        Locations.location_table[location].ap_code
                        for location in Locations.location_groups["Purchase"]
                    ]
                }]))


def update_connection_status(ctx: Rac3Context, status: bool):
    if ctx.is_connected_to_game == status:
        return

    if status:
        logger.info(f"Connected to {GAME_TITLE}")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")

    ctx.is_connected_to_game = status


async def pcsx2_sync_task(ctx: Rac3Context):
    logger.info(f"Starting {GAME_TITLE} Connector, attempting to connect to emulator...")
    ctx.game_interface.connect_to_game()
    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
        except ConnectionError:
            logger.info(f"ConnectionError")
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            logger.info(f"ExceptionError")
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


async def _handle_game_ready(ctx: Rac3Context) -> None:
    connected_to_server = (ctx.server is not None) and (ctx.slot is not None)

    new_connection = ctx.is_connected_to_server != connected_to_server
    if new_connection:
        await init(ctx, connected_to_server)
        ctx.is_connected_to_server = connected_to_server

    await update(ctx, connected_to_server)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)

    await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Rac3Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)


def launch_client():
    Utils.init_logging(CLIENT_INIT_LOG)

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = Rac3Context(args.connect, args.password)

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        # Runs Universal Tracker's internal generator
        if tracker_loaded:
            ctx.run_generator()
            ctx.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch_client()
