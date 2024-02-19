from typing import TYPE_CHECKING, Dict, Set

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import BASE_OFFSET, data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

EXPECTED_ROM_VERSION = 2


class PokemonCrystalClient(BizHawkClient):
    game = "Pokemon Crystal"
    system = ("GB", "GBC")
    local_checked_locations: Set[int]
    patch_suffix = ".apcrystal"
    local_checked_locations: Set[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.goal_flag = None

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_info = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Header"], 11, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Version"], 1, "ROM")])))

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
            if rom_version != EXPECTED_ROM_VERSION:
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
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 4, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0

            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items]
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["wArchipelagoItemReceived"],
                     (next_item.item - BASE_OFFSET).to_bytes(1, "little"), "WRAM")
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
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
