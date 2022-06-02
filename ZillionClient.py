import asyncio
import subprocess
from typing import Any, Dict, Type
import colorama  # type: ignore

from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser

from zilliandomizer.zri.memory import Memory
from zilliandomizer.zri import events
from worlds.zillion.config import base_id


class ZillionCommandProcessor(ClientCommandProcessor):
    def _cmd_test_command(self) -> None:
        """ test command processor """
        logger.info("text command executed")


class ZillionContext(CommonContext):
    game = "Zillion"
    command_processor: Type[ClientCommandProcessor] = ZillionCommandProcessor
    to_game: "asyncio.Queue[events.EventToGame]"

    def __init__(self,
                 server_address: str,
                 password: str,
                 to_game: "asyncio.Queue[events.EventToGame]"):
        super().__init__(server_address, password)
        self.to_game = to_game

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.to_game.put_nowait(events.DeathEventToGame())
        return super().on_deathlink(data)


async def zillion_sync_task(ctx: ZillionContext, to_game: "asyncio.Queue[events.EventToGame]") -> None:
    logger.info("started zillion sync task")
    from_game: "asyncio.Queue[events.EventFromGame]" = asyncio.Queue()
    memory = Memory(from_game, to_game)
    next_item = 0
    while not ctx.exit_event.is_set():
        memory.check()
        if from_game.qsize():
            event_from_game = from_game.get_nowait()
            if isinstance(event_from_game, events.AcquireLocationEventFromGame):
                ctx.locations_checked.add(event_from_game.id + base_id)
            elif isinstance(event_from_game, events.DeathEventFromGame):
                pass  # await ctx.send_death()
                # key error
                # "source": self.player_names[self.slot]
            else:
                logger.warn(f"WARNING: unhandled event from game {event_from_game}")
        if len(ctx.items_received) > next_item:
            ctx.to_game.put_nowait(
                events.ItemEventToGame(ctx.items_received[next_item] - base_id)
            )
            next_item += 1
        await asyncio.sleep(0.09375)
    memory.rai.sock.close()  # TODO: make `with`


async def run_game(rom_file: str) -> None:
    # TODO: fix this
    subprocess.Popen(["retroarch", rom_file],
                     stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


async def main() -> None:
    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a .apzl Archipelago Binary Patch file')
    # SNI parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()
    print(args)

    if args.diff_file:
        import Patch
        logger.info("patch file was supplied - creating sms rom...")
        meta, rom_file = Patch.create_rom_file(args.diff_file)
        if "server" in meta:
            args.connect = meta["server"]
        logger.info(f"wrote rom file to {rom_file}")

        asyncio.create_task(run_game(rom_file))

    to_game: "asyncio.Queue[events.EventToGame]" = asyncio.Queue()
    ctx = ZillionContext(args.connect, args.password, to_game)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    sync_task = asyncio.create_task(zillion_sync_task(ctx, to_game))

    await ctx.exit_event.wait()

    ctx.server_address = None
    await sync_task
    await ctx.shutdown()


if __name__ == "__main__":
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
