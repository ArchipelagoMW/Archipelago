import math
import time
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from BaseClasses import ItemClassification
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .data import data
from .item_data import FLY_UNLOCK_OFFSET, GRASS_OFFSET, POKEDEX_OFFSET, POKEDEX_COUNT_OFFSET
from .items import item_const_name_to_id, EXTENDED_TRAPLINK_MAPPING
from .options import Goal, ProvideShopHints, JohtoOnly
from .pokemon_data import ALL_UNOWN

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

EVENT_BYTES = math.ceil(max(data.event_flags.values()) / 8)
DEX_BYTES = math.ceil(len(data.pokemon) / 8)
GRASS_BYTES = math.ceil(sum(len(tiles) for tiles in data.grass_tiles.values()) / 8)
TRADE_BYTES = math.ceil(len(data.trades) / 8)
SIGN_BYTES = math.ceil(len(data.unown_signs) / 8)

TRACKER_EVENT_FLAGS = [
    "EVENT_GOT_KENYA",
    "EVENT_GAVE_KENYA",
    "EVENT_JASMINE_RETURNED_TO_GYM",
    "EVENT_DECIDED_TO_HELP_LANCE",
    "EVENT_CLEARED_ROCKET_HIDEOUT",
    "EVENT_CLEARED_RADIO_TOWER",
    "EVENT_BEAT_ELITE_FOUR",
    "EVENT_RESTORED_POWER_TO_KANTO",
    "EVENT_BLUE_GYM_TRACKER",
    "EVENT_BEAT_RED",
    "EVENT_CLEARED_SLOWPOKE_WELL",
    "EVENT_HERDED_FARFETCHD",
    "EVENT_RELEASED_THE_BEASTS",
    "EVENT_BEAT_FALKNER",
    "EVENT_BEAT_BUGSY",
    "EVENT_BEAT_WHITNEY",
    "EVENT_BEAT_MORTY",
    "EVENT_BEAT_JASMINE",
    "EVENT_BEAT_CHUCK",
    "EVENT_BEAT_PRYCE",
    "EVENT_BEAT_CLAIR",
    "EVENT_BEAT_BROCK",
    "EVENT_BEAT_MISTY",
    "EVENT_BEAT_LTSURGE",
    "EVENT_BEAT_ERIKA",
    "EVENT_BEAT_JANINE",
    "EVENT_BEAT_SABRINA",
    "EVENT_BEAT_BLAINE",
    "EVENT_BEAT_BLUE",
    "EVENT_FAST_SHIP_FOUND_GIRL",
    "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON",
    "EVENT_MET_BILL",
]

EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_EVENT_FLAGS}

TRACKER_EVENT_FLAGS_2 = [
    "EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY",
    "EVENT_SAW_SUICUNE_ON_ROUTE_42",
    "EVENT_SAW_SUICUNE_ON_ROUTE_36",
    "EVENT_BEAT_RIVAL_IN_MT_MOON",
    "EVENT_GOT_EON_MAIL_FROM_EUSINE",
    "EVENT_BEAT_CHERRYGROVE_RIVAL",
    "EVENT_BEAT_AZALEA_RIVAL",
    "EVENT_RIVAL_BURNED_TOWER",
    "EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL",
    "EVENT_BEAT_VICTORY_ROAD_RIVAL",
    "EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU",
    "EVENT_ROUTE_24_ROCKET",
    "EVENT_GOT_ALL_UNOWN",
    "EVENT_OBTAINED_DIPLOMA",
    "EVENT_BEAT_ROCKET_EXECUTIVEM_3",
    "EVENT_SOLVED_KABUTO_PUZZLE",
    "EVENT_SOLVED_OMANYTE_PUZZLE",
    "EVENT_SOLVED_AERODACTYL_PUZZLE",
    "EVENT_SOLVED_HO_OH_PUZZLE",
]

EVENT_FLAG_MAP_2 = {data.event_flags[event]: event for event in TRACKER_EVENT_FLAGS_2}

TRACKER_STATIC_EVENT_FLAGS = [
    "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE",
    "EVENT_FOUGHT_SUDOWOODO",
    "EVENT_LAKE_OF_RAGE_RED_GYARADOS",
    "EVENT_FOUGHT_HO_OH",
    "EVENT_FOUGHT_LUGIA",
    "EVENT_FOUGHT_SUICUNE",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_1",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_2",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_3",
    "EVENT_GOT_SHUCKIE",
    "EVENT_GOT_EEVEE",
    "EVENT_GOT_DRATINI",
    "EVENT_TOGEPI_HATCHED",
    "EVENT_GOT_TYROGUE_FROM_KIYO",
    "EVENT_UNION_CAVE_B2F_LAPRAS",
    "EVENT_FOUGHT_CELEBI",
    "EVENT_GOT_ODD_EGG",
    "EVENT_STATIC_GOLDENROD_GAME_CORNER_1",
    "EVENT_STATIC_GOLDENROD_GAME_CORNER_2",
    "EVENT_STATIC_GOLDENROD_GAME_CORNER_3",
    "EVENT_STATIC_CELADON_GAME_CORNER_PRIZE_ROOM_1",
    "EVENT_STATIC_CELADON_GAME_CORNER_PRIZE_ROOM_2",
    "EVENT_STATIC_CELADON_GAME_CORNER_PRIZE_ROOM_3",
    "EVENT_FOUGHT_SNORLAX",
]

STATIC_EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_STATIC_EVENT_FLAGS}

TRACKER_ROCKET_TRAP_EVENTS = [
    "EVENT_EXPLODING_TRAP_1",
    "EVENT_EXPLODING_TRAP_2",
    "EVENT_EXPLODING_TRAP_3",
    "EVENT_EXPLODING_TRAP_4",
    "EVENT_EXPLODING_TRAP_5",
    "EVENT_EXPLODING_TRAP_6",
    "EVENT_EXPLODING_TRAP_7",
    "EVENT_EXPLODING_TRAP_8",
    "EVENT_EXPLODING_TRAP_9",
    "EVENT_EXPLODING_TRAP_10",
    "EVENT_EXPLODING_TRAP_11",
    "EVENT_EXPLODING_TRAP_12",
    "EVENT_EXPLODING_TRAP_13",
    "EVENT_EXPLODING_TRAP_14",
    "EVENT_EXPLODING_TRAP_15",
    "EVENT_EXPLODING_TRAP_16",
    "EVENT_EXPLODING_TRAP_17",
    "EVENT_EXPLODING_TRAP_18",
    "EVENT_EXPLODING_TRAP_19",
    "EVENT_EXPLODING_TRAP_20",
    "EVENT_EXPLODING_TRAP_21",
    "EVENT_EXPLODING_TRAP_22",
]

ROCKET_TRAP_EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_ROCKET_TRAP_EVENTS}

TRACKER_KEY_ITEM_FLAGS = [
    "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
    "EVENT_HIVE_BADGE_FROM_BUGSY",
    "EVENT_PLAIN_BADGE_FROM_WHITNEY",
    "EVENT_FOG_BADGE_FROM_MORTY",
    "EVENT_STORM_BADGE_FROM_CHUCK",
    "EVENT_MINERAL_BADGE_FROM_JASMINE",
    "EVENT_GLACIER_BADGE_FROM_PRYCE",
    "EVENT_RISING_BADGE_FROM_CLAIR",
    "EVENT_BOULDER_BADGE_FROM_BROCK",
    "EVENT_CASCADE_BADGE_FROM_MISTY",
    "EVENT_THUNDER_BADGE_FROM_LTSURGE",
    "EVENT_RAINBOW_BADGE_FROM_ERIKA",
    "EVENT_SOUL_BADGE_FROM_JANINE",
    "EVENT_MARSH_BADGE_FROM_SABRINA",
    "EVENT_VOLCANO_BADGE_FROM_BLAINE",
    "EVENT_EARTH_BADGE_FROM_BLUE",

    "EVENT_GOT_RADIO_CARD",
    "EVENT_GOT_MAP_CARD",
    "EVENT_GOT_PHONE_CARD",
    "EVENT_GOT_EXPN_CARD",
    "EVENT_GOT_POKEGEAR",
    "EVENT_GOT_POKEDEX",
    "EVENT_MART_ESCAPE_ROPE",
    "EVENT_MART_WATER_STONE",

    "EVENT_RISING_BADGE_FROM_CLAIR_GYM",
]
KEY_ITEM_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_KEY_ITEM_FLAGS}

DEATH_LINK_MASK = 0b00010000
DEATH_LINK_SETTING_ADDR = data.ram_addresses["wArchipelagoOptions"] + 4
TRAP_LINK_MASK = 0b00001000
TRAP_LINK_SETTING_ADDR = data.ram_addresses["wArchipelagoOptions"] + 5
COUNT_ALL_POKEMON = len(data.pokemon)

INVERTED_EVENTS = {
    "EVENT_MET_BILL"
}

INVERTED_EVENT_IDS = {data.event_flags[event] for event in INVERTED_EVENTS}

HINT_FLAGS = {f"EVENT_SEEN_{mart_name}": [item.flag for item in mart_data.items if item.flag] for mart_name, mart_data
              in data.marts.items()}

HINT_FLAG_MAP = {data.event_flags[flag_name]: flag_name for flag_name in HINT_FLAGS.keys()}

TRAP_ID_TO_NAME = {item.item_id: item.label for item in data.items.values() if "Trap" in item.tags}
TRAP_NAME_TO_ID = {item_name: item_id for item_id, item_name in TRAP_ID_TO_NAME.items()} | EXTENDED_TRAPLINK_MAPPING

SIGN_ID_TO_NAME = {sign.id: sign.name for sign in data.unown_signs.values()}
NUM_UNOWN = len(ALL_UNOWN)


class PokemonCrystalClient(BizHawkClient):
    game = data.manifest.game
    system = ("GB", "GBC")
    patch_suffix = ".apcrystal"

    local_checked_locations: set[int]
    goal_flags: list[int]
    local_set_events: dict[str, bool]
    local_set_events_2: dict[str, bool]
    local_set_static_events: dict[str, bool]
    local_set_rocket_trap_events: dict[str, bool]
    local_found_key_items: dict[str, bool]
    local_seen_pokemon: set[int]
    local_caught_pokemon: set[int]
    local_hints: list[str]
    local_trades_completed: set[int]
    phone_trap_locations: list[int]
    current_map: list[int]
    last_death_link: float
    grass_location_mapping: dict[str, int]
    trap_link_queue: list[int]
    notify_setup_complete: bool
    remote_seen_pokemon: set[int]
    remote_caught_pokemon: set[int]
    local_seen_signs: set[str]
    local_unown_dex: list[int]
    remote_unown_dex: list[int]

    def initialize_client(self) -> None:
        self.local_checked_locations = set()
        self.goal_flags = []
        self.local_set_events = dict()
        self.local_set_events_2 = dict()
        self.local_set_static_events = dict()
        self.local_set_rocket_trap_events = dict()
        self.local_found_key_items = dict()
        self.local_seen_pokemon = set()
        self.local_caught_pokemon = set()
        self.local_hints = []
        self.local_trades_completed = set()
        self.phone_trap_locations = list()
        self.current_map = [0, 0]
        self.last_death_link = 0
        self.grass_location_mapping = dict()
        self.trap_link_queue = list()
        self.notify_setup_complete = False
        self.remote_seen_pokemon = set()
        self.remote_caught_pokemon = set()
        self.local_seen_signs = set()
        self.local_unown_dex = list()
        self.remote_unown_dex = list()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:

            # Check we're operating on a 2MB ROM
            if await bizhawk.get_memory_size(ctx.bizhawk_ctx, "ROM") != 2097152: return False

            # Check ROM name/patch version
            rom_info = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Header"], 11, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Version"], 2, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Revision"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Setting_RemoteItems"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Version"], 32, "ROM")
                                                              ])))

            rom_name = bytes([byte for byte in rom_info[0] if byte != 0]).decode("ascii")
            rom_version = int.from_bytes(rom_info[1], "little")
            rom_revision = int.from_bytes(rom_info[2], "little")
            remote_items = int.from_bytes(rom_info[3], "little")

            if rom_name == "PM_CRYSTAL":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Crystal. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != "AP_CRYSTAL":
                return False

            required_rom_version = data.rom_version if rom_revision == 0 else data.rom_version_11
            if rom_version != required_rom_version:
                try:
                    generator_apworld_version = bytes([byte for byte in rom_info[4] if byte != 0]).decode("ascii")
                except UnicodeDecodeError:
                    generator_apworld_version = None

                if not generator_apworld_version:
                    generator_apworld_version = "too old to know"
                generator_version = "{0:x}".format(rom_version)
                client_version = "{0:x}".format(required_rom_version)
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your version of pokemon_crystal.apworld "
                            "against the version used to generate this game.")
                logger.info(f"Client APWorld version: {data.manifest.world_version}, "
                            f"Generator APWorld version: {generator_apworld_version}")
                logger.info(f"ROM Revision: V1.{rom_revision}, Client checksum: {client_version}, "
                            f"Generator checksum: {generator_version}")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b011 if remote_items else 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_Seed_Auth"], 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        pokedex_seen_key = f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}"
        pokedex_caught_key = f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}"
        unown_dex_key = f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}"

        if not self.notify_setup_complete:
            if ctx.items_handling & 0b010:
                ctx.set_notify(pokedex_caught_key, pokedex_seen_key, unown_dex_key)
            self.notify_setup_complete = True

        if ctx.slot_data["goal"] == Goal.option_elite_four:
            self.goal_flags = [data.event_flags["EVENT_BEAT_ELITE_FOUR"]]
        elif ctx.slot_data["goal"] == Goal.option_diploma:
            self.goal_flags = [data.event_flags["EVENT_OBTAINED_DIPLOMA"]]
        elif ctx.slot_data["goal"] == Goal.option_rival:
            self.goal_flags = [
                data.event_flags["EVENT_BEAT_CHERRYGROVE_RIVAL"],
                data.event_flags["EVENT_BEAT_AZALEA_RIVAL"],
                data.event_flags["EVENT_RIVAL_BURNED_TOWER"],
                data.event_flags["EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL"],
                data.event_flags["EVENT_BEAT_VICTORY_ROAD_RIVAL"],
            ]
            if ctx.slot_data["johto_only"] == JohtoOnly.option_off:
                self.goal_flags.extend([
                    data.event_flags["EVENT_BEAT_RIVAL_IN_MT_MOON"],
                    data.event_flags["EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU"],
                ])
        elif ctx.slot_data["goal"] == Goal.option_defeat_team_rocket:
            self.goal_flags = [
                data.event_flags["EVENT_CLEARED_SLOWPOKE_WELL"],
                data.event_flags["EVENT_CLEARED_ROCKET_HIDEOUT"],
                data.event_flags["EVENT_BEAT_ROCKET_EXECUTIVEM_3"],
                data.event_flags["EVENT_CLEARED_RADIO_TOWER"],
            ]
            if ctx.slot_data["johto_only"] == JohtoOnly.option_off:
                self.goal_flags.append(data.event_flags["EVENT_ROUTE_24_ROCKET"])
        elif ctx.slot_data["goal"] == Goal.option_unown_hunt:
            self.goal_flags = [
                data.event_flags["EVENT_GOT_ALL_UNOWN"]
            ]
        else:
            self.goal_flags = [data.event_flags["EVENT_BEAT_RED"]]

        self.grass_location_mapping = ctx.slot_data["grass_location_mapping"]

        try:

            # Scout the locations that can be hinted if provide hints is turned on
            if ctx.slot_data["provide_shop_hints"] != ProvideShopHints.option_off and ctx.locations_info == {}:
                hint_ids = []
                for locations in HINT_FLAGS.values():
                    hint_ids.extend(loc for loc in locations if loc in ctx.missing_locations)
                if hint_ids:
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": hint_ids,
                        "create_as_hint": 0
                    }])

            overworld_guard = (data.ram_addresses["wArchipelagoSafeWrite"], [1], "WRAM")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 7, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            await self.handle_trap_link_setting(ctx, overworld_guard)

            num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0
            phone_trap_index = read_result[0][4]

            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items].item
                if next_item >= FLY_UNLOCK_OFFSET:
                    fly_unlock = next_item - FLY_UNLOCK_OFFSET
                    next_item = item_const_name_to_id("FLY_UNLOCK")
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (data.ram_addresses["wArchipelagoFlyUnlockReceived"],
                         fly_unlock.to_bytes(1, "little"), "WRAM")
                    ])
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["wArchipelagoItemReceived"],
                     next_item.to_bytes(1, "little"), "WRAM")
                ])
                await self.send_trap_link(ctx, next_item)
            elif self.trap_link_queue and not read_result[0][6]:
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoTrapReceived"],
                                                       self.trap_link_queue.pop(0).to_bytes(1, "little"),
                                                       "WRAM")])

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wEventFlags"], EVENT_BYTES, "WRAM"),  # Flags
                 (data.ram_addresses["wArchipelagoPokedexCaught"], DEX_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoPokedexSeen"], DEX_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoGrassFlags"], GRASS_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoTradeFlags"], TRADE_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoSignFlags"], SIGN_BYTES, "WRAM"),
                 (data.ram_addresses["wUnownDex"], NUM_UNOWN, "WRAM"),
                 (data.ram_addresses["wMapGroup"], 2, "WRAM")],
                [overworld_guard]
            )

            if read_result is None:
                return

            pokedex_caught_bytes = read_result[1]
            pokedex_seen_bytes = read_result[2]
            grass_cut_bytes = read_result[3]
            trade_bytes = read_result[4]
            sign_bytes = read_result[5]
            unown_dex_bytes = read_result[6]
            current_map_bytes = read_result[7]

            local_checked_locations = set()
            local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_set_events_2 = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS_2}
            local_set_static_events = {flag_name: False for flag_name in TRACKER_STATIC_EVENT_FLAGS}
            local_set_rocket_trap_events = {flag_name: False for flag_name in TRACKER_ROCKET_TRAP_EVENTS}
            local_found_key_items = {flag_name: False for flag_name in TRACKER_KEY_ITEM_FLAGS}
            remote_seen_pokemon = ctx.stored_data[pokedex_seen_key] if pokedex_seen_key in ctx.stored_data else None
            local_seen_pokemon = set(remote_seen_pokemon) if remote_seen_pokemon else set()
            remote_caught_pokemon = ctx.stored_data[
                pokedex_caught_key] if pokedex_caught_key in ctx.stored_data else None
            local_caught_pokemon = set(remote_caught_pokemon) if remote_caught_pokemon else set()
            local_hints = {flag_name: False for flag_name in HINT_FLAGS.keys()}
            local_trades_completed = set()

            goal_flags_cleared = {flag: False for flag in self.goal_flags}

            flag_bytes = read_result[0]
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    location_id = byte_i * 8 + i
                    event_set = byte & (1 << i)
                    invert_event = location_id in INVERTED_EVENT_IDS
                    if (not invert_event and event_set != 0) or (invert_event and event_set == 0):
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if location_id in goal_flags_cleared:
                            goal_flags_cleared[location_id] = True

                        if location_id in EVENT_FLAG_MAP:
                            local_set_events[EVENT_FLAG_MAP[location_id]] = True

                        if location_id in EVENT_FLAG_MAP_2:
                            local_set_events_2[EVENT_FLAG_MAP_2[location_id]] = True

                        if location_id in STATIC_EVENT_FLAG_MAP:
                            local_set_static_events[STATIC_EVENT_FLAG_MAP[location_id]] = True

                        if location_id in ROCKET_TRAP_EVENT_FLAG_MAP:
                            local_set_rocket_trap_events[ROCKET_TRAP_EVENT_FLAG_MAP[location_id]] = True

                        if location_id in KEY_ITEM_FLAG_MAP:
                            local_found_key_items[KEY_ITEM_FLAG_MAP[location_id]] = True

                        if location_id in HINT_FLAG_MAP:
                            local_hints[HINT_FLAG_MAP[location_id]] = True

            for byte_i, byte in enumerate(pokedex_caught_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        location_id = dex_number + POKEDEX_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)
                        local_caught_pokemon.add(dex_number)

            for byte_i, byte in enumerate(pokedex_seen_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        local_seen_pokemon.add(dex_number)

            for byte_i, byte in enumerate(grass_cut_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        location_id = (byte_i * 8 + i) + GRASS_OFFSET
                        if str(location_id) in self.grass_location_mapping:
                            location_id = self.grass_location_mapping[str(location_id)]
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

            for byte_i, byte in enumerate(trade_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        local_trades_completed.add(byte_i * 8 + i)

            packages = []

            if local_seen_pokemon != self.local_seen_pokemon:
                packages.append({
                    "cmd": "Set",
                    "key": pokedex_seen_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": list(local_seen_pokemon)}, ]
                })

            if local_caught_pokemon != self.local_caught_pokemon:
                packages.append({
                    "cmd": "Set",
                    "key": pokedex_caught_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": list(local_caught_pokemon)}, ]
                })

            if local_trades_completed != self.local_trades_completed:
                packages.append({
                    "cmd": "Set",
                    "key": f"pokemon_crystal_trades_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": list(local_trades_completed)}, ]
                })

            if packages:
                await ctx.send_msgs(packages)

                self.local_seen_pokemon = local_seen_pokemon
                self.local_caught_pokemon = local_caught_pokemon
                self.local_trades_completed = local_trades_completed

            if ctx.slot_data["dexcountsanity_counts"]:
                dex_count = len(local_caught_pokemon)
                check_counts = ctx.slot_data["dexcountsanity_counts"]

                for count in check_counts[:-1]:
                    location_id = count + POKEDEX_COUNT_OFFSET
                    if dex_count >= count and location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

                if dex_count >= check_counts[-1]:
                    location_id = COUNT_ALL_POKEMON + POKEDEX_COUNT_OFFSET
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

            if local_checked_locations != self.local_checked_locations:
                if "trap_locations" in ctx.slot_data:
                    for location in local_checked_locations:
                        if location not in ctx.checked_locations:
                            if str(location) in ctx.slot_data["trap_locations"]:
                                await self.send_trap_link(ctx, ctx.slot_data["trap_locations"][str(location)])

                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(local_checked_locations)
                }])

                self.local_checked_locations = local_checked_locations

            # Send game clear
            if not ctx.finished_game and all(goal_flags_cleared.values()):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            if not self.phone_trap_locations:
                phone_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(data.rom_addresses["AP_Setting_Phone_Trap_Locations"], 0x20, "ROM")],
                    [overworld_guard]
                )
                if phone_result is not None:
                    read_locations = []
                    for i in range(0, 16):
                        loc = int.from_bytes(phone_result[0][i * 2:(i + 1) * 2], "little")
                        read_locations.append(loc)
                    self.phone_trap_locations = read_locations
            else:
                hint_locations = [location for location in self.phone_trap_locations[:phone_trap_index] if
                                  location != 0
                                  and location not in ctx.locations_scouted
                                  and location not in local_checked_locations
                                  and location not in ctx.checked_locations]
                if hint_locations:
                    ctx.locations_scouted.update(hint_locations)
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": hint_locations,
                        "create_as_hint": 2
                    }])

            if local_set_events != self.local_set_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS):
                    if local_set_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_events = local_set_events

            if local_set_events_2 != self.local_set_events_2 and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS_2):
                    if local_set_events_2[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_events_2_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_events_2 = local_set_events_2

            if local_set_static_events != self.local_set_static_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_STATIC_EVENT_FLAGS):
                    if local_set_static_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_statics_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_static_events = local_set_static_events

            if local_set_rocket_trap_events != self.local_set_rocket_trap_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_ROCKET_TRAP_EVENTS):
                    if local_set_rocket_trap_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_rockettraps_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_rocket_trap_events = local_set_rocket_trap_events

            if local_found_key_items != self.local_found_key_items:
                key_bitfield = 0
                for i, location_name in enumerate(TRACKER_KEY_ITEM_FLAGS):
                    if local_found_key_items[location_name]:
                        key_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_keys_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": key_bitfield}],
                }])
                self.local_found_key_items = local_found_key_items

            provide_shop_hints = ctx.slot_data["provide_shop_hints"]
            if provide_shop_hints != ProvideShopHints.option_off:
                hints_locations = []
                for flag, locations in HINT_FLAGS.items():
                    if local_hints[flag] and flag not in self.local_hints:
                        hints_locations.extend(locations)
                        self.local_hints.append(flag)

                if hints_locations:

                    if provide_shop_hints == ProvideShopHints.option_progression:
                        item_flag_mask = ItemClassification.progression
                    elif provide_shop_hints == ProvideShopHints.option_progression_and_useful:
                        item_flag_mask = ItemClassification.progression | ItemClassification.useful
                    else:
                        item_flag_mask = 0

                    hint_ids = []
                    for location_id in hints_locations:
                        if (location_id not in ctx.missing_locations
                                or location_id in self.local_checked_locations
                                or location_id not in ctx.locations_info):
                            continue
                        if not item_flag_mask or (ctx.locations_info[location_id].flags & item_flag_mask):
                            hint_ids.append(location_id)

                    if hint_ids:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": hint_ids,
                            "create_as_hint": 2
                        }])

            local_seen_signs = set()

            for byte_i, byte in enumerate(sign_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        sign_id = (byte_i * 8 + i)
                        sign_name = SIGN_ID_TO_NAME[sign_id]
                        local_seen_signs.add(sign_name)

            if local_seen_signs != self.local_seen_signs:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_signs_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": list(local_seen_signs)}, ]
                }])
                self.local_seen_signs = local_seen_signs

            local_unown_dex = list(self.remote_unown_dex)
            for unown in unown_dex_bytes:
                if unown and unown not in local_unown_dex:
                    local_unown_dex.append(unown)

            if local_unown_dex != self.local_unown_dex:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": unown_dex_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": local_unown_dex}, ]
                }])
                self.local_unown_dex = local_unown_dex

            await self.handle_death_link(ctx, overworld_guard)

            current_map = [int(x) for x in current_map_bytes]
            if self.current_map != current_map:
                self.current_map = current_map
                message = [{"cmd": "Bounce", "slots": [ctx.slot],
                            "data": {"mapGroup": current_map[0], "mapNumber": current_map[1]}}]
                await ctx.send_msgs(message)

            if ctx.items_handling & 0b010:

                seen_bytes = bytearray(DEX_BYTES)
                caught_bytes = bytearray(DEX_BYTES)

                for i in range(1, len(data.pokemon) + 1):
                    poke_index = i - 1
                    byte_index = math.floor(poke_index / 8)
                    if i in local_seen_pokemon:
                        seen_bytes[byte_index] = seen_bytes[byte_index] | (1 << (poke_index % 8))
                    if i in local_caught_pokemon:
                        caught_bytes[byte_index] = caught_bytes[byte_index] | (1 << (poke_index % 8))

                await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [(data.ram_addresses["wArchipelagoPokedexSeen"], seen_bytes, "WRAM"),
                     (data.ram_addresses["wArchipelagoPokedexCaught"], caught_bytes, "WRAM"),
                     (data.ram_addresses["wUnownDex"], local_unown_dex, "WRAM"), ],
                    [(data.ram_addresses["wArchipelagoPokedexSeen"], pokedex_seen_bytes, "WRAM"),
                     (data.ram_addresses["wArchipelagoPokedexCaught"], pokedex_caught_bytes, "WRAM"),
                     (data.ram_addresses["wUnownDex"], unown_dex_bytes, "WRAM")]
                )

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_death_link(self, ctx: "BizHawkClientContext", guard) -> None:

        death_link_setting_status = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [(DEATH_LINK_SETTING_ADDR, 1, "WRAM")],
            [guard]
        )

        if death_link_setting_status and death_link_setting_status[0][0] & DEATH_LINK_MASK:

            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.last_death_link = ctx.last_death_link
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])

            death_link_status = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wArchipelagoDeathLink"], 1, "WRAM")], [guard])

            if not death_link_status: return

            if death_link_status[0][0] == 1:
                await ctx.send_death(ctx.player_names[ctx.slot] + " is out of usable Pokémon! "
                                     + ctx.player_names[ctx.slot] + " whited out!")
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])
                self.last_death_link = time.time()
            elif death_link_status[0][0] == 3:
                await ctx.send_death(ctx.player_names[ctx.slot] + " failed to dodge the spinner!")
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])
                self.last_death_link = time.time()
            elif ctx.last_death_link > self.last_death_link and not death_link_status[0][0]:
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [2], "WRAM")])
                self.last_death_link = ctx.last_death_link

        elif "DeathLink" in ctx.tags:
            await ctx.update_death_link(False)
            self.last_death_link = 0

    @staticmethod
    async def handle_trap_link_setting(ctx: "BizHawkClientContext", guard) -> None:
        trap_link_setting_status = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [(TRAP_LINK_SETTING_ADDR, 1, "WRAM")],
            [guard]
        )

        old_tags = ctx.tags.copy()

        if trap_link_setting_status:
            if trap_link_setting_status[0][0] & TRAP_LINK_MASK:
                ctx.tags.add("TrapLink")
            else:
                ctx.tags -= {"TrapLink"}

        if old_tags != ctx.tags and ctx.server and not ctx.server.socket.closed:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

    @staticmethod
    async def send_trap_link(ctx: "BizHawkClientContext", trap_id: int):
        if "TrapLink" not in ctx.tags or ctx.slot is None:
            return

        if trap_id not in TRAP_ID_TO_NAME: return

        await ctx.send_msgs([{
            "cmd": "Bounce",
            "tags": ["TrapLink"],
            "data": {
                "time": time.time(),
                "source": ctx.player_names[ctx.slot],
                "trap_name": TRAP_ID_TO_NAME[trap_id],
            }
        }])

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        super().on_package(ctx, cmd, args)

        if cmd == "Bounced":
            if "tags" not in args: return
            source_name = args["data"]["source"]
            if ("TrapLink" in ctx.tags) and ("TrapLink" in args["tags"]) and source_name != ctx.player_names[ctx.slot]:
                trap_name: str = args["data"]["trap_name"]
                if trap_name not in TRAP_NAME_TO_ID:
                    return

                local_trap_name = TRAP_ID_TO_NAME[TRAP_NAME_TO_ID[trap_name]]

                if "trap_weights" not in ctx.slot_data:
                    return

                if local_trap_name not in ctx.slot_data["trap_weights"]:
                    return

                if ctx.slot_data["trap_weights"][local_trap_name] == 0:
                    return

                self.trap_link_queue.append(TRAP_NAME_TO_ID[trap_name])

        elif cmd == "Retrieved":
            if ctx.items_handling & 0b010:
                if f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_caught_pokemon = args["keys"][f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}"]
                    self.remote_caught_pokemon = set(remote_caught_pokemon) if remote_caught_pokemon else set()
                if f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_seen_pokemon = args["keys"][f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}"]
                    self.remote_seen_pokemon = set(remote_seen_pokemon) if remote_seen_pokemon else set()
                if f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_unown_dex = args["keys"][f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}"]
                    self.remote_unown_dex = remote_unown_dex if remote_unown_dex else list()

        elif cmd == "SetReply":
            if args["key"] == f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}":
                self.remote_caught_pokemon = set(args["value"])
            elif args["key"] == f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}":
                self.remote_seen_pokemon = set(args["value"])
            elif args["key"] == f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}":
                self.remote_unown_dex = args["value"]
