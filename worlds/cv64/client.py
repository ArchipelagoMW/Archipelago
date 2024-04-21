from typing import TYPE_CHECKING, Set
from .locations import base_id
from .text import cv64_text_wrap, cv64_string_to_bytearray

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
import base64
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class Castlevania64Client(BizHawkClient):
    game = "Castlevania 64"
    system = "N64"
    patch_suffix = ".apcv64"
    self_induced_death = False
    received_deathlinks = 0
    death_causes = []
    currently_shopping = False
    local_checked_locations: Set[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 0x14, "ROM"), (0xBFBFD0, 12, "ROM")])
            if game_names[0].decode("ascii") != "CASTLEVANIA         ":
                return False
            if game_names[1] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                logger.info("ERROR: You appear to be running an unpatched version of Castlevania 64. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if game_names[1].decode("ascii") != "ARCHIPELAGO1":
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
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(0xBFBFE0, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            self.received_deathlinks += 1
            if "cause" in args["data"]:
                cause = args["data"]["cause"]
                if len(cause) > 88:
                    cause = cause[0x00:0x89]
            else:
                cause = f"{args['data']['source']} killed you!"
            self.death_causes.append(cause)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        try:
            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x342084, 4, "RDRAM"),
                                                              (0x389BDE, 6, "RDRAM"),
                                                              (0x389BE4, 224, "RDRAM"),
                                                              (0x389EFB, 1, "RDRAM"),
                                                              (0x389EEF, 1, "RDRAM"),
                                                              (0xBFBFDE, 2, "ROM")])

            game_state = int.from_bytes(read_state[0], "big")
            save_struct = read_state[2]
            written_deathlinks = int.from_bytes(bytearray(read_state[1][4:6]), "big")
            deathlink_induced_death = int.from_bytes(bytearray(read_state[1][0:1]), "big")
            cutscene_value = int.from_bytes(read_state[3], "big")
            current_menu = int.from_bytes(read_state[4], "big")
            num_received_items = int.from_bytes(bytearray(save_struct[0xDA:0xDC]), "big")
            rom_flags = int.from_bytes(read_state[5], "big")

            # Make sure we are in the Gameplay or Credits states before detecting sent locations and/or DeathLinks.
            # If we are in any other state, such as the Game Over state, set self_induced_death to false, so we can once
            # again send a DeathLink once we are back in the Gameplay state.
            if game_state not in [0x00000002, 0x0000000B]:
                self.self_induced_death = False
                return

            # Enable DeathLink if the bit for it is set in our ROM flags.
            if "DeathLink" not in ctx.tags and rom_flags & 0x0100:
                await ctx.update_death_link(True)

            # Scout the Renon shop locations if the shopsanity flag is written in the ROM.
            if rom_flags & 0x0001 and ctx.locations_info == {}:
                await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": [base_id + i for i in range(0x1C8, 0x1CF)],
                        "create_as_hint": 0
                    }])

            # Send a DeathLink if we died on our own independently of receiving another one.
            if "DeathLink" in ctx.tags and save_struct[0xA4] & 0x80 and not self.self_induced_death and not \
                    deathlink_induced_death:
                self.self_induced_death = True
                if save_struct[0xA4] & 0x08:
                    # Special death message for dying while having the Vamp status.
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} became a vampire and drank your blood!")
                else:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} perished. Dracula has won!")

            # Write any DeathLinks received along with the corresponding death cause starting with the oldest.
            # To minimize Bizhawk Write jank, the DeathLink write will be prioritized over the item received one.
            if self.received_deathlinks and not self.self_induced_death and not written_deathlinks:
                death_text, num_lines = cv64_text_wrap(self.death_causes[0], 96)
                await bizhawk.write(ctx.bizhawk_ctx, [(0x389BE3, [0x01], "RDRAM"),
                                                      (0x389BDF, [0x11], "RDRAM"),
                                                      (0x18BF98, bytearray([0xA2, 0x0B]) +
                                                       cv64_string_to_bytearray(death_text, False), "RDRAM"),
                                                      (0x18C097, [num_lines], "RDRAM")])
                self.received_deathlinks -= 1
                del self.death_causes[0]
            else:
                # If the game hasn't received all items yet, the received item struct doesn't contain an item, the
                # current number of received items still matches what we read before, and there are no open text boxes,
                # then fill it with the next item and write the "item from player" text in its buffer. The game will
                # increment the number of received items on its own.
                if num_received_items < len(ctx.items_received):
                    next_item = ctx.items_received[num_received_items]
                    if next_item.flags & 0b001:
                        text_color = bytearray([0xA2, 0x0C])
                    elif next_item.flags & 0b010:
                        text_color = bytearray([0xA2, 0x0A])
                    elif next_item.flags & 0b100:
                        text_color = bytearray([0xA2, 0x0B])
                    else:
                        text_color = bytearray([0xA2, 0x02])
                    received_text, num_lines = cv64_text_wrap(f"{ctx.item_names[next_item.item]}\n"
                                                              f"from {ctx.player_names[next_item.player]}", 96)
                    await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                [(0x389BE1, [next_item.item & 0xFF], "RDRAM"),
                                                 (0x18C0A8, text_color + cv64_string_to_bytearray(received_text, False),
                                                  "RDRAM"),
                                                 (0x18C1A7, [num_lines], "RDRAM")],
                                                [(0x389BE1, [0x00], "RDRAM"),   # Remote item reward buffer
                                                 (0x389CBE, save_struct[0xDA:0xDC], "RDRAM"),  # Received items
                                                 (0x342891, [0x02], "RDRAM")])   # Textbox state

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

            # Check the menu value to see if we are in Renon's shop, and set currently_shopping to True if we are.
            if current_menu == 0xA:
                self.currently_shopping = True

            # If we are currently shopping, and the current menu value is 0 (meaning we just left the shop), hint the
            # un-bought shop locations that have progression.
            if current_menu == 0 and self.currently_shopping:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": [loc for loc, n_item in ctx.locations_info.items() if n_item.flags & 0b001],
                    "create_as_hint": 2
                }])
                self.currently_shopping = False

            # Send game clear if we're in either any ending cutscene or the credits state.
            if not ctx.finished_game and (0x26 <= int(cutscene_value) <= 0x2E or game_state == 0x0000000B):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
