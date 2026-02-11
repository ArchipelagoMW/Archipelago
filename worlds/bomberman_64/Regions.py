from typing import Dict, List, NamedTuple


class Bomb64RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, Bomb64RegionData] = {
    "Menu": Bomb64RegionData(["Green Garden","Blue Resort","Red Mountain","White Glacier","Black Fortress"]),
    "Green Garden": Bomb64RegionData(["Untouchable Treasure","Friend or Foe","To Have or Have Not","Winged Guardian"]),
    "Blue Resort": Bomb64RegionData(["Switches and Bridges","Vs Artemis","Pump It Up","Sewer Savage"]),
    "Red Mountain": Bomb64RegionData(["Hot On The Trail","Vs Orion","On the Right Track","Hot Avenger"]),
    "White Glacier": Bomb64RegionData(["Blizzard Peaks","Vs Regulus","Shiny Slippery Icy Floor","Cold Killer"]),
    "Black Fortress": Bomb64RegionData(["Go For Broke","High Tech Harvester","Trap Tower","Vs Altair","Rainbow Palace"]),
    "Rainbow Palace": Bomb64RegionData(["Beyond the Clouds","Vs Spellmaker","Doom Castle","The Final Battle"]),

    "Untouchable Treasure": Bomb64RegionData(["Untouchable Treasure Clear"]),
    "Friend or Foe": Bomb64RegionData(),
    "To Have or Have Not": Bomb64RegionData(["To Have or Have Not Clear"]),
    "Winged Guardian": Bomb64RegionData(),

    "Switches and Bridges": Bomb64RegionData(["Switches and Bridges Clear"]),
    "Vs Artemis": Bomb64RegionData(),
    "Pump It Up": Bomb64RegionData(["Pump It Up Clear"]),
    "Sewer Savage": Bomb64RegionData(),

    "Hot On The Trail": Bomb64RegionData(["Hot On The Trail Clear"]),
    "Vs Orion": Bomb64RegionData(),
    "On the Right Track": Bomb64RegionData(["On the Right Track Clear"]),
    "Hot Avenger": Bomb64RegionData(),

    "Blizzard Peaks": Bomb64RegionData(["Blizzard Peaks Clear"]),
    "Vs Regulus": Bomb64RegionData(),
    "Shiny Slippery Icy Floor": Bomb64RegionData(["Shiny Slippery Icy Floor Clear"]),
    "Cold Killer": Bomb64RegionData(),

    "Go For Broke": Bomb64RegionData(["Go For Broke Clear"]),
    "High Tech Harvester": Bomb64RegionData(),
    "Trap Tower": Bomb64RegionData(["Trap Tower Clear"]),
    "Vs Altair": Bomb64RegionData(),

    "Beyond the Clouds": Bomb64RegionData(["Beyond the Clouds Clear"]),
    "Vs Spellmaker": Bomb64RegionData(),
    "Doom Castle": Bomb64RegionData(["Doom Castle Clear"]),
    "The Final Battle": Bomb64RegionData(),

    "Untouchable Treasure Clear": Bomb64RegionData(),
    "To Have or Have Not Clear": Bomb64RegionData(),

    "Switches and Bridges Clear": Bomb64RegionData(),
    "Pump It Up Clear": Bomb64RegionData(),

    "Hot On The Trail Clear": Bomb64RegionData(),
    "On the Right Track Clear": Bomb64RegionData(),

    "Blizzard Peaks Clear": Bomb64RegionData(),
    "Shiny Slippery Icy Floor Clear": Bomb64RegionData(),

    "Go For Broke Clear": Bomb64RegionData(),
    "Trap Tower Clear": Bomb64RegionData(),

    "Beyond the Clouds Clear": Bomb64RegionData(),
    "Doom Castle Clear": Bomb64RegionData(),
}

def get_exit(region, exit_name):
    for exit in region.exits:
        if exit.connected_region.name == exit_name:
            return exit