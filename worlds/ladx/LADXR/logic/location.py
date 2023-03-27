import typing
from .requirements import hasConsumableRequirement, OR
from ..locations.itemInfo import ItemInfo

from enum import Enum

class LocationType(Enum):
    Unknown = 0
    Overworld = 1
    Dungeon = 2
    Indoor = 3

class Location:
    def __init__(self, name=None, location_type=LocationType.Unknown, dungeon=None):
        self.name = name
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        if self.dungeon != None:
            assert location_type == location_type.Unknown or location_type == LocationType.Dungeon
            location_type = LocationType.Dungeon
        
        self.location_type = location_type 
        self.__connected_to = set()
        self.simple_connections = []
        self.gated_connections = []

    def add(self, *item_infos):
        if not self.name:
            meta = item_infos[0].metadata
            self.name = f"{meta.name} ({meta.area})"
            
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, other, req, *, one_way=False):
        assert isinstance(other, Location), type(other)

        if isinstance(req, bool):
            if req:
                self.connect(other, None, one_way=one_way)
            return

        if other in self.__connected_to:
            for idx, data in enumerate(self.gated_connections):
                if data[0] == other:
                    if req is None or data[1] is None:
                        self.gated_connections[idx] = (other, None)
                    else:
                        self.gated_connections[idx] = (other, OR(req, data[1]))
                    break
            for idx, data in enumerate(self.simple_connections):
                if data[0] == other:
                    if req is None or data[1] is None:
                        self.simple_connections[idx] = (other, None)
                    else:
                        self.simple_connections[idx] = (other, OR(req, data[1]))
                    break
        else:
            self.__connected_to.add(other)

            if hasConsumableRequirement(req):
                self.gated_connections.append((other, req))
            else:
                self.simple_connections.append((other, req))
        if not one_way:
            other.connect(self, req, one_way=True)
        return self

    def __repr__(self):
        return "<%s:%s:%d:%d:%d>" % (self.__class__.__name__, self.dungeon, len(self.items), len(self.simple_connections), len(self.gated_connections))

class OverworldLocation(Location):
    def __init__(self, name=None):
        assert(name)
        Location.__init__(self, name, location_type=LocationType.Overworld)

        
class IndoorLocation(Location):
    def __init__(self, name):
        assert(name)
        Location.__init__(self, name, location_type=LocationType.Indoor)

class VirtualLocation(Location):
    pass