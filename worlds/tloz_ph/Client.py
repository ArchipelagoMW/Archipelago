from random import randint
from .DSZeldaClient.DSZeldaClient import *
from .DSZeldaClient.subclasses import (get_address_from_heap, storage_key, get_stored_data, AddrFromPointer)
from .data.Items import ITEMS
from .MapWarp import map_mode
from .data.Entrances import entrance_id_to_entrance
from .data.DynamicEntrances import DYNAMIC_ENTRANCES_BY_SCENE

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from .Subclasses import PHTransition

EQUIP_TIMER_OFFSET = 0x20

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 0x268

# Addresses to read each cycle
read_keys_always = [PHAddr.game_state, PHAddr.in_cutscene, PHAddr.loading_room,
                    PHAddr.received_item_index, PHAddr.slot_id,
                    PHAddr.stage, PHAddr.room, PHAddr.entrance,
                    PHAddr.in_short_cs, PHAddr.opened_clog, PHAddr.saving
                     ]

read_keys_deathlink = []
read_keys_land = [PHAddr.getting_location, PHAddr.getting_ship_part, PHAddr.in_map]
read_keys_sea = [PHAddr.shot_frog, PHAddr.boat_health, PHAddr.drawing_sea_route]
read_keys_salvage = [PHAddr.salvage_health]

# datastore_keys
checked_key = "ph_checked_entrances"
disconnect_key = "ph_disconnect_entrances"
traversal_key = "ph_traversed_entrances"
ut_events_key = "ph_ut_events"
ut_exclude_key = "ph_keylocking"
save_scene_key = "ph_save_scene"
visited_scenes_key = "ph_visited_scenes"

class PhantomHourglassClient(DSZeldaClient):
    game = "The Legend of Zelda - Phantom Hourglass"
    system = "NDS"

    def __init__(self) -> None:
        super().__init__()
        # Required variables from inherit
        self.starting_flags = STARTING_FLAGS
        self.dungeon_key_data = DUNGEON_KEY_DATA
        self.slot_id_addr = PHAddr.slot_id
        self.received_item_index_addr = PHAddr.received_item_index
        self.starting_entrance = (11, 3, 5)  # stage, room, entrance
        self.scene_addr = (PHAddr.stage, PHAddr.room, PHAddr.floor, PHAddr.entrance)  # Stage, room, floor, entrance
        self.exit_coords_addr = (PHAddr.transition_x, PHAddr.transition_y, PHAddr.transition_z)  # x, y, z. what coords to spawn link at when entering a
        self.dynamic_entrances_by_scene = DYNAMIC_ENTRANCES_BY_SCENE
        # continuous transition
        self.er_y_offest = 164  # In ph i use coords who's y is 164 off the entrance y
        self.stage_flag_offset = STAGE_FLAGS_OFFSET
        self.hint_data = HINT_DATA
        self.entrances = ENTRANCES
        self.item_data = ITEMS

        # Ph variables
        self.goal_room = 0x3600
        self.goal_event_connect = None
        self.sent_goal = False
        self.last_treasures = 0
        self.last_potions = [0, 0]
        self.last_ship_parts = []
        self.at_sea = False
        self.lowered_water = False
        self.visited_entrances = set()
        self.redisconnected_entrances = set()
        self.checked_entrances = set()

        self.boss_warp_entrance = None
        self.last_warp_stage = None
        self.item_location_combo = None

        self.sent_event = False
        self.event_reads = []
        self.event_data = []
        self.last_saved_scene = None
        self.lss_retry_attempts = 4
        self.death_check = False
        self.death_precision = None
        self.health_address: "Address" = PHAddr.null
        self.last_health_pointer = 0
        self.save_spam_protection = False
        self.death_warning_spam_protect = False

        # Map warp vars
        self.map_mode: bool = False  # if in warp menu
        self.map_warp: "PHTransition" or None = None  # destination entrance
        self.map_warp_reselector: bool = True  # Spam prevention
        self.pen_mode_pointer = None
        self.last_pen_mode = 0x18

        self.addr_game_state = PHAddr.game_state
        self.addr_slot_id = PHAddr.slot_id
        self.addr_stage = PHAddr.stage
        self.addr_room = PHAddr.room
        self.addr_entrance = PHAddr.entrance
        self.addr_received_item_index = PHAddr.received_item_index


    async def check_game_version(self, ctx: "BizHawkClientContext") -> bool:
        rom_name_bytes = (await PHAddr.game_identifier.read_bytes(ctx))[0]
        print(f"{rom_name_bytes}")
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
        write_list = PHAddr.received_item_index.get_write_list(0)

        # Reset starting time for PH
        write_list += PHAddr.phantom_hourglass_max.get_write_list(0)

        # Set Frog flags if not randomizing frogs
        if ctx.slot_data["randomize_frogs"] == 1:
            write_list += [a.get_inner_write_list(v) for a, v in STARTING_FROG_FLAGS]
        # Set Fog Flags
        fog_bits = FOG_SETTINGS_FLAGS[ctx.slot_data["fog_settings"]]
        if len(fog_bits) > 0:
            write_list += [a.get_inner_write_list(v) for a, v in fog_bits]
        if ctx.slot_data["skip_ocean_fights"] == 1:
            write_list += PHAddr.adv_flags_22.get_write_list(0x84)
        # Ban player from harrow if not randomized
        if ctx.slot_data["randomize_harrow"] == 0:
            write_list += PHAddr.adv_flags_30.get_write_list(0x18)

        # Print starting hints
        if ctx.slot_data["dungeon_hint_location"] == 0:
            self.dungeon_hints(ctx)

        # Start with sea maps if map warping
        if ctx.slot_data["map_warp_options"]:
            write_list += PHAddr.inventory_5.get_write_list(0x1F)

        print(f"ssf write list: {write_list}")
        return write_list

    async def get_coords(self, ctx, multi=False):
        coords = await read_multiple(ctx, self.get_coord_address(multi=multi), signed=True)
        if not multi:
            return {
                "x": coords.get(PHAddr.link_x, coords.get(PHAddr.boat_x)),
                "y": coords.get(PHAddr.link_y, 0),
                "z": coords.get(PHAddr.link_z, coords.get(PHAddr.boat_z, 0))
            }
        return coords

    def update_metal_count(self, ctx):
        metal_ids = [self.item_data[i].id for i in ITEM_GROUPS["Metals"]]
        self.metal_count = sum(1 for i in ctx.items_received if i.item in metal_ids)

    async def update_treasure_tracker(self, ctx):
        self.last_treasures = await PHAddr.all_treasure_count.read(ctx)
        # print(f"Treasure Tracker! {split_bits(self.last_treasures, 8)}")

    async def give_random_treasure(self, ctx):
        address = AddrFromPointer(PHAddr.pink_coral_count + randint(0, 7))
        await address.add(ctx, 1)
        await self.update_treasure_tracker(ctx)
        logger.info(f"Got random treasure from farmable location.")

    async def update_potion_tracker(self, ctx):
        reads = await read_multiple(ctx, [PHAddr.potion_left, PHAddr.potion_right])
        self.last_potions = list(reads.values())

    def get_coord_address(self, at_sea=None, multi=False) -> list["Address"]:
        if not multi:
            at_sea = self.at_sea if at_sea is None else at_sea
            if at_sea:
                return [PHAddr.boat_x, PHAddr.boat_z]
            elif not at_sea:
                return [PHAddr.link_x, PHAddr.link_y, PHAddr.link_z]
        return [PHAddr.link_x, PHAddr.link_y, PHAddr.link_z, PHAddr.boat_x, PHAddr.boat_z]

    async def update_main_read_list(self, ctx, stage, in_game=True):
        read_keys = read_keys_always.copy()
        death_link_pointer = None
        if stage is not None:
            if stage == 0:
                read_keys += read_keys_sea
                self.health_address = PHAddr.boat_health
                self.at_sea = True
            elif stage == 3:
                # Add separate reads for instant-repairs
                read_keys += read_keys_salvage
                self.health_address = PHAddr.salvage_health
            else:
                read_keys += read_keys_land
                if in_game:
                    death_link_pointer = (PHAddr.gPlayer, 0xa)
                self.at_sea = False

            if death_link_pointer:
                addr, offset = death_link_pointer
                pointer_1 = await addr.read(ctx)
                self.health_address = AddrFromPointer(pointer_1 + offset - 0x2000000, size=2, name="link_health")
                self.last_health_pointer = pointer_1
                read_keys.append(self.health_address)
            print(f"Health Address = {self.health_address}")
            self.main_read_list = read_keys
        else:
            self.at_sea = None
        return self.main_read_list

    async def full_heal(self, ctx, bonus=0):
        if not self.at_sea:
            hearts = self.item_count(ctx, "Heart Container") + 3 + bonus
            print(f"Sent full heal hearts {hearts} addr {self.health_address}")
            await self.health_address.overwrite(ctx, hearts * 4)

    async def refill_ammo(self, ctx, text=""):
        items = [i + " (Progressive)" for i in ["Bombs", "Bombchus", "Bow"]]

        # Count upgrades
        counts = {self.item_data[i].id: 0 for i in items}
        for i in ctx.items_received:
            for k in counts:
                if k == i.item:
                    counts[k] += 1

        # Write Upgrades
        write_list = []
        for i, count in enumerate(counts.values()):
            data = self.item_data[items[i]]
            write_list += data.ammo_address.get_write_list(data.give_ammo[count - 1])
        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        await self.full_heal(ctx)
        if text == "milk_bar":
            logger.info(f"You drink a glass of milk. You feel refreshed, and your ammo has been refilled.")

    def get_progress(self, ctx, scene=0):
        # Count current metals
        self.update_metal_count(ctx)

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
            logger.info(f"You have {self.metal_count} out of {required} rare metals. There are {total} metals in total.\n"
                        f"Finding the metals {bellum_texts[ctx.slot_data['bellum_access']]}")
        elif scene == 0x160A:
            zauz_required = ctx.slot_data["zauz_required_metals"]
            logger.info(f"Zauz needs {zauz_required} rare metals to give an item. You have {self.metal_count}/{total} metals.")

    def process_loading_variable(self, read_result) -> bool:
        return read_result[PHAddr.loading_room] == 0xEE

    async def process_read_list(self, ctx: "BizHawkClientContext", read_result: dict):
        # This go true when link gets item
        if self.at_sea:
            self.getting_location = read_result.get(PHAddr.shot_frog, False)
        else:
            self.getting_location = (read_result.get(PHAddr.getting_location, 0) & 0x20
                                     or read_result.get(PHAddr.getting_ship_part, False))

    async def process_on_room_load(self, ctx, current_scene, read_result: dict):
        self.prev_rupee_count = await PHAddr.rupee_count.read(ctx)
        await self.update_potion_tracker(ctx)
        await self.update_treasure_tracker(ctx)

    async def process_in_game(self, ctx: "BizHawkClientContext", read_result: dict):
        # Detect lowering of water and update ER Map
        if not self.lowered_water and self.current_stage == 0x24:
            await self.lower_water(ctx, True)
        await self.detect_ut_event(ctx, self.current_scene)

        if self.current_stage == 3 and read_result.get(PHAddr.salvage_health, 5) <= 1:
            await self.instant_repair_salvage_arm(ctx)

        if read_result.get(PHAddr.saving) == 0x46 and not self.save_spam_protection:
            print(f"Saving scene {hex(self.current_scene)}")
            self.last_saved_scene = self.current_scene
            await self.store_data(ctx, storage_key(ctx, save_scene_key), self.last_saved_scene, "replace", default=0)
            self.save_spam_protection = True

        # Map warp entrypoint
        if read_result.get(PHAddr.in_map, 0):
            await map_mode(self, ctx, read_result)
        elif self.map_mode:
            self.map_mode = False
            self.map_warp = None
            self.map_warp_reselector = True
            logger.info(f"Illegal map menu exit, canceling all map warps")
        if self.warp_to_start_flag and self.map_warp:
            self.map_warp = None
            logger.info(f"Canceled map warp due to starting a warp to start")
        if self.map_warp and self.is_dead:
            self.map_warp = None
            logger.info(f"Map warp canceled due to death")

        if self.is_dead and ctx.slot_data["shuffle_bosses"] and self.current_scene in BOSS_WARP_SCENE_LOOKUP and not self.death_warning_spam_protect:
            if read_result[PHAddr.in_cutscene]:
                logger.info(f"WARNING! Clicking continue in a boss room will put you out of logic. Please save and quit before continuing.")
            self.death_warning_spam_protect = True
        elif not self.is_dead:
            self.death_warning_spam_protect = False


    async def detect_warp_to_start(self, ctx, read_result: dict):
        # Opened clog warp to start check
        if read_result.get(PHAddr.opened_clog, False):
            if await PHAddr.flipped_clog.read(ctx, silent=True) & 1:
                if not self.warp_to_start_flag:
                    logger.info(f"Primed a warp to start. Enter a transition to warp to {STAGES[0xB]}.")
                    self.warp_to_start_flag = True
            else:
                if self.warp_to_start_flag:
                    logger.info("Canceled warp to start.")
                    self.warp_to_start_flag = False

        # Cancel warp to start if in a dangerous situation
        if self.warp_to_start_flag:
            # Cyclone slate warp to start crashes, prevent that from working
            if self.at_sea:
                if await PHAddr.using_cyclone_slate.read(ctx, silent=True) == 1:  # is 0x65 if never used cyclone slate
                    self.warp_to_start_flag = False
                    logger.info("Canceled warp to start, Cyclone Slate is not a valid warp method")
            if self.is_dead:
                self.warp_to_start_flag = False
                logger.info("Canceled warp to start, death is not a valid warp method")
            if self.starting_entrance[:2] == (self.current_stage, read_result[PHAddr.room]):
                logger.info(f"In starting scene, canceling warp to start")
                self.warp_to_start_flag = False

    async def enter_game(self, ctx):
        self.save_slot = await PHAddr.save_slot.read(ctx, silent=True)
        self.update_metal_count(ctx)
        self.set_ending_room(ctx)
        await self.lower_water(ctx)
        await PHAddr.text_speed.overwrite(ctx, 2)  # Set text speed to fast, no matter settings
        # Set treasure prices so they match seed (save file resets it on menu)
        await PHAddr.treasure_price_index.overwrite(ctx, ctx.slot_data.get("treasure_price_index", 0))
        await self.update_stored_entrances(ctx)

        # Set warp to start location
        if ctx.slot_data["shuffle_overworld_transitions"]:
            self.starting_entrance = (11, 0, 0)


    async def watched_intro_cs(self, ctx):
        watched_intro = await PHAddr.watched_intro.read(ctx, silent=True) & 2
        return watched_intro

    async def process_hard_coded_rooms(self, ctx, current_scene):
        self.sent_event = False  # Reset per-room UT events
        self.event_data = []
        self.event_reads = []
        self.save_spam_protection = False  # Reset save spam protection

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
            await self.refill_ammo(ctx, "milk_bar")

        # Oshus gives metal info
        if current_scene in [0xB0A, 0x160A]:
            self.get_progress(ctx, current_scene)

        # Shipyard gives ship parts
        if current_scene in [0xB0D]:
            await self.edit_ship(ctx)
        if current_scene in [0xB03]:
            await self.remove_ship_parts(ctx)

        if current_scene == 0x1401:  # Bannan chest needs to happen after load
            if await PHAddr.adv_flags_22.read(ctx) & 0x8:
                await PHAddr.wayfarer_chest.set_bits(ctx, 0x80)

        # Open pedestal doors. sucks that you can't trigger it with dynaflags. slow code but game is slower
        if ctx.slot_data.get("randomize_pedestal_items", 0) > 0:

            # === TotOK ===
            if current_scene == 0x2503:  # B3
                if self.item_count(ctx, "Force Gem (B3)") >= 3 or self.item_count(ctx, "Force Gems"):
                    await PHAddr.totok_b3_state.set_bits(ctx, [0xFE, 0x0F])
            elif current_scene == 0x250B:  # B8
                if (self.item_count(ctx, "Round Crystal (Temple of the Ocean King)")
                        or self.item_count(ctx, "Round Pedestal B8 (Temple of the Ocean King)")
                        or self.item_count(ctx, "Round Crystals")):
                    await PHAddr.totok_b3_state.set_bits(ctx, 0x2)
                if (self.item_count(ctx, "Triangle Crystal (Temple of the Ocean King)")
                        or self.item_count(ctx, "Triangle Crystals")
                        or self.item_count(ctx, "Triangle Pedestal B8 (Temple of the Ocean King)")):
                    await PHAddr.totok_b3_state.set_bits(ctx, 0x4)
            elif current_scene == 0x250C:  # B9
                if (self.item_count(ctx, "Round Crystal (Temple of the Ocean King)")
                        or self.item_count(ctx, "Round Pedestal B9 (Temple of the Ocean King)")
                        or self.item_count(ctx, "Round Crystals")):
                    await PHAddr.totok_b9_state.set_bits(ctx, 0x4)
                if (self.item_count(ctx, "Triangle Crystal (Temple of the Ocean King)")
                        or self.item_count(ctx, "Triangle Pedestal B9 (Temple of the Ocean King)")
                        or self.item_count(ctx, "Triangle Crystals")):
                    await PHAddr.totok_b9_state.set_bits(ctx, 0x8)
                if (self.item_count(ctx, "Square Crystal (Temple of the Ocean King)")
                        or self.item_count(ctx, "Square Crystals")):
                    await PHAddr.totok_b9_state.set_bits(ctx,  0x22)
                if self.item_count(ctx, "Square Pedestal West (Temple of the Ocean King)"):
                    await PHAddr.totok_b9_state.set_bits(ctx,  0x20)
                if self.item_count(ctx, "Square Pedestal Center (Temple of the Ocean King)"):
                    await PHAddr.totok_b9_state.set_bits(ctx,  0x2)
            elif current_scene == 0x2510:  # B12
                gem_count = self.item_count(ctx, "Force Gem (B12)") | self.item_count(ctx, "Force Gems")*3
                if gem_count >= 3:
                    await PHAddr.totok_b12_state.set_bits(ctx, [0xFE, 0x0F])
                elif gem_count == 2:
                    await PHAddr.totok_b12_state.set_bits(ctx, 0xC)
                elif gem_count == 1:
                    await PHAddr.totok_b12_state.set_bits(ctx, 0x8)
                # Remove ability to place force gems on southern pedestals
                await PHAddr.totok_b12_pedestal_left.overwrite(ctx, 0x9)
                await PHAddr.totok_b12_pedestal_right.overwrite(ctx, 0x9)

            # === Temple of Courage ===
            elif current_scene == 0x1E00:
                if (self.item_count(ctx, "Square Pedestal North (Temple of Courage)")
                        or self.item_count(ctx, "Square Crystal (Temple of Courage)")
                        or self.item_count(ctx, "Square Crystals")):
                    await PHAddr.toc_crystal_state.set_bits(ctx, 0x10)
                if (self.item_count(ctx, "Square Pedestal South (Temple of Courage)")
                        or self.item_count(ctx, "Square Crystal (Temple of Courage)")
                        or self.item_count(ctx, "Square Crystals")):
                    await self.stage_address.set_bits(ctx, 0x80)

            # === Ghost Ship ===
            elif current_scene == 0x2900:
                if (self.item_count(ctx, "Triangle Crystal (Ghost Ship)")
                        or self.item_count(ctx, "Triangle Crystals")):
                    await self.stage_address.set_bits(ctx, 0x8, offset=1)
                if (self.item_count(ctx, "Round Crystal (Ghost Ship)")
                        or self.item_count(ctx, "Round Crystals")):
                    await self.stage_address.set_bits(ctx, 0x2, offset=3)

    async def write_totok_midway_keys(self, ctx):
        data = DUNGEON_KEY_DATA[372]
        keys = await self.key_address.read(ctx)
        keys = keys * data["value"]
        keys = data["filter"] if keys > data["filter"] else keys
        await PHAddr.small_key_storage_2.set_bits(ctx, keys)
        await PHAddr.custom_storage.set_bits(ctx, 0x1)  # Set bit to write future TotOK keys to post midway

    @staticmethod
    async def repair_salvage_arm(ctx, scene=0x500):
        prev = await read_multiple(ctx, [PHAddr.global_salvage_health, PHAddr.rupee_count, PHAddr.custom_storage])
        repair_kits = (prev[PHAddr.custom_storage] & 0xE0) >> 5
        print(f"Repair kits: {repair_kits}")
        if prev[PHAddr.global_salvage_health] <= 2:
            write_list = []
            text = f"Repaired Salvage Arm for "
            if repair_kits > 0:
                write_list += PHAddr.custom_storage.get_write_list(prev[PHAddr.custom_storage] - 0x20)
                text += f"1 Salvage Repair Kit. You have {prev[PHAddr.custom_storage]} remaining."
            else:
                # Repair cost, doesn't care if you're out of rupees out of qol
                cost = 100 if prev[PHAddr.global_salvage_health] == 0 else (6 - prev[PHAddr.global_salvage_health]) * 10
                rupees = 0 if prev[PHAddr.rupee_count] - cost <= 0 else prev[PHAddr.rupee_count] - cost
                write_list += PHAddr.rupee_count.get_write_list(rupees)
                text += f"{cost} rupees."
            write_list += PHAddr.global_salvage_health.get_write_list(5)
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
        else:
            text = f"This room automatically repairs your Salvage Arm, for a cost or a kit, when at 2 health or below."
        # Send a client message about the repair
        logger.info(text)

    @staticmethod
    async def instant_repair_salvage_arm(ctx):
        salvage_data = await PHAddr.custom_storage.read(ctx, silent=True)
        salvage_kits = (salvage_data & 0xE0) >> 5
        if salvage_kits > 0:
            write_list = (PHAddr.custom_storage.get_write_list(salvage_data - 0x20) +
                          PHAddr.salvage_health.get_write_list(5) +
                          PHAddr.global_salvage_health.get_write_list(5))  # Global salvage health
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            logger.info(f"Salvage Arm instant-repaired. You have {salvage_kits - 1} Salvage Repair Kits remaining.")

    @staticmethod
    async def remove_ship_parts(ctx):
        ship_write_list = ([1] + [0] * 8) * 8
        await PHAddr.ship_part_counts.overwrite(ctx, ship_write_list)

    async def edit_ship(self, ctx):
        # Figure out what ships player has
        ships = [1] + [0]*8
        for i in ctx.items_received:
            item_id = i.item
            item_name = self.item_id_to_name[item_id]
            if "Ship:" in item_name:
                item_data = self.item_data[item_name]
                ships[item_data.ship] = 1
        # Give ship parts
        ship_write_list = [] + ships * 8
        print(ships, ship_write_list)
        await bizhawk.write(ctx.bizhawk_ctx, [(PHAddr.ship_part_counts.addr, ship_write_list, "Main RAM")])
        await PHAddr.custom_storage.set_bits(ctx, 2)

    # Dynamic flags/ Entrances
    async def has_special_dynamic_requirements(self, ctx, data) -> bool:
        # Special case of metals
        def check_metals(d):
            if "zauz_metals" in d or "goal_requirement" in d:
                self.update_metal_count(ctx)

                # Zauz Check
                if "zauz_metals" in d:
                    print(f"Metal check: {self.metal_count} metals out of {ctx.slot_data['zauz_required_metals']}")
                    if self.metal_count < ctx.slot_data["zauz_required_metals"]:
                        if d["zauz_metals"]:
                            return False
                    else:
                        if not d["zauz_metals"]:
                            return False

                # Goal Check
                if "goal_requirement" in d:
                    print(f"Metal check: {self.metal_count} metals out of {ctx.slot_data['required_metals']}")
                    return self.metal_count >= ctx.slot_data["required_metals"]
            return True

        # Beedle points
        def check_beedle_points(d):
            if not d.get("beedle_points", False):
                return True
            reference = {"Beedle Points (10)": 10,
                         "Beedle Points (20)": 20,
                         "Beedle Points (50)": 50}
            # Count points
            reference = {self.item_data[k].id: c for k, c in reference.items()}
            points = 0
            for i in ctx.items_received:
                if i.item in reference:
                    points += reference[i.item]
            print(f"Beedle points {d.get('beedle_points')} >= {points}")
            return points >= d.get('beedle_points', 300)

        def count_spirit_gems(d):
            if "count_gems" in d:
                pack_size = ctx.slot_data["spirit_gem_packs"]
                gem_count = self.item_count(ctx, f"{d['count_gems']} Gem Pack")
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
        print(f"Setting stage flags")
        self.stage_address = await get_address_from_heap(ctx, PHAddr.gMapManager, STAGE_FLAGS_OFFSET)
        self.key_address = AddrFromPointer(self.stage_address + SMALL_KEY_OFFSET)
        if stage in STAGE_FLAGS:
            flags = STAGE_FLAGS[stage]

            # Change certain stage flags based on options
            if stage == 0 and ctx.slot_data["skip_ocean_fights"] == 1:
                flags = SKIP_OCEAN_FIGHTS_FLAGS
            if stage == 41 and ctx.slot_data["logic"] >= 1:
                flags = SPAWN_B3_REAPLING_FLAGS

            print(f"\tSetting Stage flags for {STAGES[stage]}, "
                  f"adr: {self.stage_address}")
            await self.stage_address.set_bits(ctx, flags)

        # Unlock boss door if have bk
        data = BOSS_DOOR_DATA.get(stage, False)
        if data and ctx.slot_data.get("boss_key_behaviour", True):
            if self.item_count(ctx, f"Boss Key ({data['name']})"):
                await data["address"].set_bits(ctx, data["value"])

    # Enter stage
    async def enter_special_key_room(self, ctx, stage, scene_id) -> bool:
        if stage != 0x25:
            return False
        if scene_id in [0x2509, 0x250E]:
            await self.update_key_count(ctx, 372)
        elif scene_id in [0x2500, 0x2504]:
            return False  # Do normal enter TotOK operation, see update_special_key_count for key calc
        return True

    async def update_special_key_count(self, ctx, current_stage: int, new_keys, key_data: dict, key_values, key_address: "Address") -> tuple[int, bool]:
        if current_stage == 0x25:
            if self.location_name_to_id["TotOK 1F Sea Chart Chest"] in ctx.checked_locations:
                new_keys -= 1  # Opening the SW sea chart door uses a key permanently! No savescums!
            if self.current_scene == 0x2504:  # Set B3.5 key count
                new_keys -= 2
                if not self.item_count(ctx, "Grappling Hook") and ctx.slot_data["randomize_pedestal_items"] == 0:
                    new_keys -= 1
            return new_keys, False
        elif current_stage == 372:
            return new_keys, False
        return new_keys, True

    async def get_small_key_address(self, ctx) -> "Address":
        return await get_address_from_heap(ctx, PHAddr.gMapManager, SMALL_KEY_OFFSET)

    # Called during location processing to determine what vanilla item to remove
    async def unset_special_vanilla_items(self, ctx, location, item):
        # Multiple sword items don't detect each other by default
        if item in ["Oshus' Sword", "Phantom Sword"] and self.item_count(ctx, "Sword (Progressive)"):
            self.last_vanilla_item.pop()

        # Don't remove heart containers if already at max
        if item == "Heart Container" and self.item_count(ctx, item) >= 13:
            self.last_vanilla_item.pop()

        # Farmable locations don't remove vanilla
        if "farmable" in location and location["id"] in ctx.checked_locations:
            if item == "Ship Part":
                await self.give_random_treasure(ctx)
            else:
                self.last_vanilla_item.pop()
                logger.info(f"Got farmable location")

    async def receive_key_in_own_dungeon(self, ctx, item_name: str, write_keys_to_storage):
        # TotOK - adds to key increment if you get it in the dungeon, otherwise do as usual
        if "Temple of the Ocean King" in item_name:
            return [await write_keys_to_storage(37)]
        return []

    async def received_special_small_keys(self, ctx, item_name, write_keys_to_storage):
        # TotOK Midway special data
        res = []
        if item_name == "Small Key (Temple of the Ocean King)":
            res.append(await write_keys_to_storage(37))
            if await PHAddr.custom_storage.read(ctx) & 0x1:
                res.append(await write_keys_to_storage(372))
        return res

    async def received_special_incremental(self, ctx, item_data) -> int:
        # Sand of hours check
        _value = 0
        if "Sand" in item_data.value:

            if item_data.value == "Sand":
                if not ctx.slot_data["ph_required"] or self.item_count(ctx, "Phantom Hourglass"):
                    _value = ctx.slot_data["ph_time_increment"] * 60
                else:
                    _value = 0
            elif item_data.value == "Sand PH":
                _value = ctx.slot_data["ph_starting_time"] * 60

                # If ph is required, add all time so far on finding
                if ctx.slot_data["ph_required"] and self.item_count(ctx, "Phantom Hourglass") < 2:
                    _value += (ctx.slot_data["ph_time_increment"] * 60 * self.item_count(ctx, "Sand of Hours")
                              + self.item_count(ctx, "Sand of Hours (Small)") * 3600
                              + self.item_count(ctx, "Sand of Hours (Boss)") * 7200)
            else:
                _value = item_data.value
            last_time = await item_data.address.read(ctx)
            if last_time + _value > 359940:
                print(f"Time: Last time {last_time} value {_value} new {359940 - last_time} max {359940}")
                _value = 359940 - last_time
            print(f"Sand stage {self.current_stage} {_value}")
            if self.current_stage == 0x25:
                await PHAddr.phantom_hourglass_current.add(ctx, _value)

        elif item_data.value == "pack_size":
            _value = ctx.slot_data["spirit_gem_packs"]
        else:
            raise ValueError(f"Special item value {item_data.value} is not supported")
        return _value

    async def receive_item_post_processing(self, ctx, item_name, item_data):
        # If treasure, update treasure tracker
        if hasattr(item_data, "inventory_id"):
            await self.enable_items(ctx, item_data.inventory_id)
        if "treasure" in item_data.tags:
            await self.update_treasure_tracker(ctx)
        if "Potion" in item_name:
            await self.update_potion_tracker(ctx)
        # If hint on receive, send hint (currently only treasure maps)
        if hasattr(item_data, "hint_on_receive"):
            if ctx.slot_data["randomize_salvage"] == 1:
                await self.scout_location(ctx, item_data.hint_on_receive)
        # Increment metal count
        if item_name in ITEM_GROUPS["Metals"]:
            self.metal_count += 1
            await self.process_game_completion(ctx)

        exclude_key = storage_key(ctx, ut_exclude_key)
        # Exclude forced vanilla items on not needing them any more
        if item_name == "Grappling Hook" and ctx.slot_data.get("randomize_pedestal_items", 0) in [0, 1]:
            print(f"TotOK B3 has no more useful force gems")
            data = [self.location_name_to_id[i] for i in LOCATION_GROUPS["Grappling Hook Excludes"]]
            await self.store_data(ctx, exclude_key, data)

        # Run code if you got a certain item from a certain location
        if self.item_location_combo:
            if "Mountain Passage" in self.item_location_combo["name"]:
                if ctx.slot_data["keysanity"] < 2 and "Small Key" not in item_name and ctx.slot_data["shuffle_caves"] == 0:
                    print(f"Mountain Passage has no more useful items")
                    data = [self.location_name_to_id[i] for i in LOCATION_GROUPS["Mountain Passage"]]
                    await self.store_data(ctx, exclude_key, data)

            self.item_location_combo = None

        if hasattr(item_data, "set_bit_in_room") and ctx.slot_data.get("randomize_pedestal_items", 0):
            print(f"Trying to set bit in room, room {hex(self.current_scene)}")
            if self.current_scene in item_data.set_bit_in_room:
                for addr, _value, *args in item_data.set_bit_in_room[self.current_scene]:
                    print(f"args {args}")
                    if addr == "stage_flag":
                        addr = self.stage_address
                        print(f"Stage address: {addr}")
                    if args and "count" in args[0]:
                        if self.item_count(ctx, item_name) < args[0]["count"]:
                            continue
                    if isinstance(_value, int):
                        _value = [_value]
                    await addr.set_bits(ctx, _value)

        # disconnect port entrances
        if ctx.slot_data.get("ut_blocked_entrances_behaviour", 0) == 2 and ctx.slot_data["boat_requires_sea_chart"] and hasattr(item_data, "disconnect_entrances"):
            disconnects_ids = [ENTRANCES[e].id for e in item_data.disconnect_entrances if str(ENTRANCES[e].id) in ctx.slot_data["er_pairings"]]
            await self.redisconnect(ctx, disconnects_ids)

    async def redisconnect(self, ctx, data):
        reciprocals = [ctx.slot_data["er_pairings"][str(i)] for i in data if
                       str(i) in ctx.slot_data["er_pairings"]]
        all_ids = set(data + reciprocals) if not ctx.slot_data["decouple_entrances"] else set(reciprocals)

        # Don't disconnect still blocked entrances
        for i in reciprocals:
            if not await self.conditional_er(ctx, entrance_id_to_entrance[i], silent=True):
                print(f"not redisconnecting blocked entrance {entrance_id_to_entrance[i].name}")
                all_ids.remove(i)
                if not ctx.slot_data["decouple_entrances"]:
                    print(f"\treciprocal{entrance_id_to_entrance[ctx.slot_data['er_pairings'][str(i)]].name}")
                    all_ids.remove(ctx.slot_data["er_pairings"][str(i)])
        # Don't disconnect undiscovered entrances
        self.checked_entrances |= set(get_stored_data(ctx, checked_key, set()))
        for i in all_ids.copy():
            if i not in self.checked_entrances:
                print(f"not redisconnecting unfound entrance: {entrance_id_to_entrance[i].name}")
                all_ids.remove(i)

        print(f"Redisconnecting {[self.entrance_id_to_entrance[i].name for i in all_ids]}")
        # store redisconnects
        key = storage_key(ctx, disconnect_key)
        self.redisconnected_entrances |= set(get_stored_data(ctx, disconnect_key, set()))
        await self.store_data(ctx, key, all_ids)
        self.redisconnected_entrances.update(all_ids)

    @staticmethod
    async def enable_items(ctx: "BizHawkClientContext", inventory_id: int):
        equipped_item_pointer = AddrFromPointer(await PHAddr.gItemManager.read(ctx)-0x02000000, size=4)
        equipped_item = await equipped_item_pointer.read(ctx, silent=True)
        if equipped_item == 0xffffffff:
            print(f"Items menu not visible, enabling: {hex(equipped_item_pointer + EQUIP_TIMER_OFFSET)}")
            # Enable items menu
            equipped_item_timer = AddrFromPointer(equipped_item_pointer + EQUIP_TIMER_OFFSET, size=2)
            await equipped_item_timer.overwrite(ctx, 20)
            await equipped_item_pointer.overwrite(ctx, inventory_id)

    def set_ending_room(self, ctx):
        if ctx.slot_data["goal_requirements"] == 0:
            self.goal_room = 0x2509
            if ctx.slot_data["ut_events"] > 0:
                self.goal_event_connect = ENTRANCES["GOAL: Triforce Door"]
        elif ctx.slot_data["bellum_access"] < 4:
            self.goal_room = 0x3600
            if ctx.slot_data["ut_events"] > 0:
                self.goal_event_connect = ENTRANCES["GOAL: Bellumbeck"]

    async def process_game_completion(self, ctx: "BizHawkClientContext"):
        current_scene = self.read_result[PHAddr.stage] * 0x100 + self.read_result[PHAddr.room]
        game_clear = False
        current_scene = current_scene * 0x100 if current_scene < 0x100 else current_scene  # ???
        if ctx.slot_data["bellum_access"] == 4:
            game_clear = self.metal_count >= ctx.slot_data["required_metals"]
            if game_clear and not self.sent_goal:
                await self.store_visited_entrances(ctx, ENTRANCES["GOAL"], ENTRANCES["GOAL"].vanilla_reciprocal)
                self.sent_goal = True
        else:
            game_clear = current_scene == self.goal_room  # Enter End Credits
            if game_clear and self.goal_event_connect and not self.sent_goal:
                await self.store_visited_entrances(ctx, self.goal_event_connect, self.goal_event_connect.vanilla_reciprocal)
                self.sent_goal = True
        return game_clear

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage, read_result):
        if (not read_result.get(PHAddr.drawing_sea_route, False) and read_result[PHAddr.in_cutscene]
                and self.current_scene not in [0x1701]):
            if ctx.last_death_link > self.last_deathlink and not is_dead:
                # A death was received from another player, make our player die as well
                await self.health_address.overwrite(ctx, 0)

                self.is_expecting_received_death = True
                self.last_deathlink = ctx.last_death_link

            if not self.was_alive_last_frame and not is_dead:
                # We revived from any kind of death
                self.was_alive_last_frame = True
            elif self.was_alive_last_frame and is_dead:
                # Our player just died...
                if stage not in [0, 3]:
                    health_pointer = await PHAddr.gPlayer.read(ctx)
                    if self.last_health_pointer != health_pointer:
                        print(f"Deathlink triggered with wrong health pointer. Updating main read list")
                        await self.update_main_read_list(ctx, stage, True)
                        return

                self.was_alive_last_frame = False
                print(f"health address: {self.health_address}")
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

    async def lower_water(self, ctx, allow_redisconnect=False):
        if await PHAddr.lower_water.read(ctx, silent=True) & 0x4:
            print(f"Water has been lowered...")
            for scene, data in self.er_map.items():
                for detect_data, exit_data in data.items():
                    if exit_data.stage == 0x11:
                        exit_data.set_stage(0x12)
                        self.er_map[scene][detect_data] = exit_data
            if allow_redisconnect and not self.lowered_water and ctx.slot_data.get("ut_blocked_entrances_behaviour", 0) == 2:
                print(f"Allowing redisconnect")
                water_entrances = [i.id for i in ENTRANCES.values() if "ruins_water" in i.extra_data.get("conditional", [])]
                await self.redisconnect(ctx, water_entrances)

            self.lowered_water = True

    async def detect_ut_event(self, ctx, scene):
        """
        Send UT event locations on certain flags being set in certain scenes.
        """
        if scene in UT_EVENT_DATA and not self.sent_event:
            if not self.event_reads:
                data = UT_EVENT_DATA[scene]
                data = [data] if isinstance(data, dict) else data
                self.event_data = data
                for i, event in enumerate(data):
                    address = AddrFromPointer(self.stage_address + event.get("offset", 0), size=event.get("size", 1)) if event["address"] == "stage_flags" else event["address"]
                    print(f"event data {self.event_data}")
                    self.event_data[i]["address"] = address
                    print(f"event data {self.event_data}")
                    self.event_reads.append(address)

            read_results = await read_multiple(ctx, self.event_reads)
            for event, res in zip(self.event_data, read_results.values()):
                if event["value"] & res:
                    if "entrance" in event:
                        print(f"Event detection Success!, {event['entrance']}")
                        entrance = ENTRANCES[event["entrance"]]
                        await self.store_visited_entrances(ctx, entrance, entrance.vanilla_reciprocal)
                    elif "event" in event:
                        print(f"Event detection Success!, {event['event']}")
                        key = storage_key(ctx, ut_events_key)
                        await self.store_data(ctx, key, [event["event"]])

                    self.event_reads.remove(event["address"])
                    self.event_data.remove(event)
            if not self.event_data:
                print(f"All events sent!")
                self.sent_event = True

        else:
            self.sent_event = True

    async def conditional_er(self, ctx, exit_data, silent=False) -> bool:
        print(f"\tcond. {exit_data.name} {exit_data.extra_data} lowered water: {self.lowered_water}")
        if "conditional" in exit_data.extra_data:
            # Bounce back if the entrance connects to a lower room
            if "ruins_water" in exit_data.extra_data["conditional"] and not self.lowered_water:
                if not silent: logger.info(f"This entrance is flooded (Isle of Ruins)")
                return False
            # Can't enter the sea without the correct chart
            print(f"{exit_data.extra_data['conditional']}, {exit_data.stage}, {ctx.slot_data['boat_requires_sea_chart']}")
            if "need_sea_chart" in exit_data.extra_data["conditional"] and exit_data.stage == 0 and ctx.slot_data["boat_requires_sea_chart"]:
                quadrant = exit_data.room
                chart = SEA_CHARTS[quadrant]
                print(f"chart: {chart} {self.item_count(ctx, chart)}")
                if not self.item_count(ctx, chart):
                    if not silent: logger.info(f"Missing correct sea chart ({chart})")
                    return False
        return True

    async def conditional_bounce(self, ctx, scene, entrance) -> "PHTransition" or None:
        if scene in [0, 1, 2, 3] and ctx.slot_data["boat_requires_sea_chart"]:
            chart = SEA_CHARTS[scene]
            if not self.item_count(ctx, chart):
                for e in self.entrances.values():
                    if e.detect_exit_scene(scene, entrance):
                        logger.info(f"Missing correct sea chart ({chart})")
                        return e

        return None

    async def update_stored_entrances(self, ctx: "BizHawkClientContext"):
        self.visited_entrances.clear()
        self.redisconnected_entrances.clear()
        self.visited_scenes.clear()
        self.checked_entrances.clear()
        await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [storage_key(ctx, disconnect_key),
                         storage_key(ctx, traversal_key),
                         storage_key(ctx, visited_scenes_key),
                         storage_key(ctx, checked_key)],
            }])

    # UT store entrances to remove
    async def store_visited_entrances(self, ctx: "BizHawkClientContext", detect_data, exit_data, interaction="traverse"):
        self.visited_entrances |= set(get_stored_data(ctx, traversal_key, set()))
        old_visited_entrances = self.visited_entrances.copy()
        new_data = {detect_data.id, exit_data.id} if not ctx.slot_data["decouple_entrances"] and detect_data.two_way else {detect_data.id}
        print(f"New Storage Data: {new_data} {ctx.slot_data['decouple_entrances']}")

        if interaction == "traverse" or ctx.slot_data.get("ut_blocked_entrances_behaviour", 1) == 0:
            key = storage_key(ctx, traversal_key)
            self.visited_entrances.update(new_data)
            new_data = self.visited_entrances-old_visited_entrances
        elif interaction == "check":
            key = storage_key(ctx, checked_key)
            self.checked_entrances.update(new_data)
        else:
            raise ValueError(f"store_visited_entrances() had an unhandled interaction value {interaction}")

        if new_data:
            await self.store_data(ctx, key, new_data)


    def write_respawn_entrance(self, exit_data: "PHTransition"):
        # If ER:ing to sea, set respawn entrance to where you came from cause that doesn't change by itself when warping
        if exit_data.stage == 0:
            return PHAddr.boat_respawn.get_write_list([exit_data.room, exit_data.entrance[2]])
        return []

    # fixes conflict with bizhawk_UT
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        await super().game_watcher(ctx)

    def update_boss_warp(self, ctx, stage, scene_id):
        if scene_id in BOSS_WARP_SCENE_LOOKUP:  # Boss rooms
            reverse_exit = BOSS_WARP_SCENE_LOOKUP[scene_id]
            reverse_exit_id = self.entrances[reverse_exit].id
            pair = ctx.slot_data["er_pairings"].get(f"{reverse_exit_id}", None)
            if pair is None:
                print(f"Boss Entrance not Randomized")
                return None
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
                key = storage_key(ctx, ut_events_key)
                print(f"got ut_event location for key {key} loc {location['name']}")
                if location["name"] == "TotOK 1F Sea Chart Chest":
                    await self.store_data(ctx, key, ["1f"])
            if isinstance(location["do_special"], dict):
                event_type = location["do_special"].get("event_type", None)
                if event_type == "ut_connect":
                    event_name = location["do_special"]["event_name"]
                    entr = ENTRANCES[event_name]
                    await self.store_visited_entrances(ctx, entr, entr.vanilla_reciprocal)

    async def ut_bounce_scene(self, ctx, scene):
        if not ctx.slot_data["shuffle_houses"] and map_type_lookup.get(scene) == "house":
            print(f"Not map switching due to house: {hex(scene)}")
            return
        if not ctx.slot_data["shuffle_caves"] and map_type_lookup.get(scene) == "cave":
            print(f"Not map switching due to cave: {hex(scene)}")
            return
        if map_type_lookup.get(scene) == "ship":
            return

        if scene in range(4) or scene in [0x300]:  # Sea overview if port shuffle
            tab_scene = 1 if ctx.slot_data["shuffle_ports"] else 0
        else:
            tab_scene = scene | (1 << 16) if ctx.slot_data.get("shuffle_overworld_transitions", False) else scene
        print(f"Storing new scene for UT {hex(tab_scene)}")
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"{ctx.slot}_{ctx.team}_UT_MAP",
            "default": 0,
            "operations": [{"operation": "replace", "value": tab_scene}]
        }])

        # Save visited scenes
        if ctx.slot_data.get("map_warp_options", 0):
            self.visited_scenes.add(scene)
            await self.store_data(ctx, storage_key(ctx, visited_scenes_key), [scene])

    async def process_in_menu(self, ctx: "BizHawkClientContext", read_result):
        self.death_precision = None

        if (not read_result.get(PHAddr.in_map, 0) and self.map_mode) or self.map_warp:
            self.map_mode = False
            self.map_warp = None
            self.map_warp_reselector = True
            logger.info(f"Illegal map menu exit, canceling all map warps")

        if self.last_saved_scene is None:
            key = storage_key(ctx, save_scene_key)
            await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [key]
            }])
            last_saved_scene = get_stored_data(ctx, save_scene_key)
            print(f"fetched last saved scene: {last_saved_scene}")
            self.last_saved_scene = last_saved_scene if self.lss_retry_attempts >= 0 else 0 # if last_saved_scene is not None else False
            self.lss_retry_attempts -= 1

        if self.current_stage & 0xFF == 0x6E:
            started_save_file = await PHAddr.started_save_file.read(ctx, silent=True)
            if started_save_file:
                print(f"Started save file with saved scene {hex(self.last_saved_scene)}")
                if self.warp_to_start_flag:
                    print(f"Started save file with warp to start active, warping to start")
                    self.warp_to_start_flag = False
                    self.precision_mode = [PHAddr.stage_small, 0x6E, "wts"]
                    ctx.watcher_timeout = 0.1

                elif self.last_saved_scene in BOSS_WARP_SCENE_LOOKUP:
                    print(f"Problem entrance detected")
                    warp_exit = self.update_boss_warp(ctx, self.current_stage, self.last_saved_scene)
                    if warp_exit is not None:
                        self.precision_mode = [PHAddr.stage_small, 0x6E, "warp", warp_exit]
                        ctx.watcher_timeout = 0.1



    async def precision_backup(self, ctx, precision_read):
        if len(self.precision_mode) > 2 and self.precision_mode[2] == "warp":
            if precision_read == 0x34:
                print(f"New file, cancel precision")
                return True
        return False

    def clear_variables(self):
        self.last_saved_scene = None
        self.lss_retry_attempts = 4