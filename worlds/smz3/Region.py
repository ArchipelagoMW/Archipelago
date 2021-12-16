from enum import Enum
from typing import Dict, List
from Config import *
from Item import Item, Progression, ItemType
from Region import Region
from World import World
from worlds.smz3.Location import Location

class RewardType(Enum):
    Null = 0
    Agahnim = 1
    PendantGreen = 2
    PendantNonGreen = 3
    CrystalBlue = 4
    CrystalRed = 5
    GoldenFourBoss = 6

class IReward:
    Reward: RewardType
    def CanComplete(self, items: Progression):
        pass

class IMedallionAccess:
    Medallion: ItemType

class SMRegion(Region):
    Logic: SMLogic = Config.SMLogic
    def __init__(self, world: World, config: Config):
        super().__init__(world, config)

class Z3Region(Region):
    def __init__(self, world: World, config: Config):
        super().__init__(world, config)

class Region:
    Name: str
    Area: str = Name

    Locations: List[Location]
    World: World
    Weight: int = 0

    Config: Config
    RegionItems:List[ItemType]

    locationLookup: Dict[str, Location]
    
    def GetLocation(self, name: str):
        return self.locationLookup[name]

    def __init__(self, world: World, config: Config):
        Config = config
        World = world
        locationLookup = {}

    def GenerateLocationLookup(self):
        locationLookup = {loc.Name:loc for loc in self.Locations}

    def IsRegionItem(self, item:Item):
        return item.Type in self.RegionItems

    def CanFill(self, item:Item, items:Progression):
        return self.Config.Keysanity or not item.IsDungeonItem or self.IsRegionItem(item)

    def CanEnter(items:Progression):
        return True
