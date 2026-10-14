from typing import Dict, List, NamedTuple, Optional, Set, Tuple
from BaseClasses import Location
from . import Data


class KH1Location(Location):
    game: str = "Kingdom Hearts"


class KH1LocationData(NamedTuple):
    region: str
    code: Optional[int] = None
    groups: Tuple[str, ...] = ()


def get_locations_by_group(group: str) -> Dict[str, KH1LocationData]:
    return {name: data for name, data in location_table.items() if group in data.groups}


def build_location_table(rows: List[Dict[str, str]]) -> Dict[str, KH1LocationData]:
    table: Dict[str, KH1LocationData] = {}
    for row in rows:
        table[row["name"]] = KH1LocationData(
            row["region"],
            code=int(row["id"]) if row["id"] else None,
            groups=tuple(row["groups"].split(";")) if row["groups"] else (),
        )
    return table


def build_location_name_groups(table: Dict[str, KH1LocationData]) -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}
    for name, location in table.items():
        for group in (location.region, *location.groups):
            groups.setdefault(group, set()).add(name)
    return groups


location_table: Dict[str, KH1LocationData] = build_location_table(Data.locations)
event_location_table: Dict[str, KH1LocationData] = build_location_table(Data.event_locations)
location_name_groups: Dict[str, Set[str]] = build_location_name_groups(location_table)
lookup_id_to_name: Dict[int, str] = {data.code: name for name, data in location_table.items() if data.code}
