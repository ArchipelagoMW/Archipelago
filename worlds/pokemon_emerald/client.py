import asyncio
import copy
import time
from typing import TYPE_CHECKING, Optional, Dict, Set


from NetUtils import ClientStatus
from Options import Toggle
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import BASE_OFFSET, data
from .options import Goal, RemoteItems
from .util import pokemon_data_to_json, json_to_pokemon_data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object


EXPECTED_ROM_NAME = "pokemon emerald version / AP 2"

IS_CHAMPION_FLAG = data.constants["FLAG_IS_CHAMPION"]
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
    "FLAG_HIDE_ROUTE_119_TEAM_AQUA",                    # Clear Weather Institute
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
]
KEY_LOCATION_FLAG_MAP = {data.locations[location_name].flag: location_name for location_name in KEY_LOCATION_FLAGS}

LEGENDARY_NAMES = {
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
    "Ho-oh": "HO_OH",
    "Lugia": "LUGIA"
}

DEFEATED_LEGENDARY_FLAG_MAP = {data.constants[f"FLAG_DEFEATED_{name}"]: name for name in LEGENDARY_NAMES.values()}
CAUGHT_LEGENDARY_FLAG_MAP = {data.constants[f"FLAG_CAUGHT_{name}"]: name for name in LEGENDARY_NAMES.values()}


class PokemonEmeraldClient(BizHawkClient):
    game = "Pokemon Emerald"
    system = "GBA"
    patch_suffix = ".apemerald"
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    goal_flag: Optional[int]

    wonder_trade_update_event: asyncio.Event
    latest_wonder_trades: dict
    latest_wonder_trade_reply: dict
    wonder_trade_task: Optional[asyncio.Task]
    wonder_trade_cooldown: int
    wonder_trade_cooldown_timer: int

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.goal_flag = None
        self.wonder_trade_update_event = asyncio.Event()
        self.latest_wonder_trades = {}
        self.wonder_trade_task = None
        self.wonder_trade_cooldown = 5000
        self.wonder_trade_cooldown_timer = 0

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
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

        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["gArchipelagoInfo"], 64, "ROM")]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if ctx.slot_data is not None:
            if ctx.slot_data["goal"] == Goal.option_champion:
                self.goal_flag = IS_CHAMPION_FLAG
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

        try:
            # Checks that the player is in the overworld
            overworld_guard = (data.ram_addresses["gMain"] + 4, (data.ram_addresses["CB2_Overworld"] + 1).to_bytes(4, "little"), "System Bus")

            # Read save block address
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["gSaveBlock1Ptr"], 4, "System Bus")],
                [overworld_guard]
            )
            if read_result is None:  # Not in overworld
                return

            # Checks that the save block hasn't moved
            save_block_address_guard = (data.ram_addresses["gSaveBlock1Ptr"], read_result[0], "System Bus")

            save_block_address = int.from_bytes(read_result[0], "little")

            # Handle giving the player items
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (save_block_address + 0x3778, 2, "System Bus"),                        # Number of received items
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 4, 1, "System Bus")  # Received item struct full?
                ],
                [overworld_guard, save_block_address_guard]
            )
            if read_result is None:  # Not in overworld, or save block moved
                return

            num_received_items = int.from_bytes(read_result[0], "little")
            received_item_is_empty = read_result[1][0] == 0

            # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
            # fill it with the next item
            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items]
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 0, (next_item.item - BASE_OFFSET).to_bytes(2, "little"), "System Bus"),
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 4, [1], "System Bus"),
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 5, [next_item.flags & 1], "System Bus"),
                ])

            # Read flags in 2 chunks
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(save_block_address + 0x1450, 0x96, "System Bus")],  # Flags
                [overworld_guard, save_block_address_guard]
            )
            if read_result is None:  # Not in overworld, or save block moved
                return

            flag_bytes = read_result[0]

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(save_block_address + 0x14E6, 0x96, "System Bus")],  # Flags continued
                [overworld_guard, save_block_address_guard]
            )
            if read_result is not None:
                flag_bytes += read_result[0]

            # Wonder Trades (only when connected to the server)
            if ctx.server is not None and not ctx.server.socket.closed:
                read_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [
                        (save_block_address + 0x377C, 0x50, "System Bus"),  # Wonder trade data
                        (save_block_address + 0x37CC, 1, "System Bus"),     # Is wonder trade sent
                    ],
                    [overworld_guard, save_block_address_guard]
                )

                if read_result is not None:
                    wonder_trade_pokemon_data = read_result[0]
                    trade_is_sent = read_result[1][0]

                    if trade_is_sent == 0 and wonder_trade_pokemon_data[19] == 2:
                        # Game has wonder trade data to send. Send it to data storage, remove it from the game's memory,
                        # and mark that the game is waiting on receiving a trade
                        Utils.async_start(self.wonder_trade_send(ctx, pokemon_data_to_json(wonder_trade_pokemon_data)))
                        await bizhawk.write(ctx.bizhawk_ctx, [
                            (save_block_address + 0x377C, bytes(0x50), "System Bus"),
                            (save_block_address + 0x37CC, [1], "System Bus"),
                        ])
                    elif trade_is_sent != 0 and wonder_trade_pokemon_data[19] != 2:
                        # Game is waiting on receiving a trade. See if there are any available trades that were not
                        # sent by this player, and if so, try to receive one.
                        # TODO: Should filter for trades that can't be completed (like Gen IV+ species) here and/or
                        # throttle calls to `wonder_trade_receive`.
                        if self.wonder_trade_cooldown_timer <= 0:
                            if any(item[0] != ctx.slot for key, item in self.latest_wonder_trades.items() if key != "_lock"):
                                received_trade = await self.wonder_trade_receive(ctx)
                                if received_trade is not None:
                                    await bizhawk.write(ctx.bizhawk_ctx, [
                                        (save_block_address + 0x377C, json_to_pokemon_data(received_trade), "System Bus"),
                                    ])
                        else:
                            # Very approximate "time since last loop", but extra delay is fine for this
                            self.wonder_trade_cooldown_timer -= int(ctx.watcher_timeout * 1000)

            game_clear = False
            local_checked_locations = set()
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

            if ctx.slot_data is not None and ctx.slot_data["goal"] == Goal.option_legendary_hunt:
                # If legendary hunt doesn't require catching, add defeated legendaries to caught_legendaries
                if ctx.slot_data["legendary_hunt_catch"] == Toggle.option_false:
                    for legendary, is_defeated in defeated_legendaries.items():
                        if is_defeated:
                            caught_legendaries[legendary] = True

                num_caught = 0
                for legendary, is_caught in caught_legendaries.items():
                    if is_caught and legendary in [LEGENDARY_NAMES[name] for name in ctx.slot_data["allowed_legendary_hunt_encounters"]]:
                        num_caught += 1

                if num_caught >= ctx.slot_data["legendary_hunt_count"]:
                    game_clear = True

            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(local_checked_locations)
                    }])

            # Send game clear
            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
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
                    "operations": [{"operation": "replace", "value": event_bitfield}]
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
                    "operations": [{"operation": "replace", "value": key_bitfield}]
                }])
                self.local_found_key_items = local_found_key_items
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def wonder_trade_acquire(self, ctx: BizHawkClientContext, keep_trying: bool = False) -> Optional[dict]:
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
            uuid = Utils.get_unique_identifier()
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "want_reply": True,
                "operations": [{"operation": "update", "value": {"_lock": lock}}],
                "uuid": uuid
            }])

            self.wonder_trade_update_event.clear()
            await self.wonder_trade_update_event.wait()
            reply = copy.deepcopy(self.latest_wonder_trade_reply)

            # Make sure the most recently received update was triggered by our lock attempt
            if reply.get("uuid", None) != uuid:
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

                if not keep_trying:
                    self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown)
                continue

            self.wonder_trade_cooldown = 5000
            return reply

    async def wonder_trade_send(self, ctx: BizHawkClientContext, data: str) -> None:
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
                str(wonder_trade_slot): (ctx.slot, data)
            }}]
        }])

        logger.info("Wonder trade sent! We'll notify you here when a trade has been found.")

    async def wonder_trade_receive(self, ctx: BizHawkClientContext) -> Optional[str]:
        """
        Tries to pop a pokemon out of the wonder trades. Returns `None` if
        for some reason it can't immediately remove a compatible pokemon.
        """
        from CommonClient import logger

        reply = await self.wonder_trade_acquire(ctx)

        if reply is None:
            return None

        # TODO: Filter by whether Emerald knows the species
        candidate_slots = [
            int(slot)
            for slot in reply["value"]
            if slot != "_lock" and reply["value"][slot][0] != ctx.slot
        ]

        if len(candidate_slots) == 0:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "operations": [{"operation": "update", "value": {"_lock": 0}}]
            }])
            return None

        wonder_trade_slot = max(candidate_slots)

        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"pokemon_wonder_trades_{ctx.team}",
            "default": {"_lock": 0},
            "operations": [
                {"operation": "update", "value": {"_lock": 0}},
                {"operation": "pop", "value": str(wonder_trade_slot)}
            ]
        }])

        logger.info("Wonder trade received!")
        return reply["value"][str(wonder_trade_slot)][1]

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            Utils.async_start(ctx.send_msgs([{
                "cmd": "SetNotify",
                "keys": [f"pokemon_wonder_trades_{ctx.team}"]
            }, {
                "cmd": "Get",
                "keys": [f"pokemon_wonder_trades_{ctx.team}"]
            }]))
        elif cmd == "Retrieved":
            if f"pokemon_wonder_trades_{ctx.team}" in args.get("keys", {}):
                self.latest_wonder_trades = args["keys"].get(f"pokemon_wonder_trades_{ctx.team}", {})
        elif cmd == "SetReply":
            if args.get("key", "") == f"pokemon_wonder_trades_{ctx.team}":
                self.latest_wonder_trade_reply = args
                self.latest_wonder_trades = args.get("value", {})

                if not self.wonder_trade_update_event.is_set():
                    self.wonder_trade_update_event.set()
