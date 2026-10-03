import asyncio
from collections import deque
from copy import deepcopy
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

from MultiServer import mark_raw
import dolphin_memory_engine  # type: ignore

from .ClientItemChecker import check_dungeon_item_count, check_item_count  # type: ignore

from .ClientUtils import (
    NODE_TO_STRING,
    STAGE_TO_NAME,
    CLIENT_VERSION,
    KEY_TO_OFFSET,
    base_server_data_connection,
    server_data,
)
from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME, TPItem
from .Locations import LOCATION_TABLE, TPLocation, TPLocationType
import Utils
from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    logger,
    server_loop,
    gui_enabled,
    get_base_parser,
)

from NetUtils import NetworkItem, ClientStatus

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = "Dolphin failed to connect. Please load a ROM for Twilight Princess. Trying again in 5 seconds..."
CONNECTION_REFUSED_SAVE_STATUS = "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure Twilight Princess is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."
RANDO_NOT_LOADED_MSG = "Randomizer is not loaded, Client will not work until fixed"
WRONG_SEED_LOADED_MSG = "Invalid Seed; Either the wrong seed was loaded, or you are not in game yet; Seed to use: "
CONNECT_IN_GAME_MSG = "Please load a save file and gain control of link before attempting to connect"

VALIDATION_TIME = 10

# CURR_HEALTH_ADDR = 0x804061C2
# CURR_NODE_ADDR = 0x80406B38
# SLOT_NAME_ADDR = 0x80406374
# ITEM_WRITE_ADDR = 0x80406AB0
# NODES_START_ADDR = 0x804063B0
# ACTIVE_NODE_ADDR = 0x80406B18
LINK_POINTER_ADDR = 0x8040BF6C
M_EVENT_STATUS_ADDR = 0x8040B16D

DEBUGGING = False


def set_address(
    regionCode=None,
    curr_health_addr=None,
    curr_node_addr=None,
    slot_name_addr=None,
    item_write_addr=None,
    expected_index_addr=None,
    nodes_start_addr=None,
    active_node_addr=None,
    link_pointer_addr=None,
    m_event_status_addr=None,
):
    global STRING_ENCODING
    if regionCode is None:
        regionCode = read_byte(0x80000003)
    saveFileAddr = 0x804061C0  # US by default
    STRING_ENCODING = "ascii"
    match (regionCode):
        case 0x50:  # ASCII for 'P', which is EU
            saveFileAddr = 0x80408160
            STRING_ENCODING = "ascii"
        case 0x4A:  # ASCII for 'J', which is JP
            saveFileAddr = 0x80400300
            STRING_ENCODING = "shift-jis"

    global CURR_HEALTH_ADDR, CURR_NODE_ADDR, SLOT_NAME_ADDR, ITEM_WRITE_ADDR, EXPECTED_INDEX_ADDR, NODES_START_ADDR, ACTIVE_NODE_ADDR, SAVE_FILE_ADDR, LINK_POINTER_ADDR, M_EVENT_STATUS_ADDR

    CURR_HEALTH_ADDR = (
        curr_health_addr if curr_health_addr is not None else saveFileAddr + 0x2
    )
    CURR_NODE_ADDR = (
        curr_node_addr if curr_node_addr is not None else saveFileAddr + 0x978
    )
    SLOT_NAME_ADDR = (
        slot_name_addr if slot_name_addr is not None else saveFileAddr + 0x1B4
    )
    ITEM_WRITE_ADDR = (
        item_write_addr if item_write_addr is not None else saveFileAddr + 0x8F0
    )
    EXPECTED_INDEX_ADDR = (
        expected_index_addr if expected_index_addr is not None else saveFileAddr + 0x8FC
    )
    NODES_START_ADDR = (
        nodes_start_addr if nodes_start_addr is not None else saveFileAddr + 0x1F0
    )
    ACTIVE_NODE_ADDR = (
        active_node_addr if active_node_addr is not None else saveFileAddr + 0x958
    )
    SAVE_FILE_ADDR = saveFileAddr
    LINK_POINTER_ADDR = (
        link_pointer_addr if link_pointer_addr is not None else saveFileAddr + 0x5DAC
    )
    M_EVENT_STATUS_ADDR = (
        m_event_status_addr
        if m_event_status_addr is not None
        else saveFileAddr + 0x4FAD
    )


# ...existing code...


class TPCommandProcessor(ClientCommandProcessor):
    """
    Command processor for the Twilight Princess client.

    This class handles all commands that are specific to the Twilight Princess client.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """Display the current Dolphin emulator connection status."""
        if isinstance(self.ctx, TPContext):
            assert isinstance(self.ctx.dolphin_status, str)

            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_debug(self) -> None:
        """Toggles Debug messages from showing"""
        global DEBUGGING
        DEBUGGING = not DEBUGGING

    @mark_raw
    def _cmd_name(self, name: str = "") -> None:
        """Change the name of the current save file (i.e. /name Player1 )"""

        if not isinstance(self.ctx, TPContext):
            return

        assert isinstance(name, str)

        if self.ctx.dolphin_status != CONNECTION_CONNECTED_STATUS:
            logger.info("Client must be connected to dolphin first")
            return

        if self.ctx.current_node == 0xFF:
            logger.info("Must be in game to change name")
            return

        if len(name) > 16:
            name = name[:16]

        # Pad the name with 0x00 characters to make it 16 characters long
        padded_name = name.ljust(16, "\x00")

        logger.info(f"Writing name {padded_name}")
        write_string(SLOT_NAME_ADDR, padded_name)
        return


class TPContext(CommonContext):
    """
    The context for Twilight Princess client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Twilight Princess.
    """

    command_processor = TPCommandProcessor
    game: str = "Twilight Princess"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the context with the provided server address and password.

        :param server_address: The address of the Archipelago server.
        :param password: The password for the server.
        """
        super().__init__(server_address, password)
        self.item_queue: deque[tuple[NetworkItem, int]] = deque()
        self.insurance_queue: deque[tuple[str, int]] = deque()
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_dolphin = False
        self.last_received_index = -1
        self.has_send_death = False
        self.current_node = 0xFF
        self.server_data_copy: dict[str, str | bool] = {}
        self.server_data = deepcopy(server_data)
        self.server_data_built = False
        self.server_data_sent = False
        self.validation_timer = time.time()
        # Event is used for pause as it better represents how I want to think about it
        self.validation_pause = asyncio.Event()

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect from the server and stop the Dolphin synchronization task.

        :param allow_autoreconnect: Whether to allow the client to automatically reconnect to the server.
        """
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        assert isinstance(password_requested, bool)

        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_dolphin:
                return
            self.awaiting_dolphin = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        self.connection_tried = True
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.items_received = []
            self.item_queue = deque()
            self.insurance_queue = deque()
            self.validation_timer = time.time()
            self.validation_pause.set()
            try:
                self.last_received_index = read_short(EXPECTED_INDEX_ADDR)
            except Exception:
                self.last_received_index = -1

            if args["slot_data"] is not None and "DeathLink" in args["slot_data"]:
                assert isinstance(
                    args["slot_data"]["DeathLink"], int
                ), f"{args["slot_data"]["DeathLink"]=}"
                Utils.async_start(
                    self.update_death_link(bool(args["slot_data"]["DeathLink"]))
                )
                if DEBUGGING:
                    logger.info(
                        f"Debug: Seting deathlink to {bool(args["slot_data"]["DeathLink"])}"
                    )
            if args["slot_data"] is not None and (
                not args["slot_data"]["World Version"]
                or args["slot_data"]["World Version"].removeprefix("v") != CLIENT_VERSION.removeprefix("v")
            ):
                logger.info(
                    f"""Error: Client version does not match version of generated seed.
                            Things may not work as intended,
                            Seed version:{args["slot_data"]["World Version"]} client version:{CLIENT_VERSION}"""
                )
            else:
                logger.info(f"""Connected Using Seed & client version:{CLIENT_VERSION}""")
            self.server_data_built = False
            self.server_data = deepcopy(server_data)

        elif cmd == "ReceivedItems":
            start_index = args["index"]

            if start_index == 0:
                self.items_received = []
            elif start_index != len(self.items_received):
                sync_msg = [{"cmd": "Sync"}]
                if self.locations_checked:
                    sync_msg.append(
                        {"cmd": "LocationChecks", "locations": list(self.locations_checked)}
                    )
                Utils.async_start(self.send_msgs(sync_msg))
                return

            if start_index == len(self.items_received):
                for item in args["items"]:
                    assert isinstance(
                        item, NetworkItem
                    ), f"[Twilight Princess Client] Received an item that is not a NetworkItem: {item=}"

                    item_index = len(self.items_received)
                    self.items_received.append(item)

                    # EXPECTED_INDEX_ADDR stores the number of network items
                    # already applied to the game save.
                    item_name = LOOKUP_ID_TO_NAME.get(item.item)

                    if item.player != self.slot or item.location == -1:
                        try:
                            expected_index = read_short(EXPECTED_INDEX_ADDR)
                        except Exception:
                            expected_index = -1

                        if item_index >= expected_index:
                            self.item_queue.append((item, item_index))

                    elif item_name in KEY_TO_OFFSET:
                        # Local key/counter items are stored directly in the save file.
                        key_offset = SAVE_FILE_ADDR + 0x901 + KEY_TO_OFFSET[item_name]
                        key_count = dolphin_memory_engine.read_byte(key_offset)
                        dolphin_memory_engine.write_byte(key_offset, key_count + 1)

                    self.validation_pause.set()

                self.last_received_index = len(self.items_received)

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        if DEBUGGING:
            logger.info("Debug: on deathlink trigger")

        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for Twilight Princess client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago Twilight Princess Client"
        return ui


def read_byte(console_address: int) -> int:
    """
    Read a byte from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    result = dolphin_memory_engine.read_byte(console_address)
    assert isinstance(result, int)
    return result


def read_short(console_address: int) -> int:
    """
    Read a short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    result = int.from_bytes(
        dolphin_memory_engine.read_bytes(console_address, 2), byteorder="big"
    )
    assert isinstance(result, int)
    return result


def read_pointer(console_address: int) -> int:
    """
    Read a short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    result = int.from_bytes(
        dolphin_memory_engine.read_bytes(console_address, 4), byteorder="big"
    )
    assert isinstance(result, int)
    return result


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to read from.
    :param strlen: Length of the string to read.
    :return: The string read from memory.
    """
    assert isinstance(console_address, int)
    assert isinstance(strlen, int)
    result = (
        dolphin_memory_engine.read_bytes(console_address, strlen)
        .split(b"\0", 1)[0]
        .decode(STRING_ENCODING)
    )
    assert isinstance(result, str)
    return result


def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(value, int)

    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(1, byteorder="big")
    )


def write_short(console_address: int, value: int) -> None:
    """
    Write a short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(value, int)

    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(2, byteorder="big")
    )


def write_string(console_address: int, string: str) -> None:
    """
    Write a string to Dolphin memory.

    :param console_address: Address to write to.
    :param string: String to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(string, str)

    if len(string) > 16:
        raise ValueError("String length must be 16 characters or less.")

    dolphin_memory_engine.write_bytes(
        console_address, string.encode(STRING_ENCODING) + b"\0"
    )




def _give_death(ctx: TPContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: Twilight Princess client context.
    """
    if DEBUGGING:
        logger.info("Debug: Trying to kill player")

    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and _check_status()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)
        if DEBUGGING:
            logger.info("Debug: Health set to 0")


async def _give_items(ctx: TPContext, items: list[str]) -> bool:
    """
    Give a batch of items to the player in-game.
    items must contain at max 8 items as that is the size of the queue

    :param ctx: Twilight Princess client context.
    :param items: Name of the items to give.
    :return: Whether the items were successfully given.
    """

    assert isinstance(items, list), f"{items=}"
    assert len(items) > 0, f"{items=}"
    assert (
        len(items) <= 8
    ), f"{len(items)}"  # Could put to 7 to allow for extra buffer incase

    if not await check_ingame(ctx):
        return False
    if not _check_status():
        return False

    for item_name in items:
        assert item_name in ITEM_TABLE, f"{item_name=} not in item table "
        assert isinstance(
            ITEM_TABLE[item_name].item_id, int
        ), f"{item_name=} has no item_id"

    ctx.validation_timer = time.time()

    # Only add items to the queue if it is empty
    for i in range(0, 8):
        item_stack_addr = ITEM_WRITE_ADDR + i
        if read_byte(item_stack_addr) != 0x00:
            return False

    # Now its empty
    # Add items starting at 0x8F0 so that it is given first
    for i in range(0, len(items)):
        item_stack_addr = ITEM_WRITE_ADDR + i
        # Just incase something happens
        assert (
            read_byte(item_stack_addr) == 0x00
        ), f"Tried to add to the queue but it was not empty"

        if DEBUGGING:
            logger.info(f"Debug: Giving {items[i]} into queue")

        if items[i] == "Victory":
            if not ctx.finished_game:
                logger.info("Player got victory but the game is not complete in client")
            continue

        write_byte(item_stack_addr, ITEM_TABLE[items[i]].item_id)
    # Now the queue is full and all items are added
    return True


async def give_items(ctx: TPContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Twilight Princess client context.
    """
    if (
        await check_ingame(ctx)
        and dolphin_memory_engine.read_byte(CURR_NODE_ADDR) != 0xFF
    ):

        # Items will be filtered from client item_queue to here
        item_give_queue: list[str] = []

        # Empty the Queue
        while len(ctx.item_queue) > 0:

            item, item_index = ctx.item_queue.pop()
            item_name = LOOKUP_ID_TO_NAME[item.item]
            assert (
                item_name in ITEM_TABLE
            ), f"[Twilight Princess Client] tried to give {item_name=} but it is not in the item table"

            item_data = ITEM_TABLE[item_name]

            # Basic items we don't care if are given multiple times
            if item_data.type in [
                "Rupee",
                "Ammo",
                "Trap",
                "Small key",
                "Big Key",
                "Book",
            ]:
                item_give_queue.append(item_name)

            # Items that we need to check the count of before giving to link
            elif item_data.type in [
                "Item",
                "Bottle",
                "Bug",
                "Poe",
            ]:
                # actual_item_count = check_item_count(item_name, SAVE_FILE_ADDR)

                # expected_item_count = 0
                # for item in ctx.items_received:
                #     if item.item == item_data.code:
                #         expected_item_count += 1

                # # Note: items given directly through memory will cause an item wait where an item is not given
                # # # If this occurs they did it to themselfs

                # # Usually this will be a differance of 1
                # if expected_item_count > actual_item_count:
                #     item_give_queue.append(item_name)
                # else:
                #     if DEBUGGING:
                #         logger.info(
                #             f"Debug: Tried to give {item_name=} but player already has {expected_item_count=}, {actual_item_count=}"
                #         )
                continue

            elif item_data.type in [
                "Compass",
                "Map",
            ]:
                # if (
                #     check_dungeon_item_count(
                #         item_name, SAVE_FILE_ADDR, ctx.current_node
                #     )
                #     == 0
                # ):
                #     item_give_queue.append(item_name)
                # else:
                #     if DEBUGGING:
                #         logger.info(
                #             f"Debug: Tried to give {item_name=} but player already has one"
                #         )
                continue

            elif item_data.type in [
                "Heart",
            ]:
                # actual_heart_pieace_count = read_short(SAVE_FILE_ADDR)

                # heart_piece_count = 0
                # heart_container_count = 0
                # for item in ctx.items_received:
                #     if item.item == TPItem.get_apid(ITEM_TABLE["Piece of Heart"].code):
                #         heart_piece_count += 1
                #     if item.item == TPItem.get_apid(ITEM_TABLE["Heart Container"].code):
                #         heart_container_count += 1

                # if (
                #     actual_heart_pieace_count
                #     < (heart_container_count * 5) + heart_piece_count + 15
                # ):
                #     item_give_queue.append(item_name)
                # else:
                #     if DEBUGGING:
                #         logger.info(
                #             f"Debug: Tried to give {item_name=} but player already has {actual_heart_pieace_count=}, {heart_container_count=},{heart_piece_count=}"
                #         )
                continue

            elif item_data.type == "Event":
                assert (
                    False
                ), f"[Twilight Princess Client] got an event item. {item_name=} I didn't think that could happen, as it has no id"
            else:
                assert (
                    False
                ), f"[Twilight Princess Client] {item_name=} has an invalid type {item_data.type}"

            # Only try to give a full queue or whatever is there
            if len(item_give_queue) == 8 or (
                item_index >= ctx.last_received_index - 1 and len(item_give_queue) > 0
            ):
                while not await _give_items(ctx, item_give_queue):
                    await asyncio.sleep(0.5)
                write_short(EXPECTED_INDEX_ADDR, item_index + 1)
                item_give_queue = []
        assert (
            len(item_give_queue) == 0
        ), f"[Twilight Princess Client] item give queue is not empty at the end {item_give_queue=}\n{item_index=} - {ctx.last_received_index=}"

        # Keep the save's network-item index synchronized even when some
        # received items are local or intentionally skipped by the client.
        if await check_ingame(ctx):
            expected_index = read_short(EXPECTED_INDEX_ADDR)
            if expected_index < ctx.last_received_index:
                write_short(EXPECTED_INDEX_ADDR, ctx.last_received_index)

        # Now validation should be good to occur
        ctx.validation_pause.clear()
        return
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #


async def validate_item(ctx: TPContext) -> None:

    # If paused or the timer has not passed then skip validation
    if ctx.validation_pause.is_set() or (
        time.time() < ctx.validation_timer + VALIDATION_TIME
    ):
        return

    # First check if item queue is empty as we don't want to double give
    for i in range(0, 8):
        item_stack_addr = ITEM_WRITE_ADDR + i
        if read_byte(item_stack_addr) != 0x00:
            return

    for item_name, item_data in ITEM_TABLE.items():

        if item_data.type in [
            "Rupee",
            "Ammo",
            "Trap",
            "Event",
        ]:
            # Skip all non insurable items
            continue

        elif item_data.type in [
            "Book",
            "Small key",
            "Big Key",
            "Item",
            "Bottle",
            "Bug",
            "Poe",
        ]:
            if (
                item_data.type == "Bottle"
            ):  # Bottle is only non progressive that checks together
                if item_name != "Empty Bottle (Fishing Hole)":
                    continue

            actual_item_count = check_item_count(item_name, SAVE_FILE_ADDR)

            expected_item_count = 0
            item_id = TPItem.get_apid(item_data.code)

            for item in ctx.items_received:
                if item.item == item_id:
                    expected_item_count += 1

            if item_name not in KEY_TO_OFFSET:
                expected_item_count += ctx.start_inventory.count(item_id)

            expected_item_count = min(expected_item_count, item_data.quantity)

            difference = expected_item_count - actual_item_count
            if difference > 0:
                if DEBUGGING:
                    logger.info(
                        f"Debug: Insurance caught that you missed {difference}x{item_name} adding it to the queue"
                    )
                ctx.insurance_queue.append([item_name, difference])

        elif item_data.type in [
            "Compass",
            "Map",
        ]:
            if (
                check_dungeon_item_count(item_name, NODES_START_ADDR, ctx.current_node)
                == 0
            ):
                ctx.insurance_queue.append([item_name, 1])

        elif item_data.type in [
            "Heart",
        ]:
            # Only try to give heart pieces and not containers
            if item_name != "Piece of Heart":
                continue

            actual_heart_pieace_count = read_short(SAVE_FILE_ADDR)
            heart_piece_count = 0
            heart_container_count = 0
            for item in ctx.items_received:
                if item.item == TPItem.get_apid(ITEM_TABLE["Piece of Heart"].code):
                    heart_piece_count += 1
                if item.item == TPItem.get_apid(ITEM_TABLE["Heart Container"].code):
                    heart_container_count += 1

            heart_difference = (
                (heart_container_count * 5) + heart_piece_count + 15
            ) - actual_heart_pieace_count

            if heart_difference > 0:
                ctx.insurance_queue.append([item_name, heart_difference])
        else:
            assert (
                False
            ), f"[Twilight Princess Client] {item_name=} has an invalid type {item_data.type}"

        # Validation completed so wait until starting again
        ctx.validation_pause.set()

        item_give_list: list[str] = []

        while len(ctx.insurance_queue) > 0:

            item_name, count = ctx.insurance_queue.pop()

            assert count > 0
            for _ in range(count):

                item_give_list.append(item_name)

                if len(item_give_list) == 8 or len(ctx.insurance_queue) <= 0:
                    while not await _give_items(ctx, item_give_list):
                        await asyncio.sleep(0.5)

        # Set the timer for validation to start again
        ctx.validation_timer = time.time()


async def check_locations(ctx: TPContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.
    If the location is in the active node check memory rather than save data

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: Twilight Princess client context.
    """
    current_node = read_byte(CURR_NODE_ADDR)

    locations_read = set()

    # node_start_addr = (current_node * 0x20) + NODES_START_ADDR

    for location, data in LOCATION_TABLE.items():

        # There might be a better way but this works for now
        # Also this data is a flag so node handling is not needed
        if location == "Hyrule Castle Ganondorf":
            addr = SAVE_FILE_ADDR + data.offset
            byte = read_byte(addr)
            checked = (byte & data.bit) != 0
            if checked:
                if not ctx.finished_game:
                    logger.info("Game finishing")
                # It sends multiple times incase the server does not acknoledge.
                # Upon completion check locations will stop running
                await ctx.send_msgs(
                    [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                )
                ctx.finished_game = True
                # locations_read.add(TPLocation.get_apid(data.code))
            continue

        # If there is not a valid apid dont bother checking that location
        # apids not given when logic only location
        if not isinstance(data.code, int):
            continue

        # Debug functionality
        if DEBUGGING and (
            not isinstance(data.bit, int) or not isinstance(data.offset, int)
        ):
            logger.info(f"Debug: location:{location} has weird formating")
            continue

        # Depening on locatin type find the memory address for the flag
        # Checks the active memory for the current node
        match (data.type):
            case TPLocationType.Region:
                region = data.region.value
                assert (
                    isinstance(region, int) and data.offset < 0x20
                ), f"Location {location=} has bad region {region} {data=}"
                if region == current_node:
                    addr = ACTIVE_NODE_ADDR + data.offset
                else:
                    addr = (region * 32) + NODES_START_ADDR + data.offset
            case TPLocationType.Flag:
                addr = SAVE_FILE_ADDR + data.offset
            case TPLocationType.Event:
                if DEBUGGING:
                    logger.info(f"Debug: {location}, is an event with an apid")
                continue

        byte = read_byte(addr)
        checked = (byte & data.bit) != 0
        if checked:
            locations_read.add(TPLocation.get_apid(data.code))

    # Build the server data to use a player and team keyed value
    if not ctx.server_data_built:
        new_server_data_copy = {}
        for i, data in enumerate(server_data):
            assert "TP_" not in data["key"], f"{data=}"
            new_key = f"TP_{ctx.team}_{ctx.slot}_{data["key"]}"
            ctx.server_data[i]["key"] = new_key
            new_server_data_copy[new_key] = (
                False if "Current" not in new_key else "Menu"
            )
        ctx.server_data_built = True
        ctx.server_data_copy = new_server_data_copy

    # Build out messages to set data into the server (build before location check for mid check changes)
    messages: list[dict[str, any]] = []
    results: list[dict[str, any]] = []
    assert len(ctx.server_data_copy) > 0, f"{ctx.server_data_copy=}"
    for server_copy_key, server_copy_value in ctx.server_data_copy.items():
        data = [data for data in ctx.server_data if data["key"] == server_copy_key][0]
        assert data, f"{server_copy_key=}"

        if data["Region"] == "Flag":
            assert isinstance(server_copy_value, bool), f"{server_copy_key=}"
            addr = SAVE_FILE_ADDR + data["Offset"]
            byte = read_byte(addr)
            checked = (byte & data["Flag"]) != 0
            if checked != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {checked}"
                    )
                # The value has changed so update the sever
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": checked}],
                    }
                )
                results.append({server_copy_key: checked})

        elif data["Region"] == "Region":
            assert isinstance(server_copy_value, bool), f"{server_copy_key=}"
            region = data["Node"]
            assert (
                isinstance(region, int) and data["Offset"] < 0x20
            ), f"Location {location=} has bad region {region} {data=}"
            if region == current_node:
                addr = ACTIVE_NODE_ADDR + data["Offset"]
            else:
                addr = (region * 32) + NODES_START_ADDR + data["Offset"]
            byte = read_byte(addr)
            checked = (byte & data["Flag"]) != 0
            if checked != server_copy_value:
                # The value has changed so update the sever
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {checked}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": checked}],
                    }
                )
                results.append({server_copy_key: checked})
        elif data["Region"] == "Node Number":
            assert isinstance(server_copy_value, str), f"{server_copy_key=}"
            node = NODE_TO_STRING[server_copy_value]
            if node != ctx.current_node:
                new_node_str = [
                    node
                    for node, num in NODE_TO_STRING.items()
                    if num == ctx.current_node
                ][0]
                assert isinstance(new_node_str, str), f"{new_node_str=}"
                assert new_node_str, f"{new_node_str=}"
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {new_node_str}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": new_node_str}],
                    }
                )
                results.append({server_copy_key: new_node_str})
        elif data["Region"] == "Stage":
            assert isinstance(server_copy_value, str), f"{server_copy_key=}"

            result = read_string(SAVE_FILE_ADDR + 0x58, 8)

            assert isinstance(result, str), f"{result=}"
            assert result in STAGE_TO_NAME, f"{result=}"

            current_stage_str = STAGE_TO_NAME[result]
            if current_stage_str != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {current_stage_str}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": current_stage_str}
                        ],
                    }
                )
                results.append({server_copy_key: current_stage_str})
        else:
            assert False, f"{data=}"

    # Incase the stage changed during location checking
    await asyncio.sleep(0.1)
    if current_node != read_byte(CURR_NODE_ADDR):
        if DEBUGGING:
            logger.info("Debug: Stage changed during location checks skiping checks")
        return

    new_locations_checked = locations_read.difference(ctx.locations_checked)
    if new_locations_checked:
        if DEBUGGING:
            logger.info(f"Debug: Sending location checks: {new_locations_checked}")
        await ctx.send_msgs(
            [{"cmd": "LocationChecks", "locations": new_locations_checked}]
        )
        # This might be needed if the clinet doesn't sync, it might also brick if msg is sent but nothing happens
        ctx.locations_checked.update(new_locations_checked)

    # Send out server data messages
    assert len(messages) == len(results), f"{len(messages)=} {len(results)=}"
    for message, result in zip(messages, results):
        assert (
            message["key"] in result
        ), f"{message["key"]=}, {result=}"  # No longer valid as key is individualized
        if DEBUGGING:
            logger.info(
                f"Debug: Sending message for {message["key"]}: {result[message["key"]]}"
            )
        ctx.server_data_copy[message["key"]] = result[message["key"]]
        await ctx.send_msgs(
            [
                message,
            ]
        )


async def check_alive() -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TPContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and await check_ingame(ctx):
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health == 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 5:
                if DEBUGGING:
                    logger.info(
                        "Debug: Sending Death to other players will not send death until player is alive"
                    )
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            if DEBUGGING and ctx.has_send_death:
                logger.info("Debug: Player is now alive")
            ctx.has_send_death = False


async def check_ingame(ctx: TPContext, level: int = 0) -> bool:
    """
    Check if the player is currently in-game.

    The title stage and randomizer seed pointer are used to avoid treating
    the menu or an unloaded randomizer as an active game state.
    """
    if not dolphin_memory_engine.is_hooked():
        return False

    # The title stage means that no save is currently active.
    if read_string(SAVE_FILE_ADDR + 0x4E00, 8) == "F_SP102":
        if ctx.check_in_game_msg_timer + VALIDATION_TIME <= time.time():
            ctx.check_in_game_msg_timer = time.time()
        return False

    current_node = read_byte(CURR_NODE_ADDR)

    # If the node has not changed, keep the current state.
    if current_node == ctx.current_node:
        if read_pointer(0x800042BC) != 0:
            if (
                ctx.check_in_game_msg_timer + VALIDATION_TIME <= time.time()
                and ctx.connection_tried
            ):
                logger.warning(WRONG_SEED_LOADED_MSG + ctx.SeedID)
                ctx.check_in_game_msg_timer = time.time()
            return True
        return False

    # Hyrule Field can briefly report its node while the game is loading.
    if current_node == 0x06:
        ctx.current_node = current_node

        if level > 3:
            return False

        await asyncio.sleep(3)
        if not await check_ingame(ctx, level + 1):
            return False
    else:
        ctx.current_node = current_node

    if read_pointer(0x800042BC) != 0:
        if (
            ctx.check_in_game_msg_timer + VALIDATION_TIME <= time.time()
            and ctx.connection_tried
        ):
            logger.warning(WRONG_SEED_LOADED_MSG + ctx.SeedID)
            ctx.check_in_game_msg_timer = time.time()
        return True

    return False

def _check_status() -> bool:
    """
    Check if link is in a good state to interact with.

    *Gotten from how lunar chooses when to give player items*
    """
    link_actr = read_pointer(LINK_POINTER_ADDR)

    mEventStatus = read_byte(M_EVENT_STATUS_ADDR)
    mDemoType = read_short(link_actr + 0x604)
    mEventId = read_short(link_actr + 0x7BE)

    return mEventStatus == 0 and mDemoType == 0 and mEventId == 0


async def dolphin_sync_task(ctx: TPContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Twilight Princess client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if (
                dolphin_memory_engine.is_hooked()
                and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            ):

                if not await check_ingame(ctx):
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    # Handle this here as on connect cannot deal with async calls and this is before location checks
                    if not ctx.server_data_sent:
                        await ctx.send_msgs(
                            base_server_data_connection(ctx.team, ctx.slot)
                        )
                        ctx.server_data_sent = True
                    await give_items(ctx)
                    await check_locations(ctx)
                    await validate_item(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_dolphin:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    try:
                        if not (
                            dolphin_memory_engine.read_bytes(0x80000000, 3) == b"GZ2"
                            and dolphin_memory_engine.read_byte(0x80000003)
                            in [
                                ord("E"),
                                ord("P"),
                                ord("J"),
                            ]
                        ):
                            logger.info(CONNECTION_REFUSED_GAME_STATUS)
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            dolphin_memory_engine.un_hook()
                            await asyncio.sleep(5)
                        else:
                            logger.info(CONNECTION_CONNECTED_STATUS)
                            ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                            ctx.locations_checked = set()
                            set_address()
                    except NameError as e:
                        logger.error(f"Global address not set: {e}")
                        set_address(regionCode=ord("E"))
                    except Exception as e:
                        logger.error(f"Unexpected error: {e}")
                        raise e
                else:
                    logger.info(
                        "Connection to Dolphin failed, attempting again in 5 seconds..."
                    )
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info(
                "Connection to Dolphin failed due to error, attempting again in 5 seconds..."
            )
            logger.error(traceback.format_exc())

            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the Twilight Princess client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Twilight Princess Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = TPContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(
            dolphin_sync_task(ctx), name="DolphinSync"
        )

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama  # type: ignore

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
