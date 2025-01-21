from BaseClasses import Location, LocationProgressType, Region
from worlds.ty_the_tasmanian_tiger import ty1_levels, Ty1LevelCode, Ty1Options
from collections import namedtuple


class Ty1Location:
    game: str = "Ty the Tasmanian Tiger"

    def __init__(self, name, progress_type: LocationProgressType, code: int = None, player: int = None):
        super(Ty1Location, self).__init__(name, progress_type, code, player)

A1_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Time Attack", "Glide The Gap", "Rang The Frills", "Rock Jump", "Super Chomp", "Lower The Platforms"]
A2_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Wombat Race", "Truck Trouble", "Bounce Tree", "Drive Me Batty", "Turkey Chase", "Log Climb"]
A3_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Race Rex", "Where's Elle?", "Aurora's Kids", "Quicksand Coconuts", "Ship Wreck", "Nest Egg"]
B1_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Time Attack", "Home, Sweet, Home", "Heat Dennis' House", "Tag Team Turkeys", "Ty Diving", "Neddy The Bully"]
B2_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Time Attack", "Koala Chaos", "The Old Mill", "Trap The Yabby", "Musical Icicle", "Snowy Peak"]
B3_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Time Attack", "Emu Roundup", "Frill Frenzy", "Fire Fight", "Toxic Trouble", "Secret Thunder Egg"]
C1_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Time Attack", "Lenny The Lyrebird", "Fiery Furnace", "Water Worries", "Muddy Towers", "Gantry Glide"]
C2_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Wombat Rematch", "Koala Crisis", "Cable Car Capers", "Flame Frills", "Catch Boonie", "Pillar Ponder"]
C3_THEGGS = ["Collect 300 Opals", "Find 5 Bilbies", "Race Rex", "Treasure Hunt", "Parrot Beard's Booty", "Frill Boat Battle", "Geyser Hop", "Volcanic Panic"]

LocationTuple = namedtuple('Location', ['name', 'id'])

def create_locations(level_region: Region, level_code: Ty1LevelCode, options: Ty1Options):
    level_locs = ty1_location_table[ty1_levels[level_code]]
    if "thunder_eggs" in level_locs:
        for i in range(len(level_locs["thunder_eggs"])):
            if i is 1 and options.bilbysanity == 0:
                continue
            create_loc(level_region, level_locs["thunder_eggs"][i].name, level_locs["thunder_eggs"][i].id, LocationProgressType.DEFAULT)
    if "bilbies" in level_locs and options.bilbysanity is not 2:
        for bilby_loc in level_locs["bilbies"]:
            create_loc(level_region, bilby_loc.name, bilby_loc.id, LocationProgressType.DEFAULT)
    if "golden_cogs" in level_locs:
        if options.cogsanity is 0:
            for cog_loc in level_locs["golden_cogs"]:
                create_loc(level_region, cog_loc.name, cog_loc.id, LocationProgressType.DEFAULT)
        if options.cogsanity is 1 and "cog_completion" in level_locs:
            create_loc(level_region, level_locs["cog_completion"][0].name, level_locs["cog_completion"][0].id, LocationProgressType.DEFAULT)
    if "picture_frames" in level_locs:
        if options.framesanity is 0:
            for frame_loc in level_locs["picture_frames"]:
                create_loc(level_region, frame_loc.name, frame_loc.id, LocationProgressType.DEFAULT)
        if options.framesanity is 1 and "frame_completion" in level_locs:
            create_loc(level_region, level_locs["frame_completion"][0].name, level_locs["frame_completion"][0].id, LocationProgressType.DEFAULT)
    if "attributes" in level_locs:
        if options.attributesanity is not 2:
            for attr_loc in level_locs["attributes"]:
                create_loc(level_region, attr_loc.name, attr_loc.id, LocationProgressType.DEFAULT)
    if "elemental_rangs" in level_locs:
        if options.attributesanity is 1:
            for elem_loc in level_locs["elemental_rangs"]:
                create_loc(level_region, elem_loc.name, elem_loc.id, LocationProgressType.DEFAULT)
    if "talismans" in level_locs:
        for tali_loc in level_locs["talismans"]:
            create_loc(level_region, tali_loc.name, tali_loc.id, LocationProgressType.DEFAULT)

def create_loc(reg: Region, loc_name: str, loc_code: int, progress_type: LocationProgressType):
    reg.locations += [Ty1Location(loc_name, progress_type, loc_code, reg.player)]

ty1_location_table = {
    "Two Up": {
        "thunder_eggs": [LocationTuple(f"Two Up - {egg}", 0x8750100 + i) for i, egg in enumerate(A1_THEGGS)],
        "golden_cogs": [LocationTuple(f"Two Up - Golden Cog {i + 1}", 0x8750148 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"Two Up - Bilby {name}", 0x87501AC + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"Two Up - PF {i + 1}", 0x87501E2 + i) for i in range(7)],
        "attributes": [LocationTuple("Attribute - Second Rang", 0x8750012)],
        "cog_completion": [LocationTuple("Two Up - All Golden Cogs", 0x87501A3)],
        "frame_completion": [LocationTuple("Two Up - All Picture Frames", 0x8750258)]
    },
    "Walk in the Park": {
        "thunder_eggs": [LocationTuple(f"WitP - {egg}", 0x8750108 + i) for i, egg in enumerate(A2_THEGGS)],
        "golden_cogs": [LocationTuple(f"WitP - Golden Cog {i + 1}", 0x8750153 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"WitP - Bilby {name}", 0x87501B1 + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"WitP - PF {i + 1}", 0x87501E9 + i) for i in range(6)],
        "cog_completion": [LocationTuple("WitP - All Golden Cogs", 0x87501A4)],
        "frame_completion": [LocationTuple("WitP - All Picture Frames", 0x8750259)]
    },
    "Ship Rex": {
        "thunder_eggs": [LocationTuple(f"Ship Rex - {egg}", 0x8750110 + i) for i, egg in enumerate(A3_THEGGS)],
        "golden_cogs": [LocationTuple(f"Ship Rex - Golden Cog {i + 1}", 0x875015D + i) for i in range(10)],
        "bilbies": [LocationTuple(f"Ship Rex - Bilby {name}", 0x87501B6 + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"Ship Rex - PF {i + 1}", 0x87501EF + i) for i in range(9)],
        "attributes": [LocationTuple("Attribute - Swim", 0x8750010)],
        "cog_completion": [LocationTuple("Ship Rex - All Golden Cogs", 0x87501A5)],
        "frame_completion": [LocationTuple("Ship Rex - All Picture Frames", 0x875025A)]
    },
    "Bull's Pen": {
        "talismans": [LocationTuple("Frog Talisman", 0x8750261)]
    },
    "Bridge on the River Ty": {
        "thunder_eggs": [LocationTuple(f"BotRT - {egg}", 0x8750118 + i) for i, egg in enumerate(B1_THEGGS)],
        "golden_cogs": [LocationTuple(f"BotRT - Golden Cog {i + 1}", 0x8750167 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"BotRT - Bilby {name}", 0x87501BB + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"BotRT - PF {i + 1}", 0x87501F8 + i) for i in range(20)],
        "attributes": [LocationTuple("Attribute - Dive", 0x8750011)],
        "cog_completion": [LocationTuple("BotRT - All Golden Cogs", 0x87501A6)],
        "frame_completion": [LocationTuple("BotRT - All Picture Frames", 0x875025B)]
    },
    "Snow Worries": {
        "thunder_eggs": [LocationTuple(f"Snow Worries - {egg}", 0x8750120 + i) for i, egg in enumerate(B2_THEGGS)],
        "golden_cogs": [LocationTuple(f"Snow Worries - Golden Cog {i + 1}", 0x8750171 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"Snow Worries - Bilby {name}", 0x87501C0 + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"Snow Worries - PF {i + 1}", 0x875020C + i) for i in range(24)],
        "cog_completion": [LocationTuple("Snow Worries - All Golden Cogs", 0x87501A7)],
        "frame_completion": [LocationTuple("Snow Worries - All Picture Frames", 0x875025C)]
    },
    "Outback Safari": {
        "thunder_eggs": [LocationTuple(f"Outback Safari - {egg}", 0x8750128 + i) for i, egg in enumerate(B3_THEGGS)],
        "golden_cogs": [LocationTuple(f"Outback Safari - Golden Cog {i + 1}", 0x875017B + i) for i in range(10)],
        "bilbies": [LocationTuple(f"Outback Safari - Bilby {name}", 0x87501C5 + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "cog_completion": [LocationTuple("Outback Safari - All Golden Cogs", 0x87501A8)]
    },
    "Crikey's Cove": {
        "talismans": [LocationTuple("Platypus Talisman", 0x8750262)]
    },
    "Lyre, Lyre Pants on Fire": {
        "thunder_eggs": [LocationTuple(f"LLPoF - {egg}", 0x8750130 + i) for i, egg in enumerate(C1_THEGGS)],
        "golden_cogs": [LocationTuple(f"LLPoF - Golden Cog {i + 1}", 0x8750185 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"LLPoF - Bilby {name}", 0x87501CA + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"LLPoF - PF {i + 1}", 0x8750224 + i) for i in range(5)],
        "cog_completion": [LocationTuple("LLPoF - All Golden Cogs", 0x87501A9)],
        "frame_completion": [LocationTuple("LLPoF - All Picture Frames", 0x875025D)]
    },
    "Beyond the Black Stump": {
        "thunder_eggs": [LocationTuple(f"BtBS - {egg}", 0x8750138 + i) for i, egg in enumerate(C2_THEGGS)],
        "golden_cogs": [LocationTuple(f"BtBS - Golden Cog {i + 1}", 0x875018F + i) for i in range(10)],
        "bilbies": [LocationTuple(f"BtBS - Bilby {name}", 0x87501CF + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"BtBS - PF {i + 1}", 0x8750229 + i) for i in range(29)],
        "cog_completion": [LocationTuple("BtBS - All Golden Cogs", 0x87501AA)],
        "frame_completion": [LocationTuple("BtBS - All Picture Frames", 0x875025E)]
    },
    "Rex Marks the Spot": {
        "thunder_eggs": [LocationTuple(f"RMtS - {egg}", 0x8750140 + i) for i, egg in enumerate(C3_THEGGS)],
        "golden_cogs": [LocationTuple(f"RMtS - Golden Cog {i + 1}", 0x8750199 + i) for i in range(10)],
        "bilbies": [LocationTuple(f"RMtS - Bilby {name}", 0x87501D4 + i) for i, name in enumerate(["Dad", "Mum", "Boy", "Girl", "Grandma"])],
        "picture_frames": [LocationTuple(f"RMtS - PF {i + 1}", 0x8750246 + i) for i in range(18)],
        "cog_completion": [LocationTuple("RMtS - All Golden Cogs", 0x87501AB)],
        "frame_completion": [LocationTuple("RMtS - All Picture Frames", 0x875025F)]
    },
    "Fluffy's Fjord": {
        "talismans": [LocationTuple("Cockatoo Talisman", 0x8750263)]
    },
    "Cass' Crest": {
        "talismans": [LocationTuple("Dingo Talisman", 0x8750264)]
    },
    "Final Battle": {
        "talismans": [LocationTuple("Tiger Talisman", 0x8750265)],
        "attributes": [LocationTuple("Attribute - Doomerang", 0x875001F)]
    },
    "Rainbow Cliffs": {
        "picture_frames": [LocationTuple(f"Rainbow Cliffs - PF {i + 1}", 0x87501D9 + i) for i in range(9)],
        "set_completion": [LocationTuple("Rainbow Cliffs - All Picture Frames", 0x8750260)],
        "elemental_rangs": [LocationTuple("Attribute - Flamerang", 0x8750015),
                            LocationTuple("Attribute - Frostyrang", 0x8750016),
                            LocationTuple("Attribute - Zappyrang", 0x8750017)],
        "attributes": [LocationTuple("Attribute - Extra Health", 0x8750013),
                       LocationTuple("Attribute - Zoomerang", 0x8750019),
                       LocationTuple("Attribute - Multirang", 0x875001A),
                       LocationTuple("Attribute - Infrarang", 0x875001B),
                       LocationTuple("Attribute - Megarang", 0x875001C),
                       LocationTuple("Attribute - Kaboomarang", 0x875001D),
                       LocationTuple("Attribute - Chronorang", 0x875001E)]
    },
}