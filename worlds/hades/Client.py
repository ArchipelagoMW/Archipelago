from __future__ import annotations
import atexit
import os
from pdb import run
import sys
import asyncio
import random
import shutil
from typing import Tuple, List, Iterable, Dict
import threading
import importlib.util
from urllib import request

import websockets
import copy
import Utils
import json
import logging
import pathlib

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop
import settings
import os
import ssl


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
        asyncio.create_task(self.ctx.check_connection_and_send_items_and_request_starting_info(""))


class HadesContext(CommonContext):
    # ----------------- Client start up and ending section starts  --------------------------------
    command_processor = HadesClientCommandProcessor
    game = "Hades"
    items_handling = 0b111  # full remote
    cache_items_received_names = []
    hades_slot_data = None
    players_id_to_name = None
    creating_location_to_item_mapping = False
    missing_locations_cache = []
    checked_locations_cache = []
    location_name_to_id = None
    location_to_item_map_created = False
    deathlink_pending = False
    deathlink_enabled = False
    is_connected = False
    is_receiving_items_from_connect_package = False
    polycosmos_version = "0.12"
    compact_setting_string = ""

    def __init__(self, server_address, password):
        super(HadesContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # Load here any data you might need the client to know about

        # Add hook to comunicate with StyxScribe
        subsume.AddHook(self.send_location_check_to_server, styx_scribe_recieve_prefix + "Locations updated:",
                        "HadesClient")
        subsume.AddHook(self.on_run_completion, styx_scribe_recieve_prefix + "Hades defeated", "HadesClient")
        subsume.AddHook(self.check_connection_and_send_items_and_request_starting_info,
                        styx_scribe_recieve_prefix + "Data requested", "HadesClient")
        # hook to send deathlink to other player when Zag dies
        subsume.AddHook(self.send_death, styx_scribe_recieve_prefix + "Zag died", "HadesClient")
        subsume.AddHook(self.send_location_hint_to_server, styx_scribe_recieve_prefix + "Locations hinted:", "HadesClient")

    async def server_auth(self, password_requested: bool = False):
        # This is called to autentificate with the server.
        if password_requested and not self.password:
            await super(HadesContext, self).server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        await self.send_connect()

    async def connection_closed(self):
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

    def on_package(self, cmd: str, args: dict):
        # This is what is done when a package arrives.
        if cmd == "Connected":
            # What should be done in a connection package
            self.cache_items_received_names.clear()
            self.missing_locations_cache = args["missing_locations"]
            self.checked_locations_cache = args["checked_locations"]
            self.hades_slot_data = args["slot_data"]
            if not (self.hades_slot_data["version_check"]==self.polycosmos_version):
                stringError = "WORLD GENERATED WITH POLYCOSMOS " + self.hades_slot_data["version_check"] \
                            + " AND CLIENT USING POLYCOSMOS " + self.polycosmos_version + "\n"
                stringError += "THIS ARE NOT COMPATIBLE"
                raise Exception(stringError)
            self.location_name_to_id = self.get_location_name_to_id()
            if "death_link" in self.hades_slot_data and self.hades_slot_data["death_link"]:
                asyncio.create_task(self.update_death_link(True))
                self.deathlink_enabled = True
            self.is_connected = True
            self.is_receiving_items_from_connect_package = True 

        if cmd == "RoomInfo":
            # What should be done when room info is sent.
            self.seed_name = args["seed_name"]
        
        if cmd == "RoomUpdate":
            if "checked_lodations" in args:
                collect_locations_cache = ""
                for location in args["checked_locations"]:
                    collect_locations_cache += self.location_names.lookup_in_slot(location) + "-"
                if (len(collect_locations_cache) > 0):
                    collect_locations_cache = collect_locations_cache[:-1]
                    subsume.Send(styx_scribe_send_prefix + "Locations collected:" + collect_locations_cache)

        if cmd == "ReceivedItems":
            # What should be done when an Item is recieved.
            # NOTE THIS GETS ALL ITEMS THAT HAVE BEEN RECIEVED! WE USE THIS FOR RESYNCS!
            for item in args["items"]:
                self.cache_items_received_names += [self.item_names.lookup_in_slot(item.item)]
            msg =  f"Received {', '.join([self.item_names.lookup_in_slot(item.item) for item in args['items']])}"
            # We ignore sending the package to hades if just connected, 
            #since the game is not ready for it (and will request it itself later)
            if (self.is_receiving_items_from_connect_package):
                return;
            self.send_items()

        if cmd == "LocationInfo":
            if self.creating_location_to_item_mapping:
                self.creating_location_to_item_mapping = False
                asyncio.create_task(self.create_location_to_item_dictionary(args["locations"]))
                return
            super().on_package(cmd, args)
            
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"]:
                    self.on_deathlink(args["data"])
         

    def send_items(self):
        payload_message = self.parse_array_to_string(self.cache_items_received_names)
        subsume.Send(styx_scribe_send_prefix + "Items Updated:" + payload_message)

    def parse_array_to_string(self, array_of_items):
        message = ""
        for itemname in array_of_items:
            message += itemname
            message += ","
        return message

    async def send_location_check_to_server(self, message):
        sendingLocationsId = []
        sendingLocationsName = message
        payload_message = []
        sendingLocationsId += [self.location_name_to_id[sendingLocationsName]]
        payload_message += [{"cmd": "LocationChecks", "locations": sendingLocationsId}]
        asyncio.create_task(self.send_msgs(payload_message))


    async def check_connection_and_send_items_and_request_starting_info(self, message):
        if (self.check_for_connection()):
            self.is_receiving_items_from_connect_package = False
            await self.send_items_and_request_starting_info(message)

    async def send_items_and_request_starting_info(self, message):
        self.store_settings_data()
        # send items that were already cached in connect
        self.send_items()
        self.request_location_to_item_dictionary()

    def store_settings_data(self):
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
            
        #Store the compact setting string
        self.compact_setting_string = hades_settings_string
        

    def request_location_to_item_dictionary(self):
        self.creating_location_to_item_mapping = True
        request = self.missing_locations_cache + self.checked_locations_cache
        asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": request, "create_as_hint": 0}]))

    async def create_location_to_item_dictionary(self, itemsdict):
        locationItemMapping = ""
        for networkitem in itemsdict:
            locationItemMapping += self.clear_invalid_char(self.location_names.lookup_in_slot(networkitem.location)) + "--" \
            + self.clear_invalid_char(self.player_names[networkitem.player]) + "--" \
            + self.clear_invalid_char(self.item_names.lookup_in_slot(networkitem.item, networkitem.player)) + "||"
            
        subsume.Send(styx_scribe_send_prefix + "Location to Item Map:" + locationItemMapping)
        self.creating_location_to_item_dictionary = False
        subsume.Send(styx_scribe_send_prefix + "Data finished"+self.compact_setting_string)
    
    def clear_invalid_char(self, inputstring: str):
        newstr = inputstring.replace("{", "")
        newstr = newstr.replace("}","")
        return newstr

    # ----------------- Package Management section ends --------------------------------

    # ----------------- Hints from game section starts --------------------------------

    async def send_location_hint_to_server(self, message):
        if (self.hades_slot_data["store_give_hints"] == 0):
            return;
        split_array = message.split("-")
        request = []
        for location in split_array:
            if (len(location)>0):
                request.append(self.location_name_to_id[location])
        asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": request, "create_as_hint": 2}]))

    # ----------------- Hints from game section ends --------------------------------

    # -------------deathlink section started --------------------------------
    def on_deathlink(self, data: dict):
        # What should be done when a deathlink message is recieved
        if self.deathlink_pending:
            return
        self.deathlink_pending = True
        subsume.Send(styx_scribe_send_prefix + "Deathlink recieved")
        super().on_deathlink(data)
        asyncio.create_task(self.wait_and_lower_deathlink_flag())

    def send_death(self, death_text: str = ""):
        # What should be done to send a death link
        # Avoid sending death if we died from a deathlink
        if self.deathlink_pending or not self.deathlink_enabled:
            return
        self.deathlink_pending = True
        asyncio.create_task(super().send_death(death_text))
        asyncio.create_task(self.wait_and_lower_deathlink_flag())

    async def wait_and_lower_deathlink_flag(self):
        await asyncio.sleep(3)
        self.deathlink_pending = False

    # -------------deathlink section ended

    # -------------game completion section starts
    # this is to detect game completion. Note that on futher updates this will need --------------------------------
    # to be changed to adapt to new game completion conditions
    def on_run_completion(self, message):
        #parse message
        counters = message.split("-") 
        #counters[0] is number of clears, counters[1] is number of different weapons with runs clears.
        
        hasEnoughRuns = self.hades_slot_data["hades_defeats_needed"] <= int(counters[0])
        hasEnoughWeapons = self.hades_slot_data["weapons_clears_needed"] <= int(counters[1])
        hasEnoughKeepsakes = self.hades_slot_data["keepsakes_needed"] <= int(counters[2])
        hasEnoughFates = self.hades_slot_data["fates_needed"] <= int(counters[3])
        if (hasEnoughRuns and hasEnoughWeapons and hasEnoughKeepsakes and hasEnoughFates):
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
            self.finished_game = True

    # -------------game completion section ended --------------------------------

    # ------------ game connection QoL handling
    def check_for_connection(self):
        if (self.is_connected == False):
            subsume.Send(styx_scribe_send_prefix + "Connection Error")
            return False
        return True

    # ------------ Helper method for 0.5.0

    def get_location_name_to_id(self):
        table = {}
        for locationid in self.server_locations:
            table[self.location_names.lookup_in_slot(locationid)] = locationid
        return table

    # ------------ gui section ------------------------------------------------

    def run_gui(self):
        import kvui
        from kvui import GameManager

        class HadesManager(GameManager):
            # logging_pairs for any separate logging tabs
            base_title = "Archipelago Hades Client"

        self.ui = HadesManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)


#  ------------ Methods to start the client + Hades + StyxScribe ------------

def launch_hades():
    subsume.Launch(True, None)


def launch():
    async def main(args):
        ctx = HadesContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()


    import colorama
    # --------------------- Styx Scribe initialization -----------------
    styx_scribe_path = settings.get_settings()["hades_options"]["styx_scribe_path"]
    hadespath = os.path.dirname(styx_scribe_path)

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
