import os
import asyncio
from typing import List

import pymem

import ModuleUpdate
from Utils import async_start

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop, ClientCommandProcessor, handle_url_arg
from typing import Dict

from .Items import item_data_table, inv_item_table
from.Locations import location_data_table

tracker_loaded = False

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor
    CommonContext = TrackerGameContext
    ClientCommandProcessor = TrackerCommandProcessor
    tracker_loaded = True
except ModuleNotFoundError:
    pass

ModuleUpdate.update()

class LRFF13StateCache:
    def __init__(self):
        self.in_main_menu = True
        self.key_items: Dict[str, int] = {}
        self.key_items_addresses: Dict[str, int] = {}
        self.max_ep : int = 0
        self.rando_multi_name_address : int | None = None
        self.rando_multi_item_address : int | None = None
        self.rando_multi_item : str = None
        self.rando_multi_count_address : int | None = None
        self.rando_multi_count : int = 0
        self.in_normal_menu : bool = True


class LRFF13CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)


class LRFF13Context(CommonContext):
    command_processor = LRFF13CommandProcessor
    game = "Lightning Returns: Final Fantasy XIII"
    # Indicates you get items sent from other worlds.
    items_handling = 0b111
    tags = ["AP"]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.server_connected = False
        self.lr_connected = False
        self.lr_game = None
        self.slot_data = None
        self.game_state_cache = LRFF13StateCache()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.server_connected = False
        self.lr_connected = False
        self.game_state_cache = LRFF13StateCache()
        await super(LRFF13Context, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.server_connected = False
        self.lr_connected = False
        self.lr_game = None
        self.game_state_cache = LRFF13StateCache()
        await super(LRFF13Context, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super().shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            # Request data package for LRFF13
            asyncio.create_task(self.send_msgs([
                {"cmd": "GetDataPackage", "games": [self.game]}
            ]))
            # Track checked locations from server
            self.locations_checked = set(args.get("checked_locations", []))
            self.slot_data = args.get("slot_data", {})

        if cmd in {"RoomUpdate"}:
            self.find_game()
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            self.find_game()
            self.server_connected = True
            asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}]))

        super().on_package(cmd, args)

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class LRFF13Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago LRFF13 Client"

        self.ui = LRFF13Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")     

    # Helpers for reading memory
    def read_u64(self, addr: int, use_base: bool = True) -> int:
        if use_base:
            return self.lr_game.read_ulong(self.lr_game.base_address + addr)
        else:
            return self.lr_game.read_ulong(addr)
        
    def read_u32(self, addr: int, use_base: bool = True) -> int:
        if use_base:
            return self.lr_game.read_uint(self.lr_game.base_address + addr)
        else:
            return self.lr_game.read_uint(addr)
        
    def write_u32(self, addr: int, value: int, use_base: bool = True) -> None:
        if use_base:
            self.lr_game.write_uint(self.lr_game.base_address + addr, value)
        else:
            self.lr_game.write_uint(addr, value)

    def read_byte(self, addr: int, use_base: bool = True) -> int:
        if use_base:
            return int.from_bytes(self.lr_game.read_bytes(self.lr_game.base_address + addr, 1))
        else:
            return int.from_bytes(self.lr_game.read_bytes(addr, 1))
        
    def write_byte(self, addr: int, value: int, use_base: bool = True) -> None:
        if use_base:
            self.lr_game.write_bytes(self.lr_game.base_address + addr, bytes([value]), 1)
        else:
            self.lr_game.write_bytes(addr, bytes([value]), 1)

    def read_string(self, addr: int, max_len: int, use_base: bool = True) -> str:
        if use_base:
            return self.lr_game.read_string(self.lr_game.base_address + addr, max_len)
        else:
            return self.lr_game.read_string(addr, max_len)   
        
    def write_string(self, addr: int, value: str, use_base: bool = True, null_extra_length = -1) -> None:
        if null_extra_length >= 0:
            value = value + ("\0" * (null_extra_length - len(value)))
        if use_base:
            self.lr_game.write_string(self.lr_game.base_address + addr, value)
        else:
            self.lr_game.write_string(addr, value)

    def find_game(self):
        if not self.lr_connected:
            try:
                self.lr_game = pymem.Pymem(process_name="LRFF13")
                logger.info("You are now auto-tracking")
                self.lr_connected = True
            except Exception:
                if self.lr_connected:
                    self.lr_connected = False
                logger.info("Game is not open (Try running the client as an admin if already open).")

    def get_ap_num_collected(self) -> int:
        total = 0
        mult = 1
        for i in range(3):
            key = f"key_r_multi_{i}"
            count = self.game_state_cache.key_items.get(key, 0)
            if count > 0:
                count -= 1
            total += count * mult
            mult *= 50
        return total
    
    def set_ap_num_collected(self, num: int) -> None:
        if num < 0:
            num = 0
        elif num > 124999:
            num = 124999
        for i in range(3):
            key = f"key_r_multi_{i}"
            count = (num % 50) + 1
            self.game_state_cache.key_items[key] = count
            # Write to memory
            if key in self.game_state_cache.key_items_addresses:
                self.write_byte(self.game_state_cache.key_items_addresses[key] + 18, count, False)
            num //= 50

    async def give_items(self):
        if not self.lr_connected:
            return

        if self.game_state_cache.in_main_menu:
            # Reset rando_multi item and count values if they are different
            if self.game_state_cache.rando_multi_item != "rando_multi_item":
                self.write_string(self.game_state_cache.rando_multi_item_address, "rando_multi_item", False)
            if self.game_state_cache.rando_multi_count != 32500:
                self.write_u32(self.game_state_cache.rando_multi_count_address, 32500, False)
            return
        
        try:
            if not self.game_state_cache.in_main_menu and not self.game_state_cache.in_normal_menu:
                # Send the next item in items_received using the index from get_ap_num_collected
                ap_num_collected = self.get_ap_num_collected()
                received : List[NetworkItem] = self.items_received
                if ap_num_collected < len(received) and (self.game_state_cache.key_items.get("key_r_added", 0) > 0) and self.game_state_cache.key_items.get("key_r_multi_0", 0) > 0 and self.game_state_cache.key_items.get("key_r_multi_1", 0) > 0 and self.game_state_cache.key_items.get("key_r_multi_2", 0) > 0:
                    item = received[ap_num_collected]
                    if item.item in inv_item_table:
                        item_name = inv_item_table[item.item]
                        item_info = item_data_table[item_name]

                        # Only write the item if it is not an initial garb item
                        if item_name not in self.slot_data.get("initial_equipment", []):
                            # Write the item name and set count to the item amount
                            self.write_string(self.game_state_cache.rando_multi_item_address, item_info.str_id, False, 16)
                            self.write_u32(self.game_state_cache.rando_multi_count_address, item_info.amount, False)

                            # Set the key_r_added to 0 to indicate the game can add the item now
                            self.game_state_cache.key_items["key_r_added"] = 0
                            if "key_r_added" in self.game_state_cache.key_items_addresses:
                                self.write_byte(self.game_state_cache.key_items_addresses["key_r_added"] + 18, 0, False)
                        else:
                            # Skip this item and mark it as collected
                            self.set_ap_num_collected(ap_num_collected + 1)
                            

                        # logger.debug(f"Received {item_name}.")
                # After loading a save, it's possible it's in a state where key_r_added is 0 but no item is set to be added
                elif self.game_state_cache.key_items.get("key_r_added", 0) == 0 and self.game_state_cache.rando_multi_count == 32500 and self.game_state_cache.key_items.get("key_r_multi_0", 0) > 0 and self.game_state_cache.key_items.get("key_r_multi_1", 0) > 0 and self.game_state_cache.key_items.get("key_r_multi_2", 0) > 0:
                    # Set key_r_added to 1
                    if "key_r_added" in self.game_state_cache.key_items:
                        self.game_state_cache.key_items["key_r_added"] = 1
                        if "key_r_added" in self.game_state_cache.key_items_addresses:
                            self.write_byte(self.game_state_cache.key_items_addresses["key_r_added"] + 18, 1, False)

        except Exception as e:
            if self.lr_connected:
                self.lr_connected = False
            logger.info(e)

    async def lrff13_check_locations(self):
        if self.game_state_cache.in_main_menu and not self.game_state_cache.in_normal_menu or not self.lr_connected:
            return        
        
        # Victory, check if the key item key_r_victory is present
        if self.game_state_cache.key_items.get("key_r_victory", 0) > 0 and not self.finished_game:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True

        locations : List[int] = []

        # Always include initial 3rd garb locations as
        # these are the initial garb equipment and not actually given as items
        initial_garb_names = ["Ark - Initial 3rd Garb (1)", "Ark - Initial 3rd Garb (2)", "Ark - Initial 3rd Garb (3)"]
        locations.extend([location_data_table[name].address for name in initial_garb_names if location_data_table[name].address not in self.locations_checked])

        # Check for checked locations and mark them as checked in-game
        try:
            # Loop key items and check if their count is < 50
            # if so, get index from the name key_r_ap_#### and get the location at that index
            items = list(self.game_state_cache.key_items.items())
            for idx in range(len(items)):
                name, count = items[idx]
                if name.startswith("key_r_ap_") and count < 50:
                    index_str = name[len("key_r_ap_"):]
                    if index_str.isdigit():
                        index = int(index_str)
                        # Set count to 75 to mark as checked
                        self.write_byte(self.game_state_cache.key_items_addresses[name] + 18, 75, False)

                        if index not in self.locations_checked:
                            locations.append(index)

            await self.check_locations(locations)
        except Exception as e:
            if self.lr_connected:
                self.lr_connected = False
            logger.info(e)

    async def update_game_state_cache(self):
        if not self.lr_connected:
            return
        
        new_cache = LRFF13StateCache()
        try:
            p_stats_base = self.read_u64(0x4CF79D8)
            if not p_stats_base:
                return

            new_cache.max_ep = round(self.read_u64(p_stats_base + 0x2884, False) / 2000)
            new_cache.in_main_menu = (new_cache.max_ep == 500000)
            
            # Normal menu address
            temp_ptr = self.read_u64(0x4CF19FC, True)
            temp_ptr = self.read_u64(temp_ptr + 0x8, False)
            temp_ptr = self.read_u64(temp_ptr + 0x8, False)
            temp_ptr = self.read_u64(temp_ptr + 0x80, False)
            temp_ptr = self.read_u64(temp_ptr + 0x4, False)
            temp_ptr = self.read_u64(temp_ptr + 0x14, False)
            temp_ptr = self.read_u64(temp_ptr + 0xB0, False)
            new_cache.in_normal_menu = (self.read_byte(temp_ptr + 0xB60, False) != 3)

            if not new_cache.in_main_menu:
                # Read entries until we hit an empty name or 200 entries
                key_items_ptr = self.read_u64(p_stats_base + 0x1418 + 0x174, False)
                try:
                    key_items: Dict[str, int] = {}
                    key_items_addresses: Dict[str, int] = {}
                    for i in range(200):
                        entry = key_items_ptr + (24 * i)
                        name = self.read_string(entry, 16, False)
                        if not name or name == "":
                            continue
                        count = self.read_byte(entry + 18, False)
                        if name and name != "":
                            key_items[name] = count
                            key_items_addresses[name] = entry

                    # Store into cache without replacing the cache object
                    new_cache.key_items = key_items
                    new_cache.key_items_addresses = key_items_addresses
                except Exception as e:
                    if self.lr_connected:
                        self.lr_connected = False
                    logger.info(e)

            # Calculate and cache the ran_multi/rando_multi addresses (treasure strings block)
            # Only scan if we don't already have it
            if (not self.game_state_cache.rando_multi_item_address
                or not self.game_state_cache.rando_multi_name_address
                or not self.game_state_cache.rando_multi_count_address):
                ptr1 = self.read_u64(0x4CF896C, True)
                ptr2 = self.read_u64(ptr1 + 0x4, False)
                ptr3 = self.read_u64(ptr2 + 0x310, False)
                treasures_start_ptr = self.read_u64(ptr3 + 0x1C, False)

                name_addr = self.game_state_cache.rando_multi_name_address or 0
                item_addr = self.game_state_cache.rando_multi_item_address or 0
                if treasures_start_ptr and (not name_addr or not item_addr):
                    for i in range(50000):
                        try:
                            addr = treasures_start_ptr + i
                            byteTest = self.read_byte(addr, False)
                            first_char = self.read_string(addr, 1, False)
                            if first_char != "r":
                                continue
                            s = self.read_string(addr, 16, False)
                            if s == "ran_multi":
                                name_addr = addr
                            elif s == "rando_findstring":
                                item_addr = addr
                            if name_addr and item_addr:
                                break
                        except Exception:
                            continue

                new_cache.rando_multi_name_address = name_addr
                # Special case for the item address, as we use the findstring before the actual item data
                # This prevents issues where the client needs to restart but the item data changed
                new_cache.rando_multi_item_address = item_addr + 16 + 1

                # Using the ran_multi name address, read pointer at +16 for the count (where 9999 is written)
                if name_addr:
                    try:
                        new_cache.rando_multi_count_address = self.read_u64(name_addr + 16, False) or 0
                    except Exception:
                        new_cache.rando_multi_count_address = 0
            else:
                new_cache.rando_multi_name_address = self.game_state_cache.rando_multi_name_address
                new_cache.rando_multi_item_address = self.game_state_cache.rando_multi_item_address
                new_cache.rando_multi_count_address = self.game_state_cache.rando_multi_count_address

            new_cache.rando_multi_item = self.read_string(new_cache.rando_multi_item_address, 16, False) if new_cache.rando_multi_item_address else None
            new_cache.rando_multi_count = self.read_u32(new_cache.rando_multi_count_address, False) if new_cache.rando_multi_count_address else 0

            ## # Log key items list for debugging
            ## logger.info(f"LRFF13: Key Items: {new_cache.key_items}")
            ## logger.info(f"LRFF13: Max EP: {new_cache.max_ep}")
            ## # Log the rando_multi item current value and the count
            ## logger.info(f"LRFF13: Rando Multi Item: {new_cache.rando_multi_item}")
            ## logger.info(f"LRFF13: Rando Multi Count: {new_cache.rando_multi_count}")

            self.game_state_cache = new_cache
        except Exception as e:
            if self.lr_connected:
                self.lr_connected = False
            logger.info(e)


async def lrff13_watcher(ctx: LRFF13Context):
    while not ctx.exit_event.is_set():
        try:
            if ctx.lr_connected and ctx.server_connected:
                await ctx.update_game_state_cache()
                await ctx.lrff13_check_locations()
                await ctx.give_items()
            elif not ctx.lr_connected and ctx.server_connected:
                logger.info("Game Connection lost. Disconnecting...")
                ctx.lr_game = None
                await ctx.disconnect()
        except Exception as e:
            if ctx.lr_connected:
                ctx.lr_connected = False
            logger.info(e)
        await asyncio.sleep(0.5)


def launch(*launch_args):
    async def main(args_in):
        ctx = LRFF13Context(args_in.connect, args_in.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            lrff13_watcher(ctx), name="LRFF13ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Lightning Returns: Final Fantasy XIII Client, for text interfacing.")
    parser.add_argument("url", default="", type=str, nargs="?", help="Archipelago connection url")

    args, rest = parser.parse_known_args(launch_args)
    args = handle_url_arg(args, parser)
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
