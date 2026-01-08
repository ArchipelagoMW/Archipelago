from copy import deepcopy
import csv
import logging
import pathlib
import pkgutil
from typing import Optional, TypedDict, Union, cast

from .item_data import Item


# other unused columns in Location:
# "roomid", "area", "xy","plmtypename","state","roomname","alternateroomid"
class Location(TypedDict):
    fullitemname: str
    locids: list[int]
    plmtypeid: int
    plmparamhi: int
    plmparamlo: int
    hiddenness: str
    alternateroomlocids: list[int]
    alternateroomdifferenthiddenness: str
    alternateplmparamlo: Optional[int]
    inlogic: bool
    item: Optional[Item]


def get_location_ids(loc: Location) -> list[int]:
    sv_loc_ids = [loc["plmparamlo"]]
    alt_id = loc["alternateplmparamlo"]
    if alt_id:
        # There is a plmparamlo 0, but none of the alternates are 0
        # so we can say `if loc['alternateplmparamlo']`
        sv_loc_ids.append(alt_id)
    return sv_loc_ids


spacePortLocs = ["Ready Room",
                 "Torpedo Bay",
                 "Extract Storage",
                 "Gantry",
                 "Docking Port 4",
                 "Docking Port 3",
                 "Weapon Locker",
                 "Aft Battery",
                 "Forward Battery"]


majorLocs = frozenset([
    "Ocean Vent Supply Depot",
    "Sandy Cache",
    "Shrine Of The Penumbra",
    "Subterranean Burrow",
    "Archives: Front",
    "Arena",
    "Grand Vault",
    "Harmonic Growth Enhancer",
    "West Spore Field",
    "Electromechanical Engine",
    "Fire's Bane Shrine",
    "Greater Inferno",
    "Magma Chamber",
    "Antelier",
    "Chamber Of Wind",
    "Crocomire's Lair",
    "Equipment Locker",
    "Weapon Research",
    "Armory Cache 2",
    "Syzygy Observatorium",
    "Shrine Of The Animate Spark",
    "Extract Storage",
    "Torpedo Bay",
])

eTankLocs = frozenset([
    "Sandy Burrow: Top",
    "Sediment Flow",
    "Epiphreatic Crag",
    "Mezzanine Concourse",
    "Sensor Maintenance: Top",
    "Trophobiotic Chamber",
    "Vulnar Caves Entrance",
    "Warrior Shrine: Middle",
    "Depressurization Valve",
    "Gymnasium",
    "Mining Cache",
    "Containment Area",
    "Water Garden",
    "Reliquary Access",
    "Summit Landing",
    "Ready Room"
])


def _pullCSV() -> dict[str, Location]:
    locations: dict[str, Location] = {}

    def comment_filter(line: str) -> bool:
        return (line[0] != '#')

    csv_bytes = pkgutil.get_data("subversion_rando", "subversiondata12.csv")
    if csv_bytes is None:
        logging.warning("`pkgutil.get_data` unable to read location data")
        # if pkgutil is unable to find it, try reading from file system
        path = pathlib.Path(__file__).parent.resolve()
        with open(path.joinpath('subversiondata12.csv'), 'r') as file:
            csv_lines = file.readlines()
    else:
        csv_lines = csv_bytes.decode().splitlines()

    reader = csv.DictReader(filter(comment_filter, csv_lines))
    for row in reader:
        # commas within fields -> array
        row['locids'] = row['locids'].split(',')
        row['alternateroomlocids'] = row['alternateroomlocids'].split(',')
        # hex fields we want to use -> int
        row['locids'] = [int(locstr, 16) for locstr in row['locids'] if locstr != '']
        row['alternateroomlocids'] = [
            int(locstr, 16) for locstr in row['alternateroomlocids'] if locstr != '']
        row['plmtypeid'] = int(row['plmtypeid'], 16)
        row['plmparamhi'] = int(row['plmparamhi'], 16)
        row['plmparamlo'] = int(row['plmparamlo'], 16)
        if len(row['alternateplmparamlo']):
            row['alternateplmparamlo'] = int(row['alternateplmparamlo'], 16)
        else:
            # There is a plmparamlo 0, but none of the alternates are 0
            # so we can say `if loc['alternateplmparamlo']`
            row['alternateplmparamlo'] = None
        # new key: 'inlogic'
        row['inlogic'] = False
        # the item that we place in this location
        row["item"] = None
        locations[row['fullitemname']] = cast(Location, row)
    return locations


_location_cache: Union[dict[str, Location], None] = None


def new_locations() -> dict[str, Location]:
    """ creates a new collection of `Location`s """
    global _location_cache
    if _location_cache is None:
        _location_cache = _pullCSV()

    return deepcopy(_location_cache)
