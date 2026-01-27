import asyncio
import time
import sys
import traceback

from typing import TYPE_CHECKING, Any
from copy import deepcopy

from attr import attributes

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from worlds.pso import PSOWorld
from worlds.pso.locations import LOCATION_TABLE
from worlds.pso.patcher.pso_patcher import PSO_PLAYER_NAME_BYTE_LENGTH

from ..items import ITEM_TABLE, ITEM_ID_TO_NAME, PSOItemType

import dolphin_memory_engine

from ..helpers import SLOT_NAME_ADDR, read_string, write_short, read_short, write_bit, check_bit
from ..strings.client_strings import ConnectionStatus, get_death_message
from ..strings.item_names import Item

if TYPE_CHECKING:
    import kvui

# The memory address where the player's current health is stored
CURRENT_HEALTH_ADDRESS = 0x80DA65CC

# These addresses appear to be unused throughout the game
# Use it to track the index of the last item the game knows it has received for the player
LAST_RECEIVED_ITEM_ADDRESS = 0x80C5CBA0

BANK_EMPTY_SLOT: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'
BANK_FIRST_SLOT = 0x80FD95D0
BANK_LAST_SLOT = 0x80FDA878
BANK_ITEM_COUNT = 0x80FD95CB

ATTRIBUTE_BYTES = [b'\x01', b'\x02', b'\x03', b'\x04']

# The memory address to check to see if the player is currently in game
# Technically, this is the memory address for a Mothmant, which is loaded
# when the character 'sparks' in for the first time
IS_INGAME_ADDRESS = 0x805D4AA0

# The memory address for the Ruins Entrance after Vol Opt
RUINS_DOOR_ADDRESS = 0x805127FD

PILLAR_NAMES = {Item.FOREST_PILLAR, Item.CAVES_PILLAR, Item.MINES_PILLAR}

DEBUG_SLOT_OVERRIDE = True

class PSOCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Phantasy Star Online Episode I&II Plus client commands

    Handles commands specific to Phantasy Star Online Episode I&II Plus
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with specific context

        :param ctx: the Context object from CommonClient for PSO
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status
        """
        if isinstance(self.ctx, PSOContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class PSOContext(CommonContext):
    """
    The context object for Phantasy Star Online Episode I&II Plus from CommonClient

    Manages all interactions with the Dolphin emulator and the Archipelago server for PSO
    """
    command_processor = PSOCommandProcessor
    game = "Phantasy Star Online Episode I & II Plus"
    items_handling: int = 0b111

    def __init__(self, server_address: str | None, password: str | None) -> None:
        """
        Initialize the PSO context

        :param server_address: the address of the Archipelago server
        :param password: the password for authenticating to the Archipelago server
        """
        super().__init__(server_address, password)
        self.dolphin_sync_task: asyncio.Task[None] | None = None
        self.dolphin_status: str = ConnectionStatus.INITIAL
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False

        self.current_stage_name: str = ""

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Disconnect the client from the server and reset game state variables
        """
        self.auth = None
        # self.current_stage_name = None
        await super().disconnect(*args, **kwargs)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server

        :param password_requested: whether the server requires a password; defaults to `False`
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server

        :param cmd: the command received from the server
        :param args: the arguments for the received command
        """
        if cmd == "Connected":
            super().on_package(cmd, args)
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))


    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink events from the server

        :param data: the data associated with the DeathLink event
        """
        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for the PSO Archipelago client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago Phantasy Star Online Episode I&II Plus Client"
        return ui

async def check_death(ctx: PSOContext) -> None:
    """
    When DeathLink is on, check if the player is currently dead in-game
    then notify the server of the player's death

    :param ctx: the Context object from CommonClient for PSO
    """
    if ctx.slot is not None and check_ingame():
        current_health = read_short(CURRENT_HEALTH_ADDRESS)
        if current_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                # Choose a random death message to send to the server
                death_message = get_death_message()
                await ctx.send_death(ctx.player_names[ctx.slot] + death_message)
        else:
            ctx.has_send_death = False

def _give_death(ctx: PSOContext) -> None:
    """
    Trigger a player character death in-game by setting their current health to zero

    :param ctx: the Context object from CommonClient for PSO
    """
    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == ConnectionStatus.CONNECTED
        and check_ingame()
    ):
        ctx.has_send_death = True
        # TODO: Validate this actually works
        write_short(CURRENT_HEALTH_ADDRESS, 0)


def check_ingame() -> bool:
    """
    Returns True if the player is currently loaded into the game on a character
    """
    return read_short(IS_INGAME_ADDRESS) != 0

def check_in_bank() -> bool:
    """
    Returns True if the player is currently interacting with the bank, which can prevent receiving items
    """
    return


def check_ruins_door(ctx: PSOContext) -> None:
    """
    If the player has all 3 Pillars items, unlock the Ruins Entrance
    Otherwise, ensure it's locked
    """
    received_items = ctx.items_received

    # Create a list of all received items that are pillars
    found_pillars = [item for item in received_items if ITEM_ID_TO_NAME[item.item] in PILLAR_NAMES]
    # Technically, we may not have to relock / unlock every time this runs, but it's fairly cheap and
    # good insurance for the time being
    if len(found_pillars) == 3:
        write_bit(RUINS_DOOR_ADDRESS, 0, 1)
    else:
        write_bit(RUINS_DOOR_ADDRESS, 0, 0)

    return

def check_pillars(ctx: PSOContext) -> None:
    """
    When sending the checks from Pillar locations, check if all 3 pillar have been sent.
    If the player doesn't have all 3 pillar items received, re-lock the pillar door, as the game
    will unlock it automatically when the 3rd one is triggered.
    """
    checked_locations = ctx.locations_checked
    # TODO: Decide if we want to hard code the pillars
    pillar_location_codes = {20, 21, 22}
    if not pillar_location_codes.issubset(checked_locations):
        # All the pillars haven't been activated by the player; no need to check anything else
        return

    check_ruins_door(ctx)
    return


def write_to_bank(ctx: PSOContext, item_name: str) -> bool:
    """
    Write an item to the player's in-game bank

    :param ctx: the Context object from CommonClient for PSO
    :param item_name: the name of the item being given
    :return: whether the item was written successfully (as far as we know)
    """
    # bank_slot_bytes = dolphin_memory_engine.read_bytes(BANK_LAST_SLOT, 0x18)
    # logger.critical(f"Saber is {dolphin_memory_engine.read_bytes(0x80FD95D0, 18)}")
    # logger.critical(f"Or potentially is {dolphin_memory_engine.read_bytes(0x80FD95D0, 0x18)}")
    # logger.critical(f"Second empty slot is {dolphin_memory_engine.read_bytes(0x80FD95E8, 18)}")
    # logger.critical(f"Or potentially is {dolphin_memory_engine.read_bytes(0x80FD95E8, 0x18)}")

    # Check to make sure all the bytes are zero in the last slot, to ensure it's empty
    # There might be a better way to do this
    # for byte in bank_slot_bytes:
    #     if byte not in (0, 255):
    #         logger.error(f"Byte was {byte}")
    # if bank_slot_bytes != BANK_EMPTY_SLOT:
    #     # TODO: Have another option for handling the case where the bank is full
    #     logger.error(f"Attempted to write {item_name} to bank, but the bank is full. Current bytes: {bank_slot_bytes}")
    #     return True

    SABER_BYTES = b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01'
    LAVIS_BYTES = b'\x00\x01\x00\x00\x00\x00\x01\x14\x03\x28\x05\x46\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01'
    #               item    tier    tekker  Attr    ""      ""
    #                   type    grind    ???     Amount ""      ""
    #3E 4C CC CD

    pso_item = ITEM_TABLE[item_name]

    # Make an empty container to put our bytes into
    item_bytes = b''

    if pso_item.type == PSOItemType.WEAPON:
        # Item slots in the bank are 18 bytes long, and 24 bytes away from the next item
        # We find how much padding we need to add to push the item into position
        # for _ in range(len(item_bytes), 18):
        #     item_bytes.append(0)

        # dolphin_memory_engine.write_bytes(BANK_LAST_SLOT, item_bytes)
        # dolphin_memory_engine.write_bytes(0x80FD95D0, item_bytes)
        # Retrieve the current number of items in the player's bank
        bank_current_count = dolphin_memory_engine.read_byte(BANK_ITEM_COUNT)

        if bank_current_count >= 200:
            logger.error(f"Attempted to write {item_name} to the bank, but the bank is full.")
            return False

        # TODO: Extract this to a Make Bytes function
        # Weapons start with \x00 so we add that first
        item_bytes += b'\x00'
        item_bytes += pso_item.ram_data.byte_data
        item_bytes += int.to_bytes(pso_item.max_grind, byteorder='big')
        # No Tekker or present for now
        item_bytes += b'\x00\x00'
        logger.info(f"Bytes: {item_bytes}")
        # Pick 2 random attributes and then Hit and set them to 90%, because why not
        # TODO: Figure out how to get random items in the client
        # attributes = ctx. .random.choices(ATTRIBUTE_BYTES, k=2)
        attributes = [int.to_bytes(int.from_bytes(pso_item.ram_data.byte_data[1:], byteorder='big') + 1, byteorder='big'),
                      int.to_bytes(int.from_bytes(pso_item.ram_data.byte_data[1:], byteorder='big') + 2, byteorder='big')]
        if attributes[1:] == b'\x05':
            attributes.insert(0, b'\x01')
        else:
            attributes.append(b'\x05')
        for attribute in attributes:
            item_bytes += attribute
            item_bytes += int.to_bytes(70, byteorder='big')
            logger.info(f"Bytes: {item_bytes}")

        # Throw the rest of the bytes on that we need
        item_bytes += b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01'

        # Every bank is 24 bytes (0x18) apart
        # Get the relevant memory space based on the number of items we have to skip over
        next_open_slot = BANK_FIRST_SLOT + (0x18 * bank_current_count)
        dolphin_memory_engine.write_bytes(next_open_slot, item_bytes)

        # Increment the bank counter
        dolphin_memory_engine.write_byte(BANK_ITEM_COUNT, bank_current_count + 1 )

        logger.info(f"Wrote {item_name} to bank")
        logger.info(f"Bytes: {item_bytes}")
        return True

    # If we somehow don't handle all our cases properly, we should know that
    logger.error(f"Attempted to write {item_name} to the bank, but something unexpected occurred.")
    return False


def _give_item(ctx: PSOContext, item_name: str) -> bool:
    """
    Give an item to the player in-game

    :param ctx: the Context object from CommonClient for PSO
    :param item_name: the name of the item being given
    :return: whether the item was successfully given
    """
    # TODO: Determine if this can get stuck
    if not check_ingame():
        return False

    item = ITEM_TABLE[item_name]
    match item.type:
        case PSOItemType.AREA:
            if not item.ram_data.bit_position:
                # All of our AREAs should have RAM data in the current implementation
                logger.error(f"Item {item_name} is classified as an AREA but has no ram data")
                return False
            write_bit(item.ram_data.ram_addr, item.ram_data.bit_position, 1)
            return True

        case PSOItemType.SWITCH:
            if not item.ram_data.bit_position:
                # All of our SWITCHs should have RAM data in the current implementation
                logger.error(f"Item {item_name} is classified as an SWITCH but has no ram data")
                return False

            if item_name in PILLAR_NAMES:
                check_pillars(ctx)
            else:
                logger.warning(f"Non-Pillar SWITCH {item_name} found – this may have unexpected behavior")
                write_bit(item.ram_data.ram_addr, item.ram_data.bit_position, 1)
            return True

        case PSOItemType.EVENT:
            if item_name == Item.VICTORY:
                # To my knowledge, we don't have to do anything here
                logger.info("Victory item has been sent")
            else:
                logger.error(f"EVENT item {item_name} is not specifically handled – this may have unexpected behavior")
            return True

        case PSOItemType.WEAPON:
            return write_to_bank(ctx, item_name)

        case _:
            logger.error(f"Unhandled {item.type} item not added to game: {item_name}")
    return False


async def give_items(ctx: PSOContext) -> None:
    """
    Give the player all outstanding items they have yet to receive

    :param ctx: the Context object from CommonClient for PSO
    """
    if not check_ingame():
        return

    # Read the index of the last item the game knows we received
    # Use this value to compare with w
    next_item_idx = read_short(LAST_RECEIVED_ITEM_ADDRESS) + 1

    # Fetch the list of received items
    received_items = ctx.items_received
    if len(received_items) <= next_item_idx:
        # No new items
        return

    # Iterate through the new items and give them to the player
    for idx, item_to_add in enumerate(received_items[next_item_idx:]):
        # Lookup the item from the Context and attempt to give it to the player
        while not _give_item(ctx, ITEM_ID_TO_NAME[item_to_add.item]):
            await asyncio.sleep(0.01)

        # Update the last received item index to the item that was just sent
        write_short(LAST_RECEIVED_ITEM_ADDRESS, next_item_idx)


async def check_locations(ctx: PSOContext) -> None:
    # Check to make sure the player hasn't beaten the game
    win_condition_data = LOCATION_TABLE["Defeat Dark Falz"].ram_data
    if check_bit(win_condition_data.ram_addr, win_condition_data.bit_position):
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True

    # We make a deepcopy to avoid unexpected mutations of missing_locations during our checks
    local_missing_locations = deepcopy(ctx.missing_locations)
    for missing_location in local_missing_locations:
        location_name = ctx.location_names.lookup_in_game(missing_location)
        location_data = LOCATION_TABLE[location_name].ram_data
        if check_bit(location_data.ram_addr, location_data.bit_position):
            ctx.locations_checked.add(missing_location)
    await ctx.check_locations(ctx.locations_checked)

    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def dolphin_sync_task(ctx: PSOContext) -> None:
    """
    The task loop for managing the connection to Dolphin

    While connected, we can read the emulator's memory for any relevant changes made by the player in the game

    :param ctx: the Context object from CommonClient for PSO
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == ConnectionStatus.CONNECTED:
                if not check_ingame():
                    sleep_time = 0.1
                    continue
                if ctx.slot:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                else:
                    # This 2 line section needs to be BEFORE the No Slot Name unhooking.
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, PSO_PLAYER_NAME_BYTE_LENGTH)

                        # If we need to override the slot name for testing, match your player's slot name to this
                        # DO NOT USE THIS IN A REAL GAME
                        if DEBUG_SLOT_OVERRIDE:
                            ctx.auth = "Rubix"

                        # This triggers if ctx auth is not correct.
                        if not ctx.auth:
                            ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                            ctx.auth = None
                            ctx.dolphin_status = ConnectionStatus.NO_SLOT_NAME
                            logger.info(ctx.dolphin_status)
                            dolphin_memory_engine.un_hook()
                            await asyncio.sleep(5)
                            continue

                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                sleep_time = 0.1
            else:
                if ctx.dolphin_status == ConnectionStatus.CONNECTED:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = ConnectionStatus.LOST
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    game_id = read_string(0x80000000, 6)

                    if game_id in ["GP0E8P"]:
                        logger.info(ConnectionStatus.REFUSED_GAME)
                        ctx.dolphin_status = ConnectionStatus.REFUSED_GAME
                        dolphin_memory_engine.un_hook()
                        sleep_time = 5
                        continue

                    logger.info(ConnectionStatus.CONNECTED)
                    ctx.dolphin_status = ConnectionStatus.CONNECTED
                    ctx.locations_checked = set()

                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = ConnectionStatus.LOST
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = ConnectionStatus.LOST
            await ctx.disconnect()
            sleep_time = 5
            continue


def async_main(connect: str | None = None, password: str | None = None) -> None:
    """
    Run the main async loop for the PSO client

    :param connect: the address of the Archipelago server
    :param password: the password for authenticating to the Archipelago server
    """

    async def _main(connect: str | None, password: str | None) -> None:
        ctx = PSOContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="PSODolphinSync")

        await ctx.exit_event.wait()
        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        # TODO: Determine if we need these (not in MMXCM)
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()

def sync_main(*launch_args: str):
    Utils.init_logging("Phantasy Star Online Episode I&II Plus Client")

    parser = get_base_parser()
    parser.add_argument('appso_file', default="", type=str, nargs="?", help='Path to an APPSO file')
    args = parser.parse_args(launch_args)

    if args.appso_file:
        from worlds.pso.patcher.pso_patcher import PSOPatcher
        pso_patch = PSOPatcher(args.appso_file)
        pso_patch.create_patch()

    async_main(args.connect, args.password)

if __name__ == "__main__":
    sync_main(*sys.argv[1:])


