from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KHCOMLocation, location_table, get_locations_by_category


class KHCOMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, RLRegionData] = {
        "Menu":     KHCOMRegionData(None, ["Floor 1"]),
        "Floor 1":  KHCOMRegionData([], ["Warp"]),
        "Floor 2":  KHCOMRegionData([], []),
        "Floor 3":  KHCOMRegionData([], []),
        "Floor 4":  KHCOMRegionData([], []),
        "Floor 5":  KHCOMRegionData([], []),
        "Floor 6":  KHCOMRegionData([], []),
        "Floor 7":  KHCOMRegionData([], []),
        "Floor 8":  KHCOMRegionData([], []),
        "Floor 9":  KHCOMRegionData([], []),
        "Floor 10": KHCOMRegionData([], []),
        "Floor 11": KHCOMRegionData([], []),
        "Floor 12": KHCOMRegionData([], []),
        "Floor 13": KHCOMRegionData([], []),
        "Warp":     KHCOMRegionData([], ["Floor 2", "Floor 3", "Floor 4",
                                         "Floor 5", "Floor 6", "Floor 7",
                                         "Floor 8", "Floor 9", "Floor 10",
                                         "Floor 11", "Floor 12", "Floor 13"])
    }

    # Set up locations
    
    # Floor 1 Traverse Town
    # Standard Cards
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Kingdom Key)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Blizzard)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Cure)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Potion)")
    # KOB, KOG, KTT Rewards
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Beginnings (Simba)")
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Truth (Guard Armor)")
    regions["Floor 1"].locations.append("F01 Traverse Town Entrance")
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Beginnings")
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Guidance")
    #Room of Rewards
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Rewards (Lionheart)")
    #Post Floor Boss
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Fire)")
    #Enemy Cards
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Shadow)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Soldier)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Blue Rhapsody)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Red Nocturne)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (White Mushroom)")
    regions["Floor 1"].locations.append("F01 Traverse Town Field (Black Fungus)")
    
    
    # Floor 2 Wonderland
    # Standard Cards
    regions["Floor 2"].locations.append("F02 Wonderland Field (Lady Luck)")
    regions["Floor 2"].locations.append("F02 Wonderland Bounty (Stop)")
    # KOB, KOG, KTT Rewards
    regions["Floor 2"].locations.append("F02 Wonderland Room of Beginnings (Card Soldier Red)")
    regions["Floor 2"].locations.append("F02 Wonderland Room of Truth (Trickmaster)")
    regions["Floor 2"].locations.append("F02 Wonderland Entrance")
    regions["Floor 2"].locations.append("F02 Wonderland Room of Beginnings")
    regions["Floor 2"].locations.append("F02 Wonderland Room of Guidance")
    #Enemy Cards
    regions["Floor 2"].locations.append("F02 Wonderland Field (Card Soldier Black)")
    regions["Floor 2"].locations.append("F02 Wonderland Field (Creeper Plant)")
    regions["Floor 2"].locations.append("F02 Wonderland Field (Crescendo)")
    regions["Floor 2"].locations.append("F02 Wonderland Field (Large Body)")
    
    # Floor 3 Olympus Coliseum
    # Standard Cards
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Field (Olympia)")
    # KOB, KOG, KTT Rewards
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Truth (Cloud)")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Truth (Hades)")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Guidance (Hi-Potion)")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Entrance")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Beginnings")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Guidance")
    #Room of Rewards
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Rewards (Metal Chocobo)")
    #Enemy Cards
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Field (Barrel Spider)")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Field (Bouncywild)")
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Field (Powerwild)")
    
    # Floor 4 Monstro
    # Standard Cards
    regions["Floor 4"].locations.append("F04 Monstro Field (Wishing Star)")
    # KOB, KOG, KTT Rewards
    regions["Floor 4"].locations.append("F04 Monstro Room of Guidance (Parasite Cage)")
    regions["Floor 4"].locations.append("F04 Monstro Room of Truth (Dumbo)")
    regions["Floor 4"].locations.append("F04 Monstro Entrance")
    regions["Floor 4"].locations.append("F04 Monstro Room of Beginnings")
    regions["Floor 4"].locations.append("F04 Monstro Room of Guidance")
    #Enemy Cards
    regions["Floor 4"].locations.append("F04 Monstro Field (Green Requiem)")
    regions["Floor 4"].locations.append("F04 Monstro Field (Search Ghost)")
    regions["Floor 4"].locations.append("F04 Monstro Field (Tornado Step)")
    regions["Floor 4"].locations.append("F04 Monstro Field (Yellow Opera)")
    regions["Floor 4"].locations.append("F04 Monstro Field (Air Soldier)")
    
    # Floor 5 Agrabah
    # Standard Cards
    regions["Floor 5"].locations.append("F05 Agrabah Field (Three Wishes)")
    regions["Floor 5"].locations.append("F05 Agrabah Bounty (Gravity)")
    # KOB, KOG, KTT Rewards
    regions["Floor 5"].locations.append("F05 Agrabah Room of Truth (Genie)")
    regions["Floor 5"].locations.append("F05 Agrabah Room of Truth (Jafar)")
    regions["Floor 5"].locations.append("F05 Agrabah Room of Guidance (Ether)")
    regions["Floor 5"].locations.append("F05 Agrabah Entrance")
    regions["Floor 5"].locations.append("F05 Agrabah Room of Beginnings")
    regions["Floor 5"].locations.append("F05 Agrabah Room of Guidance")
    #Enemy Cards
    regions["Floor 5"].locations.append("F05 Agrabah Field (Bandit)")
    regions["Floor 5"].locations.append("F05 Agrabah Field (Fat Bandit)")
    
    # Floor 6 Halloween Town
    # Standard Cards
    regions["Floor 6"].locations.append("F06 Halloween Town Field (Pumpkinhead)")
    # KOB, KOG, KTT Rewards
    regions["Floor 6"].locations.append("F06 Halloween Town Room of Truth (Oogie Boogie)")
    regions["Floor 6"].locations.append("F06 Halloween Town Entrance")
    regions["Floor 6"].locations.append("F06 Halloween Town Room of Beginnings")
    regions["Floor 6"].locations.append("F06 Halloween Town Room of Guidance")
    #Post Floor Boss
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Thunder)")
    #Enemy Cards
    regions["Floor 6"].locations.append("F06 Halloween Town Field (Gargoyle)")
    regions["Floor 6"].locations.append("F06 Halloween Town Field (Wight Knight)")
    
    # Floor 7 Atlantica
    # Standard Cards
    regions["Floor 7"].locations.append("F07 Atlantica Field (Crabclaw)")
    # KOB, KOG, KTT Rewards
    regions["Floor 7"].locations.append("F07 Atlantica Room of Truth (Ursula)")
    regions["Floor 7"].locations.append("F07 Atlantica Entrance")
    regions["Floor 7"].locations.append("F07 Atlantica Room of Beginnings")
    regions["Floor 7"].locations.append("F07 Atlantica Room of Guidance")
    #Post Floor Boss
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Aero)")
    #Enemy Cards
    regions["Floor 7"].locations.append("F07 Atlantica Field (Aquatank)")
    regions["Floor 7"].locations.append("F07 Atlantica Field (Darkball)")
    regions["Floor 7"].locations.append("F07 Atlantica Field (Sea Neon)")
    regions["Floor 7"].locations.append("F07 Atlantica Field (Screwdriver)")
    
    # Floor 8 Never Land
    # Standard Cards
    regions["Floor 8"].locations.append("F08 Neverland Field (Fairy Harp)")
    # KOB, KOG, KTT Rewards
    regions["Floor 8"].locations.append("F08 Neverland Room of Truth (Hook)")
    regions["Floor 8"].locations.append("F08 Neverland Room of Truth (Tinker Bell)")
    regions["Floor 8"].locations.append("F08 Neverland Entrance")
    regions["Floor 8"].locations.append("F08 Neverland Room of Beginnings")
    regions["Floor 8"].locations.append("F08 Neverland Room of Guidance")
    #Enemy Cards
    regions["Floor 8"].locations.append("F08 Neverland Field (Air Pirate)")
    regions["Floor 8"].locations.append("F08 Neverland Field (Pirate)")
    
    # Floor 9 Holloow Bastion
    # Standard Cards
    regions["Floor 9"].locations.append("F09 Hollow Bastion Field (Divine Rose)")
    # KOB, KOG, KTT Rewards
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Truth (Dragon Maleficent)")
    regions["Floor 9"].locations.append("F09 Hollow Bastion Entrance")
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Beginnings")
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Guidance")
    #Room of Rewards
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Rewards (Mushu)")
    #Enemy Cards
    regions["Floor 9"].locations.append("F09 Hollow Bastion Field (Defender)")
    regions["Floor 9"].locations.append("F09 Hollow Bastion Field (Wizard)")
    regions["Floor 9"].locations.append("F09 Hollow Bastion Field (Wyvern)")
    
    # Floor 10 100 Acre Wood
    # Rewards
    regions["Floor 10"].locations.append("F10 100 Acre Wood Complete (Bambi)")
    regions["Floor 10"].locations.append("F10 100 Acre Wood Roo (Elixir)")
    regions["Floor 10"].locations.append("F10 100 Acre Wood Owl (Spellbinder)")
    #Post Floor Boss
    regions["Floor 10"].locations.append("F10 100 Acre Wood Post Floor (Mega-Ether)")
    
    # Floor 11 Twilight Town
    # KOB, KOG, KTT Rewards
    regions["Floor 11"].locations.append("F11 Twilight Town Room of Beginnings (Vexen)")
    regions["Floor 11"].locations.append("F11 Twilight Town Entrance")
    #Post Floor Boss
    regions["Floor 11"].locations.append("F11 Twilight Town Post Floor (Mega-Potion)")
    
    # Floor 12 Destiny Islands
    # KOB, KOG, KTT Rewards
    regions["Floor 12"].locations.append("F12 Destiny Islands Room of Guidance (Darkside)")
    regions["Floor 12"].locations.append("F12 Destiny Islands Entrance")
    regions["Floor 12"].locations.append("F12 Destiny Islands Room of Beginnings")
    #Post Floor Boss
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Riku)")
    #regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Larxene)")
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Oathkeeper)")
    #regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Oblivion)")
    #Room of Rewards
    regions["Floor 12"].locations.append("F12 Destiny Islands Room of Rewards (Megalixir)")
    
    # Floor 13 Castle Oblivion
    # KOB, KOG, KTT Rewards
    regions["Floor 13"].locations.append("F13 Castle Oblivion Room of Beginnings (Axel)")
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Floor (Marluxia)")
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Marluxia (Diamond Dust)")
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Marluxia (One-Winged Angel)")
    regions["Floor 13"].locations.append("F13 Castle Oblivion Entrance")
    #Enemy Cards
    regions["Floor 13"].locations.append("F13 Castle Oblivion Field (Neoshadow)")

    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Floor 1", player).connect(multiworld.get_region("Floor 1", player))
    multiworld.get_entrance("Floor 2", player).connect(multiworld.get_region("Floor 2", player))
    multiworld.get_entrance("Floor 3", player).connect(multiworld.get_region("Floor 3", player))
    multiworld.get_entrance("Floor 4", player).connect(multiworld.get_region("Floor 4", player))
    multiworld.get_entrance("Floor 5", player).connect(multiworld.get_region("Floor 5", player))
    multiworld.get_entrance("Floor 6", player).connect(multiworld.get_region("Floor 6", player))
    multiworld.get_entrance("Floor 7", player).connect(multiworld.get_region("Floor 7", player))
    multiworld.get_entrance("Floor 8", player).connect(multiworld.get_region("Floor 8", player))
    multiworld.get_entrance("Floor 9", player).connect(multiworld.get_region("Floor 9", player))
    multiworld.get_entrance("Floor 10", player).connect(multiworld.get_region("Floor 10", player))
    multiworld.get_entrance("Floor 11", player).connect(multiworld.get_region("Floor 11", player))
    multiworld.get_entrance("Floor 12", player).connect(multiworld.get_region("Floor 12", player))
    multiworld.get_entrance("Floor 13", player).connect(multiworld.get_region("Floor 13", player))
    multiworld.get_entrance("Warp", player).connect(multiworld.get_region("Warp", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: KHCOMRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = KHCOMLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
