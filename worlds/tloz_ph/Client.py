from random import randint
from .DSZeldaClient.DSZeldaClient import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from .Subclasses import PHTransition

ROM_ADDRS = {
    "game_identifier": (0, 16, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0x060C48, 1, "Main RAM"),
    "in_cutscene": (0x1BBCF4, 1, "Main RAM"),

    "link_health": (0x1CB08E, 2, "Main RAM"),
    "boat_health": (0x1FA036, 1, "Main RAM"),
    "salvage_health": (0x1F5720, 1, "Main RAM"),

    "received_item_index": (0x1BA64C, 2, "Main RAM"),
    "slot_id": (0x1BA64A, 2, "Main RAM"),

    "stage": (0x1B2E94, 4, "Main RAM"),
    "floor": (0x1B2E98, 4, "Main RAM"),
    "room": (0x1B2EA6, 1, "Main RAM"),
    "entrance": (0x1B2EA7, 1, "Main RAM"),
    "flags": (0x1B557C, 52, "Main RAM"),

    "getting_item": (0x1B6F44, 1, "Main RAM"),
    "shot_frog": (0x1B7038, 1, "Main RAM"),
    "getting_ship_part": (0x11F5E4, 1, "Main RAM"),
    "getting_salvage": (0x1BA654, 1, "Main RAM"),

    "link_x": (0x1B6FEC, 4, "Main RAM"),
    "link_y": (0x1B6FF0, 4, "Main RAM"),
    "link_z": (0x1B6FF4, 4, "Main RAM"),
    "using_item:": (0x1BA71C, 1, "Main RAM"),
    "drawing_sea_route": (0x207C4C, 1, "Main RAM"),
    "boat_x": (0x1B8518, 4, "Main RAM"),
    "boat_z": (0x1B8520, 4, "Main RAM"),
    "save_slot": (0x1B8124, 1, "Main RAM"),
    "equipped_item": (0x1BA520, 4, "Main RAM"),
    "got_item_menu": (0x19A5B0, 1, "Main RAM"),

    "loading_stage": (0x1B2E78, 1, "Main RAM"),  # 0 when loading stage, some sorta pointer
    "loading_room": (0x10BD6F, 1, "Main RAM"),  # 0 when not loading room

    "opened_clog": (0x0FC5BC, 1, "Main RAM"),
    "flipped_clog": (0x0FA37B, 1, "Main RAM"),

    "in_short_cs": (0x1B6FE8, 1, "Main RAM"),

}

POINTERS = {
    "ADDR_gItemManager": 0x0fb4,
    "ADDR_gPlayerManager": 0x0fbc,
    "ADDR_gAdventureFlags": 0x0f74,
    "ADDR_gPlayer": 0x0f90,
    "ADDR_gOverlayManager_mLoadedOverlays_4": 0x0910,
    "ADDR_gMapManager": 0x0e60
}

EQUIP_TIMER_OFFSET = 0x20

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 0x268

# Addresses to read each cycle
read_keys_always = ["game_state", "in_cutscene", "received_item_index", "stage", "room", "slot_id",
                    "entrance", "in_short_cs",
                    "loading_room", "opened_clog"]

read_keys_deathlink = ["link_health"]
read_keys_land = ["getting_item", "getting_ship_part"]
read_keys_sea = ["shot_frog"]
read_keys_deathlink_sea = ["boat_health", "drawing_sea_route"]
read_keys_deathlink_salvage = ["salvage_health"]

class PhantomHourglassClient(DSZeldaClient):
    game = "The Legend of Zelda - Phantom Hourglass"
    system = "NDS"

    def __init__(self) -> None:
        super().__init__()
        # Required variables from inherit
        self.starting_flags = STARTING_FLAGS
        self.dungeon_key_data = DUNGEON_KEY_DATA
        self.slot_id_addr = RAM_ADDRS["slot_id"][0]
        self.received_item_index_addr = RAM_ADDRS["received_item_index"][0]
        self.starting_entrance = (11, 3, 5)  # stage, room, entrance
        self.scene_addr = (RAM_ADDRS["stage"][0], RAM_ADDRS["room"][0], RAM_ADDRS["floor"][0], RAM_ADDRS["entrance"][0])  # Stage, room, floor, entrance
        self.exit_coords_addr = (0x1B2EC8, 0x1B2ECC, 0x1B2ED0)  # x, y, z. what coords to spawn link at when entering a
        # continuous transition
        self.er_y_offest = 164  # In ph i use coords who's y is 164 off the entrance y
        self.ADDR_gMapManager = POINTERS["ADDR_gMapManager"]
        self.stage_flag_offset = STAGE_FLAGS_OFFSET
        self.hint_data = HINT_DATA
        self.entrances = ENTRANCES

        # Ph variables
        self.goal_room = 0x3600
        self.last_treasures = 0
        self.last_potions = [0, 0]
        self.last_ship_parts = []
        self.at_sea = False
        self.lowered_water = False
        self.visited_entrances = set()

        self.boss_warp_entrance = None
        self.last_warp_stage = None
        self.item_location_combo = None

    async def check_game_version(self, ctx: "BizHawkClientContext") -> bool:
        rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
        rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
        print(f"Rom Name: {rom_name}")
        if rom_name != "ZELDA_DS:PHAZEP":  # EU
            if rom_name == "ZELDA_DS:PHAZEE":  # US
                logger.error("You are using a US rom that is not supported yet. sorry!")
                self.version_offset = -64
            return False
        return True

    async def set_special_starting_flags(self, ctx: "BizHawkClientContext") -> list[tuple[int, list, str]]:
        """
        Game specific starting flag logic.
        Flags defined in STARTING_FLAGS are set automatically
        :param ctx: BizhawkClientContext
        :return: write_list
        """
        # Reset save slot
        write_list = [(0x1BA64C, [0, 0], "Main RAM")]

        # Reset starting time for PH
        ph_time_bits = split_bits(0, 4)
        write_list.append((0x1BA528, ph_time_bits, "Main RAM"))

        # Set Frog flags if not randomizing frogs
        if ctx.slot_data["randomize_frogs"] == 1:
            write_list += [(a, [v], "Main RAM") for a, v in STARTING_FROG_FLAGS]
        # Set Fog Flags
        fog_bits = FOG_SETTINGS_FLAGS[ctx.slot_data["fog_settings"]]
        if len(fog_bits) > 0:
            write_list += [(a, [v], "Main RAM") for a, v in fog_bits]
        if ctx.slot_data["skip_ocean_fights"] == 1:
            write_list += [(0x1B5592, [0x84], "Main RAM")]
        # Ban player from harrow if not randomized
        if ctx.slot_data["randomize_harrow"] == 0:
            write_list += [(0x1B559A, [0x18], "Main RAM")]

        # Print starting hints
        if ctx.slot_data["dungeon_hint_location"] == 0:
            self.dungeon_hints(ctx)

        return write_list

    async def get_coords(self, ctx, multi=False):
        coords = await read_memory_values(ctx, self.get_coord_address(multi=multi), signed=True)
        if not multi:
            return {
                "x": coords.get("link_x", coords.get("boat_x", 0)),
                "y": coords.get("link_y", 0),
                "z": coords.get("link_z", coords.get("boat_z", 0))
            }
        return coords

    def update_metal_count(self, ctx):
        metal_ids = [ITEMS_DATA[i]["id"] for i in ITEM_GROUPS["Metals"]]
        self.metal_count = sum(1 for i in ctx.items_received if i.item in metal_ids)

    async def update_treasure_tracker(self, ctx):
        self.last_treasures = await read_memory_value(ctx, 0x1BA5AC, 8)
        # print(f"Treasure Tracker! {split_bits(self.last_treasures, 8)}")

    async def give_random_treasure(self, ctx):
        address = 0x1BA5AC + randint(0, 7)
        await write_memory_value(ctx, address, 1, incr=True)
        await self.update_treasure_tracker(ctx)

    async def update_potion_tracker(self, ctx):
        read_list = {"left": (0x1BA5D8, 1, "Main RAM"),
                     "right": (0x1BA5D9, 1, "Main RAM")}
        reads = await read_memory_values(ctx, read_list)
        self.last_potions = list(reads.values())

    def get_coord_address(self, at_sea=None, multi=False) -> dict[str, tuple[int, int, str]]:
        if not multi:
            at_sea = self.at_sea if at_sea is None else at_sea
            if at_sea:
                return {k: v for k, v in RAM_ADDRS.items() if k in ["boat_x", "boat_z"]}
            elif not at_sea:
                return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}
        return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"] + ["boat_x", "boat_z"]}

    async def update_main_read_list(self, ctx, stage, in_game=True):
        read_keys = read_keys_always.copy()
        death_link_keys = []
        death_link_reads = {}
        death_link_pointers = {}
        if stage is not None:
            if stage == 0:
                read_keys += read_keys_sea
                death_link_keys = read_keys_deathlink_sea
                self.at_sea = True
            elif stage == 3:
                death_link_keys = read_keys_deathlink_salvage
                # Add separate reads for instant-repairs
                read_keys += read_keys_deathlink_salvage
            else:
                read_keys += read_keys_land
                if in_game:
                    death_link_pointers["link_health"] = ("ADDR_gPlayer", 0xa)
                self.at_sea = False

            # Read health for deathlink and cancelling warp to start on death
            for key in death_link_keys:
                value = RAM_ADDRS[key]
                if key in ["boat_health", "salvage_health"]:
                    key = "link_health"
                death_link_reads[key] = value

            death_link_reads |= {key: value for key, value in RAM_ADDRS.items() if key in death_link_keys}

            for name, pointer in death_link_pointers.items():
                addr, offset = pointer
                pointer_1 = await read_memory_value(ctx, POINTERS[addr], 4, "Data TCM")
                death_link_reads[name] = (pointer_1 + offset - 0x2000000, 2, "Main RAM")
            self.main_read_list = {k: v for k, v in RAM_ADDRS.items() if k in read_keys} | death_link_reads
        else:
            self.at_sea = None
        return self.main_read_list

    async def full_heal(self, ctx, bonus=0):
        if not self.at_sea:
            hearts = item_count(ctx, "Heart Container") + 3 + bonus
            health_address = await read_memory_value(ctx, POINTERS["ADDR_gPlayer"], 4, "Data TCM") + 0xA - 0x2000000
            print(f"Sent full heal hearts {hearts} addr {hex(health_address)}")
            await write_memory_values(ctx, health_address, split_bits(hearts * 4, 2), overwrite=True)

    async def refill_ammo(self, ctx):
        items = [i + " (Progressive)" for i in ["Bombs", "Bombchus", "Bow"]]

        # Count upgrades
        counts = {ITEMS_DATA[i]["id"]: 0 for i in items}
        for i in ctx.items_received:
            for k in counts:
                if k == i.item:
                    counts[k] += 1

        # Write Upgrades
        write_list = []
        for i, count in enumerate(counts.values()):
            data = ITEMS_DATA[items[i]]
            write_list += [(data["ammo_address"], [data["give_ammo"][count - 1]], "Main RAM")]
        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        await self.full_heal(ctx)
        logger.info(f"You drink a glass of milk. You feel refreshed, and your ammo has been refilled.")

    def get_progress(self, ctx, scene=0):
        # Count current metals
        progress = 0
        metals = [ITEMS_DATA[i]["id"] for i in ITEM_GROUPS["Metals"]]
        for i in ctx.items_received:
            if i.item in metals:
                progress += 1

        # Figure out totals
        if ctx.slot_data["goal_requirements"] < 2:
            total = ctx.slot_data["dungeons_required"]
            required = total
        elif ctx.slot_data["goal_requirements"] == 2:
            total = ctx.slot_data["metal_hunt_total"]
            required = ctx.slot_data["metal_hunt_required"]
        else:
            return True

        if scene == 0xB0A:
            # Oshus Text
            bellum_texts = ["spawns the phantoms in TotOK B13.",
                            "opens the staircase to Bellum at the bottom of TotOK.",
                            "opens the blue warp to Bellum in TotOK.",
                            "spawns the ruins of the Ghost Ship in the SW Quadrant.",
                            "wins the game."]
            logger.info(f"You have {progress} out of {required} rare metals. There are {total} metals in total.\n"
                        f"Finding the metals {bellum_texts[ctx.slot_data['bellum_access']]}")
        elif scene == 0x160A:
            zauz_required = ctx.slot_data["zauz_required_metals"]
            logger.info(f"Zauz needs {zauz_required} rare metals to give an item. You have {progress}/{total} metals.")

    def process_loading_variable(self, read_result) -> bool:
        return read_result["loading_room"]

    async def process_read_list(self, ctx: "BizHawkClientContext", read_result: dict):
        """
        Game watcher just read self.main_read_list. What do you do with the data?
        :param ctx: BizHawkClientContext
        :param read_result: dict of address name to read value
        :return:
        """
        # This go true when link gets item
        if self.at_sea:
            self.getting_location = read_result.get("shot_frog", False)
        else:
            self.getting_location = read_result.get("getting_item", 0) & 0x20 or read_result.get("getting_ship_part",
                                                                                            False)

    async def process_on_room_load(self, ctx, current_scene, read_result: dict):
        self.prev_rupee_count = await read_memory_value(ctx, 0x1ba53e, 2)
        await self.update_potion_tracker(ctx)
        await self.update_treasure_tracker(ctx)

    async def process_in_game(self, ctx, read_result: dict):

        # Detect lowering of water and update ER Map
        if not self.lowered_water and self.current_stage == 0x24:
            await self.lower_water(ctx)

    async def detect_warp_to_start(self, ctx, read_result: dict):
        # Opened clog warp to start check
        if read_result.get("opened_clog", False):
            if await read_memory_value(ctx, *RAM_ADDRS["flipped_clog"], silent=True) & 1:
                if not self.warp_to_start_flag:
                    logger.info(f"Primed a warp to start. Enter a transition to warp to {STAGES[0xB]}.")
                self.warp_to_start_flag = True
            else:
                if self.warp_to_start_flag and await read_memory_value(ctx, *RAM_ADDRS["opened_clog"], silent=True):
                    logger.info("Canceled warp to start.")
                    self.warp_to_start_flag = False

        # Cancel warp to start if in a dangerous situation
        if self.warp_to_start_flag:
            # Cyclone slate warp to start crashes, prevent that from working
            if self.at_sea:
                if await read_memory_value(ctx, 0x1B636C) == 1:  # is 0x65 if never used cyclone slate
                    self.warp_to_start_flag = False
                    logger.info("Canceled warp to start, Cyclone Slate is not a valid warp method")
            if self.is_dead:
                self.warp_to_start_flag = False
                logger.info("Canceled warp to start, death is not a valid warp method")

    async def enter_game(self, ctx):
        self.save_slot = await read_memory_value(ctx, RAM_ADDRS["save_slot"][0], silent=True)
        self.update_metal_count(ctx)
        self.set_ending_room(ctx)
        await self.lower_water(ctx)
        await write_memory_value(ctx,0x0EC754, 2, overwrite=True)  # Set text speed to fast, no matter settings
        await self.update_stored_entrances(ctx)

        # Set warp to start location
        if ctx.slot_data["shuffle_overworld_transitions"]:
            self.starting_entrance = (11, 0, 0)


    async def watched_intro_cs(self, ctx):
        return await read_memory_value(ctx, 0x1b55a8, silent=True) & 2

    async def process_hard_coded_rooms(self, ctx, current_scene):
        # Yellow warp in TotOK saves keys
        # TODO: allow this to work with ER
        if self.last_scene is not None:
            if current_scene == 0x2509 and self.last_scene == 0x2507:
                await self.write_totok_midway_keys(ctx)

        # Repair salvage arm in certain rooms
        if current_scene in [0x130A, 0x500]:
            await self.repair_salvage_arm(ctx, current_scene)

        # Milk bar refills all ammo
        if current_scene in [0xb0C]:
            await self.refill_ammo(ctx)

        # Oshus gives metal info
        if current_scene in [0xB0A, 0x160A]:
            self.get_progress(ctx, current_scene)

        # Shipyard gives ship parts
        if current_scene in [0xB0D]:
            await self.edit_ship(ctx)
        if current_scene in [0xB03]:
            await self.remove_ship_parts(ctx)

        # Open pedestal doors. sucks that you can't trigger it with dynaflags. slow code but game is slower
        if ctx.slot_data.get("randomize_pedestal_items", 0) > 0:

            # === TotOK ===
            if current_scene == 0x2503:  # B3
                if item_count(ctx, "Force Gem (B3)") >= 3 or item_count(ctx, "Force Gems"):
                    await write_memory_values(ctx, 0x2572EC, [0xFE, 0x0F])
            elif current_scene == 0x250B:  # B8
                if (item_count(ctx, "Round Crystal (Temple of the Ocean King)")
                        or item_count(ctx, "Round Pedestal B8 (Temple of the Ocean King)")
                        or item_count(ctx, "Round Crystals")):
                    await write_memory_value(ctx, 0x25762C, 0x2)
                if (item_count(ctx, "Triangle Crystal (Temple of the Ocean King)")
                        or item_count(ctx, "Triangle Pedestal B8 (Temple of the Ocean King)")
                        or item_count(ctx, "Triangle Crystals")):
                    await write_memory_value(ctx, 0x25762C, 0x4)
            elif current_scene == 0x250C:  # B9
                if (item_count(ctx, "Round Crystal (Temple of the Ocean King)")
                        or item_count(ctx, "Round Pedestal B9 (Temple of the Ocean King)")
                        or item_count(ctx, "Round Crystals")):
                    await write_memory_value(ctx, 0x257694, 0x4)
                if (item_count(ctx, "Triangle Crystal (Temple of the Ocean King)")
                        or item_count(ctx, "Triangle Pedestal B9 (Temple of the Ocean King)")
                        or item_count(ctx, "Triangle Crystals")):
                    await write_memory_value(ctx, 0x257694, 0x8)
                if (item_count(ctx, "Square Crystal (Temple of the Ocean King)")
                        or item_count(ctx, "Square Crystals")):
                    await write_memory_value(ctx, 0x257694, 0x22)
                if item_count(ctx, "Square Pedestal West (Temple of the Ocean King)"):
                    await write_memory_value(ctx, 0x257694, 0x20)
                if item_count(ctx, "Square Pedestal Center (Temple of the Ocean King)"):
                    await write_memory_value(ctx, 0x257694, 0x2)
            elif current_scene == 0x2510:  # B12
                gem_count = item_count(ctx, "Force Gem (B12)") | item_count(ctx, "Force Gems")*3
                if gem_count >= 3:
                    await write_memory_values(ctx, 0x257834, [0xFE, 0x0F])
                elif gem_count == 2:
                    await write_memory_value(ctx, 0x257834, 0xC)
                elif gem_count == 1:
                    await write_memory_value(ctx, 0x257834, 0x8)
                # Remove ability to place force gems on southern pedestals
                await write_memory_value(ctx, 0x257EA4, 0x9, overwrite=True)
                await write_memory_value(ctx, 0x257FE4, 0x9, overwrite=True)

            # === Temple of Courage ===
            elif current_scene == 0x1E00:
                if (item_count(ctx, "Square Pedestal North (Temple of Courage)")
                        or item_count(ctx, "Square Crystal (Temple of Courage)")
                        or item_count(ctx, "Square Crystals")):
                    await write_memory_value(ctx, 0x252264 , 0x10)
                if (item_count(ctx, "Square Pedestal South (Temple of Courage)")
                        or item_count(ctx, "Square Crystal (Temple of Courage)")
                        or item_count(ctx, "Square Crystals")):
                    await write_memory_value(ctx, self.stage_address, 0x80)

            # === Ghost Ship ===
            elif current_scene == 0x2900:
                if (item_count(ctx, "Triangle Crystal (Ghost Ship)")
                        or item_count(ctx, "Triangle Crystals")):
                    await write_memory_value(ctx, self.stage_address+1, 0x8)
                if (item_count(ctx, "Round Crystal (Ghost Ship)")
                        or item_count(ctx, "Round Crystals")):
                    await write_memory_value(ctx, self.stage_address+3, 0x2)

    async def write_totok_midway_keys(self, ctx):
        data = DUNGEON_KEY_DATA[372]
        keys = await read_memory_value(ctx, self.key_address)
        keys = keys * data["value"]
        keys = data["filter"] if keys > data["filter"] else keys
        await write_memory_value(ctx, 0x1BA64F, keys)
        await write_memory_value(ctx, 0x1BA661, 0x40)  # Set bit to write future TotOK keys to post midway

    @staticmethod
    async def repair_salvage_arm(ctx, scene=0x500):
        read_list = {"salvage_health": (0x1BA390, 1, "Main RAM"),
                     "rupees": (0x1BA53E, 2, "Main RAM"),
                     "repair_kits": (0x1BA661, 1, "Main RAM"), }
        prev = await read_memory_values(ctx, read_list)
        prev["repair_kits"] &= 0x7
        if prev["salvage_health"] <= 2:
            write_list = []
            text = f"Repaired Salvage Arm for "
            if prev["repair_kits"] > 0:
                write_list.append((0x1BA661, [prev["repair_kits"] - 1], "Main RAM"))
                text += f"1 Salvage Repair Kit. You have {prev['repair_kits']} remaining."
            else:
                # Repair cost, doesn't care if you're out of rupees out of qol
                cost = 100 if prev["salvage_health"] == 0 else (6 - prev["salvage_health"]) * 10
                rupees = 0 if prev["rupees"] - cost <= 0 else prev["rupees"] - cost
                write_list.append((0x1BA53E, split_bits(rupees, 2), "Main RAM"))
                text += f"{cost} rupees."
                print(rupees)
            write_list.append((0x1BA390, [5], "Main RAM"))

            print(write_list)
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
        else:
            text = f"This room automatically repairs your Salvage Arm, for a cost, when at 2 health or below."
        # Send a client message about the repair
        logger.info(text)

    @staticmethod
    async def instant_repair_salvage_arm(ctx):
        salvage_kits = await read_memory_value(ctx, 0x1BA661) & 7
        if salvage_kits > 0:
            write_list = [(0x1BA661, [salvage_kits - 1], "Main RAM"),
                          (RAM_ADDRS["salvage_health"][0], [5], "Main RAM"),
                          (0x1BA390, [5], "Main RAM")]  # Global salvage health
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            logger.info(f"Salvage Arm instant-repaired. You have {salvage_kits - 1} Salvage Repair Kits remaining.")

    @staticmethod
    async def remove_ship_parts(ctx):
        ship_write_list = ([1] + [0] * 8) * 8
        await write_memory_values(ctx, 0x1BA564, ship_write_list, overwrite=True)

    async def edit_ship(self, ctx):
        # Figure out what ships player has
        ships = [1] + [0]*8
        for i in ctx.items_received:
            item_id = i.item
            item_name = self.item_id_to_name[item_id]
            if "Ship:" in item_name:
                item_data = ITEMS_DATA[item_name]
                ships[item_data.get("ship", 0)] = 1
        # Give ship parts
        ship_write_list = [] + ships * 8
        print(ships, ship_write_list)
        await bizhawk.write(ctx.bizhawk_ctx, [(0x1BA564, ship_write_list, "Main RAM")])
        await write_memory_value(ctx, 0x1ba661, 0x80)

    # Dynamic flags/ Entrances
    async def has_special_dynamic_requirements(self, ctx, data) -> bool:
        # Special case of metals
        def check_metals(d):
            if "zauz_metals" in d or "goal_requirement" in d:
                metals_ids = [ITEMS_DATA[metal]["id"] for metal in ITEM_GROUPS["Metals"]]
                current_metals = sum([1 for i in ctx.items_received if i.item in metals_ids])
                print(f"Metal check: {current_metals} metals out of {ctx.slot_data['zauz_required_metals']}")

                # Zauz Check
                if "zauz_metals" in d:
                    if current_metals < ctx.slot_data["zauz_required_metals"]:
                        if d["zauz_metals"]:
                            return False
                    else:
                        if not d["zauz_metals"]:
                            return False

                # Goal Check
                if "goal_requirement" in d:
                    return current_metals >= ctx.slot_data["required_metals"]
            return True

        # Beedle points
        def check_beedle_points(d):
            if not d.get("beedle_points", False):
                return True
            reference = {"Beedle Points (10)": 10,
                         "Beedle Points (20)": 20,
                         "Beedle Points (50)": 50}
            # Count points
            reference = {ITEMS_DATA[k]["id"]: c for k, c in reference.items()}
            points = 0
            for i in ctx.items_received:
                if i.item in reference:
                    points += reference[i.item]
            print(f"Beedle points {d.get('beedle_points')} >= {points}")
            return points >= d.get('beedle_points', 300)

        def count_spirit_gems(d):
            if "count_gems" in d:
                pack_size = ctx.slot_data["spirit_gem_packs"]
                gem_count = item_count(ctx, f"{d['count_gems']} Gem Pack")
                count = pack_size * gem_count
                print(count, d["count_gems"])
                if count < 20:
                    return False
            return True

        # Checks
        if not check_metals(data):
            print(f"\t{data['name']} does not have enough metals")
            return False
        if not check_beedle_points(data):
            return False
        if not count_spirit_gems(data):
            print(f"\t{data['name']} does not have enough spirit packs")
            return False
        if data.get("has_lowered_water", False):
            if not self.lowered_water:
                print(f"\t{data['name']} has not lowered water")
                return False
        return True

    async def set_stage_flags(self, ctx, stage):
        self.stage_address = await get_address_from_heap(ctx, self.ADDR_gMapManager, offset=STAGE_FLAGS_OFFSET)
        self.key_address = self.stage_address + SMALL_KEY_OFFSET
        if stage in STAGE_FLAGS:
            flags = STAGE_FLAGS[stage]

            # Change certain stage flags based on options
            if stage == 0 and ctx.slot_data["skip_ocean_fights"] == 1:
                flags = SKIP_OCEAN_FIGHTS_FLAGS
            if stage == 41 and ctx.slot_data["logic"] >= 1:
                flags = SPAWN_B3_REAPLING_FLAGS

            print(f"\tSetting Stage flags for {STAGES[stage]}, "
                  f"adr: {hex(self.stage_address)}")
            await write_memory_values(ctx, self.stage_address, flags)

        # Unlock boss door if have bk
        data = BOSS_DOOR_DATA.get(stage, False)
        if data and ctx.slot_data.get("boss_key_behaviour", True):
            if item_count(ctx, f"Boss Key ({data['name']})"):
                await write_memory_value(ctx, data["address"], data["value"], size=4)

    # Enter stage
    async def enter_special_key_room(self, ctx, stage, scene_id) -> bool:
        if stage != 0x25:
            return False
        if scene_id in [0x2509, 0x250E]:
            await self.update_key_count(ctx, 372)
        elif scene_id in [0x2500, 0x2504]:
            return False  # Do normal enter TotOK operation, see update_special_key_count for key calc
        return True

    async def update_special_key_count(self, ctx, current_stage: int, new_keys, key_data: dict, key_values, key_address: int) -> tuple[int, bool]:
        if current_stage == 0x25:
            if self.location_name_to_id["TotOK 1F SW Sea Chart Chest"] in ctx.checked_locations:
                new_keys -= 1  # Opening the SW sea chart door uses a key permanently! No savescums!
            if self.current_scene == 0x2504:  # Set B3.5 key count
                new_keys -= 2
                if not item_count(ctx, "Grappling Hook"):
                    new_keys -= 1
            return new_keys, False
        return new_keys, True

    async def get_small_key_address(self, ctx) -> int:
        return await get_address_from_heap(ctx, self.ADDR_gMapManager, SMALL_KEY_OFFSET)

    # Called during location processing to determine what vanilla item to remove
    async def unset_special_vanilla_items(self, ctx, location, item):
        # Multiple sword items don't detect each other by default
        if item in ["Oshus' Sword", "Phantom Sword"] and item_count(ctx, "Sword (Progressive)"):
            self.last_vanilla_item.pop()

        # Don't remove heart containers if already at max
        if item == "Heart Container" and item_count(ctx, item) >= 13:
            self.last_vanilla_item.pop()

        # Farmable locations don't remove vanilla
        if "farmable" in location and location["id"] in ctx.checked_locations:
            if item == "Ship Part":
                await self.give_random_treasure(ctx)
            else:
                self.last_vanilla_item.pop()

    async def receive_key_in_own_dungeon(self, ctx, item_name: str, write_keys_to_storage):
        # TotOK - adds to key increment if you get it in the dungeon, otherwise do as usual
        if "Temple of the Ocean King" in item_name:
            return [await write_keys_to_storage(37)]
        return []

    async def write_totok_keys_lol(self, ctx, item_name, item_data):
        # If got totok key at vanilla location, add to memory anyway
        if item_name == "Small Key (Temple of the Ocean King)":
            data = DUNGEON_KEY_DATA[item_data["dungeon"]]
            prev_value = await read_memory_value(ctx, data["address"])
            new_value = prev_value + data["value"]
            return [(data["address"], [new_value], "Main RAM")]
        return []

    async def received_special_small_keys(self, ctx, item_name, write_keys_to_storage):
        # TotOK Midway special data
        if "Temple of the Ocean King" in item_name:
            if await read_memory_value(ctx, 0x1BA661) & 0x40:
                return [await write_keys_to_storage(372)]
        return []

    async def received_special_incremental(self, ctx, item_data) -> int:
        # Sand of hours check
        if "Sand" in item_data['value']:

            if item_data.get("value") == "Sand":
                if not ctx.slot_data["ph_required"] or item_count(ctx, "Phantom Hourglass"):
                    value = ctx.slot_data["ph_time_increment"] * 60
                else:
                    value = 0
            elif item_data.get("value") == "Sand PH":
                value = ctx.slot_data["ph_starting_time"] * 60

                # If ph is required, add all time so far on finding
                if ctx.slot_data["ph_required"] and item_count(ctx, "Phantom Hourglass") < 2:
                    value += (ctx.slot_data["ph_time_increment"] * 60 * item_count(ctx, "Sand of Hours")
                              + item_count(ctx, "Sand of Hours (Small)") * 3600
                              + item_count(ctx, "Sand of Hours (Boss)") * 7200)
            else:
                value = item_data.get("value")
            last_time = await read_memory_value(ctx, item_data["address"], size=4)
            if last_time + value > 359940:
                print(f"Time: Last time {last_time} value {value} new {359940 - last_time} max {359940}")
                value = 359940 - last_time
            print(f"Sand stage {self.current_stage} {value}")
            if self.current_stage == 0x25:
                await write_memory_value(ctx, 0x1E2A48, value, incr=True, size=4)

        elif item_data.get("value") == "pack_size":
            value = ctx.slot_data["spirit_gem_packs"]
        else:
            value = "Error!"
        return value

    async def receive_special_items(self, ctx, item_name, item_data) -> list[tuple[int, list, str]]:
        # Set ship
        print(f"special item: {item_name} {self.current_stage}")
        res = []
        if "ship" in item_data:
            if not (await read_memory_value(ctx, 0x1ba661) & 0x80):
                for addr in EQUIPPED_SHIP_PARTS_ADDR:
                    res += [(addr, [item_data["ship"]], "Main RAM")]

        elif item_name == "Refill: Health":
            await self.full_heal(ctx)

        # Open boss door if got bk in own dungeon
        elif "Boss Key" in item_name and ctx.slot_data.get("boss_key_behaviour", True):
            if self.current_stage in BOSS_DOOR_DATA and BOSS_DOOR_DATA[self.current_stage]["name"] in item_name:
                data = BOSS_DOOR_DATA[self.current_stage]
                last_value = await read_memory_value(ctx, data["address"], size=4)
                new_value = last_value | data["value"]
                res += [(data["address"], split_bits(new_value, 4), "Main RAM")]
        return res

    async def receive_item_post_processing(self, ctx, item_name, item_data):
        # If treasure, update treasure tracker
        if "inventory_id" in item_data:
            await self.enable_items(ctx, item_data["inventory_id"])
        if "treasure" in item_data:
            await self.update_treasure_tracker(ctx)
        if "Potion" in item_name:
            await self.update_potion_tracker(ctx)
        # If hint on receive, send hint (currently only treasure maps)
        if "hint_on_receive" in item_data:
            if ctx.slot_data["randomize_salvage"] == 1:
                await self.scout_location(ctx, item_data["hint_on_receive"])
        # Increment metal count
        if item_name in ITEM_GROUPS["Metals"]:
            self.metal_count += 1
            await self.process_game_completion(ctx)

        exclude_key = f"ph_keylocking_{ctx.slot}_{ctx.team}"
        # Exclude forced vanilla items on not needing them any more
        if item_name == "Grappling Hook" and ctx.slot_data.get("randomize_pedestal_items", 0) in [0, 1]:
            print(f"TotOK B3 has no more useful force gems")
            data = [self.location_name_to_id[i] for i in LOCATION_GROUPS["Grappling Hook Excludes"]]
            await self.store_data(ctx, exclude_key, data)

        # Run code if you got a certain item from a certain location
        if self.item_location_combo:
            if "Mountain Passage" in self.item_location_combo["name"]:
                if ctx.slot_data["keysanity"] < 2 and "Small Key" not in item_name:
                    print(f"Mountain Passage has no more useful items")
                    data = [self.location_name_to_id[i] for i in LOCATION_GROUPS["Mountain Passage"]]
                    await self.store_data(ctx, exclude_key, data)

            self.item_location_combo = None

        if "set_bit_in_room" in item_data and ctx.slot_data.get("randomize_pedestal_items", 0):
            print(f"Trying to set bit in room, room {hex(self.current_scene)}")
            if self.current_scene in item_data["set_bit_in_room"]:
                for addr, value, *args in item_data["set_bit_in_room"][self.current_scene]:
                    print(f"args {args}")
                    if addr == "stage_flag":
                        addr = self.stage_address
                        print(f"Stage address: {addr}")
                    if args and "count" in args[0]:
                        if item_count(ctx, item_name) < args[0]["count"]:
                            continue
                    if isinstance(value, int):
                        value = [value]
                    await write_memory_values(ctx, addr, value)


    @staticmethod
    async def enable_items(ctx: "BizHawkClientContext", inventory_id: int):
        equipped_item_pointer = await read_memory_value(ctx, POINTERS["ADDR_gItemManager"], size=4, domain="Data TCM", silent=True) - 0x02000000
        equipped_item = await read_memory_value(ctx, equipped_item_pointer, size=4, silent=True)
        if equipped_item == 0xffffffff:
            print("Items menu not visible... enabling")
            # Enable items menu
            await write_memory_value(ctx, equipped_item_pointer + EQUIP_TIMER_OFFSET, 20, size=2, overwrite=True)
            await write_memory_value(ctx, equipped_item_pointer, inventory_id, size=4, overwrite=True)

    async def remove_special_vanilla_item(self, ctx, vanilla_item: str):
        if vanilla_item == "Treasure":
            treasure_write_list = split_bits(self.last_treasures, 8)
            print(f"Treasure Write List: {treasure_write_list}")
            await write_memory_values(ctx, 0x1BA5AC, treasure_write_list, overwrite=True)
        elif vanilla_item == "Ship Part":
            await self.remove_ship_parts(ctx)
            if self.last_scene == 0xB0D:
                await self.edit_ship(ctx)
        elif "Potion" in vanilla_item:
            print(f"Pots {self.last_potions}")
            if not all(self.last_potions):
                await write_memory_values(ctx, 0x1BA5D8, self.last_potions, overwrite=True)
        elif "Oshus' Sword" in vanilla_item:
            data = ITEMS_DATA[vanilla_item]
            await write_memory_value(ctx, data["ammo_address"], 0, size=2, overwrite=True)
            return False

        elif vanilla_item in ITEM_GROUPS["Throwable Keys"]:
            # Don't do anything if vanilla bk behaviour
            if "Boss Key" in vanilla_item and not ctx.slot_data["boss_key_behaviour"]:
                return True
            # Don't do anything if vanilla pedestal item behaviour
            if ("Crystal" in vanilla_item or "Force Gem" in vanilla_item) and not ctx.slot_data.get("randomize_pedestal_items", 0):
                return True

            # Read actor id in link's held item address. For some reason it's somewhere else in GT
            if self.current_stage == 0x20:
                bk_id = await read_memory_value(ctx, 0x1CD770, silent=True, size=2)
            elif self.current_stage == 0x25:
                bk_id = await read_memory_value(ctx, 0x1CDAE0, silent=True, size=2)
            else:
                bk_id = await read_memory_value(ctx, 0x1CD510,silent=True, size=2)

            # Get the actor table
            actor_table_addr = await read_memory_value(ctx, 0x1BA8C4, size=4, silent=True) - 0x2000000
            actor_table = hex(await read_memory_value(ctx, actor_table_addr, size=250, silent=True))
            actor_table = "0" + actor_table[2:]
            print(f"Removing throwable key {vanilla_item} with bk_id {bk_id}")

            # Loop through the actor table checking if each actor has the bk_id.
            for i in range(len(actor_table)//8):
                actor_data = actor_table[i*8:(i+1)*8]
                if actor_data[1] == "0":  # filter out empty slots
                    continue
                actor_id_addr = int(actor_data, 16) + 8 - 0x2000000
                actor_id = await read_memory_value(ctx, actor_id_addr, size=4, silent=True)
                # If you find the boss key, delete its pointer
                if actor_id == bk_id:
                    little_endian_lol = actor_table_addr + len(actor_table)//2 - (i+1)*4
                    print(f"Found bk pointer: {hex(actor_table_addr)} at index {i}")
                    await write_memory_value(ctx, little_endian_lol, 0, overwrite=True, size=4)
                    break

        else:
            return False
        return True  # Removed vanilla item, don't do more processing

    def set_ending_room(self, ctx):
        if ctx.slot_data["goal_requirements"] == "beat_bellumbeck":
            self.goal_room = 0x3600
        elif ctx.slot_data["goal_requirements"] == "triforce_door":
            self.goal_room = 0x2509

    async def process_game_completion(self, ctx: "BizHawkClientContext"):
        current_scene = self.read_result["stage"] * 0x100 + self.read_result["room"]
        game_clear = False
        current_scene = current_scene * 0x100 if current_scene < 0x100 else current_scene
        if ctx.slot_data["bellum_access"] == 4:
            game_clear = self.metal_count >= ctx.slot_data["required_metals"]
        else:
            game_clear = (current_scene == self.goal_room)  # Enter End Credits
        return game_clear

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage, read_result):
        if (not read_result.get("drawing_sea_route", False) and read_result["in_cutscene"]
                and self.current_scene not in [0x1701]):
            if ctx.last_death_link > self.last_deathlink and not is_dead:
                # A death was received from another player, make our player die as well
                if stage == 0:
                    await write_memory_value(ctx, RAM_ADDRS["boat_health"][0], 0, overwrite=True)
                elif stage == 3:
                    await write_memory_value(ctx, RAM_ADDRS["salvage_health"][0], 0, overwrite=True)
                else:
                    await write_memory_value(ctx, RAM_ADDRS["link_health"][0], 0, size=2, overwrite=True)

                self.is_expecting_received_death = True
                self.last_deathlink = ctx.last_death_link

            if not self.was_alive_last_frame and not is_dead:
                # We revived from any kind of death
                self.was_alive_last_frame = True
            elif self.was_alive_last_frame and is_dead:
                # Our player just died...
                self.was_alive_last_frame = False
                if self.is_expecting_received_death:
                    # ...because of a received deathlink, so let's not make a circular chain of deaths please
                    self.is_expecting_received_death = False
                else:
                    # ...because of their own incompetence, so let's make their mates pay for that
                    await ctx.send_death(ctx.player_names[ctx.slot] + " may have disappointed the Ocean King.")
                    self.last_deathlink = ctx.last_death_link

    def add_special_er_data(self, ctx, er_map, scene, detect_data, exit_data):
        # all lowered water scenes on ruins need to account for funny scene detections
        if scene & 0xFF00 == 0x1100:
            high_scene = 0x1200 + (scene & 0xFF)
            er_map.setdefault(high_scene, {})
            # detecting 11s in scene 12s
            print(f"\tnew home scene: {high_scene}")
            er_map[high_scene][detect_data] = exit_data
            if detect_data.exit_stage == 0x11:
                new_detect = detect_data.copy()
                new_detect.set_exit_stage(0x12)
                er_map[high_scene][new_detect] = exit_data

        if detect_data.exit_stage == 0x11:
            new_detect = detect_data.copy()
            new_detect.set_exit_stage(0x12)
            print(f"\tnew detect scene: {new_detect} {new_detect.entrance} {new_detect.exit}")
            # detect scene turns to 12
            er_map[scene][new_detect] = exit_data

        # Leaving a travelling ship can make your detect entrance any quadrant
        if detect_data.exit[2] == 0xFA:
            for i in range(4):
                new_detect = detect_data.copy()
                new_detect.set_exit_room(i)
                print(f"\tnew detect scene: {new_detect} {new_detect.entrance} {new_detect.exit}")
                er_map[scene][new_detect] = exit_data

        return er_map

    async def lower_water(self, ctx):
        if await read_memory_value(ctx, 0x1B5582, silent=True) & 0x4:
            print(f"Water has been lowered...")
            for scene, data in self.er_map.items():
                for detect_data, exit_data in data.items():
                    if exit_data.stage == 0x11:
                        exit_data.set_stage(0x12)
                        self.er_map[scene][detect_data] = exit_data
            self.lowered_water = True

    async def conditional_er(self, ctx, exit_data) -> bool:
        print(f"\tcond. {exit_data.name} {exit_data.extra_data} lowered water: {self.lowered_water}")
        if "conditional" in exit_data.extra_data:
            # Bounce back if the entrance connects to a lower room
            if ("ruins_water" in exit_data.extra_data["conditional"] and not self.lowered_water
                    and exit_data.room < 0x9):
                logger.info(f"This entrance is flooded (Isle of Ruins)")
                return False
            # Can't enter the sea without the correct chart
            print(f"{exit_data.extra_data['conditional']}, {exit_data.stage}, {ctx.slot_data['boat_requires_sea_chart']}")
            if "need_sea_chart" in exit_data.extra_data["conditional"] and exit_data.stage == 0 and ctx.slot_data["boat_requires_sea_chart"]:
                quadrant = exit_data.room
                chart = SEA_CHARTS[quadrant]
                print(f"chart: {chart} {item_count(ctx, chart)}")
                if not item_count(ctx, chart):
                    logger.info(f"Missing correct sea chart ({chart})")
                    return False
        return True

    async def conditional_bounce(self, ctx, scene, entrance) -> "PHTransition" or None:
        if scene in [0, 1, 2, 3] and ctx.slot_data["boat_requires_sea_chart"]:
            chart = SEA_CHARTS[scene]
            if not item_count(ctx, chart):
                for e in self.entrances.values():
                    if e.detect_exit_scene(scene, entrance):
                        logger.info(f"Missing correct sea chart ({chart})")
                        return e

        return None

    async def update_stored_entrances(self, ctx: "BizHawkClientContext"):
        self.visited_entrances.clear()
        storage_key = f"ph_checked_entrances_{ctx.slot}_{ctx.team}"
        stored_entrances = await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [storage_key],
            }])
        print(f"fetched datapackage: {stored_entrances}")
        if stored_entrances:
            self.visited_entrances = set(stored_entrances)

    # UT store entrances to remove
    async def store_visited_entrances(self, ctx: "BizHawkClientContext", detect_data, exit_data):
        old_visited_entrances = self.visited_entrances.copy()
        storage_key = f"ph_checked_entrances_{ctx.slot}_{ctx.team}"
        self.visited_entrances.add(detect_data.id)
        self.visited_entrances.add(exit_data.id)
        print(f"visited: {self.visited_entrances} old {old_visited_entrances}")
        print(f"sending entrances: {self.visited_entrances-old_visited_entrances}")
        if len(old_visited_entrances) != len(self.visited_entrances):
            await self.store_data(ctx, storage_key, self.visited_entrances-old_visited_entrances)

    @staticmethod
    async def store_data(ctx: "BizHawkClientContext", key, data):
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": key,
            "default": set(),
            "operations": [{"operation": "update", "value": list(data)}]
        }])

    def write_respawn_entrance(self, exit_data: "PHTransition"):
        # If ER:ing to sea, set respawn entrance to where you came from cause that doesn't change by itself when warping
        if exit_data.stage == 0:
            return [(0x1B2F12, [exit_data.room, exit_data.entrance[2]], "Main RAM")]
        return []

    # fixes conflict with bizhawk_UT
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        await super().game_watcher(ctx)

    def update_boss_warp(self, ctx, stage, scene_id):
        if stage in range(42, 49) or scene_id in [0x1F06, 0x2106, 0x200A]:  # Boss rooms
            reverse_exit = BOSS_WARP_SCENE_LOOKUP[scene_id]
            reverse_exit_id = self.entrances[reverse_exit].id
            pair = ctx.slot_data["er_pairings"][f"{reverse_exit_id}"]
            self.boss_warp_entrance = self.entrance_id_to_entrance[pair]

            # If last room was a dungeon, warp to dungeon entrance
            dungeon_exit = BOSS_WARP_LOOKUP.get(self.boss_warp_entrance.stage, None)
            if dungeon_exit:
                self.boss_warp_entrance = self.entrances[dungeon_exit]

        print(f"Warp Stage: {stage}, last: {self.last_warp_stage}, current warp {self.boss_warp_entrance}")
        return self.boss_warp_entrance

    def dungeon_hints(self, ctx):
        res = []
        print(f"testing for dungeon hints")

        # Send boss reward hints
        if ctx.slot_data["dungeon_hint_type"] == 2:
            print(f"Boss reward locations: {ctx.slot_data.get('required_dungeon_locations', [])}")
            for loc in ctx.slot_data.get("required_dungeon_locations", []):
                res.append(self.location_name_to_id[loc])
        elif ctx.slot_data["dungeon_hint_type"] == 1:
            dungeons = ctx.slot_data["required_dungeons"]
            if dungeons:
                logger.info(f"Your required dungeons are:")
                for d in dungeons:
                    logger.info(f"    {d}")
            else:
                logger.info(f"You have no required dungeons.")

        # Send excluded dungeon hints
        if ctx.slot_data["excluded_dungeon_hints"]:
            dungeons = ctx.slot_data["required_dungeons"]
            excluded = [d for d in DUNGEON_NAMES[2:] if d not in dungeons]
            if excluded:
                logger.info(f"Your excluded dungeons are:")
                for d in excluded:
                    logger.info(f"    {d}")
            else:
                logger.info(f"You have no excluded dungeons.")

        return res

    async def check_location_post_processing(self, ctx, location):
        if location is not None and "do_special" in location:
            if location["do_special"] == "keylock":
                print(f"Got item in Mountain passage: {ctx.items_received[-1]}")
                self.item_location_combo = location
            if location["do_special"] == "ut_event":
                key = f"ph_ut_events_{ctx.slot}_{ctx.team}"
                print(f"got ut_event location for key {key} loc {location['name']}")
                if location["name"] == "TotOK 1F SW Sea Chart Chest":
                    await self.store_data(ctx, key, ["1f"])