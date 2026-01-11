import asyncio
import copy
import time
import traceback
import textwrap
from typing import TYPE_CHECKING, Any, List, Optional

import dolphin_memory_engine

import Utils
from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)
from NetUtils import ClientStatus, NetworkItem

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import LOCATION_TABLE, SSLocation, SSLocFlag, SSLocType, SSLocCheckedFlag
from .Hints import HINT_TABLE, SSHint
from .SSClientUtils import *

if TYPE_CHECKING:
    import kvui


class SSCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for SS client commands.
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
        if isinstance(self.ctx, SSContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}") 
            
    def _cmd_deathlink(self) -> None:
        """Toggle DeathLink."""
        if isinstance(self.ctx, SSContext):
            if "DeathLink" in self.ctx.tags:
                Utils.async_start(self.ctx.update_death_link(False))
                logger.info("Deathlink disabled.")
            else:
                Utils.async_start(self.ctx.update_death_link(True))
                logger.info("Deathlink enabled.")


class SSContext(CommonContext):
    """
    The context for the SS client.

    Manages the connection between the server and the emulator.
    """

    command_processor = SSCommandProcessor
    game: str = "Skyward Sword"
    items_handling: int = 0b001

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the SS context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """

        super().__init__(server_address, password)
        self.items_rcvd: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_rcvd_index: int = -1
        self.has_send_death: bool = False
        self.locations_for_hint: dict[str, list] = {}

        self.hints_checked = set()  # local variable
        self.checked_hints = set()  # server variable
        self.beedle_items_purchased = [0, 0, 0, 0]  # slots from left to right

        self.ingame_client_messages: list[tuple[float, str]] = []
        self.text_buffer_address: int = 0x0 # will be read from the dol when connected

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
        self.len_give_item_array: int = 0x1  # TODO CHANGE TO 0x10 WHEN GAME IS FIXED

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
            self.items_rcvd = []
            self.last_rcvd_index = -1
            self.locations_for_hint = args["slot_data"]["locations_for_hint"]
            if "death_link" in args["slot_data"]:
                Utils.async_start(
                    self.update_death_link(bool(args["slot_data"]["death_link"]))
                )
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(
                self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}])
            )
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_rcvd.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_rcvd.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
                if visited_stages_key in requested_keys_dict:
                    visited_stages = requested_keys_dict[visited_stages_key]
                    # If it has not been set before, the value in the response will be `None`.
                    visited_stage_names = (
                        set() if visited_stages is None else set(visited_stages.keys())
                    )
                    # If the current stage name is not in the set, send a message to update the dictionary on the
                    # server.
                    current_stage_name = self.current_stage_name
                    if (
                        current_stage_name
                        and current_stage_name not in visited_stage_names
                    ):
                        visited_stage_names.add(current_stage_name)
                        Utils.async_start(
                            self.update_visited_stages(current_stage_name)
                        )
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
        Initialize the GUI for SS client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago Skyward Sword Client"
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
                        "operations": [
                            {
                                "operation": "update",
                                "value": {newly_visited_stage_name: True},
                            }
                        ],
                    }
                ]
            )

    def forward_client_message(self, msg: str):
        lines = []
        for raw_line in msg.split("\n"):
            lines.extend(
                textwrap.wrap(
                    raw_line,
                    INGAME_LINE_LENGTH,
                )
            )

        timestamp = time.time()
        # We want to stagger the messages so large amounts of text can "scroll"
        # if they go over the character limit
        for line in lines:
            self.ingame_client_messages.append(
                (timestamp + len(self.ingame_client_messages) * 0.5, line)
            )

    def show_messages_ingame(self) -> None:
        # Filter out old messages
        line_list = []
        filtered_msgs = []
        curr_timestamp = time.time()
        for tup in self.ingame_client_messages:
            if curr_timestamp - tup[0] > CLIENT_TEXT_TIMEOUT:
                continue

            filtered_msgs.append(tup)
            line_list.append(tup[1])

        self.ingame_client_messages = filtered_msgs

        if len(line_list) == 0:
            self.write_string_to_buffer("")
        else:
            # Want to cap it at 16 lines so the text doesn't get too obtrusive
            # (which could happen if each line is quite short)
            self.write_string_to_buffer("\n".join(line_list[:16]))

    def on_print_json(self, args: dict):
        # Don't show messages in-game for item sends irrelevant to this slot
        if not self.is_uninteresting_item_send(args):
            self.forward_client_message(
                self.rawjsontotextparser(copy.deepcopy(args["data"]))
            )

        super().on_print_json(args)
    
    def write_string_to_buffer(self, text: str):
        if self.text_buffer_address != 0x0:
            # Truncate text to fit in the buffer, then write to buffer
            text_bytes = text.encode("utf-8")[: CLIENT_TEXT_BUFFER_SIZE - 1].ljust(
                CLIENT_TEXT_BUFFER_SIZE, b"\x00"
            )
            dolphin_memory_engine.write_bytes(self.text_buffer_address, text_bytes)


def dme_read_byte(console_address: int) -> int:
    """
    Read 1 byte from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return dolphin_memory_engine.read_byte(console_address)


def dme_write_byte(console_address: int, value: bytes) -> None:
    """
    Write 1 byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dolphin_memory_engine.write_byte(console_address, value)


def dme_read_short(console_address: int) -> int:
    """
    Read a 2-byte short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(
        dolphin_memory_engine.read_bytes(console_address, 2), byteorder="big"
    )

def dme_read_long(console_address: int) -> int:
    """
    Read a 4-byte long from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(
        dolphin_memory_engine.read_bytes(console_address, 4), byteorder="big"
    )


def dme_write_short(console_address: int, value: int) -> None:
    """
    Write a 2-byte short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(2, byteorder="big")
    )


def dme_read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return (
        dolphin_memory_engine.read_bytes(console_address, strlen)
        .split(b"\0", 1)[0]
        .decode()
    )

def dme_read_slot() -> str:
    """
    Read the slot name from dolphin memory.
    Slot name is 16 bytes, offset 20 bytes from the AP array.
    Slot name is encoded in UTF-8.

    :return: The string containing the slot name.
    """
    slot_bytes = dolphin_memory_engine.read_bytes(ARCHIPELAGO_ARRAY_ADDR + 0x14, 0x10)
    slot_bytes = slot_bytes.replace(b"\xFF", b"")

    return slot_bytes.decode("utf-8")



def _give_death(ctx: SSContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: The SS client context.
    """
    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame(get_link_ptr())
        and not check_in_minigame()
    ):
        ctx.has_send_death = True
        dme_write_short(CURR_HEALTH_ADDR, 0)


async def _give_item(ctx: SSContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The SS client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not can_receive_items(ctx):
        return False

    item_id = ITEM_TABLE[item_name].item_id  # In game item ID

    # Loop through the item array, placing the item in an empty slot (0xFF).
    for idx in range(ctx.len_give_item_array):
        slot = dme_read_byte(ARCHIPELAGO_ARRAY_ADDR + idx)
        if slot == 0xFF:
            # logger.info(f"DEBUG: Gave item {item_id} to player {ctx.player_names[ctx.slot]}.")
            dme_write_byte(ARCHIPELAGO_ARRAY_ADDR + idx, item_id)
            await asyncio.sleep(0.25)
            # If this happens, this may be an indicator that the player interrupted the itemget with something like a Fi call
            # or bed which could delete the item, so we should check for a reload
            while is_link_not_in_action(get_link_ptr(), [ITEM_GET_ACTION]):
                await asyncio.sleep(0.1)
                # While the client won't initiate an item send while the player is swimming, the player
                # can still receive items underwater if they're sent one just before entering the water.
                # The patched game *will* still give them the item, but it won't put them in the item action,
                # so we shouldn't resend the item, or else it will be duplicated.
                if is_link_in_action(get_link_ptr(), SWIM_ACTIONS):
                    break
                # If state is 0, that means a reload occurred, so we should resend the item.
                # However, we shouldn't resend the item if the user immediately enters the item get action anyway
                # (which can happen if this reload occurs due to a door, in which case the original item will still be received)
                if not check_ingame(get_link_ptr()):
                    # Reset the value at this array index to 0, to avoid duplicating the item if it was never read in the first place
                    dme_write_byte(ARCHIPELAGO_ARRAY_ADDR + idx, 0xFF)
                    debug_text = f"DEBUG: A reload deleted {ctx.player_names[ctx.slot]}'s {item_name} (ID {item_id}). Resending the item..."
                    logger.info(debug_text)
                    ctx.forward_client_message(debug_text)
                    return False
            return True

    # If unable to place the item in the array, return False.
    return False


async def give_items(ctx: SSContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: The SS client context.
    """
    if can_receive_items(ctx):
        # Read the expected index of the player, which is the index of the latest item they've received.
        expected_idx = dme_read_short(EXPECTED_INDEX_ADDR)

        # Loop through items to give.
        for item, idx in ctx.items_rcvd:
            # If the item's index is greater than the player's expected index, give the player the item.
            if expected_idx <= idx:
                # Attempt to give the item and increment the expected index.
                while not await _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                    await asyncio.sleep(0.25)

                # Increment the expected index.
                dme_write_short(EXPECTED_INDEX_ADDR, idx + 1)


async def check_locations(ctx: SSContext) -> None:
    """
    Loops through all locations and checks the sceneflag/storyflag(s) associated with the location in the location table.

    If Hylia's Realm - Defeat Demise is checked, update the server that this player has beaten the game.
    Otherwise, send the list of checked locations to the server.

    :param ctx: The SS client context.
    """
    # Don't send locations from the title screen (BiT)
    if can_send_items():
        # Loop through all locations to see if each has been checked.
        for location, data in LOCATION_TABLE.items():
            checked = False
            [flag_type, flag_bit, flag_value, addr] = data.checked_flag
            if flag_type == SSLocCheckedFlag.STORY:
                flag = dme_read_byte(addr + flag_bit)
                checked = bool(flag & flag_value)
            elif flag_type == SSLocCheckedFlag.SCENE:
                flag = dme_read_byte(STAGE_TO_SCENEFLAG_ADDR[addr] + flag_bit)
                checked = bool(flag & flag_value)
            elif flag_type == SSLocCheckedFlag.SPECL:
                if location == "Upper Skyloft - Ghost/Pipit's Crystals":
                    flag1 = bool(dme_read_byte(0x805A9B16) & 0x80)  # 5 crystals from Pipit
                    flag2 = bool(dme_read_byte(0x805A9B16) & 0x04)  # 5 crystals from Ghost
                    checked = flag1 or flag2
                if location == "Central Skyloft - Peater/Peatrice's Crystals":
                    flag1 = bool(
                        dme_read_byte(0x805A9B1A) & 0x40
                    )  # 5 crystals from Peatrice
                    flag2 = bool(dme_read_byte(0x805A9B1D) & 0x02)  # 5 crystals from Peater
                    checked = flag1 or flag2

            if checked:
                if data.code is None:  # Defeat Demise
                    if not ctx.finished_game:
                        await ctx.send_msgs(
                            [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                        )
                        ctx.finished_game = True
                else:
                    ctx.locations_checked.add(SSLocation.get_apid(data.code))
                    for slot, checks in enumerate(BEEDLE_CHECKS):
                        if ctx.beedle_items_purchased[slot] < len(BEEDLE_CHECKS[slot]) - 1:
                            ctx.beedle_items_purchased[slot] += (data.code == checks[ctx.beedle_items_purchased[slot]])
                            
        
        for hint, data in HINT_TABLE.items():
            [flag_bit, flag_value, addr] = data.checked_flag
            # All hint flags are story flags
            flag = dme_read_byte(addr + flag_bit)
            checked = bool(flag & flag_value)

            if checked or ctx.finished_game:
                for locname in ctx.locations_for_hint.get(hint, []):
                    ctx.hints_checked.add(SSLocation.get_apid(LOCATION_TABLE[locname].code))

        # Send the list of newly-checked locations & hints to the server.
        locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
        hints_checked = ctx.hints_checked.difference(ctx.checked_hints)
        if locations_checked:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}]) 
        if hints_checked:
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": hints_checked, "create_as_hint": 2}])

        ctx.checked_hints |= hints_checked


async def check_current_stage_changed(ctx: SSContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The SS client context.
    """
    new_stage_name = dme_read_string(CURR_STAGE_ADDR, 16)

    current_stage_name = ctx.current_stage_name

    if new_stage_name != current_stage_name:
        if new_stage_name == BEEDLE_STAGE:
            await scout_beedle_checks(ctx)
        ctx.current_stage_name = new_stage_name
        # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
        data_to_send = {"ss_stage_name": new_stage_name}
        message = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": data_to_send,
        }
        await ctx.send_msgs([message])

        # If the stage has never been visited before, update the server's data storage to indicate that it has been
        # visited.
        visited_stage_names = ctx.visited_stage_names
        if (
            visited_stage_names is not None
            and new_stage_name not in visited_stage_names
        ):
            visited_stage_names.add(new_stage_name)
            await ctx.update_visited_stages(new_stage_name)

async def scout_beedle_checks(ctx: SSContext) -> None:
    locs_to_scout = set()
    for slot, purchased_idx in enumerate(ctx.beedle_items_purchased):
        if len(BEEDLE_CHECKS[slot]) > purchased_idx:
            locs_to_scout.add(SSLocation.get_apid(BEEDLE_CHECKS[slot][purchased_idx]))
    
    await ctx.send_msgs([{"cmd": "LocationScouts", "locations": locs_to_scout, "create_as_hint": 2}]) 

def check_alive() -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = dme_read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: SSContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and check_ingame(get_link_ptr()) and not check_on_title_screen():
        cur_health = dme_read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False

def check_ingame(link_ptr: int) -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    if link_ptr == 0x0:
        return False
    return int.from_bytes(get_link_state(link_ptr)) != 0x0

def check_on_title_screen() -> bool:
    """
    Check if the player is on the Title Screen.
    
    :return: `True` if the player is on the title screen, otherwise `False`.
    """
    return dme_read_byte(GLOBAL_TITLE_LOADER_ADDR) != 0x0

def check_in_minigame() -> bool:
    """
    Check if the player is in a minigame.
    
    :return: `True` if the player is in a minigame, false if not.
    """
    return dme_read_byte(MINIGAME_STATE_ADDR) == 0x0

def get_link_ptr() -> int:
    return dolphin_memory_engine.read_word(LINK_PTR)

def get_link_state(link_ptr: int) -> bytes:
    return dolphin_memory_engine.read_bytes(link_ptr + CURR_STATE_OFFSET, 3)

def get_link_action(link_ptr: int) -> int:
    return dme_read_byte(link_ptr + LINK_ACTION_OFFSET)

def validate_link_state(link_ptr: int) -> bool:
    """
    Returns a bool determining whether Link is in a valid or invalid state to receive items.

    :return: True if Link is in a valid state, False if Link is in an invalid state
    """
    if link_ptr == 0x0 or get_link_state(link_ptr) in LINK_INVALID_STATES:
        return False
    else:
        return True

def validate_link_action(link_ptr: int) -> bool:
    """
    Returns a bool determining if Link is in a safe action to receive items.

    :return: True if Link is in a safe action, False if Link is not in a safe action.
    """
    if link_ptr == 0x0:
        return False
    action = dme_read_byte(link_ptr + LINK_ACTION_OFFSET)
    return action <= MAX_SAFE_ACTION

def is_link_not_in_action(link_ptr: int, actions: List[int]) -> bool:
    if link_ptr == 0x0:
        return True

    return get_link_action(link_ptr) not in actions

def is_link_in_action(link_ptr: int, actions: List[int]) -> bool:
    if link_ptr == 0x0:
        return False

    return get_link_action(link_ptr) in actions

def check_on_file_1() -> bool:
    """
    Returns a bool determining if the player is currently on File 1.

    :return: True if File 1 last selected, False otherwise
    """
    file = dme_read_byte(SELECTED_FILE_ADDR)
    return file == 0x0

def can_receive_items(ctx: SSContext) -> bool:
    """
    Link must be on File 1 in a valid state and action and not on the title screen to receive items.
    """

    link_ptr = get_link_ptr()
    return (
        link_ptr != 0x0
        and can_send_items()
        and check_alive()
        and validate_link_state(link_ptr)
        and validate_link_action(link_ptr)
        and not check_in_minigame()
        and ctx.current_stage_name != DEMISE_STAGE
    )

def can_send_items() -> bool:
    """
    Link must be on File 1 and not on the tile screen to send items.
    """
    return (not check_on_title_screen()) and check_on_file_1()


async def dolphin_sync_task(ctx: SSContext) -> None:
    """
    Manages the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The SS client context.
    """
    logger.info("Connecting to Dolphin. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if (
                dolphin_memory_engine.is_hooked()
                and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            ):
                ctx.show_messages_ingame()
                if not check_ingame(get_link_ptr()):
                    # Reset the give item array while not in the game.
                    # dolphin_memory_engine.write_bytes(ARCHIPELAGO_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = dme_read_slot()
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
                    if dme_read_string(0x80000000, 6) != "SOUE01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                        ctx.text_buffer_address = dme_read_long(CLIENT_TEXT_BUFFER_PTR)
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
                "Connection to Dolphin failed, attempting again in 5 seconds..."
            )
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the SS client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Skyward Sword Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = SSContext(connect, password)
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

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)

