import logging
import copy
import os
import random
import threading
from typing import Dict, Set, TextIO

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, RegionType, CollectionState, \
    Tutorial
from worlds.generic.Rules import set_rule
from worlds.smz3.TotalSMZ3.Item import ItemType
import worlds.smz3.TotalSMZ3.Item as TotalSMZ3Item
from worlds.smz3.TotalSMZ3.World import World as TotalSMZ3World
from worlds.smz3.TotalSMZ3.Regions.Zelda.GanonsTower import GanonsTower
from worlds.smz3.TotalSMZ3.Config import Config, GameMode, Goal, KeyShuffle, MorphLocation, SMLogic, SwordLocation, Z3Logic, OpenTower, GanonVulnerable, OpenTourian
from worlds.smz3.TotalSMZ3.Location import LocationType, locations_start_id, Location as TotalSMZ3Location
from worlds.smz3.TotalSMZ3.Patch import Patch as TotalSMZ3Patch, getWord, getWordArray
from worlds.smz3.TotalSMZ3.WorldState import WorldState
from ..AutoWorld import World, AutoLogicRegister, WebWorld
from .Rom import get_base_rom_bytes, SMZ3DeltaPatch
from .ips import IPS_Patch
from .Options import smz3_options
from Options import Accessibility

world_folder = os.path.dirname(__file__)
logger = logging.getLogger("SMZ3")


class SMZ3CollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        # for unit tests where MultiWorld is instantiated before worlds
        if hasattr(parent, "state"):
            self.smz3state = {player: TotalSMZ3Item.Progression([]) for player in parent.get_game_players("SMZ3")}
            for player, group in parent.groups.items():
                if (group["game"] == "SMZ3"):
                    self.smz3state[player] = TotalSMZ3Item.Progression([])
                    if player not in parent.state.smz3state:
                        parent.state.smz3state[player] = TotalSMZ3Item.Progression([])
        else:
            self.smz3state = {}

    def copy_mixin(self, ret) -> CollectionState:
        ret.smz3state = {player: copy.deepcopy(self.smz3state[player]) for player in self.smz3state}
        return ret

class SMZ3Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Super Metroid and A Link to the Past Crossover randomizer on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["lordlou"]
    )]


class SMZ3World(World):
    """
     A python port of Super Metroid & A Link To The Past Crossover Item Randomizer based on v11.2 of Total's SMZ3. 
     This is allowed as long as we keep features and logic as close as possible as the original.    
    """
    game: str = "SMZ3"
    topology_present = False
    data_version = 2
    option_definitions = smz3_options
    item_names: Set[str] = frozenset(TotalSMZ3Item.lookup_name_to_id)
    location_names: Set[str]
    item_name_to_id = TotalSMZ3Item.lookup_name_to_id
    location_name_to_id: Dict[str, int] = {key : locations_start_id + value.Id for key, value in TotalSMZ3World(Config(), "", 0, "").locationLookup.items()}
    web = SMZ3Web()

    remote_items: bool = False
    remote_start_inventory: bool = False

    locationNamesGT: Set[str] = {loc.Name for loc in GanonsTower(None, None).Locations}

    # first added for 0.2.6
    required_client_version = (0, 2, 6)

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.locations: Dict[str, Location] = {}
        self.unreachable = []
        super().__init__(world, player)

    @classmethod
    def isProgression(cls, itemType):
        progressionTypes = {
                                ItemType.ProgressiveShield,
                                ItemType.ProgressiveSword,
                                ItemType.Bow,
                                ItemType.Hookshot,
                                ItemType.Mushroom,
                                ItemType.Powder,
                                ItemType.Firerod,
                                ItemType.Icerod,
                                ItemType.Bombos,
                                ItemType.Ether,
                                ItemType.Quake,
                                ItemType.Lamp,
                                ItemType.Hammer,
                                ItemType.Shovel,
                                ItemType.Flute,
                                ItemType.Bugnet,
                                ItemType.Book,
                                ItemType.Bottle,
                                ItemType.Somaria,
                                ItemType.Byrna,
                                ItemType.Cape,
                                ItemType.Mirror,
                                ItemType.Boots,
                                ItemType.ProgressiveGlove,
                                ItemType.Flippers,
                                ItemType.MoonPearl,
                                ItemType.HalfMagic,

                                ItemType.Grapple,
                                ItemType.Charge,
                                ItemType.Ice,
                                ItemType.Wave,
                                ItemType.Plasma,
                                ItemType.Varia,
                                ItemType.Gravity,
                                ItemType.Morph,
                                ItemType.Bombs,
                                ItemType.SpringBall,
                                ItemType.ScrewAttack,
                                ItemType.HiJump,
                                ItemType.SpaceJump,
                                ItemType.SpeedBooster,

                                ItemType.ETank,
                                ItemType.ReserveTank,

                                ItemType.BigKeyGT,
                                ItemType.KeyGT,
                                ItemType.BigKeyEP,
                                ItemType.BigKeyDP,
                                ItemType.BigKeyTH,
                                ItemType.BigKeyPD,
                                ItemType.BigKeySP,
                                ItemType.BigKeySW,
                                ItemType.BigKeyTT,
                                ItemType.BigKeyIP,
                                ItemType.BigKeyMM,
                                ItemType.BigKeyTR,

                                ItemType.KeyHC,
                                ItemType.KeyCT,
                                ItemType.KeyDP,
                                ItemType.KeyTH,
                                ItemType.KeyPD,
                                ItemType.KeySP,
                                ItemType.KeySW,
                                ItemType.KeyTT,
                                ItemType.KeyIP,
                                ItemType.KeyMM,
                                ItemType.KeyTR,

                                ItemType.CardCrateriaL1,
                                ItemType.CardCrateriaL2,
                                ItemType.CardCrateriaBoss,
                                ItemType.CardBrinstarL1,
                                ItemType.CardBrinstarL2,
                                ItemType.CardBrinstarBoss,
                                ItemType.CardNorfairL1,
                                ItemType.CardNorfairL2,
                                ItemType.CardNorfairBoss,
                                ItemType.CardMaridiaL1,
                                ItemType.CardMaridiaL2,
                                ItemType.CardMaridiaBoss,
                                ItemType.CardWreckedShipL1,
                                ItemType.CardWreckedShipBoss,
                                ItemType.CardLowerNorfairL1,
                                ItemType.CardLowerNorfairBoss,
                            }
        return itemType in progressionTypes

    @classmethod
    def stage_assert_generate(cls, world):
        base_combined_rom = get_base_rom_bytes()

    def generate_early(self):
        self.config = Config()
        self.config.GameMode = GameMode.Multiworld
        self.config.Z3Logic = Z3Logic.Normal
        self.config.SMLogic = SMLogic(self.world.sm_logic[self.player].value)
        self.config.SwordLocation = SwordLocation(self.world.sword_location[self.player].value)
        self.config.MorphLocation = MorphLocation(self.world.morph_location[self.player].value)
        self.config.Goal = Goal(self.world.goal[self.player].value)
        self.config.KeyShuffle = KeyShuffle(self.world.key_shuffle[self.player].value)
        self.config.OpenTower = OpenTower(self.world.open_tower[self.player].value)
        self.config.GanonVulnerable = GanonVulnerable(self.world.ganon_vulnerable[self.player].value)
        self.config.OpenTourian = OpenTourian(self.world.open_tourian[self.player].value)

        self.local_random = random.Random(self.world.random.randint(0, 1000))
        self.smz3World = TotalSMZ3World(self.config, self.world.get_player_name(self.player), self.player, self.world.seed_name)
        self.smz3DungeonItems = []
        SMZ3World.location_names = frozenset(self.smz3World.locationLookup.keys())

        self.world.state.smz3state[self.player] = TotalSMZ3Item.Progression([])
    
    def generate_basic(self):
        self.smz3World.Setup(WorldState.Generate(self.config, self.world.random))
        self.dungeon = TotalSMZ3Item.Item.CreateDungeonPool(self.smz3World)
        self.dungeon.reverse()
        self.progression = TotalSMZ3Item.Item.CreateProgressionPool(self.smz3World)
        self.keyCardsItems = TotalSMZ3Item.Item.CreateKeycards(self.smz3World)
        self.SmMapsItems = TotalSMZ3Item.Item.CreateSmMaps(self.smz3World)

        niceItems = TotalSMZ3Item.Item.CreateNicePool(self.smz3World)
        junkItems = TotalSMZ3Item.Item.CreateJunkPool(self.smz3World)
        allJunkItems = niceItems + junkItems
        self.junkItemsNames = [item.Type.name for item in junkItems]

        if (self.smz3World.Config.Keysanity):
            progressionItems = self.progression + self.dungeon + self.keyCardsItems + self.SmMapsItems
        else:
            progressionItems = self.progression 
            for item in self.keyCardsItems:
                self.world.push_precollected(SMZ3Item(item.Type.name, ItemClassification.filler, item.Type, self.item_name_to_id[item.Type.name], self.player, item))

        itemPool = [SMZ3Item(item.Type.name, ItemClassification.progression, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in progressionItems] + \
                    [SMZ3Item(item.Type.name, ItemClassification.filler, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in allJunkItems]
        self.smz3DungeonItems = [SMZ3Item(item.Type.name, ItemClassification.progression, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in self.dungeon]
        self.world.itempool += itemPool

    def set_rules(self):
        # SM G4 is logically required to access Ganon's Tower in SMZ3
        self.world.completion_condition[self.player] = lambda state: \
            self.smz3World.GetRegion("Ganon's Tower").CanEnter(state.smz3state[self.player]) and \
            self.smz3World.GetRegion("Ganon's Tower").TowerAscend(state.smz3state[self.player])

        for region in self.smz3World.Regions:
            entrance = self.world.get_entrance('Menu' + "->" + region.Name, self.player)
            set_rule(entrance, lambda state, region=region: region.CanEnter(state.smz3state[self.player]))
            for loc in region.Locations:
                l = self.locations[loc.Name]
                if self.world.accessibility[self.player] != 'locations':
                    l.always_allow = lambda state, item, loc=loc: \
                        item.game == "SMZ3" and \
                        loc.alwaysAllow(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World), state.smz3state[self.player])
                old_rule = l.item_rule
                l.item_rule = lambda item, loc=loc, region=region: (\
                    item.game != "SMZ3" or \
                    loc.allow(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World), None) and \
                        region.CanFill(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World))) and old_rule(item)
                set_rule(l, lambda state, loc=loc: loc.Available(state.smz3state[self.player]))

    def create_regions(self):
        self.create_locations(self.player)
        startRegion = self.create_region(self.world, self.player, 'Menu')
        self.world.regions.append(startRegion)

        for region in self.smz3World.Regions:
            currentRegion = self.create_region(self.world, self.player, region.Name, region.locationLookup.keys(), [region.Name + "->" + 'Menu'])
            self.world.regions.append(currentRegion)
            entrance = self.world.get_entrance(region.Name + "->" + 'Menu', self.player)
            entrance.connect(startRegion)
            exit = Entrance(self.player, 'Menu' + "->" + region.Name, startRegion)
            startRegion.exits.append(exit)
            exit.connect(currentRegion)

    def apply_sm_custom_sprite(self):
        itemSprites = ["off_world_prog_item.bin", "off_world_item.bin"]
        itemSpritesAddress = [0xF800, 0xF900]
        idx = 0
        offworldSprites = {}
        for fileName in itemSprites:
            with open(world_folder + "/data/custom_sprite/" + fileName, 'rb') as stream:
                buffer = bytearray(stream.read())
                offworldSprites[0x04Eff2 + 10*((0x6B + 0x40) + idx)] = bytearray(getWordArray(itemSpritesAddress[idx])) + buffer[0:8]
                offworldSprites[0x090000 + itemSpritesAddress[idx]] = buffer[8:264]
                idx += 1
        return offworldSprites

    def convert_to_sm_item_name(self, itemName):
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
            (w0, w1) = getWord(charMap.get(char, 0x3C4E))
            data.append(w0)
            data.append(w1)
        return data

    def convert_to_lttp_item_name(self, itemName):
        return bytearray(itemName[:19].center(19, " "), 'utf8') + bytearray(0)

    def apply_item_names(self):
        patch = {}
        sm_remote_idx = 0
        lttp_remote_idx = 0
        for location in self.smz3World.Locations:
            if self.world.worlds[location.APLocation.item.player].game != self.game:
                if location.Type == LocationType.Visible or location.Type == LocationType.Chozo or location.Type == LocationType.Hidden:
                    patch[0x390000 + sm_remote_idx*64] = self.convert_to_sm_item_name(location.APLocation.item.name)
                    sm_remote_idx += 1
                    progressionItem = (0 if location.APLocation.item.advancement else 0x8000) + sm_remote_idx
                    patch[0x386000 + (location.Id * 8) + 6] = bytearray(getWordArray(progressionItem))
                else:
                    patch[0x390000 + 100 * 64 + lttp_remote_idx * 20] = self.convert_to_lttp_item_name(location.APLocation.item.name)
                    lttp_remote_idx += 1
                    progressionItem = (0 if location.APLocation.item.advancement else 0x8000) + lttp_remote_idx
                    patch[0x386000 + (location.Id * 8) + 6] = bytearray(getWordArray(progressionItem))
                
        return patch

    def SnesCustomization(self, addr: int):
        addr = (0x400000 if addr < 0x800000 else 0)| (addr & 0x3FFFFF)
        return addr

    def apply_customization(self):
        patch = {}

        # smSpinjumps
        if (self.world.spin_jumps_animation[self.player].value == 1):
            patch[self.SnesCustomization(0x9B93FE)] = bytearray([0x01])

        # z3HeartBeep
        values =    [ 0x00, 0x80, 0x40, 0x20, 0x10]
        index = self.world.heart_beep_speed[self.player].value
        patch[0x400033] = bytearray([values[index if index < len(values) else 2]])

        # z3HeartColor
        values =    [
                        [0x24, [0x18, 0x00]],
                        [0x3C, [0x04, 0x17]],
                        [0x2C, [0xC9, 0x69]],
                        [0x28, [0xBC, 0x02]]
                    ]
        index = self.world.heart_color[self.player].value
        (hud, fileSelect) = values[index if index < len(values) else 0]
        for i in range(0, 20, 2):
            patch[self.SnesCustomization(0xDFA1E + i)] = bytearray([hud])
        patch[self.SnesCustomization(0x1BD6AA)] = bytearray(fileSelect)

        # z3QuickSwap
        patch[0x40004B] = bytearray([0x01 if self.world.quick_swap[self.player].value else 0x00])

        # smEnergyBeepOff
        if (self.world.energy_beep[self.player].value == 0):
            for ([addr, value]) in [
                            [0x90EA9B, 0x80],
                            [0x90F337, 0x80],
                            [0x91E6D5, 0x80]
                        ]:
                patch[self.SnesCustomization(addr)] = bytearray([value])

        return patch

    def generate_output(self, output_directory: str):
        try:
            base_combined_rom = get_base_rom_bytes()
            basepatch = IPS_Patch.load(world_folder + "/data/zsm.ips")
            base_combined_rom = basepatch.apply(base_combined_rom)

            patcher = TotalSMZ3Patch(self.smz3World,
                                    [world.smz3World for key, world in self.world.worlds.items() if isinstance(world, SMZ3World) and hasattr(world, "smz3World")],
                                    self.world.seed_name,
                                    self.world.seed,
                                    self.local_random,
                                    {v: k for k, v in self.world.player_name.items()},
                                    next(iter(loc.player for loc in self.world.get_locations() if (loc.item.name == "SilverArrows" and loc.item.player == self.player))))
            patches = patcher.Create(self.smz3World.Config)
            patches.update(self.apply_sm_custom_sprite())
            patches.update(self.apply_item_names())
            patches.update(self.apply_customization())
            for addr, bytes in patches.items():
                offset = 0
                for byte in bytes:
                    base_combined_rom[addr + offset] = byte
                    offset += 1

            outfilebase = 'AP_' + self.world.seed_name
            outfilepname = f'_P{self.player}'
            outfilepname += f"_{self.world.get_file_safe_player_name(self.player).replace(' ', '_')}" \

            filename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.sfc')
            with open(filename, "wb") as binary_file:
                binary_file.write(base_combined_rom)
            patch = SMZ3DeltaPatch(os.path.splitext(filename)[0]+SMZ3DeltaPatch.patch_file_ending, player=self.player,
                                   player_name=self.world.player_name[self.player], patched_path=filename)
            patch.write()
            os.remove(filename)
            self.rom_name = bytearray(patcher.title, 'utf8')
        except:
            raise
        finally:
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        if (not self.smz3World.Config.Keysanity):
            for item_name in self.keyCardsItems:
                item_id = self.item_name_to_id.get(item_name.Type.name, None)
                try:
                    multidata["precollected_items"][self.player].remove(item_id)
                except ValueError as e:
                    logger.warning(f"Attempted to remove nonexistent item id {item_id} from smz3 precollected items ({item_name})")

        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            payload = multidata["connect_names"][self.world.player_name[self.player]]
            multidata["connect_names"][new_name] = payload

    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.smz3state[self.player].Add([TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World if hasattr(self, "smz3World") else None)])
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True  # indicate that a logical state change has occured
        return False

    def remove(self, state: CollectionState, item: Item) -> bool:
        name = self.collect_item(state, item, True)
        if name:
            state.smz3state[item.player].Remove([TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World if hasattr(self, "smz3World") else None)])
            state.prog_items[name, item.player] -= 1
            if state.prog_items[name, item.player] < 1:
                del (state.prog_items[name, item.player])
            return True
        return False

    def create_item(self, name: str) -> Item:
        return SMZ3Item(name, 
                        ItemClassification.progression if SMZ3World.isProgression(TotalSMZ3Item.ItemType[name]) else ItemClassification.filler,
                        TotalSMZ3Item.ItemType[name], self.item_name_to_id[name], 
                        self.player,
                        TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[name], self))

    def pre_fill(self):
        from Fill import fill_restrictive
        self.InitialFillInOwnWorld()

        if (not self.smz3World.Config.Keysanity):
            locations = [loc for loc in self.locations.values() if loc.item is None]
            self.world.random.shuffle(locations)

            all_state = self.world.get_all_state(False)
            for item in self.smz3DungeonItems:
                all_state.remove(item)

            all_dungeonItems = self.smz3DungeonItems[:]
            fill_restrictive(self.world, all_state, locations, all_dungeonItems, True, True)
            # some small or big keys (those always_allow) can be unreachable in-game
            # while logic still collects some of them (probably to simulate the player collecting pot keys in the logic), some others don't
            # so we need to remove those exceptions as progression items
            if self.world.accessibility[self.player] != 'locations':
                exception_item = [TotalSMZ3Item.ItemType.BigKeySW, TotalSMZ3Item.ItemType.BigKeySP, TotalSMZ3Item.ItemType.KeyTH]
                for item in self.smz3DungeonItems:
                    if item.item.Type in exception_item and item.location.always_allow(all_state, item) and not all_state.can_reach(item.location):
                        item.classification = ItemClassification.filler
                        item.item.Progression = False
                        item.location.event = False
                        self.unreachable.append(item.location)
        self.JunkFillGT(0.5)

    def get_pre_fill_items(self):
        if (not self.smz3World.Config.Keysanity):
            return self.smz3DungeonItems
        else:
            return []

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(self.junkItemsNames)

    def write_spoiler(self, spoiler_handle: TextIO):
            self.world.spoiler.unreachables.update(self.unreachable)

    def JunkFillGT(self, factor):
        poolLength = len(self.world.itempool)
        junkPoolIdx = [i for i in range(0, poolLength) 
                    if self.world.itempool[i].classification in (ItemClassification.filler, ItemClassification.trap) and
                    self.world.itempool[i].player == self.player]
        toRemove = []
        for loc in self.locations.values():
            # commenting this for now since doing a partial GT pre fill would allow for non SMZ3 progression in GT
            # which isnt desirable (SMZ3 logic only filters for SMZ3 items). Having progression in GT can only happen in Single Player.
            # if len(toRemove) >= int(len(self.locationNamesGT) * factor * self.smz3World.TowerCrystals / 7):
            #     break
            if loc.name in self.locationNamesGT and loc.item is None:
                poolLength = len(junkPoolIdx)
                # start looking at a random starting index and loop at start if no match found
                start = self.world.random.randint(0, poolLength)
                for off in range(0, poolLength):
                    i = (start + off) % poolLength
                    candidate = self.world.itempool[junkPoolIdx[i]]
                    if junkPoolIdx[i] not in toRemove and loc.can_fill(self.world.state, candidate, False):
                        itemFromPool = candidate
                        toRemove.append(junkPoolIdx[i])
                        break
                self.world.push_item(loc, itemFromPool, False)
                loc.event = False
        toRemove.sort(reverse = True)
        for i in toRemove: 
            self.world.itempool.pop(i)
            
    def FillItemAtLocation(self, itemPool, itemType, location):
        itemToPlace = TotalSMZ3Item.Item.Get(itemPool, itemType, self.smz3World)
        if (itemToPlace == None):
            raise Exception(f"Tried to place item {itemType} at {location.Name}, but there is no such item in the item pool")
        else:
            location.Item = itemToPlace
            itemFromPool = next((i for i in self.world.itempool if i.player == self.player and i.name == itemToPlace.Type.name), None)
            if itemFromPool is not None:
                self.world.get_location(location.Name, self.player).place_locked_item(itemFromPool)
                self.world.itempool.remove(itemFromPool)
            else:
                itemFromPool = next((i for i in self.smz3DungeonItems if i.player == self.player and i.name == itemToPlace.Type.name), None)
                if itemFromPool is not None:
                    self.world.get_location(location.Name, self.player).place_locked_item(itemFromPool)
                    self.smz3DungeonItems.remove(itemFromPool)
        itemPool.remove(itemToPlace)

    def FrontFillItemInOwnWorld(self, itemPool, itemType):
        item = TotalSMZ3Item.Item.Get(itemPool, itemType, self.smz3World)
        location = next(iter(self.world.random.sample(TotalSMZ3Location.AvailableGlobal(TotalSMZ3Location.Empty(self.smz3World.Locations), self.smz3World.Items()), 1)), None)
        if (location == None):
            raise Exception(f"Tried to front fill {item.Name} in, but no location was available")
        
        location.Item = item
        itemFromPool = next((i for i in self.world.itempool if i.player == self.player and i.name == item.Type.name and i.advancement == item.Progression), None)
        if itemFromPool is not None:
            self.world.get_location(location.Name, self.player).place_locked_item(itemFromPool)
            self.world.itempool.remove(itemFromPool)
        itemPool.remove(item)

    def InitialFillInOwnWorld(self):
        self.FillItemAtLocation(self.dungeon, TotalSMZ3Item.ItemType.KeySW, self.smz3World.GetLocation("Skull Woods - Pinball Room"))
        if (not self.smz3World.Config.Keysanity):
            self.FillItemAtLocation(self.dungeon, TotalSMZ3Item.ItemType.KeySP, self.smz3World.GetLocation("Swamp Palace - Entrance"))

        # /* Check Swords option and place as needed */
        if self.smz3World.Config.SwordLocation == SwordLocation.Uncle:
            self.FillItemAtLocation(self.progression, TotalSMZ3Item.ItemType.ProgressiveSword, self.smz3World.GetLocation("Link's Uncle"))

        # /* Check Morph option and place as needed */
        if self.smz3World.Config.MorphLocation == MorphLocation.Original:
            self.FillItemAtLocation(self.progression, TotalSMZ3Item.ItemType.Morph, self.smz3World.GetLocation("Morphing Ball"))
        elif self.smz3World.Config.MorphLocation == MorphLocation.Early:
            self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.Morph)

        # We do early Sword placement after Morph in case its Original location
        if self.smz3World.Config.SwordLocation == SwordLocation.Early:
            self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.ProgressiveSword)

        # /* We place a PB and Super in Sphere 1 to make sure the filler
        #    * doesn't start locking items behind this when there are a
        #    * high chance of the trash fill actually making them available */
        self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.Super)
        self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.PowerBomb)

    def create_locations(self, player: int):
        for name, id in SMZ3World.location_name_to_id.items():
            newLoc = SMZ3Location(player, name, id)
            self.locations[name] = newLoc
            self.smz3World.locationLookup[name].APLocation = newLoc

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


class SMZ3Location(Location):
    game: str = "SMZ3"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SMZ3Location, self).__init__(player, name, address, parent)


class SMZ3Item(Item):
    game = "SMZ3"
    type: ItemType
    item: Item

    def __init__(self, name, classification, type: ItemType, code, player: int, item: Item):
        super(SMZ3Item, self).__init__(name, classification, code, player)
        self.type = type
        self.item = item
