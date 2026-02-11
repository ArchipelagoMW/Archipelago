from typing import NamedTuple, Callable, List, Dict
from BaseClasses import CollectionState


class MMRRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, MMRRegionData] = {
    "Menu": MMRRegionData(["Clock Town"]),
    "Clock Town": MMRRegionData(["The Moon", "Trading Post", "Bomber's Hideout", "Termina Field"]),
    "The Moon": MMRRegionData([]),
    "Trading Post": MMRRegionData([]),
    "Bomber's Hideout": MMRRegionData(["Astral Observatory"]),
    "Astral Observatory": MMRRegionData(["Astral Observatory (Outside)"]),
    "Astral Observatory (Outside)": MMRRegionData(["Termina Field"]),
    "Termina Field": MMRRegionData(["Southern Swamp", "Milk Road", "Path to Mountain Village", "Great Bay", "Road to Ikana"]),
    "Southern Swamp": MMRRegionData(["Southern Swamp (Deku Palace)"]),
    "Southern Swamp (Deku Palace)": MMRRegionData(["Swamp Spider House", "Deku Palace", "Woodfall"]),
    "Swamp Spider House": MMRRegionData([]),
    "Deku Palace": MMRRegionData([]),
    "Woodfall": MMRRegionData(["Woodfall Temple"]),
    "Woodfall Temple": MMRRegionData([]),
    "Milk Road": MMRRegionData(["Gorman Brothers Track", "Romani Ranch"]),
    "Gorman Brothers Track": MMRRegionData([]),
    "Romani Ranch": MMRRegionData([]),
    "Path to Mountain Village": MMRRegionData(["Mountain Village"]),
    "Mountain Village": MMRRegionData(["Twin Islands", "Path to Snowhead"]),
    "Twin Islands": MMRRegionData(["Goron Village"]),
    "Goron Village": MMRRegionData(["Goron Shrine"]),
    "Goron Shrine": MMRRegionData([]),
    "Path to Snowhead": MMRRegionData(["Snowhead"]),
    "Snowhead": MMRRegionData(["Snowhead Temple"]),
    "Snowhead Temple": MMRRegionData([]),
    "Great Bay": MMRRegionData(["Ocean Spider House", "Fisherman's House", "Pirates' Fortress", "Pinnacle Rock", "Zora Cape"]),
    "Ocean Spider House": MMRRegionData([]),
    "Fisherman's House": MMRRegionData([]),
    "Pirates' Fortress": MMRRegionData(["Pirates' Fortress Sewers", "Pirates' Fortress (Interior)"]),
    "Pirates' Fortress Sewers": MMRRegionData(["Pirates' Fortress (Interior)"]),
    "Pirates' Fortress (Interior)": MMRRegionData([]),
    "Pinnacle Rock": MMRRegionData([]),
    "Zora Cape": MMRRegionData(["Zora Hall", "Great Bay Temple"]),
    "Zora Hall": MMRRegionData([]),
    "Great Bay Temple": MMRRegionData([]),
    "Road to Ikana": MMRRegionData(["Ikana Graveyard", "Ikana Canyon"]),
    "Ikana Graveyard": MMRRegionData([]),
    "Ikana Canyon": MMRRegionData(["Secret Shrine", "Beneath the Well", "Ikana Castle", "Stone Tower"]),
    "Secret Shrine": MMRRegionData([]),
    "Beneath the Well": MMRRegionData(["Ikana Castle"]),
    "Ikana Castle": MMRRegionData(["Beneath the Well", "Inside Ikana Castle"]),
    "Inside Ikana Castle": MMRRegionData([]),
    "Stone Tower": MMRRegionData(["Stone Tower Temple", "Stone Tower (Inverted)"]),
    "Stone Tower Temple": MMRRegionData([]),
    "Stone Tower (Inverted)": MMRRegionData(["Stone Tower Temple (Inverted)"]),
    "Stone Tower Temple (Inverted)": MMRRegionData([]),
}

def get_exit(region, exit_name):
    for exit in region.exits:
        if exit.connected_region.name == exit_name:
            return exit
