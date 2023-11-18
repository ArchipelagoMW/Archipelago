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
        "Heartless":KHCOMRegionData([], []),
        "Warp":     KHCOMRegionData([], ["Floor 2", "Floor 3", "Floor 4",
                                         "Floor 5", "Floor 6", "Floor 7",
                                         "Floor 8", "Floor 9", "Floor 10",
                                         "Floor 11", "Floor 12", "Floor 13", "Heartless"])
    }

    # Set up locations
    
    regions["Floor 1"].locations.append("Starting Checks (Attack Cards Kingdom Key)")                        
    regions["Floor 1"].locations.append("Starting Checks (Characters I Donald)")                             
    regions["Floor 1"].locations.append("Starting Checks (Characters I Goofy)")                              
    regions["Floor 1"].locations.append("Starting Checks (Characters I Jiminy Cricket)")                     
    regions["Floor 1"].locations.append("Starting Checks (Characters I Kairi)")                              
    regions["Floor 1"].locations.append("Starting Checks (Characters I Riku)")                               
    regions["Floor 1"].locations.append("Starting Checks (Characters I Sora)")                               
    regions["Floor 1"].locations.append("Starting Checks (Item Cards Potion)")                               
    regions["Floor 1"].locations.append("Starting Checks (Magic Cards Blizzard)")                            
    regions["Floor 1"].locations.append("Starting Checks (Magic Cards Cure)")                                
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Characters I Aerith)")                
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Characters I Axel)")                  
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Characters I Cid)")                   
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Characters I Leon)")                  
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Characters I Yuffie)")                
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Magic Cards Fire)")                   
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Story Sora's Tale I)")                
    regions["Floor 1"].locations.append("F01 Traverse Town Post Floor (Story Traverse Town)")                
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Beginnings (Characters I Simba)")         
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Beginnings (Magic Cards Simba)")          
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Rewards (Attack Cards Lionheart)")        
    regions["Floor 1"].locations.append("F01 Traverse Town Room of Truth (The Heartless Guard Armor)")       
    
    regions["Floor 2"].locations.append("F02 Wonderland Bounty (Magic Cards Stop)")                          
    regions["Floor 2"].locations.append("F02 Wonderland Field (Attack Cards Lady Luck)")                     
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II Alice)")                   
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II Card of Hearts)")          
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II Card of Spades)")          
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II The Cheshire Cat)")        
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II The Queen of Hearts)")     
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Characters II The White Rabbit)")        
    regions["Floor 2"].locations.append("F02 Wonderland Post Floor (Story Wonderland)")                      
    regions["Floor 2"].locations.append("F02 Wonderland Room of Truth (The Heartless Trickmaster)")          
    
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Field (Attack Cards Olympia)")                 
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Post Floor (Characters I Cloud)")              
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Post Floor (Characters II Hades)")             
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Post Floor (Characters II Philoctetes)")       
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Post Floor (Characters II Hercules)")          
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Post Floor (Story Olympus Coliseum)")          
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)")      
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Rewards (Attack Card Metal Chocobo)")  
    regions["Floor 3"].locations.append("F03 Olympus Coliseum Room of Truth (Magic Cards Cloud)")            
    
    regions["Floor 4"].locations.append("F04 Monstro Field (Wishing Star)")                                  
    regions["Floor 4"].locations.append("F04 Monstro Post Floor (Characters II Geppetto)")                   
    regions["Floor 4"].locations.append("F04 Monstro Post Floor (Characters II Pinocchio)")                  
    regions["Floor 4"].locations.append("F04 Monstro Post Floor (Story Monstro)")                            
    regions["Floor 4"].locations.append("F04 Monstro Room of Guidance (The Heartless Parasite Cage)")        
    regions["Floor 4"].locations.append("F04 Monstro Room of Truth (Characters I Dumbo)")                    
    regions["Floor 4"].locations.append("F04 Monstro Room of Truth (Magic Cards Dumbo)")                     
    
    regions["Floor 5"].locations.append("F05 Agrabah Bounty (Magic Cards Gravity)")                          
    regions["Floor 5"].locations.append("F05 Agrabah Field (Attack Cards Three Wishes)")                     
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Aladdin)")                    
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Genie)")                      
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Iago)")                       
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Jafar)")                      
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Jafar-Genie)")                
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Characters II Jasmine)")                    
    regions["Floor 5"].locations.append("F05 Agrabah Post Floor (Story Agrabah)")                            
    regions["Floor 5"].locations.append("F05 Agrabah Room of Guidance (Item Cards Ether)")                   
    regions["Floor 5"].locations.append("F05 Agrabah Room of Truth (Magic Cards Genie)")                     
    
    regions["Floor 6"].locations.append("F06 Halloween Town Field (Attack Cards Pumpkinhead)")               
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Characters II Dr. Finkelstein)")     
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Characters II Jack)")                
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Characters II Oogie Boogie)")        
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Characters II Sally)")               
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Magic Cards Thunder)")               
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Story Halloween Town)")              
    regions["Floor 6"].locations.append("F06 Halloween Town Post Floor (Story Sora's Tale II)")              
    
    regions["Floor 7"].locations.append("F07 Atlantica Field (Crabclaw)")                                    
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Characters II Ariel)")                    
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Characters II Flounder)")                 
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Characters II Ursula)")                   
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Characters II Sebastion)")                
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Story Atlantica)")                        
    regions["Floor 7"].locations.append("F07 Atlantica Post Floor (Magic Cards Aero)")                       
    
    regions["Floor 8"].locations.append("F08 Neverland Field (Attack Cards Fairy Harp)")                     
    regions["Floor 8"].locations.append("F08 Neverland Post Floor (Characters II Hook)")                     
    regions["Floor 8"].locations.append("F08 Neverland Post Floor (Characters II Peter Pan)")                
    regions["Floor 8"].locations.append("F08 Neverland Post Floor (Characters II Tinker Bell)")              
    regions["Floor 8"].locations.append("F08 Neverland Post Floor (Characters II Wendy)")                    
    regions["Floor 8"].locations.append("F08 Neverland Post Floor (Story Neverland)")                        
    regions["Floor 8"].locations.append("F08 Neverland Room of Truth (Magic Cards Tinker Bell)")             
    
    regions["Floor 9"].locations.append("F09 Hollow Bastion Field (Attack Cards Divine Rose)")               
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Characters II Belle)")               
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Characters II Dragon Maleficent)")   
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Characters II Maleficent)")          
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Characters II The Beast)")           
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Story Hollow Bastion)")              
    regions["Floor 9"].locations.append("F09 Hollow Bastion Post Floor (Story Sora's Tale III)")             
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Rewards (Characters I Mushu)")           
    regions["Floor 9"].locations.append("F09 Hollow Bastion Room of Rewards (Magic Cards Mushu)")            
    
    regions["Floor 10"].locations.append("F10 100 Acre Wood Complete (Characters I Bambi)")                   
    regions["Floor 10"].locations.append("F10 100 Acre Wood Complete (Magic Cards Bambi)")                    
    regions["Floor 10"].locations.append("F10 100 Acre Wood Owl (Attack Cards Spellbinder)")                  
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Eeyore (Characters II Eeyore)")               
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Owl (Characters II Owl)")                  
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Piglet (Characters II Piglet)")               
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Rabbit (Characters II Rabbit)")               
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Roo (Characters II Roo)")                  
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Tigger (Characters II Tigger)")               
    regions["Floor 10"].locations.append("F10 100 Acre Wood Post Floor (Characters II Vexen)")                
    regions["Floor 10"].locations.append("F10 100 Acre Wood Post Floor (Characters II Winnie the Pooh)")      
    regions["Floor 10"].locations.append("F10 100 Acre Wood Post Floor (Item Cards Mega-Ether)")              
    regions["Floor 10"].locations.append("F10 100 Acre Wood Post Floor (Story 100 Acre Wood)")                
    regions["Floor 10"].locations.append("F10 100 Acre Wood Field Scene Roo (Item Cards Elixir)")                         
    
    regions["Floor 11"].locations.append("F11 Twilight Town Post Floor (Item Cards Mega-Potion)")             
    regions["Floor 11"].locations.append("F11 Twilight Town Post Floor (Story Twilight Town)")                
    
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Attack Cards Oathkeeper)")          
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Characters I Selphie)")             
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Characters I Tidus)")               
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Characters I Wakka)")               
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Characters I Riku Replica)")        
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Characters I Namine)")              
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Story Destiny Islands)")            
    regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Story Sora's Tale IV)")             
    regions["Floor 12"].locations.append("F12 Destiny Islands Room of Truth (The Heartless Darkside)")        
    #regions["Floor 12"].locations.append("F12 Destiny Islands Post Floor (Attack Cards Oblivion)")           
    regions["Floor 12"].locations.append("F12 Destiny Islands Room of Rewards (Item Cards Megalixir)")        
                                                                         
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Floor (Characters I Marluxia)")            
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Floor (Story Castle Oblivion)")            
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Marluxia (Attack Cards Diamond Dust)")     
    regions["Floor 13"].locations.append("F13 Castle Oblivion Post Marluxia (Attack Cards One-Winged Angel)") 
    
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
