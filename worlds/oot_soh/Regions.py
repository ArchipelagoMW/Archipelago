from typing import Dict, List, NamedTuple


class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, SohRegionData] = {
    # Root Regions
    "Root": SohRegionData(["Root Exits"]),
    "Root Exits": SohRegionData(
        ["Child Spawn", "Adult Spawn", "Minuet of Forest Warp", "Bolero of Fire Warp", "Serenade of Water Warp",
         "Nocturne of Shadow Warp", "Requiem of Spirit Warp", "Prelude of Light Warp"]),
    "Child Spawn": SohRegionData(["KF Link's House"]),
    "Adult Spawn": SohRegionData(["Temple of Time"]),
    "Minuet of Forest Warp": SohRegionData(["Sacred Forest Meadow"]),
    "Bolero of Fire Warp": SohRegionData(["DMC Central Local"]),
    "Serenade of Water Warp": SohRegionData(["Lake Hylia"]),
    "Requiem of Spirit Warp": SohRegionData(["Desert Colossus"]),
    "Nocturne of Shadow Warp": SohRegionData(["Graveyard Warp Pad Region"]),
    "Prelude of Light Warp": SohRegionData(["Temple of Time"]),

    # Kokiri Forest
    "Kokiri Forest": SohRegionData(
        ["KF Link's House", "KF Mido's House", "KF Saria's House", "KF House of Twins", "KF Know It All House",
         "KF Kokiri Shop", "KF Outside Deku Tree", "Lost Woods", "LW Bridge From Forest", "KF Storms Grotto"]),
    "KF Outside Deku Tree": SohRegionData(["Deku Tree Entryway", "Kokiri Forest"]),
    "KF Link's House": SohRegionData(["Kokiri Forest"]),
    "KF Mido's House": SohRegionData(["Kokiri Forest"]),
    "KF Saria's House": SohRegionData(["Kokiri Forest"]),
    "KF House of Twins": SohRegionData(["Kokiri Forest"]),
    "KF Know It All House": SohRegionData(["Kokiri Forest"]),
    "KF Kokiri Shop": SohRegionData(["Kokiri Forest"]),
    "KF Storms Grotto": SohRegionData(["Kokiri Forest"]),

    # Lost Woods
    "LW Forest Exit": SohRegionData(["Kokiri Forest"]),
    "Lost Woods": SohRegionData(
        ["LW Forest Exit", "GC Woods Warp", "LW Bridge", "Zora River", "LW Beyond Mido", "LW Near Shortcuts Grotto"]),
    "LW Beyond Mido": SohRegionData(
        ["LW Forest Exit", "Lost Woods", "SFM Entryway", "Deku Theater", "LW Scrubs Grotto"]),
    "LW Near Shortcuts Grotto": SohRegionData(["Lost Woods"]),
    "Deku Theater": SohRegionData(["LW Beyond Mido"]),
    "LW Scrubs Grotto": SohRegionData(["LW Beyond Mido"]),
    "LW Bridge From Forest": SohRegionData(["LW Bridge"]),
    "LW Bridge": SohRegionData(["Kokiri Forest", "Hyrule Field", "Lost Woods"]),

    # Sacred Forest Meadow
    "SFM Entryway": SohRegionData(["LW Beyond Mido", "Sacred Forest Meadow", "SFM Wolfos Grotto"]),
    "Sacred Forest Meadow": SohRegionData(
        ["SFM Entryway", "Forest Temple Entryway", "SFM Fairy Grotto", "SFM Storms Grotto"]),
    "SFM Fairy Grotto": SohRegionData(["Sacred Forest Meadow"]),
    "SFM Wolfos Grotto": SohRegionData(["SFM Entry Way"]),
    "SFM Storms Grotto": SohRegionData(["Sacred Forest Meadow"]),

    # Hyrule Field
    "Hyrule Field": SohRegionData(
        ["LW Bridge", "Lake Hylia", "Gerudo Valley", "Market Entrance", "Kakariko Village", "ZR Front", "Lon Lon Ranch",
         "HF Southeast Grotto", "HF Open Grotto", "HF Inside Fence Grotto", "HF Cow Grotto", "HF Near Market Grotto",
         "HF Fairy Grotto", "HF Near Kak Grotto", "HF Tektite Grotto"]),
    "HF Southeast Grotto": SohRegionData(["Hyrule Field"]),
    "HF Open Grotto": SohRegionData(["Hyrule Field"]),
    "HF Inside Fence Grotto": SohRegionData(["Hyrule Field"]),
    "HF Cow Grotto": SohRegionData(["Hyrule Field", "HF Cow Grotto Behind Webs"]),
    "HF Cow Grotto Behind Webs": SohRegionData(["HF Cow Grotto"]),
    "HF Near Market Grotto": SohRegionData(["Hyrule Field"]),
    "HF Fairy Grotto": SohRegionData(["Hyrule Field"]),
    "HF Near Kak Grotto": SohRegionData(["Hyrule Field"]),
    "HF Tektite Grotto": SohRegionData(["Hyrule Field"]),

    # Lake Hylia
    "Lake Hylia": SohRegionData(
        ["Hyrule Field", "Zoras Domain", "LH Owl Flight", "LH Fishing Island", "LH Lab", "Water Temple Entryway",
         "LH Grotto"]),
    "LH Fishing Island": SohRegionData(["Lake Hylia", "LH Fishing Hole"]),
    "LH Owl Flight": SohRegionData(["Hyrule Field"]),
    "LH Lab": SohRegionData(["Lake Hylia"]),
    "LH Fishing Hole": SohRegionData(["LH Fishing Island"]),
    "LH Grotto": SohRegionData(["Lake Hylia"]),

    # Lon Lon Ranch
    "Lon Lon Ranch": SohRegionData(["Hyrule Field", "LLR Talons House", "LLR Stables", "LLR Tower", "LLR Grotto"]),
    "LLR Talons House": SohRegionData(["Lon Lon Ranch"]),
    "LLR Stables": SohRegionData(["Lon Lon Ranch"]),
    "LLR Tower": SohRegionData(["Lon Lon Ranch"]),
    "LLR Grotto": SohRegionData(["Lon Lon Ranch"]),

    # Market
    "Market Entrance": SohRegionData(["Hyrule Field", "Market", "Market Guard House"]),
    "Market": SohRegionData(["Market Entrance", "ToT Entrance", "Castle Grounds", "Market Bazaar", "Market Mask Shop",
                             "Market Shooting Gallery", "Market Bombchu Bowling", "Market Treasure Chest Game",
                             "Market Potion Shop", "Market Back Alley"]),
    "Market Back Alley": SohRegionData(
        ["Market", "Market Bombchu Shop", "Market Dog Lady House", "Market Man in Green House"]),
    "Market Guard House": SohRegionData(["Market Entrance"]),
    "Market Bazaar": SohRegionData(["Market"]),
    "Market Mask Shop": SohRegionData(["Market"]),
    "Market Shooting Gallery": SohRegionData(["Market"]),
    "Market Bombchu Bowling": SohRegionData(["Market"]),
    "Market Potion Shop": SohRegionData(["Market"]),
    "Market Treasure Chest Game": SohRegionData(["Market"]),
    "Market Bombchu Shop": SohRegionData(["Market Back Alley"]),
    "Market Dog Lady House": SohRegionData(["Market Back Alley"]),
    "Market Man in Green House": SohRegionData(["Market Back Alley"]),

    # Temple of Time
    "ToT Entrance": SohRegionData(["Market", "Temple of Time"]),
    "Temple of Time": SohRegionData(["ToT Entrance", "Beyond Door of Time"]),
    "Beyond Door of Time": SohRegionData(["Temple of Time"]),

    # Castle Grounds
    "Castle Grounds": SohRegionData(["Market", "Hyrule Castle Grounds", "Ganon's Castle Grounds"]),
    "Hyrule Castle Grounds": SohRegionData(
        ["Castle Grounds", "HC Garden", "HC Great Fairy Fountain", "HC Storms Grotto"]),
    "HC Garden": SohRegionData(["Hyrule Castle Grounds"]),
    "HC Great Fairy Fountain": SohRegionData(["Castle Grounds"]),
    "HC Storms Grotto": SohRegionData(["Castle Grounds", "HC Storms Grotto Behind Walls"]),
    "HC Storms Grotto Behind Walls": SohRegionData(["HC Storms Grotto"]),
    "Ganon's Castle Grounds": SohRegionData(["Castle Grounds", "OGC Great Fairy Fountain", "Ganon's Castle Ledge"]),
    "OGC Great Fairy Fountain": SohRegionData(["Castle Grounds"]),
    "Castle Grounds From Ganon's Castle": SohRegionData(["Hyrule Castle Grounds", "Ganon's Castle Ledge"]),
    "Ganon's Castle Ledge": SohRegionData(["Ganon's Castle Grounds", "Ganon's Castle Entryway"]),

    # Kakariko Village
    "Kakariko Village": SohRegionData(
        ["Hyrule Field", "Kak Carpenter Boss House", "Kak House of Skulltula", "Kak Impas House", "Kak Windmill",
         "Kak Bazaar", "Kak Shooting Gallery", "Kak Well", "Kak Potion Shop Front", "Kak Redead Grotto",
         "Kak Impas Ledge", "Kak Watchtower", "Kak Rooftop", "Kak Impas Rooftop", "The Graveyard", "Kak Behind Gate",
         "Kak Backyard"]),
    "Kak Impas Ledge": SohRegionData(["Kak Impas House Back", "Kakariko Village"]),
    "Kak Impas Rooftop": SohRegionData(["Kak Impas Ledge", "Kakariko Village"]),
    "Kak Watchtower": SohRegionData(["Kakariko Village", "Kak Rooftop"]),
    "Kak Rooftop": SohRegionData(["Kak Backyard", "Kakariko Village"]),
    "Kak Backyard": SohRegionData(
        ["Kakariko Village", "Kak Open Grotto", "Kak Granny's Potion Shop", "Kak Potion Shop Back"]),
    "Kak Carpenter Boss House": SohRegionData(["Kakariko Village"]),
    "Kak House of Skulltula": SohRegionData(["Kakariko Village"]),
    "Kak Impas House": SohRegionData(["Kakariko Village"]),
    "Kak Impas House Back": SohRegionData(["Kak Impas Ledge"]),
    "Kak Windmill": SohRegionData(["Kakariko Village"]),
    "Kak Bazaar": SohRegionData(["Kakariko Village"]),
    "Kak Shooting Gallery": SohRegionData(["Kakariko Village"]),
    "Kak Potion Shop Front": SohRegionData(["Kakariko Village", "Kak Potion Shop Back"]),
    "Kak Potion Shop Back": SohRegionData(["Kak Backyard", "Kak Potion Shop Front"]),
    "Kak Granny's Potion Shop": SohRegionData(["Kak Backyard"]),
    "Kak Redead Grotto": SohRegionData(["Kakariko Village"]),
    "Kak Open Grotto": SohRegionData(["Kak Backyard"]),
    "Kak Behind Gate": SohRegionData(["Kakariko Village", "Death Mountain"]),
    "Kak Well": SohRegionData(["Kakariko Village", "Bottom of the Well Entryway"]),

    # The Graveyard
    "The Graveyard": SohRegionData(
        ["Graveyard Shield Grave", "Graveyard Composers Grave", "Graveyard Heart Piece Grave", "Graveyard Dampes Grave",
         "Graveyard Dampes House", "Kakariko Village", "Graveyard Warp Pad Region"]),
    "Graveyard Shield Grave": SohRegionData(["The Graveyard", "Graveyard Shield Grave Back"]),
    "Graveyard Shield Grave Back": SohRegionData(["Graveyard Shield Grave"]),
    "Graveyard Heart Piece Grave": SohRegionData(["The Graveyard"]),
    "Graveyard Composers Grave": SohRegionData(["The Graveyard"]),
    "Graveyard Dampes Grave": SohRegionData(["The Graveyard", "Kak Windmill"]),
    "Graveyard Dampes House": SohRegionData(["The Graveyard"]),
    "Graveyard Warp Pad Region": SohRegionData(["The Graveyard", "Shadow Temple Entryway"]),

    # Death Mountain Trail
    "Death Mountain": SohRegionData(
        ["Kak Behind Gate", "Goron City", " Death Mountain Summit", "Dodongos Cavern Entryway", "DMT Storms Grotto"]),
    "Death Mountain Summit": SohRegionData(
        ["Death Mountain", "DMC Upper Local", "DMC Owl Flight", "DMT Cow Grotto", "DMT Great Fairy Fountain"]),
    "DMT Owl Flight": SohRegionData(["Kak Impas Rooftop"]),
    "DMT Cow Grotto": SohRegionData(["Death Mountain Summit"]),
    "DMT Storms Grotto": SohRegionData(["Death Mountain"]),
    "DMT Great Fairy Fountain": SohRegionData(["Death Mountain Summit"]),

    # Goron City
    "Goron City": SohRegionData(
        ["Death Mountain", "GC Medigoron", "GC Woods Warp", "GC Shop", "GC Darunias Chamber", "GC Grotto Platform"]),
    "GC Medigorn": SohRegionData(["Goron City"]),
    "GC Woods Warp": SohRegionData(["Goron City", "Lost Woods"]),
    "GC Darunias Chamber": SohRegionData(["Goron City", "DMC Lower Local"]),
    "GC Grotto Platform": SohRegionData(["Goron City", "GC Grotto"]),
    "GC Shop": SohRegionData(["Goron City"]),
    "GC Grotto": SohRegionData(["GC Grotto Platform"]),

    # Death Mountain Crater
    "DMC Upper Nearby": SohRegionData(["DMC Upper Local", "Death Mountain Summit", "DMC Upper Grotto"]),
    "DMC Upper Local": SohRegionData(
        ["DMC Upper Nearby", "DMC Ladder Region Nearby", "DMC Central Nearby", "DMC Central Nearby", "DMC Lower Nearby",
         "DMC Distant Platform"]),
    "DMC Ladder Region Nearby": SohRegionData(["DMC Upper Nearby", "DMC Lower Nearby"]),
    "DMC Lower Nearby": SohRegionData(
        ["DMC Lower Local", "GC Darunias Chamber", "DMC Great Fairy Fountain", "DMC Hammer Grotto"]),
    "DMC Lower Local": SohRegionData(
        ["DMC Lower Nearby", "DMC Ladder Region Nearby", "DMC Central Nearby", "DMC Central Local"]),
    "DMC Central Nearby": SohRegionData(["DMC Central Local"]),
    "DMC Central Local": SohRegionData(
        ["DMC Central Nearby", "DMC Lower Nearby", "DMC Upper Nearby", "Fire Temple Entryway", "DMC Distant Platform"]),
    "DMC Great Fairy Fountain": SohRegionData(["DMC Lower Local"]),
    "DMC Upper Grotto": SohRegionData(["DMC Upper Local"]),
    "DMC Hammer Grotto": SohRegionData(["DMC Lower Local"]),
    "DMC Distant Platform": SohRegionData(["DMC Central Local"]),

    # Zora River
    "ZR Front": SohRegionData(["Zora River", "Hyrule Field"]),
    "Zora River": SohRegionData(
        ["ZR Front", "ZR Open Grotto", "ZR Fairy Grotto", "Lost Woods", "ZR Storms Grotto", "ZR Behind Waterfall"]),
    "ZR Behind Waterfall": SohRegionData(["Zora River", "Zoras Domain"]),
    "ZR Open Grotto": SohRegionData(["Zora River"]),
    "ZR Fairy Grotto": SohRegionData(["Zora River"]),
    "ZR Storms Grotto": SohRegionData(["Zora River"]),

    # Zora's Domain
    "Zoras Domain": SohRegionData(
        ["ZR Behind Waterfall", "Lake Hylia", "ZD Behind King Zora", "ZD Shop", "Zoras Domain Island"]),
    "Zoras Domain Island": SohRegionData(["Zoras Domain", "ZD Storms Grotto"]),
    "ZD Behind King Zora": SohRegionData(["Zoras Domain", "Zoras Fountain"]),
    "ZD Shop": SohRegionData(["Zoras Domain"]),
    "ZD Storms Grotto": SohRegionData(["Zoras Domain Island"]),

    # Zora's Fountain
    "Zoras Fountain": SohRegionData(
        ["ZD Behind King Zora", "ZF Icebergs", "ZF Lakebed", "ZF Hidden Cave", "ZF Rock", "Jabu Jabus Belly Entryway",
         "ZF Great Fairy Fountain"]),
    "ZF Icebergs": SohRegionData(["Zoras Fountain", "ZF Lakebed", "ZF Ledge"]),
    "ZF Lakebed": SohRegionData(["Zoras Fountain"]),
    "ZF Ledge": SohRegionData(["Zoras Fountain", "ZF Lakebed", "ZF Icebergs", "Ice Cavern Entryway"]),
    "ZF Hidden Cave": SohRegionData(["ZF Hidden Ledge"]),
    "ZF Hidden Ledge": SohRegionData(["Zoras Fountain", "ZF Hidden Cave"]),
    "ZF Rock": SohRegionData(["Zoras Fountain"]),
    "ZF Great Fairy Fountain": SohRegionData(["Zoras Fountain"]),

    # Gerudo Valley
    "Gerudo Valley": SohRegionData(
        ["Hyrule Field", "GV Upper Stream", "GV Crate Ledge", "GV Grotto Ledge", "GV Fortress Side",
         "GV Lower Stream"]),
    "GV Upper Stream": SohRegionData(["GV Lower Stream"]),
    "GV Lower Stream": SohRegionData(["Lake Hylia"]),
    "GV Grotto Ledge": SohRegionData(["GV Lower Stream", "GV Upper Stream", "GV Octorok Grotto", "GV Crate Ledge"]),
    "GV Crate Ledge": SohRegionData(["GV Lower Stream", "GV Upper Stream"]),
    "GV Fortress Side": SohRegionData(
        ["Gerudo Fortress", "GV Upper Stream", "Gerudo Valley", "GV Carpenter Tent", "GV Storms Grotto",
         "GV Crate Ledge"]),
    "GV Carpenter Tent": SohRegionData(["GV Fortress Side"]),
    "GV Octorok Grotto": SohRegionData(["GV Grotto Ledge"]),
    "GV Storms Grotto": SohRegionData(["GV Fortress Side"]),

    # Gerudo Fortress
    "Gerudo Fortress": SohRegionData(
        ["GV Fortress Side", "GF Outside Gate", "Gerudo Training Ground Entryway", " GF Storms Grotto"]),
    "GF Outside Gate": SohRegionData(["Gerudo Fortress", "Wasteland Near Fortress"]),
    "GF Storms Grotto": SohRegionData(["Gerudo Fortress"]),

    # Haunted Wasteland
    "Wasteland Near Fortress": SohRegionData(["GF Outside Gate", "Haunted Wasteland"]),
    "Haunted Wasteland": SohRegionData(["Wasteland Near Fortress", "Wasteland Near Colossus"]),
    "Wasteland Near Colossus": SohRegionData(["Haunted Wasteland", "Desert Colossus"]),

    # Desert Colossus
    "Desert Colossus": SohRegionData(
        ["Wasteland Near Colossus", "Desert Colossus Oasis", "Colossus Great Fairy Fountain", "Spirit Temple Entryway",
         "Colossus Grotto"]),
    "Desert Colossus Oasis": SohRegionData(["Desert Colossus"]),
    "Desert Colossus From Spirit Entryway": SohRegionData(["Desert Colossus"]),
    "Colossus Great Fairy Fountain": SohRegionData(["Desert Colossus"]),
    "Colossus Grotto": SohRegionData(["Desert Colossus"]),

    # Dungeons
    # Master Quest regions are commented out until the Master Quest option is implemented

    # Deku Tree
    "Deku Tree Entryway": SohRegionData(["Deku Tree Lobby", "KF Outside Deku Tree"]), # "Deku Tree MQ 1F"
    # Vanilla
    "Deku Tree Lobby": SohRegionData(
        ["Deku Tree Entryway", "Deku Tree 2F Middle Room", "Deku Tree Compass Room", "Deku Tree Basement Lower",
         "Deku Tree Outside Boss Room", "Deku Tree Boss Entryway"]),
    "Deku Tree 2F Middle Room": SohRegionData(["Deku Tree Lobby", "Deku Tree Slingshot Room"]),
    "Deku Tree Slingshot Room": SohRegionData(["Deku Tree 2F Middle Room"]),
    "Deku Tree Compass Room": SohRegionData(["Deku Tree Lobby", "Deku Tree Boss Entryway"]),
    "Deku Tree Basement Lower": SohRegionData(
        ["Deku Tree Lobby", "Deku Tree Basement Scrub Room", "Deku Tree Basement Upper",
         "Deku Tree Outside Boss Room"]),
    "Deku Tree Basement Scrub Room": SohRegionData(["Deku Tree Basement Lower", "Deku Tree Basement Water Room Front"]),
    "Deku Tree Basement Water Room Front": SohRegionData(
        ["Deku Tree Basement Scrub Room", "Deku Tree Basement Water Room Back"]),
    "Deku Tree Basement Water Room Back": SohRegionData(
        ["Deku Tree Basement Water Room Front", "Deku Tree Basement Torch Room"]),
    "Deku Tree Basement Torch Room": SohRegionData(
        ["Deku Tree Basement Water Room Back", "Deku Tree Basement Back Lobby"]),
    "Deku Tree Basement Back Lobby": SohRegionData(
        ["Deku Tree Basement Torch Room", "Deku Tree Basement Back Room", "Deku Tree Basement Upper"]),
    "Deku Tree Basement Back Room": SohRegionData(["Deku Tree Basement Back Lobby"]),
    "Deku Tree Basement Upper": SohRegionData(
        ["Deku Tree Basement Lower", "Deku Tree Basement Back Lobby", "Deku Tree Outside Boss Room"]),
    "Deku Tree Outside Boss Room": SohRegionData(["Deku Tree Basement Upper", "Deku Tree Boss Entryway"]),
    # Master Quest
    # "Deku Tree MQ 1F": SohRegionData(["Deku Tree Entryway", "Deku Tree MQ 2F", "Deku Tree MQ Basement"]),
    # "Deku Tree MQ 2F": SohRegionData(["Deku Tree MQ 1F", "Deku Tree MQ 3F", "Deku Tree MQ Eye Target Room"]),
    # "Deku Tree MQ 3F": SohRegionData(["Deku Tree MQ 2F", "Deku Tree MQ Eye Target Room", "Deku Tree MQ Basement"]),
    # "Deku Tree MQ Eye Target Room": SohRegionData(["Deku Tree MQ Compass Room", "Deku Tree MQ 2F"]),
    # "Deku Tree MQ Compass Room": SohRegionData(["Deku Tree MQ Eye Target Room", "Deku Tree MQ Past Boulder Vines"]),
    # "Deku Tree MQ Past Boulder Vines": SohRegionData(["Deku Tree MQ Compass Room"]),
    # "Deku Tree MQ Basement": SohRegionData(
    #     ["Deku Tree MQ 1F", "Deku Tree MQ Basement Southeast Room", "Deku Tree MQ Basement Water Room Front",
    #      "Deku Tree MQ Basement Ledge"]),
    # "Deku Tree MQ Basement Southeast Room": SohRegionData(
    #     ["Deku Tree MQ Basement Water Room Front", "Deku Tree MQ Basement"]),
    # "Deku Tree MQ Basement Water Room Front": SohRegionData(
    #     ["Deku Tree MQ Basement Water Room Back", "Deku Tree MQ Basement Southeast Room"]),
    # "Deku Tree MQ Basement Water Room Back": SohRegionData(
    #     ["Deku Tree MQ Basement Water Room Front", "Deku Tree MQ Basement Southwest Room"]),
    # "Deku Tree MQ Basement Southwest Room": SohRegionData(
    #     ["Deku Tree MQ Basement Water Room Back", "Deku Tree MQ Basement Grave Room"]),
    # "Deku Tree MQ Basement Grave Room": SohRegionData(
    #     ["Deku Tree MQ Basement Ledge", "Deku Tree MQ Basement Southwest Room", "Deku Tree MQ Basement Back Room"]),
    # "Deku Tree MQ Basement Back Room": SohRegionData(["Deku Tree MQ Basement Grave Room"]),
    # "Deku Tree MQ Outside Boss Room": SohRegionData(["Deku Tree MQ Basement Ledge", "Deku Tree Boss Entryway"]),
    # Boss Room
    "Deku Tree Boss Entryway": SohRegionData(
        ["Deku Tree Outside Boss Room", "Deku Tree Boss Room"]), # "Deku Tree MQ Outside Boss Room"
    "Deku Tree Boss Room": SohRegionData(["Deku Tree Boss Entryway", "KF Outside Deku Tree"]),

    # Dodongos Cavern
    "Dodongos Cavern Entryway": SohRegionData(
        ["Dodongos Cavern Beginning", "Death Mountain Trail"]), # "Dodongos Cavern MQ Beginning"
    # Vanilla
    "Dodongos Cavern Beginning": SohRegionData(["Dodongos Cavern Entryway", "Dodongos Cavern Lobby"]),
    "Dodongos Cavern Lobby": SohRegionData(
        ["Dodongos Cavern Beginning", "Dodongos Cavern Lobby Switch", "Dodongos Cavern SE Corridor",
         "Dodongos Cavern Stairs Lower", "Dodongos Cavern Far Bridge", "Dodongos Cavern Boss Region",
         "Dodongos Cavern Boss Entryway"]),
    "Dodongos Cavern Lobby Switch": SohRegionData(["Dodongos Cavern Lobby", "Dodongos Cavern Dodongo Room"]),
    "Dodongos Cavern SE Corridor": SohRegionData(
        ["Dodongos Cavern Lobby", "Dodongos Cavern SE Room", "Dodongos Cavern Near Lower Lizalfos"]),
    "Dodongos Cavern SE Room": SohRegionData(["Dodongos Cavern SE Corridor"]),
    "Dodongos Cavern Near Lower Lizalfos": SohRegionData(
        [" Dodongos Cavern SE Corridor", "Dodongos Cavern Lower Lizalfos"]),
    "Dodongos Cavern Lower Lizalfos": SohRegionData(
        ["Dodongos Cavern Near Lower Lizalfos", "Dodongos Cavern Dodongo Room"]),
    "Dodongos Cavern Dodongo Room": SohRegionData(
        ["Dodongos Cavern Lobby Switch", "Dodongos Cavern Lower Lizalfos", "Dodongos Cavern Near Dodongo Room"]),
    "Dodongos Cavern Near Dodongo Room": SohRegionData(["Dodongos Cavern Dodongo Room"]),
    "Dodongos Cavern Stairs Lower": SohRegionData(
        ["Dodongos Cavern Lobby", "Dodongos Cavern Stairs Upper", "Dodongos Cavern Compass Room"]),
    "Dodongos Cavern Stairs Upper": SohRegionData(["Dodongos Cavern Stairs Lower", "Dodongos Cavern Armos Room"]),
    "Dodongos Cavern Compass Room": SohRegionData(["Dodongos Cavern Stairs Lower"]),
    "Dodongos Cavern Armos Room": SohRegionData(["Dodongos Cavern Stairs Upper", "Dodongos Cavern Bomb Room Lower"]),
    "Dodongos Cavern Bomb Room Lower": SohRegionData(
        ["Dodongos Cavern Armos", "Dodongos Cavern 2F Side Room", "Dodongos Cavern First Slingshot Room",
         "Dodongos Cavern Bomb Room Upper"]),
    "Dodongos Cavern 2F Side Room": SohRegionData(["Dodongos Cavern Bomb Room Lower"]),
    "Dodongos Cavern First Slingshot Room": SohRegionData(
        ["Dodongos Cavern Bomb Room Lower", "Dodongos Cavern Upper Lizalfos"]),
    "Dodongos Cavern Upper Lizalfos": SohRegionData(
        ["Dodongos Cavern Lower Lizalfos", "Dodongos Cavern First Slingshot Room",
         "Dodongos Cavern Second Slingshot Room"]),
    "Dodongos Cavern Second Slingshot Room": SohRegionData(
        ["Dodongos Cavern Upper Lizalfos", "Dodongos Cavern Bomb Room Upper"]),
    "Dodongos Cavern Bomb Room Upper": SohRegionData(
        ["Dodongos Cavern Bomb Room Lower", "Dodongos Cavern Second Slingshot Room", "Dodongos Cavern Far Bridge"]),
    "Dodongos Cavern Far Bridge": SohRegionData(["Dodongos Cavern Lobby", "Dodongos Cavern Bomb Room Upper"]),
    "Dodongos Cavern Boss Region": SohRegionData(
        ["Dodongos Cavern Lobby", "Dodongos Cavern Back Room", "Dodongos Cavern Boss Entryway"]),
    "Dodongos Cavern Back Room": SohRegionData(["Dodongos Cavern Boss Region"]),
    # Master Quest
    # "Dodongos Cavern MQ Beginning": SohRegionData(["Dodongos Cavern Entryway", "Dodongos Cavern MQ Lobby"]),
    # "Dodongos Cavern MQ Lobby": SohRegionData(
    #     ["Dodongos Cavern MQ Beginning", "Dodongos Cavern MQ Gossip Stone", "Dodongos Cavern MQ Mouth Side Bridge",
    #      "Dodongos Cavern MQ Stairs Lower", "Dodongos Cavern MQ Lower Right Side", "Dodongos Cavern MQ Poes Room",
    #      "Dodongos Cavern MQ Behind Mouth"]),
    # "Dodongos Cavern MQ Gossip Stone": SohRegionData(["Dodongos Cavern MQ Lobby"]),
    # "Dodongos Cavern MQ Mouth Side Bridge": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Torch Puzzle Upper", "Dodongos Cavern MQ Poes Room"]),
    # "Dodongos Cavern MQ Stairs Lower": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Stairs Upper", "Dodongos Cavern MQ Stairs Past Mud Wall"]),
    # "Dodongos Cavern MQ Stairs Past Mud Wall": SohRegionData(
    #     ["Dodongos Cavern MQ Stairs Upper", "Dodongos Cavern MQ Stairs Lower"]),
    # "Dodongos Cavern MQ Stairs Upper": SohRegionData(
    #     ["Dodongos Cavern MQ Stairs Lower", "Dodongos Cavern MQ Stairs Past Big Skulltulas"]),
    # "Dodongos Cavern MQ Stairs Past Big Skulltulas": SohRegionData(
    #     ["Dodongos Cavern MQ Stairs Upper", "Dodongos Cavern MQ Stairs Lower", "Dodongos Cavern MQ Dodongo Room"]),
    # "Dodongos Cavern MQ Dodongo Room": SohRegionData(
    #     ["Dodongos Cavern MQ Stairs Past Big Skulltulas", "Dodongos Cavern MQ Torch Puzzle Lower"]),
    # "Dodongos Cavern MQ Torch Puzzle Lower": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Dodongo Room", "Dodongos Cavern MQ Larvae Room",
    #      "Dodongos Cavern MQ Big Block Room", "Dodongos Cavern MQ Torch Puzzle Upper",
    #      "Dodongos Cavern MQ Upper Lizalfos"]),
    # "Dodongos Cavern MQ Big Block Room": SohRegionData(
    #     ["Dodongos Cavern MQ Torch Puzzle Lower", "Dodongos Cavern MQ Upper Lizalfos"]),
    # "Dodongos Cavern MQ Larvae Room": SohRegionData(["Dodongos Cavern MQ Torch Puzzle Lower"]),
    # "Dodongos Cavern MQ Upper Lizalfos": SohRegionData(
    #     ["Dodongos Cavern MQ Big Block Room", "Dodongos Cavern MQ Two Fires Room"]),
    # "Dodongos Cavern MQ Two Fires Room": SohRegionData(
    #     ["Dodongos Cavern MQ Upper Lizalfos", "Dodongos Cavern MQ Torch Puzzle Upper"]),
    # "Dodongos Cavern MQ Torch Puzzle Upper": SohRegionData(
    #     ["Dodongos Cavern MQ Mouth Side Bridge", "Dodongos Cavern MQ Torch Puzzle Lower",
    #      "Dodongos Cavern MQ Two Fires Room"]),
    # "Dodongos Cavern MQ Lower Right Side": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Lower Lizalfos"]),
    # "Dodongos Cavern MQ Lower Lizalfos": SohRegionData(
    #     ["Dodongos Cavern MQ Lower Right Side", "Dodongos Cavern MQ Poes Room"]),
    # "Dodongos Cavern MQ Poes Room": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Lower Lizalfos", "Dodongos Cavern MQ Mad Scrub Room"]),
    # "Dodongos Cavern MQ Mad Scrub Rom": SohRegionData(["Dodongos Cavern MQ Poes Room"]),
    # "Dodongos Cavern MQ Behind Mouth": SohRegionData(
    #     ["Dodongos Cavern MQ Lobby", "Dodongos Cavern MQ Back Behind Fire", "Dodongos Cavern MQ BossArea"]),
    # "Dodongos Cavern MQ Back Behind Fire": SohRegionData(
    #     ["Dodongos Cavern MQ Behind Mouth", "Dodongos Cavern MQ BossArea"]),
    # "Dodongos Cavern MQ BossArea": SohRegionData(
    #     ["Dodongos Cavern MQ Back Behind Fire", "Dodongos Cavern Boss Entryway"]),
    # Boss Room
    "Dodongos Cavern Boss Entryway": SohRegionData(
        ["Dodongos Cavern Boss Region", "Dodongos Cavern Boss Room"]), # "Dodongos Cavern MQ BossArea"
    "Dodongos Cavern Boss Room": SohRegionData(["Dodongos Cavern Boss Entryway", "Death Mountain"]),

    # Jabu Jabu's Belly
    "Jabu Jabus Belly Entryway": SohRegionData(
        ["Jabu Jabus Belly Beginning", "Zoras Fountain"]), # "Jabu Jabus Belly MQ Beginning"
    # Vanilla
    "Jabu Jabus Belly Beginning": SohRegionData(["Jabu Jabus Belly Entryway", "Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Main": SohRegionData(
        ["Jabu Jabus Belly Beginning", "Jabu Jabus Belly B1 North", "Jabu Jabus Belly Compass Room",
         "Jabu Jabus Belly Blue Tentacle", "Jabu Jabus Belly Green Tentacle", "Jabu Jabus Belly Bigocto Room",
         "Jabu Jabus Belly Near Boss Room"]),
    "Jabu Jabus Belly B1 North": SohRegionData(["Jabu Jabus Belly Main", "Jabu Jabus Belly Water Switch Room Ledge",
                                                "Jabu Jabus Belly Water Switch Room South"]),
    "Jabu Jabus Belly Water Switch Room Ledge": SohRegionData(
        ["Jabu Jabus Belly B1 North", "Jabu Jabus Belly Water Switch Room South"]),
    "Jabu Jabus Belly Water Switch Room South": SohRegionData(
        ["Jabu Jabus Belly B1 North", "Jabu Jabus Belly Water Switch Room Ledge", "Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Compass Room": SohRegionData(["Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Blue Tentacle": SohRegionData(["Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Green Tentacle": SohRegionData(["Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Bigocto Room": SohRegionData(
        ["Jabu Jabus Belly B1 North", "Jabu Jabus Belly Above Bigocto Room"]),
    "Jabu Jabus Belly Lift Upper": SohRegionData(["Jabu Jabus Belly Main"]),
    "Jabu Jabus Belly Near Boss Room": SohRegionData(["Jabu Jabus Belly Main", "Jabu Jabus Belly Boss Entryway"]),
    # Master Quest
    # "Jabu Jabus Belly MQ Beginning": SohRegionData(["Jabu Jabus Belly Entryway", "Jabu Jabus Belly MQ Lift Room"]),
    # "Jabu Jabus Belly MQ Lift Room": SohRegionData(
    #     ["Jabu Jabus Belly MQ Beginning", "Jabu Jabus Belly MQ Underwater Alcove", "Jabu Jabus Belly MQ Holes Room",
    #      "Jabu Jabus Belly MQ Lift Room East Ledge"]),
    # "Jabu Jabus Belly MQ Underwater Alcove": SohRegionData(["Jabu Jabus Belly MQ Lift Room"]),
    # "Jabu Jabus Belly MQ Holes Room": SohRegionData(
    #     ["Jabu Jabus Belly MQ Lift Room", "Jabu Jabus Belly MQ Water Switch Room",
    #      "Jabu Jabus Belly MQ Forked Corridor", "Jabu Jabus Belly MQ Invisible Keese Room",
    #      "Jabu Jabus Belly MQ Past Octo"]),
    # "Jabu Jabus Belly MQ Water Switch Room": SohRegionData(
    #     ["Jabu Jabus Belly MQ Beginning", "Jabu Jabus Belly MQ Holes Room"]),
    # "Jabu Jabus Belly MQ Forked Corridor": SohRegionData(
    #     ["Jabu Jabus Belly MQ Holes Room", "Jabu Jabus Belly MQ West Forked Rooms"]),
    # "Jabu Jabus Belly MQ West Forked Rooms": SohRegionData(["Jabu Jabus Belly MQ Forked Corridor"]),
    # "Jabu Jabus Belly MQ Invisible Keese Room": SohRegionData(["Jabu Jabus Belly MQ Holes Room"]),
    # "Jabu Jabus Belly MQ Past Octo": SohRegionData(
    #     ["Jabu Jabus Belly MQ Lift Room East Ledge", "Jabu Jabus Belly MQ Holes Room"]),
    # "Jabu Jabus Belly MQ Lift Room East Ledge": SohRegionData(
    #     ["Jabu Jabus Belly MQ Lift Room", "Jabu Jabus Belly MQ Boss Region"]),
    # "Jabu Jabus Belly MQ Boss Region": SohRegionData(
    #     ["Jabu Jabus Belly MQ Lift Room East Ledge", "Jabu Jabus Belly Boss Entryway"]),
    # Boss Rooms
    "Jabu Jabus Belly Boss Entryway": SohRegionData(
        ["Jabu Jabus Belly Near Boss Room", "Jabu Jabus Belly Boss Room"]), # "Jabu Jabus Belly MQ Boss Region"
    "Jabu Jabus Boss Room": SohRegionData(["Jabu Jabus Belly Boss Entryway", "Zoras Fountain"]),

    # Forest Temple
    "Forest Temple Entryway": SohRegionData(
        ["Sacred Forest Meadow", "Forest Temple First Room"]), # "Forest Temple MQ Lobby"
    # Vanilla
    "Forest Temple First Room": SohRegionData(["Forest Temple First Room", "Forest Temple South Corridor"]),
    "Forest Temple South Corridor": SohRegionData(["Forest Temple First Room", "Forest Temple Lobby"]),
    "Forest Temple Lobby": SohRegionData(
        ["Forest Temple South Corridor", "Forest Temple North Corridor", "Forest Temple NW Outdoors Lower",
         "Forest Temple NE Outdoors Lower", "Forest Temple West Corridor", "Forest Temple East Corridor",
         "Forest Temple Boss Region", "Forest Temple Boss Entryway"]),
    "Forest Temple North Corridor": SohRegionData(["Forest Temple Lobby", "Forest Temple Lower Stalfos"]),
    "Forest Temple Lower Stalfos": SohRegionData(["Forest Temple North Corridor"]),
    "Forest Temple NW Outdoors Lower": SohRegionData(
        ["Forest Temple Lobby", "Forest Temple NW Outdoors Upper", "Forest Temple Map Room", "Forest Temple Sewer",
         "Forest Temple Boss Entryway"]),
    "Forest Temple NW Outdoors Upper": SohRegionData(
        ["Forest Temple NW Outdoors Lower", "Forest Below Boss Key Chest", "Forest Temple Floormaster Room",
         "Forest Temple Block Push Room"]),
    "Forest Temple NE Outdoors Lower": SohRegionData(
        ["Forest Temple Lobby", "Forest Temple NE Outdoors Upper", "Forest Temple Sewer",
         "Forest Temple Falling Room"]),
    "Forest Temple NE Outdoors Upper": SohRegionData(
        ["Forest Temple NE Outdoors Lower", "Forest Temple Map Room", "Forest Temple Falling Room"]),
    "Forest Temple Map Room": SohRegionData(["Forest Temple NW Outdoors Lower", "Forest Temple NE Outdoors Upper"]),
    "Forest Temple Sewer": SohRegionData(["Forest Temple NW Outdoors Lower", "Forest Temple NE Outdoors Lower"]),
    "Forest Temple Below Boss Key Chest": SohRegionData(["Forest Temple NW Outdoors Upper"]),
    "Forest Temple Floormaster Room": SohRegionData(["Forest Temple NW Outdoors Upper"]),
    "Forest Temple West Corridor": SohRegionData(["Forest Temple Lobby", "Forest Temple Block Push Room"]),
    "Forest Temple Block Push Room": SohRegionData(
        ["Forest Temple West Corridor", "Forest Temple NW Outdoors Upper", "Forest Temple NW Corridor Twisted",
         "Forest Temple NW Corridor Straightened"]),
    "Forest Temple NW Corridor Twisted": SohRegionData(["Forest Temple Block Push Room", "Forest Temple Red Poe Room"]),
    "Forest Temple NW Corridor Straightened": SohRegionData(
        ["Forest Temple Below Boss Key Chest", "Forest Temple Block Push Room"]),
    "Forest Temple Red Poe Room": SohRegionData(["Forest Temple NW Corridor Twisted", "Forest Temple Upper Stalfos"]),
    "Forest Temple Upper Stalfos": SohRegionData(["Forest Temple Red Poe Room", "Forest Temple Blue Poe Room"]),
    "Forest Temple Blue Poe Room": SohRegionData(
        ["Forest Temple Upper Stalfos", "Forest Temple NE Corridor Straightened"]),
    "Forest Temple NE Corridor Straightened": SohRegionData(
        ["Forest Temple Blue Poe Room", "Forest Temple Frozen Eye Room"]),
    "Forest Temple NE Corridor Twisted": SohRegionData(["Forest Temple Frozen Eye Room", "Forest Temple Falling Room"]),
    "Forest Temple Frozen Eye Room": SohRegionData(
        ["Forest Temple NE Corridor Straightened", "Forest Temple NE Corridor Twisted"]),
    "Forest Temple Falling Room": SohRegionData(["Forest Temple NE Outdoors Lower", "Forest Temple Gree Poe Room"]),
    "Forest Temple Green Poe Room": SohRegionData(["Forest Temple Falling Room", "Forest Temple East corridor"]),
    "Forest Temple East Corridor": SohRegionData(["Forest Temple Lobby", "Forest Temple Green Poe Room"]),
    "Forest Temple Boss Region": SohRegionData(["Forest Temple Lobby", "Forest Temple Boss Entryway"]),
    # Master Quest
    # "Forest Temple MQ Lobby": SohRegionData(["Forest Temple Entryway", "Forest Temple MQ Central Region"]),
    # "Forest Temple MQ Central Region": SohRegionData(
    #     ["Forest Temple MQ Wolfos Room", "Forest Temple MQ NW Outdoors", "Forest Temple MQ NE Outdoors",
    #      "Forest Temple MQ Lower Block Puzzle", "Forest Temple MQ Basement"]),
    # "Forest Temple MQ Wolfos Room": SohRegionData(["Forest Temple MQ Central Region"]),
    # "Forest Temple MQ Lower Block Puzzle": SohRegionData(
    #     ["Forest Temple MQ Central Region", "Forest Temple MQ Middle Block Puzzle",
    #      "Forest Temple MQ After Block Puzzle", "Forest Temple MQ Outdoor Ledge"]),
    # "Forest Temple MQ Middle Block Puzzle": SohRegionData(
    #     ["Forest Temple MQ Lower Block Puzzle", "Forest Temple MQ After Block Puzzle",
    #      "Forest Temple MQ Outdoor Ledge"]),
    # "Forest Temple MQ After Block Puzzle": SohRegionData(
    #     ["Forest Temple MQ Straight Hallway", "Forest Temple MQ Joelle Room", "Forest Temple MQ NW Outdoors"]),
    # "Forest Temple MQ Straight Hallway": SohRegionData(["Forest Temple MQ Floormaster Room"]),
    # "Forest Temple MQ Floormaster Room": SohRegionData(["Forest Temple MQ Outdoor Ledge"]),
    # "Forest Temple MQ Outdoor Ledge": SohRegionData(["Forest Temple MQ NW Outdoors"]),
    # "Forest Temple MQ NW Outdoors": SohRegionData(
    #     ["Forest Temple MQ NE Outdoors", "Forest Temple MQ Outdoors Top Ledges"]),
    # "Forest Temple MQ NE Outdoors": SohRegionData(
    #     ["Forest Temple MQ NW Outdoors", "Fores Temple MQ Outdoors Top Ledges", "Forest Temple MQ NE Outdoors Ledge"]),
    # "Forest Temple MQ Outdoors Top Ledge": SohRegionData(
    #     ["Forest Temple MQ NW Outdoors", "Forest Temple MQ NE Outdoors", "Forest Temple MQ NE Outdoors Ledge"]),
    # "Forest Temple MQ NE Outdoors Ledge": SohRegionData(
    #     ["Forest Temple MQ NE Outdoors", "Forest Temple MQ Falling Room"]),
    # "Forest Temple MQ Joelle Room": SohRegionData(
    #     ["Forest Temple MQ After Block Puzzle", "Forest Temple MQ 3 Stalfos Room"]),
    # "Forest Temple MQ 3 Stalfos Room": SohRegionData(["Forest Temple MQ Joelle Room", "Forest Temple MQ Beth Room"]),
    # "Forest Temple MQ Beth Room": SohRegionData(
    #     ["Forest Temple MQ 3 Stalfos Room", "Forest Temple MQ Falling Room", "Forest Temple MQ Torch Shot Room"]),
    # "Forest Temple MQ Torch Shot Room": SohRegionData(["Forest Temple MQ Falling Room", "Forest Temple MQ Beth Room"]),
    # "Forest Temple MQ Falling Room": SohRegionData(["forest Temple MQ NE Outdoors Ledge", "Forest Temple MQ Amy Room"]),
    # "Forest Temple MQ Amy Room": SohRegionData(["Forest Temple MQ Central Region", "Forest Temple MQ Falling Room"]),
    # "Forest Temple MQ Basement": SohRegionData(
    #     ["Forest Temple MQ Central Region", "Forest Temple MQ Basement Pot Room", "Forest Temple MQ Boss Region"]),
    # "Forest Temple MQ Basement Pot Room": SohRegionData(["Forest Temple MQ Basement"]),
    # "Forest Temple MQ Boss Region": SohRegionData(["Forest Temple MQ Basement", "Forest Temple Boss Entryway"]),
    # Boss Room
    "Forest Temple Boss Entryway": SohRegionData(
        ["Forest Temple Boss Region", "Forest Temple Boos Room"]), # "Forest Temple MQ Boss Region"
    "Forest Temple Boss Room": SohRegionData(["Forest Temple Boss Entryway", "Sacred Forest Meadow"]),

    # Fire Temple
    "Fire Temple Entryway": SohRegionData(
        ["Fire Temple First Room", "DMC Central Local"]), # "Fire Temple MQ First Room Lower"
    # Vanilla
    "Fire Temple First Room": SohRegionData(
        ["Fire Temple Entryway", "Fire Temple Near Boss Room", "Fire Temple Loop Enemies", "Fire Temple Loop Exit",
         "Fire Temple Big Lava Room"]),
    "Fire Temple Near Boss Room": SohRegionData(["Fire Temple First Room", "Fire Temple Boss Entryway"]),
    "Fire Temple Loop Enemies": SohRegionData(["Fire Temple First Room", "Fire Temple Loop Tiles"]),
    "Fire Temple Loop Tiles": SohRegionData(["Fire Temple Loop Enemies", "Fire Temple Loop Flare Dancer"]),
    "Fire Temple Loop Flare Dancer": SohRegionData(["Fire Temple Loop Tiles", "Fire Temple Loop Hammer Switch"]),
    "Fire Temple Loop Hammer Switch": SohRegionData(["Fire Temple Flare Dancer", "Fire Temple Goron Room"]),
    "Fire Temple Loop Goron Room": SohRegionData(["Fire Temple Loop Hammer Switch", "Fire Temple Loop Exit"]),
    "Fire Temple Loop Exit": SohRegionData(["Fire Temple Loop Goron Room", "Fire Temple First Room"]),
    "Fire Temple Big Lava Room": SohRegionData(
        ["Fire Temple Fire Room", "Fire Temple Big Lava Room North Goron", "Fire Temple Big Lava Room North Tiles",
         "Fire Temple Big Lava Room South Goron", "Fire Temple Fire Pillar Room"]),
    "Fire Temple Big Lava Room North Goron": SohRegionData(["Fire Temple Big Lava Room"]),
    "Fire Temple Big Lava Room North Tiles": SohRegionData(["Fire Temple Big Lava Room"]),
    "Fire Temple Big Lava Room South Goron": SohRegionData(["Fire Temple Big Lava Room"]),
    "Fire Temple Fire Pillar Room": SohRegionData(["Fire Temple Big Lava Room", "Fire Temple Shortcut Room"]),
    "Fire Temple Shortcut Room": SohRegionData(
        ["Fire Temple Fire Pillar Room", "Fire Tmple Shortcut Climb", "Fire Temple Boulder Maze Lower"]),
    "Fire Temple Shortcut Climb": SohRegionData(["Fire Temple Shortcut Room", "Fire Temple Boulder Maze Upper"]),
    "Fire Temple Bolder Maze Lower": SohRegionData(
        ["Fire Temple Shortcut Room", "Fire Temple Boulder Maze Lower Side Room", "Fire Temple East Central Room",
         "Fire Temple Boulder Maze Upper"]),
    "Fire Temple Boulder Maze Lower Side Room": SohRegionData(["Fire Temple Boulder Maze Lower"]),
    "Fire Temple East Central Room": SohRegionData(
        ["Fire Temple Big Lava Room", "Fire Temple Boulder Maze Lower", "Fire Temple Fire Wall Chase",
         "Fire Temple Map Region"]),
    "Fire Temple Wall Chase": SohRegionData(
        ["Fire Tmple East Central Room", "Fire Temple Map Region", "Fire Temple Boulder Maze Upper",
         "Fire Temple Corridor"]),
    "Fire Temple Map Region": SohRegionData(["Fire Temple East Central Room"]),
    "Fire Temple Boulder Maze Upper": SohRegionData(
        ["Fire Temple Shortcut Climb", "Fire Temple Boulder Maze Lower", "Fire Temple Fire Wall Chase",
         "Fire Temple Scarecrow Room"]),
    "Fire Temple Scarecrow Room": SohRegionData(["Fire Temple Boulder Maze Upper", "Fire Temple East Peak"]),
    "Fire Temple East Peak": SohRegionData(["Fire Temple Scarecrow Room", "Fire Temple East Central Room"]),
    "Fire Temple Corridor": SohRegionData(["Fire Temple Fire Wall Chase", "Fire Temple Fire Maze Room"]),
    "Fire Temple Fire Maze Room": SohRegionData(
        ["Fire Temple Near Boss Room", "Fire Temple Fire Maze Upper", "Fire Temple Fire Maze Side Room",
         "Fire Temple West Central Lower", "Fire Temple Late Fire Maze"]),
    "Fire Temple Fire Maze Upper": SohRegionData(
        ["Fire Temple Near Boss Room", "Fire Temple Fire Maze Room", "Fire Temple Wester Central Upper"]),
    "Fire Temple Maze Side Room": SohRegionData(["Fire Temple Fire Maze Room"]),
    "Fire Temple West Central Lower": SohRegionData(
        ["Fire Temple Fire Maze Room", "Fire Temple West Central Upper", "Fire Temple Late Fire Maze"]),
    "Fire Temple West Central Upper": SohRegionData(
        ["Fire Temple Boss Entryway", "Fire Temple Fire Maze Upper", "Fire Temple West Central Lower"]),
    "Fire Temple Late Fire Maze": SohRegionData(
        ["Fire Temple Fire Maze Room", "Fire Temple West Central Lower", "Fire Temple Upper Flare Dancer"]),
    "Fire Temple Upper Flare Dancer": SohRegionData(["Fire Temple Late Fire Maze", "Fire Temple West Climb"]),
    "Fire Temple West Climb": SohRegionData(["Fire Temple Upper Flare Dancer", "Fire Temple West Peak"]),
    "Fire Temple West Peak": SohRegionData(
        ["Fire Temple West Central Upper", "Fire Temple West Climb", "Fire Temple Hammer Return Path"]),
    "Fire Temple Hammer Return Path": SohRegionData(["Fire Temple Above Fire Maze"]),
    "Fire Temple Above Fire Maze": SohRegionData(["Fire Temple Hammer Return Path", "Fire Temple Fire Maze Upper"]),
    # Master Quest
    # "Fire Temple MQ First Room Lower": SohRegionData(
    #     ["Fire Temple Entryway", "Fire Temple MQ Map Room South", "Fire Temple MQ First Room Upper",
    #      "Fire Temple Stalfos Room"]),
    # "Fire Temple MQ First Room Upper": SohRegionData(
    #     ["Fire Temple MQ First Room Lower", "Fire Temple MQ Near Boss Room", "Fire Temple MQ Big Lava Room"]),
    # "Fire Temple MQ Map Room South": SohRegionData(["Fire Temple MQ First Room Lower", "Fire Temple MQ Map Room Cage"]),
    # "Fire Temple MQ Stalfos Room": SohRegionData(["Fire Temple First Room Lower", "Fire Temple MQ Iron Knuckle Room"]),
    # "Fire Temple MQ Iron Knuckle Room": SohRegionData(
    #     ["Fire Temple MQ Stalfos Room", "Fire Temple MQ Lower Flare Dancer"]),
    # "Fire Temple MQ Lower Flare Dancer": SohRegionData(
    #     ["Fire Temple MQ Iron Knuckle Room", "Fire Temple MQ Map Room North"]),
    # "Fire Temple MQ Map Room North": SohRegionData(
    #     ["Fire Temple MQ Lower Flare Dancer", "Fire Temple MQ Map Room Cage"]),
    # "Fire Temple MQ Map Room Cage": SohRegionData(["Fire Temple MQ Map Room North", "Fire Temple MQ Map Room South"]),
    # "Fire Temple MQ Near Boss Room": SohRegionData(
    #     ["Fire Temple MQ First Room Upper", "Fire Temple MQ Near Boss Room North", "Fire Temple Boss Entryway"]),
    # "Fire Temple MQ near Boss Room North": SohRegionData(["Fire Temple MQ Near Boss Room"]),
    # "Fire Temple MQ Big Lava Room": SohRegionData(
    #     ["Fire Temple MQ First Room Upper", "Fire Temple MQ Elevator Room", "Fire Temple MQ Torch Firewall Room"]),
    # "Fire Temple MQ Torch Firewall Room": SohRegionData(["Fire Temple MQ Big Lava Room"]),
    # "Fire Temple MQ Elevator Room": SohRegionData(["Fire Temple MQ Big Lava Room"]),
    # "Fire Temple MQ Big Torch Room": SohRegionData(
    #     ["Fire Temple MQ Lower Maze", "Fire Temple MQ Elevator Room", "Fire Temple MQ Maze Shortcut Cage"]),
    # "Fire Temple MQ Lower Maze": SohRegionData(
    #     ["Fire Temple MQ Big Torch Room", "Fire Temple MQ Lower Maze Crate Cage", "Fire Temple MQ Upper Maze"]),
    # "Fire Temple MQ Lower Maze Crate Cage": SohRegionData(["Fire Temple MQ Lower Maze", "Fire Temple MQ Upper Maze"]),
    # "Fire Temple MQ Upper Maze": SohRegionData(
    #     ["Fire Temple MQ Lower Maze", "Fire Temple MQ Upper Maze Box Cage", "Fire Temple MQ Maze Shortcut",
    #      "Fire Temple MQ Burning Block Climb", "Fire Temple MQ High Torch Room"]),
    # "Fire Temple MQ Upper Maze Box Cage": SohRegionData(["Fire Temple MQ Upper Maze"]),
    # "Fire Temple MQ Maze Shortcut": SohRegionData(["Fire Temple MQ Upper Maze", "Fire Temple MQ Shortcut Cage"]),
    # "Fire Temple MQ Maze Shortcut Cage": SohRegionData(
    #     ["Fire Temple MQ Maze Shortcut", "Fire Temple MQ Big Torch Room"]),
    # "Fire Temple MQ Burning Block Cage": SohRegionData(
    #     ["Fire Temple MQ Upper Maze", "Fire Temple MQ Narrow Path Room"]),
    # "Fire Temple MQ Narrow Path Room": SohRegionData(["Fire Temple MQ Lower Maze", "Fire Temple MQ Big Lava Room"]),
    # "Fire Temple MQ High Torch Room": SohRegionData(
    #     ["Fire Temple MQ Upper Maze", "Fire Temple MQ Narrow Path Room", "Fire Temple MQ South Fire Maze"]),
    # "Fire Temple MQ South Fire Maze": SohRegionData(
    #     ["Fire Temple MQ Near Boss Room", "Fire Temple MQ High Torch Room", "Fire Temple MQ Fire Maze Platforms",
    #      "Fire Temple MQ North Fire Maze", "Fire Temple West Fire Maze"]),
    # "Fire Temple MQ Fire Maze Platforms": SohRegionData(
    #     ["Fire Temple MQ South Fire Maze", "Fire Temple MQ North Fire Maze"]),
    # "Fire Temple MQ North Fire Maze": SohRegionData(
    #     ["Fire Temple MQ South Fire Maze", "Fire Temple MQ West Fire Maze"]),
    # "Fire Temple MQ West Fire Maze": SohRegionData(
    #     ["Fire Temple MQ Fire Maze Past Wall", "Fire Temple MQ North Fire Maze"]),
    # "Fire Temple MQ Fire Maze Past Wall": SohRegionData(["Fire Temple MQ Upper Flare Dancer"]),
    # "Fire Temple MQ Upper Flare Dancer": SohRegionData(
    #     ["Fire Temple MQ Fire Maze Past Wall", "Fire Temple MQ Scarecrow Room"]),
    # "Fire Temple MQ Scarecrow Room": SohRegionData(
    #     ["Fire Temple MQ Upper Flare Dancer", "Fire Temple MQ Collapsed Stairs"]),
    # "Fire Temple MQ Collapsed Stairs": SohRegionData(
    #     ["Fire Temple MQ Fire Maze Platforms", "Fire Temple MQ Scarecrow Room"]),
    # Boos Room
    "Fire Temple Boss Entryway": SohRegionData(
        ["Fire Temple Near Boss Room", "Fire Temple Boss Room"]), # "Fire Temple MQ Near Boss Room"
    "Fire Temple Boss Room": SohRegionData(["Fire Temple Boss Entryway", "DMC Central Local"]),

    # Water Temple
    "Water Temple Entryway": SohRegionData(["Water Temple Lobby", "Lake Hylia"]), # "Water Temple MQ 3F South Ledge"
    # Vanilla
    "Water Temple Lobby": SohRegionData(
        ["Water Temple Entryway", "Water Temple East Lower", "Water Temple North Lower", "Water Temple South Lower",
         "Water Temple West Lower", "Water Temple Central Pillar Lower", "Water Temple Central Pillar Upper",
         "Water Temple East Middle", "Water Temple West Middle", "Water Temple High Water",
         "Water Temple Block Corridor", "Water Temple Falling Platform Room", "Water Temple Pre Boss Room"]),
    "Water Temple East Lower": SohRegionData(
        ["Water Temple Lobby", "Water Temple Map Room", "Water Temple Cracked Wall", "Water Temple Torch Room"]),
    "Water Temple Map Room": SohRegionData(["Water Temple East Lower"]),
    "Water Temple Cracked Wall": SohRegionData(["Water Temple East Lower"]),
    "Water Temple Torch Room": SohRegionData(["Water Temple East Lower"]),
    "Water Temple North Lower": SohRegionData(["Water Temple Lobby", "Water Temple Boulders Lower"]),
    "Water Temple Boulders Lower": SohRegionData(
        ["Water Temple North Lower", "Water Temple Block Room", "Water Temple Boulders Upper"]),
    "Water Temple Block Room": SohRegionData(["Water Temple Boulders Lower", "Water Temple Jets Room"]),
    "Water Temple Jets Room": SohRegionData(["Water Temple Block Room", "Water Temple Boulders Upper"]),
    "Water Temple Boulders Upper": SohRegionData(
        ["Water Temple Boulders Lower", "Water Temple Jets Room", "Water Temple Boss Key Room"]),
    "Water Temple Boss Key Room": SohRegionData(["Water Temple Boulders Upper"]),
    "Water Temple South Lower": SohRegionData(["Water Temple Lobby"]),
    "Water Temple West Lower": SohRegionData(["Water Temple Lobby", "Water Temple Dragon Room"]),
    "Water Temple Dragon Room": SohRegionData(["Water Temple West Lower"]),
    "Water Temple Central Pillar Lower": SohRegionData(
        ["Water Temple Lobby", "Water Temple Central Pillar Upper", "Water Temple Central Pillar Basement"]),
    "Water Temple Central Pillar Upper": SohRegionData(["Water Temple Lobby", "Water Temple Central Pillar Lower"]),
    "Water Temple Central Pillar Basement": SohRegionData(["Water Temple Central Pillar Lower"]),
    "Water Temple East Middle": SohRegionData(["Water Temple Lobby"]),
    "Water Temple West Middle": SohRegionData(["Water Temple Lobby", "Water Temple High Water"]),
    "Water Temple High Water": SohRegionData(["Water Temple Lobby"]),
    "Water Temple Block Corridor": SohRegionData(["Water Temple Lobby"]),
    "Water Temple Falling Platform Room": SohRegionData(["Water Temple Lobby", "Water Temple Dragon Pillars Room"]),
    "Water Temple Dragon Pillars Room": SohRegionData(
        ["Water Temple Falling Platform Room", "Water Temple Dark Link Room"]),
    "Water Temple Dark Link Room": SohRegionData(["Water Temple Dragon Pillars Room", "Water Temple Longshot Room"]),
    "Water Temple Longshot Room": SohRegionData(["Water Temple Dark Link Room", "Water Temple River"]),
    "Water Temple River": SohRegionData(["Water Temple Dragon Room"]),
    "Water Temple Pre Boss Room": SohRegionData(["Water Temple Lobby", "Water Temple Boss Entryway"]),
    # Master Quest
    # "Water Temple MQ 3F South Ledge": SohRegionData(
    #     ["Water Temple Entryway", "Water Temple MQ Main", "Water Temple 3F Central", "Water Temple 2F Central"]),
    # "Water Temple MQ Main": SohRegionData(
    #     ["Water Temple MQ South Ledge", "Water Temple MQ East Tower", "Water Temple MQ 3F Central",
    #      "Water Temple MQ 2F Central", "Water Temple MQ Central Pillar 1F", "Water Temple MQ Central Pillar High",
    #      "Water Temple MQ B1 Gate Switch", "Water Temple Triangle Torch Room", "Water Temple Crates Whirlpools Room"]),
    # "Water Temple MQ 3F Central": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ 3F South Ledge", "Water Temple MQ 2F Central",
    #      "Water Temple MQ Central Pillar High", "Water Temple MQ 3F North Ledge", "Water Temple MQ High Emblem",
    #      "Water Temple MQ Waterfall", "Water Temple MQ Lizalfos Hallway"]),
    # "Water Temple MQ 2F Central": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ 3F Central", "Water Temple MQ Central Pillar 2F",
    #      "Water Temple MQ Storage Room", "Water Temple MQ Behind Blue Switch 2F", "Water Temple MQ Lizalfos Hallway"]),
    # "Water Temple MQ High Emblem": SohRegionData(["Water Temple MQ 3F Central", "Water Temple MQ Main"]),
    # "Water Temple MQ 3F North Ledge": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ 3F Central", "Water Temple MQ Boss Door"]),
    # "Water Temple MQ Boss Door": SohRegionData(["Water Temple 3F North Ledge", "Water Temple Boss Entryway"]),
    # "Water Temple MQ East Tower": SohRegionData(["Water Temple MQ East Tower 1F Room"]),
    # "Water Temple MQ East Tower 1F Room": SohRegionData(["Water Temple MQ East Tower"]),
    # "Water Temple MQ Central Pillar 1F": SohRegionData(
    #     ["Water Temple MQ Central Pillar High", "Water Temple MQ Central Pillar 2F",
    #      "Water Temple MQ Central Pillar B1"]),
    # "Water Temple MQ Central Pillar 2F": SohRegionData(
    #     ["Water Temple MQ Central Pillar High", "Water Temple MQ Central Pillar B1"]),
    # "Water Temple MQ Central Pillar High": SohRegionData(["Water Temple MQ Central Pillar B1"]),
    # "Water Temple MQ Central Pillar B1": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple Central Pillar B1 Final"]),
    # "Water Temple MQ Central Pillar B1 Final": SohRegionData([]),
    # "Water Temple MQ Storage Room": SohRegionData(["Water Temple MQ Main"]),
    # "Water Temple MQ Behind Blue Switch 2F": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ Behind Blue Switch 3F"]),
    # "Water Temple MQ Behind Blue Switch 3F": SohRegionData(
    #     ["Water Temple MQ Behind blue Switch 2F", "Water Temple MQ High Emblem"]),
    # "Water Temple MQ Lizalfos Hallway": SohRegionData(["Water Temple MQ Lizalfos Cage"]),
    # "Water Temple MQ Lizalfos Cage": SohRegionData([]),
    # "Water Temple MQ Waterfall": SohRegionData(
    #     ["Water Temple MQ 3F Central", "Water Temple MQ Stalfos Pit", "Water Temple MQ Stalfos Pit Pots",
    #      "Water Temple MQ Stalfos Pit Upper"]),
    # "Water Temple MQ Stalfos Pit": SohRegionData(
    #     ["Water Temple MQ Waterfall", "Water Temple MQ Stalfos Pit Pots", "Water Temple MQ Stalfos Pit Upper"]),
    # "Water Temple MQ Stalfos Pit Pots": SohRegionData(
    #     ["Water Temple MQ Waterfall", "Water Temple MQ Stalfos Pit", "Water Temple MQ Stalfos Pit Upper"]),
    # "Water Temple MQ Stalfos Pit Upper": SohRegionData(
    #     ["Water Temple MQ Stalfos Pit", "Water Temple Stalfos Pit Pots", "Water Temple MQ After Dark Link"]),
    # "Water Temple MQ After Dark Link": SohRegionData(
    #     ["Water Temple MQ Stalfos Pit Upper", "Water Temple MQ River Skull"]),
    # "Water Temple MQ River Skull": SohRegionData(["Water Temple MQ River Pots"]),
    # "Water Temple MQ River Pots": SohRegionData(
    #     ["Water Temple MQ River Skull", "Water Temple MQ Dragon Room Tunnel", "Water Temple MQ Dragon Room Alcove",
    #      "Water Temple MQ Dragon Room Door"]),
    # "Water Temple MQ Dragon Room Tunnel": SohRegionData(
    #     ["Water Temple MQ River Pots", "Water Temple Dragon Room Alcove", "Water Temple MQ Dragon Room Door"]),
    # "Water Temple MQ Dragon Room Alcove": SohRegionData(
    #     ["Water Temple MQ Dragon Room Tunnel", "Water Temple MQ Dragon Room Door"]),
    # "Water Temple MQ Dragon Room Door": SohRegionData(
    #     ["Water Temple MQ River Pots", "Water Temple MQ Dragon Room Tunnel", "Water Temple MQ Dragon Room Alcove",
    #      "Water Temple MQ Boss Key Room Switch"]),
    # "Water Temple MQ Boss Key Room Switch": SohRegionData(
    #     ["Water Temple MQ Dragon Room Door", "Water Temple MQ Boss Key Room Pit",
    #      "Water Temple MQ Boss Key Room Chest"]),
    # "Water Temple MQ Boss Key Room Pit": SohRegionData(["Water Temple MQ Boss Key Room Switch"]),
    # "Water Temple MQ Boss Key Room Chest": SohRegionData(
    #     ["Water Temple MQ Boss Key Room Switch", "Water Temple MQ Boss Key Room Pit",
    #      "Water Temple MQ B1 Gate Switch"]),
    # "Water Temple MQ B1 Gate Switch": SohRegionData(["Water Temple MQ Main", "Water Temple MQ Boss Key Room Chest"]),
    # "Water Temple MQ Triangle Torch Room": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ Triangle Torch Cage"]),
    # "Water Temple MQ Triangle Torch Cage": SohRegionData([]),
    # "Water Temple MQ Crates Whirlpools Room": SohRegionData(
    #     ["Water Temple MQ Main", "Water Temple MQ Single Stalfos Room", "Water Temple MQ 4 Torch Room",
    #      "Water Temple MQ Basement Gated Areas"]),
    # "Water Temple MQ Single Stalfos Room": SohRegionData(["Water Temple MQ Crates Whirlpools Room"]),
    # "Water Temple MQ 4 Torch Room": SohRegionData(
    #     ["Water Temple MQ Crates Whirlpools Room", "Water Temple MQ Dodongo Room"]),
    # "Water Temple MQ Dodongo Room": SohRegionData(
    #     ["Water Temple MQ 4 Torch Room", "Water Temple MQ Basement Gated Areas"]),
    # "Water Temple MQ Basement Gated Areas": SohRegionData(["Water Temple MQ Dodongo Room"]),
    # Boss Room
    "Water Temple Boss Entryway": SohRegionData(
        ["Water Temple Pre Boss Room", "Water Temple Boss Room"]), # "Water Temple MQ Boss Door"
    "Water Temple Boss Room": SohRegionData(["Water Temple Boss Entryway", "Lake Hylia"]),

    # Spirit Temple
    "Sprit Temple Entryway": SohRegionData(
        ["Spirit Temple Lobby", "Desert Colossus Outside Temple"]), # "Spirit Temple MQ Lobby"
    # Vanilla
    "Sprit Temple Lobby": SohRegionData(["Spirit Temple Entryway", "Child Spirit Temple", "Early Adult Spirit Temple"]),
    "Child Spirit Temple": SohRegionData(["Child Spirit Temple Climb"]),
    "Child Spirit Temple Climb": SohRegionData(["Spirit Temple Central Chamber"]),
    "Early Adult Spirit Temple": SohRegionData(["Spirit Temple Central Chamber"]),
    "Spirit Temple Central Chamber": SohRegionData(
        ["Spirit Temple Outdoor Hands", "Spirit Temple Beyond Central Locked Door", "Child Spirit Temple Climb",
         "Spirit Temple Inside Statue Head"]),
    "Spirit Temple Outdoor Hands": SohRegionData(["Desert Colossus"]),
    "Spirit Temple Beyond Central Locked Door": SohRegionData(["Spirit Temple Beyond Final Locked Door"]),
    "Spirit Temple Beyond Final Locked Door": SohRegionData(["Spirit Temple Inside Statue Head"]),
    "Spirit Temple Inside Statue Head": SohRegionData(["Spirit Temple Central Chamber", "Spirit Temple Boss Entryway"]),
    # Master Quest
    # "Spirit Temple MQ Lobby": SohRegionData(
    #     ["Spirit Temple Entryway", "Spirit Temple MQ 1F West", "Spirit Temple MQ Big Block Room South"]),
    # "Spirit Temple MQ 1F West": SohRegionData(
    #     ["Spirit Temple MQ 1F Gibdo Room South", "Spirit Temple MQ Map Room South",
    #      "Spirit Temple MQ West 1F Rusted Switch"]),
    # "Spirit Temple MQ 1F Gibdo Room South": SohRegionData(
    #     ["Spirit Temple MQ 1F West", "Spirit Temple MQ 1F Gibdo Room North", "Spirit Temple MQ Turntable Room"]),
    # "Spirit Temple MQ 1F Gibdo Room North": SohRegionData([]),
    # "Spirit Temple MQ Turntable Room": SohRegionData(
    #     ["Spirit Temple MQ 1F Gibdo Room North", "Spirit Temple MQ Map Room North"]),
    # "Spirit Temple MQ Map Room North": SohRegionData(["Spirit Temple MQ Map Room South"]),
    # "Spirit Temple MQ Map Room South": SohRegionData(["Spirit Temple MQ Map Room North", "Spirit Temple MQ 1F West"]),
    # "Spirit Temple MQ West 1f Rusted Switch": SohRegionData(
    #     ["Spirit Temple MQ 1F West", "Spirit Temple MQ Under Like Like"]),
    # "Spirit Temple MQ Under Like Like": SohRegionData(
    #     ["Spirit Temple MQ West 1F Rusted Switch", "Spirit Temple MQ Broken Wall Room"]),
    # "Spirit Temple MQ Broken Wall Room": SohRegionData(
    #     ["Spirit Temple MQ Under Like Like", "Spirit Temple MQ Statue Room"]),
    # "Spirit Temple MQ Statue Room": SohRegionData(
    #     ["Spirit Temple MQ Broken Wall Room", "Spirit Temple MQ Big Block Room North",
    #      "Spirit Temple MQ Sun Block Room", "Spirit Temple MQ Statue Room East"]),
    # "Spirit Temple MQ Sun Block Room": SohRegionData(
    #     ["Spirit Temple MQ Statue Room", "Spirit Temple MQ West Iron Knuckle"]),
    # "Spirit Temple MQ West Iron Knuckle": SohRegionData(
    #     ["Spirit Temple MQ Sun Block Room", "Spirit Temple MQ Silver Gauntlets Hand"]),
    # "Spirit Temple MQ Silver Gauntlets Hand": SohRegionData(["Spirit Temple MQ West Iron Knuckle", "Desert Colossus"]),
    # "Spirit Temple MQ Big Block Room South": SohRegionData(
    #     ["Spirit Temple MQ Lobby", "Spirit Temple MQ Big Block Room North"]),
    # "Spirit Temple MQ Big Block Room North": SohRegionData(["Spirit Temple MQ Statue Room"]),
    # "Spirit Temple MQ Statue Room East": SohRegionData(
    #     ["Spirit Temple MQ Statue Room", "Spirit Temple MQ Silver Gauntlets Hand", "Spirit Temple MQ Four Beamos Room",
    #      "Spirit Temple MQ Three Suns Room 2F"]),
    # "Spirit Temple MQ Three Suns Room 2F": SohRegionData(
    #     ["Spirit Temple Statue Room East", "Spirit Temple MQ Three Suns Room 1F"]),
    # "Spirit Temple MQ Three Suns Room 1F": SohRegionData(
    #     ["Spirit Temple MQ Three Suns Room 2F", "Spirit Temple MQ 1F East"]),
    # "Spirit Temple MQ 1F East": SohRegionData(
    #     ["Spirit Temple MQ Lobby", "Spirit Temple MQ Three Suns Room 1F", "Spirit Temple MQ Leever Room",
    #      "Spirit Temple MQ Symphony Room"]),
    # "Spirit Temple MQ Leever Room": SohRegionData(["Spirit Temple MQ 1F East"]),
    # "Spirit Temple MQ Symphony Room": SohRegionData(
    #     ["Spirit Temple MQ 1F East", "Spirit Temple MQ After Symphony Room"]),
    # "Spirit Temple MQ After Symphony Room": SohRegionData(["Spirit Temple MQ Symphony Room"]),
    # "Spirit Temple MQ Four Beamos Room": SohRegionData(
    #     ["Spirit Temple MQ Statue Room East", "Spirit Temple MQ SoT Sun Room", "Spirit Temple MQ Big Wall"]),
    # "Spirit Temple MQ SoT Sun Room": SohRegionData(
    #     ["Spirit Temple MQ Four Beamos Room", "Spirit Temple MQ East Stairs to Hand",
    #      "Spirit Temple MQ 3F Gibdo Room"]),
    # "Spirit Temple MQ East Stairs to Hand": SohRegionData(
    #     ["Spirit Temple MQ SoT Sun Room", "Spirit Temple MQ East Iron Knuckle"]),
    # "Spirit Temple MQ East Iron Knuckle": SohRegionData(
    #     ["Spirit Temple MQ East Stairs to Hand", "Spirit Temple MQ Mirror Shield Hand"]),
    # "Spirit Temple MQ Mirror Shield Hand": SohRegionData(
    #     ["Spirit Temple MQ Silver Gauntlets Hand", "Spirit Temple MQ East Iron Knuckle", "Desert Colossus"]),
    # "Spirit Temple MQ 3F Gibdo Room": SohRegionData(["Spirit Temple MQ SoT Sun Room"]),
    # "Spirit Temple MQ Big Wall": SohRegionData(["Spirit Temple MQ Four Beamos Room", "Spirit Temple MQ 4F Central"]),
    # "Spirit Temple MQ 4F Central": SohRegionData(
    #     ["Spirit Temple MQ Big Wall", "Spirit Temple MQ Nine Chairs Room", "Spirit Temple MQ Big Mirror Room"]),
    # "Spirit Temple MQ Nine Chairs Room": SohRegionData(["Spirit Temple MQ 4F Central"]),
    # "Spirit Temple MQ Big Mirror Room": SohRegionData(["Spirit Temple MQ 4F Central", "Spirit Temple Big Mirror Cave"]),
    # "Spirit Temple MQ Big Mirror Cave": SohRegionData(
    #     ["Spirit Temple Inside Statue Head", "Spirit Temple MQ Statue Room"]),
    # "Spirit Temple MQ Inside Statue Head": SohRegionData(["Spirit Temple MQ Lobby", "Spirit Temple Boss Entryway"]),
    # Boss Room
    "Spirit Temple Boss Entryway": SohRegionData(
        ["Spirit Temple Inside Statue Head", "Spirit Temple Boss Room"]), # "Spirit Temple MQ Inside Statue Head"
    "Spirit  Temple Boss Room": SohRegionData(["Spirit Temple Boss Entryway", "Desert Colossus"]),

    # Shadow Temple
    "Shadow Temple Entryway": SohRegionData(
        ["Shadow Temple Beginning", "Graveyard Warp Pad Region"]), # "Shadow Temple MQ Beginning"
    # Vanilla
    "Shadow Temple Beginning": SohRegionData(["Shadow Temple Entryway", "Shadow First Beamos"]),
    "Shadow Temple First Beamos": SohRegionData(["Shadow Temple Huge Pit", "Shadow Temple Beyond Boat"]),
    "Shadow Temple Huge Pit": SohRegionData(["Shadow Temple Wind Tunnel"]),
    "Shadow Temple Wind Tunnel": SohRegionData(["Shadow Temple Beyond Boat"]),
    "Shadow Temple Beyond Boat": SohRegionData(["Shadow Temple Boss Entryway"]),
    # Master Quest
    # "Shadow Temple MQ Beginning": SohRegionData(["Shadow Temple Entryway", "Shadow Temple MQ Spinner Room"]),
    # "Shadow Temple MQ Spinner Room": SohRegionData(
    #     ["Shadow Temple Entryway", "Shadow Temple MQ First Beamos", "Shadow Temple Dead Hand Region"]),
    # "Shadow Temple MQ Dead Hand Region": SohRegionData(["Shadow Temple MQ Spinner Room"]),
    # "Shadow Temple MQ First Beamos": SohRegionData(
    #     ["Shadow Temple MQ Upper Huge Pit", "Shadow Temple B2 Spinning Blade Room"]),
    # "Shadow Temple MQ B2 Spinning Blade Room": SohRegionData(
    #     ["Shadow Temple MQ First Beamos", "Shadow Temple MQ Shortcut Path"]),
    # "Shadow Temple MQ Shortcut Path": SohRegionData(
    #     ["Shadow Temple MQ B2 Spinning Blade Room", "Shadow Temple MQ Dock"]),
    # "Shadow Temple MQ B2 to B3 Corridor": SohRegionData(
    #     ["Shadow Temple MQ First Beamos", "Shadow Temple MQ Upper Huge Pit"]),
    # "Shadow Temple MQ Upper Huge Pit": SohRegionData(
    #     ["Shadow Temple MQ Lower Huge Pit", "Shadow Temple MQ Invisible Blades Room"]),
    # "Shadow Temple MQ Invisible Blades Room": SohRegionData(["Shadow Temple MQ Upper Huge Pit"]),
    # "Shadow Temple MQ Lower Huge Pit": SohRegionData(
    #     ["Shadow Temple MQ Stone Umbrella Room", "Shadow Temple MQ Floor Spikes Room"]),
    # "Shadow Temple MQ Stone Umbrella Room": SohRegionData(
    #     ["Shadow Temple MQ Lower Huge Pit", "Shadow Temple MQ Upper Stone Umbrella"]),
    # "Shadow Temple MQ Upper Stone Umbrella": SohRegionData(["Shadow Temple MQ Stone Umbrella Room"]),
    # "Shadow Temple MQ Floor Spikes Room": SohRegionData(
    #     ["Shadow Temple MQ Stalfos Room", "Shadow Temple MQ Wind Tunnel"]),
    # "Shadow Temple MQ Stalfos Room": SohRegionData(["Shadow Temple MQ Floor Spikes Room"]),
    # "Shadow Temple MQ Wind Tunnel": SohRegionData(
    #     ["Shadow Temple MQ Floor Spikes Room", "Shadow Temple MQ Wind Hint Room", "Shadow Temple MQ B4 Gibdo Room"]),
    # "Shadow Temple MQ Wind Hint Room": SohRegionData(["Shadow Temple MQ Wind Tunnel"]),
    # "Shadow Temple MQ B4 Gibdo Room": SohRegionData(["Shadow Temple MQ Window Tunnel", "Shadow Temple MQ Dock"]),
    # "Shadow Temple MQ Dock": SohRegionData(
    #     ["Shadow Temple MQ Shortcut Path", "Shadow Temple MQ B4 Gibdo Room", "Shadow Temple MQ Beyond Boat"]),
    # "Shadow Temple MQ Beyond Boat": SohRegionData(["Shadow Temple MQ Across Chasm"]),
    # "Shadow Temple MQ Across Chasm": SohRegionData(
    #     ["Shadow Temple MQ Beyond Boat", "Shadow Temple MQ Invisible Maze", "Shadow Temple MQ Boss Door"]),
    # "Shadow Temple MQ Boss Door": SohRegionData(["Shadow Temple MQ Across Chasm", "Shadow Temple Boss Entryway"]),
    # "Shadow Temple MQ Invisible Maze": SohRegionData(
    #     ["Shadow Temple MQ Beyond Boat", "Shadow Temple MQ Spike Walls Room"]),
    # "Shadow Temple MQ Spike Walls Room": SohRegionData(["Shadow Temple MQ Invisible Maze"]),
    # Boss Room
    "Shadow Temple Boss Entryway": SohRegionData(
        ["Shadow Temple Beyond Boat", "Shadow Temple Boss Room"]), # "Shadow Temple MQ Boss Door"
    "Shadow Temple Boss Room": SohRegionData(["Shadow Temple Boss Entryway", "Graveyard Warp Pad Region"]),

    # Bottom of the Well
    "Bottom of the Well Entryway": SohRegionData(
        ["Kak Well", "Bottom of the Well Perimeter"]), # "Bottom of the Well MQ Perimeter"
    # Vanilla
    "Bottom of the Well Perimeter": SohRegionData(
        ["Bottom of the Well Entryway", "Bottom of the Well Behind Fake Walls", "Bottom of the Well Southwest Room",
         "Bottom of the Well Keese-Beamos Room", "Bottom of the Well Coffin", "Bottom of the Well Dead Hand Room",
         "Bottom of the Well Basement"]),
    "Bottom of the Well Behind Fake Walls": SohRegionData(
        ["Bottom of the Well Perimeter", "Bottom of the Well Inner Rooms", "Bottom of the Well Basement",
         "Bottom of the Well Basement Platform"]),
    "Bottom of the Well Southwest Room": SohRegionData(["Bottom of the Well Perimeter"]),
    "Bottom of the Well Keese-Beamos Room": SohRegionData(
        ["Bottom of the Well Perimeter", "Bottom of the Well Like-Like Cage",
         "Bottom of the Well Basement Useful Bomb Flowers"]),
    "Bottom of the Well Like-Like Cage": SohRegionData(["Bottom of the Well Keese-Beamos Room"]),
    "Bottom of the Well Inner Rooms": SohRegionData(["Bottom of the Well Behind Fake Walls"]),
    "Bottom of the Well Coffin Room": SohRegionData(["Bottom of the Well Perimeter"]),
    "Bottom of the Well Dead Hand Room": SohRegionData(["Bottom of the Well Perimeter"]),
    "Bottom of the Well Basement": SohRegionData(
        ["Bottom of the Well Southwest Room", "Bottom of the Well Basement Useful Bomb Flowers"]),
    "Bottom of the Well Basement Useful Bomb Flowers": SohRegionData(["Bottom of the Well Basement"]),
    "Bottom of the Well Basement Platform": SohRegionData(["Bottom of the Well Basement"]),
    # Master Quest
    # "Bottom of the Well MQ Perimeter": SohRegionData(
    #     ["Bottom of the Well Entryway", "Bottom of the Well MQ West Room Switch", "Bottom of the Well MQ Coffin Room",
    #      "Bottom of the Well MQ Locked Cage", "Bottom of the Well MQ Dead Hand Room", "Bottom of the Well MQ Middle",
    #      "Bottom of the Well MQ Basement"]),
    # "Bottom of the Well MQ West Room Switch": SohRegionData(
    #     ["Bottom of the Well MQ Perimeter", "Bottom of the Well MQ Middle", "Bottom of the Well MQ Basement"]),
    # "Bottom of the Well MQ Coffin Room": SohRegionData(["Bottom of the Well MQ Perimeter"]),
    # "Bottom of the Well MQ Locked Cage": SohRegionData(["Bottom of the Well MQ Perimeter"]),
    # "Bottom of the Well MQ Dead Hand Room": SohRegionData(["Bottom of the Well MQ Perimeter"]),
    # "Bottom of the Well MQ Middle": SohRegionData(
    #     ["Bottom of the Well Basement Switch Platform", "Bottom of the Well Basement"]),
    # "Bottom of the Well MQ Basement": SohRegionData(["Bottom of the Well MQ Perimeter"]),
    # "Bottom of the Well MQ Basement Switch Platform": SohRegionData(["Bottom of the Well Basement"]),

    # Ice Cavern
    "Ice Cavern Entryway": SohRegionData(["Ice Cavern Beginning", "ZF Ledge"]), # "Ice Cavern MQ Beginning"
    # Vanilla
    "Ice Cavern Beginning": SohRegionData(["Ice Cavern Entryway", "Ice Cavern Main"]),
    "Ice Cavern Main": SohRegionData([]),
    # Master Quest
    # "Ice Cavern MQ Beginning": SohRegionData(["Ice Cavern Entryway", "Ice Cavern MQ Hub"]),
    # "Ice Cavern MQ Hub": SohRegionData(
    #     ["Ice Cavern MQ Beginning", "Ice Cavern MQ Map Room", "Ice Cavern MQ Compass Room",
    #      "Ice Cavern MQ Scarecrow Room"]),
    # "Ice Cavern MQ Map Room": SohRegionData([]),
    # "Ice Cavern MQ Scarecrow Room": SohRegionData(["Ice Cavern MQ Hub", "Ice Cavern MQ West Corridor"]),
    # "Ice Cavern MQ West Corridor": SohRegionData(["Ice Cavern MQ Scarecrow Room", "Ice Cavern MQ Stalfos Room"]),
    # "Ice Cavern MQ Stalfos Room": SohRegionData(["Ice Cavern MQ West Corridor", "Ice Cavern MQ Beginning"]),
    # "Ice Cavern MQ Compass Room": SohRegionData([]),

    # Gerudo Training Ground
    "Gerudo Training Ground Entryway": SohRegionData(
        ["Gerudo Training Ground Lobby", "Gerudo Fortress"]), # "Gerudo Training Ground MQ Lobby"
    # Vanilla
    "Gerudo Training Ground Lobby": SohRegionData(
        ["Gerudo Training Ground Entryway", "Gerudo Training Ground Heavy Block Room",
         "Gerudo Training Ground Lava Room", "Gerudo Training Ground Central Maze"]),
    "Gerudo Training Ground Central Maze": SohRegionData(["Gerudo Training Ground Central Maze Right"]),
    "Gerudo Training Ground Central Maze Right": SohRegionData(
        ["Gerudo Training Ground Hammer Room", "Gerudo Training Ground Lava Room"]),
    "Gerudo Training Ground Lava Room": SohRegionData(
        ["Gerudo Training Ground Central Maze Right", "Gerudo Training Ground Hammer Room"]),
    "Gerudo Training Ground Hammer Room": SohRegionData(
        ["Gerudo Training Ground Eye Statue Lower", "Gerudo Training Ground Lava Room"]),
    "Gerudo Training Ground Eye Statue Lower": SohRegionData(
        ["Gerudo Training Ground Hammer Room", "Gerudo Training Ground Lava Room"]),
    "Gerudo Training Ground Eye Statue Upper": SohRegionData(["Gerudo Training Ground Eye Statue Lower"]),
    "Gerudo Training Ground Heavy Block Room": SohRegionData(
        ["Gerudo Training Ground Eye Statue Upper", "Gerudo Training Ground Like Like Room"]),
    "Gerudo Training Ground Like Like Room": SohRegionData([]),
    # Master Quest
    # "Gerudo Training Ground MQ Lobby": SohRegionData(
    #     ["Gerudo Training Ground Entryway", "Gerudo Training Ground MQ Maze Hidden Room",
    #      "Gerudo Training Ground MQ Maze First Lock", "Gerudo Training Ground MQ Sand Room",
    #      "Gerudo Training Ground MQ Dinolfos Room"]),
    # "Gerudo Training Ground MQ Maze Hidden Room": SohRegionData(["Gerudo Training Ground MQ Lobby"]),
    # "Gerudo Training Ground MQ Maze First Lock": SohRegionData(
    #     ["Gerudo Training Ground MQ Lobby", "Gerudo Training Ground MQ Maze Center"]),
    # "Gerudo Training Ground MQ Maze Center": SohRegionData(["Gerudo Training Ground MQ First Lock"]),
    # "Gerudo Training Ground MQ Sand Room": SohRegionData(
    #     ["Gerudo Training Ground MQ Lobby", "Gerudo Training Ground MQ Left Side"]),
    # "Gerudo Training Ground MQ Left Side": SohRegionData(
    #     ["Gerudo Training Ground MQ Sand Room", "Gerudo Training Ground MQ Stalfos Room"]),
    # "Gerudo Training Ground MQ Stalfos Room": SohRegionData(
    #     ["Gerudo Training Ground MQ Behind Block", "Gerudo Training Ground MQ Statue Room Ledge"]),
    # "Gerudo Training Ground MQ Behind Block": SohRegionData([]),
    # "Gerudo Training Ground MQ Statue Room Ledge": SohRegionData(
    #     ["Gerudo Training Ground MQ Stalfos Room", "Gerudo Training Ground MQ Magenta Fire Room",
    #      "Gerudo Training Ground MQ Statue Room"]),
    # "Gerudo Training Ground MQ Magenta Fire Room": SohRegionData(["Gerudo Training Ground MQ Statue Room Ledge"]),
    # "Gerudo Training Ground MQ Statue Room": SohRegionData(
    #     ["Gerudo Training Ground MQ Statue Room Ledge", "Gerudo Training Ground MQ Torch Slug Room"]),
    # "Gerudo Training Ground MQ Torch Slug Room": SohRegionData(
    #     ["Gerudo Training Ground MQ Statue Room", "Gerudo Training Ground MQ Switch Ledge"]),
    # "Gerudo Training Ground MQ Switch Ledge": SohRegionData(
    #     ["Gerudo Training Ground MQ Platforms Unlit Torch", "Gerudo Training Ground MQ Maze Right"]),
    # "Gerudo Training Ground MQ Ledge Side Platforms": SohRegionData(["Gerudo Training Ground MQ Furthest Platform"]),
    # "Gerudo Training Ground MQ Furthest Platform": SohRegionData(["Gerudo Training Ground MQ Ledge Side Platform"]),
    # "Gerudo Training Ground MQ Platforms Unlit Torch": SohRegionData(
    #     ["Gerudo Training Ground MQ  Underwater", "Gerudo Training Ground MQ Ledge Side Platforms",
    #      "Gerudo Training Ground MQ Torch Side Platforms", "Gerudo Training Ground MQ Maze Right"]),
    # "Gerudo Training Ground MQ Torch Side Platforms": SohRegionData(
    #     ["Gerudo Training Ground MQ Ledge Side Platforms", "Gerudo Training Ground MQ Platforms Unlit Torch",
    #      "Gerudo Training Ground MQ Maze Right", "Gerudo Training Ground MQ Dinolfos Room"]),
    # "Gerudo Training Ground MQ Underwater": SohRegionData(["Gerudo Training Ground MQ Platforms Unlit Torch"]),
    # "Gerudo Training Ground MQ Maze Right": SohRegionData(
    #     ["Gerudo Training Ground MQ Lobby", "Gerudo Training Ground MQ Ledge Side Platforms",
    #      "Gerudo Training Ground MQ Platforms Unlit Torch", "Gerudo Training Ground MQ Ledge Side Platforms",
    #      "Gerudo Training Ground MQ Furthest Platform"]),
    # "Gerudo Training Ground MQ Dinolfos Room": SohRegionData(["Gerudo Training Ground MQ Torch Side Platforms"]),

    # Ganon's Castle
    "Ganon's Castle Entryway": SohRegionData(
        ["Ganon's Castle Lobby", "Castle Ground From Ganon's Castle"]), # "Ganon's Castle MQ Lobby"
    # Vanilla
    "Ganon's Castle Lobby": SohRegionData(
        ["Ganon's Castle Entryway", "Ganon's Castle Forest Trial", "Ganon's Castle Fire Trial",
         "Ganon's Castle Water Trial", "Ganon's Castle Shadow Trial", "Ganon's Castle Spirit Trial",
         "Ganon's Castle Light Trial", "Ganon's Tower Entryway", "Ganon's Castle Deku Scrubs"]),
    "Ganon's Castle Deku Scrubs": SohRegionData([]),
    "Ganon's Castle Forest Trial": SohRegionData([]),
    "Ganon's Castle Fire Trial": SohRegionData([]),
    "Ganon's Castle Water Trial": SohRegionData([]),
    "Ganon's Castle Shadow Trial": SohRegionData([]),
    "Ganon's Castle Spirit Trial": SohRegionData([]),
    "Ganon's Castle Light Trial": SohRegionData([]),
    # Master Quest
    # "Ganon's Castle MQ Lobby": SohRegionData(["Ganon's Castle Entryway", "Ganon's Castle MQ Main"]),
    # "Ganon's Castle MQ Main": SohRegionData(["Ganon's Castle MQ Lobby", "Ganon's Castle MQ Forest Trial Stalfos Room",
    #                                          "Ganon's Castle MQ Fire Trial Main Room",
    #                                          "Ganon's Castle MQ Water Trial Geyser Room",
    #                                          "Ganon's Castle MQ Shadow Trial Starting Ledge",
    #                                          "Ganon's Castle MQ Spirit Trial Chairs Room",
    #                                          "Ganon's Castle MQ Light Trial Dinolfos Room",
    #                                          "Ganon's Castle MQ Deku Scrubs", "Ganon's Tower Entryway"]),
    # "Ganon's Castle MQ Deku Scrubs": SohRegionData(["Ganon's Castle MQ Main"]),
    # "Ganon's Castle MQ Forest Trial Stalfos Room": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Forest Trial Beamos Room"]),
    # "Ganon's Castle MQ Forest Trial Beamos Room": SohRegionData(
    #     ["Ganon's Castle MQ Forest Trial Stalfos Room", "Ganon's Castle MQ Forest Trial Final Room"]),
    # "Ganon's Castle MQ Forest Trial Final Room": SohRegionData(["Ganon's Castle MQ Forest Trial Beamos Room"]),
    # "Ganon's Castle MQ Fire Trial Main Room": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Fire Trial Final Room"]),
    # "Ganon's Castle MQ Fire Trial Final Room": SohRegionData([]),
    # "Ganon's Castle MQ Water Trial Geyser Room": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Water Trial Block Room"]),
    # "Ganon's Castle MQ Water Trial Block Room": SohRegionData(
    #     ["Ganon's Castle MQ Water Trial Geyser Room", "Ganon's Castle MQ Water Trial Final Room"]),
    # "Ganon's Castle MQ Water Trial Final Room": SohRegionData(["Ganon's Castle MQ Water Trial Block Room"]),
    # "Ganon's Castle MQ Shadow Trial Starting Ledge": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Shadow Trial Chest Platform"]),
    # "Ganon's Castle MQ Shadow Trial Chest Platform": SohRegionData(
    #     ["Ganon's Castle MQ Shadow Trial Chest Platform", "Ganon's Castle MQ Shadow Trial Moving Platform"]),
    # "Ganon's Castle MQ Shadow Trial Moving Platform": SohRegionData(
    #     ["Ganon's Castle MQ Chest Platform", "Ganon's Castle MQ Shadow Trial Beamos Torch"]),
    # "Ganon's Castle MQ Shadow Trial Beamos Torch": SohRegionData(
    #     ["Ganon's Castle MQ Shadow Trial Moving Platform", "Ganon's Castle MQ Shadow Trial Far Side"]),
    # "Ganon's Castle MQ Shadow Trial Far Side": SohRegionData(
    #     ["Ganon's Castle MQ Shadow Trial Beamos Torch", "Ganon's Castle MQ Shadow Trial Final Room"]),
    # "Ganon's Castle MQ Shadow Trial Final Room": SohRegionData(["Ganon's Castle MQ Shadow Trial Far Side"]),
    # "Ganon's Castle MQ Spirit Trial Chairs Room": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Spirit Trial Before Switch"]),
    # "Ganon's Castle MQ Spirit Trial Before Switch": SohRegionData(
    #     ["Ganon's Castle MQ Spirit Trial Chairs Room", "Ganon's Castle MQ Spirit Trial After Switch"]),
    # "Ganon's Castle MQ Spirit Trial After Switch": SohRegionData(
    #     ["Ganon's Castle MQ Spirit Trial Before Switch", "Ganon's Castle MQ Spirit Trial Final Room"]),
    # "Ganon's Castle MQ Spirit Trial Final Room": SohRegionData(["Ganon's Castle MQ Spirit Trial Final Room"]),
    # "Ganon's Castle MQ Light Trial Dinolfos Room": SohRegionData(
    #     ["Ganon's Castle MQ Main", "Ganon's Castle MQ Light Trial Triforce Room"]),
    # "Ganon's Castle MQ Light Trial Triforce Room": SohRegionData(
    #     ["Ganon's Castle MQ Dinolfos Room", "Ganon's Castle MQ Light Trial Boulder Room Front"]),
    # "Ganon's Castle MQ Light Trial Boulder Room Front": SohRegionData(
    #     ["Ganon's Castle MQ Light Trial Triforce Room", "Ganon's Castle MQ Boulder Room Back"]),
    # "Ganon's Castle MQ Light Trial Boulder Room Back": SohRegionData(
    #     ["Ganon's Castle MQ Light Trial Boulder Room Front", "Ganon's Castle MQ Light Trial Final Room"]),
    # "Ganon's Castle MQ Light Trial Final Room": SohRegionData([]),
    # Tower and Escape
    "Ganon's Tower Entryway": SohRegionData(
        ["Ganon's Castle Lobby", "Ganon's Tower Floor 1"]), # "Ganon's Castle MQ Main"
    "Ganon's Tower Floor 1": SohRegionData(["Ganon's Tower Entryway", "Ganon's Tower Floor 2"]),
    "Ganon's Tower Floor 2": SohRegionData(["Ganon's Tower Floor 1", "Ganon's Tower Floor 3"]),
    "Ganon's Tower Floor 3": SohRegionData(["Ganon's Tower Floor 2", "Ganon's Tower Before Ganondorf's Lair"]),
    "Ganon's Tower Before Ganondorf's Lair": SohRegionData(["Ganon's Tower Floor 3", "Ganondorf's Lair"]),
    "Ganondorf's Lair": SohRegionData(["Ganon's Castle Escape"]),
    "Ganon's Castle Escape": SohRegionData(["Ganon's Arena"]),
    "Ganon's Arena": SohRegionData([])
}
