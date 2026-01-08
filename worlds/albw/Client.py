from typing import Dict, List, Optional, Set
import asyncio
import traceback
from BaseClasses import ItemClassification
from CommonClient import CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from Patch import create_rom_file
from .Citra import CitraInterface, CitraException
from .Locations import LocationData, LocationType, all_locations, location_table
from .Items import item_code_table
from . import albw_base_id

def bytes_or(a: bytes, b: bytes) -> bytes:
    return bytes([x | y for x,y in zip(a,b)])

class ALBWClientContext(CommonContext):
    game: Optional[str] = "A Link Between Worlds"
    items_handling: Optional[int] = 0b101 # receive remote items and starting inventory
    want_slot_data: bool = True

    citra: CitraInterface
    citra_connected: bool
    server_connected: bool
    slot_data: Optional[Dict[str, any]]
    save_ptr: int
    event_flags_ptr: int
    course_flags_ptr: int
    minigame_ptr: int
    event_flags: bytes
    course_flags: List[bytes]
    minigame_flags: int
    course: int
    stage: int
    ravio_scouted: bool
    to_hint: List[int]
    invalid: bool
    last_error: str
    show_citra_connect_message: bool

    DATA_VERSION: int = 2
    AP_HEADER_LOCATION: int = 0x6fe5f8
    SAVES_LOCATION: int = 0x711de8
    EVENTS_LOCATION: int = 0x70b728
    COURSES_LOCATION: int = 0x70c8e0
    MINIGAME_LOCATION: int = 0x70d858
    GAME_LOCATION: int = 0x709df8
    TASK_MAIN_GAME_VTABLE: int = 0x6d1db4

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.citra_connected = False
        self.server_connected = False
        self.slot_data = None
        self.course_flags = []
        self.ravio_scouted = False
        self.to_hint = []
        self.citra = CitraInterface()
        self.invalid = False
        self.last_error = ""
        self.show_citra_connect_message = True

    def run_gui(self) -> None:
        from kvui import GameManager

        class ALBWManager(GameManager):
            base_title: str = "Archipelago A Link Between Worlds Client"

        self.ui = ALBWManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    
    def error(self, error: str) -> None:
        if error != self.last_error:
            logger.error(error)
            self.last_error = error
        self.invalid = True
    
    async def citra_connect(self) -> None:
        if self.show_citra_connect_message:
            logger.info("Connecting to emulator...")
        self.show_citra_connect_message = False
        self.citra_connected = False
        if not self.citra.connect():
            await asyncio.sleep(1)
        else:
            self.citra_connected = True
            if self.server_connected:
                logger.info("Emulator connected")
            else:
                logger.info("Emulator connected, but not yet connected to the multiworld")
    
    def validate_rom(self) -> None:
        if self.citra.read(self.AP_HEADER_LOCATION, 4) != b"ARCH":
            self.error("The running game was not patched with an Archipelago patch.")
        elif self.citra.read_u32(self.AP_HEADER_LOCATION + 0x4) < self.DATA_VERSION:
            self.error("Version mismatch: update your albwrandomizer library and re-patch.")
        elif self.citra.read_u32(self.AP_HEADER_LOCATION + 0x4) > self.DATA_VERSION:
            self.error("Version mismatch: update your apworld and restart the client.")
        else:
            name = self.citra.read(self.AP_HEADER_LOCATION + 0x10, 0x40)
            end = name.find(0)
            if end != -1:
                name = name[:end]
            self.auth = name.decode("utf-8")
    
    def validate_save(self) -> None:
        self.save_ptr = 0
        all_saves_ptr = self.citra.read_u32(self.SAVES_LOCATION)
        if all_saves_ptr != 0:
            self.save_ptr = self.citra.read_u32(all_saves_ptr + 0x14)
        if all_saves_ptr == 0 or self.save_ptr == 0 or self.citra.read_u32(self.save_ptr + 0x1600) != 0:
            self.invalid = True
            self.last_error = ""
        elif self.citra.read(self.save_ptr + 0xde0, 4) == b"\0\0\0\0":
            self.error("The loaded save file is not an Archipelago save file. Choose a different save file.")
        elif self.citra.read(self.save_ptr + 0xde0, 4) != b"ARCH":
            self.invalid = True
            self.last_error = ""
        elif self.citra.read_u32(self.save_ptr + 0xde8) != self.citra.read_u32(self.AP_HEADER_LOCATION + 0x8):
            self.error("The loaded save file was created for a different multiworld. Choose a different save file.")

    def validate_seed(self) -> None:
        if not self.server_connected or not self.slot_data:
            self.invalid = True
        elif self.citra.read_u32(self.AP_HEADER_LOCATION + 0x8) != self.slot_data["seed"]:
            self.error("The patch was created for a different multiworld. Make sure you are using the right patch and connecting to the correct multiworld.")

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(ALBWClientContext, self).server_auth(password_requested)
        if not self.auth:
            logger.info("Connected to the multiworld, awaiting connection to emulator to authenticate with server")
        while not self.auth and not self.exit_event.is_set():
            await asyncio.sleep(1)
        await self.send_connect()
    
    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.server_connected = True

        if cmd == "LocationInfo":
            self.to_hint = [loc.location for loc in args["locations"]
                if loc.flags & (ItemClassification.progression | ItemClassification.useful)]
        
    def get_pointers(self) -> bool:
        self.event_flags_ptr = self.citra.read_u32(self.EVENTS_LOCATION)
        self.course_flags_ptr = self.citra.read_u32(self.COURSES_LOCATION)
        self.minigame_ptr = self.citra.read_u32(self.MINIGAME_LOCATION)
        if self.event_flags_ptr == 0 or self.course_flags_ptr == 0 or self.minigame_ptr == 0:
            return False
        return True

    def is_in_game(self) -> bool:
        framework = self.citra.read_u32(self.AP_HEADER_LOCATION + 0x54)
        if framework == 0:
            return False
        task_mgr = self.citra.read_u32(framework + 0x1c)
        start_node = task_mgr + 0x44
        node = self.citra.read_u32(start_node + 4)
        loop_count = 0
        while node != start_node and loop_count < 100:
            task = self.citra.read_u32(node + 8)
            task_vtable = self.citra.read_u32(task)
            if task_vtable == self.TASK_MAIN_GAME_VTABLE:
                return True
            node = self.citra.read_u32(node + 4)
            loop_count += 1
        return False

    def read_flags(self) -> None:
        cur_event_flags = self.citra.read(self.event_flags_ptr + 0x48, 0x80)
        save_event_flags = self.citra.read(self.save_ptr + 0x40, 0x80)
        self.event_flags = bytes_or(cur_event_flags, save_event_flags)

        cur_minigame_flags = self.citra.read(self.minigame_ptr + 0x35, 1)[0]
        save_minigame_flags = self.citra.read(self.save_ptr + 0xda5, 1)[0]
        self.minigame_flags = cur_minigame_flags | save_minigame_flags

        self.course_flags.clear()
        for course in range(0, 0x20):
            cur_course_flags = self.citra.read(self.course_flags_ptr + course * 0x16c + 0x160, 0x20) \
                             + self.citra.read(self.course_flags_ptr + course * 0x16c + 0x1a0, 0x10)
            save_course_flags = self.citra.read(self.save_ptr + 0x560 + course * 0x40, 0x40)
            self.course_flags.append(bytes_or(cur_course_flags, save_course_flags))

    def check_flag(self, course: Optional[int], flag: int) -> bool:
        byte = flag >> 3
        mask = 1 << (flag & 7)
        if course is None:
            return self.event_flags[byte] & mask != 0
        else:
            return self.course_flags[course][byte] & mask != 0

    def check_location(self, loc: LocationData):
        if loc.code is not None and loc.flag is not None:
            if self.check_flag(loc.course, loc.flag):
                return True
            if loc.course == 0 and loc.flag >= 0x100:
                if self.check_flag(2, loc.flag) or self.check_flag(4, loc.flag):
                    return True
            if loc.course == 1 and loc.flag >= 0x100:
                if self.check_flag(3, loc.flag) or self.check_flag(5, loc.flag):
                    return True
        if loc.name == "Hyrule Hotfoot 75s" and self.minigame_flags & 1 != 0:
            return True
        return False

    async def check_locations(self) -> None:
        checks = []
        self.read_flags()

        for loc in all_locations:
            if self.check_location(loc):
                code = loc.code + albw_base_id
                if code not in self.locations_checked:
                    self.locations_checked.add(code)
                    checks.append(code)

        if len(checks) > 0:
            await self.send_msgs([{
                "cmd": "LocationChecks",
                "locations": checks,
            }])

        if self.check_flag(None, 685):
            await self.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])

        if not self.ravio_scouted and self.check_location(location_table["Ravio's Gift"]):
            ravio_locations = [loc.code + albw_base_id for loc in all_locations if loc.loctype == LocationType.Ravio]
            await self.send_msgs([{
                "cmd": "LocationScouts",
                "create_as_hint": 0,
                "locations": ravio_locations,
            }])
            self.ravio_scouted = True

        if self.to_hint:
            await self.send_msgs([{
                "cmd": "LocationScouts",
                "create_as_hint": 2,
                "locations": self.to_hint,
            }])
            self.to_hint = []

    def get_item(self) -> None:
        received_items_count = self.citra.read_u32(self.AP_HEADER_LOCATION + 0x50)
        current_item = self.citra.read_u32(self.AP_HEADER_LOCATION + 0xc)
        if len(self.items_received) > received_items_count and current_item == 0xffffffff:
            item_code = self.items_received[received_items_count].item - albw_base_id
            item_id = item_code_table[item_code].progress[0].item_id()
            assert item_id is not None
            self.citra.write_u32(self.AP_HEADER_LOCATION + 0xc, item_id)
    
    def get_null_item(self) -> None:
        self.citra.write_u32(self.AP_HEADER_LOCATION + 0xc, 0xffffffff)

async def game_watcher(ctx: ALBWClientContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            ctx.invalid = False
            if not ctx.citra_connected:
                await ctx.citra_connect()
            if ctx.citra_connected:
                ctx.validate_rom()
                if not ctx.invalid:
                    ctx.validate_seed()
                if not ctx.invalid:
                    if ctx.is_in_game():
                        ctx.validate_save()
                        if not ctx.invalid and ctx.get_pointers() and ctx.server_connected:
                            await ctx.check_locations()
                            ctx.get_item()
                    else:
                        ctx.get_null_item()
        except CitraException as e:
            logger.error(e)
            ctx.citra_connected = False
            ctx.last_error = ""
            ctx.show_citra_connect_message = True
        except Exception as e:
            logger.error(e)
            await ctx.disconnect()
            ctx.citra_connected = False
            ctx.server_connected = False
            ctx.last_error = ""
            ctx.show_citra_connect_message = True
        await asyncio.sleep(0.25)

def launch() -> None:
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
        args = parser.parse_args()

        if args.patch_file != "":
            create_rom_file(args.patch_file)

        ctx = ALBWClientContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.error("".join(traceback.format_exception(e)))

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()