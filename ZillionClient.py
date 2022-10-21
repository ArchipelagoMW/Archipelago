import asyncio
import base64
import platform
from typing import Any, Coroutine, Dict, Optional, Type, cast

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
from NetUtils import ClientStatus
import Utils

import colorama  # type: ignore

from zilliandomizer.zri.memory import Memory
from zilliandomizer.zri import events
from zilliandomizer.utils.loc_name_maps import id_to_loc
from zilliandomizer.options import Chars
from zilliandomizer.patch import RescueInfo

from worlds.zillion.id_maps import make_id_to_others
from worlds.zillion.config import base_id


class ZillionCommandProcessor(ClientCommandProcessor):
    ctx: "ZillionContext"

    def _cmd_sms(self) -> None:
        """ Tell the client that Zillion is running in RetroArch. """
        logger.info("ready to look for game")
        self.ctx.look_for_retroarch.set()


class ZillionContext(CommonContext):
    game = "Zillion"
    command_processor: Type[ClientCommandProcessor] = ZillionCommandProcessor
    items_handling = 1  # receive items from other players

    from_game: "asyncio.Queue[events.EventFromGame]"
    to_game: "asyncio.Queue[events.EventToGame]"
    ap_local_count: int
    """ local checks watched by server """
    next_item: int
    """ index in `items_received` """
    ap_id_to_name: Dict[int, str]
    ap_id_to_zz_id: Dict[int, int]
    start_char: Chars = "JJ"
    rescues: Dict[int, RescueInfo] = {}
    loc_mem_to_id: Dict[int, int] = {}
    got_slot_data: asyncio.Event
    """ serves as a flag for whether I am logged in to the server """

    look_for_retroarch: asyncio.Event
    """
    There is a bug in Python in Windows
    https://github.com/python/cpython/issues/91227
    that makes it so if I look for RetroArch before it's ready,
    it breaks the asyncio udp transport system.

    As a workaround, we don't look for RetroArch until this event is set.
    """

    def __init__(self,
                 server_address: str,
                 password: str) -> None:
        super().__init__(server_address, password)
        self.from_game = asyncio.Queue()
        self.to_game = asyncio.Queue()
        self.got_slot_data = asyncio.Event()

        self.look_for_retroarch = asyncio.Event()
        if platform.system() != "Windows":
            # asyncio udp bug is only on Windows
            self.look_for_retroarch.set()

        self.reset_game_state()

    def reset_game_state(self) -> None:
        for _ in range(self.from_game.qsize()):
            self.from_game.get_nowait()
        for _ in range(self.to_game.qsize()):
            self.to_game.get_nowait()
        self.got_slot_data.clear()

        self.ap_local_count = 0
        self.next_item = 0
        self.ap_id_to_name = {}
        self.ap_id_to_zz_id = {}
        self.rescues = {}
        self.loc_mem_to_id = {}

        self.locations_checked.clear()
        self.missing_locations.clear()
        self.checked_locations.clear()
        self.finished_game = False
        self.items_received.clear()

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

            payload = {
                "cmd": "Get",
                "keys": [f"zillion-{self.auth}-doors"]
            }
            asyncio.create_task(self.send_msgs([payload]))
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to ZillionClient: {args}")
                return
            keys = cast(Dict[str, Optional[str]], args["keys"])
            doors_b64 = keys[f"zillion-{self.auth}-doors"]
            if doors_b64:
                logger.info("received door data from server")
                doors = base64.b64decode(doors_b64)
                self.to_game.put_nowait(events.DoorEventToGame(doors))

    def process_from_game_queue(self) -> None:
        if self.from_game.qsize():
            event_from_game = self.from_game.get_nowait()
            if isinstance(event_from_game, events.AcquireLocationEventFromGame):
                server_id = event_from_game.id + base_id
                loc_name = id_to_loc[event_from_game.id]
                self.locations_checked.add(server_id)
                if server_id in self.missing_locations:
                    self.ap_local_count += 1
                    n_locations = len(self.missing_locations) + len(self.checked_locations) - 1  # -1 to ignore win
                    logger.info(f'New Check: {loc_name} ({self.ap_local_count}/{n_locations})')
                    asyncio.create_task(self.send_msgs([
                        {"cmd": 'LocationChecks', "locations": [server_id]}
                    ]))
                else:
                    # This will happen a lot in Zillion,
                    # because all the key words are local and unwatched by the server.
                    logger.debug(f"DEBUG: {loc_name} not in missing")
            elif isinstance(event_from_game, events.DeathEventFromGame):
                asyncio.create_task(self.send_death())
            elif isinstance(event_from_game, events.WinEventFromGame):
                if not self.finished_game:
                    asyncio.create_task(self.send_msgs([
                        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
                    ]))
                    self.finished_game = True
            elif isinstance(event_from_game, events.DoorEventFromGame):
                if self.auth:
                    doors_b64 = base64.b64encode(event_from_game.doors).decode()
                    payload = {
                        "cmd": "Set",
                        "key": f"zillion-{self.auth}-doors",
                        "operations": [{"operation": "replace", "value": doors_b64}]
                    }
                    asyncio.create_task(self.send_msgs([payload]))
            else:
                logger.warning(f"WARNING: unhandled event from game {event_from_game}")

    def process_items_received(self) -> None:
        if len(self.items_received) > self.next_item:
            zz_item_ids = [self.ap_id_to_zz_id[item.item] for item in self.items_received]
            for index in range(self.next_item, len(self.items_received)):
                ap_id = self.items_received[index].item
                from_name = self.player_names[self.items_received[index].player]
                # TODO: colors in this text, like sni client?
                logger.info(f'received {self.ap_id_to_name[ap_id]} from {from_name}')
            self.to_game.put_nowait(
                events.ItemEventToGame(zz_item_ids)
            )
            self.next_item = len(self.items_received)


async def zillion_sync_task(ctx: ZillionContext) -> None:
    logger.info("started zillion sync task")

    # to work around the Python bug where we can't check for RetroArch
    if not ctx.look_for_retroarch.is_set():
        logger.info("Start Zillion in RetroArch, then use the /sms command to connect to it.")
    await asyncio.wait((
        asyncio.create_task(ctx.look_for_retroarch.wait()),
        asyncio.create_task(ctx.exit_event.wait())
    ), return_when=asyncio.FIRST_COMPLETED)

    last_log = ""

    def log_no_spam(msg: str) -> None:
        nonlocal last_log
        if msg != last_log:
            last_log = msg
            logger.info(msg)

    # to only show this message once per client run
    help_message_shown = False

    with Memory(ctx.from_game, ctx.to_game) as memory:
        while not ctx.exit_event.is_set():
            ram = await memory.read()
            name = memory.get_player_name(ram).decode()
            if len(name):
                if name == ctx.auth:
                    # this is the name we know
                    if ctx.server and ctx.server.socket:  # type: ignore
                        if memory.have_generation_info():
                            log_no_spam("everything connected")
                            await memory.process_ram(ram)
                            ctx.process_from_game_queue()
                            ctx.process_items_received()
                        else:  # no generation info
                            if ctx.got_slot_data.is_set():
                                memory.set_generation_info(ctx.rescues, ctx.loc_mem_to_id)
                                ctx.ap_id_to_name, ctx.ap_id_to_zz_id, _ap_id_to_zz_item = \
                                    make_id_to_others(ctx.start_char)
                                ctx.next_item = 0
                                ctx.ap_local_count = len(ctx.checked_locations)
                            else:  # no slot data yet
                                asyncio.create_task(ctx.send_connect())
                                log_no_spam("logging in to server...")
                                await asyncio.wait((
                                    ctx.got_slot_data.wait(),
                                    ctx.exit_event.wait(),
                                    asyncio.sleep(6)
                                ), return_when=asyncio.FIRST_COMPLETED)  # to not spam connect packets
                    else:  # server not connected
                        log_no_spam("waiting for server connection...")
                else:  # new game
                    log_no_spam("connected to new game")
                    await ctx.disconnect()
                    ctx.reset_server_state()
                    ctx.reset_game_state()
                    memory.reset_game_state()

                    ctx.auth = name
                    asyncio.create_task(ctx.connect())
                    await asyncio.wait((
                        ctx.got_slot_data.wait(),
                        ctx.exit_event.wait(),
                        asyncio.sleep(6)
                    ), return_when=asyncio.FIRST_COMPLETED)  # to not spam connect packets
            else:  # no name found in game
                if not help_message_shown:
                    logger.info('In RetroArch, make sure "Settings > Network > Network Commands" is on.')
                    help_message_shown = True
                log_no_spam("looking for connection to game...")
                await asyncio.sleep(0.3)

            await asyncio.sleep(0.09375)
        logger.info("zillion sync task ending")


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

    ctx = ZillionContext(args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    sync_task = asyncio.create_task(zillion_sync_task(ctx))

    await ctx.exit_event.wait()

    ctx.server_address = None
    logger.debug("waiting for sync task to end")
    await sync_task
    logger.debug("sync task ended")
    await ctx.shutdown()


if __name__ == "__main__":
    Utils.init_logging("ZillionClient", exception_logger="Client")

    colorama.init()
    asyncio.run(main())
    colorama.deinit()
