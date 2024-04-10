from typing import Dict, NamedTuple, Optional, FrozenSet

from BaseClasses import Location

from .Constants import DSTAP_LOCATIONS, LOCATION_ID_OFFSET

class DSTLocation(Location):
   game: str = "Don't Starve Together"

class DSTLocationData(NamedTuple):
   address: Optional[int] = None
   tags: FrozenSet[str] = frozenset()
   name: str = ""

def generate_location_data() -> Dict[str, DSTLocationData]:
   ret: Dict[str, DSTLocationData] = {}
   for v in DSTAP_LOCATIONS:
      address:int = v[0] + LOCATION_ID_OFFSET
      name:str = v[1]
      tags:FrozenSet = frozenset(v[3])
      ret.setdefault(name, DSTLocationData(address, tags, name))
   return ret

location_data_table: Dict[str, DSTLocationData] = generate_location_data()
location_name_to_id = {name: data.address for name, data in location_data_table.items() if data.address is not None}