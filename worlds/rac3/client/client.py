"""This module provides a launchable client for connecting RAC3 running on PCSX2 Emulation to a Multiworld"""
from asyncio import create_task, run, sleep, Task
from multiprocessing import freeze_support
from time import time

from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from NetUtils import NetworkItem
from Utils import Any, async_start, init_logging
from worlds.rac3.client.callbacks import handle_respawn, pcsx2_sync_task, update
from worlds.rac3.client.message import ClientMessage
from worlds.rac3.client.rac3_interface import Rac3Interface
from worlds.rac3.client.texthelper import colorize_item_name
from worlds.rac3.constants.data.item import RAC3_ITEM_DATA_TABLE
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_type import ONE_HP_CHALLENGE_CHARACTERS
from worlds.rac3.constants.region import RAC3REGION

# Load Universal Tracker modules with aliases
tracker_loaded: bool = False
try:
    # noinspection PyUnusedImports
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
                    self.output("Not in game, please load a game file")
                    return False
                self.output(f"No Game Detected, please connect to {RAC3OPTION.GAME_TITLE_FULL}")
                return False
            self.output("No slot data, please connect to a multiworld server")
            return False
        self.output(f"Somehow this client isn't for {RAC3OPTION.GAME_TITLE_FULL}, delete this build and try again")
        return False

    @staticmethod
    def is_development_build() -> bool:
        """Checks if this is a development build by looking for -dev or a subversion."""
        return "-dev" in RAC3OPTION.VERSION_NUMBER or RAC3OPTION.VERSION_NUMBER.count(".") >= 3

    # This is not mandatory for the game. Just a client command implementation.
    def _cmd_kill(self):
        """Kill the player."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            if self.ctx.death_link:
                self.ctx.on_deathlink({"time": time(), "cause": "Amondo got gaslit", "source": "Amondo"})
            else:
                self.output("Death Link is not enabled. You can toggle Death Link with /deathlink")

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
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context) and self.ctx.slot is not None:
            if not self.is_development_build():
                self.default('Development command "weapon_exp_test" was used in a non-development build.')

            if self.ctx.slot_data[RAC3OPTION.PROGRESSIVE_WEAPONS]:
                self.output("Weapon EXP item not compatible with Progressive Weapons")
            else:
                self.ctx.game_interface.item_received(RAC3_ITEM_DATA_TABLE[RAC3ITEM.WEAPON_XP].AP_CODE,
                                                      self.ctx.player_names.get(self.ctx.slot, None), "Test Command", 0)
                self.output("Weapon EXP Received")

    def _cmd_bolt_test(self):
        """Give bolts for testing purposes."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context) and self.ctx.slot is not None:
            if not self.is_development_build():
                self.default('Development command "bolt_test" was used in a non-development build.')
            self.ctx.game_interface.item_received(RAC3_ITEM_DATA_TABLE[RAC3ITEM.BOLTS].AP_CODE,
                                                  self.ctx.player_names[self.ctx.slot], "Test Command", 0)
            self.output("Bolts Received")

    def _cmd_rac3_info(self):
        """Dump Rac3 info for debugging purposes."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.dump_info(self.ctx.slot_data)

    def _cmd_force_update(self):
        """Force an update to the game state by running all update cycle methods."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            update(self.ctx)
            self.output("Update cycle complete")
            self.ctx.code_cave_setup = False
            self.output("Forcing reset of code cave")

    def _cmd_deathlink(self):
        """Toggles Death Link on and off."""
        if not self.verify(2):
            return
        if isinstance(self.ctx, Rac3Context):
            if RAC3OPTION.DEATHLINK in self.ctx.slot_data.keys():
                self.ctx.death_link = not self.ctx.death_link
                async_start(self.ctx.update_death_link(self.ctx.death_link))
                self.output(f"Death Link set to {self.ctx.death_link}")
                if self.verify():
                    self.ctx.game_interface.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.WHITE}Death Link {'Enabled' if self.ctx.death_link else 'Disabled'}",
                        RAC3BOXTHEME.DEATHLINK)
            else:
                self.output("Death Link not found in slot_data. Please report this")

    def _cmd_respawn(self):
        """Teleports Ratchet back to the ship. If used in an unusual place, forces a respawn instead.
        You can also pause the game and hold Square on the pause menu to run this command from in-game."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            create_task(handle_respawn(self.ctx, True))

    def _cmd_homewarp(self):
        """Loads Ratchet back on the Phoenix. Does nothing if used during the intro before reaching the Phoenix.
        Also activated with the following button combo: L2 + R2 + L1 + R1 + SELECT"""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            self.output("Attempting to homewarp to the Phoenix...")
            create_task(handle_respawn(self.ctx, force_load=True))

    def _cmd_ryno(self):
        """Toggles the maximum upgrade level for the RYNO between lv5 and lv4"""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.ryno = not self.ctx.game_interface.ryno
            if self.ctx.game_interface.ryno:
                self.output("RYNO max upgrade is Lv4")
                if self.verify():
                    self.ctx.game_interface.enqueue_notification("RY3NO max upgrade set to Lv4")
            else:
                self.output("RYNO max upgrade is Lv5")
                if self.verify():
                    self.ctx.game_interface.enqueue_notification("RY3NO max upgrade set to Lv5")

    def _cmd_messagebox(self, *args):
        """Displays a message box in-game with the specified message."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            message = " ".join(args).replace("\\n", "\n")
            self.ctx.game_interface.enqueue_notification(message[:250:], duration=5.0)
            if len(message) > 250:
                self.output("Message longer than 250 characters, truncated to fit in message box.")
            self.output(f"Message box displayed with message: {message[:250:]}")

    def _cmd_one_hp(self, *args):
        """Toggles One HP Challenge for the specified character."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            character = " ".join(args).lower()
            valid_characters = {name.lower(): name for name in ONE_HP_CHALLENGE_CHARACTERS}
            if character in valid_characters:
                char_name = valid_characters[character]
                current_state = self.ctx.game_interface.one_hp_challenge.get(char_name, 0)
                new_state = 0 if current_state else 1
                self.ctx.game_interface.one_hp_challenge[char_name] = new_state
                self.output(f'One HP Challenge for {char_name} set to {"Enabled" if new_state else "Disabled"}')
                self.ctx.game_interface.enqueue_notification(
                    f'One HP Challenge for {char_name} {"Enabled" if new_state else "Disabled"}')
            else:
                self.output(f'Invalid character name. Valid options are: {", ".join(ONE_HP_CHALLENGE_CHARACTERS)}')

    def _cmd_print_vendor(self):
        """Print all items sold by the current planet's vendor to the log."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            self.ctx.game_interface.print_all_vendor_items()

    def _cmd_load_level(self, *args):
        """Loads the specified level by ID. This is not intended for normal use, but can be used for testing or to
        recover from softlocks."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            if not self.is_development_build():
                self.default('Development command "load_level" was used in a non-development build.')
            if not args:
                self.output("No level specified. Provide an integer ID or region name.")
                return

            arg = args[0]
            # If the argument is already an int, call directly
            if isinstance(arg, int):
                self.ctx.game_interface.homewarp(arg)
                return

            # Try to parse as integer string first
            try:
                level_id = int(arg)
                self.ctx.game_interface.homewarp(level_id)
                return
            except ValueError:
                # Not an integer string — treat as a region key/name and look up its ID (case-insensitive)
                key = str(arg).strip()
                region = RAC3_REGION_DATA_TABLE.get(key)
                if region is None:
                    lower_key = key.lower()
                    for k, v in RAC3_REGION_DATA_TABLE.items():
                        if k.lower() == lower_key:
                            region = v
                            break
                if region is not None:
                    level_id = region.ID
                    self.ctx.game_interface.homewarp(level_id)
                    return
                self.output("Invalid level ID or region name. Provide an integer or valid region key.")

    def _cmd_traversal(self, *args):
        """Test command for linked list traversal purposes."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            if not self.is_development_build():
                # let everyone know that a development command was used in a release build.
                self.default('Development command "traversal" was used in a non-development build.')

            # convert the hex input to an int and then do traversal with that as the target id
            try:
                target_id = int(args[0], 16)
                start_address = int(args[1], 16)
            except ValueError:
                self.output("Invalid target ID. Please provide a valid hexadecimal number.")
                return
            # try addresses in intervals of 0x100 to see if we find any good ones
            for addr in range(start_address, start_address + 0x10000, 0x100):
                moby_addr = self.ctx.game_interface.find_moby_by_id_traversal(target_id, addr)
                if moby_addr is not None:
                    self.output(
                        f"Found moby with ID {hex(target_id)} at address {hex(moby_addr)} with start address "
                        f"{hex(addr)}")

    def _cmd_iteration(self, *args):
        """Test command for linked list iteration purposes."""
        if not self.verify():
            return
        if isinstance(self.ctx, Rac3Context):
            if not self.is_development_build():
                # let everyone know that a development command was used in a release build.
                self.default('Development command "iteration" was used in a non-development build.')

            # convert the hex input to an int and then do iteration with that as the target id
            try:
                target_id = int(args[0], 16)
                start_address = int(args[1], 16)
            except ValueError:
                self.output("Invalid target ID. Please provide a valid hexadecimal number.")
                return
            moby_addr = self.ctx.game_interface.find_moby_by_id_iteration(target_id, start_address)
            if moby_addr is not None:
                self.output(f"Found moby with ID {hex(target_id)} at address {hex(moby_addr)}")
            else:
                self.output(f"Could not find moby with ID {hex(target_id)} by iterating from {hex(start_address)}")


class Rac3Context(CommonContext):
    """Class for handling server connection with the game client"""
    # Client variables
    already_hinted: set[int] = set()
    command_processor = CommandProcessor
    current_planet: str = RAC3REGION.GALAXY
    current_map: str = RAC3REGION.GALAXY
    death_link: bool = False
    game: str = RAC3OPTION.GAME_TITLE_FULL
    game_interface: Rac3Interface
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    items_handling: int = 0b111  # This is mandatory
    last_game_message: str | None = None
    last_pine_message: str | None = None
    last_server_message: str | None = None
    main_menu: bool = True
    pcsx2_sync_task: Task | None = None
    processed_item_count: int = 0
    queued_deaths: int = 0
    slot_data: dict[str, Any] | None = None
    last_deathlink_msg: str | None = None
    last_deathlink_sender: str | None = None
    code_cave_setup: bool = False
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
        """Authenticate with the Multiworld server."""
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data: dict[str, Any] = args["slot_data"]
            # logger.info(f"Received data: {args}")
            self.game_interface.proc_option(self.slot_data)
            self.locations_scouted = self.server_locations
            self.code_cave_setup = False
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
            logger.debug(f"Data Package received with args {args}")
            if RAC3OPTION.GAME_TITLE_FULL in args["data"]["games"]:
                self.data_package = args["data"]["games"][RAC3OPTION.GAME_TITLE_FULL][RAC3OPTION.PROCESSED_LOCATIONS]
                logger.debug(f"Data Package updated: {self.data_package}")
                async_start(self.send_msgs([{"cmd": "Sync"}]))
        if cmd == "PrintJSON":
            if args.get("type") == "Hint" and self.is_connected_to_game and not self.main_menu:
                net_item: NetworkItem | None = args.get("item")
                if net_item is None:
                    logger.warning("Received PrintJSON command with type Hint but no item data!")
                    return
                location_name = self.location_names.lookup_in_slot(net_item.location, net_item.player)
                receiving_player = args.get("receiving", -1)
                item_name = colorize_item_name(self.item_names.lookup_in_slot(net_item.item, receiving_player),
                                               net_item.flags)
                format_color = RAC3TEXTFORMATSTRING.NORMAL if self.slot_concerns_self(receiving_player) else (
                    RAC3TEXTFORMATSTRING.GREEN)
                player_name = self.player_names.get(receiving_player, "???")
                hint_text = (
                    f"{RAC3TEXTFORMATSTRING.WHITE}Hint: {format_color}{player_name}{RAC3TEXTFORMATSTRING.WHITE}'s "
                    f"{item_name}{RAC3TEXTFORMATSTRING.WHITE} is at\n{RAC3TEXTFORMATSTRING.GREEN}{location_name}")
                if not self.slot_concerns_self(net_item.player):
                    player_name = self.player_names.get(net_item.player, "???")
                    format_color = RAC3TEXTFORMATSTRING.NORMAL if self.slot_concerns_self(net_item.player) else (
                        RAC3TEXTFORMATSTRING.GREEN)
                    hint_text += (f"\n{RAC3TEXTFORMATSTRING.WHITE}in {format_color}{player_name}"
                                  f"{RAC3TEXTFORMATSTRING.WHITE}'s world.")
                self.game_interface.enqueue_notification(hint_text, RAC3BOXTHEME.HINT)


def launch_client():
    """Launch an instance of the Ratchet and Clank 3 client"""
    init_logging(f"{RAC3OPTION.GAME_TITLE}_Client")

    async def main():
        """The main client process"""
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
