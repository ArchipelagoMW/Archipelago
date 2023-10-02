from enum import Enum
from typing import List, Callable
from .Item import Progression
from . import Region
from . import World

class LocationType(Enum):
    Regular = 0
    HeraStandingKey = 1
    Pedestal = 2
    Ether = 3
    Bombos = 4
    NotInDungeon = 5

    Visible = 6
    Chozo = 7
    Hidden = 8

# delegate bool Requirement(Progression items);
# delegate bool Verification(Item item, Progression items);

class Location:
    Id: int
    Name: str
    Type: LocationType
    Address: int
    Region: Region

    def Weight(self): return self.weight if self.weight != None else self.Region.Weight

    canAccess: Callable = lambda items: True
    alwaysAllow: Callable = lambda item, items: True
    allow: Callable = lambda item, items: True
    weight: int

    def ItemIs(self, type, world: World): 
        item = self.APLocation.item.item if self.APLocation.item is not None and self.APLocation.item.game == "SMZ3" else None
        return item.Is(type, world) if item != None else False
    def ItemIsNot(self, type, world: World): return not self.ItemIs(type, world)

    def __init__(self, region: Region, id: int, address: int, type: LocationType, name: str, access: Callable = lambda items : True):
        self.Region = region
        self.Id = id
        self.Name = name
        self.Type = type
        self.Item = None
        self.Address = address
        self.canAccess = access
        self.alwaysAllow = lambda item, items: False
        self.allow = lambda item, items: True

    def Weighted(self, weight: int):
        self.weight = weight
        return self

    def AlwaysAllow(self, allow: Callable):
        self.alwaysAllow = allow
        return self

    def Allow(self, allow: Callable):
        self.allow = allow
        return self

    def Available(self, items: Progression):
        return self.Region.CanEnter(items) and self.canAccess(items)

    def CanFill(self, item, items: Progression):
        oldItem = self.Item
        self.Item = item
        fillable = self.alwaysAllow(item, items) or (self.Region.CanFill(item) and self.allow(item, items) and self.Available(items))
        self.Item = oldItem
        return fillable

    @staticmethod
    def Get(locations, name: str):
        loc = next((l for l in locations if l.Name == name), None)
        if (loc == None):
            raise Exception(f"Could not find location name {name}")
        return loc

    @staticmethod
    def Empty(locations):
        return [l for l in locations if l.Item == None]

    @staticmethod
    def Filled(locations):
        return [l for l in locations if l.Item != None]

    @staticmethod
    def AvailableWithinWorld(locations, items):
        result = []
        worldList = []
        [worldList.append(l.Region.World) for l in locations if l.Region.World not in worldList]
        for world in worldList:
            result += Location.AvailableGlobal([l for l in locations if l.Region.World == world], [i for i in items if i.World == world])
        return result  

    @staticmethod
    def AvailableGlobal(locations, items):
        progression = Progression(items)
        return [l for l in locations if l.Available(progression)]

    @staticmethod
    def CanFillWithinWorld(locations, item, items):
        itemWorldProgression = Progression([i for i in items if i.World == item.World].append(item))
        worldList = []
        [worldList.append(l.Region.World) for l in locations if l.Region.World not in worldList]
        worldProgression = {world.Id : Progression([i for i in items if i.World == world]) for world in worldList}
        return [l for l in locations if l.CanFill(item, worldProgression[l.Region.World.Id] and next(ll for ll in item.World.Locations if ll.Id == l.Id).Available(itemWorldProgression))]

# Start of AP integration
locations_start_id = 85000