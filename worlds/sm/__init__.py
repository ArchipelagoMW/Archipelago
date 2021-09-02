import logging
import copy
import os
from typing import Set

logger = logging.getLogger("Super Metroid")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import lookup_id_to_name as items_lookup_id_to_name
from .Items import lookup_name_to_id as items_lookup_name_to_id
from .Regions import create_regions
from .Rules import set_rules, add_entrance_rule
from .Options import sm_options

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, CollectionState
from ..AutoWorld import World

from logic.smboolmanager import SMBoolManager
from rom.rompatcher import RomPatcher
from graph.vanilla.graph_locations import locationsDict
from graph.graph_utils import getAccessPoint
from rando.ItemLocContainer import ItemLocation
from rando.Items import ItemManager
from utils.parameters import *
from logic.logic import Logic
from randomizer import VariaRandomizer

from Utils import output_path
from shutil import copy2

class SMWorld(World):
    game: str = "Super Metroid"
    topology_present = True
    options = sm_options
    item_names: Set[str] = frozenset(items_lookup_name_to_id)
    location_names: Set[str] = frozenset(locations_lookup_name_to_id)
    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id

    remote_items: bool = False

    qty = {'energy': 'vanilla',
           'minors': 100,
           'ammo': { 'Missile': 9,
                     'Super': 9,
                     'PowerBomb': 9 },
           'strictMinors' : False }

    itemManager: ItemManager

    locations = {}

    Logic.factory('vanilla')

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def __new__(cls, world, player):
        
        # Add necessary objects to CollectionState on initialization
        orig_init = CollectionState.__init__
        orig_copy = CollectionState.copy

        def sm_init(self, parent: MultiWorld):
            orig_init(self, parent)
            self.smbm = {player: SMBoolManager(player) for player in range(1, parent.players + 1)}

        def sm_copy(self):
            ret = orig_copy(self)
            ret.smbm = {player: copy.deepcopy(self.smbm[player]) for player in range(1, self.world.players + 1)}
            return ret

        CollectionState.__init__ = sm_init
        CollectionState.copy = sm_copy

        if world:
            world.state.smbm = None

        return super().__new__(cls)
    
    def generate_basic(self):
        Logic.factory('vanilla')

        self.variaRando = VariaRandomizer(self.world.sm_rom, self.world.randoPreset[self.player], self.player)

        # also need to add the names to the passed MultiWorld's CollectionState, since it was initialized before we could get to it
        if self.world.state.smbm == None:
            self.world.state.smbm = {player: SMBoolManager(player) for player in range(1, self.world.players + 1)}

        itemPool = self.variaRando.container.itemPool
        
        # Generate item pool
        pool = []
        locked_items = {}
        weaponCount = [0, 0, 0]
        for item in itemPool:
            isAdvancement = True
            if item.Type == 'Missile':
                if weaponCount[0] < 3:
                    weaponCount[0] += 1
                else:
                    isAdvancement = False
            elif item.Type == 'Super':
                if weaponCount[1] < 2:
                    weaponCount[1] += 1
                else:
                    isAdvancement = False
            elif item.Type == 'PowerBomb':
                if weaponCount[2] < 3:
                    weaponCount[2] += 1
                else:
                    isAdvancement = False

            itemClass = ItemManager.Items[item.Type].Class
            smitem = SMItem(item.Name, isAdvancement, item.Type, None if itemClass == 'Boss' else self.item_name_to_id[item.Name], player = self.player)
            if itemClass == 'Boss':
                locked_items[item.Name] = smitem
            else:
                pool.append(smitem)

        self.world.itempool += pool

        for (location, item) in locked_items.items():
            self.world.get_location(location, self.player).place_locked_item(item)

        startAP = self.world.get_entrance('StartAP', self.player)
        startAP.connect(self.world.get_region(self.variaRando.args.startLocation, self.player))

        for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions:
            src_region = self.world.get_region(src.Name, self.player)
            dest_region = self.world.get_region(dest.Name, self.player)
            src_region.exits.append(Entrance(self.player, src.Name + "|" + dest.Name, src_region))
            srcDestEntrance = self.world.get_entrance(src.Name + "|" + dest.Name, self.player)
            srcDestEntrance.connect(dest_region)
            add_entrance_rule(self.world.get_entrance(src.Name + "|" + dest.Name, self.player), self.player, getAccessPoint(src.Name).traverse)

    def set_rules(self):
        set_rules(self.world, self.player)


    def create_regions(self):
        create_locations(self, self.player)
        create_regions(self, self.world, self.player)

    def getWord(self, w):
        return (w & 0x00FF, (w & 0xFF00) >> 8)

    def APPatchRom(self, romPatcher):
        multiWorldLocations = {}
        for itemLoc in self.world.get_locations():
            if itemLoc.player == self.player and locationsDict[itemLoc.name].Id != None:
                item = ItemManager.Items[itemLoc.item.type if itemLoc.item.type in ItemManager.Items else 'ArchipelagoItem']
                (w0, w1) = self.getWord(0 if itemLoc.item.player == self.player else 1)
                (w2, w3) = self.getWord(item.Id)
                (w4, w5) = self.getWord(itemLoc.item.player - 1)
                (w6, w7) = self.getWord(0)
                multiWorldLocations[0x1C6000 + locationsDict[itemLoc.name].Id*8] = [w0, w1, w2, w3, w4, w5, w6, w7]

            
        patchDict = { 'MultiWorldLocations':  multiWorldLocations }
        romPatcher.applyIPSPatch('MultiWorldLocations', patchDict)

        playerNames = {0x1C4F00 : self.world.player_name[self.player].encode()}
        for p in range(1, self.world.players + 1):
            playerNames[0x1C5000 + (p - 1) * 16] = self.world.player_name[p][:12].upper().center(12).encode()

        romPatcher.applyIPSPatch('PlayerName', { 'PlayerName':  playerNames })

        romPatcher.commitIPS()

        itemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type if itemLoc.item.type in ItemManager.Items else 'ArchipelagoItem'], locationsDict[itemLoc.name], True) for itemLoc in self.world.get_locations() if itemLoc.player == self.player]
        romPatcher.writeItemsLocs(itemLocs)

    def generate_output(self, output_directory: str):
        outfilebase = 'AP_' + self.world.seed_name
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.world.player_name[self.player].replace(' ', '_')}" \
        
        outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.sfc')
        # copy2("Super Metroid (JU)[!].sfc", outputFilename)
        self.variaRando.PatchRom(outputFilename, self.APPatchRom)

        #for player in self.world.get_game_players("Super Metroid"):
            # outfilebase = 'AP_' + self.world.seed_name
            # outfilepname = f'_P{player}'
            # outfilepname += f"_{self.world.player_name[player].replace(' ', '_')}" \

            # outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.sfc')
            # copy2("Super Metroid (JU)[!].sfc", outputFilename)
            # romPatcher = RomPatcher(outputFilename, None)

            # romPatcher.applyIPSPatches()

            # multiWorldLocations = {}
            # for itemLoc in self.world.get_locations():
            #     if itemLoc.player == player and locationsDict[itemLoc.name].Id != None:
            #         item = self.itemManager.Items[itemLoc.item.type if itemLoc.item.type in self.itemManager.Items else 'ArchipelagoItem']
            #         (w0, w1) = self.getWord(0 if itemLoc.item.player == player else 1)
            #         (w2, w3) = self.getWord(item.Id)
            #         (w4, w5) = self.getWord(itemLoc.item.player - 1)
            #         (w6, w7) = self.getWord(0)
            #         multiWorldLocations[0x1C6000 + locationsDict[itemLoc.name].Id*8] = [w0, w1, w2, w3, w4, w5, w6, w7]

              
            # patchDict = { 'MultiWorldLocations':  multiWorldLocations }
            # romPatcher.applyIPSPatch('MultiWorldLocations', patchDict)

            # playerNames = {0x1C4F00 : self.world.player_name[player].encode()}
            # for p in range(1, self.world.players + 1):
            #     playerNames[0x1C5000 + (p - 1) * 16] = self.world.player_name[p][:12].upper().center(12).encode()

            # romPatcher.applyIPSPatch('PlayerName', { 'PlayerName':  playerNames })

            # romPatcher.commitIPS()

            # itemLocs = [ItemLocation(self.itemManager.Items[itemLoc.item.type if itemLoc.item.type in self.itemManager.Items else 'ArchipelagoItem'], locationsDict[itemLoc.name], True) for itemLoc in self.world.get_locations() if itemLoc.player == player]
            # romPatcher.writeItemsLocs(itemLocs)
            # romPatcher.end()

        pass


    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.smbm[item.player].addItem(item.type)
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True  # indicate that a logical state change has occured
        return False

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, restitempool, fill_locations):
        if world.get_game_players("Super Metroid"):
            progitempool.sort(
                key=lambda item: 1 if (item.name == 'Morph Ball') else 0)

def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["lttp_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name

def create_locations(self, player: int):
    for name, id in locations_lookup_name_to_id.items():
        self.locations[name] = SMLocation(player, name, id)

def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.LightWorld, name, player)
    ret.world = world
    if locations:
        for loc in locations:
            location = self.locations[loc]
            location.parent_regions.append(ret)
            location.parent_region = ret
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    return ret


class SMLocation(Location):
    game: str = "Super Metroid"

    def __init__(self, player: int, name: str, address=None, parent=None):
        self.parent_regions = []
        super(SMLocation, self).__init__(player, name, address, parent)

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        return self.always_allow(state, item) or (any(region.can_fill(item) for region in self.parent_regions) and self.item_rule(item) and (not check_access or self.can_reach(state)))

    def can_reach(self, state: CollectionState) -> bool:
        # self.access_rule computes faster on average, so placing it first for faster abort
        if self.access_rule(state) and any(region.can_reach(state) for region in self.parent_regions):
            return True
        return False


class SMItem(Item):
    game = "Super Metroid"

    def __init__(self, name, advancement, type, code, player: int = None):
        super(SMItem, self).__init__(name, advancement, code, player)
        self.type = type