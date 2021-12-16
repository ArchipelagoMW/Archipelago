from typing import Dict, List
from Region import Region
from Config import Config
from Item import Progression
from Region import RewardType, IReward, IMedallionAccess
from Item import ItemType
from Location import Location
import random
import Regions.Zelda.CastleTower
import Regions.Zelda.EasternPalace
import Regions.Zelda.DesertPalace
import Regions.Zelda.TowerOfHera
import Regions.Zelda.PalaceOfDarkness
import Regions.Zelda.SwampPalace
import Regions.Zelda.SkullWoods
import Regions.Zelda.ThievesTown
import Regions.Zelda.IcePalace
import Regions.Zelda.MiseryMire
import Regions.Zelda.TurtleRock
import Regions.Zelda.GanonsTower
import Regions.Zelda.LightWorld.DeathMountain.West
import Regions.Zelda.LightWorld.DeathMountain.East
import Regions.Zelda.LightWorld.NorthWest
import Regions.Zelda.LightWorld.NorthEast
import Regions.Zelda.LightWorld.South
import Regions.Zelda.HyruleCastle
import Regions.Zelda.DarkWorld.DeathMountain.West
import Regions.Zelda.DarkWorld.DeathMountain.East
import Regions.Zelda.DarkWorld.NorthWest
import Regions.Zelda.DarkWorld.NorthEast
import Regions.Zelda.DarkWorld.South
import Regions.Zelda.DarkWorld.Mire
import Regions.SuperMetroid.Crateria.Central
import Regions.SuperMetroid.Crateria.West
import Regions.SuperMetroid.Crateria.East
import Regions.SuperMetroid.Brinstar.Blue
import Regions.SuperMetroid.Brinstar.Green
import Regions.SuperMetroid.Brinstar.Kraid
import Regions.SuperMetroid.Brinstar.Pink
import Regions.SuperMetroid.Brinstar.Red
import Regions.SuperMetroid.Maridia.Outer
import Regions.SuperMetroid.Maridia.Inner
import Regions.SuperMetroid.NorfairUpper.West
import Regions.SuperMetroid.NorfairUpper.East
import Regions.SuperMetroid.NorfairUpper.Crocomire
import Regions.SuperMetroid.NorfairLower.West
import Regions.SuperMetroid.NorfairLower.East
import Regions.SuperMetroid.WreckedShip

class World:
    Locations: List[Location]
    Regions: List[Region]
    Config: Config
    Player: str
    Guid: str
    Id: int

    def Items(self):
        return [l.Item for l in self.Locations if l.Item != None]


    locationLookup: Dict[str, Location]
    regionLookup: Dict[str, Region]

    def GetLocation(self, name:str): return self.locationLookup[name]
    def GetRegion(self, name:str): return self.regionLookup[name]

    def __init__(self, config: Config, player: str, id: int, guid: str):
        self.Config = config
        self.Player = player
        self.Id = id
        self.Guid = guid

        self.Regions = [
            Regions.Zelda.CastleTower(self, self.Config),
            Regions.Zelda.EasternPalace(self, self.Config),
            Regions.Zelda.DesertPalace(self, self.Config),
            Regions.Zelda.TowerOfHera(self, self.Config),
            Regions.Zelda.PalaceOfDarkness(self, self.Config),
            Regions.Zelda.SwampPalace(self, self.Config),
            Regions.Zelda.SkullWoods(self, self.Config),
            Regions.Zelda.ThievesTown(self, self.Config),
            Regions.Zelda.IcePalace(self, self.Config),
            Regions.Zelda.MiseryMire(self, self.Config),
            Regions.Zelda.TurtleRock(self, self.Config),
            Regions.Zelda.GanonsTower(self, self.Config),
            Regions.Zelda.LightWorld.DeathMountain.West(self, self.Config),
            Regions.Zelda.LightWorld.DeathMountain.East(self, self.Config),
            Regions.Zelda.LightWorld.NorthWest(self, self.Config),
            Regions.Zelda.LightWorld.NorthEast(self, self.Config),
            Regions.Zelda.LightWorld.South(self, self.Config),
            Regions.Zelda.HyruleCastle(self, self.Config),
            Regions.Zelda.DarkWorld.DeathMountain.West(self, self.Config),
            Regions.Zelda.DarkWorld.DeathMountain.East(self, self.Config),
            Regions.Zelda.DarkWorld.NorthWest(self, self.Config),
            Regions.Zelda.DarkWorld.NorthEast(self, self.Config),
            Regions.Zelda.DarkWorld.South(self, self.Config),
            Regions.Zelda.DarkWorld.Mire(self, self.Config),
            Regions.SuperMetroid.Crateria.Central(self, self.Config),
            Regions.SuperMetroid.Crateria.West(self, self.Config),
            Regions.SuperMetroid.Crateria.East(self, self.Config),
            Regions.SuperMetroid.Brinstar.Blue(self, self.Config),
            Regions.SuperMetroid.Brinstar.Green(self, self.Config),
            Regions.SuperMetroid.Brinstar.Kraid(self, self.Config),
            Regions.SuperMetroid.Brinstar.Pink(self, self.Config),
            Regions.SuperMetroid.Brinstar.Red(self, self.Config),
            Regions.SuperMetroid.Maridia.Outer(self, self.Config),
            Regions.SuperMetroid.Maridia.Inner(self, self.Config),
            Regions.SuperMetroid.NorfairUpper.West(self, self.Config),
            Regions.SuperMetroid.NorfairUpper.East(self, self.Config),
            Regions.SuperMetroid.NorfairUpper.Crocomire(self, self.Config),
            Regions.SuperMetroid.NorfairLower.West(self, self.Config),
            Regions.SuperMetroid.NorfairLower.East(self, self.Config),
            Regions.SuperMetroid.WreckedShip(self, self.Config)
        ]

        self.Locations = []
        for r in self.Regions:
            self.Locations.append(r.Locations)

        regionLookup = {r.Name:r for r in self.Regions}
        locationLookup = {l.Name:l for l in self.Locations}
        
        for region in self.Regions:
            region.GenerateLocationLookup()


    def CanEnter(self, regionName: str, items: Progression):
        region = self.regionLookup[regionName]
        if (region == None):
            raise Exception(f"World.CanEnter: Invalid region name {regionName}", f'{regionName=}'.partition('=')[0])
        return region.CanEnter(items)

    def CanAquire(self, items: Progression, reward: RewardType):
        return next(iter([region for region in self.Regions if isinstance(region, IReward) and region.Reward == reward])).CanComplete(items)

    def CanAquireAll(self, items: Progression, *rewards: RewardType):
        return all(region.CanComplete(items) for region in self.Regions if isinstance(region, IReward) and region.Reward in rewards)

    def Setup(self, rnd: random):
        self.SetMedallions(rnd)
        self.SetRewards(rnd)

    def SetMedallions(self, rnd: random):
        medallionMap = {0:ItemType.Bombos, 1: ItemType.Ether, 2:ItemType.Quake}
        regionList = [region for region in self.Regions if isinstance(region, IMedallionAccess)]
        for region in regionList:
            region.Medallion = medallionMap[rnd.randint(0, 2)]

    def SetRewards(self, rnd: random):
        rewards = [
            RewardType.PendantGreen, RewardType.PendantNonGreen, RewardType.PendantNonGreen, RewardType.CrystalRed, RewardType.CrystalRed,
            RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue
            ]
        rnd.shuffle(rewards)
        regionList = [region for region in self.Regions if isinstance(region, IReward) and region.Reward == RewardType.Null]
        for region in regionList:
            region.Reward = rewards[0]
            rewards.remove(region.Reward)

