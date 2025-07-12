import asyncio
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import time
import queue
from typing import Dict, Optional, Set
import json
import tempfile
import zipfile

import bsdiff4
import colorama

from NetUtils import ClientStatus, NetworkItem, NetworkPlayer
from settings import get_settings
from worlds.tits_the_3rd.locations import get_location_id, MIN_CRAFT_LOCATION_ID, MAX_CRAFT_LOCATION_ID, craft_location_id_to_character_id_and_level_threshold
from worlds.tits_the_3rd.items import get_item_id
from worlds.tits_the_3rd.names.location_name import LocationName
from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.util import load_file
from worlds.tits_the_3rd.dt_utils import items as dt_items

from .animation_writer import AnimationWriter
from .memory_io import TitsThe3rdMemoryIO
from CommonClient import (
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)


class TitsThe3rdContext(CommonContext):
    """Trails in the Sky the 3rd Context"""

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.game = "Trails in the Sky the 3rd"
        self.items_handling = 0b111  # Fully Remote
        self.game_interface = None
        self.world_player_identifier: bytes = b"\x00\x00\x00\x00"
        self.location_ids = None
        self.location_name_to_ap_id = dict()
        self.location_ap_id_to_name = dict()
        self.item_name_to_ap_id = dict()
        self.item_ap_id_to_name = dict()
        self.last_received_item_index = -1
        self.non_local_locations: Dict[int, tuple] = dict()
        self.non_local_locations_initiated = False
        self.slot_data = None

        self.items_to_be_sent_notification = queue.Queue()
        self.player_name_to_game: Dict[str, str] = dict()

        self.critical_section_lock = asyncio.Lock()

    def init_game_interface(self):
        logger.info("Initiating Game Interface")
        if not self.install_game_mod():
            raise Exception("Error Installing Game Mod")
        logger.info("Finish installing game mod")
        # self.install_dt_patch() #TODO: implement this when we actually have something for this
        self.game_interface = TitsThe3rdMemoryIO(self.exit_event)

    def install_game_mod(self):
        game_dir = Path(get_settings().tits_the_3rd_options.game_installation_path)
        files_in_game_dir = os.listdir(game_dir)
        if not "ed6_win3_DX9.exe" in files_in_game_dir:
            raise Exception("Incorrect game directory")

        lb_ark_folder = game_dir / "data"
        scena_base_folder = lb_ark_folder / "ED6_DT21_BASE"
        scena_game_mod_folder = lb_ark_folder / "ED6_DT21"
        as_base_folder = lb_ark_folder / "ED6_DT30_BASE"
        as_temp_folder = lb_ark_folder / "ED6_DT30_TEMP"
        as_game_mod_folder = lb_ark_folder / "ED6_DT30"
        dt_base_folder = lb_ark_folder / "ED6_DT22_BASE"
        dt_game_mod_folder = lb_ark_folder / "ED6_DT22"
        os.makedirs(lb_ark_folder, exist_ok=True)
        # if "player.txt" in os.listdir(lb_ark_folder):
        if False:
            with open(lb_ark_folder / "player.txt") as player_id_file:
                if player_id_file.read() == f"{self.auth}-{self.seed_name}":
                    logger.info("Player has not changed. Skip installing patch")
                    return True

        if os.path.exists(scena_game_mod_folder):  # Remove previously installed mod for a clean install
            shutil.rmtree(scena_game_mod_folder)

        if os.path.exists(dt_game_mod_folder):  # Remove previously installed mod for a clean install
            shutil.rmtree(dt_game_mod_folder)

        if os.path.exists(as_game_mod_folder):  # Remove previously installed mod for a clean install
            shutil.rmtree(as_game_mod_folder)

        if os.path.exists(as_temp_folder):
            shutil.rmtree(as_temp_folder)

        if not "factoria.exe" in files_in_game_dir:
            raise Exception("factoria.exe not found. Please install factoria from https://github.com/Aureole-Suite/Factoria/releases/tag/v1.0")

        # Create the base game folders
        if not os.path.exists(scena_base_folder):
            factoria_command = f'"{game_dir/ "factoria.exe"}" --output "{scena_base_folder}" "{game_dir / "ED6_DT21.dir"}"'
            subprocess.run(factoria_command, shell=True)

        if not os.path.exists(dt_base_folder):
            factoria_command = f'"{game_dir/ "factoria.exe"}" --output "{dt_base_folder}" "{game_dir / "ED6_DT22.dir"}"'
            subprocess.run(factoria_command, shell=True)

        if not os.path.exists(as_base_folder):
            factoria_command = f'"{game_dir/ "factoria.exe"}" --output "{as_base_folder}" "{game_dir / "ED6_DT30.dir"}"'
            subprocess.run(factoria_command, shell=True)

        # Patch the game scena scripts
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file in sorted(os.listdir(scena_base_folder)):
                if file.endswith("._sn"):
                    zip_file.write(scena_base_folder / file, arcname=f"sn/{file}")

        zip_buffer.seek(0)
        patch = load_file("data/tits3rd_basepatch.bsdiff4")
        output_data = bsdiff4.patch(zip_buffer.read(), patch)
        output_buffer = io.BytesIO(output_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(output_buffer, "r") as output_file:
                output_file.extractall(temp_dir)

            os.makedirs(scena_game_mod_folder, exist_ok=True)
            os.makedirs(as_temp_folder, exist_ok=True)
            os.makedirs(as_game_mod_folder, exist_ok=True)

            sn_folder = os.path.join(temp_dir, "sn")
            if not os.path.exists(sn_folder):
                raise Exception("SN folder not found in patch output! Please contact the maintainer of the mod in the discord.")

            for file_name in os.listdir(sn_folder):
                source_path = os.path.join(sn_folder, file_name)
                shutil.move(source_path, scena_game_mod_folder)

            as_folder = os.path.join(temp_dir, "as")
            if not os.path.exists(as_folder):
                raise Exception("AS folder not found in patch output! Please contact the maintainer of the mod in the discord.")

            for file_name in os.listdir(as_folder):
                source_path = os.path.join(as_folder, file_name)
                shutil.move(source_path, as_temp_folder)

        # Create custom item table
        os.makedirs(dt_game_mod_folder, exist_ok=True)
        game_items, game_items_text = dt_items.parse_item_table(dt_base_folder / "t_item2._dt", dt_base_folder / "t_ittxt2._dt")
        last_item = game_items.pop()
        last_text = game_items_text.pop()

        for location, (player, game, item_id) in self.non_local_locations.items():
            item_name = f"{player}'s {self.item_ap_id_to_name[game][item_id]}"
            item, item_text = dt_items.create_non_local_item(50000 + location, item_name)

            game_items.append(item)
            game_items_text.append(item_text)

        game_items.append(last_item)
        game_items_text.append(last_text)

        dt_items.write_item_table(dt_game_mod_folder / "t_item2._dt", game_items)
        dt_items.write_item_text_table(dt_game_mod_folder / "t_ittxt2._dt", game_items_text)

        with open(lb_ark_folder / "player.txt", "w") as player_id_file:
            player_id_file.write(f"{self.auth}-{self.seed_name}")

        # t_magic modifications
        subprocess.run([
            os.path.join(game_dir, "factoria.exe"),
            "--output",
            os.path.join(lb_ark_folder, "ED6_DT22"),
            os.path.join(game_dir, "ED6_DT22.dir"),
        ], check=True)

        if self.slot_data["old_craft_id_to_new_craft_id"]:
            try:
                t_magic_path = os.path.join(lb_ark_folder, "ED6_DT22", "t_magic._dt")
                if not "T_MAGIC_Converter.exe" in files_in_game_dir:
                    raise Exception("T_MAGIC_Converter.exe not found. Please install T_MAGIC_Converter from <link>") #TODO: add link
                t_magic_converter_path = os.path.join(game_dir, "T_MAGIC_Converter.exe")
                try:
                    subprocess.run([
                        t_magic_converter_path,
                        t_magic_path,
                    ], check=True)
                except subprocess.CalledProcessError as err:
                    raise Exception(f"Error running t_magic_converter: {err}")
                from pprint import pprint
                t_magic_json_output_path = os.path.join(game_dir, "output", "t_magic.json")
                new_craft_id_to_old_craft_id = {v: k for k, v in self.slot_data["old_craft_id_to_new_craft_id"].items()}
                pprint(new_craft_id_to_old_craft_id)
                pprint(self.slot_data["craft_get_order"])
                with open(t_magic_json_output_path, "r") as t_magic_json_file:
                    t_magic_json = json.load(t_magic_json_file)
                    new_t_magic_json = {"Data": []}
                    for ability in t_magic_json["Data"]:
                        ability_copy = ability.copy()
                        if int(ability_copy["ID"]) in new_craft_id_to_old_craft_id:
                            new_id = int(new_craft_id_to_old_craft_id[int(ability_copy["ID"])])
                            ability_copy["ID"] = new_id
                        new_t_magic_json["Data"].append(ability_copy)
                    with open(t_magic_json_output_path, "w") as t_magic_json_file:
                        json.dump(new_t_magic_json, t_magic_json_file)
                try:
                    subprocess.run([
                        t_magic_converter_path,
                        t_magic_json_output_path
                    ], check=True)
                except subprocess.CalledProcessError as err:
                    raise Exception(f"Error running t_magic_converter: {err}")
                shutil.move(os.path.join(game_dir, "output", "t_magic._dt"), os.path.join(lb_ark_folder, "ED6_DT22", "t_magic._dt"))
            except Exception as err:
                logger.error(f"Error running t_magic_converter: {err}")
                raise err
            finally:
                output_dir = os.path.join(game_dir, "output")
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
        try:
            t_crtget_path = os.path.join(lb_ark_folder, "ED6_DT22", "t_crfget._dt")
            with open(t_crtget_path, "rb") as f:
                data = bytearray(f.read())
            pos = 0x28
            while pos < len(data):
                value = int.from_bytes(data[pos:pos+2], "little", signed=False)
                if value != 0xFFFF:
                    data[pos:pos+2] = (999).to_bytes(2, "little", signed=False)
                pos += 4
            with open(t_crtget_path, "wb") as f:
                f.write(data)
        except Exception as err:
            logger.error(f"Error modifying t_crfget: {err}")
            raise err
        try:
            animation_writer = AnimationWriter(as_temp_folder)
            for old_craft_id, new_craft_id in self.slot_data["old_craft_id_to_new_craft_id"].items():
                animation_writer.write_animation(int(new_craft_id), int(old_craft_id))
        except Exception as err:
            logger.error(f"Error writing craft animation: {err}")
        if not "AS_Converter.exe" in files_in_game_dir:
            raise Exception("AS_Converter.exe not found. Please install AS_Converter from <link>") #TODO: add link
        as_converter_path = os.path.join(game_dir, "AS_Converter.exe")
        try:
            subprocess.run([
                as_converter_path,
                os.path.join(as_temp_folder),
                os.path.join(game_dir, "outbin"),
            ], check=True)
        except Exception as err:
            logger.error(f"Error running AS_Converter: {err}")
            raise err
        try:
            for file_name in os.listdir(as_base_folder):
                source_path = os.path.join(as_base_folder, file_name)
                dest_path = os.path.join(as_game_mod_folder, file_name)
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, dest_path)
            for file_name in os.listdir("outbin"):
                source_path = os.path.join("outbin", file_name)
                dest_path = os.path.join(as_game_mod_folder, file_name.lower())
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, dest_path)
            shutil.rmtree("outbin")
        except Exception as err:
            logger.error(f"Error moving files from as_base_folder to as_game_mod_folder: {err}")
            raise err

        return True

    def reset_client_state(self):
        """
        Resets the client state to the initial state.
        """
        self.game_interface = None
        self.world_player_identifier = b"\x00\x00\x00\x00"
        self.location_ids = None
        self.location_name_to_ap_id = dict()
        self.location_ap_id_to_name = dict()
        self.item_name_to_ap_id = dict()
        self.item_ap_id_to_name = dict()
        self.last_received_item_index = -1
        self.items_to_be_sent_notification = queue.Queue()
        self.locations_checked = set()
        self.non_local_locations = dict()
        self.non_local_locations_initiated = False
        self.player_name_to_game = dict()
        self.slot_data = None
        self.next_craft_idx = {name: 0 for name in CHARACTER_ID_TO_NAME.values()}

    async def server_auth(self, password_requested: bool = False):
        """Wrapper for login."""
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            # if we dont have the seed name from the RoomInfo packet, wait until we do.
            while not self.seed_name:
                time.sleep(1)
            # Hash the seed name + player name and take the first 4 bytes as the world player identifier.
            self.world_player_identifier = f"{self.seed_name}-{self.auth}"
            self.world_player_identifier = (hashlib.sha256(self.world_player_identifier.encode()).digest())[:4]
            self.location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.locations_checked = set(args["checked_locations"])
            self.slot_data = args["slot_data"]

            games = set()
            for player in [NetworkPlayer(*player) for player in args["players"]]:
                self.player_name_to_game[player.name] = self.slot_info[player.slot].game
                games.add(self.slot_info[player.slot].game)

            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": list(games)}]))
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": self.location_ids}]))

        elif cmd == "LocationInfo":
            if not self.non_local_locations_initiated:
                for item in [NetworkItem(*item) for item in args["locations"]]:
                    receiving_player = self.player_names[item.player]
                    current_player = self.slot_info[self.slot].name
                    if receiving_player != current_player:
                        original_game = self.player_name_to_game[receiving_player]
                        self.non_local_locations[item.location] = (receiving_player, original_game, item.item)
                self.non_local_locations_initiated = True

        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

        elif cmd == "DataPackage":
            if not self.location_ids:
                # Connected package not recieved yet, wait for datapackage request after connected package
                return

            for game, game_data in args["data"]["games"].items():
                self.item_name_to_ap_id[game] = game_data["item_name_to_id"]
                self.item_ap_id_to_name[game] = {v: k for k, v in self.item_name_to_ap_id[game].items()}
            self.location_name_to_ap_id = args["data"]["games"]["Trails in the Sky the 3rd"]["location_name_to_id"]
            self.location_name_to_ap_id = {name: loc_id for name, loc_id in self.location_name_to_ap_id.items() if loc_id in self.location_ids}
            self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
            # self.item_name_to_ap_id = args["data"]["games"]["Trails in the Sky the 3rd"]["item_name_to_id"]
            # self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}

    def client_recieved_initial_server_data(self):
        """
        This returns true if the client has finished the initial conversation with the server.
        This means:
            - Authenticated with the server (self.auth is set)
            - RoomInfo package recieved (self.seed_name is set)
            - World player identifier is calculated based on the seed and player name (self.world_player_identifier is set)
        """
        return self.auth and self.seed_name and self.world_player_identifier and self.non_local_locations_initiated

    async def give_item(self):
        self.last_received_item_index = self.game_interface.read_last_item_receive_index()
        try:
            current_item = self.items_received[self.last_received_item_index + 1]
        except IndexError:
            current_item = None

        result = False

        if current_item:
            item_id = current_item.item
            # Special case where we don't actually want to give anything but just acknowledge it
            if item_id is None or item_id >= 500000:
                result = True
            # Unlock location
            elif (get_item_id(ItemName.craft_min_id) <= item_id <= get_item_id(ItemName.craft_max_id)): # Craft get
                craft_idx = 0
                for past_item in self.items_received[:self.last_received_item_index + 1]:
                    if past_item.item == item_id:
                        craft_idx += 1
                character_id = item_id - get_item_id(ItemName.craft_min_id)
                craft_id = self.slot_data["craft_get_order"][self.game_interface.CHARACTER_ID_TO_NAME[character_id]][craft_idx]
                result = self.game_interface.give_craft(character_id, craft_id)
            elif get_item_id(ItemName.area_min_id) <= item_id <= get_item_id(ItemName.area_max_id):
                result = self.game_interface.unlock_area(item_id - get_item_id(ItemName.area_min_id))
            # Unlock character
            elif get_item_id(ItemName.character_min_id) <= item_id <= get_item_id(ItemName.character_max_id):
                result = self.game_interface.unlock_character(item_id - get_item_id(ItemName.character_min_id))
            # Give Mira
            elif get_item_id(ItemName.mira_min_id) <= item_id <= get_item_id(ItemName.mira_max_id):
                result = self.game_interface.give_mira(item_id - get_item_id(ItemName.mira_min_id))
            # Give lower element sepith
            elif get_item_id(ItemName.lower_elements_sepith_min_id) <= item_id <= get_item_id(ItemName.lower_elements_sepith_max_id):
                result = self.game_interface.give_low_sepith(item_id - get_item_id(ItemName.lower_elements_sepith_min_id))
            # Give higher element sepith
            elif get_item_id(ItemName.higher_elements_sepith_min_id) <= item_id <= get_item_id(ItemName.higher_elements_sepith_max_id):
                result = self.game_interface.give_high_sepith(item_id - get_item_id(ItemName.higher_elements_sepith_min_id))
            # Give Recipe
            elif get_item_id(ItemName.recipe_min_id) <= item_id <= get_item_id(ItemName.recipe_max_id):
                result = self.game_interface.give_recipe(item_id - get_item_id(ItemName.recipe_min_id))
            # Just a normal item
            else:
                result = self.game_interface.give_item(item_id, 1)
            if result:
                while self.game_interface.is_in_event():
                    await asyncio.sleep(0.1)
                self.game_interface.write_last_item_receive_index(self.last_received_item_index + 1)
            await asyncio.sleep(0.1)

    async def send_item(self):
        if not self.items_to_be_sent_notification.empty():
            item_to_be_sent = self.items_to_be_sent_notification.get()
            item_id = 50000 + int(item_to_be_sent)  # Make that non native item be 50000 + location_id
            result = self.game_interface.send_item(item_id)
            if not result:
                self.items_to_be_sent_notification.put(item_to_be_sent)
            while self.game_interface.is_in_event():
                await asyncio.sleep(0.1)

    async def wait_for_ap_connection(self):
        """
        This method waits until the client finishes the initial connection with the server.
        See client_recieved_initial_server_data for wait requirements
        """
        if self.client_recieved_initial_server_data():
            return
        logger.info("Waiting for connect from server...")
        while not self.client_recieved_initial_server_data() and not self.exit_event.is_set():
            await asyncio.sleep(1)
        if not self.exit_event.is_set():
            # wait an extra second to process data
            await asyncio.sleep(1)
            logger.info("Received initial data from server!")

    async def check_location(self, location_id: int):
        if not self.game_interface.should_send_and_recieve_items(self.world_player_identifier):
            return
        if location_id == get_location_id(LocationName.grancel_castle_queens_bedroom):
            # Chapter 1 boss defeated
            self.finished_game = True
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        self.locations_checked.add(location_id)
        await self.send_msgs([{"cmd": "LocationChecks", "locations": self.locations_checked}])
        if location_id in self.non_local_locations:
            self.items_to_be_sent_notification.put(location_id)

    async def check_for_locations(self):
        for location_id in self.location_ids:
            if location_id in self.locations_checked:
                continue
            if (
                MIN_CRAFT_LOCATION_ID <= location_id <= MAX_CRAFT_LOCATION_ID
                and location_id in craft_location_id_to_character_id_and_level_threshold
            ):
                character_id, level_threshold = craft_location_id_to_character_id_and_level_threshold[location_id]
                if not self.game_interface.has_character(character_id):
                    continue
                if self.game_interface.read_character_level(character_id) >= level_threshold:
                    await self.check_location(location_id)
            if self.game_interface.read_flag(location_id):
                await self.check_location(location_id)


async def tits_the_3rd_watcher(ctx: TitsThe3rdContext):
    """
    Client loop, watching the Trails in the Sky the 3rd game process.
    Handles game hook attachments, checking locations, giving items, calling scena methods, etc.

    Args:
        ctx (TitsThe3rdContext): The Trails in the Sky the 3rd context instance.
    """
    await ctx.wait_for_ap_connection()
    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.1)

        if not ctx.server:
            # client disconnected from server
            ctx.reset_client_state()
            await ctx.wait_for_ap_connection()
            continue

        if not ctx.game_interface:
            ctx.init_game_interface()

        if not ctx.game_interface.is_connected():
            await ctx.game_interface.connect()
            continue

        if ctx.game_interface.should_write_world_player_identifier():
            logger.info(f"Game Start Dectected. Setting up AP Verification Hook")
            ctx.game_interface.write_world_player_identifier(ctx.world_player_identifier)
            logger.info(f"AP Verification Hook Set. You can now save and resume the game for this AP Seed")
            continue

        try:
            if ctx.exit_event.is_set():
                break

            if ctx.game_interface.should_send_and_recieve_items(ctx.world_player_identifier):
                await ctx.check_for_locations()

            if ctx.game_interface.is_valid_to_receive_item() and ctx.game_interface.should_send_and_recieve_items(wpid=ctx.world_player_identifier):
                await ctx.send_item()

            if ctx.game_interface.is_valid_to_receive_item() and ctx.game_interface.should_send_and_recieve_items(wpid=ctx.world_player_identifier):
                await ctx.give_item()

        except Exception as err:
            logger.warning("*******************************")
            logger.warning("Encountered error. Please post a message to the thread on the AP discord: https://discord.com/channels/731205301247803413/1217595862872490065")
            logger.warning("*******************************")
            logger.exception(str(err))
            # attempt to reconnect at the top of the loop
            continue


def launch():
    """
    Launch a client instance (wrapper / args parser)
    """

    async def main(args):
        """
        Launch a client instance (threaded)
        """
        ctx = TitsThe3rdContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="TitsThe3rdServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        watcher = asyncio.create_task(tits_the_3rd_watcher(ctx), name="TitsThe3rdProgressionWatcher")
        await ctx.exit_event.wait()
        await watcher
        await ctx.shutdown()

    parser = get_base_parser(description="Trails in the Sky the 3rd Client")
    args, _ = parser.parse_known_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
