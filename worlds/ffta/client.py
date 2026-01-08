from typing import TYPE_CHECKING, Dict, Set, List
import time
import logging
import sys
import struct
import asyncio
import Utils

from .options import FinalMission, JobUnlockReq

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .items import JobUnlockDict
from .locations import (MissionGroups, DispatchMissionGroups, bitflags)


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object


class FFTAClient(BizHawkClient):
    game = "Final Fantasy Tactics Advance"
    system = "GBA"
    patch_suffix = ".apffta"
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    path_items: List[int]
    pending_death_link: bool = False
    sending_death_link: bool = False
    death_link: bool = False
    job_unlock: bool = False
    goal_flag: int
    goal_id: int = 0
    unlock_law_cards: bool
    unlock_law_card_shop: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.unlock_law_cards = False
        self.unlock_law_card_shop = False

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:

        try:
            game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0A0, 10, "ROM")]))[0]).decode("ascii")
            print('Game name for validate rom ' + game_name)
            if game_name != "FFTA_USVER":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        print('context is registered for FFTA')
        print(ctx.game)
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        return True

    """"
    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)

    async def send_deathlink(self, ctx: BizHawkClientContext):
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Someone in Ivalice has fallen.")

    def on_deathlink(self, ctx: BizHawkClientContext):
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xAAABD0, 64, "ROM")]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
    """

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if ctx.slot_data is not None:
            if ctx.slot_data["final_mission"] == FinalMission.option_royal_valley:
                self.goal_id = 0x64

            elif ctx.slot_data["final_mission"] == FinalMission.option_decision_time:
                self.goal_id = 0x93

            if ctx.slot_data["law_cards"] > 1:
                self.unlock_law_cards = True
                if ctx.slot_data["law_cards"] > 2:
                    self.unlock_law_card_shop = True

            """
            if "job_unlock_req" in ctx.slot_data:
                if ctx.slot_data["job_unlock_req"] == JobUnlockReq.option_job_items:
                    self.job_unlock = True

            """
        try:
            if self.unlock_law_cards:
                law_card_read = await bizhawk.read(ctx.bizhawk_ctx,
                                                   [(0x02001fb0, 1, "System Bus"),
                                                    (0x02002025, 1, "System Bus"),
                                                    ])
                law_card_flags = [int.from_bytes(x, "little") for x in law_card_read]

                write_flags = [(0x02001fb0, (law_card_flags[0] | 0x80).to_bytes(1, "little"), "System Bus")]
                if self.unlock_law_card_shop:
                    write_flags += [(0x02002025, (law_card_flags[1] | 0x01).to_bytes(1, "little"), "System Bus")]

                if law_card_flags[0] < 0x80 or (self.unlock_law_card_shop and law_card_flags[1] < 0x01):
                    await bizhawk.write(ctx.bizhawk_ctx, write_flags)

            offset = 41234532
            flag_list = [(0x2001FD0, 50, "System Bus"), (0x2001FD1, 1, "System Bus"),
                         (0x2002AF0, 2, "System Bus"), (0x200FA18, 2, "System Bus"),
                         (0x2002B08, 0xFC, "System Bus"), (0x2002192, 1, "System Bus"),
                         (0x2000098, 1, "System Bus")]
            read_result = await bizhawk.read(ctx.bizhawk_ctx, flag_list)
            flag_bytes = read_result[0]
            received_items = int.from_bytes(read_result[2], "little")
            # mission_items = read_result[4]

            # Check for job unlock items
            """
            for byte_i, item in enumerate(mission_items):
                # Handle job unlock items

                if item in JobUnlockDict:
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x2002B08 + byte_i, bytes([0x00]), "System Bus")])

                    job_unlocks = JobUnlockDict[item]

                    if type(job_unlocks) is list:
                        for i in range(len(job_unlocks)):
                            await bizhawk.write(ctx.bizhawk_ctx, [(job_unlocks[i], bytes([0x00]), "ROM")])

                    else:
                        await bizhawk.write(ctx.bizhawk_ctx, [(job_unlocks, bytes([0x00]), "ROM")])
            """
            self.goal_flag = read_result[5]

            local_checked_locations = set()
            game_clear = False

            # Check if goal status is reached
            if self.goal_flag[0] == self.goal_id and self.goal_id != 0:
                game_clear = True

            # Check set flags
            for byte_i, byte in enumerate(flag_bytes):

                for i in range(8):

                    if byte & (1 << i) == bitflags[i]:

                        for mission in MissionGroups:
                            if byte & (1 << i) == mission[1] and byte_i == mission[2]:
                                for missionLocation in mission[0]:
                                    location_id = missionLocation.rom_address
                                    if location_id in ctx.server_locations:
                                        local_checked_locations.add(location_id)

                        for mission in DispatchMissionGroups:
                            if byte & (1 << i) == mission[1] and byte_i == mission[2]:
                                for missionLocation in mission[0]:
                                    location_id = missionLocation.rom_address
                                    if location_id in ctx.server_locations:
                                        local_checked_locations.add(location_id)

            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

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

            guard_list = [(0x200f85c, [0x00], "System Bus"), (0x2019EB9, [0x01], "System Bus"),
                          (0x2019976, [0x01], "System Bus"), (0x201997F, [0x00], "System Bus")]

            if received_items < len(ctx.items_received):
                next_item = ctx.items_received[received_items]

                not_moving = int.from_bytes(read_result[3], "little") != 0

                # Make sure Marche isn't moving on the world map when receiving an item
                if not_moving:
                    next_item_id = next_item.item - offset

                    # Make case for trap items received
                    # elif next_item.item - offset == 0x11111:

                    if len(ctx.items_received) - received_items > 1:
                        item_after = ctx.items_received[received_items + 1]
                        item_after_id = item_after.item - offset

                        await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                    [(0x2002c10, [0x00], "System Bus"),
                                                     (0x200fd2b, [0x00], "System Bus"),
                                                     (0x201f46c, (next_item_id).to_bytes(2, "little"),
                                                      "System Bus"),
                                                     (0x201f46e, (item_after_id).to_bytes(2, "little"),
                                                      "System Bus"),
                                                     (0x2002AF0, (received_items + 2).to_bytes(2, "little"),
                                                      "System Bus"),
                                                     (0x200f85c, [0x06], "System Bus"),
                                                     ], guard_list)

                    else:
                        await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                    [(0x2002c10, [0x00], "System Bus"),
                                                     (0x200fd2b, [0x00], "System Bus"),
                                                     (0x201f46c, (next_item_id).to_bytes(2, "little"), "System Bus"),
                                                     (0x201f46e, (0x0000).to_bytes(2, "little"), "System Bus"),
                                                     (0x2002AF0, (received_items + 1).to_bytes(2, "little"),
                                                      "System Bus"),
                                                     (0x200f85c, [0x06], "System Bus"),
                                                     ], guard_list)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
