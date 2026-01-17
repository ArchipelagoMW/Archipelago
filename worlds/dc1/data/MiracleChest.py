from BaseClasses import LocationProgressType, Region
from .. import DarkCloudLocation, Rules


class MiracleChest:
    name = ""
    ap_id = 0
    town_id = 0
    req_char = None
    req_geo = None

    def __init__(self, name, ap_id, town_id, req_char, req_geo):
        self.name = name
        self.ap_id = ap_id
        self.town_id = town_id
        if req_char != "":
            self.req_char = req_char
        if req_geo != "":
            self.req_geo = req_geo.split("&")

    def to_location(self, player: int, town: Region) -> DarkCloudLocation:
        loc = DarkCloudLocation(player, self.name, self.ap_id, LocationProgressType.DEFAULT, town)
        loc.access_rule = lambda state: Rules.chest_test(state, player, self.req_char, self.req_geo)
        return loc
