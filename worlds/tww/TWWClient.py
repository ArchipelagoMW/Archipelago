import asyncio
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import ISLAND_NAME_TO_SALVAGE_BIT, LOCATION_TABLE, TWWLocation, TWWLocationData, TWWLocationType
from .Memory import APBridgeError, APBridgeWriteUncertainError, ConsoleMemory, DolphinMemory, WiiMemory
from .randomizers.Charts import ISLAND_NUMBER_TO_NAME

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = (
    "{backend} failed to connect. Please load a randomized ROM for The Wind Waker. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "{backend} failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "{backend} connection was lost. Please check the game and connection."
)
CONNECTION_CONNECTED_STATUS = "{backend} connected successfully."
CONNECTION_INITIAL_STATUS = "{backend} connection has not been initiated."
ITEM_DELIVERY_UNCERTAIN_STATUS = (
    "Item delivery is paused because a Wii item write or index update could not be confirmed. "
    "To avoid duplicate or missing items, do not save this session. Reload your last save, then restart the client."
)


# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x803C4C0A

# These addresses are used for the Moblin's Letter check.
LETTER_BASE_ADDR = 0x803C4C8E
LETTER_OWND_ADDR = 0x803C4C98

# These addresses are used to check flags for locations.
CHARTS_BITFLD_ADDR = 0x803C4CFC
BASE_CHESTS_BITFLD_ADDR = 0x803C4F88
BASE_SWITCHES_BITFLD_ADDR = 0x803C4F8C
BASE_PICKUPS_BITFLD_ADDR = 0x803C4F9C
CURR_STAGE_CHESTS_BITFLD_ADDR = 0x803C5380
CURR_STAGE_SWITCHES_BITFLD_ADDR = 0x803C5384
CURR_STAGE_PICKUPS_BITFLD_ADDR = 0x803C5394

# The expected index for the following item that should be received. Uses event bits 0x60 and 0x61.
EXPECTED_INDEX_ADDR = 0x803C528C

# These bytes contain whether the player has been rewarded for finding a particular Tingle statue.
TINGLE_STATUE_1_ADDR = 0x803C523E  # 0x40 is the bit for the Dragon Tingle statue.
TINGLE_STATUE_2_ADDR = 0x803C5249  # 0x0F are the bits for the remaining Tingle statues.

# This address contains the current stage ID.
CURR_STAGE_ID_ADDR = 0x803C53A4

# This address is used to check the stage name to verify that the player is in-game before sending items.
CURR_STAGE_NAME_ADDR = 0x803C9D3C

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
GIVE_ITEM_ARRAY_ADDR = 0x803FE87C

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
SLOT_NAME_ADDR = 0x803FE8A0

# This address is the start of an array that we use to inform us of which charts lead where.
# The array is of length 49, and each element is two bytes. The index represents the chart's original destination, and
# the value represents the new destination.
# The chart name is inferrable from the chart's original destination.
CHARTS_MAPPING_ADDR = 0x803FE8E0

# This address contains the most recent spawn ID from which the player spawned.
MOST_RECENT_SPAWN_ID_ADDR = 0x803C9D44

# This address contains the most recent room number the player spawned in.
MOST_RECENT_ROOM_NUMBER_ADDR = 0x803C9D46

# Values used to detect exiting onto the highest isle in Cliff Plateau Isles.
# 42. Starting at 1 and going left to right, top to bottom, Cliff Plateau Isles is the 42nd square in the sea stage.
CLIFF_PLATEAU_ISLES_ROOM_NUMBER = 0x2A
CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_SPAWN_ID = 1  # As a note, the lower isle's spawn ID is 2.
# The dummy stage name used to identify the highest isle in Cliff Plateau Isles.
CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_DUMMY_STAGE_NAME = "CliPlaH"

# Data storage key
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "tww_visited_stages_%i"


class TWWCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for The Wind Waker client commands.

    This class handles commands specific to The Wind Waker.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status.
        """
        if isinstance(self.ctx, TWWContext):
            if isinstance(self.ctx.memory, DolphinMemory):
                logger.info(f"Dolphin Status: {self.ctx.console_status}")
            else:
                logger.info(f"Dolphin is inactive. Selected console: {self.ctx.memory.description}")

    def _cmd_console(self, address: str = "") -> bool:
        """Select Wii AP Bridge with /console <IPv4 address>, /console off for Dolphin, or /console for status."""
        if not isinstance(self.ctx, TWWContext):
            return False
        if not address:
            self.output(f"Console: {self.ctx.memory.description}. {self.ctx.console_status}")
            if self.ctx.pending_memory is not None:
                self.output(f"Switching to {self.ctx.pending_memory.description}...")
            if self.ctx.item_delivery_uncertain:
                self.output(ITEM_DELIVERY_UNCERTAIN_STATUS)
            return True
        try:
            memory = DolphinMemory() if address.lower() == "off" else WiiMemory(address)
        except ValueError as error:
            self.output(f"Invalid Wii IPv4 address: {error}. Use /console <IPv4 address> or /console off.")
            return False
        self.ctx.pending_memory = memory
        self.ctx.watcher_event.set()
        self.output(f"Selecting {memory.description}. Use /connect to join your AP server after switching.")
        return True


class TWWContext(CommonContext):
    """
    The context for The Wind Waker client.

    This class manages all interactions with the selected console and the Archipelago server for The Wind Waker.
    """

    command_processor = TWWCommandProcessor
    game: str = "The Wind Waker"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the TWW context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """

        super().__init__(server_address, password)
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.memory: ConsoleMemory = DolphinMemory()
        self.pending_memory: Optional[ConsoleMemory] = None
        self.console_status: str = CONNECTION_INITIAL_STATUS.format(backend=self.memory.name)
        self.item_delivery_uncertain: bool = False
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False

        # Bitfields used for checking locations.
        self.charts_bitfield: int
        self.chests_bitfields: dict[int, int]
        self.switches_bitfields: dict[int, int]
        self.pickups_bitfields: dict[int, int]
        self.curr_stage_chests_bitfield: int
        self.curr_stage_switches_bitfield: int
        self.curr_stage_pickups_bitfield: int

        # Keep track of when the player received their first progressive magic meter.
        self.received_magic_idx: int = -1

        # A dictionary that maps salvage locations to their sunken treasure bit.
        self.salvage_locations_map: dict[str, int] = {}

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""

        # Set of visited stages. A dictionary (used as a set) of all visited stages is set in the server's data storage
        # and updated when the player visits a new stage for the first time. To track which stages are new and need to
        # cause the server's data storage to update, the TWW AP Client keeps track of the visited stages in a set.
        # Trackers can request the dictionary from data storage to see which stages the player has visited.
        # It starts as `None` until it has been read from the server.
        self.visited_stage_names: Optional[set[str]] = None

        # Length of the item get array in memory.
        self.len_give_item_array: int = 0x10

    @property
    def connected_status(self) -> str:
        return CONNECTION_CONNECTED_STATUS.format(backend=self.memory.name)

    def memory_connection_lost(self, error: Exception) -> None:
        self.memory.un_hook()
        self.console_status = CONNECTION_LOST_STATUS.format(backend=self.memory.name)
        logger.error(f"{self.console_status} {error}. Reconnecting...")
        self.watcher_event.set()

    def pause_item_delivery(self) -> None:
        # This must survive reconnects and backend switches. The wire protocol
        # cannot tell us whether an item was consumed after a lost acknowledgment.
        self.item_delivery_uncertain = True
        logger.error(ITEM_DELIVERY_UNCERTAIN_STATUS)

    async def switch_memory(self) -> None:
        memory = self.pending_memory
        assert memory is not None
        self.pending_memory = None
        self.memory.un_hook()
        # Never carry a server slot or an item list into a different console.
        await self.disconnect()
        self.reset_server_state()
        self.reset_session_state()
        self.memory = memory
        self.console_status = CONNECTION_INITIAL_STATUS.format(backend=memory.name)
        self.received_magic_idx = -1
        self.has_send_death = False

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        self.awaiting_rom = False
        self.salvage_locations_map = {}
        self.current_stage_name = ""
        self.visited_stage_names = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info(f"Awaiting connection to {self.memory.name} to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.salvage_locations_map = {}
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
                if visited_stages_key in requested_keys_dict:
                    visited_stages = requested_keys_dict[visited_stages_key]
                    # If it has not been set before, the value in the response will be `None`.
                    visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
                    # If the current stage name is not in the set, send a message to update the dictionary on the
                    # server.
                    current_stage_name = self.current_stage_name
                    if current_stage_name and current_stage_name not in visited_stage_names:
                        visited_stage_names.add(current_stage_name)
                        Utils.async_start(self.update_visited_stages(current_stage_name))
                    self.visited_stage_names = visited_stage_names

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        try:
            _give_death(self)
        except APBridgeError as error:
            # DeathLink is delivered outside the memory sync task.
            self.memory_connection_lost(error)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for The Wind Waker client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago The Wind Waker Client"
        return ui

    async def update_visited_stages(self, newly_visited_stage_name: str) -> None:
        """
        Update the server's data storage of the visited stage names to include the newly visited stage name.

        :param newly_visited_stage_name: The name of the stage recently visited.
        """
        if self.slot is not None:
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": visited_stages_key,
                        "default": {},
                        "want_reply": False,
                        "operations": [{"operation": "update", "value": {newly_visited_stage_name: True}}],
                    }
                ]
            )

    def update_salvage_locations_map(self) -> None:
        """
        Update the client's mapping of salvage locations to their bitfield bit.

        This is necessary for the client to handle randomized charts correctly.
        """
        salvage_locations_map = {}
        for offset in range(49):
            island_name = ISLAND_NUMBER_TO_NAME[offset + 1]
            salvage_bit = ISLAND_NAME_TO_SALVAGE_BIT[island_name]

            shuffled_island_number = read_short(self, CHARTS_MAPPING_ADDR + offset * 2)
            shuffled_island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            salvage_location_name = f"{shuffled_island_name} - Sunken Treasure"

            salvage_locations_map[salvage_location_name] = salvage_bit
        self.salvage_locations_map = salvage_locations_map


def read_short(ctx: TWWContext, console_address: int) -> int:
    """
    Read a 2-byte short from console memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(ctx.memory.read_bytes(console_address, 2), byteorder="big")


def write_short(ctx: TWWContext, console_address: int, value: int) -> None:
    """
    Write a 2-byte short to console memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    ctx.memory.write_bytes(console_address, value.to_bytes(2, byteorder="big"))


def read_string(ctx: TWWContext, console_address: int, strlen: int) -> str:
    """
    Read a string from console memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return ctx.memory.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def _give_death(ctx: TWWContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: The Wind Waker client context.
    """
    if (
        ctx.slot is not None
        and ctx.memory.is_hooked()
        and ctx.console_status == ctx.connected_status
        and check_ingame(ctx)
    ):
        ctx.has_send_death = True
        write_short(ctx, CURR_HEALTH_ADDR, 0)


def _give_item(ctx: TWWContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Wind Waker client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame(ctx) or ctx.memory.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False

    item_id = ITEM_TABLE[item_name].item_id
    assert item_id is not None

    # Loop through the item array, placing the item in an empty slot.
    for idx in range(ctx.len_give_item_array):
        slot = ctx.memory.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
        if slot == 0xFF:
            # Special case: Use a different item ID for the second progressive magic meter.
            if item_name == "Progressive Magic Meter":
                if ctx.received_magic_idx == -1:
                    ctx.received_magic_idx = idx
                elif idx > ctx.received_magic_idx:
                    item_id = 0xB2
            ctx.memory.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
            return True

    # If unable to place the item in the array, return `False`.
    return False


async def give_items(ctx: TWWContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: The Wind Waker client context.
    """
    if ctx.item_delivery_uncertain:
        return
    if check_ingame(ctx) and ctx.memory.read_byte(CURR_STAGE_ID_ADDR) != 0xFF:
        # Read the expected index of the player, which is the index of the next item they're expecting to receive.
        # The expected index starts at 0 for a fresh save file.
        expected_idx = read_short(ctx, EXPECTED_INDEX_ADDR)

        # Check if there are new items.
        received_items = ctx.items_received
        if len(received_items) <= expected_idx:
            # There are no new items.
            return

        # Loop through items to give.
        # Give the player all items at an index greater than or equal to the expected index.
        for idx, item in enumerate(received_items[expected_idx:], start=expected_idx):
            # Attempt to give the item and increment the expected index.
            try:
                while True:
                    if ctx.exit_event.is_set() or ctx.pending_memory is not None:
                        return
                    if _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                        break
                    await asyncio.sleep(0.01)
            except APBridgeWriteUncertainError:
                ctx.pause_item_delivery()
                raise

            # Increment the expected index.
            try:
                write_short(ctx, EXPECTED_INDEX_ADDR, idx + 1)
            except APBridgeError:
                # Even a rejected index write leaves the acknowledged item queued
                # or consumed, so the old index must not cause another delivery.
                ctx.pause_item_delivery()
                raise


def check_special_location(ctx: TWWContext, location_name: str, data: TWWLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that require special logic.

    :param location_name: The name of the location.
    :param data: The data associated with the location.
    :raises NotImplementedError: If an unknown location name is provided.
    """
    checked = False

    # For "Windfall Island - Lenzo's House - Become Lenzo's Assistant"
    # 0x6 is delivered the final picture for Lenzo, 0x7 is a day has passed since becoming his assistant
    # Either is fine for sending the check, so check both conditions.
    if location_name == "Windfall Island - Lenzo's House - Become Lenzo's Assistant":
        assert data.address is not None
        checked = (
            ctx.memory.read_byte(data.address) & 0x6 == 0x6
            or ctx.memory.read_byte(data.address) & 0x7 == 0x7
        )

    # The "Windfall Island - Maggie - Delivery Reward" flag remains unknown.
    # However, as a temporary workaround, we can check if the player had Moblin's letter at some point, but it's no
    # longer in their Delivery Bag.
    elif location_name == "Windfall Island - Maggie - Delivery Reward":
        was_moblins_owned = (ctx.memory.read_word(LETTER_OWND_ADDR) >> 15) & 1
        dbag_contents = [ctx.memory.read_byte(LETTER_BASE_ADDR + offset) for offset in range(8)]
        checked = bool(was_moblins_owned and 0x9B not in dbag_contents)

    # For Letter from Hoskit's Girlfriend, we need to check two bytes.
    # 0x1 = Golden Feathers delivered, 0x2 = Mail sent by Hoskit's Girlfriend, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Hoskit's Girlfriend":
        assert data.address is not None
        checked = ctx.memory.read_byte(data.address) & 0x3 == 0x3

    # For Letter from Baito's Mother, we need to check two bytes.
    # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Baito's Mother":
        assert data.address is not None
        checked = ctx.memory.read_byte(data.address) & 0x3 == 0x3

    # For Letter from Grandma, we need to check two bytes.
    # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Grandma":
        assert data.address is not None
        checked = ctx.memory.read_byte(data.address) & 0x3 == 0x3

    # We check if the bits for turning all five statues are set for the Ankle's reward.
    # For some reason, the bit for the Dragon Tingle Statue is separate from the rest.
    elif location_name == "Tingle Island - Ankle - Reward for All Tingle Statues":
        dragon_tingle_statue_rewarded = ctx.memory.read_byte(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
        other_tingle_statues_rewarded = ctx.memory.read_byte(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
        checked = dragon_tingle_statue_rewarded and other_tingle_statues_rewarded

    else:
        raise NotImplementedError(f"Unknown special location: {location_name}")

    return checked


def check_regular_location(ctx: TWWContext, curr_stage_id: int, data: TWWLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that only require checking that a particular bit is set.

    The check looks at the saved data for the stage at which the location is located and the data for the current stage.
    In the latter case, this data includes data that has not yet been written to the saved data.

    :param ctx: The Wind Waker client context.
    :param curr_stage_id: The current stage at which the player is.
    :param data: The data associated with the location.
    :raises NotImplementedError: If a location with an unknown type is provided.
    """
    checked = False

    # Check the saved bitfields for the stage.
    if data.type == TWWLocationType.CHEST:
        checked = bool((ctx.chests_bitfields[data.stage_id] >> data.bit) & 1)
    elif data.type == TWWLocationType.SWTCH:
        checked = bool((ctx.switches_bitfields[data.stage_id] >> data.bit) & 1)
    elif data.type == TWWLocationType.PCKUP:
        checked = bool((ctx.pickups_bitfields[data.stage_id] >> data.bit) & 1)
    else:
        raise NotImplementedError(f"Unknown location type: {data.type}")

    # If the location is in the current stage, check the bitfields for the current stage as well.
    if not checked and curr_stage_id == data.stage_id:
        if data.type == TWWLocationType.CHEST:
            checked = bool((ctx.curr_stage_chests_bitfield >> data.bit) & 1)
        elif data.type == TWWLocationType.SWTCH:
            checked = bool((ctx.curr_stage_switches_bitfield >> data.bit) & 1)
        elif data.type == TWWLocationType.PCKUP:
            checked = bool((ctx.curr_stage_pickups_bitfield >> data.bit) & 1)
        else:
            raise NotImplementedError(f"Unknown location type: {data.type}")

    return checked


async def check_locations(ctx: TWWContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: The Wind Waker client context.
    """
    # Read the bitfield for sunken treasure locations.
    ctx.charts_bitfield = int.from_bytes(ctx.memory.read_bytes(CHARTS_BITFLD_ADDR, 8), byteorder="big")

    # Read the bitfields once before the loop to speed things up a bit.
    ctx.chests_bitfields = {}
    ctx.switches_bitfields = {}
    ctx.pickups_bitfields = {}
    for stage_id in range(0xE):
        chest_bitfield_addr = BASE_CHESTS_BITFLD_ADDR + (0x24 * stage_id)
        switches_bitfield_addr = BASE_SWITCHES_BITFLD_ADDR + (0x24 * stage_id)
        pickups_bitfield_addr = BASE_PICKUPS_BITFLD_ADDR + (0x24 * stage_id)

        ctx.chests_bitfields[stage_id] = int(ctx.memory.read_word(chest_bitfield_addr))
        ctx.switches_bitfields[stage_id] = int.from_bytes(
            ctx.memory.read_bytes(switches_bitfield_addr, 10), byteorder="big"
        )
        ctx.pickups_bitfields[stage_id] = int(ctx.memory.read_word(pickups_bitfield_addr))

    ctx.curr_stage_chests_bitfield = int(ctx.memory.read_word(CURR_STAGE_CHESTS_BITFLD_ADDR))
    ctx.curr_stage_switches_bitfield = int.from_bytes(
        ctx.memory.read_bytes(CURR_STAGE_SWITCHES_BITFLD_ADDR, 10), byteorder="big"
    )
    ctx.curr_stage_pickups_bitfield = int(ctx.memory.read_word(CURR_STAGE_PICKUPS_BITFLD_ADDR))

    # We check which locations are currently checked on the current stage.
    curr_stage_id = ctx.memory.read_byte(CURR_STAGE_ID_ADDR)

    # Loop through all locations to see if each has been checked.
    for location, data in LOCATION_TABLE.items():
        checked = False
        if data.type == TWWLocationType.CHART:
            assert location in ctx.salvage_locations_map, f'Location "{location}" salvage bit not set!'
            salvage_bit = ctx.salvage_locations_map[location]
            checked = bool((ctx.charts_bitfield >> salvage_bit) & 1)
        elif data.type == TWWLocationType.BOCTO:
            assert data.address is not None
            checked = bool((read_short(ctx, data.address) >> data.bit) & 1)
        elif data.type == TWWLocationType.EVENT:
            assert data.address is not None
            checked = bool((ctx.memory.read_byte(data.address) >> data.bit) & 1)
        elif data.type == TWWLocationType.SPECL:
            checked = check_special_location(ctx, location, data)
        else:
            checked = check_regular_location(ctx, curr_stage_id, data)

        if checked:
            if data.code is None:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            else:
                ctx.locations_checked.add(TWWLocation.get_apid(data.code))

    # Send the list of newly-checked locations to the server.
    await ctx.check_locations(ctx.locations_checked)


async def check_current_stage_changed(ctx: TWWContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The Wind Waker client context.
    """
    new_stage_name = read_string(ctx, CURR_STAGE_NAME_ADDR, 8)

    # Special handling is required for the Cliff Plateau Isles Inner Cave exit, which exits out onto the sea stage
    # rather than a unique stage.
    if (
        new_stage_name == "sea"
        and ctx.memory.read_byte(MOST_RECENT_ROOM_NUMBER_ADDR) == CLIFF_PLATEAU_ISLES_ROOM_NUMBER
        and read_short(ctx, MOST_RECENT_SPAWN_ID_ADDR) == CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_SPAWN_ID
    ):
        new_stage_name = CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_DUMMY_STAGE_NAME

    current_stage_name = ctx.current_stage_name
    if new_stage_name != current_stage_name:
        ctx.current_stage_name = new_stage_name
        # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
        data_to_send = {"tww_stage_name": new_stage_name}
        message = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": data_to_send,
        }
        await ctx.send_msgs([message])

        # If the stage has never been visited before, update the server's data storage to indicate that it has been
        # visited.
        visited_stage_names = ctx.visited_stage_names
        if visited_stage_names is not None and new_stage_name not in visited_stage_names:
            visited_stage_names.add(new_stage_name)
            await ctx.update_visited_stages(new_stage_name)


async def check_alive(ctx: TWWContext) -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(ctx, CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and check_ingame(ctx):
        cur_health = read_short(ctx, CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame(ctx: TWWContext) -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    return read_string(ctx, CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


async def dolphin_sync_task(ctx: TWWContext) -> None:
    """
    Manage the selected console connection and synchronize game state.

    The task keeps its original name for compatibility with the client startup.
    """
    logger.info("Starting console connector. Use /console for selection/status or /dolphin for Dolphin status.")
    sleep_time = 0.0
    try:
        while not ctx.exit_event.is_set():
            if sleep_time > 0.0:
                try:
                    # Also wake when the user selects a different console.
                    await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
                except asyncio.TimeoutError:
                    pass
                sleep_time = 0.0
            ctx.watcher_event.clear()
            if ctx.exit_event.is_set():
                break

            try:
                if ctx.pending_memory is not None:
                    await ctx.switch_memory()
                    continue
                if ctx.memory.is_hooked() and ctx.console_status == ctx.connected_status:
                    if not check_ingame(ctx):
                        # Reset the give item array while not in the game.
                        ctx.memory.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                        sleep_time = 0.1
                        continue
                    if ctx.slot is not None:
                        # Read charts here so transport errors use the same reconnect
                        # path as other memory operations, rather than escaping on_package.
                        if not ctx.salvage_locations_map:
                            ctx.update_salvage_locations_map()
                        if "DeathLink" in ctx.tags:
                            await check_death(ctx)
                        await give_items(ctx)
                        if ctx.pending_memory is not None or ctx.exit_event.is_set():
                            continue
                        await check_locations(ctx)
                        await check_current_stage_changed(ctx)
                    else:
                        if not ctx.auth:
                            ctx.auth = read_string(ctx, SLOT_NAME_ADDR, 0x40)
                        if ctx.awaiting_rom:
                            await ctx.server_auth()
                    sleep_time = 0.1
                else:
                    if ctx.console_status == ctx.connected_status:
                        logger.info(f"Connection to {ctx.memory.name} lost, reconnecting...")
                        ctx.console_status = CONNECTION_LOST_STATUS.format(backend=ctx.memory.name)
                    logger.info(f"Attempting to connect to {ctx.memory.description}...")
                    ctx.memory.hook()
                    if ctx.memory.is_hooked():
                        if ctx.memory.read_bytes(0x80000000, 6) != b"GZLE99":
                            ctx.console_status = CONNECTION_REFUSED_GAME_STATUS.format(backend=ctx.memory.name)
                            logger.info(ctx.console_status)
                            ctx.memory.un_hook()
                            sleep_time = 5
                        else:
                            ctx.console_status = ctx.connected_status
                            logger.info(ctx.console_status)
                            ctx.locations_checked = set()
                    else:
                        logger.info(f"Connection to {ctx.memory.name} failed, attempting again in 5 seconds...")
                        ctx.console_status = CONNECTION_LOST_STATUS.format(backend=ctx.memory.name)
                        await ctx.disconnect()
                        sleep_time = 5
            except Exception as error:
                ctx.memory_connection_lost(error)
                if not isinstance(error, APBridgeError):
                    logger.error(traceback.format_exc())
                await ctx.disconnect()
                # memory_connection_lost also wakes this task when called by DeathLink.
                ctx.watcher_event.clear()
                sleep_time = 5
    finally:
        ctx.memory.un_hook()


def main(*args: str) -> None:
    """
    Run the main async loop for the Wind Waker client.

    :param *args: Command line arguments passed to the client.
    """
    Utils.init_logging("The Wind Waker Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = TWWContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    parser = get_base_parser()
    parsed_args = parser.parse_args(args)

    import colorama

    colorama.init()
    asyncio.run(_main(parsed_args.connect, parsed_args.password))
    colorama.deinit()
