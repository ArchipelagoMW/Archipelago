from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.Files import APDeltaPatch
if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class GrinchClient(BizHawkClient):
    game = "The Grinch"
    system = "PSX"
    patch_suffix = ".apgrinch"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        grinch_identifier_ram_address: int = 0x00928C
        bytes_expected: bytes = bytes.fromhex("53554C533131305F3B37392E")
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                grinch_identifier_ram_address, len(bytes_expected), "MainRAM"
            )]))[0]
        except Exception():
            return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read save data
            save_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x3000100, 20, "System Bus")]
            )[0]

            # Check locations
            if save_data[2] & 0x04:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [23]
                }])

            # Send game clear
            if not ctx.finished_game and (save_data[5] & 0x01):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass