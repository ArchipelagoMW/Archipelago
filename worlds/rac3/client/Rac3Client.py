# Common import
from asyncio import create_task, run, sleep, Task
from multiprocessing import freeze_support
from traceback import format_exc
from typing import Optional

from client.Rac3Callbacks import init, update
from client.Rac3Interface import Rac3Interface
from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from constants.Rac3Options import RAC3OPTION
from constants.Rac3Region import RAC3REGION
from Utils import Any, async_start, Dict, init_logging

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

CLIENT_INIT_LOG = f"{RAC3OPTION.GAME_TITLE}_Client"
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
            self.ctx.game_interface.item_received(50000092)

    def _cmd_bolt_test(self):
        """Give bolts for testing purposes."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.item_received(50000091)

    def _cmd_rac3_info(self):
        """Dump Rac3 info for debugging purposes."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.dump_info(self.ctx.current_planet, self.ctx.slot_data)

    def _cmd_force_update(self):
        """Force an update to the game state by running all update cycle methods."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.update()

    def _cmd_deathlink(self):
        """If your Death Link setting is set to "Toggle", use this command to turn Death Link on and off."""
        if isinstance(self.ctx, Rac3Context):
            if RAC3OPTION.DEATHLINK in self.ctx.slot_data.keys():
                if self.ctx.slot_data[RAC3OPTION.DEATHLINK] == "toggle":
                    self.ctx.death_link = not self.ctx.death_link
                    self.output(f'Death Link set to {self.ctx.death_link}')
                else:
                    self.output(f"Death Link is not set to 'toggle' for this seed")
                    self.output(f"Death Link = {self.ctx.slot_data[RAC3OPTION.DEATHLINK]}")
            else:
                self.output(f"Death Link not found in slot_data. You are probably not connected")


class Rac3Context(CommonContext):
    # Client variables
    command_processor = CommandProcessor
    game_interface: Rac3Interface
    game = RAC3OPTION.GAME_TITLE_FULL
    pcsx2_sync_task: Optional[Task] = None
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    slot_data: Optional[dict[str, Any]] = None
    last_error_message: Optional[str] = None
    death_link = False
    queued_deaths: int = 0
    current_planet: str = RAC3REGION.GALAXY
    main_menu: bool = True
    processed_item_count = 0

    items_handling = 0b111  # This is mandatory

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = Rac3Interface(logger)

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"Death Link: {text}")
        else:
            logger.info(f"Death Link: Received from {data['source']}")
        if self.death_link:
            self.queued_deaths += 1

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"{RAC3OPTION.GAME_TITLE} Client v{CLIENT_VERSION}"
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
            if RAC3OPTION.DEATHLINK in self.slot_data:
                self.death_link = bool(self.slot_data[RAC3OPTION.DEATHLINK])
                async_start(self.update_death_link(
                    bool(self.slot_data[RAC3OPTION.DEATHLINK])))

            # async_start(self.send_msgs([ClientMessage.location_scouts(
            #     [Locations.location_table[location].ap_code for location in Locations.location_groups["Purchase"]])]))


def update_connection_status(ctx: Rac3Context, status: bool):
    if ctx.is_connected_to_game == status:
        return

    if status:
        logger.info(f"Connected to {RAC3OPTION.GAME_TITLE}")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")

    ctx.is_connected_to_game = status


async def pcsx2_sync_task(ctx: Rac3Context):
    logger.info(f"Starting {RAC3OPTION.GAME_TITLE} Connector, attempting to connect to emulator...")
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
                logger.error(format_exc())
            await sleep(3)
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
            await sleep(1)
            return
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await sleep(1)

    await sleep(1)


async def _handle_game_not_ready(ctx: Rac3Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await sleep(3)


def launch_client():
    init_logging(CLIENT_INIT_LOG)

    async def main():
        freeze_support()
        logger.info("main")
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = Rac3Context(args.connect, args.password)

        logger.info("Connecting to server...")
        ctx.server_task = create_task(server_loop(ctx), name="Server Loop")

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
        ctx.pcsx2_sync_task = create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    colorama.init()

    run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch_client()
