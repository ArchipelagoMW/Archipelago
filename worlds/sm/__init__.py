from __future__ import annotations

import logging
import copy
import os
import threading
import base64
from typing import Any, Dict, Iterable, List, Set, TextIO, TypedDict

from worlds.sm.variaRandomizer.graph.graph_utils import GraphUtils

logger = logging.getLogger("Super Metroid")

from .Regions import create_regions
from .Rules import set_rules, add_entrance_rule
from .Options import sm_options
from .Client import SMSNIClient
from .Rom import get_base_rom_path, SM_ROM_MAX_PLAYERID, SM_ROM_PLAYERDATA_COUNT, SMDeltaPatch, get_sm_symbols
import Utils

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, CollectionState, Tutorial
from ..AutoWorld import World, AutoLogicRegister, WebWorld

from logic.smboolmanager import SMBoolManager
from graph.vanilla.graph_locations import locationsDict
from graph.graph_utils import getAccessPoint
from rando.ItemLocContainer import ItemLocation
from rando.Items import ItemManager
from utils.parameters import *
from logic.logic import Logic
from randomizer import VariaRandomizer
from utils.doorsmanager import DoorsManager
from rom.rom_patches import RomPatches


class SMCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        
        # for unit tests where MultiWorld is instantiated before worlds
        if hasattr(parent, "state"):
            self.smbm = {player: SMBoolManager(player, parent.state.smbm[player].maxDiff,
                                    parent.state.smbm[player].onlyBossLeft, parent.state.smbm[player].lastAP) for player in
                                        parent.get_game_players("Super Metroid")}
            for player, group in parent.groups.items():
                if (group["game"] == "Super Metroid"):
                    self.smbm[player] = SMBoolManager(player)
                    if player not in parent.state.smbm:
                        parent.state.smbm[player] = SMBoolManager(player)
        else:
            self.smbm = {}

    def copy_mixin(self, ret) -> CollectionState:
        ret.smbm = {player: copy.deepcopy(self.smbm[player]) for player in self.smbm}
        return ret

    def get_game_players(self, multiword: MultiWorld, game_name: str):
        return tuple(player for player in multiword.get_all_ids() if multiword.game[player] == game_name)


class SMWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Metroid Client on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )]


class ByteEdit(TypedDict):
    sym: Dict[str, Any]
    offset: int
    values: Iterable[int]


locations_start_id = 82000
items_start_id = 83000

class SMWorld(World):
    """
     This is Very Adaptive Randomizer of Items and Areas for Super Metroid (VARIA SM). It supports
     a wide range of options to randomize Item locations, required skills and even the connections 
     between the main Areas!
    """

    game: str = "Super Metroid"
    topology_present = True
    data_version = 2
    option_definitions = sm_options

    item_name_to_id = {value.Name: items_start_id + value.Id for key, value in ItemManager.Items.items() if value.Id != None}
    location_name_to_id = {key: locations_start_id + value.Id for key, value in locationsDict.items() if value.Id != None}
    web = SMWeb()

    # changes to client DeathLink handling for 0.2.1
    # changes to client Remote Item handling for 0.2.6
    required_client_version = (0, 2, 6)

    itemManager: ItemManager

    Logic.factory('vanilla')

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.locations = {}
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self):
        Logic.factory('vanilla')

        self.variaRando = VariaRandomizer(self.multiworld, get_base_rom_path(), self.player)
        self.multiworld.state.smbm[self.player] = SMBoolManager(self.player, self.variaRando.maxDifficulty, lastAP = self.variaRando.args.startLocation)

        # keeps Nothing items local so no player will ever pickup Nothing
        # doing so reduces contribution of this world to the Multiworld the more Nothing there is though
        self.multiworld.local_items[self.player].value.add('Nothing')
        self.multiworld.local_items[self.player].value.add('No Energy')

        if (self.variaRando.args.morphPlacement == "early"):
            self.multiworld.local_early_items[self.player]['Morph Ball'] = 1

        self.remote_items = self.multiworld.remote_items[self.player]

        if (len(self.variaRando.randoExec.setup.restrictedLocs) > 0):
            self.multiworld.accessibility[self.player] = self.multiworld.accessibility[self.player].from_text("minimal")
            logger.warning(f"accessibility forced to 'minimal' for player {self.multiworld.get_player_name(self.player)} because of 'fun' settings")
    
    def generate_basic(self):
        itemPool = self.variaRando.container.itemPool
        self.startItems = [variaItem for item in self.multiworld.precollected_items[self.player] for variaItem in ItemManager.Items.values() if variaItem.Name == item.name]
        if self.multiworld.start_inventory_removes_from_pool[self.player]:
            for item in self.startItems:
                if (item in itemPool):
                    itemPool.remove(item)

        missingPool = 105 - len(itemPool) + 1
        for i in range(1, missingPool):
            itemPool.append(ItemManager.Items['Nothing'])
        
        # Generate item pool
        pool = []
        self.locked_items = {}
        self.NothingPool = []
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
            smitem = SMItem(item.Name, ItemClassification.progression if isAdvancement else ItemClassification.filler,
                            item.Type, None if itemClass == 'Boss' else self.item_name_to_id[item.Name], player=self.player)
            if itemClass == 'Boss':
                self.locked_items[item.Name] = smitem
            elif item.Category == 'Nothing':
                self.NothingPool.append(smitem)
            else:
                pool.append(smitem)

        self.multiworld.itempool += pool

        for (location, item) in self.locked_items.items():
            self.multiworld.get_location(location, self.player).place_locked_item(item)
            self.multiworld.get_location(location, self.player).address = None

        startAP = self.multiworld.get_entrance('StartAP', self.player)
        startAP.connect(self.multiworld.get_region(self.variaRando.args.startLocation, self.player))

        for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions:
            src_region = self.multiworld.get_region(src.Name, self.player)
            dest_region = self.multiworld.get_region(dest.Name, self.player)
            if ((src.Name + "->" + dest.Name, self.player) not in self.multiworld._entrance_cache):
                src_region.exits.append(Entrance(self.player, src.Name + "->" + dest.Name, src_region))
            srcDestEntrance = self.multiworld.get_entrance(src.Name + "->" + dest.Name, self.player)
            srcDestEntrance.connect(dest_region)
            add_entrance_rule(self.multiworld.get_entrance(src.Name + "->" + dest.Name, self.player), self.player, getAccessPoint(src.Name).traverse)

    def set_rules(self):
        set_rules(self.multiworld, self.player)


    def create_regions(self):
        create_locations(self, self.player)
        create_regions(self, self.multiworld, self.player)

    def getWordArray(self, w: int) -> List[int]:
        """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
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
            [w0, w1] = self.getWordArray(charMap.get(char, 0x3C4E))
            data.append(w0)
            data.append(w1)
        return data

    def APPrePatchRom(self, romPatcher):
        # first apply the sm multiworld code patch named 'basepatch' (also has empty tables that we'll overwrite),
        #  + apply some patches from varia that we want to be always-on.
        # basepatch and variapatches are both generated from https://github.com/lordlou/SMBasepatch
        romPatcher.applyIPSPatch(os.path.join(os.path.dirname(__file__),
                                              "data", "SMBasepatch_prebuilt", "multiworld-basepatch.ips"))
        romPatcher.applyIPSPatch(os.path.join(os.path.dirname(__file__),
                                              "data", "SMBasepatch_prebuilt", "variapatches.ips"))

    def APPostPatchRom(self, romPatcher):
        symbols = get_sm_symbols(os.path.join(os.path.dirname(__file__),
                                              "data", "SMBasepatch_prebuilt", "sm-basepatch-symbols.json"))

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
        if len(playerIdSet) > SM_ROM_PLAYERDATA_COUNT:
            # max 202 entries, but it's possible for item links to add enough replacement items for us, that are placed
            # in worlds that otherwise have no relation to us, that the 2*location count limit is exceeded
            logger.warning("SM is interacting with too many players to fit in ROM. "
                           f"Removing the highest {len(playerIdSet) - SM_ROM_PLAYERDATA_COUNT} ids to fit")
            playerIdSet = set(sorted(playerIdSet)[:SM_ROM_PLAYERDATA_COUNT])
        otherPlayerIndex: Dict[int, int] = {}  # ap player id -> rom-local player index
        playerNameData: List[ByteEdit] = []
        playerIdData: List[ByteEdit] = []
        # sort all player data by player id so that the game can look up a player's data reasonably quickly when
        # the client sends an ap playerid to the game
        for i, playerid in enumerate(sorted(playerIdSet)):
            playername = self.multiworld.player_name[playerid] if playerid != 0 else "Archipelago"
            playerIdForRom = playerid
            if playerid > SM_ROM_MAX_PLAYERID:
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
        vanillaItemTypesCount = 21
        for itemLoc in self.multiworld.get_locations():
            if itemLoc.player == self.player and locationsDict[itemLoc.name].Id != None:
                # item to place in this SM world: write full item data to tables
                if isinstance(itemLoc.item, SMItem) and itemLoc.item.type in ItemManager.Items:
                    itemId = ItemManager.Items[itemLoc.item.type].Id
                else:
                    itemId = ItemManager.Items["ArchipelagoItem"].Id + idx
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
                                            "offset": locationsDict[itemLoc.name].Id*8,
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
            with open(os.path.join(os.path.dirname(__file__), "data", "custom_sprite", itemSprite["fileName"]), 'rb') as stream:
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
            "values": [self.multiworld.death_link[self.player].value]
        }]
        remoteItem: List[ByteEdit] = [{
            "sym": symbols["config_remote_items"],
            "offset": 0,
            "values": self.getWordArray(0b001 + (0b010 if self.remote_items else 0b000))
        }]
        ownPlayerId: List[ByteEdit] = [{
            "sym": symbols["config_player_id"],
            "offset": 0,
            "values": self.getWordArray(self.player)
        }]

        patchDict = {   'MultiWorldLocations': multiWorldLocations,
                        'MultiWorldItems': multiWorldItems,
                        'offworldSprites': offworldSprites,
                        'deathLink': deathLink,
                        'remoteItem': remoteItem,
                        'ownPlayerId': ownPlayerId,
                        'playerNameData':  playerNameData,
                        'playerIdData':  playerIdData}

        # convert an array of symbolic byte_edit dicts like {"sym": symobj, "offset": 0, "values": [1, 0]}
        # to a single rom patch dict like {0x438c: [1, 0], 0xa4a5: [0, 0, 0]} which varia will understand and apply
        def resolve_symbols_to_file_offset_based_dict(byte_edits_arr: List[ByteEdit]) -> Dict[int, Iterable[int]]:
            this_patch_as_dict: Dict[int, Iterable[int]] = {}
            for byte_edit in byte_edits_arr:
                offset_within_rom_file: int = byte_edit["sym"]["offset_within_rom_file"] + byte_edit["offset"]
                this_patch_as_dict[offset_within_rom_file] = byte_edit["values"]
            return this_patch_as_dict

        for patchname, byte_edits_arr in patchDict.items():
            patchDict[patchname] = resolve_symbols_to_file_offset_based_dict(byte_edits_arr)

        romPatcher.applyIPSPatchDict(patchDict)

        openTourianGreyDoors = {0x07C823 + 5: [0x0C], 0x07C831 + 5: [0x0C]}
        romPatcher.applyIPSPatchDict({'openTourianGreyDoors': openTourianGreyDoors})


        # set rom name
        # 21 bytes
        from Main import __version__
        self.romName = bytearray(f'SM{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}', 'utf8')[:21]
        self.romName.extend([0] * (21 - len(self.romName)))
        # clients should read from 0x7FC0, the location of the rom title in the SNES header.
        # duplicative ROM name at 0x1C4F00 is still written here for now, since people with archipelago pre-0.3.0 client installed will still be depending on this location for connecting to SM
        romPatcher.applyIPSPatch('ROMName', { 'ROMName':  {0x1C4F00 : self.romName, 0x007FC0 : self.romName} })


        startItemROMAddressBase = symbols["start_item_data_major"]["offset_within_rom_file"]

        # array for each item:
        #  offset within ROM table "start_item_data_major" of this item"s info (starting status)
        #  item bitmask or amount per pickup (BVOB = base value or bitmask),
        #  offset within ROM table "start_item_data_major" of this item"s info (starting maximum/starting collected items)
        #                                 current  BVOB   max
        #                                 -------  ----   ---
        startItemROMDict = {"ETank":        [ 0x8, 0x64,  0xA],
                            "Missile":      [ 0xC,  0x5,  0xE],
                            "Super":        [0x10,  0x5, 0x12],
                            "PowerBomb":    [0x14,  0x5, 0x16],
                            "Reserve":      [0x1A, 0x64, 0x18],
                            "Morph":        [ 0x2,  0x4,  0x0],
                            "Bomb":         [ 0x3, 0x10,  0x1],
                            "SpringBall":   [ 0x2,  0x2,  0x0],
                            "HiJump":       [ 0x3,  0x1,  0x1],
                            "Varia":        [ 0x2,  0x1,  0x0],
                            "Gravity":      [ 0x2, 0x20,  0x0],
                            "SpeedBooster": [ 0x3, 0x20,  0x1],
                            "SpaceJump":    [ 0x3,  0x2,  0x1],
                            "ScrewAttack":  [ 0x2,  0x8,  0x0],
                            "Charge":       [ 0x7, 0x10,  0x5],
                            "Ice":          [ 0x6,  0x2,  0x4],
                            "Wave":         [ 0x6,  0x1,  0x4],
                            "Spazer":       [ 0x6,  0x4,  0x4],
                            "Plasma":       [ 0x6,  0x8,  0x4],
                            "Grapple":      [ 0x3, 0x40,  0x1],
                            "XRayScope":    [ 0x3, 0x80,  0x1]

        # BVOB = base value or bitmask
                            }
        mergedData = {}
        hasETank = False
        hasSpazer = False
        hasPlasma = False
        for startItem in self.startItems:
            item = startItem.Type
            if item == "ETank": hasETank = True
            if item == "Spazer": hasSpazer = True
            if item == "Plasma": hasPlasma = True
            if (item in ["ETank", "Missile", "Super", "PowerBomb", "Reserve"]):
                (currentValue, amountPerItem, maxValue) = startItemROMDict[item]
                if (startItemROMAddressBase + currentValue) in mergedData:
                    mergedData[startItemROMAddressBase + currentValue] += amountPerItem
                    mergedData[startItemROMAddressBase + maxValue] += amountPerItem
                else:
                    mergedData[startItemROMAddressBase + currentValue] = amountPerItem
                    mergedData[startItemROMAddressBase + maxValue] = amountPerItem
            else:
                (collected, bitmask, equipped) = startItemROMDict[item]
                if (startItemROMAddressBase + collected) in mergedData:
                    mergedData[startItemROMAddressBase + collected] |= bitmask
                    mergedData[startItemROMAddressBase + equipped] |= bitmask
                else:
                    mergedData[startItemROMAddressBase + collected] = bitmask
                    mergedData[startItemROMAddressBase + equipped] = bitmask

        if hasETank:
            # we are overwriting the starting energy, so add up the E from 99 (normal starting energy) rather than from 0
            mergedData[startItemROMAddressBase + 0x8] += 99
            mergedData[startItemROMAddressBase + 0xA] += 99

        if hasSpazer and hasPlasma:
            # de-equip spazer.
            # otherwise, firing the unintended spazer+plasma combo would cause massive game glitches and crashes
            mergedData[startItemROMAddressBase + 0x4] &= ~0x4

        for key, value in mergedData.items():
            if (key - startItemROMAddressBase > 7):
                [w0, w1] = self.getWordArray(value)
                mergedData[key] = [w0, w1]
            else:
                mergedData[key] = [value]


        startItemPatch = { "startItemPatch":  mergedData }
        romPatcher.applyIPSPatch("startItemPatch", startItemPatch)

        # commit all the changes we've made here to the ROM
        romPatcher.commitIPS()

        itemLocs = [
            ItemLocation(ItemManager.Items[itemLoc.item.type
                         if isinstance(itemLoc.item, SMItem) and itemLoc.item.type in ItemManager.Items else
                         'ArchipelagoItem'],
                         locationsDict[itemLoc.name], True)
            for itemLoc in self.multiworld.get_locations() if itemLoc.player == self.player
        ]
        romPatcher.writeItemsLocs(itemLocs)

        itemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type], locationsDict[itemLoc.name] if itemLoc.name in locationsDict and itemLoc.player == self.player else self.DummyLocation(self.multiworld.get_player_name(itemLoc.player) + " " + itemLoc.name), True) for itemLoc in self.multiworld.get_locations() if itemLoc.item.player == self.player]
        progItemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type], locationsDict[itemLoc.name] if itemLoc.name in locationsDict and itemLoc.player == self.player else self.DummyLocation(self.multiworld.get_player_name(itemLoc.player) + " " + itemLoc.name), True) for itemLoc in self.multiworld.get_locations() if itemLoc.item.player == self.player and itemLoc.item.advancement == True]
        # progItemLocs = [ItemLocation(ItemManager.Items[itemLoc.item.type if itemLoc.item.type in ItemManager.Items else 'ArchipelagoItem'], locationsDict[itemLoc.name], True) for itemLoc in self.multiworld.get_locations() if itemLoc.player == self.player and itemLoc.item.player == self.player and itemLoc.item.advancement == True]
        
        # romPatcher.writeSplitLocs(self.variaRando.args.majorsSplit, itemLocs, progItemLocs)
        romPatcher.writeSpoiler(itemLocs, progItemLocs)
        romPatcher.writeRandoSettings(self.variaRando.randoExec.randoSettings, itemLocs)

    def generate_output(self, output_directory: str):
        outfilebase = self.multiworld.get_out_file_name_base(self.player)
        outputFilename = os.path.join(output_directory, f"{outfilebase}.sfc")

        try:
            self.variaRando.PatchRom(outputFilename, self.APPrePatchRom, self.APPostPatchRom)
            self.write_crc(outputFilename)
            self.rom_name = self.romName
        except:
            raise
        else:
            patch = SMDeltaPatch(os.path.splitext(outputFilename)[0] + SMDeltaPatch.patch_file_ending, player=self.player,
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
            for option_name in self.option_definitions:
                option = getattr(self.multiworld, option_name)[self.player]
                slot_data[option_name] = option.value

            slot_data["Preset"] = { "Knows": {},
                                    "Settings": {"hardRooms": Settings.SettingsDict[self.player].hardRooms,
                                                 "bossesDifficulty": Settings.SettingsDict[self.player].bossesDifficulty,
                                                 "hellRuns": Settings.SettingsDict[self.player].hellRuns},
                                    "Controller": Controller.ControllerDict[self.player].__dict__}

            for knows in Knows.__dict__:
                if isKnows(knows):
                    slot_data["Preset"]["Knows"][knows] = [ getattr(Knows.knowsDict[self.player], knows).bool, 
                                                            getattr(Knows.knowsDict[self.player], knows).difficulty]

            slot_data["InterAreaTransitions"] = {}
            for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions:
                slot_data["InterAreaTransitions"][src.Name] = dest.Name
                
            slot_data["Doors"] = {}
            for door in DoorsManager.doorsDict[self.player].values():
                slot_data["Doors"][door.name] = door.getColor()

            slot_data["RomPatches"] = RomPatches.ActivePatches[self.player]
                
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.smbm[self.player].addItem(item.type)
        if (item.location != None and item.location.player == self.player):
            for entrance in self.multiworld.get_region(item.location.parent_region.name, self.player).entrances:
                if (entrance.parent_region.can_reach(state)):
                    state.smbm[self.player].lastAP = entrance.parent_region.name
                    break
        return super(SMWorld, self).collect(state, item)

    def remove(self, state: CollectionState, item: Item) -> bool:
        state.smbm[self.player].removeItem(item.type)
        return super(SMWorld, self).remove(state, item)

    def create_item(self, name: str) -> Item:
        item = next(x for x in ItemManager.Items.values() if x.Name == name)
        return SMItem(item.Name, ItemClassification.progression if item.Class != 'Minor' else ItemClassification.filler, item.Type, self.item_name_to_id[item.Name],
                      player=self.player)

    def get_filler_item_name(self) -> str:
        if self.multiworld.random.randint(0, 100) < self.multiworld.minor_qty[self.player].value:
            power_bombs = self.multiworld.power_bomb_qty[self.player].value
            missiles = self.multiworld.missile_qty[self.player].value
            super_missiles = self.multiworld.super_qty[self.player].value
            roll = self.multiworld.random.randint(1, power_bombs + missiles + super_missiles)
            if roll <= power_bombs:
                return "Power Bomb"
            elif roll <= power_bombs + missiles:
                return "Missile"
            else:
                return "Super Missile"
        else:
            return "Nothing"

    def pre_fill(self):
        if len(self.NothingPool) > 0:
            nonChozoLoc = []
            chozoLoc = []

            for loc in self.locations.values():
                if loc.item is None:
                    if locationsDict[loc.name].isChozo():
                        chozoLoc.append(loc)
                    else:
                        nonChozoLoc.append(loc)

            self.multiworld.random.shuffle(nonChozoLoc)
            self.multiworld.random.shuffle(chozoLoc)
            missingCount = len(self.NothingPool) - len(nonChozoLoc)
            locations = nonChozoLoc
            if (missingCount > 0):
                locations += chozoLoc[:missingCount]
            locations = locations[:len(self.NothingPool)]
            for item, loc in zip(self.NothingPool, locations):
                loc.place_locked_item(item)
                loc.address = loc.item.code = None

    @classmethod
    def stage_post_fill(cls, world):
        new_state = CollectionState(world)
        progitempool = []
        for item in world.itempool:
            if item.game == "Super Metroid" and item.advancement:
                progitempool.append(item)

        for item in progitempool:
            new_state.collect(item, True)
        
        bossesLoc = ['Draygon', 'Kraid', 'Ridley', 'Phantoon', 'Mother Brain']
        for player in world.get_game_players("Super Metroid"):
            for bossLoc in bossesLoc:
                if not world.get_location(bossLoc, player).can_reach(new_state):
                    world.state.smbm[player].onlyBossLeft = True
                    break

    def write_spoiler(self, spoiler_handle: TextIO):
        if self.multiworld.area_randomization[self.player].value != 0:
            spoiler_handle.write('\n\nArea Transitions:\n\n')
            spoiler_handle.write('\n'.join(['%s%s %s %s' % (f'{self.multiworld.get_player_name(self.player)}: '
                                                            if self.multiworld.players > 1 else '', src.Name,
                                                            '<=>',
                                                            dest.Name) for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions if not src.Boss]))

        if self.multiworld.boss_randomization[self.player].value != 0:
            spoiler_handle.write('\n\nBoss Transitions:\n\n')
            spoiler_handle.write('\n'.join(['%s%s %s %s' % (f'{self.multiworld.get_player_name(self.player)}: '
                                                            if self.multiworld.players > 1 else '', src.Name,
                                                            '<=>',
                                                            dest.Name) for src, dest in self.variaRando.randoExec.areaGraph.InterAreaTransitions if src.Boss]))

def create_locations(self, player: int):
    for name in locationsDict:
        self.locations[name] = SMLocation(player, name, self.location_name_to_id.get(name, None))


def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
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

    def can_reach(self, state: CollectionState) -> bool:
        # self.access_rule computes faster on average, so placing it first for faster abort
        assert self.parent_region, "Can't reach location without region"
        return self.access_rule(state) and self.parent_region.can_reach(state) and self.can_comeback(state)
    
    def can_comeback(self, state: CollectionState):
        # some specific early/late game checks
        if self.name == 'Bomb' or self.name == 'Mother Brain':
            return True

        randoExec = state.multiworld.worlds[self.player].variaRando.randoExec
        n = 2 if GraphUtils.isStandardStart(randoExec.graphSettings.startAP) else 3
        # is early game
        if (len([loc for loc in state.locations_checked if loc.player == self.player]) <= n):
            return True

        for key in locationsDict[self.name].AccessFrom.keys():
            smbm = state.smbm[self.player]
            if (randoExec.areaGraph.canAccess(  smbm, 
                                                smbm.lastAP,
                                                key,
                                                smbm.maxDiff,
                                                None)):
                return True
        return False
 

class SMItem(Item):
    game = "Super Metroid"
    type: str

    def __init__(self, name, classification, type: str, code, player: int):
        super(SMItem, self).__init__(name, classification, code, player)
        self.type = type
