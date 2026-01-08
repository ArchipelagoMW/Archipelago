"""
Animal Well Archipelago Client
Based (read: copied almost wholesale and edited) off the Zelda1 Client.
"""

import asyncio
import os
import platform
import random
import time
import traceback
import struct
import pymem
import logging
from typing import Dict, Any

from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, get_base_parser
from NetUtils import ClientStatus
import Utils
from settings import get_settings

from .. import AWSettings
from ..items import item_name_to_id, item_name_groups
from ..locations import location_name_to_id, location_table, events_table, ByteSect
from ..names import ItemNames as iname, LocationNames as lname
from ..options import FinalEggLocation, Goal
from ..client.bean_patcher import BeanPatcher
from ..client.logic_tracker import AnimalWellTracker, CheckStatus, candle_event_to_item, candle_locations

CONNECTION_ABORTED_STATUS = "Connection Aborted. Some unrecoverable error occurred."
CONNECTION_REFUSED_STATUS = ("Connection Refused. Likely causes are your game not "
                             "being properly recognized or having multiple instances open.")
CONNECTION_RESET_STATUS = "Connection was reset. Please wait"
CONNECTION_CONNECTED_STATUS = "Connected."
CONNECTION_TENTATIVE_STATUS = "Connection has been initiated."
CONNECTION_INITIAL_STATUS = "Connection has not been initiated."

DEATHLINK_MESSAGE = "The bean has died."
DEATHLINK_RECEIVED_MESSAGE = "{name} died and took you with them."

HEADER_LENGTH = 0x18
SAVE_SLOT_LENGTH = 0x27010
CUSTOM_STAMPS = 255

bean_logger = logging.getLogger("BeanLogger")


class AnimalWellCommandProcessor(ClientCommandProcessor):
    """
    CommandProcessor for Animal Well
    """

    def _cmd_connection(self):
        """Check Animal Well Connection State"""
        if isinstance(self.ctx, AnimalWellContext):
            logger.info(f"Animal Well Connection Status: {self.ctx.connection_status}")

    def _cmd_room_palette(self, val=""):
        """
        Sets an override for room palettes. Accepts a number between 0 and 31, "off" to disable,
        or "random" to pick a room palette at random.
        """
        if isinstance(self.ctx, AnimalWellContext):
            if val == "":
                self.ctx.bean_patcher.toggle_room_palette_override()
            elif val == "off":
                logger.info(f"Disabling room palette...")
                self.ctx.bean_patcher.disable_room_palette_override()
            elif val == "random":
                random_value = random.randrange(0, 31)
                logger.info(f"Randomizing room palette to {random_value}...")
                self.ctx.bean_patcher.enable_room_palette_override(random_value)
            elif val.isnumeric():
                logger.info(f"Enabling room palette {val}...")
                self.ctx.bean_patcher.enable_room_palette_override(int(val))
            else:
                logger.info(f"Enabling room palette 0x14...")
                self.ctx.bean_patcher.enable_room_palette_override(0x14)

    def _cmd_fullbright(self, val=""):
        """
        Toggles fullbright mode, which disabled darkness and lights all tiles equally.
        """
        if isinstance(self.ctx, AnimalWellContext):
            if val == "":
                self.ctx.bean_patcher.toggle_fullbright()
            elif val == "off":
                logger.info(f"Disabling fullbright...")
                self.ctx.bean_patcher.disable_fullbright()
            else:
                logger.info(f"Enabling fullbright...")
                self.ctx.bean_patcher.enable_fullbright()

    def _cmd_goodboy(self, val=""):
        """
        Disables ghost dog contact damage and the looping sound that plays while it's aggro
        """
        if isinstance(self.ctx, AnimalWellContext):
            if val == "":
                self.ctx.bean_patcher.toggle_goodboy()
            elif val == "off":
                logger.info(f"Disabling goodboy...")
                self.ctx.bean_patcher.disable_goodboy()
            else:
                logger.info(f"Enabling goodboy...")
                self.ctx.bean_patcher.enable_goodboy()

    def _cmd_gooddog(self, val=""):
        """
        Alias for /goodboy
        """
        self._cmd_goodboy(val)

    def _cmd_nodog(self, val=""):
        """
        Disables ghost dog entirely
        """
        if isinstance(self.ctx, AnimalWellContext):
            if val == "":
                self.ctx.bean_patcher.toggle_no_dog()
            elif val == "off":
                logger.info(f"Disabling no_dog...")
                self.ctx.bean_patcher.disable_no_dog()
            else:
                logger.info(f"Enabling no_dog...")
                self.ctx.bean_patcher.enable_no_dog()

    def _cmd_noghost(self, val=""):
        """
        Alias for /nodog
        """
        self._cmd_nodog(val)

    def _cmd_alwaysdog(self, val=""):
        """
        Ghost dog hunts you eternally
        """
        if isinstance(self.ctx, AnimalWellContext):
            if val == "":
                self.ctx.bean_patcher.toggle_always_dog()
            elif val == "off":
                logger.info(f"Disabling always_dog...")
                self.ctx.bean_patcher.disable_always_dog()
            else:
                logger.info(f"Enabling always_dog...")
                self.ctx.bean_patcher.enable_always_dog()

    def _cmd_alwaysghost(self, val=""):
        """
        Alias for /alwaysdog
        """
        self._cmd_alwaysdog(val)

    def _cmd_deathlink(self, val=""):
        """
        Toggles deathlink.
        """
        if isinstance(self.ctx, AnimalWellContext):
            death_link_key = f"{self.ctx.slot}|death_link"
            death_link_val = self.ctx.stored_data.get(death_link_key, None)
            try:
                if death_link_val is None:
                    death_link_val = bool(self.ctx.slot_data["death_link"])
                    self.ctx.set_notify(death_link_key)

                if val == "":
                    death_link_val = not death_link_val
                elif val == "off":
                    death_link_val = False
                elif val == "on":
                    death_link_val = True

                status_text = "Deathlink is now " + "ENABLED" if death_link_val else "DISABLED"
                self.ctx.display_text_in_client(status_text)
                logger.info(status_text)

                Utils.async_start(self.ctx.update_death_link(death_link_val))
                Utils.async_start(self.ctx.send_msgs([{
                    "cmd": "Set",
                    "key": death_link_key,
                    "default": None,
                    "want_reply": True,
                    "operations": [{"operation": "replace", "value": death_link_val}]
                }]))
            except KeyError:
                logger.error("Failed to adjust death link setting. If you are not connected to the server, "
                             "please connect before attempting to adjust this.")

    def _cmd_tracker(self, val=""):
        """
        Toggles In-game Tracker or sets specific tracker options.
        """
        if isinstance(self.ctx, AnimalWellContext):
            # get the host.yaml settings for the tracker
            host = get_settings()
            aw_settings = host.animal_well_settings
            tracker_enum = AWSettings.TrackerSetting

            # set a default if the player does not have the animal well settings already
            if host.animal_well_settings.get("in_game_tracker", None) is None:
                aw_settings["in_game_tracker"] = tracker_enum.full_tracker

            if val == "":
                aw_settings["in_game_tracker"] = tracker_enum.no_tracker \
                    if aw_settings["in_game_tracker"] == tracker_enum.full_tracker else tracker_enum.full_tracker
            elif val == "off":
                aw_settings["in_game_tracker"] = tracker_enum.no_tracker
            elif "logic" in val:
                aw_settings["in_game_tracker"] = tracker_enum.no_logic
            elif "check" in val:
                aw_settings["in_game_tracker"] = tracker_enum.checked_only
            elif val == "on":
                aw_settings["in_game_tracker"] = tracker_enum.full_tracker

            try:
                host.save()
            except:
                logger.error("Failed to save Tracker setting. "
                             "This is usually caused by having an apworld in your custom_worlds folder and your "
                             "lib/worlds folder for the same game at the same time.")

            status_text = "Tracker is now " + ("ENABLED"
                                               if host.animal_well_settings["in_game_tracker"] > tracker_enum.no_tracker
                                               else "DISABLED")

            if host.animal_well_settings["in_game_tracker"] == tracker_enum.no_logic:
                status_text += " with no logic"
            if host.animal_well_settings["in_game_tracker"] == tracker_enum.checked_only:
                status_text += " with checked locations only"
            self.ctx.display_text_in_client(status_text)
            logger.info(status_text)

            if host.animal_well_settings["in_game_tracker"] > tracker_enum.no_tracker:
                self.ctx.bean_patcher.apply_tracker_patches()
            else:
                self.ctx.bean_patcher.revert_tracker_patches()

    def _cmd_ring(self):
        """Toggles the cheater's ring in your inventory to allow noclip and get unstuck"""
        try:
            if isinstance(self.ctx, AnimalWellContext):
                if self.ctx.process_handle and self.ctx.start_address:
                    if platform.uname()[0] == "Windows":
                        active_slot = self.ctx.get_active_game_slot()
                        slot_address = self.ctx.start_address + HEADER_LENGTH + (SAVE_SLOT_LENGTH * active_slot)

                        # Read Quest State
                        flags = int.from_bytes(self.ctx.process_handle.read_bytes(slot_address + 0x1EC, 4),
                                               byteorder="little")

                        if bool(flags >> 13 & 1):
                            log_text = "Removing C. Ring from inventory"
                            logger.info(log_text)
                            self.ctx.display_text_in_client(log_text)
                        else:
                            log_text = "Adding C. Ring to inventory. Press F key (or R3 on gamepad) to use."
                            logger.info(log_text)
                            self.ctx.display_text_in_client(log_text)

                        bits = ((str(flags >> 0 & 1)) +  # House Opened
                                (str(flags >> 1 & 1)) +  # Office Opened
                                (str(flags >> 2 & 1)) +  # Closet Opened
                                (str(flags >> 3 & 1)) +  # Unknown
                                (str(flags >> 4 & 1)) +  # Unknown
                                (str(flags >> 5 & 1)) +  # Unknown
                                (str(flags >> 6 & 1)) +  # Unknown
                                (str(flags >> 7 & 1)) +  # Unknown
                                (str(flags >> 8 & 1)) +  # Switch State
                                (str(flags >> 9 & 1)) +  # Map Collected
                                (str(flags >> 10 & 1)) +  # Stamps Collected
                                (str(flags >> 11 & 1)) +  # Pencil Collected
                                (str(flags >> 12 & 1)) +  # Chameleon Defeated
                                ("0" if bool(flags >> 13 & 1) else "1") +  # C Ring Collected
                                (str(flags >> 14 & 1)) +  # Eaten By Chameleon
                                (str(flags >> 15 & 1)) +  # Inserted S Medal
                                (str(flags >> 16 & 1)) +  # Inserted E Medal
                                (str(flags >> 17 & 1)) +  # Wings Acquired
                                (str(flags >> 18 & 1)) +  # Woke Up
                                (str(flags >> 19 & 1)) +  # B.B. Wand Upgrade
                                (str(flags >> 20 & 1)) +  # Egg 65 Collected
                                (str(flags >> 21 & 1)) +  # All Candles Lit
                                (str(flags >> 22 & 1)) +  # Singularity Active
                                (str(flags >> 23 & 1)) +  # Manticore Egg Placed
                                (str(flags >> 24 & 1)) +  # Bat Defeated
                                (str(flags >> 25 & 1)) +  # Ostrich Freed
                                (str(flags >> 26 & 1)) +  # Ostrich Defeated
                                (str(flags >> 27 & 1)) +  # Eel Fight Active
                                (str(flags >> 28 & 1)) +  # Eel Defeated
                                (str(flags >> 29 & 1)) +  # No Disc in Shrine
                                (str(flags >> 30 & 1)) +  # No Disk in Statue
                                (str(flags >> 31 & 1)))[::-1]  # Unknown
                        buffer = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder="little")
                        self.ctx.process_handle.write_bytes(slot_address + 0x1EC, buffer, 4)
                    else:
                        raise NotImplementedError("Only Windows is implemented right now")
        except (pymem.exception.ProcessError, pymem.exception.MemoryReadError, pymem.exception.MemoryWriteError) as e:
            bean_logger.error("%s", e)
            self.ctx.connection_status = CONNECTION_RESET_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {self.ctx.connection_status}")
        except Exception as e:
            bean_logger.fatal("An unknown error has occurred: %s", e)
            self.ctx.connection_status = CONNECTION_ABORTED_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {self.ctx.connection_status}")

    def _cmd_songs(self, val=""):
        """Print notation for songs. Formats are UDLR or Numpad"""
        def udlr(notation: str) -> str:
            return notation.replace("1", "DL ")\
                .replace("2", "D ")\
                .replace("3", "DR ")\
                .replace("4", "L ")\
                .replace("6", "R ")\
                .replace("7", "UL ")\
                .replace("8", "U ")\
                .replace("9", "UR ")

        if isinstance(self.ctx, AnimalWellContext):
            formats = ()
            songs = {
                "Bottom to Well": "68982412",
                "Top of Well": "37373737",
                "Warp Zone": "66442288",
                "Secret Warp Zone": "68424242",
                "bunn1": "69626116",
                "bunn2": "78321242",
                "bunn3": "62486279\n"
                         "62483179",

                "Ghost Banish": "63214789",
                "cat mom": "63216321\n"
                           "32143214\n"
                           "21472148\n"
                           "98741212\n"
                           "32324789\n"
                           "69392919\n"
                           "49798999",
                "cat1": "34936",
                "cat2": "69872",
                "cat3": "77112",
                "cat4": "38334",
                "cat5": "42138",

                "egg song": "72627262\n"
                            "71317131\n"
                            "94249424\n"
                            "84348434\n"
                            "72627262\n"
                            "71317131\n"
                            "79719842\n"
                            "87148747",
                "fish mural": "44369449",
                "duck song": "82824646",
                "dog grass": "69847842",
                "paper": "69847842",
                "tv": "97138426"

            }

            if not val or val.lower() == "udlr":
                for title, notation in songs.items():
                    logger.info(f"{title}: {udlr(notation)}")
            else:
                for title, notation in songs.items():
                    logger.info(f"{title}: {notation}")


class Stamp:
    def __init__(self, x, y, stamp_type=0):
        self.x = x
        self.y = y
        self.type = stamp_type

    def data(self):
        return struct.pack("<hhh", self.x, self.y, self.type)


class Tile:
    def __init__(self, map_id, room_x, room_y, x, y, layer=0, param=0):
        self.map = map_id
        self.room_x = room_x
        self.room_y = room_y
        self.x = x
        self.y = y
        self.layer = layer
        self.param = param

    def stamp(self, stamp_type=0):
        return Stamp(self.room_x*40 + self.x - 3, self.room_y*22 + self.y - 4, stamp_type)


class AnimalWellContext(CommonContext):
    """
    Animal Well Archipelago context
    """
    command_processor = AnimalWellCommandProcessor
    items_handling = 0b111  # get sent remote and starting items

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "ANIMAL WELL"
        self.process_sync_task = None
        self.get_animal_well_process_handle_task = None
        self.process_handle = None
        self.start_address = None
        self.connection_status = CONNECTION_INITIAL_STATUS
        self.slot_data = {}
        self.slot_number: int = -1
        self.current_game_state = -1
        self.last_game_state = -1
        self.last_death_link: float = time.time()
        # used to delay starting the loop until we can see the data storage values
        self.got_data_storage: bool = False
        self.first_m_disc = True
        self.used_firecrackers: int
        self.used_berries: int

        from .. import AnimalWellWorld
        self.bean_patcher = BeanPatcher().set_logger(bean_logger).set_version_string(AnimalWellWorld.version_string)
        self.bean_patcher.set_logger(bean_logger)
        self.bean_patcher.set_bean_death_function(self.on_bean_death)
        self.bean_patcher.game_draw_routine_default_string = "Connected to the well..."
        self.stamps = []
        self.tiles = {}
        self.logic_tracker = AnimalWellTracker()
        # self.console_task = None  # pulled out for now for compatibility with current AP

        self.disconnected_intentionally = True

    def display_dialog(self, text: str, title: str, action_text: str = ""):
        if self.bean_patcher is not None and self.bean_patcher.attached_to_process:
            self.bean_patcher.display_dialog(text, title, action_text)

    def display_text_in_client(self, text: str):
        if self.bean_patcher is not None and self.bean_patcher.attached_to_process:
            self.bean_patcher.display_to_client(text)

    async def on_bean_death(self):
        # todo: put something in to modify DEATHLINK_MESSAGE based on how or where the player died, or something random
        death_link_key = f"{self.slot}|death_link"
        if self.stored_data.get(death_link_key, None) is None:
            if self.slot_data.get("death_link", None) == 1:
                await self.send_death(DEATHLINK_MESSAGE)
        else:
            if self.stored_data[death_link_key]:
                await self.send_death(DEATHLINK_MESSAGE)

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server
        """
        if password_requested and not self.password:
            await super(AnimalWellContext, self).server_auth(password_requested)
        self.tags = set()
        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        # this is to fix resending firecrackers/big blue fruit when disconnecting and reconnecting
        self.got_data_storage = False
        await super().disconnect(allow_autoreconnect)

    def run_gui(self):
        """
        Run the GUI
        """
        from kvui import GameManager

        class AnimalWellManager(GameManager):
            """
            Animal Well Manager
            """
            logging_pairs = [
                ("Client", "Archipelago"),
                ("BeanLogger", "Animal Well Log")
            ]
            base_title = "Archipelago Animal Well Client"

        self.ui = AnimalWellManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.disconnected_intentionally = True
            self.slot_data = args.get("slot_data", {})
            self.display_text_in_client("Connected to the AP server!")

            self.logic_tracker.clear_inventories()
            for option_name, option_value in self.slot_data.items():
                self.logic_tracker.player_options[option_name] = option_value
            self.logic_tracker.mark_hidden_locations()
            for location_id in args.get("checked_locations"):
                location_name = self.location_names.lookup_in_slot(location_id)
                self.logic_tracker.check_logic_status[location_name] = CheckStatus.checked.value
            if self.slot_data["goal"] == Goal.option_fireworks:
                self.bean_patcher.tracker_goal = "Fireworks"
            elif self.slot_data["goal"] == Goal.option_egg_hunt:
                self.bean_patcher.tracker_goal = "Egg Hunt to " + str(self.slot_data["eggs_needed"])
            self.bean_patcher.update_tracker_text()
            aw_settings = get_settings().animal_well_settings
            if aw_settings.get("in_game_tracker", AWSettings.TrackerSetting.full_tracker) > AWSettings.TrackerSetting.no_tracker:
                self.bean_patcher.apply_tracker_patches()
                pass
            else:
                self.bean_patcher.revert_tracker_patches()

            death_link_key = f"{self.slot}|death_link"
            Utils.async_start(self.update_death_link(self.slot_data.get("death_link", None) == 1))
            self.set_notify(death_link_key)
            self.bean_patcher.save_team = args["team"]
            self.bean_patcher.save_slot = args["slot"]
            self.bean_patcher.apply_seeded_save_patch()
            self.disconnected_intentionally = False
        try:
            if cmd == "PrintJSON":
                msg_type = args.get("type")

                if msg_type == "Chat" and not args.get("message").startswith("!"):
                    # TODO: Move ignoring lines starting with ! into a setting of some sort
                    text = args.get("data")[0]["text"]
                    self.display_text_in_client(f"{text}")
                elif msg_type == "Hint":
                    if self.slot_concerns_self(args.get("receiving")):
                        player_slot = args.get("item").player
                        item_name = self.item_names.lookup_in_slot(args.get("item").item, self.slot)
                        location_name = self.location_names.lookup_in_slot(args.get("item").location, player_slot)
                        if not self.slot_concerns_self(player_slot):
                            player_name = self.player_names.get(player_slot)
                            text = f"Hint: Your {item_name} is at {location_name} in {player_name}'s World."
                        else:
                            text = f"Hint: Your {item_name} is at your {location_name}."
                        self.display_text_in_client(text)
                    elif args.get("item").player == self.slot:
                        receiving_player_slot = args.get("receiving")
                        player_name = self.player_names.get(receiving_player_slot)
                        item_name = self.item_names.lookup_in_slot(args.get("item").item, receiving_player_slot)
                        location_name = self.location_names.lookup_in_slot(args.get("item").location, self.slot)
                        text = f"Hint: {player_name}'s {item_name} is at your {location_name}."
                        self.display_text_in_client(text)
                elif msg_type == "Join":
                    self.display_text_in_client(args.get("data")[0]["text"])
                elif msg_type == "Part":
                    self.display_text_in_client(args.get("data")[0]["text"])
                elif msg_type == "ItemCheat":
                    if args.get("receiving") != self.slot:
                        return
                    item_name = self.item_names.lookup_in_game(args.get("item").item)
                    text = f"You received your {item_name}."
                    self.display_text_in_client(text)
                elif msg_type == "ItemSend":
                    destination_player_id = args["receiving"]
                    source_player_id = args["item"][2]  # it's a tuple, so we can't index by name
                    self_slot: int = self.slot
                    # we don't want to display every item message, just ones relevant to us
                    if self_slot not in [source_player_id, destination_player_id]:
                        return
                    item_id = args["item"][0]
                    location_id = args["item"][1]
                    # classification = args["item"][3]  # may use later if we can color-code them in-game
                    item_name = self.item_names.lookup_in_slot(item_id, destination_player_id)
                    location_name = self.location_names.lookup_in_slot(location_id, source_player_id)
                    text = "Error occurred, report to ANIMAL WELL AP devs"
                    if self_slot == source_player_id:
                        destination_player_name = self.player_names[destination_player_id]
                        text = f"You sent {item_name} to {destination_player_name} from {location_name}!"
                    if self_slot == destination_player_id:
                        source_player_name = self.player_names[source_player_id]
                        text = f"{source_player_name} sent you your {item_name}!"
                    if self_slot == source_player_id and self_slot == destination_player_id:
                        text = f"You found your {item_name} at {location_name}!"
                    self.display_text_in_client(text)
                elif msg_type == "Countdown":
                    text = "".join(o["text"] for o in args.get("data"))
                    self.display_text_in_client(text)
                elif msg_type == "CommandResult":
                    pass
                elif msg_type == "Tutorial":
                    pass

            elif cmd == "ReceivedItems":
                # items = args.get("items")
                for item in args.get("items"):
                    item_name = self.item_names.lookup_in_slot(item.item)
                    if item_name == iname.key.value:
                        self.logic_tracker.key_count += 1
                    elif item_name == iname.match.value:
                        self.logic_tracker.match_count += 1
                    elif item_name == iname.bubble.value:
                        if item_name in self.logic_tracker.full_inventory:
                            self.logic_tracker.upgraded_b_wand = True
                        else:
                            self.logic_tracker.full_inventory.add(item_name)
                            self.logic_tracker.out_of_logic_full_inventory.add(item_name)
                    elif item_name in item_name_groups["Eggs"]:
                        if item_name == iname.egg_65.value:
                            self.logic_tracker.full_inventory.add(item_name)
                            self.logic_tracker.out_of_logic_full_inventory.add(item_name)
                        else:
                            self.logic_tracker.egg_tracker.add(item_name)
                    elif item_name == iname.k_shard.value:
                        self.logic_tracker.k_shard_count += 1
                    else:
                        self.logic_tracker.full_inventory.add(item_name)
                        self.logic_tracker.out_of_logic_full_inventory.add(item_name)
                self.logic_tracker.update_checks_and_regions()

            elif cmd == "RoomUpdate":
                if "checked_locations" in args:
                    for location_id in args.get("checked_locations"):
                        location_name = self.location_names.lookup_in_slot(location_id)
                        self.logic_tracker.check_logic_status[location_name] = CheckStatus.checked
            elif cmd == "RoomInfo":
                self.bean_patcher.save_seed = args["seed_name"]
            elif cmd == "SetReply":
                pass
            elif cmd == "Retrieved":
                if args["keys"].get(f"{self.slot}|death_link", None) is not None:
                    Utils.async_start(self.update_death_link(args["keys"].get(f"{self.slot}|death_link")))
            elif cmd == "None":
                self.display_text_in_client(args.get("data")[0]["text"])
            elif cmd == "Bounced":
                # since we're setting our tags properly, we don't need to check our deathlink setting
                if "DeathLink" in args.get("tags", []):
                    if self.last_death_link != args["data"]["time"]:
                        self.on_deathlink(args["data"])

        except Exception as e:
            bean_logger.error("Error while parsing Package from AP: %s", e)
            bean_logger.info("Package details: {}".format(args))

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.last_death_link = max(data["time"], self.last_death_link)
        text = DEATHLINK_RECEIVED_MESSAGE.replace("{name}", data.get("source", "A Player"))
        cause = data.get("cause", None)

        if cause is not None:
            text = cause

        logger.info(text)
        self.display_text_in_client(text)
        self.bean_patcher.set_player_state(5)

    def get_active_game_slot(self) -> int:
        """
        Get the game slot currently being played, as in the in-game slot, not the AP player slot
        """
        if platform.uname()[0] == "Windows":
            slot = self.process_handle.read_bytes(self.start_address + 0xC, 1)[0]
            return slot
        else:
            raise NotImplementedError("Only Windows is implemented right now")

    # Fetches all required tile positions for AWTracker to place stamps by
    def get_tiles(self, tile_types, map_id=0):
        if self.start_address is None:
            return
        map_addr = int.from_bytes(self.process_handle.read_bytes(self.bean_patcher.base_layer_address, 8),
                                  byteorder="little") + 0x2d0 + map_id * 0x1b8f84
        room_count = int.from_bytes(self.process_handle.read_bytes(map_addr, 2), byteorder="little")
        map_data = self.process_handle.read_bytes(map_addr + 4, 0x1b8f84)
        for room_idx in range(room_count):
            room_offset = room_idx*(8+2*22*40*4)
            room_x = map_data[room_offset]
            room_y = map_data[room_offset+1]
            for layer in range(2):
                for y in range(22):
                    for x in range(40):
                        tile_offset = room_offset + 8 + y*40*4 + x*4 + layer*22*40*4
                        room_tile = int.from_bytes(map_data[tile_offset:tile_offset+2], byteorder="little")
                        param = map_data[tile_offset+2]
                        if room_tile in tile_types:
                            if room_tile not in self.tiles:
                                self.tiles[room_tile] = []
                            self.tiles[room_tile].append(Tile(map_id, room_x, room_y, x, y, layer, param))

    def get_tiles_for_locations(self):
        tile_ids = []
        loc_tables = [loc for loc in location_table.values()]
        loc_tables.extend([loc for loc in events_table.values()])
        for loc in loc_tables:
            if not loc.tracker:
                continue
            if loc.tracker.tile not in tile_ids and loc.tracker.tile > 0:
                tile_ids.append(loc.tracker.tile)
        self.get_tiles(tile_ids)
        for tiles in self.tiles.values():
            tiles.sort(key=lambda item: (item.room_y, item.room_x, item.y, item.x))
        # logger.info(f"Found {len(self.tiles)} tile types to track")

    def get_stamps_for_locations(self, ctx):
        if not self.tiles:
            self.get_tiles_for_locations()
        self.stamps.clear()
        loc_table = location_table.copy()
        for k, v in events_table.items():
            loc_table[k] = v
        for name, loc in loc_table.items():
            if (not loc.tracker
                    or name not in self.logic_tracker.check_logic_status
                    or self.logic_tracker.check_logic_status[name] == CheckStatus.dont_show
                    or ((loc.tracker.tile not in self.tiles
                         or len(self.tiles[loc.tracker.tile]) < loc.tracker.index+1)
                        and loc.tracker.tile > 0)):
                continue
            # bake logic status into the stamp type for colored stamps patch to read
            stamp = loc.tracker.stamp | (self.logic_tracker.check_logic_status[name] << 4)

            aw_settings = get_settings().animal_well_settings
            tracker_enum = AWSettings.TrackerSetting
            aw_settings.get("in_game_tracker", tracker_enum.full_tracker)
            if aw_settings["in_game_tracker"] == tracker_enum.no_logic:
                stamp = loc.tracker.stamp | (0x30 if self.logic_tracker.check_logic_status[name] == CheckStatus.checked.value else 0x20)
            elif aw_settings["in_game_tracker"] == tracker_enum.checked_only and self.logic_tracker.check_logic_status[name] != CheckStatus.checked.value:
                continue

            if name == lname.bunny_uv.value:
                pos = struct.unpack("<ff", self.process_handle.read_bytes(self.bean_patcher.application_state_address + 0x754a8 + 0x30ec8, 8))
                bunny_x = int(pos[0]/8)
                bunny_y = int(pos[1]/8)
                self.stamps.append(Stamp(bunny_x, bunny_y, stamp))
                self.stamps[-1].x += loc.tracker.stamp_x
                self.stamps[-1].y += loc.tracker.stamp_y
            # TODO: Dream Bunny is banished to the wake up room pending options to enable bean tracking
            # elif name == lname.bunny_dream.value:
            #    if self.logic_tracker.check_logic_status[name] != CheckStatus.in_logic:
            #        continue
            #    pos = struct.unpack("<ff", self.process_handle.read_bytes(self.bean_patcher.application_state_address + 0x93670, 8))
            #    room = struct.unpack("<ii", self.process_handle.read_bytes(self.bean_patcher.application_state_address + 0x93670 + 0x20, 8))
            #    bean_x = int(pos[0]/8) + int(room[0])*40
            #    bean_y = int(pos[1]/8) + int(room[1])*22
            #    self.stamps.append(Stamp(bean_x-3, bean_y-13, stamp))"""
            elif loc.tracker.tile in self.tiles and len(self.tiles[loc.tracker.tile]) > loc.tracker.index:
                self.stamps.append(self.tiles[loc.tracker.tile][loc.tracker.index].stamp(stamp))
                self.stamps[-1].x += loc.tracker.stamp_x
                self.stamps[-1].y += loc.tracker.stamp_y
            else:
                self.stamps.append(Stamp(loc.tracker.stamp_x, loc.tracker.stamp_y, stamp))

        self.bean_patcher.tracker_total = len(self.server_locations)
        self.bean_patcher.tracker_checked = len(self.checked_locations)
        self.bean_patcher.tracker_missing = len(self.missing_locations)
        self.bean_patcher.tracker_in_logic = len({k: v for (k, v) in self.logic_tracker.check_logic_status.items()
                                                  if v == CheckStatus.in_logic
                                                  and k in location_name_to_id
                                                  and location_name_to_id[k] in self.missing_locations})
        if self.slot_data.get("candle_checks", None):
            self.bean_patcher.tracker_candles = len({k: v for (k, v) in self.logic_tracker.check_logic_status.items()
                                                     if k in candle_locations and v == CheckStatus.checked})
        else:
            self.bean_patcher.tracker_candles = len({k: v for (k, v) in self.logic_tracker.check_logic_status.items()
                                                     if k in candle_event_to_item and v == CheckStatus.checked})
        self.bean_patcher.update_tracker_text()

    def check_if_in_game(self) -> bool:
        """
        Checks if the game is currently running or is still in the main menu
        """
        try:
            current_game_state = self.process_handle.read_uchar(self.start_address + 0x750cc)
        except:
            bean_logger.error("Failure here means you have run into an unrecoverable state. Closing the client.")
            self.exit_event.set()
            if self.ui:
                self.ui.stop()
            raise Exception("Probably closed the game.")

        if current_game_state != self.last_game_state:
            self.last_game_state = current_game_state
            if current_game_state == 1:
                bean_logger.info(f"Game currently displaying the splash screens. "
                                 f"Deferring until new game is started or saved game is loaded...")
            elif current_game_state == 2:
                bean_logger.info(f"Game currently displaying the main menu. "
                                 f"Deferring until new game is started or saved game is loaded...")
            elif current_game_state == 3:
                bean_logger.info(f"Game currently displaying the new game intro scene. "
                                 f"Deferring until new game is started or saved game is loaded...")
            elif current_game_state == 4:
                bean_logger.info(f"Game is now loaded and running!")
            else:
                bean_logger.info(f"Game currently in unknown game state {current_game_state}. "
                                 f"Deferring until new game is started or saved game is loaded...")

        return current_game_state == 4


class AWLocations:
    """
    The checks the player has found
    """

    def __init__(self):
        self.byte_sect_dict: Dict[int, int] = {}
        self.loc_statuses: Dict[str, bool] = {}
        for loc_name in location_table.keys():
            self.loc_statuses[loc_name] = False

    def read_from_game(self, ctx):
        """
        Read checked locations from the process
        """
        try:
            if platform.uname()[0] == "Windows":
                if not ctx.check_if_in_game():
                    return

                active_slot = ctx.get_active_game_slot()
                slot_address = ctx.start_address + HEADER_LENGTH + (SAVE_SLOT_LENGTH * active_slot)

                self.byte_sect_dict: Dict[int, int] = {
                    ByteSect.items.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x120, 16), byteorder="little"),
                    ByteSect.flames.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x21e, 16), byteorder="little"),
                    ByteSect.bunnies.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x198, 4), byteorder="little"),
                    ByteSect.candles.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1E0, 2), byteorder="little"),
                    ByteSect.house_key.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x21C, 2), byteorder="little"),
                    ByteSect.fruits.value:
                        int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x170, 16), byteorder="little"),
                }

                for loc_name, status in self.loc_statuses.items():
                    loc_data = location_table[loc_name]

                    if loc_data.byte_section == ByteSect.flames:
                        self.loc_statuses[loc_name] = (
                                ctx.process_handle.read_bytes(slot_address + loc_data.byte_offset, 1)[0] >= 4)
                        if self.loc_statuses[loc_name]:
                            ctx.logic_tracker.check_logic_status[loc_name] = CheckStatus.checked.value
                            ctx.logic_tracker.full_inventory.add(loc_name)
                            ctx.logic_tracker.out_of_logic_full_inventory.add(loc_name)
                        continue

                    self.loc_statuses[loc_name] = (
                        bool(self.byte_sect_dict[loc_data.byte_section] >> loc_data.byte_offset & 1))

                if ctx.bean_patcher is not None and ctx.bean_patcher.attached_to_process:
                    ctx.bean_patcher.read_from_game()
            else:
                raise NotImplementedError("Only Windows is implemented right now")
        except (pymem.exception.ProcessError, pymem.exception.MemoryReadError, ConnectionResetError) as e:
            bean_logger.error("%s", e)
            ctx.connection_status = CONNECTION_RESET_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")
        except (NotImplementedError, Exception) as e:
            bean_logger.fatal("An unknown error has occurred: %s", e)
            ctx.connection_status = CONNECTION_ABORTED_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")

    async def write_to_archipelago(self, ctx):
        """
        Write checked locations to archipelago
        """
        try:
            for loc_name, status in self.loc_statuses.items():
                if status:
                    ctx.locations_checked.add(location_name_to_id[loc_name])
                    if location_table[loc_name].byte_section == ByteSect.candles:
                        ctx.logic_tracker.check_logic_status[loc_name + " Event"] = CheckStatus.checked.value
                        ctx.logic_tracker.full_inventory.add(candle_event_to_item[loc_name + " Event"])
                        ctx.logic_tracker.out_of_logic_full_inventory.add(candle_event_to_item[loc_name + " Event"])

            if ctx.slot_data.get("goal", None) == Goal.option_fireworks:
                if not ctx.finished_game and self.loc_statuses[lname.key_house]:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

            locations_checked = []
            for location in ctx.missing_locations:
                if location in ctx.locations_checked:
                    locations_checked.append(location)
            if locations_checked:
                await ctx.send_msgs([
                    {"cmd": "LocationChecks",
                     "locations": locations_checked}
                ])
        except Exception as e:
            bean_logger.fatal("An unknown error has occurred: %s", e)
            ctx.connection_status = CONNECTION_ABORTED_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")


class AWItems:
    """
    The items the player has received
    """

    def __init__(self):
        # Major progression items
        self.bubble = 0  # progressive
        # self.disc = False
        self.yoyo = False
        self.slink = False
        self.flute = False
        self.top = False
        self.lantern = False
        self.uv = False
        self.ball = False
        self.remote = False
        self.wheel = False
        self.firecrackers = True

        # Minor progression items and keys
        self.m_disc = False
        self.fanny_pack = False

        self.match = 0
        self.matchbox = False

        self.key = 0
        self.key_ring = False
        self.house_key = False
        self.office_key = False

        self.e_medal = False
        self.s_medal = False
        self.k_shard = 0

        # self.blue_flame = False
        # self.green_flame = False
        # self.violet_flame = False
        # self.pink_flame = False

        # Eggs
        self.egg_reference = False
        self.egg_brown = False
        self.egg_raw = False
        self.egg_pickled = False
        self.egg_big = False
        self.egg_swan = False
        self.egg_forbidden = False
        self.egg_shadow = False
        self.egg_vanity = False
        self.egg_service = False

        self.egg_depraved = False
        self.egg_chaos = False
        self.egg_upside_down = False
        self.egg_evil = False
        self.egg_sweet = False
        self.egg_chocolate = False
        self.egg_value = False
        self.egg_plant = False
        self.egg_red = False
        self.egg_orange = False
        self.egg_sour = False
        self.egg_post_modern = False

        self.egg_universal = False
        self.egg_lf = False
        self.egg_zen = False
        self.egg_future = False
        self.egg_friendship = False
        self.egg_truth = False
        self.egg_transcendental = False
        self.egg_ancient = False
        self.egg_magic = False
        self.egg_mystic = False
        self.egg_holiday = False
        self.egg_rain = False
        self.egg_razzle = False
        self.egg_dazzle = False

        self.egg_virtual = False
        self.egg_normal = False
        self.egg_great = False
        self.egg_gorgeous = False
        self.egg_planet = False
        self.egg_moon = False
        self.egg_galaxy = False
        self.egg_sunset = False
        self.egg_goodnight = False
        self.egg_dream = False
        self.egg_travel = False
        self.egg_promise = False
        self.egg_ice = False
        self.egg_fire = False

        self.egg_bubble = False
        self.egg_desert = False
        self.egg_clover = False
        self.egg_brick = False
        self.egg_neon = False
        self.egg_iridescent = False
        self.egg_rust = False
        self.egg_scarlet = False
        self.egg_sapphire = False
        self.egg_ruby = False
        self.egg_jade = False
        self.egg_obsidian = False
        self.egg_crystal = False
        self.egg_golden = False

        self.egg_65 = False

        self.firecracker_refill = 0
        self.big_blue_fruit = 0

    async def read_from_archipelago(self, ctx):
        """
        Read inventory state from archipelago
        """
        try:
            items = [item.item for item in ctx.items_received]

            # Major progression items
            self.bubble = len([item for item in items if item == item_name_to_id[iname.bubble.value]])
            # self.disc = item_name_to_id[iname.disc.value] in items
            self.yoyo = item_name_to_id[iname.yoyo.value] in items
            self.slink = item_name_to_id[iname.slink.value] in items
            self.flute = item_name_to_id[iname.flute.value] in items
            self.top = item_name_to_id[iname.top.value] in items
            self.lantern = item_name_to_id[iname.lantern.value] in items
            self.uv = item_name_to_id[iname.uv.value] in items
            self.ball = item_name_to_id[iname.ball.value] in items
            self.remote = item_name_to_id[iname.remote.value] in items
            self.wheel = item_name_to_id[iname.wheel.value] in items
            self.firecrackers = item_name_to_id[iname.firecrackers.value] in items

            # Minor progression items and keys
            self.m_disc = item_name_to_id[iname.m_disc.value] in items
            self.fanny_pack = item_name_to_id[iname.fanny_pack.value] in items

            self.match = len([item for item in items if item == item_name_to_id[iname.match.value]])
            self.matchbox = item_name_to_id[iname.matchbox.value] in items

            self.key = len([item for item in items if item == item_name_to_id[iname.key.value]])
            self.key_ring = item_name_to_id[iname.key_ring.value] in items
            self.house_key = item_name_to_id[iname.house_key.value] in items
            self.office_key = item_name_to_id[iname.office_key.value] in items

            self.e_medal = item_name_to_id[iname.e_medal.value] in items
            self.s_medal = item_name_to_id[iname.s_medal.value] in items
            self.k_shard = len([item for item in items if item == item_name_to_id[iname.k_shard.value]])

            # self.blue_flame = item_name_to_id[iname.blue_flame.value] in items
            # self.green_flame = item_name_to_id[iname.green_flame.value] in items
            # self.violet_flame = item_name_to_id[iname.violet_flame.value] in items
            # self.pink_flame = item_name_to_id[iname.pink_flame.value] in items

            # Eggs
            self.egg_reference = item_name_to_id[iname.egg_reference.value] in items
            self.egg_brown = item_name_to_id[iname.egg_brown.value] in items
            self.egg_raw = item_name_to_id[iname.egg_raw.value] in items
            self.egg_pickled = item_name_to_id[iname.egg_pickled.value] in items
            self.egg_big = item_name_to_id[iname.egg_big.value] in items
            self.egg_swan = item_name_to_id[iname.egg_swan.value] in items
            self.egg_forbidden = item_name_to_id[iname.egg_forbidden.value] in items
            self.egg_shadow = item_name_to_id[iname.egg_shadow.value] in items
            self.egg_vanity = item_name_to_id[iname.egg_vanity.value] in items
            self.egg_service = item_name_to_id[iname.egg_service.value] in items

            self.egg_depraved = item_name_to_id[iname.egg_depraved.value] in items
            self.egg_chaos = item_name_to_id[iname.egg_chaos.value] in items
            self.egg_upside_down = item_name_to_id[iname.egg_upside_down.value] in items
            self.egg_evil = item_name_to_id[iname.egg_evil.value] in items
            self.egg_sweet = item_name_to_id[iname.egg_sweet.value] in items
            self.egg_chocolate = item_name_to_id[iname.egg_chocolate.value] in items
            self.egg_value = item_name_to_id[iname.egg_value.value] in items
            self.egg_plant = item_name_to_id[iname.egg_plant.value] in items
            self.egg_red = item_name_to_id[iname.egg_red.value] in items
            self.egg_orange = item_name_to_id[iname.egg_orange.value] in items
            self.egg_sour = item_name_to_id[iname.egg_sour.value] in items
            self.egg_post_modern = item_name_to_id[iname.egg_post_modern.value] in items

            self.egg_universal = item_name_to_id[iname.egg_universal.value] in items
            self.egg_lf = item_name_to_id[iname.egg_lf.value] in items
            self.egg_zen = item_name_to_id[iname.egg_zen.value] in items
            self.egg_future = item_name_to_id[iname.egg_future.value] in items
            self.egg_friendship = item_name_to_id[iname.egg_friendship.value] in items
            self.egg_truth = item_name_to_id[iname.egg_truth.value] in items
            self.egg_transcendental = item_name_to_id[iname.egg_transcendental.value] in items
            self.egg_ancient = item_name_to_id[iname.egg_ancient.value] in items
            self.egg_magic = item_name_to_id[iname.egg_magic.value] in items
            self.egg_mystic = item_name_to_id[iname.egg_mystic.value] in items
            self.egg_holiday = item_name_to_id[iname.egg_holiday.value] in items
            self.egg_rain = item_name_to_id[iname.egg_rain.value] in items
            self.egg_razzle = item_name_to_id[iname.egg_razzle.value] in items
            self.egg_dazzle = item_name_to_id[iname.egg_dazzle.value] in items

            self.egg_virtual = item_name_to_id[iname.egg_virtual.value] in items
            self.egg_normal = item_name_to_id[iname.egg_normal.value] in items
            self.egg_great = item_name_to_id[iname.egg_great.value] in items
            self.egg_gorgeous = item_name_to_id[iname.egg_gorgeous.value] in items
            self.egg_planet = item_name_to_id[iname.egg_planet.value] in items
            self.egg_moon = item_name_to_id[iname.egg_moon.value] in items
            self.egg_galaxy = item_name_to_id[iname.egg_galaxy.value] in items
            self.egg_sunset = item_name_to_id[iname.egg_sunset.value] in items
            self.egg_goodnight = item_name_to_id[iname.egg_goodnight.value] in items
            self.egg_dream = item_name_to_id[iname.egg_dream.value] in items
            self.egg_travel = item_name_to_id[iname.egg_travel.value] in items
            self.egg_promise = item_name_to_id[iname.egg_promise.value] in items
            self.egg_ice = item_name_to_id[iname.egg_ice.value] in items
            self.egg_fire = item_name_to_id[iname.egg_fire.value] in items

            self.egg_bubble = item_name_to_id[iname.egg_bubble.value] in items
            self.egg_desert = item_name_to_id[iname.egg_desert.value] in items
            self.egg_clover = item_name_to_id[iname.egg_clover.value] in items
            self.egg_brick = item_name_to_id[iname.egg_brick.value] in items
            self.egg_neon = item_name_to_id[iname.egg_neon.value] in items
            self.egg_iridescent = item_name_to_id[iname.egg_iridescent.value] in items
            self.egg_rust = item_name_to_id[iname.egg_rust.value] in items
            self.egg_scarlet = item_name_to_id[iname.egg_scarlet.value] in items
            self.egg_sapphire = item_name_to_id[iname.egg_sapphire.value] in items
            self.egg_ruby = item_name_to_id[iname.egg_ruby.value] in items
            self.egg_jade = item_name_to_id[iname.egg_jade.value] in items
            self.egg_obsidian = item_name_to_id[iname.egg_obsidian.value] in items
            self.egg_crystal = item_name_to_id[iname.egg_crystal.value] in items
            self.egg_golden = item_name_to_id[iname.egg_golden.value] in items

            # todo: make this less terrible
            if "goal" in ctx.slot_data and ctx.slot_data["goal"] == Goal.option_egg_hunt:
                if (not ctx.finished_game and
                        self.egg_reference and self.egg_brown and self.egg_raw and self.egg_pickled and
                        self.egg_big and self.egg_swan and self.egg_forbidden and self.egg_shadow and
                        self.egg_vanity and self.egg_service and self.egg_depraved and self.egg_chaos and
                        self.egg_upside_down and self.egg_evil and self.egg_sweet and self.egg_chocolate and
                        self.egg_value and self.egg_plant and self.egg_red and self.egg_orange and
                        self.egg_sour and self.egg_post_modern and self.egg_universal and self.egg_lf and
                        self.egg_zen and self.egg_future and self.egg_friendship and self.egg_truth and
                        self.egg_transcendental and self.egg_ancient and self.egg_magic and self.egg_mystic and
                        self.egg_holiday and self.egg_rain and self.egg_razzle and self.egg_dazzle and
                        self.egg_virtual and self.egg_normal and self.egg_great and self.egg_gorgeous and
                        self.egg_planet and self.egg_moon and self.egg_galaxy and self.egg_sunset and
                        self.egg_goodnight and self.egg_dream and self.egg_travel and self.egg_promise and
                        self.egg_ice and self.egg_fire and self.egg_bubble and self.egg_desert and
                        self.egg_clover and self.egg_brick and self.egg_neon and self.egg_iridescent and
                        self.egg_rust and self.egg_scarlet and self.egg_sapphire and self.egg_ruby and
                        self.egg_jade and self.egg_obsidian and self.egg_crystal and self.egg_golden and self.egg_65):
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

            self.egg_65 = item_name_to_id[iname.egg_65.value] in items

            self.firecracker_refill = len([item for item in items if item == item_name_to_id["Firecracker Refill"]])
            self.big_blue_fruit = len([item for item in items if item == item_name_to_id["Big Blue Fruit"]])
        except Exception as e:
            bean_logger.fatal("An unknown error has occurred: %s", e)
            ctx.connection_status = CONNECTION_ABORTED_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")

    def write_to_game(self, ctx):
        """
        Write inventory state to the process
        """
        try:
            if platform.uname()[0] == "Windows":
                if not ctx.check_if_in_game():
                    return

                aw_settings = get_settings().animal_well_settings
                tracker_enum = AWSettings.TrackerSetting

                active_slot = ctx.get_active_game_slot()
                slot_address = ctx.start_address + HEADER_LENGTH + (SAVE_SLOT_LENGTH * active_slot)

                ctx.process_handle.write_bytes(ctx.start_address + 0xE, b"\x00", 1)  # no checksum manticores allowed!

                # Read Quest State
                flags = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1EC, 4), byteorder="little")
                inserted_s_medal = bool(flags >> 15 & 1)
                inserted_e_medal = bool(flags >> 16 & 1)

                # Write Quest State
                egg_65 = self.egg_65
                if (FinalEggLocation.internal_name not in ctx.slot_data
                        or not ctx.slot_data[FinalEggLocation.internal_name]):
                    egg_65 = bool(flags >> 20 & 1)

                bits = ((str(flags >> 0 & 1)) +  # House Opened
                        (str(flags >> 1 & 1)) +  # Office Opened
                        (str(flags >> 2 & 1)) +  # Closet Opened
                        (str(flags >> 3 & 1)) +  # Unknown
                        (str(flags >> 4 & 1)) +  # Unknown
                        (str(flags >> 5 & 1)) +  # Unknown
                        (str(flags >> 6 & 1)) +  # Unknown
                        (str(flags >> 7 & 1)) +  # Unknown
                        (str(flags >> 8 & 1)) +  # Switch State
                        "1" +  # Map Collected
                        ("1" if aw_settings["in_game_tracker"] == tracker_enum.no_tracker else "0") +  # Stamps Collected
                        "1" +  # Pencil Collected
                        (str(flags >> 12 & 1)) +  # Chameleon Defeated
                        (str(flags >> 13 & 1)) +  # C Ring Collected
                        (str(flags >> 14 & 1)) +  # Eaten By Chameleon
                        ("1" if inserted_s_medal else "0") +  # Inserted S Medal
                        ("1" if inserted_e_medal else "0") +  # Inserted E Medal
                        (str(flags >> 17 & 1)) +  # Wings Acquired
                        (str(flags >> 18 & 1)) +  # Woke Up
                        ("1" if self.bubble > 1 else "0") +  # B.B. Wand Upgrade
                        ("1" if egg_65 else "0") +  # Egg 65 Collected
                        (str(flags >> 21 & 1)) +  # All Candles Lit
                        (str(flags >> 22 & 1)) +  # Singularity Active
                        (str(flags >> 23 & 1)) +  # Manticore Egg Placed
                        (str(flags >> 24 & 1)) +  # Bat Defeated
                        (str(flags >> 25 & 1)) +  # Ostrich Freed
                        (str(flags >> 26 & 1)) +  # Ostrich Defeated
                        (str(flags >> 27 & 1)) +  # Eel Fight Active
                        (str(flags >> 28 & 1)) +  # Eel Defeated
                        (str(flags >> 29 & 1)) +  # No Disc in Shrine
                        (str(flags >> 30 & 1)) +  # No Disk in Statue
                        (str(flags >> 31 & 1)))[::-1]  # Unknown
                buffer = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder="little")
                ctx.process_handle.write_bytes(slot_address + 0x1EC, buffer, 4)

                # Write Eggs
                bits = (("1" if self.egg_reference else "0") +
                        ("1" if self.egg_brown else "0") +
                        ("1" if self.egg_raw else "0") +
                        ("1" if self.egg_pickled else "0") +
                        ("1" if self.egg_big else "0") +
                        ("1" if self.egg_swan else "0") +
                        ("1" if self.egg_forbidden else "0") +
                        ("1" if self.egg_shadow else "0") +

                        ("1" if self.egg_vanity else "0") +
                        ("1" if self.egg_service else "0") +
                        ("1" if self.egg_depraved else "0") +
                        ("1" if self.egg_chaos else "0") +
                        ("1" if self.egg_upside_down else "0") +
                        ("1" if self.egg_evil else "0") +
                        ("1" if self.egg_sweet else "0") +
                        ("1" if self.egg_chocolate else "0") +

                        ("1" if self.egg_value else "0") +
                        ("1" if self.egg_plant else "0") +
                        ("1" if self.egg_red else "0") +
                        ("1" if self.egg_orange else "0") +
                        ("1" if self.egg_sour else "0") +
                        ("1" if self.egg_post_modern else "0") +
                        ("1" if self.egg_universal else "0") +
                        ("1" if self.egg_lf else "0") +

                        ("1" if self.egg_zen else "0") +
                        ("1" if self.egg_future else "0") +
                        ("1" if self.egg_friendship else "0") +
                        ("1" if self.egg_truth else "0") +
                        ("1" if self.egg_transcendental else "0") +
                        ("1" if self.egg_ancient else "0") +
                        ("1" if self.egg_magic else "0") +
                        ("1" if self.egg_mystic else "0") +

                        ("1" if self.egg_holiday else "0") +
                        ("1" if self.egg_rain else "0") +
                        ("1" if self.egg_razzle else "0") +
                        ("1" if self.egg_dazzle else "0") +
                        ("1" if self.egg_virtual else "0") +
                        ("1" if self.egg_normal else "0") +
                        ("1" if self.egg_great else "0") +
                        ("1" if self.egg_gorgeous else "0") +

                        ("1" if self.egg_planet else "0") +
                        ("1" if self.egg_moon else "0") +
                        ("1" if self.egg_galaxy else "0") +
                        ("1" if self.egg_sunset else "0") +
                        ("1" if self.egg_goodnight else "0") +
                        ("1" if self.egg_dream else "0") +
                        ("1" if self.egg_travel else "0") +
                        ("1" if self.egg_promise else "0") +

                        ("1" if self.egg_ice else "0") +
                        ("1" if self.egg_fire else "0") +
                        ("1" if self.egg_bubble else "0") +
                        ("1" if self.egg_desert else "0") +
                        ("1" if self.egg_clover else "0") +
                        ("1" if self.egg_brick else "0") +
                        ("1" if self.egg_neon else "0") +
                        ("1" if self.egg_iridescent else "0") +

                        ("1" if self.egg_rust else "0") +
                        ("1" if self.egg_scarlet else "0") +
                        ("1" if self.egg_sapphire else "0") +
                        ("1" if self.egg_ruby else "0") +
                        ("1" if self.egg_jade else "0") +
                        ("1" if self.egg_obsidian else "0") +
                        ("1" if self.egg_crystal else "0") +
                        ("1" if self.egg_golden else "0"))[::-1]
                buffer = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder="little")
                ctx.process_handle.write_bytes(slot_address + 0x188, buffer, 8)

                # Read Opened Doors
                keys_used = ctx.process_handle.read_bytes(slot_address + 0x1AA, 1)[0]

                # Write Keys
                if self.key_ring:
                    # always show real amount of key doors left unopened for a quick way to check how many you have left
                    buffer = bytes([max(0, 6 - keys_used)])
                else:
                    buffer = bytes([max(0, self.key - keys_used)])
                ctx.process_handle.write_bytes(slot_address + 0x1B1, buffer, 1)

                # Read Candles Lit
                flags = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1E0, 2), byteorder="little")
                candles_lit = ((flags >> 0 & 1) +
                               (flags >> 1 & 1) +
                               (flags >> 2 & 1) +
                               (flags >> 3 & 1) +
                               (flags >> 4 & 1) +
                               (flags >> 5 & 1) +
                               (flags >> 6 & 1) +
                               (flags >> 7 & 1) +

                               (flags >> 8 & 1))

                # Write Matches
                if self.matchbox:
                    # always show real amount of candles left unlit for a quick way to check how many you have left
                    buffer = bytes([max(0, 9 - candles_lit)])
                else:
                    buffer = bytes([max(0, self.match - candles_lit)])
                ctx.process_handle.write_bytes(slot_address + 0x1B2, buffer, 1)

                # Read Owned Equipment
                flags = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1DC, 2), byteorder="little")
                disc = bool(flags >> 5 & 1)

                # Write Owned Equipment
                bits = ((str(flags >> 0 & 1)) +  # Unknown
                        ("1" if self.firecrackers else "0") +
                        ("1" if self.flute else "0") +
                        ("1" if self.lantern else "0") +
                        ("1" if self.top else "0") +
                        ("1" if disc else "0") +
                        ("1" if self.bubble > 0 else "0") +
                        ("1" if self.yoyo else "0") +

                        ("1" if self.slink else "0") +
                        ("1" if self.remote else "0") +
                        ("1" if self.ball else "0") +
                        ("1" if self.wheel else "0") +
                        ("1" if self.uv else "0") +
                        (str(flags >> 13 & 1)) +  # Pad
                        (str(flags >> 14 & 1)) +  # Pad
                        (str(flags >> 15 & 1)))[::-1]  # Pad
                buffer = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder="little")
                ctx.process_handle.write_bytes(slot_address + 0x1DC, buffer, 2)

                # select firecrackers if firecrackers is unlocked and no other equipment is selected,
                # since picking up other equipment before firecrackers doesn't set the selected equipment,
                # and firecrackers is given by default anyway
                if ctx.process_handle.read_bytes(slot_address + 0x1EA, 1)[0] == 0 and self.firecrackers:
                    ctx.process_handle.write_bytes(slot_address + 0x1EA, b"\x01", 1)

                # Read Other Items
                flags = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1DE, 1), byteorder="little")
                possess_m_disc = self.m_disc and (bool(flags >> 0 & 1) or ctx.first_m_disc)
                if self.m_disc:
                    if ctx.first_m_disc:
                        quest = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1EC, 8), byteorder="little")
                        quest |= 0x60000000
                        buffer = quest.to_bytes(8, byteorder="little")
                        ctx.process_handle.write_bytes(slot_address + 0x1EC, buffer, 8)
                    ctx.first_m_disc = False

                # Write Other Items
                bits = (("1" if possess_m_disc else "0") +  # Mock Disc
                        ("1" if (self.s_medal and not inserted_s_medal) else "0") +  # S Medal
                        (str(flags >> 2 & 1)) +  # Unused
                        ("1" if self.house_key else "0") +  # House Key
                        ("1" if self.office_key else "0") +  # Office Key
                        (str(flags >> 5 & 1)) +  # Unused
                        ("1" if (self.e_medal and not inserted_e_medal) else "0") +  # E Medal
                        ("1" if self.fanny_pack else "0"))[::-1]  # Fanny Pack
                buffer = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder="little")
                ctx.process_handle.write_bytes(slot_address + 0x1DE, buffer, 1)

                # Read K Shards
                k_shard_1 = bytes([0])
                if self.k_shard >= 1:
                    k_shard_1 = bytes([max(2, ctx.process_handle.read_bytes(slot_address + 0x1FE, 1)[0])])
                k_shard_2 = bytes([0])
                if self.k_shard >= 2:
                    k_shard_2 = bytes([max(2, ctx.process_handle.read_bytes(slot_address + 0x20A, 1)[0])])
                k_shard_3 = bytes([0])
                if self.k_shard >= 3:
                    k_shard_3 = bytes([max(2, ctx.process_handle.read_bytes(slot_address + 0x216, 1)[0])])

                # Write K Shards
                ctx.process_handle.write_bytes(slot_address + 0x1FE, k_shard_1, 1)
                ctx.process_handle.write_bytes(slot_address + 0x20A, k_shard_2, 1)
                ctx.process_handle.write_bytes(slot_address + 0x216, k_shard_3, 1)

                # string used for the data storage keys
                used_berries_string = f"{ctx.slot_number}|used_berries"
                used_firecrackers_string = f"{ctx.slot_number}|used_firecrackers"

                if not ctx.got_data_storage:
                    Utils.async_start(ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [used_berries_string,
                                 used_firecrackers_string,]
                    }]))
                    if used_berries_string in ctx.stored_data:
                        ctx.got_data_storage = True
                        self.big_blue_fruit = ctx.used_berries = ctx.stored_data[used_berries_string]
                        self.firecracker_refill = ctx.used_firecrackers = ctx.stored_data[used_firecrackers_string]
                else:
                    # Berries
                    # null checking since it caused issues before
                    if self.big_blue_fruit is None:
                        self.big_blue_fruit = 0
                    if ctx.used_berries is None:
                        ctx.used_berries = 0

                    # sometimes used_berries ends up bigger than big_blue_fruit, same with firecrackers
                    berries_to_use = max(self.big_blue_fruit - ctx.used_berries, 0)
                    total_hearts = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1B4, 1),
                                                  byteorder="little")
                    # berries_to_use multiplied by 3 to always give you +3 hearts
                    total_hearts = min(total_hearts + berries_to_use * 3, 255)
                    buffer = bytes([total_hearts])
                    ctx.process_handle.write_bytes(slot_address + 0x1B4, buffer, 1)
                    ctx.used_berries = self.big_blue_fruit
                    # update data storage so that we don't re-receive the berry on reconnect
                    stored_berries = ctx.stored_data[used_berries_string] or 0
                    if ctx.used_berries > stored_berries:
                        Utils.async_start(ctx.send_msgs([{
                            "cmd": "Set",
                            "key": used_berries_string,
                            "default": 0,
                            "want_reply": True,
                            "operations": [{"operation": "replace", "value": ctx.used_berries}]
                        }]))

                    # Firecrackers
                    # null checking since it caused issues before
                    if self.firecracker_refill is None:
                        self.firecracker_refill = 0
                    if ctx.used_firecrackers is None:
                        ctx.used_firecrackers = 0

                    firecrackers_to_use = max(self.firecracker_refill - ctx.used_firecrackers, 0)
                    total_firecrackers = int.from_bytes(ctx.process_handle.read_bytes(slot_address + 0x1B3, 1),
                                                        byteorder="little")
                    # multiply firecrackers to use by 6 so that it always fills up your inventory
                    total_firecrackers = min(total_firecrackers + firecrackers_to_use * 6, 6 if self.fanny_pack else 3)
                    buffer = bytes([total_firecrackers])
                    ctx.process_handle.write_bytes(slot_address + 0x1B3, buffer, 1)
                    ctx.used_firecrackers = self.firecracker_refill
                    # update data storage so that we don't re-receive the firecracker on reconnect
                    stored_firecrackers = ctx.stored_data[used_firecrackers_string] or 0
                    if ctx.used_firecrackers > stored_firecrackers:
                        Utils.async_start(ctx.send_msgs([{
                            "cmd": "Set",
                            "key": used_firecrackers_string,
                            "default": 0,
                            "want_reply": True,
                            "operations": [{"operation": "replace", "value": ctx.used_firecrackers}]
                        }]))

                # setting death count to 37 to always have the b.b. wand chest accessible
                buffer = 37
                buffer = buffer.to_bytes(2, byteorder="little")
                ctx.process_handle.write_bytes(slot_address + 0x1E4, buffer, 2)

                if ctx.bean_patcher is not None:
                    # set in-game tracker map stamps to check locations
                    if (aw_settings["in_game_tracker"] > tracker_enum.no_tracker
                            and ctx.bean_patcher.stamps_address is not None):
                        ctx.get_stamps_for_locations(ctx)
                        buffer = len(ctx.stamps).to_bytes(1, byteorder="little")
                        ctx.process_handle.write_bytes(slot_address + 0x225, buffer, 1)
                        for idx, stamp in enumerate(ctx.stamps):
                            ctx.process_handle.write_bytes(ctx.bean_patcher.stamps_address + idx*6, stamp.data(), 6)
                    ctx.bean_patcher.write_to_game()
            else:
                raise NotImplementedError("Only Windows is implemented right now")
        except (pymem.exception.ProcessError, pymem.exception.MemoryReadError, pymem.exception.MemoryWriteError,
                ConnectionResetError) as e:
            bean_logger.error("%s", e)
            ctx.connection_status = CONNECTION_RESET_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")
        except (NotImplementedError, Exception) as e:
            bean_logger.fatal("%s", e)
            ctx.connection_status = CONNECTION_ABORTED_STATUS
            traceback.print_exc()
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")


async def get_animal_well_process_handle(ctx: AnimalWellContext):
    """
    Get the process handle of Animal Well
    """
    try:
        if platform.uname()[0] == "Windows":
            bean_logger.debug("Getting process handle on Windows")
            process_handle = pymem.Pymem("Animal Well.exe")
            bean_logger.debug("Found PID %d", process_handle.process_id)

            ctx.bean_patcher.attach_to_process(process_handle)

            address = ctx.bean_patcher.application_state_address + 0x400

            if address is None:
                savefile_location = \
                    rf"C:\Users\{os.getenv('USERNAME')}\AppData\LocalLow\Billy Basso\Animal Well\AnimalWell.sav"
                bean_logger.debug("Reading save file data from default location: %s", savefile_location)
                with open(savefile_location, "rb") as savefile:
                    slot_1 = bytearray(savefile.read(HEADER_LENGTH + SAVE_SLOT_LENGTH))[HEADER_LENGTH:]

                # Find best pattern
                consecutive_start = 0
                max_length = 0
                current_length = 0
                for i in range(len(slot_1)):
                    current_length += 1
                    if slot_1[i] == 0:
                        current_length = 0
                    elif current_length > max_length:
                        max_length = current_length
                        consecutive_start = i - current_length + 1
                pattern = slot_1[consecutive_start: consecutive_start + max_length]
                bean_logger.debug("Found the longest nonzero consecutive memory at %s of length %s",
                                  hex(consecutive_start), hex(max_length))

                # Preprocess
                pattern_length = len(pattern)
                bad_chars = [-1] * 256
                for i in range(pattern_length):
                    bad_chars[pattern[i]] = i

                # Search
                address = 0
                iterations = 0
                while True:
                    try:
                        iterations += 1
                        if iterations % 0x10000 == 0:
                            await asyncio.sleep(0.05)
                        if iterations % 0x80000 == 0:
                            bean_logger.info("Looking for start address of memory, %s", hex(address))

                        i = pattern_length - 1

                        while i >= 0 and pattern[i] == process_handle.read_bytes(address + i, 1)[0]:
                            i -= 1

                        if i < 0:
                            address -= (HEADER_LENGTH + consecutive_start)
                            break
                        else:
                            address += max(1, i - bad_chars[process_handle.read_bytes(address + i, 1)[0]])
                    except pymem.exception.MemoryReadError:
                        address += max_length

            bean_logger.info("Found start address of memory, %s", hex(address))

            # Verify
            version = process_handle.read_uint(address)
            bean_logger.debug("Found version number %d", version)

            if version != 9:
                raise NotImplementedError("Animal Well version %d detected, only version 9 supported", version)

            ctx.process_handle = process_handle
            ctx.start_address = address

            ctx.bean_patcher.apply_patches()

            host = get_settings()
            tracker_enum = AWSettings.TrackerSetting
            if host.animal_well_settings["in_game_tracker"] > tracker_enum.no_tracker:
                ctx.bean_patcher.apply_tracker_patches()
            else:
                ctx.bean_patcher.revert_tracker_patches()

            ctx.display_dialog("Connected to client!", "")
        else:
            raise NotImplementedError("Only Windows is implemented right now")
    except (pymem.exception.ProcessNotFound, pymem.exception.CouldNotOpenProcess, pymem.exception.ProcessError,
            pymem.exception.MemoryReadError) as e:
        bean_logger.error("%s", e)
        ctx.connection_status = CONNECTION_REFUSED_STATUS
        traceback.print_exc()
        bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")
    except (FileNotFoundError, NotImplementedError, Exception) as e:
        bean_logger.fatal("%s", e)
        ctx.connection_status = CONNECTION_ABORTED_STATUS
        traceback.print_exc()
        bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")


async def process_sync_task(ctx: AnimalWellContext):
    """
    Connect to the Animal Well process
    """
    bean_logger.info("Starting Animal Well connector. Use /connection for status information")
    locations = AWLocations()
    items = AWItems()

    while not ctx.exit_event.is_set():
        if ctx.connection_status == CONNECTION_ABORTED_STATUS:
            return

        elif ctx.connection_status in [CONNECTION_REFUSED_STATUS, CONNECTION_RESET_STATUS]:
            await asyncio.sleep(5)
            bean_logger.info("Attempting to reconnect to Animal Well")
            if ctx.get_animal_well_process_handle_task:
                ctx.get_animal_well_process_handle_task.cancel()
            ctx.get_animal_well_process_handle_task = asyncio.create_task(get_animal_well_process_handle(ctx))
            ctx.connection_status = CONNECTION_TENTATIVE_STATUS
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")

        elif ctx.get_animal_well_process_handle_task is None and ctx.connection_status == CONNECTION_INITIAL_STATUS:
            bean_logger.info("Attempting to connect to Animal Well")
            ctx.get_animal_well_process_handle_task = asyncio.create_task(get_animal_well_process_handle(ctx))
            ctx.connection_status = CONNECTION_TENTATIVE_STATUS
            bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")

        elif (ctx.process_handle and ctx.start_address and ctx.get_animal_well_process_handle_task.done()
              and ctx.bean_patcher.save_file and ctx.current_game_state != 1):
            if ctx.connection_status == CONNECTION_TENTATIVE_STATUS:
                bean_logger.info("Successfully Connected to Animal Well")
                ctx.connection_status = CONNECTION_CONNECTED_STATUS
                bean_logger.info(f"Animal Well Connection Status: {ctx.connection_status}")

            locations.read_from_game(ctx)
            await locations.write_to_archipelago(ctx)
            await items.read_from_archipelago(ctx)
            items.write_to_game(ctx)

            if ctx.bean_patcher is not None and ctx.bean_patcher.attached_to_process:
                await ctx.bean_patcher.tick()

        await asyncio.sleep(0.1)


async def console_task(ctx: AnimalWellContext):
    while not ctx.exit_event.is_set():
        if ctx.bean_patcher is not None and ctx.bean_patcher.attached_to_process:
            ctx.bean_patcher.run_cmd_prompt()
            if cmd := ctx.bean_patcher.get_cmd():
                if cmd[0] == '/':
                    ctx.command_processor(ctx)(cmd)
                else:
                    ctx.command_processor(ctx).default(cmd)
        await asyncio.sleep(1/120)


def launch(*args):
    """
    Launch the client
    """

    async def main(*args):
        """
        main function
        """
        import urllib
        parser = get_base_parser()
        parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
        args = parser.parse_args(args)

        # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
        if args.url:
            url = urllib.parse.urlparse(args.url)
            if url.scheme == "archipelago":
                args.connect = url.netloc
                if url.username:
                    args.name = urllib.parse.unquote(url.username)
                if url.password:
                    args.password = urllib.parse.unquote(url.password)
            else:
                parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

        ctx = AnimalWellContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.process_sync_task = asyncio.create_task(process_sync_task(ctx), name="Animal Well Process Sync")
        try:
            import win32api, win32gui
        except ImportError:
            pass
        else:
            ctx.console_task = asyncio.create_task(console_task(ctx), name="Animal Well Console")

        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

        if ctx.bean_patcher is not None and len(ctx.bean_patcher.revertable_patches) > 0:
            ctx.bean_patcher.revert_patches()

        if ctx.bean_patcher is not None and len(ctx.bean_patcher.revertable_tracker_patches) > 0:
            ctx.bean_patcher.revert_tracker_patches()

        if ctx.bean_patcher is not None:
            ctx.bean_patcher.revert_seeded_save_patch()

        if ctx.process_sync_task:
            ctx.process_sync_task.cancel()
            ctx.process_sync_task = None
        if ctx.get_animal_well_process_handle_task:
            ctx.get_animal_well_process_handle_task.cancel()
            ctx.get_animal_well_process_handle_task = None
        if ctx.console_task:
            ctx.console_task.cancel()
            ctx.console_task = None

    Utils.init_logging("AnimalWellClient")

    import colorama
    colorama.init()
    asyncio.run(main(*args))
    colorama.deinit()
