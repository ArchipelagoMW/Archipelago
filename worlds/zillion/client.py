import asyncio
import base64
import io
import pkgutil
import platform
from typing import Any, ClassVar, Coroutine, Protocol, cast

from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
from NetUtils import ClientStatus
from Utils import async_start

import colorama
from typing_extensions import override

from zilliandomizer.zri.memory import Memory, RescueInfo
from zilliandomizer.zri import events
from zilliandomizer.utils.loc_name_maps import id_to_loc
from zilliandomizer.options import Chars

from .id_maps import loc_name_to_id, make_id_to_others
from .config import base_id


class ZillionCommandProcessor(ClientCommandProcessor):
    ctx: "ZillionContext"

    def _cmd_sms(self) -> None:
        """ Tell the client that Zillion is running in RetroArch. """
        logger.info("ready to look for game")
        self.ctx.look_for_retroarch.set()

    def _cmd_map(self) -> None:
        """ Toggle view of the map tracker. """
        self.ctx.ui_toggle_map()


class ToggleCallback(Protocol):
    def __call__(self) -> object: ...


class SetRoomCallback(Protocol):
    def __call__(self, rooms: list[list[int]]) -> object: ...


class ZillionContext(CommonContext):
    game = "Zillion"
    command_processor = ZillionCommandProcessor
    items_handling = 1  # receive items from other players

    known_name: str | None
    """ This is almost the same as `auth` except `auth` is reset to `None` when server disconnects, and this isn't. """

    from_game: "asyncio.Queue[events.EventFromGame]"
    to_game: "asyncio.Queue[events.EventToGame]"
    ap_local_count: int
    """ local checks watched by server """
    next_item: int
    """ index in `items_received` """
    ap_id_to_name: dict[int, str]
    ap_id_to_zz_id: dict[int, int]
    start_char: Chars = "JJ"
    rescues: dict[int, RescueInfo] = {}
    loc_mem_to_id: dict[int, int] = {}
    got_room_info: asyncio.Event
    """ flag for connected to server """
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

    ui_toggle_map: ToggleCallback
    ui_set_rooms: SetRoomCallback
    """ parameter is y 16 x 8 numbers to show in each room """

    def __init__(self,
                 server_address: str,
                 password: str) -> None:
        super().__init__(server_address, password)
        self.known_name = None
        self.from_game = asyncio.Queue()
        self.to_game = asyncio.Queue()
        self.got_room_info = asyncio.Event()
        self.got_slot_data = asyncio.Event()
        self.ui_toggle_map = lambda: None
        self.ui_set_rooms = lambda rooms: None

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

    @override
    def on_deathlink(self, data: dict[str, Any]) -> None:
        self.to_game.put_nowait(events.DeathEventToGame())
        return super().on_deathlink(data)

    @override
    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            logger.info("waiting for connection to game...")
            return
        logger.info("logging in to server...")
        await self.send_connect()

    @override
    def run_gui(self) -> None:
        from kvui import GameManager
        from kivy.core.text import Label as CoreLabel
        from kivy.graphics import Ellipse, Color, Rectangle
        from kivy.graphics.texture import Texture
        from kivy.uix.layout import Layout
        from kivy.uix.image import CoreImage
        from kivy.uix.widget import Widget

        class ZillionManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
            ]
            base_title = "Archipelago Zillion Client"

            class MapPanel(Widget):
                MAP_WIDTH: ClassVar[int] = 281

                map_background: CoreImage
                _number_textures: list[Texture] = []
                rooms: list[list[int]] = []

                def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
                    super().__init__(**kwargs)

                    FILE_NAME = "empty-zillion-map-row-col-labels-281.png"
                    image_file_data = pkgutil.get_data(__name__, FILE_NAME)
                    if not image_file_data:
                        raise FileNotFoundError(f"{__name__=} {FILE_NAME=}")
                    data = io.BytesIO(image_file_data)
                    self.map_background = CoreImage(data, ext="png")
                    assert self.map_background.texture.size[0] == ZillionManager.MapPanel.MAP_WIDTH

                    self.rooms = [[0 for _ in range(8)] for _ in range(16)]

                    self._make_numbers()
                    self.update_map()

                    self.bind(pos=self.update_map)
                    # self.bind(size=self.update_bg)

                def _make_numbers(self) -> None:
                    self._number_textures = []
                    for n in range(10):
                        label = CoreLabel(text=str(n), font_size=22, color=(0.1, 0.9, 0, 1))
                        label.refresh()
                        self._number_textures.append(label.texture)

                def update_map(self, *args: Any) -> None:  # noqa: ANN401
                    self.canvas.clear()

                    with self.canvas:
                        Color(1, 1, 1, 1)
                        Rectangle(texture=self.map_background.texture,
                                  pos=self.pos,
                                  size=self.map_background.texture.size)
                        for y in range(16):
                            for x in range(8):
                                num = self.rooms[15 - y][x]
                                if num > 0:
                                    Color(0, 0, 0, 0.4)
                                    pos = [self.pos[0] + 17 + x * 32, self.pos[1] + 14 + y * 24]
                                    Ellipse(size=[22, 22], pos=pos)
                                    Color(1, 1, 1, 1)
                                    pos = [self.pos[0] + 22 + x * 32, self.pos[1] + 12 + y * 24]
                                    num_texture = self._number_textures[num]
                                    Rectangle(texture=num_texture, size=num_texture.size, pos=pos)

            @override
            def build(self) -> Layout:
                container = super().build()
                self.map_widget = ZillionManager.MapPanel(size_hint_x=None, width=ZillionManager.MapPanel.MAP_WIDTH)
                self.main_area_container.add_widget(self.map_widget)
                return container

            def toggle_map_width(self) -> None:
                if self.map_widget.width == 0:
                    self.map_widget.width = ZillionManager.MapPanel.MAP_WIDTH
                else:
                    self.map_widget.width = 0
                self.container.do_layout()

            def set_rooms(self, rooms: list[list[int]]) -> None:
                self.map_widget.rooms = rooms
                self.map_widget.update_map()

        self.ui = ZillionManager(self)
        self.ui_toggle_map = lambda: isinstance(self.ui, ZillionManager) and self.ui.toggle_map_width()
        self.ui_set_rooms = lambda rooms: isinstance(self.ui, ZillionManager) and self.ui.set_rooms(rooms)
        run_co: Coroutine[Any, Any, None] = self.ui.async_run()
        self.ui_task = asyncio.create_task(run_co, name="UI")

    @override
    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        self.room_item_numbers_to_ui()
        if cmd == "Connected":
            logger.info("logged in to Archipelago server")
            if "slot_data" not in args:
                logger.warning("`Connected` packet missing `slot_data`")
                return
            slot_data = args["slot_data"]

            if "start_char" not in slot_data:
                logger.warning("invalid Zillion `Connected` packet, `slot_data` missing `start_char`")
                return
            self.start_char = slot_data["start_char"]
            if self.start_char not in {"Apple", "Champ", "JJ"}:
                logger.warning("invalid Zillion `Connected` packet, "
                               f"`slot_data` `start_char` has invalid value: {self.start_char}")

            if "rescues" not in slot_data:
                logger.warning("invalid Zillion `Connected` packet, `slot_data` missing `rescues`")
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
                logger.warning("invalid Zillion `Connected` packet, `slot_data` missing `loc_mem_to_id`")
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

            if len(self.loc_mem_to_id) != 394:
                logger.warning("invalid Zillion `Connected` packet, "
                               f"`slot_data` missing locations in `loc_mem_to_id` - len {len(self.loc_mem_to_id)}")

            self.got_slot_data.set()

            payload = {
                "cmd": "Get",
                "keys": [f"zillion-{self.auth}-doors"],
            }
            async_start(self.send_msgs([payload]))
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to ZillionClient: {args}")
                return
            keys = cast(dict[str, str | None], args["keys"])
            doors_b64 = keys.get(f"zillion-{self.auth}-doors", None)
            if doors_b64:
                logger.info("received door data from server")
                doors = base64.b64decode(doors_b64)
                self.to_game.put_nowait(events.DoorEventToGame(doors))
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
            self.got_room_info.set()

    def room_item_numbers_to_ui(self) -> None:
        rooms = [[0 for _ in range(8)] for _ in range(16)]
        for loc_id in self.missing_locations:
            loc_id_small = loc_id - base_id
            loc_name = id_to_loc[loc_id_small]
            y = ord(loc_name[0]) - 65
            x = ord(loc_name[2]) - 49
            if y == 9 and x == 5:
                # don't show main computer in numbers
                continue
            assert (0 <= y < 16) and (0 <= x < 8), f"invalid index from location name {loc_name}"
            rooms[y][x] += 1
        # TODO: also add locations with locals lost from loading save state or reset
        self.ui_set_rooms(rooms)

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
                    logger.info(f"New Check: {loc_name} ({self.ap_local_count}/{n_locations})")
                    async_start(self.send_msgs([
                        {"cmd": "LocationChecks", "locations": [server_id]},
                    ]))
                else:
                    # This will happen a lot in Zillion,
                    # because all the key words are local and unwatched by the server.
                    logger.debug(f"DEBUG: {loc_name} not in missing")
            elif isinstance(event_from_game, events.DeathEventFromGame):
                async_start(self.send_death())
            elif isinstance(event_from_game, events.WinEventFromGame):
                if not self.finished_game:
                    async_start(self.send_msgs([
                        {"cmd": "LocationChecks", "locations": [loc_name_to_id["J-6 bottom far left"]]},
                        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL},
                    ]))
                    self.finished_game = True
            elif isinstance(event_from_game, events.DoorEventFromGame):
                if self.auth:
                    doors_b64 = base64.b64encode(event_from_game.doors).decode()
                    payload = {
                        "cmd": "Set",
                        "key": f"zillion-{self.auth}-doors",
                        "operations": [{"operation": "replace", "value": doors_b64}],
                    }
                    async_start(self.send_msgs([payload]))
            elif isinstance(event_from_game, events.MapEventFromGame):
                row = event_from_game.map_index // 8
                col = event_from_game.map_index % 8
                room_name = f"({chr(row + 64)}-{col + 1})"
                logger.info(f"You are at {room_name}")
            else:
                logger.warning(f"WARNING: unhandled event from game {event_from_game}")

    def process_items_received(self) -> None:
        if len(self.items_received) > self.next_item:
            zz_item_ids = [self.ap_id_to_zz_id[item.item] for item in self.items_received]
            for index in range(self.next_item, len(self.items_received)):
                ap_id = self.items_received[index].item
                from_name = self.player_names[self.items_received[index].player]
                # TODO: colors in this text, like sni client?
                logger.info(f"received {self.ap_id_to_name[ap_id]} from {from_name}")
            self.to_game.put_nowait(
                events.ItemEventToGame(zz_item_ids),
            )
            self.next_item = len(self.items_received)


def name_seed_from_ram(data: bytes) -> tuple[str, str]:
    """ returns player name, and end of seed string """
    if len(data) == 0:
        # no connection to game
        return "", "xxx"
    null_index = data.find(b"\x00")
    if null_index == -1:
        logger.warning(f"invalid game id in rom {repr(data)}")
        null_index = len(data)
    name = data[:null_index].decode()
    null_index_2 = data.find(b"\x00", null_index + 1)
    if null_index_2 == -1:
        null_index_2 = len(data)
    seed_name = data[null_index + 1:null_index_2].decode()

    return name, seed_name


async def zillion_sync_task(ctx: ZillionContext) -> None:
    logger.info("started zillion sync task")

    # to work around the Python bug where we can't check for RetroArch
    if not ctx.look_for_retroarch.is_set():
        logger.info("Start Zillion in RetroArch, then use the /sms command to connect to it.")
    await asyncio.wait((
        asyncio.create_task(ctx.look_for_retroarch.wait()),
        asyncio.create_task(ctx.exit_event.wait()),
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
            game_id = memory.get_rom_to_ram_data(ram)
            name, seed_end = name_seed_from_ram(game_id)
            if len(name):
                if name == ctx.known_name:
                    ctx.auth = name
                    # this is the name we know
                    if ctx.server and ctx.server.socket:  # type: ignore
                        if ctx.got_room_info.is_set():
                            if ctx.seed_name and ctx.seed_name.endswith(seed_end):
                                # correct seed
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
                                        async_start(ctx.send_connect())
                                        log_no_spam("logging in to server...")
                                        await asyncio.wait((
                                            asyncio.create_task(ctx.got_slot_data.wait()),
                                            asyncio.create_task(ctx.exit_event.wait()),
                                            asyncio.create_task(asyncio.sleep(6)),
                                        ), return_when=asyncio.FIRST_COMPLETED)  # to not spam connect packets
                            else:  # not correct seed name
                                log_no_spam("incorrect seed - did you mix up roms?")
                        else:  # no room info
                            # If we get here, it looks like `RoomInfo` packet got lost
                            log_no_spam("waiting for room info from server...")
                    else:  # server not connected
                        log_no_spam("waiting for server connection...")
                else:  # new game
                    log_no_spam("connected to new game")
                    await ctx.disconnect()
                    ctx.reset_server_state()
                    ctx.seed_name = None
                    ctx.got_room_info.clear()
                    ctx.reset_game_state()
                    memory.reset_game_state()

                    ctx.auth = name
                    ctx.known_name = name
                    async_start(ctx.connect())
                    await asyncio.wait((
                        asyncio.create_task(ctx.got_room_info.wait()),
                        asyncio.create_task(ctx.exit_event.wait()),
                        asyncio.create_task(asyncio.sleep(6)),
                    ), return_when=asyncio.FIRST_COMPLETED)
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
    parser.add_argument("diff_file", default="", type=str, nargs="?",
                        help="Path to a .apzl Archipelago Binary Patch file")
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


def launch() -> None:
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
