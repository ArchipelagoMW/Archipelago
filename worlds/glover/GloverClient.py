import asyncio
import hashlib
import io
import json
import os
import multiprocessing
import copy
import pathlib
import subprocess
import sys
import time
from typing import Union
import zipfile
import bsdiff4
import atexit


# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
import settings
from Utils import async_start
from worlds import network_data_package

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_glover_bizhawk.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure connector_glover_bizhawk.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_glover_bizhawk.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    taglinkActive: bool,
    isDead: bool,
    isTag: bool,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    checkedLocations: list
    playerNames: list,
    triggerDeath: bool,
    triggerTag: bool,
    messages: string
}

Deathlink logic:
"Dead" is true <-> Glover is at 0 hp.

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

"""

loc_name_to_id = network_data_package["games"]["Glover"]["location_name_to_id"]
itm_name_to_id = network_data_package["games"]["Glover"]["item_name_to_id"]
script_version: int = 1
version: str = "V0.1"
patch_md5: str = "d73618ccb9f39d2e91049f05978e03db"
gvr_options = settings.get_settings().glover_options
program = None

def read_file(path):
  with open(path, "rb") as fi:
    data = fi.read()
  return data

def write_file(path, data):
  with open(path, "wb") as fi:
    fi.write(data)

def open_world_file(resource: str, mode: str = "rb", encoding: str = None):
  filename = sys.modules[__name__].__file__
  apworldExt = ".apworld"
  game = "glover/"
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

def patch_rom(rom_path, dst_path, patch_path):
  rom = read_file(rom_path)
  md5 = hashlib.md5(rom).hexdigest()
  if md5 == "a43f68079c8fff2920137585b39fc73e": # byte swapped
    swapped = bytearray(b'\0'*len(rom))
    for i in range(0, len(rom), 2):
      swapped[i] = rom[i+1]
      swapped[i+1] = rom[i]
    rom = bytes(swapped)
  elif md5 != "87aa5740dff79291ee97832da1f86205":
    logger.error(f"Unknown ROM! Please use /patch or restart the {game_name} Client to try again.")
    return False
  with open_world_file(patch_path) as f:
    patch = f.read()
  write_file(dst_path, bsdiff4.patch(rom, patch))
  return True

async def patch_and_run(show_path):
  global program
  game_name = "Glover"
  patch_path = gvr_options.get("patch_path", "")
  patch_name = f"{game_name} AP {version}.z64"
  if patch_path and os.access(patch_path, os.W_OK):
    patch_path = os.path.join(patch_path, patch_name)
  elif os.access(Utils.user_path(), os.W_OK):
    patch_path = Utils.user_path(patch_name)
  elif os.access(Utils.cache_path(), os.W_OK):
    patch_path = Utils.cache_path(patch_name)
  else:
    patch_path = None
  existing_md5 = None
  if patch_path and os.path.isfile(patch_path):
    rom = read_file(patch_path)
    existing_md5 = hashlib.md5(rom).hexdigest()
  await asyncio.sleep(0.01)
  patch_successful = True
  if not patch_path or existing_md5 != patch_md5:
    rom = gvr_options.get("rom_path", "")
    if not rom or not os.path.isfile(rom):
      rom = Utils.open_filename(f"Open your {game_name} US ROM", (("Rom Files", (".z64", ".n64")), ("All Files", "*"),))
    if not rom:
      logger.error(f"No ROM selected. Please use /patch or restart the {game_name} Client to try again.")
      return
    if not patch_path:
      patch_path = os.path.split(rom)[0]
      if os.access(patch_path, os.W_OK):
        patch_path = os.path.join(patch_path, patch_name)
      else:
        logger.error(f"Unable to find writable path... Please use /patch or restart the {game_name} Client to try again.")
        return
    logger.info("Patching...")
    patch_successful = patch_rom(rom, patch_path, "assets/Glover.patch")
    if patch_successful:
      gvr_options.rom_path = rom
      gvr_options.patch_path = os.path.split(patch_path)[0]
    else:
      gvr_options.rom_path = None
    gvr_options._changed = True
  if patch_successful:
    if show_path:
      logger.info(f"Patched {game_name} is located here: {patch_path}")
    program_path = gvr_options.get("program_path", "")
    if program_path and os.path.isfile(program_path) and (not program or program.poll() != None):
      import shlex, subprocess
      logger.info(f"Automatically starting {program_path}")
      args = [*shlex.split(program_path)]
      program_args = gvr_options.program_args
      if program_args:
        if program_args == "--lua=":
          lua = Utils.local_path("data", "lua", "connector_glover_bizhawk.lua")
          program_args = f'--lua={lua}'
          if os.access(os.path.split(lua)[0], os.W_OK):
            with open(lua, "w") as to:
              with open_world_file("assets/connector_glover_bizhawk.lua") as f:
                to.write(f.read().decode())
        args.append(program_args)
      args.append(patch_path)
      program = subprocess.Popen(
        args,
        cwd=Utils.local_path("."),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
      )

def get_item_value(ap_id):
    return ap_id

def get_location_value(ap_id):
    return ap_id

class GloverItemTracker:

  def __init__(self, ctx):
    self.ctx = ctx
    self.items = {item_name: 0 for item_name in itm_name_to_id}
    self.refresh_items()

  def refresh_items(self):
    for item in self.items:
      self.items[item] = 0
    for item in self.ctx.items_received:
      self.items[self.ctx.item_names.lookup_in_game(item.item)] += 1
    self.ctx.tab_items.content.data = []
    for item_name, amount in sorted(self.items.items()):
      if amount == 0: continue
      if amount > 1: self.ctx.tab_items.content.data.append({"text":f"{item_name}: {amount}"})
      else: self.ctx.tab_items.content.data.append({"text":f"{item_name}"})

class GloverCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_patch(self):
        """Reruns the patcher."""
        asyncio.create_task(patch_and_run(True))
        return True

    def _cmd_autostart(self):
        """Allows configuring a program to automatically start with the client.
            This allows you to, for example, automatically start Bizhawk with the patched ROM and lua.
            If already configured, disables the configuration."""
        program_path = gvr_options.get("program_path", "")
        if program_path == "" or not os.path.isfile(program_path):
            program_path = Utils.open_filename(f"Select your program to automatically start", (("All Files", "*"),))
            if program_path:
                gvr_options.program_path = program_path
                gvr_options._changed = True
                logger.info(f"Autostart configured for: {program_path}")
                if not program or program.poll() != None:
                    asyncio.create_task(patch_and_run(False))
            else:
                logger.error("No file selected...")
                return False
        else:
            gvr_options.program_path = ""
            gvr_options._changed = True
            logger.info("Autostart disabled.")
        return True

    def _cmd_rom_path(self, path=""):
        """Sets (or unsets) the file path of the vanilla ROM used for patching."""
        gvr_options.rom_path = path
        gvr_options._changed = True
        if path:
            logger.info("rom_path set!")
        else:
            logger.info("rom_path unset!")
        return True

    def _cmd_patch_path(self, path=""):
        """Sets (or unsets) the folder path of where to save the patched ROM."""
        gvr_options.patch_path = path
        gvr_options._changed = True
        if path:
            logger.info("patch_path set!")
        else:
            logger.info("patch_path unset!")
        return True

    def _cmd_program_args(self, path=""):
        """Sets (or unsets) the arguments to pass to the automatically run program. Defaults to passing the lua to Bizhawk."""
        gvr_options.program_args = path
        gvr_options._changed = True
        if path:
            logger.info("program_args set!")
        else:
            logger.info("program_args unset!")
        return True

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, GloverContext):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, GloverContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")

    def _cmd_taglink(self):
        """Toggle taglink from client. Overrides default setting."""
        if isinstance(self.ctx, GloverContext):
            self.ctx.taglink_client_override = True
            self.ctx.taglink_enabled = not self.ctx.taglink_enabled
            async_start(self.ctx.update_tag_link(self.ctx.taglink_enabled), name="Update Taglink")

    # def _cmd_tag(self):
    #     """Toggle a tag for Taglink."""
    #     if isinstance(self.ctx, GloverContext):
    #         async_start(self.ctx.send_tag_link(), name="Send Taglink")


class GloverContext(CommonContext):
    command_processor = GloverCommandProcessor
    items_handling = 0b111 #full

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Glover"
        self.n64_streams: (StreamReader, StreamWriter) = None # type: ignore
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}

        self.garib_table = {}
        self.enemy_garib_table = {}
        self.enemy_table = {}
        self.potion_table = {}
        self.garib_group_table = {}
        self.life_table = {}
        self.tip_table = {}
        self.checkpoint_table = {}
        self.switch_table = {}
        self.goal_table = {}

        self.current_world = 0
        self.current_hub = 0
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False

        self.taglink_enabled = False
        self.pending_tag_link = False
        self.taglink_sent_this_tag = False
        self.taglink_client_override = False
        self.version_warning = False
        self.messages = {}
        self.slot_data = {}
        self.sendSlot = False
        self.sync_ready = False
        self.startup = False
        self.handled_scouts = []

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GloverContext, self).server_auth(password_requested)
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
            logger.info(f"(DeathLink: Sending death to your friends...)")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.player_names[self.slot],
                    "cause": death_text
                }
            }])

    async def update_tag_link(self, tag_link: bool):
        """Helper function to set tag Link connection tag on/off and update the connection if already connected."""
        old_tags = self.tags.copy()
        if tag_link:
            self.tags.add("TagLink")
        else:
            self.tags -= {"TagLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    async def send_tag_link(self):
        """Send a tag link message."""
        if "TagLink" not in self.tags or self.slot is None:
            return
        if not hasattr(self, "instance_id"):
            self.instance_id = time.time()
        await self.send_msgs([{"cmd": "Bounce", "tags": ["TagLink"],
             "data": {
                "time": time.time(),
                "source": self.instance_id,
                "tag": True}}])

    def run_gui(self):
        from kvui import GameManager, Window, UILog

        Window.bind(on_request_close=self.on_request_close)
        asyncio.create_task(patch_and_run(True))

        class GloverManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Glover Client "+ version + " for AP"

            def build(self):
                ret = super().build()
                self.ctx.tab_items = self.add_client_tab("Items", UILog())
                return ret

        self.ui = GloverManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_request_close(self, *args):
        title = "Warning: Autostart program still running!"
        message = "Attempting to close this window again will forcibly close it."
        def cleanup(messagebox):
            self._messagebox = None
        if self._messagebox and self._messagebox.title == title:
            return False
        if program and program.poll() == None:
            self.gui_error(title, message)
            self._messagebox.bind(on_dismiss=cleanup)
            return True
        return False

    def on_package(self, cmd, args):
        if cmd == "Connected":
            self.tracker = GloverItemTracker(self)
            self.slot_data = args.get("slot_data", None)
            if version != self.slot_data["version"]:
                logger.error("Your Glover AP does not match with the generated world.")
                logger.error("Your version: "+version+" | Generated version: "+self.slot_data["version"])
                # self.event_invalid_game()
                raise Exception("Your Glover AP does not match with the generated world.\n" +
                                "Your version: "+version+" | Generated version: "+self.slot_data["version"])
            self.deathlink_enabled = bool(self.slot_data["death_link"])
            self.taglink_enabled = bool(self.slot_data["tag_link"])
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
        elif cmd == "ReceivedItems":
            self.tracker.refresh_items()
            if self.startup == False:
                for item in args["items"]:
                    player = ""
                    item_name = ""
                    for (i, name) in self.player_names.items():
                        if i == item.player:
                            player = name
                            break
                    for (name, i) in itm_name_to_id.items():
                        if item.item == i:
                            item_name = name
                            break
                    logger.info(player + " sent " + item_name)
                logger.info("The above items will be sent when Glover is loaded.")
                self.startup = True
        if isinstance(args, dict) and isinstance(args.get("data", {}), dict):
            source_name = args.get("data", {}).get("source", None)
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()
            if "TagLink" in self.tags and source_name != self.instance_id and "TagLink" in args.get("tags", []):
                if not hasattr(self, "pending_tag_link"):
                    self.pending_tag_link = False
                else:
                    self.pending_tag_link = True

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

def get_payload(ctx: GloverContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
        ctx.deathlink_pending = False
    else:
        trigger_death = False

    if ctx.taglink_enabled and ctx.pending_tag_link:
        trigger_tag = True
        ctx.taglink_sent_this_tag = True
        ctx.pending_tag_link = False
    else:
        trigger_tag = False


    # if(len(ctx.items_received) > 0) and ctx.sync_ready == True:
    #   print("Receiving Item")

    if ctx.sync_ready == True:
        ctx.startup = True
        payload = json.dumps({
                "items": [get_item_value(item.item) for item in ctx.items_received],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "triggerTag": trigger_tag,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    else:
        payload = json.dumps({
                "items": [],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "triggerTag": trigger_tag,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    if len(ctx.messages) > 0:
        ctx.messages = {}

    return payload

def get_slot_payload(ctx: GloverContext):
    payload = json.dumps({
            "slot_player": ctx.slot_data["player_name"],
            "slot_seed": ctx.slot_data["seed"],
            "slot_deathlink": ctx.deathlink_enabled,
            "slot_taglink": ctx.taglink_enabled,
            "slot_version": version,
            "slot_garib_logic": ctx.slot_data["garib_logic"],
            #"slot_garib_sorting": ctx.slot_data["garib_sorting"],
            "slot_garib_order": ctx.slot_data["garib_order"],
            "slot_world_lookup": ctx.slot_data["world_lookup"],
            "slot_switches": ctx.slot_data["switches_checks"],
            "slot_checkpoints": ctx.slot_data["checkpoint_checks"],
            "slot_checked_locations": [get_location_value(locations) for locations in ctx.locations_checked],
        })
    ctx.sendSlot = False
    return payload


async def parse_payload(payload: dict, ctx: GloverContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload["playerName"] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.taglink_enabled = False
        ctx.taglink_client_override = False
        ctx.pending_tag_link = False
        ctx.taglink_sent_this_tag = False

        ctx.finished_game = False
        ctx.location_table = {}
        ctx.auth = payload["playerName"]
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload["deathlinkActive"] and ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Turn on taglink if it is on, and if the client hasn't overriden it
    if payload["taglinkActive"] and ctx.taglink_enabled and not ctx.taglink_client_override:
        await ctx.update_tag_link(True)
        ctx.taglink_enabled = True

    # Locations handling
    demo = payload["DEMO"]
    garibslist = payload["garibs"]
    enemygaribslist = payload["enemy_garibs"]
    enemylist = payload["enemy"]
    potionlist = payload["potions"]
    goallist = payload["goal"]
    garibgrouplist = payload["garib_groups"]
    lifeslist = payload["life"]
    tipslist = payload["tip"]
    checkpointslist = payload["checkpoint"]
    switchslist = payload["switch"]

    glover_world = payload["glover_world"]
    glover_hub = payload["glover_hub"]



    # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
    # if isinstance(locations, list):
    #     locations = {}

    if isinstance(demo, bool) == False:
        demo = True
    if isinstance(garibslist, list):
        garibslist = {}
    if isinstance(enemygaribslist, list):
        enemygaribslist = {}
    if isinstance(enemylist, list):
        enemylist = {}
    if isinstance(potionlist, list):
        potionlist = {}
    if isinstance(garibgrouplist, list):
        garibgrouplist = {}
    if isinstance(lifeslist, list):
        lifeslist = {}
    if isinstance(tipslist, list):
        tipslist = {}
    if isinstance(checkpointslist, list):
        checkpointslist = {}
    if isinstance(switchslist, list):
        switchslist = {}
    if isinstance(glover_world, int) == False:
        glover_world = 0
    if isinstance(glover_hub, int) == False:
        glover_hub = 0
    if isinstance(goallist, list):
        goallist = {}
    
    if demo == False and ctx.sync_ready == True:
        locs1 = []
        scouts1 = []
        scoutsVague = []
        if ctx.garib_table != garibslist:
            ctx.garib_table = garibslist
            for locationId, value in garibslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.enemy_garib_table != enemygaribslist:
            ctx.enemy_garib_table = enemygaribslist
            for locationId, value in enemygaribslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.enemy_table != enemylist:
            ctx.enemy_table = enemylist
            for locationId, value in enemylist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.potion_table != potionlist:
            ctx.potion_table = potionlist
            for locationId, value in potionlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.garib_group_table != garibgrouplist:
            ctx.garib_group_table = garibgrouplist
            for locationId, value in garibgrouplist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.life_table != lifeslist:
            ctx.life_table = lifeslist
            for locationId, value in lifeslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.tip_table != tipslist:
            ctx.tip_table = tipslist
            tip_hints = ctx.slot_data["mr_hints_locations"]
            #For when tip hints are off
            if isinstance(tip_hints, list):
                tip_hints = {}
            tip_hints_type = ctx.slot_data["mr_hints"]
            for locationId, value in tipslist.items():
                if value == True:
                    locs1.append(int(locationId))
                    #Mr. Tip Hints
                    hint = tip_hints.get(str(locationId), None)
                    #If the hint should render
                    if not hint == None and tip_hints_type != 0:
                        #And you are aware of the player
                        if ctx.slot_concerns_self(hint["player_id"]):
                            id = hint['location_id']
                            #If the log's not vauge, make it an actual hint
                            if tip_hints_type != 2:
                                if not id in ctx.handled_scouts:
                                    scouts1.append(id)
                            #Log the vauge hint instead
                            else:
                                if not id in ctx.handled_scouts:
                                    scoutsVague.append(id)
                                    logger.info(hint['vague_hint'])
        if ctx.checkpoint_table != checkpointslist:
            ctx.checkpoint_table = checkpointslist
            for locationId, value in checkpointslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.switch_table != switchslist:
            ctx.switch_table = switchslist
            for locationId, value in switchslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.goal_table != goallist:
            ctx.goal_table = goallist
            for locationId, value in goallist.items():
                if value == True:
                    locs1.append(int(locationId))

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

        if len(scoutsVague) > 0:
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": scoutsVague,
                "create_as_hint": 0
            }])
            ctx.handled_scouts.extend(scoutsVague)
        
        #GAME VICTORY
        # if hag == True and (ctx.slot_data["victory_condition"] == 0 or ctx.slot_data["victory_condition"] == 4 or\
        #     ctx.slot_data["victory_condition"] == 6) and not ctx.finished_game:
        #     await ctx.send_msgs([{
        #         "cmd": "StatusUpdate",
        #         "status": 30
        #     }])
        #     ctx.finished_game = True
        #     ctx._set_message("You have completed your goal", None)

        # Tracker
        if ctx.current_world != glover_world:
            ctx.current_world = glover_world
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"Glover_{ctx.team}_{ctx.slot}_world",
                "default": hex(0),
                "want_reply": False,
                "operations": [{"operation": "replace",
                    "value": hex(glover_world)}]
            }])
        if ctx.current_hub != glover_hub:
            ctx.current_hub = glover_hub
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"Glover_{ctx.team}_{ctx.slot}_hub",
                "default": hex(0),
                "want_reply": False,
                "operations": [{"operation": "replace",
                    "value": hex(glover_hub)}]
            }])
    #Send Sync Data.
    if "sync_ready" in payload and payload["sync_ready"] == "true" and ctx.sync_ready == False:
        # ctx.items_handling = 0b101
        # await ctx.send_connect()
        ctx.sync_ready = True

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload["isDead"]: #Glover died
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True

                await ctx.send_death()
        else: # Glover is somehow still alive
            ctx.deathlink_sent_this_death = False

    if ctx.taglink_enabled:
        if payload["isTag"]: #Glover tagged
            ctx.pending_tag_link = False
            if not ctx.taglink_sent_this_tag:
                ctx.taglink_sent_this_tag = True

                await ctx.send_tag_link()
        else:
            ctx.taglink_sent_this_tag = False

async def n64_sync_task(ctx: GloverContext):
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
                        if ctx.game is not None and "DEMO" in data_decoded:
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
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21223), timeout=10)
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

@atexit.register
def close_program():
  global program
  if program and program.poll() == None:
    program.kill()
    program = None

def main():
    Utils.init_logging("Glover Client")
    parser = get_base_parser()
    args = sys.argv[1:]  # the default for parse_args()
    if "Glover Client" in args:
        args.remove("Glover Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()

        ctx = GloverContext(args.connect, args.password)
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
