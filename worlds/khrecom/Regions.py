from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KHRECOMLocation, location_table, get_locations_by_category


class KHRECOMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, RLRegionData] = {
        "Menu":     KHRECOMRegionData(None, ["Floor 1"]),
        "Floor 1":  KHRECOMRegionData([], ["Warp"]),
        "Floor 2":  KHRECOMRegionData([], []),
        "Floor 3":  KHRECOMRegionData([], []),
        "Floor 4":  KHRECOMRegionData([], []),
        "Floor 5":  KHRECOMRegionData([], []),
        "Floor 6":  KHRECOMRegionData([], []),
        "Floor 7":  KHRECOMRegionData([], []),
        "Floor 8":  KHRECOMRegionData([], []),
        "Floor 9":  KHRECOMRegionData([], []),
        "Floor 10": KHRECOMRegionData([], []),
        "Floor 11": KHRECOMRegionData([], []),
        "Floor 12": KHRECOMRegionData([], []),
        "Floor 13": KHRECOMRegionData([], []),
        "Heartless":KHRECOMRegionData([], []),
        "Warp":     KHRECOMRegionData([], ["Floor 2", "Floor 3", "Floor 4",
                                         "Floor 5", "Floor 6", "Floor 7",
                                         "Floor 8", "Floor 9", "Floor 10",
                                         "Floor 11", "Floor 12", "Floor 13", "Heartless"])
    }

    # Set up locations

    regions["Floor 1"].locations.append("Starting Checks (Attack Cards Kingdom Key)")
    regions["Floor 1"].locations.append("Starting Checks (Item Cards Potion)")
    regions["Floor 1"].locations.append("Starting Checks (Magic Cards Blizzard)")
    regions["Floor 1"].locations.append("Starting Checks (Magic Cards Cure)")
    regions["Floor 1"].locations.append("Traverse Town Post Floor (Magic Cards Fire)")
    regions["Floor 1"].locations.append("Traverse Town Room of Beginnings")
    regions["Floor 1"].locations.append("Traverse Town Room of Beginnings (Summon Cards Simba)")
    regions["Floor 1"].locations.append("Traverse Town Room of Guidance")
    regions["Floor 1"].locations.append("Traverse Town Room of Truth")
    regions["Floor 1"].locations.append("Traverse Town Room of Truth (Enemy Cards Guard Armor)")
    regions["Floor 1"].locations.append("Traverse Town Room of Rewards (Attack Cards Lionheart)")
    
    regions["Floor 2"].locations.append("Wonderland Bounty (Magic Cards Stop)")
    regions["Floor 2"].locations.append("Wonderland Field (Attack Cards Lady Luck)")
    regions["Floor 2"].locations.append("Wonderland Room of Beginnings")
    regions["Floor 2"].locations.append("Wonderland Room of Beginnings (Enemy Cards Card Soldier)")
    regions["Floor 2"].locations.append("Wonderland Room of Guidance")
    regions["Floor 2"].locations.append("Wonderland Room of Truth")
    regions["Floor 2"].locations.append("Wonderland Room of Truth (Enemy Cards Trickmaster)")
    
    regions["Floor 3"].locations.append("Olympus Coliseum Field (Attack Card Olympia)")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Beginnings")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Guidance")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Truth")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Truth (Enemy Cards Hades)")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Truth (Summon Cards Cloud)")
    regions["Floor 3"].locations.append("Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)")
    
    regions["Floor 4"].locations.append("Monstro Field (Attack Cards Wishing Star)")
    regions["Floor 4"].locations.append("Monstro Room of Beginnings")
    regions["Floor 4"].locations.append("Monstro Room of Guidance")
    regions["Floor 4"].locations.append("Monstro Room of Guidance (Enemy Cards Parasite Cage)")
    regions["Floor 4"].locations.append("Monstro Room of Truth")
    regions["Floor 4"].locations.append("Monstro Room of Truth (Summon Cards Dumbo)")
    
    regions["Floor 5"].locations.append("Agrabah Bounty (Magic Cards Gravity)")
    regions["Floor 5"].locations.append("Agrabah Field (Attack Cards Three Wishes)")
    regions["Floor 5"].locations.append("Agrabah Room of Beginnings")
    regions["Floor 5"].locations.append("Agrabah Room of Guidance")
    regions["Floor 5"].locations.append("Agrabah Room of Guidance (Item Cards Ether)")
    regions["Floor 5"].locations.append("Agrabah Room of Truth")
    regions["Floor 5"].locations.append("Agrabah Room of Truth (Enemy Cards Jafar)")
    regions["Floor 5"].locations.append("Agrabah Room of Truth (Summon Cards Genie)")
    
    regions["Floor 6"].locations.append("Halloween Town Field (Attack Cards Pumpkinhead)")
    regions["Floor 6"].locations.append("Halloween Town Post Floor (Magic Cards Thunder)")
    regions["Floor 6"].locations.append("Halloween Town Room of Beginnings")
    regions["Floor 6"].locations.append("Halloween Town Room of Guidance")
    regions["Floor 6"].locations.append("Halloween Town Room of Truth")
    regions["Floor 6"].locations.append("Halloween Town Room of Truth (Enemy Cards Oogie Boogie)")
    
    regions["Floor 7"].locations.append("Atlantica Field (Attack Cards Crabclaw)")
    regions["Floor 7"].locations.append("Atlantica Post Floor (Magic Cards Aero)")
    regions["Floor 7"].locations.append("Atlantica Room of Beginnings")
    regions["Floor 7"].locations.append("Atlantica Room of Guidance")
    regions["Floor 7"].locations.append("Atlantica Room of Truth")
    regions["Floor 7"].locations.append("Atlantica Room of Truth (Enemy Cards Ursula)")
    
    regions["Floor 8"].locations.append("Neverland Field (Attack Cards Fairy Harp)")
    regions["Floor 8"].locations.append("Neverland Room of Beginnings")
    regions["Floor 8"].locations.append("Neverland Room of Guidance")
    regions["Floor 8"].locations.append("Neverland Room of Truth")
    regions["Floor 8"].locations.append("Neverland Room of Truth (Enemy Cards Hook)")
    regions["Floor 8"].locations.append("Neverland Room of Truth (Summon Cards Tinker Bell)")
    
    regions["Floor 9"].locations.append("Hollow Bastion Field (Attack Cards Divine Rose)")
    regions["Floor 9"].locations.append("Hollow Bastion Room of Beginnings")
    regions["Floor 9"].locations.append("Hollow Bastion Room of Guidance")
    regions["Floor 9"].locations.append("Hollow Bastion Room of Truth")
    regions["Floor 9"].locations.append("Hollow Bastion Room of Truth (Enemy Cards Dragon Maleficent)")
    regions["Floor 9"].locations.append("Hollow Bastion Room of Rewards (Summon Cards Mushu)")
    
    regions["Floor 10"].locations.append("100 Acre Wood Clear (Summon Cards Bambi)")
    regions["Floor 10"].locations.append("100 Acre Wood Mini Game Bumble Rumble (Item Cards Elixir)")
    regions["Floor 10"].locations.append("100 Acre Wood Mini Game Whirlwind Plunge (Item Cards Mega-Ether)")
    regions["Floor 10"].locations.append("100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)")
    
   #regions["Floor 11"].locations.append("Twilight Town Post Floor (Item Cards Mega-Potion)") Bugged because of the post floor scene?
    regions["Floor 11"].locations.append("Twilight Town Room of Beginnings")
    regions["Floor 11"].locations.append("Twilight Town Room of Beginnings (Enemy Cards Vexen)")
    
    regions["Floor 12"].locations.append("Destiny Islands Post Floor (Attack Cards Oathkeeper)")
    regions["Floor 12"].locations.append("Destiny Islands Post Floor (Attack Cards Oblivion)")
    regions["Floor 12"].locations.append("Destiny Islands Post Floor (Enemy Cards Larxene)")
    regions["Floor 12"].locations.append("Destiny Islands Post Floor (Enemy Cards Riku)")
    regions["Floor 12"].locations.append("Destiny Islands Room of Beginnings")
    regions["Floor 12"].locations.append("Destiny Islands Room of Guidance")
    regions["Floor 12"].locations.append("Destiny Islands Room of Guidance (Enemy Cards Darkside)")
    regions["Floor 12"].locations.append("Destiny Islands Room of Rewards (Item Cards Megalixir)")
    
    regions["Floor 13"].locations.append("Castle Oblivion Field Marluxia")
    regions["Floor 13"].locations.append("Castle Oblivion Room of Beginnings")
    regions["Floor 13"].locations.append("Castle Oblivion Room of Beginnings (Enemy Cards Axel)")
    
    regions["Heartless"].locations.append("Heartless Air Pirate")                                              
    regions["Heartless"].locations.append("Heartless Air Soldier")                                             
    regions["Heartless"].locations.append("Heartless Aquatank")                                                
    regions["Heartless"].locations.append("Heartless Bandit")                                                  
    regions["Heartless"].locations.append("Heartless Barrel Spider")                                           
    regions["Heartless"].locations.append("Heartless Black Fungus")                                            
    regions["Heartless"].locations.append("Heartless Blue Rhapsody")                                           
    regions["Heartless"].locations.append("Heartless Bouncywild")                                              
    regions["Heartless"].locations.append("Heartless Creeper Plant")                                           
    regions["Heartless"].locations.append("Heartless Crescendo")                                               
    regions["Heartless"].locations.append("Heartless Darkball")                                                
    regions["Heartless"].locations.append("Heartless Defender")                                                
    regions["Heartless"].locations.append("Heartless Fat Bandit")                                              
    regions["Heartless"].locations.append("Heartless Gargoyle")                                                
    regions["Heartless"].locations.append("Heartless Green Requiem")                                           
    regions["Heartless"].locations.append("Heartless Large Body")                                              
    regions["Heartless"].locations.append("Heartless Neoshadow")                                               
    regions["Heartless"].locations.append("Heartless Pirate")                                                  
    regions["Heartless"].locations.append("Heartless Powerwild")                                               
    regions["Heartless"].locations.append("Heartless Red Nocturne")                                            
    regions["Heartless"].locations.append("Heartless Screwdiver")                                              
    regions["Heartless"].locations.append("Heartless Sea Neon")                                                
    regions["Heartless"].locations.append("Heartless Search Ghost")                                            
    regions["Heartless"].locations.append("Heartless Shadow")                                                  
    regions["Heartless"].locations.append("Heartless Soldier")                                                 
    regions["Heartless"].locations.append("Heartless Tornado Step")                                            
    regions["Heartless"].locations.append("Heartless White Mushroom")                                          
    regions["Heartless"].locations.append("Heartless Wight Knight")                                            
    regions["Heartless"].locations.append("Heartless Wizard")                                                  
    regions["Heartless"].locations.append("Heartless Wyvern")                                                  
    regions["Heartless"].locations.append("Heartless Yellow Opera")                                            
    
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
    multiworld.get_entrance("Heartless", player).connect(multiworld.get_region("Heartless", player))
    multiworld.get_entrance("Warp", player).connect(multiworld.get_region("Warp", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: KHRECOMRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = KHRECOMLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
