import asyncio
import time
import traceback
from typing import Any

import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import LOCATION_TABLE, TWWLocation, TWWLocationType

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for TWW. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure TWW is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x803C4C0A

# These addresses are used for the Moblin's Letter check.
LETTER_BASE_ADDR = 0x803C4C8E
LETTER_OWND_ADDR = 0x803C4C98

# These addresses are used to check flags for locations.
CHARTS_BITFLD_ADDR = 0x803C4CFC
CHESTS_BITFLD_ADDR = 0x803C5380
SWITCHES_BITFLD_ADDR = 0x803C5384
PICKUPS_BITFLD_ADDR = 0x803C5394
SEA_ALT_BITFLD_ADDR = 0x803C4FAC

# The expected index for the next item that should be received. Uses event bits 0x60 and 0x61
EXPECTED_INDEX_ADDR = 0x803C528C

# These bytes contain the bits whether the player has received the reward for finding a particular Tingle statue.
TINGLE_STATUE_1_ADDR = 0x803C523E  # 0x40 is the bit for Dragon Tingle statue
TINGLE_STATUE_2_ADDR = 0x803C5249  # 0x0F are the bits for the remaining Tingle statues

# These addresses contain the current high score for the Bird-Man Contest.
# `FCP_SCORE_LO_ADDR` is are the lower eight bits of the score, `FCP_SCORE_HI_ADDR` are the higher eight bits
FCP_SCORE_LO_ADDR = 0x803C52D3
FCP_SCORE_HI_ADDR = 0x803C52D4

# This address contains the current stage ID.
CURR_STAGE_ID_ADDR = 0x803C53A4

# This address is used to check the stage name to verify the player is in-game before sending items.
CURR_STAGE_NAME_ADDR = 0x803C9D3C

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
GIVE_ITEM_ARRAY_ADDR = 0x803FE868

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
SLOT_NAME_ADDR = 0x803FE88C


class TWWCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, TWWContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class TWWContext(CommonContext):
    command_processor = TWWCommandProcessor
    game = "The Wind Waker"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.last_rcvd_index = -1
        self.has_send_death = False

        self.len_give_item_array = 0x10

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_rcvd_index = -1
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        if cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])

    def on_deathlink(self, data: dict[str, Any]):
        super().on_deathlink(data)
        _give_death(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWWContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information")
            return
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class TWWManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago The Wind Waker Client"

        self.ui = TWWManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def read_short(console_address: int):
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return dolphin_memory_engine.read_bytes(console_address, strlen).decode().strip("\0")


def _give_death(ctx: TWWContext):
    if (
        ctx.slot
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)


def _give_item(ctx: TWWContext, item_name: str) -> bool:
    if not check_ingame() or dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False

    item_id = ITEM_TABLE[item_name].item_id

    # Loop through the give item array, placing the item in an empty slot
    for idx in range(ctx.len_give_item_array):
        slot = dolphin_memory_engine.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
        if slot == 0xFF:
            dolphin_memory_engine.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
            return True

    # Unable to place the item in the array, so return `False`
    return False


async def give_items(ctx: TWWContext):
    if check_ingame() and dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) != 0xFF:
        # Read the expected index of the player, which is the index of the latest item they've received
        expected_idx = read_short(EXPECTED_INDEX_ADDR)

        # Loop through items to give
        for item, idx in ctx.items_received_2:
            # If the index of the item is greater than the expected index of the player, give the player the item
            if expected_idx <= idx:
                # Attempt to give the item and increment the expected index
                while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                    await asyncio.sleep(0.01)

                # Increment the expected index
                write_short(EXPECTED_INDEX_ADDR, idx + 1)


async def check_locations(ctx: TWWContext):
    # We check which locations are currently checked on the current stage
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    # Read in various bitfields for the locations in the current stage
    charts_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(CHARTS_BITFLD_ADDR, 8))
    sea_alt_bitfield = dolphin_memory_engine.read_word(SEA_ALT_BITFLD_ADDR)
    chests_bitfield = dolphin_memory_engine.read_word(CHESTS_BITFLD_ADDR)
    switches_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(SWITCHES_BITFLD_ADDR, 10))
    pickups_bitfield = dolphin_memory_engine.read_word(PICKUPS_BITFLD_ADDR)

    for location, data in LOCATION_TABLE.items():
        checked = False

        # Special-case checks
        if data.type == TWWLocationType.SPECL:
            # The flag for "Windfall Island - Maggie - Delivery Reward" is still unknown.
            # However, as a temporary workaround, we can just check if the player had Moblin's letter at some point,
            # but it's no longer in their Delivery Bag
            if location == "Windfall Island - Maggie - Delivery Reward":
                was_moblins_owned = (dolphin_memory_engine.read_word(LETTER_OWND_ADDR) >> 15) & 1
                dbag_contents = [dolphin_memory_engine.read_byte(LETTER_BASE_ADDR + offset) for offset in range(8)]
                checked = was_moblins_owned and 0x9B not in dbag_contents

            # For Letter from Baito's Mother, we need to check two bytes
            # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
            if location == "Mailbox - Letter from Baito's Mother":
                checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

            # For Letter from Grandma, we need to check two bytes
            # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
            if location == "Mailbox - Letter from Grandma":
                checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

            # For the Ankle's reward, we check if the bits for turning all five statues are set
            # For some reason, the bit for the Dragon Tingle Statue is located in a separate location than the rest
            if location == "Tingle Island - Ankle - Reward for All Tingle Statues":
                dragon_tingle_statue_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
                other_tingle_statues_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
                checked = dragon_tingle_statue_rewarded and other_tingle_statues_rewarded

            # For the Bird-Man Contest, we check if the high score is greater than 250 yards
            if location == "Flight Control Platform - Bird-Man Contest - First Prize":
                high_score = dolphin_memory_engine.read_byte(FCP_SCORE_LO_ADDR) + (
                    dolphin_memory_engine.read_byte(FCP_SCORE_HI_ADDR) << 8
                )
                checked = high_score > 250

        # Regular checks
        elif data.stage_id == curr_stage_id:
            match data.type:
                case TWWLocationType.CHART:
                    checked = (charts_bitfield >> data.bit) & 1
                case TWWLocationType.BOCTO:
                    checked = (read_short(data.address) >> data.bit) & 1
                case TWWLocationType.CHEST:
                    checked = (chests_bitfield >> data.bit) & 1
                case TWWLocationType.SWTCH:
                    checked = (switches_bitfield >> data.bit) & 1
                case TWWLocationType.PCKUP:
                    checked = (pickups_bitfield >> data.bit) & 1
                case TWWLocationType.EVENT:
                    checked = (dolphin_memory_engine.read_byte(data.address) >> data.bit) & 1

        # Sea (Alt) chests
        elif curr_stage_id == 0x0 and data.stage_id == 0x1:
            assert data.type == TWWLocationType.CHEST
            checked = (sea_alt_bitfield >> data.bit) & 1

        if checked:
            location_id = TWWLocation.get_apid(data.code)
            if location_id:
                ctx.locations_checked.add(location_id)
            else:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

    # Send the list of newly-checked locations to the server
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def check_alive():
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWContext):
    if check_ingame():
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame():
    return read_string(CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


async def dolphin_sync_task(ctx: TWWContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    # Reset give item array while not in game
                    dolphin_memory_engine.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) != b"GZLE99":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect=None, password=None):
    Utils.init_logging("The Wind Waker Client")

    async def _main(connect, password):
        ctx = TWWContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
