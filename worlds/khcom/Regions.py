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
    regions["Floor 1"].locations.append("Kingdom Key")
    regions["Floor 1"].locations.append("Blizzard")
    regions["Floor 1"].locations.append("Cure")
    regions["Floor 1"].locations.append("Potion")
    # KOB, KOG, KTT Rewards
    regions["Floor 1"].locations.append("Simba")
    regions["Floor 1"].locations.append("Guard Armor")
    regions["Floor 1"].locations.append("Key of Beginnings F01")
    regions["Floor 1"].locations.append("Key of Guidance F01")
    regions["Floor 1"].locations.append("Key to Truth F01")
    #Room of Rewards
    regions["Floor 1"].locations.append("Lionheart")
    #Post Floor Boss
    regions["Floor 1"].locations.append("Fire")
    #Enemy Cards
    regions["Floor 1"].locations.append("Shadow")
    regions["Floor 1"].locations.append("Soldier")
    regions["Floor 1"].locations.append("Blue Rhapsody")
    regions["Floor 1"].locations.append("Red Nocturne")
    regions["Floor 1"].locations.append("White Mushroom")
    regions["Floor 1"].locations.append("Black Fungus")
    
    
    # Floor 2 Wonderland
    # Standard Cards
    regions["Floor 2"].locations.append("Lady Luck")
    regions["Floor 2"].locations.append("Stop")
    # KOB, KOG, KTT Rewards
    regions["Floor 2"].locations.append("Card Soldier (Red)")
    regions["Floor 2"].locations.append("Trickmaster")
    regions["Floor 2"].locations.append("Key of Beginnings F02")
    regions["Floor 2"].locations.append("Key of Guidance F02")
    regions["Floor 2"].locations.append("Key to Truth F02")
    #Enemy Cards
    regions["Floor 2"].locations.append("Card Soldier (Black)")
    regions["Floor 2"].locations.append("Creeper Plant")
    regions["Floor 2"].locations.append("Crescendo")
    regions["Floor 2"].locations.append("Large Body")
    
    # Floor 3 Olympus Coliseum
    # Standard Cards
    regions["Floor 3"].locations.append("Olympia")
    # KOB, KOG, KTT Rewards
    regions["Floor 3"].locations.append("Cloud")
    regions["Floor 3"].locations.append("Hades")
    regions["Floor 3"].locations.append("Hi-Potion")
    regions["Floor 3"].locations.append("Key of Beginnings F03")
    regions["Floor 3"].locations.append("Key of Guidance F03")
    regions["Floor 3"].locations.append("Key to Truth F03")
    #Room of Rewards
    regions["Floor 3"].locations.append("Metal Chocobo")
    #Enemy Cards
    regions["Floor 3"].locations.append("Barrel Spider")
    regions["Floor 3"].locations.append("Bouncywild")
    regions["Floor 3"].locations.append("Powerwild")
    
    # Floor 4 Monstro
    # Standard Cards
    regions["Floor 4"].locations.append("Wishing Star")
    # KOB, KOG, KTT Rewards
    regions["Floor 4"].locations.append("Parasite Cage")
    regions["Floor 4"].locations.append("Dumbo")
    regions["Floor 4"].locations.append("Key of Beginnings F04")
    regions["Floor 4"].locations.append("Key of Guidance F04")
    regions["Floor 4"].locations.append("Key to Truth F04")
    #Enemy Cards
    regions["Floor 4"].locations.append("Green Requiem")
    regions["Floor 4"].locations.append("Search Ghost")
    regions["Floor 4"].locations.append("Tornado Step")
    regions["Floor 4"].locations.append("Yellow Opera")
    regions["Floor 4"].locations.append("Air Soldier")
    
    # Floor 5 Agrabah
    # Standard Cards
    regions["Floor 5"].locations.append("Three Wishes")
    regions["Floor 5"].locations.append("Gravity")
    # KOB, KOG, KTT Rewards
    regions["Floor 5"].locations.append("Genie")
    regions["Floor 5"].locations.append("Jafar")
    regions["Floor 5"].locations.append("Ether")
    regions["Floor 5"].locations.append("Key of Beginnings F05")
    regions["Floor 5"].locations.append("Key of Guidance F05")
    regions["Floor 5"].locations.append("Key to Truth F05")
    #Enemy Cards
    regions["Floor 5"].locations.append("Bandit")
    regions["Floor 5"].locations.append("Fat Bandit")
    
    # Floor 6 Halloween Town
    # Standard Cards
    regions["Floor 6"].locations.append("Pumpkinhead")
    regions["Floor 6"].locations.append("Gravity")
    # KOB, KOG, KTT Rewards
    regions["Floor 6"].locations.append("Oogie Boogie")
    regions["Floor 6"].locations.append("Key of Beginnings F06")
    regions["Floor 6"].locations.append("Key of Guidance F06")
    regions["Floor 6"].locations.append("Key to Truth F06")
    #Post Floor Boss
    regions["Floor 6"].locations.append("Thunder")
    #Enemy Cards
    regions["Floor 6"].locations.append("Gargoyle")
    regions["Floor 6"].locations.append("Wight Knight")
    
    # Floor 7 Atlantica
    # Standard Cards
    regions["Floor 7"].locations.append("Crabclaw")
    # KOB, KOG, KTT Rewards
    regions["Floor 7"].locations.append("Ursula")
    regions["Floor 7"].locations.append("Key of Beginnings F07")
    regions["Floor 7"].locations.append("Key of Guidance F07")
    regions["Floor 7"].locations.append("Key to Truth F07")
    #Post Floor Boss
    regions["Floor 7"].locations.append("Aero")
    #Enemy Cards
    regions["Floor 7"].locations.append("Aquatank")
    regions["Floor 7"].locations.append("Darkball")
    regions["Floor 7"].locations.append("Sea Neon")
    
    # Floor 8 Never Land
    # Standard Cards
    regions["Floor 8"].locations.append("Fairy Harp")
    # KOB, KOG, KTT Rewards
    regions["Floor 8"].locations.append("Hook")
    regions["Floor 8"].locations.append("Tinker Bell")
    regions["Floor 8"].locations.append("Key of Beginnings F08")
    regions["Floor 8"].locations.append("Key of Guidance F08")
    regions["Floor 8"].locations.append("Key to Truth F08")
    #Enemy Cards
    regions["Floor 8"].locations.append("Air Pirate")
    regions["Floor 8"].locations.append("Pirate")
    
    # Floor 9 Holloow Bastion
    # Standard Cards
    regions["Floor 9"].locations.append("Divine Rose")
    # KOB, KOG, KTT Rewards
    regions["Floor 9"].locations.append("Dragon Malificent")
    regions["Floor 9"].locations.append("Key of Beginnings F09")
    regions["Floor 9"].locations.append("Key of Guidance F09")
    regions["Floor 9"].locations.append("Key to Truth F09")
    #Room of Rewards
    regions["Floor 9"].locations.append("Mushu")
    #Enemy Cards
    regions["Floor 9"].locations.append("Defender")
    regions["Floor 9"].locations.append("Wizard")
    regions["Floor 9"].locations.append("Wyvern")
    
    # Floor 10 100 Acre Wood
    # Rewards
    regions["Floor 10"].locations.append("Bambi")
    regions["Floor 10"].locations.append("Elixir")
    regions["Floor 10"].locations.append("Spellbinder")
    #Post Floor Boss
    regions["Floor 10"].locations.append("Mega-Ether")
    
    # Floor 11 Twilight Town
    # KOB, KOG, KTT Rewards
    regions["Floor 11"].locations.append("Vexen")
    regions["Floor 11"].locations.append("Key of Beginnings F11")
    #Post Floor Boss
    regions["Floor 11"].locations.append("Mega-Potion")
    
    # Floor 12 Destiny Islands
    # Standard Cards
    regions["Floor 12"].locations.append("Divine Rose")
    # KOB, KOG, KTT Rewards
    regions["Floor 12"].locations.append("Darkside")
    regions["Floor 12"].locations.append("Key of Beginnings F12")
    regions["Floor 12"].locations.append("Key of Guidance F12")
    #Post Floor Boss
    regions["Floor 12"].locations.append("Riku")
    regions["Floor 12"].locations.append("Larxene")
    #Room of Rewards
    regions["Floor 12"].locations.append("Megalixir")
    
    # Floor 13 Castle Oblivion
    # Standard Cards
    regions["Floor 13"].locations.append("Divine Rose")
    # KOB, KOG, KTT Rewards
    regions["Floor 13"].locations.append("Axel")
    regions["Floor 13"].locations.append("Marluxia")
    regions["Floor 13"].locations.append("Key of Beginnings F13")
    #Enemy Cards
    regions["Floor 13"].locations.append("Neoshadow")

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
