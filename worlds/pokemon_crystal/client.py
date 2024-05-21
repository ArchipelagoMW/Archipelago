from typing import TYPE_CHECKING, Dict, Set, List

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import BASE_OFFSET, data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

EXPECTED_ROM_VERSION = 3

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
    "EVENT_BEAT_RED"
]
EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_EVENT_FLAGS}

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
    "EVENT_GOT_POKEDEX"
]
KEY_ITEM_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_KEY_ITEM_FLAGS}


class PokemonCrystalClient(BizHawkClient):
    game = "Pokemon Crystal"
    system = ("GB", "GBC")
    local_checked_locations: Set[int]
    patch_suffix = ".apcrystal"
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    phone_trap_locations: List[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.goal_flag = None
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.phone_trap_locations = []

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_info = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Header"], 11, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Version"], 2, "ROM")])))

            rom_name = bytes([byte for byte in rom_info[0] if byte != 0]).decode("ascii")
            rom_version = int.from_bytes(rom_info[1], "little")
            # logger.info(rom_name)
            # logger.info(rom_version)
            if rom_name == "PM_CRYSTAL":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Crystal. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != "AP_CRYSTAL":
                return False
            if rom_version != data.rom_version:
                generator_version = "{0:x}".format(rom_version)
                client_version = "{0:x}".format(data.rom_version)
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                logger.info(f"Client checksum: {client_version}, Generator checksum: {generator_version}")
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
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_Seed_Name"], 64, "ROM")]))[0]
        print(bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8"))
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if ctx.slot_data is not None:
            if ctx.slot_data["goal"] == 0:
                self.goal_flag = data.event_flags["EVENT_BEAT_ELITE_FOUR"]
            else:
                self.goal_flag = data.event_flags["EVENT_BEAT_RED"]
        try:
            overworld_guard = (data.ram_addresses["wArchipelagoSafeWrite"], [1], "WRAM")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 5, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0
            phone_trap_index = read_result[0][4]

            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items].item - BASE_OFFSET
                next_item = next_item if next_item < 256 else next_item - 256
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["wArchipelagoItemReceived"],
                     next_item.to_bytes(1, "little"), "WRAM")
                ])

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wEventFlags"], 0x100, "WRAM")],  # Flags
                [overworld_guard]
            )

            if read_result is None:
                return

            game_clear = False
            local_checked_locations = set()
            local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_found_key_items = {flag_name: False for flag_name in TRACKER_KEY_ITEM_FLAGS}

            flag_bytes = read_result[0]
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + BASE_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if self.goal_flag is not None and flag_id == self.goal_flag:
                            game_clear = True

                        if flag_id in EVENT_FLAG_MAP:
                            local_set_events[EVENT_FLAG_MAP[flag_id]] = True

                        if flag_id in KEY_ITEM_FLAG_MAP:
                            local_found_key_items[KEY_ITEM_FLAG_MAP[flag_id]] = True

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

            if not len(self.phone_trap_locations):
                phone_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(data.rom_addresses["AP_Setting_Phone_Trap_Locations"], 0x40, "ROM")],  # Flags
                    [overworld_guard]
                )
                if phone_result is not None:
                    read_locations = []
                    for i in range(0, 16):
                        loc = int.from_bytes(phone_result[0][i * 4:(i + 1) * 4], "little")
                        read_locations.append(loc)
                    self.phone_trap_locations = read_locations
            else:
                hint_locations = [location for location in self.phone_trap_locations[:phone_trap_index] if
                                  location != 0 and location not in local_checked_locations]
                if len(hint_locations):
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

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
