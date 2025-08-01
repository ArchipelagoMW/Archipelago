"""
A module containing context and functions relevant to running the client. This module should only be imported for type
checking or launching the client, otherwise it will probably cause circular import issues.
"""

import asyncio
import copy
import enum
import subprocess
from typing import Any

import settings
from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, logger, gui_enabled
import Patch
import Utils

from . import BizHawkContext, ConnectionStatus, NotConnectedError, RequestFailedError, connect, disconnect, get_hash, \
    get_script_version, get_system, ping, display_message
from .client import BizHawkClient, AutoBizHawkClientRegister


EXPECTED_SCRIPT_VERSION = 1


class AuthStatus(enum.IntEnum):
    NOT_AUTHENTICATED = 0
    NEED_INFO = 1
    PENDING = 2
    AUTHENTICATED = 3


class TextCategory(str, enum.Enum):
    ALL = "all"
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    OTHER = "other"
    HINT = "hint"
    CHAT = "chat"
    SERVER = "server"


class BizHawkClientCommandProcessor(ClientCommandProcessor):
    def _cmd_bh(self):
        """Shows the current status of the client's connection to BizHawk"""
        assert isinstance(self.ctx, BizHawkClientContext)

        if self.ctx.bizhawk_ctx.connection_status == ConnectionStatus.NOT_CONNECTED:
            logger.info("BizHawk Connection Status: Not Connected")
        elif self.ctx.bizhawk_ctx.connection_status == ConnectionStatus.TENTATIVE:
            logger.info("BizHawk Connection Status: Tentatively Connected")
        elif self.ctx.bizhawk_ctx.connection_status == ConnectionStatus.CONNECTED:
            logger.info("BizHawk Connection Status: Connected")

    def _cmd_toggle_text(self, category: str | None = None, toggle: str | None = None):
        """Sets types of incoming messages to forward to the emulator"""
        assert isinstance(self.ctx, BizHawkClientContext)

        if category is None:
            logger.info("Usage: /toggle_text category [toggle]\n\n"
                        "category: incoming, outgoing, other, hint, chat, and server\n"
                        "Or \"all\" to toggle all categories at once\n\n"
                        "toggle: on, off, true, or false\n"
                        "Or omit to set it to the opposite of its current state\n\n"
                        "Example: /toggle_text outgoing on")
            return

        category = category.lower()
        value: bool | None
        if toggle is None:
            value = None
        elif toggle.lower() in ("on", "true"):
            value = True
        elif toggle.lower() in ("off", "false"):
            value = False
        else:
            logger.info(f'Unknown value "{toggle}", should be on|off|true|false')
            return

        valid_categories = (
            TextCategory.ALL,
            TextCategory.OTHER,
            TextCategory.INCOMING,
            TextCategory.OUTGOING,
            TextCategory.HINT,
            TextCategory.CHAT,
            TextCategory.SERVER,
        )
        if category not in valid_categories:
            logger.info(f'Unknown value "{category}", should be {"|".join(valid_categories)}')
            return

        if category == TextCategory.ALL:
            if value is None:
                logger.info('Must specify "on" or "off" for category "all"')
                return
            
            if value:
                self.ctx.text_passthrough_categories.update((
                    TextCategory.OTHER,
                    TextCategory.INCOMING,
                    TextCategory.OUTGOING,
                    TextCategory.HINT,
                    TextCategory.CHAT,
                    TextCategory.SERVER,
                ))
            else:
                self.ctx.text_passthrough_categories.clear()
        else:
            if value is None:
                value = category not in self.ctx.text_passthrough_categories

            if value:
                self.ctx.text_passthrough_categories.add(category)
            else:
                self.ctx.text_passthrough_categories.remove(category)

        logger.info(f"Currently Showing Categories: {', '.join(self.ctx.text_passthrough_categories)}")


class BizHawkClientContext(CommonContext):
    command_processor = BizHawkClientCommandProcessor
    text_passthrough_categories: set[str]
    server_seed_name: str | None = None
    auth_status: AuthStatus
    password_requested: bool
    client_handler: BizHawkClient | None
    slot_data: dict[str, Any] | None = None
    rom_hash: str | None = None
    bizhawk_ctx: BizHawkContext

    watcher_timeout: float
    """The maximum amount of time the game watcher loop will wait for an update from the server before executing"""

    def __init__(self, server_address: str | None, password: str | None):
        super().__init__(server_address, password)
        self.text_passthrough_categories = set()
        self.auth_status = AuthStatus.NOT_AUTHENTICATED
        self.password_requested = False
        self.client_handler = None
        self.bizhawk_ctx = BizHawkContext()
        self.watcher_timeout = 0.5

    def _categorize_text(self, args: dict) -> TextCategory:
        if "type" not in args or args["type"] in {"Hint", "Join", "Part", "TagsChanged", "Goal", "Release", "Collect",
                                                  "Countdown", "ServerChat", "ItemCheat"}:
            return TextCategory.SERVER
        elif args["type"] == "Chat":
            return TextCategory.CHAT
        elif args["type"] == "ItemSend":
            if args["item"].player == self.slot:
                return TextCategory.OUTGOING
            elif args["receiving"] == self.slot:
                return TextCategory.INCOMING
            else:
                return TextCategory.OTHER

    def on_print_json(self, args: dict):
        super().on_print_json(args)
        if self.bizhawk_ctx.connection_status == ConnectionStatus.CONNECTED:
            if self._categorize_text(args) in self.text_passthrough_categories:
                Utils.async_start(display_message(self.bizhawk_ctx, self.rawjsontotextparser(copy.deepcopy(args["data"]))))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago BizHawk Client"
        return ui

    def on_package(self, cmd, args):
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)
            self.auth_status = AuthStatus.AUTHENTICATED
        elif cmd == "RoomInfo":
            self.server_seed_name = args.get("seed_name", None)

        if self.client_handler is not None:
            self.client_handler.on_package(self, cmd, args)

    async def server_auth(self, password_requested: bool=False):
        self.password_requested = password_requested

        if self.bizhawk_ctx.connection_status != ConnectionStatus.CONNECTED:
            logger.info("Awaiting connection to BizHawk before authenticating")
            return

        if self.client_handler is None:
            return

        # Ask handler to set auth
        if self.auth is None:
            self.auth_status = AuthStatus.NEED_INFO
            await self.client_handler.set_auth(self)

            # Handler didn't set auth, ask user for slot name
            if self.auth is None:
                await self.get_username()

        if password_requested and not self.password:
            self.auth_status = AuthStatus.NEED_INFO
            await super(BizHawkClientContext, self).server_auth(password_requested)

        await self.send_connect()
        self.auth_status = AuthStatus.PENDING

    async def disconnect(self, allow_autoreconnect: bool=False):
        self.auth_status = AuthStatus.NOT_AUTHENTICATED
        self.server_seed_name = None
        await super().disconnect(allow_autoreconnect)


async def _game_watcher(ctx: BizHawkClientContext):
    showed_connecting_message = False
    showed_connected_message = False
    showed_no_handler_message = False

    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), ctx.watcher_timeout)
        except asyncio.TimeoutError:
            pass

        ctx.watcher_event.clear()

        try:
            if ctx.bizhawk_ctx.connection_status == ConnectionStatus.NOT_CONNECTED:
                showed_connected_message = False

                if not showed_connecting_message:
                    logger.info("Waiting to connect to BizHawk...")
                    showed_connecting_message = True

                # Since a call to `connect` can take a while to return, this will cancel connecting
                # if the user has decided to close the client.
                connect_task = asyncio.create_task(connect(ctx.bizhawk_ctx), name="BizHawkConnect")
                exit_task = asyncio.create_task(ctx.exit_event.wait(), name="ExitWait")
                await asyncio.wait([connect_task, exit_task], return_when=asyncio.FIRST_COMPLETED)

                if exit_task.done():
                    connect_task.cancel()
                    return

                if not connect_task.result():
                    # Failed to connect
                    continue

                showed_no_handler_message = False

                script_version = await get_script_version(ctx.bizhawk_ctx)

                if script_version != EXPECTED_SCRIPT_VERSION:
                    logger.info(f"Connector script is incompatible. Expected version {EXPECTED_SCRIPT_VERSION} but "
                                f"got {script_version}. Disconnecting.")
                    disconnect(ctx.bizhawk_ctx)
                    continue

            showed_connecting_message = False

            await ping(ctx.bizhawk_ctx)

            if not showed_connected_message:
                showed_connected_message = True
                logger.info("Connected to BizHawk")

            rom_hash = await get_hash(ctx.bizhawk_ctx)
            if ctx.rom_hash is not None and ctx.rom_hash != rom_hash:
                if ctx.server is not None and not ctx.server.socket.closed:
                    logger.info(f"ROM changed. Disconnecting from server.")

                ctx.auth = None
                ctx.username = None
                ctx.client_handler = None
                ctx.finished_game = False
                await ctx.disconnect(False)
            ctx.rom_hash = rom_hash

            if ctx.client_handler is None:
                system = await get_system(ctx.bizhawk_ctx)
                ctx.client_handler = await AutoBizHawkClientRegister.get_handler(ctx, system)

                if ctx.client_handler is None:
                    if not showed_no_handler_message:
                        logger.info("No handler was found for this game. Double-check that the apworld is installed "
                                    "correctly and that you loaded the right ROM file.")
                        showed_no_handler_message = True
                    continue
                else:
                    showed_no_handler_message = False
                    logger.info(f"Running handler for {ctx.client_handler.game}")

        except RequestFailedError as exc:
            logger.info(f"Lost connection to BizHawk: {exc.args[0]}")
            continue
        except NotConnectedError:
            continue

        # Server auth
        if ctx.server is not None and not ctx.server.socket.closed:
            if ctx.auth_status == AuthStatus.NOT_AUTHENTICATED:
                Utils.async_start(ctx.server_auth(ctx.password_requested))
        else:
            ctx.auth_status = AuthStatus.NOT_AUTHENTICATED

        # Call the handler's game watcher
        await ctx.client_handler.game_watcher(ctx)


async def _run_game(rom: str):
    import os
    auto_start = settings.get_settings().bizhawkclient_options.rom_start

    if auto_start is True:
        emuhawk_path = settings.get_settings().bizhawkclient_options.emuhawk_path
        subprocess.Popen(
            [
                emuhawk_path,
                f"--lua={Utils.local_path('data', 'lua', 'connector_bizhawk_generic.lua')}",
                os.path.realpath(rom),
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif isinstance(auto_start, str):
        import shlex

        subprocess.Popen(
            [
                *shlex.split(auto_start),
                os.path.realpath(rom)
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def _patch_and_run_game(patch_file: str):
    try:
        metadata, output_file = Patch.create_rom_file(patch_file)
        Utils.async_start(_run_game(output_file))
        return metadata
    except Exception as exc:
        logger.exception(exc)
        Utils.messagebox("Error Patching Game", str(exc), True)
        return {}


def launch(*launch_args: str) -> None:
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
        args = parser.parse_args(launch_args)

        if args.patch_file != "":
            metadata = _patch_and_run_game(args.patch_file)
            if "server" in metadata:
                args.connect = metadata["server"]

        ctx = BizHawkClientContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(_game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.exception(e)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("BizHawkClient", exception_logger="Client")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
