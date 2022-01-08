import logging
import copy
import os
import threading
import sys
import pathlib
import Patch
from typing import Dict, List, Set

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, CollectionState
from worlds.generic.Rules import add_rule, set_rule
import worlds.smz3.TotalSMZ3.Item as TotalSMZ3Item
from worlds.smz3.TotalSMZ3.World import World as TotalSMZ3World
from worlds.smz3.TotalSMZ3.Config import Config, MorphLocation, SwordLocation
from worlds.smz3.TotalSMZ3.Location import locations_start_id, Location as TotalSMZ3Location
from worlds.smz3.TotalSMZ3.Patch import Patch as TotalSMZ3Patch
from ..AutoWorld import World
from .Rom import get_base_rom_bytes
from .ips import IPS_Patch

class SMZ3World(World):
    game: str = "SMZ3"
    topology_present = False
    data_version = 0
    # options = sm_options
    item_names: Set[str] = frozenset(TotalSMZ3Item.lookup_name_to_id)
    location_names: Set[str]
    item_name_to_id = TotalSMZ3Item.lookup_name_to_id
    location_name_to_id: Dict[str, int] = {key : locations_start_id + value.Id for key, value in TotalSMZ3World(Config({}), "", 0, "").locationLookup.items()}

    remote_items: bool = False
    remote_start_inventory: bool = False

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.locations = {}
        super().__init__(world, player)
        
    def __new__(cls, world, player):
        # Add necessary objects to CollectionState on initialization
        orig_init = CollectionState.__init__
        orig_copy = CollectionState.copy

        def smz3_init(self, parent: MultiWorld):
            if (hasattr(parent, "state")): # for unit tests where MultiWorld is instanciated before worlds
                self.smz3state = {player: TotalSMZ3Item.Progression([]) for player in parent.get_game_players("SMZ3")}
            orig_init(self, parent)

        def smz3_copy(self):
            ret = orig_copy(self)
            ret.smz3state = {player: copy.deepcopy(self.smz3state[player]) for player in self.world.get_game_players("SMZ3")}
            return ret

        CollectionState.__init__ = smz3_init
        CollectionState.copy = smz3_copy

        if world:
            world.state.smz3state = {}

        return super().__new__(cls)

    def generate_early(self):
        self.smz3World = TotalSMZ3World(Config({}), self.world.get_player_name(self.player), self.player, self.world.seed_name)
        self.smz3DungeonItems = []
        SMZ3World.location_names = frozenset(self.smz3World.locationLookup.keys())

        self.world.state.smz3state[self.player] = TotalSMZ3Item.Progression([])
        self.world.accessibility[self.player] = self.world.accessibility[self.player].from_text("none")
    
    def generate_basic(self):
        self.smz3World.Setup(self.world.random)
        self.dungeon = TotalSMZ3Item.Item.CreateDungeonPool(self.smz3World)
        self.dungeon.reverse()
        self.progression = TotalSMZ3Item.Item.CreateProgressionPool(self.smz3World)
        self.keyCardsItems = TotalSMZ3Item.Item.CreateKeycards(self.smz3World)
        #self.totalSMZ3ItemsMap = {i.Type.name:i for i in (self.dungeon + self.progression + self.keyCardsItems)}
        niceItems = TotalSMZ3Item.Item.CreateNicePool(self.smz3World)
        junkItems = TotalSMZ3Item.Item.CreateJunkPool(self.smz3World)
        allJunkItems = niceItems + junkItems

        if (self.smz3World.Config.Keysanity):
            progressionItems = self.dungeon + self.progression
            progressionItems = progressionItems + self.keyCardsItems
        else:
            progressionItems = self.progression 
            for item in self.keyCardsItems:
                self.world.push_precollected(SMZ3Item(item.Type.name, True, item.Type, self.item_name_to_id[item.Type.name], self.player, item))

        itemPool = [SMZ3Item(item.Type.name, True, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in progressionItems] + \
                    [SMZ3Item(item.Type.name, False, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in allJunkItems]
        self.smz3DungeonItems = [SMZ3Item(item.Type.name, True, item.Type, self.item_name_to_id[item.Type.name], self.player, item) for item in self.dungeon]
        self.world.itempool += itemPool

    def set_rules(self):
        self.world.completion_condition[self.player] = lambda state: self.smz3World.GetRegion("Ganon's Tower").CanEnter(state.smz3state[self.player]) and \
                                                                    state.smz3state[self.player].BigKeyGT

        for region in self.smz3World.Regions:
            entrance = self.world.get_entrance('Menu' + "->" + region.Name, self.player)
            set_rule(entrance, lambda state, region=region: region.CanEnter(state.smz3state[self.player]))
            for loc in region.Locations:
                l = self.locations[loc.Name]
                l.always_allow = lambda state, item, loc=loc: \
                    item.game == "SMZ3" and \
                    loc.alwaysAllow(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World), state.smz3state[self.player])
                l.item_rule = lambda item, loc=loc, region=region: \
                    item.game != "SMZ3" or \
                    loc.allow(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World), None) and \
                        region.CanFill(TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World))
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

    def generate_output(self, output_directory: str):
        try:
            base_combined_rom = get_base_rom_bytes()
            basepatch = IPS_Patch.load("worlds/smz3/zsm.ips")
            base_combined_rom = basepatch.apply(base_combined_rom)

            patcher = TotalSMZ3Patch(self.smz3World,
                                    [world.smz3World for key, world in self.world.worlds.items() if isinstance(world, SMZ3World)],
                                    self.world.seed_name,
                                    self.world.seed,
                                    self.world.random,
                                    self.world.world_name_lookup,
                                    next(iter(loc.player for loc in self.world.get_locations() if loc.item == self.create_item("SilverArrows"))))
            patches = patcher.Create(self.smz3World.Config)
            for addr, bytes in patches.items():
                offset = 0
                for byte in bytes:
                    base_combined_rom[addr + offset] = byte
                    offset += 1
            filename = f"SMZ3_{self.world.seed}_{self.world.get_player_name(self.player)}.sfc"
            filename = os.path.join(output_directory, filename)
            with open(filename, "wb") as binary_file:
                binary_file.write(base_combined_rom)
            Patch.create_patch_file(filename, player=self.player, player_name=self.world.player_name[self.player], game=Patch.GAME_SMZ3)
            self.rom_name = bytearray(patcher.title, 'utf8')
        except:
            raise
        finally:
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            payload = multidata["connect_names"][self.world.player_name[self.player]]
            multidata["connect_names"][new_name] = payload
            del (multidata["connect_names"][self.world.player_name[self.player]])

    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.smz3state[item.player].Add([TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World)])
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True  # indicate that a logical state change has occured
        return False

    def remove(self, state: CollectionState, item: Item) -> bool:
        name = self.collect_item(state, item, True)
        if name:
            state.smz3state[item.player].Remove([TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.smz3World)])
            state.prog_items[name, item.player] -= 1
            if state.prog_items[name, item.player] < 1:
                del (state.prog_items[name, item.player])
            return True
        return False

    #def collectOwnProgSMZ3Item(self, state: CollectionState, item: TotalSMZ3Item.Item) -> bool:
    #    state.smz3state[self.player].Add([item])
    #    state.prog_items[item.Type.name, self.player] += 1

    def create_item(self, name: str) -> Item:
        return SMZ3Item(name, True, TotalSMZ3Item.ItemType[name], self.item_name_to_id[name], player = self.player)

    def pre_fill(self):
        from Fill import fill_restrictive
        self.InitialFillInOwnWorld()

        if (not self.smz3World.Config.Keysanity):
            #state = CollectionState(self.world)
            #for i in (self.progression + self.keyCardsItems):
            #    state.collect(self.create_item(i.Type.name), True)
                # self.collectOwnProgSMZ3Item(state, i)    
            #items = []
            #for i in self.dungeon:
            #    for i2 in self.smz3Items:
            #        if i.Type.name == i2.name:
            #            items.append(i2)
            #            break
            fill_restrictive(self.world, self.world.get_all_state(False), [loc for loc in self.locations.values() if loc.item is None], self.smz3DungeonItems, True, True)

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
        itemFromPool = next((i for i in self.world.itempool if i.player == self.player and i.name == item.Type.name), None)
        if itemFromPool is not None:
            self.world.get_location(location.Name, self.player).place_locked_item(itemFromPool)
            self.world.itempool.remove(itemFromPool)
        itemPool.remove(item)

    def InitialFillInOwnWorld(self):
        self.FillItemAtLocation(self.dungeon, TotalSMZ3Item.ItemType.KeySW, self.smz3World.GetLocation("Skull Woods - Pinball Room"))

        # /* Check Swords option and place as needed */
        if self.smz3World.Config.SwordLocation == SwordLocation.Uncle:
            self.FillItemAtLocation(self.progression, TotalSMZ3Item.ItemType.ProgressiveSword, self.smz3World.GetLocation("Link's Uncle"))
        else:
            self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.ProgressiveSword)

        # /* Check Morph option and place as needed */
        if self.smz3World.Config.MorphLocation == MorphLocation.Original:
            self.FillItemAtLocation(self.progression, TotalSMZ3Item.ItemType.Morph, self.smz3World.GetLocation("Morphing Ball"))
        else:
            self.FrontFillItemInOwnWorld(self.progression, TotalSMZ3Item.ItemType.Morph)

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

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        oldItem = self.item
        self.item = item
        result = self.always_allow(state, item) or (self.item_rule(item) and (not check_access or self.can_reach(state)))
        self.item = oldItem
        return result

    #def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
    #    return self.parent_region.world.worlds[self.player].smz3World.GetLocation(self.name).CanFill(
    #        TotalSMZ3Item.Item(TotalSMZ3Item.ItemType[item.name], self.parent_region.world.worlds[self.player]), state.smz3state[self.player])
        # return self.always_allow(state, item) or (self.item_rule(item) and (not check_access or self.can_reach(state)))


class SMZ3Item(Item):
    game = "SMZ3"

    def __init__(self, name, advancement, type, code, player: int = None, item = None):
        self.type = type
        self.item = item
        super(SMZ3Item, self).__init__(name, advancement, code, player)