# Common import
from asyncio import create_task, run, sleep, Task
from multiprocessing import freeze_support
from traceback import format_exc
from typing import Optional

from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from Utils import Any, async_start, Dict, init_logging
from worlds.rac3.client.callbacks import init, update
from worlds.rac3.client.interface import Rac3Interface
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION

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
CLIENT_VERSION = "0.1.0"  # This is automatically updated by the GitHub actions workflow


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

    def _cmd_respawn(self):
        """Teleports Ratchet back to the ship. If used in an unusual place, forces a respawn instead.
        You can also pause the game and hold Square on the pause menu to run this command from in-game."""
        if isinstance(self.ctx, Rac3Context):
            pause_address = RAC3_REGION_DATA_TABLE[self.ctx.current_planet].PAUSE_ADDRESS
            if pause_address is not None:
                self.ctx.game_interface.unpause_game(self.ctx.current_planet)
                self.ctx.game_interface.teleport_to_ship(self.ctx.current_planet)
            else:
                self.output(f'Ship teleport is disabled on {self.ctx.current_planet}.')


class Rac3Context(CommonContext):
    # Client variables
    command_processor = CommandProcessor
    game_interface: Rac3Interface
    game = RAC3OPTION.GAME_TITLE_FULL
    pcsx2_sync_task: Optional[Task] = None
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    slot_data: Optional[dict[str, Any]] = None
    last_server_message: Optional[str] = None
    last_pine_message: Optional[str] = None
    last_game_message: Optional[str] = None
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


async def pcsx2_sync_task(ctx: Rac3Context):
    logger.info(f"Starting {RAC3OPTION.GAME_TITLE_FULL} Connector")

    while not ctx.exit_event.is_set():
        try:
            connected_to_server = (ctx.server is not None) and (ctx.slot is not None)
            connected_to_game = ctx.game_interface.get_connection_state()

            if connected_to_server and not ctx.is_connected_to_server:
                logger.info("Connected to server")
                ctx.is_connected_to_server = connected_to_server
                if connected_to_game:
                    await init(ctx)
                else:
                    logger.info("Waiting for game connection...")

            if connected_to_game and not ctx.is_connected_to_game:
                logger.info(f"Connected to {RAC3OPTION.GAME_TITLE_FULL}")
                ctx.last_pine_message = None
                ctx.is_connected_to_game = connected_to_game
                if connected_to_server:
                    await init(ctx)
                else:
                    logger.info("Waiting for server connection...")

            if not connected_to_game:
                if ctx.is_connected_to_game:
                    ctx.game_interface.disconnect_from_game()
                    logger.info("Connection to game lost, attempting to reconnect...")
                elif ctx.last_pine_message is None:
                    message = "Not connected to the PCSX2 instance, attempting to connect..."
                    logger.info(message)
                    ctx.last_pine_message = message
                ctx.game_interface.connect_to_game()

            if not connected_to_server:
                if ctx.server:
                    ctx.last_server_message = None
                elif ctx.last_server_message is None:
                    message = "Waiting for player to connect to server"
                    logger.info(message)
                    ctx.last_server_message = message

            if connected_to_game and connected_to_server:
                await _handle_game_ready(ctx)

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
        await sleep(1)
    logger.info(f"{RAC3OPTION.GAME_TITLE_FULL} Client Shutdown")


async def _handle_game_ready(ctx: Rac3Context) -> None:
    # Quite a lot of stuff ended up in this function, even though it might
    # have fit better in init(). It just didn't work when I put it there,
    # probably because of when the game loads stuff.

    if ctx.slot_data is not None:
        # Check if exit to main menu
        menu = ctx.main_menu
        ctx.main_menu = ctx.game_interface.check_main_menu()

        if ctx.main_menu:
            if ctx.last_game_message is None:
                message = "Currently on Main Menu, please load a file..."
                logger.info(message)
                ctx.last_game_message = message

        if menu is True and ctx.main_menu is False:
            logger.info("Starting game...")
            ctx.game_interface.reset_file()
            logger.info("Old state removed!")
            logger.info("Checking for items...")
            for item in ctx.items_received:
                ctx.game_interface.item_received(item.item)
            ctx.processed_item_count = len(ctx.items_received)
            logger.info("Items received!")
            logger.info("Checking locations...")
            for loc in ctx.locations_checked:
                ctx.game_interface.collect_location(loc)
            logger.info("Locations collected!")
            logger.info("Checking cosmetics...")
            ctx.game_interface.add_cosmetics()
            logger.info("Load the latest autosave to apply cosmetics")
            logger.info("Game READY!")

        if not ctx.main_menu:
            await update(ctx)
            await sleep(1)


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
