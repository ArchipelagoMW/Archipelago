from enum import Enum
from typing import Dict, List
from .Config import *

class RewardType(Enum):
    Null = 0
    Agahnim = 1 << 0
    PendantGreen = 1 << 1
    PendantNonGreen = 1 << 2
    CrystalBlue = 1 << 3
    CrystalRed = 1 << 4
    BossTokenKraid = 1 << 5
    BossTokenPhantoon = 1 << 6
    BossTokenDraygon = 1 << 7
    BossTokenRidley = 1 << 8

    AnyPendant = PendantGreen | PendantNonGreen
    AnyCrystal = CrystalBlue | CrystalRed
    AnyBossToken = BossTokenKraid | BossTokenPhantoon | BossTokenDraygon | BossTokenRidley

class IReward:
    Reward: RewardType
    def CanComplete(self, items):
        pass

class IMedallionAccess:
    Medallion = None

class Region:
    from . import Location
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
        self.world = world
        self.locationLookup = {}
        self.RegionItems = []

    def GenerateLocationLookup(self):
        self.locationLookup = {loc.Name:loc for loc in self.Locations}

    def IsRegionItem(self, item):
        return item.Type in self.RegionItems

    def CanFill(self, item):
        return self.Config.Keysanity or not item.IsDungeonItem() or self.IsRegionItem(item)

    def CanEnter(self, items):
        return True

class SMRegion(Region):
    Logic: SMLogic = Config.SMLogic
    def __init__(self, world, config: Config):
        super().__init__(world, config)

class Z3Region(Region):
    def __init__(self, world, config: Config):
        super().__init__(world, config)
