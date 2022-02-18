import logging
import copy
import os
import threading
from typing import Set, List

logger = logging.getLogger("Super Metroid")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import lookup_name_to_id as items_lookup_name_to_id
from .Regions import create_regions
from .Rules import set_rules, add_entrance_rule
from .Options import sm_options
from .Rom import get_base_rom_path, ROM_PLAYER_LIMIT
import Utils

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, CollectionState
from ..AutoWorld import World, AutoLogicRegister
import Patch

from logic.smboolmanager import SMBoolManager
from graph.vanilla.graph_locations import locationsDict
from graph.graph_utils import getAccessPoint
from rando.ItemLocContainer import ItemLocation
from rando.Items import ItemManager
from utils.parameters import *
from logic.logic import Logic
from randomizer import VariaRandomizer


class SMCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        # for unit tests where MultiWorld is instantiated before worlds
        if hasattr(parent, "state"):
            self.smbm = {player: SMBoolManager(player, parent.state.smbm[player].maxDiff,
                                               parent.state.smbm[player].onlyBossLeft) for player in
                         parent.get_game_players("Super Metroid")}
        else:
            self.smbm = {}

    def copy_mixin(self, ret) -> CollectionState:
        ret.smbm = {player: copy.deepcopy(self.smbm[player]) for player in self.world.get_game_players("Super Metroid")}
        return ret


class SMWorld(World):
    game: str = "Super Metroid"
    topology_present = True
    data_version = 1
    options = sm_options
    item_names: Set[str] = frozenset(items_lookup_name_to_id)
    location_names: Set[str] = frozenset(locations_lookup_name_to_id)
    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id

    remote_items: bool = False
    remote_start_inventory: bool = False

    itemManager: ItemManager

    locations = {}
    hint_blacklist = {'Nothing', 'No Energy'}

    Logic.factory('vanilla')

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    def generate_early(self):
        Logic.factory('vanilla')

        self.variaRando = VariaRandomizer(self.world, get_base_rom_path(), self.player)
        self.world.state.smbm[self.player] = SMBoolManager(self.player, self.variaRando.maxDifficulty)

        # keeps Nothing items local so no player will ever pickup Nothing
        # doing so reduces contribution of this world to the Multiworld the more Nothing there is though
        self.world.local_items[self.player].value.add('Nothing')
        self.world.local_items[self.player].value.add('No Energy')

        if (self.variaRando.args.morphPlacement == "early"):
            self.world.local_items[self.player].value.add('Morph')

        if (len(self.variaRando.randoExec.setup.restrictedLocs) > 0):
            self.world.accessibility[self.player] = self.world.accessibility[self.player].from_text("items")
            logger.warning(f"accessibility forced to 'items' for player {self.world.get_player_name(self.player)} because of 'fun' settings")
    
    def generate_basic(self):
        itemPool = self.variaRando.container.itemPool
        self.startItems = [variaItem for item in self.world.precollected_items[self.player] for variaItem in ItemManager.Items.values() if variaItem.Name == item.name]
        if self.world.start_inventory_removes_from_pool[self.player]:
            for item in self.startItems:
                if (item in itemPool):
                    itemPool.remove(item)

        missingPool = 105 - len(itemPool) + 1
        for i in range(1, missingPool):
            itemPool.append(ItemManager.Items['Nothing'])
        
        # Generate item pool
        pool = []
        self.locked_items = {}
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
            elif item.Category == 'Nothing':
                isAdvancement = False

            itemClass = ItemManager.Items[item.Type].Class
            smitem = SMItem(item.Name, isAdvancement, item.Type, None if itemClass == 'Boss' else self.item_name_to_id[item.Name], player = self.player)
            if itemClass == 'Boss':
                self.locked_items[item.Name] = smitem
            else:
                pool.append(smitem)

        self.world.itempool += pool

        for (location, item) in self.locked_items.items():
            self.world.get_location(location, self.player).place_locked_item(item)
            self.world.get_location(location, self.player).address = None

        startAP = self.world.get_entrance('StartAP', self.player)
        startAP.connect(self.world.get_region(self.variaRando.args.startLocation, self.player))

        for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions:
            src_region = self.world.get_region(src.Name, self.player)
            dest_region = self.world.get_region(dest.Name, self.player)
            src_region.exits.append(Entrance(self.player, src.Name + "->" + dest.Name, src_region))
            srcDestEntrance = self.world.get_entrance(src.Name + "->" + dest.Name, self.player)
            srcDestEntrance.connect(dest_region)
            add_entrance_rule(self.world.get_entrance(src.Name + "->" + dest.Name, self.player), self.player, getAccessPoint(src.Name).traverse)

    def set_rules(self):
        set_rules(self.world, self.player)


    def create_regions(self):
        create_locations(self, self.player)
        create_regions(self, self.world, self.player)

    def get_required_client_version(self):
        # changes to client DeathLink handling for 0.2.1
        return max(super(SMWorld, self).get_required_client_version(), (0, 2, 1))

    def getWord(self, w):
        return (w & 0x00FF, (w & 0xFF00) >> 8)
    
    def getWordArray(self, w):
        return [w & 0x00FF, (w & 0xFF00) >> 8]

    # used for remote location Credits Spoiler of local items
    class DummyLocation:
        def __init__(self, name):
            self.Name = name

        def isBoss(self):
            return False

    def convertToROMItemName(self, itemName):
        charMap = { "A" : 0x3CE0, 
                    "B" : 0x3CE1,
                    "C" : 0x3CE2,
                    "D" : 0x3CE3,
                    "E" : 0x3CE4,
                    "F" : 0x3CE5,
                    "G" : 0x3CE6,
                    "H" : 0x3CE7,
                    "I" : 0x3CE8,
                    "J" : 0x3CE9,
                    "K" : 0x3CEA,
                    "L" : 0x3CEB,
                    "M" : 0x3CEC,
                    "N" : 0x3CED,
                    "O" : 0x3CEE,
                    "P" : 0x3CEF,
                    "Q" : 0x3CF0,
                    "R" : 0x3CF1,
                    "S" : 0x3CF2,
                    "T" : 0x3CF3,
                    "U" : 0x3CF4,
                    "V" : 0x3CF5,
                    "W" : 0x3CF6,
                    "X" : 0x3CF7,
                    "Y" : 0x3CF8,
                    "Z" : 0x3CF9,
                    " " : 0x3C4E,
                    "!" : 0x3CFF,
                    "?" : 0x3CFE,
                    "'" : 0x3CFD,
                    "," : 0x3CFB,
                    "." : 0x3CFA,
                    "-" : 0x3CCF,
                    "_" : 0x000E,
                    "1" : 0x3C00,
                    "2" : 0x3C01,
                    "3" : 0x3C02,
                    "4" : 0x3C03,
                    "5" : 0x3C04,
                    "6" : 0x3C05,
                    "7" : 0x3C06,
                    "8" : 0x3C07,
                    "9" : 0x3C08,
                    "0" : 0x3C09,
                    "%" : 0x3C0A}
        data = []

        itemName = itemName.upper()[:26]
        itemName = itemName.strip()
        itemName = itemName.center(26, " ")    
        itemName = "___" + itemName + "___"

        for char in itemName:
            (w0, w1) = self.getWord(charMap.get(char, 0x3C4E))
            data.append(w0)
            data.append(w1)
        return data

    def APPatchRom(self, romPatcher):
        multiWorldLocations = {}
        multiWorldItems = {}
        idx = 0
        itemId = 0
        self.playerIDMap = {}
        playerIDCount = 0 # 0 is for "Archipelago" server
        for itemLoc in self.world.get_locations():
            romPlayerID = itemLoc.item.player if itemLoc.item.player <= ROM_PLAYER_LIMIT else 0
            if itemLoc.player == self.player and locationsDict[itemLoc.name].Id != None:
                if itemLoc.item.type in ItemManager.Items:
                    itemId = ItemManager.Items[itemLoc.item.type].Id 
                else:
                    itemId = ItemManager.Items['ArchipelagoItem'].Id + idx
                    multiWorldItems[0x029EA3 + idx*64] = self.convertToROMItemName(itemLoc.item.name)
                    idx += 1
                
                if (romPlayerID > 0 and romPlayerID not in self.playerIDMap.keys()):
                    playerIDCount += 1
                    self.playerIDMap[romPlayerID] = playerIDCount

                (w0, w1) = self.getWord(0 if itemLoc.item.player == self.player else 1)
                (w2, w3) = self.getWord(itemId)
                (w4, w5) = self.getWord(romPlayerID)
                (w6, w7) = self.getWord(0 if itemLoc.item.advancement else 1)
                multiWorldLocations[0x1C6000 + locationsDict[itemLoc.name].Id*8] = [w0, w1, w2, w3, w4, w5, w6, w7]

            if itemLoc.item.player == self.player:
                if (romPlayerID > 0 and romPlayerID not in self.playerIDMap.keys()):
                    playerIDCount += 1
                    self.playerIDMap[romPlayerID] = playerIDCount

        itemSprites = ["off_world_prog_item.bin", "off_world_item.bin"]
        idx = 0
        offworldSprites = {}
        for fileName in itemSprites:
            with open(Utils.local_path("lib", "worlds", "sm", "data", "custom_sprite", fileName) if Utils.is_frozen() else Utils.local_path("worlds", "sm", "data", "custom_sprite", fileName), 'rb') as stream:
                buffer = bytearray(stream.read())
                offworldSprites[0x027882 + 10*(21 + idx) + 2] = buffer[0:8]
                offworldSprites[0x049100 + idx*256] = buffer[8:264]
                idx += 1
            
        openTourianGreyDoors = {0x07C823 + 5: [0x0C], 0x07C831 + 5: [0x0C]}

        deathLink = {0x277f04: [self.world.death_link[self.player].value]}

        playerNames = {}
        playerNameIDMap = {}
        playerNames[0x1C5000] = "Archipelago".upper().center(16).encode()
        playerNameIDMap[0x1C5800] = self.getWordArray(0)
        for key,value in self.playerIDMap.items():
            playerNames[0x1C5000 + value * 16] = self.world.player_name[key][:16].upper().center(16).encode()
            playerNameIDMap[0x1C5800 + value * 2] = self.getWordArray(key)

        patchDict = {   'MultiWorldLocations': multiWorldLocations,
                        'MultiWorldItems': multiWorldItems,
                        'offworldSprites': offworldSprites,
                        'openTourianGreyDoors': openTourianGreyDoors,
                        'deathLink': deathLink,
                        'PlayerName':  playerNames,
                        'PlayerNameIDMap':  playerNameIDMap}
        romPatcher.applyIPSPatchDict(patchDict)

        # set rom name
        # 21 bytes
        from Main import __version__
        self.romName = bytearray(f'SM{__version__.replace(".", "")[0:3]}_{self.player}_{self.world.seed:11}\0', 'utf8')[:21]
        self.romName.extend([0] * (21 - len(self.romName)))
        romPatcher.applyIPSPatch('ROMName', { 'ROMName':  {0x1C4F00 : self.romName, 0x007FC0 : self.romName} })

        startItemROMAddressBase = 0x2FD8B9

        # current, base value or bitmask, max, base value or bitmask
        startItemROMDict = {'ETank': [0x8, 0x64, 0xA, 0x64],
                            'Missile': [0xC, 0x5, 0xE, 0x5],
                            'Super': [0x10, 0x5, 0x12, 0x5],
                            'PowerBomb': [0x14, 0x5, 0x16, 0x5],
                            'Reserve': [0x1A, 0x64, 0x18, 0x64],
                            'Morph': [0x2, 0x4, 0x0, 0x4],
                            'Bomb': [0x3, 0x10, 0x1, 0x10],
                            'SpringBall': [0x2, 0x2, 0x0, 0x2],
                            'HiJump': [0x3, 0x1, 0x1, 0x1],
                            'Varia': [0x2, 0x1, 0x0, 0x1],
                            'Gravity': [0x2, 0x20, 0x0, 0x20],
                            'SpeedBooster': [0x3, 0x20, 0x1, 0x20],
                            'SpaceJump': [0x3, 0x2, 0x1, 0x2],
                            'ScrewAttack': [0x2, 0x8, 0x0, 0x8],
                            'Charge': [0x7, 0x10, 0x5, 0x10],
                            'Ice': [0x6, 0x2, 0x4, 0x2], 
                            'Wave': [0x6, 0x1, 0x4, 0x1],
                            'Spazer': [0x6, 0x4, 0x4, 0x4], 
                            'Plasma': [0x6, 0x8, 0x4, 0x8],
                            'Grapple': [0x3, 0x40, 0x1, 0x40],
                            'XRayScope': [0x3, 0x80, 0x1, 0x80]
                            }
        mergedData = {}
        hasETank = False
        hasSpazer = False
        hasPlasma = False
        for startItem in self.startItems:
            item = startItem.Type
            if item == 'ETank': hasETank = True
            if item == 'Spazer': hasSpazer = True
            if item == 'Plasma': hasPlasma = True
            if (item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Reserve']):
                (currentValue, currentBase, maxValue, maxBase) = startItemROMDict[item]
                if (startItemROMAddressBase + currentValue) in mergedData:
                    mergedData[startItemROMAddressBase + currentValue] += currentBase
                    mergedData[startItemROMAddressBase + maxValue] += maxBase
                else:
                    mergedData[startItemROMAddressBase + currentValue] = currentBase
                    mergedData[startItemROMAddressBase + maxValue] = maxBase
            else:
                (collected, currentBitmask, equipped, maxBitmask) = startItemROMDict[item]
                if (startItemROMAddressBase + collected) in mergedData:
                    mergedData[startItemROMAddressBase + collected] |= currentBitmask
                    mergedData[startItemROMAddressBase + equipped] |= maxBitmask
                else:
                    mergedData[startItemROMAddressBase + collected] = currentBitmask
                    mergedData[startItemROMAddressBase + equipped] = maxBitmask

        if hasETank:
            mergedData[startItemROMAddressBase + 0x8] += 99
            mergedData[startItemROMAddressBase + 0xA] += 99

        if hasSpazer and hasPlasma:
            mergedData[startItemROMAddressBase + 0x4] &= ~0x4

        for key, value in mergedData.items():
            if (key - startItemROMAddressBase > 7):
                (w0, w1) = self.getWord(value)
                mergedData[key] = [w0, w1]
            else:
                mergedData[key] = [value]
            

        startItemPatch = { 'startItemPatch':  mergedData }
        romPatcher.applyIPSPatch('startItemPatch', startItemPatch)

        romPatcher.commitIPS()

        itemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type if itemLoc.item.type in ItemManager.Items else 'ArchipelagoItem'], locationsDict[itemLoc.name], True) for itemLoc in self.world.get_locations() if itemLoc.player == self.player]
        romPatcher.writeItemsLocs(itemLocs) 

        itemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type], locationsDict[itemLoc.name] if itemLoc.name in locationsDict and itemLoc.player == self.player else self.DummyLocation(self.world.get_player_name(itemLoc.player) + " " + itemLoc.name), True) for itemLoc in self.world.get_locations() if itemLoc.item.player == self.player] 
        progItemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type], locationsDict[itemLoc.name] if itemLoc.name in locationsDict and itemLoc.player == self.player else self.DummyLocation(self.world.get_player_name(itemLoc.player) + " " + itemLoc.name), True) for itemLoc in self.world.get_locations() if itemLoc.item.player == self.player and itemLoc.item.advancement == True] 
        # progItemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type if itemLoc.item.type in ItemManager.Items else 'ArchipelagoItem'], locationsDict[itemLoc.name], True) for itemLoc in self.world.get_locations() if itemLoc.player == self.player and itemLoc.item.player == self.player and itemLoc.item.advancement == True]
        
        # romPatcher.writeSplitLocs(self.variaRando.args.majorsSplit, itemLocs, progItemLocs)
        romPatcher.writeSpoiler(itemLocs, progItemLocs)
        romPatcher.writeRandoSettings(self.variaRando.randoExec.randoSettings, itemLocs)

    def generate_output(self, output_directory: str):
        try:
            outfilebase = 'AP_' + self.world.seed_name
            outfilepname = f'_P{self.player}'
            outfilepname += f"_{self.world.player_name[self.player].replace(' ', '_')}" \

            outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.sfc')
            self.variaRando.PatchRom(outputFilename, self.APPatchRom)

            self.write_crc(outputFilename)

            Patch.create_patch_file(outputFilename, player=self.player, player_name=self.world.player_name[self.player], game=Patch.GAME_SM)
            os.unlink(outputFilename)
            self.rom_name = self.romName
        except:
            raise
        finally:
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def checksum_mirror_sum(self, start, length, mask = 0x800000):
        while (not(length & mask) and mask):
            mask >>= 1

        part1 = sum(start[:mask]) & 0xFFFF
        part2 = 0

        next_length = length - mask
        if next_length:
            part2 = self.checksum_mirror_sum(start[mask:], next_length, mask >> 1)

            while (next_length < mask):
                next_length += next_length
                part2 += part2

            length = mask + mask

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
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]


    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.smbm[self.player].addItem(item.type)
        return super(SMWorld, self).collect(state, item)

    def remove(self, state: CollectionState, item: Item) -> bool:
        state.smbm[self.player].removeItem(item.type)
        return super(SMWorld, self).remove(state, item)

    def create_item(self, name: str) -> Item:
        item = next(x for x in ItemManager.Items.values() if x.Name == name)
        return SMItem(item.Name, True, item.Type, self.item_name_to_id[item.Name], player = self.player)

    def pre_fill(self):
        if (self.variaRando.args.morphPlacement == "early") and next((item for item in self.world.itempool if item.player == self.player and item.name == "Morph Ball"), False):
            viable = []
            for location in self.world.get_locations():
                if location.player == self.player \
                        and location.item is None \
                        and location.can_reach(self.world.state):
                    viable.append(location)
            self.world.random.shuffle(viable)
            key = self.world.create_item("Morph Ball", self.player)
            loc = viable.pop()
            loc.place_locked_item(key)
            self.world.itempool[:] = [item for item in self.world.itempool if
                                        item.player != self.player or
                                        item.name != "Morph Ball"] 

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, nonlocalrestitempool,
                        restitempool, fill_locations):      
        if world.get_game_players("Super Metroid"):
            progitempool.sort(
                key=lambda item: 1 if (item.name == 'Morph Ball') else 0)

    def post_fill(self):
        new_state = CollectionState(self.world)
        progitempool = []
        for item in self.world.itempool:
            if item.player == self.player and item.advancement:
                progitempool.append(item)

        for item in progitempool:
            new_state.collect(item, True)

        bossesLoc = ['Draygon', 'Kraid', 'Ridley', 'Phantoon', 'Mother Brain']
        for bossLoc in bossesLoc:
            if (not self.world.get_location(bossLoc, self.player).can_reach(new_state)):
                self.world.state.smbm[self.player].onlyBossLeft = True
                break

def create_locations(self, player: int):
    for name, id in locations_lookup_name_to_id.items():
        self.locations[name] = SMLocation(player, name, id)

def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.LightWorld, name, player)
    ret.world = world
    if locations:
        for loc in locations:
            location = self.locations[loc]
            location.parent_region = ret
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    return ret


class SMLocation(Location):
    game: str = "Super Metroid"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SMLocation, self).__init__(player, name, address, parent)

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        return self.always_allow(state, item) or (self.item_rule(item) and (not check_access or self.can_reach(state)))


class SMItem(Item):
    game = "Super Metroid"

    def __init__(self, name, advancement, type, code, player: int = None):
        super(SMItem, self).__init__(name, advancement, code, player)
        self.type = type
