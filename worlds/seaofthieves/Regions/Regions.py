import copy
import typing

from BaseClasses import MultiWorld, Region, Entrance
from worlds.seaofthieves.Locations.Locations import *
from ..Locations.LocationCollection import LocationDetailsCollection
from ...generic.Rules import add_rule, exclusion_rules
from ..Items.Items import Items
from ..Configurations import SotOptionsDerived
import typing
from worlds.seaofthieves.Regions.RegionDetails import RegionDetails, Regions
from worlds.seaofthieves.Regions.ConnectionDetails import ConnectionDetails


class SOTRegion(Region):
    subregions: typing.List[Region] = []

    def __init__(self, regionName: str, player: int, world, hint: typing.Optional[str] = None):
        super().__init__(regionName, player, world, hint)


class RegionAdder:

    def __init__(self, player: int, locationDetailsCollection: LocationDetailsCollection,
                 options: SotOptionsDerived.SotOptionsDerived):
        self.player = player

        self.locationDetailsCollection = locationDetailsCollection
        self.options: SotOptionsDerived.SotOptionsDerived = options

        self.__added_regions: typing.List[SOTRegion] = list()
        pass

    def addRulesForLocationsInRegions(self, world: MultiWorld):
        player = self.player

        temp = world.get_locations(self.player)
        for lll in temp:

            # for some reason, get_location needs to be called and we cant use the return of get_locations
            LOC = world.get_location(lll.name, player)
            locDetails = LOC.locDetails

            if not locDetails.doRandomize:
                exclusion_rules(world, self.player, {LOC.name})
            else:
                locDetails.setLambda(LOC, player)

    def add(self, region_details: RegionDetails, world: MultiWorld):
        sotRegion = SOTRegion(region_details.name, self.player, world)
        world.regions.append(sotRegion)
        self.__added_regions.append(sotRegion)

    def link_regions_and_locations(self):
        for region in self.__added_regions:
            locations: typing.List[SOTLocation] = self.locationDetailsCollection.getLocationsForRegion(region.name,
                                                                                                       self.player)
            for loc in locations:
                loc.parent_region = region
            region.locations.extend(locations)


    def connect(self, world: MultiWorld, source: str, target: str, rule=None) -> None:
        sourceRegion = world.get_region(source, self.player)
        targetRegion = world.get_region(target, self.player)

        sourceRegion.connect(targetRegion, rule=rule)

    def connect2(self, world: MultiWorld, source: str, target: str, rule=None) -> None:
        self.connect(world, source, target, rule)
        self.connect(world, target, source, rule)

    def connectFromDetails2(self, world: MultiWorld, details: ConnectionDetails):
        self.connect(world, details.start.name, details.end.name, details.lamb(self.player))
        self.connect(world, details.end.name, details.start.name, details.lamb(self.player))


# REG_NAME_EM_RB_VOYAGE = "Seas of Bones"

def create_regions(world: MultiWorld, options: SotOptionsDerived.SotOptionsDerived, player: int,
                   locationDetailsCollection: LocationDetailsCollection) -> RegionAdder:
    region_adder = RegionAdder(player, locationDetailsCollection, options)

    for region_detail in Regions.__dict__.items():
        if region_detail[0].startswith("R_"):
            region_adder.add(region_detail[1], world)

    return region_adder
