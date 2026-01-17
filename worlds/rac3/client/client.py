# Common import
from asyncio import create_task, run, sleep, Task
from multiprocessing import freeze_support
from time import time
from traceback import format_exc
from typing import Optional

from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from Utils import Any, async_start, init_logging
from worlds.rac3 import RAC3_ITEM_DATA_TABLE, RAC3ITEM
from worlds.rac3.client.callbacks import handle_respawn, init, update
from worlds.rac3.client.interface import Rac3Interface
from worlds.rac3.client.message import ClientMessage
from worlds.rac3.constants.data.item import ITEM_FROM_AP_CODE
from worlds.rac3.constants.data.location import LOCATION_FROM_AP_CODE
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_type import ONE_HP_CHALLENGE_CHARACTERS
from worlds.rac3.constants.region import RAC3REGION

# Load Universal Tracker modules with aliases
tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (TrackerCommandProcessor as ClientCommandProcessor,
                                              TrackerGameContext as CommonContext, UT_VERSION)

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext

    print("ERROR: Universal Tracker is not loaded")


class CommandProcessor(ClientCommandProcessor):
    def verify(self, level: int = 4) -> bool:
        """
        Checks various levels of connection before allowing a command.
        Level 1: Client is for RAC 3
        Level 2: Client is connected to a multiworld server
        Level 3: Client is connected to the game
        Level 4: Player is in game
        """
        if isinstance(self.ctx, Rac3Context):
            if level == 1:
                return True
            if self.ctx.slot_data:
                if level == 2:
                    return True
                if self.ctx.is_connected_to_game:
                    if level == 3:
                        return True
                    if not self.ctx.main_menu:
                        return True
                    else:
                        self.output("Not in game, please load a game file")
                        return False
                else:
                    self.output(f"No Game Detected, please connect to {RAC3OPTION.GAME_TITLE_FULL}")
                    return False
            else:
                self.output("No slot data, please connect to a multiworld server")
                return False
        else:
            self.output(f"Somehow this client isn't for {RAC3OPTION.GAME_TITLE_FULL}, delete this build and try again")
            return False

    # This is not mandatory for the game. Just a client command implementation.
    def _cmd_kill(self):
        """Kill the game."""
        if isinstance(self.ctx, Rac3Context):
            self.ctx.on_deathlink({"time": time(), "cause": "Amondo got gaslit"})

    def _cmd_connect_rac3(self):
        """Attempt to connect the client to the emulator"""
        if not self.verify(1):
            return
        if isinstance(self.ctx, Rac3Context):
            if self.ctx.game_interface.get_connection_state():
                self.output("Already Connected to Emulator")
            else:
                self.ctx.game_interface.connect_to_game()

    # def _cmd_auto_connect(self):
    #     """Toggle the client attempting to connect to the emulator automatically"""
    #     if isinstance(self.ctx, Rac3Context):
    #         self.ctx.auto_connect = not self.ctx.auto_connect
    #         if self.ctx.auto_connect:
    #             logger.info("Emulator Auto-connect enabled")
    #         else:
    #             logger.info("Emulator Auto-connect disabled")
    #     else:
    #         logger.info("Somehow this client isn't for Ratchet and Clank 3, delete this build and try again")

    def _cmd_weapon_exp_test(self):
        """Give weapon exp for testing purposes."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            if self.ctx.slot_data[RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS]:
                self.output(f"Weapon EXP item not compatible with Progressive Weapons")
            else:
                self.ctx.game_interface.item_received(RAC3_ITEM_DATA_TABLE[RAC3ITEM.WEAPON_XP].AP_CODE,
                                                      self.ctx.player_names[self.ctx.slot], "Test Command", 0)
                self.output(f"Weapon EXP Received")

    def _cmd_bolt_test(self):
        """Give bolts for testing purposes."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.item_received(RAC3_ITEM_DATA_TABLE[RAC3ITEM.BOLTS].AP_CODE,
                                                  self.ctx.player_names[self.ctx.slot], "Test Command", 0)
            self.output(f"Bolts Received")

    def _cmd_rac3_info(self):
        """Dump Rac3 info for debugging purposes."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.dump_info(self.ctx.slot_data)

    def _cmd_force_update(self):
        """Force an update to the game state by running all update cycle methods."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            update(self.ctx)
            self.output(f"Update cycle complete")

    def _cmd_deathlink(self):
        """Toggles Death Link on and off."""
        if not self.verify(2):
            return
        if isinstance(self.ctx, Rac3Context):
            if RAC3OPTION.DEATHLINK in self.ctx.slot_data.keys():
                self.ctx.death_link = not self.ctx.death_link
                async_start(self.ctx.update_death_link(self.ctx.death_link))
                self.output(f'Death Link set to {self.ctx.death_link}')
            else:
                self.output(f"Death Link not found in slot_data. Please report this")

    def _cmd_respawn(self):
        """Teleports Ratchet back to the ship. If used in an unusual place, forces a respawn instead.
        You can also pause the game and hold Square on the pause menu to run this command from in-game."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            if create_task(handle_respawn(self.ctx, True)):
                self.output(f'Player respawned on {self.ctx.current_planet}')
            else:
                self.output(f'Player cannot respawn right now')

    def _cmd_ryno(self):
        """Toggles the maximum upgrade level for the RYNO between lv5 and lv4"""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.ryno = not self.ctx.game_interface.ryno
            if self.ctx.game_interface.ryno:
                self.output(f'RYNO max upgrade is Lv4')
            else:
                self.output(f'RYNO max upgrade is Lv5')

    def _cmd_messagebox(self, *args):
        """Displays a message box in-game with the specified message."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            message = " ".join(args)
            self.ctx.game_interface.notification_queue.append((message[:225:], RAC3BOXTHEME.DEFAULT))
            if len(message) > 225:
                self.output(f'Message longer than 225 characters, truncated to fit in message box.')
            self.output(f'Message box displayed with message: {message[:225:]}')
    
    def _cmd_one_hp(self, *args):
        """Toggles One HP Challenge for the specified character."""
        if not self.verify(4):
            return
        if isinstance(self.ctx, Rac3Context):
            character = " ".join(args).lower()
            valid_characters = {name.lower(): name for name in ONE_HP_CHALLENGE_CHARACTERS}
            if character in valid_characters:
                char_name = valid_characters[character]
                current_state = self.ctx.game_interface.one_hp_challenge.get(char_name, False)
                new_state = not current_state
                self.ctx.game_interface.one_hp_challenge[char_name] = new_state
                self.output(f'One HP Challenge for {char_name} set to {new_state}')
            else:
                self.output(f'Invalid character name. Valid options are: {", ".join(ONE_HP_CHALLENGE_CHARACTERS)}')


class Rac3Context(CommonContext):
    # Client variables
    command_processor = CommandProcessor
    current_planet: str = RAC3REGION.GALAXY
    death_link: bool = False
    game: str = RAC3OPTION.GAME_TITLE_FULL
    game_interface: Rac3Interface
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    items_handling: int = 0b111  # This is mandatory
    last_game_message: Optional[str] = None
    last_pine_message: Optional[str] = None
    last_server_message: Optional[str] = None
    main_menu: bool = True
    pcsx2_sync_task: Optional[Task] = None
    processed_item_count: int = 0
    queued_deaths: int = 0
    slot_data: Optional[dict[str, Any]] = None
    last_deathlink_msg: Optional[str] = None
    last_deathlink_sender: Optional[str] = None
    data_package: int = 0

    def __init__(self, server_address: str, password: str):
        super().__init__(server_address, password)
        self.game_interface = Rac3Interface()

    def on_deathlink(self, data: dict[str, Any]) -> None:
        text = data.get("cause", "")
        if text:
            logger.info(f"Death Link: {text}")
        else:
            logger.info(f"Death Link: Received from {data['source']}")
        if self.death_link:
            self.queued_deaths += 1
            self.last_deathlink_msg = text if text else "???"
            self.last_deathlink_sender = data.get("source", "???")

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"{RAC3OPTION.GAME_TITLE} Client v{RAC3OPTION.VERSION_NUMBER}"
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
            self.locations_scouted = self.server_locations
            async_start(self.send_msgs([ClientMessage.location_scouts(list(self.server_locations))]))
            # async_start(self.send_msgs([{"cmd": "GetDataPackage", "games": [RAC3OPTION.PROCESSED_LOCATIONS]}]))

            # Set death link tag if it was requested in options
            if RAC3OPTION.DEATHLINK in self.slot_data:
                if self.slot_data[RAC3OPTION.DEATHLINK]:
                    self.death_link = bool(self.slot_data[RAC3OPTION.DEATHLINK])
                    async_start(self.update_death_link(self.death_link))

            # async_start(self.send_msgs([ClientMessage.location_scouts(
            #     [Locations.location_table[location].ap_code for location in Locations.location_groups["Purchase"]])]))
        if cmd == "DataPackage":
            logger.debug(f'Data Package received with args {args}')
            if RAC3OPTION.GAME_TITLE_FULL in args["data"]["games"]:
                self.data_package = args["data"]["games"][RAC3OPTION.GAME_TITLE_FULL][RAC3OPTION.PROCESSED_LOCATIONS]
                logger.debug(f"Data Package updated: {self.data_package}")
                async_start(self.send_msgs([{'cmd': 'Sync'}]))


async def pcsx2_sync_task(ctx: Rac3Context):
    logger.info(f"Starting {RAC3OPTION.GAME_TITLE_FULL} Connector")
    connected_to_game: bool = False
    connection_retry_attempts: int = 0
    while not ctx.exit_event.is_set():
        try:
            connected_to_server = (ctx.server is not None) and (ctx.slot is not None)
            if connected_to_server and not ctx.is_connected_to_server:
                logger.info("Connected to server")
                ctx.is_connected_to_server = connected_to_server
                if ctx.slot_data.get(RAC3OPTION.VERSION, "0.0.0") < RAC3OPTION.VERSION_NUMBER:
                    await ctx.disconnect(False)
                    logger.warning(
                        f"Client is v{RAC3OPTION.VERSION_NUMBER}, please downgrade to v"
                        f"{ctx.slot_data[RAC3OPTION.VERSION]}")
                    await sleep(10)
                    continue
                if ctx.slot_data[RAC3OPTION.VERSION] > RAC3OPTION.VERSION_NUMBER:
                    await ctx.disconnect(False)
                    logger.warning(
                        f"Client is v{RAC3OPTION.VERSION_NUMBER}, please upgrade to v"
                        f"{ctx.slot_data[RAC3OPTION.VERSION]}")
                    await sleep(10)
                    continue
                if connected_to_game:
                    await init(ctx)
                else:
                    logger.info("Waiting for game connection...")

            connected_to_game = ctx.game_interface.get_connection_state()
            if connected_to_game and not ctx.is_connected_to_game:
                logger.info(f"Connected to {RAC3OPTION.GAME_TITLE_FULL}")
                ctx.last_pine_message = None
                ctx.is_connected_to_game = connected_to_game
                if connected_to_server:
                    await init(ctx)
                else:
                    logger.info("Waiting for server connection...")

            if not connected_to_game and not ctx.game_interface.is_connecting:
                if ctx.is_connected_to_game:
                    ctx.game_interface.disconnect_from_game()
                    logger.info("Connection to game lost")
                elif ctx.last_pine_message is None:
                    message = "Not connected to the PCSX2 instance"
                    logger.info(message)
                    ctx.last_pine_message = message
                ctx.game_interface.connect_to_game()
                if not ctx.game_interface.get_connection_state():
                    if connection_retry_attempts < 3:
                        connection_retry_attempts += 1

                    retry_wait = connection_retry_attempts * 10
                    logger.warning(f'Could not connect to RaC3! Will retry connection in {retry_wait} seconds...')
                    await sleep(retry_wait)
                else:
                    connection_retry_attempts = 0

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
            # await sleep(3)

        await sleep(0.5)
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
            if menu:
                ctx.game_interface.main_menu = True
            if ctx.last_game_message is None:
                message = "Currently on Main Menu, please load a file..."
                logger.info(message)
                ctx.last_game_message = message
            await sleep(5)

        if menu is True and ctx.main_menu is False:
            await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_PLAYING)])
            logger.info("Starting game...")
            ctx.game_interface.reset_file()
            logger.info("Old state removed!")
            logger.info("Checking for items...")
            logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")
            logger.info(f"Items Received: {len(ctx.items_received)}")
            items_to_process = ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, len(ctx.items_received))
            counter = 0
            for count, item in enumerate(ctx.items_received):
                counter += 1
                logger.debug(f"Processing item {count}: {ITEM_FROM_AP_CODE[item.item]}")
                if count > items_to_process:
                    logger.debug(f"Handle Later")
                    continue
                ctx.game_interface.important_items(item.item, ctx.player_names[ctx.slot], ctx.player_names[
                    item.player], item.location)
            ctx.processed_item_count = min(counter, items_to_process)
            await ctx.send_msgs([ClientMessage.set_processed(ctx.processed_item_count)])
            logger.info(f"Items Processed: {ctx.processed_item_count}")
            logger.info("Checking locations...")
            counter = 0
            for loc in ctx.checked_locations:
                logger.debug(f"Collecting location: {LOCATION_FROM_AP_CODE[loc]}")
                ctx.game_interface.collect_location(loc)
                counter += 1
            logger.info(f"Locations collected: {counter}")
            ctx.game_interface.fix_health()
            ctx.game_interface.reset_death_count()
            logger.info("Checking cosmetics...")
            ctx.game_interface.add_cosmetics()
            logger.info("Load the latest autosave to apply cosmetics")
            logger.info("Game READY!")

        if not ctx.main_menu:
            await update(ctx)
            logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")


def launch_client():
    init_logging(f"{RAC3OPTION.GAME_TITLE}_Client")

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
