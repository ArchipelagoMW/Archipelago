import asyncio
import hashlib
import io
import json
import os
import multiprocessing
import copy
import pathlib
import random
import subprocess
import sys
import time
from typing import Union
import zipfile
from asyncio import StreamReader, StreamWriter
import bsdiff4


# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
import settings
from Utils import async_start
from worlds import network_data_package

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure banjoTooie_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    isDead: bool,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    playerNames: list,
    triggerDeath: bool,
    messages: string
}

Deathlink logic:
"Dead" is true <-> Banjo is at 0 hp.

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

"""

bt_loc_name_to_id = network_data_package["games"]["Banjo-Tooie"]["location_name_to_id"]
bt_itm_name_to_id = network_data_package["games"]["Banjo-Tooie"]["item_name_to_id"]
script_version: int = 4
version: str = "V4.4.2"
game_append_version: str = "V44"
patch_md5: str = "e1549e5f99c73ea442e1b78d17fdf66b"

def get_item_value(ap_id):
    return ap_id

async def run_game(romfile):
        auto_start = settings.get_settings()["banjo-tooie_options"].get("rom_start", True)
        if auto_start is True:
            import webbrowser
            webbrowser.open(romfile)
        elif os.path.isfile(auto_start):
            subprocess.Popen([auto_start, romfile],
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def apply_patch():
    fpath = pathlib.Path(__file__)
    archipelago_root = None
    for i in range(0, 5,+1) :
        if fpath.parents[i].stem == "Archipelago":
            archipelago_root = pathlib.Path(__file__).parents[i]
            break
    patch_path = None
    if archipelago_root:
        patch_path = os.path.join(archipelago_root, "Banjo-Tooie-AP"+game_append_version+".z64")
    if not patch_path or check_rom(patch_path) != patch_md5:
        logger.info("Please open Banjo-Tooie and load banjo_tooie_connector.lua")
        await asyncio.sleep(0.01)
        rom = Utils.open_filename("Open your Banjo-Tooie US ROM", (("Rom Files", (".z64", ".n64")), ("All Files", "*"),))
        if not rom:
            logger.info("No ROM selected. Please restart the Banjo-Tooie Client to try again.")
            return
        if not patch_path:
            patch_path = os.path.split(rom) + "/Banjo-Tooie-AP"+game_append_version+".z64"
        patch_rom(rom, patch_path, "Banjo-Tooie.patch")
    if patch_path:
        logger.info("Patched Banjo-Tooie is located in " + patch_path)


class BanjoTooieCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, BanjoTooieContext):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, BanjoTooieContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")


class BanjoTooieContext(CommonContext):
    command_processor = BanjoTooieCommandProcessor
    items_handling = 0b111 #full

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Banjo-Tooie"
        self.n64_streams: (StreamReader, StreamWriter) = None # type: ignore
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.movelist_table = {}
        self.cheatorewardslist_table = {}
        self.honeybrewardslist_table = {}
        self.treblelist_table = {}
        self.stationlist_table = {}
        self.jinjofamlist_table = {}
        self.jinjolist_table = {}
        self.pages_table = {}
        self.honeycomb_table = {}
        self.glowbo_table = {}
        self.doubloon_table = {}
        self.notes_table = {}
        self.worldlist_table = {}
        self.chuffy_table = {}
        self.mystery_table = {}
        self.roystenlist_table = {}
        self.jiggychunks_table = {}
        self.goggles_table = False
        self.dino_kids_table = {}
        self.signpost_table = {}
        self.warppads_table = {}
        self.silos_table = {}
        self.nests_table = {}
        self.roar = False
        self.jiggy_table = {}
        self.current_map = 0
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False
        self.version_warning = False
        self.messages = {}
        self.slot_data = {}
        self.sendSlot = False
        self.sync_ready = False
        self.startup = False
        self.handled_scouts = []
        # AquaPhoenix Contributed with the Gruntilda Insults
        self.death_messages = [
            "Gruntilda:    Did you hear that lovely clack, \n                     My broomstick gave you such a whack!",
            "Gruntilda:    AAAH! I see it makes you sad, \n                     To know your skills are really bad!",
            "Gruntilda:    I hit that bird right on the beak, \n                     Let it be the end of her cheek!",
            "Gruntilda:    My fiery blast you just tasted, \n                     Grunty's spells on you are wasted!",
            "Gruntilda:    Hopeless bear runs to and fro, \n                     But takes a whack for being so slow!",
            "Gruntilda:    So I got you there once more, \n                     I knew your skills were very poor!",
            "Gruntilda:    Simply put I'm rather proud, \n                     Your yelps and screams I heard quite loud!",
            "Gruntilda:    Grunty's fireball you did kiss, \n                     You're so slow I can hardly miss!",
            "Gruntilda:    In this world you breathe your last,\n                     Now your friends had better think fast!",
            "Gruntilda:    This is fun it's quite a treat, \n                     To see you suffer in defeat",
            "Gruntilda:    That death just now, I saw coming, \n                     Your skill issues are rather stunning!",
            "Gruntilda:    Seeing this pathetic display, \n                     Is serotonin in my day",
            "Gruntilda:    What a selfish thing to do,\n                     Your friends just died because of you!",
            "Gruntilda:    You tried something rather stupid,\n                     I hope no one will try what you did"
        ]

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BanjoTooieContext, self).server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            self.awaiting_rom = True
            return
        return

    def _set_message(self, msg: dict, msg_id: Union[int, None]):
        if msg_id == None:
            self.messages.update({len(self.messages)+1: msg })
        else:
            self.messages.update({msg_id:msg})

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")

    async def send_death(self, death_text: str = ""):
        if self.server and self.server.socket:
            logger.info(f"{random.choice(self.death_messages)} \n(DeathLink: Sending death to your friends...)")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.player_names[self.slot],
                    "cause": death_text
                }
            }])

    def run_gui(self):
        from kvui import GameManager

        class BanjoTooieManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Banjo-Tooie Client "+ version + " for AP"

        self.ui = BanjoTooieManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        asyncio.create_task(apply_patch())

    def on_package(self, cmd, args):
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)
            if version != self.slot_data["version"]:
                logger.error("Your Banjo-Tooie AP does not match with the generated world.")
                logger.error("Your version: "+version+" | Generated version: "+self.slot_data["version"])
                # self.event_invalid_game()
                raise Exception("Your Banjo-Tooie AP does not match with the generated world.\n" +
                                "Your version: "+version+" | Generated version: "+self.slot_data["version"])
            self.deathlink_enabled = bool(self.slot_data["death_link"])
            fpath = pathlib.Path(__file__)
            archipelago_root = None
            for i in range(0, 5,+1) :
                if fpath.parents[i].stem == "Archipelago":
                    archipelago_root = pathlib.Path(__file__).parents[i]
                    break
            async_start(run_game(os.path.join(archipelago_root, "Banjo-Tooie-AP"+game_append_version+".z64")))
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
        elif cmd == "ReceivedItems":
            if self.startup == False:
                for item in args["items"]:
                    player = ""
                    item_name = ""
                    for (i, name) in self.player_names.items():
                        if i == item.player:
                            player = name
                            break
                    for (name, i) in bt_itm_name_to_id.items():
                        if item.item == i:
                            item_name = name
                            break
                    logger.info(player + " sent " + item_name)
                logger.info("The above items will be sent when Banjo-Tooie is loaded.")
                self.startup = True

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
            relevant = args.get("type", None) in {"ItemSend"}
            if relevant:
                relevant = False
                item = args["item"]
                if self.slot_concerns_self(args["receiving"]):
                    relevant = True
                elif self.slot_concerns_self(item.player):
                    relevant = True

                if relevant == True:
                    msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                    player = self.player_names[int(args["data"][0]["text"])]
                    to_player = self.player_names[int(args["data"][0]["text"])]
                    for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data["type"] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                    item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                    # self._set_message(msg, None)
                    self._set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player }, None)
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
            relevant = args.get("type", None) in {"ItemSend"}
            if relevant:
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                player = self.player_names[int(args["data"][0]["text"])]
                to_player = self.player_names[int(args["data"][0]["text"])]
                for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data["type"] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                # self._set_message(msg, None)
                self._set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player}, None)

def get_payload(ctx: BanjoTooieContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
        ctx.deathlink_pending = False
    else:
        trigger_death = False

    # if(len(ctx.items_received) > 0) and ctx.sync_ready == True:
    #   print("Receiving Item")

    if ctx.sync_ready == True:
        ctx.startup = True
        payload = json.dumps({
                "items": [get_item_value(item.item) for item in ctx.items_received],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    else:
        payload = json.dumps({
                "items": [],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    if len(ctx.messages) > 0:
        ctx.messages = {}

    # if len(ctx.items_received) > 0 and ctx.sync_ready == True:
    #     ctx.items_received = []

    return payload

def get_slot_payload(ctx: BanjoTooieContext):
    payload = json.dumps({
            "slot_player": ctx.slot_data["player_name"],
            "slot_seed": ctx.slot_data["seed"],
            "slot_deathlink": ctx.deathlink_enabled,
            "slot_tower_of_tragedy": ctx.slot_data["tower_of_tragedy"],
            "slot_randomize_bk_moves": ctx.slot_data["randomize_bk_moves"],
            "slot_speed_up_minigames": ctx.slot_data["speed_up_minigames"],
            "slot_skip_puzzles": ctx.slot_data["skip_puzzles"],
            "slot_backdoors": ctx.slot_data["backdoors"],
            "slot_open_hag1": ctx.slot_data["open_hag1"],
            "slot_randomize_chuffy": ctx.slot_data["randomize_chuffy"],
            "slot_worlds": ctx.slot_data["worlds"],
            "slot_world_order": ctx.slot_data["world_order"],
            "slot_keys": ctx.slot_data["world_keys"],
            "slot_skip_klungo": ctx.slot_data["skip_klungo"],
            "slot_victory_condition": ctx.slot_data["victory_condition"],
            "slot_minigame_hunt_length": ctx.slot_data["minigame_hunt_length"],
            "slot_boss_hunt_length": ctx.slot_data["boss_hunt_length"],
            "slot_jinjo_family_rescue_length": ctx.slot_data["jinjo_family_rescue_length"],
            "slot_token_hunt_length": ctx.slot_data["token_hunt_length"],
            "slot_version": version,
            "slot_silo_costs": ctx.slot_data["jamjars_silo_costs"],
            "slot_preopened_silo": ctx.slot_data["preopened_silos"],
            "slot_randomize_warp_pads": ctx.slot_data["randomize_warp_pads"],
            "slot_randomize_silos": ctx.slot_data["randomize_silos"],
            "slot_zones": ctx.slot_data["loading_zones"],
            "slot_dialog_character": ctx.slot_data["dialog_character"],
            "slot_nestsanity": ctx.slot_data["nestsanity"],
            "slot_hints": ctx.slot_data["hints"],
            "slot_hints_activated": ctx.slot_data["signpost_hints"],
            "slot_extra_cheats": ctx.slot_data["extra_cheats"],
            "slot_easy_canary": ctx.slot_data["easy_canary"],
            "slot_randomize_signposts": ctx.slot_data["randomize_signposts"]
        })
    ctx.sendSlot = False
    return payload


async def parse_payload(payload: dict, ctx: BanjoTooieContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload["playerName"] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.finished_game = False
        ctx.location_table = {}
        ctx.chuffy_table = {}
        ctx.movelist_table = {}
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.auth = payload["playerName"]
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload["deathlinkActive"] and ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Locations handling
    demo = payload["DEMO"]
    chuffy = payload["chuffy"]
    treblelist = payload["treble"]
    stationlist = payload["stations"]
    mystery = payload["mystery"]
    roystenlist = payload["roysten"]
    jinjofamlist = payload["jinjofam"]
    jinjolist = payload["jinjos"]
    pageslist = payload["pages"]
    honeycomblist = payload["honeycomb"]
    glowbolist = payload["glowbo"]
    doubloonlist = payload["doubloon"]
    noteslist = payload["notes"]
    movelist = payload["unlocked_moves"]
    hag = payload["hag"]
    cheatorewardslist = payload["cheato_rewards"]
    honeybrewardslist = payload["honeyb_rewards"]
    jiggychunklist = payload["jiggy_chunks"]
    goggles = payload["goggles"]
    jiggylist = payload["jiggies"]
    dino_kids = payload["dino_kids"]
    nests = payload["nests"]
    roar_obtain = payload["roar"]
    signposts = payload["signposts"]
    warp_pads = payload["warppads"]
    silos = payload["silos"]
    worldslist = payload["worlds"]
    banjo_map = payload["banjo_map"]

    # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
    # if isinstance(locations, list):
    #     locations = {}
    if isinstance(chuffy, list):
        chuffy = {}
    if isinstance(treblelist, list):
        treblelist = {}
    if isinstance(stationlist, list):
        stationlist = {}
    if isinstance(mystery, list):
        mystery = {}
    if isinstance(roystenlist, list):
        roystenlist = {}
    if isinstance(jinjofamlist, list):
        jinjofamlist = {}
    if isinstance(cheatorewardslist, list):
        cheatorewardslist = {}
    if isinstance(honeybrewardslist, list):
        honeybrewardslist = {}
    if isinstance(jiggychunklist, list):
        jiggychunklist = {}
    if isinstance(worldslist, list):
        worldslist = {}
    if isinstance(dino_kids, list):
        dino_kids = {}
    if isinstance(nests, list):
        nests = {}
    if isinstance(signposts, list):
        signposts = {}
    if isinstance(goggles, bool) == False:
        goggles = False
    if isinstance(demo, bool) == False:
        demo = True
    if isinstance(banjo_map, int) == False:
        banjo_map = 0
    if isinstance(jiggylist, list):
        jiggylist = {}
    if isinstance(jinjolist, list):
        jinjolist = {}
    if isinstance(movelist, list):
        movelist = {}
    if isinstance(pageslist, list):
        pageslist = {}
    if isinstance(honeycomblist, list):
        honeycomblist = {}
    if isinstance(glowbolist, list):
        glowbolist = {}
    if isinstance(doubloonlist, list):
        doubloonlist = {}
    if isinstance(noteslist, list):
        noteslist = {}
    if isinstance(warp_pads, list):
        warp_pads = {}
    if isinstance(silos, list):
        silos = {}
    if isinstance(hag, bool) == False:
        hag = False
    if isinstance(roar_obtain, bool) == False:
        roar_obtain = False

    if demo == False and ctx.sync_ready == True:
        locs1 = []
        scouts1 = []
        if ctx.chuffy_table != chuffy:
            ctx.chuffy_table = chuffy
            for locationId, value in chuffy.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.treblelist_table != treblelist:
            ctx.treblelist_table = treblelist
            for locationId, value in treblelist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.stationlist_table != stationlist:
            ctx.stationlist_table = stationlist
            for locationId, value in stationlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.mystery_table != mystery:
            ctx.mystery_table = mystery
            for locationId, value in mystery.items():
                if locationId == "REMOVE": #Don't need to handle this here
                    continue
                if value == True:
                    locs1.append(int(locationId))
        if ctx.roystenlist_table != roystenlist:
            ctx.roystenlist_table = roystenlist
            for locationId, value in roystenlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jiggychunks_table != jiggychunklist:
            ctx.jiggychunks_table = jiggychunklist
            for locationId, value in jiggychunklist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.goggles_table != goggles:
            ctx.goggles_table = goggles
            if goggles == True:
                locs1.append(1231005)
        if ctx.dino_kids_table != dino_kids:
            ctx.dino_kids_table = dino_kids
            for locationId, value in dino_kids.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.nests_table != nests:
            ctx.nests_table = nests
            for locationId, value in nests.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.signpost_table != signposts:
                ctx.signpost_table = signposts
                actual_hints = ctx.slot_data["hints"]
                for locationId, value in signposts.items():
                    if value == True:
                        locs1.append(int(locationId))
                        hint = actual_hints.get(str(locationId), None)

                        if not hint is None and hint.get('should_add_hint')\
                          and not hint.get('location_id') is None\
                          and not hint.get('location_player_id') is None\
                          and ctx.slot_concerns_self(hint['location_player_id']):
                            id = hint['location_id']
                            if not id in ctx.handled_scouts:
                                scouts1.append(id)
        if ctx.warppads_table != warp_pads:
            ctx.warppads_table = warp_pads
            for locationId, value in warp_pads.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.silos_table != silos:
            ctx.silos_table = silos
            for locationId, value in silos.items():
                if value == True:
                    locs1.append(int(locationId))        
        if ctx.roar != roar_obtain:
            ctx.roar = roar_obtain
            if roar_obtain == True:
                locs1.append(1231009)
        if ctx.jiggy_table != jiggylist:
            ctx.jiggy_table = jiggylist
            for locationId, value in jiggylist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jinjolist_table != jinjolist:
            ctx.jinjolist_table = jinjolist
            for locationId, value in jinjolist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.pages_table != pageslist:
            ctx.pages_table = pageslist
            for locationId, value in pageslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.honeycomb_table != honeycomblist:
            ctx.honeycomb_table = honeycomblist
            for locationId, value in honeycomblist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.glowbo_table != glowbolist:
            ctx.glowbo_table = glowbolist
            for locationId, value in glowbolist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.doubloon_table != doubloonlist:
            ctx.doubloon_table = doubloonlist
            for locationId, value in doubloonlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.notes_table != noteslist:
            ctx.notes_table = noteslist
            for locationId, value in noteslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.movelist_table != movelist:
            ctx.movelist_table = movelist
            for locationId, value in movelist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jinjofamlist_table != jinjofamlist:
            ctx.jinjofamlist_table = jinjofamlist
            for locationId, value in jinjofamlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.cheatorewardslist_table != cheatorewardslist:
            ctx.cheatorewardslist_table = cheatorewardslist
            for locationId, value in cheatorewardslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.honeybrewardslist_table != honeybrewardslist:
            ctx.honeybrewardslist_table = honeybrewardslist
            for locationId, value in honeybrewardslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.slot_data["skip_puzzles"] == 1:
            if ctx.worldlist_table != worldslist:
                ctx.worldlist_table = worldslist
                for locationId, value in worldslist.items():
                    if value == True:
                        locs1.append(int(locationId))
        #Mumbo Tokens
        if ctx.slot_data["victory_condition"] == 1 or ctx.slot_data["victory_condition"] == 2 or \
            ctx.slot_data["victory_condition"] == 3 or ctx.slot_data["victory_condition"] == 4 or \
            ctx.slot_data["victory_condition"] == 6:
                locs1 = mumbo_tokens_loc(locs1, ctx.slot_data["victory_condition"])

        if len(locs1) > 0:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": locs1
            }])

            if len(locs1) > 0:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": locs1
                }])

        if len(scouts1) > 0:
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": scouts1,
                "create_as_hint": 2
            }])
            ctx.handled_scouts.extend(scouts1)

        #GAME VICTORY
        #Beat Hag-1
        if hag == True and (ctx.slot_data["victory_condition"] == 0 or ctx.slot_data["victory_condition"] == 4 or\
            ctx.slot_data["victory_condition"] == 6) and not ctx.finished_game:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": 30
            }])
            ctx.finished_game = True
            ctx._set_message("You have completed your goal", None)

        #Mumbo Tokens
        if (ctx.slot_data["victory_condition"] == 1 or ctx.slot_data["victory_condition"] == 2) and not ctx.finished_game:
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if ((ctx.slot_data["victory_condition"] == 1 and mumbo_tokens >= ctx.slot_data["minigame_hunt_length"]) or
                        (ctx.slot_data["victory_condition"] == 2 and mumbo_tokens >= ctx.slot_data["boss_hunt_length"]) or
                        (ctx.slot_data["victory_condition"] == 3 and mumbo_tokens >= ctx.slot_data["jinjo_family_rescue_length"])):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True
                        ctx._set_message("You have completed your goal", None)

        if (ctx.current_map == 401 and ctx.slot_data["victory_condition"] == 5 and not ctx.finished_game):
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if (mumbo_tokens >= ctx.slot_data["token_hunt_length"]):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

        if (ctx.current_map == 401 and ctx.slot_data["victory_condition"] == 3 and not ctx.finished_game):
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if (mumbo_tokens >= ctx.slot_data["jinjo_family_rescue_length"]):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

        # Ozone Banjo-Tooie Tracker
        if ctx.current_map != banjo_map:
            ctx.current_map = banjo_map
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"Banjo_Tooie_{ctx.team}_{ctx.slot}_map",
                "default": hex(0),
                "want_reply": False,
                "operations": [{"operation": "replace",
                    "value": hex(banjo_map)}]
            }])
    #Send Aync Data.
    if "sync_ready" in payload and payload["sync_ready"] == "true" and ctx.sync_ready == False:
        # ctx.items_handling = 0b101
        # await ctx.send_connect()
        ctx.sync_ready = True

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload["isDead"]: #Banjo died
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True

                await ctx.send_death()
        else: # Banjo is somehow still alive
            ctx.deathlink_sent_this_death = False

def mumbo_tokens_loc(locs: list, goaltype: int) -> list:
    for locationId in locs:
        if goaltype == 1 or goaltype == 4:
            if locationId == 1230598: #MT
                locs.append(1230968)
            if locationId == 1230610: #GM
                locs.append(1230969)
            if locationId == 1230616: #WW
                locs.append(1230970)
            if locationId == 1230617: #WW
                locs.append(1230971)
            if locationId == 1230619: #WW
                locs.append(1230972)
            if locationId == 1230620: #WW
                locs.append(1230973)
            if locationId == 1230626: #JRL
                locs.append(1230974)
            if locationId == 1230641: #TDL
                locs.append(1230975)
            if locationId == 1230648: #GI
                locs.append(1230976)
            if locationId == 1230654: #GI
                locs.append(1230977)
            if locationId == 1230663: #HFP
                locs.append(1230978)
            if locationId == 1230668: #CCL
                locs.append(1230979)
            if locationId == 1230670: #CCL
                locs.append(1230980)
            if locationId == 1230673: #CCL
                locs.append(1230981)
            if locationId == 1230749: #CCL
                locs.append(1230982)
        if goaltype == 2 or goaltype == 4 or goaltype == 6:
            if locationId == 1230596: #MT
                locs.append(1230960)
            if locationId == 1230606: #GGM
                locs.append(1230961)
            if locationId == 1230618: #WW
                locs.append(1230962)
            if locationId == 1230632: #JRL
                locs.append(1230963)
            if locationId == 1230639: #TDL
                locs.append(1230964)
            if locationId == 1230745: #GI
                locs.append(1230965)
            if locationId == 1230656: #HFP
                locs.append(1230966)
            if locationId == 1230666: #CC
                locs.append(1230967)
        if goaltype == 3 or goaltype == 4:
            if locationId == 1230676: #JINJOFAM
                locs.append(1230983)
            if locationId == 1230677: #JINJOFAM
                locs.append(1230984)
            if locationId == 1230678: #JINJOFAM
                locs.append(1230985)
            if locationId == 1230679: #JINJOFAM
                locs.append(1230986)
            if locationId == 1230680: #JINJOFAM
                locs.append(1230987)
            if locationId == 1230681: #JINJOFAM
                locs.append(1230988)
            if locationId == 1230682: #JINJOFAM
                locs.append(1230989)
            if locationId == 1230683: #JINJOFAM
                locs.append(1230990)
            if locationId == 1230684: #JINJOFAM
                locs.append(1230991)
    return locs

async def n64_sync_task(ctx: BanjoTooieContext):
    logger.info("Starting n64 connector. Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            if ctx.sendSlot == True:
                msg = get_slot_payload(ctx).encode()
            else:
                msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get("scriptVersion", 0)
                    getSlotData = data_decoded.get("getSlot", 0)
                    if getSlotData == True:
                        ctx.sendSlot = True
                    elif reported_version >= script_version:
                        if ctx.game is not None and "jiggies" in data_decoded:
                            # Not just a keep alive ping, parse
                            async_start(parse_payload(data_decoded, ctx, False))
                        if not ctx.auth:
                            ctx.auth = data_decoded["playerName"]
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                "Your connection to the Archipelago server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.n64_status = error_status
                logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to N64")
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21221), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue
            except OSError:
                logger.debug("Connection Failed, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue
            except Exception as error:
                logger.info("Unknown Error: %r", error)
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                break

def read_file(path):
    with open(path, "rb") as fi:
        data = fi.read()
    return data

def write_file(path, data):
    with open(path, "wb") as fi:
        fi.write(data)

def swap(data):
    swapped_data = bytearray(b'\0'*len(data))
    for i in range(0, len(data), 2):
        swapped_data[i] = data[i+1]
        swapped_data[i+1] = data[i]
    return bytes(swapped_data)

def check_rom(patchedRom):
    if os.path.isfile(patchedRom):
        rom = read_file(patchedRom)
        md5 = hashlib.md5(rom).hexdigest()
        return md5
    else:
        return "00000"

def patch_rom(romPath, dstPath, patchPath):
    rom = read_file(romPath)
    md5 = hashlib.md5(rom).hexdigest()
    if (md5 == "ca0df738ae6a16bfb4b46d3860c159d9"): # byte swapped
        rom = swap(rom)
    elif (md5 != "40e98faa24ac3ebe1d25cb5e5ddf49e4"):
        logger.error("Unknown ROM!")
        return
    patch = openFile(patchPath).read()
    write_file(dstPath, bsdiff4.patch(rom, patch))

def openFile(resource: str, mode: str = "rb", encoding: str = None):
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    game = "banjo_tooie/"
    if apworldExt in filename:
        zip_path = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
        with zipfile.ZipFile(zip_path) as zf:
            zipFilePath = game + resource
            if mode == "rb":
                return zf.open(zipFilePath, "r")
            else:
                return io.TextIOWrapper(zf.open(zipFilePath, "r"), encoding)
    else:
        return open(os.path.join(pathlib.Path(__file__).parent, resource), mode, encoding=encoding)

def main():
    Utils.init_logging("Banjo-Tooie Client")
    parser = get_base_parser()
    args = sys.argv[1:]  # the default for parse_args()
    if "Banjo-Tooie Client" in args:
        args.remove("Banjo-Tooie Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()

        ctx = BanjoTooieContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()
