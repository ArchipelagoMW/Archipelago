import asyncio
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import ISLAND_NAME_TO_SALVAGE_BIT, LOCATION_TABLE, TWWLocation, TWWLocationData, TWWLocationType
from .randomizers.Charts import ISLAND_NUMBER_TO_NAME

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for The Wind Waker. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure The Wind Waker is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


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
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class TWWContext(CommonContext):
    """
    The context for The Wind Waker client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for The Wind Waker.
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
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
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

        # Keep track of whether the player has yet received their first progressive magic meter.
        self.received_magic: bool = False

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

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
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
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.update_salvage_locations_map()
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
        _give_death(self)

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
        self.salvage_locations_map = {}
        for offset in range(49):
            island_name = ISLAND_NUMBER_TO_NAME[offset + 1]
            salvage_bit = ISLAND_NAME_TO_SALVAGE_BIT[island_name]

            shuffled_island_number = read_short(CHARTS_MAPPING_ADDR + offset * 2)
            shuffled_island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            salvage_location_name = f"{shuffled_island_name} - Sunken Treasure"

            self.salvage_locations_map[salvage_location_name] = salvage_bit


def read_short(console_address: int) -> int:
    """
    Read a 2-byte short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2), byteorder="big")


def write_short(console_address: int, value: int) -> None:
    """
    Write a 2-byte short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2, byteorder="big"))


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return dolphin_memory_engine.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def _give_death(ctx: TWWContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: The Wind Waker client context.
    """
    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)


def _give_item(ctx: TWWContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Wind Waker client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame() or dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False

    item_id = ITEM_TABLE[item_name].item_id

    # Loop through the item array, placing the item in an empty slot.
    for idx in range(ctx.len_give_item_array):
        slot = dolphin_memory_engine.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
        if slot == 0xFF:
            # Special case: Use a different item ID for the second progressive magic meter.
            if item_name == "Progressive Magic Meter":
                if ctx.received_magic:
                    item_id = 0xB2
                else:
                    ctx.received_magic = True
            dolphin_memory_engine.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
            return True

    # If unable to place the item in the array, return `False`.
    return False


async def give_items(ctx: TWWContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: The Wind Waker client context.
    """
    if check_ingame() and dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) != 0xFF:
        # Read the expected index of the player, which is the index of the next item they're expecting to receive.
        # The expected index starts at 0 for a fresh save file.
        expected_idx = read_short(EXPECTED_INDEX_ADDR)

        # Check if there are new items.
        received_items = ctx.items_received
        if len(received_items) <= expected_idx:
            # There are no new items.
            return

        # Loop through items to give.
        # Give the player all items at an index greater than or equal to the expected index.
        for idx, item in enumerate(received_items[expected_idx:], start=expected_idx):
            # Attempt to give the item and increment the expected index.
            while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                await asyncio.sleep(0.01)

            # Increment the expected index.
            write_short(EXPECTED_INDEX_ADDR, idx + 1)


def check_special_location(location_name: str, data: TWWLocationData) -> bool:
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
        checked = (
            dolphin_memory_engine.read_byte(data.address) & 0x6 == 0x6
            or dolphin_memory_engine.read_byte(data.address) & 0x7 == 0x7
        )

    # The "Windfall Island - Maggie - Delivery Reward" flag remains unknown.
    # However, as a temporary workaround, we can check if the player had Moblin's letter at some point, but it's no
    # longer in their Delivery Bag.
    elif location_name == "Windfall Island - Maggie - Delivery Reward":
        was_moblins_owned = (dolphin_memory_engine.read_word(LETTER_OWND_ADDR) >> 15) & 1
        dbag_contents = [dolphin_memory_engine.read_byte(LETTER_BASE_ADDR + offset) for offset in range(8)]
        checked = was_moblins_owned and 0x9B not in dbag_contents

    # For Letter from Hoskit's Girlfriend, we need to check two bytes.
    # 0x1 = Golden Feathers delivered, 0x2 = Mail sent by Hoskit's Girlfriend, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Hoskit's Girlfriend":
        checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

    # For Letter from Baito's Mother, we need to check two bytes.
    # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Baito's Mother":
        checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

    # For Letter from Grandma, we need to check two bytes.
    # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Grandma":
        checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

    # We check if the bits for turning all five statues are set for the Ankle's reward.
    # For some reason, the bit for the Dragon Tingle Statue is separate from the rest.
    elif location_name == "Tingle Island - Ankle - Reward for All Tingle Statues":
        dragon_tingle_statue_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
        other_tingle_statues_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
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
    ctx.charts_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(CHARTS_BITFLD_ADDR, 8), byteorder="big")

    # Read the bitfields once before the loop to speed things up a bit.
    ctx.chests_bitfields = {}
    ctx.switches_bitfields = {}
    ctx.pickups_bitfields = {}
    for stage_id in range(0xE):
        chest_bitfield_addr = BASE_CHESTS_BITFLD_ADDR + (0x24 * stage_id)
        switches_bitfield_addr = BASE_SWITCHES_BITFLD_ADDR + (0x24 * stage_id)
        pickups_bitfield_addr = BASE_PICKUPS_BITFLD_ADDR + (0x24 * stage_id)

        ctx.chests_bitfields[stage_id] = int(dolphin_memory_engine.read_word(chest_bitfield_addr))
        ctx.switches_bitfields[stage_id] = int.from_bytes(
            dolphin_memory_engine.read_bytes(switches_bitfield_addr, 10), byteorder="big"
        )
        ctx.pickups_bitfields[stage_id] = int(dolphin_memory_engine.read_word(pickups_bitfield_addr))

    ctx.curr_stage_chests_bitfield = int(dolphin_memory_engine.read_word(CURR_STAGE_CHESTS_BITFLD_ADDR))
    ctx.curr_stage_switches_bitfield = int.from_bytes(
        dolphin_memory_engine.read_bytes(CURR_STAGE_SWITCHES_BITFLD_ADDR, 10), byteorder="big"
    )
    ctx.curr_stage_pickups_bitfield = int(dolphin_memory_engine.read_word(CURR_STAGE_PICKUPS_BITFLD_ADDR))

    # We check which locations are currently checked on the current stage.
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    # Loop through all locations to see if each has been checked.
    for location, data in LOCATION_TABLE.items():
        checked = False
        if data.type == TWWLocationType.CHART:
            assert location in ctx.salvage_locations_map, f'Location "{location}" salvage bit not set!'
            salvage_bit = ctx.salvage_locations_map[location]
            checked = bool((ctx.charts_bitfield >> salvage_bit) & 1)
        elif data.type == TWWLocationType.BOCTO:
            assert data.address is not None
            checked = bool((read_short(data.address) >> data.bit) & 1)
        elif data.type == TWWLocationType.EVENT:
            checked = bool((dolphin_memory_engine.read_byte(data.address) >> data.bit) & 1)
        elif data.type == TWWLocationType.SPECL:
            checked = check_special_location(location, data)
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
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def check_current_stage_changed(ctx: TWWContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The Wind Waker client context.
    """
    new_stage_name = read_string(CURR_STAGE_NAME_ADDR, 8)

    # Special handling is required for the Cliff Plateau Isles Inner Cave exit, which exits out onto the sea stage
    # rather than a unique stage.
    if (
        new_stage_name == "sea"
        and dolphin_memory_engine.read_byte(MOST_RECENT_ROOM_NUMBER_ADDR) == CLIFF_PLATEAU_ISLES_ROOM_NUMBER
        and read_short(MOST_RECENT_SPAWN_ID_ADDR) == CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_SPAWN_ID
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


async def check_alive() -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and check_ingame():
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame() -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    return read_string(CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


async def dolphin_sync_task(ctx: TWWContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The Wind Waker client context.
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
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    # Reset the give item array while not in the game.
                    dolphin_memory_engine.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    sleep_time = 0.1
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                sleep_time = 0.1
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
                        sleep_time = 5
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            sleep_time = 5
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the Wind Waker client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
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

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
