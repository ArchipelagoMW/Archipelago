import asyncio
import sys
import time
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

from worlds.tomba import constants
from worlds.tomba.world import TombaWorld
from worlds.tomba.items import ItemHandler, ItemData, ItemBehavior
from worlds.tomba.locations import LocationHandler
from worlds.tomba.client.retroarch import RetroArchException
from worlds.tomba.client.game import TombaGame, TombaException

MIN_TICK_DURATION = 0.1


class VersionError(Exception):
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

    # List of items found by the player to process
    found_items: list[ItemData] = []

    def __init__(
        self,
        server_address: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(server_address, password)

        self.package_handlers = {
            "Connected": self.on_connected,
        }

        self.tomba = TombaGame()
        self.had_invalid_slot_data = None

        self.won = False

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
            self.tomba.should_reset_auth = True
            self.had_invalid_slot_data = False

        while self.tomba.auth is None:
            await asyncio.sleep(0.1)

            # Just return if we're closing
            if self.exit_event.is_set():
                return
        self.auth = self.tomba.auth
        await self.send_connect()

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
        generated_version = tuplize_version(self.slot_data.get("world_version", "2.0.0"))
        client_version = TombaWorld.world_version
        if generated_version.major != client_version.major:
            self.disconnected_intentionally = True
            raise VersionError(
                f"The installed world ({client_version.as_simple_string()}) is incompatible with "
                f"the world this game was generated on ({generated_version.as_simple_string()})"
            )

        # DEBUG
        logger.info("missing locations")
        logger.info(self.missing_locations)
        logger.info("checked locations")
        logger.info(self.checked_locations)
        logger.info("items received")
        logger.info(self.items_received)

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

            if await self.tomba.receive_item(network_item.item, network_item.player):
                self.tomba.set_saved_archipelago_index(index + 1)

    async def update_found_items(self):
        """Update the list of found items to be processed in the main loop"""
        newly_found_items = await self.tomba.get_pending_found_items()
        if newly_found_items is None:
            return

        for game_id in newly_found_items:
            item = ItemHandler.by_game_id.get(game_id, None)
            if item is None:
                logger.error(f"Player got an unknown item game ID: {game_id}")
                return

            self.found_items.append(item)

        if len(newly_found_items):
            await self.tomba.request_clear_obtained_items()

    async def process_found_items(self):
        if len(self.found_items) <= 0:
            return

        item = self.found_items.pop(0)
        if not await self.on_item_get(item):
            # Put back the item in the queue if it fails to process
            self.found_items.append(item)

    async def on_item_get(self, item: ItemData) -> bool:
        if item.behavior is ItemBehavior.ORIGINAL:
            return await self.tomba.receive_item(item.id, 0)

        location_ids = LocationHandler.filter(item.id, self.tomba.area_id, self.tomba.section_id)
        if location_ids is None:
            logger.error(f"Player got an item with no location: {item.name}")
            return await self.tomba.receive_item(item.id, 0)

        first_unchecked = next((id for id in location_ids if id not in self.checked_locations), None)

        location_id = first_unchecked
        if location_id is None:
            # TODO: In case this happens, we might want to check the implemented logic
            # or give the item directly to the player
            logger.error(f"Player has found {item.name} but there are no location left to send it.")
            return True

        logger.debug(f"Sending location check to server for {location_id}")
        await self.check_locations([location_id])
        return True

    async def on_victory(self):
        pass  # await self.send_victory()

    async def send_victory(self):
        if not self.won:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            logger.info("victory!")
            await self.send_msgs(message)
            self.won = True

    async def game_loop(self) -> None:
        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                logger.info("(Re)Starting game loop")

                await self.tomba.wait_for_retroarch_connection()
                await self.tomba.perform_auth()
                # If we find ourselves with new auth, reconnect
                if self.auth and self.tomba.auth != self.auth:
                    logger.info("Detected new ROM, disconnecting...")
                    await self.disconnect()
                    continue

                if not self.items_received:
                    await self.sync()

                last_tick = time.time()
                while True:
                    if self.connection_status == ConnectionStatus.CONNECTED:
                        await self.tomba.main_tick(self.on_victory)

                        await self.process_items_received()

                        await self.update_found_items()
                        await self.process_found_items()

                    now = time.time()
                    tick_duration = now - last_tick
                    sleep_duration = max(MIN_TICK_DURATION - tick_duration, 0)
                    await asyncio.sleep(sleep_duration)

                    last_tick = now
            except (TimeoutError, RetroArchException, TombaException):
                await asyncio.sleep(1.0)
            except Exception:  # DEBUG
                await asyncio.sleep(1.0)


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
