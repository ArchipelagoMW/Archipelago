from collections import Counter

from BaseClasses import Location, Region
from worlds.ty_the_tasmanian_tiger.options import Ty1Options


class Ty1Location(Location):
    game: str = "Ty the Tasmanian Tiger"

class ReqData:
    name: str
    count: int = 1

class LocData:
    def __init__(self, code: int, region: str,):
        """
        Represents a location with associated conditions.

        :param code: A unique identifier for the location.
        :param region: Name of the containing region.
        """
        self.code = code
        self.region = region

def create_location(player: int, options: Ty1Options, reg: Region, name: str, data: LocData):
    location = Ty1Location(player, name, data.code, reg)
    #print("Creating location: " + name + " in " + reg.name)
    reg.locations.append(location)

def create_locations(player: int, options: Ty1Options, reg: Region):
    # THUNDER EGGS
    for (key, data) in thunder_eggs_dict.items():
        if data.region != reg.name:
            continue
        if options.bilbysanity == 0 and "Find 5 Bilbies" in key:
            continue
        create_location(player, options, reg, key, data)
    # BILBY COMPLETION
    for (key, data) in bilby_completion_dict.items():
        if data.region != reg.name:
            continue
        create_location(player, options, reg, key, data)
    # TALISMANS
    for (key, data) in talismans_dict.items():
        if data.region != reg.name:
            continue
        create_location(player, options, reg, key, data)
    # GOLDEN COGS
    if options.cogsanity == 0:
        for (key, data) in golden_cogs_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # BILBIES
    if options.bilbysanity != 2:
        for (key, data) in bilbies_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # PICTURE FRAMES
    if options.framesanity == 0:
        for (key, data) in picture_frames_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # FRAME COMPLETION
    if options.framesanity == 1:
        for (key, data) in frame_completion_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # COG COMPLETION#
    if options.cogsanity == 1:
        for (key, data) in cog_completion_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # ATTRIBUTES
    if options.attributesanity != 2:
        for (key, data) in attributes_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)
    # ELEMENTAL RANGS
    if options.attributesanity == 1:
        for (key, data) in elemental_rangs_dict.items():
            if data.region != reg.name:
                continue
            create_location(player, options, reg, key, data)

# Thunder_eggs Dictionary
thunder_eggs_dict = {
    # Two Up ---------------------------------------------------------------------------------------------------------
    "Two Up - Collect 300 Opals":
        LocData(0x08750100, "Two Up"),
    "Two Up - Find 5 Bilbies":
        LocData(0x08750101, "Two Up - Upper Area"),
    "Two Up - Time Attack":
        LocData(0x08750102, "Two Up"),
    "Two Up - Glide The Gap":
        LocData(0x08750103, "Two Up - End Area"),
    "Two Up - Rang The Frills":
        LocData(0x08750104, "Two Up"),
    "Two Up - Rock Jump":
        LocData(0x08750105, "Two Up"),
    "Two Up - Super Chomp":
        LocData(0x08750106, "Two Up"),
    "Two Up - Lower The Platforms":
        LocData(0x08750107, "Two Up - Upper Area"),
    # Walk -----------------------------------------------------------------------------------------------------------
    "WitP - Collect 300 Opals":
        LocData(0x08750108, "Walk in the Park"),
    "WitP - Find 5 Bilbies":
        LocData(0x08750109, "Walk in the Park"),
    "WitP - Wombat Race":
        LocData(0x0875010A, "Walk in the Park"),
    "WitP - Truck Trouble":
        LocData(0x0875010B, "Walk in the Park"),
    "WitP - Bounce Tree":
        LocData(0x0875010C, "Walk in the Park"),
    "WitP - Drive Me Batty":
        LocData(0x0875010D, "Walk in the Park"),
    "WitP - Turkey Chase":
        LocData(0x0875010E, "Walk in the Park"),
    "WitP - Log Climb":
        LocData(0x0875010F, "Walk in the Park"),
    # Ship -----------------------------------------------------------------------------------------------------------
    "Ship Rex - Collect 300 Opals":
        LocData(0x08750110, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Find 5 Bilbies":
        LocData(0x08750111, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Race Rex":
        LocData(0x08750112, "Ship Rex"),
    "Ship Rex - Where's Elle?":
        LocData(0x08750113, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Aurora's Kids":
        LocData(0x08750114, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Quicksand Coconuts":
        LocData(0x08750115, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Ship Wreck":
        LocData(0x08750116, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Nest Egg":
        LocData(0x08750117, "Ship Rex - Beyond Gate 1"),
    # Bridge ---------------------------------------------------------------------------------------------------------
    "BotRT - Collect 300 Opals":
        LocData(0x08750118, "Bridge on the River Ty"),
    "BotRT - Find 5 Bilbies":
        LocData(0x08750119, "Bridge on the River Ty"),
    "BotRT - Time Attack":
        LocData(0x0875011A, "Bridge on the River Ty"),
    "BotRT - Home, Sweet, Home":
        LocData(0x0875011B, "Bridge on the River Ty"),
    "BotRT - Heat Dennis' House":
        LocData(0x0875011C, "Bridge on the River Ty"),
    "BotRT - Tag Team Turkeys":
        LocData(0x0875011D, "Bridge on the River Ty"),
    "BotRT - Ty Diving":
        LocData(0x0875011E, "Bridge on the River Ty"),
    "BotRT - Neddy The Bully":
        LocData(0x0875011F, "Bridge on the River Ty"),
    # Snow -----------------------------------------------------------------------------------------------------------
    "Snow Worries - Collect 300 Opals":
        LocData(0x08750120, "Snow Worries - Underwater"),
    "Snow Worries - Find 5 Bilbies":
        LocData(0x08750121, "Snow Worries"),
    "Snow Worries - Time Attack":
        LocData(0x08750122, "Snow Worries"),
    "Snow Worries - Koala Chaos":
        LocData(0x08750123, "Snow Worries"),
    "Snow Worries - The Old Mill":
        LocData(0x08750124, "Snow Worries"),
    "Snow Worries - Trap The Yabby":
        LocData(0x08750125, "Snow Worries - Underwater"),
    "Snow Worries - Musical Icicle":
        LocData(0x08750126, "Snow Worries"),
    "Snow Worries - Snowy Peak":
        LocData(0x08750127, "Snow Worries"),
    # Outback --------------------------------------------------------------------------------------------------------
    "Outback Safari - Collect 300 Opals":
        LocData(0x08750128, "Outback Safari"),
    "Outback Safari - Find 5 Bilbies":
        LocData(0x08750129, "Outback Safari"),
    "Outback Safari - Time Attack":
        LocData(0x0875012A, "Outback Safari"),
    "Outback Safari - Emu Roundup":
        LocData(0x0875012B, "Outback Safari"),
    "Outback Safari - Frill Frenzy":
        LocData(0x0875012C, "Outback Safari"),
    "Outback Safari - Fire Fight":
        LocData(0x0875012D, "Outback Safari"),
    "Outback Safari - Toxic Trouble":
        LocData(0x0875012E, "Outback Safari"),
    "Outback Safari - Secret Thunder Egg":
        LocData(0x0875012F, "Outback Safari"),
    # Lyre -----------------------------------------------------------------------------------------------------------
    "LLPoF - Collect 300 Opals":
        LocData(0x08750130, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Find 5 Bilbies":
        LocData(0x08750131, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Time Attack":
        LocData(0x08750132, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Lenny The Lyrebird":
        LocData(0x08750133, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Fiery Furnace":
        LocData(0x08750134, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Water Worries":
        LocData(0x08750135, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Muddy Towers":
        LocData(0x08750136, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Gantry Glide":
        LocData(0x08750137, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Stump ----------------------------------------------------------------------------------------------------------
    "BtBS - Collect 300 Opals":
        LocData(0x08750138, "Beyond the Black Stump - Upper Area"),
    "BtBS - Find 5 Bilbies":
        LocData(0x08750139, "Beyond the Black Stump - Upper Area"),
    "BtBS - Wombat Rematch":
        LocData(0x0875013A, "Beyond the Black Stump"),
    "BtBS - Koala Crisis":
        LocData(0x0875013B, "Beyond the Black Stump"),
    "BtBS - Cable Car Capers":
        LocData(0x0875013C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Flame Frills":
        LocData(0x0875013D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Catch Boonie":
        LocData(0x0875013E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Pillar Ponder":
        LocData(0x0875013F, "Beyond the Black Stump - Upper Area"),
    # Rex Marks ------------------------------------------------------------------------------------------------------
    "RMtS - Collect 300 Opals":
        LocData(0x08750140, "Rex Marks the Spot - Underwater"),
    "RMtS - Find 5 Bilbies":
        LocData(0x08750141, "Rex Marks the Spot"),
    "RMtS - Race Rex":
        LocData(0x08750142, "Rex Marks the Spot - Underwater"),
    "RMtS - Treasure Hunt":
        LocData(0x08750143, "Rex Marks the Spot - Underwater"),
    "RMtS - Parrot Beard's Booty":
        LocData(0x08750144, "Rex Marks the Spot"),
    "RMtS - Frill Boat Battle":
        LocData(0x08750145, "Rex Marks the Spot - Underwater"),
    "RMtS - Geyser Hop":
        LocData(0x08750146, "Rex Marks the Spot"),
    "RMtS - Volcanic Panic":
        LocData(0x08750147, "Rex Marks the Spot"),
}

# Golden_cogs Dictionary
golden_cogs_dict = {
    # Next to Julius
    "Two Up - Golden Cog 1":
        LocData(0x08750148, "Two Up"),
    # On small platform in the water near purple crab
    "Two Up - Golden Cog 2":
        LocData(0x08750149, "Two Up"),
    # On wood platform near 20 opal ledge in upper area
    "Two Up - Golden Cog 3":
        LocData(0x0875014A, "Two Up - Upper Area"),
    # On platform next to second rang
    "Two Up - Golden Cog 4":
        LocData(0x0875014B, "Two Up"),
    # On platform next to bilby at bridge near purple crab
    "Two Up - Golden Cog 5":
        LocData(0x0875014C, "Two Up"),
    # On pontoon in deep water in upper area
    "Two Up - Golden Cog 6":
        LocData(0x0875014D, "Two Up - Upper Area"),
    # In cave near start
    "Two Up - Golden Cog 7":
        LocData(0x0875014E, "Two Up"),
    # On raised area before Julius
    "Two Up - Golden Cog 8":
        LocData(0x0875014F, "Two Up"),
    # On platform near start next to cog 7
    "Two Up - Golden Cog 9":
        LocData(0x08750150, "Two Up"),
    # On tall platform next to 20 opal ledge before cave leading to bridge
    "Two Up - Golden Cog 10":
        LocData(0x08750151, "Two Up"),
    # On platform near frills near start before logs
    "WitP - Golden Cog 1":
        LocData(0x08750152, "Walk in the Park"),
    # Logs area near two crates towards top of slide 1
    "WitP - Golden Cog 2":
        LocData(0x08750153, "Walk in the Park"),
    # Behind waterfall at top of slide 1
    "WitP - Golden Cog 3":
        LocData(0x08750154, "Walk in the Park"),
    # In slide 1 cave
    "WitP - Golden Cog 4":
        LocData(0x08750155, "Walk in the Park"),
    # Wood platform in valley
    "WitP - Golden Cog 5":
        LocData(0x08750156, "Walk in the Park"),
    # Platform at bottom of slide 2
    "WitP - Golden Cog 6":
        LocData(0x08750157, "Walk in the Park"),
    # Logs area, first cog seen to the right after first two logs
    "WitP - Golden Cog 7":
        LocData(0x08750158, "Walk in the Park"),
    # Platform halfway up boulder slopes
    "WitP - Golden Cog 8":
        LocData(0x08750159, "Walk in the Park"),
    # Under bridge at end
    "WitP - Golden Cog 9":
        LocData(0x0875015A, "Walk in the Park"),
    # Behind at the very start
    "WitP - Golden Cog 10":
        LocData(0x0875015B, "Walk in the Park"),
    # On floating platform to the right after entering spire area beyond gate 2
    "Ship Rex - Golden Cog 1":
        LocData(0x0875015C, "Ship Rex - Beyond Gate 1"),
    # On pillar to the right after entering main area beyond gate 1
    "Ship Rex - Golden Cog 2":
        LocData(0x0875015D, "Ship Rex - Beyond Gate 1"),
    # Wood platform at start
    "Ship Rex - Golden Cog 3":
        LocData(0x0875015E, "Ship Rex"),
    # Large rockpool
    "Ship Rex - Golden Cog 4":
        LocData(0x0875015F, "Ship Rex - Beyond Gate 1"),
    # Floating platform reached from geyser
    "Ship Rex - Golden Cog 5":
        LocData(0x08750160, "Ship Rex - Beyond Gate 1"),
    # Island in the corner near end of coconuts (left of eels)
    "Ship Rex - Golden Cog 6":
        LocData(0x08750161, "Ship Rex - Beyond Gate 1"),
    # Small rockpool
    "Ship Rex - Golden Cog 7":
        LocData(0x08750162, "Ship Rex - Beyond Gate 1"),
    # Top of spire
    "Ship Rex - Golden Cog 8":
        LocData(0x08750163, "Ship Rex - Beyond Gate 1"),
    # Floating platform near opal machine
    "Ship Rex - Golden Cog 9":
        LocData(0x08750164, "Ship Rex - Beyond Gate 1"),
    # Large raised area in ship wreck area
    "Ship Rex - Golden Cog 10":
        LocData(0x08750165, "Ship Rex - Beyond Gate 1"),
    # On pillar near big tree in starting area (glide down from higher area)
    "BotRT - Golden Cog 1":
        LocData(0x08750166, "Bridge on the River Ty"),
    # Behind cobweb after first dunny
    "BotRT - Golden Cog 2":
        LocData(0x08750167, "Bridge on the River Ty"),
    # Hidden in corner below first dunny
    "BotRT - Golden Cog 3":
        LocData(0x08750168, "Bridge on the River Ty"),
    # On pillar in spider den
    "BotRT - Golden Cog 4":
        LocData(0x08750169, "Bridge on the River Ty"),
    # Hidden side of steps near dennis
    "BotRT - Golden Cog 5":
        LocData(0x0875016A, "Bridge on the River Ty"),
    # Dead tree near opal machine
    "BotRT - Golden Cog 6":
        LocData(0x0875016B, "Bridge on the River Ty"),
    # Platform protected by bats and pontoons in corner
    "BotRT - Golden Cog 7":
        LocData(0x0875016C, "Bridge on the River Ty"),
    # Platform in middle of water under large bridge
    "BotRT - Golden Cog 8":
        LocData(0x0875016D, "Bridge on the River Ty"),
    # Hollow log in Dennis' house
    "BotRT - Golden Cog 9":
        LocData(0x0875016E, "Bridge on the River Ty"),
    # Under small bridge along Dennis escort path
    "BotRT - Golden Cog 10":
        LocData(0x0875016F, "Bridge on the River Ty"),
    # Pillar platforming on the right side of right ice path at start
    "Snow Worries - Golden Cog 1":
        LocData(0x08750170, "Snow Worries"),
    # Middle of hole in ice above ice sheet
    "Snow Worries - Golden Cog 2":
        LocData(0x08750171, "Snow Worries"),
    # Pillar at the base of mountain steps
    "Snow Worries - Golden Cog 3":
        LocData(0x08750172, "Snow Worries"),
    # Underwater before gate
    "Snow Worries - Golden Cog 4":
        LocData(0x08750173, "Snow Worries - Underwater"),
    # Behind house at start
    "Snow Worries - Golden Cog 5":
        LocData(0x08750174, "Snow Worries"),
    # On central raised area in ice valley
    "Snow Worries - Golden Cog 6":
        LocData(0x08750175, "Snow Worries"),
    # Underwater behind gate
    "Snow Worries - Golden Cog 7":
        LocData(0x08750176, "Snow Worries - Underwater"),
    # Hidden cave beyond icicle cave
    "Snow Worries - Golden Cog 8":
        LocData(0x08750177, "Snow Worries"),
    # Small platform on right side ice path before bilby and opal ring around tree
    "Snow Worries - Golden Cog 9":
        LocData(0x08750178, "Snow Worries"),
    # On beam above arena steps
    "Snow Worries - Golden Cog 10":
        LocData(0x08750179, "Snow Worries"),
    # On ledge after gap jump in upper waterfall area
    "Outback Safari - Golden Cog 1":
        LocData(0x0875017A, "Outback Safari"),
    # Behind rock in lower waterfall cave
    "Outback Safari - Golden Cog 2":
        LocData(0x0875017B, "Outback Safari"),
    # In ring of hay bales towards end of Shazza escort path
    "Outback Safari - Golden Cog 3":
        LocData(0x0875017C, "Outback Safari"),
    # Inside shed between emus and Shazza escort path
    "Outback Safari - Golden Cog 4":
        LocData(0x0875017D, "Outback Safari"),
    # Inside shed down right path near start
    "Outback Safari - Golden Cog 5":
        LocData(0x0875017E, "Outback Safari"),
    # Inside shed in emus area
    "Outback Safari - Golden Cog 6":
        LocData(0x0875017F, "Outback Safari"),
    # Inside shed in water towers area
    "Outback Safari - Golden Cog 7":
        LocData(0x08750180, "Outback Safari"),
    # Inside shed in corner of lower waterfall area
    "Outback Safari - Golden Cog 8":
        LocData(0x08750181, "Outback Safari"),
    # In ring of hay bales near path leading up to upper area
    "Outback Safari - Golden Cog 9":
        LocData(0x08750182, "Outback Safari"),
    # In shed on spiral path leading to upper area
    "Outback Safari - Golden Cog 10":
        LocData(0x08750183, "Outback Safari"),
    # Hidden by trees on right at bottom of slide
    "LLPoF - Golden Cog 1":
        LocData(0x08750184, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # On pillar at the bottom of slide
    "LLPoF - Golden Cog 2":
        LocData(0x08750185, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # On pillar near spy eggs and bilby in alcove
    "LLPoF - Golden Cog 3":
        LocData(0x08750186, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Ice block
    "LLPoF - Golden Cog 4":
        LocData(0x08750187, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # On metal pillar next to water worries log entrance
    "LLPoF - Golden Cog 5":
        LocData(0x08750188, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Bounce tree
    "LLPoF - Golden Cog 6":
        LocData(0x08750189, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # On pillar before slide
    "LLPoF - Golden Cog 7":
        LocData(0x0875018A, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Spy egg pillar after first log teleport
    "LLPoF - Golden Cog 8":
        LocData(0x0875018B, "Lyre, Lyre Pants on Fire"),
    # Hidden behind cobweb in lever area
    "LLPoF - Golden Cog 9":
        LocData(0x0875018C, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Pillar between "jump to the other side" broken bridge
    "LLPoF - Golden Cog 10":
        LocData(0x0875018D, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Hidden alcove after pillar ponder thunder egg
    "BtBS - Golden Cog 1":
        LocData(0x0875018E, "Beyond the Black Stump - Upper Area"),
    # Snow pile at bottom of cliff area at end
    "BtBS - Golden Cog 2":
        LocData(0x0875018F, "Beyond the Black Stump - Upper Area"),
    # On platform in logs area
    "BtBS - Golden Cog 3":
        LocData(0x08750190, "Beyond the Black Stump - Upper Area"),
    # On ledge on cliff at end
    "BtBS - Golden Cog 4":
        LocData(0x08750191, "Beyond the Black Stump - Upper Area"),
    # At end of opal path on ground at bottom of cliff area at end
    "BtBS - Golden Cog 5":
        LocData(0x08750192, "Beyond the Black Stump - Upper Area"),
    # Ice cave spire
    "BtBS - Golden Cog 6":
        LocData(0x08750193, "Beyond the Black Stump"),
    # Ice block
    "BtBS - Golden Cog 7":
        LocData(0x08750194, "Beyond the Black Stump"),
    # Pillar near to Elizabeth in corner
    "BtBS - Golden Cog 8":
        LocData(0x08750195, "Beyond the Black Stump"),
    # Warp flower cog
    "BtBS - Golden Cog 9":
        LocData(0x08750196, "Beyond the Black Stump"),
    # Next to portal at top of cable cars
    "BtBS - Golden Cog 10":
        LocData(0x08750197, "Beyond the Black Stump - Upper Area"),
    # Underwater near volcano thunder egg and warp flower cog
    "RMtS - Golden Cog 1":
        LocData(0x08750198, "Rex Marks the Spot - Underwater"),
    # On moving platform
    "RMtS - Golden Cog 2":
        LocData(0x08750199, "Rex Marks the Spot"),
    # On large platform near skull rock at start
    "RMtS - Golden Cog 3":
        LocData(0x0875019A, "Rex Marks the Spot"),
    # In middle of sea mines
    "RMtS - Golden Cog 4":
        LocData(0x0875019B, "Rex Marks the Spot - Underwater"),
    # Underwater near eels between coconut shores and bald island !!!!!FRANK!!!!!!
    "RMtS - Golden Cog 5":
        LocData(0x0875019C, "Rex Marks the Spot - Underwater"),
    # Bald island cog
    "RMtS - Golden Cog 6":
        LocData(0x0875019D, "Rex Marks the Spot"),
    # Volcano cog
    "RMtS - Golden Cog 7":
        LocData(0x0875019E, "Rex Marks the Spot"),
    # Coconut shores cog (on floating platform requiring button hit)
    "RMtS - Golden Cog 8":
        LocData(0x0875019F, "Rex Marks the Spot"),
    # Anchor island
    "RMtS - Golden Cog 9":
        LocData(0x087501A0, "Rex Marks the Spot"),
    # Warp flower cog
    "RMtS - Golden Cog 10":
        LocData(0x087501A1, "Rex Marks the Spot"),
}

# Bilbies Dictionary
bilbies_dict = {
    "Two Up - Bilby Dad":
        LocData(0x087501AC, "Two Up"),
    "Two Up - Bilby Mum":
        LocData(0x087501AD, "Two Up"),
    "Two Up - Bilby Boy":
        LocData(0x087501AE, "Two Up"),
    "Two Up - Bilby Girl":
        LocData(0x087501AF, "Two Up"),
    "Two Up - Bilby Grandma":
        LocData(0x087501B0, "Two Up - Upper Area"),
    "WitP - Bilby Dad":
        LocData(0x087501B1, "Walk in the Park"),
    "WitP - Bilby Mum":
        LocData(0x087501B2, "Walk in the Park"),
    "WitP - Bilby Boy":
        LocData(0x087501B3, "Walk in the Park"),
    "WitP - Bilby Girl":
        LocData(0x087501B4, "Walk in the Park"),
    "WitP - Bilby Grandma":
        LocData(0x087501B5, "Walk in the Park"),
    "Ship Rex - Bilby Dad":
        LocData(0x087501B6, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Bilby Mum":
        LocData(0x087501B7, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Bilby Boy":
        LocData(0x087501B8, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Bilby Girl":
        LocData(0x087501B9, "Ship Rex - Beyond Gate 1"),
    "Ship Rex - Bilby Grandma":
        LocData(0x087501BA, "Ship Rex - Beyond Gate 1"),
    "BotRT - Bilby Dad":
        LocData(0x087501BB, "Bridge on the River Ty"),
    "BotRT - Bilby Mum":
        LocData(0x087501BC, "Bridge on the River Ty"),
    "BotRT - Bilby Boy":
        LocData(0x087501BD, "Bridge on the River Ty"),
    "BotRT - Bilby Girl":
        LocData(0x087501BE, "Bridge on the River Ty"),
    "BotRT - Bilby Grandma":
        LocData(0x087501BF, "Bridge on the River Ty"),
    "Snow Worries - Bilby Dad":
        LocData(0x087501C0, "Snow Worries"),
    "Snow Worries - Bilby Mum":
        LocData(0x087501C1, "Snow Worries"),
    "Snow Worries - Bilby Boy":
        LocData(0x087501C2, "Snow Worries"),
    "Snow Worries - Bilby Girl":
        LocData(0x087501C3, "Snow Worries"),
    "Snow Worries - Bilby Grandma":
        LocData(0x087501C4, "Snow Worries"),
    "Outback Safari - Bilby Dad":
        LocData(0x087501C5, "Outback Safari"),
    "Outback Safari - Bilby Mum":
        LocData(0x087501C6, "Outback Safari"),
    "Outback Safari - Bilby Boy":
        LocData(0x087501C7, "Outback Safari"),
    "Outback Safari - Bilby Girl":
        LocData(0x087501C8, "Outback Safari"),
    "Outback Safari - Bilby Grandma":
        LocData(0x087501C9, "Outback Safari"),
    "LLPoF - Bilby Dad":
        LocData(0x087501CA, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Bilby Mum":
        LocData(0x087501CB, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Bilby Boy":
        LocData(0x087501CC, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Bilby Girl":
        LocData(0x087501CD, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "LLPoF - Bilby Grandma":
        LocData(0x087501CE, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "BtBS - Bilby Dad":
        LocData(0x087501CF, "Beyond the Black Stump - Upper Area"),
    "BtBS - Bilby Mum":
        LocData(0x087501D0, "Beyond the Black Stump"),
    "BtBS - Bilby Boy":
        LocData(0x087501D1, "Beyond the Black Stump"),
    "BtBS - Bilby Girl":
        LocData(0x087501D2, "Beyond the Black Stump"),
    "BtBS - Bilby Grandma":
        LocData(0x087501D3, "Beyond the Black Stump - Upper Area"),
    "RMtS - Bilby Dad":
        LocData(0x087501D4, "Rex Marks the Spot"),
    "RMtS - Bilby Mum":
        LocData(0x087501D5, "Rex Marks the Spot"),
    "RMtS - Bilby Boy":
        LocData(0x087501D6, "Rex Marks the Spot"),
    "RMtS - Bilby Girl":
        LocData(0x087501D7, "Rex Marks the Spot"),
    "RMtS - Bilby Grandma":
        LocData(0x087501D8, "Rex Marks the Spot")
}

# Picture_frames Dictionary
picture_frames_dict = {
    # Inside Julius' lab
    "Rainbow Cliffs - PF 1":
        LocData(0x087501D9, "Rainbow Cliffs - PF"),
    # Above talisman display platform
    "Rainbow Cliffs - PF 2":
        LocData(0x087501DA, "Rainbow Cliffs - PF"),
    # Above 1-up down path near Julius' lab
    "Rainbow Cliffs - PF 3":
        LocData(0x087501DB, "Rainbow Cliff - PF"),
    # Corner island next to waterfall cave
    "Rainbow Cliffs - PF 4":
        LocData(0x087501DC, "Rainbow Cliffs - PF"),
    # At entrance to C-zone
    "Rainbow Cliffs - PF 5":
        LocData(0x087501DD, "Rainbow Cliffs - PF"),
    # Near portal to Cass' Crest in E-zone
    "Rainbow Cliffs - PF 6":
        LocData(0x087501DE, "Final Gauntlet"),
    # On the way to A-zone
    "Rainbow Cliffs - PF 7":
        LocData(0x087501DF, "Rainbow Cliffs - PF"),
    # In B-zone
    "Rainbow Cliffs - PF 8":
        LocData(0x087501E0, "Pippy Beach"),
    # Between houses in A-zone
    "Rainbow Cliffs - PF 9":
        LocData(0x087501E1, "Bli Bli Station Gate"),
    # At start
    "Two Up - PF 1":
        LocData(0x087501E2, "Two Up - PF"),
    # Waterfall at top of steps by first bilby
    "Two Up - PF 2":
        LocData(0x087501E3, "Two Up - PF"),
    # Centre of two trees before cave leading to bridge
    "Two Up - PF 3":
        LocData(0x087501E4, "Two Up - PF"),
    # Near dunny on large steps leading down towards ending water section with second rang
    "Two Up - PF 4":
        LocData(0x087501E5, "Two Up - PF"),
    # Near the two crates in upper area
    "Two Up - PF 5":
        LocData(0x087501E6, "Two Up - Upper Area - PF"),
    # In corner near slope down to second rang area from where bunyip is in upper area
    "Two Up - PF 6":
        LocData(0x087501E7, "Two Up - Upper Area - PF"),
    # Empty grassy area next to dunny near spy egg thunder egg
    "Two Up - PF 7":
        LocData(0x087501E8, "Two Up - PF"),
    # At bottom of boulder slopes
    "WitP - PF 1":
        LocData(0x087501E9, "Walk in the Park - PF"),
    # Above middle of valley
    "WitP - PF 2":
        LocData(0x087501EA, "Walk in the Park - PF"),
    # At start
    "WitP - PF 3":
        LocData(0x087501EB, "Walk in the Park - PF"),
    # Inside lower entrance to bat cave
    "WitP - PF 4":
        LocData(0x087501EC, "Walk in the Park - PF"),
    # In waterfall at end
    "WitP - PF 5":
        LocData(0x087501ED, "Walk in the Park - PF"),
    # With bats in bat cave
    "WitP - PF 6":
        LocData(0x087501EE, "Walk in the Park - PF"),
    # Top of spire
    "Ship Rex - PF 1":
        LocData(0x087501EF, "Ship Rex - Beyond Gate 1"),
    # Small island in Ship Wreck area
    "Ship Rex - PF 2":
        LocData(0x087501F0, "Ship Rex - Beyond Gate 1"),
    # Ledge between Nest and Coconut start
    "Ship Rex - PF 3":
        LocData(0x087501F1, "Ship Rex - Beyond Gate 1"),
    # Side of island near tunnel into rock pool
    "Ship Rex - PF 4":
        LocData(0x087501F2, "Ship Rex - Beyond Gate 1"),
    # End of coconuts - Far
    "Ship Rex - PF 5":
        LocData(0x087501F3, "Ship Rex - Beyond Gate 1"),
    # Above shed at start
    "Ship Rex - PF 6":
        LocData(0x087501F4, "Ship Rex - PF"),
    # Right side hut - Start
    "Ship Rex - PF 7":
        LocData(0x087501F5, "Ship Rex - PF"),
    # Left side hut - Start
    "Ship Rex - PF 8":
        LocData(0x087501F6, "Ship Rex - PF"),
    # End of coconuts - Near
    "Ship Rex - PF 9":
        LocData(0x087501F7, "Ship Rex - Beyond Gate 1"),
    # Above Neddy bilby (Above bridge)
    "BotRT - PF 1":
        LocData(0x087501F8, "Bridge on the River Ty - PF"),
    # Ledge near large tree - Large tree (Glide to cog)
    "BotRT - PF 2":
        LocData(0x087501F9, "Bridge on the River Ty - PF"),
    # Corner next to bilby mum
    "BotRT - PF 3":
        LocData(0x087501FA, "Bridge on the River Ty - PF"),
    # Ledge over first bridge
    "BotRT - PF 4":
        LocData(0x087501FB, "Bridge on the River Ty - PF"),
    # Under big tree next to PF 2
    "BotRT - PF 5":
        LocData(0x087501FC, "Bridge on the River Ty - PF"),
    # Next to Rex Diving
    "BotRT - PF 6":
        LocData(0x087501FD, "Bridge on the River Ty - PF"),
    # Under big tree at start - Before 1st Bridge
    "BotRT - PF 7":
        LocData(0x087501FE, "Bridge on the River Ty - PF"),
    # Next to Neddy bilby (Between burner and bridge)
    "BotRT - PF 8":
        LocData(0x087501FF, "Bridge on the River Ty - PF"),
    # Above gap in big bridge (near Neddy)
    "BotRT - PF 9":
        LocData(0x08750200, "Bridge on the River Ty - PF"),
    # Under tree at Ramp onto big bridge
    "BotRT - PF 10":
        LocData(0x08750201, "Bridge on the River Ty - PF"),
    # Under waterfall before spider den
    "BotRT - PF 11":
        LocData(0x08750202, "Bridge on the River Ty - PF"),
    # Dennis House
    "BotRT - PF 12":
        LocData(0x08750203, "Bridge on the River Ty - PF"),
    # Above big bridge - Dennis House side
    "BotRT - PF 13":
        LocData(0x08750204, "Bridge on the River Ty - PF"),
    # Under big bridge - Dennis House side
    "BotRT - PF 14":
        LocData(0x08750205, "Bridge on the River Ty - PF"),
    # Corner near moving platforms
    "BotRT - PF 15":
        LocData(0x08750206, "Bridge on the River Ty - PF"),
    # Above pontoon next to Dennis Starting location
    "BotRT - PF 16":
        LocData(0x08750207, "Bridge on the River Ty - PF"),
    # Neddy Den 1
    "BotRT - PF 17":
        LocData(0x08750208, "Bridge on the River Ty - PF"),
    # Neddy Den 2
    "BotRT - PF 18":
        LocData(0x08750209, "Bridge on the River Ty - PF"),
    # Neddy Den 3
    "BotRT - PF 19":
        LocData(0x0875020A, "Bridge on the River Ty - PF"),
    # Neddy Den 4
    "BotRT - PF 20":
        LocData(0x0875020B, "Bridge on the River Ty - PF"),
    # Above round dirt patch at start
    "Snow Worries - PF 1":
        LocData(0x0875020C, "Snow Worries - PF"),
    # Above round dirt patch by left ice hole
    "Snow Worries - PF 2":
        LocData(0x0875020D, "Snow Worries - PF"),
    # Next to boonie (Above snow)
    "Snow Worries - PF 3":
        LocData(0x0875020E, "Snow Worries - PF"),
    # Opposite cog 9
    "Snow Worries - PF 4":
        LocData(0x0875020F, "Snow Worries - PF"),
    # Ice Spike area
    "Snow Worries - PF 5":
        LocData(0x08750210, "Snow Worries - PF"),
    # Start of pillar platforming - Right side at start
    "Snow Worries - PF 6":
        LocData(0x08750211, "Snow Worries - PF"),
    # Behind pillar platforming - Right side at start
    "Snow Worries - PF 7":
        LocData(0x08750212, "Snow Worries - PF"),
    # Corner before Right Ice Hole
    "Snow Worries - PF 8":
        LocData(0x08750213, "Snow Worries - PF"),
    # Corner after Right Ice Hole (Near frills)
    "Snow Worries - PF 9":
        LocData(0x08750214, "Snow Worries - PF"),
    # Above round dirt patch near bilby dad
    "Snow Worries - PF 10":
        LocData(0x08750215, "Snow Worries - PF"),
    # Next to boonie (Above ice)
    "Snow Worries - PF 11":
        LocData(0x08750216, "Snow Worries - PF"),
    # Near ice blocks - higher on slope
    "Snow Worries - PF 12":
        LocData(0x08750217, "Snow Worries - PF"),
    # Behind ice blocks
    "Snow Worries - PF 13":
        LocData(0x08750218, "Snow Worries - PF"),
    # Above round dirt patch near icicle cave
    "Snow Worries - PF 14":
        LocData(0x08750219, "Snow Worries - PF"),
    # Left side - 1st indent
    "Snow Worries - PF 15":
        LocData(0x0875021A, "Snow Worries - PF"),
    # Left side - 3rd indent
    "Snow Worries - PF 16":
        LocData(0x0875021B, "Snow Worries - PF"),
    # Left side - 2nd indent
    "Snow Worries - PF 17":
        LocData(0x0875021C, "Snow Worries - PF"),
    # Corner after left ice hole
    "Snow Worries - PF 18":
        LocData(0x0875021D, "Snow Worries - PF"),
    # Behind house
    "Snow Worries - PF 19":
        LocData(0x0875021E, "Snow Worries - PF"),
    # Near Mim
    "Snow Worries - PF 20":
        LocData(0x0875021F, "Snow Worries - PF"),
    # Bottom of center path - on left before left ice hole (above snow)
    "Snow Worries - PF 21":
        LocData(0x08750220, "Snow Worries - PF"),
    # Left of path leading to mountain steps
    "Snow Worries - PF 22":
        LocData(0x08750221, "Snow Worries - PF"),
    # Bottom of right side path (On snow past tree bilby)
    "Snow Worries - PF 23":
        LocData(0x08750222, "Snow Worries - PF"),
    # Between PF 8 and PF 23
    "Snow Worries - PF 24":
        LocData(0x08750223, "Snow Worries - PF"),
    # Between "Jump to the other side" gap
    "LLPoF - PF 1":
        LocData(0x08750224, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # At Start
    "LLPoF - PF 2":
        LocData(0x08750225, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Bottom of slide
    "LLPoF - PF 3":
        LocData(0x08750226, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Next to bounce tree
    "LLPoF - PF 4":
        LocData(0x08750227, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Next to dunny @ top of slide
    "LLPoF - PF 5":
        LocData(0x08750228, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    # Behind cable car platform house
    "BtBS - PF 1":
        LocData(0x08750229, "Beyond the Black Stump - Upper Area - PF"),
    # Corner near cable car platform house near ice
    "BtBS - PF 2":
        LocData(0x0875022A, "Beyond the Black Stump - Upper Area - PF"),
    # Corner past cable car platform house 1
    "BtBS - PF 3":
        LocData(0x0875022B, "Beyond the Black Stump - Upper Area - PF"),
    # Corner past cable car platform house 2
    "BtBS - PF 4":
        LocData(0x0875022C, "Beyond the Black Stump - Upper Area - PF"),
    # Ski slope level 4 - Right Side
    "BtBS - PF 5":
        LocData(0x0875022D, "Beyond the Black Stump - Upper Area - PF"),
    # Ski slope level 4 - left side
    "BtBS - PF 6":
        LocData(0x0875022E, "Beyond the Black Stump - Upper Area - PF"),
    # Ski slope level 2
    "BtBS - PF 7":
        LocData(0x0875022F, "Beyond the Black Stump - Upper Area - PF"),
    # Ski slope level 3
    "BtBS - PF 8":
        LocData(0x08750230, "Beyond the Black Stump - Upper Area - PF"),
    # Ski slope level 1
    "BtBS - PF 9":
        LocData(0x08750231, "Beyond the Black Stump - Upper Area - PF"),
    # Above fire logs near Rafflesia to Liz
    "BtBS - PF 10":
        LocData(0x08750232, "Beyond the Black Stump - PF"),
    # Behind fire @ start
    "BtBS - PF 11":
        LocData(0x08750233, "Beyond the Black Stump - PF"),
    # Above fire opposite Katie
    "BtBS - PF 12":
        LocData(0x08750234, "Beyond the Black Stump - PF"),
    # Between Boonie and Liz
    "BtBS - PF 13":
        LocData(0x08750235, "Beyond the Black Stump - PF"),
    # Center of valley leading to Katie
    "BtBS - PF 14":
        LocData(0x08750236, "Beyond the Black Stump - PF"),
    # Past 3rd flower in flower chain
    "BtBS - PF 15":
        LocData(0x08750237, "Beyond the Black Stump - PF"),
    # Near ice block cog
    "BtBS - PF 16":
        LocData(0x08750238, "Beyond the Black Stump - PF"),
    # Above crossroads at start
    "BtBS - PF 17":
        LocData(0x08750239, "Beyond the Black Stump - PF"),
    # Under final log in log climb
    "BtBS - PF 18":
        LocData(0x0875023A, "Beyond the Black Stump - PF"),
    # Next to bunyip in pillar area
    "BtBS - PF 19":
        LocData(0x0875023B, "Beyond the Black Stump - Upper Area - PF"),
    # Straight ahead after log climb
    "BtBS - PF 20":
        LocData(0x0875023C, "Beyond the Black Stump - Upper Area - PF"),
    # Left side after first big ice patch after log climb
    "BtBS - PF 21":
        LocData(0x0875023D, "Beyond the Black Stump - Upper Area - PF"),
    # Between cable car platform and bilby mum
    "BtBS - PF 22":
        LocData(0x0875023E, "Beyond the Black Stump - Upper Area - PF"),
    # Just before Bad Boonie
    "BtBS - PF 23":
        LocData(0x0875023F, "Beyond the Black Stump - Upper Area - PF"),
    # Above platform start of final log in log climb
    "BtBS - PF 24":
        LocData(0x08750240, "Beyond the Black Stump - Upper Area - PF"),
    # Above blue tongues
    "BtBS - PF 25":
        LocData(0x08750241, "Beyond the Black Stump - PF"),
    # End area next to cliff ledge cog
    "BtBS - PF 26":
        LocData(0x08750242, "Beyond the Black Stump - Upper Area - PF"),
    # Next to Cog 5
    "BtBS - PF 27":
        LocData(0x08750243, "Beyond the Black Stump - Upper Area - PF"),
    # In trees - Turret area 1
    "BtBS - PF 28":
        LocData(0x08750244, "Beyond the Black Stump - Upper Area - PF"),
    # In trees - Turret area 2
    "BtBS - PF 29":
        LocData(0x08750245, "Beyond the Black Stump - Upper Area - PF"),
    # Bald island
    "RMtS - PF 1":
        LocData(0x08750246, "Rex Marks the Spot - PF"),
    # Anchor island
    "RMtS - PF 2":
        LocData(0x08750247, "Rex Marks the Spot - PF"),
    # Coconut shores near geyser
    "RMtS - PF 3":
        LocData(0x08750248, "Rex Marks the Spot - PF"),
    # Coconut shores near cog in water towards bald island
    "RMtS - PF 4":
        LocData(0x08750249, "Rex Marks the Spot - PF"),
    # Coconut shores near shores chest
    "RMtS - PF 5":
        LocData(0x0875024A, "Rex Marks the Spot - PF"),
    # Figure 8 island towards coconut shores floating platform cog
    "RMtS - PF 6":
        LocData(0x0875024B, "Rex Marks the Spot - PF"),
    # Figure 8 island opposite PF 6 towards PF 5
    "RMtS - PF 7":
        LocData(0x0875024C, "Rex Marks the Spot - PF"),
    # Figure 8 island opposite PF 6 away from PF 5 next to PF 7
    "RMtS - PF 8":
        LocData(0x0875024D, "Rex Marks the Spot - PF"),
    # Skull rock
    "RMtS - PF 9":
        LocData(0x0875024E, "Rex Marks the Spot - PF"),
    # Figure 8 island on the right of opal path at start
    "RMtS - PF 10":
        LocData(0x0875024F, "Rex Marks the Spot - PF"),
    # Crab island towards cog underwater near warp flower cog
    "RMtS - PF 11":
        LocData(0x08750250, "Rex Marks the Spot - PF"),
    # Crab island closest to fence near bilby
    "RMtS - PF 12":
        LocData(0x08750251, "Rex Marks the Spot - PF"),
    # Crab island on approach from opal path
    "RMtS - PF 13":
        LocData(0x08750252, "Rex Marks the Spot - PF"),
    # Island on the right of opal path leading to crab island next to dunny
    "RMtS - PF 14":
        LocData(0x08750253, "Rex Marks the Spot - PF"),
    # Same island as PF 14 near sunken ship
    "RMtS - PF 15":
        LocData(0x08750254, "Rex Marks the Spot - PF"),
    # Same island as PF 15 opposite side
    "RMtS - PF 16":
        LocData(0x08750255, "Rex Marks the Spot - PF"),
    # Outside volcano entrance
    "RMtS - PF 17":
        LocData(0x08750256, "Rex Marks the Spot - PF"),
    # Inside volcano
    "RMtS - PF 18":
        LocData(0x08750257, "Rex Marks the Spot - PF")
}

# Attributes Dictionary
attributes_dict = {
    "Attribute - Second Rang":
        LocData(0x08750312, "Two Up"),
    "Attribute - Swim":
        LocData(0x08750310, "Ship Rex"),
    "Attribute - Dive":
        LocData(0x08750311, "Bridge on the River Ty"),
    "Attribute - Doomerang":
        LocData(0x08750318, "Final Battle"),
    "Attribute - Extra Health":
        LocData(0x08750313, "Rainbow Cliffs"),
    "Attribute - Aquarang":
        LocData(0x0875031D, "Ship Rex"),
    "Attribute - Zoomerang":
        LocData(0x0875031A, "Rainbow Cliffs"),
    "Attribute - Multirang":
        LocData(0x0875031E, "Rainbow Cliffs"),
    "Attribute - Infrarang":
        LocData(0x0875031B, "Rainbow Cliffs"),
    "Attribute - Megarang":
        LocData(0x08750319, "Rainbow Cliffs"),
    "Attribute - Kaboomarang":
        LocData(0x08750317, "Rainbow Cliffs"),
    "Attribute - Chronorang":
        LocData(0x0875031F, "Rainbow Cliffs"),
}

# Cog_completion Dictionary
cog_completion_dict = {
    "Two Up - All Golden Cogs":
        LocData(0x087501A2, "Two Up - Upper Area"),
    "WitP - All Golden Cogs":
        LocData(0x087501A3, "Walk in the Park"),
    "Ship Rex - All Golden Cogs":
        LocData(0x087501A4, "Ship Rex - Beyond Gate 1"),
    "BotRT - All Golden Cogs":
        LocData(0x087501A5, "Bridge on the River Ty"),
    "Snow Worries - All Golden Cogs":
        LocData(0x087501A6, "Snow Worries - Underwater"),
    "Outback Safari - All Golden Cogs":
        LocData(0x087501A7, "Outback Safari"),
    "LLPoF - All Golden Cogs":
        LocData(0x087501A8, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "BtBS - All Golden Cogs":
        LocData(0x087501A9, "Beyond the Black Stump - Upper Area"),
    "RMtS - All Golden Cogs":
        LocData(0x087501AA, "Rex Marks the Spot - Underwater"),
}

# Frame_completion Dictionary
frame_completion_dict = {
    "Rainbow Cliffs - All Picture Frames":
        LocData(0x08750258, "Final Gauntlet"),
    "Two Up - All Picture Frames":
        LocData(0x08750259, "Two Up - Upper Area - PF"),
    "WitP - All Picture Frames":
        LocData(0x0875025A, "Walk in the Park - PF"),
    "Ship Rex - All Picture Frames":
        LocData(0x0875025B, "Ship Rex - Beyond Gate 1"),
    "BotRT - All Picture Frames":
        LocData(0x0875025C, "Bridge on the River Ty - PF"),
    "Snow Worries - All Picture Frames":
        LocData(0x0875025D, "Snow Worries - PF"),
    "LLPoF - All Picture Frames":
        LocData(0x0875025E, "Lyre, Lyre Pants on Fire - Beyond Gate"),
    "BtBS - All Picture Frames":
        LocData(0x0875025F, "Beyond the Black Stump - Upper Area - PF"),
    "RMtS - All Picture Frames":
        LocData(0x08750260, "Rex Marks the Spot - PF"),
}

bilby_completion_dict = {
    "Two Up - Bilby Completion":
        LocData(0x08750270, "Rainbow Cliffs"),
    "WitP - Bilby Completion":
        LocData(0x08750271, "Rainbow Cliffs"),
    "Ship Rex - Bilby Completion":
        LocData(0x08750272, "Rainbow Cliffs"),
    "BotRT - Bilby Completion":
        LocData(0x08750273, "Rainbow Cliffs"),
    "Snow Worries - Bilby Completion":
        LocData(0x08750274, "Rainbow Cliffs"),
    "Outback Safari - Bilby Completion":
        LocData(0x08750275, "Rainbow Cliffs"),
    "LLPoF - Bilby Completion":
        LocData(0x08750276, "Rainbow Cliffs"),
    "BtBS - Bilby Completion":
        LocData(0x08750277, "Rainbow Cliffs"),
    "RMtS - Bilby Completion":
        LocData(0x08750278, "Rainbow Cliffs"),
}

# Talismans Dictionary
talismans_dict = {
    "Frog Talisman":
        LocData(0x08750261, "Bull's Pen"),
    "Platypus Talisman":
        LocData(0x08750262, "Crikey's Cove"),
    "Cockatoo Talisman":
        LocData(0x08750263, "Fluffy's Fjord"),
    "Dingo Talisman":
        LocData(0x08750264, "Cass' Crest"),
    "Tiger Talisman":
        LocData(0x08750265, "Final Battle"),
}

# Elemental Rangs Dictionary
elemental_rangs_dict = {
    # Counts are set to hub te count in regions.py in evaluate_condition
    "Attribute - Flamerang":
        LocData(0x08750316, "Rainbow Cliffs"),
    "Attribute - Frostyrang":
        LocData(0x08750315, "Rainbow Cliffs"),
    "Attribute - Zappyrang":
        LocData(0x0875031C, "Rainbow Cliffs")
}

ty1_location_table = {
    **thunder_eggs_dict,
    **golden_cogs_dict,
    **bilbies_dict,
    **picture_frames_dict,
    **attributes_dict,
    **cog_completion_dict,
    **frame_completion_dict,
    **bilby_completion_dict,
    **talismans_dict,
    **elemental_rangs_dict
}
