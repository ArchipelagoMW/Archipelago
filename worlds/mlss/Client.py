import typing
from typing import TYPE_CHECKING, Optional, Set
import struct

from NetUtils import ClientStatus
from .Locations import roomCount, nonBlock, beanstones, roomException, shop, badge, pants, eReward
from .Items import items_by_id

import asyncio

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROOM_ARRAY_POINTER = 0x51fa00

class MLSSClient(BizHawkClient):
    game = "Mario & Luigi Superstar Saga"
    system = "GBA"
    patch_suffix = ".apmlss"
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]
    eCount: int
    eUsed: []
    player_name: Optional[str]
    checked_flags: typing.Dict[int, list] = {}

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.rom_slot_name = None
        self.seed_verify = False
        self.eCount = 0
        self.eUsed = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 14, "ROM")]))
            rom_name = bytes([byte for byte in rom_name_bytes[0] if byte != 0]).decode("UTF-8")
            if not rom_name.startswith("MARIO&LUIGIU"):
                return False
            if rom_name == "MARIO&LUIGIUA8":
                logger.info("ERROR: You appear to be running an unpatched version of Mario & Luigi Superstar Saga. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != "MARIO&LUIGIUAP":
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.rom_slot_name = rom_name
        self.seed_verify = False
        name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xDF0000, 16, "ROM")]))[0])
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name

        for i in range(59):
            self.checked_flags[i] = []

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.player_name

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == 'RoomInfo':
            ctx.seed_name = args['seed_name']

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:
            if ctx.seed_name is None:
                return
            if not self.seed_verify:
                seed = await bizhawk.read(ctx.bizhawk_ctx, [(0xDF00A0, len(ctx.seed_name), "ROM")])
                seed = seed[0].decode("UTF-8")
                if seed != ctx.seed_name:
                    logger.info("ERROR: The ROM you loaded is for a different game of AP. "
                                "Please make sure the host has sent you the correct patch file,"
                                "and that you have opened the correct ROM.")
                    raise bizhawk.ConnectorError("Loaded ROM is for Incorrect lobby.")
                self.seed_verify = True

            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x4564, 59, "EWRAM"),
                                                              (0x2330, 2, "IWRAM"), (0x3FE0, 1, "IWRAM"), (0x304A, 1, "EWRAM"),
                                                              (0x304B, 1, "EWRAM"), (0x304C, 4, "EWRAM"), (0x3060, 6, "EWRAM"),
                                                              (0x4808, 2, "EWRAM"), (0x4407, 1, "EWRAM"), (0x2339, 1, "IWRAM")])
            flags = read_state[0]
            current_room = int.from_bytes(read_state[1], 'little')
            shop_init = read_state[2][0]
            shop_scroll = read_state[3][0] & 0x1F
            is_buy = (read_state[4][0] != 0)
            shop_address = (struct.unpack('<I', read_state[5])[0]) & 0xFFFFFF
            logo = bytes([byte for byte in read_state[6] if byte < 0x70]).decode("UTF-8")
            received_index = (read_state[7][0] << 8) + read_state[7][1]
            cackletta = (read_state[8][0] & 0x40)
            shopping = (read_state[9][0] & 0xF)

            if logo != "MLSSAP":
                return

            locs_to_send = set()

            # Checking shop purchases
            if is_buy:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x304A, [0x0, 0x0], "EWRAM")])
                if shop_address != 0x3c0618 and shop_address != 0x3c0684:
                    location = shop[shop_address][shop_scroll]
                else:
                    if shop_init & 0x1 != 0:
                        location = badge[shop_address][shop_scroll]
                    else:
                        location = pants[shop_address][shop_scroll]
                if location in ctx.server_locations:
                    locs_to_send.add(location)

            # Loop for recieving items. Item is written as an ID into 0x3057.
            # ASM reads the ID in a loop and give the player the item before resetting the RAM address to 0x0.
            # If RAM address isn't 0x0 yet break out and try again later to give the rest of the items
            for i in range(len(ctx.items_received) - received_index):
                item_data = items_by_id[ctx.items_received[received_index + i].item]
                b = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(0x3057, 1, "EWRAM")], [(0x3057, [0x0], "EWRAM")])
                if b is None:
                    break
                await bizhawk.write(ctx.bizhawk_ctx, [(0x3057, [id_to_RAM(item_data.itemID)], "EWRAM"), (0x4808, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100], "EWRAM")])
                await asyncio.sleep(.1)

            # Early return and location send if you are currently in a shop,
            # since other flags aren't going to change
            if shopping & 0x3 == 0x3:
                if locs_to_send != self.local_checked_locations:
                    self.local_checked_locations = locs_to_send

                    if locs_to_send is not None:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": list(locs_to_send)
                        }])
                return

            # Checking flags that aren't digspots or blocks
            for item in nonBlock:
                address, mask, location = item
                if location in self.local_checked_locations:
                    continue
                flag_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(address, 1, "EWRAM"), (0x3060, 6, "EWRAM")])
                flag_byte = flag_bytes[0][0]
                backup_logo = bytes([byte for byte in flag_bytes[1] if byte < 0x70]).decode("UTF-8")
                if backup_logo != "MLSSAP":
                    return
                if flag_byte & mask != 0:
                    if location >= 0xDA0000:
                        await ctx.send_msgs([{
                            "cmd": "Set",
                            "key": f"mlss_flag_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "or", "value": 1 << (location - 0xDA0000)}]
                        }])
                        continue
                    if location in roomException:
                        if current_room not in roomException[location]:
                            exception = True
                        else:
                            exception = False
                    else:
                        exception = True

                    if location in eReward:
                        if location not in self.eUsed:
                            self.eUsed += [location]
                            location = eReward[len(self.eUsed) - 1]
                        else:
                            continue
                    if (location in ctx.server_locations) and exception:
                        locs_to_send.add(location)

            # Check for set location flags.
            for byte_i, byte in enumerate(bytearray(flags)):
                for j in range(8):
                    if j in self.checked_flags[byte_i]:
                        continue
                    and_value = 1 << j
                    if byte & and_value != 0:
                        flag_id = byte_i * 8 + (j + 1)
                        room, item = find_key(roomCount, flag_id)
                        pointer_arr = await bizhawk.read(ctx.bizhawk_ctx,
                                                         [(ROOM_ARRAY_POINTER + ((room - 1) * 4), 4, "ROM")])
                        pointer = (struct.unpack('<I', pointer_arr[0])[0])
                        pointer = pointer & 0xFFFFFF
                        offset = await bizhawk.read(ctx.bizhawk_ctx, [(pointer, 1, "ROM")])
                        offset = offset[0][0]
                        if offset != 0:
                            offset = 2
                        pointer += (item * 8) + 1 + offset
                        for key, value in beanstones.items():
                            if pointer == value:
                                pointer = key
                                break
                        if pointer in ctx.server_locations:
                            self.checked_flags[byte_i] += [j]
                            locs_to_send.add(pointer)

            if not ctx.finished_game and cackletta != 0:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mlss_room_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": current_room}]
            }])

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass


def find_key(dictionary, target):
    leftover = target

    for key, value in dictionary.items():
        if leftover > value:
            leftover -= value
        else:
            return key, leftover


def id_to_RAM(id_: int):
    code = id_
    if 0x1C <= code <= 0x1F:
        code += 0xE
    if 0x20 <= code <= 0x26:
        code -= 0x4
    return code
