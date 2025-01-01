import math
from typing import TYPE_CHECKING, List, Optional, Set

from NetUtils import ClientStatus, NetworkItem

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import item_to_index

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class YuGiOh2006Client(BizHawkClient):
    game = "Yu-Gi-Oh! 2006"
    system = "GBA"
    patch_suffix = ".apygo06"
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check if ROM is some version of Yu-Gi-Oh! 2006
            game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 11, "ROM")]))[0]).decode("ascii")
            if game_name != "YUGIOHWCT06":
                return False

            # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
            # validating a ROM where there's no slot name to read.
            try:
                slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x30, 32, "ROM")]))[0]
                self.rom_slot_name = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = False
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.rom_slot_name

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x0, 8, "EWRAM"),
                    (0x52E8, 32, "EWRAM"),
                    (0x5308, 32, "EWRAM"),
                    (0x5325, 1, "EWRAM"),
                    (0x6C38, 4, "EWRAM"),
                ],
            )
            game_state = read_state[0].decode("utf-8")
            locations = read_state[1]
            items = read_state[2]
            amount_items = int.from_bytes(read_state[3], "little")
            money = int.from_bytes(read_state[4], "little")

            # make sure save was created
            if game_state != "YWCT2006":
                return
            local_items = bytearray(items)
            await bizhawk.guarded_write(
                ctx.bizhawk_ctx,
                [(0x5308, parse_items(bytearray(items), ctx.items_received), "EWRAM")],
                [(0x5308, local_items, "EWRAM")],
            )
            money_received = 0
            for item in ctx.items_received:
                if item.item == item_to_index["5000DP"] + 5730000:
                    money_received += 1
            if money_received > amount_items:
                await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [
                        (0x6C38, (money + (money_received - amount_items) * 5000).to_bytes(4, "little"), "EWRAM"),
                        (0x5325, money_received.to_bytes(2, "little"), "EWRAM"),
                    ],
                    [
                        (0x6C38, money.to_bytes(4, "little"), "EWRAM"),
                        (0x5325, amount_items.to_bytes(2, "little"), "EWRAM"),
                    ],
                )

            locs_to_send = set()

            # Check for set location flags.
            for byte_i, byte in enumerate(bytearray(locations)):
                for i in range(8):
                    and_value = 1 << i
                    if byte & and_value != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + 5730001
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            # Send game clear if we're in either any ending cutscene or the credits state.
            if not ctx.finished_game and locations[18] & (1 << 5) != 0:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass


# Parses bit-map for local items and adds the received items to that bit-map
def parse_items(local_items: bytearray, items: List[NetworkItem]) -> bytearray:
    array = local_items
    for item in items:
        index = item.item - 5730001
        if index != 254:
            byte = math.floor(index / 8)
            bit = index % 8
            array[byte] = array[byte] | (1 << bit)
    return array
