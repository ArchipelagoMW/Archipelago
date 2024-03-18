from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KHRECOMLocation, location_table, get_locations_by_category


class KHRECOMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int, options):
    regions: Dict[str, KHRECOMRegionData] = {
        "Menu":     KHRECOMRegionData(None, ["Traverse Town"]),
        "Traverse Town":  KHRECOMRegionData([], ["Castle Oblivion Halls"]),
        "Wonderland":  KHRECOMRegionData([], []),
        "Olympus Coliseum":  KHRECOMRegionData([], []),
        "Monstro":  KHRECOMRegionData([], []),
        "Agrabah":  KHRECOMRegionData([], []),
        "Halloween Town":  KHRECOMRegionData([], []),
        "Atlantica":  KHRECOMRegionData([], []),
        "Neverland":  KHRECOMRegionData([], []),
        "Hollow Bastion":  KHRECOMRegionData([], []),
        "100 Acre Wood": KHRECOMRegionData([], []),
        "Twilight Town": KHRECOMRegionData([], []),
        "Destiny Islands": KHRECOMRegionData([], []),
        "Castle Oblivion": KHRECOMRegionData([], []),
        "Heartless":KHRECOMRegionData([], []),
        "Levels":KHRECOMRegionData([], []),
        "Castle Oblivion Halls":     KHRECOMRegionData([], ["Wonderland", "Olympus Coliseum", "Monstro",
                                         "Agrabah", "Halloween Town", "Atlantica",
                                         "Neverland", "Hollow Bastion", "100 Acre Wood",
                                         "Twilight Town", "Destiny Islands", "Castle Oblivion", "Heartless", "Levels"])
    }

    # Set up locations

    regions["Traverse Town"].locations.append("Starting Checks (Attack Cards Kingdom Key)")
    regions["Traverse Town"].locations.append("Starting Checks (Item Cards Potion)")
    regions["Traverse Town"].locations.append("Starting Checks (Magic Cards Blizzard)")
    regions["Traverse Town"].locations.append("Starting Checks (Magic Cards Cure)")
    if options.checks_behind_leon:
        regions["Traverse Town"].locations.append("Traverse Town Room of Beginnings")
        regions["Traverse Town"].locations.append("Traverse Town Room of Beginnings (Summon Cards Simba)")
    regions["Traverse Town"].locations.append("Traverse Town Room of Guidance")
    regions["Traverse Town"].locations.append("Traverse Town Room of Truth")
    regions["Traverse Town"].locations.append("Traverse Town Room of Truth (Enemy Cards Guard Armor)")
    regions["Traverse Town"].locations.append("Traverse Town Room of Rewards (Attack Cards Lionheart)")
    if options.days_locations:
        regions["Traverse Town"].locations.append("Traverse Town Bounty (Attack Cards Maverick Flare)")
        regions["Traverse Town"].locations.append("Traverse Town Room of Rewards (Enemy Cards Saix)")
    
    regions["Wonderland"].locations.append("Wonderland Bounty (Magic Cards Stop)")
    regions["Wonderland"].locations.append("Wonderland Field (Attack Cards Lady Luck)")
    regions["Wonderland"].locations.append("Wonderland Room of Beginnings")
    regions["Wonderland"].locations.append("Wonderland Room of Beginnings (Enemy Cards Card Soldier)")
    regions["Wonderland"].locations.append("Wonderland Room of Guidance")
    regions["Wonderland"].locations.append("Wonderland Room of Truth")
    regions["Wonderland"].locations.append("Wonderland Room of Truth (Enemy Cards Trickmaster)")
    if options.days_locations:
        regions["Wonderland"].locations.append("Wonderland Room of Rewards (Enemy Cards Xemnas)")
    
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Field (Attack Card Olympia)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Beginnings")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Guidance")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Truth")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Truth (Enemy Cards Hades)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Truth (Summon Cards Cloud)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)")
    if options.days_locations:
        regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Rewards (Attack Cards Total Eclipse)")
    
    regions["Monstro"].locations.append("Monstro Field (Attack Cards Wishing Star)")
    regions["Monstro"].locations.append("Monstro Room of Beginnings")
    regions["Monstro"].locations.append("Monstro Room of Guidance")
    regions["Monstro"].locations.append("Monstro Room of Guidance (Enemy Cards Parasite Cage)")
    regions["Monstro"].locations.append("Monstro Room of Truth")
    regions["Monstro"].locations.append("Monstro Room of Truth (Summon Cards Dumbo)")
    if options.days_locations:
        regions["Monstro"].locations.append("Monstro Room of Rewards (Enemy Cards Xaldin)")
    
    regions["Agrabah"].locations.append("Agrabah Bounty (Magic Cards Gravity)")
    regions["Agrabah"].locations.append("Agrabah Field (Attack Cards Three Wishes)")
    regions["Agrabah"].locations.append("Agrabah Room of Beginnings")
    regions["Agrabah"].locations.append("Agrabah Room of Guidance")
    regions["Agrabah"].locations.append("Agrabah Room of Guidance (Item Cards Ether)")
    regions["Agrabah"].locations.append("Agrabah Room of Truth")
    regions["Agrabah"].locations.append("Agrabah Room of Truth (Enemy Cards Jafar)")
    regions["Agrabah"].locations.append("Agrabah Room of Truth (Summon Cards Genie)")
    if options.days_locations:
        regions["Agrabah"].locations.append("Agrabah Room of Rewards (Enemy Cards Luxord)")
    
    regions["Halloween Town"].locations.append("Halloween Town Field (Attack Cards Pumpkinhead)")
    regions["Halloween Town"].locations.append("Halloween Town Room of Beginnings")
    regions["Halloween Town"].locations.append("Halloween Town Room of Guidance")
    regions["Halloween Town"].locations.append("Halloween Town Room of Truth")
    regions["Halloween Town"].locations.append("Halloween Town Room of Truth (Enemy Cards Oogie Boogie)")
    if options.days_locations:
        regions["Halloween Town"].locations.append("Halloween Town Room of Rewards (Attack Cards Bond of Flame)")
    
    regions["Atlantica"].locations.append("Atlantica Field (Attack Cards Crabclaw)")
    regions["Atlantica"].locations.append("Atlantica Room of Beginnings")
    regions["Atlantica"].locations.append("Atlantica Room of Guidance")
    regions["Atlantica"].locations.append("Atlantica Room of Truth")
    regions["Atlantica"].locations.append("Atlantica Room of Truth (Enemy Cards Ursula)")
    if options.days_locations:
        regions["Atlantica"].locations.append("Atlantica Room of Rewards (Enemy Cards Demyx)")
    
    regions["Neverland"].locations.append("Neverland Field (Attack Cards Fairy Harp)")
    regions["Neverland"].locations.append("Neverland Room of Beginnings")
    regions["Neverland"].locations.append("Neverland Room of Guidance")
    regions["Neverland"].locations.append("Neverland Room of Truth")
    regions["Neverland"].locations.append("Neverland Room of Truth (Enemy Cards Hook)")
    regions["Neverland"].locations.append("Neverland Room of Truth (Summon Cards Tinker Bell)")
    if options.days_locations:
        regions["Neverland"].locations.append("Neverland Room of Rewards (Attack Cards Midnight Roar)")
    
    regions["Hollow Bastion"].locations.append("Hollow Bastion Field (Attack Cards Divine Rose)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Beginnings")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Guidance")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Truth")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Truth (Enemy Cards Dragon Maleficent)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Rewards (Summon Cards Mushu)")
    if options.days_locations:
        regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Rewards (Enemy Cards Xigbar)")
    
    regions["100 Acre Wood"].locations.append("100 Acre Wood Clear (Summon Cards Bambi)")
    if options.minigames:
        regions["100 Acre Wood"].locations.append("100 Acre Wood Bumble Rumble (Item Cards Elixir)")
        regions["100 Acre Wood"].locations.append("100 Acre Wood Whirlwind Plunge (Item Cards Mega-Ether)")
    regions["100 Acre Wood"].locations.append("100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)")
    
   #regions["Twilight Town"].locations.append("11F Exit Hall Riku III (Item Cards Mega-Potion)")
    regions["Twilight Town"].locations.append("Twilight Town Room of Beginnings")
    regions["Twilight Town"].locations.append("Twilight Town Room of Beginnings (Enemy Cards Vexen)")
    if options.days_locations:
        regions["Twilight Town"].locations.append("Twilight Town Room of Rewards (Enemy Cards Roxas)")
       #regions["Twilight Town"].locations.append("Twilight Town Bounty (Enemy Cards Ansem)")
    
    regions["Destiny Islands"].locations.append("Destiny Islands Room of Guidance (Attack Cards Oathkeeper)")
    regions["Destiny Islands"].locations.append("Destiny Islands Room of Beginnings")
    regions["Destiny Islands"].locations.append("Destiny Islands Room of Guidance")
    regions["Destiny Islands"].locations.append("Destiny Islands Room of Guidance (Enemy Cards Darkside)")
    regions["Destiny Islands"].locations.append("Destiny Islands Room of Rewards (Item Cards Megalixir)")
    if options.days_locations:
       #regions["Destiny Islands"].locations.append("Destiny Islands Bounty (Enemy Cards Zexion)")
        regions["Destiny Islands"].locations.append("Destiny Islands Room of Rewards (Attack Cards Two Become One)")
    
    regions["Castle Oblivion"].locations.append("Castle Oblivion Field Marluxia")
    regions["Castle Oblivion"].locations.append("Castle Oblivion Room of Beginnings")
    regions["Castle Oblivion"].locations.append("Castle Oblivion Room of Beginnings (Enemy Cards Axel)")
    if options.days_locations:
       #regions["Castle Oblivion"].locations.append("Castle Oblivion Bounty (Enemy Cards Lexaeus)")
        regions["Castle Oblivion"].locations.append("Castle Oblivion Room of Rewards (Attack Cards Star Seeker)")
    
    regions["Castle Oblivion"].locations.append("Final Marluxia")
    
    regions["Castle Oblivion Halls"].locations.append("01F Exit Hall Axel I (Magic Cards Fire)")
    regions["Castle Oblivion Halls"].locations.append("06F Exit Hall Larxene I (Magic Cards Thunder)")
    regions["Castle Oblivion Halls"].locations.append("07F Exit Hall Riku I (Magic Cards Aero)")
    regions["Castle Oblivion Halls"].locations.append("12F Exit Hall Larxene II (Attack Cards Oblivion)")
    regions["Castle Oblivion Halls"].locations.append("12F Exit Hall Larxene II (Enemy Cards Larxene)")
    regions["Castle Oblivion Halls"].locations.append("12F Exit Hall Riku IV (Enemy Cards Riku)")
    
    regions["Heartless"].locations.append("Defeat 1 Heartless Air Pirate")                                              
    regions["Heartless"].locations.append("Defeat 2 Heartless Air Pirate")                                              
    regions["Heartless"].locations.append("Defeat 3 Heartless Air Pirate")                                              
    regions["Heartless"].locations.append("Defeat 1 Heartless Air Soldier")                                             
    regions["Heartless"].locations.append("Defeat 2 Heartless Air Soldier")                                             
    regions["Heartless"].locations.append("Defeat 3 Heartless Air Soldier")                                             
    regions["Heartless"].locations.append("Defeat 1 Heartless Aquatank")                                                
    regions["Heartless"].locations.append("Defeat 2 Heartless Aquatank")                                                
    regions["Heartless"].locations.append("Defeat 3 Heartless Aquatank")                                                
    regions["Heartless"].locations.append("Defeat 1 Heartless Bandit")                                                  
    regions["Heartless"].locations.append("Defeat 2 Heartless Bandit")                                                  
    regions["Heartless"].locations.append("Defeat 3 Heartless Bandit")                                                  
    regions["Heartless"].locations.append("Defeat 1 Heartless Barrel Spider")                                           
    regions["Heartless"].locations.append("Defeat 2 Heartless Barrel Spider")                                           
    regions["Heartless"].locations.append("Defeat 3 Heartless Barrel Spider")                                           
    regions["Heartless"].locations.append("Defeat 1 Heartless Black Fungus")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Black Fungus")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Black Fungus")                                            
    regions["Heartless"].locations.append("Defeat 1 Heartless Blue Rhapsody")                                           
    regions["Heartless"].locations.append("Defeat 2 Heartless Blue Rhapsody")                                           
    regions["Heartless"].locations.append("Defeat 3 Heartless Blue Rhapsody")                                           
    regions["Heartless"].locations.append("Defeat 1 Heartless Bouncywild")                                              
    regions["Heartless"].locations.append("Defeat 2 Heartless Bouncywild")                                              
    regions["Heartless"].locations.append("Defeat 3 Heartless Bouncywild")                                              
    regions["Heartless"].locations.append("Defeat 1 Heartless Creeper Plant")                                           
    regions["Heartless"].locations.append("Defeat 2 Heartless Creeper Plant")                                           
    regions["Heartless"].locations.append("Defeat 3 Heartless Creeper Plant")                                           
    regions["Heartless"].locations.append("Defeat 1 Heartless Crescendo")                                               
    regions["Heartless"].locations.append("Defeat 2 Heartless Crescendo")                                               
    regions["Heartless"].locations.append("Defeat 3 Heartless Crescendo")                                               
    regions["Heartless"].locations.append("Defeat 1 Heartless Darkball")                                                
    regions["Heartless"].locations.append("Defeat 2 Heartless Darkball")                                                
    regions["Heartless"].locations.append("Defeat 3 Heartless Darkball")                                                
    regions["Heartless"].locations.append("Defeat 1 Heartless Defender")                                                
    regions["Heartless"].locations.append("Defeat 2 Heartless Defender")                                                
    regions["Heartless"].locations.append("Defeat 3 Heartless Defender")                                                
    regions["Heartless"].locations.append("Defeat 1 Heartless Fat Bandit")                                              
    regions["Heartless"].locations.append("Defeat 2 Heartless Fat Bandit")                                              
    regions["Heartless"].locations.append("Defeat 3 Heartless Fat Bandit")                                              
    regions["Heartless"].locations.append("Defeat 1 Heartless Gargoyle")                                                
    regions["Heartless"].locations.append("Defeat 2 Heartless Gargoyle")                                                
    regions["Heartless"].locations.append("Defeat 3 Heartless Gargoyle")                                                
    regions["Heartless"].locations.append("Defeat 1 Heartless Green Requiem")                                           
    regions["Heartless"].locations.append("Defeat 2 Heartless Green Requiem")                                           
    regions["Heartless"].locations.append("Defeat 3 Heartless Green Requiem")                                           
    regions["Heartless"].locations.append("Defeat 1 Heartless Large Body")                                              
    regions["Heartless"].locations.append("Defeat 2 Heartless Large Body")                                              
    regions["Heartless"].locations.append("Defeat 3 Heartless Large Body")                                              
    regions["Heartless"].locations.append("Defeat 1 Heartless Neoshadow")                                               
    regions["Heartless"].locations.append("Defeat 2 Heartless Neoshadow")                                               
    regions["Heartless"].locations.append("Defeat 3 Heartless Neoshadow")                                               
    regions["Heartless"].locations.append("Defeat 1 Heartless Pirate")                                                  
    regions["Heartless"].locations.append("Defeat 2 Heartless Pirate")                                                  
    regions["Heartless"].locations.append("Defeat 3 Heartless Pirate")                                                  
    regions["Heartless"].locations.append("Defeat 1 Heartless Powerwild")                                               
    regions["Heartless"].locations.append("Defeat 2 Heartless Powerwild")                                               
    regions["Heartless"].locations.append("Defeat 3 Heartless Powerwild")                                               
    regions["Heartless"].locations.append("Defeat 1 Heartless Red Nocturne")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Red Nocturne")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Red Nocturne")                                            
    regions["Heartless"].locations.append("Defeat 1 Heartless Screwdiver")                                              
    regions["Heartless"].locations.append("Defeat 2 Heartless Screwdiver")                                              
    regions["Heartless"].locations.append("Defeat 3 Heartless Screwdiver")                                              
    regions["Heartless"].locations.append("Defeat 1 Heartless Sea Neon")                                                
    regions["Heartless"].locations.append("Defeat 2 Heartless Sea Neon")                                                
    regions["Heartless"].locations.append("Defeat 3 Heartless Sea Neon")                                                
    regions["Heartless"].locations.append("Defeat 1 Heartless Search Ghost")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Search Ghost")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Search Ghost")                                            
    regions["Heartless"].locations.append("Defeat 1 Heartless Shadow")                                                  
    regions["Heartless"].locations.append("Defeat 2 Heartless Shadow")                                                  
    regions["Heartless"].locations.append("Defeat 3 Heartless Shadow")                                                  
    regions["Heartless"].locations.append("Defeat 1 Heartless Soldier")                                                 
    regions["Heartless"].locations.append("Defeat 2 Heartless Soldier")                                                 
    regions["Heartless"].locations.append("Defeat 3 Heartless Soldier")                                                 
    regions["Heartless"].locations.append("Defeat 1 Heartless Tornado Step")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Tornado Step")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Tornado Step")                                            
    regions["Heartless"].locations.append("Defeat 1 Heartless White Mushroom")                                          
    regions["Heartless"].locations.append("Defeat 2 Heartless White Mushroom")                                          
    regions["Heartless"].locations.append("Defeat 3 Heartless White Mushroom")                                          
    regions["Heartless"].locations.append("Defeat 1 Heartless Wight Knight")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Wight Knight")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Wight Knight")                                            
    regions["Heartless"].locations.append("Defeat 1 Heartless Wizard")                                                  
    regions["Heartless"].locations.append("Defeat 2 Heartless Wizard")                                                  
    regions["Heartless"].locations.append("Defeat 3 Heartless Wizard")                                                  
    regions["Heartless"].locations.append("Defeat 1 Heartless Wyvern")                                                  
    regions["Heartless"].locations.append("Defeat 2 Heartless Wyvern")                                                  
    regions["Heartless"].locations.append("Defeat 3 Heartless Wyvern")                                                  
    regions["Heartless"].locations.append("Defeat 1 Heartless Yellow Opera")                                            
    regions["Heartless"].locations.append("Defeat 2 Heartless Yellow Opera")                                            
    regions["Heartless"].locations.append("Defeat 3 Heartless Yellow Opera")                                            
    
    if options.levels:
        regions["Levels"].locations.append("Level 02 (Sleight Sliding Dash)")
        regions["Levels"].locations.append("Level 07 (Sleight Stun Impact)")
        regions["Levels"].locations.append("Level 12 (Sleight Strike Raid)")
        regions["Levels"].locations.append("Level 17 (Sleight Blitz)")
        regions["Levels"].locations.append("Level 22 (Sleight Zantetsuken)")
        regions["Levels"].locations.append("Level 27 (Sleight Sonic Blade)")
        regions["Levels"].locations.append("Level 32 (Sleight Lethal Frame)")
        regions["Levels"].locations.append("Level 37 (Sleight Tornado)")
        regions["Levels"].locations.append("Level 42 (Sleight Ars Arcanum)")
        regions["Levels"].locations.append("Level 47 (Sleight Holy)")
        regions["Levels"].locations.append("Level 52 (Sleight Ragnarok)")
        regions["Levels"].locations.append("Level 57 (Sleight Mega Flare)")
    if options.minigames:
        regions["100 Acre Wood"].locations.append("100 Acre Wood Balloon Glider (Sleight Firaga Burst)")
        regions["100 Acre Wood"].locations.append("100 Acre Wood Veggie Panic (Sleight Cross-slash+)")
        regions["100 Acre Wood"].locations.append("100 Acre Wood Jump-a-Thon (Sleight Idyll Romp)")
    regions["100 Acre Wood"].locations.append("100 Acre Wood Clear (Sleight Paradise LV2)")
    regions["100 Acre Wood"].locations.append("100 Acre Wood Clear (Sleight Paradise LV3)")
    regions["100 Acre Wood"].locations.append("100 Acre Wood Piglet (Sleight Confuse)")
    regions["Agrabah"].locations.append("Agrabah Bounty (Sleight Graviga)")
    regions["Agrabah"].locations.append("Agrabah Bounty (Sleight Gravira)")
    regions["Agrabah"].locations.append("Agrabah Ally (Sleight Sandstorm LV2)")
    regions["Agrabah"].locations.append("Agrabah Ally (Sleight Sandstorm LV3)")
    regions["Agrabah"].locations.append("Agrabah Room of Rewards (Sleight Warp)")
    regions["Agrabah"].locations.append("Agrabah Room of Truth (Sleight Showtime LV2)")
    regions["Agrabah"].locations.append("Agrabah Room of Truth (Sleight Showtime LV3)")
    regions["Atlantica"].locations.append("Atlantica Bounty (Sleight Homing Blizzara)")
    regions["Atlantica"].locations.append("Atlantica Bounty (Sleight Shock Impact)")
    regions["Atlantica"].locations.append("Atlantica Ally (Sleight Spiral Wave LV2)")
    regions["Atlantica"].locations.append("Atlantica Ally (Sleight Spiral Wave LV3)")
    regions["Atlantica"].locations.append("Atlantica Room of Rewards (Sleight Quake)")
    regions["Castle Oblivion Halls"].locations.append("01F Exit Hall Axel I (Sleight Fira)")
    regions["Castle Oblivion Halls"].locations.append("01F Exit Hall Axel I (Sleight Firaga)")
    regions["Castle Oblivion Halls"].locations.append("06F Exit Hall Larxene I (Sleight Thundara)")
    regions["Castle Oblivion Halls"].locations.append("06F Exit Hall Larxene I (Sleight Thundaga)")
    regions["Castle Oblivion Halls"].locations.append("07F Exit Hall Riku I (Sleight Aeroga)")
    regions["Castle Oblivion Halls"].locations.append("07F Exit Hall Riku I (Sleight Aerora)")
   #regions["Castle Oblivion Halls"].locations.append("08F Exit Hall Riku II (Sleight Magnet Spiral)")
    regions["Castle Oblivion Halls"].locations.append("10F Exit Hall Vexen I (Sleight Freeze)")
    regions["Castle Oblivion"].locations.append("Castle Oblivion Bounty (Sleight Raging Storm)")
    regions["Castle Oblivion"].locations.append("Castle Oblivion Entrance (Sleight Trinity Limit)")
    regions["Destiny Islands"].locations.append("Destiny Islands Bounty (Sleight Judgment)")
    regions["Halloween Town"].locations.append("Halloween Town Bounty (Sleight Gifted Miracle)")
    regions["Halloween Town"].locations.append("Halloween Town Ally (Sleight Surprise! LV2)")
    regions["Halloween Town"].locations.append("Halloween Town Ally (Sleight Surprise! LV3)")
    regions["Halloween Town"].locations.append("Halloween Town Entrance (Sleight Terror)")
    regions["Halloween Town"].locations.append("Halloween Town Room of Rewards (Sleight Bind)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Bounty (Sleight Reflect Raid)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Ally (Sleight Furious Volley LV2)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Ally (Sleight Furious Volley LV3)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Rewards (Sleight Flare Breath LV2)")
    regions["Hollow Bastion"].locations.append("Hollow Bastion Room of Rewards (Sleight Flare Breath LV3)")
    regions["Monstro"].locations.append("Monstro Bounty (Sleight Fire Raid)")
    regions["Monstro"].locations.append("Monstro Room of Rewards (Sleight Aqua Splash)")
    regions["Monstro"].locations.append("Monstro Room of Truth (Sleight Splash LV2)")
    regions["Monstro"].locations.append("Monstro Room of Truth (Sleight Splash LV3)")
    regions["Neverland"].locations.append("Neverland Ally (Sleight Hummingbird LV2)")
    regions["Neverland"].locations.append("Neverland Ally (Sleight Hummingbird LV3)")
    regions["Neverland"].locations.append("Neverland Bounty (Sleight Teleport)")
    regions["Neverland"].locations.append("Neverland Room of Rewards (Sleight Thunder Raid)")
    regions["Neverland"].locations.append("Neverland Room of Truth (Sleight Twinkle LV2)")
    regions["Neverland"].locations.append("Neverland Room of Truth (Sleight Twinkle LV3)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Bounty (Sleight Blizzard Raid)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Truth (Sleight Cross-slash)")
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Room of Truth (Sleight Omnislash)")
    regions["Traverse Town"].locations.append("Starting Checks (Sleight Blizzaga)")
    regions["Traverse Town"].locations.append("Starting Checks (Sleight Blizzara)")
    regions["Traverse Town"].locations.append("Starting Checks (Sleight Cura)")
    regions["Traverse Town"].locations.append("Starting Checks (Sleight Curaga)")
    regions["Traverse Town"].locations.append("Pick Up Goofy In Battle (Sleight Goofy Smash)")
    regions["Traverse Town"].locations.append("Pick Up Goofy In Battle (Sleight Goofy Tornado LV2)")
    regions["Traverse Town"].locations.append("Pick Up Goofy In Battle (Sleight Goofy Tornado LV3)")
    regions["Traverse Town"].locations.append("Pick Up Donald In Battle (Sleight Magic LV2)")
    regions["Traverse Town"].locations.append("Pick Up Donald In Battle (Sleight Magic LV3)")
    regions["Traverse Town"].locations.append("Pick Up Goofy In Battle (Sleight Wild Crush)")
    if options.checks_behind_leon:
        regions["Traverse Town"].locations.append("Pick Up Pluto In Battle (Sleight Lucky Bounty LV2)")
        regions["Traverse Town"].locations.append("Pick Up Pluto In Battle (Sleight Lucky Bounty LV3)")
        regions["Traverse Town"].locations.append("Traverse Town Room of Beginnings (Sleight Proud Roar LV2)")
        regions["Traverse Town"].locations.append("Traverse Town Room of Beginnings (Sleight Proud Roar LV3)")
    regions["Twilight Town"].locations.append("Twilight Town Bounty (Sleight Warpinator)")
    regions["Twilight Town"].locations.append("Twilight Town Room of Rewards (Sleight Stardust Blitz)")
    regions["Wonderland"].locations.append("Wonderland Bounty (Sleight Stopga)")
    regions["Wonderland"].locations.append("Wonderland Bounty (Sleight Stopra)")
    regions["Wonderland"].locations.append("Wonderland Room of Rewards (Sleight Synchro)")
    
    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Traverse Town"        , player).connect(multiworld.get_region("Traverse Town"        , player))
    multiworld.get_entrance("Wonderland"           , player).connect(multiworld.get_region("Wonderland"           , player))
    multiworld.get_entrance("Olympus Coliseum"     , player).connect(multiworld.get_region("Olympus Coliseum"     , player))
    multiworld.get_entrance("Monstro"              , player).connect(multiworld.get_region("Monstro"              , player))
    multiworld.get_entrance("Agrabah"              , player).connect(multiworld.get_region("Agrabah"              , player))
    multiworld.get_entrance("Halloween Town"       , player).connect(multiworld.get_region("Halloween Town"       , player))
    multiworld.get_entrance("Atlantica"            , player).connect(multiworld.get_region("Atlantica"            , player))
    multiworld.get_entrance("Neverland"            , player).connect(multiworld.get_region("Neverland"            , player))
    multiworld.get_entrance("Hollow Bastion"       , player).connect(multiworld.get_region("Hollow Bastion"       , player))
    multiworld.get_entrance("100 Acre Wood"        , player).connect(multiworld.get_region("100 Acre Wood"        , player))
    multiworld.get_entrance("Twilight Town"        , player).connect(multiworld.get_region("Twilight Town"        , player))
    multiworld.get_entrance("Destiny Islands"      , player).connect(multiworld.get_region("Destiny Islands"      , player))
    multiworld.get_entrance("Castle Oblivion"      , player).connect(multiworld.get_region("Castle Oblivion"      , player))
    multiworld.get_entrance("Heartless"            , player).connect(multiworld.get_region("Heartless"            , player))
    multiworld.get_entrance("Castle Oblivion Halls", player).connect(multiworld.get_region("Castle Oblivion Halls", player))
    multiworld.get_entrance("Levels"               , player).connect(multiworld.get_region("Levels"               , player))


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
