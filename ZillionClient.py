import asyncio
import subprocess
from typing import Any, Coroutine, Dict, Type
import colorama
from NetUtils import ClientStatus
import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser

from zilliandomizer.zri.memory import Memory
from zilliandomizer.zri import events
from zilliandomizer.utils.loc_name_maps import id_to_loc
from zilliandomizer.options import Chars
from zilliandomizer.patch import RescueInfo

from worlds.zillion.id_maps import make_id_to_others
from worlds.zillion.config import base_id

# TODO: make sure close button works on ZillionClient window
# TODO: test: receive remote rescue in scrolling hallway


class ZillionCommandProcessor(ClientCommandProcessor):
    def _cmd_test_command(self) -> None:
        """ test command processor """
        logger.info("text command executed")


class ZillionContext(CommonContext):
    game = "Zillion"
    command_processor: Type[ClientCommandProcessor] = ZillionCommandProcessor
    to_game: "asyncio.Queue[events.EventToGame]"
    items_handling = 1  # receive items from other players

    start_char: Chars = "JJ"
    rescues: Dict[int, RescueInfo] = {}
    loc_mem_to_id: Dict[int, int] = {}
    got_slot_data: asyncio.Event

    def __init__(self,
                 server_address: str,
                 password: str,
                 to_game: "asyncio.Queue[events.EventToGame]"):
        super().__init__(server_address, password)
        self.to_game = to_game
        self.got_slot_data = asyncio.Event()

    # override
    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.to_game.put_nowait(events.DeathEventToGame())
        return super().on_deathlink(data)

    # override
    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            logger.info('waiting for connection to game...')
            return
        logger.info("logging in to server...")
        await self.send_connect()

    # override
    def run_gui(self) -> None:
        from kvui import GameManager

        class ZillionManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Zillion Client"

        self.ui = ZillionManager(self)
        run_co: Coroutine[Any, Any, None] = self.ui.async_run()  # type: ignore
        # kivy types missing
        self.ui_task = asyncio.create_task(run_co, name="UI")

    def on_package(self, cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Connected":
            logger.info("logged in to Archipelago server")
            if "slot_data" not in args:
                logger.warn("`Connected` packet missing `slot_data`")
                return
            slot_data = args["slot_data"]

            if "start_char" not in slot_data:
                logger.warn("invalid Zillion `Connected` packet, `slot_data` missing `start_char`")
                return
            self.start_char = slot_data['start_char']
            if self.start_char not in {"Apple", "Champ", "JJ"}:
                logger.warn("invalid Zillion `Connected` packet, "
                            f"`slot_data` `start_char` has invalid value: {self.start_char}")

            if "rescues" not in slot_data:
                logger.warn("invalid Zillion `Connected` packet, `slot_data` missing `rescues`")
                return
            rescues = slot_data["rescues"]
            self.rescues = {}
            for rescue_id, json_info in rescues.items():
                assert rescue_id in ("0", "1"), f"invalid rescue_id in Zillion slot_data: {rescue_id}"
                # TODO: just take start_char out of the RescueInfo so there's no opportunity for a mismatch?
                assert json_info["start_char"] == self.start_char, \
                    f'mismatch in Zillion slot data: {json_info["start_char"]} {self.start_char}'
                ri = RescueInfo(json_info["start_char"],
                                json_info["room_code"],
                                json_info["mask"])
                self.rescues[0 if rescue_id == "0" else 1] = ri

            if "loc_mem_to_id" not in slot_data:
                logger.warn("invalid Zillion `Connected` packet, `slot_data` missing `loc_mem_to_id`")
                return
            loc_mem_to_id = slot_data["loc_mem_to_id"]
            self.loc_mem_to_id = {}
            for mem_str, id_str in loc_mem_to_id.items():
                mem = int(mem_str)
                id_ = int(id_str)
                room_i = mem // 256
                assert 0 <= room_i < 74
                assert id_ in id_to_loc
                self.loc_mem_to_id[mem] = id_

            self.got_slot_data.set()


async def zillion_sync_task(ctx: ZillionContext, to_game: "asyncio.Queue[events.EventToGame]") -> None:
    logger.info("started zillion sync task")
    from_game: "asyncio.Queue[events.EventFromGame]" = asyncio.Queue()

    with Memory(from_game, to_game) as memory:
        found_name = False
        help_message_shown = False
        logger.info("looking for game...")
        while (not found_name) and (not ctx.exit_event.is_set()):
            # logger.info("looking for name")
            name = await memory.check_for_player_name()
            # logger.info(f"found name {name}")
            if len(name):
                # logger.info("len(name)")
                ctx.auth = name.decode()
                found_name = True
                logger.info("connected to game")
                if ctx.server and ctx.server.socket:  # type: ignore
                    logger.info("logging in to server...")
                    await ctx.send_connect()
                else:
                    logger.info("waiting for server connection...")
            else:
                if not help_message_shown:
                    logger.info('In RetroArch, make sure "Settings > Network > Network Commands" is on.')
                    help_message_shown = True
                # logger.info("before sleep")
                await asyncio.sleep(0.3)
                # logger.info("after sleep")

        ap_id_to_name: Dict[int, str] = {}
        ap_id_to_zz_id: Dict[int, int] = {}
        if not ctx.exit_event.is_set():
            logger.info("waiting for server login...")
            await ctx.got_slot_data.wait()
            memory.set_generation_info(ctx.rescues, ctx.loc_mem_to_id)
            ap_id_to_name, ap_id_to_zz_id, _ap_id_to_zz_item = make_id_to_others(ctx.start_char)

        next_item = 0
        while not ctx.exit_event.is_set():
            await memory.check()
            if from_game.qsize():
                event_from_game = from_game.get_nowait()
                if isinstance(event_from_game, events.AcquireLocationEventFromGame):
                    server_id = event_from_game.id + base_id
                    loc_name = id_to_loc[event_from_game.id]
                    ctx.locations_checked.add(server_id)
                    # TODO: progress number "(1/146)" or something like that
                    if server_id in ctx.missing_locations:
                        logger.info(f'New Check: {loc_name}')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [server_id]}])
                    else:
                        logger.info(f"DEBUG: {loc_name} not in missing")
                elif isinstance(event_from_game, events.DeathEventFromGame):
                    try:
                        await ctx.send_death()
                    except KeyError:
                        logger.warning("KeyError sending death")
                elif isinstance(event_from_game, events.WinEventFromGame):
                    if not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                else:
                    logger.warning(f"WARNING: unhandled event from game {event_from_game}")
            if len(ctx.items_received) > next_item:
                zz_item_ids = [ap_id_to_zz_id[item.item] for item in ctx.items_received]
                for index in range(next_item, len(ctx.items_received)):
                    ap_id = ctx.items_received[index].item
                    # TODO: what do I want to log here? do I need anything? is the logging from CommonClient enough?
                    logger.info(f'received item {ap_id_to_name[ap_id]}')
                ctx.to_game.put_nowait(
                    events.ItemEventToGame(zz_item_ids)
                )
                next_item = len(ctx.items_received)
            await asyncio.sleep(0.09375)


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
    # TODO: change logging to debug
    logger.info("waiting for sync task to end")
    await sync_task
    logger.info("sync task ended")
    await ctx.shutdown()


if __name__ == "__main__":
    Utils.init_logging("ZillionClient", exception_logger="Client")

    colorama.init()
    asyncio.run(main())
    colorama.deinit()
