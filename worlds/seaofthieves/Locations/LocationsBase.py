from .Locations import LocDetails, WebLocationCollection
import typing

from ..Items.ItemReqEvalAnd import ItemReqEvalAnd
from ..Items.ItemReqEvalOr import ItemReqEvalOr

class LocationsBase:

    descriptor: str = ""

    # def __init__(self):
    #     self.locations: typing.List[LocDetails] = []
    #
    # def getLocations(self):
    #     return self.locations
    #
    # def update_doRand(self, conditional: bool):
    #     self.doRand = conditional
    #
    # def addUniques(self, name: str, wlc: WebLocationCollection, doRand: bool):
    #     count = 1
    #     for wl in wlc:
    #         self.locations.append(LocDetails(name + ": " + str(count), WebLocationCollection([wl]), doRand))
    #         count += 1
    def __init__(self):
        self.locations = []

    def getLocations(self):
        return self.locations

    def addUniques(self, name: str, wlc, doRand: bool):
        count = 1
        for wl in wlc:
            if wl.name is not None:
                use_name = wl.name
            else:
                use_name = name + ": " + str(count)
            self.locations.append(LocDetails(use_name, WebLocationCollection([wl]), doRand))
            count += 1
