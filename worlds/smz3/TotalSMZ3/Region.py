from enum import Enum
from typing import Dict, List
from worlds.smz3.TotalSMZ3.Config import *

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
    def CanComplete(self, items):
        pass

class IMedallionAccess:
    Medallion: object

class Region:
    import worlds.smz3.TotalSMZ3.Location as Location
    Name: str
    Area: str

    Locations: List[Location.Location]
    Weight: int = 0

    Config: Config

    locationLookup: Dict[str, Location.Location]
    
    def GetLocation(self, name: str):
        return self.locationLookup[name]

    def __init__(self, world, config: Config):
        self.Config = config
        self.World = world
        self.locationLookup = {}
        self.RegionItems = []

    def GenerateLocationLookup(self):
        locationLookup = {loc.Name:loc for loc in self.Locations}

    def IsRegionItem(self, item):
        return item.Type in self.RegionItems

    def CanFill(self, item, items):
        return self.Config.Keysanity or not item.IsDungeonItem() or self.IsRegionItem(item)

    def CanEnter(items):
        return True

class SMRegion(Region):
    Logic: SMLogic = Config.SMLogic
    def __init__(self, world, config: Config):
        super().__init__(world, config)

class Z3Region(Region):
    def __init__(self, world, config: Config):
        super().__init__(world, config)
