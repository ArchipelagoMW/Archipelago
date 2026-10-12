# Python standard libraries
import asyncio
import json
import logging
import os
import subprocess
import sys
import shlex

from asyncio import Task
from datetime import datetime
from logging import Logger
from shutil import which
from typing import Awaitable

# Misc imports
import colorama
from psutil import NoSuchProcess

import PyMemoryEditor
from PyMemoryEditor import OpenProcess, ProcessNotFoundError

# Archipelago imports
import ModuleUpdate
import Utils

from CommonClient import server_loop, gui_enabled
from NetUtils import ClientStatus

# Jak imports
from .game_id import jak3_name, jak3_gk, jak3_goalc
from .agents.memory_reader import Jak3MemoryReader, autopsy
from .agents.repl_client import Jak3ReplClient
from . import Jak3World
from .options import CompletionCondition
from .items import item_table, ITEM_ID_FILLER_START, ITEM_ID_FILLER_END, TRAP_ID_START, TRAP_ID_END, SECRET_ID_START, SECRET_ID_END

# Load Universal Tracker
tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerCommandProcessor as ClientCommandProcessor,
        TrackerGameContext as CommonContext,
        UT_VERSION
    )

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext
    UT_VERSION = 0

ModuleUpdate.update()
logger = logging.getLogger("Jak3Client")
all_tasks: set[Task] = set()


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


class Jak3ClientCommandProcessor(ClientCommandProcessor):
    ctx: "Jak3Context"

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


class Jak3Context(CommonContext):
    game = jak3_name
    items_handling = 0b111  # Full item handling
    command_processor = Jak3ClientCommandProcessor

    repl: Jak3ReplClient
    memr: Jak3MemoryReader

    repl_task: asyncio.Task
    memr_task: asyncio.Task

    slot_seed: str

    def __init__(self, server_address: str | None, password: str | None) -> None:
        self.memr = Jak3MemoryReader(self.on_location_check,
                                     self.on_finish_check,
                                     self.on_deathlink_check,
                                     self.on_deathlink_toggle,
                                     self.on_orb_spend,
                                     self.on_gem_spend,
                                     self.on_log_error,
                                     self.on_log_warn,
                                     self.on_log_success,
                                     self.on_log_info)
        self.repl = Jak3ReplClient(self.on_log_error,
                                   self.on_log_warn,
                                   self.on_log_success,
                                   self.on_log_info,
                                   self.memr)
        super().__init__(server_address, password)

    def run_generator(self):
        if tracker_loaded:
            super().run_generator()

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Jak 3 ArchipelaGOAL Client"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"

        # AP version is added behind this automatically
        ui.base_title += " | Archipelago"
        return ui

    def run_gui(self):
        ui_class = self.make_gui()
        self.ui = ui_class(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Jak3Context, self).server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        await self.send_connect()

    async def connect(self, address: str | None = None) -> None:
        if not self.repl.connected or not self.memr.connected:
            self.on_log_warn(logger, "Please wait for the Compiler and Memory Reader to connect to the game!")
            return
        await super(Jak3Context, self).connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.locations_checked = set()  # Clear this set to gracefully handle server disconnects.
        await super(Jak3Context, self).disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd == "RoomInfo":
            self.slot_seed = args["seed_name"]
            self.memr.slot_seed = self.slot_seed[:8]
            self.repl.slot_seed = self.slot_seed[:8]
            self.memr.load_data()
            self.repl.load_data()

        if cmd == "Connected":
            slot_data = args["slot_data"]
            completion_type = slot_data["jak_3_completion_condition"]
            specific_mission_value = slot_data.get("specific_mission_for_completion", 71)
            mission_count_value = slot_data.get("number_of_missions_for_completion", 60)
            self.memr.checks_per_mission = slot_data["checks_per_mission"]
            self.memr.location_check_mode = slot_data.get("location_check_mode", 1)
            self.memr.orb_bundle_count = slot_data.get("orb_bundle_count", 600)
            self.memr.orb_bundle_size = (slot_data.get("orbs_per_bundle", 20)
                                         if slot_data.get("orbsanity", 0) else 0)

            if not self.repl.received_initial_items and self.repl.initial_item_count < 0:
                self.repl.initial_item_count = 0

            create_task_log_exception(
                self.repl.setup_options(
                    self.auth[:16],
                    self.slot_seed[:8],
                    slot_data.get("trap_effect_duration", 30),
                    completion_type,
                    specific_mission_value,
                    mission_count_value,
                    slot_data.get("jak_is_jak2", 0),
                    slot_data.get("randomize_burning_bush_cost", 0),
                    slot_data.get("burning_bush_cost_get_to", 4),
                    slot_data.get("burning_bush_cost_race", 8),
                    slot_data.get("burning_bush_cost_other", 12),
                    slot_data.get("minigame_medal_checks", 0),
                    slot_data.get("orbsanity", 0),
                    slot_data.get("orbs_per_bundle", 20)))

            # Tell the server if Deathlink is enabled or disabled in the in-game options.
            # This allows us to "remember" the user's choice.
            self.on_deathlink_toggle()

        if cmd == "ReceivedItems":
            if not self.repl.received_initial_items and not self.repl.processed_initial_items:
                self.repl.received_initial_items = True
                self.repl.initial_item_count = len(args["items"])
                create_task_log_exception(self.repl.send_connection_status("wait"))

            for index, item in enumerate(args["items"], start=args["index"]):
                logger.debug(f"index: {str(index)}, item: {str(item)}")
                self.repl.item_inbox[index] = item

    async def json_to_game_text(self, args: dict):
        if "type" in args and args["type"] in {"ItemSend"}:
            my_item_name: str | None = None
            my_item_finder: str | None = None
            their_item_name: str | None = None
            their_item_owner: str | None = None

            item = args["item"]
            recipient = args["receiving"]

            def is_filler_or_trap(item_id: int) -> bool:
                return (ITEM_ID_FILLER_START <= item_id <= ITEM_ID_FILLER_END) or (
                        TRAP_ID_START <= item_id <= TRAP_ID_END) or (
                        SECRET_ID_START <= item_id <= SECRET_ID_END)

            if self.slot_concerns_self(recipient):
                my_item_name = self.item_names.lookup_in_game(item.item)
                if self.slot_concerns_self(item.player):
                    my_item_finder = "MYSELF"
                else:
                    my_item_finder = self.player_names[item.player]

            if self.slot_concerns_self(item.player) and not self.slot_concerns_self(recipient):
                their_item_name = self.item_names.lookup_in_slot(item.item, recipient)
                their_item_owner = self.player_names[recipient]

            self.repl.queue_game_text(my_item_name, my_item_finder, their_item_name, their_item_owner)

    def on_print_json(self, args: dict) -> None:
        create_task_log_exception(self.json_to_game_text(args))
        super(Jak3Context, self).on_print_json(args)

    # We need to do a little more than just use CommonClient's on_deathlink.
    def on_deathlink(self, data: dict):
        if self.memr.deathlink_enabled:
            self.repl.received_deathlink = True
            super().on_deathlink(data)

    def on_location_check(self, location_ids: list[int]):
        create_task_log_exception(self.check_locations(location_ids))

    async def ap_inform_finished_game(self):
        if not self.finished_game and self.memr.finished_game:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            await self.send_msgs(message)
            self.finished_game = True

    def on_finish_check(self):
        create_task_log_exception(self.ap_inform_finished_game())

    # We need to do a little more than just use CommonClient's send_death.
    async def ap_inform_deathlink(self):
        if self.memr.deathlink_enabled:
            player = self.player_names[self.slot] if self.slot is not None else "Jak"
            death_text = autopsy(self.memr.cause_of_death).replace("Jak", player)
            await self.send_death(death_text)
            self.on_log_warn(logger, death_text)

        # Reset all flags, but leave the death count alone.
        self.memr.send_deathlink = False

    def on_deathlink_check(self):
        create_task_log_exception(self.ap_inform_deathlink())

    # We don't need an ap_inform function because update_death_link solves that need.
    def on_deathlink_toggle(self):
        create_task_log_exception(self.update_death_link(self.memr.deathlink_enabled))

    def on_orb_spend(self, amount: int):
        create_task_log_exception(self.repl.acknowledge_orb_spend(amount))

    def on_gem_spend(self, amount: int):
        create_task_log_exception(self.repl.acknowledge_gem_spend(amount))

    def _markup_panels(self, msg: str, c: str = None):
        color = self.jsontotextparser.color_codes[c] if c else None
        message = f"[color={color}]{msg}[/color]" if c else msg
        self.ui.log_panels["Archipelago"].on_message_markup(message)
        self.ui.log_panels["All"].on_message_markup(message)

    def on_log_error(self, lg: Logger, message: str):
        lg.error(message)
        if self.ui:
            self._markup_panels(message, "red")

    def on_log_warn(self, lg: Logger, message: str):
        lg.warning(message)
        if self.ui:
            self._markup_panels(message, "orange")

    def on_log_success(self, lg: Logger, message: str):
        lg.info(message)
        if self.ui:
            self._markup_panels(message, "green")

    def on_log_info(self, lg: Logger, message: str):
        lg.info(message)
        if self.ui:
            self._markup_panels(message)

    async def run_repl_loop(self):
        while True:
            try:
                await self.repl.main_tick()
                await asyncio.sleep(0.1)
            # This catch re-engages the memr loop, enabling the client to re-connect on losing the process
            except NoSuchProcess:
                logger.debug("Compiler process lost. Restarting Compiler loop.")

    async def run_memr_loop(self):
        while True:
            try:
                await self.memr.main_tick()
                await asyncio.sleep(0.1)
            # This catch re-engages the memr loop, enabling the client to re-connect on losing the process
            except NoSuchProcess:
                logger.debug("Memory reader process lost. Restarting Memory reader loop.")

def find_root_directory(ctx: Jak3Context):

    if Utils.is_windows:
        appdata = os.getenv("APPDATA")
        settings_path = os.path.normpath(f"{appdata}/OpenGOAL-Launcher/settings.json")
    elif Utils.is_linux:
        home = os.path.expanduser("~")
        settings_path = os.path.normpath(f"{home}/.config/OpenGOAL-Launcher/settings.json")
    elif Utils.is_macos:
        home = os.path.expanduser("~")
        settings_path = os.path.normpath(f"{home}/Library/Application Support/OpenGOAL-Launcher/settings.json")
    else:
        ctx.on_log_error(logger, f"Unknown operating system: {sys.platform}!")
        return

    err_title = "Unable to locate the ArchipelaGOAL install directory"
    alt_instructions = (f"Please verify that OpenGOAL and ArchipelaGOAL are installed properly. "
                        f"If the problem persists, follow these steps:\n"
                        f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                        f"   Then click Advanced > Open Game Data Folder.\n"
                        f"   Go up one folder, then copy this path.\n"
                        f"   Run the Archipelago Launcher, click Open host.yaml.\n"
                        f"   Set the value of 'Jak3_options > root_directory' to this path.\n"
                        f"   Replace all backslashes in the path with forward slashes.\n"
                        f"   Set the value of 'Jak3_options > auto_detect_root_directory' to false, "
                        f"then save and close the host.yaml file.\n"
                        f"   Close all launchers, games, clients, and console windows, then restart Archipelago.")

    if not os.path.exists(settings_path):
        msg = (f"{err_title}: The OpenGOAL settings file does not exist.\n"
               f"{alt_instructions}")
        ctx.on_log_error(logger, msg)
        return

    with open(settings_path, "r") as f:
        load = json.load(f)

        try:
            settings_version = load["version"]
            logger.debug(f"OpenGOAL settings file version: {settings_version}")
        except KeyError:
            msg = (f"{err_title}: The OpenGOAL settings file has no version number!\n"
                   f"{alt_instructions}")
            ctx.on_log_error(logger, msg)
            return

        try:
            if settings_version == "2.0":
                jak3_installed = load["games"]["Jak 3"]["isInstalled"]
                mod_sources = load["games"]["Jak 3"]["modsInstalledVersion"]
            elif settings_version == "3.0":
                jak3_installed = load["games"]["jak3"]["isInstalled"]
                mod_sources = load["games"]["jak3"]["mods"]
            else:
                msg = (f"{err_title}: The OpenGOAL settings file has an unknown version number ({settings_version}).\n"
                       f"{alt_instructions}")
                ctx.on_log_error(logger, msg)
                return
        except KeyError as e:
            msg = (f"{err_title}: The OpenGOAL settings file does not contain key entry {e}!\n"
                   f"{alt_instructions}")
            ctx.on_log_error(logger, msg)
            return

        if not jak3_installed:
            msg = (f"{err_title}: The OpenGOAL Launcher is missing a normal install of Jak 3!\n"
                   f"{alt_instructions}")
            ctx.on_log_error(logger, msg)
            return

        if mod_sources is None:
            msg = (f"{err_title}: No mod sources have been configured in the OpenGOAL Launcher!\n"
                   f"{alt_instructions}")
            ctx.on_log_error(logger, msg)
            return

        archipelagoal_source = None
        for src in mod_sources:
            for mod in mod_sources[src].keys():
                if mod == "archipelagoal-3":
                    archipelagoal_source = src
        if archipelagoal_source is None:
            msg = (f"{err_title}: The ArchipelaGOAL mod is not installed in the OpenGOAL Launcher!\n"
                   f"{alt_instructions}")
            ctx.on_log_error(logger, msg)
            return

        base_path = load["installationDir"]
        mod_relative_path = f"features/jak3/mods/{archipelagoal_source}/archipelagoal-3"
        mod_path = os.path.normpath(
            os.path.join(
                os.path.normpath(base_path),
                os.path.normpath(mod_relative_path)))

    return mod_path


async def run_game(ctx: Jak3Context):

    gk_running = False
    try:
        OpenProcess(name=jak3_gk)
        gk_running = True
    except ProcessNotFoundError:
        ctx.on_log_warn(logger, "Game not running, attempting to start.")

    goalc_running = False
    try:
        OpenProcess(name=jak3_goalc)
        goalc_running = True
    except ProcessNotFoundError:
        ctx.on_log_warn(logger, "Compiler not running, attempting to start.")

    try:
        auto_detect_root_directory = Jak3World.settings.auto_detect_root_directory
        if auto_detect_root_directory:
            root_path = find_root_directory(ctx)
        else:
            root_path = Jak3World.settings.root_directory

            if "/" not in root_path:
                msg = (f"The ArchipelaGOAL root directory contains no path. (Are you missing forward slashes?)\n"
                       f"Please check your host.yaml file.\n"
                       f"Verify the value of 'jak3_options > root_directory' is a valid existing path, "
                       f"and all backslashes have been replaced with forward slashes.")
                ctx.on_log_error(logger, msg)
                return

        root_path = os.path.normpath(root_path)
        if not os.path.exists(root_path):
            msg = (f"The ArchipelaGOAL root directory does not exist, unable to locate the Game and Compiler.\n"
                   f"Please check your host.yaml file.\n"
                   f"If the value of 'jak3_options > auto_detect_root_directory' is true, verify that OpenGOAL "
                   f"is installed properly.\n"
                   f"If it is false, check the value of 'jak3_options > root_directory'. "
                   f"Verify it is a valid existing path, and all backslashes have been replaced with forward slashes.")
            ctx.on_log_error(logger, msg)
            return

        gk_path = os.path.join(root_path, jak3_gk)
        goalc_path = os.path.join(root_path, jak3_goalc)
        if not os.path.exists(gk_path) or not os.path.exists(goalc_path):
            msg = (f"The Game and Compiler could not be found in the ArchipelaGOAL root directory.\n"
                   f"Please check your host.yaml file.\n"
                   f"If the value of 'jak3_options > auto_detect_root_directory' is true, verify that OpenGOAL "
                   f"is installed properly.\n"
                   f"If it is false, check the value of 'jak3_options > root_directory'. "
                   f"Verify it is a valid existing path, and all backslashes have been replaced with forward slashes.")
            ctx.on_log_error(logger, msg)
            return

        if not gk_running:
            config_relative_path = "../_settings/archipelagoal-3"
            config_path = os.path.normpath(
                os.path.join(
                    root_path,
                    os.path.normpath(config_relative_path)))

            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            log_path = os.path.join(Utils.user_path("logs"), f"Jak3Game_{timestamp}.txt")
            log_path = os.path.normpath(log_path)
            with open(log_path, "w") as log_file:
                gk_args = [gk_path, "--game", "jak3",
                 "--config-path", config_path,
                 "--", "-v", "-boot", "-fakeiso", "-debug"]

                if Utils.is_windows:
                    gk_process = subprocess.Popen(
                        gk_args,
                        stdout=log_file,
                        stderr=log_file,
                        creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    gk_process = subprocess.Popen(
                        gk_args,
                        stdout=log_file,
                        stderr=log_file)

        if not goalc_running:
            proj_path = os.path.join(root_path, "data")
            if os.path.exists(proj_path):
                goalc_args = []
                possible_relative_paths = {
                    "../../../../../active/jak3/data/iso_data/jak3",
                    "./data/iso_data/jak3",
                }

                for iso_relative_path in possible_relative_paths:
                    iso_path = os.path.normpath(
                        os.path.join(
                            root_path,
                            os.path.normpath(iso_relative_path)))

                    if os.path.exists(iso_path):
                        goalc_args = [goalc_path, "--game", "jak3", "--proj-path", proj_path, "--iso-path", iso_path]
                        logger.debug(f"iso_data folder found: {iso_path}")
                        break
                    else:
                        logger.debug(f"iso_data folder not found, continuing: {iso_path}")

                if not goalc_args:
                    msg = (f"The iso_data folder could not be found.\n"
                           f"Please follow these steps:\n"
                           f"   Run the OpenGOAL Launcher, click Jak 3 > Advanced > Open Game Data Folder.\n"
                           f"   Copy the iso_data folder from this location.\n"
                           f"   Click Jak 3 > Features > Mods > ArchipelaGOAL > Advanced > "
                           f"Open Game Data Folder.\n"
                           f"   Paste the iso_data folder in this location.\n"
                           f"   Click Advanced > Compile. When this is done, click Continue.\n"
                           f"   Close all launchers, games, clients, and console windows, then restart Archipelago.\n"
                           f"(See Setup Guide for more details.)")
                    ctx.on_log_error(logger, msg)
                    return
            else:
                goalc_args = [goalc_path, "--game", "jak3"]

            # Directly ripped from jak1 client
            if Utils.is_windows:
                goalc_process = subprocess.Popen(goalc_args, creationflags=subprocess.CREATE_NEW_CONSOLE)

            elif Utils.is_linux:
                terminal = which('x-terminal-emulator') or which('gnome-terminal') or which('konsole') or which('xterm')

                # Don't allow the terminal application to attempt loading system libraries, this can cause OpenSSL
                # errors when launching the REPL due to version mismatches between system vs shipped libraries.
                env = os.environ
                if "LD_LIBRARY_PATH" in env:
                    env = env.copy()
                    del env["LD_LIBRARY_PATH"]

                if terminal:
                    goalc_process = subprocess.Popen([terminal, '-e', shlex.join(goalc_args)], env=env)
                else:
                    msg = (f"Your Linux installation does not have a supported terminal application.\n"
                            f"We support the following options:\n"
                            f"   x-terminal-emulator\n"
                            f"   gnome-terminal\n"
                            f"   konsole\n"
                            f"   xterm\n"
                            f"Please install one of these and try again.")
                    ctx.on_log_error(logger, msg)
                    return

            elif Utils.is_macos:
                terminal = [which('open'), '-W', '-a', 'Terminal.app']
                goalc_process = subprocess.Popen([*terminal, *goalc_args])

    except AttributeError as e:
        if " " in e.args[0]:
            ctx.on_log_error(logger, e.args[0])
        else:
            ctx.on_log_error(logger,
                             f"Host.yaml does not contain {e.args[0]}, unable to locate game executables.")
        return
    except FileNotFoundError as e:
        msg = (f"The following path could not be found: {e.filename}\n"
               f"Please check your host.yaml file.\n"
               f"If the value of 'jak3_options > auto_detect_root_directory' is true, verify that OpenGOAL "
               f"is installed properly.\n"
               f"If it is false, check the value of 'jak3_options > root_directory'."
               f"Verify it is a valid existing path, and all backslashes have been replaced with forward slashes.")
        ctx.on_log_error(logger, msg)
        return

    ctx.on_log_info(logger, "This may take a bit... Wait for the game's title sequence before continuing!")
    await asyncio.sleep(5)
    ctx.repl.initiated_connect = True
    ctx.memr.initiated_connect = True


async def main():
    Utils.init_logging("Jak3Client", exception_logger="Client")

    ctx = Jak3Context(None, None)

    # If UT is loaded, run the generator and remove the tracker tag so we're treated as a game client.
    if tracker_loaded:
        ctx.run_generator()
        ctx.tags.discard("Tracker")

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.repl_task = create_task_log_exception(ctx.run_repl_loop())
    ctx.memr_task = create_task_log_exception(ctx.run_memr_loop())

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    create_task_log_exception(run_game(ctx))
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()