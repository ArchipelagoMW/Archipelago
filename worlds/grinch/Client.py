from typing import TYPE_CHECKING
from .Locations import grinch_locations
from .Items import ALL_ITEMS_TABLE
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.Files import APDeltaPatch
if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from CommonClient import logger


class GrinchClient(BizHawkClient):
    game = "The Grinch"
    system = "PSX"
    patch_suffix = ".apgrinch"
    items_handling = 0b111
    last_received_index = 0

    def __init__(self):
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        # TODO Check the ROM data to see if it matches against bytes expected
        grinch_identifier_ram_address: int = 0x00928C
        bytes_expected: bytes = bytes.fromhex("e903c14f4becf89082f43ec936a68e62")
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                grinch_identifier_ram_address, 11, "MainRAM")]))[0]

            psx_rom_name = bytes_actual.decode("ascii")
            if psx_rom_name != "SLUS_011.97":
                logger.error("Invalid rom detected. You are not playing Grinch USA Version.")
                raise Exception("Invalid rom detected. You are not playing Grinch USA Version.")
        except Exception():
            return False

        ctx.game = self.game
        ctx.items_handling = self.items_handling
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        await ctx.get_username()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        #If the player is not connected to an AP Server, or their connection was disconnected.
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:
            # # Read save data
            # save_data = await bizhawk.read(
            #     ctx.bizhawk_ctx,
            #     [(0x3000100, 20, "System Bus")]
            # )[0]
            #
            # # Check locations
            # if save_data[2] & 0x04:
            #     await ctx.send_msgs([{
            #         "cmd": "LocationChecks",
            #         "locations": [23]
            #     }])
            #
            # # Send game clear
            # if not ctx.finished_game and (save_data[5] & 0x01):
            #     await ctx.send_msgs([{
            #         "cmd": "StatusUpdate",
            #         "status": ClientStatus.CLIENT_GOAL
            #     }])
            await self.location_checker(ctx)
            await self.receiving_items_handler(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_checker(self, ctx: "BizHawkClientContext"):
        # TODO Write a function to check if I am ingame, determine how I am playing the game vs not in demo mode/game menu
        # Update the AP Server to know what locations are not checked yet.
        for missing_location in ctx.missing_locations:
            local_location = ctx.location_names.lookup_in_game(missing_location)
            # Missing location is the AP ID & we need to convert it back to a location name within our game.
            # Using the location name, we can then get the Grinch ram data from there.
            grinch_loc_ram_data = grinch_locations[local_location]

            # Grinch ram data may have more than one address to update, so we are going to loop through all addresses in a location
            for addr_to_update in grinch_loc_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                current_ram_address_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                    addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                if is_binary:
                    if (current_ram_address_value & (1 << addr_to_update.binary_bit_pos)) > 0:
                        ctx.locations_checked.add(missing_location)
                else:
                    expected_int_value = addr_to_update.value
                    if expected_int_value == current_ram_address_value:
                        ctx.locations_checked.add(missing_location)

        # Update the AP server with the locally checked list of locations (In other words, locations I found in Grinch)
        await ctx.check_locations(ctx.locations_checked)

    async def receiving_items_handler(self, ctx: "BizHawkClientContext"):
        # Len will give us the size of the items received list & we will track that against how many items we received already
        # If the list says that we have 3 items and we already received items, we will ignore and continue.
        # Otherwise, we will get the new items and give them to the player.
        if len(ctx.items_received) == self.last_received_index:
            return

        # Ensures we only get the new items that we want to give the player
        new_items_only = ctx.items_received[self.last_received_index:]

        for item_received in new_items_only:
            local_item = ctx.item_names.lookup_in_game(item_received.item)
            grinch_item_ram_data = ALL_ITEMS_TABLE[local_item]

            for addr_to_update in grinch_item_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                if is_binary:
                    current_ram_address_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                        addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                    current_ram_address_value = (current_ram_address_value | (1 << addr_to_update.binary_bit_pos))
                else:
                    current_ram_address_value = addr_to_update.value

                # Write the updated value back into RAM
                await bizhawk.write(ctx.bizhawk_ctx, [(addr_to_update.ram_address,
                    current_ram_address_value.to_bytes(addr_to_update.bit_size, "little"), "MainRAM")])

            self.last_received_index += 1