import asyncio
import subprocess
import json
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import time
import random
import os
import sys

from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start
from NetUtils import ClientStatus
from settings import get_settings
import dolphin_memory_engine
from .watchdog import events
from .watchdog import observers
from .locations import location_data as locations, caves
from .items import item_data as items
from MultiServer import mark_raw
import platform

class Pikmin2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_force_relink(self):
        """Try to relink to the game if linking fails. Use with caution!"""
        try:
            f = open(os.path.join(self.ctx.src_path, "01-GPVE-Pikmin2_SaveData.gci"), "rb")
            b = f.read()
            ba = bytearray(b)
            offset = 24640
            if (b[offset + 2] == ord("I")): # fake file is here, must read from second file slot instead
                offset = 73792
            # link to game
            logger.info("Linking to Pikmin 2")
            if (ba[offset + 44] == 0xBE and ba[offset + 45] == 0xEF and ba[offset + 46] == 0xCA and ba[offset + 47] == 0xFE):
                self.ctx.recv_addr = (ba[offset + 48] << 24) + (ba[offset + 49] << 16) + (ba[offset + 50] << 8) + (ba[offset + 51])
                logger.info("Found pointer at " + hex(self.ctx.recv_addr))
                # check that pointer has correct value
                result = dolphin_memory_engine.read_bytes(self.ctx.recv_addr, 4)
                if (result == b'\xde\xad\xc0\xde'): # make sure pointer has correct value
                    # add day 1 location check
                    logger.info("Granting Day 1 check")
                    self.ctx.locations_checked.add(1)
                    logger.info("Linking successful.")
                    self.ctx.linked = True
                else:
                    logger.info(f"Linking failed. Pointer value was {result}, which is incorrect. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
            else:
                logger.info("Linking failed. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
        except Exception as e:
            logger.info(str(e))
    
    def _cmd_status(self):
        """Get the current game status."""
        if (self.ctx.win_condition == 0):
            logger.info(f"Goal: Collect Louie")
        elif (self.ctx.win_condition == 1):
            logger.info(f"Goal: Collect {self.ctx.poko_amount} Pokos")
        elif (self.ctx.win_condition == 2):
            logger.info(f"Goal: Collect {self.ctx.treasure_amount} Treasures")
        logger.info(f"Current Pokos (does not include enemy corpses): {calculate_pokos(self.ctx)}")
        logger.info(f"Current Treasure Count (does not include sprays): {calculate_treasures(self.ctx)}")
    
    @mark_raw
    def _cmd_cave(self, cave):
        """Takes a cave as input, and outputs what that cave has been randomized to."""
        caves = ["Emergence Cave", "Subterranean Complex", "Frontier Cavern", "Hole of Beasts", "White Flower Garden", "Bulblax Kingdom", "Snagret Hole", "Citadel of Spiders", "Glutton's Kitchen", "Shower Room", "Submerged Castle", "Cavern of Chaos", "Hole of Heroes", "Dream Den"]
        cave_abbrs = ["EC", "SC", "FC", "HoB", "WFG", "BK", "SH", "CoS", "GK", "SR", "SMGC", "CoC", "HoH", "DD"]
        rando_cave = None
        cave_name = None
        for i in range(0, len(caves)):
            if (cave.lower() == caves[i].lower()):
                abbr = cave_abbrs[i]
                cave_name = caves[i]
                rando_cave = self.ctx.cave_mapping[abbr]
                break
        if rando_cave == None:
            for i in range(0, len(cave_abbrs)):
                if (cave.lower() == cave_abbrs[i].lower()):
                    cave_name = caves[i]
                    rando_cave = self.ctx.cave_mapping[cave_abbrs[i]]
                    break
        if (rando_cave != None):
            rando_cave_name = ""
            for j in range(0, len(cave_abbrs)):
                if (rando_cave == cave_abbrs[j]):
                    rando_cave_name = caves[j]
                    break
            logger.info(f"{cave_name} has been randomized to {rando_cave_name}.")
        else:
            logger.info(f"{cave} is not a valid cave. Valid caves are: {", ".join(caves + cave_abbrs)}")

class Pikmin2Context(CommonContext):
    tags = {"AP"}
    game = "Pikmin 2"
    command_processor = Pikmin2CommandProcessor
    items_handling = 0b111
    connected = False
    linked = False
    collected = []
    recv_addr = None
    recv_item_index = -1
    game_end = False
    victory = False
    dolphin_executable_path = None
    game_path = None
    mapping_path = None
    src_path = None
    seed = None
    win_condition = None
    poko_amount = None
    treasure_amount = None
    slot_number = 0
    deathlink_queue = []
    deathlink_index = 0
    last_deathlink = 0
    send_extinction = False
    send_captain_down = False
    death_link = 0
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.pieces_needed = 0
        self.finished_game = False
        self.game = "Pikmin 2"
        self.slot_number = 0
        self.connected = False
        self.linked = False
        self.collected = []
        self.recv_addr = None
        self.game_end = False
        self.victory = False
        self.seed = None
        self.recv_item_index = -1
        self.win_condition = None
        self.poko_amount = None
        self.treasure_amount = None

    
    def run_gui(self):
        from kvui import GameManager

        class Pikmin2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pikmin 2 Client"

        self.ui = Pikmin2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    
    def on_package(self, cmd, args):
        if (cmd == 'ReceivedItems'): 
            if (self.recv_item_index == -1): # first recv items pkt from server will set our item index
                self.recv_item_index = sync_item_state(self)
    
    def on_deathlink(self, data):
        super().on_deathlink(data)
        if (self.death_link == 1):
            self.deathlink_queue.append(300)
        elif (self.death_link == 2):
            self.deathlink_queue.append(301)
        elif (self.death_link == 3):
            deaths = [300, 301]
            self.deathlink_queue.append(deaths[random.randint(0, 1)])
            
class Handler(events.PatternMatchingEventHandler):
    def __init__(self, ctx):
        # Set the patterns for PatternMatchingEventHandler
        events.PatternMatchingEventHandler.__init__(self, patterns=['*GPVE*.gci'],
                                                             ignore_directories=True, case_sensitive=True)
        self.ctx = ctx

    def on_modified(self, event):
        error = True
        while error:
            error = False
            try:
                print("Attempting file open")
                f = open(os.path.join(self.ctx.src_path, "01-GPVE-Pikmin2_SaveData.gci"), "rb")
                b = f.read()
                f.close()
                ba = bytearray(b)
                offset = 24640
                if (b[offset + 2] == ord("I")): # fake file is here, must read from second file slot instead
                    offset = 73792
                if not self.ctx.linked:
                    # link to game
                    logger.info("Linking to Pikmin 2")
                    if (ba[offset + 44] == 0xBE and ba[offset + 45] == 0xEF and ba[offset + 46] == 0xCA and ba[offset + 47] == 0xFE):
                        self.ctx.recv_addr = (ba[offset + 48] << 24) + (ba[offset + 49] << 16) + (ba[offset + 50] << 8) + (ba[offset + 51])
                        logger.info("Found pointer at " + hex(self.ctx.recv_addr))
                        # check that pointer has correct value
                        result = dolphin_memory_engine.read_bytes(self.ctx.recv_addr, 4)
                        if (result == b'\xde\xad\xc0\xde'): # make sure pointer has correct value
                            # add day 1 location check
                            logger.info("Granting Day 1 check")
                            self.ctx.locations_checked.add(1)
                            logger.info("Linking successful.")
                            self.ctx.linked = True
                        else:
                            logger.info(f"Linking failed. Pointer value was {result}, which is incorrect. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
                    else:
                        logger.info("Linking failed. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
                if (self.ctx.linked):
                    if ((b[offset + 60] & 128) != 0): # leftmost bit is set == logged item, NOT "normal" playtime (I would hope)
                        itemID = (b[offset + 62] << 8) + b[offset + 63]
                        checksum = ((b[offset + 60] - 128) << 8) + b[offset + 61]
                        cave = (b[offset + 52] << 24) + (b[offset + 53] << 16) + (b[offset + 54] << 8) + (b[offset + 55])
                        sublevel = (b[offset + 56] << 24) + (b[offset + 57] << 16) + (b[offset + 58] << 8) + (b[offset + 59])
                        if not cave in caves.keys():
                            cave = 0
                            sublevel = 0
                        if (itemID != checksum or itemID < 0):
                            print("Error (probably not a logged item)")
                            break
                        if (itemID == 89 and self.ctx.win_condition == 0): # louie
                            self.ctx.victory = True
                        # deathlink
                        if (itemID == 300):
                            if (time.time() - self.ctx.last_deathlink > 0.5 and self.ctx.death_link != 0): 
                                logger.info("Pikmin extinction, sending DeathLink packet")
                                self.ctx.send_extinction = True
                                self.ctx.last_deathlink = time.time()
                        elif (itemID == 301):
                            if (time.time() - self.ctx.last_deathlink > 0.5 and self.ctx.death_link != 0): 
                                logger.info("Captains down, sending DeathLink packet")
                                self.ctx.send_captain_down = True
                                self.ctx.last_deathlink = time.time()
                        else: # regular item
                            c = 0
                            s = 0
                            if (cave != 0):
                                c = self.ctx.cave_mapping[caves[cave]]
                                s = self.ctx.sublevel_mapping[c][sublevel - 1] + 1
                            self.ctx.locations_checked.add(read_received_item(itemID, c, s, self.ctx.mapping))

            except Exception as e:
                # logger.info(e)
                error = True

def calculate_pokos(ctx: Pikmin2Context):
    poko_count = 0
    # logger.info(ctx.items_received)
    for nwitem in ctx.items_received:
        itemID = nwitem.item - 1
        # logger.info(itemID)
        if (itemID >= 500):
            itemID -= 292
        if (itemID >= 302):
            itemID -= 96
        if (itemID >= 218):
            itemID -= 30
        poko_count += items[itemID][4]
    return poko_count

def calculate_treasures(ctx: Pikmin2Context):
    t_count = 0
    # logger.info(ctx.items_received)
    for nwitem in ctx.items_received:
        itemID = nwitem.item - 1
        if (itemID != 302 and itemID != 303):
            t_count += 1
    return t_count

def read_received_item(itemID, cave, sublevel, mapping):
    explorerKit = 0
    if (itemID >= 500): # it's an explorer kit treasure
        itemID -= 500
        explorerKit = 1
    elif (itemID < 218 and itemID >= 188): # it's an archipelago treasure
        itemID -= 188
        if (itemID >= 0 and itemID <= 25):
            count = 1
            for location in locations:
                if (location[5] == 0 and location[6] == itemID): # overworld treasure
                    return count
                count += 1
        else:
            count = 1
            for location in locations:
                if (location[0].startswith(cave) and location[5] == sublevel and location[6] == itemID): # cave treasure
                    return count
                count += 1
    for item in items:
        if (item[2] == itemID and item[3] == explorerKit):
            key = [loc for loc, i in mapping.items() if i == item[0]]
            key = key[0]
            count = 1
            for location in locations:
                if (location[0] == key):
                    return count
                count += 1

def write_received_item(recv_addr, id):
    if (recv_addr == None):
        return False
    # print(id, result)
    if (dolphin_memory_engine.read_bytes(recv_addr, 4) != b'\xde\xad\xc0\xde'): # game not ready
        return False
    translated_id = id + (0xDEADC0DE + 1)
    one = (translated_id >> 24) & 0x000000FF
    two = (translated_id >> 16) & 0x000000FF
    three = (translated_id >> 8) & 0x000000FF
    four = translated_id & 0x000000FF
    # print(one, two, three, four)
    # print(bytes([one, two, three, four]))
    dolphin_memory_engine.write_bytes(recv_addr, bytes([one, two, three, four]))
    print("Successfully wrote item " + str(id))
    return True     

def sync_item_state(ctx):
    # Run when the client connects to the server and receives all items. It calculates which items have already been received based on the save file, 
    # which is more accurate than the previous method of storing this information in a file. If the game crashes or is reset, items that weren't saved will now be resent!
    # Note that if duplicate items are sent through cheats, these WILL be lost forever if the game isn't saved due to the way this is calculated. But, that shouldn't
    # be a problem in a normal run.
    error = True
    while error:
        error = False
        try:
            print("Attempting file open")
            f = open(os.path.join(ctx.src_path, "01-GPVE-Pikmin2_SaveData.gci"), "rb")
            b = f.read()
            f.close()
            offset = 24640
            if (b[offset + 2] == ord("I")): # fake file is here, must read from second file slot instead
                offset = 73792
            treasure_offset = 1231
            ek_offset = treasure_offset + (len(items) + 30 - 13 - 3) + 2
            item_counter = 0
            for item_pkt in ctx.items_received:
                item_id = item_pkt.item
                if (item_id == 303 or item_id == 304): # skip filler sprays
                    item_counter += 1
                    continue
                if (item_id > 500): # ek treasure
                    item_id -= 500
                    if (b[offset + ek_offset + item_id - 1] != 0):
                        item_counter += 1
                    else:
                        break
                else:
                    # logger.info(offset + treasure_offset + item_id - 1)
                    if (b[offset + treasure_offset + item_id - 1] != 0):
                        item_counter += 1
                    else:
                        break
            logger.info("Received item count: " + str(item_counter))
            return item_counter
        except FileNotFoundError as e:
            raise Exception("Your Pikmin 2 save file was not found. Double-check the save path you provided to the client, relaunch, and try again. If this is your first time launching Pikmin 2, make sure a save file has been created!")
        except Exception as e:
            logger.info("An unexpected error occurred: " + str(e) + ". Retrying.")
            error = True
    return 0

def mark_treasure_checks(ctx):
    treasures = calculate_treasures(ctx)
    location_ids = []
    for i in range(ctx.treasure_collection_sv, ctx.treasure_collection_ev + 1, ctx.treasure_collection_i):
        if (treasures >= i):
            location_ids.append(201 + i)
    return location_ids

def mark_poko_checks(ctx):
    pokos = calculate_pokos(ctx)
    location_ids = []
    for i in range(1, 11):
        if (pokos >= int((i / 10.0) * ctx.debt)):
            location_ids.append(402 + i)
    return location_ids

async def game_watch(ctx: Pikmin2Context):
    while not ctx.exit_event.is_set():
        if (not ctx.connected):
            ctx.game_path = Path(filedialog.askopenfilename(
                initialdir="/",
                title="Select patched Pikmin 2 ROM",
                filetypes=[("Patched Pikmin 2 ROM", "*.iso")]
            ))
            ctx.mapping_path = Path(filedialog.askopenfilename(
                initialdir="/",
                title="Select Pikmin 2 setup file",
                filetypes=[("APPIK2 file", "*.appik2")]
            ))
            system = platform.system()
            ctx.src_path = get_settings().pikmin2_options.save_folder
            if (system != "Linux"):
                ctx.dolphin_executable_path = get_settings().pikmin2_options.dolphin_path
            f = open(ctx.mapping_path)
            data = json.load(f)
            ctx.seed = data["seed"]
            ctx.mapping = data["items"]
            ctx.win_condition = int(data["win_condition"])
            ctx.poko_amount = int(data["poko_amount"])
            ctx.treasure_amount = int(data["treasure_amount"])
            ctx.slot_number = int(data["slot"])
            ctx.cave_mapping = data["caves"]
            ctx.sublevel_mapping = data["sublevels"]
            ctx.treasure_collection_checks = int(data["treasure_collection_checks"])
            ctx.treasure_collection_sv = int(data["treasure_collection_sv"])
            ctx.treasure_collection_ev = int(data["treasure_collection_ev"])
            ctx.treasure_collection_i = int(data["treasure_collection_i"])
            ctx.poko_collection_checks = int(data["poko_collection_checks"])
            ctx.debt = int(data["debt"])
            ctx.death_link = int(data["death_link"])
            if (ctx.death_link != 0):
                ctx.tags.add("DeathLink")
            f.close()
            if (system == "Linux"):
                process_obj = subprocess.Popen(["dolphin-emu", f"--exec=\"{ctx.game_path}\"", "--batch"]) # TEST THIS PLS
            else:
                process_obj = subprocess.Popen([ctx.dolphin_executable_path, f"--exec={ctx.game_path}", "--batch"])
           
            while not dolphin_memory_engine.is_hooked():
                dolphin_memory_engine.hook()
            print(dolphin_memory_engine.is_hooked())
            event_handler = Handler(ctx)
            observer = observers.Observer()
            observer.schedule(event_handler, path=ctx.src_path, recursive=True)
            observer.start()
            ctx.connected = True
        else:
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                "locations": list(ctx.locations_checked)})
            # print(ctx.locations_checked)
            async_start(ctx.send_msgs(sync_msg))
            # print(ctx.items_received, len(ctx.items_received), ctx.recv_item_index)
            if (ctx.recv_item_index != -1): # set to something real on server connection
                if (ctx.treasure_collection_checks != 0):
                    for id in mark_treasure_checks(ctx):
                        ctx.locations_checked.add(id)
                if (ctx.poko_collection_checks != 0):
                    for id in mark_poko_checks(ctx):
                        ctx.locations_checked.add(id)
                if (len(ctx.items_received) > 0 and ctx.recv_item_index < len(ctx.items_received)):
                    next = ctx.items_received[ctx.recv_item_index]
                    # logger.info(ctx.items_received)
                    # logger.info(ctx.recv_item_index)
                    next_id = next.item
                    if (next.player != ctx.slot_number or next_id == 303 or next_id == 304 or next.location >= 202): # item is being sent from another game and must be processed or item is a spray or item is from a collect treasure/pokos check
                        # print(next_id)
                        # print(ctx.recv_addr)
                        result = write_received_item(ctx.recv_addr, next_id - 1)
                        if result:
                            ctx.recv_item_index += 1
                    else: # item is from the game and can be ignored
                        ctx.recv_item_index += 1

            # handle deathlinks
            if (len(ctx.deathlink_queue) > 0 and ctx.deathlink_index < len(ctx.deathlink_queue)):
                result = write_received_item(ctx.recv_addr, ctx.deathlink_queue[ctx.deathlink_index])
                if result:
                    ctx.deathlink_index += 1
            if (ctx.send_captain_down):
                ctx.send_captain_down = False
                async_start(ctx.send_death("Both of your captains died. Dandori issue."))
            elif (ctx.send_extinction):
                ctx.send_extinction = False
                async_start(ctx.send_death("All of your Pikmin were killed. Dandori issue."))

            if (ctx.win_condition == 1 and calculate_pokos(ctx) >= ctx.poko_amount):
                ctx.victory = True
            if (ctx.win_condition == 2 and len(ctx.items_received) >= ctx.treasure_amount):
                ctx.victory = True
            if (ctx.victory and not ctx.game_end):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.game_end = True
        await asyncio.sleep(0.1)
def main():
    async def _main():
        ctx = Pikmin2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watch(ctx), name="Pikmin2ProgressionWatcher")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    asyncio.run(_main())

def launch():
    parser = get_base_parser(description="Pikmin 2 Client")
    args = parser.parse_args()
    main()