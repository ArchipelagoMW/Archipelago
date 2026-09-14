import asyncio
import os
import sys
import time
import traceback
from argparse import Namespace
from enum import Enum

from Utils import init_logging, tuplize_version, loglevel_mapping
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    server_loop,
)
from NetUtils import ClientStatus

from .. import constants
from ..world import TombaWorld
from ..locations import LocationHandler
from ..helpers import Cleared
from ..events import EventData
from ..items import ItemHandler
from ..client.handlers import Handler
from ..client.handlers.found import FoundHandler
from ..client.handlers.check import CheckHandler
from .emulators.emulator import EmulatorException, KEEP_ALIVE_INTERVAL
from ..client.game import TombaGame, TombaException

if os.environ.get("TOMBA_DEV_MODE") == "1" or constants.RELEASE_TYPE != constants.ReleaseType.PRODUCTION:
    from ..client.debug.command_processor import TombaCommandProcessor
else:
    from CommonClient import ClientCommandProcessor

    TombaCommandProcessor = ClientCommandProcessor

MIN_TICK_DURATION = 0.1


class VersionError(Exception):
    pass


class ServerAuthException(Exception):
    pass


class ConnectionStatus(Enum):
    NOT_CONNECTED = 0
    CONNECTED = 1


class TombaContext(CommonContext):
    tags = {"AP"}
    game = constants.GAME
    items_handling = 0b111
    want_slot_data = True
    client_loop: asyncio.Task[None]
    tomba: TombaGame
    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED
    command_processor = TombaCommandProcessor

    found_handler: FoundHandler
    check_handler: CheckHandler

    should_reset_auth: bool

    deathlink_pending: bool

    sent_checks: list[int] = []

    def __init__(
        self,
        server_address: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(server_address, password)

        self.package_handlers = {"Connected": self.on_connected}

        self.tomba = TombaGame(self)
        self.should_reset_auth = False
        self.had_invalid_slot_data = None

        self.found_handler = FoundHandler(self, self.tomba)
        self.check_handler = CheckHandler(self, self.tomba)

        self.won = False
        self.deathlink_pending = False
        self.deathlink_status = False

        self.periodic_handlers: list[Handler] = [
            Handler(self.tomba.keep_alive, interval_ms=KEEP_ALIVE_INTERVAL),
            Handler(self.tomba.patch_game, interval_ms=1000),
            Handler(self.tomba.update_section, interval_ms=2000),
            Handler(self.tomba.update_events, interval_ms=250),
            Handler(self.tomba.update_inventory, interval_ms=750),
            Handler(self.check_handler.update_locations, interval_ms=500),
            Handler(self.tomba.update_messages, interval_ms=500),
            Handler(self.tomba.update_deathlink, interval_ms=750),
        ]

        self.sent_checks = []

    async def check_locations(self, raw_locations: list[int]) -> None:
        locations = [location for location in raw_locations if location not in self.sent_checks]

        if len(locations) <= 0:
            logger.debug(f"All locations from {raw_locations} are sent")
            return

        self.sent_checks.extend(locations)

        logger.debug(f"Location checks: {locations}")
        await super().check_locations(locations)

        for id in locations:
            location = LocationHandler.by_id[id]
            await self.check_handler.handle(location.name)

    def run_gui(self):
        from kvui import GameManager

        class TombaManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"Archipelago {constants.GAME} Client"

        self.ui = TombaManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def event_invalid_slot(self):
        # The next time we try to connect, reset the game loop for new auth
        self.had_invalid_slot_data = True
        self.auth = None
        # Don't try to autoreconnect, it will just fail
        self.disconnected_intentionally = True
        CommonContext.event_invalid_slot(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TombaContext, self).server_auth(password_requested)

        if self.had_invalid_slot_data:
            # We are connecting when previously we had the wrong ROM or server - just in case
            # re-read the ROM so that if the user had the correct address but wrong ROM, we
            # allow a successful reconnect
            self.should_reset_auth = True
            self.had_invalid_slot_data = False

        await super(TombaContext, self).get_username()
        await self.send_connect()

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def on_package(self, cmd: str, args: dict):
        callback = self.package_handlers.get(cmd, self.on_unhandled_package)
        callback(cmd, args)

    def on_unhandled_package(self, cmd: str, args: dict):
        pass

    def on_connected(self, cmd: str, args: dict):
        self.connection_status = ConnectionStatus.NOT_CONNECTED

        if self.slot is not None:
            self.game = self.slot_info[self.slot].game
        self.slot_data = args.get("slot_data", {})

        if self.slot_data["deathlink"]:
            self.deathlink_status = True

        generated_version = tuplize_version(self.slot_data.get("world_version", "2.0.0"))
        client_version = TombaWorld.world_version
        if generated_version.major != client_version.major:
            self.disconnected_intentionally = True
            raise VersionError(
                f"The installed world ({client_version.as_simple_string()}) is incompatible with "
                f"the world this game was generated on ({generated_version.as_simple_string()})"
            )

        logger.info("Server Status: Connected")

        self.sent_checks.extend(self.checked_locations)

        self.connection_status = ConnectionStatus.CONNECTED

    async def sync(self):
        sync_msg = [{"cmd": "Sync"}]
        await self.send_msgs(sync_msg)

    async def process_items_received(self):
        """Process items sent by Archipelago"""
        index = await self.tomba.get_saved_archipelago_index()
        if index is None:
            return

        if index < len(self.items_received):
            network_item = self.items_received[index]
            item = ItemHandler.by_id.get(network_item.item, None)
            if item is None:
                logger.warning(f"Received an unknown item from {network_item.player}: ID is {network_item.item}")
            elif not await self.tomba.inventory_handler.receive_item(item, network_item.player):
                return

            await self.tomba.set_saved_archipelago_index(index + 1)

    async def on_victory(self):
        await self.send_victory()

    async def on_event_cleared(self, event: EventData):
        location = LocationHandler.by_name[Cleared(event.name)]
        logger.debug(f"Sending location check to server for {event}")
        await self.check_locations([location.id])

    async def send_victory(self):
        if not self.won:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            logger.info("victory!")
            await self.send_msgs(message)
            self.won = True

    def is_deathlink_enabled(self) -> bool:
        return "DeathLink" in self.tags

    async def game_loop(self) -> None:
        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                logger.info("(Re)Starting game loop")

                await self.tomba.wait_for_emulator_connection()

                if not self.items_received:
                    await self.sync()

                last_tick = time.time()
                while True:
                    if self.connection_status == ConnectionStatus.CONNECTED:
                        if self.should_reset_auth:
                            self.should_reset_auth = False
                            raise ServerAuthException("Resetting due to wrong archipelago server")

                        if self.deathlink_status != self.is_deathlink_enabled():
                            await self.update_death_link(self.deathlink_status)

                        for handler in self.periodic_handlers:
                            current_time = time.perf_counter() * 1000
                            if current_time - handler.last_run >= handler.interval_ms:
                                handler_start = time.perf_counter()

                                await handler.callback(*handler.args, **handler.kwargs)
                                handler.last_run = current_time

                                handler_duration = (time.perf_counter() - handler_start) * 1000
                                handler.last_run = current_time

                                if handler_duration > 50.0:
                                    pass  # logger.debug(f"[SLOW WARNING] Handler {handler.callback.__name__} took {handler_duration:.2f}ms")

                        await self.process_items_received()

                        # await self.found_handler.update_found_items()

                    now = time.time()
                    tick_duration = now - last_tick
                    sleep_duration = max(MIN_TICK_DURATION - tick_duration, 0)
                    await asyncio.sleep(sleep_duration)

                    last_tick = now
            except (TimeoutError, EmulatorException, TombaException) as e:
                logger.error(e)
            except Exception:  # DEBUG
                logger.critical(traceback.format_exc())


async def main(args: Namespace) -> None:
    ctx = TombaContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    else:
        init_logging("TombaClient", exception_logger="Client", loglevel=loglevel_mapping[args.loglevel])

    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(ctx.game_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


if __name__ == "__main__":
    from worlds.tomba.client.launch import launch_tomba_client

    launch_tomba_client(*sys.argv[1:])
