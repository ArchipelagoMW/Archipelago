import asyncio
import traceback
from typing import Optional, Any

import dolphin_memory_engine as dme

import ModuleUpdate
from worlds.pokepark.adresses import \
    LOCATIONS, \
    MemoryAddress, ITEMS, PowerItem, POWER_MAP
from worlds.pokepark.dme_helper import read_memory

ModuleUpdate.update()

import Utils

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

SLOT_NAME_ADDR = 0x80001820
GIVE_ITEM_ADDR = 0x80001804
OPCODE_ADDR = 0x80001808
GLOBAL_MANAGER_STRUC_POINTER = 0x80001800
CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Pokepark. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Pokepark is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "pokepark_visited_stages_%i"

STAGE_NAME_MAP = {
    0x0101.to_bytes(2): "Meadow Zone Overworld",
    0x0201.to_bytes(2): "Treehouse",

}


class PokeparkCommandProcessor(ClientCommandProcessor):

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
        if isinstance(self.ctx, PokeparkContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class PokeparkContext(CommonContext):
    command_processor = PokeparkCommandProcessor
    game = "PokePark"
    items_handling = 0b111  # full remote
    victory = False

    def __init__(self, server_address, password):
        super(PokeparkContext, self).__init__(server_address, password)
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_rcvd_index: int = -1
        self.visited_stage_names: Optional[set[str]] = None

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        self.current_stage_name = ""
        self.visited_stage_names = None
        self.dash_index = 0
        self.thunderbolt_index = 0
        self.health_index = 0
        self.iron_tail_index = 0
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
            self.items_received_2 = []
            self.last_rcvd_index = -1
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
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

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class PokeparkManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pokepark Client"

        self.ui = PokeparkManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

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


def _give_item(ctx: PokeparkContext, item_id: int) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Pokepark client context.
    :param item_id: Id of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame():
        return False

    item_slot = dme.read_word(GIVE_ITEM_ADDR)
    opcode_slot = dme.read_word(OPCODE_ADDR)
    if item_id not in ITEMS:
        return True
    item = ITEMS[item_id]
    if item_slot == 0xFFFFFFFF and opcode_slot == 0xFFFFFFFF:

        if isinstance(item, PowerItem):
            if item.item_name == "Progressive Dash":
                index = ctx.dash_index
                ctx.dash_index += 1
            elif item.item_name == "Progressive Thunderbolt":
                index = ctx.thunderbolt_index
                ctx.thunderbolt_index += 1
            elif item.item_name == "Progressive Health":
                index = ctx.health_index
                ctx.health_index += 1
            elif item.item_name == "Progressive Iron Tail":
                index = ctx.iron_tail_index
                ctx.iron_tail_index += 1
            else:
                return False

            max_index = len(POWER_MAP[item.item_id]) - 1
            if index <= max_index:
                item_id = POWER_MAP[item.item_id][index]
                opcode = item.opcode
            else:
                return True

        else:
            item_id = item.item_id
            opcode = item.opcode
        dme.write_word(OPCODE_ADDR, opcode)
        dme.write_word(GIVE_ITEM_ADDR, item_id)
        return True

    return False


async def give_items(ctx: PokeparkContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Pokepark client context.
    """
    global_manager_data_struc_address = dme.read_word(GLOBAL_MANAGER_STRUC_POINTER)
    chapter_address = global_manager_data_struc_address + 0x2d
    if check_ingame():
        # Read the expected index of the player, which is the index of the latest item they've received.
        expected_idx = int.from_bytes(dme.read_bytes(chapter_address, 2), byteorder="big")

        # Loop through items to give.
        for item, idx in ctx.items_received_2:
            # If the item's index is greater than the player's expected index, give the player the item.
            if expected_idx <= idx:
                # Attempt to give the item and increment the expected index.
                while not _give_item(ctx, item.item):
                    await asyncio.sleep(0.01)

                # Increment the expected index.
                dme.write_bytes(chapter_address, (idx + 0x1).to_bytes(2, byteorder="big"))


async def check_current_stage_changed(ctx: PokeparkContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The Pokepark client context.
    """
    global_manager_data_struc_address = dme.read_word(GLOBAL_MANAGER_STRUC_POINTER)
    new_stage = dme.read_bytes(global_manager_data_struc_address + 0x5F00, 2)
    new_stage_name = STAGE_NAME_MAP.get(new_stage)
    if new_stage_name:
        current_stage_name = ctx.current_stage_name
        if new_stage_name != current_stage_name:
            ctx.current_stage_name = new_stage_name
            # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
            data_to_send = {"pokepark_stage_name": new_stage_name}
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


async def check_locations(ctx: PokeparkContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: The Pokepark client context.
    """

    global_manager_data_struc_address = dme.read_word(GLOBAL_MANAGER_STRUC_POINTER)
    for location in LOCATIONS:
        expected_value = location.expected_value
        memory = MemoryAddress(global_manager_data_struc_address,
                               location.final_offset,
                               memory_range=location.memory_range)
        current_value = read_memory(dme, memory)
        if (current_value & location.bit_mask) == expected_value:
            for locationId in location.location_ids:
                ctx.locations_checked.add(locationId)

    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return dme.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def check_ingame() -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    global_manager_data_struc_address = dme.read_word(GLOBAL_MANAGER_STRUC_POINTER)
    pointer = dme.read_byte(global_manager_data_struc_address + 0x1B8)
    chapter_address = global_manager_data_struc_address + 0x2d
    expected_idx = int.from_bytes(dme.read_bytes(chapter_address, 2), byteorder="big")
    if pointer == 0 and expected_idx == 0:
        return False
    return True


async def dolphin_sync_task(ctx: PokeparkContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The Wind Waker client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    # Reset the give item array while not in the game.
                    dme.write_bytes(GIVE_ITEM_ADDR, bytes([0xFF] * 8))
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot is not None:

                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
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
                dme.hook()
                if dme.is_hooked():
                    value = dme.read_bytes(0x80000000, 6)
                    if value not in (b"R8AJ99", b"R8AE99", b"R8AP99"):
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
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
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def check_victory(items: list[NetworkItem], ctx: PokeparkContext):
    for item in items:
        if item.item == 999999:
            send_victory(ctx)


def send_victory(ctx: PokeparkContext):
    if ctx.victory:
        return

    ctx.victory = True
    ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    logger.info("Congratulations")
    return


def main(connect=None, password=None):
    Utils.init_logging("PokeparkClient", exception_logger="Client")

    async def _main(connect, password):
        ctx = PokeparkContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
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
    parser = get_base_parser(description="Pokepark Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)
