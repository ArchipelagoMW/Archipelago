import copy
import typing
from ..Locations import LocDetails
from .ShopLocation import ShopLocation

class ShopLocationList():

    def __init__(self, name: str, shop_locations: typing.Optional[typing.List[LocDetails]] = None):
        self.name: str = name
        self.shop_locations: typing.List[ShopLocation] = list() if shop_locations is None else shop_locations
        self.shop_locations_temp: typing.List[ShopLocation] = list()


    def add(self, loc: ShopLocation):
        self.shop_locations_temp.append(loc)
        l = copy.deepcopy(loc)
        self.shop_locations.append(l)


    def display_text(self) -> str:
        txt: str = ""
        line: int = 1
        for loc in self.shop_locations:
            txt += "[{}] {}\n".format(line, loc.display_text())
        return txt

    def remove_non_pickle_members(self):
        for i in range(len(self.shop_locations_temp)):
            self.shop_locations[i].item_name_override = self.shop_locations_temp[i].item.name
        self.shop_locations_temp.clear()
