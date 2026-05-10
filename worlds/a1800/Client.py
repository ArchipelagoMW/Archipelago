# pyright: reportOptionalMemberAccess=false
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from pathlib import Path
from typing import Callable, Optional

from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from NetUtils import ClientStatus, NetworkItem
from settings import get_settings
from Utils import Version, __version__

from .Settings import A1800Settings
from .rcon.rcon_mmap_client import RCONMMapClient, RCONTimeout


class A1800Context(CommonContext):
    command_processor = ClientCommandProcessor
    game = "Anno 1800"
    items_handling = 0b111  # full remote

    # updated by spinup server
    mod_version: Version = Version(0, 0, 0)

    def __init__(self, server_address: Optional[str], password: Optional[str], mmap_file_path: Path):
        super(A1800Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.rcon_mmap_client: Optional[RCONMMapClient] = None
        self.mmap_file_path = mmap_file_path
        self.awaiting_bridge = False
        self.write_data_path = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(A1800Context, self).server_auth(password_requested)

        if not self.auth:
            unkown_identity_exception = Exception("Cannot connect to a server with unknown own identity, "
                                                  "please connect to Anno 1800 t least once first.")
            if self.rcon_mmap_client and self.rcon_mmap_client.connected:
                try:
                    await get_info(self)  # retrieve current auth code
                except TimeoutError:
                    raise unkown_identity_exception
            else:
                raise unkown_identity_exception

        await self.send_connect()

    def print_to_game(self, text: str):
        self.rcon_mmap_client.send_command(f"/print {text}")

    def on_package(self, cmd: str, args: dict):  # type: ignore
        if cmd in {"Connected", "RoomUpdate"}:
            # catch up sync anything that is already cleared.
            # if "checked_locations" in args and args["checked_locations"]:
            #     self.rcon_mmap_client.send_commands({item_name: f'/ap-receive-item {item_name}' for
            #                                          item_name in args["checked_locations"]})
            pass  # TODO ?

    def run_gui(self):
        from kvui import GameManager

        class A1800Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
            ]
            base_title = "Archipelago Anno 1800 Client"

        self.ui = A1800Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def a1800_game_watcher(ctx: A1800Context):
    next_bridge = time.perf_counter() + 1
    next_connect = time.perf_counter()
    try:
        while not ctx.exit_event.is_set():
            # TODO: restore on-demand refresh
            if ctx.rcon_mmap_client and ctx.rcon_mmap_client.connected and ctx.auth and time.perf_counter() > next_bridge:
                next_bridge = time.perf_counter() + 1
                ctx.awaiting_bridge = False

                try:
                    data = json.loads(ctx.rcon_mmap_client.send_command("/ap-sync") or "")
                except RCONTimeout:
                    ctx.rcon_mmap_client.connected = False
                    logger.warning("Anno 1800 Client has lost connection. Did you pause or quit the game?")
                    continue
                if not ctx.rcon_mmap_client.connected or not ctx.auth:
                    pass  # not connected or auth failed, wait for new attempt
                elif data.get("slot_name") != ctx.auth:
                    logger.warning(
                        f"Connected World is not the expected one {data.get("slot_name", "None")} != {ctx.auth}")
                elif data.get("seed_name") != ctx.seed_name:
                    logger.warning(
                        f"Connected Multiworld is not the expected one {data.get("seed_name", "None")} != {ctx.seed_name}")
                else:
                    locations_checked: set[int] = {int(location_id)
                                                   for location_id in data.get("locations_checked", [])}
                    victory = data.get("victory")

                    if not ctx.finished_game and victory:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

                    if ctx.locations_checked != locations_checked:
                        logger.debug(
                            f"New locations checked: "
                            f"{[ctx.location_names.lookup_in_game(location_id) for location_id in locations_checked - ctx.locations_checked]}")
                        ctx.locations_checked = locations_checked
                        await ctx.check_locations(ctx.locations_checked)

            if ctx.rcon_mmap_client and (not ctx.rcon_mmap_client.connected or not ctx.auth) and time.perf_counter() > next_connect:
                ctx.rcon_mmap_client.connect()
                if ctx.rcon_mmap_client.connected:
                    await get_info(ctx)
                if not ctx.rcon_mmap_client.connected or not ctx.auth:
                    ctx.rcon_mmap_client.connected = False
                    logger.info("Couldn't connect to Anno 1800. Please unpause and/or load into an Anno 1800 game to reconnect.")
                    logger.info("Retrying in 5s...")
                    next_connect = time.perf_counter() + 5
                else:
                    logger.info(f"Successfully reconnected to Anno 1800.")

            await asyncio.sleep(0.1)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Anno 1800 Bridge")


async def a1800_server_watcher(ctx: A1800Context):
    try:
        while not ctx.exit_event.is_set():
            if ctx.rcon_mmap_client and ctx.rcon_mmap_client.connected and ctx.auth:
                while ctx.send_index < len(ctx.items_received):
                    transfer_item: NetworkItem = ctx.items_received[ctx.send_index]
                    item_id = transfer_item.item
                    try:
                        ctx.rcon_mmap_client.send_command(f"/ap-receive-item {item_id}")
                    except:
                        ctx.rcon_mmap_client.connected = False
                        logger.warning("Anno 1800 Client has lost connection. Did you pause or quit the game?")
                        continue
                    ctx.send_index += 1
            await asyncio.sleep(0.1)

    except Exception:
        ctx.exit_event.set()

    finally:
        if ctx.rcon_mmap_client:
            ctx.rcon_mmap_client.close()
            ctx.rcon_mmap_client = None


async def get_info(ctx: A1800Context):
    info = json.loads(ctx.rcon_mmap_client.send_command("/ap-rcon-info") or "")
    ctx.auth = info.get("slot_name")
    ctx.seed_name = info.get("seed_name")


async def a1800_spinup(ctx: A1800Context) -> bool:
    if ctx.mmap_file_path.name != "A1800APCommunication.dat":
        logger.fatal(
            f"Could not find an active Anno 1800 Archipelago mod in supplied mods folder: {ctx.mmap_file_path}")
        logger.fatal("If this folder is incorrect, please correct it in your host.yaml under a1800_options.")
        logger.fatal("If this folder is correct, you have not installed an Archipelago mod or it is inactive.")
        logger.fatal("Please install one or activate it by removing the - in front.")
        logger.fatal("Then restart this client.")
        return False

    try:
        next_connect = time.perf_counter()
        while not ctx.auth and not ctx.exit_event.is_set():
            try:
                ctx.rcon_mmap_client = RCONMMapClient(ctx.mmap_file_path)
            except FileNotFoundError:
                logger.debug(f"FileNotFound: {ctx.mmap_file_path}")
                pass

            if ctx.rcon_mmap_client and time.perf_counter() > next_connect:
                ctx.rcon_mmap_client.connect()
                if ctx.rcon_mmap_client.connected:
                    await get_info(ctx)
                if not ctx.rcon_mmap_client.connected or not ctx.auth:
                    ctx.rcon_mmap_client.connected = False
                    ctx.auth = None
                    logger.info("Couldn't connect to Anno 1800. Please load into an Anno 1800 game and unpause to connect.")
                    logger.info("Retrying in 5s...")
                    next_connect = time.perf_counter() + 5
                else:
                    logger.info(f"Successfully connected to Anno 1800. Slot name is {ctx.auth}.")
                    logger.info("Ready to connect to the Archipelago server via the Connect button or /connect.")
            await asyncio.sleep(0.1)

    except Exception as e:
        logger.exception(e, extra={"compact_gui": True})
        msg = "Aborted Anno 1800 Bridge"
        logger.error(msg)
        ctx.gui_error(msg, e)
        ctx.exit_event.set()

    else:
        if ctx.auth:
            logger.info(
                f"Got World Information from Anno 1800 Archipelago Mod for seed {ctx.seed_name} in slot {ctx.auth}")
        return True

    return False


async def main(make_context: Callable[[], A1800Context]):
    ctx = make_context()
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    a1800_server_task = asyncio.create_task(a1800_spinup(ctx), name="A1800Spinup")
    successful_launch = await a1800_server_task
    if successful_launch:
        a1800_server_watch_task = asyncio.create_task(a1800_server_watcher(ctx), name="A1800ServerWatcher")
        a1800_game_watch_task = asyncio.create_task(a1800_game_watcher(ctx), name="A1800GameWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await a1800_game_watch_task
        await a1800_server_watch_task

    await ctx.shutdown()


settings: A1800Settings = get_settings().a1800_options


def launch():
    import colorama
    global executable
    colorama.just_fix_windows_console()

    parser = get_base_parser()
    args = parser.parse_args()

    a1800_mods_folder_path = Path(settings.a1800_mods_folder_path)

    if not a1800_mods_folder_path.exists():
        print(f"Path {a1800_mods_folder_path} does not exist or could not be accessed.")
    if not a1800_mods_folder_path.is_dir():
        print(f"Path {a1800_mods_folder_path} is not a folder.")

    mods = [mod for mod in a1800_mods_folder_path.iterdir()]

    mod_regex = re.compile(fr"AP-(\d*)-P(\d*)-(.*)-.*")
    mod_path = None
    for mod in mods:
        if mod.name.startswith("-"):
            continue
        modinfo_path = (mod / "modinfo.json")
        if modinfo_path.exists() and modinfo_path.is_file():
            data = {}
            with modinfo_path.open("r") as modinfo_file:
                data = json.load(modinfo_file)
            if data and "ModID" in data:
                if mod_regex.search(data["ModID"]):
                    mod_path = mod

    if not mod_path:
        print(f"Could not find Anno 1800 archipelago mod in mods folder.")

    asyncio.run(main(lambda: A1800Context(args.connect, args.password,
                mod_path / "A1800APCommunication.dat" if mod_path else a1800_mods_folder_path)))

    colorama.deinit()
