from __future__ import annotations

import asyncio
import copy
import ctypes
import json
import logging
import multiprocessing
import os.path
import re
import sys
import tempfile
import typing
import queue
import zipfile
import io
import random
from pathlib import Path

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from Utils import init_logging, is_windows

if __name__ == "__main__":
    init_logging("SC2Client", exception_logger="Client")

logger = logging.getLogger("Client")
sc2_logger = logging.getLogger("Starcraft2")

import nest_asyncio
from worlds._sc2common import bot
from worlds._sc2common.bot.data import Race
from worlds._sc2common.bot.main import run_game
from worlds._sc2common.bot.player import Bot
from worlds.sc2wol import SC2WoLWorld
from worlds.sc2wol.Items import lookup_id_to_name, get_full_item_list, ItemData, type_flaggroups, upgrade_numbers
from worlds.sc2wol.Locations import SC2WOL_LOC_ID_OFFSET
from worlds.sc2wol.MissionTables import lookup_id_to_mission
from worlds.sc2wol.Regions import MissionInfo

import colorama
from NetUtils import ClientStatus, NetworkItem, RawJSONtoTextParser, JSONtoTextParser, JSONMessagePart
from MultiServer import mark_raw

loop = asyncio.get_event_loop_policy().new_event_loop()
nest_asyncio.apply(loop)
max_bonus: int = 13
victory_modulo: int = 100

# GitHub repo where the Map/mod data is hosted for /download_data command
DATA_REPO_OWNER = "Ziktofel"
DATA_REPO_NAME = "Archipelago-SC2-data"
DATA_API_VERSION = "API2"


# Data version file path.
# This file is used to tell if the downloaded data are outdated
# Associated with /download_data command
def get_metadata_file():
    return os.environ["SC2PATH"] + os.sep + "ArchipelagoSC2Metadata.txt"


class StarcraftClientProcessor(ClientCommandProcessor):
    ctx: SC2Context

    def _cmd_difficulty(self, difficulty: str = "") -> bool:
        """Overrides the current difficulty set for the world.  Takes the argument casual, normal, hard, or brutal"""
        options = difficulty.split()
        num_options = len(options)

        if num_options > 0:
            difficulty_choice = options[0].lower()
            if difficulty_choice == "casual":
                self.ctx.difficulty_override = 0
            elif difficulty_choice == "normal":
                self.ctx.difficulty_override = 1
            elif difficulty_choice == "hard":
                self.ctx.difficulty_override = 2
            elif difficulty_choice == "brutal":
                self.ctx.difficulty_override = 3
            else:
                self.output("Unable to parse difficulty '" + options[0] + "'")
                return False

            self.output("Difficulty set to " + options[0])
            return True

        else:
            if self.ctx.difficulty == -1:
                self.output("Please connect to a seed before checking difficulty.")
            else:
                current_difficulty = self.ctx.difficulty
                if self.ctx.difficulty_override >= 0:
                    current_difficulty = self.ctx.difficulty_override
                self.output("Current difficulty: " + ["Casual", "Normal", "Hard", "Brutal"][current_difficulty])
            self.output("To change the difficulty, add the name of the difficulty after the command.")
            return False


    def _cmd_game_speed(self, game_speed: str = "") -> bool:
        """Overrides the current game speed for the world.
         Takes the arguments default, slower, slow, normal, fast, faster"""
        options = game_speed.split()
        num_options = len(options)

        if num_options > 0:
            speed_choice = options[0].lower()
            if speed_choice == "default":
                self.ctx.game_speed_override = 0
            elif speed_choice == "slower":
                self.ctx.game_speed_override = 1
            elif speed_choice == "slow":
                self.ctx.game_speed_override = 2
            elif speed_choice == "normal":
                self.ctx.game_speed_override = 3
            elif speed_choice == "fast":
                self.ctx.game_speed_override = 4
            elif speed_choice == "faster":
                self.ctx.game_speed_override = 5
            else:
                self.output("Unable to parse game speed '" + options[0] + "'")
                return False

            self.output("Game speed set to " + options[0])
            return True

        else:
            if self.ctx.game_speed == -1:
                self.output("Please connect to a seed before checking game speed.")
            else:
                current_speed = self.ctx.game_speed
                if self.ctx.game_speed_override >= 0:
                    current_speed = self.ctx.game_speed_override
                self.output("Current game speed: "
                            + ["Default", "Slower", "Slow", "Normal", "Fast", "Faster"][current_speed])
            self.output("To change the game speed, add the name of the speed after the command,"
                        " or Default to select based on difficulty.")
            return False

    def _cmd_color(self, color: str = "") -> bool:
        player_colors = [
            "White", "Red", "Blue", "Teal",
            "Purple", "Yellow", "Orange", "Green",
            "LightPink", "Violet", "LightGrey", "DarkGreen",
            "Brown", "LightGreen", "DarkGrey", "Pink",
            "Rainbow", "Random", "Default"
        ]
        match_colors = [player_color.lower() for player_color in player_colors]
        if color:
            if color.lower() not in match_colors:
                self.output(color + " is not a valid color.  Available colors: " + ', '.join(player_colors))
                return False
            if color.lower() == "random":
                color = random.choice(player_colors[:16])
            self.ctx.player_color = match_colors.index(color.lower())
            self.output("Color set to " + player_colors[self.ctx.player_color])
        else:
            self.output("Current player color: " + player_colors[self.ctx.player_color])
            self.output("To change your colors, add the name of the color after the command.")
            self.output("Available colors: " + ', '.join(player_colors))

    def _cmd_disable_mission_check(self) -> bool:
        """Disables the check to see if a mission is available to play.  Meant for co-op runs where one player can play
        the next mission in a chain the other player is doing."""
        self.ctx.missions_unlocked = True
        sc2_logger.info("Mission check has been disabled")
        return True

    def _cmd_play(self, mission_id: str = "") -> bool:
        """Start a Starcraft 2 mission"""

        options = mission_id.split()
        num_options = len(options)

        if num_options > 0:
            mission_number = int(options[0])

            self.ctx.play_mission(mission_number)

        else:
            sc2_logger.info(
                "Mission ID needs to be specified.  Use /unfinished or /available to view ids for available missions.")
            return False

        return True

    def _cmd_available(self) -> bool:
        """Get what missions are currently available to play"""

        request_available_missions(self.ctx)
        return True

    def _cmd_unfinished(self) -> bool:
        """Get what missions are currently available to play and have not had all locations checked"""

        request_unfinished_missions(self.ctx)
        return True

    @mark_raw
    def _cmd_set_path(self, path: str = '') -> bool:
        """Manually set the SC2 install directory (if the automatic detection fails)."""
        if path:
            os.environ["SC2PATH"] = path
            is_mod_installed_correctly()
            return True
        else:
            sc2_logger.warning("When using set_path, you must type the path to your SC2 install directory.")
        return False

    def _cmd_download_data(self) -> bool:
        """Download the most recent release of the necessary files for playing SC2 with
        Archipelago. Will overwrite existing files."""
        if "SC2PATH" not in os.environ:
            check_game_install_path()

        if os.path.exists(get_metadata_file()):
            with open(get_metadata_file(), "r") as f:
                metadata = f.read()
        else:
            metadata = None

        tempzip, metadata = download_latest_release_zip(DATA_REPO_OWNER, DATA_REPO_NAME, DATA_API_VERSION,
                                                       metadata=metadata, force_download=True)

        if tempzip != '':
            try:
                zipfile.ZipFile(tempzip).extractall(path=os.environ["SC2PATH"])
                sc2_logger.info(f"Download complete. Package installed.")
                with open(get_metadata_file(), "w") as f:
                    f.write(metadata)
            finally:
                os.remove(tempzip)
        else:
            sc2_logger.warning("Download aborted/failed. Read the log for more information.")
            return False
        return True


class SC2JSONtoTextParser(JSONtoTextParser):
    def __init__(self, ctx):
        self.handlers = {
            "ItemSend": self._handle_color,
            "ItemCheat": self._handle_color,
            "Hint": self._handle_color,
        }
        super().__init__(ctx)

    def _handle_color(self, node: JSONMessagePart):
        codes = node["color"].split(";")
        buffer = "".join(self.color_code(code) for code in codes if code in self.color_codes)
        return buffer + self._handle_text(node) + '</c>'

    def color_code(self, code: str):
        return '<c val="' + self.color_codes[code] + '">'


class SC2Context(CommonContext):
    command_processor = StarcraftClientProcessor
    game = "Starcraft 2 Wings of Liberty"
    items_handling = 0b111
    difficulty = -1
    game_speed = -1
    all_in_choice = 0
    mission_order = 0
    player_color = 2
    mission_req_table: typing.Dict[str, MissionInfo] = {}
    final_mission: int = 29
    announcements = queue.Queue()
    sc2_run_task: typing.Optional[asyncio.Task] = None
    missions_unlocked: bool = False  # allow launching missions ignoring requirements
    generic_upgrade_missions = 0
    generic_upgrade_research = 0
    generic_upgrade_items = 0
    current_tooltip = None
    last_loc_list = None
    difficulty_override = -1
    game_speed_override = -1
    mission_id_to_location_ids: typing.Dict[int, typing.List[int]] = {}
    last_bot: typing.Optional[ArchipelagoBot] = None

    def __init__(self, *args, **kwargs):
        super(SC2Context, self).__init__(*args, **kwargs)
        self.raw_text_parser = SC2JSONtoTextParser(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SC2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
        if self.ui:
            self.ui.first_check = True

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.difficulty = args["slot_data"]["game_difficulty"]
            if "game_speed" in args["slot_data"]:
                self.game_speed = args["slot_data"]["game_speed"]
            else:
                self.game_speed = 0
            self.all_in_choice = args["slot_data"]["all_in_map"]
            slot_req_table = args["slot_data"]["mission_req"]
            # Maintaining backwards compatibility with older slot data
            self.mission_req_table = {
                mission: MissionInfo(
                    **{field: value for field, value in mission_info.items() if field in MissionInfo._fields}
                )
                for mission, mission_info in slot_req_table.items()
            }
            self.mission_order = args["slot_data"].get("mission_order", 0)
            self.final_mission = args["slot_data"].get("final_mission", 29)
            self.player_color = args["slot_data"].get("player_color", 2)
            self.generic_upgrade_missions = args["slot_data"].get("generic_upgrade_missions", 0)
            self.generic_upgrade_items = args["slot_data"].get("generic_upgrade_items", 0)
            self.generic_upgrade_research = args["slot_data"].get("generic_upgrade_research", 0)

            self.build_location_to_mission_mapping()

            # Looks for the required maps and mods for SC2. Runs check_game_install_path.
            maps_present = is_mod_installed_correctly()
            if os.path.exists(get_metadata_file()):
                with open(get_metadata_file(), "r") as f:
                    current_ver = f.read()
                    sc2_logger.debug(f"Current version: {current_ver}")
                if is_mod_update_available(DATA_REPO_OWNER, DATA_REPO_NAME, DATA_API_VERSION, current_ver):
                    sc2_logger.info("NOTICE: Update for required files found. Run /download_data to install.")
            elif maps_present:
                sc2_logger.warning("NOTICE: Your map files may be outdated (version number not found). "
                                   "Run /download_data to update them.")


    def on_print_json(self, args: dict):
        # goes to this world
        if "receiving" in args and self.slot_concerns_self(args["receiving"]):
            relevant = True
        # found in this world
        elif "item" in args and self.slot_concerns_self(args["item"].player):
            relevant = True
        # not related
        else:
            relevant = False

        if relevant:
            self.announcements.put(self.raw_text_parser(copy.deepcopy(args["data"])))

        super(SC2Context, self).on_print_json(args)

    def run_gui(self):
        from kvui import GameManager, HoverBehavior, ServerToolTip
        from kivy.app import App
        from kivy.clock import Clock
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.gridlayout import GridLayout
        from kivy.lang import Builder
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.floatlayout import FloatLayout
        from kivy.properties import StringProperty

        class HoverableButton(HoverBehavior, Button):
            pass

        class MissionButton(HoverableButton):
            tooltip_text = StringProperty("Test")
            ctx: SC2Context

            def __init__(self, *args, **kwargs):
                super(HoverableButton, self).__init__(*args, **kwargs)
                self.layout = FloatLayout()
                self.popuplabel = ServerToolTip(text=self.text)
                self.layout.add_widget(self.popuplabel)

            def on_enter(self):
                self.popuplabel.text = self.tooltip_text

                if self.ctx.current_tooltip:
                    App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

                if self.tooltip_text == "":
                    self.ctx.current_tooltip = None
                else:
                    App.get_running_app().root.add_widget(self.layout)
                    self.ctx.current_tooltip = self.layout

            def on_leave(self):
                self.ctx.ui.clear_tooltip()

            @property
            def ctx(self) -> CommonContext:
                return App.get_running_app().ctx

        class MissionLayout(GridLayout):
            pass

        class MissionCategory(GridLayout):
            pass

        class SC2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Starcraft2", "Starcraft2"),
            ]
            base_title = "Archipelago Starcraft 2 Client"

            mission_panel = None
            last_checked_locations = {}
            mission_id_to_button = {}
            launching: typing.Union[bool, int] = False  # if int -> mission ID
            refresh_from_launching = True
            first_check = True
            ctx: SC2Context

            def __init__(self, ctx):
                super().__init__(ctx)

            def clear_tooltip(self):
                if self.ctx.current_tooltip:
                    App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

                self.ctx.current_tooltip = None

            def build(self):
                container = super().build()

                panel = TabbedPanelItem(text="Starcraft 2 Launcher")
                self.mission_panel = panel.content = MissionLayout()

                self.tabs.add_widget(panel)

                Clock.schedule_interval(self.build_mission_table, 0.5)

                return container

            def build_mission_table(self, dt):
                if (not self.launching and (not self.last_checked_locations == self.ctx.checked_locations or
                                            not self.refresh_from_launching)) or self.first_check:
                    self.refresh_from_launching = True

                    self.mission_panel.clear_widgets()
                    if self.ctx.mission_req_table:
                        self.last_checked_locations = self.ctx.checked_locations.copy()
                        self.first_check = False

                        self.mission_id_to_button = {}
                        categories = {}
                        available_missions, unfinished_missions = calc_unfinished_missions(self.ctx)

                        # separate missions into categories
                        for mission in self.ctx.mission_req_table:
                            if not self.ctx.mission_req_table[mission].category in categories:
                                categories[self.ctx.mission_req_table[mission].category] = []

                            categories[self.ctx.mission_req_table[mission].category].append(mission)

                        for category in categories:
                            category_panel = MissionCategory()
                            if category.startswith('_'):
                                category_display_name = ''
                            else:
                                category_display_name = category
                            category_panel.add_widget(
                                Label(text=category_display_name, size_hint_y=None, height=50, outline_width=1))

                            for mission in categories[category]:
                                text: str = mission
                                tooltip: str = ""
                                mission_id: int = self.ctx.mission_req_table[mission].id
                                # Map has uncollected locations
                                if mission in unfinished_missions:
                                    text = f"[color=6495ED]{text}[/color]"
                                elif mission in available_missions:
                                    text = f"[color=FFFFFF]{text}[/color]"
                                # Map requirements not met
                                else:
                                    text = f"[color=a9a9a9]{text}[/color]"
                                    tooltip = f"Requires: "
                                    if self.ctx.mission_req_table[mission].required_world:
                                        tooltip += ", ".join(list(self.ctx.mission_req_table)[req_mission - 1] for
                                                             req_mission in
                                                             self.ctx.mission_req_table[mission].required_world)

                                        if self.ctx.mission_req_table[mission].number:
                                            tooltip += " and "
                                    if self.ctx.mission_req_table[mission].number:
                                        tooltip += f"{self.ctx.mission_req_table[mission].number} missions completed"
                                remaining_location_names: typing.List[str] = [
                                    self.ctx.location_names[loc] for loc in self.ctx.locations_for_mission(mission)
                                    if loc in self.ctx.missing_locations]

                                if mission_id == self.ctx.final_mission:
                                    if mission in available_missions:
                                        text = f"[color=FFBC95]{mission}[/color]"
                                    else:
                                        text = f"[color=D0C0BE]{mission}[/color]"
                                    if tooltip:
                                        tooltip += "\n"
                                    tooltip += "Final Mission"

                                if remaining_location_names:
                                    if tooltip:
                                        tooltip += "\n"
                                    tooltip += f"Uncollected locations:\n"
                                    tooltip += "\n".join(remaining_location_names)

                                mission_button = MissionButton(text=text, size_hint_y=None, height=50)
                                mission_button.tooltip_text = tooltip
                                mission_button.bind(on_press=self.mission_callback)
                                self.mission_id_to_button[mission_id] = mission_button
                                category_panel.add_widget(mission_button)

                            category_panel.add_widget(Label(text=""))
                            self.mission_panel.add_widget(category_panel)

                elif self.launching:
                    self.refresh_from_launching = False

                    self.mission_panel.clear_widgets()
                    self.mission_panel.add_widget(Label(text="Launching Mission: " +
                                                             lookup_id_to_mission[self.launching]))
                    if self.ctx.ui:
                        self.ctx.ui.clear_tooltip()

            def mission_callback(self, button):
                if not self.launching:
                    mission_id: int = next(k for k, v in self.mission_id_to_button.items() if v == button)
                    if self.ctx.play_mission(mission_id):
                        self.launching = mission_id
                        Clock.schedule_once(self.finish_launching, 10)

            def finish_launching(self, dt):
                self.launching = False

        self.ui = SC2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        import pkgutil
        data = pkgutil.get_data(SC2WoLWorld.__module__, "Starcraft2.kv").decode()
        Builder.load_string(data)

    async def shutdown(self):
        await super(SC2Context, self).shutdown()
        if self.last_bot:
            self.last_bot.want_close = True
        if self.sc2_run_task:
            self.sc2_run_task.cancel()

    def play_mission(self, mission_id: int) -> bool:
        if self.missions_unlocked or \
                is_mission_available(self, mission_id):
            if self.sc2_run_task:
                if not self.sc2_run_task.done():
                    sc2_logger.warning("Starcraft 2 Client is still running!")
                self.sc2_run_task.cancel()  # doesn't actually close the game, just stops the python task
            if self.slot is None:
                sc2_logger.warning("Launching Mission without Archipelago authentication, "
                                   "checks will not be registered to server.")
            self.sc2_run_task = asyncio.create_task(starcraft_launch(self, mission_id),
                                                    name="Starcraft 2 Launch")
            return True
        else:
            sc2_logger.info(
                f"{lookup_id_to_mission[mission_id]} is not currently unlocked.  "
                f"Use /unfinished or /available to see what is available.")
            return False

    def build_location_to_mission_mapping(self):
        mission_id_to_location_ids: typing.Dict[int, typing.Set[int]] = {
            mission_info.id: set() for mission_info in self.mission_req_table.values()
        }

        for loc in self.server_locations:
            mission_id, objective = divmod(loc - SC2WOL_LOC_ID_OFFSET, victory_modulo)
            mission_id_to_location_ids[mission_id].add(objective)
        self.mission_id_to_location_ids = {mission_id: sorted(objectives) for mission_id, objectives in
                                           mission_id_to_location_ids.items()}

    def locations_for_mission(self, mission: str):
        mission_id: int = self.mission_req_table[mission].id
        objectives = self.mission_id_to_location_ids[self.mission_req_table[mission].id]
        for objective in objectives:
            yield SC2WOL_LOC_ID_OFFSET + mission_id * 100 + objective


async def main():
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    args = parser.parse_args()

    ctx = SC2Context(args.connect, args.password)
    ctx.auth = args.name
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()

    await ctx.shutdown()


maps_table = [
    "ap_liberation_day", "ap_the_outlaws", "ap_zero_hour",
    "ap_evacuation", "ap_outbreak", "ap_safe_haven", "ap_havens_fall",
    "ap_smash_and_grab", "ap_the_dig", "ap_the_moebius_factor", "ap_supernova", "ap_maw_of_the_void",
    "ap_devils_playground", "ap_welcome_to_the_jungle", "ap_breakout", "ap_ghost_of_a_chance",
    "ap_the_great_train_robbery", "ap_cutthroat", "ap_engine_of_destruction", "ap_media_blitz", "ap_piercing_the_shroud",
    "ap_whispers_of_doom", "ap_a_sinister_turn", "ap_echoes_of_the_future", "ap_in_utter_darkness",
    "ap_gates_of_hell", "ap_belly_of_the_beast", "ap_shatter_the_sky", "ap_all_in"
]

wol_default_categories = [
    "Mar Sara", "Mar Sara", "Mar Sara", "Colonist", "Colonist", "Colonist", "Colonist",
    "Artifact", "Artifact", "Artifact", "Artifact", "Artifact", "Covert", "Covert", "Covert", "Covert",
    "Rebellion", "Rebellion", "Rebellion", "Rebellion", "Rebellion", "Prophecy", "Prophecy", "Prophecy", "Prophecy",
    "Char", "Char", "Char", "Char"
]
wol_default_category_names = [
    "Mar Sara", "Colonist", "Artifact", "Covert", "Rebellion", "Prophecy", "Char"
]


def calculate_items(ctx: SC2Context) -> typing.List[int]:
    items = ctx.items_received
    network_item: NetworkItem
    accumulators: typing.List[int] = [0 for _ in type_flaggroups]

    for network_item in items:
        name: str = lookup_id_to_name[network_item.item]
        item_data: ItemData = get_full_item_list()[name]

        # exists exactly once
        if item_data.quantity == 1:
            accumulators[type_flaggroups[item_data.type]] |= 1 << item_data.number

        # exists multiple times
        elif item_data.type == "Upgrade" or item_data.type == "Progressive Upgrade":
            flaggroup = type_flaggroups[item_data.type]

            # Generic upgrades apply only to Weapon / Armor upgrades
            if item_data.type != "Upgrade" or ctx.generic_upgrade_items == 0:
                accumulators[flaggroup] += 1 << item_data.number
            else:
                for bundled_number in upgrade_numbers[item_data.number]:
                    accumulators[flaggroup] += 1 << bundled_number

        # sum
        else:
            accumulators[type_flaggroups[item_data.type]] += item_data.number

    # Upgrades from completed missions
    if ctx.generic_upgrade_missions > 0:
        upgrade_flaggroup = type_flaggroups["Upgrade"]
        num_missions = ctx.generic_upgrade_missions * len(ctx.mission_req_table)
        amounts = [
            num_missions // 100,
            2 * num_missions // 100,
            3 * num_missions // 100
        ]
        upgrade_count = 0
        completed = len([id for id in ctx.mission_id_to_location_ids if SC2WOL_LOC_ID_OFFSET + victory_modulo * id in ctx.checked_locations])
        for amount in amounts:
            if completed >= amount:
                upgrade_count += 1
        # Equivalent to "Progressive Weapon/Armor Upgrade" item
        for bundled_number in upgrade_numbers[5]:
            accumulators[upgrade_flaggroup] += upgrade_count << bundled_number

    return accumulators


def calc_difficulty(difficulty):
    if difficulty == 0:
        return 'C'
    elif difficulty == 1:
        return 'N'
    elif difficulty == 2:
        return 'H'
    elif difficulty == 3:
        return 'B'

    return 'X'


async def starcraft_launch(ctx: SC2Context, mission_id: int):
    sc2_logger.info(f"Launching {lookup_id_to_mission[mission_id]}. If game does not launch check log file for errors.")

    with DllDirectory(None):
        run_game(bot.maps.get(maps_table[mission_id - 1]), [Bot(Race.Terran, ArchipelagoBot(ctx, mission_id),
                                                                name="Archipelago", fullscreen=True)], realtime=True)


class ArchipelagoBot(bot.bot_ai.BotAI):
    game_running: bool = False
    mission_completed: bool = False
    boni: typing.List[bool]
    setup_done: bool
    ctx: SC2Context
    mission_id: int
    want_close: bool = False
    can_read_game = False
    last_received_update: int = 0

    def __init__(self, ctx: SC2Context, mission_id):
        self.setup_done = False
        self.ctx = ctx
        self.ctx.last_bot = self
        self.mission_id = mission_id
        self.boni = [False for _ in range(max_bonus)]

        super(ArchipelagoBot, self).__init__()

    async def on_step(self, iteration: int):
        if self.want_close:
            self.want_close = False
            await self._client.leave()
            return
        game_state = 0
        if not self.setup_done:
            self.setup_done = True
            start_items = calculate_items(self.ctx)
            if self.ctx.difficulty_override >= 0:
                difficulty = calc_difficulty(self.ctx.difficulty_override)
            else:
                difficulty = calc_difficulty(self.ctx.difficulty)
            if self.ctx.game_speed_override >= 0:
                game_speed = self.ctx.game_speed_override
            else:
                game_speed = self.ctx.game_speed
            await self.chat_send("?SetOptions {} {} {} {}".format(
                difficulty,
                self.ctx.generic_upgrade_research,
                self.ctx.all_in_choice,
                game_speed
            ))
            await self.chat_send("?GiveResources {} {} {}".format(
                start_items[8],
                start_items[9],
                start_items[10]
            ))
            await self.chat_send("?GiveTerranTech {} {} {} {} {} {} {} {} {} {}".format(
                start_items[0], start_items[1], start_items[2], start_items[3], start_items[4],
                start_items[5], start_items[6], start_items[12], start_items[13], start_items[14]))
            await self.chat_send("?GiveProtossTech {}".format(start_items[7]))
            await self.chat_send("?SetColor rr " + str(self.ctx.player_color))  # TODO: Add faction color options
            await self.chat_send("?LoadFinished")
            self.last_received_update = len(self.ctx.items_received)

        else:
            if not self.ctx.announcements.empty():
                message = self.ctx.announcements.get(timeout=1)
                await self.chat_send("?SendMessage " + message)
                self.ctx.announcements.task_done()

            # Archipelago reads the health
            for unit in self.all_own_units():
                if unit.health_max == 38281:
                    game_state = int(38281 - unit.health)
                    self.can_read_game = True

            if iteration == 160 and not game_state & 1:
                await self.chat_send("?SendMessage Warning: Archipelago unable to connect or has lost connection to " +
                                     "Starcraft 2 (This is likely a map issue)")

            if self.last_received_update < len(self.ctx.items_received):
                current_items = calculate_items(self.ctx)
                await self.chat_send("?GiveTerranTech {} {} {} {} {} {} {} {} {} {}".format(
                    current_items[0], current_items[1], current_items[2], current_items[3], current_items[4],
                    current_items[5], current_items[6], current_items[12], current_items[13], current_items[14]))
                await self.chat_send("?GiveProtossTech {}".format(current_items[7]))
                self.last_received_update = len(self.ctx.items_received)

            if game_state & 1:
                if not self.game_running:
                    print("Archipelago Connected")
                    self.game_running = True

                if self.can_read_game:
                    if game_state & (1 << 1) and not self.mission_completed:
                        if self.mission_id != self.ctx.final_mission:
                            print("Mission Completed")
                            await self.ctx.send_msgs(
                                [{"cmd": 'LocationChecks',
                                  "locations": [SC2WOL_LOC_ID_OFFSET + victory_modulo * self.mission_id]}])
                            self.mission_completed = True
                        else:
                            print("Game Complete")
                            await self.ctx.send_msgs([{"cmd": 'StatusUpdate', "status": ClientStatus.CLIENT_GOAL}])
                            self.mission_completed = True

                    for x, completed in enumerate(self.boni):
                        if not completed and game_state & (1 << (x + 2)):
                            await self.ctx.send_msgs(
                                [{"cmd": 'LocationChecks',
                                  "locations": [SC2WOL_LOC_ID_OFFSET + victory_modulo * self.mission_id + x + 1]}])
                            self.boni[x] = True

                else:
                    await self.chat_send("?SendMessage LostConnection - Lost connection to game.")


def request_unfinished_missions(ctx: SC2Context):
    if ctx.mission_req_table:
        message = "Unfinished Missions: "
        unlocks = initialize_blank_mission_dict(ctx.mission_req_table)
        unfinished_locations = initialize_blank_mission_dict(ctx.mission_req_table)

        _, unfinished_missions = calc_unfinished_missions(ctx, unlocks=unlocks)

        # Removing All-In from location pool
        final_mission = lookup_id_to_mission[ctx.final_mission]
        if final_mission in unfinished_missions.keys():
            message = f"Final Mission Available: {final_mission}[{ctx.final_mission}]\n" + message
            if unfinished_missions[final_mission] == -1:
                unfinished_missions.pop(final_mission)

        message += ", ".join(f"{mark_up_mission_name(ctx, mission, unlocks)}[{ctx.mission_req_table[mission].id}] " +
                             mark_up_objectives(
                                 f"[{len(unfinished_missions[mission])}/"
                                 f"{sum(1 for _ in ctx.locations_for_mission(mission))}]",
                                 ctx, unfinished_locations, mission)
                             for mission in unfinished_missions)

        if ctx.ui:
            ctx.ui.log_panels['All'].on_message_markup(message)
            ctx.ui.log_panels['Starcraft2'].on_message_markup(message)
        else:
            sc2_logger.info(message)
    else:
        sc2_logger.warning("No mission table found, you are likely not connected to a server.")


def calc_unfinished_missions(ctx: SC2Context, unlocks=None):
    unfinished_missions = []
    locations_completed = []

    if not unlocks:
        unlocks = initialize_blank_mission_dict(ctx.mission_req_table)

    available_missions = calc_available_missions(ctx, unlocks)

    for name in available_missions:
        objectives = set(ctx.locations_for_mission(name))
        if objectives:
            objectives_completed = ctx.checked_locations & objectives
            if len(objectives_completed) < len(objectives):
                unfinished_missions.append(name)
                locations_completed.append(objectives_completed)

        else:  # infer that this is the final mission as it has no objectives
            unfinished_missions.append(name)
            locations_completed.append(-1)

    return available_missions, dict(zip(unfinished_missions, locations_completed))


def is_mission_available(ctx: SC2Context, mission_id_to_check):
    unfinished_missions = calc_available_missions(ctx)

    return any(mission_id_to_check == ctx.mission_req_table[mission].id for mission in unfinished_missions)


def mark_up_mission_name(ctx: SC2Context, mission, unlock_table):
    """Checks if the mission is required for game completion and adds '*' to the name to mark that."""

    if ctx.mission_req_table[mission].completion_critical:
        if ctx.ui:
            message = "[color=AF99EF]" + mission + "[/color]"
        else:
            message = "*" + mission + "*"
    else:
        message = mission

    if ctx.ui:
        unlocks = unlock_table[mission]

        if len(unlocks) > 0:
            pre_message = f"[ref={list(ctx.mission_req_table).index(mission)}|Unlocks: "
            pre_message += ", ".join(f"{unlock}({ctx.mission_req_table[unlock].id})" for unlock in unlocks)
            pre_message += f"]"
            message = pre_message + message + "[/ref]"

    return message


def mark_up_objectives(message, ctx, unfinished_locations, mission):
    formatted_message = message

    if ctx.ui:
        locations = unfinished_locations[mission]

        pre_message = f"[ref={list(ctx.mission_req_table).index(mission) + 30}|"
        pre_message += "<br>".join(location for location in locations)
        pre_message += f"]"
        formatted_message = pre_message + message + "[/ref]"

    return formatted_message


def request_available_missions(ctx: SC2Context):
    if ctx.mission_req_table:
        message = "Available Missions: "

        # Initialize mission unlock table
        unlocks = initialize_blank_mission_dict(ctx.mission_req_table)

        missions = calc_available_missions(ctx, unlocks)
        message += \
            ", ".join(f"{mark_up_mission_name(ctx, mission, unlocks)}"
                      f"[{ctx.mission_req_table[mission].id}]"
                      for mission in missions)

        if ctx.ui:
            ctx.ui.log_panels['All'].on_message_markup(message)
            ctx.ui.log_panels['Starcraft2'].on_message_markup(message)
        else:
            sc2_logger.info(message)
    else:
        sc2_logger.warning("No mission table found, you are likely not connected to a server.")


def calc_available_missions(ctx: SC2Context, unlocks=None):
    available_missions = []
    missions_complete = 0

    # Get number of missions completed
    for loc in ctx.checked_locations:
        if loc % victory_modulo == 0:
            missions_complete += 1

    for name in ctx.mission_req_table:
        # Go through the required missions for each mission and fill up unlock table used later for hover-over tooltips
        if unlocks:
            for unlock in ctx.mission_req_table[name].required_world:
                unlocks[list(ctx.mission_req_table)[unlock - 1]].append(name)

        if mission_reqs_completed(ctx, name, missions_complete):
            available_missions.append(name)

    return available_missions


def mission_reqs_completed(ctx: SC2Context, mission_name: str, missions_complete: int):
    """Returns a bool signifying if the mission has all requirements complete and can be done

    Arguments:
    ctx -- instance of SC2Context
    locations_to_check -- the mission string name to check
    missions_complete -- an int of how many missions have been completed
    mission_path -- a list of missions that have already been checked
"""
    if len(ctx.mission_req_table[mission_name].required_world) >= 1:
        # A check for when the requirements are being or'd
        or_success = False

        # Loop through required missions
        for req_mission in ctx.mission_req_table[mission_name].required_world:
            req_success = True

            # Check if required mission has been completed
            if not (ctx.mission_req_table[list(ctx.mission_req_table)[req_mission - 1]].id *
                    victory_modulo + SC2WOL_LOC_ID_OFFSET) in ctx.checked_locations:
                if not ctx.mission_req_table[mission_name].or_requirements:
                    return False
                else:
                    req_success = False

            # Grid-specific logic (to avoid long path checks and infinite recursion)
            if ctx.mission_order in (3, 4):
                if req_success:
                    return True
                else:
                    if req_mission is ctx.mission_req_table[mission_name].required_world[-1]:
                        return False
                    else:
                        continue

            # Recursively check required mission to see if it's requirements are met, in case !collect has been done
            # Skipping recursive check on Grid settings to speed up checks and avoid infinite recursion
            if not mission_reqs_completed(ctx, list(ctx.mission_req_table)[req_mission - 1], missions_complete):
                if not ctx.mission_req_table[mission_name].or_requirements:
                    return False
                else:
                    req_success = False

            # If requirement check succeeded mark or as satisfied
            if ctx.mission_req_table[mission_name].or_requirements and req_success:
                or_success = True

        if ctx.mission_req_table[mission_name].or_requirements:
            # Return false if or requirements not met
            if not or_success:
                return False

        # Check number of missions
        if missions_complete >= ctx.mission_req_table[mission_name].number:
            return True
        else:
            return False
    else:
        return True


def initialize_blank_mission_dict(location_table):
    unlocks = {}

    for mission in list(location_table):
        unlocks[mission] = []

    return unlocks


def check_game_install_path() -> bool:
    # First thing: go to the default location for ExecuteInfo.
    # An exception for Windows is included because it's very difficult to find ~\Documents if the user moved it.
    if is_windows:
        # The next five lines of utterly inscrutable code are brought to you by copy-paste from Stack Overflow.
        # https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path/30924555#
        import ctypes.wintypes
        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        documentspath = buf.value
        einfo = str(documentspath / Path("StarCraft II\\ExecuteInfo.txt"))
    else:
        einfo = str(bot.paths.get_home() / Path(bot.paths.USERPATH[bot.paths.PF]))

    # Check if the file exists.
    if os.path.isfile(einfo):

        # Open the file and read it, picking out the latest executable's path.
        with open(einfo) as f:
            content = f.read()
        if content:
            try:
                base = re.search(r" = (.*)Versions", content).group(1)
            except AttributeError:
                sc2_logger.warning(f"Found {einfo}, but it was empty. Run SC2 through the Blizzard launcher, then "
                                   f"try again.")
                return False
            if os.path.exists(base):
                executable = bot.paths.latest_executeble(Path(base).expanduser() / "Versions")

                # Finally, check the path for an actual executable.
                # If we find one, great. Set up the SC2PATH.
                if os.path.isfile(executable):
                    sc2_logger.info(f"Found an SC2 install at {base}!")
                    sc2_logger.debug(f"Latest executable at {executable}.")
                    os.environ["SC2PATH"] = base
                    sc2_logger.debug(f"SC2PATH set to {base}.")
                    return True
                else:
                    sc2_logger.warning(f"We may have found an SC2 install at {base}, but couldn't find {executable}.")
            else:
                sc2_logger.warning(f"{einfo} pointed to {base}, but we could not find an SC2 install there.")
    else:
        sc2_logger.warning(f"Couldn't find {einfo}. Run SC2 through the Blizzard launcher, then try again. "
                           f"If that fails, please run /set_path with your SC2 install directory.")
    return False


def is_mod_installed_correctly() -> bool:
    """Searches for all required files."""
    if "SC2PATH" not in os.environ:
        check_game_install_path()

    mapdir = os.environ['SC2PATH'] / Path('Maps/ArchipelagoCampaign')
    mods = ["ArchipelagoCore", "ArchipelagoPlayer", "ArchipelagoPlayerWoL", "ArchipelagoTriggers"]
    modfiles = [os.environ["SC2PATH"] / Path("Mods/" + mod + ".SC2Mod") for mod in mods]
    wol_required_maps = ["WoL" + os.sep + map_name + ".SC2Map" for map_name in maps_table]
    needs_files = False

    # Check for maps.
    missing_maps = []
    for mapfile in wol_required_maps:
        if not os.path.isfile(mapdir / mapfile):
            missing_maps.append(mapfile)
    if len(missing_maps) >= 19:
        sc2_logger.warning(f"All map files missing from {mapdir}.")
        needs_files = True
    elif len(missing_maps) > 0:
        for map in missing_maps:
            sc2_logger.debug(f"Missing {map} from {mapdir}.")
            sc2_logger.warning(f"Missing {len(missing_maps)} map files.")
        needs_files = True
    else:  # Must be no maps missing
        sc2_logger.info(f"All maps found in {mapdir}.")

    # Check for mods.
    for modfile in modfiles:
        if os.path.isfile(modfile) or os.path.isdir(modfile):
            sc2_logger.info(f"Archipelago mod found at {modfile}.")
        else:
            sc2_logger.warning(f"Archipelago mod could not be found at {modfile}.")
            needs_files = True

    # Final verdict.
    if needs_files:
        sc2_logger.warning(f"Required files are missing. Run /download_data to acquire them.")
        return False
    else:
        sc2_logger.debug(f"All map/mod files are properly installed.")
        return True


class DllDirectory:
    # Credit to Black Sliver for this code.
    # More info: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setdlldirectoryw
    _old: typing.Optional[str] = None
    _new: typing.Optional[str] = None

    def __init__(self, new: typing.Optional[str]):
        self._new = new

    def __enter__(self):
        old = self.get()
        if self.set(self._new):
            self._old = old

    def __exit__(self, *args):
        if self._old is not None:
            self.set(self._old)

    @staticmethod
    def get() -> typing.Optional[str]:
        if sys.platform == "win32":
            n = ctypes.windll.kernel32.GetDllDirectoryW(0, None)
            buf = ctypes.create_unicode_buffer(n)
            ctypes.windll.kernel32.GetDllDirectoryW(n, buf)
            return buf.value
        # NOTE: other OS may support os.environ["LD_LIBRARY_PATH"], but this fix is windows-specific
        return None

    @staticmethod
    def set(s: typing.Optional[str]) -> bool:
        if sys.platform == "win32":
            return ctypes.windll.kernel32.SetDllDirectoryW(s) != 0
        # NOTE: other OS may support os.environ["LD_LIBRARY_PATH"], but this fix is windows-specific
        return False


def download_latest_release_zip(owner: str, repo: str, api_version: str, metadata: str = None, force_download=False) -> (str, str):
    """Downloads the latest release of a GitHub repo to the current directory as a .zip file."""
    import requests

    headers = {"Accept": 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{api_version}"

    r1 = requests.get(url, headers=headers)
    if r1.status_code == 200:
        latest_metadata = r1.json()
        cleanup_downloaded_metadata(latest_metadata)
        latest_metadata = str(latest_metadata)
        # sc2_logger.info(f"Latest version: {latest_metadata}.")
    else:
        sc2_logger.warning(f"Status code: {r1.status_code}")
        sc2_logger.warning(f"Failed to reach GitHub. Could not find download link.")
        sc2_logger.warning(f"text: {r1.text}")
        return "", metadata

    if (force_download is False) and (metadata == latest_metadata):
        sc2_logger.info("Latest version already installed.")
        return "", metadata

    sc2_logger.info(f"Attempting to download latest version of API version {api_version} of {repo}.")
    download_url = r1.json()["assets"][0]["browser_download_url"]

    r2 = requests.get(download_url, headers=headers)
    if r2.status_code == 200 and zipfile.is_zipfile(io.BytesIO(r2.content)):
        tempdir = tempfile.gettempdir()
        file = tempdir + os.sep + f"{repo}.zip"
        with open(file, "wb") as fh:
            fh.write(r2.content)
        sc2_logger.info(f"Successfully downloaded {repo}.zip.")
        return file, latest_metadata
    else:
        sc2_logger.warning(f"Status code: {r2.status_code}")
        sc2_logger.warning("Download failed.")
        sc2_logger.warning(f"text: {r2.text}")
        return "", metadata


def cleanup_downloaded_metadata(medatada_json):
    for asset in medatada_json['assets']:
        del asset['download_count']


def is_mod_update_available(owner: str, repo: str, api_version: str, metadata: str) -> bool:
    import requests

    headers = {"Accept": 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{api_version}"

    r1 = requests.get(url, headers=headers)
    if r1.status_code == 200:
        latest_metadata = r1.json()
        cleanup_downloaded_metadata(latest_metadata)
        latest_metadata = str(latest_metadata)
        if metadata != latest_metadata:
            return True
        else:
            return False

    else:
        sc2_logger.warning(f"Failed to reach GitHub while checking for updates.")
        sc2_logger.warning(f"Status code: {r1.status_code}")
        sc2_logger.warning(f"text: {r1.text}")
        return False


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
