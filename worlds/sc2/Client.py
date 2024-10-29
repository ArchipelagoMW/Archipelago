from __future__ import annotations

import asyncio
import copy
import ctypes
import enum
import inspect
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
import concurrent.futures
from pathlib import Path

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from Utils import init_logging, is_windows, async_start
from . import ItemNames, Options
from .ItemGroups import item_name_groups
from .Options import (
    MissionOrder, KerriganPrimalStatus, kerrigan_unit_available, KerriganPresence,
    GameSpeed, GenericUpgradeItems, GenericUpgradeResearch, ColorChoice, GenericUpgradeMissions,
    LocationInclusion, ExtraLocations, MasteryLocations, ChallengeLocations, VanillaLocations,
    DisableForcedCamera, SkipCutscenes, GrantStoryTech, GrantStoryLevels, TakeOverAIAllies, RequiredTactics,
    SpearOfAdunPresence, SpearOfAdunPresentInNoBuild, SpearOfAdunAutonomouslyCastAbilityPresence,
    SpearOfAdunAutonomouslyCastPresentInNoBuild
)


if __name__ == "__main__":
    init_logging("SC2Client", exception_logger="Client")

logger = logging.getLogger("Client")
sc2_logger = logging.getLogger("Starcraft2")

import nest_asyncio
from worlds._sc2common import bot
from worlds._sc2common.bot.data import Race
from worlds._sc2common.bot.main import run_game
from worlds._sc2common.bot.player import Bot
from .Items import (lookup_id_to_name, get_full_item_list, ItemData, type_flaggroups, upgrade_numbers,
                    upgrade_numbers_all)
from .Locations import SC2WOL_LOC_ID_OFFSET, LocationType, SC2HOTS_LOC_ID_OFFSET
from .MissionTables import (lookup_id_to_mission, SC2Campaign, lookup_name_to_mission,
                            lookup_id_to_campaign, MissionConnection, SC2Mission, campaign_mission_table, SC2Race)
from .Regions import MissionInfo

import colorama
from Options import Option
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes
from MultiServer import mark_raw

pool = concurrent.futures.ThreadPoolExecutor(1)
loop = asyncio.get_event_loop_policy().new_event_loop()
nest_asyncio.apply(loop)
MAX_BONUS: int = 28
VICTORY_MODULO: int = 100

# GitHub repo where the Map/mod data is hosted for /download_data command
DATA_REPO_OWNER = "Ziktofel"
DATA_REPO_NAME = "Archipelago-SC2-data"
DATA_API_VERSION = "API3"

# Bot controller
CONTROLLER_HEALTH: int = 38281
CONTROLLER2_HEALTH: int = 38282

# Games
STARCRAFT2 = "Starcraft 2"
STARCRAFT2_WOL = "Starcraft 2 Wings of Liberty"


# Data version file path.
# This file is used to tell if the downloaded data are outdated
# Associated with /download_data command
def get_metadata_file() -> str:
    return os.environ["SC2PATH"] + os.sep + "ArchipelagoSC2Metadata.txt"


class ConfigurableOptionType(enum.Enum):
    INTEGER = enum.auto()
    ENUM = enum.auto()

class ConfigurableOptionInfo(typing.NamedTuple):
    name: str
    variable_name: str
    option_class: typing.Type[Option]
    option_type: ConfigurableOptionType = ConfigurableOptionType.ENUM
    can_break_logic: bool = False


class ColouredMessage:
    def __init__(self, text: str = '', *, keep_markup: bool = False) -> None:
        self.parts: typing.List[dict] = []
        if text:
            self(text, keep_markup=keep_markup)
    def __call__(self, text: str, *, keep_markup: bool = False) -> 'ColouredMessage':
        add_json_text(self.parts, text, keep_markup=keep_markup)
        return self
    def coloured(self, text: str, colour: str) -> 'ColouredMessage':
        add_json_text(self.parts, text, type="color", color=colour)
        return self
    def location(self, location_id: int, player_id: int) -> 'ColouredMessage':
        add_json_location(self.parts, location_id, player_id)
        return self
    def item(self, item_id: int, player_id: int, flags: int = 0) -> 'ColouredMessage':
        add_json_item(self.parts, item_id, player_id, flags)
        return self
    def player(self, player_id: int) -> 'ColouredMessage':
        add_json_text(self.parts, str(player_id), type=JSONTypes.player_id)
        return self
    def send(self, ctx: SC2Context) -> None:
        ctx.on_print_json({"data": self.parts, "cmd": "PrintJSON"})


class StarcraftClientProcessor(ClientCommandProcessor):
    ctx: SC2Context

    def formatted_print(self, text: str) -> None:
        """Prints with kivy formatting to the GUI, and also prints to command-line and to all logs"""
        # Note(mm): Bold/underline can help readability, but unfortunately the CommonClient does not filter bold tags from command-line output.
        # Regardless, using `on_print_json` to get formatted text in the GUI and output in the command-line and in the logs,
        # without having to branch code from CommonClient
        self.ctx.on_print_json({"data": [{"text": text, "keep_markup": True}]})

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
    
    @mark_raw
    def _cmd_received(self, filter_search: str = "") -> bool:
        """List received items.
        Pass in a parameter to filter the search by partial item name or exact item group."""
        # Groups must be matched case-sensitively, so we properly capitalize the search term
        # eg. "Spear of Adun" over "Spear Of Adun" or "spear of adun"
        # This fails a lot of item name matches, but those should be found by partial name match
        formatted_filter_search = " ".join([(part.lower() if len(part) <= 3 else part.lower().capitalize()) for part in filter_search.split()])

        def item_matches_filter(item_name: str) -> bool:
            # The filter can be an exact group name or a partial item name
            # Partial item name can be matched case-insensitively
            if filter_search.lower() in item_name.lower():
                return True
            # The search term should already be formatted as a group name
            if formatted_filter_search in item_name_groups and item_name in item_name_groups[formatted_filter_search]:
                return True
            return False

        items = get_full_item_list()
        categorized_items: typing.Dict[SC2Race, typing.List[int]] = {}
        parent_to_child: typing.Dict[int, typing.List[int]] = {}
        items_received: typing.Dict[int, typing.List[NetworkItem]] = {}
        filter_match_count = 0
        for item in self.ctx.items_received:
            items_received.setdefault(item.item, []).append(item)
        items_received_set = set(items_received)
        for item_data in items.values():
            if item_data.parent_item:
                parent_to_child.setdefault(items[item_data.parent_item].code, []).append(item_data.code)
            else:
                categorized_items.setdefault(item_data.race, []).append(item_data.code)
        for faction in SC2Race:
            has_printed_faction_title = False
            def print_faction_title():
                if not has_printed_faction_title:
                    self.formatted_print(f" [u]{faction.name}[/u] ")
            
            for item_id in categorized_items[faction]:
                item_name = self.ctx.item_names.lookup_in_game(item_id)
                received_child_items = items_received_set.intersection(parent_to_child.get(item_id, []))
                matching_children = [child for child in received_child_items
                                     if item_matches_filter(self.ctx.item_names.lookup_in_game(child))]
                received_items_of_this_type = items_received.get(item_id, [])
                item_is_match = item_matches_filter(item_name)
                if item_is_match or len(matching_children) > 0:
                    # Print found item if it or its children match the filter
                    if item_is_match:
                        filter_match_count += len(received_items_of_this_type)
                    for item in received_items_of_this_type:
                        print_faction_title()
                        has_printed_faction_title = True
                        (ColouredMessage('* ').item(item.item, self.ctx.slot, flags=item.flags)
                            (" from ").location(item.location, item.player)
                            (" by ").player(item.player)
                        ).send(self.ctx)
                
                if received_child_items:
                    # We have this item's children
                    if len(matching_children) == 0:
                        # ...but none of them match the filter
                        continue

                    if not received_items_of_this_type:
                        # We didn't receive the item itself
                        print_faction_title()
                        has_printed_faction_title = True
                        ColouredMessage("- ").coloured(item_name, "black")(" - not obtained").send(self.ctx)
                    
                    for child_item in matching_children:
                        received_items_of_this_type = items_received.get(child_item, [])
                        for item in received_items_of_this_type:
                            filter_match_count += len(received_items_of_this_type)
                            (ColouredMessage('  * ').item(item.item, self.ctx.slot, flags=item.flags)
                                (" from ").location(item.location, item.player)
                                (" by ").player(item.player)
                            ).send(self.ctx)
                    
                    non_matching_children = len(received_child_items) - len(matching_children)
                    if non_matching_children > 0:
                        self.formatted_print(f"  + {non_matching_children} child items that don't match the filter")
        if filter_search == "":
            self.formatted_print(f"[b]Obtained: {len(self.ctx.items_received)} items[/b]")
        else:
            self.formatted_print(f"[b]Filter \"{filter_search}\" found {filter_match_count} out of {len(self.ctx.items_received)} obtained items[/b]")
        return True
    
    def _cmd_option(self, option_name: str = "", option_value: str = "") -> None:
        """Sets a Starcraft game option that can be changed after generation. Use "/option list" to see all options."""

        LOGIC_WARNING = f"  *Note changing this may result in logically unbeatable games*\n"

        options = (
            ConfigurableOptionInfo('kerrigan_presence', 'kerrigan_presence', Options.KerriganPresence, can_break_logic=True),
            ConfigurableOptionInfo('soa_presence', 'spear_of_adun_presence', Options.SpearOfAdunPresence, can_break_logic=True),
            ConfigurableOptionInfo('soa_in_nobuilds', 'spear_of_adun_present_in_no_build', Options.SpearOfAdunPresentInNoBuild, can_break_logic=True),
            ConfigurableOptionInfo('control_ally', 'take_over_ai_allies', Options.TakeOverAIAllies, can_break_logic=True),
            ConfigurableOptionInfo('minerals_per_item', 'minerals_per_item', Options.MineralsPerItem, ConfigurableOptionType.INTEGER),
            ConfigurableOptionInfo('gas_per_item', 'vespene_per_item', Options.VespenePerItem, ConfigurableOptionType.INTEGER),
            ConfigurableOptionInfo('supply_per_item', 'starting_supply_per_item', Options.StartingSupplyPerItem, ConfigurableOptionType.INTEGER),
            ConfigurableOptionInfo('no_forced_camera', 'disable_forced_camera', Options.DisableForcedCamera),
            ConfigurableOptionInfo('skip_cutscenes', 'skip_cutscenes', Options.SkipCutscenes),
        )

        WARNING_COLOUR = "salmon"
        CMD_COLOUR = "slateblue"
        boolean_option_map = {
            'y': 'true', 'yes': 'true', 'n': 'false', 'no': 'false',
        }

        help_message = ColouredMessage(inspect.cleandoc("""
            Options
        --------------------
        """))('\n')
        for option in options:
            option_help_text = inspect.cleandoc(option.option_class.__doc__ or "No description provided.").split('\n', 1)[0]
            help_message.coloured(option.name, CMD_COLOUR)(": " + " | ".join(option.option_class.options)
                + f" -- {option_help_text}\n")
            if option.can_break_logic:
                help_message.coloured(LOGIC_WARNING, WARNING_COLOUR)
        help_message("--------------------\nEnter an option without arguments to see its current value.\n")

        if not option_name or option_name == 'list' or option_name == 'help':
            help_message.send(self.ctx)
            return
        for option in options:
            if option_name == option.name:
                option_value = boolean_option_map.get(option_value, option_value)
                if not option_value:
                    pass
                elif option.option_type == ConfigurableOptionType.ENUM and option_value in option.option_class.options:
                    self.ctx.__dict__[option.variable_name] = option.option_class.options[option_value]
                elif option.option_type == ConfigurableOptionType.INTEGER:
                    try:
                        self.ctx.__dict__[option.variable_name] = int(option_value, base=0)
                    except:
                        self.output(f"{option_value} is not a valid integer")
                else:
                    self.output(f"Unknown option value '{option_value}'")
                ColouredMessage(f"{option.name} is '{option.option_class.get_option_name(self.ctx.__dict__[option.variable_name])}'").send(self.ctx)
                break
        else:
            self.output(f"Unknown option '{option_name}'")
            help_message.send(self.ctx)

    def _cmd_color(self, faction: str = "", color: str = "") -> None:
        """Changes the player color for a given faction."""
        player_colors = [
            "White", "Red", "Blue", "Teal",
            "Purple", "Yellow", "Orange", "Green",
            "LightPink", "Violet", "LightGrey", "DarkGreen",
            "Brown", "LightGreen", "DarkGrey", "Pink",
            "Rainbow", "Random", "Default"
        ]
        var_names = {
            'raynor': 'player_color_raynor',
            'kerrigan': 'player_color_zerg',
            'primal': 'player_color_zerg_primal',
            'protoss': 'player_color_protoss',
            'nova': 'player_color_nova',
        }
        faction = faction.lower()
        if not faction:
            for faction_name, key in var_names.items():
                self.output(f"Current player color for {faction_name}: {player_colors[self.ctx.__dict__[key]]}")
            self.output("To change your color, add the faction name and color after the command.")
            self.output("Available factions: " + ', '.join(var_names))
            self.output("Available colors: " + ', '.join(player_colors))
            return
        elif faction not in var_names:
            self.output(f"Unknown faction '{faction}'.")
            self.output("Available factions: " + ', '.join(var_names))
            return
        match_colors = [player_color.lower() for player_color in player_colors]
        if not color:
            self.output(f"Current player color for {faction}: {player_colors[self.ctx.__dict__[var_names[faction]]]}")
            self.output("To change this faction's colors, add the name of the color after the command.")
            self.output("Available colors: " + ', '.join(player_colors))
        else:
            if color.lower() not in match_colors:
                self.output(color + " is not a valid color.  Available colors: " + ', '.join(player_colors))
                return
            if color.lower() == "random":
                color = random.choice(player_colors[:16])
            self.ctx.__dict__[var_names[faction]] = match_colors.index(color.lower())
            self.ctx.pending_color_update = True
            self.output(f"Color for {faction} set to " + player_colors[self.ctx.__dict__[var_names[faction]]])

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
        pool.submit(self._download_data)
        return True

    @staticmethod
    def _download_data() -> bool:
        if "SC2PATH" not in os.environ:
            check_game_install_path()

        if os.path.exists(get_metadata_file()):
            with open(get_metadata_file(), "r") as f:
                metadata = f.read()
        else:
            metadata = None

        tempzip, metadata = download_latest_release_zip(
            DATA_REPO_OWNER, DATA_REPO_NAME, DATA_API_VERSION, metadata=metadata, force_download=True)

        if tempzip:
            try:
                zipfile.ZipFile(tempzip).extractall(path=os.environ["SC2PATH"])
                sc2_logger.info(f"Download complete. Package installed.")
                if metadata is not None:
                    with open(get_metadata_file(), "w") as f:
                        f.write(metadata)
            finally:
                os.remove(tempzip)
        else:
            sc2_logger.warning("Download aborted/failed. Read the log for more information.")
            return False
        return True


class SC2JSONtoTextParser(JSONtoTextParser):
    def __init__(self, ctx) -> None:
        self.handlers = {
            "ItemSend": self._handle_color,
            "ItemCheat": self._handle_color,
            "Hint": self._handle_color,
        }
        super().__init__(ctx)

    def _handle_color(self, node: JSONMessagePart) -> str:
        codes = node["color"].split(";")
        buffer = "".join(self.color_code(code) for code in codes if code in self.color_codes)
        return buffer + self._handle_text(node) + '</c>'

    def color_code(self, code: str) -> str:
        return '<c val="' + self.color_codes[code] + '">'


class SC2Context(CommonContext):
    command_processor = StarcraftClientProcessor
    game = STARCRAFT2
    items_handling = 0b111

    def __init__(self, *args, **kwargs) -> None:
        super(SC2Context, self).__init__(*args, **kwargs)
        self.raw_text_parser = SC2JSONtoTextParser(self)

        self.difficulty = -1
        self.game_speed = -1
        self.disable_forced_camera = 0
        self.skip_cutscenes = 0
        self.all_in_choice = 0
        self.mission_order = 0
        self.player_color_raynor = ColorChoice.option_blue
        self.player_color_zerg = ColorChoice.option_orange
        self.player_color_zerg_primal = ColorChoice.option_purple
        self.player_color_protoss = ColorChoice.option_blue
        self.player_color_nova = ColorChoice.option_dark_grey
        self.pending_color_update = False
        self.kerrigan_presence = 0
        self.kerrigan_primal_status = 0
        self.levels_per_check = 0
        self.checks_per_level = 1
        self.mission_req_table: typing.Dict[SC2Campaign, typing.Dict[str, MissionInfo]] = {}
        self.final_mission: int = 29
        self.announcements: queue.Queue = queue.Queue()
        self.sc2_run_task: typing.Optional[asyncio.Task] = None
        self.missions_unlocked: bool = False  # allow launching missions ignoring requirements
        self.generic_upgrade_missions = 0
        self.generic_upgrade_research = 0
        self.generic_upgrade_items = 0
        self.location_inclusions: typing.Dict[LocationType, int] = {}
        self.plando_locations: typing.List[str] = []
        self.current_tooltip = None
        self.last_loc_list = None
        self.difficulty_override = -1
        self.game_speed_override = -1
        self.mission_id_to_location_ids: typing.Dict[int, typing.List[int]] = {}
        self.last_bot: typing.Optional[ArchipelagoBot] = None
        self.slot_data_version = 2
        self.grant_story_tech = 0
        self.required_tactics = RequiredTactics.option_standard
        self.take_over_ai_allies = TakeOverAIAllies.option_false
        self.spear_of_adun_presence = SpearOfAdunPresence.option_not_present
        self.spear_of_adun_present_in_no_build = SpearOfAdunPresentInNoBuild.option_false
        self.spear_of_adun_autonomously_cast_ability_presence = SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present
        self.spear_of_adun_autonomously_cast_present_in_no_build = SpearOfAdunAutonomouslyCastPresentInNoBuild.option_false
        self.minerals_per_item = 15
        self.vespene_per_item = 15
        self.starting_supply_per_item = 2
        self.nova_covert_ops_only = False
        self.kerrigan_levels_per_mission_completed = 0

    async def server_auth(self, password_requested: bool = False) -> None:
        self.game = STARCRAFT2
        if password_requested and not self.password:
            await super(SC2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
        if self.ui:
            self.ui.first_check = True

    def is_legacy_game(self):
        return self.game == STARCRAFT2_WOL

    def event_invalid_game(self):
        if self.is_legacy_game():
            self.game = STARCRAFT2
            super().event_invalid_game()
        else:
            self.game = STARCRAFT2_WOL
            async_start(self.send_connect())

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.difficulty = args["slot_data"]["game_difficulty"]
            self.game_speed = args["slot_data"].get("game_speed", GameSpeed.option_default)
            self.disable_forced_camera = args["slot_data"].get("disable_forced_camera", DisableForcedCamera.default)
            self.skip_cutscenes = args["slot_data"].get("skip_cutscenes", SkipCutscenes.default)
            self.all_in_choice = args["slot_data"]["all_in_map"]
            self.slot_data_version = args["slot_data"].get("version", 2)
            slot_req_table: dict = args["slot_data"]["mission_req"]

            first_item = list(slot_req_table.keys())[0]
            # Maintaining backwards compatibility with older slot data
            if first_item in [str(campaign.id) for campaign in SC2Campaign]:
                # Multi-campaign
                self.mission_req_table = {}
                for campaign_id in slot_req_table:
                    campaign = lookup_id_to_campaign[int(campaign_id)]
                    self.mission_req_table[campaign] = {
                        mission: self.parse_mission_info(mission_info)
                        for mission, mission_info in slot_req_table[campaign_id].items()
                    }
            else:
                # Old format
                self.mission_req_table = {SC2Campaign.GLOBAL: {
                        mission: self.parse_mission_info(mission_info)
                        for mission, mission_info in slot_req_table.items()
                    }
                }

            self.mission_order = args["slot_data"].get("mission_order", MissionOrder.option_vanilla)
            self.final_mission = args["slot_data"].get("final_mission", SC2Mission.ALL_IN.id)
            self.player_color_raynor = args["slot_data"].get("player_color_terran_raynor", ColorChoice.option_blue)
            self.player_color_zerg = args["slot_data"].get("player_color_zerg", ColorChoice.option_orange)
            self.player_color_zerg_primal = args["slot_data"].get("player_color_zerg_primal", ColorChoice.option_purple)
            self.player_color_protoss = args["slot_data"].get("player_color_protoss", ColorChoice.option_blue)
            self.player_color_nova = args["slot_data"].get("player_color_nova", ColorChoice.option_dark_grey)
            self.generic_upgrade_missions = args["slot_data"].get("generic_upgrade_missions", GenericUpgradeMissions.default)
            self.generic_upgrade_items = args["slot_data"].get("generic_upgrade_items", GenericUpgradeItems.option_individual_items)
            self.generic_upgrade_research = args["slot_data"].get("generic_upgrade_research", GenericUpgradeResearch.option_vanilla)
            self.kerrigan_presence = args["slot_data"].get("kerrigan_presence", KerriganPresence.option_vanilla)
            self.kerrigan_primal_status = args["slot_data"].get("kerrigan_primal_status", KerriganPrimalStatus.option_vanilla)
            self.kerrigan_levels_per_mission_completed = args["slot_data"].get("kerrigan_levels_per_mission_completed", 0)
            self.kerrigan_levels_per_mission_completed_cap = args["slot_data"].get("kerrigan_levels_per_mission_completed_cap", -1)
            self.kerrigan_total_level_cap = args["slot_data"].get("kerrigan_total_level_cap", -1)
            self.grant_story_tech = args["slot_data"].get("grant_story_tech", GrantStoryTech.option_false)
            self.grant_story_levels = args["slot_data"].get("grant_story_levels", GrantStoryLevels.option_additive)
            self.required_tactics = args["slot_data"].get("required_tactics", RequiredTactics.option_standard)
            self.take_over_ai_allies = args["slot_data"].get("take_over_ai_allies", TakeOverAIAllies.option_false)
            self.spear_of_adun_presence = args["slot_data"].get("spear_of_adun_presence", SpearOfAdunPresence.option_not_present)
            self.spear_of_adun_present_in_no_build = args["slot_data"].get("spear_of_adun_present_in_no_build", SpearOfAdunPresentInNoBuild.option_false)
            self.spear_of_adun_autonomously_cast_ability_presence = args["slot_data"].get("spear_of_adun_autonomously_cast_ability_presence", SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present)
            self.spear_of_adun_autonomously_cast_present_in_no_build = args["slot_data"].get("spear_of_adun_autonomously_cast_present_in_no_build", SpearOfAdunAutonomouslyCastPresentInNoBuild.option_false)
            self.minerals_per_item = args["slot_data"].get("minerals_per_item", 15)
            self.vespene_per_item = args["slot_data"].get("vespene_per_item", 15)
            self.starting_supply_per_item = args["slot_data"].get("starting_supply_per_item", 2)
            self.nova_covert_ops_only = args["slot_data"].get("nova_covert_ops_only", False)

            if self.required_tactics == RequiredTactics.option_no_logic:
                # Locking Grant Story Tech/Levels if no logic
                self.grant_story_tech = GrantStoryTech.option_true
                self.grant_story_levels = GrantStoryLevels.option_minimum

            self.location_inclusions = {
                LocationType.VICTORY: LocationInclusion.option_enabled, # Victory checks are always enabled
                LocationType.VANILLA: args["slot_data"].get("vanilla_locations", VanillaLocations.default),
                LocationType.EXTRA: args["slot_data"].get("extra_locations", ExtraLocations.default),
                LocationType.CHALLENGE: args["slot_data"].get("challenge_locations", ChallengeLocations.default),
                LocationType.MASTERY: args["slot_data"].get("mastery_locations", MasteryLocations.default),
            }
            self.plando_locations = args["slot_data"].get("plando_locations", [])

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

    @staticmethod
    def parse_mission_info(mission_info: dict[str, typing.Any]) -> MissionInfo:
        if mission_info.get("id") is not None:
            mission_info["mission"] = lookup_id_to_mission[mission_info["id"]]
        elif isinstance(mission_info["mission"], int):
            mission_info["mission"] = lookup_id_to_mission[mission_info["mission"]]

        return MissionInfo(
            **{field: value for field, value in mission_info.items() if field in MissionInfo._fields}
        )

    def find_campaign(self, mission_name: str) -> SC2Campaign:
        data = self.mission_req_table
        for campaign in data.keys():
            if mission_name in data[campaign].keys():
                return campaign
        sc2_logger.info(f"Attempted to find campaign of unknown mission '{mission_name}'; defaulting to GLOBAL")
        return SC2Campaign.GLOBAL



    def on_print_json(self, args: dict) -> None:
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

    def run_gui(self) -> None:
        from .ClientGui import start_gui
        start_gui(self)


    async def shutdown(self) -> None:
        await super(SC2Context, self).shutdown()
        if self.last_bot:
            self.last_bot.want_close = True
        if self.sc2_run_task:
            self.sc2_run_task.cancel()

    def play_mission(self, mission_id: int) -> bool:
        if self.missions_unlocked or is_mission_available(self, mission_id):
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
                f"{lookup_id_to_mission[mission_id].mission_name} is not currently unlocked.  "
                f"Use /unfinished or /available to see what is available.")
            return False

    def build_location_to_mission_mapping(self) -> None:
        mission_id_to_location_ids: typing.Dict[int, typing.Set[int]] = {
            mission_info.mission.id: set() for campaign_mission in self.mission_req_table.values() for mission_info in campaign_mission.values()
        }

        for loc in self.server_locations:
            offset = SC2WOL_LOC_ID_OFFSET if loc < SC2HOTS_LOC_ID_OFFSET \
                else (SC2HOTS_LOC_ID_OFFSET - SC2Mission.ALL_IN.id * VICTORY_MODULO)
            mission_id, objective = divmod(loc - offset, VICTORY_MODULO)
            mission_id_to_location_ids[mission_id].add(objective)
        self.mission_id_to_location_ids = {mission_id: sorted(objectives) for mission_id, objectives in
                                           mission_id_to_location_ids.items()}

    def locations_for_mission(self, mission_name: str):
        mission = lookup_name_to_mission[mission_name]
        mission_id: int = mission.id
        objectives = self.mission_id_to_location_ids[mission_id]
        for objective in objectives:
            yield get_location_offset(mission_id) + mission_id * VICTORY_MODULO + objective


class CompatItemHolder(typing.NamedTuple):
    name: str
    quantity: int = 1


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

# These items must be given to the player if the game is generated on version 2
API2_TO_API3_COMPAT_ITEMS: typing.Set[CompatItemHolder] = {
    CompatItemHolder(ItemNames.PHOTON_CANNON),
    CompatItemHolder(ItemNames.OBSERVER),
    CompatItemHolder(ItemNames.WARP_HARMONIZATION),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON, 3),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR, 3),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_SHIELDS, 3),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON, 3),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR, 3),
    CompatItemHolder(ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE, 3)
}


def compat_item_to_network_items(compat_item: CompatItemHolder) -> typing.List[NetworkItem]:
    item_id = get_full_item_list()[compat_item.name].code
    network_item = NetworkItem(item_id, 0, 0, 0)
    return compat_item.quantity * [network_item]


def calculate_items(ctx: SC2Context) -> typing.Dict[SC2Race, typing.List[int]]:
    items = ctx.items_received.copy()
    # Items unlocked in API2 by default (Prophecy default items)
    if ctx.slot_data_version < 3:
        for compat_item in API2_TO_API3_COMPAT_ITEMS:
            items.extend(compat_item_to_network_items(compat_item))

    network_item: NetworkItem
    accumulators: typing.Dict[SC2Race, typing.List[int]] = {race: [0 for _ in type_flaggroups[race]] for race in SC2Race}

    # Protoss Shield grouped item specific logic
    shields_from_ground_upgrade: int = 0
    shields_from_air_upgrade: int = 0

    item_list = get_full_item_list()
    for network_item in items:
        name: str = lookup_id_to_name[network_item.item]
        item_data: ItemData = item_list[name]

        # exists exactly once
        if item_data.quantity == 1:
            accumulators[item_data.race][type_flaggroups[item_data.race][item_data.type]] |= 1 << item_data.number

        # exists multiple times
        elif item_data.type in ["Upgrade", "Progressive Upgrade","Progressive Upgrade 2"]:
            flaggroup = type_flaggroups[item_data.race][item_data.type]

            # Generic upgrades apply only to Weapon / Armor upgrades
            if item_data.type != "Upgrade" or ctx.generic_upgrade_items == 0:
                accumulators[item_data.race][flaggroup] += 1 << item_data.number
            else:
                if name == ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE:
                    shields_from_ground_upgrade += 1
                if name == ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE:
                    shields_from_air_upgrade += 1
                for bundled_number in upgrade_numbers[item_data.number]:
                    accumulators[item_data.race][flaggroup] += 1 << bundled_number

            # Regen bio-steel nerf with API3 - undo for older games
            if ctx.slot_data_version < 3 and name == ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL:
                current_level = (accumulators[item_data.race][flaggroup] >> item_data.number) % 4
                if current_level == 2:
                    # Switch from level 2 to level 3 for compatibility
                    accumulators[item_data.race][flaggroup] += 1 << item_data.number
        # sum
        else:
            if name == ItemNames.STARTING_MINERALS:
                accumulators[item_data.race][type_flaggroups[item_data.race][item_data.type]] += ctx.minerals_per_item
            elif name == ItemNames.STARTING_VESPENE:
                accumulators[item_data.race][type_flaggroups[item_data.race][item_data.type]] += ctx.vespene_per_item
            elif name == ItemNames.STARTING_SUPPLY:
                accumulators[item_data.race][type_flaggroups[item_data.race][item_data.type]] += ctx.starting_supply_per_item
            else:
                accumulators[item_data.race][type_flaggroups[item_data.race][item_data.type]] += item_data.number

    # Fix Shields from generic upgrades by unit class (Maximum of ground/air upgrades)
    if shields_from_ground_upgrade > 0 or shields_from_air_upgrade > 0:
        shield_upgrade_level = max(shields_from_ground_upgrade, shields_from_air_upgrade)
        shield_upgrade_item = item_list[ItemNames.PROGRESSIVE_PROTOSS_SHIELDS]
        for _ in range(0, shield_upgrade_level):
            accumulators[shield_upgrade_item.race][type_flaggroups[shield_upgrade_item.race][shield_upgrade_item.type]] += 1 << shield_upgrade_item.number

    # Kerrigan levels per check
    accumulators[SC2Race.ZERG][type_flaggroups[SC2Race.ZERG]["Level"]] += (len(ctx.checked_locations) // ctx.checks_per_level) * ctx.levels_per_check

    # Upgrades from completed missions
    if ctx.generic_upgrade_missions > 0:
        total_missions = sum(len(ctx.mission_req_table[campaign]) for campaign in ctx.mission_req_table)
        for race in SC2Race:
            if "Upgrade" not in type_flaggroups[race]:
                continue
            upgrade_flaggroup = type_flaggroups[race]["Upgrade"]
            num_missions = ctx.generic_upgrade_missions * total_missions
            amounts = [
                num_missions // 100,
                2 * num_missions // 100,
                3 * num_missions // 100
            ]
            upgrade_count = 0
            completed = len([id for id in ctx.mission_id_to_location_ids if get_location_offset(id) + VICTORY_MODULO * id in ctx.checked_locations])
            for amount in amounts:
                if completed >= amount:
                    upgrade_count += 1
            # Equivalent to "Progressive Weapon/Armor Upgrade" item
            for bundled_number in upgrade_numbers[upgrade_numbers_all[race]]:
                accumulators[race][upgrade_flaggroup] += upgrade_count << bundled_number

    return accumulators


def calc_difficulty(difficulty: int):
    if difficulty == 0:
        return 'C'
    elif difficulty == 1:
        return 'N'
    elif difficulty == 2:
        return 'H'
    elif difficulty == 3:
        return 'B'

    return 'X'


def get_kerrigan_level(ctx: SC2Context, items: typing.Dict[SC2Race, typing.List[int]], missions_beaten: int) -> int:
    item_value = items[SC2Race.ZERG][type_flaggroups[SC2Race.ZERG]["Level"]]
    mission_value = missions_beaten * ctx.kerrigan_levels_per_mission_completed
    if ctx.kerrigan_levels_per_mission_completed_cap != -1:
        mission_value = min(mission_value, ctx.kerrigan_levels_per_mission_completed_cap)
    total_value = item_value + mission_value
    if ctx.kerrigan_total_level_cap != -1:
        total_value = min(total_value, ctx.kerrigan_total_level_cap)
    return total_value


def calculate_kerrigan_options(ctx: SC2Context) -> int:
    options = 0

    # Bits 0, 1
    # Kerrigan unit available
    if ctx.kerrigan_presence in kerrigan_unit_available:
        options |= 1 << 0

    # Bit 2
    # Kerrigan primal status by map
    if ctx.kerrigan_primal_status == KerriganPrimalStatus.option_vanilla:
        options |= 1 << 2

    return options


def caclulate_soa_options(ctx: SC2Context) -> int:
    options = 0

    # Bits 0, 1
    # SoA Calldowns available
    soa_presence_value = 0
    if ctx.spear_of_adun_presence == SpearOfAdunPresence.option_not_present:
        soa_presence_value = 0
    elif ctx.spear_of_adun_presence == SpearOfAdunPresence.option_lotv_protoss:
        soa_presence_value = 1
    elif ctx.spear_of_adun_presence == SpearOfAdunPresence.option_protoss:
        soa_presence_value = 2
    elif ctx.spear_of_adun_presence == SpearOfAdunPresence.option_everywhere:
        soa_presence_value = 3
    options |= soa_presence_value << 0

    # Bit 2
    # SoA Calldowns for no-builds
    if ctx.spear_of_adun_present_in_no_build == SpearOfAdunPresentInNoBuild.option_true:
        options |= 1 << 2

    # Bits 3,4
    # Autocasts
    soa_autocasts_presence_value = 0
    if ctx.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_not_present:
        soa_autocasts_presence_value = 0
    elif ctx.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_lotv_protoss:
        soa_autocasts_presence_value = 1
    elif ctx.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_protoss:
        soa_autocasts_presence_value = 2
    elif ctx.spear_of_adun_autonomously_cast_ability_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_everywhere:
        soa_autocasts_presence_value = 3
    options |= soa_autocasts_presence_value << 3

    # Bit 5
    # Autocasts in no-builds
    if ctx.spear_of_adun_autonomously_cast_present_in_no_build == SpearOfAdunAutonomouslyCastPresentInNoBuild.option_true:
        options |= 1 << 5

    return options

def kerrigan_primal(ctx: SC2Context, kerrigan_level: int) -> bool:
    if ctx.kerrigan_primal_status == KerriganPrimalStatus.option_always_zerg:
        return True
    elif ctx.kerrigan_primal_status == KerriganPrimalStatus.option_always_human:
        return False
    elif ctx.kerrigan_primal_status == KerriganPrimalStatus.option_level_35:
        return kerrigan_level >= 35
    elif ctx.kerrigan_primal_status == KerriganPrimalStatus.option_half_completion:
        total_missions = len(ctx.mission_id_to_location_ids)
        completed = sum((mission_id * VICTORY_MODULO + get_location_offset(mission_id)) in ctx.checked_locations
                         for mission_id in ctx.mission_id_to_location_ids)
        return completed >= (total_missions / 2)
    elif ctx.kerrigan_primal_status == KerriganPrimalStatus.option_item:
        codes = [item.item for item in ctx.items_received]
        return get_full_item_list()[ItemNames.KERRIGAN_PRIMAL_FORM].code in codes
    return False

async def starcraft_launch(ctx: SC2Context, mission_id: int):
    sc2_logger.info(f"Launching {lookup_id_to_mission[mission_id].mission_name}. If game does not launch check log file for errors.")

    with DllDirectory(None):
        run_game(bot.maps.get(lookup_id_to_mission[mission_id].map_file), [Bot(Race.Terran, ArchipelagoBot(ctx, mission_id),
                                                                name="Archipelago", fullscreen=True)], realtime=True)


class ArchipelagoBot(bot.bot_ai.BotAI):
    __slots__ = [
        'game_running',
        'mission_completed',
        'boni',
        'setup_done',
        'ctx',
        'mission_id',
        'want_close',
        'can_read_game',
        'last_received_update',
    ]

    def __init__(self, ctx: SC2Context, mission_id: int):
        self.game_running = False
        self.mission_completed = False
        self.want_close = False
        self.can_read_game = False
        self.last_received_update: int = 0
        self.setup_done = False
        self.ctx = ctx
        self.ctx.last_bot = self
        self.mission_id = mission_id
        self.boni = [False for _ in range(MAX_BONUS)]

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
            missions_beaten = self.missions_beaten_count()
            kerrigan_level = get_kerrigan_level(self.ctx, start_items, missions_beaten)
            kerrigan_options = calculate_kerrigan_options(self.ctx)
            soa_options = caclulate_soa_options(self.ctx)
            if self.ctx.difficulty_override >= 0:
                difficulty = calc_difficulty(self.ctx.difficulty_override)
            else:
                difficulty = calc_difficulty(self.ctx.difficulty)
            if self.ctx.game_speed_override >= 0:
                game_speed = self.ctx.game_speed_override
            else:
                game_speed = self.ctx.game_speed
            await self.chat_send("?SetOptions {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
                difficulty,
                self.ctx.generic_upgrade_research,
                self.ctx.all_in_choice,
                game_speed,
                self.ctx.disable_forced_camera,
                self.ctx.skip_cutscenes,
                kerrigan_options,
                self.ctx.grant_story_tech,
                self.ctx.take_over_ai_allies,
                soa_options,
                self.ctx.mission_order,
                1 if self.ctx.nova_covert_ops_only else 0,
                self.ctx.grant_story_levels
            ))
            await self.chat_send("?GiveResources {} {} {}".format(
                start_items[SC2Race.ANY][0],
                start_items[SC2Race.ANY][1],
                start_items[SC2Race.ANY][2]
            ))
            await self.updateTerranTech(start_items)
            await self.updateZergTech(start_items, kerrigan_level)
            await self.updateProtossTech(start_items)
            await self.updateColors()
            await self.chat_send("?LoadFinished")
            self.last_received_update = len(self.ctx.items_received)

        else:
            if self.ctx.pending_color_update:
                await self.updateColors()

            if not self.ctx.announcements.empty():
                message = self.ctx.announcements.get(timeout=1)
                await self.chat_send("?SendMessage " + message)
                self.ctx.announcements.task_done()

            # Archipelago reads the health
            controller1_state = 0
            controller2_state = 0
            for unit in self.all_own_units():
                if unit.health_max == CONTROLLER_HEALTH:
                    controller1_state = int(CONTROLLER_HEALTH - unit.health)
                    self.can_read_game = True
                elif unit.health_max == CONTROLLER2_HEALTH:
                    controller2_state = int(CONTROLLER2_HEALTH - unit.health)
                    self.can_read_game = True
            game_state = controller1_state + (controller2_state << 15)

            if iteration == 160 and not game_state & 1:
                await self.chat_send("?SendMessage Warning: Archipelago unable to connect or has lost connection to " +
                                     "Starcraft 2 (This is likely a map issue)")

            if self.last_received_update < len(self.ctx.items_received):
                current_items = calculate_items(self.ctx)
                missions_beaten = self.missions_beaten_count()
                kerrigan_level = get_kerrigan_level(self.ctx, current_items, missions_beaten)
                await self.updateTerranTech(current_items)
                await self.updateZergTech(current_items, kerrigan_level)
                await self.updateProtossTech(current_items)
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
                                  "locations": [get_location_offset(self.mission_id) + VICTORY_MODULO * self.mission_id]}])
                            self.mission_completed = True
                        else:
                            print("Game Complete")
                            await self.ctx.send_msgs([{"cmd": 'StatusUpdate', "status": ClientStatus.CLIENT_GOAL}])
                            self.mission_completed = True

                    for x, completed in enumerate(self.boni):
                        if not completed and game_state & (1 << (x + 2)):
                            await self.ctx.send_msgs(
                                [{"cmd": 'LocationChecks',
                                  "locations": [get_location_offset(self.mission_id) + VICTORY_MODULO * self.mission_id + x + 1]}])
                            self.boni[x] = True
                else:
                    await self.chat_send("?SendMessage LostConnection - Lost connection to game.")

    def missions_beaten_count(self):
        return len([location for location in self.ctx.checked_locations if location % VICTORY_MODULO == 0])

    async def updateColors(self):
        await self.chat_send("?SetColor rr " + str(self.ctx.player_color_raynor))
        await self.chat_send("?SetColor ks " + str(self.ctx.player_color_zerg))
        await self.chat_send("?SetColor pz " + str(self.ctx.player_color_zerg_primal))
        await self.chat_send("?SetColor da " + str(self.ctx.player_color_protoss))
        await self.chat_send("?SetColor nova " + str(self.ctx.player_color_nova))
        self.ctx.pending_color_update = False

    async def updateTerranTech(self, current_items):
        terran_items = current_items[SC2Race.TERRAN]
        await self.chat_send("?GiveTerranTech {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
            terran_items[0], terran_items[1], terran_items[2], terran_items[3], terran_items[4],
            terran_items[5], terran_items[6], terran_items[7], terran_items[8], terran_items[9], terran_items[10],
            terran_items[11], terran_items[12], terran_items[13]))

    async def updateZergTech(self, current_items, kerrigan_level):
        zerg_items = current_items[SC2Race.ZERG]
        kerrigan_primal_by_items = kerrigan_primal(self.ctx, kerrigan_level)
        kerrigan_primal_bot_value = 1 if kerrigan_primal_by_items else 0
        await self.chat_send("?GiveZergTech {} {} {} {} {} {} {} {} {} {} {} {}".format(
            kerrigan_level, kerrigan_primal_bot_value, zerg_items[0], zerg_items[1], zerg_items[2],
            zerg_items[3], zerg_items[4], zerg_items[5], zerg_items[6], zerg_items[9], zerg_items[10], zerg_items[11]
        ))

    async def updateProtossTech(self, current_items):
        protoss_items = current_items[SC2Race.PROTOSS]
        await self.chat_send("?GiveProtossTech {} {} {} {} {} {} {} {} {} {}".format(
            protoss_items[0], protoss_items[1], protoss_items[2], protoss_items[3], protoss_items[4],
            protoss_items[5], protoss_items[6], protoss_items[7], protoss_items[8], protoss_items[9]
        ))


def request_unfinished_missions(ctx: SC2Context) -> None:
    if ctx.mission_req_table:
        message = "Unfinished Missions: "
        unlocks = initialize_blank_mission_dict(ctx.mission_req_table)
        unfinished_locations: typing.Dict[SC2Mission, typing.List[str]] = {}

        _, unfinished_missions = calc_unfinished_missions(ctx, unlocks=unlocks)

        for mission in unfinished_missions:
            objectives = set(ctx.locations_for_mission(mission))
            if objectives:
                remaining_objectives = objectives.difference(ctx.checked_locations)
                unfinished_locations[mission] = [ctx.location_names.lookup_in_game(location_id) for location_id in remaining_objectives]
            else:
                unfinished_locations[mission] = []

        # Removing All-In from location pool
        final_mission = lookup_id_to_mission[ctx.final_mission]
        if final_mission in unfinished_missions.keys():
            message = f"Final Mission Available: {final_mission}[{ctx.final_mission}]\n" + message
            if unfinished_missions[final_mission] == -1:
                unfinished_missions.pop(final_mission)

        message += ", ".join(f"{mark_up_mission_name(ctx, mission, unlocks)}[{ctx.mission_req_table[ctx.find_campaign(mission)][mission].mission.id}] " +
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


def calc_unfinished_missions(ctx: SC2Context, unlocks: typing.Optional[typing.Dict] = None):
    unfinished_missions: typing.List[str] = []
    locations_completed: typing.List[typing.Union[typing.Set[int], typing.Literal[-1]]] = []

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


def is_mission_available(ctx: SC2Context, mission_id_to_check: int) -> bool:
    unfinished_missions = calc_available_missions(ctx)

    return any(mission_id_to_check == ctx.mission_req_table[ctx.find_campaign(mission)][mission].mission.id for mission in unfinished_missions)


def mark_up_mission_name(ctx: SC2Context, mission_name: str, unlock_table: typing.Dict) -> str:
    """Checks if the mission is required for game completion and adds '*' to the name to mark that."""

    campaign = ctx.find_campaign(mission_name)
    mission_info = ctx.mission_req_table[campaign][mission_name]
    if mission_info.completion_critical:
        if ctx.ui:
            message = "[color=AF99EF]" + mission_name + "[/color]"
        else:
            message = "*" + mission_name + "*"
    else:
        message = mission_name

    if ctx.ui:
        campaign_missions = list(ctx.mission_req_table[campaign].keys())
        unlocks: typing.List[str]
        index = campaign_missions.index(mission_name)
        if index in unlock_table[campaign]:
            unlocks = unlock_table[campaign][index]
        else:
            unlocks = []

        if len(unlocks) > 0:
            pre_message = f"[ref={mission_info.mission.id}|Unlocks: "
            pre_message += ", ".join(f"{unlock}({ctx.mission_req_table[ctx.find_campaign(unlock)][unlock].mission.id})" for unlock in unlocks)
            pre_message += f"]"
            message = pre_message + message + "[/ref]"

    return message


def mark_up_objectives(message, ctx, unfinished_locations, mission):
    formatted_message = message

    if ctx.ui:
        locations = unfinished_locations[mission]
        campaign = ctx.find_campaign(mission)

        pre_message = f"[ref={list(ctx.mission_req_table[campaign]).index(mission) + 30}|"
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
                      f"[{ctx.mission_req_table[ctx.find_campaign(mission)][mission].mission.id}]"
                      for mission in missions)

        if ctx.ui:
            ctx.ui.log_panels['All'].on_message_markup(message)
            ctx.ui.log_panels['Starcraft2'].on_message_markup(message)
        else:
            sc2_logger.info(message)
    else:
        sc2_logger.warning("No mission table found, you are likely not connected to a server.")


def calc_available_missions(ctx: SC2Context, unlocks: typing.Optional[dict] = None) -> typing.List[str]:
    available_missions: typing.List[str] = []
    missions_complete = 0

    # Get number of missions completed
    for loc in ctx.checked_locations:
        if loc % VICTORY_MODULO == 0:
            missions_complete += 1

    for campaign in ctx.mission_req_table:
        # Go through the required missions for each mission and fill up unlock table used later for hover-over tooltips
        for mission_name in ctx.mission_req_table[campaign]:
            if unlocks:
                for unlock in ctx.mission_req_table[campaign][mission_name].required_world:
                    parsed_unlock = parse_unlock(unlock)
                    # TODO prophecy-only wants to connect to WoL here
                    index = parsed_unlock.connect_to - 1
                    unlock_mission = list(ctx.mission_req_table[parsed_unlock.campaign])[index]
                    unlock_campaign = ctx.find_campaign(unlock_mission)
                    if unlock_campaign in unlocks:
                        if index not in unlocks[unlock_campaign]:
                            unlocks[unlock_campaign][index] = list()
                        unlocks[unlock_campaign][index].append(mission_name)

            if mission_reqs_completed(ctx, mission_name, missions_complete):
                available_missions.append(mission_name)

    return available_missions


def parse_unlock(unlock: typing.Union[typing.Dict[typing.Literal["connect_to", "campaign"], int], MissionConnection, int]) -> MissionConnection:
    if isinstance(unlock, int):
        # Legacy
        return MissionConnection(unlock)
    elif isinstance(unlock, MissionConnection):
        return unlock
    else:
        # Multi-campaign
        return MissionConnection(unlock["connect_to"], lookup_id_to_campaign[unlock["campaign"]])


def mission_reqs_completed(ctx: SC2Context, mission_name: str, missions_complete: int) -> bool:
    """Returns a bool signifying if the mission has all requirements complete and can be done

    Arguments:
    ctx -- instance of SC2Context
    locations_to_check -- the mission string name to check
    missions_complete -- an int of how many missions have been completed
    mission_path -- a list of missions that have already been checked
    """
    campaign = ctx.find_campaign(mission_name)

    if len(ctx.mission_req_table[campaign][mission_name].required_world) >= 1:
        # A check for when the requirements are being or'd
        or_success = False

        # Loop through required missions
        for req_mission in ctx.mission_req_table[campaign][mission_name].required_world:
            req_success = True
            parsed_req_mission = parse_unlock(req_mission)

            # Check if required mission has been completed
            mission_id = ctx.mission_req_table[parsed_req_mission.campaign][
                list(ctx.mission_req_table[parsed_req_mission.campaign])[parsed_req_mission.connect_to - 1]].mission.id
            if not (mission_id * VICTORY_MODULO + get_location_offset(mission_id)) in ctx.checked_locations:
                if not ctx.mission_req_table[campaign][mission_name].or_requirements:
                    return False
                else:
                    req_success = False

            # Grid-specific logic (to avoid long path checks and infinite recursion)
            if ctx.mission_order in (MissionOrder.option_grid, MissionOrder.option_mini_grid, MissionOrder.option_medium_grid):
                if req_success:
                    return True
                else:
                    if parsed_req_mission == ctx.mission_req_table[campaign][mission_name].required_world[-1]:
                        return False
                    else:
                        continue

            # Recursively check required mission to see if it's requirements are met, in case !collect has been done
            # Skipping recursive check on Grid settings to speed up checks and avoid infinite recursion
            if not mission_reqs_completed(ctx, list(ctx.mission_req_table[parsed_req_mission.campaign])[parsed_req_mission.connect_to - 1], missions_complete):
                if not ctx.mission_req_table[campaign][mission_name].or_requirements:
                    return False
                else:
                    req_success = False

            # If requirement check succeeded mark or as satisfied
            if ctx.mission_req_table[campaign][mission_name].or_requirements and req_success:
                or_success = True

        if ctx.mission_req_table[campaign][mission_name].or_requirements:
            # Return false if or requirements not met
            if not or_success:
                return False

        # Check number of missions
        if missions_complete >= ctx.mission_req_table[campaign][mission_name].number:
            return True
        else:
            return False
    else:
        return True


def initialize_blank_mission_dict(location_table: typing.Dict[SC2Campaign, typing.Dict[str, MissionInfo]]):
    unlocks: typing.Dict[SC2Campaign, typing.Dict] = {}

    for mission in list(location_table):
        unlocks[mission] = {}

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
        documentspath: str = buf.value
        einfo = str(documentspath / Path("StarCraft II\\ExecuteInfo.txt"))
    else:
        einfo = str(bot.paths.get_home() / Path(bot.paths.USERPATH[bot.paths.PF]))

    # Check if the file exists.
    if os.path.isfile(einfo):

        # Open the file and read it, picking out the latest executable's path.
        with open(einfo) as f:
            content = f.read()
        if content:
            search_result = re.search(r" = (.*)Versions", content)
            if not search_result:
                sc2_logger.warning(f"Found {einfo}, but it was empty. Run SC2 through the Blizzard launcher, "
                                    "then try again.")
                return False
            base = search_result.group(1)

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
    sc2_path: str = os.environ["SC2PATH"]
    mapdir = sc2_path / Path('Maps/ArchipelagoCampaign')
    mods = ["ArchipelagoCore", "ArchipelagoPlayer", "ArchipelagoPlayerSuper", "ArchipelagoPatches",
            "ArchipelagoTriggers", "ArchipelagoPlayerWoL", "ArchipelagoPlayerHotS",
            "ArchipelagoPlayerLotV", "ArchipelagoPlayerLotVPrologue", "ArchipelagoPlayerNCO"]
    modfiles = [sc2_path / Path("Mods/" + mod + ".SC2Mod") for mod in mods]
    wol_required_maps: typing.List[str] = ["WoL" + os.sep + mission.map_file + ".SC2Map" for mission in SC2Mission
                         if mission.campaign in (SC2Campaign.WOL, SC2Campaign.PROPHECY)]
    hots_required_maps: typing.List[str] = ["HotS" + os.sep + mission.map_file + ".SC2Map" for mission in campaign_mission_table[SC2Campaign.HOTS]]
    lotv_required_maps: typing.List[str] = ["LotV" + os.sep + mission.map_file + ".SC2Map" for mission in SC2Mission
                                            if mission.campaign in (SC2Campaign.LOTV, SC2Campaign.PROLOGUE, SC2Campaign.EPILOGUE)]
    nco_required_maps: typing.List[str] = ["NCO" + os.sep + mission.map_file + ".SC2Map" for mission in campaign_mission_table[SC2Campaign.NCO]]
    required_maps = wol_required_maps + hots_required_maps + lotv_required_maps + nco_required_maps
    needs_files = False

    # Check for maps.
    missing_maps: typing.List[str] = []
    for mapfile in required_maps:
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


def download_latest_release_zip(
    owner: str,
    repo: str,
    api_version: str,
    metadata: typing.Optional[str] = None,
    force_download=False
) -> typing.Tuple[str, typing.Optional[str]]:
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


def cleanup_downloaded_metadata(medatada_json: dict) -> None:
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


def get_location_offset(mission_id):
    return SC2WOL_LOC_ID_OFFSET if mission_id <= SC2Mission.ALL_IN.id \
        else (SC2HOTS_LOC_ID_OFFSET - SC2Mission.ALL_IN.id * VICTORY_MODULO)


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
