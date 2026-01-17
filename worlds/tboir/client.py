from __future__ import annotations
import asyncio
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import time
from enum import Enum
import json
import os
from queue import Queue
import traceback
from uuid import uuid4
import colorama

import ModuleUpdate
from NetUtils import ClientStatus, HintStatus, NetworkItem
import settings
from worlds.tboir import TboiSettings
ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("Isaac Client", exception_logger="Client")

from CommonClient import gui_enabled, logger, ClientCommandProcessor, \
    CommonContext, server_loop

class IsaacClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True


class IsaacContext(CommonContext):
    settings: TboiSettings = None

    save_data_path: str = ""
    mod_viable: bool = False
    client_version = Utils.Version(1,0,0)

    class State(Enum):
        DISCONNECTED = 1
        GATHERING_DATA = 2
        CONNECTED = 3

    @dataclass
    class Command:
        type: str
        payload: any

    @dataclass
    class SaveData:
        session_id: str
        timestamp: int
        actor: str
        commands: list[IsaacContext.Command]

    command_processor: int = IsaacClientCommandProcessor
    game = "The Binding of Isaac Repentance"
    items_handling = 0b111  # full remote
    current_state = State.DISCONNECTED
    options = {}
    scouted_locations = {}
    hintable_locations = {}
    save_corruption_timer = 0

    def __init__(self, server_address: str | None, password: str | None):
        super(IsaacContext, self).__init__(server_address, password)
        s = settings.get_settings()
        self.settings = s.tboir_options

    def resolve_paths(self):
        try:
            if not self.settings.game_folder or not self.settings.game_folder.endswith("The Binding of Isaac Rebirth"):
                self.settings = TboiSettings()
                self.gui_error("Invalid game directory", "Please select the directory which contains your Binding of Isaac executable.\nUsually located in 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\' called 'The Binding of Isaac Rebirth'.")
                return

            settings.get_settings()["tboir_options"] = self.settings
        except:
            self.settings = TboiSettings()
            self.gui_error("Invalid game directory", "Please select the directory which contains your Binding of Isaac executable.\nUsually located in 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\' called 'The Binding of Isaac Rebirth'.")
            return

        potential_mod_dirs = []
        if os.path.isdir(os.path.join(self.settings.game_folder, "mods")):
            potential_mod_dirs = [
                name for name in os.listdir(os.path.join(self.settings.game_folder, "mods"))
                if (name.startswith('the archipelago of isaac') or name.startswith('ap_mod')) and os.path.isdir(os.path.join(os.path.join(self.settings.game_folder, "mods"), name))
                ]
        
        if len(potential_mod_dirs) == 0:
            self.gui_error("Mod not found", "The Archipelago of Isaac mod does not seem to be installed. Please subscribe to the mod on the steam workshop.")
            return
        if len(potential_mod_dirs) > 1:
            self.gui_error("Multiple Archipelago mods", "There seem to be multiple Archipelago mods installed.")
            return

        supported_client_file = os.path.join(self.settings.game_folder, "mods", potential_mod_dirs[0], "supported_client")
        if os.path.isfile(supported_client_file):
            with open(supported_client_file, "r", encoding="utf-8") as f:
                v_nums = f.read().split('.')
                v = Utils.Version(int(v_nums[0]),int(v_nums[1]),int(v_nums[2]))
                if v < self.client_version:
                    self.gui_error("Mod to old", "Your Archipelago of Isaac mod seems to be outdated. Please updated it to the newest version.")
                    return
                elif v > self.client_version:
                    self.gui_error("Client to old", "Your Isaac client seems to be outdated. Please download the newest .apworld file.")
                    return
        else:
            self.gui_error("Mod to old", "Your Archipelago of Isaac mod seems to be outdated. Please updated it to the newest version.")
            return
        self.mod_viable = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(IsaacContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(IsaacContext, self).connection_closed()
        if self.current_state == self.State.CONNECTED:
            self.current_state = self.State.DISCONNECTED
            self.ui.tabs.children[4].trigger_action()
            self.ui.remove_client_tab(self.ui.tabs.children[0])
            self.ui.tracker_tab = None

    async def shutdown(self):
        await super(IsaacContext, self).shutdown()
    
    def set_data(self, key: str, value: any):
        self.stored_data[key] = value
        Utils.async_start(self.send_msgs([
            {"cmd": "Set", "key": key, "want_reply": False, "operations": [{"operation": "replace", "value": value}]}
            ]))
       

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.current_state = self.State.GATHERING_DATA
            self.options = args['slot_data']['options']
            if "deathlink" in self.options:
                self.options["death_link"] = self.options["deathlink"]
            if self.options["death_link"]:
                Utils.async_start(self.update_death_link(True))
            Utils.async_start(self.send_msgs([
                {"cmd": "Get", "keys": [f"isaac_{self.slot}_saveslot",
                                        f"isaac_{self.slot}_run_info",
                                        f"isaac_{self.slot}_goals",
                                        f"isaac_{self.slot}_session_id"]}]))
            if len(self.locations_scouted) == 0:
                Utils.async_start(self.send_msgs([
                    {"cmd": "LocationScouts", "locations": [code for code in self.server_locations], "create_as_hint": False}]))
        if cmd in {"Retrieved"}:
            if f"isaac_{self.slot}_saveslot" in args["keys"]:
                if self.stored_data[f"isaac_{self.slot}_saveslot"] is None:
                    self.set_data(f"isaac_{self.slot}_saveslot", 0)
            if f"isaac_{self.slot}_run_info" in args["keys"]:
                if self.stored_data[f"isaac_{self.slot}_run_info"] is None:
                    self.set_data(f"isaac_{self.slot}_run_info", {"discarded_items": {}, "to_be_distributed": [], "received_items": {}})
            if f"isaac_{self.slot}_goals" in args["keys"]:
                if self.stored_data[f"isaac_{self.slot}_goals"] is None:
                    self.set_data(f"isaac_{self.slot}_goals", {goal: False for goal in self.options["goals"]})
            if f"isaac_{self.slot}_session_id" in args["keys"]:
                if self.stored_data[f"isaac_{self.slot}_session_id"] is None:
                    self.set_data(f"isaac_{self.slot}_session_id", str(uuid4().int))
            if f"_read_hints_{self.team}_{self.slot}" in args["keys"]:
                self.update_hints()
        if cmd in {"SetReply"}:
            if f"_read_hints_{self.team}_{self.slot}" == args["key"]:
                self.update_hints()
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received) and self.current_state == self.State.CONNECTED:
                items = []
                for item in args['items']:
                    net_item = {"item": item[0], "location": item[1], "player": item[2], "flags": item[3]}
                    items.append(net_item)
                self.commands_to_be_sent.put(IsaacContext.Command(
                    type="ReceiveItems",
                    payload=items
                ))
                self.ui.tracker_tab.on_item_update(args['items'])
        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                self.ui.tracker_tab.on_location_update(self.checked_locations)
                self.update_hints()
        if cmd in {"LocationInfo"}:
            if "locations" in args:
                self.scouted_locations |= { l.location: {"item": l.item, "location": l.location, "player": l.player, "flags": l.flags } for l in args["locations"]}
                self.update_hints()

    def update_hints(self):
        hinted_locations = set([ hint["location"] for hint in self.stored_data[f"_read_hints_{self.team}_{self.slot}"] if hint["finding_player"] == self.slot ]) | self.checked_locations
        self.hintable_locations = set({ k: v for k, v in self.scouted_locations.items() if
                                    k not in hinted_locations and (
                                        ("Progression Items" in self.options["hint_types_from_fortunes"] and v["flags"] & 0b001) or
                                        ("Useful Items" in self.options["hint_types_from_fortunes"] and v["flags"] & 0b010) or
                                        ("Junk Items" in self.options["hint_types_from_fortunes"] and v["flags"] & 0b000) or
                                        ("Traps" in self.options["hint_types_from_fortunes"] and v["flags"] & 0b100)
                                    )})
        if self.current_state == self.State.CONNECTED:
            cmd = IsaacContext.Command(
                type = "HintableLocations",
                payload = list(self.hintable_locations)
            )
            self.commands_to_be_sent.put(cmd)
 
    def on_deathlink(self, data):
        if self.current_state == self.State.CONNECTED:
            if self.options["death_link"]:
                cmd = IsaacContext.Command(
                        type = "Kill",
                        payload = None
                    )
                self.commands_to_be_sent.put(cmd)
        return super().on_deathlink(data)
    
    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class IsaacManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Isaac Client"
            tracker_tab = None

            def build(self):
                container = super().build()
                return container

        self.ui = IsaacManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    commands_to_be_sent = Queue()

    def process_mod_command(self, c: IsaacContext.Command):
        if c.type == "RequestAll":
            resp = IsaacContext.Command(
                type = "AllData",
                payload = {
                    "run_info": self.stored_data[f"isaac_{self.slot}_run_info"],
                    "session_id": self.stored_data[f"isaac_{self.slot}_session_id"],
                    "goals": self.stored_data[f"isaac_{self.slot}_goals"],
                    "checked_locations": [code for code in self.checked_locations],
                    "missing_locations": [code for code in self.missing_locations],
                    "received_items": [{ "flags": item.flags, "item": item.item, "location": item.location, "player": item.player } for item in self.items_received],
                    "item_names": { game: { code: name  for code, name in self.item_names[game].items() if game == self.game or any(scout["item"] == code and self.slot_info[scout["player"]].game == game for scout in self.scouted_locations.values()) } for game in set(slot.game for slot in self.slot_info.values())},
                    "location_names": { code: name for code, name in self.location_names[self.game].items() },
                    "slot_info": {k: {"name": v.name, "game": v.game} for k, v in self.slot_info.items()},
                    "slot": self.slot,
                    "options": self.options,
                    "scouted_locations": self.scouted_locations,
                    "hintable_locations": list(self.hintable_locations)
                }
            )
            self.commands_to_be_sent.put(resp)
        elif c.type == "Set":
            self.set_data(f"isaac_{self.slot}_{c.payload["key"]}", c.payload["data"])
            self.ui.tracker_tab.on_runinfo_update(self.stored_data[f"isaac_{self.slot}_run_info"])
            self.ui.tracker_tab.on_goals_update(self.stored_data[f"isaac_{self.slot}_goals"])
        elif c.type == "SendLocations":
            self.ui.tracker_tab.on_location_update(c.payload)
            Utils.async_start(self.check_locations(c.payload))
        elif c.type == "HintLocations":
            item = self.scouted_locations[c.payload[0]]
            state = HintStatus.HINT_UNSPECIFIED
            if item["player"] == self.slot:
                if item["flags"] & 0b001:
                    state = HintStatus.HINT_PRIORITY
                if item["flags"] & 0b010:
                    state = HintStatus.HINT_NO_PRIORITY
                if item["flags"] & 0b100:
                    state = HintStatus.HINT_AVOID
            Utils.async_start(self.send_msgs([
                    {"cmd": "CreateHints", "player": self.slot, "locations": c.payload, "status": state}]))
        elif c.type == "Died":
            if self.options["death_link"]:
                Utils.async_start(self.send_death("Skill Issue"))
        else:
            pass

    def poll(self):
        if not os.path.isfile(self.save_data_path): return

        try:
            data = json.loads(open(self.save_data_path).read())
            save_data = IsaacContext.SaveData(
                session_id=data["session_id"],
                timestamp=data["timestamp"],
                actor=data["actor"],
                commands=[IsaacContext.Command(type=c["type"], payload=c["payload"]) for c in data["commands"]]
            )

            if save_data.actor != "mod": return

            for c in save_data.commands:
                self.process_mod_command(c)

            new_save_data = IsaacContext.SaveData(
                session_id=self.stored_data[f"isaac_{self.slot}_session_id"],
                timestamp=int(time.monotonic() * 1000),
                actor="client",
                commands=[self.commands_to_be_sent.get() for _ in range(self.commands_to_be_sent.qsize())]
            )
            with open(self.save_data_path, "w") as f:
                dump = json.dumps(asdict(new_save_data))
                f.write(dump)

            if all(self.stored_data[f"isaac_{self.slot}_goals"].values()) and not self.finished_game:
                self.finished_game = True
                Utils.async_start(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
        except:
            if self.save_corruption_timer > 10:
                self.save_corruption_timer = 0

                new_save_data = IsaacContext.SaveData(
                    session_id="",
                    timestamp=int(time.monotonic() * 1000),
                    actor="client",
                    commands=[]
                )
                with open(self.save_data_path, "w") as f:
                    dump = json.dumps(asdict(new_save_data))
                    f.write(dump)
            else:
                self.save_corruption_timer += 1

async def game_watcher(ctx: IsaacContext):
    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.1)
        if ctx._messagebox and ctx._messagebox._is_open: continue
        try:
            if not ctx.mod_viable:
                ctx.resolve_paths()

            if ctx.current_state == ctx.State.GATHERING_DATA \
                    and f"isaac_{ctx.slot}_saveslot" in ctx.stored_data.keys() \
                    and f"isaac_{ctx.slot}_session_id" in ctx.stored_data.keys() \
                    and f"isaac_{ctx.slot}_run_info" in ctx.stored_data.keys() \
                    and f"isaac_{ctx.slot}_goals" in ctx.stored_data.keys() \
                    and len(ctx.scouted_locations) > 0:
                while ctx.stored_data[f"isaac_{ctx.slot}_saveslot"] == 0:
                    logger.info('Enter save slot (1-3):')
                    try:
                        slot = int(await ctx.console_input())
                        if slot >= 1 and slot <= 3:
                            ctx.stored_data[f"isaac_{ctx.slot}_saveslot"] = slot
                            ctx.set_data(f"isaac_{ctx.slot}_saveslot", slot)
                    except:
                        pass
                logger.info(f'Connecting to save slot {ctx.stored_data[f"isaac_{ctx.slot}_saveslot"]}')
                ctx.save_data_path = os.path.join(ctx.settings.game_folder, "data", "the archipelago of isaac", f"save{ctx.stored_data[f"isaac_{ctx.slot}_saveslot"]}.dat")
                ctx.current_state = ctx.State.CONNECTED
                
                from worlds.tboir.tracker import TrackerLayout
                ctx.ui.tracker_tab = TrackerLayout()
                ctx.ui.add_client_tab("Tracker", ctx.ui.tracker_tab)

                ctx.ui.tracker_tab.on_connect(ctx)
                ctx.ui.tracker_tab.on_runinfo_update(ctx.stored_data[f"isaac_{ctx.slot}_run_info"])
                ctx.ui.tracker_tab.on_goals_update(ctx.stored_data[f"isaac_{ctx.slot}_goals"])
                ctx.ui.tracker_tab.on_location_update(ctx.checked_locations)
                ctx.ui.tracker_tab.on_item_update(ctx.items_received)
                ctx.ui.tabs.children[0].trigger_action()
            if ctx.current_state == ctx.State.CONNECTED:
                ctx.poll()
        except Exception as e:
            ctx.gui_error("ERROR", traceback.format_exc())


async def main():
    ctx = IsaacContext(None, None)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    progression_watcher = asyncio.create_task(
        game_watcher(ctx), name="IsaacProgressionWatcher")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await progression_watcher

    await ctx.shutdown()
    
if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()

def launch():
    # use colorama to display colored text highlighting
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
