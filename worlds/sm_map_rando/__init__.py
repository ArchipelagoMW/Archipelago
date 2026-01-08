from __future__ import annotations

from collections import Counter
import logging
import copy
import os
import platform
import shutil
import sys
import tempfile
import threading
import base64
import itertools
import json
from typing import Any, Dict, Iterable, List, Optional, Set, TextIO, TypedDict

from BaseClasses import LocationProgressType, Region, Entrance, Location, MultiWorld, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive
from Utils import snes_to_pc
from worlds.AutoWorld import World, AutoLogicRegister, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

logger = logging.getLogger("Super Metroid Map Rando")

from .Rom import get_base_rom_path, get_sm_symbols, openFile, SMMR_ROM_MAX_PLAYERID, SMMR_ROM_PLAYERDATA_COUNT, SMMapRandoDeltaPatch 
from .ips import IPS_Patch
from .Client import SMMRSNIClient
from importlib.metadata import version, PackageNotFoundError

required_pysmmaprando_version = "0.119.1"

class WrongVersionError(Exception):
    pass

try:
    if version("pysmmaprando") != required_pysmmaprando_version:
        raise WrongVersionError
    from pysmmaprando import build_app_data, validate_settings_ap, randomize_ap, customize_seed_ap, CustomizeRequest, Item as MapRandoItem

# required for APWorld distribution outside official AP releases as stated at https://docs.python.org/3/library/zipimport.html:
# ZIP import of dynamic modules (.pyd, .so) is disallowed.
except (ImportError, WrongVersionError, PackageNotFoundError) as e:
    python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    if sys.platform.startswith('win'):
        abi_version = f"cp{sys.version_info.major}{sys.version_info.minor}-win_amd64"
    elif sys.platform.startswith('linux'):
        if platform.machine() == 'x86_64':
            abi_version = f"{python_version}-manylinux_2_17_{platform.machine()}.manylinux2014_{platform.machine()}"
        else:
            abi_version = f"{python_version}-manylinux_2_28_{platform.machine()}"
    elif sys.platform.startswith('darwin'):
        mac_ver = platform.mac_ver()[0].split('.')
        abi_version = f"{python_version}-macosx_10_12_x86_64.macosx_11_0_arm64.macosx_10_12_universal2"
    map_rando_lib_file = f'https://github.com/lordlou/MapRandomizer/releases/download/v{required_pysmmaprando_version}/pysmmaprando-{required_pysmmaprando_version}-{python_version}-{abi_version}.whl'
    import Utils
    if not Utils.is_frozen():
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', map_rando_lib_file])
    else:
        import requests
        import zipfile
        import io
        import glob
        import shutil
        dirs_to_delete = glob.glob(f"{os.path.dirname(sys.executable)}/lib/pysmmaprando-*.dist-info")
        for dir in dirs_to_delete:
            shutil. rmtree(dir)
        with requests.get(map_rando_lib_file) as r:
            r.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(f"{os.path.dirname(sys.executable)}/lib")
            
    from pysmmaprando import build_app_data, validate_settings_ap, randomize_ap, customize_seed_ap, CustomizeRequest, Item as MapRandoItem

def GetAPWorldPath():
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    game = "sm_map_rando/"
    if apworldExt in filename:
        return filename[:filename.index(apworldExt) + len(apworldExt)]
    else:
        return None

map_rando_app_data = build_app_data(GetAPWorldPath())

from .Options import SMMROptions

class ByteEdit(TypedDict):
    sym: Dict[str, Any]
    offset: int
    values: Iterable[int]

class SMMapRandoWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Metroid Map Rando Client on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )]


locations_start_id = 86000
items_start_id = 87000

locations_count = 100

location_address_to_id = {}
with openFile("/".join((os.path.dirname(__file__), "data", "loc_address_to_id.json")), "r") as stream:
    location_address_to_id = json.load(stream)

class SMMapRandoWorld(World):
    """
    After planet Zebes exploded, Mother Brain put it back together again but arranged it differently this time.

    Can you find the items needed to defeat Mother Brain and restore peace to the galaxy?
    """

    game: str = "Super Metroid Map Rando"
    data_version = 0
    options_dataclass = SMMROptions
    options: SMMROptions

    smmr_location_names = map_rando_app_data.game_data.get_location_names()

    item_name_to_id = {item_name: items_start_id + idx for idx, item_name in 
                                enumerate(itertools.chain(map_rando_app_data.game_data.item_isv.keys,
                                                          ["ArchipelagoItem", "ArchipelagoProgItem", "ArchipelagoUsefulItem", "ArchipelagoUsefulProgItem",
                                                           "ProgMissile", "ProgSuper", "ProgPowerBomb"]))}
    location_name_to_id = {loc_name: locations_start_id + location_address_to_id[str(addr)] for idx, (loc_name, addr) in 
                                enumerate(itertools.chain(zip(  smmr_location_names, 
                                                                map_rando_app_data.game_data.get_location_addresses())))}
    
    missile_item_id = 1
    nothing_item_id = 22
    prog_missile_item_id = 27

    web = SMMapRandoWeb()

    required_client_version = (0, 4, 4)

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()
        self.locations = {}
        self.region_area_name = {}

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)
        
    @classmethod
    def validate_settings(cls, settings_string: str) -> bool:
        return validate_settings_ap(settings_string, map_rando_app_data) is not None

    def generate_early(self):
        self.map_rando_settings = validate_settings_ap(json.dumps(self.options.map_rando_options.value), map_rando_app_data)
        self.randomizer_ap = randomize_ap(self.map_rando_settings, 
                                            self.random.randrange(9999999999),
                                            (self.multiworld.seed & 0xFFFFFFFF) if self.options.common_map.value else None,
                                            (self.multiworld.seed & 0xFFFFFFFF) if self.options.common_map.value and self.options.common_door_colors.value else None,
                                            map_rando_app_data)
        if self.randomizer_ap is None:
            raise Exception(f"Map Rando failed to randomize for player {self.player_name}")

    def create_region(self, world: MultiWorld, player: int, name: str, locations, exit, items_required = None):
        logger.debug(f"create_region: {name} {locations} {items_required}")
        ret = Region(name, player, world)
        if locations is not None:
            for loc in locations:
                location = self.locations[loc]
                location.parent_region = ret
                ret.locations.append(location)
        if exit is not None:
            entrance = Entrance(player, exit, ret)
            ret.exits.append(entrance)
            if items_required is not None:
                set_rule(entrance, lambda state : state.has_all_counts(Counter(items_required), player))
        return ret

    def create_regions(self):
        remaining_locations = []
        # create locations
        for loc_name, id in SMMapRandoWorld.location_name_to_id.items():
            self.locations[loc_name] = SMMRLocation(self.player, loc_name, len(self.randomizer_ap.spoiler_log.summary) - 1, id)
            remaining_locations.append(loc_name)

        # create regions
        self.region_dict = []
        for spoilerSummary in self.randomizer_ap.spoiler_log.summary:
            for spoilerItemSummary in spoilerSummary.items:
                logger.debug(f"Map rando Item placement: {spoilerItemSummary.item} {spoilerItemSummary.location.room} {spoilerItemSummary.location.node}")

        cumulative_required_items = []

        for spoilerSummary in self.randomizer_ap.spoiler_log.summary:
            counter = Counter(cumulative_required_items)
            for spoilerItemSummary in spoilerSummary.items:
                if spoilerItemSummary.item == "Missile":
                    if counter.get("ProgMissile", 0) < 3:
                        counter["ProgMissile"] += 1
                        cumulative_required_items.append("ProgMissile")
                elif spoilerItemSummary.item == "Super":
                    if counter.get("ProgSuper", 0) < 2:
                        counter["ProgSuper"] += 1
                        cumulative_required_items.append("ProgSuper")
                elif spoilerItemSummary.item == "PowerBomb":
                    if counter.get("ProgPowerBomb", 0) < 3:
                        counter["ProgPowerBomb"] += 1
                        cumulative_required_items.append("ProgPowerBomb")
                else:
                    cumulative_required_items.append(spoilerItemSummary.item)
            self.region_dict.append(self.create_region(  self.multiworld, 
                                                        self.player, 
                                                        f"step {spoilerSummary.step}",
                                                        [f"{spoilerItemSummary.location.room} {spoilerItemSummary.location.node}" for spoilerItemSummary in spoilerSummary.items],
                                                        f"to step {spoilerSummary.step + 1}" if spoilerSummary.step < len(self.randomizer_ap.spoiler_log.summary) else None,
                                                        cumulative_required_items[:]))
            for spoilerItemSummary in spoilerSummary.items:
                loc_name = f"{spoilerItemSummary.location.room} {spoilerItemSummary.location.node}"
                self.locations[loc_name].step = spoilerSummary.step
                remaining_locations.remove(loc_name)

        # if start location isnt Escape
        if (len(self.randomizer_ap.spoiler_log.summary) > 0):
            self.multiworld.regions += self.region_dict

            for loc_name in remaining_locations:
                region = self.multiworld.get_region(f"step {len(self.randomizer_ap.spoiler_log.summary) - 1}", self.player)
                self.locations[loc_name].parent_region = region
                region.locations.append(self.locations[loc_name])

            for spoilerSummary in self.randomizer_ap.spoiler_log.summary[:-1]:
                entrance = self.multiworld.get_entrance(f"to step {spoilerSummary.step + 1}", self.player)
                entrance.connect(self.multiworld.get_region(f"step {spoilerSummary.step + 1}", self.player));

            self.multiworld.regions += [
                self.create_region(self.multiworld, self.player, 'Menu', None, 'StartAP')
            ]
        else:
            self.multiworld.regions += [
                self.create_region(self.multiworld, self.player, 'Menu', None, 'StartAP'),
                self.create_region(self.multiworld, self.player, 'step 1', SMMapRandoWorld.location_name_to_id.keys(), None)
            ]

        startAP = self.multiworld.get_entrance('StartAP', self.player)
        startAP.connect(self.multiworld.get_region("step 1", self.player))

    def create_items(self):
        pool = []
        item_placement = [item.to_int() for item in self.randomizer_ap.randomization.item_placement]
        weaponCount = [0, 0, 0]         
        for spoilerSummary in self.randomizer_ap.spoiler_log.summary:
            for spoilerItemSummary in spoilerSummary.items:
                isAdvancement = True
                new_item_name = spoilerItemSummary.item
                if new_item_name == 'Missile':
                    if weaponCount[0] < 3:
                        weaponCount[0] += 1
                        new_item_name = 'ProgMissile'
                    else:
                        isAdvancement = False
                elif new_item_name == 'Super':
                    if weaponCount[1] < 2:
                        weaponCount[1] += 1
                        new_item_name = 'ProgSuper'
                    else:
                        isAdvancement = False
                elif new_item_name == 'PowerBomb':
                    if weaponCount[2] < 3:
                        weaponCount[2] += 1
                        new_item_name = 'ProgPowerBomb'
                    else:
                        isAdvancement = False
                elif new_item_name == 'Nothing':
                    isAdvancement = False
                new_item_id = SMMapRandoWorld.item_name_to_id[spoilerItemSummary.item]
                item_placement[SMMapRandoWorld.smmr_location_names.index(f"{spoilerItemSummary.location.room} {spoilerItemSummary.location.node}")] = -1
                mr_item = SMMRItem(new_item_name,
                            ItemClassification.progression if isAdvancement else ItemClassification.filler, 
                            new_item_id, 
                            player=self.player,
                            step=spoilerSummary.step)
                pool.append(mr_item)

        for i, item_id in enumerate(item_placement):
            if item_id != -1:
                mr_item = SMMRItem(SMMapRandoWorld.item_id_to_name[item_id + items_start_id], 
                                ItemClassification.filler, 
                                item_id + items_start_id, 
                                player=self.player,
                                step=len(self.randomizer_ap.spoiler_log.summary) - 1)
                pool.append(mr_item)
            
        self.multiworld.itempool += pool
        
    def set_rules(self):
        if (len(self.randomizer_ap.spoiler_log.summary) > 0):     
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(self.multiworld.get_entrance(f"to step {len(self.randomizer_ap.spoiler_log.summary)}", self.player))
        else:
            self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        
        def sort_list_by_step(list_to_sort: List, reverse=False):
            player_list = []
            indexes_list = []
            for i, progitem in enumerate(list_to_sort):
                if (progitem.player == self.player):
                    player_list.append(progitem)
                    indexes_list.append(i)
            player_list.sort(key=lambda item: item.step, reverse=reverse)
            for item in zip(player_list, indexes_list):
                list_to_sort[item[1]] = item[0]

        sort_list_by_step(progitempool, True)
        sort_list_by_step(fill_locations)

    def post_fill(self):
        self.startItems = [variaItem for item in self.multiworld.precollected_items[self.player] for variaItem in self.item_name_to_id.keys() if variaItem == item.name]
        spheres: List[Location] = getattr(self.multiworld, "_smmr_spheres", None)
        if spheres is None:
            spheres = list(self.multiworld.get_spheres())
            setattr(self.multiworld, "_smmr_spheres", spheres)
    
    def create_item(self, name: str) -> Item:
        is_progression = name != 'Missile' and name != 'Super' and name != 'PowerBomb' and name != 'Nothing'
        return SMMRItem(name, ItemClassification.progression if is_progression else ItemClassification.filler, self.item_name_to_id[name], player=self.player, step=0)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(['Missile', 'Missile', 'Missile', 'Missile', 'Missile', 'Super', 'PowerBomb'])

    def getWordArray(self, w: int) -> List[int]:
        """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
        return [w & 0x00FF, (w & 0xFF00) >> 8]

    def convertToROMItemName(self, itemName):
        charMap = { "A" : 0x2CC0, 
                    "B" : 0x2CC1,
                    "C" : 0x2CC2,
                    "D" : 0x2CC3,
                    "E" : 0x2CC4,
                    "F" : 0x2CC5,
                    "G" : 0x2CC6,
                    "H" : 0x2CC7,
                    "I" : 0x2CC8,
                    "J" : 0x2CC9,
                    "K" : 0x2CCA,
                    "L" : 0x2CCB,
                    "M" : 0x2CCC,
                    "N" : 0x2CCD,
                    "O" : 0x2CCE,
                    "P" : 0x2CCF,
                    "Q" : 0x2CD0,
                    "R" : 0x2CD1,
                    "S" : 0x2CD2,
                    "T" : 0x2CD3,
                    "U" : 0x2CD4,
                    "V" : 0x2CD5,
                    "W" : 0x2CD6,
                    "X" : 0x2CD7,
                    "Y" : 0x2CD8,
                    "Z" : 0x2CD9,
                    " " : 0x2C0F,
                    "!" : 0x2CDF,
                    "?" : 0x2CDE,
                    "'" : 0x2CDD,
                    "," : 0x2CDA,
                    "." : 0x2CDA,
                    "-" : 0x2CDD,
                    "_" : 0x000F,
                    "1" : 0x2C01,
                    "2" : 0x2C02,
                    "3" : 0x2C03,
                    "4" : 0x2C04,
                    "5" : 0x2C05,
                    "6" : 0x2C06,
                    "7" : 0x2C07,
                    "8" : 0x2C08,
                    "9" : 0x2C09,
                    "0" : 0x2C00,
                    "%" : 0x2C0A}
        data = []

        itemName = itemName.upper()[:26]
        itemName = itemName.strip()
        itemName = itemName.center(26, " ")    
        itemName = "___" + itemName + "___"

        for char in itemName:
            [w0, w1] = self.getWordArray(charMap.get(char, 0x2CDE))
            data.append(w0)
            data.append(w1)
        return data
    
    def current_key_pascal(self, option):
        """Converts a snake_case string to PascalCase."""
        # Replace underscores with spaces
        temp_string = option.current_key.replace("_", " ")
        # Capitalize the first letter of each word
        titled_string = temp_string.title()
        # Remove spaces to form PascalCase
        pascal_case_string = titled_string.replace(" ", "")
        return pascal_case_string
        
    def generate_output(self, output_directory: str):
        with open(get_base_rom_path(), 'rb') as stream:
            self.rom = bytearray(stream.read())

        customize_request = CustomizeRequest(
            self.rom,
            "",
            f"{self.options.etank_color_red.value:02X}{self.options.etank_color_green.value:02X}{self.options.etank_color_blue.value:02X}",
            self.current_key_pascal(self.options.item_dot_change),
            self.options.transition_letters.value == 1,
            bool(self.options.reserve_hud_style.value),
            self.options.room_palettes.current_key,
            self.current_key_pascal(self.options.tile_theme),
            self.options.door_colors.current_key,
            self.options.music.current_key,
            bool(self.options.disable_beeping.value),
            self.options.screen_shaking.current_key.title(),
            self.options.screen_flashing.current_key.title(),
            bool(self.options.screw_attack_animation.value),
            bool(self.options.room_names.value),
            self.options.shot.current_key.title(),
            self.options.jump.current_key.title(),
            self.options.dash.current_key.title(),
            self.options.item_select.current_key.title(),
            self.options.item_cancel.current_key.title(),
            self.options.angle_up.current_key.title(),
            self.options.angle_down.current_key.title(),
            "on" if "Left" in self.options.spin_lock_buttons else "off",
            "on" if "Right" in self.options.spin_lock_buttons else "off",
            "on" if "Up" in self.options.spin_lock_buttons else "off",
            "on" if "Down" in self.options.spin_lock_buttons else "off",
            "on" if "X" in self.options.spin_lock_buttons else "off",
            "on" if "Y" in self.options.spin_lock_buttons else "off",
            "on" if "A" in self.options.spin_lock_buttons else "off",
            "on" if "B" in self.options.spin_lock_buttons else "off",
            "on" if "L" in self.options.spin_lock_buttons else "off",
            "on" if "R" in self.options.spin_lock_buttons else "off",
            "on" if "Select" in self.options.spin_lock_buttons else "off",
            "on" if "Start" in self.options.spin_lock_buttons else "off",
            "on" if "Left" in self.options.quick_reload_buttons else "off",
            "on" if "Right" in self.options.quick_reload_buttons else "off",
            "on" if "Up" in self.options.quick_reload_buttons else "off",
            "on" if "Down" in self.options.quick_reload_buttons else "off",
            "on" if "X" in self.options.quick_reload_buttons else "off",
            "on" if "Y" in self.options.quick_reload_buttons else "off",
            "on" if "A" in self.options.quick_reload_buttons else "off",
            "on" if "B" in self.options.quick_reload_buttons else "off",
            "on" if "L" in self.options.quick_reload_buttons else "off",
            "on" if "R" in self.options.quick_reload_buttons else "off",
            "on" if "Select" in self.options.quick_reload_buttons else "off",
            "on" if "Start" in self.options.quick_reload_buttons else "off",
            bool(self.options.moonwalk.value)
        )
        sorted_item_locs = list(self.locations.values())
        items = []
        for itemLoc in sorted_item_locs:
            if itemLoc.address is not None:
                item_code = items_start_id
                if isinstance(itemLoc.item, SMMRItem):
                    item_code = itemLoc.item.code if itemLoc.item.code - items_start_id < SMMapRandoWorld.prog_missile_item_id else itemLoc.item.code - SMMapRandoWorld.prog_missile_item_id + SMMapRandoWorld.missile_item_id
                elif itemLoc.item.advancement:
                    if itemLoc.item.useful:
                        item_code = self.item_name_to_id['ArchipelagoUsefulProgItem']
                    else:
                        item_code = self.item_name_to_id['ArchipelagoProgItem']
                else:
                    if itemLoc.item.useful:
                        item_code = self.item_name_to_id['ArchipelagoUsefulItem']
                    else:
                        item_code = self.item_name_to_id['ArchipelagoItem']
                items.append(MapRandoItem(item_code - items_start_id))
        
        # if start location isnt Escape
        if (len(self.randomizer_ap.spoiler_log.summary) > 0):
            spheres: List[Location] = getattr(self.multiworld, "_smmr_spheres", None)
            summary =  [   (
                            sphere_idx, 
                            (loc.item.code if loc.item.code - items_start_id < SMMapRandoWorld.prog_missile_item_id else loc.item.code - SMMapRandoWorld.prog_missile_item_id + SMMapRandoWorld.missile_item_id) - items_start_id, 
                            self.multiworld.get_player_name(loc.player) + " world" if loc.player != self.player else None
                        ) 
                    for sphere_idx, sphere in enumerate(spheres) for loc in sphere if loc.item.player == self.player and loc.item.name != "Nothing"
                    ]
            
            item_spoiler_infos = []
            for item_spoiler_info in self.randomizer_ap.randomization.essential_spoiler_data.item_spoiler_info:
                for (step, item_id, location) in summary:
                    if (item_spoiler_info.item.to_int() == item_id):
                        if (location is not None):
                            item_spoiler_info.step = step
                            item_spoiler_info.area = location
                        break
                item_spoiler_infos.append(item_spoiler_info)
        else:
            item_spoiler_infos = None

        patched_rom_bytes = customize_seed_ap(
            customize_request, 
            map_rando_app_data, 
            self.map_rando_settings,
            self.randomizer_ap.randomization,
            False,
            items,
            item_spoiler_infos
            )
        #patched_rom_bytes = None
        #with open(get_base_rom_path(), "rb") as stream:
        #    patched_rom_bytes = stream.read()

        patches = []
        patches.append(IPS_Patch.load("/".join((os.path.dirname(self.__file__),
                                              "data", "SMBasepatch_prebuilt", "multiworld-basepatch.ips"))))
        symbols = get_sm_symbols("/".join((os.path.dirname(self.__file__),
                                              "data", "SMBasepatch_prebuilt", "sm-basepatch-symbols.json")))

        # gather all player ids and names relevant to this rom, then write player name and player id data tables
        playerIdSet: Set[int] = {0}  # 0 is for "Archipelago" server
        for itemLoc in self.multiworld.get_locations():
            assert itemLoc.item, f"World of player '{self.multiworld.player_name[itemLoc.player]}' has a loc.item " + \
                                 f"that is {itemLoc.item} during generate_output"
            # add each playerid who has a location containing an item to send to us *or* to an item_link we're part of
            if itemLoc.item.player == self.player or \
                    (itemLoc.item.player in self.multiworld.groups and
                     self.player in self.multiworld.groups[itemLoc.item.player]['players']):
                playerIdSet |= {itemLoc.player}
            # add each playerid, including item link ids, that we'll be sending items to
            if itemLoc.player == self.player:
                playerIdSet |= {itemLoc.item.player}
        if len(playerIdSet) > SMMR_ROM_PLAYERDATA_COUNT:
            # max 202 entries, but it's possible for item links to add enough replacement items for us, that are placed
            # in worlds that otherwise have no relation to us, that the 2*location count limit is exceeded
            logger.warning("SMMR is interacting with too many players to fit in ROM. "
                           f"Removing the highest {len(playerIdSet) - SMMR_ROM_PLAYERDATA_COUNT} ids to fit")
            playerIdSet = set(sorted(playerIdSet)[:SMMR_ROM_PLAYERDATA_COUNT])
        otherPlayerIndex: Dict[int, int] = {}  # ap player id -> rom-local player index
        playerNameData: List[ByteEdit] = []
        playerIdData: List[ByteEdit] = []
        # sort all player data by player id so that the game can look up a player's data reasonably quickly when
        # the client sends an ap playerid to the game
        for i, playerid in enumerate(sorted(playerIdSet)):
            playername = self.multiworld.player_name[playerid] if playerid != 0 else "Archipelago"
            playerIdForRom = playerid
            if playerid > SMMR_ROM_MAX_PLAYERID:
                # note, playerIdForRom = 0 is not unique so the game cannot look it up.
                # instead it will display the player received-from as "Archipelago"
                playerIdForRom = 0
                if playerid == self.player:
                    raise Exception(f"SM rom cannot fit enough bits to represent self player id {playerid}")
                else:
                    logger.warning(f"SM rom cannot fit enough bits to represent player id {playerid}, setting to 0 in rom")
            otherPlayerIndex[playerid] = i
            playerNameData.append({"sym": symbols["rando_player_name_table"],
                                   "offset": i * 16,
                                   "values": playername[:16].upper().center(16).encode()})
            playerIdData.append({"sym": symbols["rando_player_id_table"],
                                 "offset": i * 2,
                                 "values": self.getWordArray(playerIdForRom)})

        multiWorldLocations: List[ByteEdit] = []
        multiWorldItems: List[ByteEdit] = []
        idx = 0
        vanillaItemTypesCount = 23
        locations_nothing = bytearray(20)
        for itemLoc in self.multiworld.get_locations():
            if itemLoc.player == self.player:
                # item to place in this SMMR world: write full item data to tables
                if isinstance(itemLoc.item, SMMRItem) and itemLoc.item.code < items_start_id + vanillaItemTypesCount:
                    if itemLoc.item.code == items_start_id + self.nothing_item_id:
                        locations_nothing[(itemLoc.address - locations_start_id)//8] |= 1 << (itemLoc.address % 8)
                    itemId = itemLoc.item.code - items_start_id
                else:
                    itemId = self.item_name_to_id['ArchipelagoItem'] - items_start_id + idx
                    multiWorldItems.append({"sym": symbols["message_item_names"],
                                            "offset": (vanillaItemTypesCount + idx)*64,
                                            "values": self.convertToROMItemName(itemLoc.item.name)})
                    idx += 1

                if itemLoc.item.player == self.player:
                    itemDestinationType = 0  # dest type 0 means 'regular old SM item' per itemtable.asm
                elif itemLoc.item.player in self.multiworld.groups and \
                        self.player in self.multiworld.groups[itemLoc.item.player]['players']:
                    # dest type 2 means 'SM item link item that sends to the current player and others'
                    # per itemtable.asm (groups are synonymous with item_links, currently)
                    itemDestinationType = 2
                else:
                    itemDestinationType = 1  # dest type 1 means 'item for entirely someone else' per itemtable.asm

                [w0, w1] = self.getWordArray(itemDestinationType)
                [w2, w3] = self.getWordArray(itemId)
                [w4, w5] = self.getWordArray(otherPlayerIndex[itemLoc.item.player] if itemLoc.item.player in
                                             otherPlayerIndex else 0)
                [w6, w7] = self.getWordArray(0 if itemLoc.item.advancement else 1)
                multiWorldLocations.append({"sym": symbols["rando_item_table"],
                                            "offset": (itemLoc.address - locations_start_id)*8,
                                            "values": [w0, w1, w2, w3, w4, w5, w6, w7]})

        itemSprites = [{"fileName":          "off_world_prog_item.bin",
                        "paletteSymbolName": "prog_item_eight_palette_indices",
                        "dataSymbolName":    "offworld_graphics_data_progression_item"},

                       {"fileName":          "off_world_item.bin",
                        "paletteSymbolName": "nonprog_item_eight_palette_indices",
                        "dataSymbolName":    "offworld_graphics_data_item"}]
        idx = 0
        offworldSprites: List[ByteEdit] = []
        for itemSprite in itemSprites:
            with openFile("/".join((os.path.dirname(self.__file__), "data", "custom_sprite", itemSprite["fileName"])), 'rb') as stream:
                buffer = bytearray(stream.read())
                offworldSprites.append({"sym": symbols[itemSprite["paletteSymbolName"]],
                                        "offset": 0,
                                        "values": buffer[0:8]})
                offworldSprites.append({"sym": symbols[itemSprite["dataSymbolName"]],
                                        "offset": 0,
                                        "values": buffer[8:264]})
                idx += 1

        deathLink: List[ByteEdit] = [{
            "sym": symbols["config_deathlink"],
            "offset": 0,
            "values": [self.options.death_link.value]
        }]
        remoteItem: List[ByteEdit] = [{
            "sym": symbols["config_remote_items"],
            "offset": 0,
            "values": self.getWordArray(0b001 + (0b010 if self.options.remote_items else 0b000))
        }]
        ownPlayerId: List[ByteEdit] = [{
            "sym": symbols["config_player_id"],
            "offset": 0,
            "values": self.getWordArray(self.player)
        }]

        location_nothing: List[ByteEdit] = [{
            "sym": symbols["locations_nothing"],
            "offset": 0,
            "values": locations_nothing
        }]

        patchDict = {   'MultiWorldLocations': multiWorldLocations,
                        'MultiWorldItems': multiWorldItems,
                        'offworldSprites': offworldSprites,
                        'deathLink': deathLink,
                        'remoteItem': remoteItem,
                        'ownPlayerId': ownPlayerId,
                        'playerNameData':  playerNameData,
                        'playerIdData':  playerIdData,
                        'location_nothing': location_nothing}

        # convert an array of symbolic byte_edit dicts like {"sym": symobj, "offset": 0, "values": [1, 0]}
        # to a single rom patch dict like {0x438c: [1, 0], 0xa4a5: [0, 0, 0]}
        def resolve_symbols_to_file_offset_based_dict(byte_edits_arr: List[ByteEdit]) -> Dict[int, Iterable[int]]:
            this_patch_as_dict: Dict[int, Iterable[int]] = {}
            for byte_edit in byte_edits_arr:
                offset_within_rom_file: int = byte_edit["sym"]["offset_within_rom_file"] + byte_edit["offset"]
                this_patch_as_dict[offset_within_rom_file] = byte_edit["values"]
            return this_patch_as_dict

        for patchname, byte_edits_arr in patchDict.items():
            patches.append(IPS_Patch(resolve_symbols_to_file_offset_based_dict(byte_edits_arr)))
        

        # set rom name
        # 21 bytes
        from Main import __version__
        self.romName = bytearray(f'SMMR{__version__.replace(".", "")[0:3]}{required_pysmmaprando_version.replace(".", "")}{self.player}{self.multiworld.seed:8}', 'utf8')[:21]
        self.romName.extend([0] * (21 - len(self.romName)))
        self.rom_name = self.romName
        # clients should read from 0x7FC0, the location of the rom title in the SNES header.
        patches.append(IPS_Patch({0x007FC0 : self.romName}))

        # array for each item: (must match Map Rando's new_game_extra.asm !initial_X addresses)
        #  offset within ROM of this item"s info (starting status)
        #  item bitmask or amount per pickup (BVOB = base value or bitmask),
        #  offset within ROM of this item"s info (starting maximum/starting collected items)
        #  
        #                                 current  BVOB   max
        #                                 -------  ----   ---
        startItemROMDict = {"ETank":        [ snes_to_pc(0xB5FE52), 0x64, snes_to_pc(0xB5FE54)],
                            "Missile":      [ snes_to_pc(0xB5FE5C),  0x5, snes_to_pc(0xB5FE5E)],
                            "Super":        [ snes_to_pc(0xB5FE60),  0x5, snes_to_pc(0xB5FE62)],
                            "PowerBomb":    [ snes_to_pc(0xB5FE64),  0x5, snes_to_pc(0xB5FE66)],
                            "ReserveTank":  [ snes_to_pc(0xB5FE56), 0x64, snes_to_pc(0xB5FE58)],
                            "Morph":        [ snes_to_pc(0xB5FE04),  0x4, snes_to_pc(0xB5FE06)],
                            "Bombs":        [ snes_to_pc(0xB5FE05), 0x10, snes_to_pc(0xB5FE07)],
                            "SpringBall":   [ snes_to_pc(0xB5FE04),  0x2, snes_to_pc(0xB5FE06)],
                            "HiJump":       [ snes_to_pc(0xB5FE05),  0x1, snes_to_pc(0xB5FE07)],
                            "Varia":        [ snes_to_pc(0xB5FE04),  0x1, snes_to_pc(0xB5FE06)],
                            "Gravity":      [ snes_to_pc(0xB5FE04), 0x20, snes_to_pc(0xB5FE06)],
                            "SpeedBooster": [ snes_to_pc(0xB5FE05), 0x20, snes_to_pc(0xB5FE07)],
                            "SpaceJump":    [ snes_to_pc(0xB5FE05),  0x2, snes_to_pc(0xB5FE07)],
                            "ScrewAttack":  [ snes_to_pc(0xB5FE04),  0x8, snes_to_pc(0xB5FE06)],
                            "Charge":       [ snes_to_pc(0xB5FE09), 0x10, snes_to_pc(0xB5FE0B)],
                            "Ice":          [ snes_to_pc(0xB5FE08),  0x2, snes_to_pc(0xB5FE0A)],
                            "Wave":         [ snes_to_pc(0xB5FE08),  0x1, snes_to_pc(0xB5FE0A)],
                            "Spazer":       [ snes_to_pc(0xB5FE08),  0x4, snes_to_pc(0xB5FE0A)],
                            "Plasma":       [ snes_to_pc(0xB5FE08),  0x8, snes_to_pc(0xB5FE0A)],
                            "Grapple":      [ snes_to_pc(0xB5FE05), 0x40, snes_to_pc(0xB5FE07)],
                            "XRayScope":    [ snes_to_pc(0xB5FE05), 0x80, snes_to_pc(0xB5FE07)]

        # BVOB = base value or bitmask
                            }
        mergedData = {}
        hasETank = False
        hasSpazer = False
        hasPlasma = False
        for startItem in self.startItems:
            item = startItem
            if item == "ETank": hasETank = True
            if item == "Spazer": hasSpazer = True
            if item == "Plasma": hasPlasma = True
            if (item in ["ETank", "Missile", "Super", "PowerBomb", "Reserve"]):
                (currentValue, amountPerItem, maxValue) = startItemROMDict[item]
                if currentValue in mergedData:
                    mergedData[currentValue] += amountPerItem
                    mergedData[maxValue] += amountPerItem
                else:
                    mergedData[currentValue] = amountPerItem
                    mergedData[maxValue] = amountPerItem
            else:
                (collected, bitmask, equipped) = startItemROMDict[item]
                if collected in mergedData:
                    mergedData[collected] |= bitmask
                    mergedData[equipped] |= bitmask
                else:
                    mergedData[collected] = bitmask
                    mergedData[equipped] = bitmask

        if hasETank:
            # we are overwriting the starting energy, so add up the E from 99 (normal starting energy) rather than from 0
            mergedData[snes_to_pc(0xB5FE52)] += 99
            mergedData[snes_to_pc(0xB5FE54)] += 99

        if hasSpazer and hasPlasma:
            # de-equip spazer.
            # otherwise, firing the unintended spazer+plasma combo would cause massive game glitches and crashes
            mergedData[snes_to_pc(0xB5FE0A)] &= ~0x4

        for key, value in mergedData.items():
            if (key > snes_to_pc(0xB5FE0B)):
                [w0, w1] = self.getWordArray(value)
                mergedData[key] = [w0, w1]
            else:
                mergedData[key] = [value]

        patches.append(IPS_Patch(mergedData))

        # commit all the changes we've made here to the ROM
        for ips in patches:
            patched_rom_bytes = ips.apply(patched_rom_bytes)

        outfilebase = self.multiworld.get_out_file_name_base(self.player)
        outputFilename = os.path.join(output_directory, f"{outfilebase}.sfc")

        with open(outputFilename, "wb") as binary_file:
            binary_file.write(bytes(patched_rom_bytes))

        try:
            self.write_crc(outputFilename)
        except:
            raise
        else:
            patch = SMMapRandoDeltaPatch(os.path.splitext(outputFilename)[0] + SMMapRandoDeltaPatch.patch_file_ending, player=self.player,
                                            player_name=self.multiworld.player_name[self.player], patched_path=outputFilename)
            patch.write()
        finally:
            if os.path.exists(outputFilename):
                os.unlink(outputFilename)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def checksum_mirror_sum(self, start, length, mask = 0x800000):
        while not(length & mask) and mask:
            mask >>= 1

        part1 = sum(start[:mask]) & 0xFFFF
        part2 = 0

        next_length = length - mask
        if next_length:
            part2 = self.checksum_mirror_sum(start[mask:], next_length, mask >> 1)

            while (next_length < mask):
                next_length += next_length
                part2 += part2

        return (part1 + part2) & 0xFFFF

    def write_bytes(self, buffer, startaddress: int, values):
        buffer[startaddress:startaddress + len(values)] = values

    def write_crc(self, romName):
        with open(romName, 'rb') as stream:
            buffer = bytearray(stream.read())
            crc = self.checksum_mirror_sum(buffer, len(buffer))
            inv = crc ^ 0xFFFF
            self.write_bytes(buffer, 0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])
        with open(romName, 'wb') as outfile:
            outfile.write(buffer)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def fill_slot_data(self): 
        slot_data = {}
        if not self.multiworld.is_race:
            locations_nothing = [itemLoc.address - locations_start_id 
                                for itemLoc in self.locations.values()
                                if itemLoc.address is not None and itemLoc.player == self.player and itemLoc.item.code == items_start_id + self.nothing_item_id ]
        
            slot_data["locations_nothing"] = locations_nothing
                
        return slot_data
    
    # def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
    #    player_hint_data = {}
    #    for (loc_name, location) in self.locations.items():
    #        if not loc_name.startswith("f_"):
    #            player_hint_data[location.address] = self.region_area_name[location.parent_region.index]
    #    hint_data[self.player] = player_hint_data
    
    
class SMMRLocation(Location):
    game: str = SMMapRandoWorld.game

    def __init__(self, player: int, name: str, step: int, address=None, parent=None):
        super(SMMRLocation, self).__init__(player, name, address, parent)
        self.step = step

class SMMRItem(Item):
    game: str = SMMapRandoWorld.game

    def __init__(self, name, classification, code, player: int, step: int):
        super(SMMRItem, self).__init__(name, classification, code, player)
        self.step = step