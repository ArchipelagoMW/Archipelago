import typing
import random

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import (createResourcePackName, item_table, progressive_table, progressive_item_list,
    lookup_name_to_item, resourcepack_items as resourcePackItems, lookup_name_to_id as items_lookup_name_to_id)

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import raft_options

from BaseClasses import Region, RegionType, Entrance, Location, MultiWorld, Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld


class RaftWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Raft integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SunnyBat", "Awareqwx"]
    )]


class RaftWorld(World):
    """
    Raft is a flooded world exploration game. You're stranded on a small raft in the middle of the
    ocean, and you must survive on trash floating by you on the top of the water and around/on any
    islands that you come across.
    """
    game: str = "Raft"
    web = RaftWeb()

    item_name_to_id = items_lookup_name_to_id.copy()
    lastItemId = max(filter(lambda val: val is not None, item_name_to_id.values()))

    location_name_to_id = locations_lookup_name_to_id
    options = raft_options

    data_version = 2
    required_client_version = (0, 3, 4)

    def generate_basic(self):
        minRPSpecified = self.world.minimum_resource_pack_amount[self.player].value
        maxRPSpecified = self.world.maximum_resource_pack_amount[self.player].value
        minimumResourcePackAmount = min(minRPSpecified, maxRPSpecified)
        maximumResourcePackAmount = max(minRPSpecified, maxRPSpecified)
        # Generate item pool
        pool = []
        for item in item_table:
            raft_item = self.create_item_replaceAsNecessary(item["name"])
            pool.append(raft_item)

        extraItemNamePool = []
        extras = len(location_table) - len(item_table) - 1 # Victory takes up 1 unaccounted-for slot
        if extras > 0:
            if (self.world.use_resource_packs[self.player].value):
                for packItem in resourcePackItems:
                    for i in range(minimumResourcePackAmount, maximumResourcePackAmount + 1):
                        extraItemNamePool.append(createResourcePackName(i, packItem))

            if self.world.duplicate_items[self.player].value != 0:
                dupeItemPool = item_table.copy()
                # Remove frequencies if necessary
                if self.world.island_frequency_locations[self.player].value != 3: # Not completely random locations
                    dupeItemPool = (itm for itm in dupeItemPool if "Frequency" not in itm["name"])
                
                # Remove progression or non-progression items if necessary
                if (self.world.duplicate_items[self.player].value == 1): # Progression only
                    dupeItemPool = (itm for itm in dupeItemPool if itm["progression"] == True)
                elif (self.world.duplicate_items[self.player].value == 2): # Non-progression only
                    dupeItemPool = (itm for itm in dupeItemPool if itm["progression"] == False)
                
                dupeItemPool = list(dupeItemPool)
                # Finally, add items as necessary
                if len(dupeItemPool) > 0:
                    for item in dupeItemPool:
                        extraItemNamePool.append(item["name"])
            
            if (len(extraItemNamePool) > 0):
                for randomItem in random.choices(extraItemNamePool, k=extras):
                    raft_item = self.create_item_replaceAsNecessary(randomItem)
                    pool.append(raft_item)

        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data
    
    def get_pre_fill_items(self):
        if self.world.island_frequency_locations[self.player] in [0, 1]:
            return [loc.item for loc in self.world.get_filled_locations()]
        return []
    
    def create_item_replaceAsNecessary(self, name: str) -> Item:
        isFrequency = "Frequency" in name
        shouldUseProgressive = ((isFrequency and self.world.island_frequency_locations[self.player].value == 2)
            or (not isFrequency and self.world.progressive_items[self.player].value))
        if shouldUseProgressive and name in progressive_table:
            name = progressive_table[name]
        return self.create_item(name)

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        return RaftItem(name, ItemClassification.progression if item["progression"] else ItemClassification.filler,
                        self.item_name_to_id[name], player=self.player)
    
    def create_resourcePack(self, rpName: str) -> Item:
        return RaftItem(rpName, ItemClassification.filler, self.item_name_to_id[rpName], player=self.player)
    
    def collect_item(self, state, item, remove=False):
        if item.name in progressive_item_list:
            prog_table = progressive_item_list[item.name]
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(RaftWorld, self).collect_item(state, item, remove)

    def pre_fill(self):
        if self.world.island_frequency_locations[self.player] == 0:
            self.setLocationItem("Radio Tower Frequency to Vasagatan", "Vasagatan Frequency")
            self.setLocationItem("Vasagatan Frequency to Balboa", "Balboa Island Frequency")
            self.setLocationItem("Relay Station quest", "Caravan Island Frequency")
            self.setLocationItem("Caravan Island Frequency to Tangaroa", "Tangaroa Frequency")
            self.setLocationItem("Tangaroa Frequency to Varuna Point", "Varuna Point Frequency")
            self.setLocationItem("Varuna Point Frequency to Temperance", "Temperance Frequency")
            self.setLocationItem("Temperance Frequency to Utopia", "Utopia Frequency")
        elif self.world.island_frequency_locations[self.player] == 1:
            self.setLocationItemFromRegion("RadioTower", "Vasagatan Frequency")
            self.setLocationItemFromRegion("Vasagatan", "Balboa Island Frequency")
            self.setLocationItemFromRegion("BalboaIsland", "Caravan Island Frequency")
            self.setLocationItemFromRegion("CaravanIsland", "Tangaroa Frequency")
            self.setLocationItemFromRegion("Tangaroa", "Varuna Point Frequency")
            self.setLocationItemFromRegion("Varuna Point", "Temperance Frequency")
            self.setLocationItemFromRegion("Temperance", "Utopia Frequency")
        # Victory item
        self.world.get_location("Utopia Complete", self.player).place_locked_item(
            RaftItem("Victory", ItemClassification.progression, None, player=self.player))
    
    def setLocationItem(self, location: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.world.itempool))
        self.world.itempool.remove(itemToUse)
        self.world.get_location(location, self.player).place_locked_item(itemToUse)
    
    def setLocationItemFromRegion(self, region: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.world.itempool))
        self.world.itempool.remove(itemToUse)
        location = random.choice(list(loc for loc in location_table if loc["region"] == region))
        self.world.get_location(location["name"], self.player).place_locked_item(itemToUse)
    
    def fill_slot_data(self):
        return {
            "IslandGenerationDistance": self.world.island_generation_distance[self.player].value,
            "ExpensiveResearch": self.world.expensive_research[self.player].value
        }

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            locationObj = RaftLocation(player, location, loc_id, ret)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))

    return ret

class RaftLocation(Location):
    game = "Raft"


class RaftItem(Item):
    game = "Raft"
