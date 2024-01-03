from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KH1Location, location_table, get_locations_by_category


class KH1RegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int, sephiroth: bool):
    regions: Dict[str, KH1RegionData] = {
        "Menu":             KH1RegionData(None, ["Awakening", "Levels"]),
        "Awakening":        KH1RegionData([],   ["Destiny Islands"]),
        "Destiny Islands":  KH1RegionData([],   ["Traverse Town"]),
        "Traverse Town":    KH1RegionData([],   ["World Map"]),
        "Wonderland":       KH1RegionData([],   []),
        "Olympus Coliseum": KH1RegionData([],   []),
        "Deep Jungle":      KH1RegionData([],   []),
        "Agrabah":          KH1RegionData([],   []),
        "Monstro":          KH1RegionData([],   []),
        "Atlantica":        KH1RegionData([],   []),
        "Halloween Town":   KH1RegionData([],   []),
        "Neverland":        KH1RegionData([],   []),
        "Hollow Bastion":   KH1RegionData([],   []),
        "End of the World": KH1RegionData([],   []),
        "Levels":           KH1RegionData([],   []),
        "World Map":        KH1RegionData([],   ["Wonderland", "Olympus Coliseum", "Deep Jungle",
                                         "Agrabah", "Monstro", "Atlantica",
                                         "Halloween Town", "Neverland", "Hollow Bastion",
                                         "End of the World"])
    }

    # Set up locations
   #regions["Destiny Islands"].locations.append("Destiny Islands Chest"), missable
    regions["Traverse Town"].locations.append("Traverse Town 1st District Candle Puzzle Chest"),
    regions["Traverse Town"].locations.append("Traverse Town 1st District Accessory Shop Roof Chest"),
    regions["Traverse Town"].locations.append("Traverse Town 2nd District Boots and Shoes Awning Chest"),
    regions["Traverse Town"].locations.append("Traverse Town 2nd District Rooftop Chest"),
    regions["Traverse Town"].locations.append("Traverse Town 2nd District Gizmo Shop Facade Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Alleyway Balcony Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Alleyway Blue Room Awning Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Alleyway Corner Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Green Room Clock Puzzle Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Green Room Table Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Red Room Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Mystical House Yellow Trinity Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Accessory Shop Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Secret Waterway White Trinity Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Geppetto's House Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Item Workshop Right Chest"),
    regions["Traverse Town"].locations.append("Traverse Town 1st District Blue Trinity Balcony Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Mystical House Glide Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Alleyway Behind Crates Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Item Workshop Left Chest"),
    regions["Traverse Town"].locations.append("Traverse Town Secret Waterway Near Stairs Chest"),
    regions["Wonderland"].locations.append("Wonderland Rabbit Hole Green Trinity Chest"),
   #regions["Wonderland"].locations.append("Wonderland Rabbit Hole Defeat Heartless After Trial Chest"),
   #regions["Wonderland"].locations.append("Wonderland Rabbit Hole Defeat Heartless After Hollow Bastion Chest"),
    regions["Wonderland"].locations.append("Wonderland Bizarre Room Green Trinity Chest"),
    regions["Wonderland"].locations.append("Wonderland Queen's Castle Hedge Left Red Chest"),
    regions["Wonderland"].locations.append("Wonderland Queen's Castle Hedge Right Blue Chest"),
    regions["Wonderland"].locations.append("Wonderland Queen's Castle Hedge Right Red Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Thunder Plant Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Glide Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Nut Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Corner Chest"),
    regions["Wonderland"].locations.append("Wonderland Bizarre Room Lamp Chest"),
    regions["Wonderland"].locations.append("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"),
    regions["Wonderland"].locations.append("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"),
    regions["Wonderland"].locations.append("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"),
    regions["Wonderland"].locations.append("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"),
    regions["Wonderland"].locations.append("Wonderland Lotus Forest Through the Painting White Trinity Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Tree House Beneath Tree House Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Tree House Rooftop Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Hippo's Lagoon Center Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Hippo's Lagoon Left Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Hippo's Lagoon Right Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Vines Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Vines 2 Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Climbing Trees Blue Trinity Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Tunnel Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Cavern of Hearts White Trinity Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Camp Blue Trinity Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Tent Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Waterfall Cavern Low Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Waterfall Cavern Middle Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Waterfall Cavern High Wall Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Waterfall Cavern High Middle Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Cliff Right Cliff Left Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Cliff Right Cliff Right Chest"),
    regions["Deep Jungle"].locations.append("Deep Jungle Tree House Suspended Boat Chest"),
   #regions["100 Acre Wood"].locations.append("100 Acre Wood Meadow Inside Log Chest"),
    regions["Agrabah"].locations.append("Agrabah Plaza By Storage Chest"),
    regions["Agrabah"].locations.append("Agrabah Plaza Raised Terrace Chest"),
    regions["Agrabah"].locations.append("Agrabah Plaza Top Corner Chest"),
    regions["Agrabah"].locations.append("Agrabah Alley Chest"),
    regions["Agrabah"].locations.append("Agrabah Bazaar Across Windows Chest"),
    regions["Agrabah"].locations.append("Agrabah Bazaar High Corner Chest"),
    regions["Agrabah"].locations.append("Agrabah Main Street Right Palace Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Main Street High Above Alley Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Main Street High Above Palace Gates Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Palace Gates Low Chest"),
    regions["Agrabah"].locations.append("Agrabah Palace Gates High Opposite Palace Chest"),
    regions["Agrabah"].locations.append("Agrabah Palace Gates High Close to Palace Chest"),
    regions["Agrabah"].locations.append("Agrabah Storage Green Trinity Chest"),
    regions["Agrabah"].locations.append("Agrabah Storage Behind Barrel Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Entrance Left Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Entrance Tall Tower Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Hall High Left Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Hall Near Bottomless Hall Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Bottomless Hall Raised Platform Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Bottomless Hall Pillar Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Bottomless Hall Across Chasm Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Treasure Room Across Platforms Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Treasure Room Small Treasure Pile Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Treasure Room Large Treasure Pile Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Treasure Room Above Fire Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Relic Chamber Jump from Stairs Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Relic Chamber Stairs Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Dark Chamber Abu Gem Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Dark Chamber Across from Relic Chamber Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Dark Chamber Bridge Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Dark Chamber Near Save Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Hidden Room Right Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Hidden Room Left Chest"),
    regions["Agrabah"].locations.append("Agrabah Aladdin's House Main Street Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Aladdin's House Plaza Entrance Chest"),
    regions["Agrabah"].locations.append("Agrabah Cave of Wonders Entrance White Trinity Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 6 Other Platform Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 6 Low Chest"),
    regions["Atlantica"].locations.append("Atlantica Sunken Ship In Flipped Boat Chest"),
    regions["Atlantica"].locations.append("Atlantica Sunken Ship Seabed Chest"),
    regions["Atlantica"].locations.append("Atlantica Sunken Ship Inside Ship Chest"),
    regions["Atlantica"].locations.append("Atlantica Ariel's Grotto High Chest"),
    regions["Atlantica"].locations.append("Atlantica Ariel's Grotto Middle Chest"),
    regions["Atlantica"].locations.append("Atlantica Ariel's Grotto Low Chest"),
    regions["Atlantica"].locations.append("Atlantica Ursula's Lair Use Fire on Urchin Chest"),
    regions["Atlantica"].locations.append("Atlantica Undersea Gorge Jammed by Ariel's Grotto Chest"),
    regions["Atlantica"].locations.append("Atlantica Triton's Palace White Trinity Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Moonlight Hill White Trinity Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Bridge Under Bridge"),
    regions["Halloween Town"].locations.append("Halloween Town Boneyard Tombstone Puzzle Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Bridge Right of Gate Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Cemetary Behind Grave Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Cemetary By Cat Shape Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Cemetary Between Graves Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Lower Iron Cage Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Upper Iron Cage Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Hollow Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Grounds Red Trinity Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Guillotine Square High Tower Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Guillotine Square Pumpkin Structure Left Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Entrance Steps Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Oogie's Manor Inside Entrance Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Bridge Left of Gate Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Cemetary By Striped Grave Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Guillotine Square Under Jack's House Stairs Chest"),
    regions["Halloween Town"].locations.append("Halloween Town Guillotine Square Pumpkin Structure Right Chest"),
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Coliseum Gates Left Behind Columns Chest"),
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Coliseum Gates Right Blue Trinity Chest"),
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Coliseum Gates Left Blue Trinity Chest"),
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Coliseum Gates White Trinity Chest"),
    regions["Olympus Coliseum"].locations.append("Olympus Coliseum Coliseum Gates Blizzara Chest"),
    regions["Monstro"].locations.append("Monstro Mouth Boat Deck Chest"),
    regions["Monstro"].locations.append("Monstro Mouth High Platform Boat Side Chest"),
    regions["Monstro"].locations.append("Monstro Mouth High Platform Across from Boat Chest"),
    regions["Monstro"].locations.append("Monstro Mouth Near Ship Chest"),
    regions["Monstro"].locations.append("Monstro Mouth Green Trinity Top of Boat Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 2 Ground Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 2 Platform Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 5 Platform Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 3 Ground Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 3 Near Chamber 6 Entrance Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest"),
    regions["Monstro"].locations.append("Monstro Mouth High Platform Near Teeth Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 5 Atop Barrel Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 5 Low 2nd Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 5 Low 1st Chest"),
    regions["Neverland"].locations.append("Neverland Pirate Ship Deck White Trinity Chest"),
    regions["Neverland"].locations.append("Neverland Pirate Ship Crows Nest Chest"),
    regions["Neverland"].locations.append("Neverland Hold Yellow Trinity Right Blue Chest"),
    regions["Neverland"].locations.append("Neverland Hold Yellow Trinity Left Blue Chest"),
    regions["Neverland"].locations.append("Neverland Galley Chest"),
    regions["Neverland"].locations.append("Neverland Cabin Chest"),
    regions["Neverland"].locations.append("Neverland Hold Flight 1st Chest "),
    regions["Neverland"].locations.append("Neverland Clock Tower Chest"),
    regions["Neverland"].locations.append("Neverland Hold Flight 2nd Chest"),
    regions["Neverland"].locations.append("Neverland Hold Yellow Trinity Green Chest"),
    regions["Neverland"].locations.append("Neverland Captain's Cabin Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls Water's Surface Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls Under Water 1st Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls Under Water 2nd Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls Floating Platform Near Save Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls Floating Platform Near Bubble Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls High Platform Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Castle Gates Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Castle Gates Freestanding Pillar Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Castle Gates High Pillar Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Great Crest Lower Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Great Crest After Battle Platform Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion High Tower 2nd Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion High Tower 1st Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion High Tower Above Sliding Gates Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Library Top of Bookshelf Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Library 1st Floor Turn the Carousel Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Library Top of Bookshelf Turn the Carousel Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Library 2nd Floor Turn the Carousel 1st Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Library 2nd Floor Turn the Carousel 2nd Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Lift Stop Library Node Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Lift Stop Outside Library Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Base Level Bubble Under the Wall Platform Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Base Level Platform Near Entrance Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Base Level Near Crystal Switch Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Waterway Near Save Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Waterway Blizzard on Bubble Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Waterway Unlock Passage from Base Level Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Dungeon By Candles Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Dungeon Corner Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Grand Hall Steps Right Side Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Grand Hall Oblivion Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Grand Hall Left of Gate Chest"),
   #regions["Hollow Bastion"].locations.append("Hollow Bastion Entrance Hall Push the Statue Chest"),
    regions["Hollow Bastion"].locations.append("Hollow Bastion Rising Falls White Trinity Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 1st Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 2nd Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 3rd Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 4th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 5th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 6th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 10th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 9th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 8th Chest"),
   #regions["End of the World"].locations.append("End of the World Final Dimension 7th Chest"),
   #regions["End of the World"].locations.append("End of the World Giant Crevasse 3rd Chest"),
   #regions["End of the World"].locations.append("End of the World Giant Crevasse 1st Chest"),
   #regions["End of the World"].locations.append("End of the World Giant Crevasse 4th Chest"),
   #regions["End of the World"].locations.append("End of the World Giant Crevasse 2nd Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Traverse Town Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Wonderland Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Olympus Coliseum Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Deep Jungle Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Agrabah Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Atlantica Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Halloween Town Chest"),
   #regions["End of the World"].locations.append("End of the World World Terminus Neverland Chest"),
    regions["End of the World"].locations.append("End of the World World Terminus 100 Acre Wood Chest"),
    regions["End of the World"].locations.append("End of the World World Terminus Hollow Bastion Chest"),
    regions["End of the World"].locations.append("End of the World Final Rest Chest"),
    regions["Monstro"].locations.append("Monstro Chamber 6 White Trinity Chest"),
   #regions["Awakening"].locations.append("Awakening Chest"), missable
   
   #regions["End of the World"].locations.append("Chronicles Sora's Story")
    regions["Wonderland"].locations.append("Chronicles Wonderland")
    regions["Olympus Coliseum"].locations.append("Chronicles Olympus Coliseum")
    regions["Deep Jungle"].locations.append("Chronicles Deep Jungle")
    regions["Agrabah"].locations.append("Chronicles Agrabah")
    regions["Monstro"].locations.append("Chronicles Monstro")
   #regions["100 Acre Wood"].locations.append("Chronicles 100 Acre Wood")
    regions["Atlantica"].locations.append("Chronicles Atlantica")
    regions["Halloween Town"].locations.append("Chronicles Halloween Town")
   #regions["Neverland"].locations.append("Chronicles Neverland")
    
    regions["Agrabah"].locations.append("Ansem's Secret Report 1")
    regions["Hollow Bastion"].locations.append("Ansem's Secret Report 2")
    regions["Atlantica"].locations.append("Ansem's Secret Report 3")
    regions["Hollow Bastion"].locations.append("Ansem's Secret Report 4")
    regions["Hollow Bastion"].locations.append("Ansem's Secret Report 5")
    regions["Hollow Bastion"].locations.append("Ansem's Secret Report 6")
    regions["Halloween Town"].locations.append("Ansem's Secret Report 7")
    regions["Olympus Coliseum"].locations.append("Ansem's Secret Report 8")
    regions["Neverland"].locations.append("Ansem's Secret Report 9")
    regions["Hollow Bastion"].locations.append("Ansem's Secret Report 10")
   #regions["Agrabah"].locations.append("Ansem's Secret Report 11")
    if sephiroth:
        regions["Olympus Coliseum"].locations.append("Ansem's Secret Report 12")
   #regions["Hollow Bastion"].locations.append("Ansem's Secret Report 13")
   
    regions["Levels"].locations.append("Level 1")
    regions["Levels"].locations.append("Level 2")
    regions["Levels"].locations.append("Level 3")
    regions["Levels"].locations.append("Level 4")
    regions["Levels"].locations.append("Level 5")
    regions["Levels"].locations.append("Level 6")
    regions["Levels"].locations.append("Level 7")
    regions["Levels"].locations.append("Level 8")
    regions["Levels"].locations.append("Level 9")
    regions["Levels"].locations.append("Level 10")
    regions["Levels"].locations.append("Level 11")
    regions["Levels"].locations.append("Level 12")
    regions["Levels"].locations.append("Level 13")
    regions["Levels"].locations.append("Level 14")
    regions["Levels"].locations.append("Level 15")
    regions["Levels"].locations.append("Level 16")
    regions["Levels"].locations.append("Level 17")
    regions["Levels"].locations.append("Level 18")
    regions["Levels"].locations.append("Level 19")
    regions["Levels"].locations.append("Level 20")
    regions["Levels"].locations.append("Level 21")
    regions["Levels"].locations.append("Level 22")
    regions["Levels"].locations.append("Level 23")
    regions["Levels"].locations.append("Level 24")
    regions["Levels"].locations.append("Level 25")
    regions["Levels"].locations.append("Level 26")
    regions["Levels"].locations.append("Level 27")
    regions["Levels"].locations.append("Level 28")
    regions["Levels"].locations.append("Level 29")
    regions["Levels"].locations.append("Level 30")
    regions["Levels"].locations.append("Level 31")
    regions["Levels"].locations.append("Level 32")
    regions["Levels"].locations.append("Level 33")
    regions["Levels"].locations.append("Level 34")
    regions["Levels"].locations.append("Level 35")
    regions["Levels"].locations.append("Level 36")
    regions["Levels"].locations.append("Level 37")
    regions["Levels"].locations.append("Level 38")
    regions["Levels"].locations.append("Level 39")
    regions["Levels"].locations.append("Level 40")
    regions["Levels"].locations.append("Level 41")
    regions["Levels"].locations.append("Level 42")
    regions["Levels"].locations.append("Level 43")
    regions["Levels"].locations.append("Level 44")
    regions["Levels"].locations.append("Level 45")
    regions["Levels"].locations.append("Level 46")
    regions["Levels"].locations.append("Level 47")
    regions["Levels"].locations.append("Level 48")
    regions["Levels"].locations.append("Level 49")
    regions["Levels"].locations.append("Level 50")
    regions["Levels"].locations.append("Level 51")
    regions["Levels"].locations.append("Level 52")
    regions["Levels"].locations.append("Level 53")
    regions["Levels"].locations.append("Level 54")
    regions["Levels"].locations.append("Level 55")
    regions["Levels"].locations.append("Level 56")
    regions["Levels"].locations.append("Level 57")
    regions["Levels"].locations.append("Level 58")
    regions["Levels"].locations.append("Level 59")
    regions["Levels"].locations.append("Level 60")
    regions["Levels"].locations.append("Level 61")
    regions["Levels"].locations.append("Level 62")
    regions["Levels"].locations.append("Level 63")
    regions["Levels"].locations.append("Level 64")
    regions["Levels"].locations.append("Level 65")
    regions["Levels"].locations.append("Level 66")
    regions["Levels"].locations.append("Level 67")
    regions["Levels"].locations.append("Level 68")
    regions["Levels"].locations.append("Level 69")
    regions["Levels"].locations.append("Level 70")
    regions["Levels"].locations.append("Level 71")
    regions["Levels"].locations.append("Level 72")
    regions["Levels"].locations.append("Level 73")
    regions["Levels"].locations.append("Level 74")
    regions["Levels"].locations.append("Level 75")
    regions["Levels"].locations.append("Level 76")
    regions["Levels"].locations.append("Level 77")
    regions["Levels"].locations.append("Level 78")
    regions["Levels"].locations.append("Level 79")
    regions["Levels"].locations.append("Level 80")
    regions["Levels"].locations.append("Level 81")
    regions["Levels"].locations.append("Level 82")
    regions["Levels"].locations.append("Level 83")
    regions["Levels"].locations.append("Level 84")
    regions["Levels"].locations.append("Level 85")
    regions["Levels"].locations.append("Level 86")
    regions["Levels"].locations.append("Level 87")
    regions["Levels"].locations.append("Level 88")
    regions["Levels"].locations.append("Level 89")
    regions["Levels"].locations.append("Level 90")
    regions["Levels"].locations.append("Level 91")
    regions["Levels"].locations.append("Level 92")
    regions["Levels"].locations.append("Level 93")
    regions["Levels"].locations.append("Level 94")
    regions["Levels"].locations.append("Level 95")
    regions["Levels"].locations.append("Level 96")
    regions["Levels"].locations.append("Level 97")
    regions["Levels"].locations.append("Level 98")
    regions["Levels"].locations.append("Level 99")
    regions["Levels"].locations.append("Level 100")
   
    regions["Olympus Coliseum"].locations.append("Complete Phil Cup")
    regions["Olympus Coliseum"].locations.append("Complete Pegasus Cup")
    regions["Olympus Coliseum"].locations.append("Complete Hercules Cup")
    regions["Olympus Coliseum"].locations.append("Complete Hades Cup")

    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Awakening", player).connect(multiworld.get_region("Awakening", player))
    multiworld.get_entrance("Destiny Islands", player).connect(multiworld.get_region("Destiny Islands", player))
    multiworld.get_entrance("Traverse Town", player).connect(multiworld.get_region("Traverse Town", player))
    multiworld.get_entrance("Wonderland", player).connect(multiworld.get_region("Wonderland", player))
    multiworld.get_entrance("Olympus Coliseum", player).connect(multiworld.get_region("Olympus Coliseum", player))
    multiworld.get_entrance("Deep Jungle", player).connect(multiworld.get_region("Deep Jungle", player))
    multiworld.get_entrance("Agrabah", player).connect(multiworld.get_region("Agrabah", player))
    multiworld.get_entrance("Monstro", player).connect(multiworld.get_region("Monstro", player))
    multiworld.get_entrance("Atlantica", player).connect(multiworld.get_region("Atlantica", player))
    multiworld.get_entrance("Halloween Town", player).connect(multiworld.get_region("Halloween Town", player))
    multiworld.get_entrance("Neverland", player).connect(multiworld.get_region("Neverland", player))
    multiworld.get_entrance("Hollow Bastion", player).connect(multiworld.get_region("Hollow Bastion", player))
    multiworld.get_entrance("End of the World", player).connect(multiworld.get_region("End of the World", player))
    multiworld.get_entrance("World Map", player).connect(multiworld.get_region("World Map", player))
    multiworld.get_entrance("Levels", player).connect(multiworld.get_region("Levels", player))

def create_region(multiworld: MultiWorld, player: int, name: str, data: KH1RegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = KH1Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
