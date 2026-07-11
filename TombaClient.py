import asyncio
import sys
import time
from argparse import Namespace

from Utils import init_logging, tuplize_version, loglevel_mapping
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    server_loop,
)

from worlds.tomba import constants
from worlds.tomba.world import TombaWorld
from worlds.tomba.items import ITEM_NAME_TO_ID
from worlds.tomba.client import retroarch
from worlds.tomba.client.game import TombaGame

MIN_TICK_DURATION = 0.1


class VersionError(Exception):
    pass


class TombaContext(CommonContext):
    tags = {"AP"}
    game = constants.GAME
    items_handling = 0b101
    want_slot_data = True
    client_loop: asyncio.Task[None]
    tomba: TombaGame

    def __init__(
        self,
        server_address: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(server_address, password)

        self.package_handlers = {
            "Connected": self.on_connected,
            "ReceivedItems": self.on_received_items,
        }

        self.tomba = TombaGame()
        self.had_invalid_slot_data = None

        # Checks received from server
        self.received_checks = []
        # Checks found by the client
        self.found_checks = []

        self.received_index = 0

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
        logger.debug("missing locations")
        logger.debug(self.missing_locations)
        logger.debug("checked locations")
        logger.debug(self.checked_locations)

        self.received_checks = [
            {"item": ITEM_NAME_TO_ID[constants.CHARITY_WINGS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHARITY_WINGS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHARITY_WINGS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHARITY_WINGS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHARITY_WINGS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.FURIOUS_TORNADO], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHICK], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHICK], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.CHICK], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.BANANAS], "location": 0, "player": 1, "flags": 1},
            {"item": ITEM_NAME_TO_ID[constants.BANANAS], "location": 0, "player": 1, "flags": 1},
        ]

    def on_received_items(self, cmd: str, args: dict):
        for index, item in enumerate(args["items"], start=args["index"]):
            self.received_checks[index] = item

    async def sync(self):
        sync_msg = [{"cmd": "Sync"}]
        await self.send_msgs(sync_msg)

    async def process_received_checks(self):
        # TODO: Fetch received_index from the game

        if self.received_index < len(self.received_checks):
            item = self.received_checks[self.received_index]

            if await self.tomba.receive_item(item["item"], item["player"]):
                # TODO: Save received index in RAM
                self.received_index += 1

    async def game_loop(self) -> None:
        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                self.found_checks.clear()
                self.received_checks.clear()

                await self.tomba.wait_for_retroarch_connection()
                await self.tomba.perform_auth()
                # If we find ourselves with new auth, reconnect
                if self.auth and self.tomba.auth != self.auth:
                    logger.info("Detected new ROM, disconnecting...")
                    await self.disconnect()
                    continue

                if not self.received_checks:
                    await self.sync()

                await self.tomba.wait_for_game_ready()

                last_tick = time.time()
                while True:
                    await self.tomba.main_tick()

                    await self.process_received_checks()

                    now = time.time()
                    tick_duration = now - last_tick
                    sleep_duration = max(MIN_TICK_DURATION - tick_duration, 0)
                    await asyncio.sleep(sleep_duration)

                    last_tick = now
            except (
                retroarch.RetroArchException,
                asyncio.TimeoutError,
                TimeoutError,
                ConnectionResetError,
            ):
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
