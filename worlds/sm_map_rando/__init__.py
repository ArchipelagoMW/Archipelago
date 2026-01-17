from __future__ import annotations

from collections import Counter
import logging
import copy
import os
import platform
import pkgutil
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

from .Rom import make_ips_patches, SMMapRandoProcedurePatch
from .ips import IPS_Patch
from .Client import SMMRSNIClient
from .ItemMatching import match_item_metroid, match_item_generic
from importlib.metadata import version, PackageNotFoundError

required_pysmmaprando_version = "0.119.2+experimental2"

class WrongVersionError(Exception):
    pass

try:
    if version("pysmmaprando") != required_pysmmaprando_version:
        raise WrongVersionError
    from pysmmaprando import build_app_data, validate_settings_ap, randomize_ap, customize_seed_ap, randomization_to_json, CustomizeRequest, Item as MapRandoItem

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
    map_rando_lib_file = f'https://github.com/snowflav-goob/MapRandomizer/releases/download/v{required_pysmmaprando_version}/pysmmaprando-{required_pysmmaprando_version}-{python_version}-{abi_version}.whl'
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
            
    from pysmmaprando import build_app_data, validate_settings_ap, randomize_ap, customize_seed_ap, randomization_to_json, CustomizeRequest, Item as MapRandoItem

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

location_address_to_id = json.loads(pkgutil.get_data(__name__, "/".join(("data", "loc_address_to_id.json"))).decode("utf-8"))

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

    def generate_output(self, output_directory: str):
        try:
            randomization = self.randomizer_ap.randomization
            sorted_item_locs = list(self.locations.values())
            items = []
            if self.options.item_matching.value == 0: # ItemMatching.option_metroid:
                match_item = match_item_metroid
            else:
                match_item = match_item_generic

            for itemLoc in sorted_item_locs:
                if itemLoc.address is None:
                    continue
                if itemLoc.item.player == self.player:
                    item_code = itemLoc.item.code if itemLoc.item.code - items_start_id < SMMapRandoWorld.prog_missile_item_id else itemLoc.item.code - SMMapRandoWorld.prog_missile_item_id + SMMapRandoWorld.missile_item_id
                else:
                    item_code = match_item(self, itemLoc.item)
                items.append(MapRandoItem(item_code - items_start_id))

            randomization.item_placement = items

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

                # pyo3 is stupid and the process must be broken down into these steps to actually replace data
                esd = randomization.essential_spoiler_data
                esd.item_spoiler_info = item_spoiler_infos
                randomization.essential_spoiler_data = esd

            self.randomizer_ap.randomization = randomization

            ips_patches = make_ips_patches(self, match_item)

            customize_settings = self.options.as_dict(
                "etank_color_red", "etank_color_green", "etank_color_blue",
                "item_dot_change",
                "transition_letters",
                "reserve_hud_style",
                "room_palettes",
                "tile_theme",
                "door_colors",
                "music",
                "disable_beeping",
                "screen_shaking", "screen_flashing",
                "screw_attack_animation",
                "room_names",
                "shot", "jump", "dash",
                "item_select", "item_cancel",
                "angle_up", "angle_down",
                "spin_lock_buttons", "quick_reload_buttons",
                "moonwalk"
            )

            randomizer_data = {
                "customize_settings": customize_settings,
                "map_rando_settings": self.options.map_rando_options.value,
                "randomization": randomization_to_json(self.randomizer_ap.randomization),
            }

            patch = SMMapRandoProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("rando_data.json", json.dumps(randomizer_data).encode("utf-8"))
            for ips_patch_name, ips in ips_patches.items():
                patch.procedure[1][1].append(ips_patch_name)
                patch.write_file(f"{ips_patch_name}.ips", ips.encode())

            outfilebase = self.multiworld.get_out_file_name_base(self.player)
            patch.write(os.path.join(output_directory, f"{outfilebase}{patch.patch_file_ending}"))
        except:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

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
    
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        map_layout = self.options.map_rando_options.value.get("map_layout", None)
        if map_layout is not None and map_layout == "Vanilla":
            return
        player_hint_data = {}
        for spoilerSummary in self.randomizer_ap.spoiler_log.summary:
            for spoilerItemSummary in spoilerSummary.items:
                loc_name = f"{spoilerItemSummary.location.room} {spoilerItemSummary.location.node}"
                player_hint_data[self.location_name_to_id[loc_name]] = spoilerItemSummary.location.area
        hint_data[self.player] = player_hint_data
    
    
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
