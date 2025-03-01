import asyncio
import copy
import orjson
import random
import time
from typing import TYPE_CHECKING, Optional, Dict, Set, Tuple
import uuid

from NetUtils import ClientStatus
from Options import Toggle
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import BASE_OFFSET, POKEDEX_OFFSET, data
from .options import Goal, RemoteItems
from .util import pokemon_data_to_json, json_to_pokemon_data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


EXPECTED_ROM_NAME = "pokemon emerald version / AP 5"

DEFEATED_WALLACE_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_WALLACE"]
DEFEATED_STEVEN_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_STEVEN"]
DEFEATED_NORMAN_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_NORMAN_1"]

# These flags are communicated to the tracker as a bitfield using this order.
# Modifying the order will cause undetectable autotracking issues.
TRACKER_EVENT_FLAGS = [
    "FLAG_DEFEATED_RUSTBORO_GYM",
    "FLAG_DEFEATED_DEWFORD_GYM",
    "FLAG_DEFEATED_MAUVILLE_GYM",
    "FLAG_DEFEATED_LAVARIDGE_GYM",
    "FLAG_DEFEATED_PETALBURG_GYM",
    "FLAG_DEFEATED_FORTREE_GYM",
    "FLAG_DEFEATED_MOSSDEEP_GYM",
    "FLAG_DEFEATED_SOOTOPOLIS_GYM",
    "FLAG_RECEIVED_POKENAV",                            # Talk to Mr. Stone
    "FLAG_DELIVERED_STEVEN_LETTER",
    "FLAG_DELIVERED_DEVON_GOODS",
    "FLAG_HIDE_ROUTE_119_TEAM_AQUA_SHELLY",             # Clear Weather Institute
    "FLAG_MET_ARCHIE_METEOR_FALLS",                     # Magma steals meteorite
    "FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT",              # Clear Magma Hideout
    "FLAG_MET_TEAM_AQUA_HARBOR",                        # Aqua steals submarine
    "FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE",              # Clear Aqua Hideout
    "FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_MAGMA_NOTE",  # Clear Space Center
    "FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN",
    "FLAG_HIDE_SKY_PILLAR_TOP_RAYQUAZA",                # Rayquaza departs for Sootopolis
    "FLAG_OMIT_DIVE_FROM_STEVEN_LETTER",                # Steven gives Dive HM (clears seafloor cavern grunt)
    "FLAG_IS_CHAMPION",
    "FLAG_PURCHASED_HARBOR_MAIL",
    "FLAG_REGI_DOORS_OPENED",
    "FLAG_RETURNED_DEVON_GOODS",
    "FLAG_DOCK_REJECTED_DEVON_GOODS",
    "FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY",
    "FLAG_WINGULL_SENT_ON_ERRAND",
    "FLAG_WINGULL_DELIVERED_MAIL",
    "FLAG_MET_PRETTY_PETAL_SHOP_OWNER",
]
EVENT_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_EVENT_FLAGS}

KEY_LOCATION_FLAGS = [
    "NPC_GIFT_RECEIVED_HM_CUT",
    "NPC_GIFT_RECEIVED_HM_FLY",
    "NPC_GIFT_RECEIVED_HM_SURF",
    "NPC_GIFT_RECEIVED_HM_STRENGTH",
    "NPC_GIFT_RECEIVED_HM_FLASH",
    "NPC_GIFT_RECEIVED_HM_ROCK_SMASH",
    "NPC_GIFT_RECEIVED_HM_WATERFALL",
    "NPC_GIFT_RECEIVED_HM_DIVE",
    "NPC_GIFT_RECEIVED_ACRO_BIKE",
    "NPC_GIFT_RECEIVED_WAILMER_PAIL",
    "NPC_GIFT_RECEIVED_DEVON_GOODS_RUSTURF_TUNNEL",
    "NPC_GIFT_RECEIVED_LETTER",
    "NPC_GIFT_RECEIVED_METEORITE",
    "NPC_GIFT_RECEIVED_GO_GOGGLES",
    "NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON",
    "NPC_GIFT_RECEIVED_ITEMFINDER",
    "NPC_GIFT_RECEIVED_DEVON_SCOPE",
    "NPC_GIFT_RECEIVED_MAGMA_EMBLEM",
    "NPC_GIFT_RECEIVED_POKEBLOCK_CASE",
    "NPC_GIFT_RECEIVED_SS_TICKET",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_2_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_1_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_4_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_6_KEY",
    "ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_2_SCANNER",
    "ITEM_ABANDONED_SHIP_CAPTAINS_OFFICE_STORAGE_KEY",
    "NPC_GIFT_RECEIVED_OLD_ROD",
    "NPC_GIFT_RECEIVED_GOOD_ROD",
    "NPC_GIFT_RECEIVED_SUPER_ROD",
    "NPC_GIFT_RECEIVED_EON_TICKET",
    "NPC_GIFT_RECEIVED_AURORA_TICKET",
    "NPC_GIFT_RECEIVED_MYSTIC_TICKET",
    "NPC_GIFT_RECEIVED_OLD_SEA_MAP",
]
KEY_LOCATION_FLAG_MAP = {data.locations[location_name].flag: location_name for location_name in KEY_LOCATION_FLAGS}

# .lower() keys for backward compatibility between 0.4.5 and 0.4.6
LEGENDARY_NAMES = {k.lower(): v for k, v in {
    "Groudon": "GROUDON",
    "Kyogre": "KYOGRE",
    "Rayquaza": "RAYQUAZA",
    "Latias": "LATIAS",
    "Latios": "LATIOS",
    "Regirock": "REGIROCK",
    "Regice": "REGICE",
    "Registeel": "REGISTEEL",
    "Mew": "MEW",
    "Deoxys": "DEOXYS",
    "Ho-Oh": "HO_OH",
    "Lugia": "LUGIA",
}.items()}

DEFEATED_LEGENDARY_FLAG_MAP = {data.constants[f"FLAG_DEFEATED_{name}"]: name for name in LEGENDARY_NAMES.values()}
CAUGHT_LEGENDARY_FLAG_MAP = {data.constants[f"FLAG_CAUGHT_{name}"]: name for name in LEGENDARY_NAMES.values()}

SHOAL_CAVE_MAPS = tuple(data.constants[map_name] for map_name in [
    "MAP_SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM",
    "MAP_SHOAL_CAVE_LOW_TIDE_INNER_ROOM",
])


class PokemonEmeraldClient(BizHawkClient):
    game = "Pokemon Emerald"
    system = "GBA"
    patch_suffix = ".apemerald"

    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    local_defeated_legendaries: Dict[str, bool]
    goal_flag: Optional[int]

    wonder_trade_update_event: asyncio.Event
    latest_wonder_trade_reply: dict
    wonder_trade_cooldown: int
    wonder_trade_cooldown_timer: int
    queued_received_trade: Optional[str]

    death_counter: Optional[int]
    previous_death_link: float
    ignore_next_death_link: bool

    current_map: Optional[int]

    def initialize_client(self):
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.local_defeated_legendaries = {}
        self.goal_flag = None
        self.wonder_trade_update_event = asyncio.Event()
        self.wonder_trade_cooldown = 5000
        self.wonder_trade_cooldown_timer = 0
        self.death_counter = None
        self.previous_death_link = 0
        self.ignore_next_death_link = False
        self.current_map = None
        self.queued_received_trade = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if not rom_name.startswith("pokemon emerald version"):
                return False
            if rom_name == "pokemon emerald version":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Emerald. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != EXPECTED_ROM_NAME:
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["gArchipelagoInfo"], 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        if ctx.slot_data["goal"] == Goal.option_champion:
            self.goal_flag = DEFEATED_WALLACE_FLAG
        elif ctx.slot_data["goal"] == Goal.option_steven:
            self.goal_flag = DEFEATED_STEVEN_FLAG
        elif ctx.slot_data["goal"] == Goal.option_norman:
            self.goal_flag = DEFEATED_NORMAN_FLAG
        elif ctx.slot_data["goal"] == Goal.option_legendary_hunt:
            self.goal_flag = None

        if ctx.slot_data["remote_items"] == RemoteItems.option_true and not ctx.items_handling & 0b010:
            ctx.items_handling = 0b011
            Utils.async_start(ctx.send_msgs([{
                "cmd": "ConnectUpdate",
                "items_handling": ctx.items_handling
            }]))

            # Need to make sure items handling updates and we get the correct list of received items
            # before continuing. Otherwise we might give some duplicate items and skip others.
            # Should patch remote_items option value into the ROM in the future to guarantee we get the
            # right item list before entering this part of the code
            await asyncio.sleep(0.75)
            return

        try:
            guards: Dict[str, Tuple[int, bytes, str]] = {}

            # Checks that the player is in the overworld
            guards["IN OVERWORLD"] = (
                data.ram_addresses["gMain"] + 4,
                (data.ram_addresses["CB2_Overworld"] + 1).to_bytes(4, "little"),
                "System Bus"
            )

            # Read save block addresses
            read_result = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (data.ram_addresses["gSaveBlock1Ptr"], 4, "System Bus"),
                    (data.ram_addresses["gSaveBlock2Ptr"], 4, "System Bus"),
                ]
            )

            # Checks that the save data hasn't moved
            guards["SAVE BLOCK 1"] = (data.ram_addresses["gSaveBlock1Ptr"], read_result[0], "System Bus")
            guards["SAVE BLOCK 2"] = (data.ram_addresses["gSaveBlock2Ptr"], read_result[1], "System Bus")

            sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")
            sb2_address = int.from_bytes(guards["SAVE BLOCK 2"][1], "little")

            await self.handle_tracker_info(ctx, guards)
            await self.handle_death_link(ctx, guards)
            await self.handle_received_items(ctx, guards)
            await self.handle_wonder_trade(ctx, guards)

            # Read flags in 2 chunks
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x1450, 0x96, "System Bus")],  # Flags
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )
            if read_result is None:  # Not in overworld, or save block moved
                return
            flag_bytes = read_result[0]

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x14E6, 0x96, "System Bus")],  # Flags continued
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )
            if read_result is not None:
                flag_bytes += read_result[0]

            # Read pokedex flags
            pokedex_caught_bytes = bytes(0)
            if ctx.slot_data["dexsanity"] == Toggle.option_true:
                # Read pokedex flags
                read_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(sb2_address + 0x28, 0x34, "System Bus")],
                    [guards["IN OVERWORLD"], guards["SAVE BLOCK 2"]]
                )
                if read_result is not None:
                    pokedex_caught_bytes = read_result[0]

            game_clear = False
            local_checked_locations: set[int] = set()
            local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_found_key_items = {location_name: False for location_name in KEY_LOCATION_FLAGS}
            defeated_legendaries = {legendary_name: False for legendary_name in LEGENDARY_NAMES.values()}
            caught_legendaries = {legendary_name: False for legendary_name in LEGENDARY_NAMES.values()}

            # Check set flags
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + BASE_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if flag_id == self.goal_flag:
                            game_clear = True

                        if flag_id in DEFEATED_LEGENDARY_FLAG_MAP:
                            defeated_legendaries[DEFEATED_LEGENDARY_FLAG_MAP[flag_id]] = True

                        if flag_id in CAUGHT_LEGENDARY_FLAG_MAP:
                            caught_legendaries[CAUGHT_LEGENDARY_FLAG_MAP[flag_id]] = True

                        if flag_id in EVENT_FLAG_MAP:
                            local_set_events[EVENT_FLAG_MAP[flag_id]] = True

                        if flag_id in KEY_LOCATION_FLAG_MAP:
                            local_found_key_items[KEY_LOCATION_FLAG_MAP[flag_id]] = True

            # Check pokedex
            if ctx.slot_data["dexsanity"] == Toggle.option_true:
                for byte_i, byte in enumerate(pokedex_caught_bytes):
                    for i in range(8):
                        if byte & (1 << i) != 0:
                            dex_number = (byte_i * 8 + i) + 1

                            location_id = dex_number + BASE_OFFSET + POKEDEX_OFFSET
                            if location_id in ctx.server_locations:
                                local_checked_locations.add(location_id)

            # Count legendary hunt flags
            if ctx.slot_data["goal"] == Goal.option_legendary_hunt:
                # If legendary hunt doesn't require catching, add defeated legendaries to caught_legendaries
                if ctx.slot_data["legendary_hunt_catch"] == Toggle.option_false:
                    for legendary, is_defeated in defeated_legendaries.items():
                        if is_defeated:
                            caught_legendaries[legendary] = True

                num_caught = 0
                for legendary, is_caught in caught_legendaries.items():
                    if is_caught and legendary in [LEGENDARY_NAMES[name.lower()] for name in ctx.slot_data["allowed_legendary_hunt_encounters"]]:
                        num_caught += 1

                if num_caught >= ctx.slot_data["legendary_hunt_count"]:
                    game_clear = True

            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.check_locations(local_checked_locations)

            # Send game clear
            if not ctx.finished_game and game_clear:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL,
                }])

            # Send tracker event flags
            if local_set_events != self.local_set_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS):
                    if local_set_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_emerald_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_events = local_set_events

            if local_found_key_items != self.local_found_key_items:
                key_bitfield = 0
                for i, location_name in enumerate(KEY_LOCATION_FLAGS):
                    if local_found_key_items[location_name]:
                        key_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_emerald_keys_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": key_bitfield}],
                }])
                self.local_found_key_items = local_found_key_items

            if ctx.slot_data["goal"] == Goal.option_legendary_hunt:
                if caught_legendaries != self.local_defeated_legendaries and ctx.slot is not None:
                    legendary_bitfield = 0
                    for i, legendary_name in enumerate(LEGENDARY_NAMES.values()):
                        if caught_legendaries[legendary_name]:
                            legendary_bitfield |= 1 << i

                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_emerald_legendaries_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "or", "value": legendary_bitfield}],
                    }])
                    self.local_defeated_legendaries = caught_legendaries
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_tracker_info(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        # Current map
        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x4, 2, "System Bus"),  # Current map
                (sb1_address + 0x1450 + (data.constants["FLAG_SYS_SHOAL_TIDE"] // 8), 1, "System Bus"),
            ],
            [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
        )
        if read_result is None:  # Save block moved
            return

        current_map = int.from_bytes(read_result[0], "big")
        shoal_cave = int(read_result[1][0] & (1 << (data.constants["FLAG_SYS_SHOAL_TIDE"] % 8)) > 0)
        if current_map != self.current_map:
            self.current_map = current_map
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": {
                    "type": "MapUpdate",
                    "mapId": current_map,
                    **({"tide": shoal_cave} if current_map in SHOAL_CAVE_MAPS else {}),
                },
            }])

    async def handle_death_link(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Checks whether the player has died while connected and sends a death link if so. Queues a death link in the game
        if a new one has been received.
        """
        if ctx.slot_data.get("death_link", Toggle.option_false) == Toggle.option_true:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.previous_death_link = ctx.last_death_link

            sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")
            sb2_address = int.from_bytes(guards["SAVE BLOCK 2"][1], "little")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [
                    (sb1_address + 0x177C + (52 * 4), 4, "System Bus"),  # White out stat
                    (sb1_address + 0x177C + (22 * 4), 4, "System Bus"),  # Canary stat
                    (sb2_address + 0xAC, 4, "System Bus"),               # Encryption key
                ],
                [guards["SAVE BLOCK 1"], guards["SAVE BLOCK 2"]]
            )
            if read_result is None:  # Save block moved
                return

            encryption_key = int.from_bytes(read_result[2], "little")
            times_whited_out = int.from_bytes(read_result[0], "little") ^ encryption_key

            # Canary is an unused stat that will always be 0. There is a low chance that we've done this read on
            # a frame where the user has just entered a battle and the encryption key has been changed, but the data
            # has not yet been encrypted with the new key. If `canary` is 0, `times_whited_out` is correct.
            canary = int.from_bytes(read_result[1], "little") ^ encryption_key

            # Skip all deathlink code if save is not yet loaded (encryption key is zero) or white out stat not yet
            # initialized (starts at 100 as a safety for subtracting values from an unsigned int).
            if canary == 0 and encryption_key != 0 and times_whited_out >= 100:
                if self.previous_death_link != ctx.last_death_link:
                    self.previous_death_link = ctx.last_death_link
                    if self.ignore_next_death_link:
                        self.ignore_next_death_link = False
                    else:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(data.ram_addresses["gArchipelagoDeathLinkQueued"], [1], "System Bus")]
                        )

                if self.death_counter is None:
                    self.death_counter = times_whited_out
                elif times_whited_out > self.death_counter:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} is out of usable POKéMON! "
                                         f"{ctx.player_names[ctx.slot]} whited out!")
                    self.ignore_next_death_link = True
                    self.death_counter = times_whited_out

    async def handle_received_items(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Checks the index of the most recently received item and whether the item queue is full. Writes the next item
        into the game if necessary.
        """
        received_item_address = data.ram_addresses["gArchipelagoReceivedItem"]

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x3778, 2, "System Bus"),      # Number of received items
                (received_item_address + 4, 1, "System Bus")  # Received item struct full?
            ],
            [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
        )
        if read_result is None:  # Not in overworld, or save block moved
            return

        num_received_items = int.from_bytes(read_result[0], "little")
        received_item_is_empty = read_result[1][0] == 0

        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received) and received_item_is_empty:
            next_item = ctx.items_received[num_received_items]
            should_display = 1 if next_item.flags & 1 or next_item.player == ctx.slot else 0
            await bizhawk.write(ctx.bizhawk_ctx, [
                (received_item_address + 0, (next_item.item - BASE_OFFSET).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 4, [1], "System Bus"),
                (received_item_address + 5, [should_display], "System Bus"),
            ])

    async def handle_wonder_trade(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Read wonder trade status from save data and either send a queued pokemon to data storage or attempt to retrieve
        one from data storage and write it into the save.
        """
        from CommonClient import logger

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x377C, 0x50, "System Bus"),  # Wonder trade data
                (sb1_address + 0x37CC, 1, "System Bus"),     # Is wonder trade sent
            ],
            [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
        )

        if read_result is not None:
            wonder_trade_pokemon_data = read_result[0]
            trade_is_sent = read_result[1][0]

            if trade_is_sent == 0 and wonder_trade_pokemon_data[19] == 2:
                # Game has wonder trade data to send. Send it to data storage, remove it from the game's memory,
                # and mark that the game is waiting on receiving a trade
                success = await bizhawk.guarded_write(ctx.bizhawk_ctx, [
                    (sb1_address + 0x377C, bytes(0x50), "System Bus"),
                    (sb1_address + 0x37CC, [1], "System Bus"),
                ], [guards["SAVE BLOCK 1"]])
                if success:
                    Utils.async_start(self.wonder_trade_send(ctx, pokemon_data_to_json(wonder_trade_pokemon_data)))
            elif trade_is_sent != 0 and wonder_trade_pokemon_data[19] != 2:
                # Game is waiting on receiving a trade.
                if self.queued_received_trade is not None:
                    # Client is holding a trade, ready to write it into the game
                    success = await bizhawk.guarded_write(ctx.bizhawk_ctx, [
                        (sb1_address + 0x377C, json_to_pokemon_data(self.queued_received_trade), "System Bus"),
                    ], [guards["SAVE BLOCK 1"]])

                    # Notify the player if it was written, otherwise hold it for the next loop
                    if success:
                        logger.info("Wonder trade received!")
                        self.queued_received_trade = None

                elif self.wonder_trade_cooldown_timer <= 0 and f"pokemon_wonder_trades_{ctx.team}" in ctx.stored_data:
                    # See if there are any available trades that were not sent by this player. If so, try to receive one.
                    if any(item[0] != ctx.slot
                            for key, item in ctx.stored_data.get(f"pokemon_wonder_trades_{ctx.team}", {}).items()
                            if key != "_lock" and orjson.loads(item[1])["species"] <= 386):
                        self.queued_received_trade = await self.wonder_trade_receive(ctx)
                        if self.queued_received_trade is None:
                            self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                            self.wonder_trade_cooldown *= 2
                            self.wonder_trade_cooldown += random.randrange(0, 500)
                        else:
                            self.wonder_trade_cooldown = 5000

                else:
                    # Very approximate "time since last loop", but extra delay is fine for this
                    self.wonder_trade_cooldown_timer -= int(ctx.watcher_timeout * 1000)

    async def wonder_trade_acquire(self, ctx: "BizHawkClientContext", keep_trying: bool = False) -> Optional[dict]:
        """
        Acquires a lock on the `pokemon_wonder_trades_{ctx.team}` key in
        datastorage. Locking the key means you have exclusive access
        to modifying the value until you unlock it or the key expires (5
        seconds).

        If `keep_trying` is `True`, it will keep trying to acquire the lock
        until successful. Otherwise it will return `None` if it fails to
        acquire the lock.
        """
        while not ctx.exit_event.is_set():
            lock = int(time.time_ns() / 1000000)
            message_uuid = str(uuid.uuid4())
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "want_reply": True,
                "operations": [{"operation": "update", "value": {"_lock": lock}}],
                "uuid": message_uuid,
            }])

            self.wonder_trade_update_event.clear()
            try:
                await asyncio.wait_for(self.wonder_trade_update_event.wait(), 5)
            except asyncio.TimeoutError:
                if not keep_trying:
                    return None
                continue

            reply = copy.deepcopy(self.latest_wonder_trade_reply)

            # Make sure the most recently received update was triggered by our lock attempt
            if reply.get("uuid", None) != message_uuid:
                if not keep_trying:
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown)
                continue

            # Make sure the current value of the lock is what we set it to
            # (I think this should theoretically never run)
            if reply["value"]["_lock"] != lock:
                if not keep_trying:
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown)
                continue

            # Make sure that the lock value we replaced is at least 5 seconds old
            # If it was unlocked before our change, its value was 0 and it will look decades old
            if lock - reply["original_value"]["_lock"] < 5000:
                # Multiple clients trying to lock the key may get stuck in a loop of checking the lock
                # by trying to set it, which will extend its expiration. So if we see that the lock was
                # too new when we replaced it, we should wait for increasingly longer periods so that
                # eventually the lock will expire and a client will acquire it.
                self.wonder_trade_cooldown *= 2
                self.wonder_trade_cooldown += random.randrange(0, 500)

                if not keep_trying:
                    self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown)
                continue

            # We have the lock, reset the cooldown and return
            self.wonder_trade_cooldown = 5000
            return reply

    async def wonder_trade_send(self, ctx: "BizHawkClientContext", data: str) -> None:
        """
        Sends a wonder trade pokemon to data storage
        """
        from CommonClient import logger

        reply = await self.wonder_trade_acquire(ctx, True)

        wonder_trade_slot = 0
        while str(wonder_trade_slot) in reply["value"]:
            wonder_trade_slot += 1

        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"pokemon_wonder_trades_{ctx.team}",
            "default": {"_lock": 0},
            "operations": [{"operation": "update", "value": {
                "_lock": 0,
                str(wonder_trade_slot): (ctx.slot, data),
            }}],
        }])

        logger.info("Wonder trade sent! We'll notify you here when a trade has been found.")

    async def wonder_trade_receive(self, ctx: "BizHawkClientContext") -> Optional[str]:
        """
        Tries to pop a pokemon out of the wonder trades. Returns `None` if
        for some reason it can't immediately remove a compatible pokemon.
        """
        reply = await self.wonder_trade_acquire(ctx)

        if reply is None:
            return None

        candidate_slots = [
            int(slot)
            for slot in reply["value"]
            if slot != "_lock" \
                and reply["value"][slot][0] != ctx.slot \
                and orjson.loads(reply["value"][slot][1])["species"] <= 386
        ]

        if len(candidate_slots) == 0:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "operations": [{"operation": "update", "value": {"_lock": 0}}],
            }])
            return None

        wonder_trade_slot = max(candidate_slots)

        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"pokemon_wonder_trades_{ctx.team}",
            "default": {"_lock": 0},
            "operations": [
                {"operation": "update", "value": {"_lock": 0}},
                {"operation": "pop", "value": str(wonder_trade_slot)},
            ]
        }])

        return reply["value"][str(wonder_trade_slot)][1]

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Connected":
            Utils.async_start(ctx.send_msgs([{
                "cmd": "SetNotify",
                "keys": [f"pokemon_wonder_trades_{ctx.team}"],
            }, {
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "operations": [{"operation": "default", "value": None}]  # value is ignored
            }]))
        elif cmd == "SetReply":
            if args.get("key", "") == f"pokemon_wonder_trades_{ctx.team}":
                self.latest_wonder_trade_reply = args
                self.wonder_trade_update_event.set()
