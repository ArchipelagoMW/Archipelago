from typing import Dict, List
import random

import worlds.smz3.TotalSMZ3.Region as Region
import worlds.smz3.TotalSMZ3.Config as Config
import worlds.smz3.TotalSMZ3.Item as Item
import worlds.smz3.TotalSMZ3.Location as Location

from worlds.smz3.TotalSMZ3.Regions.Zelda.CastleTower import CastleTower
from worlds.smz3.TotalSMZ3.Regions.Zelda.EasternPalace import EasternPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.DesertPalace import DesertPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.TowerOfHera import TowerOfHera
from worlds.smz3.TotalSMZ3.Regions.Zelda.PalaceOfDarkness import PalaceOfDarkness
from worlds.smz3.TotalSMZ3.Regions.Zelda.SwampPalace import SwampPalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.SkullWoods import SkullWoods
from worlds.smz3.TotalSMZ3.Regions.Zelda.ThievesTown import ThievesTown
from worlds.smz3.TotalSMZ3.Regions.Zelda.IcePalace import IcePalace
from worlds.smz3.TotalSMZ3.Regions.Zelda.MiseryMire import MiseryMire
from worlds.smz3.TotalSMZ3.Regions.Zelda.TurtleRock import TurtleRock
from worlds.smz3.TotalSMZ3.Regions.Zelda.GanonsTower import GanonsTower
from worlds.smz3.TotalSMZ3.Regions.Zelda.LightWorld.DeathMountain.West import West as LightWorldDeathMountainWest
from worlds.smz3.TotalSMZ3.Regions.Zelda.LightWorld.DeathMountain.East import East as LightWorldDeathMountainEast
from worlds.smz3.TotalSMZ3.Regions.Zelda.LightWorld.NorthWest import NorthWest as LightWorldNorthWest
from worlds.smz3.TotalSMZ3.Regions.Zelda.LightWorld.NorthEast import NorthEast as LightWorldNorthEast
from worlds.smz3.TotalSMZ3.Regions.Zelda.LightWorld.South import South as LightWorldSouth
from worlds.smz3.TotalSMZ3.Regions.Zelda.HyruleCastle import HyruleCastle
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.DeathMountain.West import West as DarkWorldDeathMountainWest
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.DeathMountain.East import East as DarkWorldDeathMountainEast
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.NorthWest import NorthWest as DarkWorldNorthWest
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.NorthEast import NorthEast as DarkWorldNorthEast
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.South import South as DarkWorldSouth
from worlds.smz3.TotalSMZ3.Regions.Zelda.DarkWorld.Mire import Mire as DarkWorldMire
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Crateria.Central import Central
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Crateria.West import West as CrateriaWest 
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Crateria.East import East as CrateriaEast
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Brinstar.Blue import Blue
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Brinstar.Green import Green
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Brinstar.Kraid import Kraid
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Brinstar.Pink import Pink
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Brinstar.Red import Red
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Maridia.Outer import Outer
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.Maridia.Inner import Inner
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.NorfairUpper.West import West as NorfairUpperWest
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.NorfairUpper.East import East as NorfairUpperEast
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.NorfairUpper.Crocomire import Crocomire
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.NorfairLower.West import West as NorfairLowerWest
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.NorfairLower.East import East as NorfairLowerEast
from worlds.smz3.TotalSMZ3.Regions.SuperMetroid.WreckedShip import WreckedShip

class World:
    Locations: List[Location.Location]
    Regions: List[Region.Region]
    Config: Config.Config
    Player: str
    Guid: str
    Id: int

    def Items(self):
        return [l.Item for l in self.Locations if l.Item != None]

    locationLookup: Dict[str, Location.Location]
    regionLookup: Dict[str, Region.Region]

    def GetLocation(self, name:str): return self.locationLookup[name]
    def GetRegion(self, name:str): return self.regionLookup[name]

    def __init__(self, config: Config, player: str, id: int, guid: str):
        self.Config = config
        self.Player = player
        self.Id = id
        self.Guid = guid

        self.Regions = [
            CastleTower(self, self.Config),
            EasternPalace(self, self.Config),
            DesertPalace(self, self.Config),
            TowerOfHera(self, self.Config),
            PalaceOfDarkness(self, self.Config),
            SwampPalace(self, self.Config),
            SkullWoods(self, self.Config),
            ThievesTown(self, self.Config),
            IcePalace(self, self.Config),
            MiseryMire(self, self.Config),
            TurtleRock(self, self.Config),
            GanonsTower(self, self.Config),
            LightWorldDeathMountainWest(self, self.Config),
            LightWorldDeathMountainEast(self, self.Config),
            LightWorldNorthWest(self, self.Config),
            LightWorldNorthEast(self, self.Config),
            LightWorldSouth(self, self.Config),
            HyruleCastle(self, self.Config),
            DarkWorldDeathMountainWest(self, self.Config),
            DarkWorldDeathMountainEast(self, self.Config),
            DarkWorldNorthWest(self, self.Config),
            DarkWorldNorthEast(self, self.Config),
            DarkWorldSouth(self, self.Config),
            DarkWorldMire(self, self.Config),
            Central(self, self.Config),
            CrateriaWest(self, self.Config),
            CrateriaEast(self, self.Config),
            Blue(self, self.Config),
            Green(self, self.Config),
            Kraid(self, self.Config),
            Pink(self, self.Config),
            Red(self, self.Config),
            Outer(self, self.Config),
            Inner(self, self.Config),
            NorfairUpperWest(self, self.Config),
            NorfairUpperEast(self, self.Config),
            Crocomire(self, self.Config),
            NorfairLowerWest(self, self.Config),
            NorfairLowerEast(self, self.Config),
            WreckedShip(self, self.Config)
        ]

        self.Locations = []
        for r in self.Regions:
            self.Locations = self.Locations + r.Locations

        self.regionLookup = {r.Name:r for r in self.Regions}
        self.locationLookup = {loc.Name:loc for loc in self.Locations}
        
        for region in self.Regions:
            region.GenerateLocationLookup()


    def CanEnter(self, regionName: str, items: Item.Progression):
        region = self.regionLookup[regionName]
        if (region == None):
            raise Exception(f"World.CanEnter: Invalid region name {regionName}", f'{regionName=}'.partition('=')[0])
        return region.CanEnter(items)

    def CanAquire(self, items: Item.Progression, reward: Region.RewardType):
        return next(iter([region for region in self.Regions if isinstance(region, Region.IReward) and region.Reward == reward])).CanComplete(items)

    def CanAquireAll(self, items: Item.Progression, *rewards: Region.RewardType):
        return all(region.CanComplete(items) for region in self.Regions if isinstance(region, Region.IReward) and region.Reward in rewards)

    def Setup(self, rnd: random):
        self.SetMedallions(rnd)
        self.SetRewards(rnd)

    def SetMedallions(self, rnd: random):
        medallionMap = {0: Item.ItemType.Bombos, 1: Item.ItemType.Ether, 2: Item.ItemType.Quake}
        regionList = [region for region in self.Regions if isinstance(region, Region.IMedallionAccess)]
        for region in regionList:
            region.Medallion = medallionMap[rnd.randint(0, 2)]

    def SetRewards(self, rnd: random):
        rewards = [
            Region.RewardType.PendantGreen, Region.RewardType.PendantNonGreen, Region.RewardType.PendantNonGreen, Region.RewardType.CrystalRed, Region.RewardType.CrystalRed,
            Region.RewardType.CrystalBlue, Region.RewardType.CrystalBlue, Region.RewardType.CrystalBlue, Region.RewardType.CrystalBlue, Region.RewardType.CrystalBlue
            ]
        rnd.shuffle(rewards)
        regionList = [region for region in self.Regions if isinstance(region, Region.IReward) and region.Reward == Region.RewardType.Null]
        for region in regionList:
            region.Reward = rewards[0]
            rewards.remove(region.Reward)

