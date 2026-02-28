"""Donkey Kong 64 client for Archipelago."""

import ModuleUpdate

ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("DK64Context", exception_logger="Client")

import asyncio
import colorama
import random
import sys
import time
import traceback
import typing

from archipelago.client.common import DK64MemoryMap, create_task_log_exception, check_version, get_ap_version
from archipelago.client.emu_loader import EmuLoaderClient
from archipelago.client.items import item_ids, item_names_to_id, trap_name_to_index, trap_index_to_name
from archipelago.client.check_flag_locations import location_flag_to_name, location_name_to_flag
from archipelago.client.ap_check_ids import check_id_to_name, check_names_to_id
from CommonClient import CommonContext, get_base_parser, gui_enabled, logger, server_loop, ClientCommandProcessor
from NetUtils import ClientStatus
from randomizer.Patching.ItemRando import normalize_location_name

# Constants
MAX_DELIVER_COUNT = 10000
MAX_STRING_LENGTH = 0x20
FAST_TEXT_SPEED = 50
NORMAL_TEXT_SPEED = 130
MIN_ITEMS_FOR_SPEED_SCALING = 5
KONG_COUNT = 5
LEVEL_COUNT = 7
HINT_BITFIELD_SIZE = 5


class CreateHintsParams:
    """Parameters for creating hints."""

    def __init__(self, location_id: int, player_id: int):
        """Initialize CreateHintsParams."""
        self.location = location_id
        self.player = player_id

    def __eq__(self, other):
        """Check equality for CreateHintsParams."""
        if not isinstance(other, CreateHintsParams):
            return False
        return self.location == other.location and self.player == other.player

    def __hash__(self):
        """Hash for CreateHintsParams."""
        return hash((self.location, self.player))


class MessageDisplayHandler:
    """Handles message display modes and speeds."""

    def __init__(self, client):
        """Initialize message display handler."""
        self.client = client

    def should_display_item(self, item_data: dict, send_mode: int) -> bool:
        """Determine if an item should be displayed based on send mode."""
        if send_mode == 3:  # display_nothing
            return False
        elif send_mode == 2:  # display_only_progression
            return item_data.get("progression", False)
        elif send_mode == 1:  # display_all_items
            return True


class IceTrapHandler:
    """Handles ice trap logic and mappings."""

    # Ice trap type to fed ID mapping
    ICE_TRAP_MAPPINGS = {
        "bubble": 0x018,  # TRANSFER_ITEM_FAKEITEM
        "reverse": 0x041,  # TRANSFER_ITEM_FAKEITEM_REVERSE
        "slow": 0x040,  # TRANSFER_ITEM_FAKEITEM_SLOW
        "disable_a": 0x042,  # TRANSFER_ITEM_FAKEITEM_DISABLEA
        "disable_b": 0x043,  # TRANSFER_ITEM_FAKEITEM_DISABLEB
        "disable_z": 0x044,  # TRANSFER_ITEM_FAKEITEM_DISABLEZ
        "disable_c_up": 0x045,  # TRANSFER_ITEM_FAKEITEM_DISABLECU
        "get_out": 0x046,  # TRANSFER_ITEM_FAKEITEM_GETOUT
        "dry": 0x047,  # TRANSFER_ITEM_FAKEITEM_DRY
        "flip": 0x048,  # TRANSFER_ITEM_FAKEITEM_FLIP
        "icefloor": 0x049,  # TRANSFER_ITEM_FAKEITEM_ICEFLOOR
        "paper": 0x04A,  # TRANSFER_ITEM_FAKEITEM_PAPER
        "slip": 0x04B,  # TRANSFER_ITEM_FAKEITEM_SLIP
        "animal": 0x04C,  # TRANSFER_ITEM_FAKEITEM_ANIMAL
        "rockfall": 0x04D,  # TRANSFER_ITEM_FAKEITEM_ROCKFALL
        "disabletag": 0x04E,  # TRANSFER_ITEM_FAKEITEM_DISABLETAG
    }

    @classmethod
    async def handle_ice_trap(cls, client, count_data: dict):
        """Handle ice trap processing."""
        # Update counter
        count_struct_address = client.n64_client.read_u32(DK64MemoryMap.count_struct_pointer)
        if count_struct_address == 0:
            logger.warning("CountStruct pointer is null, cannot write ice trap data")
            return None

        address = count_struct_address + 0x012
        current_value = client.n64_client.read_u16(address)
        client.n64_client.write_u16(address, current_value + 1)

        # Trigger the actual ice trap effect
        ice_trap_type = count_data.get("ice_trap_type", "bubble")
        fed_id = cls.ICE_TRAP_MAPPINGS.get(ice_trap_type, 0x018)  # Default to bubble
        await client.writeFedData(fed_id)

        return 0x056  # TRANSFER_ITEM_HELM_HURRY_FAKEITEM


class CountStructHandler:
    """Handles CountStruct memory operations."""

    # Field offsets within CountStruct
    OFFSETS = {
        "bp_count": 0x000,
        "hint_bitfield": 0x005,
        "key_bitfield": 0x00A,
        "kong_bitfield": 0x00B,
        "crowns": 0x00C,
        "special_items": 0x00D,
        "medals": 0x00E,
        "pearls": 0x00F,
        "fairies": 0x010,
        "ice_traps": 0x012,
        "junk_items": 0x014,
        "race_coins": 0x016,
        "flag_moves": 0x018,
    }

    @classmethod
    def get_address(cls, client, field: str, offset: int = 0) -> int:
        """Get the memory address for a CountStruct field."""
        count_struct_address = client.n64_client.read_u32(DK64MemoryMap.count_struct_pointer)
        if count_struct_address == 0:
            raise ValueError("CountStruct pointer is null")

        base_offset = cls.OFFSETS.get(field)
        if base_offset is None:
            raise ValueError(f"Unknown CountStruct field: {field}")

        return count_struct_address + base_offset + offset

    @classmethod
    def validate_bounds(cls, kong: int = None, level: int = None, bit: int = None):
        """Validate kong, level, and bit bounds."""
        if kong is not None and (kong < 0 or kong >= KONG_COUNT):
            raise ValueError(f"Invalid kong: {kong} (must be 0-{KONG_COUNT - 1})")
        if level is not None and (level < 0 or level >= LEVEL_COUNT):
            raise ValueError(f"Invalid level: {level} (must be 0-{LEVEL_COUNT - 1})")
        if bit is not None and (bit < 0 or bit >= 8):
            raise ValueError(f"Invalid bit: {bit} (must be 0-7)")


class DK64Client:
    """Client for Donkey Kong 64."""

    n64_client = None
    game = None
    auth = None
    memory_pointer = None
    stop_bizhawk_spam = False
    seed_started = False
    locations_scouted = {}
    recvd_checks = {}
    pending_checks = []
    remaining_checks = []
    sent_checks = []
    item_names = None
    players = None
    _purchase_cache = {}
    ENABLE_DEATHLINK = False
    ENABLE_RINGLINK = False
    ENABLE_TAGLINK = False
    ENABLE_TRAPLINK = False
    deathlink_debounce = True
    pending_deathlink = False

    # Display and speed settings
    send_mode = 1
    current_speed = NORMAL_TEXT_SPEED
    current_map = 0

    # Hint system
    last_hint_bitfield = [0] * HINT_BITFIELD_SIZE
    sent_hints = set()
    helm_hurry_enabled = False

    # ==================== CONNECTION METHODS ====================

    async def wait_for_pj64(self):
        """Wait for emulator to connect to the game."""
        clear_waiting_message = True
        if not self.stop_bizhawk_spam:
            logger.info("Waiting on connection to emulator...")
            self.n64_client = EmuLoaderClient()
            self.stop_bizhawk_spam = True
        while True:
            try:
                emulator_connected = False

                # Try to connect to any available emulator
                if not self.n64_client.is_connected():
                    emulator_connected = self.n64_client.connect()
                else:
                    emulator_connected = True
                valid_rom = False
                if emulator_connected:
                    valid_rom = self.n64_client.validate_rom()
                    logger.info("Emulator connected, validating ROM...")

                while not valid_rom:
                    if not self.n64_client.is_connected():
                        emulator_connected = self.n64_client.connect()
                    if clear_waiting_message:
                        logger.info("Waiting on valid ROM...")
                        clear_waiting_message = False
                    await asyncio.sleep(1.0)
                    if self.n64_client.is_connected():
                        valid_rom = self.n64_client.validate_rom()

                self.stop_bizhawk_spam = False
                logger.info("Emulator Connected to ROM!")
                return
            except Exception as e:
                await asyncio.sleep(1.0)
                logger.error(f"Error connecting to emulator, retrying... {str(e)}")
                # Reset connection on error
                if self.n64_client:
                    self.n64_client.disconnect()
                pass

    # ==================== GAME STATE METHODS ====================

    def check_safe_gameplay(self):
        """Check if the game is in a valid state for sending items."""
        current_gamemode = self.n64_client.read_u8(DK64MemoryMap.CurrentGamemode)
        next_gamemode = self.n64_client.read_u8(DK64MemoryMap.NextGamemode)
        return current_gamemode in [6, 0xD] and next_gamemode in [6, 0xA, 0xD]

    def safe_to_send(self):
        """Check if it's safe to send an item."""
        countdown_value = self.n64_client.read_u8(self.memory_pointer + DK64MemoryMap.safety_text_timer)
        return countdown_value == 0

    def safe_to_send_shopkeeper(self):
        """Check if it's safe to send a shopkeeper item."""
        try:
            # First check the regular safety timer
            if not self.safe_to_send():
                return False

            # Then check if we can receive shopkeeper items (not in shops)
            can_receive = self.n64_client.read_u8(self.memory_pointer + DK64MemoryMap.can_receive_shopkeeper)
            return can_receive != 0
        except Exception:
            return self.safe_to_send()

    def is_shopkeeper_item(self, item_data: dict) -> bool:
        """Check if an item is a shopkeeper NPC."""
        flag_id = item_data.get("flag_id")
        if flag_id is None:
            return False

        shopkeeper_flags = {962, 963, 964, 965}  # Cranky, Funky, Candy, Snide
        return flag_id in shopkeeper_flags

    async def validate_client_connection(self):
        """Validate the client connection."""
        self.memory_pointer = self.n64_client.read_u32(DK64MemoryMap.memory_pointer)
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.connection, 0xFF)
        if self.n64_client.read_u8(DK64MemoryMap.eeprom_determined) == 1:
            if self.n64_client.read_u32(DK64MemoryMap.save_type) != 2:
                # Map emulator IDs to their setup guides
                emulator_setup_guides = {
                    "Project64": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-Project-64",
                    "Project64_v4": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-Project-64",
                    "RMG": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-Rosalies-Mupen-GUI",
                    "ParallelLauncher": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-Parallel-Launcher",
                    "RetroArch": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-RetroArch",
                    "BizHawk": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-BizHawk-DK64-Edition",
                    "Simple64": "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators:-Simple64",
                }

                emulator_id = self.n64_client.emulator_info.id.name
                setup_guide = emulator_setup_guides.get(emulator_id, "https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators")

                logger.error(f"{self.n64_client.emulator_info.id.name} is not set up correctly! Please follow the appropriate setup guide to ensure the game works!")
                logger.error(f"{setup_guide}")
                raise Exception("Bad emulator setup")

    # ==================== MESSAGING METHODS ====================

    def send_message(self, item_name, player_name, event_type="from"):
        """Send a message to the game."""

        def sanitize_and_trim(input_string, max_length=MAX_STRING_LENGTH):
            normalized = normalize_location_name(input_string)
            sanitized = "".join(e for e in normalized if e.isalnum() or e == " ").strip()
            return sanitized[:max_length]

        stripped_item_name = sanitize_and_trim(item_name)
        stripped_player_name = sanitize_and_trim(player_name)
        self.n64_client.write_bytestring(self.memory_pointer + DK64MemoryMap.fed_string, f"{stripped_item_name}".upper())
        self.n64_client.write_bytestring(self.memory_pointer + DK64MemoryMap.fed_subtitle, f"{event_type} {stripped_player_name}".upper())

    def set_speed(self, speed: int):
        """Set the speed of the display text in game."""
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.text_timer, speed)

    # ==================== ITEM PROCESSING METHODS ====================

    async def recved_item_from_ap(self, item_id, item_name, from_player, index):
        """Handle an item received from Archipelago."""
        if not self.started_file():
            return

        item_data = item_ids.get(item_id)
        if not item_data:
            logger.warning(f"Unknown item ID: {item_id}")
            return

        # Check if this is a shopkeeper item
        is_shopkeeper = self.is_shopkeeper_item(item_data)

        await self._wait_for_safe_send(is_shopkeeper)

        self._handle_message_display(item_data, item_name, from_player, index)
        await self._process_item_data(item_data, item_name)

        next_index = index + 1
        self.n64_client.write_u16(self.memory_pointer + DK64MemoryMap.counter_offset, next_index)

    async def _wait_for_safe_send(self, is_shopkeeper=False):
        """Wait until it's safe to send an item."""
        if is_shopkeeper:
            while not self.safe_to_send_shopkeeper():
                await asyncio.sleep(0.1)
        else:
            while not self.safe_to_send():
                await asyncio.sleep(0.1)

    def _handle_message_display(self, item_data: dict, item_name: str, from_player: str, index: int):
        """Handle message display based on send mode and item type."""
        if not hasattr(self, "_message_handler"):
            self._message_handler = MessageDisplayHandler(self)

        should_display = self._message_handler.should_display_item(item_data, self.send_mode)
        if should_display:
            self.set_speed(FAST_TEXT_SPEED)
            self.send_message(item_name, from_player, "from")

    async def _process_item_data(self, item_data: dict, item_name: str):
        """Process the item data and apply it to the game."""
        if item_data.get("flag_id") is not None:
            flag_id = item_data.get("flag_id")
            self.setFlag(flag_id)
        elif item_data.get("fed_id") is not None:
            await self.writeFedData(item_data.get("fed_id"))
        elif item_data.get("count_id") is not None:
            await self.writeCountData(item_data.get("count_id"))
        else:
            logger.warning(f"Item {item_name} has no flag, fed, or count id")

    async def writeFedData(self, fed_item):
        """Write the fed item data to the game."""
        current_fed_item = self.n64_client.read_u32(self.memory_pointer + DK64MemoryMap.arch_items)
        # If item is being processed, don't update
        while current_fed_item != 0:
            current_fed_item = self.n64_client.read_u32(self.memory_pointer + DK64MemoryMap.arch_items)
            await asyncio.sleep(0.1)
            if current_fed_item == 0:
                break
        self.n64_client.write_u8(self.memory_pointer + 0x7, fed_item)

    async def writeCountData(self, count_data):
        """Write count data directly to the CountStruct system."""
        if isinstance(count_data, list):
            # Handle multiple count items (like Camera and Shockwave combo)
            for item in count_data:
                await self.writeCountData(item)
            return

        if not isinstance(count_data, dict):
            logger.warning(f"Invalid count_data format: {count_data}")
            return

        # Get the CountStruct address from the pointer
        count_struct_address = self.n64_client.read_u32(DK64MemoryMap.count_struct_pointer)
        if count_struct_address == 0:
            logger.warning("CountStruct pointer is null, cannot write count data")
            return

        # Write directly to CountStruct based on the field type
        field = count_data.get("field")
        helm_hurry_item_type = None

        if field == "bp_count":
            if "kong" in count_data:
                kong = count_data.get("kong", 0)
                # Validate ranges
                if kong < 0 or kong > 4:
                    logger.warning(f"Invalid Kong: Kong={kong}")
                    return
                byte_index = kong
            else:
                byte_index = count_data.get("byte", 0)

            if byte_index < 5:
                address = count_struct_address + 0x000 + byte_index
                current_value = self.n64_client.read_u8(address)
                self.n64_client.write_u8(address, current_value + 1)
                helm_hurry_item_type = 0x04A  # TRANSFER_ITEM_HELM_HURRY_BLUEPRINT
            else:
                logger.warning(f"Invalid hint bitfield position: byte={byte_index}")

        elif field == "hint_bitfield":
            # Hint bitfield: 5 bytes starting at offset 0x005
            # Convert kong/level to byte/bit if needed
            if "kong" in count_data and "level" in count_data:
                kong = count_data.get("kong", 0)
                level = count_data.get("level", 0)
                CountStructHandler.validate_bounds(kong=kong, level=level)
                byte_index = kong
                bit_index = level
            else:
                byte_index = count_data.get("byte", 0)
                bit_index = count_data.get("bit", 0)
                CountStructHandler.validate_bounds(kong=byte_index, level=bit_index)

            # Ensure we don't exceed the 5-byte hint bitfield and 7 bits per kong
            if byte_index < HINT_BITFIELD_SIZE and bit_index < LEVEL_COUNT:
                address = CountStructHandler.get_address(self, "hint_bitfield", byte_index)
                current_value = self.n64_client.read_u8(address)
                new_value = current_value | (1 << bit_index)
                self.n64_client.write_u8(address, new_value)
            else:
                logger.warning(f"Invalid hint bitfield position: byte={byte_index}, bit={bit_index}")

        elif field == "key_bitfield":
            # Key bitfield: 1 byte at offset 0x00A
            bit_index = count_data.get("bit", 0)
            address = count_struct_address + 0x00A
            current_value = self.n64_client.read_u8(address)
            new_value = current_value | (1 << bit_index)
            self.n64_client.write_u8(address, new_value)
            helm_hurry_item_type = 0x04F  # TRANSFER_ITEM_HELM_HURRY_KEY

        elif field == "kong_bitfield":
            # Kong bitfield: 1 byte at offset 0x00B
            bit_index = count_data.get("bit", 0)
            address = count_struct_address + 0x00B
            current_value = self.n64_client.read_u8(address)
            new_value = current_value | (1 << bit_index)
            self.n64_client.write_u8(address, new_value)
            helm_hurry_item_type = 0x053  # TRANSFER_ITEM_HELM_HURRY_KONG

        elif field == "crowns":
            # Crowns: 1 byte counter at offset 0x00C
            address = count_struct_address + 0x00C
            current_value = self.n64_client.read_u8(address)
            self.n64_client.write_u8(address, current_value + 1)
            helm_hurry_item_type = 0x050  # TRANSFER_ITEM_HELM_HURRY_CROWN

        elif field == "special_items":
            # Special items: 1 byte bitfield at offset 0x00D
            bit_name = count_data.get("bit")
            address = count_struct_address + 0x00D
            current_value = self.n64_client.read_u8(address)

            if bit_name == "nintendo_coin":
                new_value = current_value | 0x80  # bit 7
                helm_hurry_item_type = 0x04B  # TRANSFER_ITEM_HELM_HURRY_COMPANYCOIN
            elif bit_name == "rareware_coin":
                new_value = current_value | 0x40  # bit 6
                helm_hurry_item_type = 0x04B  # TRANSFER_ITEM_HELM_HURRY_COMPANYCOIN
            elif bit_name == "bean":
                new_value = current_value | 0x20  # bit 5
                helm_hurry_item_type = 0x051  # TRANSFER_ITEM_HELM_HURRY_BEAN
            else:
                logger.warning(f"Unknown special_items bit: {bit_name}")
                return

            self.n64_client.write_u8(address, new_value)

        elif field == "medals":
            # Medals: 1 byte counter at offset 0x00E
            address = count_struct_address + 0x00E
            current_value = self.n64_client.read_u8(address)
            self.n64_client.write_u8(address, current_value + 1)
            helm_hurry_item_type = 0x04D  # TRANSFER_ITEM_HELM_HURRY_MEDAL

        elif field == "pearls":
            # Pearls: 1 byte counter at offset 0x00F
            address = count_struct_address + 0x00F
            current_value = self.n64_client.read_u8(address)
            self.n64_client.write_u8(address, current_value + 1)
            helm_hurry_item_type = 0x052  # TRANSFER_ITEM_HELM_HURRY_PEARL

        elif field == "fairies":
            # Fairies: 1 byte counter at offset 0x010
            address = count_struct_address + 0x010
            current_value = self.n64_client.read_u8(address)
            self.n64_client.write_u8(address, current_value + 1)
            helm_hurry_item_type = 0x054  # TRANSFER_ITEM_HELM_HURRY_FAIRY

        elif field == "rainbow_coins":
            await self.writeFedData(0x015)  # TRANSFER_ITEM_RAINBOWCOIN
            # Rainbow coins should trigger Helm Hurry with HHITEM_RAINBOWCOIN (6)
            if self.helm_hurry_enabled:
                self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.helm_hurry_item, 6)

        elif field == "ice_traps":
            # Ice traps: 2 byte counter at offset 0x012
            # Also need to trigger the actual ice trap effect via fed system
            helm_hurry_item_type = await IceTrapHandler.handle_ice_trap(self, count_data)

        elif field == "junk_items":
            # Junk items: 2 byte counter at offset 0x014
            address = count_struct_address + 0x014
            current_value = self.n64_client.read_u16(address)
            self.n64_client.write_u16(address, current_value + 1)
            # Junk items don't contribute to Helm Hurry timer

        elif field == "race_coins":
            # Race coins: 2 byte counter at offset 0x016
            address = count_struct_address + 0x016
            current_value = self.n64_client.read_u16(address)
            self.n64_client.write_u16(address, current_value + 1)
            # Race coins don't contribute to Helm Hurry timer

        elif field == "flag_moves":
            # Flag moves: bitfield at offset 0x018
            bit_name = count_data.get("bit")
            address = count_struct_address + 0x018
            current_value = self.n64_client.read_u8(address)

            if bit_name == "diving":
                new_value = current_value | 0x80  # bit 7 (0x80 >> 0)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            elif bit_name == "oranges":
                new_value = current_value | 0x40  # bit 6 (0x80 >> 1)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            elif bit_name == "barrels":
                new_value = current_value | 0x20  # bit 5 (0x80 >> 2)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            elif bit_name == "vines":
                new_value = current_value | 0x10  # bit 4 (0x80 >> 3)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            elif bit_name == "camera":
                new_value = current_value | 0x08  # bit 3 (0x80 >> 4)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            elif bit_name == "shockwave":
                new_value = current_value | 0x04  # bit 2 (0x80 >> 5)
                helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE
            else:
                logger.warning(f"Unknown flag_moves bit: {bit_name}")
                return

            self.n64_client.write_u8(address, new_value)

        elif count_data.get("item") is not None and count_data.get("level") is not None:
            # These are fed items with level/tier information (like progression slams, etc.)
            item_id = count_data.get("item")

            # Map requirement item IDs to transfer item IDs based on the type
            # REQITEM_MOVE (2) with level 3 should be TRANSFER_ITEM_SLAMUPGRADE (0x033 = 51)
            if item_id == 2:  # REQITEM_MOVE
                # For slam upgrades, use TRANSFER_ITEM_SLAMUPGRADE
                fed_id = 0x033  # TRANSFER_ITEM_SLAMUPGRADE
            else:
                fed_id = item_id

            await self.writeFedData(fed_id)
            # Most fed items with levels are moves, so they should trigger Helm Hurry
            helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE

        elif count_data.get("item") is not None and count_data.get("level") is None:
            # These are requirement_item enum values that map to archipelago_items
            fed_id = count_data.get("item")
            await self.writeFedData(fed_id)
            # These could be various types, but most are moves or other progression items
            # For now, assume they're moves unless we have better classification
            helm_hurry_item_type = 0x04C  # TRANSFER_ITEM_HELM_HURRY_MOVE

        else:
            logger.warning(f"Unknown count_data field: {count_data}")
            return

        # Send Helm Hurry timer update if we have a relevant item type and Helm Hurry is enabled
        if helm_hurry_item_type is not None and self.helm_hurry_enabled:
            self.writeHelmHurryItem(helm_hurry_item_type)

    def writeHelmHurryItem(self, helm_hurry_item_type):
        """Write Helm Hurry item type directly to memory."""
        # Map the hex values to the corresponding HHITEM enum values
        # Based on common_enums.h HHITEM enum (1-indexed, 0 = HHITEM_NOTHING)
        helm_hurry_mapping = {
            0x04A: 2,  # HHITEM_BLUEPRINT
            0x04B: 3,  # HHITEM_COMPANYCOIN
            0x04C: 4,  # HHITEM_MOVE
            0x04D: 5,  # HHITEM_MEDAL
            0x04F: 7,  # HHITEM_KEY
            0x050: 8,  # HHITEM_CROWN
            0x051: 9,  # HHITEM_BEAN
            0x052: 10,  # HHITEM_PEARL
            0x053: 11,  # HHITEM_KONG
            0x054: 12,  # HHITEM_FAIRY
            0x056: 14,  # HHITEM_FAKEITEM
        }

        hhitem_value = helm_hurry_mapping.get(helm_hurry_item_type, 0)
        if hhitem_value > 0:
            self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.helm_hurry_item, hhitem_value)

    def _getShopStatus(self, p_type: int, p_value: int, p_kong: int) -> bool:
        """Get the status of a shop item."""
        if p_type == 0xFFFF:
            return False
        if p_value == 0:
            return False
        if p_kong > 4:
            p_kong = 0
        kong_base = 0x807FC950 + (p_kong * 0x5E)
        if p_type < 5:
            val = self.n64_client.read_u8(kong_base + p_type)
            if p_type in (1, 3):
                # Slam, Ammo Belt
                return val >= p_type
            else:
                return (val & (1 << (p_value - 1))) != 0
        else:
            return self.readFlag(p_value) != 0

    def getMoveStatus(self, move_flag: int) -> bool:
        """Get the status of a move."""
        item_kong = (move_flag >> 12) & 7
        if item_kong > 4:
            item_kong = 0
        item_type = (move_flag >> 8) & 15
        if item_type == 7:
            return True
        item_index = move_flag & 0xFF
        address = 0x807FC950 + (0x5E * item_kong) + item_type
        value = self.n64_client.read_u8(address)
        offset = 0
        if item_index > 0:
            offset = item_index - 1
        return ((value >> offset) & 1) != 0

    def getCheckStatus(self, check_type, flag_index=None, shop_index=None, level_index=None, kong_index=None) -> bool:
        """Get the status of a check."""
        if check_type == "shop" and shop_index is not None and level_index is not None and kong_index is not None:
            FLAG_SHOPFLAG = 800
            LEVEL_AZTEC = 1
            LEVEL_GALLEON = 3
            LEVEL_CAVES = 5
            LEVEL_CASTLE = 6
            SHOP_CRANKY = 0
            SHOP_FUNKY = 1
            SHOP_CANDY = 2

            shop_flag = None

            if shop_index == SHOP_CRANKY:
                # Cranky: FLAG_SHOPFLAG + (level * 5) + kong
                shop_flag = FLAG_SHOPFLAG + (level_index * 5) + kong_index
            elif shop_index == SHOP_FUNKY and level_index < 7:
                # Funky: FLAG_SHOPFLAG + ((level + 8) * 5) + kong
                shop_flag = FLAG_SHOPFLAG + ((level_index + 8) * 5) + kong_index
            elif shop_index == SHOP_CANDY:
                # Candy has two ranges (Aztec-Galleon and Caves/Castle)
                if LEVEL_AZTEC <= level_index <= LEVEL_GALLEON:
                    candy_offset = level_index - LEVEL_AZTEC
                    shop_flag = FLAG_SHOPFLAG + ((candy_offset + 15) * 5) + kong_index
                elif LEVEL_CAVES <= level_index <= LEVEL_CASTLE:
                    candy_offset = level_index - LEVEL_CAVES
                    shop_flag = FLAG_SHOPFLAG + ((candy_offset + 18) * 5) + kong_index
            if shop_flag is None:
                return False

            return self.readFlag(shop_flag)
        else:
            return self.readFlag(flag_index)

    async def readChecks(self, cb):
        """Run checks in parallel using asyncio."""
        new_checks = []
        checks_to_read = self.remaining_checks

        for id in checks_to_read:
            name = check_id_to_name.get(id)
            # Try to get the check via location_name_to_flag
            check = location_name_to_flag.get(name)
            if check:
                # Assuming we did find it in location_name_to_flag
                check_status = self.getCheckStatus("location", check)
                if check_status:
                    self.remaining_checks.remove(id)
                    new_checks.append(id)
                    if self.locations_scouted.get(id):
                        self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))
            # If its not there using the id lets try to get it via item_ids
            else:
                # If the content is 3 parts separated by a space, we can assume it's a shop check
                content = name.split(" ")
                if ("Cranky" in name or "Candy" in name or "Funky" in name) and len(content) == 3:
                    level_mapping = {"Japes": 0, "Aztec": 1, "Factory": 2, "Galleon": 3, "Forest": 4, "Caves": 5, "Castle": 6, "Isles": 7}
                    shop_mapping = {"Cranky": 0, "Funky": 1, "Candy": 2}
                    kong_mapping = {"Donkey": 0, "Diddy": 1, "Lanky": 2, "Tiny": 3, "Chunky": 4}

                    level_index = level_mapping.get(content[0])
                    shop_index = shop_mapping.get(content[1])
                    kong_index = kong_mapping.get(content[2])

                    # Handle shared shops by checking the DK flag (kong_index 0)
                    if content[2] == "Shared":
                        kong_index = 0  # Use DK flag for shared shops

                    # If any of these are not set, continue
                    if level_index is None or shop_index is None or kong_index is None:
                        continue

                    check_status = self.getCheckStatus("shop", None, shop_index, level_index, kong_index)
                    if check_status:
                        self.remaining_checks.remove(id)
                        new_checks.append(id)
                        if self.locations_scouted.get(id):
                            self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))
                    continue
                else:
                    check = item_ids.get(id)
                    if check:
                        flag_id = check.get("flag_id")
                        if not flag_id:
                            # logger.error(f"Item {name} has no flag_id")
                            continue
                        else:
                            check_status = self.getCheckStatus("location", flag_id)
                            if check_status:
                                self.remaining_checks.remove(id)
                                new_checks.append(id)
                                if self.locations_scouted.get(id):
                                    self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))

        if new_checks:
            cb(new_checks)
        return True

    async def reset_auth(self):
        """Reset the auth by looking up a username from ROM."""
        username = self.n64_client.read_bytestring(DK64MemoryMap.name_location, 16).strip()
        # Strip all trailing \x00
        username = username.replace("\x00", "")
        self.auth = username

    def started_file(self):
        """Check if the file has been started."""
        # Checks to see if the file has been started
        if not self.seed_started:
            status = self.readFlag(0) == 1
            if status:
                self.seed_started = True
            return status
        return True

    should_reset_auth = False

    # ==================== MEMORY OPERATIONS ====================

    def setFlag(self, index: int) -> int:
        """Set a flag in the game."""
        byte_index = index >> 3
        shift = index & 7
        offset = DK64MemoryMap.EEPROM + byte_index
        val = self.n64_client.read_u8(offset)
        self.n64_client.write_u8(offset, val | (1 << shift))
        return 1

    def readFlag(self, index: int) -> int:
        """Read a flag in the game."""
        byte_index = index >> 3
        shift = index & 7
        offset = DK64MemoryMap.EEPROM + byte_index
        val = self.n64_client.read_u8(offset)
        return (val >> shift) & 1

    def hasKong(self, kong_index: int) -> bool:
        """Check if a kong is available using the CountStruct system."""
        if kong_index < 0 or kong_index >= KONG_COUNT:
            return False

        try:
            # Kong bitfield: 1 byte at offset 0x00B
            address = CountStructHandler.get_address(self, "kong_bitfield")
            current_value = self.n64_client.read_u8(address)

            # Check if the bit for this kong is set
            return (current_value & (1 << kong_index)) != 0
        except ValueError:
            return False

    async def wait_for_game_ready(self):
        """Wait for the game to be ready."""
        logger.info("Waiting on game to be in valid state...")
        while not self.check_safe_gameplay():
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise Exception("Resetting due to wrong archipelago server")
        logger.info("Game connection ready!")

    async def is_victory(self, win_condition_item=0, helm_hurry=False):
        """Check if the game is in a victory state."""
        end_credits_complete = self.readFlag(DK64MemoryMap.end_credits) == 1
        win_condition = win_condition_item  # WinConditionComplex.beat_krool = 0 is default

        # Helm hurry can be enabled either by specific win conditions OR by the helm_hurry flag (treasure hurry)
        helm_hurry_enabled = helm_hurry or win_condition not in [0, 1, 2]  # beat_krool, get_key8, krem_kapture don't use Helm Hurry unless explicitly enabled

        if helm_hurry_enabled:
            # For Helm Hurry, victory is achieved when EITHER the helm hurry completion flag is set OR K. Rool is beaten
            helm_hurry_finished = self.readFlag(0x3CB) == 1  # FLAG_HELM_HURRY_DISABLED (0x3CB = 971)
            return helm_hurry_finished or end_credits_complete
        else:
            # Standard mode: only end credits count as victory
            return end_credits_complete

    async def get_current_map(self):
        """Get the current map."""
        return self.n64_client.read_u32(DK64MemoryMap.current_map)

    def get_current_deliver_count(self):
        """Get the current deliver count."""
        data = self.n64_client.read_u16(self.memory_pointer + DK64MemoryMap.counter_offset)

        # If our data is too high, try reading again
        if data > MAX_DELIVER_COUNT:
            data = self.n64_client.read_u16(self.memory_pointer + DK64MemoryMap.counter_offset)
            if data > MAX_DELIVER_COUNT:
                return None

        return data

    async def main_tick(self, item_get_cb, deathlink_cb, map_change_cb, ring_link, tag_link, trap_link, hint_cb=None):
        """Game loop tick."""
        await self.readChecks(item_get_cb)
        # await self.item_tracker.readItems()
        if await self.get_current_map() != self.current_map:
            self.current_map = await self.get_current_map()
            await map_change_cb(self.current_map)

        def check_safe_death():
            """Check if it's safe to send a death."""
            return self.n64_client.read_u8(self.memory_pointer + DK64MemoryMap.can_die) != 1

        if self.ENABLE_DEATHLINK:
            death_state = self.n64_client.read_u8(self.memory_pointer + DK64MemoryMap.send_death)
            if self.deathlink_debounce and death_state == 0:
                self.deathlink_debounce = False
            elif not self.deathlink_debounce and death_state == 1:
                # logger.info("YOU DIED.")
                await deathlink_cb()
                self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.send_death, 0)
                self.deathlink_debounce = True

            if self.pending_deathlink:
                logger.info("Got a deathlink")
                while check_safe_death():
                    await asyncio.sleep(0.1)
                self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.receive_death, 1)
                self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.send_death, 0)
                self.pending_deathlink = False
                self.deathlink_debounce = True
                await asyncio.sleep(5)
        if self.ENABLE_RINGLINK:
            await ring_link()
        if self.ENABLE_TAGLINK:
            await tag_link()
        if self.ENABLE_TRAPLINK:
            await trap_link()

        # Check for hint access
        if hint_cb:
            await self.check_hint_access(hint_cb)

        current_deliver_count = self.get_current_deliver_count()
        if current_deliver_count is None:
            return

        if current_deliver_count > MAX_DELIVER_COUNT:
            logger.info(f"Current deliver count: {current_deliver_count}")
            logger.info(f"Received checks: {len(self.recvd_checks)}")
            logger.info(f"Pending checks: {len(self.pending_checks)}")
            logger.info("Current deliver count is too high, PLEASE REPORT THIS TO THE DK64 TEAM")
            return
        if current_deliver_count in self.recvd_checks:
            # Get the next item in recvd_checks
            item = self.recvd_checks[current_deliver_count]
            item_name = self.item_names.lookup_in_game(item.item)
            player_name = self.players.get(item.player)
            await self.recved_item_from_ap(item.item, item_name, player_name, current_deliver_count)
            # Remove the item from pending_checks
            self.pending_checks.remove(item)
        else:
            for item in self.pending_checks.copy():
                self.pending_checks.remove(item)

        if len(self.sent_checks) > 0:
            cloned_checks = self.sent_checks.copy()
            for item in cloned_checks:
                status = self.safe_to_send()
                while not status:
                    await asyncio.sleep(0.1)
                    status = self.safe_to_send()
                # Strip out special characters from item name
                item_name = item[0]
                sender = item[1]
                self.send_message(item_name, sender, "to")
                self.sent_checks.remove(item)

    def safe_clear_death_events(self):
        """Clear any death events that may be pending."""
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.receive_death, 0)
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.send_death, 0)
        self.pending_deathlink = False
        self.deathlink_debounce = True

    # ==================== HINT SYSTEM METHODS ====================

    def read_hint_bitfield(self):
        """Read the current hint bitfield from memory."""
        count_struct_address = self.n64_client.read_u32(DK64MemoryMap.count_struct_pointer)
        if count_struct_address == 0:
            return [0] * HINT_BITFIELD_SIZE

        hint_bitfield = []
        for i in range(HINT_BITFIELD_SIZE):
            address = count_struct_address + 0x005 + i
            hint_bitfield.append(self.n64_client.read_u8(address))
        return hint_bitfield

    async def check_hint_access(self, hint_callback):
        """Check if any new hints have been accessed."""
        if not self.memory_pointer:
            return

        current_hint_bitfield = self.read_hint_bitfield()

        # Check each byte and bit for changes
        for kong in range(KONG_COUNT):
            for level in range(LEVEL_COUNT):
                old_bit = (self.last_hint_bitfield[kong] >> level) & 1
                new_bit = (current_hint_bitfield[kong] >> level) & 1

                # If bit changed from 0 to 1, a hint was accessed
                if old_bit == 0 and new_bit == 1:
                    hint_key = (kong, level)
                    if hint_key not in self.sent_hints:
                        self.sent_hints.add(hint_key)
                        await hint_callback(kong, level)

        # Update last known state
        self.last_hint_bitfield = current_hint_bitfield.copy()


class DK64CommandProcessor(ClientCommandProcessor):
    """Command processor for Donkey Kong 64 commands."""

    def __init__(self, ctx):
        """Initialize the DK64 command processor."""
        super().__init__(ctx)

    def _cmd_reset_deathlink(self):
        """Reset the deathlink state."""
        if isinstance(self.ctx, DK64Context):
            self.ctx.client.safe_clear_death_events()
            logger.info("Deathlink state reset")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, DK64Context):
            if self.ctx.ENABLE_DEATHLINK:
                self.ctx.ENABLE_DEATHLINK = False
                self.ctx.client.ENABLE_DEATHLINK = False
                create_task_log_exception(self.ctx.update_death_link(False))
                logger.info("Deathlink disabled")
            else:
                self.ctx.ENABLE_DEATHLINK = True
                self.ctx.client.ENABLE_DEATHLINK = True
                create_task_log_exception(self.ctx.update_death_link(True))
                logger.info("Deathlink enabled")

    def _cmd_taglink(self):
        """Toggle taglink from client. Overrides default setting."""
        if isinstance(self.ctx, DK64Context):
            if self.ctx.ENABLE_TAGLINK:
                self.ctx.ENABLE_TAGLINK = False
                self.ctx.client.ENABLE_TAGLINK = False
                self.ctx.tags.discard("TagLink")
                logger.info("Taglink disabled")
            else:
                self.ctx.ENABLE_TAGLINK = True
                self.ctx.client.ENABLE_TAGLINK = True
                logger.info("Taglink enabled")
                self.ctx.tags.add("TagLink")
            create_task_log_exception(self.ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": self.ctx.tags}]))

    def _cmd_ringlink(self):
        """Toggle ringlink from client. Overrides default setting."""
        if isinstance(self.ctx, DK64Context):
            if self.ctx.ENABLE_RINGLINK:
                self.ctx.ENABLE_RINGLINK = False
                self.ctx.client.ENABLE_RINGLINK = False
                self.ctx.tags.discard("RingLink")
                logger.info("Ringlink disabled")
            else:
                self.ctx.ENABLE_RINGLINK = True
                self.ctx.client.ENABLE_RINGLINK = True
                logger.info("Ringlink enabled")
                self.ctx.tags.add("RingLink")
            create_task_log_exception(self.ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": self.ctx.tags}]))

    def _cmd_traplink(self):
        """Toggle traplink from client. Overrides default setting."""
        if isinstance(self.ctx, DK64Context):
            if self.ctx.ENABLE_TRAPLINK:
                self.ctx.ENABLE_TRAPLINK = False
                self.ctx.client.ENABLE_TRAPLINK = False
                self.ctx.tags.discard("TrapLink")
                logger.info("Traplink disabled")
            else:
                self.ctx.ENABLE_TRAPLINK = True
                self.ctx.client.ENABLE_TRAPLINK = True
                logger.info("Traplink enabled")
                self.ctx.tags.add("TrapLink")
            create_task_log_exception(self.ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": self.ctx.tags}]))


class DK64Context(CommonContext):
    """Context for Donkey Kong 64."""

    tags = {"AP"}
    game = "Donkey Kong 64"
    la_task = None
    found_checks = []
    last_resend = time.time()
    ENABLE_DEATHLINK = False
    ENABLE_RINGLINK = False
    ENABLE_TAGLINK = False
    ENABLE_TRAPLINK = False
    command_processor = DK64CommandProcessor
    won = False
    hint_locations = {}
    handled_scouts = []

    def reset_checks(self):
        """Reset the checks."""
        # Only include location IDs that actually exist in this multiworld
        # For shared shops, only the 10 selected ones will be in missing_locations
        all_possible_checks = set(check_id_to_name.keys())
        if hasattr(self, "missing_locations") and self.missing_locations:
            # Filter to only locations that exist in this world
            actual_checks = all_possible_checks.intersection(self.missing_locations)
            self.remaining_checks = list(actual_checks)

            # Debug logging for shared shops
            shared_shop_ids = set()
            for location_id in actual_checks:
                location_name = check_id_to_name.get(location_id, "")
                if "Shared" in location_name:
                    shared_shop_ids.add(location_id)
        else:
            self.remaining_checks = list(all_possible_checks)
        self.client.remaining_checks = self.remaining_checks
        self.client.recvd_checks = {}
        self.client.pending_checks = []
        self.found_checks = []
        self.client.flag_lookup = None
        self.handled_scouts = []
        self.create_hints_params = []

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        """Initialize the DK64 context."""
        self.client = DK64Client()
        self.client.game = self.game.upper()
        self.slot_data = {}
        self.reset_checks()

        super().__init__(server_address, password)

    def already_running(self) -> bool:
        """Check if the GUI is already running."""
        try:
            import ctypes

            mutex = ctypes.windll.kernel32.CreateMutexW(None, 1, "DK64_GUI_MUTEX")
            return ctypes.GetLastError() == 183  # ERROR_ALREADY_EXISTS
        except Exception:
            return False

    def run_gui(self) -> None:
        """Run the GUI."""
        if self.already_running():
            print("GUI already running.")
            sys.exit(1)
        from kvui import GameManager

        class DK64Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
            ]
            base_title = f"Archipelago Donkey Kong 64 Client (Version {get_ap_version()})"

            def build(self):
                b = super().build()
                return b

        self.ui = DK64Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def send_checks(self):
        """Send the checks to the server."""
        if self.found_checks:
            message = [{"cmd": "LocationChecks", "locations": self.found_checks}]
            await self.send_msgs(message)
            self.found_checks = []

    had_invalid_slot_data: typing.Optional[bool] = None

    def event_invalid_slot(self):
        """Handle an invalid slot event."""
        # The next time we try to connect, reset the game loop for new auth
        self.had_invalid_slot_data = True
        self.auth = None
        # Don't try to autoreconnect, it will just fail
        self.disconnected_intentionally = True
        CommonContext.event_invalid_slot(self)

    async def send_victory(self):
        """Send a victory message."""
        if not self.won:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            logger.info("victory!")
            await self.send_msgs(message)
            self.won = True

    def new_checks(self, item_ids):
        """Handle new checks."""
        self.found_checks += item_ids
        create_task_log_exception(self.send_checks())

    async def server_auth(self, password_requested: bool = False):
        """Authenticate with the server."""
        if password_requested and not self.password:
            await super(DK64Context, self).server_auth(password_requested)
        if self.had_invalid_slot_data:
            # We are connecting when previously we had the wrong ROM or server - just in case
            # re-read the ROM so that if the user had the correct address but wrong ROM, we
            # allow a successful reconnect
            self.client.should_reset_auth = True
            self.had_invalid_slot_data = False
            self.reset_checks()

        while self.client.auth is None:
            await asyncio.sleep(0.1)

            # Just return if we're closing
            if self.exit_event.is_set():
                return

        self.auth = self.client.auth
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        """Handle a package."""
        self.client.item_names = self.item_names
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            self.slot_data = args.get("slot_data", {})
            self.setup_hint_locations()
            if self.slot_data.get("Version"):
                ap_version = get_ap_version()
                server_ver = self.slot_data.get("Version")
                server_major = server_ver.split(".")[0]
                server_minor = server_ver.split(".")[1]
                server_patch = server_ver.split(".")[2]
                # Get the current version from the ap_version.py file
                ap_major = ap_version.split(".")[0]
                ap_minor = ap_version.split(".")[1]
                ap_patch = ap_version.split(".")[2]
                if server_major != ap_major or server_minor != ap_minor:
                    logger.error("Your DK64 APworld does not match with the generated world.")
                    logger.error(f"Your version: {ap_version} | Generated version: {server_ver}")
                    raise Exception("Your DK64 APworld does not match with the generated world.\n" + f"Your version: {ap_version} | Generated version: {server_ver}")
                if server_patch != ap_patch:
                    logger.warning("Your DK64 APworld does not match with the generated world, but this should not be a breaking change.")
                    logger.warning("While we try to maintain backwards compatibility on patch versions, be warned that something might break.")
            if self.slot_data.get("death_link"):
                if "DeathLink" not in self.tags:
                    create_task_log_exception(self.update_death_link(True))
                    self.ENABLE_DEATHLINK = True
                    self.client.ENABLE_DEATHLINK = True
            if self.slot_data.get("ring_link"):
                if "RingLink" not in self.tags:
                    self.tags.add("RingLink")
                    self.ENABLE_RINGLINK = True
                    self.client.ENABLE_RINGLINK = True
                    asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))
            if self.slot_data.get("tag_link"):
                if "TagLink" not in self.tags:
                    self.tags.add("TagLink")
                    self.ENABLE_TAGLINK = True
                    self.client.ENABLE_TAGLINK = True
                    asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))
            if self.slot_data.get("trap_link"):
                if "TrapLink" not in self.tags:
                    self.tags.add("TrapLink")
                    self.ENABLE_TRAPLINK = True
                    self.client.ENABLE_TRAPLINK = True
                    asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))
            if self.slot_data.get("receive_notifications"):
                self.client.send_mode = self.slot_data.get("receive_notifications")
            # Set Helm Hurry flag in client
            self.client.helm_hurry_enabled = self.slot_data.get("helm_hurry", False)
            self.client.players = self.player_names
            # Reset checks after we have missing_locations info
            self.reset_checks()
            missing_locations = self.missing_locations
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": list(missing_locations)}]))
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                self.client.recvd_checks[index] = item
                self.client.pending_checks.append(item)
        if cmd == "LocationInfo":
            self.client.locations_scouted = {}
            for location in args.get("locations"):
                if location.player != self.slot:
                    # If the location is in the list, remove it
                    player_name = self.player_names.get(location.player)
                    location_id = location.location
                    item_name = self.item_names.lookup_in_game(location.item, self.slot_info[location.player].game)
                    self.client.locations_scouted[location_id] = {"player": player_name, "item_name": item_name}
        if isinstance(args, dict) and isinstance(args.get("data", {}), dict):
            source_name = args.get("data", {}).get("source", None)
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()
            if "RingLink" in self.tags and source_name != self.instance_id and "RingLink" in args.get("tags", []):
                if not hasattr(self, "pending_ring_link"):
                    self.pending_ring_link = 0
                self.pending_ring_link += args["data"]["amount"]
            if "TagLink" in self.tags and source_name != self.instance_id and "TagLink" in args.get("tags", []):
                if not hasattr(self, "pending_tag_link"):
                    self.pending_tag_link = False, 0
                try:
                    kong = args.get("data", {}).get("kong", 5)  # Default to 5 if not provided
                except Exception:
                    kong = 5
                self.pending_tag_link = True, kong
            if "TrapLink" in self.tags and source_name != self.player_names.get(self.slot) and "TrapLink" in args.get("tags", []):
                if not hasattr(self, "pending_trap_link"):
                    self.pending_trap_link = 0

                self.pending_trap_link = trap_name_to_index.get(args["data"]["trap_name"], 0)

                if self.pending_trap_link != 0:
                    self.pending_trap_original = args["data"]["trap_name"]
                    self.pending_trap_source = source_name

    async def send_ring_link(self, amount: int):
        """Send a ring link message."""
        if "RingLink" not in self.tags or self.slot is None:
            return
        if not hasattr(self, "instance_id"):
            self.instance_id = time.time()
        await self.send_msgs([{"cmd": "Bounce", "tags": ["RingLink"], "data": {"time": time.time(), "source": self.instance_id, "amount": amount}}])

    async def handle_ring_link(self):
        """Handle ring link functionality for DK64 items."""
        if not self.client.ENABLE_RINGLINK:
            return
        self.bypass_ring_link = False
        # Initialize previous values for all DK64 items if not set
        if not hasattr(self, "prev_base_ammo"):
            self.prev_base_ammo = 0
            self.bypass_ring_link = True
        if not hasattr(self, "prev_homing_ammo"):
            self.prev_homing_ammo = 0
            self.bypass_ring_link = True
        if not hasattr(self, "prev_oranges"):
            self.prev_oranges = 0
            self.bypass_ring_link = True
        if not hasattr(self, "prev_crystal_coconuts"):
            self.prev_crystal_coconuts = 0
            self.bypass_ring_link = True
        if not hasattr(self, "prev_film"):
            self.prev_film = 0
            self.bypass_ring_link = True
        # Read current values for all DK64 items (u16 reads)
        curr_base_ammo = self.client.n64_client.read_u16(DK64MemoryMap.ammo_base)
        curr_homing_ammo = self.client.n64_client.read_u16(DK64MemoryMap.homing_ammo)
        curr_oranges = self.client.n64_client.read_u16(DK64MemoryMap.oranges)
        curr_crystal_coconuts = self.client.n64_client.read_u16(DK64MemoryMap.crystal_coconuts)
        curr_film = self.client.n64_client.read_u16(DK64MemoryMap.film)
        # Calculate differences
        base_ammo_diff = curr_base_ammo - self.prev_base_ammo
        homing_ammo_diff = curr_homing_ammo - self.prev_homing_ammo
        oranges_diff = curr_oranges - self.prev_oranges
        film_diff = curr_film - self.prev_film

        # Special handling for crystal coconuts - only track 150-unit increments
        # Convert current and previous values to 150-unit increments
        curr_coconut_increments = curr_crystal_coconuts // 150
        prev_coconut_increments = self.prev_crystal_coconuts // 150
        coconuts_diff = curr_coconut_increments - prev_coconut_increments

        # Send or receive ring link for any positive or negative differences
        total_items_gained = 0
        total_items_lost = 0
        if base_ammo_diff > 0:
            total_items_gained += base_ammo_diff
        elif base_ammo_diff < 0:
            total_items_lost += abs(base_ammo_diff)
        if homing_ammo_diff > 0:
            total_items_gained += homing_ammo_diff
        elif homing_ammo_diff < 0:
            total_items_lost += abs(homing_ammo_diff)
        if oranges_diff > 0:
            total_items_gained += oranges_diff
        elif oranges_diff < 0:
            total_items_lost += abs(oranges_diff)
        if coconuts_diff > 0:
            total_items_gained += coconuts_diff
        elif coconuts_diff < 0:
            total_items_lost += abs(coconuts_diff)
        if film_diff > 0:
            total_items_gained += film_diff
        elif film_diff < 0:
            total_items_lost += abs(film_diff)
        if self.bypass_ring_link is True:
            # If we bypass ring link, we don't send any items
            total_items_gained = 0
            total_items_lost = 0
            self.bypass_ring_link = False
        if total_items_gained > 0:
            await self.send_ring_link(total_items_gained)
        if total_items_lost > 0:
            await self.send_ring_link(-total_items_lost)

        # Update previous values
        self.prev_base_ammo = curr_base_ammo
        self.prev_homing_ammo = curr_homing_ammo
        self.prev_oranges = curr_oranges
        self.prev_crystal_coconuts = curr_crystal_coconuts
        self.prev_film = curr_film

        # Handle incoming ring link items
        if not hasattr(self, "pending_ring_link"):
            self.pending_ring_link = 0

        if self.pending_ring_link != 0:
            # Distribute items evenly across the 5 item types
            # Each ring link item adds 1 to each type (except coconuts which add 150)
            items_to_add = self.pending_ring_link

            # Current Ammo Belt amount
            # Ammo Belt is a 1-byte value: 0 = 50, 1 = 100, 2 = 200
            curr_base_ammo_belt = self.client.n64_client.read_u8(DK64MemoryMap.ammo_belt)
            ammo_belt_capacity = 50
            if curr_base_ammo_belt == 1:
                ammo_belt_capacity = 100
            elif curr_base_ammo_belt == 2:
                ammo_belt_capacity = 200
            # Add items to base ammo
            new_base_ammo = max(0, min(curr_base_ammo + items_to_add, ammo_belt_capacity))
            self.client.n64_client.write_u16(DK64MemoryMap.ammo_base, new_base_ammo)

            # If ammo belt is 2 we can carry up to 20 homing ammo, else only 10
            homing_belt_capacity = 10
            if curr_base_ammo_belt == 2:
                homing_belt_capacity = 20
            # Add items to homing ammo
            new_homing_ammo = max(0, min(curr_homing_ammo + items_to_add, homing_belt_capacity))
            self.client.n64_client.write_u16(DK64MemoryMap.homing_ammo, new_homing_ammo)

            # Add items to oranges
            orange_capacity = 20
            if curr_base_ammo_belt == 1:
                orange_capacity = 25
            elif curr_base_ammo_belt == 2:
                orange_capacity = 30
            new_oranges = max(0, min(curr_oranges + items_to_add, orange_capacity))
            self.client.n64_client.write_u16(DK64MemoryMap.oranges, new_oranges)

            # Get the banana fairy total
            # This is disabled for now, as we don't have a way to read it so we're just always going to assume 0
            # banana_fairy_total = self.client.n64_client.read_u16(DK64MemoryMap.banana_fairy_total)
            banana_fairy_total = 0
            # Default is 20, each fairy adds 1
            coconut_total = 20
            if banana_fairy_total > 0:
                coconut_total += banana_fairy_total
            elif self.prev_crystal_coconuts > coconut_total:
                # If we have more coconuts than the total, we need to reset it
                coconut_total = self.prev_crystal_coconuts
            # Add items to crystal coconuts (150 per item)
            new_crystal_coconuts = max(0, min(curr_crystal_coconuts + (items_to_add * 150), coconut_total))
            self.client.n64_client.write_u16(DK64MemoryMap.crystal_coconuts, new_crystal_coconuts)

            # We do the same using the film
            film_total = 10
            if banana_fairy_total > 0:
                film_total += banana_fairy_total
            elif self.prev_film > film_total:
                # If we have more film than the total, we need to reset it
                film_total = self.prev_film
            # Add items to film
            new_film = max(0, min(curr_film + items_to_add, film_total))
            self.client.n64_client.write_u16(DK64MemoryMap.film, new_film)
            # Update previous values
            self.prev_base_ammo = new_base_ammo
            self.prev_homing_ammo = new_homing_ammo
            self.prev_oranges = new_oranges
            self.prev_crystal_coconuts = new_crystal_coconuts
            self.prev_film = new_film

            self.pending_ring_link = 0

    async def send_tag_link(self, kong: int):
        """Send a tag link message."""
        if "TagLink" not in self.tags or self.slot is None:
            return
        print(f"Sending tag link for kong {kong}")
        if not hasattr(self, "instance_id"):
            self.instance_id = time.time()
        await self.send_msgs([{"cmd": "Bounce", "tags": ["TagLink"], "data": {"time": time.time(), "source": self.instance_id, "tag": False, "kong": kong}}])

    async def handle_tag_link(self):
        """Handle tag link functionality for DK64 items."""
        if not self.client.ENABLE_TAGLINK:
            return
        current_kong = self.client.n64_client.read_u8(DK64MemoryMap.current_kong)
        if not hasattr(self, "pending_tag_link"):
            self.pending_tag_link = False, 0  # (is_pending, kong)
        if not hasattr(self, "previous_kong"):
            self.previous_kong = current_kong
        # If the current kong is different from the previous kong, send a tag link
        if current_kong != self.previous_kong:
            await self.send_tag_link(current_kong)
            self.previous_kong = current_kong

        if self.pending_tag_link[0]:
            # Check if its safe to cause a tag in the game
            if self.client.n64_client.read_u8(self.client.memory_pointer + DK64MemoryMap.can_tag) == 1:
                # If it is safe, send the tag
                kong = self.pending_tag_link[1]
                invalid_kong = True

                # Check if we have the requested kong using CountStruct system
                if self.client.hasKong(kong):
                    self.client.n64_client.write_u8(self.client.memory_pointer + DK64MemoryMap.tag_kong, kong)
                    current_kong = kong
                    invalid_kong = False

                if invalid_kong:
                    # Check if we have any kong not our current kong
                    valid_kongs = [current_kong]
                    # Check each int from 0 to 4 excluding current_kong
                    for i in range(5):
                        if i != current_kong and self.client.hasKong(i):
                            valid_kongs.append(i)

                    # If the only valid kong is the current kong, we can't tag
                    if len(valid_kongs) == 1:
                        self.pending_tag_link = False, 0
                    # Else randomly select a kong from valid_kongs, excluding the current kong
                    else:
                        valid_kongs.remove(current_kong)  # Ensure we don't tag the current kong
                        kong = random.choice(valid_kongs)
                        self.client.n64_client.write_u8(self.client.memory_pointer + DK64MemoryMap.tag_kong, kong)
                        current_kong = kong
                self.previous_kong = current_kong
                self.pending_tag_link = False, 0  # Reset pending tag link

    async def send_trap_link(self, trap_name: str):
        """Send a trap link message."""
        if "TrapLink" not in self.tags or self.slot is None:
            return
        logger.info(f"Sending trap link: {trap_name}")

        player_name = self.player_names.get(self.slot)

        await self.send_msgs([{"cmd": "Bounce", "tags": ["TrapLink"], "data": {"time": time.time(), "source": player_name, "trap_name": trap_name}}])

    async def handle_trap_link(self):
        """Handle trap link functionality for DK64 items."""
        if not self.client.ENABLE_TRAPLINK:
            return

        activated_trap = self.client.n64_client.read_u8(self.client.memory_pointer + DK64MemoryMap.is_trapped)
        if activated_trap != 0:
            trap_name = trap_index_to_name.get(activated_trap, "Bubble Trap")
            await self.send_trap_link(trap_name)
            self.client.n64_client.write_u8(self.client.memory_pointer + DK64MemoryMap.is_trapped, 0)

        if not hasattr(self, "pending_trap_link"):
            self.pending_trap_link = 0
        if not hasattr(self, "pending_trap_original"):
            self.pending_trap_original = ""
        if not hasattr(self, "pending_trap_source"):
            self.pending_trap_source = ""

        if self.pending_trap_link != 0:
            self.client.n64_client.write_u8(self.client.memory_pointer + DK64MemoryMap.sent_trap, self.pending_trap_link)
            self.pending_trap_link = 0
            logger.info(f"Received linked {self.pending_trap_original} from {self.pending_trap_source}")

    async def sync(self):
        """Sync the game."""
        sync_msg = [{"cmd": "Sync"}]
        await self.send_msgs(sync_msg)

    async def send_deathlink(self):
        """Send a deathlink."""
        if self.ENABLE_DEATHLINK:
            self.last_death_link = time.time()
            player_name = self.player_names.get(self.slot)
            await self.send_death(player_name + " slipped on a banana")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Handle a deathlink."""
        if self.ENABLE_DEATHLINK:
            self.client.pending_deathlink = True

    def setup_hint_locations(self):
        """Set up the mapping between hint positions and location IDs."""
        try:
            if not hasattr(self, "hint_locations"):
                self.hint_locations = {}

            # Get hint location mapping from slot_data
            hint_mapping = self.slot_data.get("HintLocationMapping", {})

            # Convert string keys back to tuples and store as location IDs
            for key, location_id in hint_mapping.items():
                if "," in key:
                    parts = key.split(",")
                    if len(parts) == 2:
                        try:
                            kong = int(parts[0])
                            level = int(parts[1])
                            self.hint_locations[(kong, level)] = location_id
                        except ValueError:
                            logger.warning(f"Invalid hint mapping key format: {key}")
        except Exception as e:
            logger.error(f"Error setting up hint locations: {e}")
            import traceback

            logger.error(traceback.format_exc())

    async def handle_hint_accessed(self, kong: int, level: int):
        """Handle when a hint is accessed in the game."""
        try:
            # Create a unique identifier for this hint position
            hint_key = (kong, level)

            # Map level index to actual level names for logging
            level_names = ["Japes", "Aztec", "Factory", "Galleon", "Forest", "Caves", "Castle"]
            kong_names = ["DK", "Diddy", "Lanky", "Tiny", "Chunky"]

            if 0 <= kong < 5 and 0 <= level < 7:
                level_name = level_names[level]
                kong_name = kong_names[kong]
                logger.debug(f"Hint accessed: {kong_name} in {level_name}")

                # Check if we have hint location mapping from slot data
                if hasattr(self, "hint_locations") and hint_key in self.hint_locations:
                    wrinkly_door_id = self.hint_locations[hint_key]

                    # Check if we have hint data using the wrinkly door location ID as key (like BT client)
                    hints_data = self.slot_data.get("hints", {})
                    hint_data = hints_data.get(str(wrinkly_door_id), None)

                    if hint_data:
                        # Use hint data if available
                        if hint_data.get("should_add_hint") and hint_data.get("location_id") is not None and hint_data.get("location_player_id") is not None:

                            # Get the actual location and player from hint data
                            actual_location_id = hint_data["location_id"]
                            finding_player_id = hint_data["location_player_id"]

                            logger.debug(f"Creating hint for location {actual_location_id} owned by player {finding_player_id}")

                            # Create hint parameters
                            params = CreateHintsParams(actual_location_id, finding_player_id)
                            if params not in self.handled_scouts:
                                # Collect params for batch processing
                                if not hasattr(self, "create_hints_params"):
                                    self.create_hints_params = []
                                self.create_hints_params.append(params)
                            else:
                                logger.debug(f"Hint params already handled: {params}")
                        else:
                            logger.debug(f"Hint data validation failed for location {wrinkly_door_id}")
                    else:
                        logger.debug(f"No hint data found for wrinkly door location {wrinkly_door_id}")
                else:
                    logger.warning(f"No hint location mapping found for {kong_name} in {level_name}")
            else:
                logger.warning(f"Invalid hint position: kong={kong}, level={level}")
        except Exception as e:
            logger.error(f"Error handling hint access: {e}")

    async def process_hint_params(self):
        """Process collected hint parameters and send them to the server."""
        if hasattr(self, "create_hints_params") and self.create_hints_params:
            for params in self.create_hints_params:
                await self.send_msgs([{"cmd": "CreateHints", "locations": [params.location], "player": params.player}])
                self.handled_scouts.append(params)
            self.create_hints_params.clear()

    async def run_game_loop(self):
        """Run the game loop."""

        async def victory():
            """Handle a victory."""
            await self.send_victory()

        async def ring_link():
            """Handle a ring link."""
            await self.handle_ring_link()

        async def tag_link():
            """Handle a tag link."""
            await self.handle_tag_link()

        async def trap_link():
            """Handle a trap link."""
            await self.handle_trap_link()

        async def deathlink():
            """Handle a deathlink."""
            await self.send_deathlink()

        async def map_change(map_id):
            """Send a current map id on map change."""
            await self.send_msgs([{"cmd": "Set", "key": f"DK64Rando_{self.team}_{self.slot}_map", "default": hex(0), "want_reply": False, "operations": [{"operation": "replace", "value": map_id}]}])

        async def hint_accessed(kong, level):
            """Handle when a hint is accessed in-game."""
            await self.handle_hint_accessed(kong, level)

        def on_item_get(dk64_checks):
            """Handle an item get."""
            built_checks_list = []
            for check in dk64_checks:
                check_name = check_id_to_name.get(check)
                if check_name:
                    built_checks_list.append(check)
                    continue
                item = item_ids.get(check)
                if item:
                    built_checks_list.append(check)
            self.new_checks(built_checks_list)

        # yield to allow UI to start
        await asyncio.sleep(0)
        while True:
            await asyncio.sleep(3)

            try:
                if not self.client.stop_bizhawk_spam:
                    logger.info("(Re)Starting game loop")
                # On restart of game loop, clear all checks, just in case we swapped ROMs
                # this isn't totally neccessary, but is extra safety against cross-ROM contamination
                self.reset_checks()
                await self.client.wait_for_pj64()

                async def disconnect_check():
                    if self.auth and self.client.auth != self.auth:
                        self.auth = self.client.auth
                        # It would be neat to reconnect here, but connection needs this loop to be running
                        logger.info("Detected new ROM, disconnecting...")
                        await self.disconnect()

                while self.auth is None:
                    await self.client.validate_client_connection()
                    await self.client.reset_auth()
                    await disconnect_check()
                    await asyncio.sleep(3)

                if not self.client.recvd_checks:
                    logger.info("No checks received yet, requesting...")
                    await self.sync()

                await asyncio.sleep(1.0)
                while True:
                    logger.debug("Game loop tick")
                    await self.client.reset_auth()
                    await disconnect_check()
                    await self.client.validate_client_connection()
                    if await self.client.is_victory(self.slot_data.get("win_condition_item", 0), self.slot_data.get("helm_hurry", False)):
                        await victory()
                    status = self.client.check_safe_gameplay()
                    if status is False:
                        await asyncio.sleep(0.5)
                        continue
                    await self.client.main_tick(on_item_get, deathlink, map_change, ring_link, tag_link, trap_link, hint_accessed)
                    await asyncio.sleep(0.5)
                    now = time.time()
                    if self.last_resend + 0.5 < now:
                        self.last_resend = now
                        await self.send_checks()
                    await self.process_hint_params()
                    if self.client.should_reset_auth:
                        self.client.should_reset_auth = False
                        raise Exception("Resetting due to wrong archipelago server")
            # There is 100% better ways to handle this exception, but for now this will do to allow us to exit the loop
            except Exception as e:
                print(e)
                logger.error(f"Exception in game loop: {e}")
                await asyncio.sleep(1.0)


def launch():
    """Launch the DK64 client."""

    async def main():
        """Entrypoint of codebase."""
        parser = get_base_parser(description="Donkey Kong 64 Client.")
        parser.add_argument("--url", help="Archipelago connection url")

        args = parser.parse_args()
        check_version()

        ctx = DK64Context(args.connect, args.password)
        ctx.items_handling = 0b001
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        ctx.la_task = create_task_log_exception(ctx.run_game_loop())
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    colorama.init()
    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch()
