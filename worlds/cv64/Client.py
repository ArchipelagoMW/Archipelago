from typing import TYPE_CHECKING, Optional, Dict, Set
from .Locations import base_id
from .Text import cv64_text_wrap, cv64_string_to_bytes
from time import time

from NetUtils import ClientStatus
from worlds.AutoBizHawkClient import BizHawkClient

if TYPE_CHECKING:
    from BizHawkClient import BizHawkClientContext
else:
    BizHawkClientContext = object


class Castlevania64Client(BizHawkClient):
    game = "Castlevania 64"
    system = "N64"
    local_checked_locations: Set[int]
    rom_slot_name: Optional[str]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from BizHawkClient import RequestFailedError, bizhawk_read
        from CommonClient import logger

        try:
            # Check if ROM is some version of Castlevania 64
            game_name = ((await bizhawk_read(ctx, [(0x20, 0x14, "ROM")]))[0]).decode("ascii")
            if game_name != "CASTLEVANIA         ":
                return False
            
            # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
            # validating a ROM where there's no slot name to read.
            try:
                slot_name_bytes = (await bizhawk_read(ctx, [(0xBFBFE0, 0x10, "ROM")]))[0]
                self.rom_slot_name = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        ctx.auth = self.rom_slot_name

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        from BizHawkClient import RequestFailedError, bizhawk_guarded_write, bizhawk_read

        try:
            read_state = await bizhawk_read(ctx, [(0x342084, 4, "RDRAM"),
                                                  (0x389BDF, 5, "RDRAM"),
                                                  (0x389BE4, 224, "RDRAM"),
                                                  (0x389EFB, 1, "RDRAM")])

            game_state = int.from_bytes(read_state[0], "big")
            # deathlink_number = int.from_bytes(bytearray(read_state[1][3:5]), "big")
            save_struct = read_state[2]
            cutscene_value = int.from_bytes(read_state[3], "big")

            if game_state not in [0x00000002 or 0x0000000B]:  # Make sure we are in the Gameplay or Credits states.
                return

            num_received_items = int.from_bytes(bytearray(save_struct[0xDA:0xDC]), "big")

            # If the game hasn't received all items yet, the received item struct doesn't contain an item, the current
            # number of received items still matches what we read before, and there are no open text boxes, then
            # fill it with the next item and write the "item from player" text in its buffer. The game will increment
            # the number of received items on its own.
            if num_received_items < len(ctx.items_received):
                next_item = ctx.items_received[num_received_items]
                if next_item.flags & 0b001:
                    text_color = [0xA2, 0x0C]
                elif next_item.flags & 0b010:
                    text_color = [0xA2, 0x0A]
                elif next_item.flags & 0b100:
                    text_color = [0xA2, 0x0B]
                else:
                    text_color = [0xA2, 0x02]
                received_text, num_lines = cv64_text_wrap(f"{ctx.item_names[next_item.item]}\n"
                                                          f"from {ctx.player_names[next_item.player]}", 96)
                await bizhawk_guarded_write(ctx, [(0x389BE1, (next_item.item - base_id).to_bytes(1, "big"), "RDRAM"),
                                                  (0x18C0A8, text_color + cv64_string_to_bytes(received_text, False),
                                                   "RDRAM"),
                                                  (0x18C1A7, [num_lines], "RDRAM")],
                                            [(0x389BE1, [0x00], "RDRAM"), (0x389CBE, save_struct[0xDA:0xDC], "RDRAM"),
                                             (0x342891, [0x02], "RDRAM")])

            flag_bytes = bytearray(save_struct[0x00:0x44]) + bytearray(save_struct[0x90:0x9F])
            locs_to_send = set()

            # Check for set location flags.
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    and_value = 0x80 >> i
                    if byte & and_value != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + base_id
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

            # Send a DeathLink if we died on our own
            # if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time():
                # currently_dead = save_struct[0xA4] & 0x80
                # await ctx.handle_deathlink_state(currently_dead)

            # Send game clear if we're in either any ending cutscene or the credits state.
            if not ctx.finished_game and (0x26 <= int(cutscene_value) <= 0x2E or game_state == 0x0000000B):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
