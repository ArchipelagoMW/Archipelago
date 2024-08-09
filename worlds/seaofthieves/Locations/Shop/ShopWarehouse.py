import typing

from .ShopLocationList import ShopLocationList
from .ShopLocation import ShopLocation
from ..Locations import LocDetails

class ShopWarehouse:

    def __init__(self):
        self.name_to_group: typing.Dict[str, ShopLocationList] = {}

    def add_group(self, group: ShopLocationList):
        self.name_to_group[group.name] = group

    def add_location(self, loc: ShopLocation):
        split_word: str = "Shop"
        group_name: str = "{}{}".format(loc.locDetails.name.partition(split_word)[0], split_word)

        if group_name not in self.name_to_group.keys():
            self.name_to_group[group_name] = ShopLocationList(group_name)

        self.name_to_group[group_name].add(loc)

    def remove_non_pickle_members(self):
        for group in self.name_to_group.keys():
            self.name_to_group[group].remove_non_pickle_members()