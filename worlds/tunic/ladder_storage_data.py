from typing import Dict, List, Set, NamedTuple, Optional


# ladders in overworld, since it is the most complex area for ladder storage
class OWLadderInfo(NamedTuple):
    ladders: Set[str]  # ladders where the top or bottom is at the same elevation
    portals: List[str]  # portals at the same elevation, only those without doors
    regions: List[str]  # regions where a melee enemy can hit you out of ladder storage


# groups for ladders at the same elevation, for use in determing whether you can ls to entrances in diff rulesets
ow_ladder_groups: Dict[str, OWLadderInfo] = {
    # lowest elevation
    "LS Elev 0": OWLadderInfo({"Ladders in Overworld Town", "Ladder to Ruined Atoll", "Ladder to Swamp"},
                              ["Swamp Redux 2_conduit", "Overworld Cave_", "Atoll Redux_lower", "Maze Room_",
                              "Town Basement_beach", "Archipelagos Redux_lower", "Archipelagos Redux_lowest"],
                              ["Overworld Beach"]),
    # also the east filigree room
    "LS Elev 1": OWLadderInfo({"Ladders near Weathervane", "Ladders in Overworld Town", "Ladder to Swamp"},
                              ["Furnace_gyro_lower", "Furnace_gyro_west", "Swamp Redux 2_wall"],
                              ["Overworld Tunnel Turret"]),
    # also the fountain filigree room and ruined passage door
    "LS Elev 2": OWLadderInfo({"Ladders near Weathervane", "Ladders to West Bell"},
                              ["Archipelagos Redux_upper", "Ruins Passage_east"],
                              ["After Ruined Passage"]),
    # also old house door
    "LS Elev 3": OWLadderInfo({"Ladders near Weathervane", "Ladder to Quarry", "Ladders to West Bell",
                               "Ladders in Overworld Town"},
                              [],
                              ["Overworld after Envoy", "East Overworld"]),
    # skip top of top ladder next to weathervane level, does not provide logical access to anything
    "LS Elev 4": OWLadderInfo({"Ladders near Dark Tomb", "Ladder to Quarry", "Ladders to West Bell", "Ladders in Well",
                               "Ladders in Overworld Town"},
                              ["Darkwoods Tunnel_"],
                              []),
    "LS Elev 5": OWLadderInfo({"Ladders near Overworld Checkpoint", "Ladders near Patrol Cave"},
                              ["PatrolCave_", "Forest Belltower_", "Fortress Courtyard_", "ShopSpecial_"],
                              ["East Overworld"]),
    # skip top of belltower, middle of dark tomb ladders, and top of checkpoint, does not grant access to anything
    "LS Elev 6": OWLadderInfo({"Ladders near Patrol Cave", "Ladder near Temple Rafters"},
                              ["Temple_rafters"],
                              ["Overworld above Patrol Cave"]),
    # in-line with the chest above dark tomb, gets you up the mountain stairs
    "LS Elev 7": OWLadderInfo({"Ladders near Patrol Cave", "Ladder near Temple Rafters", "Ladders near Dark Tomb"},
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


class LadderInfo(NamedTuple):
    origin: str  # origin region
    destination: str  # destination portal
    ladders_req: Optional[str] = None  # ladders required to do this
    dest_is_region: bool = False  # whether it is a region that you are going to


easy_ls: List[LadderInfo] = [
    # In the furnace
    # Furnace ladder to the fuse entrance
    LadderInfo("Furnace Ladder Area", "Furnace, Overworld Redux_gyro_upper_north"),
    # Furnace ladder to Dark Tomb
    LadderInfo("Furnace Ladder Area", "Furnace, Crypt Redux_"),
    # Furnace ladder to the West Garden connector
    LadderInfo("Furnace Ladder Area", "Furnace, Overworld Redux_gyro_west"),

    # West Garden
    # exit after Garden Knight
    LadderInfo("West Garden before Boss", "Archipelagos Redux, Overworld Redux_upper"),
    # West Garden laurels exit
    LadderInfo("West Garden after Terry", "Archipelagos Redux, Overworld Redux_lowest"),
    # Magic dagger house, only relevant with combat logic on
    LadderInfo("West Garden after Terry", "Archipelagos Redux, archipelagos_house_"),

    # Atoll, use the little ladder you fix at the beginning
    LadderInfo("Ruined Atoll", "Atoll Redux, Overworld Redux_lower"),
    LadderInfo("Ruined Atoll", "Atoll Redux, Frog Stairs_mouth"),  # special case

    # East Forest
    # Entrance by the dancing fox holy cross spot
    LadderInfo("East Forest", "East Forest Redux, East Forest Redux Laddercave_upper"),

    # From the west side of Guard House 1 to the east side
    LadderInfo("Guard House 1 West", "East Forest Redux Laddercave, East Forest Redux_gate"),
    LadderInfo("Guard House 1 West", "East Forest Redux Laddercave, Forest Boss Room_"),

    # Fortress Exterior
    # shop, ls at the ladder by the telescope
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard, Shop_"),
    # Fortress main entry and grave path lower entry, ls at the ladder by the telescope
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Main_Big Door"),
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Reliquary_Lower"),
    # Use the top of the ladder by the telescope
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Reliquary_Upper"),
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress East_"),

    # same as above, except from the east side of the area
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Overworld Redux_"),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Shop_"),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Main_Big Door"),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Reliquary_Lower"),

    # same as above, except from the Beneath the Vault entrance ladder
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard, Overworld Redux_", "Ladder to Beneath the Vault"),
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard, Fortress Main_Big Door",
               "Ladder to Beneath the Vault"),
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard, Fortress Reliquary_Lower",
               "Ladder to Beneath the Vault"),

    # Swamp to Gauntlet
    LadderInfo("Swamp Mid", "Swamp Redux 2, Cathedral Arena_", "Ladders in Swamp"),

    # Ladder by the hero grave
    LadderInfo("Back of Swamp", "Swamp Redux 2, Overworld Redux_conduit"),
    LadderInfo("Back of Swamp", "Swamp Redux 2, Shop_"),
]

# if we can gain elevation or get knocked down, add the harder ones
medium_ls: List[LadderInfo] = [
    # region-destination versions of easy ls spots
    LadderInfo("East Forest", "East Forest Dance Fox Spot", dest_is_region=True),
    # fortress courtyard knockdowns are never logically relevant, the fuse requires upper
    LadderInfo("Back of Swamp", "Swamp Mid", dest_is_region=True),
    LadderInfo("Back of Swamp", "Swamp Front", dest_is_region=True),

    # gain height off the northeast fuse ramp
    LadderInfo("Ruined Atoll", "Atoll Redux, Frog Stairs_eye"),

    # Upper exit from the Forest Grave Path, use LS at the ladder by the gate switch
    LadderInfo("Forest Grave Path Main", "Sword Access, East Forest Redux_upper"),

    # Upper exits from the courtyard. Use the ramp in the courtyard, then the blocks north of the first fuse
    LadderInfo("Fortress Exterior from Overworld", "Fortress Courtyard Upper", dest_is_region=True),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Reliquary_Upper"),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress East_"),
    LadderInfo("Fortress Exterior from East Forest", "Fortress Courtyard Upper", dest_is_region=True),
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard, Fortress Reliquary_Upper",
               "Ladder to Beneath the Vault"),
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard, Fortress East_", "Ladder to Beneath the Vault"),
    LadderInfo("Fortress Exterior near cave", "Fortress Courtyard Upper", "Ladder to Beneath the Vault",
               dest_is_region=True),

    # need to gain height to get up the stairs
    LadderInfo("Lower Mountain", "Mountain, Mountaintop_"),

    # Where the rope is behind Monastery
    LadderInfo("Quarry Entry", "Quarry Redux, Monastery_back"),
    LadderInfo("Quarry Monastery Entry", "Quarry Redux, Monastery_back"),
    LadderInfo("Quarry Back", "Quarry Redux, Monastery_back"),

    LadderInfo("Rooted Ziggurat Lower Back", "ziggurat2020_3, ziggurat2020_2_"),
    LadderInfo("Rooted Ziggurat Lower Back", "Rooted Ziggurat Lower Entry", dest_is_region=True),
    LadderInfo("Rooted Ziggurat Lower Back", "Rooted Ziggurat Lower Mid Checkpoint", dest_is_region=True),

    # Swamp to Overworld upper
    LadderInfo("Swamp Mid", "Swamp Redux 2, Overworld Redux_wall", "Ladders in Swamp"),
    LadderInfo("Back of Swamp", "Swamp Redux 2, Overworld Redux_wall"),
]

hard_ls: List[LadderInfo] = [
    # lower ladder, go into the waterfall then above the bonfire, up a ramp, then through the right wall
    LadderInfo("Beneath the Well Front", "Sewer, Sewer_Boss_", "Ladders in Well"),
    LadderInfo("Beneath the Well Front", "Sewer, Overworld Redux_west_aqueduct", "Ladders in Well"),
    LadderInfo("Beneath the Well Front", "Beneath the Well Back", "Ladders in Well", dest_is_region=True),
    # go through the hexagon engraving above the vault door
    LadderInfo("Frog's Domain Front", "frog cave main, Frog Stairs_Exit", "Ladders to Frog's Domain"),
    # the turret at the end here is not affected by enemy rando
    LadderInfo("Frog's Domain Front", "Frog's Domain Back", "Ladders to Frog's Domain", dest_is_region=True),
    # todo: see if we can use that new laurels strat here
    # LadderInfo("Rooted Ziggurat Lower Back", "ziggurat2020_3, ziggurat2020_FTRoom_"),
    # go behind the cathedral to reach the door, pretty easily doable
    LadderInfo("Swamp Mid", "Swamp Redux 2, Cathedral Redux_main", "Ladders in Swamp"),
    LadderInfo("Back of Swamp", "Swamp Redux 2, Cathedral Redux_main"),
    # need to do hc midair, probably cannot get into this without hc
    LadderInfo("Swamp Mid", "Swamp Redux 2, Cathedral Redux_secret", "Ladders in Swamp"),
    LadderInfo("Back of Swamp", "Swamp Redux 2, Cathedral Redux_secret"),
]
