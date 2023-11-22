from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Region, Entrance, MultiWorld
from .locations import location_table, RiskOfRainLocation, get_classic_item_pickups

if TYPE_CHECKING:
    from . import RiskOfRainWorld


class RoRRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_explore_regions(ror2_world: "RiskOfRainWorld") -> None:
    player = ror2_world.player
    ror2_options = ror2_world.options
    multiworld = ror2_world.multiworld
    # Default Locations
    non_dlc_regions: Dict[str, RoRRegionData] = {
        "Menu":                                 RoRRegionData(None, ["Distant Roost", "Distant Roost (2)",
                                                                     "Titanic Plains", "Titanic Plains (2)"]),
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
        "Commencement":                         RoRRegionData(None, ["Victory", "Petrichor V"]),
        "OrderedStage_5":                       RoRRegionData(None, ["Hidden Realm: A Moment, Fractured",
                                                                     "Commencement"]),
        "OrderedStage_1":                       RoRRegionData(None, ["Hidden Realm: Bazaar Between Time",
                                                                     "Hidden Realm: Gilded Coast", "Abandoned Aqueduct",
                                                                     "Wetland Aspect"]),
        "OrderedStage_2":                       RoRRegionData(None, ["Rallypoint Delta", "Scorched Acres"]),
        "OrderedStage_3":                       RoRRegionData(None, ["Abyssal Depths", "Siren's Call",
                                                                     "Sundered Grove"]),
        "OrderedStage_4":                       RoRRegionData(None, ["Sky Meadow"]),
        "Hidden Realm: A Moment, Fractured":    RoRRegionData(None, ["Hidden Realm: A Moment, Whole"]),
        "Hidden Realm: A Moment, Whole":        RoRRegionData(None, ["Victory", "Petrichor V"]),
        "Void Fields":                          RoRRegionData(None, []),
        "Victory":                              RoRRegionData(None, None),
        "Petrichor V":                          RoRRegionData(None, []),
        "Hidden Realm: Bulwark's Ambry":        RoRRegionData(None, None),
        "Hidden Realm: Bazaar Between Time":    RoRRegionData(None, ["Void Fields"]),
        "Hidden Realm: Gilded Coast":           RoRRegionData(None, None)
    }
    dlc_other_regions: Dict[str, RoRRegionData] = {
        "The Planetarium":                      RoRRegionData(None, ["Victory", "Petrichor V"]),
        "Void Locus":                           RoRRegionData(None, ["The Planetarium"])
    }
    # Totals of each item
    chests = int(ror2_options.chests_per_stage)
    shrines = int(ror2_options.shrines_per_stage)
    scavengers = int(ror2_options.scavengers_per_stage)
    scanners = int(ror2_options.scanner_per_stage)
    newt = int(ror2_options.altars_per_stage)
    all_location_regions = {**non_dlc_regions}
    if ror2_options.dlc_sotv:
        all_location_regions = {**non_dlc_regions, **dlc_regions}

    # Locations
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
    if ror2_options.dlc_sotv:
        non_dlc_regions["Menu"].region_exits.append("Siphoned Forest")
        other_regions["OrderedStage_1"].region_exits.append("Aphelian Sanctuary")
        other_regions["OrderedStage_2"].region_exits.append("Sulfur Pools")
        other_regions["Void Fields"].region_exits.append("Void Locus")
        other_regions["Commencement"].region_exits.append("The Planetarium")
        regions_pool: Dict = {**all_location_regions, **other_regions, **dlc_other_regions}

    # Check to see if Victory needs to be removed from regions
    if ror2_options.victory == "mithrix":
        other_regions["Hidden Realm: A Moment, Whole"].region_exits.pop(0)
        dlc_other_regions["The Planetarium"].region_exits.pop(0)
    elif ror2_options.victory == "voidling":
        other_regions["Commencement"].region_exits.pop(0)
        other_regions["Hidden Realm: A Moment, Whole"].region_exits.pop(0)
    elif ror2_options.victory == "limbo":
        other_regions["Commencement"].region_exits.pop(0)
        dlc_other_regions["The Planetarium"].region_exits.pop(0)

    # Create all the regions
    for name, data in regions_pool.items():
        multiworld.regions.append(create_explore_region(multiworld, player, name, data))

    # Connect all the regions to their exits
    for name, data in regions_pool.items():
        create_connections_in_regions(multiworld, player, name, data)


def create_explore_region(multiworld: MultiWorld, player: int, name: str, data: RoRRegionData) -> Region:
    region = Region(name, player, multiworld)
    if data.locations:
        for location_name in data.locations:
            location_data = location_table.get(location_name)
            location = RiskOfRainLocation(player, location_name, location_data, region)
            region.locations.append(location)

    return region


def create_connections_in_regions(multiworld: MultiWorld, player: int, name: str, data: RoRRegionData) -> None:
    region = multiworld.get_region(name, player)
    if data.region_exits:
        for region_exit in data.region_exits:
            r_exit_stage = Entrance(player, region_exit, region)
            exit_region = multiworld.get_region(region_exit, player)
            r_exit_stage.connect(exit_region)
            region.exits.append(r_exit_stage)


def create_classic_regions(ror2_world: "RiskOfRainWorld") -> None:
    player = ror2_world.player
    ror2_options = ror2_world.options
    multiworld = ror2_world.multiworld
    menu = create_classic_region(multiworld, player, "Menu")
    multiworld.regions.append(menu)
    # By using a victory region, we can define it as being connected to by several regions
    #   which can then determine the availability of the victory.
    victory_region = create_classic_region(multiworld, player, "Victory")
    multiworld.regions.append(victory_region)
    petrichor = create_classic_region(multiworld, player, "Petrichor V",
                                      get_classic_item_pickups(ror2_options.total_locations.value))
    multiworld.regions.append(petrichor)

    # classic mode can get to victory from the beginning of the game
    to_victory = Entrance(player, "beating game", petrichor)
    petrichor.exits.append(to_victory)
    to_victory.connect(victory_region)

    connection = Entrance(player, "Lobby", menu)
    menu.exits.append(connection)
    connection.connect(petrichor)


def create_classic_region(multiworld: MultiWorld, player: int, name: str, locations: Dict[str, int] = {}) -> Region:
    ret = Region(name, player, multiworld)
    for location_name, location_id in locations.items():
        ret.locations.append(RiskOfRainLocation(player, location_name, location_id, ret))
    return ret
