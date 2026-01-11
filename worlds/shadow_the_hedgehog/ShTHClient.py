import asyncio
import math
import random
import struct
from datetime import datetime, timedelta
import time
import traceback
from typing import Any, Dict, Optional
from copy import deepcopy
import dolphin_memory_engine

import Utils
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from .Options import WeaponsanityHold
from . import Levels, Items, Locations, Utils as ShadowUtils, Weapons, Story, Objects, Names
from .Levels import *
from .Locations import GetStageInformation, GetAlignmentsForStage, \
    GetStageEnemysanityInformation, MissionClearLocations

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a ROM for Shadow The Hedgehog. Currently {1}. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Shadow The Hedgehog is running."
)

CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

SHADOW_THE_HEDGEHOG_GAME_ID = "GUPE8P"
SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED = "GUPR8P"
SHADOW_THE_HEDGEHOG_GAME_ID_SX = "GUPX8P"

valid_game_bytes = [
    bytes(SHADOW_THE_HEDGEHOG_GAME_ID, "utf-8"),
    bytes(SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED, "utf-8"),
    bytes(SHADOW_THE_HEDGEHOG_GAME_ID_SX, "utf-8")
]

SAVE_VALUE_CHECK = False

@dataclass
class CharacterAddress:
    name: str
    met_address: int

def GetGameAddress(ctx, base_address):
    if (base_address == GAME_ADDRESSES.FIRST_STORY_MODE_STAGE_ADDRESS and ctx.game_id ==
            bytes(SHADOW_THE_HEDGEHOG_GAME_ID_SX, "utf-8")):
        return GAME_ADDRESSES.FIRST_STORY_MODE_STAGE_ADDRESS_SX

    elif (base_address == GAME_ADDRESSES.FIRST_STORY_MODE_STAGE_ADDRESS and ctx.game_id ==
            bytes(SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED, "utf-8")):
        return GAME_ADDRESSES.FIRST_STORY_MODE_STAGE_ADDRESS_RELOADED

    return base_address


class GAME_ADDRESSES:
    STORY_MODE_COUNTER = 0x80576988
    westopolis_save_info_base_address = 0x80576BE0
    ADDRESS_ALIEN_COUNT = 0x8057FB54
    ADDRESS_SOLDIER_COUNT = 0x8057FB4C
    ADDRESS_EGG_COUNT = 0x8057FB50
    SAVE_DATA_LOADED = 0x805E326B
    CHECKPOINT_RESPAWN_ID = 0x80575FBF
    STAGE_MUSIC_NAME = 0x805813D0

    ADDRESS_MISSION_MANAGER = 0x80575EF8

    ADDRESS_LAST_STORY_OPTION = 0x80578020
    ADDRESS_WEAPONS_BYTES = 0x80578068
    ADDRESS_LAST_CUTSCENE = 0x805EF2A0
    ADDRESS_EXPERT_MODE_UNLOCK = 0x80578021
    CUTSCENE_BUFFER = 0x805F7A2A
    ADDRESS_MISSION_ALIGNMENT = 0x80575F1F

    DARK_GAUGE_ADDRESS = 0x805766D4
    HERO_GAUGE_ADDRESS = 0x805766C8
    RINGS_ADDRESS = 0x8057670C

    SPECIAL_WEAPONS_ADDRESS = 0x80578068
    SPECIAL_WEAPONS_ADDRESS_APPROVED = 0x80579FC4
    ADDRESS_LAST_STORY_APPROVED = 0x80579F7C
    CURRENT_WEAPON_ID_ADDRESS = 0x805766F8
    CURRENT_AMMO_ADDRESS = 0x80576700

    ADDRESS_WATCHED_CUTSCENES = 0x805780AC
    ADDRESS_STORY_ROUTE = 0x804C4BA8

    ADDRESS_CURRENT_LEVEL = 0x805EF95A
    ADDRESS_SELECT_LEVEL = 0x80584722
    ADDRESS_LOADING_MAYBE = 0x80570B26

    ADDRESS_LEVEL_STATUS = 0x80575F80
    button_menu_address = 0x8056ED4F
    CHECKPOINT_FLAGS = [0x80575FFC, 0x80576018, 0x80576034, 0x80576050,
                        0x8057606C, 0x80576088, 0x805760A4, 0x805760C0]

    is_paused_address = 0x805EE1DC
    boss_save_info_base_address = 0x80577499
    boss_final_additional_unlock_address = 0x80577720
    CURRENT_STAGE_BASE_KEYSANITY_ADDRESS = 0x8057fb80
    LIVES_ADDRESS = 0x80576704

    EXTRA_SAVE_DATA = 0x805780D0

    MENU_ENUM = 0x80583ACC
    LEVEL_SET_DATA = 0x809AF000

    CENTRAL_CITY_TIMER = 0x807D6924
    COSMIC_FALL_TIMER = 0x807D6C18
    LAST_WAY_TIMER = 0x807D6C90

    SUBTITLE_INFO = 0x8057FA6C
    LAST_SUBTITLE_TEXT = 0x80573340

    CharacterAddresses = [
        CharacterAddress("Sonic", 0x8057D77B),
        CharacterAddress("Tails", 0x8057D77F),
        CharacterAddress("Knuckles", 0x8057D783),
        CharacterAddress("Amy", 0x8057D787),
        CharacterAddress("Eggman", 0x8057D7A3),
        CharacterAddress("Rouge", 0x8057D78B),
        CharacterAddress("Omega", 0x8057D78F),
        CharacterAddress("Doom", 0x8057D7A7),
        CharacterAddress("Espio", 0x8057D797),
        CharacterAddress("Charmy", 0x8057D79F),
        CharacterAddress("Vector", 0x8057D793),
        CharacterAddress("Maria", 0x8057D79B),
    ]

    FIRST_STORY_MODE_STAGE_ADDRESS = 0x802D2131
    FIRST_STORY_MODE_STAGE_ADDRESS_SX = 0x80004BE5
    FIRST_STORY_MODE_STAGE_ADDRESS_RELOADED = 0x800046FD

class LevelStatusOptions:
    LoadingFirstTime = 0x00
    NotInLevel = 0x01
    Loading = 0x02
    Active = 0x03
    InCutscene = 0x04
    Paused = 0x05
    Finish = 0x06
    Restarting = 0x07
    Reloading = 0x08
    Death = 0x09
    Saving = 0x0A
    Blackout = 0x0B
    Other = 0x10

class MenuOptions:
    NotInMenu = 0x00
    MainMenu = 0x01
    Options = 0x02
    Story = 0x03
    StoryRecap = 0x05
    Select = 0x06



last_level = None
memory_data = {}
def ShowSETChanges(current_level):
    global memory_data
    global last_level

    if current_level is None:
        memory_data = {}
        return

    if last_level != current_level:
        last_level = current_level
        memory_data = {}

    length = Objects.GetSETFileLength(current_level)
    if length is None or length == 0:
        return

    start_address = GAME_ADDRESSES.LEVEL_SET_DATA
    set_item_count = length

    #809AF000 + (2C * (109-1)) + 20

    show_known = False
    known_objects = [ s.index for s in Objects.GetDesirableObjectsForStage(current_level) ]

    new_outputs = []
    for i in range(0, set_item_count):

        if not show_known and i in known_objects:
            continue

        spawn_data = start_address  + (0x2C * i) + 0x20
        object_type = spawn_data + 0x08
        link_id_ref = object_type + 0x02
        object_additional_pointer = None

        loaded_bytes = dolphin_memory_engine.read_bytes(spawn_data+3, 1)
        loaded_spawn_data = int.from_bytes(loaded_bytes, byteorder='big')

        loaded_bytes = dolphin_memory_engine.read_bytes(object_type, 2)
        loaded_object_type = int.from_bytes(loaded_bytes, byteorder='big')

        loaded_bytes = dolphin_memory_engine.read_bytes(link_id_ref, 1)
        link_id = int.from_bytes(loaded_bytes, byteorder='big')

        if loaded_spawn_data == 0 and loaded_object_type == 0 and spawn_data in memory_data:
            del memory_data[spawn_data]

        if spawn_data not in memory_data:
            memory_data[spawn_data] = [None, None]

        last_known = memory_data[spawn_data]
        last_known_spawn = last_known[0]

        extra_data_pointer = spawn_data + 0x10

        loaded_extra_pointer_bytes = dolphin_memory_engine.read_bytes(extra_data_pointer, 4)
        loaded_extra_pointer = int.from_bytes(loaded_extra_pointer_bytes, byteorder='big')

        loaded_from_extra_pointer_bytes = dolphin_memory_engine.read_bytes(loaded_extra_pointer, 100)

        if last_known_spawn != loaded_spawn_data:
            outputs = Objects.PrintSETChange(spawn_data, i, loaded_object_type, last_known_spawn, loaded_spawn_data,
                                   loaded_from_extra_pointer_bytes, link_id)
            memory_data[spawn_data] = [loaded_spawn_data, loaded_object_type]

            new_outputs.extend(outputs)

    if new_outputs is not None and len(new_outputs) > 0:
        new_outputs = sorted(new_outputs, key=lambda s:
        #SETObject(ObjectType.BLACK_ASSASSIN, Levels.CURRENT_LEVEL, 24, '8', region=0)
                             0 if not s.startswith("SETObject") else
                             int(s.split(" ")[3].replace("'","").replace(",", ""))
                             )

        for line in new_outputs:
            logger.info(line)


def f1():
    pass

class ShTHCommandProcessor(ClientCommandProcessor):

    reports = []
    region = 0


    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, ShTHContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


    #def _cmd_print_report(self):
    #    for p in self.reports:
    #        print("index=", p[0], "region=", p[1], "counter=", self.reports.index(p))

    #def _cmd_region_break(self):
    #    self.region += 1

    #def _cmd_region_clear(self):
    #    self.region = 0
    #    self.reports = []

    #def _cmd_set_r(self, *args):
    #    arguments = self.parse_args(args)
    #    self.reports.append((arguments["i"], self.region))


    #def arg_finish(self, build, type, results, value):
    ##    to_use = " ".join(build)

    #   if value:
    #        results[type] = to_use
    #    else:
    #        results[type+to_use] = True

    def parse_args(self, args, value=True):
        arguments = {}
        arg_build = []
        arg_type = None
        arg_building = False
        for arg in args:
            if arg.startswith('/'):
                if arg_building:
                    self.arg_finish(arg_build, arg_type, arguments, value)
                arg_building = True
                if len(arg) > 1:
                    arg_type = arg[1]
                if len(arg) > 2:
                    arg_build.append(arg[2:])
            elif arg_building:
                arg_build.append(arg)

        if arg_building:
            self.arg_finish(arg_build, arg_type, arguments, value)

        return arguments

    def _cmd_weapons(self, *args):
        """Prints the current weapons to the client."""
        if isinstance(self.ctx, ShTHContext):
            #print(args)
            arguments = self.parse_args(args)
            stage = self.ctx.last_level
            if 's' in arguments:
                stage = arguments['s']
                if stage == "":
                    logger.error("Invalid s value")
                    return


            #
            available = True
            if 'a' in arguments:
                if 's' in arguments:
                    available = False
                else:
                    stage = None

            held = False
            if 'h' in arguments:
                held = True

                if self.ctx.weapon_sanity_hold_option != Options.WeaponsanityHold.option_unlocked:
                    available = False

            weapons = self.ctx.getWeapons(stage=stage, available=available, held=held)
            logger.info("Available weapons:\n%s", "\n".join([ w.replace("Weapon:", "") for w in weapons]))


    def _cmd_vehicle(self, *args):
        """Prints the current vehicle status to the client."""
        if isinstance(self.ctx, ShTHContext):
            #print(args)
            if self.ctx.vehicle_logic == Options.VehicleLogic.option_false:
                logger.error("Vehicle logic not enabled.")
            else:
                data = self.ctx.get_unlocked_vehicles()
                for d in data:
                    logger.info("%s : %s", d[0], "(Available)" if d[1] else "(Out Of Logic)")



    def _cmd_story(self, *args):
        """Sets the in-game story steps to an available stage."""
        if isinstance(self.ctx, ShTHContext):
            stage = None
            arguments = self.parse_args(args)
            if 's' in arguments:
                stage = arguments['s']
                self.ctx.set_story_mode(stage)
            else:
                available = self.ctx.get_story_accessible_stages()
                available_names = [ Levels.LEVEL_ID_TO_LEVEL[n] for n in available]
                logger.info(available_names)

    def _cmd_gates(self, *args):
        """Prints the requirements for the next available gate."""
        if isinstance(self.ctx, ShTHContext):
            gate_info = self.get_gate_info(self.ctx)
            print(gate_info)
            if len(gate_info) == 0:
                logger.info("No more gates to open!")
            else:
                logger.info("\n".join([ str(g[0]) + ":" + str(g[1]) + "/" + str(g[2]) for g in gate_info]))

    def _cmd_token(self, *args):
        """ Show requirements for GO Mode"""
        if isinstance(self.ctx, ShTHContext):
            stage = None
            arguments = self.parse_args(args)
            token_dict = self.get_required_tokens(self.ctx)
            if token_dict is None:
                logger.error("Unable to work out tokens")
            else:
                logger.info("\n".join([ f"{s[0]}={s[1]}/{s[2]}" for s in token_dict]))

    def _cmd_boss(self, *args):
        """ Show story based requirements for accessibility to a boss"""
        if isinstance(self.ctx, ShTHContext):
            stage = None
            arguments = self.parse_args(args)
            if 's' in arguments:
                stage = arguments['s']

            self.ctx.find_boss(stage)

    def _cmd_spawnmessage(self, *args):
        """ Show spawn messages in game when information changes"""
        if isinstance(self.ctx, ShTHContext):
            if len(self.ctx.level_state.keys()) > 0:
                self.ctx.level_state["spawn_message"] = True
                logger.info("Spawn messages enabled")
                pass

    def _cmd_despawn(self, *args):
        """Despawn enemies when the checked are cleared."""
        if isinstance(self.ctx, ShTHContext):
            if len(self.ctx.level_state.keys()) > 0:
                self.ctx.level_state["despawn"] = True
                self.ctx.despawn_enemies()
                pass

    def get_required_and_active_count(self, ctx, stage, type):
        if stage is None:
            return 0
        required_count = 0
        reached_count = 0
        current_count = 0
        freq_or_avail_count = 0
        completed = False

        (mission_clear_locations, mission_locations, end_location,
         enemysanity_locations, checkpointsanity_locations,
         charactersanity_locations, token_locations, keysanity_locations,
         weaponsanity_locations, boss_locations, warp_locations,
         object_locations) = Locations.GetAllLocationInfo()

        info = Items.GetItemLookupDict()

        if type == "dark":
            dark = [ m for m in Locations.MissionClearLocations if m.stageId == stage
                  and m.alignmentId == MISSION_ALIGNMENT_DARK ]
            if len(dark) > 0:
                dark = dark[0]
                if dark.requirement_count is not None:
                    required_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        dark.requirement_count,dark.stageId, dark.alignmentId, ctx.override_settings)

                    freq_or_avail_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        100, dark.stageId, dark.alignmentId, ctx.override_settings)

                    associated_locations = [ (x.locationId, x) for x in mission_locations if x.alignmentId == dark.alignmentId and
                      x.stageId == dark.stageId and x.count <= required_count ]

                    checked = [ m for m in ctx.checked_locations if m in [ a[0] for a in associated_locations] ]
                    if len(checked) == 0:
                        reached_count = 0
                    else:
                        reached_count = max([ a[1].count for a in associated_locations if a[0] in checked])
                    if "dark_progress" in ctx.level_state:
                        current_count = ctx.level_state["dark_progress"]
                    else:
                        current_count = None

                    if reached_count >= required_count:
                        completed = True


        if type == "hero":
            dark = [ m for m in Locations.MissionClearLocations if m.stageId == stage
                  and m.alignmentId == MISSION_ALIGNMENT_HERO ]
            if len(dark) > 0:
                dark = dark[0]
                if dark.requirement_count is not None:
                    required_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        dark.requirement_count, dark.stageId, dark.alignmentId, ctx.override_settings)

                    freq_or_avail_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        100, dark.stageId, dark.alignmentId, ctx.override_settings)

                    associated_locations = [(x.locationId, x) for x in mission_locations if
                                            x.alignmentId == dark.alignmentId and
                                            x.stageId == dark.stageId and x.count <= required_count]

                    checked = [m for m in ctx.checked_locations if m in [a[0] for a in associated_locations]]
                    if len(checked) == 0:
                        reached_count = 0
                    else:
                        reached_count = max([a[1].count for a in associated_locations if a[0] in checked])

                    if "hero_progress" in ctx.level_state:
                        current_count = ctx.level_state["hero_progress"]
                    else:
                        current_count = None

                    if reached_count >= required_count:
                        completed = True



        if type == "darkclear":
            dark = [ m for m in Locations.MissionClearLocations if m.stageId == stage
                  and m.alignmentId == MISSION_ALIGNMENT_DARK ]
            if len(dark) > 0:
                dark = dark[0]
                if dark.requirement_count is not None:
                    required_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        dark.requirement_count, dark.stageId, dark.alignmentId, ctx.override_settings)

                    freq_or_avail_count = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                                  dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                        dark.requirement_count, dark.stageId, dark.alignmentId, ctx.override_settings)

                    current_count = len([unlock for unlock in ctx.handled if unlock[0].item in info and \
                         info[unlock[0].item].stageId == stage
                         and info[unlock[0].item].alignmentId == dark.alignmentId and
                         info[unlock[0].item].type == "level_object"])

                    current_count += len([unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
                                         info[unlock[0].item].stageId == stage
                                         and info[unlock[0].item].alignmentId == dark.alignmentId and
                                         info[unlock[0].item].type == "level_object"])
                    # Get dark id and lookup

                    associated_location = [x.locationId for x in mission_clear_locations if
                                            x.alignmentId == dark.alignmentId and
                                            x.stageId == dark.stageId ][0]

                    if associated_location in ctx.checked_locations:
                        completed = True



        if type == "heroclear":
            dark = [ m for m in Locations.MissionClearLocations if m.stageId == stage
                  and m.alignmentId == MISSION_ALIGNMENT_HERO ]
            if len(dark) > 0:
                if len(dark) > 0:
                    dark = dark[0]
                    if dark.requirement_count is not None:
                        required_count = ShadowUtils.getMaxRequired(
                            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                                      dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                            dark.requirement_count, dark.stageId, dark.alignmentId, ctx.override_settings)

                        freq_or_avail_count = ShadowUtils.getMaxRequired(
                            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                                      dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.alignmentId,
                                                                  ctx.override_settings),
                            dark.requirement_count, dark.stageId, dark.alignmentId, ctx.override_settings)

                        current_count = len([unlock for unlock in ctx.handled if unlock[0].item in info and \
                                             info[unlock[0].item].stageId == stage
                                             and info[unlock[0].item].alignmentId == dark.alignmentId and
                                             info[unlock[0].item].type == "level_object"])

                        current_count += len([unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
                                             info[unlock[0].item].stageId == stage
                                             and info[unlock[0].item].alignmentId == dark.alignmentId and
                                             info[unlock[0].item].type == "level_object"])

                        associated_location = [x.locationId for x in mission_clear_locations if
                                               x.alignmentId == dark.alignmentId and
                                               x.stageId == dark.stageId][0]

                        if associated_location in ctx.checked_locations:
                            completed = True

        if type == "gun":
            dark = [ m for m in Locations.GetEnemySanityLocations() if m.stageId == stage
                  and m.enemyClass == Locations.ENEMY_CLASS_GUN ]
            if len(dark) > 0:
                dark = dark[0]
                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    dark.total_count, dark.stageId, dark.enemyClass, ctx.override_settings)

                freq_or_avail_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    100, dark.stageId, dark.enemyClass, ctx.override_settings)

                associated_locations = [(x.locationId, x) for x in enemysanity_locations if
                                        x.alignmentId == dark.enemyClass and
                                        x.stageId == dark.stageId and x.count <= required_count]

                checked = [m for m in ctx.checked_locations if m in [a[0] for a in associated_locations]]
                if len(checked) == 0:
                    reached_count = 0
                else:
                    reached_count = max([a[1].count for a in associated_locations if a[0] in checked])
                if "gun_progress" in ctx.level_state:
                    current_count = ctx.level_state["gun_progress"]
                else:
                    current_count = None

                if reached_count >= required_count:
                    completed = True

        if type == "egg":
            dark = [ m for m in Locations.GetEnemySanityLocations() if m.stageId == stage
                     and m.enemyClass == Locations.ENEMY_CLASS_EGG ]
            if len(dark) > 0:
                dark = dark[0]
                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    dark.total_count, dark.stageId, dark.enemyClass, ctx.override_settings)

                freq_or_avail_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    100, dark.stageId, dark.enemyClass, ctx.override_settings)

                associated_locations = [(x.locationId, x) for x in enemysanity_locations if
                                        x.alignmentId == dark.enemyClass and
                                        x.stageId == dark.stageId and x.count <= required_count]

                checked = [m for m in ctx.checked_locations if m in [a[0] for a in associated_locations]]
                if len(checked) == 0:
                    reached_count = 0
                else:
                    reached_count = max([a[1].count for a in associated_locations if a[0] in checked])

                if "egg_progress" in ctx.level_state:
                    current_count = ctx.level_state["egg_progress"]
                else:
                    current_count = None

                if reached_count >= required_count:
                    completed = True

        if type == "alien":
            dark = [m for m in Locations.GetEnemySanityLocations() if m.stageId == stage
                    and m.enemyClass == Locations.ENEMY_CLASS_ALIEN]
            if len(dark) > 0:
                dark = dark[0]
                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    dark.total_count,dark.stageId, dark.enemyClass, ctx.override_settings)

                freq_or_avail_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                              dark.mission_object_name, ctx,
                                                                  dark.stageId, dark.enemyClass,
                                                                  ctx.override_settings),
                    100, dark.stageId, dark.enemyClass, ctx.override_settings)

                associated_locations = [(x.locationId, x) for x in enemysanity_locations if
                                        x.alignmentId == dark.enemyClass and
                                        x.stageId == dark.stageId and x.count <= required_count]

                checked = [m for m in ctx.checked_locations if m in [a[0] for a in associated_locations]]
                if len(checked) == 0:
                    reached_count = 0
                else:
                    reached_count = max([a[1].count for a in associated_locations if a[0] in checked])

                if "alien_progress" in ctx.level_state:
                    current_count = ctx.level_state["alien_progress"]
                else:
                    current_count = None

                if reached_count >= required_count:
                    completed = True

        return required_count, reached_count, current_count, freq_or_avail_count, completed

    def get_gate_info(self, ctx):
        required_items = ctx.gate_requirements
        info = Items.GetItemLookupDict()
        current_items = [info[i.item].name for i in ctx.items_received]

        result = []
        for item in required_items.items():
            gate_no = item[0]
            gate_reqs = item[1]
            enough = True
            for gate_req in gate_reqs.items():
                item_name = gate_req[0]
                count = gate_req[1]
                if current_items.count(item_name) < count:
                    enough = False

            if not enough:
                for gate_req in gate_reqs.items():
                    item_name = gate_req[0]
                    total = gate_req[1]
                    count = current_items.count(item_name)
                    result.append((item_name, count, total))
                break
            else:
                print(f"Gate {gate_no} is open")

        return result


    def get_required_tokens(self, ctx):
        token_requirements = []

        if ctx.requires_emeralds:
            token_requirements.append(("Chaos Emeralds", len(ctx.emeralds), 7))

        if ctx.required_mission_tokens > 0:
            token_requirements.append(("Mission Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.StandardMissionToken]),
                                       ctx.required_mission_tokens))

        if ctx.required_dark_tokens > 0:
            token_requirements.append(("Dark Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.StandardDarkToken]),
                                       ctx.required_dark_tokens))

        if ctx.required_hero_tokens > 0:
            token_requirements.append(("Hero Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.StandardHeroToken]),
                                       ctx.required_hero_tokens))

        if ctx.required_objective_tokens > 0:
            token_requirements.append(("Objective Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.ObjectiveToken]),
                                       ctx.required_objective_tokens))

        if ctx.required_final_tokens > 0:
            token_requirements.append(("Final Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.FinalToken]),
                                       ctx.required_final_tokens))

        if ctx.required_boss_tokens > 0:
            token_requirements.append(("Boss Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.BossToken]),
                                       ctx.required_boss_tokens))

        if ctx.required_final_boss_tokens > 0:
            token_requirements.append(("Final Boss Tokens",
                                       len([t for t in ctx.tokens if
                                            t[1].name == Items.Progression.FinalBossToken]),
                                       ctx.required_final_boss_tokens))

        return token_requirements


    def _cmd_story_progression(self, *args):
        """ Show story accessible stages"""
        if isinstance(self.ctx, ShTHContext):
            arguments = self.parse_args(args)

            quiet = False
            if "q" in arguments:
                quiet = True

            available = self.ctx.get_story_accessible_stages()
            types = ["heroclear", "darkclear"]
            dataset = {}
            for stage in available:
                for valid_type in types:
                    details = self.get_required_and_active_count(self.ctx, stage, valid_type)
                    dataset[(stage,valid_type)] = details
                    if quiet:
                        continue

                    if details is not None:
                        location_total_required = details[0]
                        location_reached_total = details[1]
                        current_count = details[2]
                        freq_or_avail = details[3]
                        complete = details[4]
                        if location_total_required > 0:
                            if "clear" in valid_type and current_count is not None:
                                logger.info("%s sanity for %s is %d/%d (%d available)%s", valid_type.capitalize(),
                                            Levels.LEVEL_ID_TO_LEVEL[stage],
                                            current_count, location_total_required,
                                            freq_or_avail, "\t(Complete)" if complete else "")
            return dataset





    def _cmd_story_hint(self, *args):
        """Using known path data, recommend a location to hint"""
        data = self._cmd_story_progression("/q")

        item_weights = {}

        info = Items.GetItemLookupDict()

        for item in data.items():
            stage = item[0][0]
            cleartype = item[0][1]
            details = item[1]

            alignment = None
            if cleartype == "heroclear":
                alignment = Levels.MISSION_ALIGNMENT_HERO
            elif cleartype == "darkclear":
                alignment = Levels.MISSION_ALIGNMENT_DARK

            location_total_required = details[0]
            location_reached_total = details[1]
            current_count = details[2]
            freq_or_avail = details[3]
            complete = details[4]
            if location_total_required == 0 or complete or alignment is None:
                continue

            left = location_total_required - current_count
            if left <= 0:
                continue

            item_name = [ i.name for i in info.values() if i.stageId == stage and i.alignmentId == alignment ][0]
            item_weights[item_name] = pow(1/left, 0.5)

        if len(item_weights.keys()) == 0:
            logger.info("Nothing to hint on")

        randomised_item = random.sample(list(item_weights.keys()), k=1, weights=list(item_weights.values()))[0]
        logger.info("Recommended item to hint for is:%s", randomised_item)

        pass
        #options = _cmd_story_progression("/q")

    def _cmd_sanity(self, *args):
        """Prints the current sanities to the client."""
        if isinstance(self.ctx, ShTHContext):
            arguments = self.parse_args(args)
            #print(arguments)

            stage = None
            if "s" in arguments:
                stage = arguments["s"]

            if stage is None and (self.ctx.last_level is None or self.ctx.level_state.keys() == 0):
                stages = self.ctx.available_levels
            else:
                stageId = None
                if stage is None:
                    stageId = self.ctx.last_level
                else:
                    stageId = stage
                    if type(stage) == str:
                        if stage.isdigit():
                            stageId = int(stage)
                        else:
                            stage = stage.upper()
                            level_by_name = {v.upper(): k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
                            if stage in level_by_name:
                                stageId = level_by_name[stage]
                stages = [stageId]

                stages = []
                for stageId in stages:
                    if stageId is not None:
                        valid_types = ['dark', 'hero', 'gun', 'egg', 'alien', 'darkclear', 'heroclear']
                        enemy_sanities = ['gun', 'alien', 'egg']
                        objective_sanities = ['dark', 'hero']
                        for valid_type in valid_types:
                            if (valid_type in arguments.keys() or
                                    len(arguments) == 0 or
                                    (len(arguments) == 1 and stageId != self.ctx.last_level) ):
                                if valid_type in enemy_sanities and not self.ctx.enemy_sanity:
                                    break
                                if valid_type in objective_sanities and not self.ctx.objective_sanity:
                                    break
                                details = self.get_required_and_active_count(self.ctx, stageId, valid_type)
                                if details is None:
                                    continue
                                location_total_required = details[0]
                                location_reached_total = details[1]
                                current_count = details[2]
                                freq_or_avail = details[3]
                                complete = details[4]
                                if location_total_required > 0:
                                    if "clear" in valid_type and current_count is not None:
                                        logger.info("%s sanity is %d/%d %s(%d available)", valid_type.capitalize(),
                                                    current_count, location_total_required,
                                                    "(Complete) " if complete else "",
                                                    freq_or_avail)
                                    elif current_count is not None:
                                        logger.info("%s sanity is %d/%d (Current: %d) (Frequency %d)", valid_type.capitalize(),
                                                    location_reached_total, location_total_required, current_count,freq_or_avail)
                                    elif "clear" in valid_type:
                                        pass
                                    else:
                                        pass
                    else:
                        logger.error("Invalid level provided")


@dataclass
class StageAlignmentAddress:
    stageId: int
    alignmentId: int
    tally_address: Optional[int]
    #addressSize: int
    #searchIndex: int | None
    #totalSearchIndex: int | None

class SAVE_STRUCTURE_DETAILS:
    LevelClears = 4
    # Repeat Dark for Normal and Hero
    AlignmentClear = 1
    AlignmentUnknown1 = 3
    AlignmentMissionRank = 4
    AlignmentTimeMinutes = 4
    AlignmentTimeSeconds = 1
    AlignmentTimeMilliseconds = 1
    AlignmentUnknown2 = 6
    AlignmentScore = 4

    Keys = 20  # 4 Bytes for each Key ID?

    AlignmentOrder = ["Dark", "Neutral", "Hero"]

    Size = 4 + (24 * 3) + 20

class SAVE_STRUCTURE_BOSS_DETAILS:
    Unlocked = 1
    BossUnknown1 = 3
    BossRank = 4
    BossTimeMinutes = 4
    BossTimeSeconds = 1
    BossTimeMilliseconds = 1

    Extra = 10

    Size = 96




KEY_IDENTIFIER_BY_STAGE = \
{
    STAGE_WESTOPOLIS:       [0x3F, 0x40, 0x3C, 0x3D, 0x3E], #Ordered
    STAGE_DIGITAL_CIRCUIT:  [0x3C, 0x40, 0x3D, 0x3E, 0x3F], #Ordered
    STAGE_GLYPHIC_CANYON:   [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_LETHAL_HIGHWAY:   [0x3F, 0x3C, 0x3E, 0x3D, 0x40], #Ordered
    STAGE_CRYPTIC_CASTLE:   [0x3E, 0x3D, 0x3C, 0x40, 0x3F], #Ordered, dark then neutral
    STAGE_PRISON_ISLAND:    [0x3D, 0x3C, 0x3E, 0x3F, 0x40], #Ordered
    STAGE_CIRCUS_PARK:      [0x40, 0x3C, 0x3D, 0x3E, 0x3F], #Ordered
    STAGE_CENTRAL_CITY:     [0x3E, 0x3C, 0x3F, 0x3D, 0x40], #Ordered, by dark mission
    STAGE_THE_DOOM:         [0xC9, 0xCA, 0xCB, 0xCC, 0x05], #Ordered
    STAGE_SKY_TROOPS:       [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_MAD_MATRIX:       [0x3C, 0x40, 0x3E, 0x3F, 0x3D], #Ordered - C/Y/G/R/R
    STAGE_DEATH_RUINS:      [0x01, 0x02, 0x03, 0x04, 0x05], #Ordered
    STAGE_THE_ARK:          [0x04, 0x01, 0x02, 0x05, 0x03], #Ordered
    STAGE_AIR_FLEET:        [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_IRON_JUNGLE:      [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered checkpoint order
    STAGE_SPACE_GADGET:     [0x04, 0x01, 0x02, 0x03, 0x05], #Ordered Dark first
    STAGE_LOST_IMPACT:      [0x03, 0x04, 0x05, 0x01, 0x02], #Ordered
    STAGE_GUN_FORTRESS:     [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_BLACK_COMET:      [0x60, 0x5F, 0x61, 0x62, 0x63], #Ordered
    STAGE_LAVA_SHELTER:     [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered, dark first
    STAGE_COSMIC_FALL:      [0x03, 0x04, 0x05, 0x01, 0x02], #Ordered
    STAGE_FINAL_HAUNT:      [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_THE_LAST_WAY:     [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
}


def GetStageUnlockAddresses():
    unlock_addresses = {}
    stage_index = 0
    boss_index = 0

    for stage in Levels.ALL_STAGES:
        if stage not in Levels.BOSS_STAGES:
            unlock_addresses[stage] = (GAME_ADDRESSES.westopolis_save_info_base_address +
                                                       (SAVE_STRUCTURE_DETAILS.Size * stage_index))
            stage_index += 1
        else:
            unlock_addresses[stage] = (GAME_ADDRESSES.boss_save_info_base_address +
                                       (SAVE_STRUCTURE_BOSS_DETAILS.Size * boss_index))
            boss_index += 1

    return unlock_addresses

def GetFinalBossAdditionalUnlock():
    unlock_addresses = {}
    boss_index = 0

    for stage in Levels.FINAL_BOSSES:
            unlock_addresses[stage] = (GAME_ADDRESSES.boss_final_additional_unlock_address +
                                       (SAVE_STRUCTURE_BOSS_DETAILS.Size * boss_index))
            boss_index += 1

    return unlock_addresses

def GetKeysanityAddresses():
    unlock_addresses = []

    for i in range(0, 5):
        unlock_addresses.append(GAME_ADDRESSES.CURRENT_STAGE_BASE_KEYSANITY_ADDRESS + (i*0x4))

    return unlock_addresses


def GetStageClearAddresses():

    clear_addresses = {}
    stage_index = 0
    boss_index = 0

    for stage in Levels.ALL_STAGES:
        if stage not in Levels.BOSS_STAGES:
            stage_alignments = GetAlignmentsForStage(stage)
            for alignment in stage_alignments:

                alignment_complete_address = (GAME_ADDRESSES.westopolis_save_info_base_address +
                                                       (SAVE_STRUCTURE_DETAILS.Size * stage_index) + (alignment * 24)) + 4

                alignment_rank_address = (alignment_complete_address + SAVE_STRUCTURE_DETAILS.AlignmentClear + SAVE_STRUCTURE_DETAILS.AlignmentUnknown1)

                alignment_time_address = (alignment_rank_address + SAVE_STRUCTURE_DETAILS.AlignmentMissionRank)

                clear_addresses[(stage, alignment)] = (alignment_complete_address, alignment_rank_address, alignment_time_address)

            stage_index += 1
        else:
            boss_complete_address = (GAME_ADDRESSES.boss_save_info_base_address +
                                              (SAVE_STRUCTURE_BOSS_DETAILS.Size * boss_index)) + 3

            boss_rank_address = (boss_complete_address + SAVE_STRUCTURE_BOSS_DETAILS.Unlocked +
                                 SAVE_STRUCTURE_BOSS_DETAILS.BossUnknown1)

            boss_time_address = (boss_rank_address + SAVE_STRUCTURE_BOSS_DETAILS.BossRank)

            clear_addresses[(stage, None)] = (boss_complete_address, boss_rank_address, boss_time_address)

            boss_index += 1

    return clear_addresses


def writeBytes(addr, data):
    #traceback.print_stack()

    print("write=", addr, data)
    dolphin_memory_engine.write_bytes(addr, data)


#DEFAULT_SEARCH_INDEX = (16 * 6) + 8
#SECONDARY_SEARCH_INDEX = (16 * 16) + 8
#CC_HERO_INDEX = (30 * 16) + 4
#PI_TD_HERO_INDEX = (16 * 6) + 4
#DEFAULT_TOTAL_INDEX_HERO = (16 * 5) + 4
#DEFAULT_TOTAL_INDEX = (16 * 5) + 8


StageAlignmentAddresses = [
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT),
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, GAME_ADDRESSES.ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, GAME_ADDRESSES.ADDRESS_ALIEN_COUNT),
    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, None),
    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT),
    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT),

    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT),
    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, GAME_ADDRESSES.ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, GAME_ADDRESSES.ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT,),
    StageAlignmentAddress(STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, GAME_ADDRESSES.ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT),

    StageAlignmentAddress(STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None)
]





def GetStageAlignmentAddress(stage_id, alignment_id):
    i = [ n for n in StageAlignmentAddresses if n.stageId == stage_id and n.alignmentId == alignment_id]
    if len(i) == 0:
        return None
    return i[0]


class ShTHContext(CommonContext):
    command_processor = ShTHCommandProcessor
    game = "Shadow The Hedgehog"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.override_settings = []
        self.dolphin_sync_task: Optional[asyncio.Task] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.game_id = None
        self.awaiting_rom = False
        self.awaiting_server = True
        self.invalid_rom = False
        self.last_rcvd_index = -1
        self.has_send_death = False
        self.available_levels = []

        self.items_to_handle = []
        self.handled = []
        self.level_state = {}
        self.characters_met = []
        self.checkpoint_snapshots = []
        self.checkpoint_trap_active = False
        self.lives = 0
        self.objective_sanity = False
        self.objective_percentage = 100
        self.objective_item_percentage = 100
        self.checkpoint_sanity = False
        self.character_sanity = False
        #self.checked_locations = []
        self.required_mission_tokens = 0
        self.required_hero_tokens = 0
        self.required_dark_tokens = 0
        self.required_final_tokens = 0
        self.required_objective_tokens = 0
        self.required_boss_tokens = 0
        self.required_final_boss_tokens = 0
        self.requires_emeralds = True
        self.key_sanity = False
        self.key_collection_method = Options.KeyCollectionMethod.default
        self.keys_required_for_doors = Options.KeysRequiredForDoors.default
        self.gates = {}
        self.gate_requirements = {}
        self.select_gates = Options.SelectGates.default
        self.select_gates_count = Options.SelectGatesCount.default
        self.gate_unlock_requirement = Options.GateUnlockRequirement.default

        self.enemy_sanity = False
        self.enemy_objective_sanity = False
        self.weapon_sanity_unlock = False
        self.weapon_sanity_hold_option = 0
        self.vehicle_logic = False
        self.level_buffer = None
        self.ring_link = False
        self.auto_clear_missions = False
        self.select_mode_available = True
        self.story_mode_available = False
        self.required_client_version = None
        self.expected_version_check = False
        self.enemy_sanity_percentage = 0
        self.enemy_objective_frequency = 0
        self.objective_frequency = 0
        self.enemy_frequency = 0

        self.hero_gauge_buffer = 0
        self.dark_gauge_buffer = 0
        self.hero_cooldown = None
        self.dark_cooldown = None
        self.hero_max_meter = 0
        self.dark_max_meter = 0
        self.hero_gauge_last = 0
        self.dark_gauge_last = 0

        self.poison_traps = 0
        self.ammo_traps = 0
        self.checkpoint_traps = 0
        self.ammo_boosts = {}

        self.junk_delay = 0

        self.tokens = []
        self.emeralds = []
        self.restart = False

        self.game_tags = []
        self.previous_rings = None
        self.ring_link_rings = 0
        self.instance_id = time.time()
        self.debug_logging = False
        self.error_logging = True
        self.info_logging = True
        self.last_level = None
        self.last_weapon = None
        self.boss_delay = 0
        self.last_accessible_levels = []
        self.level_status = None

        self.objective_completion_enemy_percentage = 100
        self.objective_completion_percentage = 100
        self.objective_enemy_percentage = 100
        self.objective_item_percentage_available = 100
        self.objective_item_enemy_percentage_available = 100
        self.music = None

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""
        self.level_keys = []
        self.music = None
        self.key_restore_complete = False
        self.shuffled_story_mode = Story.DefaultStoryMode
        self.successful_shuffle = False
        self.include_last_way_shuffle = False
        self.dead = False
        self.initialised = False
        self.secret_story_progression = False
        self.minimum_rank = Options.MinimumRank.option_e
        self.select_bosses = False
        self.select_initialised = False
        self.weapon_delay = None
        self.save_value = None
        self.save_rejected = False

        self.object_unlocks = False
        self.object_pulleys = False
        self.object_ziplines = False
        self.object_units = False
        self.object_rockets = False
        self.object_light_dashes = False
        self.object_warp_holes = False
        self.shadow_boxes = False
        self.energy_cores = False
        self.door_sanity = False
        self.gold_beetle_sanity = False
        self.objective_sanity_behaviour = None
        self.difficult_enemy_sanity = False
        self.objective_sanity_system = None

        self.last_subtitle_text_pointer = None
        self.last_subtitle_default_text = None
        self.last_subtitle_ttl = None
        self.last_subtitle_ttl_pointer = None
        self.last_save_index = None
        self.last_save_index_message = None
        self.last_subtitle_message_base_pointer = None


    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        self.current_stage_name = ""
        await super().disconnect(allow_autoreconnect)


    def HasWeaponBeenHeld(self, name):
        locations = Locations.GetLocationInfoDict()
        hold_locations = [ locations[s].other for s in self.checked_locations if locations[s].location_type == Locations.LOCATION_TYPE_WEAPON_HOLD]
        return name in [ h for h in hold_locations ]

    def getWeapons(self, available=True, stage=None, held=False):
        info = Items.GetItemLookupDict()
        weapon_dict = Weapons.GetWeaponDict()
        weapon_group_dict = Weapons.GetWeaponGroupsDict()

        allowed_weapons = [weapon_dict[info[unlock[0].item].name] for unlock in self.handled if
                           unlock[0].item in info and \
                           info[unlock[0].item].type == "Weapon"]

        allowed_weapons_by_group = [weapon_group_dict[info[unlock[0].item].name] for unlock in self.handled if
                           unlock[0].item in info and \
                           info[unlock[0].item].type == "WeaponGroup"]

        weapons_to_handle = [weapon_dict[info[unlock[0].item].name] for unlock in self.items_to_handle if unlock[0].item in info and \
                             info[unlock[0].item].type == "Weapon"]

        weapons_by_weapon_groups_to_handle = [weapon_group_dict[info[unlock[0].item].name] for unlock in self.items_to_handle if
                             unlock[0].item in info and \
                             info[unlock[0].item].type == "WeaponGroup"]


        allowed_weapons.extend(weapons_to_handle)
        for items in allowed_weapons_by_group:
            allowed_weapons.extend(items)
        for items in weapons_by_weapon_groups_to_handle:
            allowed_weapons.extend(items)

        if stage is not None:
            weapons_by_stage = Weapons.GetWeaponByStageDict()
            stageId = stage
            if type(stage) == str:
                if stage.isdigit():
                    stageId = int(stage)
                else:
                    level_by_name = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
                    if stage in level_by_name:
                        stageId = level_by_name[stage]

            weapons_in_stage = weapons_by_stage[stageId]
            if available:
                allowed_weapons = [ r for r in allowed_weapons if r.game_id in weapons_in_stage ]
            else:
                allowed_weapons = [ r for r in weapon_dict.values() if r.game_id in weapons_in_stage ]

        results = [ weapon.name for weapon in allowed_weapons ]

        if held and self.weapon_sanity_hold_option != Options.WeaponsanityHold.option_off:
            results = [ r + " " + ("(Held)" if self.HasWeaponBeenHeld(r) else "(Not Held)")
                        for r in results ]
            pass

        return results

    async def server_auth(self, username_requested: bool = True, password_requested: bool = False,
                          expectedUsername: str = None):
        if username_requested and not self.auth:
            await super(ShTHContext, self).get_username()
            if expectedUsername is not None and self.username != expectedUsername:
                self.auth = None
        if password_requested and not self.password:
            await super(ShTHContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information")
            return
        logger.info("Auth complete, connecting")
        await self.send_connect()

    def restoreState(self):
        (mission_clear_locations, mission_locations, end_location, enemy_locations,
            checkpointsanity_locations, charactersanity_locations,
         token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
         warp_locations, object_locations) = Locations.GetAllLocationInfo()

        if self.character_sanity:
            characters = []
            for character in GAME_ADDRESSES.CharacterAddresses:
                characterName = character.name
                charLocation = [char for char in charactersanity_locations if char.other == characterName]
                if len(charLocation) > 0:
                    characters.append(charLocation[0])

            already_checked_chars = [ c for c in characters if c.locationId in self.checked_locations ]
            for char in already_checked_chars:
                self.characters_met.append(char.other)

    def despawn_enemies(self):
        enemy_types = Objects.GetStandardEnemyTypes()
        relevant_objects = Objects.GetDesirableObjectsForStage(self.last_level)
        if relevant_objects is None or len(relevant_objects) == 0:
            return

        relevant_objects = [ r for r in relevant_objects if r.object_type in enemy_types and r.vehicle is None]

        relevant_objects = [ r for r in relevant_objects if GetObjectLocationName(r)[0] in self.checked_locations]

        start_address = GAME_ADDRESSES.LEVEL_SET_DATA
        max_index = max([o.index for o in relevant_objects])

        full_loaded_bytes = dolphin_memory_engine.read_bytes(start_address, (0x2C * (max_index + 1)))

        for object in relevant_objects:
            base_index = (0x2C * object.index) + 0x20
            spawn_base_byte = base_index + 0x03
            #object_type_index = base_index + 0x08
            #extra_data_pointer = base_index + 0x10

            despawn = 4
            despawn_bytes = despawn.to_bytes(4, byteorder='big')

            spawn_data = start_address + (0x2C * object.index) + 0x20

            loaded_bytes = [full_loaded_bytes[spawn_base_byte]]
            loaded_spawn_data = int.from_bytes(loaded_bytes, byteorder='big')

            if loaded_spawn_data not in [0x0, 0x8]:
                writeBytes(spawn_data, despawn_bytes)


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args["slot_data"]

            if "check_level" in slot_data:
                print("CheckLevel is", slot_data["check_level"])
                self.level_buffer = slot_data["check_level"]

            if "objective_sanity" in slot_data:
                self.objective_sanity = slot_data["objective_sanity"]

            if "objective_percentage" in slot_data:
                self.objective_percentage = slot_data["objective_percentage"]

            if "objective_item_percentage" in slot_data:
                self.objective_item_percentage = slot_data["objective_item_percentage"]

            if "checkpoint_sanity" in slot_data:
                self.checkpoint_sanity = slot_data["checkpoint_sanity"]

            if "character_sanity" in slot_data:
                self.character_sanity = slot_data["character_sanity"]

            if "key_sanity" in slot_data:
                self.key_sanity = slot_data["key_sanity"]

            if "key_collection_method" in slot_data:
                self.key_collection_method = slot_data["key_collection_method"]

            if "keys_required_for_doors" in slot_data:
                self.keys_required_for_doors = slot_data["keys_required_for_doors"]

            if "gates" in slot_data:
                self.gates = slot_data["gates"]
            if "gate_requirements" in slot_data:
                self.gate_requirements = slot_data["gate_requirements"]
                print("GR=", self.gate_requirements)
            if "select_gates" in slot_data:
                self.select_gates = slot_data["select_gates"]
            if "select_gates_count" in slot_data:
                self.select_gates_count = slot_data["select_gates_count"]
            if "gate_unlock_requirement" in slot_data:
                self.gate_unlock_requirement = slot_data["gate_unlock_requirement"]

            if "required_mission_tokens" in slot_data:
                self.required_mission_tokens = slot_data["required_mission_tokens"]

            if "required_hero_tokens" in slot_data:
                self.required_hero_tokens = slot_data["required_hero_tokens"]

            if "required_dark_tokens" in slot_data:
                self.required_dark_tokens = slot_data["required_dark_tokens"]

            if "required_final_tokens" in slot_data:
                self.required_final_tokens = slot_data["required_final_tokens"]

            if "required_objective_tokens" in slot_data:
                self.required_objective_tokens = slot_data["required_objective_tokens"]

            if "required_boss_tokens" in slot_data:
                self.required_boss_tokens = slot_data["required_boss_tokens"]

            if "required_final_boss_tokens" in slot_data:
                self.required_final_boss_tokens = slot_data["required_final_boss_tokens"]

            if "requires_emeralds" in slot_data:
                self.requires_emeralds = slot_data["requires_emeralds"]

            if "enemy_sanity" in slot_data:
                self.enemy_sanity = slot_data["enemy_sanity"]

            if "enemy_objective_sanity" in slot_data:
                self.enemy_objective_sanity = slot_data["enemy_objective_sanity"]

            if "weapon_sanity_hold" in slot_data:
                self.weapon_sanity_hold_option = slot_data["weapon_sanity_hold"]

            if "weapon_sanity_unlock" in slot_data:
                self.weapon_sanity_unlock = slot_data["weapon_sanity_unlock"]

            if "vehicle_logic" in slot_data:
                self.vehicle_logic = slot_data["vehicle_logic"]

            if "ring_link" in slot_data:
                self.ring_link = slot_data["ring_link"]

            if "auto_clear_missions" in slot_data:
                self.auto_clear_missions = slot_data["auto_clear_missions"]

            if "story_mode_available" in slot_data:
                self.story_mode_available = slot_data["story_mode_available"]

            if "select_mode_available" in slot_data:
                self.select_mode_available = slot_data["select_mode_available"]

            if "required_client_version" in slot_data:
                self.required_client_version = slot_data["required_client_version"]

            if "enemy_sanity_percentage" in slot_data:
                self.enemy_sanity_percentage = slot_data["enemy_sanity_percentage"]

            if "override_settings" in slot_data:
                self.override_settings = slot_data["override_settings"]

            if "objective_completion_enemy_percentage" in slot_data:
                self.objective_completion_enemy_percentage = slot_data["objective_completion_enemy_percentage"]

            if "objective_completion_percentage" in slot_data:
                self.objective_completion_percentage = slot_data["objective_completion_percentage"]

            if "objective_enemy_percentage" in slot_data:
                self.objective_enemy_percentage = slot_data["objective_enemy_percentage"]

            if "objective_item_percentage_available" in slot_data:
                self.objective_item_percentage_available = slot_data["objective_item_percentage_available"]

            if "objective_item_enemy_percentage_available" in slot_data:
                self.objective_item_enemy_percentage_available = slot_data["objective_item_enemy_percentage_available"]

            if "shuffled_story_mode" in slot_data:
                self.shuffled_story_mode = Story.StringToStory(slot_data["shuffled_story_mode"])

            if "include_last_way_shuffle" in slot_data:
                self.include_last_way_shuffle = slot_data["include_last_way_shuffle"]

            if "secret_story_progression" in slot_data:
                self.secret_story_progression = slot_data["secret_story_progression"]

            if "select_bosses" in slot_data:
                self.select_bosses = slot_data["select_bosses"]

            if "minimum_rank" in slot_data:
                self.minimum_rank = slot_data["minimum_rank"]

            if "enemy_objective_frequency" in slot_data:
                self.enemy_objective_frequency = slot_data["enemy_objective_frequency"]

            if "objective_frequency" in slot_data:
                self.objective_frequency = slot_data["objective_frequency"]

            if "enemy_frequency" in slot_data:
                self.enemy_frequency = slot_data["enemy_frequency"]

            if "save_value" in slot_data:
                self.save_value = slot_data["save_value"]

            if "shadow_mod" in slot_data:
                mod = slot_data["shadow_mod"]
                if mod == Options.ShadowMod.option_vanilla and self.game_id != bytes(SHADOW_THE_HEDGEHOG_GAME_ID, "utf-8"):
                    logger.fatal("Wrong shadow mod detected")
                    self.invalid_rom = True
                    return

                elif mod == Options.ShadowMod.option_reloaded and self.game_id != bytes(SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED, "utf-8"):
                    logger.fatal("Wrong shadow mod detected")
                    self.disconnect(True)
                    self.invalid_rom = True
                    return

                elif mod == Options.ShadowMod.option_sx and self.game_id != bytes(SHADOW_THE_HEDGEHOG_GAME_ID_SX, "utf-8"):
                    logger.fatal("Wrong shadow mod detected")
                    self.invalid_rom = True
                    return



            if "object_unlocks" in slot_data:
                self.object_unlocks = slot_data["object_unlocks"]

            if "object_pulleys" in slot_data:
                self.object_pulleys = slot_data["object_pulleys"]

            if "object_ziplines" in slot_data:
                self.object_ziplines = slot_data["object_ziplines"]

            if "object_units" in slot_data:
                self.object_units = slot_data["object_units"]

            if "object_rockets" in slot_data:
                self.object_rockets = slot_data["object_rockets"]

            if "object_light_dashes" in slot_data:
                self.object_light_dashes = slot_data["object_light_dashes"]

            if "object_warp_holes" in slot_data:
                self.object_warp_holes = slot_data["object_warp_holes"]

            if "shadow_boxes" in slot_data:
                self.shadow_boxes = slot_data["shadow_boxes"]

            if "energy_cores" in slot_data:
                self.energy_cores = slot_data["energy_cores"]

            if "door_sanity" in slot_data:
                self.door_sanity = slot_data["door_sanity"]

            if "gold_beetle_sanity" in slot_data:
                self.gold_beetle_sanity = slot_data["gold_beetle_sanity"]

            if "objective_sanity_system" in slot_data:
                self.objective_sanity_system = slot_data["objective_sanity_system"]

            if "objective_sanity_behaviour" in slot_data:
                self.objective_sanity_behaviour = slot_data["objective_sanity_behaviour"]

            if "difficult_enemy_sanity" in slot_data:
                self.difficult_enemy_sanity = slot_data["difficult_enemy_sanity"]

            self.restoreState()
            self.awaiting_server = False

            #self.items_received_2 = []
            #self.last_rcvd_index = -1
            #self.update_salvage_locations_map()
            #if "death_link" in args["slot_data"]:
            #    Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
            #visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            #Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_to_handle.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
                    self.junk_delay = 0
            self.items_to_handle.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            pass
        elif cmd == "Bounced":
            if "tags" in args:
                related_tags = args["tags"]
                if "RingLink" in related_tags:
                    handle_received_rings(self, args["data"])
            #requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            #if self.slot is not None:
            #    visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            #    if visited_stages_key in requested_keys_dict:
            #        visited_stages = requested_keys_dict[visited_stages_key]
            #        # If it has not been set before, the value in the response will be None
            #       visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
            #        # If the current stage name is not in the set, send a message to update the dictionary on the
            #        # server.
            #        current_stage_name = self.current_stage_name
            #        if current_stage_name and current_stage_name not in visited_stage_names:
            #            visited_stage_names.add(current_stage_name)
            #            Utils.async_start(self.update_visited_stages(current_stage_name))
            #        self.visited_stage_names = visited_stage_names
        #Utils.async_start(self.process_shth_data(cmd, args))

    def on_deathlink(self, data: Dict[str, Any]):
        super().on_deathlink(data)
        #_give_death(self)

    def run_gui(self):
        from kvui import GameManager

        class ShTHManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Shadow The Hedgehog"

        self.ui = ShTHManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


    def stage_to_stage_id(self, stage):
        stageId = stage
        if type(stage) == str:

            if stage.isdigit():
                stageId = int(stage)
            else:
                level_by_name = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
                level_by_name_easy_keys = [(name.upper().replace(" ", ""), name) for name in level_by_name]
                level_by_name_easy = {}
                for keys in level_by_name_easy_keys:
                    level_by_name_easy[keys[0]] = level_by_name[keys[1]]
                stage_easy = stage.upper().replace(" ", "")
                if stage_easy in level_by_name_easy:
                    stageId = level_by_name_easy[stage_easy]
                else:
                    return None

        return stageId

    def find_boss(self, stage):
        stageId = self.stage_to_stage_id(stage)
        if stageId is None:
            return None

        story = self.shuffled_story_mode
        routes_to_boss = [ s for s in story if s.boss ==  stageId]
        if len(routes_to_boss) == 0:
            logger.error("Boss not available")
            return None

        location_dict = Locations.GetLocationInfoDict()
        remaining_locations = self.missing_locations
        uncleared_stages = [location_dict[l] for l in remaining_locations
                            if l in location_dict and location_dict[l].location_type == Locations.LOCATION_TYPE_MISSION_CLEAR]

        known_route = False
        for route in routes_to_boss:
            uncleared = [ u for u in uncleared_stages if u.stageId == route.start_stage_id and u.alignmentId == route.alignment_id]
            if len(uncleared) == 0:
                known_route = True
                logger.info("Route to boss %s via %s %s", Levels.LEVEL_ID_TO_LEVEL[route.boss],
                            Levels.LEVEL_ID_TO_LEVEL[route.start_stage_id],
                            ALIGNMENT_TO_STRING[route.alignment_id])
            pass

        if not known_route:
            logger.info("Route currently unknown.")

    def get_unlocked_vehicles(self):
        if not self.auth:
            return []

        vehicle_data = Items.GetVehicles()
        results = []

        for vehicle in vehicle_data:
            have_vehicle = False
            if ((vehicle.itemId + Items.BASE_ID) in [ h[0].item for h in self.handled ] or
                    (vehicle.itemId + Items.BASE_ID) in [i[0].item for i in self.items_to_handle]):
                have_vehicle = True

            results.append((vehicle.name, have_vehicle))

        return results

    def get_story_accessible_stages(self):
        if not self.auth:
            return False

        results = []
        for stageId in Levels.ALL_STAGES:
            if is_level_accessible(self, stageId, story=True):
                results.append(stageId)

        return results

    def set_story_mode(self, stage):
        if not self.auth:
            return False
        stageId = self.stage_to_stage_id(stage)
        if stageId is None:
            return None

        if not is_level_accessible(self, stageId, story=True):
            logger.error("Level is not accessible: %s", stage)
            return False

        elif stageId in Levels.BOSS_STAGES and stageId not in Levels.FINAL_BOSSES and stageId != Levels.BOSS_DEVIL_DOOM:
            logger.error("Unavailable to set story bosses due to oversight, "
                         "please lookup with /boss command until future updates.")
            return False

        story_block = Levels.STAGE_TO_STORY_BLOCK[stageId]

        story_counter = GAME_ADDRESSES.STORY_MODE_COUNTER
        count = 1
        count_bytes = count.to_bytes(4, byteorder='big')
        writeBytes(story_counter, count_bytes)

        story_step = story_counter + ((count+1) * 4)
        stage_bytes = story_block.to_bytes(4, byteorder='big')
        writeBytes(story_step, stage_bytes)

        logger.info("Stage available. Please select continue.")

        return True


def RankToOption(rank_number, rank_option):
    required_rank = Options.MinimumRank.option_e
    if rank_option == Options.MinimumRank.option_a:
        required_rank = 0
    elif rank_option == Options.MinimumRank.option_b:
        required_rank = 1
    elif rank_option == Options.MinimumRank.option_c:
        required_rank = 2
    elif rank_option == Options.MinimumRank.option_d:
        required_rank = 3
    elif rank_option == Options.MinimumRank.option_e:
        required_rank = 4

    if rank_number > required_rank:
        return True

    return False

async def check_save_loaded(ctx):

    # Check a save is loaded. Write to static memory address with seed info
    # Determine save is invalid if seed isn't blank
    # Throw exception if save is not configured
    # If first load, set the memory to whether it can go in the save-data

    if ctx.save_rejected:
        return False

    loaded = False

    loaded_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.SAVE_DATA_LOADED, 1)
    loaded_bytes = int.from_bytes(loaded_bytes, byteorder='big')

    # This doesn't yet factor in fully loaded, so this needs to be fixed

    if loaded_bytes == 1:
        loaded = True

    mission_clear_locations, mission_locations, end_location, enemy_locations,\
        checkpointsanity_locations, charactersanity_locations,\
        token_locations, keysanity_locations, weaponsanity_locations, boss_locations,\
        warp_locations, object_locations = Locations.GetAllLocationInfo()

    random_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.EXTRA_SAVE_DATA, 8)
    loaded_bytes = int.from_bytes(random_bytes, byteorder='big')

    first_game_load = False
    ctx.save_rejected = False
    if loaded_bytes == 0:
        first_game_load = True
    elif SAVE_VALUE_CHECK and loaded_bytes != ctx.save_value:
        logger.error("Unrecognised save value. Please load from the correct/new save.")
        ctx.save_rejected = True
        loaded = False

    # TODO: Check for newly obtained instead of all

    if loaded and len(ctx.level_state.keys()) == 0:

        per_stage = {}
        cleared_missions = []

        messages = []
        for stage_clear_address in GetStageClearAddresses().items():
            stage, alignment = stage_clear_address[0]
            clear_address_data = stage_clear_address[1]
            clear_address = clear_address_data[0]
            clear_address_rank = clear_address_data[1]
            clear_address_time = clear_address_data[2]

            if not is_level_accessible(ctx, stage):
                continue

            if ctx.story_mode_available and is_level_accessible(ctx, stage, story=True):
                if stage not in ctx.available_levels:
                    ctx.available_levels.append(stage)

            if not is_mission_completable(ctx, stage, alignment):
                #print("IMC", stage, alignment, "not completable")
                continue

            time_bytes = dolphin_memory_engine.read_bytes(clear_address_time, 6)
            time_data = struct.unpack('>IBB', time_bytes)

            # Add handle that level must not be set to default time!

            current_bytes = dolphin_memory_engine.read_bytes(clear_address, 1)
            current_status = int.from_bytes(current_bytes, byteorder='big')

            # TODO: Handle auto boss clears and completion based on time

            if current_status == 1:
                if first_game_load:
                    pass
                    #ctx.save_rejected = True
                    #logger.error("Game has preloaded but has clear data. Please start from a new save.")
                    #break

                if time_data[0] == 99 and time_data[1] == 59 and time_data[2] == 99:
                    continue

                if ctx.minimum_rank != Options.MinimumRank.option_e:
                    rank_bytes = dolphin_memory_engine.read_bytes(clear_address_rank, 4)
                    rank = int.from_bytes(rank_bytes, byteorder='big')
                    if RankToOption(rank, ctx.minimum_rank):
                        continue

                cleared_missions.append((stage,alignment))
                if stage not in per_stage:
                    per_stage[stage] = []
                per_stage[stage].append(alignment)

                clear_location = [m for m in mission_clear_locations if m.stageId == stage
                                  and m.alignmentId == alignment and m.locationId not in ctx.checked_locations]

                associated_token_locations = [t for t in token_locations if t.alignmentId ==
                                              alignment and t.stageId == stage and t.locationId not in ctx.checked_locations]

                boss_location = [ b for b in boss_locations if b.stageId == stage and b.locationId not in
                                   ctx.checked_locations ]

                if len(associated_token_locations) > 0:
                    messages.extend([ a.locationId for a in associated_token_locations])

                if len(clear_location) == 1:
                    messages.append(clear_location[0].locationId)

                if len(boss_location) == 1:
                    messages.append(boss_location[0].locationId)
            elif current_status == 0:
                clear_location = [m for m in mission_clear_locations if m.stageId == stage
                                  and m.alignmentId == alignment and m.locationId in ctx.checked_locations]

                if len(clear_location) > 0:
                    for c in clear_location:
                        logger.info(f"Restore {c.name}")
                        set_complete = 1
                        set_complete_bytes = set_complete.to_bytes(1, byteorder='big')

                        set_seconds = 58
                        set_seconds_bytes = set_seconds.to_bytes(1, byteorder='big')

                        writeBytes(clear_address, set_complete_bytes)
                        writeBytes(clear_address_time+4, set_seconds_bytes)


        # decide settings for goal

        set_last_way = IsEndGameEnabled(ctx)

        last_way_available_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_LAST_STORY_OPTION, 1)
        is_last_way_available = int.from_bytes(last_way_available_bytes, byteorder='big')
        if (set_last_way and
                (not ctx.include_last_way_shuffle or not ctx.story_mode_available)):
            if is_last_way_available != 1:
                set_to = 1
                set_last_way_bytes = set_to.to_bytes(1, byteorder='big')
                writeBytes(GAME_ADDRESSES.ADDRESS_LAST_STORY_OPTION, set_last_way_bytes)

                # Review
                for cutscene in range(0, 16):
                    buffer_address_cutscene = GAME_ADDRESSES.CUTSCENE_BUFFER + (8 * cutscene)
                    to_write = 0
                    set_blank = to_write.to_bytes(4, byteorder='big')
                    writeBytes(buffer_address_cutscene, set_blank)
        else:
            if is_last_way_available:
                logger.error("Last Way disabled, not yet meeting goal criteria.")
                set_to = 0
                set_last_way_bytes = set_to.to_bytes(1, byteorder='big')
                writeBytes(GAME_ADDRESSES.ADDRESS_LAST_STORY_OPTION, set_last_way_bytes)
                writeBytes(GAME_ADDRESSES.ADDRESS_LAST_STORY_APPROVED, set_last_way_bytes)

        finished = False

        # TODO: Write 0s to cutscene chain to allow them to be skipped
        # Mainly for final story
        # If possible, work out how to kick the player out after TLW
        # Or don't let it finish, etc.

        last_cutscene_data = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_LAST_CUTSCENE, 4)
        last_cutscene_id = int.from_bytes(last_cutscene_data, byteorder='big')
        # Full CGI Cutscenes seem to go to  809F1300, which includes 8201!
        # 926 Is the moment Super Shadow is successful
        if last_cutscene_id in (926, 8201, 8202, 8203, 8204):
            finished = True


        if len(messages) > 0:
            unsent_messages = [ message for message in messages if message not in ctx.checked_locations]
            message = [{"cmd": 'LocationChecks', "locations": unsent_messages}]
            await ctx.send_msgs(message)

        if finished and not ctx.finished_game:
            clear_location = Locations.GetClearLocation()[0]
            message = [{"cmd": 'LocationChecks', "locations": [clear_location.locationId]}]
            await ctx.send_msgs(message)

            ctx.finished_game = True
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])

        expected_version = ShadowUtils.GetVersionString()
        if (not ctx.expected_version_check and
                ctx.required_client_version is not None and
                expected_version != ctx.required_client_version):
            logger.error("Unexpected version from generation and runtime. Client errors on older versions are likely to occur.")
            ctx.expected_version_check = True

        # Check for mission completes

    if loaded and first_game_load and not ctx.save_rejected:
        new_bytes = ctx.save_value.to_bytes(8, byteorder='big')
        writeBytes(GAME_ADDRESSES.EXTRA_SAVE_DATA, new_bytes)

    return loaded


def IsEndGameEnabled(ctx):
    set_last_way = True
    if ctx.requires_emeralds:
        if len(ctx.emeralds) != 7:
            set_last_way = False

    if ctx.required_mission_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.StandardMissionToken]) < ctx.required_mission_tokens:
            set_last_way = False

    if ctx.required_dark_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.StandardDarkToken]) < ctx.required_dark_tokens:
            set_last_way = False

    if ctx.required_hero_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.StandardHeroToken]) < ctx.required_hero_tokens:
            set_last_way = False

    if ctx.required_objective_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.ObjectiveToken]) < ctx.required_objective_tokens:
            set_last_way = False

    if ctx.required_final_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.FinalToken]) < ctx.required_final_tokens:
            set_last_way = False

    if ctx.required_boss_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.BossToken]) < ctx.required_boss_tokens:
            set_last_way = False

    if ctx.required_final_boss_tokens > 0:
        if len([t for t in ctx.tokens if
                t[1].name == Items.Progression.FinalBossToken]) < ctx.required_final_boss_tokens:
            set_last_way = False

    return set_last_way

def HandleLocationAutoclears():
    location_dict = Locations.GetLocationInfoDict()
    all_locations = location_dict.values()
    level_clears = [ a for a in all_locations if a.location_type == Locations.LOCATION_TYPE_MISSION_CLEAR]
    space_gadget_hero = [ a for a in level_clears if a.stageId == STAGE_SPACE_GADGET
                             and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    space_gadget_neutral = [a for a in level_clears if a.stageId == STAGE_SPACE_GADGET
                         and a.alignmentId == MISSION_ALIGNMENT_NEUTRAL][0]

    cosmic_fall_hero = [a for a in level_clears if a.stageId == STAGE_COSMIC_FALL
                         and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    cosmic_fall_dark = [a for a in level_clears if a.stageId == STAGE_COSMIC_FALL
                         and a.alignmentId == MISSION_ALIGNMENT_DARK][0]

    digital_circuit_dark = [a for a in level_clears if a.stageId == STAGE_DIGITAL_CIRCUIT
                        and a.alignmentId == MISSION_ALIGNMENT_DARK][0]

    digital_circuit_hero = [a for a in level_clears if a.stageId == STAGE_DIGITAL_CIRCUIT
                        and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    return {
        space_gadget_neutral.locationId: space_gadget_hero,
        cosmic_fall_dark.locationId: cosmic_fall_hero,
        digital_circuit_hero.locationId: digital_circuit_dark
    }


def is_level_accessible(ctx, stageId, story=False):
    info = Items.GetItemLookupDict()

    if stageId in ctx.available_levels:
        return True

    if ctx.select_mode_available and not story:
        i = [
            unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                        and info[unlock[0].item].type == "level_unlock"
        ]

        i2 = [
            unlock for unlock in ctx.handled if unlock[0].item in info
                                                        and info[unlock[0].item].type == "level_unlock"
        ]

        i.extend(i2)

        levels_unlocked_by_item = [ info[level[0].item].stageId for level in i ]

        available = True
        if stageId in Levels.BOSS_STAGES and stageId not in Levels.FINAL_BOSSES:
            boss_stage_requirement = Story.GetVanillaBossStage(stageId)
            if boss_stage_requirement is not None:
                available = is_level_accessible(ctx, boss_stage_requirement)

        if stageId in levels_unlocked_by_item and available:
            return True

    if ctx.story_mode_available:
        mission_locations = Locations.MissionClearLocations
        storyMode = ctx.shuffled_story_mode
        checking = [stageId]
        checked = []
        success = False
        while len(checking) > 0:
            first = checking.pop()
            checked.append(first)

            leads = [ s for s in storyMode if s.end_stage_id == first or s.boss == first]
            for lead in leads:
                if lead.start_stage_id in checked:
                    continue

                if lead.start_stage_id is None:
                    success = True
                    break

                ml = [ Levels.GetLevelCompletionNames(m.stageId, m.alignmentId)
                       for m in mission_locations if m.alignmentId == lead.alignment_id and m.stageId == lead.start_stage_id]

                ml_id, ml_name = ml[0]
                if ml_id in ctx.checked_locations:
                    checking.append(lead.start_stage_id)

        return success

    return False




# By handling in this function, all handling is auto-handled with stage access, etc as well!

def is_mission_completable(ctx, stage, alignment):
    relevant_level_clears = [ mc for mc in MissionClearLocations if mc.alignmentId == alignment and mc.stageId == stage]
    relevant_boss_clears = [ b for b in Locations.BossClearLocations if b.stageId == stage ]
    info = Items.GetItemLookupDict()

    if not is_level_accessible(ctx, stage):
        return False

    if len(relevant_level_clears) == 0 and len(relevant_boss_clears) == 0:
        return False

    if len(relevant_boss_clears) > 0:
        return True

    clear = relevant_level_clears[0]

    if clear.requirement_count is None:
        return True

    stage_detail = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                  clear.mission_object_name, ctx,
                                                                  clear.stageId, clear.alignmentId,
                                                                  ctx.override_settings)

    is_objective_sanity = ShadowUtils.GetObjectiveSanityFlag(ctx, stage_detail)

    if not is_objective_sanity or\
        ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear:
        return True

    stage_detail = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                             clear.mission_object_name, ctx,
                                                             clear.stageId, clear.alignmentId,
                                                             ctx.override_settings)

    max_required = ShadowUtils.getMaxRequired(stage_detail, clear.requirement_count,
        stage, alignment, ctx.override_settings)

    i = [item for item in ctx.items_received if item.item in info and \
         info[item.item].stageId == stage and info[item.item].type == "level_object"
         and info[item.item].alignmentId == alignment]

    if len(i) >= max_required:
        return True

    return False

def complete_completable_levels(ctx):
    location_dict = Locations.GetLocationInfoDict()
    remaining_locations = ctx.missing_locations

    new_clears = []
    uncleared_stages = [ location_dict[l] for l in remaining_locations
                         if l in location_dict and location_dict[l].location_type == Locations.LOCATION_TYPE_MISSION_CLEAR ]

    uncleared_bosses = [location_dict[l].stageId for l in remaining_locations
                        if l in location_dict and location_dict[l].location_type == Locations.LOCATION_TYPE_BOSS]

    story = ctx.shuffled_story_mode
    for mission in uncleared_stages:

        if mission.stageId in Levels.BOSS_STAGES:
            continue

        if not is_level_accessible(ctx, mission.stageId):
            continue

        completable = is_mission_completable(ctx, mission.stageId, mission.alignmentId)
        if not completable:
            continue

        # Check if mission is available
        # Check if mission is clearable

        # Don't autoclear missions if they lead to a stage you haven't accessed via story mode yet
        # Makes tracking easier for getting to that stage
        if ctx.story_mode_available:
            story_path_entry = [ s for s in story if s.start_stage_id == mission.stageId
                                     and s.alignment_id == mission.alignmentId][0]

            routes_to = [ s for s in story if s.end_stage_id == story_path_entry.end_stage_id ]
            if story_path_entry.end_stage_id is None:
                routes_to = [ s for s in routes_to if s.boss == story_path_entry.boss ]

            if story_path_entry.boss is not None:
                r_boss = [b for b in Locations.BossClearLocations if b.stageId == story_path_entry.boss][0]
                boss_location_id, boss_location_name = Locations.GetBossLocationName(r_boss.name, r_boss.stageId)
                u_bosses = [b for b in uncleared_bosses if b == boss_location_id]
                if len(u_bosses) != 0:
                    continue

            available = False
            for route in routes_to:
                is_remaining = [ s for s in uncleared_stages
                                 if s.stageId == route.start_stage_id and s.alignmentId == route.alignment_id ]

                if route.boss is not None:
                    r_boss = [ b for b in Locations.BossClearLocations if b.stageId == route.boss][0]
                    boss_location_id, boss_location_name = Locations.GetBossLocationName(r_boss.name, r_boss.stageId)
                    u_bosses = [ b for b in uncleared_bosses if b == boss_location_id]
                    if len(u_bosses) != 0:
                        continue

                if len(is_remaining) == 0:
                    available = True

            if not available:
                continue

            to_end_boss = [ s for s in story if s.start_stage_id == mission.stageId and s.alignment_id == mission.alignmentId]
            if len(to_end_boss) == 1:
                boss_path = to_end_boss[0]
                if boss_path.boss is not None:
                    r_boss_l = [b for b in Locations.BossClearLocations if b.stageId == boss_path.boss]
                    if len(r_boss_l) == 1:
                        r_boss = r_boss_l[0]
                        boss_location_id, boss_location_name = Locations.GetBossLocationName(r_boss.name, r_boss.stageId)
                        u_bosses = [b for b in uncleared_bosses if b == boss_location_id]
                        if len(u_bosses) != 0:
                            continue
                    else:
                        print("Unable to find boss clear location for", boss_path)

        mission_complete_locations = [ l for l in location_dict.values() if l.stageId == mission.stageId and
                               l.location_type == Locations.LOCATION_TYPE_MISSION_CLEAR
                               and l.locationId in ctx.checked_locations ]

        other_locations = [ l for l in remaining_locations if l in location_dict and location_dict[l].stageId == mission.stageId and
                            location_dict[l].location_type != Locations.LOCATION_TYPE_MISSION_CLEAR and
                            location_dict[l].location_type != Locations.LOCATION_TYPE_TOKEN and
                            location_dict[l].location_type != Locations.LOCATION_TYPE_WARP
                            ]

        if len(mission_complete_locations) > 0 and len(other_locations) == 0:
            new_clears.append(mission.locationId)
            # Mark as completed!
            pass

        auto_clears = HandleLocationAutoclears()
        if mission.locationId in auto_clears and auto_clears[mission.locationId].locationId in ctx.checked_locations:
            new_clears.append(mission.locationId)

    token_clears = []
    for clear in new_clears:
        clear_data = location_dict[clear]
        token_locations = [l for l in remaining_locations if l in location_dict if location_dict[l].stageId == clear_data.stageId and \
                            clear_data.alignmentId == location_dict[l].alignmentId and
                           location_dict[l].location_type == Locations.LOCATION_TYPE_TOKEN ]
        token_clears.extend(token_locations)

    new_clears.extend(token_clears)
    return new_clears





def check_story(ctx):
    story_mode = ctx.shuffled_story_mode
    if ctx.successful_shuffle:
        return
    for story in story_mode:
        if story.start_stage_id is not None:
            index = Levels.ALL_STAGES.index(story.start_stage_id)
            base_pointer = GAME_ADDRESSES.ADDRESS_STORY_ROUTE + (20*4 * index)
            write_pointer = None
            if story.alignment_id == MISSION_ALIGNMENT_DARK:
                write_pointer = base_pointer + (7*4)
            elif story.alignment_id == MISSION_ALIGNMENT_NEUTRAL:
                write_pointer = base_pointer + (10*4)
            elif story.alignment_id == MISSION_ALIGNMENT_HERO:
                write_pointer = base_pointer + (13*4)

            boss_write_pointer = None
            if story.boss is not None:
                boss_index = Levels.ALL_STAGES.index(story.boss)
                boss_base_pointer = GAME_ADDRESSES.ADDRESS_STORY_ROUTE + (20 * 4 * boss_index)
                if story.alignment_id == MISSION_ALIGNMENT_DARK:
                    boss_write_pointer = boss_base_pointer + (7 * 4)
                elif story.alignment_id == MISSION_ALIGNMENT_NEUTRAL:
                    boss_write_pointer = boss_base_pointer + (10 * 4)
                elif story.alignment_id == MISSION_ALIGNMENT_HERO:
                    boss_write_pointer = boss_base_pointer + (13 * 4)

            # if there is a boss in the way, we need to write the boss in instead
            # but need to write to locations to the boss

            if write_pointer is not None and boss_write_pointer is None:
                story_block = Levels.STAGE_TO_STORY_BLOCK[story.end_stage_id]
                new_bytes = story_block.to_bytes(4, byteorder='big')
                writeBytes(write_pointer, new_bytes)
            elif write_pointer is not None and boss_write_pointer is not None:
                story_block = Levels.STAGE_TO_STORY_BLOCK[story.boss]
                new_bytes = story_block.to_bytes(4, byteorder='big')
                writeBytes(write_pointer, new_bytes)

                if story.end_stage_id is not None:
                    story_block = Levels.STAGE_TO_STORY_BLOCK[story.end_stage_id]
                    new_bytes = story_block.to_bytes(4, byteorder='big')
                    writeBytes(boss_write_pointer, new_bytes)
                else:
                    # Hopefully will end story mode as these are final stages into credits?
                    pass
            else:
                print("Whoops?")
        else:
            new_bytes = story.end_stage_id.to_bytes(3, byteorder='big')
            writeBytes(GetGameAddress(ctx, GAME_ADDRESSES.FIRST_STORY_MODE_STAGE_ADDRESS), new_bytes)


    ctx.successful_shuffle = True



def check_cheats():
    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    new_value = 0xFFFFFFFF
    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES, new_bytes)

    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES+4, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES+4, new_bytes)

    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES + 8, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.ADDRESS_WATCHED_CUTSCENES + 8, new_bytes)

    ##
    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CENTRAL_CITY_TIMER, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    new_value = 0xFFFF
    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.CENTRAL_CITY_TIMER, new_bytes)

    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.COSMIC_FALL_TIMER, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    new_value = 0xFFFF
    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.COSMIC_FALL_TIMER, new_bytes)

    current_value_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.LAST_WAY_TIMER, 4)
    current_value = int.from_bytes(current_value_bytes, byteorder='big')

    new_value = 0xFFFF
    if current_value != new_value:
        new_bytes = new_value.to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.LAST_WAY_TIMER, new_bytes)


def CheckAutoWarps(ctx):
    found_warps = []

    if not ctx.story_mode_available or not ctx.secret_story_progression:
        return []

    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = Locations.GetAllLocationInfo()

    story = ctx.shuffled_story_mode
    for path in story:
        if path.start_stage_id is None:
            continue

        start_warp_location = [w for w in warp_locations if w.stageId == path.start_stage_id]
        if len(start_warp_location) != 1 or start_warp_location[0].locationId not in ctx.checked_locations:
            continue

        clear_location = [ c for c in clear_locations if c.alignmentId == path.alignment_id and
                           path.start_stage_id == c.stageId ]
        if len(clear_location) != 1 or clear_location[0].locationId not in ctx.checked_locations:
            continue

        # If the stage has been cleared, either a previous bug
        # Or a collect has changed the behaviour

        end_path_location = path.end_stage_id

        if path.boss is not None:
            boss_warp_location = [w for w in warp_locations if w.stageId == path.boss]
            if len(boss_warp_location) == 1 and boss_warp_location[0].locationId not in ctx.checked_locations:
                if boss_warp_location[0].locationId not in found_warps:
                    found_warps.append(boss_warp_location[0].locationId)

            boss_clear_location = [c for c in boss_locations if path.boss == c.stageId]
            if len(boss_clear_location) != 1 or boss_clear_location[0].locationId not in ctx.checked_locations:
                # Disable the end path if it isn't accessible
                end_path_location = None

        # Don't check the end path if there isn't one
        if end_path_location is not None:
            end_warp_location = [w for w in warp_locations if w.stageId == end_path_location]
            if len(end_warp_location) == 1 and end_warp_location[0].locationId not in ctx.checked_locations:
                if end_warp_location[0].locationId not in found_warps:

                    if is_level_accessible(ctx,end_warp_location[0].stageId, story=True):
                        found_warps.append(end_warp_location[0].locationId)

    return found_warps

# When not in a level, check the level
async def check_level_status(ctx):

    # If in a level, return the level ID

    # Sync level unlocked status
    # Add available levels to save-data

    last_accessible_levels = ctx.last_accessible_levels.copy()

    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = Locations.GetAllLocationInfo()

    # Check mission clears and keys and clear checks from those not known to the server
    info = Items.GetItemLookupDict()
    i = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "level_unlock"
         ]

    levels_to_unlock = [ info[level[0].item].stageId for level in i ]
    ctx.available_levels.extend(levels_to_unlock)

    CheckGateConditions(ctx)

    remove = []
    for ix in i:
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    item_behaviour_changed = False
    if ctx.available_levels != last_accessible_levels or not ctx.select_initialised:
        item_behaviour_changed = True
        ctx.select_initialised = True

    # Set working address to set accessibility to levels
    # This data should save when the game is saved
    # Consider locking levels the player does not have access to

    #if 100 not in ctx.available_levels:
    #    ctx.available_levels.append(100)

    if item_behaviour_changed:
        for level in LEVEL_ID_TO_LEVEL.keys():
            if level in ctx.available_levels:
                new_count = 1
            else:
                new_count = 0

            address = GetStageUnlockAddresses()[level]
            current_value_bytes = dolphin_memory_engine.read_bytes(address, 4)
            current_value = int.from_bytes(current_value_bytes, byteorder='big')

            if ctx.level_buffer is not None and ctx.level_buffer == level:
                if current_value != 0:
                    continue

            if current_value != new_count:
                new_bytes = new_count.to_bytes(4, byteorder='big')
                writeBytes(address, new_bytes)

                if level in Levels.FINAL_BOSSES:
                    boss_level = level

                    final_boss_unlock_address = GetFinalBossAdditionalUnlock()[boss_level]
                    extra_count = 1
                    new_extra_bytes = extra_count.to_bytes(4, byteorder='big')
                    writeBytes(final_boss_unlock_address, new_extra_bytes)

        ctx.last_accessible_levels = ctx.available_levels.copy()

    found_emerald_items = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "emerald"
    ]

    remove = []
    for ix in found_emerald_items:
        item_no = ix[0].item
        if item_no not in ctx.emeralds:
            ctx.emeralds.append(item_no)
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    found_token_items = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "Token"
    ]

    remove = []
    for ix in found_token_items:
        item_no = ix[0].item
        ctx.tokens.append((item_no, info[ix[0].item]))
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    # need to handle receiving stage items here too

    force_retry = item_behaviour_changed

    current_screen_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.MENU_ENUM, 4)
    current_screen = int.from_bytes(current_screen_bytes, byteorder='big')

    if current_screen != MenuOptions.NotInMenu:
        extra_messages = CheckAutoWarps(ctx)

        if len(extra_messages) > 0:
            message = [{"cmd": 'LocationChecks', "locations": extra_messages}]
            await ctx.send_msgs(message)
            check = [l for l in HandleLocationAutoclears() if l in extra_messages]
            ctx.level_state["temp"] = True

    current_level_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_CURRENT_LEVEL, 2)
    current_level = int.from_bytes(current_level_bytes, byteorder='big')

    if current_level == 0:

        # Reset the level state when not in a level
        if (len(ctx.level_state) != 0 or force_retry or
                ("temp" in ctx.level_state and ctx.level_state["temp"])):
            ctx.level_state = {}
            ctx.level_keys = []
            ctx.music = None
            print("Set music to None")
            ctx.key_restore_complete = False
            if ctx.auto_clear_missions:
                new_messages = complete_completable_levels(ctx)
            else:
                new_messages = []

            #logger.debug("Detected screen %d", current_screen)

            if len(new_messages) > 0:
                message = [{"cmd": 'LocationChecks', "locations": new_messages}]
                await ctx.send_msgs(message)
                check = [ l for l in HandleLocationAutoclears() if l in new_messages ]
                ctx.level_state["temp"] = True

        return None
    else:

        level_status_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_LEVEL_STATUS, 4)
        level_status_value = int.from_bytes(level_status_bytes, byteorder='big')

        if level_status_value in [LevelStatusOptions.LoadingFirstTime, LevelStatusOptions.NotInLevel,
                                  LevelStatusOptions.Loading,
                                  LevelStatusOptions.Saving,
                                  LevelStatusOptions.Other, LevelStatusOptions.Restarting]:

            ctx.level_status = None
            ctx.junk_delay = 0
            return current_level

        LSValues = [v for k, v in LevelStatusOptions.__dict__.items() if not k.startswith('__') and not callable(v)]

        if level_status_value not in LSValues:
            logger.error("Unknown level status value: %d", level_status_value)
            pass

        ctx.level_status = level_status_value

        selected_level_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_SELECT_LEVEL, 2)
        selected_level = int.from_bytes(selected_level_bytes, byteorder='big')

        in_story_mode = False
        if selected_level != current_level and ctx.last_level != current_level:
            in_story_mode = True

        # If select mode only, show error when on assumed story mode
        if not ctx.story_mode_available and in_story_mode and current_level not in Levels.LAST_STORY_STAGES:
            ctx.last_level = current_level
            logger.error("Currently in story mode, your options require playing in Select Mode.")
            return None

        if (ctx.last_level is None or current_level != ctx.last_level) and current_level in Levels.LEVEL_ID_TO_LEVEL:
            if ctx.info_logging and ctx.boss_delay == 0:
                logger.info("Now in level: %s", Levels.LEVEL_ID_TO_LEVEL[current_level])
            ctx.last_level = current_level

            if in_story_mode:
                warp_location = [ w for w in warp_locations if w.stageId == current_level]
                if len(warp_location) == 1 and warp_location[0].locationId not in ctx.checked_locations:
                    messages = [warp_location[0].locationId]
                    message = [{"cmd": 'LocationChecks', "locations": messages}]
                    await ctx.send_msgs(message)

                if current_level == BOSS_DEVIL_DOOM and not IsEndGameEnabled(ctx):

                    if level_status_value != LevelStatusOptions.Active:
                        ctx.boss_delay = 1
                        ctx.last_level = None
                        return None

                    current_rings_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.RINGS_ADDRESS, 4)
                    current_rings = int.from_bytes(current_rings_bytes, byteorder="big")

                    if ctx.boss_delay == 0:
                        ctx.last_level = None
                        if 0 < current_rings < 50:
                            logger.info("You do not have the required items to fight the final boss")
                            logger.info("Set rings to 0")
                            new_rings = 0
                            new_bytes = new_rings.to_bytes(4, byteorder='big')
                            writeBytes(GAME_ADDRESSES.RINGS_ADDRESS, new_bytes)
                            ctx.boss_delay = 3
                    else:
                        ctx.boss_delay -= 1
                        ctx.last_level = None

                    return None

            this_stage_unlock = [unlock for unlock in ctx.handled if unlock[0].item in info and \
             info[unlock[0].item].stageId == current_level and info[unlock[0].item].type == "level_unlock"]

            if len(this_stage_unlock) == 0:
                #message = [{"cmd": 'LocationChecks', "locations": messages}]
                #await ctx.send_msgs(message)
                # Give the player the stage unlock (for story convinence)
                pass


        # Check if level has loaded

        return current_level


COMPLETE_FLAG_OFF = 0
COMPLETE_FLAG_OFF_SET = 1
COMPLETE_FLAG_READY = 2
COMPLETE_FLAG_ON_SET = 3

COMPLETE_FLAG_ON_MANUAL = 4


async def disable_weapon(ctx):

    if ctx.level_status == LevelStatusOptions.Paused or ctx.level_status == LevelStatusOptions.InCutscene:
        return

    current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.DARK_GAUGE_ADDRESS, 4)
    current_dark_gauge = int.from_bytes(current_dark_gauge_bytes, byteorder="big")

    current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.HERO_GAUGE_ADDRESS, 4)
    current_hero_gauge = int.from_bytes(current_hero_gauge_bytes, byteorder="big")
    time.sleep(0.1)

    current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.DARK_GAUGE_ADDRESS, 4)
    current_dark_gauge2 = int.from_bytes(current_dark_gauge_bytes, byteorder="big")

    current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.HERO_GAUGE_ADDRESS, 4)
    current_hero_gauge2 = int.from_bytes(current_hero_gauge_bytes, byteorder="big")

    # Sleep not preferable, required to ensure game processes end of dark/hero gauge in case of active power Shadow
    # Which would then not drop the weapon!

    if current_hero_gauge2 < current_hero_gauge or \
        current_dark_gauge2 < current_dark_gauge:
        new_bytes = int(0).to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.DARK_GAUGE_ADDRESS, new_bytes)

        new_bytes = int(0).to_bytes(4, byteorder='big')
        writeBytes(GAME_ADDRESSES.HERO_GAUGE_ADDRESS, new_bytes)

        time.sleep(0.5)

        ctx.hero_gauge_buffer += current_hero_gauge
        ctx.dark_gauge_buffer += current_dark_gauge

        ctx.junk_delay += 25

    new_bytes = int(0).to_bytes(4, byteorder='big')
    writeBytes(GAME_ADDRESSES.CURRENT_AMMO_ADDRESS, new_bytes)


def number_to_bit_array(number):
    # Convert the number to binary and remove the '0b' prefix
    binary_string = bin(number)[2:]
    # Convert each character in the binary string to an integer
    bit_array = [int(bit) for bit in binary_string]
    return bit_array


async def handle_special_weapons(ctx, info, weapons_to_handle):
    new_messages = []

    weapon_dict = Weapons.GetWeaponDict()
    special_weapons_info = Items.GetSpecialWeapons()

    rifle_components = [info[unlock[0].item] for unlock in ctx.handled if unlock[0].item in info \
                       and info[unlock[0].item].type == "Rifle Component"]

    rifle_components_new = [info[unlock[0].item] for unlock in weapons_to_handle if unlock[0].item in info \
                           and info[unlock[0].item].type == "Rifle Component"]

    rifle_components.extend(rifle_components_new)

    rifle_complete = True
    for component in Items.GetRifleComponents():
        matches = [ c for c in rifle_components if c.name == component.name ]
        if len(matches) == 0:
            rifle_complete = False

    special_weapons = [info[unlock[0].item] for unlock in ctx.handled if unlock[0].item in info \
                       and info[unlock[0].item].type == "Weapon" and
                       Weapons.WeaponAttributes.SPECIAL in weapon_dict[info[unlock[0].item].name].attributes]

    special_weapons_new = [info[unlock[0].item] for unlock in weapons_to_handle if unlock[0].item in info \
                           and info[unlock[0].item].type == "Weapon" and
                           Weapons.WeaponAttributes.SPECIAL in weapon_dict[info[unlock[0].item].name].attributes]

    special_weapons.extend(special_weapons_new)

    weapon_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    for special_weapon in special_weapons_info:
        matching = [w for w in special_weapons if w.name == special_weapon.name or
                    w.name == "Weapon:" + special_weapon.name]
        if len(matching) >= 1:
            weapon_value[i] = 1
        if len(matching) >= 2 and i + 1 < len(weapon_value):
            weapon_value[i + 1] = 1
        i += 2

    if rifle_complete:
        if weapon_value[-1] != 1:
            new_messages.append(LOCATION_ID_SHADOW_RIFLE_COMPLETE)
            weapon_value[-1] = 1

    weapon_value.reverse()

    weapon_value_to_write = int("".join([str(w) for w in weapon_value]), 2)

    current_special_weapons = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.SPECIAL_WEAPONS_ADDRESS, 2)
    current_special_weapons_value = int.from_bytes(current_special_weapons, byteorder="big")

    current_special_weapons_approved = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.SPECIAL_WEAPONS_ADDRESS_APPROVED, 2)
    current_special_weapons_approved_value = int.from_bytes(current_special_weapons_approved, byteorder="big")

    bits = number_to_bit_array(current_special_weapons_approved_value)
    while len(bits) < len(weapon_value):
        bits.insert(0, 0)

    while len(bits) > len(weapon_value):
        bits.pop(0)

    for index in range(0, len(bits)):
        w = weapon_value[index]
        b = bits[index]

        if w == 1 and b == 1:
            set_to = 1
        else:
            set_to = 0

        bits[index] = set_to

    approved_weapon_value_to_write = int("".join([str(w) for w in bits]), 2)

    if approved_weapon_value_to_write != current_special_weapons_approved_value:
        new_approved_bytes = approved_weapon_value_to_write.to_bytes(2, byteorder='big')
        writeBytes(GAME_ADDRESSES.SPECIAL_WEAPONS_ADDRESS_APPROVED, new_approved_bytes)

    if current_special_weapons_value != weapon_value_to_write:
        new_bytes = weapon_value_to_write.to_bytes(2, byteorder='big')
        logger.info(f"Write special weapons {weapon_value_to_write}")
        writeBytes(GAME_ADDRESSES.SPECIAL_WEAPONS_ADDRESS, new_bytes)

    return new_messages

async def check_weapons(ctx, current_level):
    info = Items.GetItemLookupDict()

    weapons_to_handle = [unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
         info[unlock[0].item].type == "Weapon" or info[unlock[0].item].type == "Rifle Component" or
                         info[unlock[0].item].type == "WeaponGroup"]

    newly_handled = []
    newly_handled.extend(weapons_to_handle)

    mission_clear_locations, mission_locations, end_location, enemysanity_locations, \
        checkpointsanity_locations, charactersanity_locations, \
        token_locations, keysanity_locations, weaponsanity_locations, boss_locations,\
        warp_locations, object_locations = Locations.GetAllLocationInfo()

    messages = []

    weapon_messages = await handle_special_weapons(ctx, info, weapons_to_handle)
    messages.extend(weapon_messages)

    special_weapons_info = Items.GetSpecialWeapons()

    if len(weapons_to_handle) > 0:
        remove = []
        for r in newly_handled:
            ctx.handled.append(r)
            remove.append(r)

        for r in remove:
            ctx.items_to_handle.remove(r)

    if ctx.weapon_sanity_unlock or ctx.weapon_sanity_hold_option > 0:
        current_weapon_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CURRENT_WEAPON_ID_ADDRESS, 4)
        current_weapon_id = int.from_bytes(current_weapon_bytes, byteorder="big")

        weapon_dict = Weapons.GetWeaponDict()
        weapon_dict_by_id = Weapons.GetWeaponDictById()
        special_weapons_lower = []
        for special in special_weapons_info:
            if special.name in weapon_dict and Weapons.WeaponAttributes.SPECIAL in weapon_dict[special.name].attributes \
                    and special.name != "Shadow Rifle":
                special_weapons_lower.append(weapon_dict[special.name].game_id - 1)
                pass
            elif ("Weapon:" + special.name in weapon_dict and Weapons.WeaponAttributes.SPECIAL in
                  weapon_dict["Weapon:" + special.name].attributes and special.name != "Shadow Rifle"):
                special_weapons_lower.append(weapon_dict["Weapon:" + special.name].game_id - 1)
                pass

        if len([l for l in special_weapons_lower if l == current_weapon_id]) > 0:
            current_weapon_id = current_weapon_id + 1

        if current_weapon_id == 0:
            current_weapon_id = None

        if ctx.weapon_sanity_unlock:
            allowed_weapons = [weapon_dict[info[unlock[0].item].name] for unlock in ctx.handled if unlock[0].item in info and \
                                 info[unlock[0].item].type == "Weapon"]

            allowed_weapon_groups = [info[unlock[0].item].name for unlock in ctx.handled if unlock[0].item in info and \
                                 info[unlock[0].item].type == "WeaponGroup"]

            for group in allowed_weapon_groups:
                group_weapons = Weapons.WeaponGroups[group]
                matching_weapons = [ w for w in Weapons.WEAPON_INFO if w.game_id in group_weapons]
                allowed_weapons.extend(matching_weapons)

            allowed_weapons_by_id = {}
            for a in allowed_weapons:
                allowed_weapons_by_id[a.game_id] = a

            valid_weapon_ids = [ weapon.game_id for weapon in weapon_dict.values() ]
            weapons_by_stage = Weapons.GetWeaponByStageDict()

            if current_weapon_id is None:
                pass
            elif current_weapon_id not in valid_weapon_ids:
                logger.error("Unknown weapon held by player: %d", current_weapon_id)
                ctx.last_weapon = current_weapon_id
                current_weapon_id = None

            elif current_level in weapons_by_stage and current_weapon_id not in weapons_by_stage[current_level]\
                    and ctx.last_weapon != current_weapon_id and \
                    not Weapons.WeaponAttributes.SPECIAL in weapon_dict_by_id[current_weapon_id].attributes:

                if current_weapon_id in Objects.GetShadowBonusWeapons(current_level):
                    logger.error("Bonus Shadow Box item obtained!")
                    await disable_weapon(ctx)
                    current_weapon_id = None
                else:
                    logger.error("Unknown weapon (%s) for this stage. Please report this.", weapon_dict_by_id[current_weapon_id].name)
                    await disable_weapon(ctx)
                    current_weapon_id = None

            elif current_weapon_id not in allowed_weapons_by_id.keys() and ctx.last_weapon != current_weapon_id:
                if ctx.weapon_delay is not None:
                    if ctx.weapon_delay == 0:
                        ctx.weapon_delay = None
                    else:
                        ctx.weapon_delay -= 1
                else:
                    logger.error("You have not unlocked the %s", weapon_dict_by_id[current_weapon_id].name)
                    ctx.weapon_delay = 5
                await disable_weapon(ctx)
                ctx.last_weapon = None

                if ctx.weapon_sanity_hold_option == WeaponsanityHold.option_on:

                    # Give the check, remove the check later
                    current_weapon = weapon_dict_by_id[current_weapon_id]
                    weapon_locations = [l.locationId for l in weaponsanity_locations if
                                        l.other == current_weapon.name and \
                                        l.locationId not in ctx.handled and l.locationId not in ctx.checked_locations]
                    if len(weapon_locations) > 0:
                        logger.error("But the check for  %s must be given", weapon_dict_by_id[current_weapon_id].name)
                        messages.extend(weapon_locations)
                current_weapon_id = None

        if current_weapon_id is not None:
            check_ammo_boost = False
            if ctx.weapon_sanity_hold_option in \
                (WeaponsanityHold.option_unlocked, WeaponsanityHold.option_on):

                if ctx.last_weapon != current_weapon_id:
                    #logger.info("Now holding weapon: %s", weapon_dict_by_id[current_weapon_id].name)
                    ctx.last_weapon = current_weapon_id
                    check_ammo_boost = True

                current_weapon = weapon_dict_by_id[current_weapon_id]
                weapon_locations = [ l.locationId for l in weaponsanity_locations if l.other == current_weapon.name and \
                                     l.locationId not in ctx.handled ]
                messages.extend(weapon_locations)

            if check_ammo_boost or ctx.last_weapon != current_weapon_id:
                if current_weapon_id in ctx.ammo_boosts and ctx.ammo_boosts[current_weapon_id] != 0:
                    value = ctx.ammo_boosts[current_weapon_id]
                    ctx.ammo_boosts[current_weapon_id] = 0

                    current_ammo_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CURRENT_AMMO_ADDRESS, 4)
                    current_ammo = int.from_bytes(current_ammo_bytes, byteorder="big")
                    if current_ammo < 10:
                        new_ammo = 50 * value
                    else:
                        new_ammo = current_ammo * 2 * value

                    new_bytes = new_ammo.to_bytes(4, byteorder='big')
                    writeBytes(GAME_ADDRESSES.CURRENT_AMMO_ADDRESS, new_bytes)



    if len(messages) > 0:
        message = [{"cmd": 'LocationChecks', "locations": messages}]
        await ctx.send_msgs(message)

def give_warp_keys():
    # Give warp keys if a story stage is complete and the boss inbetween if set, only run when on Select?


    pass


def get_last_index_storage_location(ctx):
    if ctx.level_buffer is None:
        return None
    return [ l[1] for l in GetStageUnlockAddresses().items() if l[0] == ctx.level_buffer ][0]

def get_last_index(ctx):
    if ctx.last_save_index is None:
        decided_last_index_address = get_last_index_storage_location(ctx)
        if decided_last_index_address is None:
            return -1

        current_potential_bytes = dolphin_memory_engine.read_bytes(decided_last_index_address, 4)
        current_potential = int.from_bytes(current_potential_bytes[1:3], byteorder="big")
        ctx.last_save_index = current_potential

    #print("GLI", ctx.last_save_index)

    return ctx.last_save_index


def get_last_index_message(ctx):
    if ctx.last_save_index is None:
        decided_last_index_address = get_last_index_storage_location(ctx)
        if decided_last_index_address is None:
            return -1

        current_potential_bytes = dolphin_memory_engine.read_bytes(decided_last_index_address, 4)
        current_potential = int.from_bytes(current_potential_bytes[1:3], byteorder="big")
        ctx.last_save_index = current_potential

    if ctx.last_save_index_message is None:
        ctx.last_save_index_message = ctx.last_save_index

    print("GLIM", ctx.last_save_index_message)

    return ctx.last_save_index_message


def set_last_index(ctx, new_value):
    decided_last_index_address = get_last_index_storage_location(ctx)
    if decided_last_index_address is None:
        print("unable to set last index", ctx.level_buffer)
        return

    current_potential_bytes = list(dolphin_memory_engine.read_bytes(decided_last_index_address, 4))
    bytes_to_manip = list(new_value.to_bytes(2, byteorder="big"))
    current_potential_bytes[1] = bytes_to_manip[0]
    current_potential_bytes[2] = bytes_to_manip[1]
    potential_bytes = bytes(current_potential_bytes)
    writeBytes(decided_last_index_address, potential_bytes)
    ctx.last_save_index = new_value

def set_last_index_message(ctx, new_value):
    # Check not to overwrite a higher value
    if ctx.last_save_index is None:
        ctx.last_save_index = 0

    if ctx.last_save_index <= new_value:
        set_last_index(ctx, new_value)

    ctx.last_save_index_message = new_value

def should_send_ring_link(ctx, death):
    should_send = True
    if ctx.ring_link != Options.RingLink.option_unsafe:
        if death:
            should_send = False
        elif ctx.last_level == Levels.STAGE_CIRCUS_PARK:
            should_send = False
        elif ctx.last_level == Levels.BOSS_DEVIL_DOOM:
            should_send = False
        elif ctx.restart:
            should_send = False

    return should_send

async def handle_ring_link(ctx, level, death):
    ring_link = False
    old_tags = ctx.game_tags.copy()
    if ctx.poison_traps > 0:
        return
    if ctx.ring_link != Options.RingLink.option_off:
        if "RingLink" not in ctx.game_tags:
            ctx.game_tags.append("RingLink")
        ring_link = True
    else:
        ctx.game_tags = []
    if old_tags != ctx.game_tags and ctx.server and not ctx.server.socket.closed:
        await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.game_tags}])

    if level is None or not ring_link:
        ctx.previous_rings = None
        return

    should_send = should_send_ring_link(ctx, death)

    difference = 0
    if should_send:
        previous = ctx.previous_rings
        current_rings_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.RINGS_ADDRESS, 4)
        current_rings = int.from_bytes(current_rings_bytes, byteorder="big")

        if current_rings == 0 and ctx.previous_rings is not None and ctx.previous_rings > 20:
            # count as death scenario rather
            pass
        elif ctx.previous_rings is None:
            ctx.previous_rings = current_rings
        else:
            ctx.previous_rings = current_rings
            difference = current_rings - previous
            #if difference != 0:
                #print("ring diff=", difference)
    else:
        ctx.previous_rings = None

    if difference != 0:
        msg = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": {
                "time":  time.time(),
                "source": ctx.instance_id,
                "amount": difference
            },
            "tags": ctx.game_tags
        }

        await ctx.send_msgs([msg])

def handle_received_rings(ctx, data):
    amount = data["amount"]
    source = data["source"]

    if source == ctx.instance_id:
        return

    should_receive = should_send_ring_link(ctx, False)

    if should_receive:
        ctx.ring_link_rings += amount
        ctx.previous_rings = None


async def check_junk(ctx, current_level, death):
    info = Items.GetItemLookupDict()

    if ctx.level_status != LevelStatusOptions.Active:
        return

    last_index = get_last_index(ctx)

    filler = [(unlock,info[unlock[0].item]) for unlock in ctx.items_to_handle if unlock[0].item in info and \
        info[unlock[0].item].classification == ItemClassification.filler and unlock[1] > last_index ]

    traps = [(unlock,info[unlock[0].item]) for unlock in ctx.items_to_handle if unlock[0].item in info and \
        info[unlock[0].item].classification == ItemClassification.trap and unlock[1] > last_index ]

    if ctx.junk_delay > 0 and len(traps) == 0:
        if ctx.level_status not in [ LevelStatusOptions.Active, LevelStatusOptions.Paused,
                                     LevelStatusOptions.InCutscene]:
            ctx.junk_delay = 0
        else:
            ctx.junk_delay -= 1
            return

    latest_index = None

    maxable_items = []
    if len(filler) > 0:
        maxable_items.extend(filler)

    if len(traps) > 0:
        maxable_items.extend(traps)

    if len(maxable_items) > 0:
        latest_index = max([ u[0][1] for u in maxable_items])

    filler_nothing = [ f for f in filler if f[1].name == Items.Junk.NothingJunk]
    filler_gauge_dark = [ f for f in filler if f[1].type == "gauge" and f[1].alignmentId == MISSION_ALIGNMENT_DARK]
    filler_gauge_hero = [ f for f in filler if f[1].type == "gauge" and f[1].alignmentId == MISSION_ALIGNMENT_HERO]
    filler_rings = [ f for f in filler if f[1].type == "rings"]
    filler_ammo_boosts = [ f for f in filler if f[1].type == "ammoboost"]

    ammo_traps = [ a for a in traps if a[1].type == "ammotrap" ]
    poison_traps = [a for a in traps if a[1].type == "poisontrap"]
    checkpoint_traps = [a for a in traps if a[1].type == "checkpointtrap" ]

    newly_handled = []
    newly_handled.extend([f[0] for f in filler_nothing])

    if len(ammo_traps) > 0:
        print("add ammo traps")
        ctx.ammo_traps += len(ammo_traps)
        newly_handled.extend([u[0] for u in ammo_traps])

    if len(poison_traps) > 0:
        print("add poison traps")
        ctx.poison_traps += len(poison_traps)
        newly_handled.extend([u[0] for u in poison_traps])

    if len(checkpoint_traps) > 0:
        print("add check traps")
        ctx.checkpoint_traps += len(checkpoint_traps)
        newly_handled.extend([u[0] for u in checkpoint_traps])

    if len(filler_ammo_boosts) > 0:
        for boost in filler_ammo_boosts:
            weapon_id = boost[1].value
            if weapon_id not in ctx.ammo_boosts:
                ctx.ammo_boosts[weapon_id] = 0
            ctx.ammo_boosts[weapon_id] += 1

        newly_handled.extend([u[0] for u in filler_ammo_boosts])

    RING_LIMIT = 999
    GAUGE_LIMIT = 30000

    ring_link_available = should_send_ring_link(ctx, death)

    if (len(filler_rings) > 0 or ctx.ring_link_rings != 0) and ring_link_available :
        current_rings_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.RINGS_ADDRESS, 4)
        current_rings = int.from_bytes(current_rings_bytes, byteorder="big")
        rings_changed = False
        for ringJunk in filler_rings:
            if current_rings >= RING_LIMIT:
                logger.info("Ring limit has been reached")
                break

            if current_rings + ringJunk[1].value >= RING_LIMIT:
                logger.info("Ring limit has been reached")
                continue

            current_rings += ringJunk[1].value
            newly_handled.append(ringJunk[0])
            rings_changed = True

        if ctx.ring_link_rings != 0 and ctx.ring_link_rings is not None:
            rings_changed = True
            current_rings += ctx.ring_link_rings
            if current_rings < 0:
                current_rings = 0
            ctx.ring_link_rings = 0

        if rings_changed:
            new_bytes = current_rings.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.RINGS_ADDRESS, new_bytes)

    if len(filler_gauge_hero) > 0:
        for gaugeJunk in filler_gauge_hero:
            #print("add hero gauge:", ctx.hero_gauge_buffer, gaugeJunk[1].value)
            ctx.hero_gauge_buffer += gaugeJunk[1].value
            newly_handled.append(gaugeJunk[0])

    if ctx.hero_max_meter > 0:
        ctx.hero_max_meter -= 10

    if ctx.dark_max_meter > 0:
        ctx.dark_max_meter -= 10

    if ctx.hero_gauge_buffer > 0:

        current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.HERO_GAUGE_ADDRESS, 4)
        current_hero_gauge = int.from_bytes(current_hero_gauge_bytes, byteorder="big")

        increase = GAUGE_LIMIT - current_hero_gauge
        if ctx.hero_gauge_buffer < increase:
            increase = ctx.hero_gauge_buffer

        if increase > 1000:
            increase = 1000

        now = datetime.now()

        if ctx.hero_cooldown is not None and now > ctx.hero_cooldown:
            ctx.hero_cooldown = None

        if ctx.hero_cooldown is not None:
            pass
        elif ctx.hero_gauge_buffer > 100 and increase < 100 \
            and ctx.hero_gauge_last == current_hero_gauge:
            pass
        else:
            #print("gauge diff", ctx.hero_gauge_buffer, increase, ctx.hero_max_meter)
            ctx.hero_gauge_buffer -= increase

            ctx.hero_max_meter += increase
            if ctx.hero_max_meter > 60000:
                cooldown_until = now + timedelta(seconds=75)
                ctx.hero_cooldown = cooldown_until
                ctx.hero_max_meter = 0

            new_hero_value = current_hero_gauge + increase
            #print("new hero", new_hero_value)
            new_bytes = new_hero_value.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.HERO_GAUGE_ADDRESS, new_bytes)

        ctx.hero_gauge_last = current_hero_gauge

    if len(filler_gauge_dark) > 0:
        for gaugeJunk in filler_gauge_dark:
            ctx.dark_gauge_buffer += gaugeJunk[1].value
            newly_handled.append(gaugeJunk[0])

    if ctx.dark_gauge_buffer > 0:
        current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.DARK_GAUGE_ADDRESS, 4)
        current_dark_gauge = int.from_bytes(current_dark_gauge_bytes, byteorder="big")

        increase = GAUGE_LIMIT - current_dark_gauge
        if ctx.dark_gauge_buffer < increase:
            increase = ctx.dark_gauge_buffer

        if increase > 1000:
            increase = 1000

        now = datetime.now()

        if ctx.dark_cooldown is not None and now > ctx.dark_cooldown:
            ctx.dark_cooldown = None

        if ctx.dark_cooldown is not None:
            pass
        elif ctx.dark_gauge_buffer > 100 and increase < 100 and \
                ctx.dark_gauge_last == current_dark_gauge:
            pass
        else:
            ctx.dark_max_meter += increase
            #print("gauge diff", ctx.dark_gauge_buffer, increase, ctx.dark_max_meter)

            if ctx.dark_max_meter > 60000:
                cooldown_until = now + timedelta(seconds=75)
                ctx.dark_cooldown = cooldown_until
                ctx.dark_max_meter = 0

            ctx.dark_gauge_buffer -= increase

            new_dark_value = current_dark_gauge + increase
            new_bytes = new_dark_value.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.DARK_GAUGE_ADDRESS, new_bytes)

        ctx.dark_gauge_last = current_dark_gauge

    if ctx.checkpoint_traps > 0:
        current_check_choice = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CHECKPOINT_RESPAWN_ID, 4)
        print("current check choice is", current_check_choice)
        if current_check_choice not in [0, 1]:
            checkpoint_data_for_stage = [c for c in Locations.CheckpointLocations if c.stageId == current_level]
            print("checks", checkpoint_data_for_stage)
            active = None
            if len(checkpoint_data_for_stage) > 0:
                print("available level checks")
                total_count = checkpoint_data_for_stage[0].total_count

                check_zero_addr = GAME_ADDRESSES.CHECKPOINT_FLAGS[0]
                checkpoint_status_bytes = dolphin_memory_engine.read_bytes(check_zero_addr, 1)
                checkpoint_zero_status = int.from_bytes(checkpoint_status_bytes, byteorder='big') == 1

                # Checkpoint trap will only trigger on a check that isn't the first/second
                # And also requires the first to be active for detecting restart

                if checkpoint_zero_status:
                    for i in range(1, total_count):
                        print("count=", i)
                        addr = GAME_ADDRESSES.CHECKPOINT_FLAGS[i]
                        checkpoint_status_bytes = dolphin_memory_engine.read_bytes(addr, 1)
                        checkpoint_status = int.from_bytes(checkpoint_status_bytes, byteorder='big') == 1
                        print("check status=", checkpoint_status)
                        if checkpoint_status:
                            print("Yes check status", i)
                            mission_clear_locations, mission_locations, end_location, enemysanity_locations, \
                                checkpointsanity_locations, charactersanity_locations, \
                                token_locations, keysanity_locations, weaponsanity_locations, boss_locations, \
                                warp_locations, object_locations = Locations.GetAllLocationInfo()

                            # Check the check has been completed beforeadding to active
                            if ctx.checkpoint_sanity:
                                locations = [c.locationId for c in checkpointsanity_locations if
                                             c.stageId == current_level and
                                             c.count == (i+1)]

                                checked_locations = [ c for c in ctx.checked_locations if c in locations ]
                                print("locs=", locations, checked_locations, ctx.checked_locations)

                                if len(checked_locations) > 0:
                                    print("active enabled")
                                    active = addr
                            else:
                                print("force active enabled")
                                active = addr

            if active is not None:
                print("Activate checkpoint trap")
                ctx.checkpoint_trap_active = True
                new_respawn_id = 0
                new_bytes = new_respawn_id.to_bytes(4, byteorder='big')
                writeBytes(GAME_ADDRESSES.CHECKPOINT_RESPAWN_ID, new_bytes)
                writeBytes(active, new_bytes)
                ctx.checkpoint_traps -= 1

            pass
    if ctx.poison_traps > 0:
        print("Poison Traps ==", ctx.poison_traps)
        current_rings_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.RINGS_ADDRESS, 4)
        current_rings = int.from_bytes(current_rings_bytes, byteorder="big")

        if current_rings > 0:
            print("Poisons, rings > 0")
            new_rings = current_rings - math.floor(pow(current_rings, 0.3))
            new_bytes = new_rings.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.RINGS_ADDRESS, new_bytes)
            r = random.random()
            if r < (1 / current_rings):
                print("Poison reduce", r)
                ctx.poison_traps -= 1
        elif current_rings == 1:
            print("Poisons, rings == 1")
            new_rings = current_rings - 1
            new_bytes = new_rings.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.RINGS_ADDRESS, new_bytes)
            ctx.poison_traps -= 1
        else:
            print("Not doing anything ith poison trap")

    if ctx.ammo_traps > 0:
        print("Ammo Traps ==", ctx.ammo_traps)
        current_ammo_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CURRENT_AMMO_ADDRESS, 4)
        current_ammo = int.from_bytes(current_ammo_bytes, byteorder="big")

        # TODO: Consider numbers based on the weapon held

        if current_ammo % 10 > 1:
            print("Activate ammo trap")
            if current_ammo > 50:
                new_ammo = 41
            elif current_ammo > 30:
                new_ammo = 21
            else:
                new_ammo = 1
            new_bytes = new_ammo.to_bytes(4, byteorder='big')
            writeBytes(GAME_ADDRESSES.CURRENT_AMMO_ADDRESS, new_bytes)
            ctx.ammo_traps -= 1
        else:
            print("Not doing anything ith ammo trap")

    remove = []
    for r in newly_handled:
        ctx.handled.append(r)
        remove.append(r)

    for r in remove:
        ctx.items_to_handle.remove(r)

    if latest_index is not None:
        set_last_index(ctx, latest_index)


async def clearout_individual_enemies_by_percentage(ctx, stageId):

    if ctx.objective_sanity_system == Options.ObjectiveSanitySystem.option_count_up:
        return

    known_objects = [s for s in Objects.GetDesirableObjectsForStage(stageId)]
    enemy_types = Objects.GetStandardEnemyTypes()
    #logger.error("enemy types=%s: %d", str(enemy_types), len(known_objects))
    if known_objects is None or len(known_objects) == 0:
        return

    relevant_objects = [r for r in known_objects if r.object_type in enemy_types]

    is_objective = False

    checks_to_autoclear = []

    if ctx.enemy_objective_sanity and (stageId, MISSION_ALIGNMENT_DARK) in Objects.STAGE_OBJECT_ITEMS:
        dark_objects = [ d for d in relevant_objects if d.object_type in Objects.STAGE_OBJECT_ITEMS[(stageId, MISSION_ALIGNMENT_DARK)] ]
        if len(dark_objects) > 0:
            dark_subtract = 0
            dark_subtract += sum([ d.count-1 for d in dark_objects if d.count > 1])

            mission = [m for m in MissionClearLocations if m.stageId == stageId and m.alignmentId == MISSION_ALIGNMENT_DARK][0]
            required_count = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                      mission.mission_object_name, ctx,
                                                      mission.stageId, mission.alignmentId,
                                                      ctx.override_settings),
                mission.requirement_count-dark_subtract, mission.stageId, mission.alignmentId, ctx.override_settings)

            completed_dark_objects = [ o for o in dark_objects if GetObjectLocationName(o)[0] in ctx.checked_locations]
            if len(completed_dark_objects) >= required_count:
                incompleted_dark_objects = [ GetObjectLocationName(o)[0] for o in dark_objects if GetObjectLocationName(o)[0] in ctx.missing_locations]
                checks_to_autoclear.extend(incompleted_dark_objects)


    if ctx.enemy_objective_sanity and (stageId, MISSION_ALIGNMENT_HERO) in Objects.STAGE_OBJECT_ITEMS:
        hero_objects = [d for d in relevant_objects if
                        d.object_type in Objects.STAGE_OBJECT_ITEMS[(stageId, MISSION_ALIGNMENT_HERO)]]
        if len(hero_objects) > 0:

            mission = \
            [m for m in MissionClearLocations if m.stageId == stageId and m.alignmentId == MISSION_ALIGNMENT_HERO][0]

            hero_subtract = 0
            hero_subtract += sum([d.count - 1 for d in hero_objects if d.count > 1])

            required_count = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                          mission.mission_object_name, ctx,
                                                          mission.stageId, mission.alignmentId,
                                                          ctx.override_settings),
                mission.requirement_count-hero_subtract, mission.stageId, mission.alignmentId, ctx.override_settings)

            completed_hero_objects = [o for o in hero_objects if GetObjectLocationName(o)[0] in ctx.checked_locations]
            if len(completed_hero_objects) >= required_count:
                incompleted_hero_objects = [GetObjectLocationName(o)[0] for o in hero_objects if
                                            GetObjectLocationName(o)[0] in ctx.missing_locations]
                checks_to_autoclear.extend(incompleted_hero_objects)

    if ctx.enemy_sanity:
        #logger.error("enemy sanity is on")
        egg_objects = [d for d in relevant_objects if
                        d.object_type in Objects.GetEggTypes() ]
        if len(egg_objects) > 0:
            by_type_eggs = [m for m in Locations.GetEnemySanityLocations() if m.stageId == stageId
                    and m.enemyClass == Locations.ENEMY_CLASS_EGG]

            if len(by_type_eggs) > 0:
                by_type_egg = by_type_eggs[0]

                egg_subtract = 0
                if ctx.difficult_enemy_sanity is not None and not ctx.difficult_enemy_sanity:
                    egg_subtract += len([d for d in egg_objects if d.is_hard])

                egg_subtract += sum([d.count - 1 for d in egg_objects if d.count > 1])

                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              by_type_egg.mission_object_name, ctx,
                                                              by_type_egg.stageId, by_type_egg.enemyClass,
                                                              ctx.override_settings),
                    by_type_egg.total_count-egg_subtract, by_type_egg.stageId, by_type_egg.enemyClass, ctx.override_settings)

                completed_egg_objects = [o for o in egg_objects if GetObjectLocationName(o)[0] in ctx.checked_locations]
                if len(completed_egg_objects) >= required_count:
                    incompleted_egg_objects = [GetObjectLocationName(o)[0] for o in egg_objects if
                                                GetObjectLocationName(o)[0] in ctx.missing_locations]
                    checks_to_autoclear.extend(incompleted_egg_objects)

        alien_objects = [d for d in relevant_objects if
                       d.object_type in Objects.GetAlienTypes()]
        #logger.error("alien_objects=%s", str(alien_objects))
        if len(alien_objects) > 0:
            by_type_aliens = [m for m in Locations.GetEnemySanityLocations() if m.stageId == stageId
                           and m.enemyClass == Locations.ENEMY_CLASS_ALIEN]
            if len(by_type_aliens) > 0:
                by_type_alien = by_type_aliens[0]

                alien_subtract = 0
                if ctx.difficult_enemy_sanity is not None and not ctx.difficult_enemy_sanity:
                    alien_subtract += len([d for d in alien_objects if d.is_hard])

                alien_subtract += sum([d.count - 1 for d in alien_objects if d.count > 1])

                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              by_type_alien.mission_object_name, ctx,
                                                              by_type_alien.stageId, by_type_alien.enemyClass,
                                                              ctx.override_settings),
                    by_type_alien.total_count-alien_subtract, by_type_alien.stageId, by_type_alien.enemyClass, ctx.override_settings)

                completed_alien_objects = [o for o in alien_objects if GetObjectLocationName(o)[0] in ctx.checked_locations]

                #logger.error("aliens--%d / %d / %d", required_count, len(completed_alien_objects), len(alien_objects))
                if len(completed_alien_objects) >= required_count:
                    incompleted_alien_objects = [GetObjectLocationName(o)[0] for o in alien_objects if
                                               GetObjectLocationName(o)[0] in ctx.missing_locations]
                    #logger.error("aliens2--%d / %d / %d", len(incompleted_alien_objects))
                    checks_to_autoclear.extend(incompleted_alien_objects)

        gun_objects = [d for d in relevant_objects if
                       d.object_type in Objects.GetGunTypes()]
        if len(gun_objects) > 0:
            by_type_guns = [m for m in Locations.GetEnemySanityLocations() if m.stageId == stageId
                           and m.enemyClass == Locations.ENEMY_CLASS_GUN]

            if len(by_type_guns) > 0:

                by_type_gun = by_type_guns[0]

                gun_subtract = 0
                if ctx.difficult_enemy_sanity is not None and not ctx.difficult_enemy_sanity:
                    gun_subtract += len([d for d in gun_objects if d.is_hard])

                gun_subtract += sum([d.count - 1 for d in gun_objects if d.count > 1])

                required_count = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                              by_type_gun.mission_object_name, ctx,
                                                              by_type_gun.stageId, by_type_gun.enemyClass,
                                                              ctx.override_settings),
                    by_type_gun.total_count-gun_subtract, by_type_gun.stageId, by_type_gun.enemyClass, ctx.override_settings)

                completed_gun_objects = [o for o in gun_objects if GetObjectLocationName(o)[0] in ctx.checked_locations]
                if len(completed_gun_objects) >= required_count:
                    incompleted_gun_objects = [GetObjectLocationName(o)[0] for o in gun_objects if
                                               GetObjectLocationName(o)[0] in ctx.missing_locations]
                    checks_to_autoclear.extend(incompleted_gun_objects)


    if len(checks_to_autoclear) > 0:
        logger.error("Autoclear enemies")
        message = [{"cmd": 'LocationChecks', "locations": checks_to_autoclear}]
        await ctx.send_msgs(message)


async def handle_objects(ctx, current_level):

    time = datetime.now()

    if ctx.level_state is None or len(ctx.level_state.keys()) == 0:
        return

    if "object_status" not in ctx.level_state:
        ctx.level_state["object_status"] = {}

    relevant_objects = Objects.GetDesirableObjectsForStage(current_level)
    if relevant_objects is None or len(relevant_objects) == 0:
        return

    length = Objects.GetSETFileLength(current_level)
    if length is None or length == 0:
        return

    info = Items.GetItemLookupDict()
    mission_clear_locations, mission_locations, end_location, enemysanity_locations, \
        checkpointsanity_locations, charactersanity_locations, \
        token_locations, keysanity_locations, weaponsanity_locations, boss_locations, \
        warp_locations, object_locations = Locations.GetAllLocationInfo()

    force_despawn = 0x04
    spawn_inform = 0x01
    despawn_bytes = force_despawn.to_bytes(1, byteorder='big')
    spawn_bytes = spawn_inform.to_bytes(1, byteorder='big')

    start_address = GAME_ADDRESSES.LEVEL_SET_DATA

    key_sanity = ctx.key_sanity
    object_unlocks = ctx.object_unlocks
    vehicle_sanity = ctx.vehicle_logic
    shadow_box_sanity = ctx.shadow_boxes
    core_sanity = ctx.energy_cores
    beetle_sanity = ctx.gold_beetle_sanity
    door_sanity = ctx.door_sanity
    warp_hole_sanity = ctx.object_warp_holes
    pulley_sanity = ctx.object_pulleys
    rocket_sanity = ctx.object_rockets
    unit_sanity = ctx.object_units
    trail_sanity = ctx.object_light_dashes
    zip_sanity = ctx.object_ziplines

    # Check whether certain items are unlocked

    allowed_pulley = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Pulley"]) > 0

    allowed_zipwire = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Zipwire"]) > 0

    allowed_heal_units = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Heal Units"]) > 0

    allowed_bombs = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                         info[unlock[0].item].name == "Bombs"]) > 0

    allowed_rockets = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Rocket"]) > 0

    allowed_light_dashes = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Air Shoes"]) > 0

    allowed_warp_holes = len([info[unlock[0].item].name for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].name == "Warp Holes"]) > 0

    allowed_vehicles = [info[unlock[0].item] for unlock in ctx.items_to_handle if unlock[0].item in info and \
                       info[unlock[0].item].type == "Vehicle"]

    messages = []

    states_to_add = {}
    states_to_remove = []

    max_index = max([ o.index for o in relevant_objects])

    full_loaded_bytes = dolphin_memory_engine.read_bytes(start_address, (0x2C * (max_index+1)))

    # TODO: Load all object data here in one read rather than within the FOR loop

    for object in relevant_objects:
        object_index = object.index

        spawn_data = start_address + (0x2C * object_index) + 0x20
        base_index = (0x2C * object_index) + 0x20

        spawn_address = spawn_data + 0x03
        spawn_base_byte = base_index + 0x03

        object_type_index = base_index + 0x08

        extra_data_pointer = spawn_data + 0x10

        loaded_bytes = [full_loaded_bytes[spawn_base_byte]]
        #loaded_bytes = dolphin_memory_engine.read_bytes(spawn_base_byte, 1)
        loaded_spawn_data = int.from_bytes(loaded_bytes, byteorder='big')

        loaded_bytes = full_loaded_bytes[object_type_index:object_type_index+2]
        #loaded_bytes = dolphin_memory_engine.read_bytes(object_type, 2)
        loaded_object_type = int.from_bytes(loaded_bytes, byteorder='big')

        expected_type = Objects.GetTypeId(object.object_type)

        if expected_type is not None and Objects.GetTypeId(object.object_type) != loaded_object_type:
            if loaded_object_type == 0x00:
                break
            print("Failed to read type correctly",
                  "Coded Type", Objects.GetTypeId(object.object_type),
                  "Loaded Type", loaded_object_type,
                  "Coded Type", expected_type,
                  "Index", object.index,
                  "Name", object.name)

        # TODO: Only load the extra bytes when needed
        loaded_extra_pointer_bytes = dolphin_memory_engine.read_bytes(extra_data_pointer, 4)
        loaded_extra_pointer = int.from_bytes(loaded_extra_pointer_bytes, byteorder='big')

        object_id, object_name = Names.GetObjectLocationName(object)
        if "spawn_message" in ctx.level_state and ctx.level_state["spawn_message"] and loaded_spawn_data in (0x03, 0x0B):
            if object.index not in ctx.level_state["spawn_messages"]:
                are_locations = [o for o in object_locations if o.locationId in ctx.server_locations
                                 and o.locationId == object_id]
                if len(are_locations) > 0:
                    should_display = len([ o for o in are_locations if o.locationId in ctx.missing_locations]) > 0

                    if should_display:
                        logger.error("%s has spawned", object_name)
                ctx.level_state["spawn_messages"].append(object.index)

        despawn = False
        spawn = False

        if object.object_type == Objects.ObjectType.BOMB:
            object_name = "Object_Bombs"
            if object_unlocks and unit_sanity and not allowed_bombs:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.STANDARD_PULLEY:
            object_name = "Object_Pulley"
            if object_unlocks and pulley_sanity and not allowed_pulley:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.ROCKET:
            object_name = "Object_Rocket"
            if object_unlocks and rocket_sanity and not allowed_rockets:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.WARP_HOLE:
            object_name = "Object_WarpHole"
            if object_unlocks and warp_hole_sanity and not allowed_warp_holes:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.BOMB_SERVER:
            object_name = "Object_Bombs"
            if object_unlocks and unit_sanity and not allowed_bombs:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.HEAL_UNIT:
            object_name = "Object_Heals"
            if object_unlocks and unit_sanity and not allowed_heal_units:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.HEAL_SERVER:
            object_name = "Object_Heals"
            if object_unlocks and unit_sanity and not allowed_heal_units:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.LIGHT_DASH_TRAIL:
            object_name = "Object_LightDash"
            if object_unlocks and trail_sanity and not allowed_light_dashes:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.SPACE_ZIPWIRE:
            object_name = "Object_Zipwire"
            if object_unlocks and zip_sanity and not allowed_zipwire:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.GUN_ZIPWIRE:
            object_name = "Object_Zipwire"
            if object_unlocks and zip_sanity and not allowed_zipwire:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.CIRCUS_ZIPWIRE:
            object_name = "Object_Zipwire"
            if object_unlocks and zip_sanity and not allowed_zipwire:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif object.object_type == Objects.ObjectType.BALLOON_ZIPWIRE:
            object_name = "Object_Zipwire"
            if object_unlocks and zip_sanity and not allowed_zipwire:
                despawn = True
                states_to_add[object_name] = False
            else:
                if object_name in ctx.level_state:
                    spawn = True
                    states_to_remove.append(object_name)

        elif vehicle_sanity and object.object_type == Objects.ObjectType.VEHICLE:
            spawn = False
            spawn_name = None
            if object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_LIFT or \
                object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_LIFT_FAST  :
                spawn_name = "Gun Lift"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.AIR_SAUCER:
                spawn_name = "Air Saucer"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.ARMORED_CAR:
                spawn_name = "Armored Car"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.BLACK_VOLT:
                spawn_name = "Black Volt"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.BLACK_TURRET:
                spawn_name = "Black Turret"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.BLACK_HAWK:
                spawn_name = "Black Hawk"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.CONVERTIBLE:
                spawn_name = "Convertible"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_CANNON:
                spawn_name = "Gun Cannon"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_JUMPER:
                spawn_name = "Gun Jumper"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_MOTORCYCLE:
                spawn_name = "Gun Motorcycle"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.GUN_TURRET:
                spawn_name = "Gun Turret"
            elif object.vehicle == Objects.ObjectType.ObjectTypeVehicle.STANDARD_CAR:
                spawn_name = "Standard Car"

            if spawn_name is None:
                print("Invalid vehicle:", object.vehicle, object.index)
            else:
                despawn = len([x for x in allowed_vehicles if x.name == Names.GetNameForVehicle(spawn_name)]) == 0

                if despawn:
                    states_to_add[spawn_name] = False
                else:
                    if spawn_name in ctx.level_state:
                        print("Force spawn of vehicle as unlocked now", ctx.level_state)
                        spawn = True
                        states_to_remove.append(spawn_name)

        elif vehicle_sanity and object.object_type == Objects.ObjectType.BLACK_WARRIOR and \
                object.vehicle == Objects.ObjectType.ObjectTypeVehicle.AIR_SAUCER:
            OnAirSaucerBytesDiff = 0x5C
            OnAirSaucerBytesAddress = loaded_extra_pointer + OnAirSaucerBytesDiff

            loaded_bytes = dolphin_memory_engine.read_bytes(OnAirSaucerBytesAddress, 4)
            current_riding_saucer_value = int.from_bytes(loaded_bytes, byteorder='big')
            not_on_saucer = 0x00
            on_saucer = 0x01
            if len([ x for x in allowed_vehicles if x.name == Names.GetNameForVehicle("Air Saucer") ]) == 0:
                if current_riding_saucer_value != not_on_saucer:
                    not_on_air_saucer_bytes = not_on_saucer.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, not_on_air_saucer_bytes)
            else:
                if current_riding_saucer_value != on_saucer:
                    on_air_saucer_bytes = on_saucer.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, on_air_saucer_bytes)

        elif vehicle_sanity and object.object_type == Objects.ObjectType.BLACK_VOLT and \
                object.vehicle == Objects.ObjectType.ObjectTypeVehicle.BLACK_VOLT:
            OnAirSaucerBytesDiff = 0x38
            OnAirSaucerBytesAddress = loaded_extra_pointer + OnAirSaucerBytesDiff

            loaded_bytes = dolphin_memory_engine.read_bytes(OnAirSaucerBytesAddress, 4)
            current_riding_saucer_value = int.from_bytes(loaded_bytes, byteorder='big')
            black_volt_despawn_on_kill = 0x10
            black_volt_rideable_on_kill = 0x11

            if len([ x for x in allowed_vehicles if x.name == Names.GetNameForVehicle("Black Volt") ]) == 0:
                if current_riding_saucer_value != black_volt_despawn_on_kill:
                    despawn_on_kill_bytes = black_volt_despawn_on_kill.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, despawn_on_kill_bytes)
            else:
                if current_riding_saucer_value != black_volt_rideable_on_kill:
                    spawn_on_kill_bytes = black_volt_rideable_on_kill.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, spawn_on_kill_bytes)

        elif vehicle_sanity and object.object_type == Objects.ObjectType.BLACK_HAWK and \
                object.vehicle == Objects.ObjectType.ObjectTypeVehicle.BLACK_HAWK:

            OnAirSaucerBytesDiff = 0x38
            OnAirSaucerBytesAddress = loaded_extra_pointer + OnAirSaucerBytesDiff

            loaded_bytes = dolphin_memory_engine.read_bytes(OnAirSaucerBytesAddress, 4)
            current_riding_saucer_value = int.from_bytes(loaded_bytes, byteorder='big')
            black_hawk_despawn_on_kill = 0x00
            black_hawk_rideable_on_kill = 0x01

            if len([ x for x in allowed_vehicles if x.name == Names.GetNameForVehicle("Black Hawk") ]) == 0:
                if current_riding_saucer_value != black_hawk_despawn_on_kill:
                    despawn_on_kill_bytes = black_hawk_despawn_on_kill.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, despawn_on_kill_bytes)
            elif True:
                if current_riding_saucer_value != black_hawk_rideable_on_kill:
                    spawn_on_kill_bytes = black_hawk_rideable_on_kill.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, spawn_on_kill_bytes)

        elif vehicle_sanity and object.object_type == Objects.ObjectType.BLACK_ASSASSIN and \
                object.vehicle == Objects.ObjectType.ObjectTypeVehicle.AIR_SAUCER:
            OnAirSaucerBytesDiff = 0x1C
            OnAirSaucerBytesAddress = loaded_extra_pointer + OnAirSaucerBytesDiff

            loaded_bytes = dolphin_memory_engine.read_bytes(OnAirSaucerBytesAddress, 4)
            current_riding_saucer_value = int.from_bytes(loaded_bytes, byteorder='big')
            appear_type_warp = 0x02
            appear_type_warp_saucer = 0x03
            if len([ x for x in allowed_vehicles if x.name == Names.GetNameForVehicle("Air Saucer") ]) == 0:
                if current_riding_saucer_value != appear_type_warp:
                    not_on_air_saucer_bytes = appear_type_warp.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, not_on_air_saucer_bytes)
            elif True:
                if current_riding_saucer_value != appear_type_warp_saucer:
                    on_air_saucer_bytes = appear_type_warp_saucer.to_bytes(4, byteorder='big')
                    writeBytes(OnAirSaucerBytesAddress, on_air_saucer_bytes)

        if despawn and loaded_spawn_data not in (0x00, 0x04):
            writeBytes(spawn_address, despawn_bytes)

        if not despawn and spawn and loaded_spawn_data in (0x00, 0x04):
            writeBytes(spawn_address, spawn_bytes)

        object_values_complete = []
        # Objects which weirdly change state
        if object.object_type in [Objects.ObjectType.GLYPHIC_CANYON_TEMPLE, Objects.ObjectType.CRYPTIC_CASTLE_LANTERN,
                                  Objects.ObjectType.CREAM, Objects.ObjectType.CHEESE, Objects.ObjectType.SKY_TROOPS_EGG_SHIP,
                                  Objects.ObjectType.SKY_TROOPS_TEMPLE, Objects.ObjectType.MAD_MATRIX_BOMB,
                                  Objects.ObjectType.MAD_MATRIX_TERMINAL, Objects.ObjectType.LAVA_SHELTER_DEFENSE
                                  ]:
            object_values_complete.append(0xB)
            object_values_complete.append(0x8)

        if object.object_type in [
                                  Objects.ObjectType.GUN_SOLDIER
                                  ]:
            object_values_complete.append(0x9)
            #object_values_complete.append(0xB)
            object_values_complete.append(0x8)

        if object.object_type in [
                                  Objects.ObjectType.BLACK_LARVAE
                                  ]:
            object_values_complete.append(0x8)


        # Objects which despawn
        if object.object_type in [Objects.ObjectType.GUN_BEETLE, Objects.ObjectType.BIG_FOOT,
                                  Objects.ObjectType.GUN_ROBOT, Objects.ObjectType.EGG_CLOWN,
                                  Objects.ObjectType.EGG_PAWN, Objects.ObjectType.SHADOW_ANDROID,
                                  Objects.ObjectType.BLACK_ASSASSIN, Objects.ObjectType.BLACK_VOLT,
                                  Objects.ObjectType.BLACK_HAWK, Objects.ObjectType.BLACK_WARRIOR,
                                  Objects.ObjectType.BLACK_OAK, Objects.ObjectType.BLACK_WING,
                                  Objects.ObjectType.BLACK_WORM, Objects.ObjectType.ARTIFICIAL_CHAOS,

                                  Objects.ObjectType.PRISON_ISLAND_DISC, Objects.ObjectType.CENTRAL_CITY_BIG_BOMB,
                                  Objects.ObjectType.THE_ARK_DEFENSE_UNIT, Objects.ObjectType.SPACE_GADGET_DEFENSE_UNIT,
                                  Objects.ObjectType.GUN_FORTRESS_COMPUTER, Objects.ObjectType.DOOM_RESEARCHER

                                  ]:

            # Enemies which respawn write 8 then B in quick succession
            object_values_complete.append(0xB)
            object_values_complete.append(0x8)

        # Base style objects 0
        if (key_sanity and object.object_type == Objects.ObjectType.KEY) or \
            (shadow_box_sanity and object.object_type == Objects.ObjectType.SHADOW_BOX) or \
            (core_sanity and object.object_type == Objects.ObjectType.ENERGY_CORE or \
            object.object_type == Objects.ObjectType.ENERGY_CORE_IN_WOOD_BOX) or \
            (True and ( object.object_type in Objects.GetItemBoxTypes()
            )):

            object_values_complete = [0x0]

        if len(object_values_complete) != 0:
            expected_object_id, expected_object_name = Names.GetObjectLocationName(object)

            related_locations = [l.locationId for l in object_locations if
                                 l.name == expected_object_name]

            arch_location_complete = len([l for l in related_locations if
                                          l not in ctx.handled
                                          and l not in ctx.checked_locations]) == 0

            is_world_location = len([l for l in related_locations if
                                          l in ctx.server_locations]) != 0

            if len(related_locations) == 0:
                print("Related  locations not recognised:", expected_object_name)
                continue
            elif not is_world_location:
                #print("Unrecognised as world item:", expected_object_name)
                continue

            if object.index in ctx.level_state["object_status"]:
                object_status = ctx.level_state["object_status"][object.index]
                if object_status in object_values_complete:
                    arch_location_complete = True

            if not arch_location_complete:
                if loaded_spawn_data in object_values_complete:
                    ctx.level_state["object_status"][object.index] = 0x0B
                    messages.extend(related_locations)

        if beetle_sanity and object.object_type == Objects.ObjectType.GOLD_BEETLE:

            expected_object_id, expected_object_name = Names.GetObjectLocationName(object)

            related_locations = [l.locationId for l in object_locations if
                                 l.name == expected_object_name]

            arch_location_complete = len([l for l in related_locations if
                                          l not in ctx.handled
                                          and l not in ctx.checked_locations]) == 0

            if object.index in ctx.level_state["object_status"]:
                object_status = ctx.level_state["object_status"][object.index]
                if object_status in (0x00, 0x08):
                    arch_location_complete = True

            if not arch_location_complete:
                if loaded_spawn_data in (0x00, 0x08):
                    ctx.level_state["object_status"][object.index] = 0x08
                    messages.extend(related_locations)


        if door_sanity and object.object_type == Objects.ObjectType.KEY_DOOR:
            expected_object_id, expected_object_name = Names.GetObjectLocationName(object)

            related_locations = [l.locationId for l in object_locations if
                            l.name == expected_object_name ]

            arch_location_complete = len([ l for l in related_locations if
                                           l not in ctx.handled
                                           and l not in ctx.checked_locations]) == 0

            # TODO: Consider other options with the door, such as:
            # Always open
            # Open on N Key
            # Open on Global Key
            # Prevent opening animation
            # etc.

            door_status_address = spawn_data + 1
            loaded_bytes = dolphin_memory_engine.read_bytes(door_status_address, 1)
            current_door_status = int.from_bytes(loaded_bytes, byteorder='big')

            if object.index in ctx.level_state["object_status"]:
                object_status = ctx.level_state["object_status"][object.index]
                if object_status == 0x00:
                    arch_location_complete = True

            if not arch_location_complete:
                if current_door_status == 0x40:
                    ctx.level_state["object_status"][object.index] = 0x00
                    messages.extend(related_locations)

    if len(messages) > 0:
        message = [{"cmd": 'LocationChecks', "locations": messages}]
        await ctx.send_msgs(message)

    for key, value in states_to_add.items():
        if key not in ctx.level_state:
            print("Add to state", key, value)
            ctx.level_state[key] = value

    for entry in states_to_remove:
        if entry in ctx.level_state:
            print("Delete from state", entry)
            del ctx.level_state[entry]
            print("Delete from state", ctx.level_state)

def TextToShadowBytes(message):
    shadow_bytes = []
    for c in message:
        shadow_bytes.append(0)
        shadow_bytes.append(ord(c))

    shadow_bytes.extend([0,0])
    return bytes(bytearray(shadow_bytes))


def DisplayMessages(ctx):
    display_time = 0xFF

    info = Items.GetItemLookupDict()

    last_index = get_last_index_message(ctx)
    latest_index = None
    displayable = False

    if last_index is not None and ctx.last_subtitle_text_pointer is None:
        # get the next message to display
        latest_index = None
        message = None

        rec_info = None

        messages = []
        messages.extend(ctx.handled)
        messages.extend(ctx.items_to_handle)

        if len(messages) == 0:
            return

        next_messages = [ l[1] for l in messages if l[1] > last_index]
        if len(next_messages) == 0:
            return
        next_message = next_messages[0]

        if next_message > last_index:
            rec_info = [ m[0] for m in messages if m[1] == next_message ][0]

        if rec_info is not None and rec_info.item is not None and rec_info.item in info:
            message = f"Received {info[rec_info.item].name}"

        if message is not None:
            displayable = DisplayMessageInGame(ctx, message, display_time)
            if displayable:
                latest_index = next_message

    elif ctx.last_subtitle_text_pointer is not None:
        DisplayMessageInGame(ctx, None, None)

    if displayable and latest_index is not None:
        set_last_index_message(ctx, latest_index)

def DisplayMessageInGame(ctx, message, display_time):

    is_subtitle_active_address = GAME_ADDRESSES.SUBTITLE_INFO
    subtitle_reference_pointer_address = is_subtitle_active_address + (4*7)

    subtitle_data_pointer_offset = (16*3)
    subtitle_data_display_time_offset = (3*4)

    subtitle_active_bytes = dolphin_memory_engine.read_bytes(is_subtitle_active_address, 4)
    subtitle_active = int.from_bytes(subtitle_active_bytes, byteorder="big")

    message_state_changed = False
    # Wait until subtitle is active
    if subtitle_active == 0xFFFFFFFF:
        message_state_changed = True

    if message_state_changed and subtitle_active != ctx.last_subtitle_message_base_pointer:
        message_state_changed = True

    subtitle_reference_active = None
    if not message_state_changed:
        ctx.last_subtitle_message_base_pointer = subtitle_active
        subtitle_reference_pointer_bytes = dolphin_memory_engine.read_bytes(subtitle_reference_pointer_address, 4)
        subtitle_reference_pointer = int.from_bytes(subtitle_reference_pointer_bytes, byteorder="big")

        subtitle_reference_active_address = subtitle_reference_pointer + subtitle_data_pointer_offset
        subtitle_reference_active_bytes = dolphin_memory_engine.read_bytes(subtitle_reference_active_address, 4)

        subtitle_reference_active = int.from_bytes(subtitle_reference_active_bytes, byteorder="big")

    if message_state_changed:
        if ctx.last_subtitle_text_pointer is not None:
            writeBytes(ctx.last_subtitle_text_pointer, ctx.last_subtitle_default_text)
            ctx.last_subtitle_text_pointer = None
            ctx.last_subtitle_default_text = None

        if ctx.last_subtitle_ttl is not None:
            writeBytes(ctx.last_subtitle_ttl_pointer, ctx.last_subtitle_ttl)
            ctx.last_subtitle_ttl = None
            ctx.last_subtitle_ttl_pointer = None

        ctx.last_subtitle_base_pointer = None

        #print("Message stopped being displayed")
        # check last known information for ttl and message data and restore it!
        return False

    if message is None:
        return None


    ttl_address = subtitle_reference_active+subtitle_data_display_time_offset
    subtitle_ttl_bytes = dolphin_memory_engine.read_bytes(ttl_address, 4)
    ttl_bytes = display_time.to_bytes(4, byteorder='big')

    if subtitle_ttl_bytes != ttl_bytes:
        writeBytes(ttl_address, ttl_bytes)
        ctx.last_subtitle_ttl = subtitle_ttl_bytes
        ctx.last_subtitle_ttl_pointer = ttl_address

    text_pointer_address = GAME_ADDRESSES.LAST_SUBTITLE_TEXT
    text_pointer_bytes = dolphin_memory_engine.read_bytes(text_pointer_address, 4)
    text_pointer = int.from_bytes(text_pointer_bytes, byteorder="big")

    shadow_message_bytes = TextToShadowBytes(message)


    current_subtitle_bytes = dolphin_memory_engine.read_bytes(text_pointer, len(shadow_message_bytes))
    if current_subtitle_bytes != shadow_message_bytes:
        writeBytes(text_pointer, shadow_message_bytes)
        ctx.last_subtitle_text_pointer = text_pointer
        ctx.last_subtitle_default_text = current_subtitle_bytes


    return True



async def update_level_behaviour(ctx, current_level, death):
    # based on the level
    # work out which addresses to use for checks for each mission objective
    # handle picked up keys as they picked up
    # handle enemy counters if checks are enabled
    # Set initial value (to level of value from server)
    # If higher than previous value, recognise as check and reduce by 1

    await handle_objects(ctx, current_level)

    await clearout_individual_enemies_by_percentage(ctx, current_level)

    #ShowSETChanges(current_level)

    #DisplayMessages(ctx)

    # Add handle for first load of level, when state is blank

    info = Items.GetItemLookupDict()
    mission_clear_locations, mission_locations, end_location, enemysanity_locations,\
        checkpointsanity_locations, charactersanity_locations,\
        token_locations, keysanity_locations, weaponsanity_locations, boss_locations,\
        warp_locations, object_locations = Locations.GetAllLocationInfo()

    handle_count = 0

    if death or ctx.restart:
        ctx.level_keys = []
        if ctx.debug_logging:
            logger.error("Handle death/restart")
        if len(ctx.checkpoint_snapshots) > 0 and not ctx.restart:
            last_snapshot = ctx.checkpoint_snapshots[-1][1]
            ctx.level_state = deepcopy(last_snapshot)
        else:
            ctx.level_state = {}

        ctx.restart = False

        return

    await check_weapons(ctx, current_level)
    await check_junk(ctx, current_level, death)

    if len(ctx.level_state.keys()) == 0:
        ctx.level_state["active"] = True
        ctx.level_state["hero_count"] = 0
        ctx.level_state["hero_active"] = True
        ctx.level_state["dark_count"] = 0
        ctx.level_state["dark_active"] = True
        ctx.level_state["hero_completable"] = COMPLETE_FLAG_OFF
        ctx.level_state["dark_completable"] = COMPLETE_FLAG_OFF
        ctx.level_state["hero_progress"] = 0
        ctx.level_state["dark_progress"] = 0

        ctx.level_state["alien_progress"] = 0
        ctx.level_state["egg_progress"] = 0
        ctx.level_state["gun_progress"] = 0
        ctx.level_state["key_index"] = 0
        ctx.level_state["characters_set"] = False
        ctx.level_state["spawn_messages"] = []
        ctx.level_state["key_check_index"] = -1
        ctx.level_state["music_set"] = True
        ctx.checkpoint_trap_active = False

        ctx.checkpoint_snapshots = []

        i = [unlock for unlock in ctx.handled if unlock[0].item in info and \
             info[unlock[0].item].stageId == current_level and info[unlock[0].item].type == "level_object"]

        group_by_alignment = {}
        for ix in i:
            item = info[ix[0].item]
            if item.alignmentId not in group_by_alignment:
                group_by_alignment[item.alignmentId] = []
            group_by_alignment[item.alignmentId].append(item)

        if ctx.level_state["hero_active"] and ctx.objective_sanity:
            if Levels.MISSION_ALIGNMENT_HERO in group_by_alignment:
                hero_count = len(group_by_alignment[Levels.MISSION_ALIGNMENT_HERO])
                handle_count += 1
            else:
                hero_count = 0

            ctx.level_state["hero_count"] = hero_count

        if ctx.level_state["dark_active"] and ctx.objective_sanity:
            if Levels.MISSION_ALIGNMENT_DARK in group_by_alignment:
                dark_count = len(group_by_alignment[Levels.MISSION_ALIGNMENT_DARK])
                handle_count += 1
            else:
                dark_count = 0
            ctx.level_state["dark_count"] = dark_count

    current_alignment = dolphin_memory_engine.read_byte(GAME_ADDRESSES.ADDRESS_MISSION_ALIGNMENT)

    i = [unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
         info[unlock[0].item].stageId == current_level and \
         #info[unlock[0].item].alignmentId == current_alignment and
         info[unlock[0].item].type == "level_object" ]

    remove = []
    for ix in i:
        if info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_DARK and ctx.objective_sanity:
            ctx.level_state["dark_count"] += 1
        elif info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_HERO and ctx.objective_sanity:
            ctx.level_state["hero_count"] += 1
        ctx.handled.append(ix)
        remove.append(ix)
        handle_count += 1

    for r in remove:
        ctx.items_to_handle.remove(r)

    #hero_address = None
    #dark_address = None
    dark_write = None
    hero_write = None


    hero_address_data = GetStageAlignmentAddress(current_level, Levels.MISSION_ALIGNMENT_HERO)
    dark_address_data = GetStageAlignmentAddress(current_level, Levels.MISSION_ALIGNMENT_DARK)

    hero_address = None
    hero_address_size = 4

    dark_address = None
    dark_address_size = 4

    hero_address_total = None
    dark_address_total = None

    hero_max_hit = False
    dark_max_hit = False

    alien_address_size = 4
    gun_address_size = 4
    egg_address_size = 4

    restore_hero = False
    restore_dark = False

    dark_default_tally_address = None
    dark_working_1_address_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_MISSION_MANAGER + 16, 4)
    dark_working_1_address = int.from_bytes(dark_working_1_address_bytes, byteorder="big")
    if dark_working_1_address != 0:
        dark_working_2_address_bytes = dolphin_memory_engine.read_bytes(dark_working_1_address + 12, 4)
        dark_working_2_address = int.from_bytes(dark_working_2_address_bytes, byteorder="big")
        if dark_working_2_address != 0:
            dark_address_total = dark_working_2_address + 8
            dark_default_tally_address = dark_address_total + 16

    hero_default_tally_address = None
    hero_working_1_address_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_MISSION_MANAGER + 32, 4)
    hero_working_1_address = int.from_bytes(hero_working_1_address_bytes, byteorder="big")
    if hero_working_1_address != 0:
        hero_working_2_address_bytes = dolphin_memory_engine.read_bytes(hero_working_1_address + 12, 4)
        hero_working_2_address = int.from_bytes(hero_working_2_address_bytes, byteorder="big")
        if hero_working_2_address != 0:
            hero_address_total = hero_working_2_address + 8
            hero_default_tally_address = hero_address_total + 16

    if hero_address_data is not None:
        if hero_address_data.tally_address is not None:
            hero_address = hero_address_data.tally_address
        else:
            hero_address = hero_default_tally_address

    if dark_address_data is not None:
        if dark_address_data.tally_address is not None:
            dark_address = dark_address_data.tally_address
        else:
            dark_address = dark_default_tally_address

    #if hero_address_data is not None and hero_address is not None:
    #    current_pointer = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
    #    mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + hero_address_data.searchIndex
    #    hero_address = mission_requirement_count

    #if dark_address_data is not None and dark_address_data.searchIndex is not None:
    #    current_pointer = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
    #    mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + dark_address_data.searchIndex
    #    dark_address = mission_requirement_count

    stageInfo = GetStageInformation(current_level)
    heroInfo = None
    stageInfoHero = [ s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_HERO ]
    if len(stageInfoHero) > 0 and hero_address is not None:
        heroInfo = stageInfoHero[0]

    darkInfo = None
    stageInfoDark = [s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_DARK]
    if len(stageInfoDark) > 0 and dark_address is not None:
        darkInfo = stageInfoDark[0]

    EnemyInfo = GetStageEnemysanityInformation(current_level)
    alienInfo = None
    stageInfoAlien = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_ALIEN]
    if len(stageInfoAlien) > 0:
        alienInfo = stageInfoAlien[0]
    gunInfo = None
    stageInfoGun = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_GUN]
    if len(stageInfoGun) > 0:
        gunInfo = stageInfoGun[0]
    eggInfo = None
    stageInfoEgg = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_EGG]
    if len(stageInfoEgg) > 0:
        eggInfo = stageInfoEgg[0]

    extra_increase = 100

    if heroInfo is not None and heroInfo.requirement_count is not None:
        hero_count = ctx.level_state["hero_count"]

        location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                     heroInfo.mission_object_name,
                                                                     ctx, heroInfo.stageId,
                                                                     heroInfo.alignmentId,
                                                                     ctx.override_settings)

        result_sanity = ShadowUtils.GetObjectiveSanityFlag(ctx, location_details)

        heroMaxAdjusted = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                      heroInfo.mission_object_name, ctx,
                                                                  heroInfo.stageId, heroInfo.alignmentId,
                                                                  ctx.override_settings), heroInfo.requirement_count,
            current_level, MISSION_ALIGNMENT_HERO, ctx.override_settings)

        heroMaxAvailable = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                      heroInfo.mission_object_name, ctx,
                                                                  heroInfo.stageId, heroInfo.alignmentId,
                                                                  ctx.override_settings), heroInfo.requirement_count,
            current_level, MISSION_ALIGNMENT_HERO, ctx.override_settings)

        difference_over = heroMaxAdjusted - heroInfo.requirement_count
        if difference_over < 0:
            difference_over = 0

        hero_write = hero_count

        if (ctx.objective_sanity and ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear
                and result_sanity):
            hero_write = ctx.level_state["hero_progress"]

        if ctx.objective_sanity and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear\
                and result_sanity:
            restore_hero = True

        set_max_up = False
        hero_completable = ctx.level_state["hero_completable"]
        if hero_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            if ctx.objective_sanity and result_sanity: #and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear:
                hero_count_max = heroMaxAvailable + extra_increase
            else:
                relevant_keys = [ l for l in Levels.MINIMUM_STAGE_REQUIREMENTS if
                                  l[0] == current_level and l[1] == MISSION_ALIGNMENT_HERO ]
                if len(relevant_keys) == 1:
                    max_value = relevant_keys[0][2] + 1
                    if heroMaxAdjusted < max_value:
                        hero_count_max = max_value
                        logger.error("Issue with total hero enemies from created seed")
                    else:
                        hero_count_max = heroMaxAdjusted
                else:
                        hero_count_max = heroMaxAdjusted
            ctx.level_state["hero_completable"] = COMPLETE_FLAG_OFF_SET
        elif hero_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            hero_count_max = heroMaxAdjusted

            if ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_manual_clear or\
                ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear:
                ctx.level_state["hero_completable"] = COMPLETE_FLAG_ON_MANUAL
                hero_write = ctx.level_state["hero_progress"]
            else:
                ctx.level_state["hero_completable"] = COMPLETE_FLAG_ON_SET
            handle_count = True
        else:
            set_max_up = False
            hero_count_max = 255

        if hero_count >= heroMaxAdjusted or ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear:
            hero_max_hit = True

        if set_max_up and hero_address_total is not None:
            new_count = hero_count_max
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            writeBytes(hero_address_total, new_bytes)

        if handle_count > 0 and hero_write is not None and ctx.objective_sanity and result_sanity\
                and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear:
            new_count = hero_write
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            writeBytes(hero_address, new_bytes)

    if darkInfo is not None and darkInfo.requirement_count is not None:
        dark_count = ctx.level_state["dark_count"]

        location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                     darkInfo.mission_object_name,
                                                                     ctx, darkInfo.stageId,
                                                                     darkInfo.alignmentId,
                                                                     ctx.override_settings)

        result_sanity = ShadowUtils.GetObjectiveSanityFlag(ctx, location_details)

        darkMaxAdjusted = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                      darkInfo.mission_object_name, ctx,
                                                                  darkInfo.stageId, darkInfo.alignmentId,
                                                                  ctx.override_settings), darkInfo.requirement_count,
            current_level, MISSION_ALIGNMENT_DARK, ctx.override_settings)

        darkMaxAvailable = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                      darkInfo.mission_object_name, ctx,
                                                                  darkInfo.stageId, darkInfo.alignmentId,
                                                                  ctx.override_settings), darkInfo.requirement_count,
            current_level, MISSION_ALIGNMENT_DARK, ctx.override_settings)

        difference_over = darkMaxAdjusted - darkInfo.requirement_count
        if difference_over < 0:
            difference_over = 0

        set_max_up = False
        dark_write = dark_count
        if (ctx.objective_sanity and ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear
                and result_sanity):
            dark_write = ctx.level_state["dark_progress"]

        if ctx.objective_sanity and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear\
                and result_sanity:
            restore_dark = True

        dark_completable = ctx.level_state["dark_completable"]
        if dark_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            if ctx.objective_sanity and result_sanity: #and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear:
                dark_count_max = darkMaxAvailable + extra_increase
            else:
                relevant_keys = [l for l in Levels.MINIMUM_STAGE_REQUIREMENTS if
                                 l[0] == current_level and l[1] == MISSION_ALIGNMENT_DARK]
                if len(relevant_keys) == 1:
                    max_value = relevant_keys[0][2] + 1
                    if darkMaxAdjusted < max_value:
                        logger.error("Issue with total dark enemies from created seed")
                        dark_count_max = max_value
                    else:
                        dark_count_max = darkMaxAdjusted
                else:
                    dark_count_max = darkMaxAdjusted
            ctx.level_state["dark_completable"] = COMPLETE_FLAG_OFF_SET
        elif dark_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            dark_count_max = darkMaxAdjusted

            if ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_manual_clear or \
                    ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear:
                ctx.level_state["dark_completable"] = COMPLETE_FLAG_ON_MANUAL
                dark_write = ctx.level_state["dark_progress"]
                handle_count = True
            else:
                ctx.level_state["dark_completable"] = COMPLETE_FLAG_ON_SET

        else:
            set_max_up = False
            dark_count_max = 255

        if dark_count >= darkMaxAdjusted or ctx.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear:
            dark_max_hit = True

        #if ctx.objective_sanity and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_default and \
        #        result_sanity:
        #    dark_write = ctx.level_state["dark_progress"]

        if set_max_up and dark_address_total is not None:
            #dark_total_address = dark_address - 16
            #if dark_address == ADDRESS_SOLIDER_COUNT:
            #
            #    current_pointer = dolphin_memory_engine.read_bytes(ADDRESS_MISSION_DARK_POINTER, dark_address_size)
            #    mission_requirement_count = (int.from_bytes(current_pointer, byteorder="big") +
            #                                 dark_address_data.totalSearchIndex)
            #    dark_total_address = mission_requirement_count
            #else:
            #    dark_total_address = dark_address - 16

            new_count = dark_count_max
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            writeBytes(dark_address_total, new_bytes)

        if handle_count > 0 and dark_write is not None and ctx.objective_sanity and result_sanity\
                and ctx.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear:
            new_count = dark_write
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            writeBytes(dark_address, new_bytes)

    ## Handle new events

    expected_hero_value = hero_write
    expected_dark_value = dark_write

    hero_progress = False
    dark_progress = False

    alien_progress = False
    gun_progress = False
    egg_progress = False

    enemysanity = ctx.enemy_sanity

    if hero_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big', signed=True)

        if current_count is not None and expected_hero_value is not None and current_count < expected_hero_value:
            if not death and ctx.level_state["hero_progress"] != 0:
                logger.info("Detected decrease in hero count")
                ctx.level_state["hero_progress"] -= 1

                if enemysanity and hero_address == GAME_ADDRESSES.ADDRESS_ALIEN_COUNT:
                    ctx.level_state["alien_progress"] -= 1

        if expected_hero_value is not None and current_count > expected_hero_value:
            if ctx.debug_logging:
                logger.debug("Hero count increased:%d %d", current_count, expected_hero_value)

            required_count = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                          heroInfo.mission_object_name, ctx,
                                                                  heroInfo.stageId, heroInfo.alignmentId,
                                                                  ctx.override_settings),
                heroInfo.requirement_count, heroInfo.stageId, heroInfo.alignmentId, ctx.override_settings)

            diff_over = required_count - heroInfo.requirement_count
            if diff_over > 0:
                extra_increase += diff_over

            valid_compare_count = heroInfo.requirement_count + extra_increase

            if current_count > valid_compare_count:
                if ctx.info_logging:
                    logger.error("invalid value read for hero count:%d %d",current_count, valid_compare_count)
            new_count = (current_count - expected_hero_value)
            ctx.level_state["hero_progress"] += new_count
            if not ctx.objective_sanity:
                ctx.level_state["hero_count"] += new_count
            hero_progress = True
            if enemysanity and hero_address == GAME_ADDRESSES.ADDRESS_ALIEN_COUNT:
                ctx.level_state["alien_progress"] += new_count
                alien_progress = True

        if hero_address is not None and hero_write is not None and restore_hero and current_count != expected_hero_value\
                and ctx.level_state["hero_completable"] != COMPLETE_FLAG_ON_MANUAL:
            new_count = expected_hero_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            writeBytes(hero_address, new_bytes)

    if dark_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big', signed=True)

        if current_count is not None and expected_dark_value is not None and current_count < expected_dark_value:
            if not death and ctx.level_state["dark_progress"] != 0:
                logger.info("Detected decrease in dark count")
                ctx.level_state["dark_progress"] -= 1

                if enemysanity and dark_address == GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT:
                    ctx.level_state["gun_progress"] -= 1


        if expected_dark_value is not None and current_count > expected_dark_value:
            if ctx.debug_logging:
                logger.info("Dark count increased: %d %d", current_count, expected_dark_value)

            required_count = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                          darkInfo.mission_object_name, ctx,
                                                                  darkInfo.stageId, darkInfo.alignmentId,
                                                                  ctx.override_settings),
                darkInfo.requirement_count, darkInfo.stageId, darkInfo.alignmentId, ctx.override_settings)

            diff_over = required_count - darkInfo.requirement_count
            if diff_over > 0:
                extra_increase += diff_over

            valid_compare_count = darkInfo.requirement_count + extra_increase

            if current_count > valid_compare_count:
                if ctx.error_logging:
                    logger.error("invalid value read for dark count: %d %d",current_count, valid_compare_count)
            else:
                new_count = (current_count - expected_dark_value)
                ctx.level_state["dark_progress"] += new_count
                dark_progress = True
                if not ctx.objective_sanity:
                    ctx.level_state["dark_count"] += new_count
                if enemysanity and dark_address == GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT:
                    ctx.level_state["gun_progress"] += new_count
                    gun_progress = True
        #elif expected_dark_value > current_count >= 0:
        #    ctx.level_state["dark_progress"] = current_count

        if dark_address is not None and dark_write is not None and restore_dark and current_count != expected_dark_value\
                and ctx.level_state["dark_completable"] != COMPLETE_FLAG_ON_MANUAL:
            new_count = expected_dark_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            writeBytes(dark_address, new_bytes)

    if enemysanity and hero_address != GAME_ADDRESSES.ADDRESS_ALIEN_COUNT and alienInfo is not None:
        alien_count = ctx.level_state["alien_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_ALIEN_COUNT, alien_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big', signed=True)

        if current_count is not None and alien_count is not None and current_count < alien_count:
            if not death and ctx.level_state["alien_progress"] != 0:
                logger.info("Detected decrease in alien count")
                ctx.level_state["alien_progress"] -= 1


        if current_count > alien_count:
            if current_count > alienInfo.total_count + extra_increase:
                if ctx.info_logging:
                    logger.error("Error with alien count: %d %d", current_count, alienInfo.total_count + extra_increase)
            ctx.level_state["alien_progress"] += (current_count - alien_count)
            alien_progress = True

    if enemysanity and dark_address != GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT and gunInfo is not None:
        gun_count = ctx.level_state["gun_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_SOLDIER_COUNT, gun_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big', signed=True)

        if current_count is not None and gun_count is not None and current_count < gun_count:
            if not death and ctx.level_state["gun_progress"] != 0:
                logger.info("Detected decrease in gun count")
                ctx.level_state["gun_progress"] -= 1

        if current_count > gun_count:
            if current_count > gunInfo.total_count + extra_increase:
                if ctx.info_logging:
                    logger.error("Error with gun count: %d %d", current_count, gunInfo.total_count + extra_increase)
            ctx.level_state["gun_progress"] += (current_count - gun_count)
            gun_progress = True

    if enemysanity and hero_address != GAME_ADDRESSES.ADDRESS_EGG_COUNT and eggInfo is not None:
        egg_count = ctx.level_state["egg_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_EGG_COUNT, egg_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big', signed=True)

        #logger.info("Egg %d", current_count)

        if current_count is not None and egg_count is not None and current_count < egg_count:
            if not death and ctx.level_state["egg_progress"] != 0:
                logger.info("Detected decrease in egg count")
                ctx.level_state["egg_progress"] -= 1

        if current_count > egg_count:
            if current_count > eggInfo.total_count + extra_increase:
                if ctx.info_logging:
                    logger.error("Error with egg count: %d %d", current_count, eggInfo.total_count + extra_increase)
            ctx.level_state["egg_progress"] += (current_count - egg_count)
            egg_progress = True

    messages = []
    if hero_progress or dark_progress or alien_progress or gun_progress or egg_progress:
        # TODO: Check which check we are up to for hero and dark
        # Send only unchecked locations
        # Need state to be restorable maybe


        # Signal archipelago a check has been made
        if hero_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_HERO and \
                l.stageId == current_level and l.count <= ctx.level_state["hero_progress"] and l.locationId not in ctx.checked_locations ]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)
            elif ctx.debug_logging:
                logger.error("Hero Progress: no new checks %d", ctx.level_state["hero_progress"])

        if dark_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_DARK and \
                l.stageId == current_level and l.count <= ctx.level_state["dark_progress"]
                                   and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)
            elif ctx.debug_logging:
                logger.error("Dark Progress: no new checks %d", ctx.level_state["dark_progress"])

        if alien_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_ALIEN and \
                                  l.stageId == current_level and l.count <= ctx.level_state["alien_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)
            elif ctx.debug_logging:
                logger.error("Alien Progress: no new checks %d", ctx.level_state["alien_progress"])

        if gun_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_GUN and \
                                  l.stageId == current_level and l.count <= ctx.level_state["gun_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)
            elif ctx.debug_logging:
                logger.error("GUN Progress: no new checks %d", ctx.level_state["gun_progress"])

        if egg_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_EGG and \
                                  l.stageId == current_level and l.count <= ctx.level_state["egg_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)
            elif ctx.debug_logging:
                logger.error("Egg Progress: no new checks %d", ctx.level_state["egg_progress"])


    # Check checkpoint flags and save the state when a new one is activated
    checkpoint_data_for_stage = [c for c in Locations.CheckpointLocations if c.stageId == current_level]
    if len(checkpoint_data_for_stage) > 0:
        total_count = checkpoint_data_for_stage[0].total_count
        max_checkpoint_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.CHECKPOINT_RESPAWN_ID, 1)
        max_checkpoint = int.from_bytes(max_checkpoint_bytes, byteorder='big')

        if (max_checkpoint == 0 and len(ctx.level_state.keys()) > 0 and
                len(ctx.checkpoint_snapshots) > 1):
            if not ctx.checkpoint_trap_active:
                if ctx.debug_logging:
                    logger.error("Detected a stage restart (CP)")
                ctx.restart = True
                ctx.level_state = {}
                ctx.checkpoint_snapshots = []
            else:
                first_addr = GAME_ADDRESSES.CHECKPOINT_FLAGS[0]
                checkpoint_status_bytes = dolphin_memory_engine.read_bytes(first_addr, 1)
                checkpoint_status = int.from_bytes(checkpoint_status_bytes, byteorder='big') == 1
                if not checkpoint_status:
                    if ctx.debug_logging:
                        logger.error("Detected a stage restart (CP) (with checktrap)")
                    ctx.restart = True
                    ctx.level_state = {}
                    ctx.checkpoint_snapshots = []

        active = []
        new = []
        for i in range(0, total_count):
            addr = GAME_ADDRESSES.CHECKPOINT_FLAGS[i]
            checkpoint_status_bytes = dolphin_memory_engine.read_bytes(addr, 1)
            checkpoint_status = int.from_bytes(checkpoint_status_bytes, byteorder='big') == 1
            if checkpoint_status:
                active.append(i + 1)
        max_active = max(active) if len(active) > 0 else 0
        #if max_active != max_checkpoint:
        #    if ctx.info_logging:
        #        logger.error("Checkpoint data not valid %d %d", max_active, max_checkpoint)
        #else:
        active_snapshots = [x[0] for x in ctx.checkpoint_snapshots]
        for a in active:
            if a not in active_snapshots:
                new.append(a)
                ctx.checkpoint_snapshots.append((a, deepcopy(ctx.level_state)))
                if ctx.checkpoint_sanity:
                    locations = [c.locationId for c in checkpointsanity_locations if c.stageId == current_level and
                                 c.count == a]
                    messages.extend(locations)

    if ctx.key_sanity and current_level in KEY_IDENTIFIER_BY_STAGE:
        key_addresses = GetKeysanityAddresses()
        if "key_index" in ctx.level_state:
            state_key_index = ctx.level_state["key_index"]
            if state_key_index < len(key_addresses):
                current_key_bytes = dolphin_memory_engine.read_bytes(key_addresses[state_key_index], 4)
                current_key_data = int.from_bytes(current_key_bytes, byteorder='big')
                if current_key_data != 0xFFFFFFFF and current_key_data != 0x0:
                    key_options = KEY_IDENTIFIER_BY_STAGE[current_level]
                    if current_key_data in ctx.level_keys:
                        logger.error("Duplicate key:%s", str(current_key_data))
                        empty_bytes = 0xFFFFFFFF.to_bytes(4, byteorder='big')
                        writeBytes(key_addresses[state_key_index], empty_bytes)
                    elif current_key_data in key_options:
                        # What to do when the player gets a new key
                        logger.error("Take key away when arch key item only")
                        if ctx.key_collection_method == Options.KeyCollectionMethod.option_arch:
                            empty_bytes = 0xFFFFFFFF.to_bytes(4, byteorder='big')
                            writeBytes(key_addresses[state_key_index], empty_bytes)
                        else:
                            ctx.level_state["key_index"] = state_key_index + 1
                            ctx.level_keys.append(current_key_data)

                        #key_index = key_options.index(current_key_data)
                        #key_locations = [k for k in keysanity_locations if k.stageId == current_level and k.count == key_index]
                        #if len(key_locations) == 0:
                        #    if ctx.error_logging:
                        #        logger.error("Unable to find location associated %d %d", key_index, current_level)
                        #else:
                        #    messages.extend([k.locationId for k in key_locations])
                    elif current_key_data == 0:
                        # Fake key, ignore
                        logger.error("Detected fake key - increment")
                        ctx.level_state["key_index"] = state_key_index + 1
                    else:
                        if ctx.error_logging:
                            logger.error("Unknown key object: %d %s %s", current_level, str(key_options), str(current_key_data))
                        key_locations = [k for k in keysanity_locations if k.stageId == current_level and k.count == state_key_index]
                        messages.extend([k.locationId for k in key_locations])
                elif not ctx.key_restore_complete:
                    door_requirement = ctx.keys_required_for_doors
                    if state_key_index < (5 - door_requirement):
                        fake_key_value = 0
                        fake_key_bytes = fake_key_value.to_bytes(4, byteorder='big')
                        ctx.level_state["key_index"] = state_key_index + 1
                        writeBytes(key_addresses[state_key_index], fake_key_bytes)
                        logger.error("Fake key added")
                    else:
                        key_options_unknown = KEY_IDENTIFIER_BY_STAGE[current_level]
                        keys_to_confirm = [ k for k in key_options_unknown if k not in ctx.level_keys]
                        key_ind = [ key_options_unknown.index(k) for k in keys_to_confirm ]
                        key_locations = [k.locationId for k in keysanity_locations if k.stageId == current_level and k.count in key_ind]
                        checked_keys = [ c for c in ctx.checked_locations if c in key_locations]
                        if len(checked_keys) > 0:
                            first_key_location_id = checked_keys.pop()
                            key_data = [k for k in keysanity_locations if k.locationId == first_key_location_id][0]
                            key_value_to_write = key_options_unknown[key_data.count]
                            restored_key_bytes = key_value_to_write.to_bytes(4, byteorder='big')
                            logger.error("Key index restored")
                            writeBytes(key_addresses[state_key_index], restored_key_bytes)
                        else:
                            logger.error("Key restore complete")
                            info = Items.GetItemLookupDict()

                            handled_key_items = [k for k in ctx.handled if info[k[0].item].type == "key"]
                            for item in handled_key_items:
                                ctx.handled.remove(item)

                            ctx.key_restore_complete = True
                else:
                    if ctx.level_state["key_check_index"] != ctx.last_rcvd_index:
                        info = Items.GetItemLookupDict()

                        key_items = [unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
                                              info[unlock[0].item].stageId == current_level and
                                              info[unlock[0].item].type == "key" and unlock not in ctx.handled]

                        for item in key_items:
                            empty_bytes = 0x00.to_bytes(4, byteorder='big')
                            writeBytes(key_addresses[state_key_index], empty_bytes)
                            ctx.handled.append(item)
                            state_key_index += 1
                            logger.error("Give arch key")
                            if state_key_index > 4:
                                break

                            logger.error("increment key index")
                            ctx.level_state["key_index"] = state_key_index

                        ctx.level_state["key_check_index"] = ctx.last_rcvd_index
        else:
            logger.error("Key index not present")

    # If an objective is currently completable then check for pause state, etc

    is_back_button = 0x20

    if ctx.objective_sanity:
        if (dark_max_hit and current_alignment == MISSION_ALIGNMENT_DARK) or \
                (hero_max_hit and current_alignment == MISSION_ALIGNMENT_HERO):
            current_paused_data = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.is_paused_address, 1)
            currently_paused = int.from_bytes(current_paused_data, byteorder='big') == 1

            button_data = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.button_menu_address, 1)
            button_data_byte = int.from_bytes(button_data, byteorder='big')
            if currently_paused and button_data_byte == is_back_button:
                if current_alignment == MISSION_ALIGNMENT_DARK:
                    ctx.level_state["dark_completable"] = COMPLETE_FLAG_READY
                    #new_messages = complete_completable_levels(ctx, current_level, current_alignment)
                    #messages.extend(new_messages)
                elif current_alignment == MISSION_ALIGNMENT_HERO:
                    ctx.level_state["hero_completable"] = COMPLETE_FLAG_READY
                    #new_messages = complete_completable_levels(ctx, current_level, current_alignment)
                    #messages.extend(new_messages)


    if len(messages) > 0:
        message = [{"cmd": 'LocationChecks', "locations": messages}]
        await ctx.send_msgs(message)



async def check_death(ctx: ShTHContext):
    level_status_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.ADDRESS_LEVEL_STATUS, 4)
    level_status_value = int.from_bytes(level_status_bytes, byteorder='big')

    if level_status_value == LevelStatusOptions.Death or level_status_value == LevelStatusOptions.Reloading:
        if ctx.dead:
            return None
        ctx.dead = True
        return True

    if level_status_value == LevelStatusOptions.Restarting:
        ctx.restart = True

    ctx.dead = False

    #lives_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.LIVES_ADDRESS, 4)
    #life_count = int.from_bytes(lives_bytes, byteorder='big')

    #if life_count > ctx.lives:
    #    ctx.lives = life_count
    #elif life_count < ctx.lives:
    #    if ctx.dead:
    #        ctx.dead = False
    #    ctx.lives = life_count
    #    if ctx.debug_logging:
    ##        logger.error("Detected a death - lives!")
    #    ctx.current_rings_bytes = dolphin_memory_engine.read_bytes(GAME_ADDRESSES.RINGS_ADDRESS, 4)
    #    #return True

    #if ctx.dead:
    #    return None

    return False

def CheckGateConditions(ctx: ShTHContext):
    required_items = ctx.gate_requirements
    info = Items.GetItemLookupDict()
    current_items = [ info[i.item].name for i in ctx.items_received ]

    max_gate = 0
    for item in required_items.items():
        gate_no = item[0]
        gate_reqs = item[1]
        enough = True
        for gate_req in gate_reqs.items():
            item_name = gate_req[0]
            count = gate_req[1]
            if current_items.count(item_name) < count:
                enough = False
                break

        if enough:
            max_gate = gate_no

    for gate in ctx.gates.items():
        if int(gate[0]) > int(max_gate):
            continue

        opening = False

        stages = gate[1]
        for stage in stages:
            if stage not in ctx.available_levels:
                if not opening:
                    logger.info(f"Gate {gate[0]} is open!")
                    logger.info("")
                    opening = True
                ctx.available_levels.append(stage)

def resetGameState(ctx):
    if ctx.initialised:
        ctx.successful_shuffle = False
        ctx.initialised = False
        ctx.select_initialised = False

music_files = [
"sng_Battle1.adx",
"sng_Battle2.adx",
"sng_E1001.adx",
"sng_E4101.adx",
"sng_E4201.adx",
"sng_E5024.adx",
"sng_E5204.adx",
"sng_E8003.adx",
"sng_E8201.adx",
"sng_stg0100.adx",
"sng_stg0200.adx",
"sng_stg0201.adx",
"sng_stg0202.adx",
"sng_stg0210.adx",
"sng_stg0300.adx",
"sng_stg0301.adx",
"sng_stg0302.adx",
"sng_stg0310.adx",
"sng_stg0400.adx",
"sng_stg0401.adx",
"sng_stg0402.adx",
"sng_stg0403.adx",
"sng_stg0404.adx",
"sng_stg0410.adx",
"sng_stg0500.adx",
"sng_stg0501.adx",
"sng_stg0502.adx",
"sng_stg0503.adx",
"sng_stg0504.adx",
"sng_stg0510.adx",
"sng_stg0600.adx",
"sng_stg0601.adx",
"sng_stg0602.adx",
"sng_stg0603.adx",
"sng_stg0604.adx",
"sng_stg0610.adx",
"sng_stg0611.adx",
"sng_stg0612.adx",
"sng_stg0700.adx",
"sng_stg0710.adx",
"sng_stg0710b.adx",
"sng_stg0800.adx",
"sng_sys01.adx",
"sng_sys02.adx",
"sng_sys03.adx",
"sng_sys04.adx",
"sng_sys05.adx",
"sng_vox01.adx",
"sng_vox02.adx",
"sng_vox03.adx",
"sng_vox04.adx",
"sng_vox05.adx",
"sng_vox06.adx"
]

def GetStageSong():
    possible_files = [ p for p in music_files if len(p) == 15]
    return random.choice(possible_files)

async def set_music(ctx, level):
    if level is None:
        return

    set_state = False
    if ("music_set" not in ctx.level_state or not ctx.level_state["music_set"]) and ctx.music is None:
        set_state = True

    if "music_set" in ctx.level_state:
        ctx.music = None

    if set_state:
        chosen_value = GetStageSong()
        new_bytes = bytes(chosen_value, "utf-8")
        writeBytes(GAME_ADDRESSES.STAGE_MUSIC_NAME, new_bytes)
        ctx.music = chosen_value

    pass

async def check_charactersanity(ctx, level):
    if level is None:
        return

    messages = []

    (mission_clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations,
     charactersanity_locations, token_locations, keysanity_locations,
     weaponsanity_locations, boss_locations, warp_locations,
     object_locations) = Locations.GetAllLocationInfo()

    new_met_characters = []

    if "characters_set" not in ctx.level_state:
        check = True
        set_state = False
    elif ctx.level_state["characters_set"]:
        # Check if both characters in level found, if no, keep check true
        set_state = True
        check = True
    else:
        check = True
        set_state = True

    if ctx.character_sanity:
        for character in GAME_ADDRESSES.CharacterAddresses:
            if character.name in ctx.characters_met:
                continue
            characterSet_bytes = dolphin_memory_engine.read_bytes(character.met_address, 1)
            characterSet = int.from_bytes(characterSet_bytes, byteorder='big') == 1
            if characterSet:
                charLocation = [char.locationId for char in charactersanity_locations if char.other == character.name]
                if len(charLocation) > 0:
                    if charLocation[0] not in ctx.checked_locations:
                        messages.append(charLocation[0])
                        new_met_characters.append(character.name)
    else:
        if len(ctx.characters_met) == 0:
            new_met_characters.extend(
                [c.name for c in GAME_ADDRESSES.CharacterAddresses]
            )

    if check:
        #print("Check character state")
        for character in ctx.characters_met:
            relevantCharData = [c for c in GAME_ADDRESSES.CharacterAddresses if c.name == character]
            if len(relevantCharData) != 0:
                relevantChar = relevantCharData[0]
                char_seen = dolphin_memory_engine.read_bytes(relevantChar.met_address, 1)
                char_seen_value = int.from_bytes(char_seen, byteorder='big')
                if char_seen_value == 0:
                    new_value = 1
                    new_bytes = new_value.to_bytes(1, byteorder='big')
                    writeBytes(relevantChar.met_address, new_bytes)

        if set_state:
            ctx.level_state["characters_set"] = True

    if set_state and len(new_met_characters) > 0:
        ctx.characters_met.extend(new_met_characters)

    if len(messages) > 0 and set_state:
        #print("Send messages")
        unsent_messages = [message for message in messages if message not in ctx.checked_locations]
        message = [{"cmd": 'LocationChecks', "locations": unsent_messages}]
        await ctx.send_msgs(message)


async def dolphin_sync_task(ctx: ShTHContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        death = False
        try:
            if ctx.slot is not None:
                pass
            else:
                if ctx.awaiting_rom:
                    await ctx.server_auth()

            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.invalid_rom:
                    await ctx.disconnect()
                    await asyncio.sleep(5)

                elif ctx.awaiting_server:
                    await asyncio.sleep(1)
                    continue

                if not await check_save_loaded(ctx):
                    # Reset give item array while not in game.
                    #writeBytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    resetGameState(ctx)
                    await asyncio.sleep(0.1)

                    if ctx.ring_link == Options.RingLink.option_unsafe:
                        await handle_ring_link(ctx, None, death)

                    continue

                if not ctx.initialised:
                    ctx.initialised = True
                check_story(ctx)

                death = await check_death(ctx)
                if death is None:
                    continue
                level = await check_level_status(ctx)
                check_cheats()
                await check_charactersanity(ctx, level)
                await set_music(ctx, level)
                if level is not None and ctx.level_status is not None:
                    await update_level_behaviour(ctx,level, death)
                    await handle_ring_link(ctx, level, death)

                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS and not ctx.invalid_rom:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                if ctx.invalid_rom:
                    logger.error("Invalid rom modification.")
                    break
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    # Hook and check the game?!
                    game_id_bytes = dolphin_memory_engine.read_bytes(0x80000000, 6)
                    if game_id_bytes not in valid_game_bytes:
                        logger.info(CONNECTION_REFUSED_GAME_STATUS.format("", str(game_id_bytes)))
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        logger.info(f"Shadow The Hedgehog Client connected: Version:{'.'.join([ str(s) for s in ShadowUtils.VERSION])}")
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.game_id = game_id_bytes
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception as e:
            logger.error(e)
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed with exception, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            resetGameState(ctx)
            await ctx.disconnect(True)
            await asyncio.sleep(5)
            continue


def main(connect=None, password=None):
    Utils.init_logging("Shadow The Hedgehog Client")

    async def _main(connect, password):
        ctx = ShTHContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
