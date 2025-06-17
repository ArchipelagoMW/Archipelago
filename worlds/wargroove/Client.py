from __future__ import annotations

import atexit
import os
import pkgutil
import sys
import asyncio
import random
import typing
from typing import Tuple, List, Iterable, Dict

from . import WargrooveWorld
from .Items import item_table, faction_table, CommanderData, ItemData

import ModuleUpdate
ModuleUpdate.update()

import Utils
import json
import logging

if __name__ == "__main__":
    Utils.init_logging("WargrooveClient", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

wg_logger = logging.getLogger("WG")


class WargrooveClientCommandProcessor(ClientCommandProcessor):
    def _cmd_sacrifice_summon(self):
        """Toggles sacrifices and summons On/Off"""
        if isinstance(self.ctx, WargrooveContext):
            self.ctx.has_sacrifice_summon = not self.ctx.has_sacrifice_summon
            if self.ctx.has_sacrifice_summon:
                self.output(f"Sacrifices and summons are enabled.")
            else:
                unit_summon_response_file = os.path.join(self.ctx.game_communication_path, "unitSummonResponse")
                if os.path.exists(unit_summon_response_file):
                    os.remove(unit_summon_response_file)
                self.output(f"Sacrifices and summons are disabled.")

    def _cmd_deathlink(self):
        """Toggles deathlink On/Off"""
        if isinstance(self.ctx, WargrooveContext):
            self.ctx.has_death_link = not self.ctx.has_death_link
            Utils.async_start(self.ctx.update_death_link(self.ctx.has_death_link), name="Update Deathlink")
            if self.ctx.has_death_link:
                death_link_send_file = os.path.join(self.ctx.game_communication_path, "deathLinkSend")
                if os.path.exists(death_link_send_file):
                    os.remove(death_link_send_file)
                self.output(f"Deathlink enabled.")
            else:
                death_link_receive_file = os.path.join(self.ctx.game_communication_path, "deathLinkReceive")
                if os.path.exists(death_link_receive_file):
                    os.remove(death_link_receive_file)
                self.output(f"Deathlink disabled.")

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True

    def _cmd_commander(self, *commander_name: Iterable[str]):
        """Set the current commander to the given commander."""
        if commander_name:
            self.ctx.set_commander(' '.join(commander_name))
        else:
            if self.ctx.can_choose_commander:
                commanders = self.ctx.get_commanders()
                wg_logger.info('Unlocked commanders: ' +
                               ', '.join((commander.name for commander, unlocked in commanders if unlocked)))
                wg_logger.info('Locked commanders: ' +
                               ', '.join((commander.name for commander, unlocked in commanders if not unlocked)))
            else:
                wg_logger.error('Cannot set commanders in this game mode.')


class WargrooveContext(CommonContext):
    command_processor: int = WargrooveClientCommandProcessor
    game = "Wargroove"
    items_handling = 0b111  # full remote
    current_commander: CommanderData = faction_table["Starter"][0]
    can_choose_commander: bool = False
    commander_defense_boost_multiplier: int = 0
    income_boost_multiplier: int = 0
    starting_groove_multiplier: float
    has_death_link: bool = False
    has_sacrifice_summon: bool = True
    player_stored_units_key: str = ""
    ai_stored_units_key: str = ""
    max_stored_units: int = 1000
    faction_item_ids = {
        'Starter': 0,
        'Cherrystone': 52025,
        'Felheim': 52026,
        'Floran': 52027,
        'Heavensong': 52028,
        'Requiem': 52029,
        'Outlaw': 52030
    }
    buff_item_ids = {
        'Income Boost': 52023,
        'Commander Defense Boost': 52024,
    }
    unit_classes = {
        "archer",
        "ballista",
        "balloon",
        "dog",
        "dragon",
        "giant",
        "harpoonship",
        "harpy",
        "knight",
        "mage",
        "merman",
        "rifleman",
        "soldier",
        "spearman",
        "thief",
        "thief_with_gold",
        "travelboat",
        "trebuchet",
        "turtle",
        "villager",
        "wagon",
        "warship",
        "witch",
    }

    def __init__(self, server_address, password):
        super(WargrooveContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        game_options = WargrooveWorld.settings

        # Validate the AppData directory with Wargroove save data.
        # By default, Windows sets an environment variable we can leverage.
        # However, other OSes don't usually have this value set, so we need to rely on a settings value instead.
        appdata_wargroove = None
        if "appdata" in os.environ:
            appdata_wargroove = os.environ['appdata']
        else:
            try:
                appdata_wargroove = game_options.save_directory
            except FileNotFoundError:
                print_error_and_close("WargrooveClient couldn't detect a path to the AppData folder.\n"
                                      "Unable to infer required game_communication_path.\n"
                                      "Try setting the \"save_directory\" value in your local options file "
                                      "to the AppData folder containing your Wargroove saves.")
        appdata_wargroove = os.path.expandvars(os.path.join(appdata_wargroove, "Chucklefish", "Wargroove"))
        if not os.path.isdir(appdata_wargroove):
            print_error_and_close(f"WargrooveClient couldn't find Wargroove data in your AppData folder.\n"
                                  f"Looked in \"{appdata_wargroove}\".\n"
                                  f"If you haven't yet booted the game at least once, boot Wargroove "
                                  f"and then close it to attempt to fix this error.\n"
                                  f"If the AppData folder above seems wrong, try setting the "
                                  f"\"save_directory\" value in your local options file "
                                  f"to the AppData folder containing your Wargroove saves.")

        # Check for the Wargroove game executable path.
        # This should always be set regardless of the OS.
        root_directory = game_options["root_directory"]
        if not os.path.isfile(os.path.join(root_directory, "win64_bin", "wargroove64.exe")):
            print_error_and_close(f"WargrooveClient couldn't find wargroove64.exe in "
                                  f"\"{root_directory}/win64_bin/\".\n"
                                  f"Unable to infer required game_communication_path.\n"
                                  f"Please verify the \"root_directory\" value in your local "
                                  f"options file is set correctly.")
        self.game_communication_path = os.path.join(root_directory, "AP")
        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
        self.remove_communication_files()
        atexit.register(self.remove_communication_files)
        if not os.path.isdir(appdata_wargroove):
            print_error_and_close("WargrooveClient couldn't find Wargoove in appdata!"
                                  "Boot Wargroove and then close it to attempt to fix this error")
        mods_directory = os.path.join(appdata_wargroove, "mods", "ArchipelagoMod")
        save_directory = os.path.join(appdata_wargroove, "save")

        # Wargroove doesn't always create the mods directory, so we have to do it
        if not os.path.isdir(mods_directory):
            os.makedirs(mods_directory)
        resources = ["data/mods/ArchipelagoMod/maps.dat",
                     "data/mods/ArchipelagoMod/mod.dat",
                     "data/mods/ArchipelagoMod/modAssets.dat",
                     "data/save/campaign-c40a6e5b0cdf86ddac03b276691c483d.cmp",
                     "data/save/campaign-c40a6e5b0cdf86ddac03b276691c483d.cmp.bak"]
        file_paths = [os.path.join(mods_directory, "maps.dat"),
                      os.path.join(mods_directory, "mod.dat"),
                      os.path.join(mods_directory, "modAssets.dat"),
                      os.path.join(save_directory, "campaign-c40a6e5b0cdf86ddac03b276691c483d.cmp"),
                      os.path.join(save_directory, "campaign-c40a6e5b0cdf86ddac03b276691c483d.cmp.bak")]
        for resource, destination in zip(resources, file_paths):
            file_data = pkgutil.get_data("worlds.wargroove", resource)
            if file_data is None:
                print_error_and_close("WargrooveClient couldn't find Wargoove mod and save files in install!")
            with open(destination, 'wb') as f:
                f.write(file_data)

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        with open(os.path.join(self.game_communication_path, "deathLinkReceive"), 'w+') as f:
            text = data.get("cause", "")
            if text:
                f.write(f"DeathLink: {text}")
            else:
                f.write(f"DeathLink: Received from {data['source']}")
        super(WargrooveContext, self).on_deathlink(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(WargrooveContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(WargrooveContext, self).connection_closed()
        self.remove_communication_files()
        self.checked_locations.clear()
        self.server_locations.clear()
        self.finished_game = False

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(WargrooveContext, self).shutdown()
        self.remove_communication_files()
        self.checked_locations.clear()
        self.server_locations.clear()
        self.finished_game = False

    def remove_communication_files(self):
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                os.remove(root + "/" + file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            slot_data = args["slot_data"]
            self.has_death_link = slot_data.get("death_link", False)
            filename = f"AP_settings.json"
            with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                json.dump(slot_data, f)
                self.can_choose_commander = slot_data["can_choose_commander"]
                print('can choose commander:', self.can_choose_commander)
                self.starting_groove_multiplier = slot_data["starting_groove_multiplier"]
                self.income_boost_multiplier = slot_data["income_boost"]
                self.commander_defense_boost_multiplier = slot_data["commander_defense_boost"]
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    pass

            self.player_stored_units_key = f"wargroove_player_units_{self.team}"
            self.ai_stored_units_key = f"wargroove_ai_units_{self.team}"
            self.set_notify(self.player_stored_units_key, self.ai_stored_units_key)

            self.update_commander_data()
            self.ui.update_tracker()

            random.seed(self.seed_name + str(self.slot))
            # Our indexes start at 1 and we have 24 levels
            for i in range(1, 25):
                filename = f"seed{i}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.write(str(random.randint(0, 4294967295)))

        if cmd in {"RoomInfo"}:
            self.seed_name = args["seed_name"]

        if cmd in {"ReceivedItems"}:
            received_ids = [item.item for item in self.items_received]
            for network_item in self.items_received:
                filename = f"AP_{str(network_item.item)}.item"
                path = os.path.join(self.game_communication_path, filename)

                # Newly-obtained items
                if not os.path.isfile(path):
                    open(path, 'w').close()
                    # Announcing commander unlocks
                    item_name = self.item_names.lookup_in_game(network_item.item)
                    if item_name in faction_table.keys():
                        for commander in faction_table[item_name]:
                            logger.info(f"{commander.name} has been unlocked!")

                with open(path, 'w') as f:
                    item_count = received_ids.count(network_item.item)
                    if self.buff_item_ids["Income Boost"] == network_item.item:
                        f.write(f"{item_count * self.income_boost_multiplier}")
                    elif self.buff_item_ids["Commander Defense Boost"] == network_item.item:
                        f.write(f"{item_count * self.commander_defense_boost_multiplier}")
                    else:
                        f.write(f"{item_count}")

                print_filename = f"AP_{str(network_item.item)}.item.print"
                print_path = os.path.join(self.game_communication_path, print_filename)
                if not os.path.isfile(print_path):
                    open(print_path, 'w').close()
                    with open(print_path, 'w') as f:
                        f.write("Received " +
                                self.item_names.lookup_in_game(network_item.item) +
                                " from " +
                                self.player_names[network_item.player])
            self.update_commander_data()
            self.ui.update_tracker()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        pass

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager, HoverBehavior, ServerToolTip
        from kivymd.uix.tab import MDTabsItem, MDTabsItemText
        from kivy.lang import Builder
        from kivy.uix.togglebutton import ToggleButton
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        import pkgutil

        class TrackerLayout(BoxLayout):
            pass

        class CommanderSelect(BoxLayout):
            pass

        class CommanderButton(ToggleButton):
            pass

        class FactionBox(BoxLayout):
            pass

        class CommanderGroup(BoxLayout):
            pass

        class ItemTracker(BoxLayout):
            pass

        class ItemLabel(Label):
            pass

        class WargrooveManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("WG", "WG Console"),
            ]
            base_title = "Archipelago Wargroove Client"
            ctx: WargrooveContext
            unit_tracker: ItemTracker
            trigger_tracker: BoxLayout
            boost_tracker: BoxLayout
            commander_buttons: Dict[int, List[CommanderButton]]
            tracker_items = {
                "Swordsman": ItemData(None, "Unit", False),
                "Dog": ItemData(None, "Unit", False),
                **item_table
            }

            def build(self):
                container = super().build()
                self.add_client_tab("Wargroove", self.build_tracker())
                return container

            def build_tracker(self) -> TrackerLayout:
                try:
                    tracker = TrackerLayout(orientation="horizontal")
                    commander_select = CommanderSelect(orientation="vertical")
                    self.commander_buttons = {}

                    for faction, commanders in faction_table.items():
                        faction_box = FactionBox(size_hint=(None, None), width=100 * len(commanders), height=70)
                        commander_group = CommanderGroup()
                        commander_buttons = []
                        for commander in commanders:
                            commander_button = CommanderButton(text=commander.name, group="commanders")
                            if faction == "Starter":
                                commander_button.disabled = False
                            commander_button.bind(on_press=lambda instance: self.ctx.set_commander(instance.text))
                            commander_buttons.append(commander_button)
                            commander_group.add_widget(commander_button)
                        self.commander_buttons[faction] = commander_buttons
                        faction_box.add_widget(Label(text=faction, size_hint_x=None, pos_hint={'left': 1}, size_hint_y=None, height=10))
                        faction_box.add_widget(commander_group)
                        commander_select.add_widget(faction_box)
                    item_tracker = ItemTracker(padding=[0,20])
                    self.unit_tracker = BoxLayout(orientation="vertical")
                    other_tracker = BoxLayout(orientation="vertical")
                    self.trigger_tracker = BoxLayout(orientation="vertical")
                    self.boost_tracker = BoxLayout(orientation="vertical")
                    other_tracker.add_widget(self.trigger_tracker)
                    other_tracker.add_widget(self.boost_tracker)
                    item_tracker.add_widget(self.unit_tracker)
                    item_tracker.add_widget(other_tracker)
                    tracker.add_widget(commander_select)
                    tracker.add_widget(item_tracker)
                    self.update_tracker()
                    return tracker
                except Exception as e:
                    print(e)

            def update_tracker(self):
                received_ids = [item.item for item in self.ctx.items_received]
                for faction, item_id in self.ctx.faction_item_ids.items():
                    for commander_button in self.commander_buttons[faction]:
                        commander_button.disabled = not (faction == "Starter" or item_id in received_ids)
                self.unit_tracker.clear_widgets()
                self.trigger_tracker.clear_widgets()
                for name, item in self.tracker_items.items():
                    if item.type in ("Unit", "Trigger"):
                        status_color = (1, 1, 1, 1) if item.code is None or item.code in received_ids else (0.6, 0.2, 0.2, 1)
                        label = ItemLabel(text=name, color=status_color)
                        if item.type == "Unit":
                            self.unit_tracker.add_widget(label)
                        else:
                            self.trigger_tracker.add_widget(label)
                self.boost_tracker.clear_widgets()
                extra_income = received_ids.count(52023) * self.ctx.income_boost_multiplier
                extra_defense = received_ids.count(52024) * self.ctx.commander_defense_boost_multiplier
                income_boost = ItemLabel(text="Extra Income: " + str(extra_income))
                defense_boost = ItemLabel(text="Comm Defense: " + str(100 + extra_defense))
                self.boost_tracker.add_widget(income_boost)
                self.boost_tracker.add_widget(defense_boost)

        self.ui = WargrooveManager(self)
        data = pkgutil.get_data(WargrooveWorld.__module__, "Wargroove.kv").decode()
        Builder.load_string(data)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def update_commander_data(self):
        if self.can_choose_commander:
            faction_items = 0
            faction_item_names = [faction + ' Commanders' for faction in faction_table.keys()]
            for network_item in self.items_received:
                if self.item_names.lookup_in_game(network_item.item) in faction_item_names:
                    faction_items += 1
            starting_groove = (faction_items - 1) * self.starting_groove_multiplier
            # Must be an integer larger than 0
            starting_groove = int(max(starting_groove, 0))
            data = {
                "commander": self.current_commander.internal_name,
                "starting_groove": starting_groove
            }
        else:
            data = {
                "commander": "seed",
                "starting_groove": 0
            }
        filename = 'commander.json'
        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
            json.dump(data, f)
        if self.ui:
            self.ui.update_tracker()

    def set_commander(self, commander_name: str) -> bool:
        """Sets the current commander to the given one, if possible"""
        if not self.can_choose_commander:
            wg_logger.error("Cannot set commanders in this game mode.")
            return
        match_name = commander_name.lower()
        for commander, unlocked in self.get_commanders():
            if commander.name.lower() == match_name or commander.alt_name and commander.alt_name.lower() == match_name:
                if unlocked:
                    self.current_commander = commander
                    self.syncing = True
                    wg_logger.info(f"Commander set to {commander.name}.")
                    self.update_commander_data()
                    return True
                else:
                    wg_logger.error(f"Commander {commander.name} has not been unlocked.")
                    return False
        else:
            wg_logger.error(f"{commander_name} is not a recognized Wargroove commander.")

    def get_commanders(self) -> List[Tuple[CommanderData, bool]]:
        """Gets a list of commanders with their unlocked status"""
        commanders = []
        received_ids = [item.item for item in self.items_received]
        for faction in faction_table.keys():
            unlocked = faction == 'Starter' or self.faction_item_ids[faction] in received_ids
            commanders += [(commander, unlocked) for commander in faction_table[faction]]
        return commanders


async def game_watcher(ctx: WargrooveContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file == "deathLinkSend" and ctx.has_death_link:
                    with open(os.path.join(ctx.game_communication_path, file), 'r') as f:
                        failed_mission = f.read()
                        if ctx.slot is not None:
                            await ctx.send_death(f"{ctx.player_names[ctx.slot]} failed {failed_mission}")
                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    sending = sending+[(int(st))]
                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file.find("victory") > -1:
                    victory = True
                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file == "unitSacrifice" or file == "unitSacrificeAI":
                    if ctx.has_sacrifice_summon:
                        stored_units_key = ctx.player_stored_units_key
                        if file == "unitSacrificeAI":
                            stored_units_key = ctx.ai_stored_units_key
                        with open(os.path.join(ctx.game_communication_path, file), 'r') as f:
                            unit_class = f.read()
                            message = [{"cmd": 'Set', "key": stored_units_key,
                                        "default": [],
                                        "want_reply": True,
                                        "operations": [{"operation": "add", "value": [unit_class[:64]]}]}]
                            await ctx.send_msgs(message)
                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file == "unitSummonRequestAI" or file == "unitSummonRequest":
                    if ctx.has_sacrifice_summon:
                        stored_units_key = ctx.player_stored_units_key
                        if file == "unitSummonRequestAI":
                            stored_units_key = ctx.ai_stored_units_key
                        with open(os.path.join(ctx.game_communication_path, "unitSummonResponse"), 'w') as f:
                            if stored_units_key in ctx.stored_data:
                                stored_units = ctx.stored_data[stored_units_key]
                                if stored_units is None:
                                    stored_units = []
                                wg1_stored_units = [unit for unit in stored_units if unit in ctx.unit_classes]
                                if len(wg1_stored_units) != 0:
                                    summoned_unit = random.choice(wg1_stored_units)
                                    message = [{"cmd": 'Set', "key": stored_units_key,
                                                "default": [],
                                                "want_reply": True,
                                                "operations": [{"operation": "remove", "value": summoned_unit[:64]}]}]
                                    await ctx.send_msgs(message)
                                    f.write(summoned_unit)
                    os.remove(os.path.join(ctx.game_communication_path, file))

        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

def launch(*launch_args: str):
    async def main():
        args = parser.parse_args(launch_args)
        ctx = WargrooveContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="WargrooveProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Wargroove Client, for text interfacing.")

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
