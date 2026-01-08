import json
import shutil
import zipfile
from typing import Optional, cast, Dict, Any
import asyncio
import multiprocessing
import os
import subprocess
import traceback

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils
from settings import get_settings
from .data.Planets import get_all_active_locations
from . import Rac2Settings
from .Container import Rac2ProcedurePatch
from .ClientCheckLocations import handle_checked_location
from .Callbacks import update, init
from .ClientReceiveItems import handle_received_items
from .NotificationManager import NotificationManager
from .Rac2Interface import HUD_MESSAGE_DURATION, ConnectionState, Rac2Interface, Rac2Planet


class Rac2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_test_hud(self, *args):
        """Send a message to the game interface."""
        if isinstance(self.ctx, Rac2Context):
            self.ctx.notification_manager.queue_notification(' '.join(map(str, args)))

    def _cmd_status(self):
        """Display the current PCSX2 connection status."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(f"Connection status: {'Connected' if self.ctx.is_connected else 'Disconnected'}")

    def _cmd_segments(self):
        """Display the memory segment table."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(self.ctx.game_interface.get_segment_pointer_table())

    def _cmd_test_deathlink(self, deaths: str):
        """Queue up specified number of deaths."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(f"Queuing {deaths} deaths.")
            self.ctx.notification_manager.queue_notification("Received test deathlink")
            self.ctx.queued_deaths = int(deaths)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, Rac2Context):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
            logger.info(message)
            self.ctx.notification_manager.queue_notification(message)


class Rac2Context(CommonContext):
    current_planet: Optional[Rac2Planet] = None
    previous_planet: Optional[Rac2Planet] = None
    is_pending_death_link_reset = False
    command_processor = Rac2CommandProcessor
    game_interface: Rac2Interface
    notification_manager: NotificationManager
    game = "Ratchet & Clank 2"
    items_handling = 0b111
    pcsx2_sync_task = None
    is_connected = ConnectionState.DISCONNECTED
    is_loading: bool = False
    slot_data: dict[str, Utils.Any] = None
    last_error_message: Optional[str] = None
    death_link_enabled = False
    queued_deaths: int = 0
    previous_decoy_glove_ammo: int = 0

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = Rac2Interface(logger)
        self.notification_manager = NotificationManager(HUD_MESSAGE_DURATION)

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        if self.death_link_enabled:
            self.queued_deaths += 1
            cause = data.get("cause", "")
            if cause:
                self.notification_manager.queue_notification(f"DeathLink: {cause}")
            else:
                self.notification_manager.queue_notification(f"DeathLink: Received from {data['source']}")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Rac2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            # Set death link tag if it was requested in options
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))

            # Scout all active locations for lookups that may be required later on
            all_locations = [loc.location_id for loc in get_all_active_locations(self.slot_data)]
            self.locations_scouted = set(all_locations)
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.locations_scouted)
            }]))

    def run_gui(self):
        from kvui import GameManager

        class Rac2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Ratchet & Clank 2 Client"

        self.ui = Rac2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def update_connection_status(ctx: Rac2Context, status: bool):
    if ctx.is_connected == status:
        return

    if status:
        logger.info("Connected to Ratchet & Clank 2")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")
    ctx.is_connected = status


async def pcsx2_sync_task(ctx: Rac2Context):
    logger.info("Starting Ratchet & Clank 2 Connector, attempting to connect to emulator...")
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
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


async def handle_check_goal_complete(ctx: Rac2Context):
    if ctx.current_planet is Rac2Planet.Yeedil:
        moby = ctx.game_interface.get_moby(197)
        if moby is not None and ctx.game_interface.get_moby(197).state == 0x11:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_deathlink(ctx: Rac2Context):
    if ctx.game_interface.get_alive():
        if ctx.is_pending_death_link_reset:
            ctx.is_pending_death_link_reset = False
        if ctx.queued_deaths > 0 and ctx.game_interface.get_pause_state() == 0 and ctx.game_interface.get_ratchet_state() != 97:
            ctx.is_pending_death_link_reset = True
            ctx.game_interface.kill_player()
            ctx.queued_deaths -= 1
    else:
        if not ctx.is_pending_death_link_reset:
            await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of Nanotech.")
            ctx.is_pending_death_link_reset = True


async def _handle_game_ready(ctx: Rac2Context):
    if ctx.is_loading:
        if not ctx.game_interface.is_loading():
            ctx.is_loading = False
            current_planet = ctx.game_interface.get_current_planet()
            if current_planet is not None:
                logger.info(f"Loaded planet {current_planet} ({current_planet.name})")
            await asyncio.sleep(1)
        await asyncio.sleep(0.1)
        return
    elif ctx.game_interface.is_loading():
        ctx.game_interface.logger.info("Waiting for planet to load...")
        ctx.is_loading = True
        return

    connected_to_server = (ctx.server is not None) and (ctx.slot is not None)
    if ctx.current_planet != ctx.game_interface.get_current_planet() and connected_to_server:
        ctx.previous_planet = ctx.current_planet
        ctx.current_planet = ctx.game_interface.get_current_planet()
        init(ctx)
    update(ctx, connected_to_server)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        current_inventory = ctx.game_interface.get_current_inventory()
        if ctx.current_planet is not None and ctx.current_planet > 0 and ctx.game_interface.get_pause_state() in [0, 5]:
            await handle_received_items(ctx, current_inventory)
        if ctx.current_planet and ctx.current_planet > 0:
            await handle_checked_location(ctx)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_deathlink(ctx)
        await asyncio.sleep(0.1)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Rac2Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)


async def run_game(iso_file):
    auto_start = get_settings().rac2_options.get("iso_start", True)

    if auto_start is True:
        import webbrowser
        webbrowser.open(iso_file)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, iso_file, "-batch"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(aprac2_file: str):
    settings: Optional[Rac2Settings] = get_settings().get("rac2_options", False)
    assert settings, "No Rac2 Settings?"

    aprac2_file = os.path.abspath(aprac2_file)
    base_name = os.path.splitext(aprac2_file)[0]
    output_path = base_name + '.iso'

    if not os.path.exists(output_path):
        from .PatcherUI import PatcherUI
        patcher = PatcherUI(aprac2_file, output_path, logger)
        await patcher.async_run()
        if patcher.errored:
            raise Exception("Patching Failed")

    game_ini_path: str = settings.game_ini
    if os.path.exists(game_ini_path):
        version = Rac2ProcedurePatch.get_game_version_from_iso(output_path)
        crc = get_pcsx2_crc(output_path)
        if version and crc:
            file_name = f"{version}_{crc:X}.ini"
            file_path = os.path.join(os.path.dirname(game_ini_path), file_name)
            shutil.copy(game_ini_path, file_path)

    Utils.async_start(run_game(output_path))


def get_name_from_aprac2(aprac2_path: str) -> str:
    with zipfile.ZipFile(aprac2_path) as zip_file:
        with zip_file.open("archipelago.json") as file:
            archipelago_json = file.read().decode("utf-8")
            archipelago_json = json.loads(archipelago_json)
    return cast(Dict[str, Any], archipelago_json)["player_name"]


def get_pcsx2_crc(iso_path: str) -> Optional[int]:
    if not os.path.exists(iso_path):
        return False

    ELF_START: int = 0x00258800
    ELF_SIZE: int = 0x27F53C
    crc: int = 0
    with open(iso_path, "rb") as iso_file:
        iso_file.seek(ELF_START)
        for i in range(int(ELF_SIZE / 4)):
            crc ^= int.from_bytes(iso_file.read(4), "little")

    return crc


def launch():
    Utils.init_logging("RAC2 Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument('aprac2_file', default="", type=str, nargs="?",
                            help='Path to an aprac2 file')
        args = parser.parse_args()

        ctx = Rac2Context(args.connect, args.password)

        if os.path.isfile(args.aprac2_file):
            logger.info("aprac2 file supplied, beginning patching process...")
            await patch_and_run_game(args.aprac2_file)
            ctx.auth = get_name_from_aprac2(args.aprac2_file)

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
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


if __name__ == '__main__':
    launch()
