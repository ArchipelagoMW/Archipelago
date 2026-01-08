import os
import sys
import asyncio
import threading
import importlib.util
import Utils
import pathlib
from typing import Dict, NamedTuple, Optional

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop
import settings


# --------------------- Styx Scribe useful globals -----------------
global subsume

styx_scribe_recieve_prefix = "Polycosmos to Client:"
styx_scribe_send_prefix = "Client to Polycosmos:"     

# --------------------- Styx Scribe useful globals -----------------


# Here we implement methods for the client

class HadesClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        #This is a really stupid solution, but it works so idk
        Utils.async_start(self.ctx.check_connection_and_send_items_and_request_starting_info(""))


class HadesContext(CommonContext):
    # ----------------- Client start up and ending section starts  --------------------------------
    command_processor = HadesClientCommandProcessor
    game = "Hades"
    items_handling = 0b111  # full remote
    polycosmos_version = "0.14"
    
    is_connected : bool
    deathlink_pending : bool
    deathlink_enabled : bool
    creating_location_to_item_mapping : bool
    is_receiving_items_from_connect_package : bool    
    
    location_name_to_id : dict

    def __init__(self, server_address: Optional[str] = None, password: Optional[str] = None):
        super(HadesContext, self).__init__(server_address, password)
        self.hades_slot_data = None
        
        self.is_connected = False
        self.deathlink_pending = False
        self.deathlink_enabled = False
        self.creating_location_to_item_mapping = False
        self.is_receiving_items_from_connect_package = False

        self.missing_locations_cache = []
        self.checked_locations_cache = []


        # Add hook to comunicate with StyxScribe
        subsume.AddHook(self.send_location_check_to_server, styx_scribe_recieve_prefix + "Locations updated:",
                        "HadesClient")
        subsume.AddHook(self.on_run_completion, styx_scribe_recieve_prefix + "Hades defeated", "HadesClient")
        subsume.AddHook(self.check_connection_and_send_items_and_request_starting_info,
                        styx_scribe_recieve_prefix + "Data requested", "HadesClient")
        # hook to send deathlink to other player when Zag dies
        subsume.AddHook(self.send_death, styx_scribe_recieve_prefix + "Zag died", "HadesClient")
        subsume.AddHook(self.send_location_hint_to_server, styx_scribe_recieve_prefix \
            + "Locations hinted:", "HadesClient")

    async def server_auth(self, password_requested: bool = False) -> None:
        # This is called to autentificate with the server.
        if password_requested and not self.password:
            await super(HadesContext, self).server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        await self.send_connect()

    async def connection_closed(self) -> None:
        # This is called when the connection is closed (duh!)
        # This will send the message always, but only process by Styx scribe if actually in game
        subsume.Send(styx_scribe_send_prefix + "Connection Error")
        self.is_connected = False
        self.is_receiving_items_from_connect_package = False
        await super(HadesContext, self).connection_closed()

    # Do not touch this
    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        # What is called when the app gets shutdown
        subsume.close()
        await super(HadesContext, self).shutdown()

    # ----------------- Client start up and ending section end  --------------------------------

    # ----------------- Package Management section starts --------------------------------

    def on_package(self, cmd: str, args: dict) -> None:
        # This is what is done when a package arrives.
        if cmd == "Connected":
            # What should be done in a connection package
            self.hades_slot_data = args["slot_data"]
            if not (self.hades_slot_data["version_check"] == self.polycosmos_version):
                stringError = "WORLD GENERATED WITH POLYCOSMOS " + self.hades_slot_data["version_check"] \
                            + " AND CLIENT USING POLYCOSMOS " + self.polycosmos_version + "\n"
                stringError += "THESE ARE NOT COMPATIBLE"
                raise Exception(stringError)
            
            self.location_name_to_id = self.get_location_name_to_id()

            if "death_link" in self.hades_slot_data and self.hades_slot_data["death_link"]:
                Utils.async_start(self.update_death_link(True))
                self.deathlink_enabled = True
            self.is_connected = True
            self.is_receiving_items_from_connect_package = True 

        if cmd == "RoomInfo":
            # What should be done when room info is sent.
            self.seed_name = args["seed_name"]
        
        if cmd == "RoomUpdate":
             if "checked_lodations" in args and len(args["checked_locations"]) > 0:
                subsume.Send(styx_scribe_send_prefix + "Locations collected:" + "-".join(
                    (location) for location in args["checked_locations"]
                ))

        if cmd == "ReceivedItems":
            # We ignore sending the package to hades if just connected,
            # since the game is not ready for it (and will request it itself later)
            if self.is_receiving_items_from_connect_package:
                return
            self.send_items()

        if cmd == "LocationInfo":
            if self.creating_location_to_item_mapping:
                self.creating_location_to_item_mapping = False
                self.create_location_to_item_dictionary(args["locations"])
                return
            super().on_package(cmd, args)
        
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"]:
                    self.on_deathlink(args["data"])

    def send_items(self) -> None:
        payload_message = ",".join(self.item_names.lookup_in_game(item.item) for item in self.items_received)
        subsume.Send(styx_scribe_send_prefix + "Items Updated:" + payload_message)

    async def send_location_check_to_server(self, message : str) -> None:
        await self.check_locations([self.location_name_to_id[message]])

    async def check_connection_and_send_items_and_request_starting_info(self, message : str) -> None:
        if self.check_for_connection():
            self.is_receiving_items_from_connect_package = False
            # send items that were already cached in connect
            self.send_items()
            self.request_location_to_item_dictionary()

    def store_settings_data(self) -> None:
        hades_settings_string = ""
        #codify in the string all heat settings
        hades_settings_string += str(self.hades_slot_data["heat_system"]) + "-"
        hades_settings_string += str(self.hades_slot_data["hard_labor_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["lasting_consequences_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["convenience_fee_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["jury_summons_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["extreme_measures_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["calisthenics_program_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["benefits_package_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["middle_management_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["underworld_customs_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["forced_overtime_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["heightened_security_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["routine_inspection_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["damage_control_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["approval_process_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["tight_deadline_pact_amount"]) + "-"
        hades_settings_string += str(self.hades_slot_data["personal_liability_pact_amount"]) + "-"
                
        #Codify in the string all the fillers values
        hades_settings_string += str(self.hades_slot_data["darkness_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["keys_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["gemstones_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["diamonds_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["titan_blood_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["nectar_pack_value"]) + "-"
        hades_settings_string += str(self.hades_slot_data["ambrosia_pack_value"]) + "-"

        #Codify in the string all game settings
        hades_settings_string += str(self.hades_slot_data["location_system"]) + "-"
        hades_settings_string += str(self.hades_slot_data["reverse_order_em"]) + "-"
        hades_settings_string += str(self.hades_slot_data["keepsakesanity"]) + "-"
        hades_settings_string += str(self.hades_slot_data["weaponsanity"]) + "-"
        hades_settings_string += str(self.hades_slot_data["storesanity"]) + "-"
        hades_settings_string += str(self.hades_slot_data["initial_weapon"]) + "-"
        hades_settings_string += str(self.hades_slot_data["ignore_greece_deaths"]) + "-"
        hades_settings_string += str(self.hades_slot_data["fatesanity"]) + "-"
        hades_settings_string += str(self.hades_slot_data["hidden_aspectsanity"]) + "-"
        hades_settings_string += str(self.polycosmos_version) + "-"
        hades_settings_string += str(self.hades_slot_data["automatic_rooms_finish_on_hades_defeat"]) + "-"

        #Codify in the string all the finishing conditions
        hades_settings_string += str(self.hades_slot_data["hades_defeats_needed"]) + "-"
        hades_settings_string += str(self.hades_slot_data["weapons_clears_needed"]) + "-"
        hades_settings_string += str(self.hades_slot_data["keepsakes_needed"]) + "-"
        hades_settings_string += str(self.hades_slot_data["fates_needed"]) + "-"
            
        return hades_settings_string

    def request_location_to_item_dictionary(self) -> None:
        self.creating_location_to_item_mapping = True
        request = self.server_locations
        Utils.async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": request, "create_as_hint": 0}]))

    def create_location_to_item_dictionary(self, itemsdict : Optional[dict]) -> None:
        locationItemMapping = ""
        for networkitem in itemsdict:

            location = self.parse_to_len_encode(self.location_names.lookup_in_slot(networkitem.location))
            player_name = self.parse_to_len_encode(self.player_names[networkitem.player])
            item_name = self.parse_to_len_encode(self.item_names.lookup_in_slot(networkitem.item, networkitem.player))
                        
            locationItemMapping += self.parse_to_len_encode(location+player_name+item_name)
            
        subsume.Send(styx_scribe_send_prefix + "Location to Item Map:" + locationItemMapping)
        subsume.Send(styx_scribe_send_prefix + "Data finished" + self.store_settings_data())
    
    def parse_to_len_encode(self, inputstring: str) -> str:
        output = self.clear_invalid_char(inputstring)
        return str(len(output)) + "|" + output

    def clear_invalid_char(self, inputstring: str) -> str:
        newstr = inputstring.replace("{", "")
        newstr = newstr.replace("}", "")
        return newstr

    # ----------------- Package Management section ends --------------------------------

    # ----------------- Hints from game section starts --------------------------------

    async def send_location_hint_to_server(self, message : str) -> None:
        if self.hades_slot_data["store_give_hints"] == 0:
            return
        split_array = message.split("-")
        request = []
        for location in split_array:
            if len(location) > 0:
                request.append(self.location_name_to_id[location])
        Utils.async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": request, "create_as_hint": 2}]))

    # ----------------- Hints from game section ends ------------------------

    # -------------deathlink section started --------------------------------
    def on_deathlink(self, data: dict) -> None:
        # What should be done when a deathlink message is recieved
        if self.deathlink_pending:
            return
        self.deathlink_pending = True
        subsume.Send(styx_scribe_send_prefix + "Deathlink received")
        super().on_deathlink(data)
        Utils.async_start(self.wait_and_lower_deathlink_flag())

    def send_death(self, death_text: str = "") -> None:
        # What should be done to send a death link
        # Avoid sending death if we died from a deathlink
        if self.deathlink_pending or not self.deathlink_enabled:
            return
        self.deathlink_pending = True
        Utils.async_start(super().send_death(death_text))
        Utils.async_start(self.wait_and_lower_deathlink_flag())

    async def wait_and_lower_deathlink_flag(self) -> None:
        await asyncio.sleep(3)
        self.deathlink_pending = False

    # -------------deathlink section ended

    # -------------game completion section starts
    # this is to detect game completion. Note that on futher updates this will need --------------------------------
    # to be changed to adapt to new game completion conditions
    def on_run_completion(self, message : str) -> None:
        #parse message
        counters = message.split("-") 
        #counters[0] is number of clears, counters[1] is number of different weapons with runs clears.
        
        hasEnoughRuns = self.hades_slot_data["hades_defeats_needed"] <= int(counters[0])
        hasEnoughWeapons = self.hades_slot_data["weapons_clears_needed"] <= int(counters[1])
        hasEnoughKeepsakes = self.hades_slot_data["keepsakes_needed"] <= int(counters[2])
        hasEnoughFates = self.hades_slot_data["fates_needed"] <= int(counters[3])
        if hasEnoughRuns and hasEnoughWeapons and hasEnoughKeepsakes and hasEnoughFates:
            Utils.async_start(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
            self.finished_game = True

    # -------------game completion section ended --------------------------------

    # ------------ game connection QoL handling
    def check_for_connection(self) -> bool:
        if not self.is_connected:
            subsume.Send(styx_scribe_send_prefix + "Connection Error")
            return False
        return True

    # ------------ Helper method to invert lookup table. Can erase if AP has its own internal one.

    def get_location_name_to_id(self):
        table = {}
        for locationid in self.server_locations:
            table[self.location_names.lookup_in_slot(locationid)] = locationid
        return table


    # ------------ gui section ------------------------------------------------

    def run_gui(self) -> None:
        from kvui import GameManager

        class HadesManager(GameManager):
            # logging_pairs for any separate logging tabs
            base_title = "Archipelago Hades Client"

        self.ui = HadesManager(self)
        self.ui_task = Utils.async_start(self.ui.async_run(), name="UI")

#  ------------ Methods to start the client + Hades + StyxScribe ------------

def launch_hades():
    subsume.Launch(True, None)


def launch():
    async def main(args):
        ctx = HadesContext(args.connect, args.password)
        ctx.server_task = Utils.async_start(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama
    # --------------------- Styx Scribe initialization -----------------
    styx_scribe_path = settings.get_settings()["hades_options"]["styx_scribe_path"]

    # Parsing of styxscribe path. This will try to find it on the same folder if it fails.
    last_slash = styx_scribe_path.rfind("/")
    if (last_slash == -1):
        print("Invalid path given to hades client for styxscribe. Cant parse")
        return

    filesbstr = styx_scribe_path[last_slash + 1 :]
    if (filesbstr != "StyxScribe.py"):
        print("Path given does not correspond to StyxScribe. Attempting to parse")
        styx_scribe_path = styx_scribe_path[:last_slash + 1] + "StyxScribe.py"

    hadespath = os.path.dirname(styx_scribe_path)

    if (not os.path.exists(hadespath)):
        print("Styx scribe not found at path.")

    spec = importlib.util.spec_from_file_location("StyxScribe", str(styx_scribe_path))
    styx_scribe = importlib.util.module_from_spec(spec)
    sys.modules["StyxScribe"] = styx_scribe
    spec.loader.exec_module(styx_scribe)

    global subsume
    subsume = styx_scribe.StyxScribe("Hades")
    # hack to make it work without chdir
    subsume.proxy_purepaths = {
        None: hadespath / subsume.executable_cwd_purepath / styx_scribe.LUA_PROXY_STDIN,
        False: hadespath / subsume.executable_cwd_purepath / styx_scribe.LUA_PROXY_FALSE,
        True: hadespath / subsume.executable_cwd_purepath / styx_scribe.LUA_PROXY_TRUE
    }
    subsume.args[0] = os.path.normpath(os.path.join(hadespath, subsume.args[0]))
    subsume.executable_purepath = pathlib.PurePath(hadespath, subsume.executable_purepath)
    for i in range(len(subsume.plugins_paths)):
        subsume.plugins_paths[i] = pathlib.PurePath(hadespath, subsume.plugins_paths[i])

    subsume.LoadPlugins()
    # --------------------- Styx Scribe initialization -----------------

    thr = threading.Thread(target=launch_hades, args=(), kwargs={})
    thr.start()
    parser = get_base_parser()
    args = parser.parse_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
