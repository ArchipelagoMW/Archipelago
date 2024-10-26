import logging
import os
import subprocess
from logging import Logger

import colorama

import asyncio
from asyncio import Task

from typing import Set, Awaitable, Optional, List

import pymem
from pymem.exception import ProcessNotFound

import Utils
from NetUtils import ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled
from .Options import EnableOrbsanity

from .GameID import jak1_name
from .client.ReplClient import JakAndDaxterReplClient
from .client.MemoryReader import JakAndDaxterMemoryReader

import ModuleUpdate
ModuleUpdate.update()


logger = logging.getLogger("JakClient")
all_tasks: Set[Task] = set()


def create_task_log_exception(awaitable: Awaitable) -> asyncio.Task:
    async def _log_exception(a):
        try:
            return await a
        except Exception as e:
            logger.exception(e)
        finally:
            all_tasks.remove(task)
    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)
    return task


class JakAndDaxterClientCommandProcessor(ClientCommandProcessor):
    ctx: "JakAndDaxterContext"

    # The command processor is not async so long-running operations like the /repl connect command
    # (which takes 10-15 seconds to compile the game) have to be requested with user-initiated flags.
    # The flags are checked by the agents every main_tick.
    def _cmd_repl(self, *arguments: str):
        """Sends a command to the OpenGOAL REPL. Arguments:
        - connect : connect the client to the REPL (goalc).
        - status : check internal status of the REPL."""
        if arguments:
            if arguments[0] == "connect":
                self.ctx.on_log_info(logger, "This may take a bit... Wait for the success audio cue before continuing!")
                self.ctx.repl.initiated_connect = True
            if arguments[0] == "status":
                create_task_log_exception(self.ctx.repl.print_status())

    def _cmd_memr(self, *arguments: str):
        """Sends a command to the Memory Reader. Arguments:
        - connect : connect the memory reader to the game process (gk).
        - status : check the internal status of the Memory Reader."""
        if arguments:
            if arguments[0] == "connect":
                self.ctx.memr.initiated_connect = True
            if arguments[0] == "status":
                create_task_log_exception(self.ctx.memr.print_status())


class JakAndDaxterContext(CommonContext):
    game = jak1_name
    items_handling = 0b111  # Full item handling
    command_processor = JakAndDaxterClientCommandProcessor

    # We'll need two agents working in tandem to handle two-way communication with the game.
    # The REPL Client will handle the server->game direction by issuing commands directly to the running game.
    # But the REPL cannot send information back to us, it only ingests information we send it.
    # Luckily OpenGOAL sets up memory addresses to write to, that AutoSplit can read from, for speedrunning.
    # We'll piggyback off this system with a Memory Reader, and that will handle the game->server direction.
    repl: JakAndDaxterReplClient
    memr: JakAndDaxterMemoryReader

    # And two associated tasks, so we have handles on them.
    repl_task: asyncio.Task
    memr_task: asyncio.Task

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        self.repl = JakAndDaxterReplClient(self.on_log_error,
                                           self.on_log_warn,
                                           self.on_log_success,
                                           self.on_log_info)
        self.memr = JakAndDaxterMemoryReader(self.on_location_check,
                                             self.on_finish_check,
                                             self.on_deathlink_check,
                                             self.on_deathlink_toggle,
                                             self.on_orb_trade,
                                             self.on_log_error,
                                             self.on_log_warn,
                                             self.on_log_success,
                                             self.on_log_info)
        # self.repl.load_data()
        # self.memr.load_data()
        super().__init__(server_address, password)

    def run_gui(self):
        from kvui import GameManager

        class JakAndDaxterManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Jak and Daxter ArchipelaGOAL Client"

        self.ui = JakAndDaxterManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(JakAndDaxterContext, self).server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):

        if cmd == "Connected":
            slot_data = args["slot_data"]
            orbsanity_option = slot_data["enable_orbsanity"]
            if orbsanity_option == EnableOrbsanity.option_per_level:
                orbsanity_bundle = slot_data["level_orbsanity_bundle_size"]
            elif orbsanity_option == EnableOrbsanity.option_global:
                orbsanity_bundle = slot_data["global_orbsanity_bundle_size"]
            else:
                orbsanity_bundle = 1

            create_task_log_exception(
                self.repl.setup_options(orbsanity_option,
                                        orbsanity_bundle,
                                        slot_data["fire_canyon_cell_count"],
                                        slot_data["mountain_pass_cell_count"],
                                        slot_data["lava_tube_cell_count"],
                                        slot_data["citizen_orb_trade_amount"],
                                        slot_data["oracle_orb_trade_amount"],
                                        slot_data["jak_completion_condition"]))

            # Because Orbsanity and the orb traders in the game are intrinsically linked, we need the server
            # to track our trades at all times to support async play. "Retrieved" will tell us the orbs we lost,
            # while "ReceivedItems" will tell us the orbs we gained. This will give us the correct balance.
            if orbsanity_option in [EnableOrbsanity.option_per_level, EnableOrbsanity.option_global]:
                async def get_orb_balance():
                    await self.send_msgs([{"cmd": "Get", "keys": [f"jakanddaxter_{self.auth}_orbs_paid"]}])

                create_task_log_exception(get_orb_balance())

        if cmd == "Retrieved":
            if f"jakanddaxter_{self.auth}_orbs_paid" in args["keys"]:
                orbs_traded = args["keys"][f"jakanddaxter_{self.auth}_orbs_paid"]
                orbs_traded = orbs_traded if orbs_traded is not None else 0
                create_task_log_exception(self.repl.subtract_traded_orbs(orbs_traded))

        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                logger.debug(f"index: {str(index)}, item: {str(item)}")
                self.repl.item_inbox[index] = item

    async def json_to_game_text(self, args: dict):
        if "type" in args and args["type"] in {"ItemSend"}:
            my_item_name: Optional[str] = None
            my_item_finder: Optional[str] = None
            their_item_name: Optional[str] = None
            their_item_owner: Optional[str] = None

            item = args["item"]
            recipient = args["receiving"]

            # Receiving an item from the server.
            if self.slot_concerns_self(recipient):
                my_item_name = self.item_names.lookup_in_game(item.item)

                # Did we find it, or did someone else?
                if self.slot_concerns_self(item.player):
                    my_item_finder = "MYSELF"
                else:
                    my_item_finder = self.player_names[item.player]

            # Sending an item to the server.
            if self.slot_concerns_self(item.player):
                their_item_name = self.item_names.lookup_in_slot(item.item, recipient)

                # Does it belong to us, or to someone else?
                if self.slot_concerns_self(recipient):
                    their_item_owner = "MYSELF"
                else:
                    their_item_owner = self.player_names[recipient]

            # Write to game display.
            self.repl.queue_game_text(my_item_name, my_item_finder, their_item_name, their_item_owner)

    def on_print_json(self, args: dict) -> None:

        # Even though N items come in as 1 ReceivedItems packet, there are still N PrintJson packets to process,
        # and they all arrive before the ReceivedItems packet does. Defer processing of these packets as
        # async tasks to speed up large releases of items.
        create_task_log_exception(self.json_to_game_text(args))
        super(JakAndDaxterContext, self).on_print_json(args)

    def on_deathlink(self, data: dict):
        if self.memr.deathlink_enabled:
            self.repl.received_deathlink = True
            super().on_deathlink(data)

    async def ap_inform_location_check(self, location_ids: List[int]):
        message = [{"cmd": "LocationChecks", "locations": location_ids}]
        await self.send_msgs(message)

    def on_location_check(self, location_ids: List[int]):
        create_task_log_exception(self.ap_inform_location_check(location_ids))

    async def ap_inform_finished_game(self):
        if not self.finished_game and self.memr.finished_game:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            await self.send_msgs(message)
            self.finished_game = True

    def on_finish_check(self):
        create_task_log_exception(self.ap_inform_finished_game())

    async def ap_inform_deathlink(self):
        if self.memr.deathlink_enabled:
            player = self.player_names[self.slot] if self.slot is not None else "Jak"
            death_text = self.memr.cause_of_death.replace("Jak", player)
            await self.send_death(death_text)
            self.on_log_warn(logger, death_text)

        # Reset all flags, but leave the death count alone.
        self.memr.send_deathlink = False
        self.memr.cause_of_death = ""

    def on_deathlink_check(self):
        create_task_log_exception(self.ap_inform_deathlink())

    async def ap_inform_deathlink_toggle(self):
        await self.update_death_link(self.memr.deathlink_enabled)

    def on_deathlink_toggle(self):
        create_task_log_exception(self.ap_inform_deathlink_toggle())

    async def ap_inform_orb_trade(self, orbs_changed: int):
        if self.memr.orbsanity_enabled:
            await self.send_msgs([{"cmd": "Set",
                                   "key": f"jakanddaxter_{self.auth}_orbs_paid",
                                   "default": 0,
                                   "want_reply": False,
                                   "operations": [{"operation": "add", "value": orbs_changed}]
                                   }])

    def on_orb_trade(self, orbs_changed: int):
        create_task_log_exception(self.ap_inform_orb_trade(orbs_changed))

    def on_log_error(self, lg: Logger, message: str):
        lg.error(message)
        if self.ui:
            color = self.jsontotextparser.color_codes["red"]
            self.ui.log_panels["Archipelago"].on_message_markup(f"[color={color}]{message}[/color]")
            self.ui.log_panels["All"].on_message_markup(f"[color={color}]{message}[/color]")

    def on_log_warn(self, lg: Logger, message: str):
        lg.warning(message)
        if self.ui:
            color = self.jsontotextparser.color_codes["orange"]
            self.ui.log_panels["Archipelago"].on_message_markup(f"[color={color}]{message}[/color]")
            self.ui.log_panels["All"].on_message_markup(f"[color={color}]{message}[/color]")

    def on_log_success(self, lg: Logger, message: str):
        lg.info(message)
        if self.ui:
            color = self.jsontotextparser.color_codes["green"]
            self.ui.log_panels["Archipelago"].on_message_markup(f"[color={color}]{message}[/color]")
            self.ui.log_panels["All"].on_message_markup(f"[color={color}]{message}[/color]")

    def on_log_info(self, lg: Logger, message: str):
        lg.info(message)
        if self.ui:
            self.ui.log_panels["Archipelago"].on_message_markup(f"{message}")
            self.ui.log_panels["All"].on_message_markup(f"{message}")

    async def run_repl_loop(self):
        while True:
            await self.repl.main_tick()
            await asyncio.sleep(0.1)

    async def run_memr_loop(self):
        while True:
            await self.memr.main_tick()
            await asyncio.sleep(0.1)


async def run_game(ctx: JakAndDaxterContext):

    # These may already be running. If they are not running, try to start them.
    # TODO - Support other OS's. Pymem is Windows-only.
    gk_running = False
    try:
        pymem.Pymem("gk.exe")  # The GOAL Kernel
        gk_running = True
    except ProcessNotFound:
        ctx.on_log_warn(logger, "Game not running, attempting to start.")

    goalc_running = False
    try:
        pymem.Pymem("goalc.exe")  # The GOAL Compiler and REPL
        goalc_running = True
    except ProcessNotFound:
        ctx.on_log_warn(logger, "Compiler not running, attempting to start.")

    try:
        # Validate folder and file structures of the ArchipelaGOAL root directory.
        root_path = Utils.get_settings()["jakanddaxter_options"]["root_directory"]

        # Always trust your instincts.
        if "/" not in root_path:
            msg = (f"The ArchipelaGOAL root directory contains no path. (Are you missing forward slashes?)\n"
                   f"Please check that the value of 'jakanddaxter_options > root_directory' in your host.yaml file "
                   f"is a valid existing path, and all backslashes have been replaced with forward slashes.")
            ctx.on_log_error(logger, msg)
            return

        # Start by checking the existence of the root directory provided in the host.yaml file.
        root_path = os.path.normpath(root_path)
        if not os.path.exists(root_path):
            msg = (f"The ArchipelaGOAL root directory does not exist, unable to locate the Game and Compiler.\n"
                   f"Please check that the value of 'jakanddaxter_options > root_directory' in your host.yaml file "
                   f"is a valid existing path, and all backslashes have been replaced with forward slashes.")
            ctx.on_log_error(logger, msg)
            return

        # Now double-check the existence of the two executables we need.
        gk_path = os.path.join(root_path, "gk.exe")
        goalc_path = os.path.join(root_path, "goalc.exe")
        if not os.path.exists(gk_path) or not os.path.exists(goalc_path):
            msg = (f"The Game and Compiler could not be found in the ArchipelaGOAL root directory.\n"
                   f"Please check the value of 'jakanddaxter_options > root_directory' in your host.yaml file, "
                   f"and ensure that path contains gk.exe, goalc.exe, and a data folder.")
            ctx.on_log_error(logger, msg)
            return

        # Now we can FINALLY attempt to start the programs.
        if not gk_running:
            # Per-mod saves and settings are stored outside the ArchipelaGOAL root folder, so we have to traverse
            # a relative path, normalize it, and pass it in as an argument to gk. This folder will be created if
            # it does not exist.
            config_relative_path = "../_settings/archipelagoal"
            config_path = os.path.normpath(
                os.path.join(
                    root_path,
                    os.path.normpath(config_relative_path)))

            # The game freezes if text is inadvertently selected in the stdout/stderr data streams. Let's pipe those
            # streams to a file, and let's not clutter the screen with another console window.
            log_path = os.path.join(Utils.user_path("logs"), "JakAndDaxterGame.txt")
            log_path = os.path.normpath(log_path)
            with open(log_path, "w") as log_file:
                gk_process = subprocess.Popen(
                    [gk_path, "--game", "jak1",
                     "--config-path", config_path,
                     "--", "-v", "-boot", "-fakeiso", "-debug"],
                    stdout=log_file,
                    stderr=log_file,
                    creationflags=subprocess.CREATE_NO_WINDOW)

        if not goalc_running:
            # For the OpenGOAL Compiler, the existence of the "data" subfolder indicates you are running it from
            # a built package. This subfolder is treated as its proj_path.
            proj_path = os.path.join(root_path, "data")
            if os.path.exists(proj_path):

                # Look for "iso_data" path to automate away an oft-forgotten manual step of mod updates.
                # All relative paths should start from root_path and end with "jak1".
                goalc_args = []
                possible_relative_paths = {
                    "../../../../../active/jak1/data/iso_data/jak1",
                    "./data/iso_data/jak1",
                }

                for iso_relative_path in possible_relative_paths:
                    iso_path = os.path.normpath(
                        os.path.join(
                            root_path,
                            os.path.normpath(iso_relative_path)))

                    if os.path.exists(iso_path):
                        goalc_args = [goalc_path, "--game", "jak1", "--proj-path", proj_path, "--iso-path", iso_path]
                        logger.debug(f"iso_data folder found: {iso_path}")
                        break
                    else:
                        logger.debug(f"iso_data folder not found, continuing: {iso_path}")

                if not goalc_args:
                    msg = (f"The iso_data folder could not be found.\n"
                           f"Please follow these steps:\n"
                           f"   Run the OpenGOAL Launcher, click Jak and Daxter > Advanced > Open Game Data Folder.\n"
                           f"   Copy the iso_data folder from this location.\n"
                           f"   Click Jak and Daxter > Features > Mods > ArchipelaGOAL > Advanced > "
                           f"Open Game Data Folder.\n"
                           f"   Paste the iso_data folder in this location.\n"
                           f"   Click Advanced > Compile. When this is done, click Continue.\n"
                           f"   Close all launchers, games, clients, and console windows, then restart Archipelago.\n"
                           f"(See Setup Guide for more details.)")
                    ctx.on_log_error(logger, msg)
                    return

            # The non-existence of the "data" subfolder indicates you are running it from source, as a developer.
            # The compiler will traverse upward to find the project path on its own. It will also assume your
            # "iso_data" folder is at the root of your repository. Therefore, we don't need any of those arguments.
            else:
                goalc_args = [goalc_path, "--game", "jak1"]

            # This needs to be a new console. The REPL console cannot share a window with any other process.
            goalc_process = subprocess.Popen(goalc_args, creationflags=subprocess.CREATE_NEW_CONSOLE)

    except AttributeError as e:
        ctx.on_log_error(logger, f"Host.yaml does not contain {e.args[0]}, unable to locate game executables.")
        return
    except FileNotFoundError as e:
        msg = (f"The ArchipelaGOAL root directory path is invalid.\n"
               f"Please check that the value of 'jakanddaxter_options > root_directory' in your host.yaml file "
               f"is a valid existing path, and all backslashes have been replaced with forward slashes.")
        ctx.on_log_error(logger, msg)
        return

    # Auto connect the repl and memr agents. Sleep 5 because goalc takes just a little bit of time to load,
    # and it's not something we can await.
    ctx.on_log_info(logger, "This may take a bit... Wait for the game's title sequence before continuing!")
    await asyncio.sleep(5)
    ctx.repl.initiated_connect = True
    ctx.memr.initiated_connect = True


async def main():
    Utils.init_logging("JakAndDaxterClient", exception_logger="Client")

    ctx = JakAndDaxterContext(None, None)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.repl_task = create_task_log_exception(ctx.run_repl_loop())
    ctx.memr_task = create_task_log_exception(ctx.run_memr_loop())

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Find and run the game (gk) and compiler/repl (goalc).
    create_task_log_exception(run_game(ctx))
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
