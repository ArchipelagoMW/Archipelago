import asyncio
import copy
from dataclasses import dataclass
import time
import traceback
import textwrap
import socket
import struct
import threading
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
from .Cubes import cubes_table
from .SSClientUtils import *

if TYPE_CHECKING:
    import kvui

class AsyncUDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, client):
        self.client: AsyncWiiMemoryClient = client
        
    def datagram_received(self, data, addr):
        self.client.handle_response(data)
    
    def error_received(self, exc):
        print(f"UDP error: {exc}")
        self.client.established = False

class CommandRequest:
    def __init__(self, command: bytes, timeout: float = 10.0):
        self.command = command
        self.timeout = timeout
        self.future = asyncio.Future()
        self.timestamp = time.time()

class AsyncWiiMemoryClient:
    def __init__(self, wii_ip, port=43673):
        self.wii_ip = wii_ip
        self.port = port
        self.transport = None
        self.protocol = None
        self.established = False
        
        # Queue for UDP queries to the wii
        self.command_queue = asyncio.Queue()
        self.current_request: Optional[CommandRequest] = None
        self.queue_processor_task = None
        
    async def connect(self):
        """Establish connection to Wii"""
        try:
            loop = asyncio.get_event_loop()
            self.transport, self.protocol = await loop.create_datagram_endpoint(
                lambda: AsyncUDPProtocol(self),
                remote_addr=(self.wii_ip, self.port)
            )
            sock = self.transport.get_extra_info('socket')
            self.my_ip = sock.getsockname()[0]
            self.my_port = sock.getsockname()[1]

            self.queue_processor_task = asyncio.create_task(self._process_command_queue())
            
            # Send IP / port info so the Wii can write back
            try:
                await self.establish_connection()
                self.established = True
                return True
            except asyncio.TimeoutError:
                self.established = False
                return False
                
        except Exception as e:
            print(f"Connection failed: {e}")
            self.established = False
            return False

    async def disconnect(self):
        if self.queue_processor_task:
            self.queue_processor_task.cancel()
            try:
                await self.queue_processor_task
            except asyncio.CancelledError:
                pass
        
        if self.transport:
            self.transport.close()
            
        self.established = False

    async def establish_connection(self, timeout=1):
        """Try to send a packet with IP and Port to establish connection to Wii server"""
        command = b'\x00' + socket.inet_aton(self.my_ip) + struct.pack('>H', self.my_port)
        
        response = await self._send_command_queued(command, timeout)
        
        if len(response) > 0:
            return True
        else:
            raise Exception(f"Establishing UDP connection failed")
    
    async def _send_command_queued(self, command: bytes, timeout=2):
        """Queue up command to read/write to console"""
            
        request = CommandRequest(command, timeout)
        await self.command_queue.put(request)
        
        try:
            # Wait for wii's response
            response = await asyncio.wait_for(request.future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            print(f"Command {command} timed out")
            self.established = False
            raise

    async def _process_command_queue(self):
        """Process commands from queue with rate limiting"""
        while True:
            try:
                request = await self.command_queue.get()
                
                # Send command to wii
                if self.transport and not request.future.cancelled():
                    self.current_request = request
                    self.transport.sendto(request.command)
                    
                    asyncio.create_task(self._handle_request_timeout(request))
                elif request.future and not request.future.cancelled():
                    # Connection lost, cancel the request
                    request.future.set_exception(ConnectionError("Not connected"))
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in command queue: {e}")
                if self.current_request and not self.current_request.future.cancelled():
                    self.current_request.future.set_exception(e)

    async def _handle_request_timeout(self, request: CommandRequest):
        """Handle timeout for a specific request"""
        try:
            await asyncio.sleep(request.timeout)
            if self.current_request == request and not request.future.done():
                request.future.set_exception(asyncio.TimeoutError())
                self.current_request = None
        except asyncio.CancelledError:
            pass

    def handle_response(self, data):
        """Handle incoming UDP response"""
        if self.current_request and not self.current_request.future.done():
            self.current_request.future.set_result(data)
            self.current_request = None
        else:
            print(f"Received unexpected response: {data}")

    async def read_bytes(self, address, length, timeout=2):
        """Read bytes from memory address"""
        command = struct.pack('>BII', 0x01, address, length)  # READ - 0x01
        # The wii will validate that this sum mod 256 is correct
        checksum = sum(command) & 0xFF
        command += checksum.to_bytes(1, 'big')
        
        response = await self._send_command_queued(command, timeout)
        
        if len(response) == length:
            return response
        else:
            raise Exception(f"Read failed at address 0x{address:08x}")
    
    async def write_bytes(self, address, data, timeout=2):
        """Write bytes to memory address"""
        command = struct.pack('>BII', 0x02, address, len(data)) + data  # WRITE - 0x02
        # The wii will validate that this sum mod 256 is correct
        checksum = sum(command) & 0xFF
        command += checksum.to_bytes(1, 'big')
        
        response = await self._send_command_queued(command, timeout)
        
        if len(response) == 1:
            return True
        else:
            raise Exception(f"Write failed at address 0x{address:08x}")
    
    async def signal_dc(self, timeout=2) -> bytes:
        """Send a signal to the Wii that the client lost connection"""
        command = struct.pack('>B', 0x05)  # DISCONNECT - 0x05
        
        response = await self._send_command_queued(command, timeout)
        
        if len(response) > 0:
            return response
        else:
            raise Exception(f"Read failed at address")
    
    def close(self):
        """Close connection"""
        self.established = False
        if self.transport:
            self.transport.close()
            self.transport = None

@dataclass
class BatchFlagHandler:
    flags: bytes
    base_addr: int
    def lookup_byte(self, addr: int) -> int:
        offset = addr - self.base_addr
        assert(offset >= 0)
        return self.flags[offset]

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
        Switch to Dolphin mode and display the current Dolphin emulator connection status.
        """
        if isinstance(self.ctx, SSContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")
            if self.ctx.is_hooked() and self.ctx.on_console:
                self.ctx.wii_memory_client.close()
            self.ctx.on_console = False
    
    def _cmd_console(self, ip_addr: str) -> None:
        """
        Switch to console mode, connecting to a UDP server on a Wii (must be on the same network)
        """
        if isinstance(self.ctx, SSContext):
            logger.info(f"Starting up a Wii client...")
            self.ctx.wii_ip = ip_addr
            if self.ctx.is_hooked() and not self.ctx.on_console:
                # Re-display network info again (for testing things on dolphin)
                dolphin_memory_engine.write_bytes(NETWORK_USAGE_BOOL, b'\x01')
                dolphin_memory_engine.un_hook()
            self.ctx.on_console = True
            self.ctx.start_wii_client(ip_addr)
            
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
        self.sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_rcvd_index: int = -1
        self.has_send_death: bool = False
        self.locations_for_hint: dict[str, list] = {}
        self.lost_client_connection: bool = False

        self.hints_checked = set()  # local variable
        self.checked_hints = set()  # server variable
        self.beedle_items_purchased = [0, 0, 0, 0]  # slots from left to right
        self.cubes_checked = set() #local variable
        
        self.ingame_client_messages: list[tuple[float, str]] = []
        self.text_buffer_address: int = 0x0 # will be read from the dol when connected
        self.link_ptr: int = 0x0 # will be read from the dol when connected
        self.link_state: bytes = b'\x00\x00\x00'
        self.link_action: int = 0
        self.on_console: bool = False
        self.wii_memory_client: AsyncWiiMemoryClient = None
        self.wii_ip: str = "0.0.0.0"
        self.socket = None # Server socket
        self.client_socket = None # Connection from Wii

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
            logger.info("Awaiting connection to the game to get player information.")
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
        asyncio.create_task(self._give_death())

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

    async def show_messages_ingame(self) -> None:
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
            await self.write_string_to_buffer("")
        else:
            # Want to cap it at 16 lines so the text doesn't get too obtrusive
            # (which could happen if each line is quite short)
            await self.write_string_to_buffer("\n".join(line_list[:16]))

    def on_print_json(self, args: dict):
        # Don't show messages in-game for item sends irrelevant to this slot
        if not self.is_uninteresting_item_send(args):
            self.forward_client_message(
                self.rawjsontotextparser(copy.deepcopy(args["data"]))
            )

        super().on_print_json(args)
    
    async def write_string_to_buffer(self, text: str):
        if self.text_buffer_address != 0x0:
            # Truncate text to fit in the buffer, then write to buffer
            text_bytes = text.encode("utf-8")[: CLIENT_TEXT_BUFFER_SIZE - 1].ljust(
                CLIENT_TEXT_BUFFER_SIZE, b"\x00"
            )
            await self.write_bytes(self.text_buffer_address, text_bytes)
    
    def start_wii_client(self, ip):
        """Initialize the async Wii client"""
        if self.wii_memory_client:
            self.wii_memory_client.close()
        self.wii_memory_client = AsyncWiiMemoryClient(ip)
    
    def close_wii_client(self):
        """Close Wii client connection"""
        if self.wii_memory_client:
            if self.wii_memory_client.established:
                self.wii_memory_client.signal_dc()
            self.wii_memory_client.close()
            self.wii_memory_client = None
    
    def is_hooked(self):
        if self.on_console:
            return self.wii_memory_client and self.wii_memory_client.established
        
        return dolphin_memory_engine.is_hooked() and self.dolphin_status == CONNECTION_CONNECTED_STATUS

    async def read_bytes(self, console_address: int, num_bytes: int) -> bytes:
        """
        Read bytes from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        if self.on_console:
            return await self.wii_memory_client.read_bytes(console_address, num_bytes)

        return dolphin_memory_engine.read_bytes(console_address, num_bytes)
    
    async def write_bytes(self, console_address: int, to_write: bytes):
        """
        Write bytes to the game's memory

        :param console_address: Address to write to.
        :param to_write: Bytes to write
        """
        if self.on_console:
            await self.wii_memory_client.write_bytes(console_address, to_write)
            return
            
        dolphin_memory_engine.write_bytes(console_address, to_write)

    async def read_byte(self, console_address: int) -> int:
        """
        Read 1 byte from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        bytes = await self.read_bytes(console_address, 1)
        return int.from_bytes(bytes, byteorder='big')

    async def read_short(self, console_address: int) -> int:
        """
        Read a 2-byte short from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        bytes = await self.read_bytes(console_address, 2)
        return int.from_bytes(bytes, byteorder='big')

    async def read_long(self, console_address: int) -> int:
        """
        Read a 4-byte long from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        bytes = await self.read_bytes(console_address, 4)
        return int.from_bytes(bytes, byteorder='big')
    
    async def write_byte(self, console_address: int, value: int) -> None:
        """
        Write a byte to the game's memory

        :param console_address: Address to write to.
        :param value: Value to write.
        """
        await self.write_bytes(
            console_address, value.to_bytes(1, byteorder="big")
        )
    
    async def write_short(self, console_address: int, value: int) -> None:
        """
        Write a 2-byte short to the game's memory

        :param console_address: Address to write to.
        :param value: Value to write.
        """
        await self.write_bytes(
            console_address, value.to_bytes(2, byteorder="big")
        )
    
    async def read_string(self, console_address: int, strlen: int) -> str:
        """
        Read a string from the game's memory.

        :param console_address: Address to start reading from.
        :param strlen: Length of the string to read.
        :return: The string.
        """
        strbytes = await self.read_bytes(console_address, strlen)
        return (
            strbytes
            .split(b"\0", 1)[0]
            .decode()
        )
    
    async def read_slot(self) -> str:
        """
        Read the slot name from the game's memory
        Slot name is 16 bytes, offset 20 bytes from the AP array.
        Slot name is encoded in UTF-8.

        :return: The string containing the slot name.
        """
        slot_bytes = await self.read_bytes(ARCHIPELAGO_ARRAY_ADDR + 0x14, 0x10)
        slot_bytes = slot_bytes.replace(b"\xFF", b"")

        return slot_bytes.decode("utf-8")

    async def read_scene_flags(self) -> bytes:
        """
        Read bytes from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        if self.on_console:
            res_bytes = bytes()
            for i in range(13):
                res_bytes += await self.wii_memory_client.read_bytes(SCENEFLAG_START_ADDR + 32 * i, 32)
            return res_bytes

        return dolphin_memory_engine.read_bytes(SCENEFLAG_START_ADDR, 416)

    async def read_story_flags(self) -> bytes:
        """
        Read bytes from the game's memory

        :param console_address: Address to read from.
        :return: The value read from memory.
        """
        if self.on_console:
            res_bytes = bytes()
            for i in range(8):
                res_bytes += await self.wii_memory_client.read_bytes(STORYFLAG_START_ADDR + 32 * i, 32)
            return res_bytes

        return dolphin_memory_engine.read_bytes(STORYFLAG_START_ADDR, 256)

    async def _give_death(self) -> None:
        """
        Trigger the player's death in-game by setting their current health to zero.
        """
        if (
            self.slot is not None
            and self.is_hooked()
            and self.check_ingame()
            and not await self.check_in_minigame()
        ):
            self.has_send_death = True
            await self.write_short(CURR_HEALTH_ADDR, 0)


    async def _give_item(self, item_name: str) -> bool:
        """
        Give an item to the player in-game.

        :param ctx: The SS client context.
        :param item_name: Name of the item to give.
        :return: Whether the item was successfully given.
        """
        if not await self.can_receive_items():
            return False

        item_id = ITEM_TABLE[item_name].item_id  # In game item ID

        # Loop through the item array, placing the item in an empty slot (0xFF).
        for idx in range(self.len_give_item_array):
            slot = await self.read_byte(ARCHIPELAGO_ARRAY_ADDR + idx)
            if slot == 0xFF:
                # logger.info(f"DEBUG: Gave item {item_id} to player {ctx.player_names[ctx.slot]}.")
                await self.write_byte(ARCHIPELAGO_ARRAY_ADDR + idx, item_id)
                await asyncio.sleep(0.25)
                await self.cache_link_data() # Recalculate State & Action
                # If this happens, this may be an indicator that the player interrupted the itemget with something like a Fi call
                # or bed which could delete the item, so we should check for a reload
                while self.is_link_not_in_action([ITEM_GET_ACTION]):
                    await asyncio.sleep(0.2)
                    await self.cache_link_data() # Recalculate State & Action
                    # While the client won't initiate an item send while the player is swimming, the player
                    # can still receive items underwater if they're sent one just before entering the water.
                    # The patched game *will* still give them the item, but it won't put them in the item action,
                    # so we shouldn't resend the item, or else it will be duplicated.
                    if self.is_link_in_action(SWIM_ACTIONS):
                        break
                    # If state is 0, that means a reload occurred, so we should resend the item.
                    # However, we shouldn't resend the item if the user immediately enters the item get action anyway
                    # (which can happen if this reload occurs due to a door, in which case the original item will still be received)
                    if not self.check_ingame():
                        # Reset the value at this array index to 0, to avoid duplicating the item if it was never read in the first place
                        await self.write_byte(ARCHIPELAGO_ARRAY_ADDR + idx, 0xFF)
                        debug_text = f"DEBUG: A reload deleted {self.player_names[self.slot]}'s {item_name} (ID {item_id}). Resending the item..."
                        logger.info(debug_text)
                        self.forward_client_message(debug_text)
                        return False
                return True

        # If unable to place the item in the array, return False.
        return False


    async def give_items(self) -> None:
        """
        Give the player all outstanding items they have yet to receive.

        :param ctx: The SS client context.
        """
        if await self.can_receive_items():
            # Read the expected index of the player, which is the index of the latest item they've received.
            expected_idx = await self.read_short(EXPECTED_INDEX_ADDR)

            # Loop through items to give.
            for item, idx in self.items_rcvd:
                # If the item's index is greater than the player's expected index, give the player the item.
                if expected_idx <= idx:
                    # Attempt to give the item and increment the expected index.
                    while not await self._give_item(LOOKUP_ID_TO_NAME[item.item]):
                        await asyncio.sleep(0.25)
                        await self.cache_link_data()

                    # Increment the expected index.
                    await self.write_short(EXPECTED_INDEX_ADDR, idx + 1)


    async def check_locations(self) -> None:
        """
        Loops through all locations and checks the sceneflag/storyflag(s) associated with the location in the location table.

        If Hylia's Realm - Defeat Demise is checked, update the server that this player has beaten the game.
        Otherwise, send the list of checked locations to the server.

        :param ctx: The SS client context.
        """
        # Don't send locations from the title screen (BiT)
        if await self.can_send_items():
            storyflags = BatchFlagHandler(await self.read_story_flags(), STORYFLAG_START_ADDR)
            sceneflags = BatchFlagHandler(await self.read_scene_flags(), SCENEFLAG_START_ADDR)
            # Loop through all locations to see if each has been checked.
            for location, data in LOCATION_TABLE.items():
                checked = False
                [flag_type, flag_bit, flag_value, addr] = data.checked_flag
                if flag_type == SSLocCheckedFlag.STORY:
                    flag = storyflags.lookup_byte(addr + flag_bit)
                    checked = bool(flag & flag_value)
                elif flag_type == SSLocCheckedFlag.SCENE:
                    flag = sceneflags.lookup_byte(STAGE_TO_SCENEFLAG_ADDR[addr] + flag_bit)
                    checked = bool(flag & flag_value)
                elif flag_type == SSLocCheckedFlag.SPECL:
                    if location == "Upper Skyloft - Ghost/Pipit's Crystals":
                        byte = await self.read_byte(0x805A9B16)
                        flag1 = bool(byte & 0x80)  # 5 crystals from Pipit
                        flag2 = bool(byte & 0x04)  # 5 crystals from Ghost
                        checked = flag1 or flag2
                    if location == "Central Skyloft - Peater/Peatrice's Crystals":
                        bytelong = await self.read_long(0x805A9B1A)
                        flag1 = bool(
                            bytelong & 0x40000000
                        )  # 5 crystals from Peatrice
                        flag2 = bool(bytelong & 0x02)  # 5 crystals from Peater
                        checked = flag1 or flag2

                if checked:
                    if data.code is None:  # Defeat Demise
                        if not self.finished_game:
                            await self.send_msgs(
                                [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                            )
                            self.finished_game = True
                    else:
                        self.locations_checked.add(SSLocation.get_apid(data.code))
                        for slot, checks in enumerate(BEEDLE_CHECKS):
                            if self.beedle_items_purchased[slot] < len(BEEDLE_CHECKS[slot]) - 1:
                                self.beedle_items_purchased[slot] += (data.code == checks[self.beedle_items_purchased[slot]])
                                
            
            for hint, data in HINT_TABLE.items():
                [flag_bit, flag_value, addr] = data.checked_flag
                # All hint flags are story flags
                flag = storyflags.lookup_byte(addr + flag_bit)
                checked = bool(flag & flag_value)

                if checked or self.finished_game:
                    for locname in self.locations_for_hint.get(hint, []):
                        self.hints_checked.add(SSLocation.get_apid(LOCATION_TABLE[locname].code))

            for i, (name, (flag_bit, flag_value, addr)) in enumerate(cubes_table):
                flag = storyflags.lookup_byte(addr + flag_bit)
                checked = bool(flag & flag_value)

                if checked and i not in self.cubes_checked:
                    self.cubes_checked.add(i)

                    bit = 1 << i
                    await self.send_msgs([{
                        "cmd": "Set",
                        "key": f"skyward_sword_cubes_{self.team}_{self.slot}",
                        "default": 0,
                        "want_reply": True,
                        "operations": [{"operation": "or", "value": bit}],
                    }])

            # Send the list of newly-checked locations & hints to the server.
            locations_checked = self.locations_checked.difference(self.checked_locations)
            hints_checked = self.hints_checked.difference(self.checked_hints)
            if locations_checked:
                await self.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}]) 
            if hints_checked:
                await self.send_msgs([{"cmd": "LocationScouts", "locations": hints_checked, "create_as_hint": 2}])

            self.checked_hints |= hints_checked


    async def check_current_stage_changed(self) -> None:
        """
        Check if the player has moved to a new stage.
        If so, update all trackers with the new stage name.
        If the stage has never been visited, additionally update the server.

        :param ctx: The SS client context.
        """
        new_stage_name = await self.read_string(CURR_STAGE_ADDR, 16)

        current_stage_name = self.current_stage_name

        if new_stage_name != current_stage_name:
            if new_stage_name == BEEDLE_STAGE:
                await self.scout_beedle_checks()
            self.current_stage_name = new_stage_name
            # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
            data_to_send = {"ss_stage_name": new_stage_name}
            message = {
                "cmd": "Bounce",
                "slots": [self.slot],
                "data": data_to_send,
            }
            await self.send_msgs([message])

            # If the stage has never been visited before, update the server's data storage to indicate that it has been
            # visited.
            visited_stage_names = self.visited_stage_names
            if (
                visited_stage_names is not None
                and new_stage_name not in visited_stage_names
            ):
                visited_stage_names.add(new_stage_name)
                await self.update_visited_stages(new_stage_name)

    async def scout_beedle_checks(self) -> None:
        locs_to_scout = set()
        for slot, purchased_idx in enumerate(self.beedle_items_purchased):
            if len(BEEDLE_CHECKS[slot]) > purchased_idx:
                locs_to_scout.add(SSLocation.get_apid(BEEDLE_CHECKS[slot][purchased_idx]))
        
        await self.send_msgs([{"cmd": "LocationScouts", "locations": locs_to_scout, "create_as_hint": 2}]) 

    async def check_alive(self) -> bool:
        """
        Check if the player is currently alive in-game.

        :return: `True` if the player is alive, otherwise `False`.
        """
        cur_health = await self.read_short(CURR_HEALTH_ADDR)
        return cur_health > 0


    async def check_death(self) -> None:
        """
        Check if the player is currently dead in-game.
        If DeathLink is on, notify the server of the player's death.

        :return: `True` if the player is dead, otherwise `False`.
        """
        if self.slot is not None and self.check_ingame() and not await self.check_on_title_screen():
            cur_health = await self.read_short(CURR_HEALTH_ADDR)
            if cur_health <= 0:
                if not self.has_send_death and time.time() >= self.last_death_link + 3:
                    self.has_send_death = True
                    await self.send_death(self.player_names[self.slot] + " ran out of hearts.")
            else:
                self.has_send_death = False

    def check_ingame(self) -> bool:
        """
        Check if the player is currently in-game.

        :return: `True` if the player is in-game, otherwise `False`.
        """
        return int.from_bytes(self.link_state) != 0x0

    async def check_on_title_screen(self) -> bool:
        """
        Check if the player is on the Title Screen.
        
        :return: `True` if the player is on the title screen, otherwise `False`.
        """
        return await self.read_byte(GLOBAL_TITLE_LOADER_ADDR) != 0x0

    async def check_in_minigame(self) -> bool:
        """
        Check if the player is in a minigame.
        
        :return: `True` if the player is in a minigame, false if not.
        """
        return await self.read_byte(MINIGAME_STATE_ADDR) == 0x0
    
    async def cache_link_data(self):
        self.link_ptr = await self.read_long(LINK_PTR)
        self.link_state = await self.get_link_state()
        self.link_action = await self.get_link_action()

    async def get_link_ptr(self) -> int:
        return await self.read_long(LINK_PTR)

    async def get_link_state(self) -> bytes:
        if self.link_ptr == 0x0: return b'\x00\x00\x00'
        return await self.read_bytes(self.link_ptr + CURR_STATE_OFFSET, 3)

    async def get_link_action(self) -> int:
        if self.link_ptr == 0x0: return 0
        return await self.read_byte(self.link_ptr + LINK_ACTION_OFFSET)

    def validate_link_state(self) -> bool:
        """
        Returns a bool determining whether Link is in a valid or invalid state to receive items.

        :return: True if Link is in a valid state, False if Link is in an invalid state
        """
        if self.link_ptr == 0x0 or self.link_state in LINK_INVALID_STATES:
            return False
        else:
            return True

    def validate_link_action(self) -> bool:
        """
        Returns a bool determining if Link is in a safe action to receive items.

        :return: True if Link is in a safe action, False if Link is not in a safe action.
        """
        if self.link_ptr == 0x0:
            return False
        return self.link_action <= MAX_SAFE_ACTION

    def is_link_not_in_action(self, actions: List[int]) -> bool:
        if self.link_ptr == 0x0:
            return True

        return self.link_action not in actions

    def is_link_in_action(self, actions: List[int]) -> bool:
        if self.link_ptr == 0x0:
            return False

        return self.link_action in actions

    async def check_on_file_1(self) -> bool:
        """
        Returns a bool determining if the player is currently on File 1.

        :return: True if File 1 last selected, False otherwise
        """
        file = await self.read_byte(SELECTED_FILE_ADDR)
        return file == 0x0

    async def can_receive_items(self) -> bool:
        """
        Link must be on File 1 in a valid state and action and not on the title screen to receive items.
        """

        return (
            self.link_ptr != 0x0
            and await self.can_send_items()
            and await self.check_alive()
            and self.validate_link_state()
            and self.validate_link_action()
            and not await self.check_in_minigame()
            and self.current_stage_name != DEMISE_STAGE
        )

    async def can_send_items(self) -> bool:
        """
        Link must be on File 1 and not on the tile screen to send items.
        """
        return (not await self.check_on_title_screen()) and await self.check_on_file_1()

async def do_sync_task(ctx: SSContext) -> None:
    """
    Manages the connection to Dolphin or the game.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The SS client context.
    """
    logger.info("Connecting to Dolphin. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        if ctx.on_console:
            try:
                if ctx.is_hooked():
                    await ctx.cache_link_data()
                    await ctx.show_messages_ingame()
                    if not ctx.check_ingame():
                        await asyncio.sleep(0.1)
                        continue
                    if ctx.slot is not None:
                        if "DeathLink" in ctx.tags:
                            await ctx.check_death()
                        await ctx.give_items()
                        await ctx.check_locations()
                        await ctx.check_current_stage_changed()
                    else:
                        if not ctx.auth:
                            ctx.auth = await ctx.read_slot()
                        if ctx.awaiting_rom:
                            await ctx.server_auth()
                    await asyncio.sleep(0.1)
                else:
                    logger.info("Attempting to connect to the console...")
                    ctx.close_wii_client()
                    ctx.start_wii_client(ctx.wii_ip)
                    await ctx.wii_memory_client.connect()

                    if ctx.wii_memory_client.established:
                        logger.info(CONSOLE_CONNECTED_STATUS)
                        ctx.locations_checked = set()
                        ctx.text_buffer_address = await ctx.read_long(CLIENT_TEXT_BUFFER_PTR)
                        await ctx.cache_link_data()
                        if ctx.lost_client_connection:
                            logger.info("Attempting to reconnect to the server.")
                            await ctx.connect()
                        
                        ctx.lost_client_connection = False
                    else:
                        logger.info(
                            "Connection to console failed, attempting again in 5 seconds..."
                        )
                        await ctx.disconnect()
                        await asyncio.sleep(5)
                        continue
            except TimeoutError:
                print("Lost packet from console, attempting to reconnect...")
                ctx.close_wii_client()
                ctx.start_wii_client(ctx.wii_ip)
                if not await ctx.wii_memory_client.connect():
                    ctx.lost_client_connection = True
                    logger.info("Lost packet from console and couldn't reconnect. Attempting again in 5 seconds...")
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                else:
                    print("Reconnected successfully.")
                continue
            except Exception:
                ctx.close_wii_client()
                logger.info(
                    "Connection to console failed, attempting again in 5 seconds..."
                )
                logger.error(traceback.format_exc())
                await ctx.disconnect()
                await asyncio.sleep(5)
                continue
        else:
            try:
                if ctx.is_hooked():
                    await ctx.cache_link_data()
                    await ctx.show_messages_ingame()
                    if not ctx.check_ingame():
                        await asyncio.sleep(0.1)
                        continue
                    if ctx.slot is not None:
                        if "DeathLink" in ctx.tags:
                            await ctx.check_death()
                        await ctx.give_items()
                        await ctx.check_locations()
                        await ctx.check_current_stage_changed()
                    else:
                        if not ctx.auth:
                            ctx.auth = await ctx.read_slot()
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
                        if await ctx.read_string(0x80000000, 6) != "SOUE01":
                            logger.info(CONNECTION_REFUSED_GAME_STATUS)
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            dolphin_memory_engine.un_hook()
                            await asyncio.sleep(5)
                        else:
                            logger.info(CONNECTION_CONNECTED_STATUS)
                            ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                            ctx.locations_checked = set()
                            ctx.text_buffer_address = await ctx.read_long(CLIENT_TEXT_BUFFER_PTR)
                            await ctx.cache_link_data()
                            await ctx.write_byte(NETWORK_USAGE_BOOL, 0) # stop network messages
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

        ctx.sync_task = asyncio.create_task(
            do_sync_task(ctx), name="GameSync"
        )

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.sync_task:
            await asyncio.sleep(3)
            await ctx.sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)


