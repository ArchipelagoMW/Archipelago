from __future__ import annotations

import atexit
import os
import sys
import asyncio
import pkgutil
import random
import typing
import Utils
import json
import logging
import ModuleUpdate
from typing import Tuple, List, Iterable, Dict, Any

from settings import get_settings
from . import Wargroove2World
from .Items import item_table, faction_table, CommanderData, ItemData, item_id_name

from .Levels import LEVEL_COUNT, FINAL_LEVEL_COUNT, region_names, \
    low_victory_checks_levels, high_victory_checks_levels, \
    FINAL_LEVEL_1, FINAL_LEVEL_2, FINAL_LEVEL_3, FINAL_LEVEL_4, final_levels, final_filler_levels
from .Locations import location_table, location_id_name
from .RegionFilter import Wargroove2LogicFilter
from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("Wargroove2Client", exception_logger="Client")

wg2_logger = logging.getLogger("WG2")


class Wargroove2ClientCommandProcessor(ClientCommandProcessor):
    def _cmd_sacrifice_summon(self):
        """Toggles sacrifices and summons On/Off"""
        if isinstance(self.ctx, Wargroove2Context):
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
        if isinstance(self.ctx, Wargroove2Context):
            self.ctx.has_death_link = not self.ctx.has_death_link
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
            self.ctx.set_commander(' '.join(commander_name[0]))
        else:
            if self.ctx.can_choose_commander:
                commanders = self.ctx.get_commanders()
                wg2_logger.info('Unlocked commanders: ' +
                                ', '.join((commander.name for commander, unlocked in commanders if unlocked)))
                wg2_logger.info('Locked commanders: ' +
                                ', '.join((commander.name for commander, unlocked in commanders if not unlocked)))
            else:
                wg2_logger.error('Cannot set commanders in this game mode.')


class Wargroove2Context(CommonContext):
    command_processor = Wargroove2ClientCommandProcessor
    game = "Wargroove 2"
    items_handling = 0b111  # full remote
    current_commander: CommanderData = faction_table["Starter"][0]
    can_choose_commander: bool = False
    commander_defense_boost_multiplier: int = 0
    income_boost_multiplier: int = 0
    starting_groove_multiplier: int = 0
    has_death_link: bool = False
    has_sacrifice_summon: bool = True
    victory_locations: int = 1
    objective_locations: int = 1
    final_levels: int = 1
    level_shuffle_seed: int = 0
    slot_data: dict[str, Any]
    stored_finale_key: str = ""
    player_stored_units_key: str = ""
    ai_stored_units_key: str = ""
    faction_item_ids = {
        'Starter': 0,
        'Cherrystone': 252034,
        'Felheim': 252035,
        'Floran': 252036,
        'Heavensong': 252037,
        'Requiem': 252038,
        'Pirate': 252039,
        'Faahri': 252040
    }
    buff_item_ids = {
        'Income Boost': 252032,
        'Commander Defense Boost': 252033,
        'Groove Boost': 252041,
    }

    def __init__(self, server_address, password):
        super(Wargroove2Context, self).__init__(server_address, password)
        self.send_index = 0
        self.syncing = False
        self.awaiting_bridge = False

        options = get_settings()
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        game_options = options.wargroove2_options

        # Validate the AppData directory with Wargroove save data.
        # By default, Windows sets an environment variable we can leverage.
        # However, other OSes don't usually have this value set, so we need to rely on a settings value instead.
        appdata_wargroove = None
        if "appdata" in os.environ:
            self.level_directory = "levels"
            appdata_wargroove = os.environ['appdata']
        else:
            try:
                appdata_wargroove = game_options.save_directory
            except FileNotFoundError:
                print_error_and_close("Wargroove2Client couldn't detect a path to the AppData folder.\n"
                                      "Unable to infer required game_communication_path.\n"
                                      "Try setting the \"save_directory\" value in your local options file "
                                      "to the AppData folder containing your Wargroove 2 saves.")
        appdata_wargroove = os.path.expandvars(os.path.join(appdata_wargroove, "Chucklefish", "Wargroove2"))
        if not os.path.isdir(appdata_wargroove):
            print_error_and_close(f"Wargroove2Client couldn't find Wargroove 2 data in your AppData folder.\n"
                                  f"Looked in \"{appdata_wargroove}\".\n"
                                  f"If you haven't yet booted the game at least once, boot Wargroove 2 "
                                  f"and then close it to attempt to fix this error.\n"
                                  f"If the AppData folder above seems wrong, try setting the "
                                  f"\"save_directory\" value in your local options file "
                                  f"to the AppData folder containing your Wargroove 2 saves.")

        root_directory = os.path.join(game_options.root_directory)
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

        mods_directory = os.path.join(appdata_wargroove, "mods", "ArchipelagoMod")
        save_directory = os.path.join(appdata_wargroove, "save")

        # Wargroove 2 doesn't always create the mods directory, so we have to do it
        if not os.path.isdir(mods_directory):
            os.makedirs(mods_directory)
        resources = [os.path.join("data", "mods", "ArchipelagoMod", "maps.dat"),
                     os.path.join("data", "mods", "ArchipelagoMod", "mod.dat"),
                     os.path.join("data", "mods", "ArchipelagoMod", "modAssets.dat"),
                     os.path.join("data", "save", "campaign-45747c660b6a2f09601327a18d662a7d.cmp"),
                     os.path.join("data", "save", "campaign-45747c660b6a2f09601327a18d662a7d.cmp.bak")]
        file_paths = [os.path.join(mods_directory, "maps.dat"),
                      os.path.join(mods_directory, "mod.dat"),
                      os.path.join(mods_directory, "modAssets.dat"),
                      os.path.join(save_directory, "campaign-45747c660b6a2f09601327a18d662a7d.cmp"),
                      os.path.join(save_directory, "campaign-45747c660b6a2f09601327a18d662a7d.cmp.bak")]
        for i in range(0, len(resources)):
            file_data = pkgutil.get_data("worlds.wargroove2", resources[i])
            if file_data is None:
                print_error_and_close("Wargroove2Client couldn't find Wargoove 2 mod and save files in install!")
            with open(file_paths[i], 'wb') as f:
                f.write(file_data)

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        with open(os.path.join(self.game_communication_path, "deathLinkReceive"), 'w+') as f:
            text = data.get("cause", "")
            if text:
                f.write(f"DeathLink: {text}")
            else:
                f.write(f"DeathLink: Received from {data['source']}")
        super(Wargroove2Context, self).on_deathlink(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Wargroove2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(Wargroove2Context, self).connection_closed()
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
        await super(Wargroove2Context, self).shutdown()
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
            self.slot_data = args["slot_data"]
            self.victory_locations = self.slot_data.get("victory_locations", 1)
            self.objective_locations = self.slot_data.get("objective_locations", 1)
            self.has_death_link = self.slot_data.get("death_link", False)
            self.final_levels = self.slot_data.get("final_levels", 1)
            self.level_shuffle_seed = self.slot_data.get("level_shuffle_seed", 0)
            filename = f"AP_settings.json"
            with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                json.dump(args["slot_data"], f)
                self.can_choose_commander = self.slot_data["commander_choice"] != 0
                self.starting_groove_multiplier = self.slot_data["groove_boost"]
                self.income_boost_multiplier = self.slot_data["income_boost"]
                self.commander_defense_boost_multiplier = self.slot_data["commander_defense_boost"]
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    pass

            self.stored_finale_key = f"wargroove_2_{self.slot}_{self.team}"
            self.set_notify(self.stored_finale_key)
            self.player_stored_units_key = f"wargroove_player_units_{self.team}"
            self.set_notify(self.player_stored_units_key)
            self.ai_stored_units_key = f"wargroove_ai_units_{self.team}"
            self.set_notify(self.ai_stored_units_key)

            self.update_commander_data()
            self.ui.update_ui()

            random.seed(str(self.seed_name) + str(self.slot))
            # Our indexes start at 0 and we have ?? levels
            for i in range(0, 100):
                filename = f"seed{i}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.write(str(random.randint(0, 4294967295)))
            for i in range(0, LEVEL_COUNT):
                filename = f"AP_{i + 1}.map"
                level_file_name = self.slot_data[f"Level File #{i}"]
                file_data = pkgutil.get_data("worlds.wargroove2", os.path.join(self.level_directory, level_file_name))
                if file_data is None:
                    print_error_and_close("Wargroove2Client couldn't find Wargoove 2 level files in install!")
                else:
                    with open(os.path.join(self.game_communication_path, filename), 'wb') as f:
                        f.write(file_data)
            for i in range(0, FINAL_LEVEL_COUNT):
                filename = f"AP_{i + LEVEL_COUNT + 1}.map"
                level_file_name = self.slot_data[f"Final Level File #{i}"]
                file_data = pkgutil.get_data("worlds.wargroove2", os.path.join(self.level_directory, level_file_name))
                if file_data is None:
                    print_error_and_close("Wargroove2Client couldn't find Wargoove 2 level files in install!")
                else:
                    with open(os.path.join(self.game_communication_path, filename), 'wb') as f:
                        f.write(file_data)

        if cmd in {"RoomInfo"}:
            self.seed_name = args["seed_name"]

        if cmd in {"ReceivedItems"}:
            received_ids = [item.item for item in self.items_received]
            for network_item in self.items_received:
                filename = f"AP_{str(network_item.item)}.item"
                path = os.path.join(self.game_communication_path, filename)

                # Newly-obtained items
                if not os.path.isfile(path):
                    # Announcing commander unlocks
                    item_name = self.item_names.lookup_in_slot(network_item.item)
                    if item_name in faction_table.keys():
                        for commander in faction_table[item_name]:
                            logger.info(f"{commander.name} has been unlocked!")

                with open(path, 'w') as f:
                    item_count = received_ids.count(network_item.item)
                    if self.buff_item_ids["Income Boost"] == network_item.item:
                        f.write(f"{item_count * self.income_boost_multiplier}")
                    elif self.buff_item_ids["Commander Defense Boost"] == network_item.item:
                        f.write(f"{item_count * self.commander_defense_boost_multiplier}")
                    elif self.buff_item_ids["Groove Boost"] == network_item.item:
                        f.write(f"{item_count * self.starting_groove_multiplier}")
                    else:
                        f.write(f"{item_count}")

                print_filename = f"AP_{network_item.item}.item.print"
                print_path = os.path.join(self.game_communication_path, print_filename)
                if not os.path.isfile(print_path):
                    open(print_path, 'w').close()
                    with open(print_path, 'w') as f:
                        f.write("Received " +
                                self.item_names.lookup_in_slot(network_item.item) +
                                " from " +
                                self.player_names[network_item.player])
            self.update_commander_data()
            self.ui.update_ui()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        pass
            self.ui.update_ui()

        if cmd in {"Retrieved"}:
            self.ui.update_levels()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager
        from kivymd.uix.tab import MDTabsItem, MDTabsItemText
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.lang import Builder
        from kivy.uix.togglebutton import ToggleButton
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        import pkgutil

        class TrackerLayout(BoxLayout):
            pass

        class LevelsLayout(BoxLayout):
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

        class LevelTracker(BoxLayout):
            pass

        class ItemLabel(Label):
            pass

        class Wargroove2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("WG2", "WG2 Console"),
            ]
            base_title = "Archipelago Wargroove 2 Client"
            ctx: Wargroove2Context
            unit_tracker: ItemTracker
            level_tracker: LevelTracker
            level_1_Layout: GridLayout(cols=1)
            level_2_Layout: GridLayout(cols=1)
            level_3_Layout: GridLayout(cols=1)
            level_4_Layout: GridLayout(cols=1)
            trigger_tracker: BoxLayout
            boost_tracker: BoxLayout
            commander_buttons: Dict[str, List[CommanderButton]]
            tracker_items = {
                "Swordsman": ItemData(None, "Unit"),
                "Dog": ItemData(None, "Unit"),
                **item_table
            }

            def build(self):
                container = super().build()
                self.add_client_tab("WG2 Tracker", self.build_tracker())
                self.add_client_tab("WG2 Levels", self.build_levels())
                return container

            def build_levels(self) -> LevelsLayout:
                levels_layout = LevelsLayout(orientation="horizontal")
                try:
                    level_tracker = LevelTracker(padding=[0, 20])
                    self.level_1_Layout = GridLayout(cols=1)
                    self.level_2_Layout = GridLayout(cols=1)
                    self.level_3_Layout = GridLayout(cols=1)
                    self.level_4_Layout = GridLayout(cols=1)
                    level_tracker.add_widget(self.level_1_Layout)
                    level_tracker.add_widget(self.level_2_Layout)
                    level_tracker.add_widget(self.level_3_Layout)
                    level_tracker.add_widget(self.level_4_Layout)
                    levels_layout.add_widget(level_tracker)
                    self.update_levels()
                except Exception as e:
                    print(e)
                return levels_layout

            def update_levels(self):
                received_names = [item_id_name[item.item] for item in self.ctx.items_received]
                levels = low_victory_checks_levels + high_victory_checks_levels
                level_rules = {level.name: level.location_rules for level in levels}
                region_filter = Wargroove2LogicFilter(received_names)
                self.level_1_Layout.clear_widgets()
                self.level_2_Layout.clear_widgets()
                self.level_3_Layout.clear_widgets()
                self.level_4_Layout.clear_widgets()
                level_counter = 1
                unreachable_levels = list(range(5, 28 + 1))
                for region_name in region_names:
                    fully_beaten_text = ""
                    level_name_text = "\n"
                    status_color = (0.6, 0.2, 0.2, 1)
                    is_fully_beaten = True
                    is_victory_reached = False
                    if level_counter <= LEVEL_COUNT and hasattr(self.ctx, 'slot_data'):
                        level_name = self.ctx.slot_data[region_name]
                        level_name_text = f"\n{level_name}"
                        if level_name in level_rules:
                            for location_name in level_rules[level_name].keys():
                                rule_factory = level_rules[level_name][location_name]
                                is_beatable = rule_factory is None or rule_factory(self.ctx.slot)(region_filter)
                                is_fully_beaten = is_fully_beaten and \
                                                  location_table[location_name] in self.ctx.checked_locations
                                if location_name.endswith(": Victory"):
                                    if location_table[location_name] in self.ctx.checked_locations:
                                        is_victory_reached = True
                                        status_color = (1.0, 1.0, 1.0, 1)
                                        if level_counter <= 4:
                                            next_level = (level_counter - 1) * 4 + 6 - level_counter
                                            unreachable_levels.remove(next_level)
                                            unreachable_levels.remove(next_level + 1)
                                            unreachable_levels.remove(next_level + 2)
                                        elif level_counter <= 16:
                                            unreachable_levels.remove(level_counter + 12)
                                    elif level_counter in unreachable_levels:
                                        status_color = (0.35, 0.2, 0.2, 1)
                                        level_name_text = ""
                                        break
                                    elif is_beatable:
                                        status_color = (0.6, 0.6, 0.2, 1)
                                elif is_beatable and location_table[location_name] not in self.ctx.checked_locations:
                                    fully_beaten_text = "*"
                        else:
                            is_victory_reached = True
                            status_color = (1.0, 1.0, 1.0, 1)
                            if level_counter <= 4:
                                next_level = (level_counter - 1) * 4 + 6 - level_counter
                                unreachable_levels.remove(next_level)
                                unreachable_levels.remove(next_level + 1)
                                unreachable_levels.remove(next_level + 2)
                            elif level_counter <= 16:
                                unreachable_levels.remove(level_counter + 12)

                    if is_fully_beaten and is_victory_reached:
                        fully_beaten_text = " (100%)"

                    label = ItemLabel(text=region_name + fully_beaten_text + level_name_text, color=status_color)
                    if level_counter == 1:
                        self.level_1_Layout.add_widget(label)
                    elif level_counter == 2:
                        self.level_2_Layout.add_widget(label)
                    elif level_counter == 3:
                        self.level_3_Layout.add_widget(label)
                    elif level_counter == 4:
                        self.level_4_Layout.add_widget(label)
                    elif level_counter <= 7:
                        self.level_1_Layout.add_widget(label)
                    elif level_counter <= 10:
                        self.level_2_Layout.add_widget(label)
                    elif level_counter <= 13:
                        self.level_3_Layout.add_widget(label)
                    elif level_counter <= 16:
                        self.level_4_Layout.add_widget(label)
                    elif level_counter <= 19:
                        self.level_1_Layout.add_widget(label)
                    elif level_counter <= 22:
                        self.level_2_Layout.add_widget(label)
                    elif level_counter <= 25:
                        self.level_3_Layout.add_widget(label)
                    else:
                        self.level_4_Layout.add_widget(label)
                    level_counter += 1

                final_level_rules = {final_level.name: final_level.location_rules for final_level in final_levels}
                filler_final_level_rules = {final_level.name: final_level.location_rules
                                            for final_level in final_filler_levels}
                final_level_rules = final_level_rules | filler_final_level_rules
                final_level_1_name = None
                final_level_2_name = None
                final_level_3_name = None
                final_level_4_name = None
                level_name_text = "\n"
                if self.ctx.stored_finale_key in self.ctx.stored_data.keys():
                    stored_data = self.ctx.stored_data[self.ctx.stored_finale_key]
                    final_level_1_name = self.ctx.slot_data[FINAL_LEVEL_1]
                    final_level_2_name = self.ctx.slot_data[FINAL_LEVEL_2]
                    final_level_3_name = self.ctx.slot_data[FINAL_LEVEL_3]
                    final_level_4_name = self.ctx.slot_data[FINAL_LEVEL_4]
                else:
                    stored_data = None
                if stored_data is not None and final_level_1_name in stored_data:
                    level_name_text = f"\n{final_level_1_name}"
                    status_color = (1.0, 1.0, 1.0, 1)
                elif final_level_1_name is not None and region_filter.has_all(["Final North", "Final Center"],
                                                                              self.ctx.slot):
                    level_name_text = f"\n{final_level_1_name}"
                    final_level_rule = final_level_rules[final_level_1_name][f"{final_level_1_name}: Victory"]
                    if final_level_rule is None:
                        status_color = (0.6, 0.6, 0.2, 1)
                    else:
                        is_beatable = final_level_rule(self.ctx.slot)(region_filter)
                        if is_beatable:
                            status_color = (0.6, 0.6, 0.2, 1)
                        else:
                            status_color = (0.6, 0.2, 0.2, 1)
                else:
                    status_color = (0.35, 0.2, 0.2, 1)
                label = ItemLabel(text=FINAL_LEVEL_1 + level_name_text, color=status_color)
                self.level_1_Layout.add_widget(label)
                level_name_text = "\n"
                if stored_data is not None and final_level_2_name in stored_data:
                    level_name_text = f"\n{final_level_2_name}"
                    status_color = (1.0, 1.0, 1.0, 1)
                elif final_level_2_name is not None and region_filter.has_all(["Final East", "Final Center"],
                                                                              self.ctx.slot):
                    level_name_text = f"\n{final_level_2_name}"
                    final_level_rule = final_level_rules[final_level_2_name][f"{final_level_2_name}: Victory"]
                    if final_level_rule is None:
                        status_color = (0.6, 0.6, 0.2, 1)
                    else:
                        is_beatable = final_level_rule(self.ctx.slot)(region_filter)
                        if is_beatable:
                            status_color = (0.6, 0.6, 0.2, 1)
                        else:
                            status_color = (0.6, 0.2, 0.2, 1)
                else:
                    status_color = (0.35, 0.2, 0.2, 1)
                label = ItemLabel(text=FINAL_LEVEL_2 + level_name_text, color=status_color)
                self.level_2_Layout.add_widget(label)
                level_name_text = "\n"
                if stored_data is not None and final_level_3_name in stored_data:
                    level_name_text = f"\n{final_level_3_name}"
                    status_color = (1.0, 1.0, 1.0, 1)
                elif final_level_3_name is not None and region_filter.has_all(["Final South", "Final Center"],
                                                                              self.ctx.slot):
                    level_name_text = f"\n{final_level_3_name}"
                    final_level_rule = final_level_rules[final_level_3_name][f"{final_level_3_name}: Victory"]
                    if final_level_rule is None:
                        status_color = (0.6, 0.6, 0.2, 1)
                    else:
                        is_beatable = final_level_rule(self.ctx.slot)(region_filter)
                        if is_beatable:
                            status_color = (0.6, 0.6, 0.2, 1)
                        else:
                            status_color = (0.6, 0.2, 0.2, 1)
                else:
                    status_color = (0.35, 0.2, 0.2, 1)
                label = ItemLabel(text=FINAL_LEVEL_3 + level_name_text, color=status_color)
                self.level_3_Layout.add_widget(label)
                level_name_text = "\n"
                if stored_data is not None and final_level_4_name in stored_data:
                    level_name_text = f"\n{final_level_4_name}"
                    status_color = (1.0, 1.0, 1.0, 1)
                elif final_level_4_name is not None and region_filter.has_all(["Final West", "Final Center"],
                                                                              self.ctx.slot):
                    level_name_text = f"\n{final_level_4_name}"
                    final_level_rule = final_level_rules[final_level_4_name][f"{final_level_4_name}: Victory"]
                    if final_level_rule is None:
                        status_color = (0.6, 0.6, 0.2, 1)
                    else:
                        is_beatable = final_level_rule(self.ctx.slot)(region_filter)
                        if is_beatable:
                            status_color = (0.6, 0.6, 0.2, 1)
                        else:
                            status_color = (0.6, 0.2, 0.2, 1)
                else:
                    status_color = (0.35, 0.2, 0.2, 1)
                label = ItemLabel(text=FINAL_LEVEL_4 + level_name_text, color=status_color)
                self.level_4_Layout.add_widget(label)

            def build_tracker(self) -> TrackerLayout:
                tracker = TrackerLayout(orientation="horizontal")
                try:
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
                        faction_box.add_widget(
                            Label(text=faction, size_hint_x=None, pos_hint={'left': 1}, size_hint_y=None, height=10))
                        faction_box.add_widget(commander_group)
                        commander_select.add_widget(faction_box)
                    item_tracker = ItemTracker(padding=[0, 20])
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
                return tracker

            def update_tracker(self):
                received_ids = [item.item for item in self.ctx.items_received]
                for faction, item_id in self.ctx.faction_item_ids.items():
                    for commander_button in self.commander_buttons[faction]:
                        commander_button.disabled = not (faction == "Starter" or item_id in received_ids)
                self.unit_tracker.clear_widgets()
                self.trigger_tracker.clear_widgets()
                for name, item in self.tracker_items.items():
                    if item.type in ("Unit", "Trigger"):
                        status_color = (1, 1, 1, 1) if item.code is None or item.code in received_ids else (
                            0.6, 0.2, 0.2, 1)
                        label = ItemLabel(text=name, color=status_color)
                        if item.type == "Unit":
                            self.unit_tracker.add_widget(label)
                        else:
                            self.trigger_tracker.add_widget(label)
                self.boost_tracker.clear_widgets()
                extra_income = received_ids.count(252032) * self.ctx.income_boost_multiplier
                extra_defense = received_ids.count(252033) * self.ctx.commander_defense_boost_multiplier
                extra_groove = received_ids.count(252041) * self.ctx.starting_groove_multiplier
                income_boost = ItemLabel(text="Extra Income: " + str(extra_income))
                defense_boost = ItemLabel(text="Comm Defense: " + str(100 + extra_defense))
                groove_boost = ItemLabel(text="Starting Groove: " + str(extra_groove))
                self.boost_tracker.add_widget(income_boost)
                self.boost_tracker.add_widget(defense_boost)
                self.boost_tracker.add_widget(groove_boost)

            def update_ui(self):
                self.update_tracker()
                self.update_levels()

        self.ui = Wargroove2Manager(self)
        data = pkgutil.get_data(Wargroove2World.__module__, "Wargroove2.kv").decode()
        Builder.load_string(data)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def update_commander_data(self):
        if self.can_choose_commander:
            data = {
                "commander": self.current_commander.internal_name
            }
        else:
            data = {
                "commander": "seed"
            }
        filename = 'commander.json'
        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
            json.dump(data, f)
        if self.ui:
            self.ui.update_ui()

    def set_commander(self, commander_name: str) -> bool:
        """Sets the current commander to the given one, if possible"""
        if not self.can_choose_commander:
            wg2_logger.error("Cannot set commanders in this game mode.")
            return False
        match_name = commander_name.lower()
        for commander, unlocked in self.get_commanders():
            if commander.name.lower() == match_name or commander.alt_name and commander.alt_name.lower() == match_name:
                if unlocked:
                    self.current_commander = commander
                    self.syncing = True
                    wg2_logger.info(f"Commander set to {commander.name}.")
                    self.update_commander_data()
                    return True
                else:
                    wg2_logger.error(f"Commander {commander.name} has not been unlocked.")
                    return False
        else:
            wg2_logger.error(f"{commander_name} is not a recognized Wargroove 2 commander.")
            return False

    def get_commanders(self) -> List[Tuple[CommanderData, bool]]:
        """Gets a list of commanders with their unlocked status"""
        commanders = []
        received_ids = [item.item for item in self.items_received]
        for faction in faction_table.keys():
            unlocked = faction == 'Starter' or self.faction_item_ids[faction] in received_ids
            commanders += [(commander, unlocked) for commander in faction_table[faction]]
        return commanders


async def game_watcher(ctx: Wargroove2Context):
    while not ctx.exit_event.is_set():
        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending: set = set()
        victory = False
        await ctx.update_death_link(ctx.has_death_link)
        for _root, _dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = int(file.split("send", -1)[1])
                    loc_name = location_id_name[st]
                    total_locations = 1
                    if loc_name is not None and loc_name.endswith("Victory"):
                        total_locations = ctx.victory_locations
                    elif loc_name is not None and \
                            st < location_table["Humble Beginnings Rebirth: Talk to Nadia Extra 1"]:  # type: ignore
                        total_locations = ctx.objective_locations
                    for i in range(1, total_locations):
                        sending.add(location_table[loc_name + f" Extra {i}"])
                    sending.add(st)

                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file == "deathLinkSend" and ctx.has_death_link:
                    with open(os.path.join(ctx.game_communication_path, file), 'r') as f:
                        failed_mission = f.read()
                        if ctx.slot is not None:
                            await ctx.send_death(f"{ctx.player_names[ctx.slot]} failed {failed_mission}")
                    os.remove(os.path.join(ctx.game_communication_path, file))
                if file == "victory":
                    with open(os.path.join(ctx.game_communication_path, file), 'r') as f:
                        victory_level = f.read()
                        final_level_list = []
                        if ctx.stored_finale_key in ctx.stored_data.keys():
                            final_level_list = ctx.stored_data[ctx.stored_finale_key]
                            if final_level_list is None:
                                final_level_list = []

                        if victory_level not in final_level_list:
                            final_level_list.append(victory_level)
                            ctx.stored_data[ctx.stored_finale_key] = final_level_list

                        message = [{"cmd": 'Set', "key": ctx.stored_finale_key,
                                    "default": final_level_list,
                                    "want_reply": True,
                                    "operations": [{"operation": "replace", "value": final_level_list}]}]
                        await ctx.send_msgs(message)
                        final_levels_won = len(ctx.stored_data[ctx.stored_finale_key])
                        completed_levels = ", ".join(final_level_list)
                        logger.info(f"({final_levels_won}/{ctx.final_levels}) final levels conquered! Completed: "
                                    f"{completed_levels}")
                        if final_levels_won >= ctx.final_levels:
                            victory = True
                    os.remove(os.path.join(ctx.game_communication_path, file))
                    ctx.ui.update_levels()
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
                if file == "unitSummonRequest" or file == "unitSummonRequestAI":
                    if ctx.has_sacrifice_summon:
                        stored_units_key = ctx.player_stored_units_key
                        if file == "unitSummonRequestAI":
                            stored_units_key = ctx.ai_stored_units_key
                        with open(os.path.join(ctx.game_communication_path, "unitSummonResponse"), 'w') as f:
                            if stored_units_key in ctx.stored_data:
                                stored_units = ctx.stored_data[stored_units_key]
                                if stored_units is not None and len(stored_units) != 0:
                                    summoned_unit = random.choice(stored_units)
                                    message = [{"cmd": 'Set', "key": stored_units_key,
                                                "default": [],
                                                "want_reply": True,
                                                "operations": [{"operation": "remove", "value": summoned_unit[:64]}]}]
                                    await ctx.send_msgs(message)
                                    f.write(summoned_unit)
                    os.remove(os.path.join(ctx.game_communication_path, file))
        ctx.locations_checked = sending
        message = [{"cmd": "LocationChecks", "locations": list(sending)}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)


def launch():
    async def main(args):
        ctx = Wargroove2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="Wargroove2ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Wargroove 2 Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
