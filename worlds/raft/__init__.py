import typing

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import (createResourcePackName, item_table, progressive_table, progressive_item_list,
    lookup_name_to_item, resourcepack_items as resourcePackItems, lookup_name_to_id as items_lookup_name_to_id)

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import RaftOptions

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld


class RaftWeb(WebWorld):
    theme = "ocean"
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
    options_dataclass = RaftOptions
    options: RaftOptions

    required_client_version = (0, 3, 4)

    def create_items(self):
        minRPSpecified = self.options.minimum_resource_pack_amount.value
        maxRPSpecified = self.options.maximum_resource_pack_amount.value
        minimumResourcePackAmount = min(minRPSpecified, maxRPSpecified)
        maximumResourcePackAmount = max(minRPSpecified, maxRPSpecified)
        isFillingFrequencies = self.options.island_frequency_locations.is_filling_frequencies_in_world()
        # Generate item pool
        pool = []
        frequencyItems = []
        for item in item_table:
            raft_item = self.create_item_replaceAsNecessary(item["name"])
            if isFillingFrequencies and "Frequency" in item["name"]:
                frequencyItems.append(raft_item)
            else:
                pool.append(raft_item)
        if isFillingFrequencies:
            if not hasattr(self.multiworld, "raft_frequencyItemsPerPlayer"):
                self.multiworld.raft_frequencyItemsPerPlayer = {}
            self.multiworld.raft_frequencyItemsPerPlayer[self.player] = frequencyItems

        extraItemNamePool = []
        extras = len(location_table) - len(item_table) - 1 # Victory takes up 1 unaccounted-for slot
        if extras > 0:
            if (self.options.filler_item_types != self.options.filler_item_types.option_duplicates): # Use resource packs
                for packItem in resourcePackItems:
                    for i in range(minimumResourcePackAmount, maximumResourcePackAmount + 1):
                        extraItemNamePool.append(createResourcePackName(i, packItem))

            if self.options.filler_item_types != self.options.filler_item_types.option_resource_packs: # Use duplicate items
                dupeItemPool = item_table.copy()
                # Remove frequencies if necessary
                if self.options.island_frequency_locations != self.options.island_frequency_locations.option_anywhere: # Not completely random locations
                    # If we let frequencies stay in with progressive-frequencies, the progressive-frequency item
                    # will be included 7 times. This is a massive flood of progressive-frequency items, so we
                    # instead add progressive-frequency as its own item a smaller amount of times to prevent
                    # flooding the duplicate item pool with them.
                    if self.options.island_frequency_locations == self.options.island_frequency_locations.option_progressive:
                        for _ in range(2):
                            # Progressives are not in item_pool, need to create faux item for duplicate item pool
                            # This can still be filtered out later by duplicate_items setting
                            dupeItemPool.append({ "name": "progressive-frequency", "progression": True }) # Progressive frequencies need to be included
                    # Always remove non-progressive Frequency items
                    dupeItemPool = (itm for itm in dupeItemPool if "Frequency" not in itm["name"])
                
                # Remove progression or non-progression items if necessary
                if (self.options.duplicate_items == self.options.duplicate_items.option_progression): # Progression only
                    dupeItemPool = (itm for itm in dupeItemPool if itm["progression"] == True)
                elif (self.options.duplicate_items == self.options.duplicate_items.option_non_progression): # Non-progression only
                    dupeItemPool = (itm for itm in dupeItemPool if itm["progression"] == False)
                
                dupeItemPool = list(dupeItemPool)
                # Finally, add items as necessary
                if len(dupeItemPool) > 0:
                    for item in dupeItemPool:
                        extraItemNamePool.append(item["name"])
            
            if (len(extraItemNamePool) > 0):
                for randomItem in self.random.choices(extraItemNamePool, k=extras):
                    raft_item = self.create_item_replaceAsNecessary(randomItem)
                    pool.append(raft_item)

        self.multiworld.itempool += pool

        # Victory item
        self.multiworld.get_location("Utopia Complete", self.player).place_locked_item(
            RaftItem("Victory", ItemClassification.progression, None, player=self.player))

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)
    
    def get_pre_fill_items(self):
        if self.options.island_frequency_locations.is_filling_frequencies_in_world():
            return [loc.item for loc in self.multiworld.get_filled_locations()]
        return []
    
    def create_item_replaceAsNecessary(self, name: str) -> Item:
        isFrequency = "Frequency" in name
        shouldUseProgressive = bool((isFrequency and self.options.island_frequency_locations == self.options.island_frequency_locations.option_progressive)
            or (not isFrequency and self.options.progressive_items))
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
        if item.advancement is False:
            return None
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
        if self.options.island_frequency_locations == self.options.island_frequency_locations.option_vanilla:
            self.setLocationItem("Radio Tower Frequency to Vasagatan", "Vasagatan Frequency")
            self.setLocationItem("Vasagatan Frequency to Balboa", "Balboa Island Frequency")
            self.setLocationItem("Relay Station quest", "Caravan Island Frequency")
            self.setLocationItem("Caravan Island Frequency to Tangaroa", "Tangaroa Frequency")
            self.setLocationItem("Tangaroa Frequency to Varuna Point", "Varuna Point Frequency")
            self.setLocationItem("Varuna Point Frequency to Temperance", "Temperance Frequency")
            self.setLocationItem("Temperance Frequency to Utopia", "Utopia Frequency")
        elif self.options.island_frequency_locations == self.options.island_frequency_locations.option_random_on_island:
            self.setLocationItemFromRegion("RadioTower", "Vasagatan Frequency")
            self.setLocationItemFromRegion("Vasagatan", "Balboa Island Frequency")
            self.setLocationItemFromRegion("BalboaIsland", "Caravan Island Frequency")
            self.setLocationItemFromRegion("CaravanIsland", "Tangaroa Frequency")
            self.setLocationItemFromRegion("Tangaroa", "Varuna Point Frequency")
            self.setLocationItemFromRegion("Varuna Point", "Temperance Frequency")
            self.setLocationItemFromRegion("Temperance", "Utopia Frequency")
        elif self.options.island_frequency_locations in [
            self.options.island_frequency_locations.option_random_island_order,
            self.options.island_frequency_locations.option_random_on_island_random_order
        ]:
            locationToFrequencyItemMap = {
                "Vasagatan": "Vasagatan Frequency",
                "BalboaIsland": "Balboa Island Frequency",
                "CaravanIsland": "Caravan Island Frequency",
                "Tangaroa": "Tangaroa Frequency",
                "Varuna Point": "Varuna Point Frequency",
                "Temperance": "Temperance Frequency",
                "Utopia": "Utopia Frequency"
            }
            locationToVanillaFrequencyLocationMap = {
                "RadioTower": "Radio Tower Frequency to Vasagatan",
                "Vasagatan": "Vasagatan Frequency to Balboa",
                "BalboaIsland": "Relay Station quest",
                "CaravanIsland": "Caravan Island Frequency to Tangaroa",
                "Tangaroa": "Tangaroa Frequency to Varuna Point",
                "Varuna Point": "Varuna Point Frequency to Temperance",
                "Temperance": "Temperance Frequency to Utopia"
            }
            # Utopia is never chosen until the end, otherwise these are chosen randomly
            availableLocationList = ["Vasagatan", "BalboaIsland", "CaravanIsland", "Tangaroa", "Varuna Point", "Temperance", "Utopia"]
            previousLocation = "RadioTower"
            while (len(availableLocationList) > 0):
                if (len(availableLocationList) > 1):
                    currentLocation = availableLocationList[self.random.randint(0, len(availableLocationList) - 2)]
                else:
                    currentLocation = availableLocationList[0] # Utopia (only one left in list)
                availableLocationList.remove(currentLocation)
                if self.options.island_frequency_locations == self.options.island_frequency_locations.option_random_island_order:
                    self.setLocationItem(locationToVanillaFrequencyLocationMap[previousLocation], locationToFrequencyItemMap[currentLocation])
                elif self.options.island_frequency_locations == self.options.island_frequency_locations.option_random_on_island_random_order:
                    self.setLocationItemFromRegion(previousLocation, locationToFrequencyItemMap[currentLocation])
                previousLocation = currentLocation
    
    def setLocationItem(self, location: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.multiworld.raft_frequencyItemsPerPlayer[self.player]))
        self.multiworld.raft_frequencyItemsPerPlayer[self.player].remove(itemToUse)
        self.multiworld.get_location(location, self.player).place_locked_item(itemToUse)
    
    def setLocationItemFromRegion(self, region: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.multiworld.raft_frequencyItemsPerPlayer[self.player]))
        self.multiworld.raft_frequencyItemsPerPlayer[self.player].remove(itemToUse)
        location = self.random.choice(list(loc for loc in location_table if loc["region"] == region))
        self.multiworld.get_location(location["name"], self.player).place_locked_item(itemToUse)
    
    def fill_slot_data(self):
        return {
            "IslandGenerationDistance": self.options.island_generation_distance.value,
            "ExpensiveResearch": bool(self.options.expensive_research),
            "DeathLink": bool(self.options.death_link)
        }

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
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
