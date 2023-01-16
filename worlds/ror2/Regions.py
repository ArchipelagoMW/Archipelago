from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, RegionType, Entrance, CollectionState
from .Locations import orderedstage_location, location_table, RiskOfRainLocation


class RoRRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    # Default Locations
    non_dlc_regions: Dict[str, RoRRegionData] = {
        "Menu":                                 RoRRegionData(None, ["Distant Roost", "Distant Roost (2)", "Titanic Plains", "Titanic Plains (2)"]),
        "Distant Roost":                        RoRRegionData([], ["OrderedStage_1"]),
        "Distant Roost (2)":                    RoRRegionData([], ["OrderedStage_1"]),
        "Titanic Plains":                       RoRRegionData([], ["OrderedStage_1"]),
        "Titanic Plains (2)":                   RoRRegionData([], ["OrderedStage_1"]),
        "Abandoned Aqueduct":                   RoRRegionData([], ["OrderedStage_2"]),
        "Wetland Aspect":                       RoRRegionData([], ["OrderedStage_2"]),
        "Rallypoint Delta":                     RoRRegionData([], ["OrderedStage_3"]),
        "Scorched Acres":                       RoRRegionData([], ["OrderedStage_3"]),
        "Abyssal Depths":                       RoRRegionData([], ["OrderedStage_4"]),
        "Siren's Call":                         RoRRegionData([], ["OrderedStage_4"]),
        "Sundered Grove":                       RoRRegionData([], ["OrderedStage_4"]),
        "Sky Meadow":                           RoRRegionData([], ["Hidden Realm: Bulwark's Ambry", "OrderedStage_5"]),
    }
    # SOTV Regions
    dlc_regions: Dict[str, RoRRegionData] = {
        "Siphoned Forest":                      RoRRegionData([], ["OrderedStage_1"]),
        "Aphelian Sanctuary":                   RoRRegionData([], ["OrderedStage_2"]),
        "Sulfur Pools":                         RoRRegionData([], ["OrderedStage_3"])
    }
    other_regions: Dict[str, RoRRegionData] = {
        "Commencement":                         RoRRegionData(None, ["Victory"]),
        "OrderedStage_5":                       RoRRegionData(None, ["Hidden Realm: A Moment, Fractured", "Commencement"]),
        "OrderedStage_1":                       RoRRegionData(None, ["Hidden Realm: Bazaar Between Time",
                                                "Hidden Realm: Gilded Coast", "Abandoned Aqueduct", "Wetland Aspect"]),
        "OrderedStage_2":                       RoRRegionData(None, ["Rallypoint Delta", "Scorched Acres"]),
        "OrderedStage_3":                       RoRRegionData(None, ["Abyssal Depths", "Siren's Call", "Sundered Grove"]),
        "OrderedStage_4":                       RoRRegionData(None, ["Sky Meadow"]),
        "Hidden Realm: A Moment, Fractured":    RoRRegionData(None, ["Hidden Realm: A Moment, Whole", "Victory"]),
        "Hidden Realm: A Moment, Whole":        RoRRegionData(None, ["Victory"]),
        "Void Fields":                          RoRRegionData(None, []),
        "Victory":                              RoRRegionData(None, None),
        "Petrichor V":                          RoRRegionData(None, ["Victory"]),
        "Hidden Realm: Bulwark's Ambry":        RoRRegionData(None, ["Void Fields"]),
        "Hidden Realm: Bazaar Between Time":    RoRRegionData(None, None),
        "Hidden Realm: Gilded Coast":           RoRRegionData(None, None)
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
    all_location_regions = {**non_dlc_regions}
    if multiworld.dlc_sotv[player]:
        all_location_regions = {**non_dlc_regions, **dlc_regions}
    for key in all_location_regions:
        if key == "Menu":
            continue
        # Chests
        for i in range(0, chests):
            all_location_regions[key].locations.append(f"{key}: Chest {i + 1}")
        # Shrines
        for i in range(0, shrines):
            all_location_regions[key].locations.append(f"{key}: Shrine {i + 1}")
        # Scavengers
        if scavengers > 0:
            for i in range(0, scavengers):
                all_location_regions[key].locations.append(f"{key}: Scavenger {i + 1}")
        # Radio Scanners
        if scanners > 0:
            for i in range(0, scanners):
                all_location_regions[key].locations.append(f"{key}: Radio Scanner {i + 1}")
        # Newt Altars
        if newt > 0:
            for i in range(0, newt):
                all_location_regions[key].locations.append(f"{key}: Newt Altar {i + 1}")
    regions_pool: Dict = {**all_location_regions, **other_regions}
    # DLC Locations
    if multiworld.dlc_sotv[player]:
        non_dlc_regions["Menu"].region_exits.append("Siphoned Forest")
        other_regions["OrderedStage_2"].region_exits.append("Aphelian Sanctuary")
        other_regions["OrderedStage_3"].region_exits.append("Sulfur Pools")
        other_regions["Commencement"].region_exits.append("The Planetarium")
        other_regions["Void Fields"].region_exits.append("Void Locus")
        # for key in dlc_regions:
        #     # DLC Chests
        #     for i in range(0, chests):
        #         dlc_regions[key].locations.append(f"{key}: Chest {i + 1}")
        #     # DLC Shrines
        #     for i in range(0, shrines):
        #         dlc_regions[key].locations.append(f"{key}: Shrine {i + 1}")
        #     # DLC Scavengers
        #     if scavengers > 0:
        #         for i in range(0, scavengers):
        #             dlc_regions[key].locations.append(f"{key}: Scavenger {i + 1}")
        #     # DLC Radio Scanners
        #     if scanners > 0:
        #         for i in range(0, scanners):
        #             dlc_regions[key].locations.append(f"{key}: Radio Scanner {i + 1}")
        #     # DLC Newt Altars
        #     if newt > 0:
        #         for i in range(0, newt):
        #             dlc_regions[key].locations.append(f"{key}: Newt Altar {i + 1}")
        if multiworld.dlc_sotv[player]:
            regions_pool: Dict = {**all_location_regions, **other_regions, **dlc_other_regions}
    # Create all the regions
    for name, data in regions_pool.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))
    # Connect all the regions to their exits
    for name, data in regions_pool.items():
        create_connections_in_regions(multiworld, player, name, data)
    # multiworld.get_entrance("Distant Roost", player).connect(multiworld.get_region("Distant Roost", player))
    # multiworld.get_entrance("Distant Roost (2)", player).connect(multiworld.get_region("Distant Roost (2)", player))
    # multiworld.get_entrance("Titanic Plains", player).connect(multiworld.get_region("Titanic Plains", player))
    # multiworld.get_entrance("Titanic Plains (2)", player).connect(multiworld.get_region("Titanic Plains (2)", player))
    # multiworld.get_entrance("Abandoned Aqueduct", player).connect(multiworld.get_region("Abandoned Aqueduct", player))
    # multiworld.get_entrance("Wetland Aspect", player).connect(multiworld.get_region("Wetland Aspect", player))
    # multiworld.get_entrance("Rallypoint Delta", player).connect(multiworld.get_region("Rallypoint Delta", player))
    # multiworld.get_entrance("Scorched Acres", player).connect(multiworld.get_region("Scorched Acres", player))
    # multiworld.get_entrance("Abyssal Depths", player).connect(multiworld.get_region("Abyssal Depths", player))
    # multiworld.get_entrance("Siren's Call", player).connect(multiworld.get_region("Siren's Call", player))
    # multiworld.get_entrance("Sundered Grove", player).connect(multiworld.get_region("Sundered Grove", player))
    # multiworld.get_entrance("Sky Meadow", player).connect(multiworld.get_region("Sky Meadow", player))
    # if multiworld.dlc_sotv[player]:
    #     multiworld.get_entrance("Siphoned Forest", player).connect(multiworld.get_region("Siphoned Forest", player))
    #     multiworld.get_entrance("Aphelian Sanctuary", player).connect(multiworld.get_region("Aphelian Sanctuary", player))
    #     multiworld.get_entrance("Sulfur Pools", player).connect(multiworld.get_region("Sulfur Pools", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: RoRRegionData):
    region = Region(name, RegionType.Generic, name, player, multiworld)
    if data.locations:
        for location_name in data.locations:
            location_data = location_table.get(location_name)
            location = RiskOfRainLocation(player, location_name, location_data, region)
            region.locations.append(location)

    return region


def create_connections_in_regions(multiworld: MultiWorld, player: int, name: str, data: RoRRegionData):
    # menu
    region = multiworld.get_region(name, player)
    # menu entrance
    entrance = Entrance(player, name, region)
    # entrance.access_rule = lambda state: state.has(name)
    # entrance.connect(region, name, player)
    # if not multiworld.get_region(name, player).entrances:
    #     entrance.connect(region, name, player)
    if data.region_exits:
        for region_exit in data.region_exits:
            # Distant Roost Entrance
            # has_item(player, r_exit, name)
            # Menu -> Distant Roost
            r_exit_stage = Entrance(player, region_exit, region)
            # Distant Roost Region
            exit_region = multiworld.get_region(region_exit, player)
            r_exit_stage.connect(exit_region)
            # entrance.connect(region, r_exit_stage, player)
            # if name == "Menu":
            #     print("Menu")
            # else:
            #     r_exit.connect(region)
            region.exits.append(r_exit_stage)
# create regions in a for loop
# use created regions to add connections
# Menu will search for all regions in its exit and connect them
# Have a entrance... Menu
# Have a exit event... OrderedStage_1
#
