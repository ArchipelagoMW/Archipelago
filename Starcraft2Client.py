from __future__ import annotations

import multiprocessing
import logging
import asyncio
import os.path

import nest_asyncio
import sc2

from sc2.main import run_game
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.player import Bot

from worlds.sc2wol.Regions import MissionInfo
from worlds.sc2wol.MissionTables import lookup_id_to_mission
from worlds.sc2wol.Items import lookup_id_to_name, item_table
from worlds.sc2wol.Locations import SC2WOL_LOC_ID_OFFSET
from worlds.sc2wol import SC2WoLWorld

from Utils import init_logging

if __name__ == "__main__":
    init_logging("SC2Client", exception_logger="Client")

logger = logging.getLogger("Client")
sc2_logger = logging.getLogger("Starcraft2")

import colorama

from NetUtils import *
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser

nest_asyncio.apply()


class StarcraftClientProcessor(ClientCommandProcessor):
    ctx: SC2Context

    def _cmd_disable_mission_check(self) -> bool:
        """Disables the check to see if a mission is available to play.  Meant for co-op runs where one player can play
        the next mission in a chain the other player is doing."""
        self.ctx.missions_unlocked = True
        sc2_logger.info("Mission check has been disabled")

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

        return True

    def _cmd_available(self) -> bool:
        """Get what missions are currently available to play"""

        request_available_missions(self.ctx.checked_locations, self.ctx.mission_req_table, self.ctx.ui)
        return True

    def _cmd_unfinished(self) -> bool:
        """Get what missions are currently available to play and have not had all locations checked"""

        request_unfinished_missions(self.ctx.checked_locations, self.ctx.mission_req_table, self.ctx.ui, self.ctx)
        return True


class SC2Context(CommonContext):
    command_processor = StarcraftClientProcessor
    game = "Starcraft 2 Wings of Liberty"
    items_handling = 0b111
    difficulty = -1
    all_in_choice = 0
    mission_req_table = None
    items_rec_to_announce = []
    rec_announce_pos = 0
    items_sent_to_announce = []
    sent_announce_pos = 0
    announcements = []
    announcement_pos = 0
    sc2_run_task: typing.Optional[asyncio.Task] = None
    missions_unlocked = False
    current_tooltip = None
    last_loc_list = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SC2Context, self).server_auth(password_requested)
        if not self.auth:
            logger.info('Enter slot name:')
            self.auth = await self.console_input()

        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.difficulty = args["slot_data"]["game_difficulty"]
            self.all_in_choice = args["slot_data"]["all_in_map"]
            slot_req_table = args["slot_data"]["mission_req"]
            self.mission_req_table = {}
            # Compatibility for 0.3.2 server data.
            if "category" not in next(iter(slot_req_table)):
                for i, mission_data in enumerate(slot_req_table.values()):
                    mission_data["category"] = wol_default_categories[i]
            for mission in slot_req_table:
                self.mission_req_table[mission] = MissionInfo(**slot_req_table[mission])

        if cmd in {"PrintJSON"}:
            noted = False
            if "receiving" in args:
                if args["receiving"] == self.slot:
                    self.announcements.append(args["data"])
                    noted = True
            if not noted and "item" in args:
                if args["item"].player == self.slot:
                    self.announcements.append(args["data"])

    def run_gui(self):
        from kvui import GameManager, HoverBehavior, ServerToolTip, fade_in_animation
        from kivy.app import App
        from kivy.clock import Clock
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.gridlayout import GridLayout
        from kivy.lang import Builder
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.floatlayout import FloatLayout
        from kivy.properties import StringProperty

        import Utils

        class HoverableButton(HoverBehavior, Button):
            pass

        class MissionButton(HoverableButton):
            tooltip_text = StringProperty("Test")

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
                if self.ctx.current_tooltip:
                    App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

                self.ctx.current_tooltip = None

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
            launching = False
            refresh_from_launching = True
            first_check = True

            def __init__(self, ctx):
                super().__init__(ctx)

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
                        available_missions = []
                        unfinished_locations = initialize_blank_mission_dict(self.ctx.mission_req_table)
                        unfinished_missions = calc_unfinished_missions(self.ctx.checked_locations,
                                                                       self.ctx.mission_req_table,
                                                                       self.ctx, available_missions=available_missions,
                                                                       unfinished_locations=unfinished_locations)

                        # separate missions into categories
                        for mission in self.ctx.mission_req_table:
                            if not self.ctx.mission_req_table[mission].category in categories:
                                categories[self.ctx.mission_req_table[mission].category] = []

                            categories[self.ctx.mission_req_table[mission].category].append(mission)

                        for category in categories:
                            category_panel = MissionCategory()
                            category_panel.add_widget(Label(text=category, size_hint_y=None, height=50, outline_width=1))

                            # Map is completed
                            for mission in categories[category]:
                                text = mission
                                tooltip = ""

                                # Map has uncollected locations
                                if mission in unfinished_missions:
                                    text = f"[color=6495ED]{text}[/color]"

                                    tooltip = f"Uncollected locations:\n"
                                    tooltip += "\n".join(location for location in unfinished_locations[mission])
                                elif mission in available_missions:
                                    text = f"[color=FFFFFF]{text}[/color]"
                                # Map requirements not met
                                else:
                                    text = f"[color=a9a9a9]{text}[/color]"
                                    tooltip = f"Requires: "
                                    if len(self.ctx.mission_req_table[mission].required_world) > 0:
                                        tooltip += ", ".join(list(self.ctx.mission_req_table)[req_mission-1] for
                                                             req_mission in
                                                             self.ctx.mission_req_table[mission].required_world)

                                        if self.ctx.mission_req_table[mission].number > 0:
                                            tooltip += " and "
                                    if self.ctx.mission_req_table[mission].number > 0:
                                        tooltip += f"{self.ctx.mission_req_table[mission].number} missions completed"

                                mission_button = MissionButton(text=text, size_hint_y=None, height=50)
                                mission_button.tooltip_text = tooltip
                                mission_button.bind(on_press=self.mission_callback)
                                self.mission_id_to_button[self.ctx.mission_req_table[mission].id] = mission_button
                                category_panel.add_widget(mission_button)

                            category_panel.add_widget(Label(text=""))
                            self.mission_panel.add_widget(category_panel)

                elif self.launching:
                    self.refresh_from_launching = False

                    self.mission_panel.clear_widgets()
                    self.mission_panel.add_widget(Label(text="Launching Mission"))

            def mission_callback(self, button):
                if not self.launching:
                    self.ctx.play_mission(list(self.mission_id_to_button.keys())
                                          [list(self.mission_id_to_button.values()).index(button)])
                    self.launching = True
                    Clock.schedule_once(self.finish_launching, 10)

            def finish_launching(self, dt):
                self.launching = False

        self.ui = SC2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

        Builder.load_file(Utils.local_path(os.path.dirname(SC2WoLWorld.__file__), "Starcraft2.kv"))

    async def shutdown(self):
        await super(SC2Context, self).shutdown()
        if self.sc2_run_task:
            self.sc2_run_task.cancel()

    def play_mission(self, mission_id):
        if self.missions_unlocked or \
                is_mission_available(mission_id, self.checked_locations, self.mission_req_table):
            if self.sc2_run_task:
                if not self.sc2_run_task.done():
                    sc2_logger.warning("Starcraft 2 Client is still running!")
                self.sc2_run_task.cancel()  # doesn't actually close the game, just stops the python task
            if self.slot is None:
                sc2_logger.warning("Launching Mission without Archipelago authentication, "
                                   "checks will not be registered to server.")
            self.sc2_run_task = asyncio.create_task(starcraft_launch(self, mission_id),
                                                        name="Starcraft 2 Launch")
        else:
            sc2_logger.info(
                f"{lookup_id_to_mission[mission_id]} is not currently unlocked.  "
                f"Use /unfinished or /available to see what is available.")


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
    "ap_traynor01", "ap_traynor02", "ap_traynor03",
    "ap_thanson01", "ap_thanson02", "ap_thanson03a", "ap_thanson03b",
    "ap_ttychus01", "ap_ttychus02", "ap_ttychus03", "ap_ttychus04", "ap_ttychus05",
    "ap_ttosh01", "ap_ttosh02", "ap_ttosh03a", "ap_ttosh03b",
    "ap_thorner01", "ap_thorner02", "ap_thorner03", "ap_thorner04", "ap_thorner05s",
    "ap_tzeratul01", "ap_tzeratul02", "ap_tzeratul03", "ap_tzeratul04",
    "ap_tvalerian01", "ap_tvalerian02a", "ap_tvalerian02b", "ap_tvalerian03"
]

wol_default_categories = [
    "Mar Sara", "Mar Sara", "Mar Sara", "Colonist", "Colonist", "Colonist", "Colonist",
    "Artifact", "Artifact", "Artifact", "Artifact", "Artifact", "Covert", "Covert", "Covert", "Covert",
    "Rebellion", "Rebellion", "Rebellion", "Rebellion", "Rebellion", "Prophecy", "Prophecy", "Prophecy", "Prophecy",
    "Char", "Char", "Char", "Char"
]


def calculate_items(items):
    unit_unlocks = 0
    armory1_unlocks = 0
    armory2_unlocks = 0
    upgrade_unlocks = 0
    building_unlocks = 0
    merc_unlocks = 0
    lab_unlocks = 0
    protoss_unlock = 0
    minerals = 0
    vespene = 0
    supply = 0

    for item in items:
        data = lookup_id_to_name[item.item]

        if item_table[data].type == "Unit":
            unit_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Upgrade":
            upgrade_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Armory 1":
            armory1_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Armory 2":
            armory2_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Building":
            building_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Mercenary":
            merc_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Laboratory":
            lab_unlocks += (1 << item_table[data].number)
        elif item_table[data].type == "Protoss":
            protoss_unlock += (1 << item_table[data].number)
        elif item_table[data].type == "Minerals":
            minerals += item_table[data].number
        elif item_table[data].type == "Vespene":
            vespene += item_table[data].number
        elif item_table[data].type == "Supply":
            supply += item_table[data].number

    return [unit_unlocks, upgrade_unlocks, armory1_unlocks, armory2_unlocks, building_unlocks, merc_unlocks,
            lab_unlocks, protoss_unlock, minerals, vespene, supply]


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


async def starcraft_launch(ctx: SC2Context, mission_id):
    ctx.rec_announce_pos = len(ctx.items_rec_to_announce)
    ctx.sent_announce_pos = len(ctx.items_sent_to_announce)
    ctx.announcements_pos = len(ctx.announcements)

    sc2_logger.info(f"Launching {lookup_id_to_mission[mission_id]}. If game does not launch check log file for errors.")

    run_game(sc2.maps.get(maps_table[mission_id - 1]), [Bot(Race.Terran, ArchipelagoBot(ctx, mission_id),
                                                            name="Archipelago", fullscreen=True)], realtime=True)


class ArchipelagoBot(sc2.bot_ai.BotAI):
    game_running = False
    mission_completed = False
    first_bonus = False
    second_bonus = False
    third_bonus = False
    fourth_bonus = False
    fifth_bonus = False
    sixth_bonus = False
    seventh_bonus = False
    eight_bonus = False
    ctx: SC2Context = None
    mission_id = 0

    can_read_game = False

    last_received_update = 0

    def __init__(self, ctx: SC2Context, mission_id):
        self.ctx = ctx
        self.mission_id = mission_id

        super(ArchipelagoBot, self).__init__()

    async def on_step(self, iteration: int):
        game_state = 0
        if iteration == 0:
            start_items = calculate_items(self.ctx.items_received)
            difficulty = calc_difficulty(self.ctx.difficulty)
            await self.chat_send("ArchipelagoLoad {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
                difficulty,
                start_items[0], start_items[1], start_items[2], start_items[3], start_items[4],
                start_items[5], start_items[6], start_items[7], start_items[8], start_items[9],
                self.ctx.all_in_choice, start_items[10]))
            self.last_received_update = len(self.ctx.items_received)

        else:
            if self.ctx.announcement_pos < len(self.ctx.announcements):
                index = 0
                message = ""
                while index < len(self.ctx.announcements[self.ctx.announcement_pos]):
                    message += self.ctx.announcements[self.ctx.announcement_pos][index]["text"]
                    index += 1

                index = 0
                start_rem_pos = -1
                # Remove unneeded [Color] tags
                while index < len(message):
                    if message[index] == '[':
                        start_rem_pos = index
                        index += 1
                    elif message[index] == ']' and start_rem_pos > -1:
                        temp_msg = ""

                        if start_rem_pos > 0:
                            temp_msg = message[:start_rem_pos]
                        if index < len(message) - 1:
                            temp_msg += message[index + 1:]

                        message = temp_msg
                        index += start_rem_pos - index
                        start_rem_pos = -1
                    else:
                        index += 1

                await self.chat_send("SendMessage " + message)
                self.ctx.announcement_pos += 1

            # Archipelago reads the health
            for unit in self.all_own_units():
                if unit.health_max == 38281:
                    game_state = int(38281 - unit.health)
                    self.can_read_game = True

            if iteration == 160 and not game_state & 1:
                await self.chat_send("SendMessage Warning: Archipelago unable to connect or has lost connection to " +
                                     "Starcraft 2 (This is likely a map issue)")

            if self.last_received_update < len(self.ctx.items_received):
                current_items = calculate_items(self.ctx.items_received)
                await self.chat_send("UpdateTech {} {} {} {} {} {} {} {}".format(
                    current_items[0], current_items[1], current_items[2], current_items[3], current_items[4],
                    current_items[5], current_items[6], current_items[7]))
                self.last_received_update = len(self.ctx.items_received)

            if game_state & 1:
                if not self.game_running:
                    print("Archipelago Connected")
                    self.game_running = True

                if self.can_read_game:
                    if game_state & (1 << 1) and not self.mission_completed:
                        if self.mission_id != 29:
                            print("Mission Completed")
                            await self.ctx.send_msgs([
                                {"cmd": 'LocationChecks', "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id]}])
                            self.mission_completed = True
                        else:
                            print("Game Complete")
                            await self.ctx.send_msgs([{"cmd": 'StatusUpdate', "status": ClientStatus.CLIENT_GOAL}])
                            self.mission_completed = True

                    if game_state & (1 << 2) and not self.first_bonus:
                        print("1st Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 1]}])
                        self.first_bonus = True

                    if not self.second_bonus and game_state & (1 << 3):
                        print("2nd Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 2]}])
                        self.second_bonus = True

                    if not self.third_bonus and game_state & (1 << 4):
                        print("3rd Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 3]}])
                        self.third_bonus = True

                    if not self.fourth_bonus and game_state & (1 << 5):
                        print("4th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 4]}])
                        self.fourth_bonus = True

                    if not self.fifth_bonus and game_state & (1 << 6):
                        print("5th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 5]}])
                        self.fifth_bonus = True

                    if not self.sixth_bonus and game_state & (1 << 7):
                        print("6th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 6]}])
                        self.sixth_bonus = True

                    if not self.seventh_bonus and game_state & (1 << 8):
                        print("6th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 7]}])
                        self.seventh_bonus = True

                    if not self.eight_bonus and game_state & (1 << 9):
                        print("6th Bonus Collected")
                        await self.ctx.send_msgs(
                            [{"cmd": 'LocationChecks',
                              "locations": [SC2WOL_LOC_ID_OFFSET + 100 * self.mission_id + 8]}])
                        self.eight_bonus = True

                else:
                    await self.chat_send("LostConnection - Lost connection to game.")


def calc_objectives_completed(mission, missions_info, locations_done, unfinished_locations, ctx):
    objectives_complete = 0

    if missions_info[mission].extra_locations > 0:
        for i in range(missions_info[mission].extra_locations):
            if (missions_info[mission].id * 100 + SC2WOL_LOC_ID_OFFSET + i) in locations_done:
                objectives_complete += 1
            else:
                unfinished_locations[mission].append(ctx.location_name_getter(
                    missions_info[mission].id * 100 + SC2WOL_LOC_ID_OFFSET + i))

        return objectives_complete

    else:
        return -1


def request_unfinished_missions(locations_done, location_table, ui, ctx):
    if location_table:
        message = "Unfinished Missions: "
        unlocks = initialize_blank_mission_dict(location_table)
        unfinished_locations = initialize_blank_mission_dict(location_table)

        unfinished_missions = calc_unfinished_missions(locations_done, location_table, ctx, unlocks=unlocks,
                                                       unfinished_locations=unfinished_locations)

        message += ", ".join(f"{mark_up_mission_name(mission, location_table, ui,unlocks)}[{location_table[mission].id}] " +
                             mark_up_objectives(
                                 f"[{unfinished_missions[mission]}/{location_table[mission].extra_locations}]",
                                 ctx, unfinished_locations, mission)
                             for mission in unfinished_missions)

        if ui:
            ui.log_panels['All'].on_message_markup(message)
            ui.log_panels['Starcraft2'].on_message_markup(message)
        else:
            sc2_logger.info(message)
    else:
        sc2_logger.warning("No mission table found, you are likely not connected to a server.")


def calc_unfinished_missions(locations_done, locations, ctx, unlocks=None, unfinished_locations=None,
                             available_missions=[]):
    unfinished_missions = []
    locations_completed = []

    if not unlocks:
        unlocks = initialize_blank_mission_dict(locations)

    if not unfinished_locations:
        unfinished_locations = initialize_blank_mission_dict(locations)

    if len(available_missions) > 0:
        available_missions = []

    available_missions.extend(calc_available_missions(locations_done, locations, unlocks))

    for name in available_missions:
        if not locations[name].extra_locations == -1:
            objectives_completed = calc_objectives_completed(name, locations, locations_done, unfinished_locations, ctx)

            if objectives_completed < locations[name].extra_locations:
                unfinished_missions.append(name)
                locations_completed.append(objectives_completed)

        else:
            unfinished_missions.append(name)
            locations_completed.append(-1)

    return {unfinished_missions[i]: locations_completed[i] for i in range(len(unfinished_missions))}


def is_mission_available(mission_id_to_check, locations_done, locations):
    unfinished_missions = calc_available_missions(locations_done, locations)

    return any(mission_id_to_check == locations[mission].id for mission in unfinished_missions)


def mark_up_mission_name(mission, location_table, ui, unlock_table):
    """Checks if the mission is required for game completion and adds '*' to the name to mark that."""

    if location_table[mission].completion_critical:
        if ui:
            message = "[color=AF99EF]" + mission + "[/color]"
        else:
            message = "*" + mission + "*"
    else:
        message = mission

    if ui:
        unlocks = unlock_table[mission]

        if len(unlocks) > 0:
            pre_message = f"[ref={list(location_table).index(mission)}|Unlocks: "
            pre_message += ", ".join(f"{unlock}({location_table[unlock].id})" for unlock in unlocks)
            pre_message += f"]"
            message = pre_message + message + "[/ref]"

    return message


def mark_up_objectives(message, ctx, unfinished_locations, mission):
    formatted_message = message

    if ctx.ui:
        locations = unfinished_locations[mission]

        pre_message = f"[ref={list(ctx.mission_req_table).index(mission)+30}|"
        pre_message += "<br>".join(location for location in locations)
        pre_message += f"]"
        formatted_message = pre_message + message + "[/ref]"

    return formatted_message


def request_available_missions(locations_done, location_table, ui):
    if location_table:
        message = "Available Missions: "

        # Initialize mission unlock table
        unlocks = initialize_blank_mission_dict(location_table)

        missions = calc_available_missions(locations_done, location_table, unlocks)
        message += \
            ", ".join(f"{mark_up_mission_name(mission, location_table, ui, unlocks)}[{location_table[mission].id}]"
                      for mission in missions)

        if ui:
            ui.log_panels['All'].on_message_markup(message)
            ui.log_panels['Starcraft2'].on_message_markup(message)
        else:
            sc2_logger.info(message)
    else:
        sc2_logger.warning("No mission table found, you are likely not connected to a server.")


def calc_available_missions(locations_done, locations, unlocks=None):
    available_missions = []
    missions_complete = 0

    # Get number of missions completed
    for loc in locations_done:
        if loc % 100 == 0:
            missions_complete += 1

    for name in locations:
        # Go through the required missions for each mission and fill up unlock table used later for hover-over tooltips
        if unlocks:
            for unlock in locations[name].required_world:
                unlocks[list(locations)[unlock-1]].append(name)

        if mission_reqs_completed(name, missions_complete, locations_done, locations):
            available_missions.append(name)

    return available_missions


def mission_reqs_completed(location_to_check, missions_complete, locations_done, locations):
    """Returns a bool signifying if the mission has all requirements complete and can be done

    Keyword arguments:
    locations_to_check -- the mission string name to check
    missions_complete -- an int of how many missions have been completed
    locations_done -- a list of the location ids that have been complete
    locations -- a dict of MissionInfo for mission requirements for this world"""
    if len(locations[location_to_check].required_world) >= 1:
        # A check for when the requirements are being or'd
        or_success = False

        # Loop through required missions
        for req_mission in locations[location_to_check].required_world:
            req_success = True

            # Check if required mission has been completed
            if not (locations[list(locations)[req_mission-1]].id * 100 + SC2WOL_LOC_ID_OFFSET) in locations_done:
                if not locations[location_to_check].or_requirements:
                    return False
                else:
                    req_success = False

            # Recursively check required mission to see if it's requirements are met, in case !collect has been done
            if not mission_reqs_completed(list(locations)[req_mission-1], missions_complete, locations_done,
                                          locations):
                if not locations[location_to_check].or_requirements:
                    return False
                else:
                    req_success = False

            # If requirement check succeeded mark or as satisfied
            if locations[location_to_check].or_requirements and req_success:
                or_success = True

        if locations[location_to_check].or_requirements:
            # Return false if or requirements not met
            if not or_success:
                return False

        # Check number of missions
        if missions_complete >= locations[location_to_check].number:
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


if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
