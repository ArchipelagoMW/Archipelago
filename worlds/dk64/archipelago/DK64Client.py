"""Donkey Kong 64 client for Archipelago."""

import ModuleUpdate

ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("DK64Context", exception_logger="Client")
import json
import asyncio
import colorama
import sys
import random
import traceback

import time
import typing
from client.common import DK64MemoryMap, create_task_log_exception, check_version
from client.pj64 import PJ64Client
from client.items import item_ids, item_names_to_id
from client.check_flag_locations import location_flag_to_name, location_name_to_flag
from client.ap_check_ids import check_id_to_name, check_names_to_id
from CommonClient import CommonContext, get_base_parser, gui_enabled, logger, server_loop, ClientCommandProcessor
from NetUtils import ClientStatus
from ap_version import version as ap_version


class DK64Client:
    """Client for Donkey Kong 64."""

    n64_client = None
    tracker = None
    game = None
    auth = None
    locations_scouted = {}
    recvd_checks = {}
    pending_checks = []
    players = None
    stop_bizhawk_spam = False
    remaining_checks = []
    flag_lookup = None
    seed_started = False
    sent_checks = []
    item_names = None
    memory_pointer = None
    _purchase_cache = {}
    deathlink_debounce = True
    pending_deathlink = False
    send_mode = 1
    ENABLE_DEATHLINK = False
    ENABLE_RINGLINK = False
    ENABLE_TAGLINK = False
    current_speed = 130
    current_map = 0

    async def wait_for_pj64(self):
        """Wait for PJ64 to connect to the game."""
        clear_waiting_message = True
        if not self.stop_bizhawk_spam:
            logger.info("Waiting on connection to PJ64...")
            self.n64_client = PJ64Client()
            self.stop_bizhawk_spam = True
        while True:
            try:
                socket_connected = False
                valid_rom = self.n64_client.validate_rom(self.game, DK64MemoryMap.memory_pointer)
                if self.n64_client.socket is not None and not socket_connected:
                    logger.info("Connected to PJ64")
                    socket_connected = True
                while not valid_rom:
                    if self.n64_client.socket is not None and not socket_connected:
                        logger.info("Connected to PJ64")
                        socket_connected = True
                    if clear_waiting_message:
                        logger.info("Waiting on valid ROM...")
                        clear_waiting_message = False
                    await asyncio.sleep(1.0)
                    valid_rom = self.n64_client.validate_rom(self.game, DK64MemoryMap.memory_pointer)
                self.stop_bizhawk_spam = False
                logger.info("PJ64 Connected to ROM!")
                return
            except (BlockingIOError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)
                logger.error("Error connecting to PJ64, retrying...")
                pass

    def check_safe_gameplay(self):
        """Check if the game is in a valid state for sending items."""
        current_gamemode = self.n64_client.read_u8(DK64MemoryMap.CurrentGamemode)
        next_gamemode = self.n64_client.read_u8(DK64MemoryMap.NextGamemode)
        return current_gamemode in [6, 0xD] and next_gamemode in [6, 0xA, 0xD]

    def safe_to_send(self):
        """Check if it's safe to send an item."""
        countdown_value = self.n64_client.read_u8(self.memory_pointer + DK64MemoryMap.safety_text_timer)
        return countdown_value == 0

    async def validate_client_connection(self):
        """Validate the client connection."""
        if not self.memory_pointer:
            self.memory_pointer = self.n64_client.read_u32(DK64MemoryMap.memory_pointer)
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.connection, 0xFF)

    def send_message(self, item_name, player_name, event_type="from"):
        """Send a message to the game."""

        def sanitize_and_trim(input_string, max_length=0x20):
            sanitized = "".join(e for e in input_string if e.isalnum() or e == " ").strip()
            return sanitized[:max_length]

        stripped_item_name = sanitize_and_trim(item_name)
        stripped_player_name = sanitize_and_trim(player_name)
        self.n64_client.write_bytestring(self.memory_pointer + DK64MemoryMap.fed_string, f"{stripped_item_name}")
        self.n64_client.write_bytestring(self.memory_pointer + DK64MemoryMap.fed_subtitle, f"{event_type} {stripped_player_name}")

    def set_speed(self, speed: int):
        """Set the speed of the display text in game."""
        self.n64_client.write_u8(self.memory_pointer + DK64MemoryMap.text_timer, speed)

    async def recved_item_from_ap(self, item_id, item_name, from_player, index):
        """Handle an item received from Archipelago."""
        # Don't allow getting an item until you've got your first check
        if not self.started_file():
            return

        # Spin until we either:
        # get an exception from a bad read (emu shut down or reset)
        # beat the game
        # the client handles the last pending item
        status = self.safe_to_send()
        while not status:
            await asyncio.sleep(0.1)
            status = self.safe_to_send()
        next_index = index + 1
        item_data = item_ids.get(item_id)
        if item_data:
            if self.send_mode == 6:
                if self.current_speed != 130:
                    self.set_speed(130)
                    self.current_speed = 130
                # Progression only, no speed changes
                if item_data.get("progression", False):
                    self.send_message(item_name, from_player, "from")
            elif self.send_mode == 5:
                if self.current_speed != 130:
                    self.set_speed(130)
                    self.current_speed = 130
                # Extended whitelist, no speed changes
                if item_data.get("progression", False):
                    self.send_message(item_name, from_player, "from")
                elif item_data.get("extended_whitelist", False):
                    self.send_message(item_name, from_player, "from")
            elif self.send_mode == 4:
                # Display both default and extended whitelist items
                # But display just the extended whitelist items at a faster speed
                if item_data.get("progression", False):
                    if self.current_speed != 130:
                        self.set_speed(130)
                        self.current_speed = 130
                    self.send_message(item_name, from_player, "from")
                elif item_data.get("extended_whitelist", False):
                    if self.current_speed != 50:
                        self.set_speed(50)
                        self.current_speed = 50
                    self.send_message(item_name, from_player, "from")
            elif self.send_mode == 3:
                # Send everything super fast on both whitelist and extended whitelist
                if self.current_speed != 50:
                    self.current_speed = 50
                    self.set_speed(50)
                if item_data.get("progression", False):
                    self.send_message(item_name, from_player, "from")
                elif item_data.get("extended_whitelist", False):
                    self.send_message(item_name, from_player, "from")
            elif self.send_mode == 2:
                # If we have more than 5 items queued, from 130 to 50, do a percentage of the total items
                # But only display progression items, discard the rest
                length = len(self.pending_checks) - index
                if length <= 5:
                    if self.current_speed != 130:
                        self.current_speed = 130
                        self.set_speed(130)
                    if item_data.get("progression", False):
                        self.send_message(item_name, from_player, "from")
                    elif item_data.get("extended_whitelist", False):
                        self.send_message(item_name, from_player, "from")
                else:
                    speed = round(130 - (80 / length))
                    if speed < 50:
                        speed = 50
                    if self.current_speed != speed:
                        self.current_speed = speed
                        self.set_speed(speed)
                    if item_data.get("progression", False):
                        self.send_message(item_name, from_player, "from")
            elif self.send_mode == 1:
                # If we have more than 5 items queued, from 130 to 50, do a percentage of the total items
                # If we have 5 or less, do 130
                length = len(self.pending_checks) - index
                if length <= 5:
                    if self.current_speed != 130:
                        self.current_speed = 130
                        self.set_speed(130)
                else:
                    speed = round(130 - (80 / length))
                    if speed < 50:
                        speed = 50
                    if self.current_speed != speed:
                        self.current_speed = speed
                        self.set_speed(speed)
                if item_data.get("progression", False):
                    self.send_message(item_name, from_player, "from")
                elif item_data.get("extended_whitelist", False):
                    self.send_message(item_name, from_player, "from")
            else:
                raise Exception("Invalid message mode")

            if item_data.get("flag_id", None) is not None:
                self.setFlag(item_data.get("flag_id"))
            elif item_data.get("fed_id", None) is not None:
                await self.writeFedData(item_data.get("fed_id"))
            else:
                logger.warning(f"Item {item_name} has no flag or fed id")
        self.n64_client.write_u16(self.memory_pointer + DK64MemoryMap.counter_offset, next_index)

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

    def _build_flag_lookup(self):
        """Cache flag mappings to avoid repeated reads."""
        # Verify if the lookup table is already built, and that we've checked some locations
        if self.flag_lookup is not None:
            return
        self.flag_lookup = {}
        for flut_index in range(0x400):
            raw_flag = self.n64_client.read_u16(0x807E2EE0 + (4 * flut_index))
            if raw_flag == 0xFFFF:
                break
            target_flag = self.n64_client.read_u16(0x807E2EE0 + (4 * flut_index) + 2)
            self.flag_lookup[raw_flag] = target_flag

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

    def getCheckStatus(self, check_type, flag_index=None, shop_index=None, level_index=None, kong_index=None, _bulk_read_dict={}) -> bool:
        """Get the status of a check."""
        # shop_index: 0 = cranky, 1 = funky, 2 = candy, 3 = bfi
        # flag_index: as expected
        if check_type == "shop":
            cache_key = (shop_index, kong_index, level_index)
            if cache_key in self._purchase_cache:
                # Retrieve cached values
                purchase_type, purchase_value, purchase_kong = self._purchase_cache[cache_key]
            else:
                # Calculate header and read values
                if shop_index == 3:
                    header = 0x807FF6E8
                else:
                    header = 0x807FF400 + (shop_index * 0xF0) + (kong_index * 0x30) + (level_index * 6)
                purchase_type = self.n64_client.read_u16(header + 0)
                purchase_value = self.n64_client.read_u16(header + 2)
                purchase_kong = self.n64_client.read_u8(header + 4)
                # Cache the values
                self._purchase_cache[cache_key] = (purchase_type, purchase_value, purchase_kong)

            return self._getShopStatus(purchase_type, purchase_value, purchase_kong)
        else:
            self._build_flag_lookup()
            # Check if the flag exists in the lookup table
            if self.flag_lookup.get(flag_index):
                target_flag = self.flag_lookup[flag_index]
                if target_flag & 0x8000:
                    return self.getMoveStatus(target_flag)
                elif target_flag == 0xFFFE:
                    has_camera = self.readFlag(0x2FD) != 0
                    has_shockwave = self.readFlag(0x179) != 0
                    return has_camera and has_shockwave
                return _bulk_read_dict.get(target_flag) != 0
            else:
                return _bulk_read_dict.get(flag_index) != 0

    def bulk_lookup(self, flag_index, _bulk_read_dict):
        """Bulk lookup of flags."""
        self._build_flag_lookup()
        if self.flag_lookup.get(flag_index):
            target_flag = self.flag_lookup[flag_index]
            byte_index = target_flag >> 3
            offset = DK64MemoryMap.EEPROM + byte_index
            _bulk_read_dict[target_flag] = offset
        else:
            byte_index = flag_index >> 3
            offset = DK64MemoryMap.EEPROM + byte_index
            _bulk_read_dict[flag_index] = offset

    async def readChecks(self, cb):
        """Run checks in parallel using asyncio."""
        new_checks = []
        _bulk_read_dict = {}
        for id in self.remaining_checks:
            name = check_id_to_name.get(id)
            # Try to get the check via location_name_to_flag
            check = location_name_to_flag.get(name)
            if check:
                self.bulk_lookup(check, _bulk_read_dict)
            # If its not there using the id lets try to get it via item_ids
            else:
                check = item_ids.get(id)
                if check:
                    flag_id = check.get("flag_id")
                    if not flag_id:
                        # logger.error(f"Item {name} has no flag_id")
                        continue
                    else:
                        self.bulk_lookup(flag_id, _bulk_read_dict)
        dict_data = self.n64_client.read_dict(_bulk_read_dict)
        # Json loads the dict_data
        dict_data = json.loads(dict_data)
        # For each item in the dict, the key is the index the value is the val for byte_shift. Keep the key the same but set the value to the result of byte_shift
        for key, val in dict_data.items():
            shift = int(key) & 7
            flag_status = (int(val[0]) >> shift) & 1
            _bulk_read_dict[int(key)] = flag_status
        for id in self.remaining_checks[:]:
            name = check_id_to_name.get(id)
            # Try to get the check via location_name_to_flag
            check = location_name_to_flag.get(name)
            if check:
                # Assuming we did find it in location_name_to_flag
                check_status = self.getCheckStatus("location", check, _bulk_read_dict=_bulk_read_dict)
                if check_status:
                    # logger.info(f"Found {name} via location_name_to_flag")
                    self.remaining_checks.remove(id)
                    new_checks.append(id)
                    if self.locations_scouted.get(id):
                        self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))
            # If its not there using the id lets try to get it via item_ids
            else:
                # If the content is 3 parts separated by a space, we can assume it's a shop check
                content = name.split(" ")
                if name == "The Banana Fairy's Gift":
                    check_status = self.getCheckStatus("shop", None, 3, None, None)
                    if check_status:
                        # logger.info(f"Found {name} via location_name_to_flag")
                        self.remaining_checks.remove(id)
                        new_checks.append(id)
                        if self.locations_scouted.get(id):
                            self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))
                    continue
                elif ("Cranky" in name or "Candy" in name or "Funky" in name) and len(content) == 3:
                    level_mapping = {"Japes": 0, "Aztec": 1, "Factory": 2, "Galleon": 3, "Forest": 4, "Caves": 5, "Castle": 6, "Isles": 7}
                    shop_mapping = {"Cranky": 0, "Funky": 1, "Candy": 2}
                    kong_mapping = {"Donkey": 0, "Diddy": 1, "Lanky": 2, "Tiny": 3, "Chunky": 4}

                    level_index = level_mapping.get(content[0])
                    shop_index = shop_mapping.get(content[1])
                    kong_index = kong_mapping.get(content[2])

                    # If any of these are not set, continue
                    if level_index is None or shop_index is None or kong_index is None:
                        continue

                    check_status = self.getCheckStatus("shop", None, shop_index, level_index, kong_index)
                    if check_status:
                        # print(f"Found {name} via shop check")
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
                            check_status = self.getCheckStatus("location", flag_id, _bulk_read_dict=_bulk_read_dict)
                            if check_status:
                                # logger.info(f"Found {name} via item_ids")
                                self.remaining_checks.remove(id)
                                new_checks.append(id)
                                if self.locations_scouted.get(id):
                                    self.sent_checks.append((self.locations_scouted.get(id).get("item_name"), self.locations_scouted.get(id).get("player")))

        if new_checks:
            cb(new_checks)
        return True

    async def reset_auth(self):
        """Reset the auth by looking up a username from ROM."""
        username = self.n64_client.read_bytestring(0x1FF3000 + 0xB0000000, 16).strip()
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

    async def wait_for_game_ready(self):
        """Wait for the game to be ready."""
        logger.info("Waiting on game to be in valid state...")
        while not self.check_safe_gameplay():
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise Exception("Resetting due to wrong archipelago server")
        logger.info("Game connection ready!")

    async def is_victory(self):
        """Check if the game is in a victory state."""
        return self.readFlag(DK64MemoryMap.end_credits) == 1

    async def get_current_map(self):
        """Get the current map."""
        return self.n64_client.read_u32(DK64MemoryMap.current_map)

    def get_current_deliver_count(self):
        """Get the current deliver count."""
        data = self.n64_client.read_u16(self.memory_pointer + DK64MemoryMap.counter_offset)
        # If our data is too high, (Above 10000) we need to reset it
        if data > 10000:
            # Try reading again
            data = self.n64_client.read_u16(self.memory_pointer + DK64MemoryMap.counter_offset)
            # If its still too high, raise an exception
            if data > 10000:
                return None
            else:
                return data
        return data

    async def main_tick(self, item_get_cb, deathlink_cb, map_change_cb, ring_link, tag_link):
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
        current_deliver_count = self.get_current_deliver_count()
        # If current_deliver_count is None
        if current_deliver_count is None:
            return

        if current_deliver_count > 10000:
            logger.info(f"Current deliver count: {current_deliver_count}")
            logger.info(f"Recieved checks: {len(self.recvd_checks)}")
            logger.info(f"Pending checks: {len(self.pending_checks)}")
            logger.info("Current deliver count is too high, PLEASE REPORT THIS TO THE DK64 TEAM")
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
    command_processor = DK64CommandProcessor
    won = False

    def reset_checks(self):
        """Reset the checks."""
        self.remaining_checks = list(check_id_to_name.keys()).copy()
        self.client.remaining_checks = self.remaining_checks
        self.client.recvd_checks = {}
        self.client.pending_checks = []
        self.found_checks = []
        self.client.flag_lookup = None

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
                ("Tracker", "Tracker"),
            ]
            base_title = f"Archipelago Donkey Kong 64 Client (Version {ap_version})"

            def build(self):
                b = super().build()
                return b

        self.ui = DK64Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def send_checks(self):
        """Send the checks to the server."""
        message = [{"cmd": "LocationChecks", "locations": self.found_checks}]
        await self.send_msgs(message)

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
            if self.slot_data.get("Version"):
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
            if self.slot_data.get("receive_notifications"):
                self.client.send_mode = self.slot_data.get("receive_notifications")
            self.client.players = self.player_names
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
                # Using item_names_to_id get the kong flag_id
                number_map = {
                    0: "Donkey",
                    1: "Diddy",
                    2: "Lanky",
                    3: "Tiny",
                    4: "Chunky",
                }
                kong_name = None
                kong_key = number_map.get(kong, None)
                if kong_key is not None:
                    kong_id = item_names_to_id.get(kong_key, None)
                    if kong_id is not None:
                        kong_name = item_ids.get(kong_id, None)
                invalid_kong = True
                # Read the flag_id location to see if we have the kong
                if kong_name:
                    kong_flag_id = kong_name.get("flag_id", None)
                    if kong_flag_id is not None:
                        has_kong = self.client.readFlag(kong_flag_id) != 0
                        if has_kong:
                            self.client.n64_client.write_u8(self.client.memory_pointer + DK64MemoryMap.tag_kong, kong)
                            current_kong = kong
                            invalid_kong = False
                if invalid_kong:
                    # Check if we have any kong not our current kong
                    valid_kongs = [current_kong]
                    # Check each int from 0 to 4 excluding current_kong
                    for i in range(5):
                        if i != current_kong:
                            kong_key = number_map.get(i, None)
                            if kong_key:
                                kong_id = item_names_to_id.get(kong_key, None)
                                if kong_id is not None:
                                    kong_name = item_ids.get(kong_id, None)
                            else:
                                kong_name = None
                            if kong_name:
                                kong_flag_id = kong_name.get("flag_id", None)
                                if kong_flag_id:
                                    has_kong = self.client.readFlag(kong_flag_id) != 0
                                    if has_kong:
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

        async def deathlink():
            """Handle a deathlink."""
            await self.send_deathlink()

        async def map_change(map_id):
            """Send a current map id on map change."""
            await self.send_msgs([{"cmd": "Set", "key": f"DK64Rando_{self.team}_{self.slot}_map", "default": hex(0), "want_reply": False, "operations": [{"operation": "replace", "value": map_id}]}])

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
                    await self.sync()

                await asyncio.sleep(1.0)
                while True:
                    await self.client.reset_auth()
                    await disconnect_check()
                    await self.client.validate_client_connection()
                    if await self.client.is_victory():
                        await victory()
                    status = self.client.check_safe_gameplay()
                    if status is False:
                        await asyncio.sleep(0.5)
                        continue
                    await self.client.main_tick(on_item_get, deathlink, map_change, ring_link, tag_link)
                    await asyncio.sleep(1)
                    now = time.time()
                    if self.last_resend + 0.5 < now:
                        self.last_resend = now
                        await self.send_checks()
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
