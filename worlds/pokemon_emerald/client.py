import asyncio
from argparse import Namespace
import json
import os
import subprocess
from typing import Optional, Dict, Set, Tuple, Any

from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, gui_enabled, logger
from NetUtils import ClientStatus
import Patch
from settings import get_settings
from Utils import async_start

from .data import BASE_OFFSET, data
from .options import Goal


GBA_SOCKET_PORT = 43053

EXPECTED_SCRIPT_VERSION = 3

CONNECTION_STATUS_TIMING_OUT = "Connection timing out. Please restart your emulator, then restart connector_pkmn_emerald.lua"
CONNECTION_STATUS_REFUSED = "Connection refused. Please start your emulator and make sure connector_pkmn_emerald.lua is running"
CONNECTION_STATUS_RESET = "Connection was reset. Please restart your emulator, then restart connector_pkmn_emerald.lua"
CONNECTION_STATUS_TENTATIVE = "Initial connection made"
CONNECTION_STATUS_CONNECTED = "Connected"
CONNECTION_STATUS_INITIAL = "Connection has not been initiated"

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
    # TODO: Add Harbor Mail event here
]
EVENT_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_EVENT_FLAGS}

KEY_LOCATION_FLAGS = [
    "NPC_GIFT_RECEIVED_HM01",
    "NPC_GIFT_RECEIVED_HM02",
    "NPC_GIFT_RECEIVED_HM03",
    "NPC_GIFT_RECEIVED_HM04",
    "NPC_GIFT_RECEIVED_HM05",
    "NPC_GIFT_RECEIVED_HM06",
    "NPC_GIFT_RECEIVED_HM07",
    "NPC_GIFT_RECEIVED_HM08",
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
    "ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_4_SCANNER",
    "ITEM_ABANDONED_SHIP_CAPTAINS_OFFICE_STORAGE_KEY",
    "NPC_GIFT_RECEIVED_OLD_ROD",
    "NPC_GIFT_RECEIVED_GOOD_ROD",
    "NPC_GIFT_RECEIVED_SUPER_ROD",
]
KEY_LOCATION_FLAG_MAP = {data.locations[location_name].flag: location_name for location_name in KEY_LOCATION_FLAGS}


class GBACommandProcessor(ClientCommandProcessor):
    def _cmd_gba(self) -> None:
        """Check GBA Connection State"""
        if isinstance(self.ctx, GBAContext):
            logger.info(f"GBA Status: {self.ctx.gba_status}")


class GBAContext(CommonContext):
    game = "Pokemon Emerald"
    command_processor = GBACommandProcessor
    items_handling = 0b011
    gba_streams: Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    gba_status: Optional[str]
    awaiting_rom = False
    gba_push_pull_task: Optional[asyncio.Task]
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    goal_flag: int = IS_CHAMPION_FLAG

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.gba_streams = None
        self.gba_status = CONNECTION_STATUS_INITIAL
        self.gba_push_pull_task = None
        self.local_checked_locations = set()
        self.local_set_events = {event_name: False for event_name in TRACKER_EVENT_FLAGS}
        self.local_found_key_items = {location_name: False for location_name in KEY_LOCATION_FLAGS}

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(GBAContext, self).server_auth(password_requested)
        if self.auth is None:
            self.awaiting_rom = True
            logger.info("Awaiting connection to GBA to get Player information")
            return
        await self.send_connect()

    def run_gui(self) -> None:
        from kvui import GameManager

        class GBAManager(GameManager):
            base_title = "Archipelago Pokémon Emerald Client"

        self.ui = GBAManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            slot_data = args.get("slot_data", None)
            if slot_data is not None:
                if slot_data["goal"] == Goal.option_champion:
                    self.goal_flag = IS_CHAMPION_FLAG
                elif slot_data["goal"] == Goal.option_steven:
                    self.goal_flag = DEFEATED_STEVEN_FLAG
                elif slot_data["goal"] == Goal.option_norman:
                    self.goal_flag = DEFEATED_NORMAN_FLAG


def create_payload(ctx: GBAContext) -> str:
    payload = json.dumps({
        "items": [[item.item - BASE_OFFSET, item.flags & 1] for item in ctx.items_received]
    })

    return payload


async def handle_read_data(gba_data: Dict[str, Any], ctx: GBAContext) -> None:
    local_checked_locations = set()
    game_clear = False

    if "slot_name" in gba_data:
        if ctx.auth is None:
            ctx.auth = bytes([byte for byte in gba_data["slot_name"] if byte != 0]).decode("utf-8")
            if ctx.awaiting_rom:
                await ctx.server_auth(False)

    if "flag_bytes" in gba_data:
        local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
        local_found_key_items = {location_name: False for location_name in KEY_LOCATION_FLAGS}

        # If flag is set and corresponds to a location, add to local_checked_locations
        for byte_i, byte in enumerate(gba_data["flag_bytes"]):
            for i in range(8):
                if byte & (1 << i) != 0:
                    flag_id = byte_i * 8 + i

                    location_id = flag_id + BASE_OFFSET
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

                    if flag_id == ctx.goal_flag:
                        game_clear = True

                    if flag_id in EVENT_FLAG_MAP:
                        local_set_events[EVENT_FLAG_MAP[flag_id]] = True

                    if flag_id in KEY_LOCATION_FLAG_MAP:
                        local_found_key_items[KEY_LOCATION_FLAG_MAP[flag_id]] = True

        if local_checked_locations != ctx.local_checked_locations:
            ctx.local_checked_locations = local_checked_locations

            if local_checked_locations is not None:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(local_checked_locations)
                }])

        if not ctx.finished_game and game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

        if local_set_events != ctx.local_set_events:
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
            ctx.local_set_events = local_set_events

        if local_found_key_items != ctx.local_found_key_items:
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
            ctx.local_found_key_items = local_found_key_items


async def gba_send_receive_task(ctx: GBAContext) -> None:
    logger.info("Waiting to connect to GBA. Use /gba for status information")
    while not ctx.exit_event.is_set():
        error_status: Optional[str] = None

        if ctx.gba_streams is None:
            # Make initial connection
            try:
                logger.debug("Attempting to connect to GBA...")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", GBA_SOCKET_PORT), timeout=10)
                ctx.gba_status = CONNECTION_STATUS_TENTATIVE
            except asyncio.TimeoutError:
                logger.debug("Connection to GBA timed out. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_TIMING_OUT
                continue
            except ConnectionRefusedError:
                logger.debug("Connection to GBA refused. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_REFUSED
                continue
        else:
            (reader, writer) = ctx.gba_streams

            message = create_payload(ctx).encode("utf-8")
            writer.write(message)
            writer.write(b"\n")

            # Write
            try:
                await asyncio.wait_for(writer.drain(), timeout=2)
            except asyncio.TimeoutError:
                logger.debug("Connection to GBA timed out. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection to GBA lost. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None

            # Read
            try:
                data_bytes = await asyncio.wait_for(reader.readline(), timeout=5)
                data_decoded = json.loads(data_bytes.decode("utf-8"))

                if data_decoded["script_version"] != EXPECTED_SCRIPT_VERSION:
                    logger.warning(f"Your connector script is incompatible with this client. Expected version {EXPECTED_SCRIPT_VERSION}, got {data_decoded['script_version']}.")
                    break

                async_start(handle_read_data(data_decoded, ctx))
            except asyncio.TimeoutError:
                logger.debug("Connection to GBA timed out during read. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection to GBA lost during read. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None

            if error_status:
                ctx.gba_status = error_status
                logger.info("Lost connection to GBA and attempting to reconnect. Use /gba for status updates")
            elif ctx.gba_status == CONNECTION_STATUS_TENTATIVE:
                logger.info("Connected to GBA")
                ctx.gba_status = CONNECTION_STATUS_CONNECTED


async def run_game(rom_file_path: str) -> None:
    auto_start = get_settings()["pokemon_emerald_settings"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(rom_file_path)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, rom_file_path],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(patch_file_path: str) -> None:
    meta_data, output_file_path = Patch.create_rom_file(patch_file_path)
    async_start(run_game(output_file_path))


parser = get_base_parser()
parser.add_argument("apemerald_file", default="", type=str, nargs="?", help="Path to an APEMERALD file")
args = parser.parse_args()


def launch() -> None:
    async def main(args: Namespace) -> None:
        ctx = GBAContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        if args.apemerald_file:
            logger.info("Beginning patching process...")
            async_start(patch_and_run_game(args.apemerald_file))

        ctx.gba_push_pull_task = asyncio.create_task(gba_send_receive_task(ctx), name="GBA Push/Pull")

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
