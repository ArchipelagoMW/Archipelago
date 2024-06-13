# for making rules for ladder storage in overworld
from typing import Dict, List, Set, NamedTuple


class LadderInfo(NamedTuple):
    ladders: Set[str]  # ladders where the top or bottom is at the same elevation
    portals: List[str]  # portals at the same elevation, only those without doors
    regions: List[str]  # regions where a melee enemy can hit you out of ladder storage


# groups for ladders at the same elevation, for use in determing whether you can ls to entrances in diff rulesets
ow_ladder_groups: Dict[str, LadderInfo] = {
    # lowest elevation
    "LS Elev 0": LadderInfo({"Ladders in Overworld Town", "Ladder to Ruined Atoll", "Ladder to Swamp"},
                            ["Swamp Redux 2_conduit", "Overworld Cave_", "Atoll Redux_lower", "Maze Room_",
                             "Town Basement_beach", "Archipelagos Redux_lowest"],
                            ["Overworld Beach"]),
    # also the east filigree room
    "LS Elev 1": LadderInfo({"Ladders near Weathervane", "Ladders in Overworld Town", "Ladder to Swamp"},
                            ["Furnace_gyro_lower", "Swamp Redux 2_wall"],
                            ["Overworld Tunnel Turret"]),
    # also the fountain filigree room and ruined passage door
    "LS Elev 2": LadderInfo({"Ladders near Weathervane", "Ladders to West Bell"},
                            ["Archipelagos Redux_lower", "Ruins Passage_east"],
                            ["After Ruined Passage"]),
    # also old house door
    "LS Elev 3": LadderInfo({"Ladders near Weathervane", "Ladder to Quarry", "Ladders to West Bell",
                             "Ladders in Overworld Town"},
                            [],
                            ["Overworld after Envoy", "East Overworld"]),
    # skip top of top ladder next to weathervane level, does not provide logical access to anything
    "LS Elev 4": LadderInfo({"Ladders near Dark Tomb", "Ladder to Quarry", "Ladders to West Bell", "Ladders in Well",
                             "Ladders in Overworld Town"},
                            ["Darkwoods Tunnel_"],
                            []),
    "LS Elev 5": LadderInfo({"Ladders near Overworld Checkpoint", "Ladders near Patrol Cave"},
                            ["PatrolCave_", "Forest Belltower_", "Fortress Courtyard_", "ShopSpecial_"],
                            ["East Overworld"]),
    # skip top of belltower, middle of dark tomb ladders, and top of checkpoint, does not grant access to anything
    "LS Elev 6": LadderInfo({"Ladders near Patrol Cave", "Ladder near Temple Rafters"},
                            ["Temple_rafters"],
                            ["Overworld above Patrol Cave"]),
    # in-line with the chest above dark tomb, gets you up the mountain stairs
    "LS Elev 7": LadderInfo({"Ladders near Patrol Cave", "Ladder near Temple Rafters", "Ladders near Dark Tomb"},
                            ["Mountain_"],
                            ["Upper Overworld"]),
}


# ladders accessible within different regions of overworld, only those that are relevant
# other scenes will just have them hardcoded since this type of structure is not necessary there
region_ladders: Dict[str, Set[str]] = {
    "Overworld": {"Ladders near Weathervane", "Ladders near Overworld Checkpoint", "Ladders near Dark Tomb",
                  "Ladders in Overworld Town", "Ladder to Swamp", "Ladders in Well"},
    "Overworld Beach": {"Ladder to Ruined Atoll"},
    "Overworld at Patrol Cave": {"Ladders near Patrol Cave"},
    "Overworld Quarry Entry": {"Ladder to Quarry"},
    "Overworld Belltower": {"Ladders to West Bell"},
    "Overworld after Temple Rafters": {"Ladders near Temple Rafters"},
}
