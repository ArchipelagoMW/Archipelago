import asyncio
import sys
import time
from argparse import Namespace

from Utils import init_logging
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    server_loop,
)

from worlds.tomba import constants
from worlds.tomba.client import retroarch

MIN_TICK_DURATION = 0.1
CORE_TYPE = "playstation"


class TombaClient:
    playstation: retroarch.RetroArch

    def __init__(self, retroarch_address="127.0.0.1", retroarch_port=55355):
        self.retroarch_address = retroarch_address
        self.retroarch_port = retroarch_port

    async def wait_for_retroarch_connection(self):
        logger.info("Waiting on connection to Retroarch...")
        self.playstation = retroarch.RetroArch(self.retroarch_address, self.retroarch_port)

        while True:
            try:
                version = await self.playstation.get_retroarch_version()
                status, core_type, rom_name, _ = await self.playstation.get_retroarch_status()

                if retroarch.is_connected(status) and core_type == CORE_TYPE:
                    break
            except (BlockingIOError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)
                pass

            await asyncio.sleep(1.0)

        logger.info(f"Connected to Retroarch {version} running {rom_name}")

    async def main_tick(self):
        pass


class TombaContext(CommonContext):
    tags = {"AP"}
    game = constants.GAME
    client_loop: asyncio.Task[None]
    client: TombaClient

    def __init__(
        self,
        server_address: str | None = None,
        password: str | None = None,
    ) -> None:
        self.client = TombaClient()

        super().__init__(server_address, password)

    def run_gui(self):
        from kvui import GameManager

        class TombaManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"Archipelago {constants.GAME} Client"

        self.ui = TombaManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def game_loop(self) -> None:
        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                await self.client.wait_for_retroarch_connection()

                last_tick = time.time()
                while True:
                    await self.client.main_tick()

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
        init_logging("TombaClient", exception_logger="Client")

    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(ctx.game_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


if __name__ == "__main__":
    from worlds.tomba.client.launch import launch_tomba_client

    launch_tomba_client(*sys.argv[1:])
