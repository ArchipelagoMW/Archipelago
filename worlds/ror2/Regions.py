from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, RegionType, Entrance
from .Locations import orderedstage_location

class RoRRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    # Default Locations
    non_dlc_regions: Dict[str, RoRRegionData] = {
        "Menu":                                 RoRRegionData(None, ["Distant Roost","Distant Roost (2)", "Titanic Plains" "Titanic Plains (2)"]),
        "Distant Roost":                        RoRRegionData([], ["Abandoned Aqueduct", "Wetland Aspect"]),
        "Distant Roost (2)":                    RoRRegionData([], ["Abandoned Aqueduct", "Wetland Aspect"]),
        "Titanic Plains":                       RoRRegionData([], ["Abandoned Aqueduct", "Wetland Aspect"]),
        "Titanic Plains (2)":                   RoRRegionData([], ["Abandoned Aqueduct", "Wetland Aspect"]),
        "Abandoned Aqueduct":                   RoRRegionData([], ["Rallypoint Delta", "Scorched Acres"]),
        "Wetland Aspect":                       RoRRegionData([], ["Rallypoint Delta", "Scorched Acres"]),
        "Rallypoint Delta":                     RoRRegionData([], ["Abyssal Depths", "Siren's Call", "Sundered Grove"]),
        "Scorched Acres":                       RoRRegionData([], ["Abyssal Depths", "Siren's Call", "Sundered Grove"]),
        "Abyssal Depths":                       RoRRegionData([], ["Sky Meadow"]),
        "Siren's Call":                         RoRRegionData([], ["Sky Meadow"]),
        "Sundered Grove":                       RoRRegionData([], ["Sky Meadow"]),
        "Sky Meadow":                           RoRRegionData([], ["Commencement", "Hidden Realm: Bulwark's Ambry"]),
    }
    # SOTV Regions
    dlc_regions: Dict[str, RoRRegionData] = {
        "Siphoned Forest":                      RoRRegionData([], ["Abandoned Aqueduct", "Wetland Aspect", "Aphelian Sanctuary"]),
        "Aphelian Sanctuary":                   RoRRegionData([], ["Rallypoint Delta", "Scorched Acres", "Sulfur Pools"]),
        "Sulfur Pools":                         RoRRegionData([], ["Abyssal Depths", "Siren's Call", "Sundered Grove"])
    }
    other_regions: Dict[str, RoRRegionData] = {
        "Commencement":                         RoRRegionData(None, ["Victory"]),
        "OrderedStage_5":                       RoRRegionData(None, ["Hidden Realm: A Moment, Fractured"]),
        "OrderedStage_1":                       RoRRegionData(None, ["Hidden Realm: Bazzar Between Time", "Hidden Realm: Gilded Coast"]),
        "Hidden Realm: A Moment, Fractured":    RoRRegionData(None, ["Hidden Realm: A Moment, Whole", "Victory"]),
        "Hidden Realm: A Moment, Whole":        RoRRegionData(None, ["Victory"]),
        "Void Fields":                          RoRRegionData(None, []),
    }
    dlc_other_regions: Dict[str, RoRRegionData] = {
        "The Planetarium": RoRRegionData(None, ["Victory"]),
        "Void Locus": RoRRegionData(None, ["The Planetarium"])
    }
    # Totals of each item
    chests = int(multiworld.chests_per_stage[player])
    shrines = int(multiworld.shrines_per_stage[player])
    scavengers = int(multiworld.scavengers_per_stage[player])
    scanners = int(multiworld.scanner_per_stage[player])
    newt = int(multiworld.altars_per_stage[player])
    for key in non_dlc_regions:
        if key == "Menu":
            continue
        # Chests
        for i in range(0, chests):
            non_dlc_regions[key].locations.append(f"{key}: Chest {i + 1}")
        # Shrines
        for i in range(0, shrines):
            non_dlc_regions[key].locations.append(f"{key}: Shrine {i + 1}")
        # Scavengers
        if scavengers > 0:
            for i in range(0, scavengers):
                non_dlc_regions[key].locations.append(f"{key}: Scavenger {i + 1}")
        # Radio Scanners
        if scanners > 0:
            for i in range(0, scanners):
                non_dlc_regions[key].locations.append(f"{key}: Radio Scanner {i + 1}")
        # Newt Altars
        if newt > 0:
            for i in range(0, newt):
                non_dlc_regions[key].locations.append(f"{key}: Newt Altar {i + 1}")
    regions_pool: Dict = {**non_dlc_regions, **other_regions}
    # DLC Locations
    if multiworld.dlc_sotv[player]:
        non_dlc_regions["Menu"].region_exits.append("Siphoned Forest")
        non_dlc_regions["Distant Roost"].region_exits.append("Aphelian Sanctuary")
        non_dlc_regions["Distant Roost (2)"].region_exits.append("Aphelian Sanctuary")
        non_dlc_regions["Titanic Plains"].region_exits.append("Aphelian Sanctuary")
        non_dlc_regions["Titanic Plains (2)"].region_exits.append("Aphelian Sanctuary")
        non_dlc_regions["Abandoned Aqueduct"].region_exits.append("Sulfur Pools")
        non_dlc_regions["Wetland Aspect"].region_exits.append("Sulfur Pools")
        other_regions["Commencement"].region_exits.append("The Planetarium")
        other_regions["Void Fields"].region_exits.append("Void Locus")
        for key in dlc_regions:
            # DLC Chests
            for i in range(0, chests):
                dlc_regions[key].locations.append(f"{key}: Chest {i + 1}")
            # DLC Shrines
            for i in range(0, shrines):
                dlc_regions[key].locations.append(f"{key}: Shrine {i + 1}")
            # DLC Scavengers
            if scavengers > 0:
                for i in range(0, scavengers):
                    dlc_regions[key].locations.append(f"{key}: Scavenger {i + 1}")
            # DLC Radio Scanners
            if scanners > 0:
                for i in range(0, scanners):
                    dlc_regions[key].locations.append(f"{key}: Radio Scanner {i + 1}")
            # DLC Newt Altars
            if newt > 0:
                for i in range(0, newt):
                    dlc_regions[key].locations.append(f"{key}: Newt Altar {i + 1}")
            regions_pool: Dict = {**non_dlc_regions, **dlc_regions, **other_regions, **dlc_other_regions}
    for name, data in non_dlc_regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))


def create_region(multiworld: MultiWorld, player: int, name: str, data: RoRRegionData):
    region = Region(name, RegionType.Generic, name, player, multiworld)
    # if data.locations:
        # for location_name in data.locations:

    print(region)
    return region
