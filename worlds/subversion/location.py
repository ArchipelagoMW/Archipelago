from typing import Optional

from BaseClasses import Location, Region
from .config import base_id

from subversion_rando.location_data import Location as SvLocation, new_locations

location_data = new_locations()

id_to_name = {
    loc["plmparamlo"] + base_id: loc_name
    for loc_name, loc in location_data.items()
}

name_to_id = {
    n: id_
    for id_, n in id_to_name.items()
}

fallen_locs = {
    loc["alternateplmparamlo"]: loc["plmparamlo"]
    for loc in location_data.values()
    if loc["alternateplmparamlo"]
}
"""
fallen location id from rom (that AP doesn't know)
to location id that AP knows about
"""


class SubversionLocation(Location):
    game = "Subversion"
    sv_loc: SvLocation

    def __init__(self,
                 player: int,
                 name: str,
                 parent: Optional[Region] = None) -> None:
        loc_id = name_to_id[name]
        super().__init__(player, name, loc_id, parent)
        self.sv_loc = location_data[name]
