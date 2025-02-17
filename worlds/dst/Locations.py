from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Location

from .Constants import DSTAP_LOCATIONS, LOCATION_ID_OFFSET, LOCATION_DAY_OFFSET

class DSTLocation(Location):
    game: str = "Don't Starve Together"

class DSTLocationData(NamedTuple):
    address: Optional[int] = None
    tags: Set[str] = set()
    name: str = ""

def generate_location_data() -> Dict[str, DSTLocationData]:
    ret: Dict[str, DSTLocationData] = {}
    # Add normal locations from table
    for v in DSTAP_LOCATIONS:
        address:int = v[0] + LOCATION_ID_OFFSET
        name:str = v[1]
        tags:Set = set(v[3])

        if "nonwinter" in tags:
            tags.update(["autumn", "spring", "summer"])
        if "nonspring" in tags:
            tags.update(["autumn", "winter", "summer"])
        if "nonsummer" in tags:
            tags.update(["autumn", "winter", "spring"])

        ret.setdefault(name, DSTLocationData(address, tags, name))
    # Add dynamic locations - Experimental; Will probably won't keep at all
    # for i in range(1, 100):
    #    name:str = f"Survive {i} Days"
    #    ret.setdefault(name, DSTLocationData(i+LOCATION_DAY_OFFSET, set(["survivedays"]), name))
    return ret

location_data_table: Dict[str, DSTLocationData] = generate_location_data()
location_name_to_id = {name: data.address for name, data in location_data_table.items() if data.address is not None}