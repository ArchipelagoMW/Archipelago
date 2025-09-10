import time
from typing import TYPE_CHECKING
import asyncio
import NetUtils
import copy

import Utils
from .Locations import grinch_locations, GrinchLocation
from .Items import ALL_ITEMS_TABLE, MISSION_ITEMS_TABLE, GADGETS_TABLE, KEYS_TABLE, GrinchItemData #, SLEIGH_PARTS_TABLE
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from CommonClient import logger


# Stores received index of last item received in PS1 memory card save data
# By storing this index, it will remember the last item received and prevent item duplication loops
RECV_ITEM_ADDR = 0x010068
RECV_ITEM_BITSIZE = 4

# Maximum number of times we check if we are in demo mode or not
MAX_DEMO_MODE_CHECK = 30

# List of Menu Map IDs
MENU_MAP_IDS: list[int] = [0x00, 0x02, 0x35, 0x36, 0x37]

MAX_EGGS: int = 200
EGG_COUNT_ADDR: int = 0x010058
EGG_ADDR_BYTESIZE: int = 2

class GrinchClient(BizHawkClient):
    game = "The Grinch"
    system = "PSX"
    patch_suffix = ".apgrinch"
    items_handling = 0b111
    demo_mode_buffer = 0
    last_map_location = -1
    ingame_log = False
    previous_egg_count: int = 0

    def __init__(self):
        super().__init__()
        self.last_received_index = 0
        self.loading_bios_msg = False
        self.loc_unlimited_eggs = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger
        # TODO Check the ROM data to see if it matches against bytes expected
        grinch_identifier_ram_address: int = 0x00928C
        bios_identifier_ram_address: int = 0x097F30
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                grinch_identifier_ram_address, 11, "MainRAM")]))[0]

            psx_rom_name = bytes_actual.decode("ascii")
            if psx_rom_name != "SLUS_011.97":
                bios_bytes_check: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    bios_identifier_ram_address, 24, "MainRAM")]))[0]
                if "System ROM Version" in bios_bytes_check.decode("ascii"):
                    if not self.loading_bios_msg:
                        self.loading_bios_msg = True
                        logger.error("BIOS is currently loading. Will wait up to 5 seconds before retrying.")
                    return False

                logger.error("Invalid rom detected. You are not playing Grinch USA Version.")
                raise Exception("Invalid rom detected. You are not playing Grinch USA Version.")
        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = self.items_handling
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.25
        self.loading_bios_msg = False

        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        from CommonClient import logger
        super().on_package(ctx, cmd, args)
        match cmd:
            case "Connected":  # On Connect
                self.loc_unlimited_eggs = bool(ctx.slot_data["give_unlimited_eggs"])
                logger.info("You are now connected to the client. "+
                    "There may be a slight delay to check you are not in demo mode before locations start to send.")

                ring_link_enabled = bool(ctx.slot_data["ring_link"])

                tags = copy.deepcopy(ctx.tags)
                if ring_link_enabled:
                    Utils.async_start(self.ring_link_output(ctx), name="EggLink")
                    ctx.tags.add("RingLink")
                else:
                    ctx.tags -= { "RingLink" }

                if tags != ctx.tags:
                    Utils.async_start(ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}]), "Update RingLink Tags")

            case "Bounced":
                if "tags" not in args:
                    return

                if "RingLink" in ctx.tags and "RingLink" in args["tags"] and args["data"]["source"] != ctx.player_names[ctx.slot]:
                    Utils.async_start(self.ring_link_input(args["data"]["amount"], ctx), "SyncEggs")

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        await ctx.get_username()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import  logger
        #If the player is not connected to an AP Server, or their connection was disconnected.
        if not ctx.slot:
            return

        try:
            if not await self.ingame_checker(ctx):
                return

            await self.location_checker(ctx)
            await self.receiving_items_handler(ctx)
            await self.goal_checker(ctx)
            await self.option_handler(ctx)
            await self.constant_address_update(ctx)

        except bizhawk.RequestFailedError as ex:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            logger.error("Failure to connect / authenticate the grinch. Error details: " + str(ex))
            pass
        except Exception as genericEx:
            # For all other errors, catch this and let the client gracefully disconnect
            logger.error("Unknown error occurred while playing the grinch. Error details: " + str(genericEx))
            await ctx.disconnect(False)
            pass

    async def location_checker(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        # Update the AP Server to know what locations are not checked yet.
        local_locations_checked: list[int] = []
        local_ap_locations: set[int] = copy.deepcopy(ctx.missing_locations)
        for missing_location in local_ap_locations:
            # local_location = ctx.location_names.lookup_in_game(missing_location)
            # Missing location is the AP ID & we need to convert it back to a location name within our game.
            # Using the location name, we can then get the Grinch ram data from there.
            grinch_loc_name = ctx.location_names.lookup_in_game(missing_location)
            grinch_loc_ram_data = grinch_locations[grinch_loc_name]

            # Grinch ram data may have more than one address to update, so we are going to loop through all addresses in a location
            # We use a list here to keep track of all our checks. If they are all true, then and only then do we mark that location as checked.
            ram_checked_list: list[bool] = []
            for addr_to_update in grinch_loc_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                current_ram_address_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                    addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                if is_binary:
                    ram_checked_list.append((current_ram_address_value & (1 << addr_to_update.binary_bit_pos)) > 0)
                else:
                    expected_int_value = addr_to_update.value
                    ram_checked_list.append(expected_int_value == current_ram_address_value)
            if all(ram_checked_list):
                local_locations_checked.append(GrinchLocation.get_apid(grinch_loc_ram_data.id))

        # Update the AP server with the locally checked list of locations (In other words, locations I found in Grinch)
        locations_sent_to_ap: set[int] = await ctx.check_locations(local_locations_checked)
        if len(locations_sent_to_ap) > 0:
            await self.remove_physical_items(ctx)
        ctx.locations_checked = set(local_locations_checked)

    async def receiving_items_handler(self, ctx: "BizHawkClientContext"):
        # Len will give us the size of the items received list & we will track that against how many items we received already
        # If the list says that we have 3 items and we already received items, we will ignore and continue.
        # Otherwise, we will get the new items and give them to the player.

        self.last_received_index = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
            RECV_ITEM_ADDR, RECV_ITEM_BITSIZE, "MainRAM")]))[0], "little")
        if len(ctx.items_received) == self.last_received_index:
            return

        # Ensures we only get the new items that we want to give the player
        new_items_only = ctx.items_received[self.last_received_index:]

        for item_received in new_items_only:
            local_item = ctx.item_names.lookup_in_game(item_received.item)
            grinch_item_ram_data = ALL_ITEMS_TABLE[local_item]

            for addr_to_update in grinch_item_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                current_ram_address_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                    addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                if is_binary:
                    current_ram_address_value = (current_ram_address_value | (1 << addr_to_update.binary_bit_pos))
                elif addr_to_update.update_existing_value:
                    # Grabs minimum value of a list of numbers and makes sure it does not go above max count possible
                    current_ram_address_value += addr_to_update.value
                    current_ram_address_value = min(current_ram_address_value, addr_to_update.max_count)
                else:
                    current_ram_address_value = addr_to_update.value

                # Write the updated value back into RAM
                await self.update_and_validate_address(ctx, addr_to_update.ram_address, current_ram_address_value, addr_to_update.bit_size)


            self.last_received_index += 1
            await self.update_and_validate_address(ctx, RECV_ITEM_ADDR, self.last_received_index, RECV_ITEM_BITSIZE)

    async def goal_checker(self, ctx: "BizHawkClientContext"):
        if not ctx.finished_game:
            goal_loc = grinch_locations["Neutralizing Santa"]
            goal_ram_address = goal_loc.update_ram_addr[0]
            current_ram_address_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                goal_ram_address.ram_address, goal_ram_address.bit_size, "MainRAM")]))[0], "little")
            if (current_ram_address_value & (1 << goal_ram_address.binary_bit_pos)) > 0:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": NetUtils.ClientStatus.CLIENT_GOAL,
                }])

    # This function's entire purpose is to take away items we physically received ingame, but have not received from AP
    async def remove_physical_items(self, ctx: "BizHawkClientContext"):
        list_recv_itemids: list[int] = [netItem.item for netItem in ctx.items_received]
        items_to_check: dict[str, GrinchItemData] = {**GADGETS_TABLE} #, **SLEIGH_PARTS_TABLE
        heart_count = len(list(item_id for item_id in list_recv_itemids if item_id == 42570))
        heart_item_data = ALL_ITEMS_TABLE["Heart of Stone"]
        await self.update_and_validate_address(ctx, heart_item_data.update_ram_addr[0].ram_address, min(heart_count, 4), 1)

        # Setting Who Lake Mission Count back to 0 to prevent warping after completing 3 missions
        await self.update_and_validate_address(ctx,0x0100F0, 0, 4)

        for (item_name, item_data) in items_to_check.items():
            # If item is an event or already been received, ignore.
            if item_data.id is None or GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                continue

            # This assumes we don't have the item so we must set all the data to 0
            for addr_to_update in item_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                if is_binary:
                    current_bin_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                        addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                    current_bin_value &= ~(1 << addr_to_update.binary_bit_pos)
                    await self.update_and_validate_address(ctx, addr_to_update.ram_address, current_bin_value, 1)
                else:
                    await self.update_and_validate_address(ctx, addr_to_update.ram_address, 0, 1)

    # Removes the regional access until you actually received it from AP.
    async def constant_address_update(self, ctx: "BizHawkClientContext"):
        list_recv_itemids: list[int] = [netItem.item for netItem in ctx.items_received]
        items_to_check: dict[str, GrinchItemData] = {**KEYS_TABLE, **MISSION_ITEMS_TABLE}

        for (item_name, item_data) in items_to_check.items():
            # If item is an event or already been received, ignore.
            if item_data.id is None: # or GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                continue

            # This will either constantly update the item to ensure you still have it or take it away if you don't deserve it
            for addr_to_update in item_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False
                if is_binary:
                    current_bin_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
                        addr_to_update.ram_address, addr_to_update.bit_size, "MainRAM")]))[0], "little")
                    if GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                        current_bin_value |= (1 << addr_to_update.binary_bit_pos)
                    else:
                        current_bin_value &= ~(1 << addr_to_update.binary_bit_pos)
                    await self.update_and_validate_address(ctx, addr_to_update.ram_address, current_bin_value, 1)
                else:
                    if GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                        await self.update_and_validate_address(ctx, addr_to_update.ram_address, addr_to_update.value, 1)
                    else:
                        await self.update_and_validate_address(ctx, addr_to_update.ram_address, 0, 1)

    async def ingame_checker(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger

        ingame_map_id = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
            0x010000, 1, "MainRAM")]))[0], "little")

        #If not in game or at a menu, or loading the publisher logos
        if ingame_map_id <= 0x04 or ingame_map_id >= 0x35:
            return False

        #If grinch has changed maps
        if not ingame_map_id == self.last_map_location:
            # If the last "map" we were on was a menu or a publisher logo
            if self.last_map_location in MENU_MAP_IDS:
                # Reset our demo mode checker just in case the game is in demo mode.
                self.demo_mode_buffer = 0
                self.ingame_log = False
                return False

            # Update the previous map we were on to be the current map.
            self.last_map_location = ingame_map_id

        # Use this as a delayed check to make sure we are in game
        if not self.demo_mode_buffer == MAX_DEMO_MODE_CHECK:
            await asyncio.sleep(0.1)
            self.demo_mode_buffer += 1
            return False

        demo_mode = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(
            0x01008A, 1, "MainRAM")]))[0], "little")
        if demo_mode == 1:
            return False

        if not self.ingame_log:
            logger.info("You can now start sending locations from the Grinch!")
            self.ingame_log = True
        return True

    async def option_handler(self, ctx: "BizHawkClientContext"):
        if self.loc_unlimited_eggs:
            await bizhawk.write(ctx.bizhawk_ctx, [(EGG_COUNT_ADDR, MAX_EGGS.to_bytes(2,"little"), "MainRAM")])

    async def update_and_validate_address(self, ctx: "BizHawkClientContext", address_to_validate: int, expected_value: int, byte_size: int):
        await bizhawk.write(ctx.bizhawk_ctx, [(address_to_validate, expected_value.to_bytes(byte_size, "little"), "MainRAM")])
        current_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address_to_validate, byte_size, "MainRAM")]))[0], "little")
        if not current_value == expected_value:
            if address_to_validate == 0x010000 or address_to_validate == 0x08FB94 or address_to_validate == 0x010058: # TODO Temporairly skips teleportation addresses; to be changed later on.
                return
            raise Exception("Unable to update address as expected. Address: "+ str(address_to_validate)+"; Expected Value: "+str(expected_value))

    async def ring_link_output(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        while not ctx.exit_event or ctx.slot:

            try:
                current_egg_count = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(EGG_COUNT_ADDR, EGG_ADDR_BYTESIZE, "MainRAM")]))[0], "little")

                if (current_egg_count - self.previous_egg_count) != 0:
                    msg = {
                        "cmd": "Bounce",
                        "data": {
                            "time": time.time(),
                            "source": ctx.player_names[ctx.slot],
                            "amount": current_egg_count - self.previous_egg_count
                        },
                        "tags": ["RingLink"]
                    }
                    await ctx.send_msgs([msg])
                    self.previous_egg_count = current_egg_count
            except Exception as ex:
                logger.error("While monitoring grinch's egg count ingame, an error occured. Details:"+ str(ex))

    async def ring_link_input(self, egg_amount: int, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        current_egg_count = int.from_bytes(
            (await bizhawk.read(ctx.bizhawk_ctx, [(EGG_COUNT_ADDR, EGG_ADDR_BYTESIZE, "MainRAM")]))[0], "little")
        current_egg_count = min(current_egg_count + egg_amount, MAX_EGGS)
        await bizhawk.write(ctx.bizhawk_ctx, [(EGG_COUNT_ADDR,
            int(current_egg_count).to_bytes(EGG_ADDR_BYTESIZE, "little"), "MainRAM")])
        self.previous_egg_count = current_egg_count