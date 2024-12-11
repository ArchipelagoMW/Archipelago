from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Location, Region
from .GameData import ItemType
from worlds.gstla.gen.LocationData import LocationData, all_locations as all_gen_locations, LocationType
from worlds.gstla.gen.LocationNames import loc_names_by_id

if TYPE_CHECKING:
    from .Items import GSTLAItem

def allow_djinn(_, item: 'GSTLAItem') -> bool:
    return item.item_data.type == ItemType.Djinn

class GSTLALocation(Location):
    game: str = "Golden Sun The Lost Age"
    location_data: LocationData
    item: 'GSTLAItem'

    def __init__(self, player: int, name: str, location: LocationData, region: Region):
        # Yes, calling str(name) because it's secretly an enum, and pickling does terrible things in MultiServer
        super(GSTLALocation, self).__init__(player, str(name), location.ap_id, region)
        self.location_data = location

    @staticmethod
    def create_djinn_location(player: int, name: str, location: LocationData, region: Region) -> 'GSTLALocation':
        ret = GSTLALocation(player, name, location, region)
        ret.always_allow = allow_djinn
        return ret

    @staticmethod
    def create_event_location(player: int, name: str, location: LocationData, region: Region):
        ret = GSTLALocation(player, name, location, region)
        ret.address = None
        return ret

def create_loctype_to_datamapping() -> Dict[LocationType, List[LocationData]]:
    """Creates a dictionary mapping LocationType to a list of all locations
    of that type
    """
    types: Dict[LocationType, List[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types


all_locations: List[LocationData] = all_gen_locations
location_name_to_id: Dict[str, LocationData] = {loc_names_by_id[location.ap_id]: location for location in all_locations}
location_type_to_data: Dict[LocationType, List[LocationData]] = create_loctype_to_datamapping()
