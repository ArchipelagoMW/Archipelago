
import time
import logging
from typing import TYPE_CHECKING, Set, Dict, Any

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from ..data.Constants import *
from ..data.DynamicEntrances import DYNAMIC_ENTRANCES_BY_SCENE
from ..Util import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from ..data.Entrances import PHTransition

logger = logging.getLogger("Client")
# Adding test edit

# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFFFFFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret


def item_count(ctx, item_name):
    return sum([1 for i in ctx.items_received if i.item == ITEMS_DATA[item_name]["id"]])


# Read list of address data
async def read_memory_values(ctx, read_list: dict[str, tuple[int, int, str]], signed=False) -> dict[str, int]:
    keys = read_list.keys()
    read_data = [(a, s, d) for a, s, d in read_list.values()]
    read_result = await bizhawk.read(ctx.bizhawk_ctx, read_data)
    values = [int.from_bytes(i, "little", signed=signed) for i in read_result]
    return {key: value for key, value in zip(keys, values)}


# Read single address
async def read_memory_value(ctx, address: int, size=1, domain="Main RAM", signed=False, silent=False) -> int:
    read_result = await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)])
    if not silent:
        print("Reading memory value", hex(address), size, domain, ", got value",
              hex(int.from_bytes(read_result[0], "little")))
    return int.from_bytes(read_result[0], "little", signed=signed)


# Write single address
async def write_memory_value(ctx, address: int, value: int, domain="Main RAM", incr=None, size=1, unset=False,
                             overwrite=False):
    prev = await read_memory_value(ctx, address, size, domain)
    if incr is not None:
        value = -value if unset else value
        if incr:
            write_value = prev + value
        else:
            write_value = prev - value
        write_value = 0 if write_value <= 0 else write_value
    else:
        if unset:
            print(f"Unseting bit {hex(address)} {hex(value)} with filter {hex(~value)} from prev {hex(prev)} "
                  f"for result {hex(prev & (~value))}")
            write_value = prev & (~value)
        elif not overwrite:
            write_value = prev | value
        else:
            write_value = value
    write_value = split_bits(write_value, size)
    print(f"Writing Memory: {hex(address)}, {write_value}, {size}, {domain}, {incr}, {unset}")
    await bizhawk.write(ctx.bizhawk_ctx, [(address, write_value, domain)])
    return write_value


# Write list of values starting from address
async def write_memory_values(ctx, address: int, values: list, domain="Main RAM", overwrite=False, size=4):
    if not overwrite:
        prev = await read_memory_value(ctx, address, len(values), domain)
        new_values = [old | new for old, new in zip(split_bits(prev, size), values)]
        print(f"\tvalues: {new_values}, old: {split_bits(prev, size)}")
    else:
        new_values = values
    await bizhawk.write(ctx.bizhawk_ctx, [(address, new_values, domain)])


# Get address from pointer
async def get_address_from_heap(ctx, pointer, offset=0) -> int:
    m_course = 0
    while m_course == 0:
        m_course = await read_memory_value(ctx, pointer, 4, domain="Data TCM")
    read = await read_memory_value(ctx, m_course - 0x02000000, 4)
    print(f"Got map address @ {hex(read + offset - 0x02000000)}")
    return read + offset - 0x02000000


class DSZeldaClient(BizHawkClient):
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    local_tracker: Dict[str, Any]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]
    location_area_to_watches: Dict[int, dict[str, dict]]
    watches: Dict[str, tuple[int, int, str]]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict()
        self.location_name_to_id = build_location_name_to_id_dict()
        self.location_area_to_watches = build_location_room_to_watches()
        self.scene_to_dynamic_flag = build_scene_to_dynamic_flag()
        self.hint_scene_to_watches = build_hint_scene_to_watches()
        self.entrance_id_to_entrance = build_entrance_id_to_data()

        self.starting_flags = None
        self.dungeon_key_data = None
        self.slot_id_addr = None
        self.received_item_index_addr = None
        self.starting_entrance = (11, 3, 5)  # stage, room, entrance
        self.scene_addr = (0, 0, 0, 0)  # Stage, room, floor, entrance
        self.exit_coords_addr = (0x1B2EC8, 0x1B2ECC, 0x1B2ED0)  # x, y, z. what coords to spawn link at when entering a
        # continuous transition
        self.er_y_offest = 164  # In ph i use coords who's y is 164 off the entrance y
        self.ADDR_gMapManager = 0xe60
        self.stage_flag_offset = 0x268
        self.entrances = {}
        self.hint_data = {}

        self.local_checked_locations = set()
        self.local_scouted_locations = set()
        self.local_tracker = {}

        self._set_deathlink = False  # Check for toggling death link setting
        self.last_deathlink = None
        self.was_alive_last_frame = False
        self.is_expecting_received_death = False
        self.is_dead = False  # Read from read_result

        self.save_slot = 0
        self.version_offset = 0

        self.last_scene = None
        self.locations_in_scene = {}
        self.watches = {}
        self.receiving_location = False
        self.last_vanilla_item: list[str | list[tuple[str, int]]] = []
        self.delay_reset = False
        self.getting_location = False

        self._previous_game_state = False  # Updated every successful cycle
        self._just_entered_game = False  # Set when disconnected or on menu, unset after one full cycle of fully loaded
        self._loaded_menu_read_list = False  #
        self._from_menu = True  # Last scene was menu
        self._dynamic_flags_to_reset = []

        self.main_read_list = {}
        self.read_result = {}
        self.current_stage = 0xB
        self.current_scene = None
        self.last_stage = None
        self.entering_from = None
        self.entering_dungeon = None
        self.current_entrance = None

        self.stage_address = 0  # Used for scene flags
        self.new_stage_loading = None

        self.getting_location_type = None

        self._entered_entrance = False
        self._loading_scene = False
        self._backup_coord_read = None
        self.prev_rupee_count = 0
        self._log_received_items = False

        self.warp_to_start_flag = False
        self.er_map: dict[int, dict["PHTransition", "PHTransition"]] = {}
        self.er_in_scene: dict["PHTransition", "PHTransition"] | None = None
        self.er_exit_coord_writes: list | None = None

        self.delay_pickup = None
        self.last_key_count = 0
        self.key_address = 0
        self.key_value = 0
        self.metal_count = 0

        self.last_dungeon_warp_target = None

        self.tried_short_cs = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            if not await self.check_game_version(ctx):
                logger.error("Invalid rom")
                return False
        except bizhawk.RequestFailedError:
            logger.error("Invalid rom")
            return False
        except UnicodeDecodeError:
            logger.error("You are using Bizhawk version 2.9.x, please use version 2.10.x")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5
        print(f"validation: {ctx.game}, {ctx.items_handling}")
        return True

    async def check_game_version(self, ctx: "BizHawkClientContext") -> bool:
        """
        DSZeldaClient calls validate rom, this is for detecting game version and setting game specific variables
        :param ctx:
        :return: valid rom
        """
        return False

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self._set_deathlink = True
                self.last_deathlink = time.time()
        super().on_package(ctx, cmd, args)

    def get_coord_address(self, at_sea=None, multi=False) -> dict[str, tuple[int, int, str]]:
        """
        get a dictionary for link/ship/boat coordinate read data of the current scene
        :param at_sea: guess this still exists, for switching between vehicular and human coords
        :param multi: for when you want to return all possible coord addresses. used as a backup load detector
        :return: dict of link_coord to write_data
        """
        pass

    async def get_coords(self, ctx, multi=False) -> dict:
        """
        organize the coords in a neat dictionary
        :param ctx:
        :param multi: gives all coords
        :return:
        """
        pass

    async def full_heal(self, ctx, bonus=0):
        """
        full heals the player. Called when getting heart containers, but can be called elsewhere too
        :param ctx:
        :param bonus:
        :return:
        """
        pass

    async def watched_intro_cs(self, ctx):
        """
        you know how it's random whether niko talks or not at the beginning?
        this tries to fix that. make it read a memory value or something
        :param ctx:
        :return:
        """
        return False

    async def scout_location(self, ctx: "BizHawkClientContext", locations):
        """
        sends a hint for the requested locations
        :param ctx:
        :param locations:
        :return:
        """
        local_scouted_locations = set(ctx.locations_scouted)
        for loc in locations:
            local_scouted_locations.add(LOCATIONS_DATA[loc]["id"])

        if self.local_scouted_locations != local_scouted_locations:
            self.local_scouted_locations = local_scouted_locations
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.local_scouted_locations),
                "create_as_hint": int(2)
            }])

    async def get_small_key_address(self, ctx) -> int:
        """
        in ph small keys are tied to map data, in st there is a consistent address for them
        :param ctx:
        :return:
        """
        return 0

    def process_loading_variable(self, read_result) -> bool:
        """
        Loading variable can vary whether it should be one or 0
        this should fix that
        :param read_result: dict of all the read data
        :return: is loading
        """
        return False

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None or ctx.slot == 0:
            self._just_entered_game = True
            self._loaded_menu_read_list = False
            self.last_scene = None
            self._from_menu = True
            self.er_in_scene = None
            ctx.watcher_timeout = 0.5
            return

        # Enable "DeathLink" tag if option was enabled
        if self._set_deathlink:
            self._set_deathlink = False
            await ctx.update_death_link(True)

        # Get main read list before entering loop
        if not self._loaded_menu_read_list:
            await self.update_main_read_list(ctx, self.current_stage, in_game=False)
            self._loaded_menu_read_list = True

        try:
            # Read main read list
            read_result = await read_memory_values(ctx, self.main_read_list)
            self.read_result = read_result

            in_game = read_result["game_state"]
            slot_memory = read_result["slot_id"]
            current_stage = read_result["stage"]
            self.current_stage = current_stage

            # Loading variables
            loading_scene = self.process_loading_variable(read_result)
            loading = loading_scene or self._entered_entrance

            # If player is on title screen, don't do anything else
            if not in_game or current_stage not in STAGES:
                self._previous_game_state = False
                self._from_menu = True
                ctx.watcher_timeout = 0.5
                print("NOT IN GAME")
                # Finished game?
                if not ctx.finished_game:
                    await self._process_game_completion(ctx)
                return

            # While game from main menu
            if in_game and not self._previous_game_state:
                if not await self.watched_intro_cs(ctx):
                    print("In Intro CS")
                    return
                self._just_entered_game = True
                self.last_stage = None
                self.last_scene = None

            # Single call just entered from menu methods
            if in_game and self._from_menu:
                self._generate_er_map(ctx)
                self._from_menu = False
                ctx.watcher_timeout = 0.1  # 9 frame interval to catch 11 frame ER windows (old)
                                           # 6 frame intervals to catch bounce timings
                await self.enter_game(ctx)
                print(f"Started Game")

            # getting_location can be overwritten in process_read_list
            self.getting_location = read_result.get("getting_location", None)
            self.is_dead = not read_result.get("link_health", 12)

            # Get current scene
            current_room = read_result.get("room", None)
            current_room = 0 if current_room == 0xFF and current_stage != 0x29 else current_room  # Resetting in a dungeon sets a special value
            current_room = 3 if current_room == 0xFF else current_room
            self.current_scene = current_scene = current_stage * 0x100 + current_room
            current_entrance = read_result.get("entrance", 0)
            num_received_items = read_result.get("received_item_index", None)


            await self.process_read_list(ctx, read_result)

            # Process on new room. As soon as it's triggered, changing the scene variable changes entrance destination
            if current_scene != self.last_scene and not self._entered_entrance and not self._loading_scene:
                # Trigger a different entrance to vanilla
                current_stage, current_room, current_entrance = await self._entrance_warp(ctx, current_scene, current_entrance)
                current_scene = current_stage * 0x100 + current_room
                self.current_entrance = current_entrance

                # Backup in case of missing loading
                self._backup_coord_read = await self.get_coords(ctx, multi=True)

                # Send data to tracker
                await self.ut_bounce_scene(ctx, current_stage, current_room, current_entrance)

                # Set dynamic flags on scene
                await self._reset_dynamic_flags(ctx)
                await self._set_dynamic_flags(ctx, current_scene)



                self._entered_entrance = time.time()  # Triggered first part of loading - setting new room
                self.entering_dungeon = None
                if self.delay_reset:
                    self.delay_reset = 0
                    await self._remove_vanilla_item(ctx, num_received_items)

            # Nothing happens while loading
            if ctx.server is not None and not loading and not self._loading_scene and not self._entered_entrance:

                # If new file, set up starting flags
                if slot_memory == 0:
                    if await self.watched_intro_cs(ctx):  # Check if watched intro cs
                        await self._set_starting_flags(ctx)

                # Read for checks on specific global flags
                if len(self.watches) > 0:
                    watch_result = await read_memory_values(ctx, self.watches)
                    for loc_name, prev_value in watch_result.items():
                        loc_data = LOCATIONS_DATA[loc_name]
                        if prev_value & loc_data["value"]:
                            print(f"Got read item {loc_name} from address {loc_data['address']} "
                                  f"looking at bit {loc_data['value']}")

                            force_remove = False
                            await self._process_checked_locations(ctx, loc_name, force_remove)
                            self.receiving_location = True
                            self.watches.pop(loc_name)

                # Check if link is getting location
                if self.getting_location and not self.receiving_location and self.locations_in_scene is not None:
                    self.receiving_location = True
                    print("Receiving Item")
                    if self.delay_reset > 1:
                        self.delay_reset = 0
                    await self._process_checked_locations(ctx, None, detection_type=self.getting_location_type)

                # Process received items
                if num_received_items is not None and num_received_items < len(ctx.items_received):
                    if self._just_entered_game:
                        self._log_received_items = True
                    await self._process_received_items(ctx, num_received_items, self._log_received_items)
                else:
                    self._log_received_items = False

                if num_received_items > len(ctx.items_received):
                    await write_memory_value(ctx, self.received_item_index_addr, len(ctx.items_received), size=2, overwrite=True)
                    logger.info(f"Save file has more items than Multiworld. Probable cause: loaded wrong save file. \n"
                                f"Reset item count to Multiworld's. If this is the wrong save file, you can safely quit without saving.")

                # Exit location received cs
                if self.receiving_location and not self.getting_location:
                    self.receiving_location = False

                    # Increment delay reset, probably haven't received item yet
                    if self.delay_reset == 1:
                        self.delay_reset += 1
                        print(f"Delay Reset still active, {self.delay_reset}")

                    # Check for delayed pickup first!
                    elif self.delay_pickup is not None:
                        print(f"Delay pickup {self.delay_pickup}")
                        fallback, pickups = self.delay_pickup
                        need_fallback = True
                        for location, item, value in pickups:
                            new_item_read = await self.get_item_read(ctx, item)
                            if "Rupee" in item:
                                if new_item_read - value == ITEMS_DATA[item]["value"]:
                                    await self._process_checked_locations(ctx, location, True, item=item)
                                    need_fallback = False
                            elif new_item_read != value:
                                await self._process_checked_locations(ctx, location, True, item=item)
                                need_fallback = False

                        if need_fallback:
                            vanilla_item = LOCATIONS_DATA[fallback]["vanilla_item"]
                            await self._process_checked_locations(ctx, fallback, True, item=vanilla_item)

                        self.delay_pickup = None
                        self.last_key_count = 0

                    # Remove vanilla item
                    elif self.last_vanilla_item:
                        print("Item Received Successfully")
                        await self._remove_vanilla_item(ctx, num_received_items)


                await self.detect_warp_to_start(ctx, read_result)
                await self.process_in_game(ctx, read_result)

                self._just_entered_game = False

                # Finished game?
                if not ctx.finished_game:
                    await self._process_game_completion(ctx)

                # Process Deathlink
                if "DeathLink" in ctx.tags:
                    await self.process_deathlink(ctx, self.is_dead, self.current_stage, read_result)

            # Started actual scene loading
            if self._entered_entrance and loading_scene:
                self._loading_scene = True  # Second phase of loading room
                self._entered_entrance = False
                await self._set_er_coords(ctx)
                print("Loading Scene", current_scene)

            # Fully loaded room
            if self._loading_scene and not loading:
                print("Fully Loaded Room", current_scene)
                self._loading_scene = False
                self._backup_coord_read = None

                # Load potential entrance warp destinations, and dynamic entrances
                self.er_in_scene = self.er_map.get(current_scene, dict())
                await self._set_dynamic_entrances(ctx, current_scene)

                print(f"Entered new scene {hex(current_scene)} with ER:")
                for i, v in self.er_in_scene.items():
                    print(f"\t{i} => {v} {i.exit}")

                await self.process_on_room_load(ctx, current_scene, read_result)
                await self._load_local_locations(ctx, current_scene)
                await self._process_scouted_locations(ctx, current_scene)

                # Check if entering dungeon
                if current_stage in self.dungeon_key_data and self.last_stage != current_stage:
                    self.entering_dungeon = current_stage
                    self.entering_from = self.last_scene
                else:
                    self.entering_from = current_scene  # stage and room

                # Run entering stage code
                if self.last_stage != current_stage:
                    print("Fully Loaded Stage")
                    await self._enter_stage(ctx, current_stage, current_scene)
                    await self.update_main_read_list(ctx, current_stage)

                # Hard coded room stuff
                await self.process_hard_coded_rooms(ctx, current_scene)

                self.last_stage = current_stage
                self.last_scene = current_scene
                print(f"Updated last scene!")

            self._previous_game_state = in_game

            # In case of a short load being missed, have a backup check on coords (they stay the same during transitions)
            if self._entered_entrance and self._backup_coord_read:
                if time.time() - self._entered_entrance > 1:
                    if not loading_scene:
                        self._loading_scene = True  # Second phase of loading room
                        self._entered_entrance = False
                        print("Missed loading read, using backup")

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

    async def update_main_read_list(self, ctx: "BizHawkClientContext", stage: int, in_game=True):
        """
        called with in_game=False when connecting for the first time,
        and then called with in_game=True on entering a new stage.
        decide what addresses to read each client cycle. needs to set self.main_read_list
        :param ctx:
        :param stage: useful to read different flags when in vehicle
        :param in_game: for setting flags to read before in game, to be able to detect when in game
        :return:
        """
        pass

    def _generate_er_map(self, ctx):
        # Creates a map from scene to dict of entrance dataclass to exit dataclass
        if ctx.slot_data.get("er_pairings", None):
            res = {}
            pairings = {int(k): v for k, v in ctx.slot_data["er_pairings"].items()}

            # Loop through entrance data, format data
            for data in self.entrances.values():

                # Figure pair from generation
                if data.id in pairings:
                    exit_id = pairings[data.id]
                    exit_data = self.entrance_id_to_entrance[exit_id]

                    # Create map from scene to entrance dataclass
                    res.setdefault(data.scene, {})
                    res[data.scene][data] = exit_data
                    print(f"Creating scene data {hex(data.scene)}: {data} => {exit_data}")
                    res = self.add_special_er_data(ctx, res, data.scene, data, exit_data)

            self.er_map = res
            print(f"ER Map:")
            for scene, data in self.er_map.items():
                print(f"\t{hex(scene)}")
                for d2, d3 in data.items():
                    print(f"\t\t{d2} => {d3}")



    def add_special_er_data(self, ctx, er_map, scene, detect_data, exit_data):
        """
        for adding special bonus data to ER dictionary.
        Used in ph for making sure Isle of Ruins entrances work no matter the water level.
        :param ctx:
        :param er_map:
        :param scene:
        :param detect_data:
        :param exit_data:
        :return:
        """
        return er_map

    async def enter_game(self, ctx):
        """
        called once on entering game from menu
        :param ctx:
        :return:
        """
        pass

    async def _set_starting_flags(self, ctx: "BizHawkClientContext") -> None:
        write_list = [(self.slot_id_addr, split_bits(ctx.slot, 2), "Main RAM")]
        print(f"New game, setting starting flags for slot {ctx.slot}")
        for adr, *value in STARTING_FLAGS:
            write_list.append((adr, value, "Main RAM"))

        write_list += await self.set_special_starting_flags(ctx)
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def set_special_starting_flags(self, ctx: "BizHawkClientContext") -> list[tuple[int, list, str]]:
        """
         gets called on entering a new save file. flags defined in `self.starting_flags` are set automatically. intended
         to be used for conditional flags.
         :param ctx:
         :return: write_list
         """
        write_list = []
        return write_list

    async def process_read_list(self, ctx: "BizHawkClientContext", read_result: dict):
        """
        called every cycle in game, even while loading
        Game watcher just read self.main_read_list. process data to set up key variables
        :param ctx: BizHawkClientContext
        :param read_result: dict of address name to read value
        :return:
        """

    async def _entrance_warp(self, ctx, going_to, entrance=0):
        e_write_list = []
        res = ((going_to & 0xFF00) >> 8, going_to & 0xFF, entrance)
        defer_entrance = False

        def write_entrance(s, r, e):
            return [(self.scene_addr[0], split_bits(s, 4), "Main RAM"),
                    (self.scene_addr[1], split_bits(r, 1), "Main RAM"),
                    (self.scene_addr[2], split_bits(0, 4), "Main RAM"),
                    (self.scene_addr[3], split_bits(e, 1), "Main RAM")]

        def write_er(exit_d: "PHTransition"):
            if exit_d.entrance[2] == 0xFA:
                # Special condition for exiting ships at sea
                new_entrance = tuple(list(exit_d.entrance[:2]) + [exit_d.extra_data["ship_exit"]])
                write_res = write_entrance(*new_entrance)
            else:
                write_res = write_entrance(*exit_d.entrance)

            if exit_d.entrance[2] > 0xFA:
                x, y, z = exit_d.coords
                print(f"exit coords {x} {y} {z}")
                self.er_exit_coord_writes = [(self.exit_coords_addr[0], split_bits(x, 4), "Main RAM"),
                                             (self.exit_coords_addr[1], split_bits(y, 4), "Main RAM"),
                                             (self.exit_coords_addr[2], split_bits(z, 4), "Main RAM")]

            write_res += self.write_respawn_entrance(exit_d)

            return write_res

        def post_process(d):
            new_entrance = d.entrance
            # Ship exits are weird
            if new_entrance[2] == 0xFA:
                new_entrance = tuple(list(new_entrance[:2]) + [d.extra_data["ship_exit"]])
            d.debug_print()
            return write_er(d), new_entrance

        # Warp to start
        if self.warp_to_start_flag:
            self.warp_to_start_flag = False
            home = self.starting_entrance[0]*0x100 + self.starting_entrance[1]
            if home != self.last_scene:
                e_write_list += write_entrance(*self.starting_entrance)
                res = self.starting_entrance
                self.current_stage = self.starting_entrance[0]
                logger.info("Warping to Start")
            else:
                logger.info("Warp to start failed, warping from home scene")

        elif self.er_in_scene:

            # Determine Entrance Warp
            coords = await self.get_coords(ctx)
            for detect_data, exit_data in self.er_in_scene.items():
                print(f"trying to detect ER {res} {detect_data.entrance} {detect_data.detect_exit(going_to, entrance, coords, self.er_y_offest)}")
                if detect_data.detect_exit(going_to, entrance, coords, self.er_y_offest):
                    if await self.conditional_er(ctx, exit_data):
                        print(f"Detected entrance: {detect_data} => {exit_data}")
                        e_write_list, res = post_process(exit_data)
                        defer_entrance = True
                    else:
                        e_write_list, res = post_process(detect_data)
                    break

        # Unrandomized entrances can still have bounce conditions
        if not e_write_list:
            bounce_entrance = await self.conditional_bounce(ctx, going_to, entrance)
            print(f"Trying bounce: {bounce_entrance}")
            if bounce_entrance:
                e_write_list, res = post_process(bounce_entrance)


        if e_write_list:
            print(f"Writing entrance warp {e_write_list}")
            await bizhawk.write(ctx.bizhawk_ctx, e_write_list)
        if defer_entrance:
            await self.store_visited_entrances(ctx, detect_data, exit_data)

        return res

    def write_respawn_entrance(self, exit_data):
        """
        when at sea in ph with island shuffle on, the respawn point is not tied to the exit and must be set manually.
        :param exit_data:
        :return: list of write data
        """
        return []

    async def conditional_bounce(self, cxt, scene, entrance) -> "PhantomHourglassEntrance" or None:
        """
        checks for bounce conditions if entrance is not affected by ER.
        returns the entrance to return to
        :param cxt:
        :param scene:
        :param entrance:
        :return:
        """

    async def store_visited_entrances(self, ctx, detect_data, exit_data):
        """
        store visited entrances as a set of ints to datastorage
        :param ctx:
        :param detect_data:
        :param exit_data:
        :return:
        """

    async def conditional_er(self, ctx, conditions) -> bool:
        """
        for handling custom conditional ER statements.
        If return false, ER will pop you back out the entrance you came from
        :param ctx:
        :param conditions:
        :return:
        """
        return True

    async def _reset_dynamic_flags(self, ctx):
        print(f"resetting flags {self._dynamic_flags_to_reset}")
        reset_data = [DYNAMIC_FLAGS[n] for n in self._dynamic_flags_to_reset]
        res = await self._process_dynamic_flags(ctx, reset_data)
        self._dynamic_flags_to_reset.clear()
        return res

    async def _set_dynamic_flags(self, ctx, scene):
        # Loop dynamic flags in scene
        if scene in self.scene_to_dynamic_flag:
            print(f"Flags on Scene: {[i['name'] for i in self.scene_to_dynamic_flag[scene]]}")
            return await self._process_dynamic_flags(ctx, self.scene_to_dynamic_flag[scene], True)
        return []
    # Main Loop

    async def _process_dynamic_flags(self, ctx, flag_list, reset=False):
        read_addr = set()
        set_bits, unset_bits = {}, {}
        for data in flag_list:

            # Items, locations, slot data
            if not await self._has_dynamic_requirements(ctx, data):
                continue

            # Create read/write lists
            for a, v in data.get("set_if_true", []):
                read_addr.add(a)
                # You can add an item name as a value, and it will set the value to it's count
                if type(v) is str:
                    v = item_count(ctx, v)
                set_bits[a] = set_bits.get(a, 0) | v
                print(f"\tsetting bit for {data['name']}")
            for a, v in data.get("unset_if_true", []):
                read_addr.add(a)
                unset_bits[a] = unset_bits.get(a, 0) | v
                print(f"\tunsetting bit for {data['name']}")
            for a, v in data.get("overwrite_if_true", []):
                read_addr.add(a)
                if type(v) is str:
                    v = item_count(ctx, v)
                set_bits[a] = v
                unset_bits[a] = ~v
                print(f"\toverwriting bit for {data['name']}")

            # Special full heal condition
            if "full_heal" in data:
                await self.full_heal(ctx)

            # Create list of flags to reset
            if reset:
                self._dynamic_flags_to_reset += data.get("reset_flags", [])

        # Write dynamic flags to memory
        read_list = {a: (a, 1, "Main RAM") for a in read_addr}
        prev = await read_memory_values(ctx, read_list)
        print(f"prevs: {[[hex(int(a)), hex(v)] for a, v in prev.items()]}")

        # Calculate values to write
        for a, v in set_bits.items():
            prev[a] = prev[a] | v
        for a, v in unset_bits.items():
            prev[a] = prev[a] & (~v)

        # Write
        write_list = [(int(a), [v], "Main RAM") for a, v in prev.items()]
        print(f"Dynaflags writes: {[[hex(a), [hex(i) for i in v]] for a, v, _ in write_list]}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        return write_list

    async def _set_dynamic_entrances(self, ctx, scene):
        print(f"Setting dynamic Entrances on {hex(scene)}:")
        for data in DYNAMIC_ENTRANCES_BY_SCENE.get(scene, dict()).values():

            # Check requirements
            if not await self._has_dynamic_requirements(ctx, data):
                continue

            # Overwrite er_in_scene with dynamic entrance
            detect_data = data["detect_data"]
            if data["exit_data"] is None:
                if data["destination"] == "_connected_dungeon_entrance":
                    self.er_in_scene[detect_data] = self.update_boss_warp(ctx, self.current_stage, scene)
            else:
                self.er_in_scene[detect_data] = data["exit_data"]
            print(f"\t{detect_data} => {data['exit_data']}")

    async def _has_dynamic_requirements(self, ctx, data) -> bool:
        def check_items(d):
            if "has_items" in d:
                counter = [0] * len(d["has_items"])
                label = "has_items"
            elif "not_has_all_items" in d:
                counter = [0] * len(d["not_has_all_items"])
                label = "not_has_all_items"
            else:
                return True

            for has_item in ctx.items_received:
                for i, want_item in enumerate(d[label]):
                    if has_item.item == ITEMS_DATA[want_item[0]]["id"]:
                        counter[i] += 1

            for item, count_have in zip(d.get("has_items", []), counter):
                item, count_want, *operation = item
                if not operation:
                    if (count_want == 0 and count_have != 0) or (count_want > 0 and count_have < count_want):
                        return False
                elif operation[0] == "has_exact":
                    if count_want != count_have:
                        return False
                elif operation[0] == "not_has":
                    if count_have >= count_want:
                        return False

            not_have_counter = 0
            for item, count_have in zip(d.get("not_has_all_items", []), counter):
                item, count_want, *operation = item
                if count_have > count_want:
                    not_have_counter += 1
                if not_have_counter == len(counter):
                    return False

            return True

        # Check location conditions
        def check_locations(d):
            for loc in d.get("has_locations", []):
                if self.location_name_to_id[loc] not in ctx.checked_locations:
                    return False
            for loc in d.get("not_has_locations", []):
                if self.location_name_to_id[loc] in ctx.checked_locations:
                    return False
            if "any_not_has_locations" in d:
                for loc in d.get("any_not_has_locations", []):
                    if self.location_name_to_id[loc] not in ctx.checked_locations:
                        return True
                return False
            if "any_has_locations" in d:
                for loc in d.get("any_has_locations", []):
                    if self.location_name_to_id[loc] in ctx.checked_locations:
                        return True
                return False
            return True

        def check_slot_data(d):
            if "has_slot_data" in d:
                for slot, value in d["has_slot_data"]:
                    if type(value) is list:
                        if ctx.slot_data.get(slot, None) not in value:
                            return False
                    else:
                        if ctx.slot_data.get(slot, None) != value:
                            return False
            return True

        # Came from particular location
        def check_last_room(d):
            # print(f"checking last scene {self.last_scene} {d.get('last_scenes', [])}")
            for i in d.get("not_last_scenes", []):
                if self.last_scene == i:
                    return False
            for i in d.get("last_scenes", []):
                if self.last_scene != i:
                    return False
            return True

        # Read a dict of addresses to see if they match value
        async def check_bits(d):
            if "check_bits" in d:
                r_list = {addr: (addr, 1, "Main RAM") for addr, _, *args in d["check_bits"]}
                v_lookup = {addr: v for addr, v, *args in d["check_bits"]}
                arg_lookup = {addr: args for addr, v, *args in d["check_bits"] if args}
                values = await read_memory_values(ctx, r_list)
                for addr, p in values.items():
                    if not arg_lookup.get(addr, False):
                        if not (p & v_lookup[addr]):
                            return False
                    elif "not" in arg_lookup[addr]:
                        if p & v_lookup[addr]:
                            return False
            return True

        def has_entrance(d):
            if "not_on_entrance" in d:
                if self.current_entrance in d["not_on_entrance"]:
                    return False
            if "on_entrance" in d:
                if self.current_entrance not in d["on_entrance"]:
                    return False
            return True

        if not check_items(data):
            print(f"\t{data['name']} does not have item reqs")
            return False
        if not check_locations(data):
            print(f"\t{data['name']} does not have location reqs")
            return False
        if not check_slot_data(data):
            print(f"\t{data['name']} does not have slot data reqs")
            return False
        if not check_last_room(data):
            print(f"\t{data['name']} came from wrong room {hex(self.last_scene)}")
            return False
        if not await check_bits(data):
            print(f"\t{data['name']} is missing bits")
            return False
        if not await self.has_special_dynamic_requirements(ctx, data):
            return False
        if not has_entrance(data):
            return False

        return True

    async def has_special_dynamic_requirements(self, ctx, data) -> bool:
        """
        for adding game specific dynamic parameters
        ph uses this for beedle points and metal counters
        :param ctx:
        :param data:
        :return:
        """
        return True

    async def _process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None, r=False,
                                        detection_type=None, item: str | None = None):
        local_checked_locations = set()
        all_checked_locations = ctx.checked_locations
        location = None

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            self.receiving_location = True
            loc_id = self.location_name_to_id[pre_process]
            location = LOCATIONS_DATA[pre_process]
            if r or (loc_id not in all_checked_locations):
                await self._set_vanilla_item(ctx, location, item)
                local_checked_locations.add(loc_id)
            print(f"pre-processed {pre_process}, vanill {self.last_vanilla_item}")
        else:
            # Get link's coords
            link_coords = await self.get_coords(ctx)

            # Certain checks use their detection method to differentiate them, like frogs and salvage
            locations_in_scene = self.locations_in_scene.copy()

            # Figure out what check was just gotten
            for i, loc in enumerate(locations_in_scene.items()):
                loc_name, location = loc
                loc_bytes = self.location_name_to_id[loc_name]

                if "address" in location or self.cancel_location_read(location):
                    continue

                print(f"Processing locs {loc_name}")
                print(
                    f"\t{location.get('x_max', 0x8FFFFFFF)} > {link_coords['x']} > {location.get('x_min', -0x8FFFFFFF)}")
                print(
                    f"\t{location.get('z_max', 0x8FFFFFFF)} > {link_coords['z']} > {location.get('z_min', -0x8FFFFFFF)}")

                if (location.get("x_max", 0x8FFFFFFF) > link_coords["x"] > location.get("x_min", -0x8FFFFFFF) and
                        location.get("z_max", 0x8FFFFFFF) > link_coords["z"] > location.get("z_min", -0x8FFFFFFF) and
                        location.get("y", link_coords["y"]) == link_coords["y"]):
                    # For rooms with checks that move or are close, check what you got first
                    if "delay_pickup" in location:
                        if len(self.locations_in_scene) > i + 1:
                            await self._set_delay_pickup(ctx, loc_name, location)
                            break

                    local_checked_locations.add(loc_bytes)
                    await self._set_vanilla_item(ctx, location)
                    print(f"Got location {loc_name}! with vanilla {self.last_vanilla_item} id {loc_bytes}")
                    self.locations_in_scene.pop(loc_name)  # Remove location for overlapping purposes
                    break
                location = None

        if location is not None:
            if "set_bit" in location:
                for addr, bit in location["set_bit"]:
                    print(f"Setting bit {bit} for location vanil {location['vanilla_item']}")
                    await write_memory_value(ctx, addr, bit)

            # Delay reset of vanilla item from certain address reads
            if "delay_reset" in location:
                self.delay_reset = 1
                print(f"Started Delay Reset for {self.last_vanilla_item}")

        # Send locations
        # print(f"Local locations: {local_checked_locations} in \n{all_checked_locations}")
        if any([i not in all_checked_locations for i in local_checked_locations]):
            print(f"Sending Locations: {local_checked_locations}")
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(local_checked_locations)
            }])

        await self.check_location_post_processing(ctx, location)

    def cancel_location_read(self, location) -> bool:
        """
        called on the main path of _process_checked_location.
        used to cancel special reads that should only happen on special reads
        used in st for stamp book locations
        :param location:
        :return:
        """
        return False

    async def get_item_read(self, ctx, item_name: str) -> int:
        if "Small Key" in item_name:
            return await read_memory_value(ctx, self.key_address)
        else:
            item = ITEMS_DATA[item_name]
            return await read_memory_value(ctx, item["address"], item.get("size", 1))

    async def _set_delay_pickup(self, ctx, loc_name, location):
        delay_locations = []
        delay_pickup = location["delay_pickup"]
        if type(delay_pickup) is str:
            delay_locations.append(delay_pickup)
        elif type(delay_pickup) is list:
            delay_locations += delay_pickup

        self.delay_pickup = [loc_name, []]
        for loc in delay_locations:
            delay_item_check: str | list[str] = LOCATIONS_DATA[loc]["vanilla_item"]
            if isinstance(delay_item_check, str):
                delay_item_check = [delay_item_check]
            for item in delay_item_check:
                self.delay_pickup[1].append([loc, item, await self.get_item_read(ctx, item)])
        print(f"Delay pickup {self.delay_pickup}")
    # Processes events defined in data\dynamic_flags.py

    async def _set_vanilla_item(self, ctx, location, vanilla_item: str | None = None):
        item: str | list[str] = vanilla_item or location["vanilla_item"]
        if isinstance(item, str):
            item_data = ITEMS_DATA[item]
            print(f"Setting vanilla for {item} {item_data}")
            if item is not None and not item_data.get("dummy", False):
                if ("incremental" in item_data or "progressive" in item_data or
                        item_data["id"] not in [i.item for i in ctx.items_received] or
                        "always_process" in item_data):
                    self.last_vanilla_item.append(item)

                    await self.unset_special_vanilla_items(ctx, location, item)

        # If there are multiple items possible at this location, store all of them with current counts for later
        else:
            self.last_vanilla_item.append([(_item, await self.get_item_read(ctx, _item)) for _item in item])

    async def unset_special_vanilla_items(self, ctx, location, item):
        """
        called after _set_vanilla_item if it was successful.
        self.last_vanilla_item.pop() any item/location combinations you don't want to remove
        used for farmable rupee spots, or overlap between progressive and non progressive variants of the same item
        :param ctx:
        :param location:
        :param item:
        :return:
        """
        pass

    async def check_location_post_processing(self, ctx, location: dict):
        """
        for running code on specific locations
        in st, this is used for sending goal on location
        :param ctx:
        :param location:
        :return:
        """
        return

    async def _process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int, log_items=False) -> None:
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        next_item = ctx.items_received[num_received_items].item
        item_name = self.item_id_to_name[next_item]
        item_data = ITEMS_DATA[item_name]
        item_value = 0

        if log_items:
            logger.info(f"Received Backlogged Item: {item_name}")

        # Increment in-game items received count
        received_item_address = self.received_item_index_addr
        write_list = [(received_item_address, split_bits(num_received_items + 1, 2), "Main RAM")]
        print(f"Vanilla item: {self.last_vanilla_item} for {item_name}")

        # If same as vanilla item don't remove
        if self.last_vanilla_item and item_name == self.last_vanilla_item[-1] and "always_process" not in item_data:
            self.last_vanilla_item.pop()
            print(f"oops it's vanilla or dummy! {self.last_vanilla_item}")
            write_list += await self.write_totok_keys_lol(ctx, item_name, item_data)

        # Handle Small Keys
        elif "Small Key" in item_name:

            async def write_keys_to_storage(dungeon) -> tuple[int, list, str]:
                key_data = DUNGEON_KEY_DATA[dungeon]
                prev = await read_memory_value(ctx, key_data["address"])
                bit_filter = key_data["filter"]
                new_v = prev | bit_filter if (prev & bit_filter) + key_data[
                    "value"] > bit_filter else prev + key_data["value"]
                print(f"Writing {key_data['name']} key to storage: {hex(prev)} -> {hex(new_v)}")
                return key_data["address"], [new_v], "Main RAM"

            # Get key in own dungeon
            if self.current_stage == item_data["dungeon"]:
                print("In dungeon! Getting Key")
                self.key_value = await read_memory_value(ctx, self.key_address)
                self.key_value = 7 if self.key_value > 7 else self.key_value
                write_list.append((self.key_address, [self.key_value + 1], "Main RAM"))
                write_list += await self.receive_key_in_own_dungeon(ctx, item_name, write_keys_to_storage)

            # Get key elsewhere
            else:
                write_list.append(await write_keys_to_storage(item_data["dungeon"]))

            # Extra key operations, in ph writing totok midway keys
            write_list += await self.received_special_small_keys(ctx, item_name, write_keys_to_storage)

        # Handle ammo refills
        elif "refill" in item_data:
            refill_id = ITEMS_DATA[item_data["refill"]]["id"]
            prog_received = min(sum([1 for i in ctx.items_received[:num_received_items] if i.item == refill_id]),
                                len(item_data["give_ammo"])) - 1
            if prog_received >= 0:
                write_list.append((item_data["address"], [item_data["give_ammo"][prog_received]], "Main RAM"))

        elif "address" in item_data or "progressive" in item_data:
            # Handle progressive items (not to be confused with progression items)
            prog_received = 0
            if "progressive" in item_data:
                prog_received = min(sum([1 for i in ctx.items_received[:num_received_items] if i.item == next_item]),
                                    len(item_data["progressive"]) - 1)
                item_address, item_value = item_data["progressive"][prog_received]
            else:
                item_address = item_data["address"]

            # Read address item is to be written to
            prev_value = await read_memory_value(ctx, item_address, domain="Main RAM",
                                                 size=item_data.get("size", 1))

            # Handle different writing operations
            if "incremental" in item_data:
                if type(item_data.get("value", 1)) is str:
                    value = await self.received_special_incremental(ctx, item_data)
                else:
                    value = item_data.get("value", 1)

                    # Heal on heart container
                    if item_name == "Heart Container":
                        await self.full_heal(ctx)

                item_value = prev_value + value
                item_value = 0 if item_value <= 0 else item_value
                if "Rupee" in item_name:
                    item_value = min(item_value, 9999)
                if "size" in item_data:
                    item_value = split_bits(item_value, item_data["size"])
                if "max" in item_data:
                    item_value = min(item_data["max"], item_value)
            elif "progressive" in item_data:
                if "progressive_overwrite" in item_data and prog_received >= 1:
                    item_value = item_value  # Bomb upgrades need to overwrite of everything breaks
                else:
                    item_value = prev_value | item_value
            else:
                item_value = prev_value | item_data["value"]

            item_values = item_value if type(item_value) is list else [item_value]
            item_values = [min(255, i) for i in item_values]
            write_list.append((item_address, item_values, "Main RAM"))

            # Handle special item conditions
            if "give_ammo" in item_data:
                write_list.append((item_data["ammo_address"], [item_data["give_ammo"][prog_received]], "Main RAM"))
            if "set_bit" in item_data:
                for adr, bit in item_data["set_bit"]:
                    bit_prev = await read_memory_value(ctx, adr)
                    write_list.append((adr, [bit | bit_prev], "Main RAM"))

        # Special game-specific items
        write_list += await self.receive_special_items(ctx, item_name, item_data)

        # Write the new item to memory!
        print("Write list:")
        for addr, value, domain in write_list:
            print(f"  {hex(addr)}: {value} ({domain})")
        # print(f"Write list: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

        await self.receive_item_post_processing(ctx, item_name, item_data)
    # Called when a stage has fully loaded

    async def receive_key_in_own_dungeon(self, ctx, item_name: str, write_keys_to_storage) -> list:
        """
        called in `_process_received_items` if you receive a key in it's own dungeon.
        for giving the player the key directly
        :param ctx:
        :param item_name:
        :param write_keys_to_storage: inner function that writes keys to storage based on key data
        :return: write data
        """
        return []

    async def write_totok_keys_lol(self, ctx, item_name, item_data) -> list:
        """
        if you get a key in TotOK, even in vanilla location, write to storage so that you get it again later
        :param ctx:
        :param item_name:
        :param item_data:
        :return: write data
        """
        return []

    async def received_special_small_keys(self, ctx, item_name, write_keys_to_storage) -> list:
        """
        called in `_process_received_items` if you got a small key. for doing special key stuff.
        in ph, this is used for saving giving midway keys
        :param ctx:
        :param item_name:
        :param write_keys_to_storage: inner function that writes keys to storage based on key data
        :return: write data
        """
        return []

    async def received_special_incremental(self, ctx, item_data) -> int:
        """
        processes incremental item values that are strings for special data, ofter defined by slot data
        :param ctx:
        :param item_data: item data
        :return: value to increment by
        """
        return 0
    # Called when checking location!

    async def receive_special_items(self, ctx, item_name, item_data) -> list[tuple[int, list, str]]:
        """
        called in `_process_received_items` for adding custom item cases
        :param ctx:
        :param item_name:
        :param item_data:
        :return: write list
        """
        return []

    async def receive_item_post_processing(self, ctx, item_name, item_data):
        """
        called at the end of `_process_received_items`. for calling other functions on getting items.
        ph uses it for giving all the ship parts as one item, for resetting the treasure tracker
        and for sending hints on getting treasure maps
        :param ctx:
        :param item_name:
        :param item_data:
        :return:
        """
        pass
    # Set checks to look for inventory changes

    async def _remove_vanilla_item(self, ctx: "BizHawkClientContext", num_received_items):
        print(f"Removing vanilla items {self.last_vanilla_item}")
        for item in self.last_vanilla_item:
            if isinstance(item, str):
                # Handle game specific items
                if "dummy" in ITEMS_DATA[item]:
                    continue
                if not await self.remove_special_vanilla_item(ctx, item):
                    data = ITEMS_DATA[item]
                    value = data.get('value', 1)
                    if "Small Key" in item:
                        address = self.key_address = await self.get_small_key_address(ctx)
                        print("small key?")
                    elif "progressive" in data:
                        write_list = []
                        index = sum([1 for i in ctx.items_received[:num_received_items] if i.item == data["id"]])
                        if index >= len(data["progressive"]):
                            continue
                        address, value = data["progressive"][index]
                        if "give_ammo" in data:
                            ammo_v = data["give_ammo"][min(max(index - 1, 0), len(data["give_ammo"])-1)]
                            write_list.append((data["ammo_address"], [ammo_v], "Main RAM"))
                        # Progressive overwrite fix
                        if "progressive_overwrite" in data and index > 1:
                            write_list.append((data["progressive"][index-1][0], [data["progressive"][index-1][1]], "Main RAM"))
                        await bizhawk.write(ctx.bizhawk_ctx, write_list)
                    else:
                        address, value = data["address"], data.get("value", 1)

                    # Catch vanilla rupees going over 9999
                    if "Rupee" in item:
                        if self.prev_rupee_count + value > 9999:
                            value =  9999 - self.prev_rupee_count

                    await write_memory_value(ctx, address, value,
                                             incr=data.get('incremental', None), unset=True, size=data.get("size", 1))

            # If item is a list of items, we instead want to check which one Link got and loop that back into this process
            else:
                for _item, _count in item:
                    new_item_read = await self.get_item_read(ctx, _item)
                    if "Rupee" in item:
                        if new_item_read - _count == ITEMS_DATA[_item]["value"]:
                            self.last_vanilla_item.append(_item)
                            break
                    elif new_item_read != _count:
                        self.last_vanilla_item.append(_item)
                        break

        self.last_vanilla_item.clear()
    # Called during location processing to determine what vanilla item to remove

    async def remove_special_vanilla_item(self, ctx, vanilla_item: str):
        """
        called first in remove_vanilla_item.
        for removing game specific item cases like treasure and vehicle parts
        :param ctx:
        :param vanilla_item:
        :return: false if you didn't remove a special item and want to remove normally
        """
        return False

    async def detect_warp_to_start(self, ctx, read_result: dict):
        """
        called every cycle in game. detect warp to start, and cancel any nasty conflicts
        :param ctx:
        :param read_result:
        :return:
        """
        pass

    async def process_in_game(self, ctx, read_result: dict):
        """
        called every cycle in game, not while loading
        :param ctx:
        :param read_result:
        :return:
        """
        pass

    async def process_game_completion(self, ctx: "BizHawkClientContext"):
        """
        Process if player has reached goal
        :param ctx: BizHawkClientContext
        :return: sends game completion to server if return true
        """
        return False

    async def process_on_room_load(self, ctx, current_scene, read_result: dict):
        """
        called once when room is fully loaded, early in the sequence
        :param ctx:
        :param current_scene:
        :param read_result:
        :return:
        """
        pass

    async def process_hard_coded_rooms(self, ctx, current_scene):
        """
        called when room has fully loaded, after most of the obligate methods
        for running specific code for specific rooms, that can't be handled by dynamic flags
        :param ctx:
        :param current_scene:
        :return:
        """
        pass

    async def _set_er_coords(self, ctx):
        if self.er_exit_coord_writes:
            await bizhawk.write(ctx.bizhawk_ctx, self.er_exit_coord_writes)
            self.er_exit_coord_writes = None

    async def enter_special_key_room(self, ctx, stage, scene_id) -> bool:
        """
        called on entering a new stage, to set small keys in a different way to default
        used in ph to give totok keys without resetting the counter
        :param ctx:
        :param stage:
        :param scene_id:
        :return: true if did special operation, false if not and want to do normal operation
        """
        return False

    async def set_stage_flags(self, ctx, stage):
        """
        called on entering a new stage. sets stage flags. ST doesn't do this yet
        :param ctx:
        :param stage:
        :return:
        """
        pass

    async def _enter_stage(self, ctx, stage, scene_id):
        await self.set_stage_flags(ctx, stage)
        # Give dungeon keys
        if stage in self.dungeon_key_data:
            if not await self.enter_special_key_room(ctx, stage, scene_id):
                await self.update_key_count(ctx, stage)
        self.entering_from = scene_id

    def update_boss_warp(self, ctx, stage, scene_id):
        """
        method for setting self.last_dungeon_warp_target for redirecting warps after bosses in entrance rando
        :param ctx:
        :param stage:
        :param scene_id:
        :return: PHTransition for the location
        """
        return None

    async def _load_local_locations(self, ctx, scene):
        # Load locations in room into loop
        self.locations_in_scene = self.location_area_to_watches.get(scene, {}).copy()
        print(f"Locations in scene {scene}: {self.locations_in_scene.keys()}")
        self.watches = {}
        sram_read_list = {}
        locations_found = ctx.checked_locations
        if self.locations_in_scene is not None:
            # Create memory watches for checks triggerd by flags, and make list for checking sram
            for loc_name, location in self.locations_in_scene.items():
                loc_id = self.location_name_to_id[loc_name]
                if loc_id in locations_found:
                    if "address" in location:
                        read = await read_memory_value(ctx, location["address"])
                        if read & location["value"]:
                            print(f"Location {loc_name} has already been found and triggered")
                            continue
                else:
                    if "sram_addr" in location and location["sram_addr"] is not None:
                        sram_read_list[loc_name] = (location["sram_addr"], 1, "SRAM")
                        print(f"\tCreated sram read for loacation {loc_name}")

                if "address" in location:
                    self.watches[loc_name] = (location["address"], 1, "Main RAM")

            # Read and set locations missed when bizhawk was disconnected
            if self.save_slot == 0 and len(sram_read_list) > 0:
                sram_reads = await read_memory_values(ctx, sram_read_list)
                for loc_name, value in sram_reads.items():
                    if value & LOCATIONS_DATA[loc_name]["sram_value"]:
                        await self._process_checked_locations(ctx, loc_name)

    async def update_special_key_count(self, ctx, current_stage: int, new_keys:int, key_data: dict, key_values: dict, key_address: int) -> tuple[int, bool]:
        """
        called on enter stage if you want to change the number of keys written based on a parameter.
        used in ph for removing a totok key after opening the door on 1f
        :param ctx:
        :param current_stage:
        :param new_keys: number of keys in memory
        :param key_data:
        :param key_values: previous key read values, dict
        :param key_address: location of key counter in heap
        :return: number of keys to write, reset key storage
        """
        return new_keys, True

    async def update_key_count(self, ctx, current_stage: int) -> None:
        """
        Called when entering a dungeon. Updates key count based on a tracker counter in memory,
        specified in self.dungeon_key_data
        :param ctx:
        :param current_stage:
        :return:
        """
        key_address = self.key_address = await self.get_small_key_address(ctx)
        key_data = self.dungeon_key_data.get(current_stage, None)
        read_list = {"dungeon": (key_address, 1, "Main RAM"),
                     "tracker": (key_data["address"], 1, "Main RAM")}
        key_values = await read_memory_values(ctx, read_list)

        new_keys = (((key_values["tracker"] & key_data["filter"]) // key_data["value"])
                    + key_values["dungeon"])

        # Create write list, reset key tracker
        if new_keys != 0:
            new_keys = 7 if new_keys >= 7 else new_keys
            new_keys, reset_key_count = await self.update_special_key_count(ctx, current_stage, new_keys, key_data, key_values, key_address)
            new_keys = 0 if new_keys < 0 else new_keys
            write_list = [(key_address, [new_keys], "Main RAM")]
            if reset_key_count:
                reset_tracker = (~key_data["filter"]) & key_values["tracker"]
                write_list += [(key_data["address"], [reset_tracker], "Main RAM")]

            print(f"Finally writing keys to memory {hex(key_address)} with value {hex(new_keys)}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def _process_scouted_locations(self, ctx: "BizHawkClientContext", scene):
        def check_items(d):
            for item in d.get("has_items", []):
                if ITEMS_DATA[item]["id"] not in [i.item for i in ctx.items_received]:
                    return False
            return True

        def check_slot_data(d):
            for args in d.get("slot_data", []):
                if type(args) is str:
                    option, value = args, [True]
                else:
                    option, value = args
                    value = [value] if type(value) is int else value  # Support lists of values
                if ctx.slot_data.get(option, "unknown_slot_data") not in value:
                    return False
            return True

        local_scouted_locations = set(ctx.locations_scouted)
        if self.hint_scene_to_watches.get(scene, []):
            print(f"hints {self.hint_scene_to_watches.get(scene, [])}")
        for hint_name in self.hint_scene_to_watches.get(scene, []):
            hint_data = self.hint_data[hint_name]
            # Check requirements
            if not check_items(hint_data):
                continue
            if not check_slot_data(hint_data):
                continue

            # Figure out locations to hint
            if "locations" in hint_data:
                # Hint required dungeons
                if "Dungeon Hints" in hint_data["locations"]:
                    local_scouted_locations.update(self.dungeon_hints(ctx))
                else:
                    locations_checked = ctx.locations_scouted
                    for loc in hint_data["locations"]:
                        loc_id = self.location_name_to_id[loc]
                        if loc_id in locations_checked:
                            continue
                        local_scouted_locations.add(loc_id)
            else:
                local_scouted_locations.add(self.location_name_to_id[hint_name])

        # Send hints
        if self.local_scouted_locations != local_scouted_locations:
            self.local_scouted_locations = local_scouted_locations
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.local_scouted_locations),
                "create_as_hint": int(2)
            }])

    async def _process_game_completion(self, ctx: "BizHawkClientContext"):
        if await self.process_game_completion(ctx):
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage, read_result):
        """
        process deathlink, both sending and receiving.
        :param ctx:
        :param is_dead:
        :param stage:
        :param read_result:
        :return:
        """

    async def ut_bounce_scene(self, ctx, stage, room, entrance):
        print(f"UT Bouncing {hex(stage)} {room} {entrance}")
        await ctx.send_msgs([{
            "cmd": "Bounce",
            "games": [self.game],
            "slots": [ctx.slot],
            "tags": ['Tracker'],
            "data": {"stage": stage,
                     "room": room,
                     "entrance": entrance}
        }])

    def dungeon_hints(self, ctx):
        """
        Write out dungeon hints depending on settings
        :param ctx:
        :return: list of location to scout
        """
        return []
