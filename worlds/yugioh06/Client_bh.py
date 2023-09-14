import logging
import math
import sys
from typing import TYPE_CHECKING, Optional, Dict, Set, List

from worlds.yugioh06 import item_to_index

# TODO: REMOVE ASAP
# This imports the bizhawk apworld if it's not already imported. This code block should be removed for a PR.
if "worlds._bizhawk" not in sys.modules:
    import importlib
    import os
    import zipimport

    bh_apworld_path = os.path.join(os.path.dirname(sys.modules["worlds"].__file__), "_bizhawk.apworld")
    if os.path.isfile(bh_apworld_path):
        importer = zipimport.zipimporter(bh_apworld_path)
        spec = importer.find_spec(os.path.basename(bh_apworld_path).rsplit(".", 1)[0])
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = f"worlds.{mod.__package__}"
        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        importer.exec_module(mod)
    elif not os.path.isdir(os.path.splitext(bh_apworld_path)[0]):
        logging.error("Did not find _bizhawk.apworld required to play Pokemon Emerald.")


from worlds.LauncherComponents import SuffixIdentifier, components
from NetUtils import ClientStatus, NetworkItem
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

# Add .apemerald suffix to bizhawk client
for component in components:
    if component.script_name == "BizHawkClient":
        component.file_identifier = SuffixIdentifier((*component.file_identifier.suffixes, ".apygo06"))
        break

class YuGiOh2006Client(BizHawkClient):
    game = "Yu-Gi-Oh! 2006"
    system = "GBA"
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # Check if ROM is some version of Yu-Gi-Oh! 2006
            game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 11, "ROM")]))[0]).decode("ascii")
            if game_name != "YUGIOHWCT06":
                return False

            # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
            # validating a ROM where there's no slot name to read.
            try:
                slot_name_bytes = \
                (await bizhawk.read(ctx.bizhawk_ctx, [(0x30, 32, "ROM")]))[0]
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
        ctx.want_slot_data = True
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        ctx.auth = self.rom_slot_name

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        try:
            read_state = await bizhawk.read(ctx.bizhawk_ctx,
                                            [(0x0, 8, "EWRAM"),
                                            (0x52e8, 32, "EWRAM"),
                                            (0x5308, 32, "EWRAM"),
                                            (0x5325, 1, "EWRAM"),
                                            (0x6c38, 4, "EWRAM")])
            game_state = bytes([byte for byte in read_state[0] if byte != 0]).decode("utf-8")
            locations = read_state[1]
            items = read_state[2]
            amount_items = int.from_bytes(read_state[3], "little")
            money = int.from_bytes(read_state[4], "little")

            # make sure save was created
            if game_state != 'YWCT2006':
                return
            await bizhawk.write(ctx.bizhawk_ctx, [(0x5308, parse_items(bytearray(items), ctx.items_received), "EWRAM")])
            money_received = 0
            for item in ctx.items_received:
                if item.item == item_to_index["5000DP"] + 5730000:
                    money_received += 1
            if money_received > amount_items:
                await bizhawk.write(ctx.bizhawk_ctx,
                                [(0x6c38, (money + (money_received - amount_items) * 5000).to_bytes(4, "little"),
                                  "EWRAM"),
                                 (0x5325, money_received.to_bytes(4, "little"), "EWRAM")])

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
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

                # Send game clear if we're in either any ending cutscene or the credits state.
            if not ctx.finished_game and bytearray(locations)[18] & (1 << 5) != 0:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass


def parse_items(localItems, items: List[NetworkItem]):
    array = localItems
    for item in items:
        index = item.item - 5730001
        if index != 254:
            byte = math.floor(index / 8)
            bit = index % 8
            array[byte] = array[byte] | (1 << bit)
    return array


