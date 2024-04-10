from typing import TYPE_CHECKING, Set
from .locations import base_id, get_location_names_to_ids
from .items import get_item_info

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
import base64
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class CastlevaniaCotMClient(BizHawkClient):
    game = "Castlevania - Circle of the Moon"
    system = "GBA"
    patch_suffix = ".apcvcotm"
    local_dss = {}
    self_induced_death = False
    received_deathlinks = 0
    local_checked_locations: Set[int]
    killed_drac_2 = False

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 0xC, "ROM"), (0x7FFF00, 12, "ROM")])
            if game_names[0].decode("ascii") != "DRACULA AGB1":
                return False
            if game_names[1] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                logger.info("ERROR: You appear to be running an unpatched version of Castlevania: Circle of the Moon. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if game_names[1].decode("ascii") != "ARCHIPELAG01":
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
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(0x7FFF10, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            self.received_deathlinks += 1

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        try:
            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x45D8, 1, "EWRAM"),
                                                              (0x25374, 32, "EWRAM"),
                                                              (0x25674, 20, "EWRAM"),
                                                              (0x253D0, 2, "EWRAM"),
                                                              (0x2572C, 3, "EWRAM"),
                                                              (0x2572F, 8, "EWRAM")])

            game_state = int.from_bytes(read_state[0], "little")
            flag_bytes = read_state[1]
            cards_array = list(read_state[2])
            max_ups_array = list(read_state[4])
            magic_items_array = list(read_state[5])
            num_received_items = int.from_bytes(bytearray(read_state[3]), "little")

            # Make sure we are in the Gameplay or Credits states before detecting sent locations.
            # If we are in any other state, such as the Game Over state, reset the textbox buffers back to 0 so that we
            # don't receive the most recent item upon loading back in.
            #
            # If the intro cutscene floor broken flag is not set, then assume we are in the demo; at no point during
            # regular gameplay will this flag not be set.
            if game_state not in [0x6, 0x21] or not flag_bytes[6] & 0x02:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x25300, [0, 0, 0, 0, 0, 0, 0, 0], "EWRAM")])
                return

            # Scout all Locations and capture the ones with local DSS Cards.
            if ctx.locations_info == {}:

                await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": [code for name, code in get_location_names_to_ids().items()],
                        "create_as_hint": 0
                    }])
            elif self.local_dss == {}:
                self.local_dss = {loc.item & 0xFF: location_id for location_id, loc in ctx.locations_info.items()
                                  if loc.player == ctx.slot and (loc.item >> 8) & 0xFF == 0xE6}

            if num_received_items < len(ctx.items_received):
                next_item = ctx.items_received[num_received_items]

                # Figure out what inventory array and offset from said array to increment based on what we are
                # receiving.
                item_type = next_item.item & 0xFF00
                item_index = next_item.item & 0xFF
                if item_type == 0xE600:  # Card
                    inv_offset = 0x25674
                    inv_array = cards_array
                elif item_type == 0xE800:  # Magic Item
                    inv_offset = 0x2572F
                    inv_array = magic_items_array
                    if item_index > 5:  # The unused Map's index is skipped over.
                        item_index -= 1
                else:  # Max Up
                    inv_offset = 0x2572C
                    inv_array = max_ups_array

                await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                            [(0x25300, bytearray(int.to_bytes(get_item_info(ctx.item_names[
                                                                                                next_item.item],
                                                                 "textbox id"), 2, "little")), "EWRAM"),
                                             (0x25304, [1], "EWRAM"),
                                             ((inv_offset + item_index), [inv_array[item_index] + 1], "EWRAM")],
                                            [(0x25300, [0], "EWRAM"),    # Textbox ID buffer
                                             (0x25304, [0], "EWRAM"),    # Received item index buffer
                                             (0x253D0, read_state[3], "EWRAM")])  # Received items index

            locs_to_send = set()

            # Check for set location flags.
            for byte_index, byte in enumerate(flag_bytes):
                for i in range(8):
                    and_value = 0x01 << i
                    if byte & and_value != 0:
                        flag_id = byte_index * 8 + i

                        location_id = flag_id + base_id
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

                        # Detect the "killed Dracula II" flag for the purposes of sending the game clear.
                        if flag_id == 0xBC:
                            self.killed_drac_2 = True

            # Check for acquired local DSS Cards.
            for byte_index, byte in enumerate(cards_array):
                if byte and byte_index in self.local_dss:
                    locs_to_send.add(self.local_dss[byte_index])

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

            # Send game clear if we're in the credits state or the Dracula II kill was detected.
            if not ctx.finished_game and (game_state == 0x21 or self.killed_drac_2):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
