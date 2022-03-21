from .full_logic import CHECKS_BY_NAME, CHECKS_BY_HEX, NECESSARY_EVENT_PANELS, ALWAYS_EVENT_HEX_CODES

start = 158000

typeToOffset = {
    "General": 0,
    "Discard": 500,
    "Vault": 550,
    "Laser": 600,
    "Laser Event": 700
}

panelTypesToShuffle = {
    "General", "Discard", "Vault", "Laser" #Base This off of settings in the future!!
}

alwaysLocations = {
    "Tutorial Gate Open",
    
    "Outside Tutorial Vault Box",
    "Outside Tutorial Discard",
    "Outside Tutorial Dots Introduction 5",
    "Outside Tutorial Squares Introduction 9",
    
    "Glass Factory Discard",
    "Glass Factory Vertical Symmetry 5",
    "Glass Factory Rotational Symmetry 3",
    "Glass Factory Melting 3",
    
    "Symmetry Island Black Dots 5",
    "Symmetry Island Colored Dots 6",
    "Symmetry Island Fading Lines 7",
    "Symmetry Island Scenery Outlines 5",
    "Symmetry Island Laser",
    
    "Orchard Apple Tree 5",
    
    "Desert Vault Box",
    "Desert Discard",
    "Desert Sun Reflection 8",
    "Desert Artificial Light Reflection 3",
    "Desert Pond Reflection 5",
    "Desert Flood Reflection 5",
    "Desert Laser",
    
    "Quarry Mill Eraser and Dots 6",
    "Quarry Mill Eraser and Squares 8",
    "Quarry Mill Small Squares & Dots & and Eraser",
    "Quarry Boathouse Intro Shapers",
    "Quarry Boathouse Eraser and Shapers 5",
    "Quarry Boathouse Stars & Eraser & and Shapers 2",
    "Quarry Boathouse Stars & Eraser & and Shapers 5",
    "Quarry Laser",
    
    "Shadows Lower Avoid 8",
    "Shadows Environmental Avoid 8",
    "Shadows Follow 5",
    "Shadows Laser",
    
    "Keep Hedge Maze 4",
    "Keep Pressure Plates 4",
    "Keep Discard",
    "Keep Laser Hedges",
    "Keep Laser Pressure Plates",
    
    "Shipwreck Vault Box",
    "Shipwreck Discard",
    
    "Monastery Rhombic Avoid 3",
    "Monastery Branch Follow 2",
    "Monastery Laser",
    
    "Town Cargo Box Discard",
    "Town Hexagonal Reflection",
    "Town Square Avoid",
    "Town Town Discard",
    "Town Symmetry Squares 5 + Dots",
    "Town Full Dot Grid Shapers 5",
    "Town Shapers & Dots & and Eraser",
    "Town RGB Squares",
    "Town RGB Stars",
    "Town Laser",
    
    "Theater Discard",
    
    "Jungle Discard",
    "Jungle Waves 3",
    "Jungle Waves 7",
    "Jungle Popup Wall 6",
    "Jungle Laser",
    
    "River Vault",
    
    "Bunker Drawn Squares 5",
    "Bunker Drawn Squares 9",
    "Bunker Drawn Squares through Tinted Glass 3",
    "Bunker Drop-Down Door Squares 2",
    "Bunker Laser",
    
    "Swamp Seperatable Shapers 6",
    "Swamp Combinable Shapers 8",
    "Swamp Broken Shapers 4",
    "Swamp Cyan Underwater Negative Shapers 5",
    "Swamp Platform Shapers 4",
    "Swamp Rotated Shapers 4",
    "Swamp Red Underwater Negative Shapers 4",
    "Swamp More Rotated Shapers 4",
    "Swamp Blue Underwater Negative Shapers 5",
    "Swamp Laser",
    
    "Treehouse Yellow Bridge 9",
    "Treehouse First Purple Bridge 5",
    "Treehouse Second Purple Bridge 7",
    "Treehouse Green Bridge 7",
    "Treehouse Green Bridge Discard",
    "Treehouse Left Orange Bridge 14",
    "Treehouse Burned House Discard",
    "Treehouse Right Orange Bridge 12",
    "Treehouse Laser",
    
    "Mountaintop Trap Door Triple Exit",
    "Mountaintop Discard",
    "Mountaintop Vault Box",

    "Inside Mountain Obscured Vision 5",
    "Inside Mountain Moving Background 7",
    "Inside Mountain Physically Obstructed 3",
    "Inside Mountain Angled Inside Trash 2",
    "Inside Mountain Color Cycle 5",
    "Inside Mountain Same Solution 6",
    "Inside Mountain Elevator Discard",
    "Inside Mountain Giant Puzzle",
    
    
    
    "Inside Mountain Final Room Elevator Start"
}

uncommonOptionalLocations = {
    "Mountaintop River Shape",
    "Tutorial Patio Floor",
    "Theater Tutorial Video",
    "Theater Desert Video",
    "Theater Jungle Video",
    "Theater Challenge Video",
    "Theater Shipwreck Video",
    "Theater Mountain Video"
}

hardOptionalLocations = {
    "Tutorial Gate Close",
    "Quarry Mill Big Squares & Dots & and Eraser",
    "Swamp Underwater Back Optional",
    
    "Inside Mountain Secret Area Dot Grid Triangles 4",
    "Inside Mountain Secret Area Symmetry Triangles",
    "Inside Mountain Secret Area Stars & Squares and Triangles 2",
    "Inside Mountain Secret Area Shapers and Triangles 2",
    "Inside Mountain Secret Area Symmetry Shapers",
    "Inside Mountain Secret Area Broken and Negative Shapers",
    "Inside Mountain Secret Area Broken Shapers",
    
    "Inside Mountain Secret Area Rainbow Squares",
    "Inside Mountain Secret Area Squares & Stars and Colored Eraser",
    "Inside Mountain Secret Area Rotated Broken Shapers",
    "Inside Mountain Secret Area Stars and Squares",
    "Inside Mountain Secret Area Lone Pillar",
    "Inside Mountain Secret Area Wooden Beam Shapers",
    "Inside Mountain Secret Area Wooden Beam Squares and Shapers",
    "Inside Mountain Secret Area Wooden Beam Shapers and Squares",
    "Inside Mountain Secret Area Wooden Beam Shapers and Stars",
    "Inside Mountain Secret Area Upstairs Invisible Dots 8",
    "Inside Mountain Secret Area Upstairs Invisible Dot Symmetry 3",
    "Inside Mountain Secret Area Upstairs Dot Grid Shapers",
    "Inside Mountain Secret Area Upstairs Dot Grid Rotated Shapers",
    
    "Challenge Vault Box",
    "Theater Walkway Vault Box",
    "Inside Mountain Bottom Layer Discard"
}

locations = alwaysLocations | uncommonOptionalLocations | hardOptionalLocations #TODO: Determined by settings

event_location_table = {CHECKS_BY_HEX[panelHex]["checkName"] + " Solved":None for panelHex in NECESSARY_EVENT_PANELS if CHECKS_BY_HEX[panelHex]["checkName"] not in locations or panelHex in ALWAYS_EVENT_HEX_CODES}



location_table = event_location_table | {location: CHECKS_BY_NAME[location]["idOffset"] + start + typeToOffset[CHECKS_BY_NAME[location]["panelType"]] for location in locations if CHECKS_BY_NAME[location]["panelType"] in panelTypesToShuffle}
location_table_backwards = {CHECKS_BY_NAME[location]["idOffset"] + start + typeToOffset[CHECKS_BY_NAME[location]["panelType"]]: location for location in locations if CHECKS_BY_NAME[location]["panelType"] in panelTypesToShuffle}