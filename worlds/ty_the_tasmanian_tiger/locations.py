from BaseClasses import Location, Region
from worlds.ty_the_tasmanian_tiger.options import Ty1Options


class Ty1Location(Location):
    game: str = "Ty the Tasmanian Tiger"


class LocData:
    def __init__(self, code: int, region: str):
        """
        Represents a location with associated conditions.

        :param code: A unique identifier for the location.
        :param region: Name of the containing region.
        """
        self.code = code
        self.region = region


def create_location(player: int, reg: Region, name: str, code: int):
    location = Ty1Location(player, name, code, reg)
    reg.locations.append(location)


def create_locations_from_dict(loc_dict, reg, player):
    for (key, data) in loc_dict.items():
        if data.region != reg.name:
            continue
        create_location(player, reg, key, data.code)


def create_locations(player: int, options: Ty1Options, reg: Region):
    # THUNDER EGGS
    create_locations_from_dict(thunder_eggs_dict, reg, player)
    # GOLDEN COGS
    create_locations_from_dict(golden_cogs_dict, reg, player)
    # COG COMPLETION
    create_locations_from_dict(cog_completion_dict, reg, player)
    # BILBIES
    create_locations_from_dict(bilbies_dict, reg, player)
    # BILBY COMPLETION
    create_locations_from_dict(bilby_completion_dict, reg, player)
    # TALISMANS
    create_locations_from_dict(talismans_dict, reg, player)
    # PICTURE FRAMES
    if options.framesanity == 0:
        create_locations_from_dict(picture_frames_dict, reg, player)
    # FRAME COMPLETION
    if options.framesanity == 1:
        create_locations_from_dict(frame_completion_dict, reg, player)
    # SCALES
    if options.scalesanity:
        create_locations_from_dict(scales_dict, reg, player)
        if reg.name == "Rainbow Cliffs":
            create_location(player, reg, "Attribute - Extra Health", 0x08750313)
    # OPALS
    if options.opalsanity:
        create_locations_from_dict(opals_dict, reg, player)
    # SIGNS
    if options.signsanity:
        create_locations_from_dict(signposts_dict, reg, player)
    # LIVES
    if options.lifesanity:
        create_locations_from_dict(extra_lives_dict, reg,player)
    # ATTRIBUTES
    create_locations_from_dict(attributes_dict, reg, player)
    # ELEMENTAL RANGS
    create_locations_from_dict(elemental_rangs_dict, reg, player)
    # TIME ATTACK CHALLENGES
    if options.gate_time_attacks:
        create_locations_from_dict(time_attack_challenge_dict, reg, player)


thunder_eggs_dict = {
    # Two Up Thunder Eggs
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
    # Walk Thunder Eggs
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
    # Ship Thunder Eggs
    "Ship Rex - Collect 300 Opals":
        LocData(0x08750110, "Ship Rex - Beyond Gate"),
    "Ship Rex - Find 5 Bilbies":
        LocData(0x08750111, "Ship Rex - Beyond Gate"),
    "Ship Rex - Race Rex":
        LocData(0x08750112, "Ship Rex"),
    "Ship Rex - Where's Elle?":
        LocData(0x08750113, "Ship Rex - Beyond Gate"),
    "Ship Rex - Aurora's Kids":
        LocData(0x08750114, "Ship Rex - Beyond Gate"),
    "Ship Rex - Quicksand Coconuts":
        LocData(0x08750115, "Ship Rex - Beyond Gate"),
    "Ship Rex - Ship Wreck":
        LocData(0x08750116, "Ship Rex - Beyond Gate"),
    "Ship Rex - Nest Egg":
        LocData(0x08750117, "Ship Rex - Beyond Gate"),
    # Bridge Thunder Eggs
    "BotRT - Collect 300 Opals":
        LocData(0x08750118, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Find 5 Bilbies":
        LocData(0x08750119, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Time Attack":
        LocData(0x0875011A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Home, Sweet, Home":
        LocData(0x0875011B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Heat Dennis' House":
        LocData(0x0875011C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Tag Team Turkeys":
        LocData(0x0875011D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Ty Diving":
        LocData(0x0875011E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Neddy The Bully":
        LocData(0x0875011F, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Snow Thunder Eggs
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
    # Outback Thunder Eggs
    "Outback Safari - Collect 300 Opals":
        LocData(0x08750128, "Outback Safari"),
    "Outback Safari - Find 5 Bilbies":
        LocData(0x08750129, "Outback Safari"),
    "Outback Safari - Race Shazza":
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
    # Lyre Thunder Eggs
    "LLPoF - Collect 300 Opals":
        LocData(0x08750130, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Find 5 Bilbies":
        LocData(0x08750131, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Time Attack":
        LocData(0x08750132, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Lenny The Lyrebird":
        LocData(0x08750133, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Fiery Furnace":
        LocData(0x08750134, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Water Worries":
        LocData(0x08750135, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Muddy Towers":
        LocData(0x08750136, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Gantry Glide":
        LocData(0x08750137, "Lyre, Lyre Pants on Fire"),
    # Stump Thunder Eggs
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
    # Rex Marks Thunder Eggs
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
        LocData(0x0875015C, "Ship Rex - Beyond Gate"),
    # On pillar to the right after entering main area Beyond Gate
    "Ship Rex - Golden Cog 2":
        LocData(0x0875015D, "Ship Rex - Beyond Gate"),
    # Wood platform at start
    "Ship Rex - Golden Cog 3":
        LocData(0x0875015E, "Ship Rex"),
    # Large rockpool
    "Ship Rex - Golden Cog 4":
        LocData(0x0875015F, "Ship Rex - Beyond Gate"),
    # Floating platform reached from geyser
    "Ship Rex - Golden Cog 5":
        LocData(0x08750160, "Ship Rex - Beyond Gate"),
    # Island in the corner near end of coconuts (left of eels)
    "Ship Rex - Golden Cog 6":
        LocData(0x08750161, "Ship Rex - Beyond Gate"),
    # Small rockpool
    "Ship Rex - Golden Cog 7":
        LocData(0x08750162, "Ship Rex - Beyond Gate"),
    # Top of spire
    "Ship Rex - Golden Cog 8":
        LocData(0x08750163, "Ship Rex - Beyond Gate"),
    # Floating platform near opal machine
    "Ship Rex - Golden Cog 9":
        LocData(0x08750164, "Ship Rex - Beyond Gate"),
    # Large raised area in ship wreck area
    "Ship Rex - Golden Cog 10":
        LocData(0x08750165, "Ship Rex - Beyond Gate"),
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
        LocData(0x0875016A, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Dead tree near opal machine
    "BotRT - Golden Cog 6":
        LocData(0x0875016B, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Platform protected by bats and pontoons in corner
    "BotRT - Golden Cog 7":
        LocData(0x0875016C, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Platform in middle of water under large bridge
    "BotRT - Golden Cog 8":
        LocData(0x0875016D, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Hollow log in Dennis' house
    "BotRT - Golden Cog 9":
        LocData(0x0875016E, "Bridge on the River Ty - Beyond Broken Bridge"),
    # Under small bridge along Dennis escort path
    "BotRT - Golden Cog 10":
        LocData(0x0875016F, "Bridge on the River Ty - Beyond Broken Bridge"),
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
        LocData(0x08750184, "Lyre, Lyre Pants on Fire"),
    # On pillar at the bottom of slide
    "LLPoF - Golden Cog 2":
        LocData(0x08750185, "Lyre, Lyre Pants on Fire"),
    # On pillar near spy eggs and bilby in alcove
    "LLPoF - Golden Cog 3":
        LocData(0x08750186, "Lyre, Lyre Pants on Fire"),
    # Ice block
    "LLPoF - Golden Cog 4":
        LocData(0x08750187, "Lyre, Lyre Pants on Fire"),
    # On metal pillar next to water worries log entrance
    "LLPoF - Golden Cog 5":
        LocData(0x08750188, "Lyre, Lyre Pants on Fire"),
    # Bounce tree
    "LLPoF - Golden Cog 6":
        LocData(0x08750189, "Lyre, Lyre Pants on Fire"),
    # On pillar before slide
    "LLPoF - Golden Cog 7":
        LocData(0x0875018A, "Lyre, Lyre Pants on Fire"),
    # Spy egg pillar after first log teleport
    "LLPoF - Golden Cog 8":
        LocData(0x0875018B, "Lyre, Lyre Pants on Fire"),
    # Hidden behind cobweb in lever area
    "LLPoF - Golden Cog 9":
        LocData(0x0875018C, "Lyre, Lyre Pants on Fire"),
    # Pillar between "jump to the other side" broken bridge
    "LLPoF - Golden Cog 10":
        LocData(0x0875018D, "Lyre, Lyre Pants on Fire"),
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
        LocData(0x087501B6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Bilby Mum":
        LocData(0x087501B7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Bilby Boy":
        LocData(0x087501B8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Bilby Girl":
        LocData(0x087501B9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Bilby Grandma":
        LocData(0x087501BA, "Ship Rex - Beyond Gate"),
    "BotRT - Bilby Dad":
        LocData(0x087501BB, "Bridge on the River Ty"),
    "BotRT - Bilby Mum":
        LocData(0x087501BC, "Bridge on the River Ty"),
    "BotRT - Bilby Boy":
        LocData(0x087501BD, "Bridge on the River Ty"),
    "BotRT - Bilby Girl":
        LocData(0x087501BE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Bilby Grandma":
        LocData(0x087501BF, "Bridge on the River Ty - Beyond Broken Bridge"),
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
        LocData(0x087501CA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Bilby Mum":
        LocData(0x087501CB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Bilby Boy":
        LocData(0x087501CC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Bilby Girl":
        LocData(0x087501CD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Bilby Grandma":
        LocData(0x087501CE, "Lyre, Lyre Pants on Fire"),
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

picture_frames_dict = {
    # Inside Julius' lab
    "Rainbow Cliffs - PF 1":
        LocData(0x087501D9, "Rainbow Cliffs - PF"),
    # Above talisman display platform
    "Rainbow Cliffs - PF 2":
        LocData(0x087501DA, "Rainbow Cliffs - PF"),
    # Above 1-up down path near Julius' lab
    "Rainbow Cliffs - PF 3":
        LocData(0x087501DB, "Rainbow Cliffs - PF"),
    # Corner island next to waterfall cave
    "Rainbow Cliffs - PF 4":
        LocData(0x087501DC, "Rainbow Cliffs - PF"),
    # At entrance to C-zone
    "Rainbow Cliffs - PF 5":
        LocData(0x087501DD, "Rainbow Cliffs - PF"),
    # Near portal to Cass' Crest in E-zone
    "Rainbow Cliffs - PF 6":
        LocData(0x087501DE, "Final Gauntlet - PF"),
    # On the way to A-zone
    "Rainbow Cliffs - PF 7":
        LocData(0x087501DF, "Rainbow Cliffs - PF"),
    # In B-zone
    "Rainbow Cliffs - PF 8":
        LocData(0x087501E0, "Pippy Beach - PF"),
    # Between houses in A-zone
    "Rainbow Cliffs - PF 9":
        LocData(0x087501E1, "Bli Bli Station Gate - PF"),
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
        LocData(0x087501EF, "Ship Rex - Beyond Gate - PF"),
    # Small island in Ship Wreck area
    "Ship Rex - PF 2":
        LocData(0x087501F0, "Ship Rex - Beyond Gate - PF"),
    # Ledge between Nest and Coconut start
    "Ship Rex - PF 3":
        LocData(0x087501F1, "Ship Rex - Beyond Gate - PF"),
    # Side of island near tunnel into rock pool
    "Ship Rex - PF 4":
        LocData(0x087501F2, "Ship Rex - Beyond Gate - PF"),
    # End of coconuts - Far
    "Ship Rex - PF 5":
        LocData(0x087501F3, "Ship Rex - Beyond Gate - PF"),
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
        LocData(0x087501F7, "Ship Rex - Beyond Gate - PF"),
    # Above Neddy bilby (Above bridge)
    "BotRT - PF 1":
        LocData(0x087501F8, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
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
        LocData(0x087501FD, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Under big tree at start - Before 1st Bridge
    "BotRT - PF 7":
        LocData(0x087501FE, "Bridge on the River Ty - PF"),
    # Next to Neddy bilby (Between burner and bridge)
    "BotRT - PF 8":
        LocData(0x087501FF, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Above gap in big bridge (near Neddy)
    "BotRT - PF 9":
        LocData(0x08750200, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Under tree at Ramp onto big bridge
    "BotRT - PF 10":
        LocData(0x08750201, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Under waterfall before spider den
    "BotRT - PF 11":
        LocData(0x08750202, "Bridge on the River Ty - PF"),
    # Dennis House
    "BotRT - PF 12":
        LocData(0x08750203, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Above big bridge - Dennis House side
    "BotRT - PF 13":
        LocData(0x08750204, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Under big bridge - Dennis House side
    "BotRT - PF 14":
        LocData(0x08750205, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Corner near moving platforms
    "BotRT - PF 15":
        LocData(0x08750206, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Above pontoon next to Dennis Starting location
    "BotRT - PF 16":
        LocData(0x08750207, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Neddy Den 1
    "BotRT - PF 17":
        LocData(0x08750208, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Neddy Den 2
    "BotRT - PF 18":
        LocData(0x08750209, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Neddy Den 3
    "BotRT - PF 19":
        LocData(0x0875020A, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    # Neddy Den 4
    "BotRT - PF 20":
        LocData(0x0875020B, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
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
        LocData(0x08750224, "Lyre, Lyre Pants on Fire - PF"),
    # At Start
    "LLPoF - PF 2":
        LocData(0x08750225, "Lyre, Lyre Pants on Fire - PF"),
    # Bottom of slide
    "LLPoF - PF 3":
        LocData(0x08750226, "Lyre, Lyre Pants on Fire - PF"),
    # Next to bounce tree
    "LLPoF - PF 4":
        LocData(0x08750227, "Lyre, Lyre Pants on Fire - PF"),
    # Next to dunny @ top of slide
    "LLPoF - PF 5":
        LocData(0x08750228, "Lyre, Lyre Pants on Fire - PF"),
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

attributes_dict = {
    "Attribute - Second Rang":
        LocData(0x08750312, "Two Up"),
    "Attribute - Swim":
        LocData(0x08750310, "Ship Rex"),
    "Attribute - Dive":
        LocData(0x08750311, "Bridge on the River Ty"),
    "Attribute - Doomerang":
        LocData(0x08750318, "Final Battle"),
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

cog_completion_dict = {
    "Two Up - All Golden Cogs":
        LocData(0x087501A2, "Two Up - Upper Area"),
    "WitP - All Golden Cogs":
        LocData(0x087501A3, "Walk in the Park"),
    "Ship Rex - All Golden Cogs":
        LocData(0x087501A4, "Ship Rex - Beyond Gate"),
    "BotRT - All Golden Cogs":
        LocData(0x087501A5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "Snow Worries - All Golden Cogs":
        LocData(0x087501A6, "Snow Worries - Underwater"),
    "Outback Safari - All Golden Cogs":
        LocData(0x087501A7, "Outback Safari"),
    "LLPoF - All Golden Cogs":
        LocData(0x087501A8, "Lyre, Lyre Pants on Fire"),
    "BtBS - All Golden Cogs":
        LocData(0x087501A9, "Beyond the Black Stump - Upper Area"),
    "RMtS - All Golden Cogs":
        LocData(0x087501AA, "Rex Marks the Spot - Underwater"),
}

frame_completion_dict = {
    "Rainbow Cliffs - All Picture Frames":
        LocData(0x08750258, "Rainbow Cliffs"),
    "Two Up - All Picture Frames":
        LocData(0x08750259, "Two Up - Upper Area - PF"),
    "WitP - All Picture Frames":
        LocData(0x0875025A, "Walk in the Park - PF"),
    "Ship Rex - All Picture Frames":
        LocData(0x0875025B, "Ship Rex - Beyond Gate - PF"),
    "BotRT - All Picture Frames":
        LocData(0x0875025C, "Bridge on the River Ty - Beyond Broken Bridge - PF"),
    "Snow Worries - All Picture Frames":
        LocData(0x0875025D, "Snow Worries - PF"),
    "LLPoF - All Picture Frames":
        LocData(0x0875025E, "Lyre, Lyre Pants on Fire - PF"),
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

elemental_rangs_dict = {
    "Attribute - Flamerang":
        LocData(0x08750316, "Rainbow Cliffs"),
    "Attribute - Frostyrang":
        LocData(0x08750315, "Rainbow Cliffs"),
    "Attribute - Zappyrang":
        LocData(0x0875031C, "Rainbow Cliffs")
}

scales_dict = {
    # Behind right-hand house in A-zone
    "Rainbow Scale 1":
        LocData(0x8750350, "Bli Bli Station Gate"),
    # Behind left-hand house in A-zone
    "Rainbow Scale 2":
        LocData(0x8750351, "Bli Bli Station Gate"),
    # In corner hidden behind Julius' lab
    "Rainbow Scale 3":
        LocData(0x8750352, "Rainbow Cliffs"),
    # Under Thunder Egg collector in B-zone
    "Rainbow Scale 4":
        LocData(0x8750353, "Pippy Beach"),
    # Just past flame logs in C-zone
    "Rainbow Scale 5":
        LocData(0x8750354, "Lake Burril"),
    # On small ledge on the side of starting pillar
    "Rainbow Scale 6":
        LocData(0x8750355, "Rainbow Cliffs"),
    # Inside waterfall cave
    "Rainbow Scale 7":
        LocData(0x8750356, "Rainbow Cliffs"),
    # Corner island next to waterfall cave
    "Rainbow Scale 8":
        LocData(0x8750357, "Rainbow Cliffs"),
    # Side of path between B-zone and Julius' lab 1
    "Rainbow Scale 9":
        LocData(0x8750358, "Rainbow Cliffs"),
    # Next to extra life
    "Rainbow Scale 10":
        LocData(0x8750359, "Rainbow Cliffs"),
    # Above water next to Julius' lab (pontoon scale)
    "Rainbow Scale 11":
        LocData(0x875035A, "Rainbow Cliffs"),
    # After pillar platforms leading up to C-zone
    "Rainbow Scale 12":
        LocData(0x875035B, "Rainbow Cliffs"),
    # In the water next to pillar platforms leading up to C-zone
    "Rainbow Scale 13":
        LocData(0x875035C, "Rainbow Cliffs"),
    # Behind rock at entrance to B-zone
    "Rainbow Scale 14":
        LocData(0x875035D, "Rainbow Cliffs"),
    # Inside starting pillar
    "Rainbow Scale 15":
        LocData(0x875035E, "Rainbow Cliffs"),
    # Underwater near Julius' lab
    "Rainbow Scale 16":
        LocData(0x875035F, "Rainbow Cliffs"),
    # On wooden platform in C-zone
    "Rainbow Scale 17":
        LocData(0x8750360, "Lake Burril"),
    # Under Thunder Egg collector in C-zone
    "Rainbow Scale 18":
        LocData(0x8750361, "Lake Burril"),
    # Just past ice wall in B-zone
    "Rainbow Scale 19":
        LocData(0x8750362, "Pippy Beach"),
    # Next to water wheel on wooden walkway at Julius' lab
    "Rainbow Scale 20":
        LocData(0x8750363, "Rainbow Cliffs"),
    # Underwater near waterfall cave
    "Rainbow Scale 21":
        LocData(0x8750364, "Rainbow Cliffs"),
    # Just past E-zone gate
    "Rainbow Scale 22":
        LocData(0x8750365, "Final Gauntlet"),
    # Hidden around corner in E-zone
    "Rainbow Scale 23":
        LocData(0x8750366, "Final Gauntlet"),
    # Floating in the air next to starting pillar
    "Rainbow Scale 24":
        LocData(0x8750367, "Rainbow Cliffs"),
    # Under Thunder Egg collector in A-zone
    "Rainbow Scale 25":
        LocData(0x8750368, "Rainbow Cliffs"),
}

opals_dict = {
    "Two Up - Opal 1": LocData(0x8754350, "Two Up"),
    "Two Up - Opal 2": LocData(0x8754351, "Two Up"),
    "Two Up - Opal 3": LocData(0x8754352, "Two Up"),
    "Two Up - Opal 4": LocData(0x8754353, "Two Up"),
    "Two Up - Opal 5": LocData(0x8754354, "Two Up"),
    "Two Up - Opal 6": LocData(0x8754355, "Two Up"),
    "Two Up - Opal 7": LocData(0x8754356, "Two Up"),
    "Two Up - Opal 8": LocData(0x8754357, "Two Up"),
    "Two Up - Opal 9": LocData(0x8754358, "Two Up"),
    "Two Up - Opal 10": LocData(0x8754359, "Two Up"),
    "Two Up - Opal 11": LocData(0x875435A, "Two Up"),
    "Two Up - Opal 12": LocData(0x875435B, "Two Up"),
    "Two Up - Opal 13": LocData(0x875435C, "Two Up"),
    "Two Up - Opal 14": LocData(0x875435D, "Two Up"),
    "Two Up - Opal 15": LocData(0x875435E, "Two Up"),
    "Two Up - Opal 16": LocData(0x875435F, "Two Up"),
    "Two Up - Opal 17": LocData(0x8754360, "Two Up"),
    "Two Up - Opal 18": LocData(0x8754361, "Two Up"),
    "Two Up - Opal 19": LocData(0x8754362, "Two Up"),
    "Two Up - Opal 20": LocData(0x8754363, "Two Up"),
    "Two Up - Opal 21": LocData(0x8754364, "Two Up"),
    "Two Up - Opal 22": LocData(0x8754365, "Two Up"),
    "Two Up - Opal 23": LocData(0x8754366, "Two Up"),
    "Two Up - Opal 24": LocData(0x8754367, "Two Up"),
    "Two Up - Opal 25": LocData(0x8754368, "Two Up"),
    "Two Up - Opal 26": LocData(0x8754369, "Two Up"),
    "Two Up - Opal 27": LocData(0x875436A, "Two Up"),
    "Two Up - Opal 28": LocData(0x875436B, "Two Up"),
    "Two Up - Opal 29": LocData(0x875436C, "Two Up"),
    "Two Up - Opal 30": LocData(0x875436D, "Two Up"),
    "Two Up - Opal 31": LocData(0x875436E, "Two Up"),
    "Two Up - Opal 32": LocData(0x875436F, "Two Up"),
    "Two Up - Opal 33": LocData(0x8754370, "Two Up"),
    "Two Up - Opal 34": LocData(0x8754371, "Two Up"),
    "Two Up - Opal 35": LocData(0x8754372, "Two Up"),
    "Two Up - Opal 36": LocData(0x8754373, "Two Up"),
    "Two Up - Opal 37": LocData(0x8754374, "Two Up"),
    "Two Up - Opal 38": LocData(0x8754375, "Two Up"),
    "Two Up - Opal 39": LocData(0x8754376, "Two Up"),
    "Two Up - Opal 40": LocData(0x8754377, "Two Up"),
    "Two Up - Opal 41": LocData(0x8754378, "Two Up"),
    "Two Up - Opal 42": LocData(0x8754379, "Two Up"),
    "Two Up - Opal 43": LocData(0x875437A, "Two Up"),
    "Two Up - Opal 44": LocData(0x875437B, "Two Up"),
    "Two Up - Opal 45": LocData(0x875437C, "Two Up"),
    "Two Up - Opal 46": LocData(0x875437D, "Two Up"),
    "Two Up - Opal 47": LocData(0x875437E, "Two Up"),
    "Two Up - Opal 48": LocData(0x875437F, "Two Up"),
    "Two Up - Opal 49": LocData(0x8754380, "Two Up"),
    "Two Up - Opal 50": LocData(0x8754381, "Two Up"),
    "Two Up - Opal 51": LocData(0x8754382, "Two Up"),
    "Two Up - Opal 52": LocData(0x8754383, "Two Up"),
    "Two Up - Opal 53": LocData(0x8754384, "Two Up"),
    "Two Up - Opal 54": LocData(0x8754385, "Two Up"),
    "Two Up - Opal 55": LocData(0x8754386, "Two Up"),
    "Two Up - Opal 56": LocData(0x8754387, "Two Up"),
    "Two Up - Opal 57": LocData(0x8754388, "Two Up"),
    "Two Up - Opal 58": LocData(0x8754389, "Two Up"),
    "Two Up - Opal 59": LocData(0x875438A, "Two Up"),
    "Two Up - Opal 60": LocData(0x875438B, "Two Up"),
    "Two Up - Opal 61": LocData(0x875438C, "Two Up"),
    "Two Up - Opal 62": LocData(0x875438D, "Two Up"),
    "Two Up - Opal 63": LocData(0x875438E, "Two Up"),
    "Two Up - Opal 64": LocData(0x875438F, "Two Up"),
    "Two Up - Opal 65": LocData(0x8754390, "Two Up"),
    "Two Up - Opal 66": LocData(0x8754391, "Two Up"),
    "Two Up - Opal 67": LocData(0x8754392, "Two Up"),
    "Two Up - Opal 68": LocData(0x8754393, "Two Up"),
    "Two Up - Opal 69": LocData(0x8754394, "Two Up"),
    "Two Up - Opal 70": LocData(0x8754395, "Two Up"),
    "Two Up - Opal 71": LocData(0x8754396, "Two Up"),
    "Two Up - Opal 72": LocData(0x8754397, "Two Up"),
    "Two Up - Opal 73": LocData(0x8754398, "Two Up"),
    "Two Up - Opal 74": LocData(0x8754399, "Two Up"),
    "Two Up - Opal 75": LocData(0x875439A, "Two Up"),
    "Two Up - Opal 76": LocData(0x875439B, "Two Up"),
    "Two Up - Opal 77": LocData(0x875439C, "Two Up"),
    "Two Up - Opal 78": LocData(0x875439D, "Two Up"),
    "Two Up - Opal 79": LocData(0x875439E, "Two Up"),
    "Two Up - Opal 80": LocData(0x875439F, "Two Up"),
    "Two Up - Opal 81": LocData(0x87543A0, "Two Up"),
    "Two Up - Opal 82": LocData(0x87543A1, "Two Up"),
    "Two Up - Opal 83": LocData(0x87543A2, "Two Up"),
    "Two Up - Opal 84": LocData(0x87543A3, "Two Up"),
    "Two Up - Opal 85": LocData(0x87543A4, "Two Up"),
    "Two Up - Opal 86": LocData(0x87543A5, "Two Up"),
    "Two Up - Opal 87": LocData(0x87543A6, "Two Up"),
    "Two Up - Opal 88": LocData(0x87543A7, "Two Up"),
    "Two Up - Opal 89": LocData(0x87543A8, "Two Up"),
    "Two Up - Opal 90": LocData(0x87543A9, "Two Up"),
    "Two Up - Opal 91": LocData(0x87543AA, "Two Up"),
    "Two Up - Opal 92": LocData(0x87543AB, "Two Up"),
    "Two Up - Opal 93": LocData(0x87543AC, "Two Up"),
    "Two Up - Opal 94": LocData(0x87543AD, "Two Up"),
    "Two Up - Opal 95": LocData(0x87543AE, "Two Up"),
    "Two Up - Opal 96": LocData(0x87543AF, "Two Up"),
    "Two Up - Opal 97": LocData(0x87543B0, "Two Up"),
    "Two Up - Opal 98": LocData(0x87543B1, "Two Up"),
    "Two Up - Opal 99": LocData(0x87543B2, "Two Up"),
    "Two Up - Opal 100": LocData(0x87543B3, "Two Up"),
    "Two Up - Opal 101": LocData(0x87543B4, "Two Up"),
    "Two Up - Opal 102": LocData(0x87543B5, "Two Up"),
    "Two Up - Opal 103": LocData(0x87543B6, "Two Up"),
    "Two Up - Opal 104": LocData(0x87543B7, "Two Up"),
    "Two Up - Opal 105": LocData(0x87543B8, "Two Up"),
    "Two Up - Opal 106": LocData(0x87543B9, "Two Up"),
    "Two Up - Opal 107": LocData(0x87543BA, "Two Up"),
    "Two Up - Opal 108": LocData(0x87543BB, "Two Up"),
    "Two Up - Opal 109": LocData(0x87543BC, "Two Up"),
    "Two Up - Opal 110": LocData(0x87543BD, "Two Up"),
    "Two Up - Opal 111": LocData(0x87543BE, "Two Up"),
    "Two Up - Opal 112": LocData(0x87543BF, "Two Up"),
    "Two Up - Opal 113": LocData(0x87543C0, "Two Up"),
    "Two Up - Opal 114": LocData(0x87543C1, "Two Up"),
    "Two Up - Opal 115": LocData(0x87543C2, "Two Up"),
    "Two Up - Opal 116": LocData(0x87543C3, "Two Up"),
    "Two Up - Opal 117": LocData(0x87543C4, "Two Up - Upper Area"),
    "Two Up - Opal 118": LocData(0x87543C5, "Two Up - Upper Area"),
    "Two Up - Opal 119": LocData(0x87543C6, "Two Up - Upper Area"),
    "Two Up - Opal 120": LocData(0x87543C7, "Two Up - Upper Area"),
    "Two Up - Opal 121": LocData(0x87543C8, "Two Up - Upper Area"),
    "Two Up - Opal 122": LocData(0x87543C9, "Two Up - Upper Area"),
    "Two Up - Opal 123": LocData(0x87543CA, "Two Up - Upper Area"),
    "Two Up - Opal 124": LocData(0x87543CB, "Two Up - Upper Area"),
    "Two Up - Opal 125": LocData(0x87543CC, "Two Up - Upper Area"),
    "Two Up - Opal 126": LocData(0x87543CD, "Two Up - Upper Area"),
    "Two Up - Opal 127": LocData(0x87543CE, "Two Up - Upper Area"),
    "Two Up - Opal 128": LocData(0x87543CF, "Two Up - Upper Area"),
    "Two Up - Opal 129": LocData(0x87543D0, "Two Up - Upper Area"),
    "Two Up - Opal 130": LocData(0x87543D1, "Two Up - Upper Area"),
    "Two Up - Opal 131": LocData(0x87543D2, "Two Up"),
    "Two Up - Opal 132": LocData(0x87543D3, "Two Up"),
    "Two Up - Opal 133": LocData(0x87543D4, "Two Up"),
    "Two Up - Opal 134": LocData(0x87543D5, "Two Up"),
    "Two Up - Opal 135": LocData(0x87543D6, "Two Up"),
    "Two Up - Opal 136": LocData(0x87543D7, "Two Up"),
    "Two Up - Opal 137": LocData(0x87543D8, "Two Up"),
    "Two Up - Opal 138": LocData(0x87543D9, "Two Up"),
    "Two Up - Opal 139": LocData(0x87543DA, "Two Up"),
    "Two Up - Opal 140": LocData(0x87543DB, "Two Up"),
    "Two Up - Opal 141": LocData(0x87543DC, "Two Up"),
    "Two Up - Opal 142": LocData(0x87543DD, "Two Up"),
    "Two Up - Opal 143": LocData(0x87543DE, "Two Up"),
    "Two Up - Opal 144": LocData(0x87543DF, "Two Up"),
    "Two Up - Opal 145": LocData(0x87543E0, "Two Up"),
    "Two Up - Opal 146": LocData(0x87543E1, "Two Up"),
    "Two Up - Opal 147": LocData(0x87543E2, "Two Up"),
    "Two Up - Opal 148": LocData(0x87543E3, "Two Up"),
    "Two Up - Opal 149": LocData(0x87543E4, "Two Up"),
    "Two Up - Opal 150": LocData(0x87543E5, "Two Up"),
    "Two Up - Opal 151": LocData(0x87543E6, "Two Up"),
    "Two Up - Opal 152": LocData(0x87543E7, "Two Up"),
    "Two Up - Opal 153": LocData(0x87543E8, "Two Up"),
    "Two Up - Opal 154": LocData(0x87543E9, "Two Up"),
    "Two Up - Opal 155": LocData(0x87543EA, "Two Up"),
    "Two Up - Opal 156": LocData(0x87543EB, "Two Up"),
    "Two Up - Opal 157": LocData(0x87543EC, "Two Up"),
    "Two Up - Opal 158": LocData(0x87543ED, "Two Up - Upper Area"),
    "Two Up - Opal 159": LocData(0x87543EE, "Two Up - Upper Area"),
    "Two Up - Opal 160": LocData(0x87543EF, "Two Up - Upper Area"),
    "Two Up - Opal 161": LocData(0x87543F0, "Two Up - Upper Area"),
    "Two Up - Opal 162": LocData(0x87543F1, "Two Up - Upper Area"),
    "Two Up - Opal 163": LocData(0x87543F2, "Two Up - Upper Area"),
    "Two Up - Opal 164": LocData(0x87543F3, "Two Up - Upper Area"),
    "Two Up - Opal 165": LocData(0x87543F4, "Two Up - Upper Area"),
    "Two Up - Opal 166": LocData(0x87543F5, "Two Up - Upper Area"),
    "Two Up - Opal 167": LocData(0x87543F6, "Two Up - Upper Area"),
    "Two Up - Opal 168": LocData(0x87543F7, "Two Up"),
    "Two Up - Opal 169": LocData(0x87543F8, "Two Up"),
    "Two Up - Opal 170": LocData(0x87543F9, "Two Up"),
    "Two Up - Opal 171": LocData(0x87543FA, "Two Up"),
    "Two Up - Opal 172": LocData(0x87543FB, "Two Up"),
    "Two Up - Opal 173": LocData(0x87543FC, "Two Up"),
    "Two Up - Opal 174": LocData(0x87543FD, "Two Up"),
    "Two Up - Opal 175": LocData(0x87543FE, "Two Up"),
    "Two Up - Opal 176": LocData(0x87543FF, "Two Up"),
    "Two Up - Opal 177": LocData(0x8754400, "Two Up"),
    "Two Up - Opal 178": LocData(0x8754401, "Two Up"),
    "Two Up - Opal 179": LocData(0x8754402, "Two Up"),
    "Two Up - Opal 180": LocData(0x8754403, "Two Up"),
    "Two Up - Opal 181": LocData(0x8754404, "Two Up"),
    "Two Up - Opal 182": LocData(0x8754405, "Two Up"),
    "Two Up - Opal 183": LocData(0x8754406, "Two Up"),
    "Two Up - Opal 184": LocData(0x8754407, "Two Up"),
    "Two Up - Opal 185": LocData(0x8754408, "Two Up"),
    "Two Up - Opal 186": LocData(0x8754409, "Two Up"),
    "Two Up - Opal 187": LocData(0x875440A, "Two Up"),
    "Two Up - Opal 188": LocData(0x875440B, "Two Up"),
    "Two Up - Opal 189": LocData(0x875440C, "Two Up"),
    "Two Up - Opal 190": LocData(0x875440D, "Two Up"),
    "Two Up - Opal 191": LocData(0x875440E, "Two Up"),
    "Two Up - Opal 192": LocData(0x875440F, "Two Up"),
    "Two Up - Opal 193": LocData(0x8754410, "Two Up"),
    "Two Up - Opal 194": LocData(0x8754411, "Two Up"),
    "Two Up - Opal 195": LocData(0x8754412, "Two Up"),
    "Two Up - Opal 196": LocData(0x8754413, "Two Up"),
    "Two Up - Opal 197": LocData(0x8754414, "Two Up"),
    "Two Up - Opal 198": LocData(0x8754415, "Two Up"),
    "Two Up - Opal 199": LocData(0x8754416, "Two Up"),
    "Two Up - Opal 200": LocData(0x8754417, "Two Up"),
    "Two Up - Opal 201": LocData(0x8754418, "Two Up"),
    "Two Up - Opal 202": LocData(0x8754419, "Two Up"),
    "Two Up - Opal 203": LocData(0x875441A, "Two Up"),
    "Two Up - Opal 204": LocData(0x875441B, "Two Up"),
    "Two Up - Opal 205": LocData(0x875441C, "Two Up"),
    "Two Up - Opal 206": LocData(0x875441D, "Two Up"),
    "Two Up - Opal 207": LocData(0x875441E, "Two Up"),
    "Two Up - Opal 208": LocData(0x875441F, "Two Up"),
    "Two Up - Opal 209": LocData(0x8754420, "Two Up"),
    "Two Up - Opal 210": LocData(0x8754421, "Two Up"),
    "Two Up - Opal 211": LocData(0x8754422, "Two Up"),
    "Two Up - Opal 212": LocData(0x8754423, "Two Up"),
    "Two Up - Opal 213": LocData(0x8754424, "Two Up"),
    "Two Up - Opal 214": LocData(0x8754425, "Two Up"),
    "Two Up - Opal 215": LocData(0x8754426, "Two Up"),
    "Two Up - Opal 216": LocData(0x8754427, "Two Up"),
    "Two Up - Opal 217": LocData(0x8754428, "Two Up"),
    "Two Up - Opal 218": LocData(0x8754429, "Two Up"),
    "Two Up - Opal 219": LocData(0x875442A, "Two Up"),
    "Two Up - Opal 220": LocData(0x875442B, "Two Up"),
    "Two Up - Opal 221": LocData(0x875442C, "Two Up"),
    "Two Up - Opal 222": LocData(0x875442D, "Two Up"),
    "Two Up - Opal 223": LocData(0x875442E, "Two Up"),
    "Two Up - Opal 224": LocData(0x875442F, "Two Up"),
    "Two Up - Opal 225": LocData(0x8754430, "Two Up"),
    "Two Up - Opal 226": LocData(0x8754431, "Two Up"),
    "Two Up - Opal 227": LocData(0x8754432, "Two Up"),
    "Two Up - Opal 228": LocData(0x8754433, "Two Up"),
    "Two Up - Opal 229": LocData(0x8754434, "Two Up"),
    "Two Up - Opal 230": LocData(0x8754435, "Two Up"),
    "Two Up - Opal 231": LocData(0x8754436, "Two Up"),
    "Two Up - Opal 232": LocData(0x8754437, "Two Up"),
    "Two Up - Opal 233": LocData(0x8754438, "Two Up"),
    "Two Up - Opal 234": LocData(0x8754439, "Two Up"),
    "Two Up - Opal 235": LocData(0x875443A, "Two Up"),
    "Two Up - Opal 236": LocData(0x875443B, "Two Up"),
    "Two Up - Opal 237": LocData(0x875443C, "Two Up"),
    "Two Up - Opal 238": LocData(0x875443D, "Two Up"),
    "Two Up - Opal 239": LocData(0x875443E, "Two Up"),
    "Two Up - Opal 240": LocData(0x875443F, "Two Up"),
    "Two Up - Opal 241": LocData(0x8754440, "Two Up"),
    "Two Up - Opal 242": LocData(0x8754441, "Two Up"),
    "Two Up - Opal 243": LocData(0x8754442, "Two Up"),
    "Two Up - Opal 244": LocData(0x8754443, "Two Up"),
    "Two Up - Opal 245": LocData(0x8754444, "Two Up"),
    "Two Up - Opal 246": LocData(0x8754445, "Two Up"),
    "Two Up - Opal 247": LocData(0x8754446, "Two Up"),
    "Two Up - Opal 248": LocData(0x8754447, "Two Up"),
    "Two Up - Opal 249": LocData(0x8754448, "Two Up"),
    "Two Up - Opal 250": LocData(0x8754449, "Two Up"),
    "Two Up - Opal 251": LocData(0x875444A, "Two Up"),
    "Two Up - Opal 252": LocData(0x875444B, "Two Up"),
    "Two Up - Opal 253": LocData(0x875444C, "Two Up"),
    "Two Up - Opal 254": LocData(0x875444D, "Two Up"),
    "Two Up - Opal 255": LocData(0x875444E, "Two Up"),
    "Two Up - Opal 256": LocData(0x875444F, "Two Up"),
    "Two Up - Opal 257": LocData(0x8754450, "Two Up"),
    "Two Up - Opal 258": LocData(0x8754451, "Two Up"),
    "Two Up - Opal 259": LocData(0x8754452, "Two Up"),
    "Two Up - Opal 260": LocData(0x8754453, "Two Up"),
    "Two Up - Opal 261": LocData(0x8754454, "Two Up"),
    "Two Up - Opal 262": LocData(0x8754455, "Two Up"),
    "Two Up - Opal 263": LocData(0x8754456, "Two Up"),
    "Two Up - Opal 264": LocData(0x8754457, "Two Up"),
    "Two Up - Opal 265": LocData(0x8754458, "Two Up"),
    "Two Up - Opal 266": LocData(0x8754459, "Two Up"),
    "Two Up - Opal 267": LocData(0x875445A, "Two Up"),
    "Two Up - Opal 268": LocData(0x875445B, "Two Up"),
    "Two Up - Opal 269": LocData(0x875445C, "Two Up"),
    "Two Up - Opal 270": LocData(0x875445D, "Two Up"),
    "Two Up - Opal 271": LocData(0x875445E, "Two Up"),
    "Two Up - Opal 272": LocData(0x875445F, "Two Up"),
    "Two Up - Opal 273": LocData(0x8754460, "Two Up"),
    "Two Up - Opal 274": LocData(0x8754461, "Two Up"),
    "Two Up - Opal 275": LocData(0x8754462, "Two Up"),
    "Two Up - Opal 276": LocData(0x8754463, "Two Up"),
    "Two Up - Opal 277": LocData(0x8754464, "Two Up"),
    "Two Up - Opal 278": LocData(0x8754465, "Two Up"),
    "Two Up - Opal 279": LocData(0x8754466, "Two Up"),
    "Two Up - Opal 280": LocData(0x8754467, "Two Up"),
    "Two Up - Opal 281": LocData(0x8754468, "Two Up"),
    "Two Up - Opal 282": LocData(0x8754469, "Two Up"),
    "Two Up - Opal 283": LocData(0x875446A, "Two Up"),
    "Two Up - Opal 284": LocData(0x875446B, "Two Up"),
    "Two Up - Opal 285": LocData(0x875446C, "Two Up"),
    "Two Up - Opal 286": LocData(0x875446D, "Two Up"),
    "Two Up - Opal 287": LocData(0x875446E, "Two Up"),
    "Two Up - Opal 288": LocData(0x875446F, "Two Up"),
    "Two Up - Opal 289": LocData(0x8754470, "Two Up"),
    "Two Up - Opal 290": LocData(0x8754471, "Two Up"),
    "Two Up - Opal 291": LocData(0x8754472, "Two Up"),
    "Two Up - Opal 292": LocData(0x8754473, "Two Up"),
    "Two Up - Opal 293": LocData(0x8754474, "Two Up"),
    "Two Up - Opal 294": LocData(0x8754475, "Two Up"),
    "Two Up - Opal 295": LocData(0x8754476, "Two Up"),
    "Two Up - Opal 296": LocData(0x8754477, "Two Up"),
    "Two Up - Opal 297": LocData(0x8754478, "Two Up"),
    "Two Up - Opal 298": LocData(0x8754479, "Two Up"),
    "Two Up - Opal 299": LocData(0x875447A, "Two Up"),
    "Two Up - Opal 300": LocData(0x875447B, "Two Up"),
    "WitP - Opal 1": LocData(0x8755350, "Walk in the Park"),
    "WitP - Opal 2": LocData(0x8755351, "Walk in the Park"),
    "WitP - Opal 3": LocData(0x8755352, "Walk in the Park"),
    "WitP - Opal 4": LocData(0x8755353, "Walk in the Park"),
    "WitP - Opal 5": LocData(0x8755354, "Walk in the Park"),
    "WitP - Opal 6": LocData(0x8755355, "Walk in the Park"),
    "WitP - Opal 7": LocData(0x8755356, "Walk in the Park"),
    "WitP - Opal 8": LocData(0x8755357, "Walk in the Park"),
    "WitP - Opal 9": LocData(0x8755358, "Walk in the Park"),
    "WitP - Opal 10": LocData(0x8755359, "Walk in the Park"),
    "WitP - Opal 11": LocData(0x875535A, "Walk in the Park"),
    "WitP - Opal 12": LocData(0x875535B, "Walk in the Park"),
    "WitP - Opal 13": LocData(0x875535C, "Walk in the Park"),
    "WitP - Opal 14": LocData(0x875535D, "Walk in the Park"),
    "WitP - Opal 15": LocData(0x875535E, "Walk in the Park"),
    "WitP - Opal 16": LocData(0x875535F, "Walk in the Park"),
    "WitP - Opal 17": LocData(0x8755360, "Walk in the Park"),
    "WitP - Opal 18": LocData(0x8755361, "Walk in the Park"),
    "WitP - Opal 19": LocData(0x8755362, "Walk in the Park"),
    "WitP - Opal 20": LocData(0x8755363, "Walk in the Park"),
    "WitP - Opal 21": LocData(0x8755364, "Walk in the Park"),
    "WitP - Opal 22": LocData(0x8755365, "Walk in the Park"),
    "WitP - Opal 23": LocData(0x8755366, "Walk in the Park"),
    "WitP - Opal 24": LocData(0x8755367, "Walk in the Park"),
    "WitP - Opal 25": LocData(0x8755368, "Walk in the Park"),
    "WitP - Opal 26": LocData(0x8755369, "Walk in the Park"),
    "WitP - Opal 27": LocData(0x875536A, "Walk in the Park"),
    "WitP - Opal 28": LocData(0x875536B, "Walk in the Park"),
    "WitP - Opal 29": LocData(0x875536C, "Walk in the Park"),
    "WitP - Opal 30": LocData(0x875536D, "Walk in the Park"),
    "WitP - Opal 31": LocData(0x875536E, "Walk in the Park"),
    "WitP - Opal 32": LocData(0x875536F, "Walk in the Park"),
    "WitP - Opal 33": LocData(0x8755370, "Walk in the Park"),
    "WitP - Opal 34": LocData(0x8755371, "Walk in the Park"),
    "WitP - Opal 35": LocData(0x8755372, "Walk in the Park"),
    "WitP - Opal 36": LocData(0x8755373, "Walk in the Park"),
    "WitP - Opal 37": LocData(0x8755374, "Walk in the Park"),
    "WitP - Opal 38": LocData(0x8755375, "Walk in the Park"),
    "WitP - Opal 39": LocData(0x8755376, "Walk in the Park"),
    "WitP - Opal 40": LocData(0x8755377, "Walk in the Park"),
    "WitP - Opal 41": LocData(0x8755378, "Walk in the Park"),
    "WitP - Opal 42": LocData(0x8755379, "Walk in the Park"),
    "WitP - Opal 43": LocData(0x875537A, "Walk in the Park"),
    "WitP - Opal 44": LocData(0x875537B, "Walk in the Park"),
    "WitP - Opal 45": LocData(0x875537C, "Walk in the Park"),
    "WitP - Opal 46": LocData(0x875537D, "Walk in the Park"),
    "WitP - Opal 47": LocData(0x875537E, "Walk in the Park"),
    "WitP - Opal 48": LocData(0x875537F, "Walk in the Park"),
    "WitP - Opal 49": LocData(0x8755380, "Walk in the Park"),
    "WitP - Opal 50": LocData(0x8755381, "Walk in the Park"),
    "WitP - Opal 51": LocData(0x8755382, "Walk in the Park"),
    "WitP - Opal 52": LocData(0x8755383, "Walk in the Park"),
    "WitP - Opal 53": LocData(0x8755384, "Walk in the Park"),
    "WitP - Opal 54": LocData(0x8755385, "Walk in the Park"),
    "WitP - Opal 55": LocData(0x8755386, "Walk in the Park"),
    "WitP - Opal 56": LocData(0x8755387, "Walk in the Park"),
    "WitP - Opal 57": LocData(0x8755388, "Walk in the Park"),
    "WitP - Opal 58": LocData(0x8755389, "Walk in the Park"),
    "WitP - Opal 59": LocData(0x875538A, "Walk in the Park"),
    "WitP - Opal 60": LocData(0x875538B, "Walk in the Park"),
    "WitP - Opal 61": LocData(0x875538C, "Walk in the Park"),
    "WitP - Opal 62": LocData(0x875538D, "Walk in the Park"),
    "WitP - Opal 63": LocData(0x875538E, "Walk in the Park"),
    "WitP - Opal 64": LocData(0x875538F, "Walk in the Park"),
    "WitP - Opal 65": LocData(0x8755390, "Walk in the Park"),
    "WitP - Opal 66": LocData(0x8755391, "Walk in the Park"),
    "WitP - Opal 67": LocData(0x8755392, "Walk in the Park"),
    "WitP - Opal 68": LocData(0x8755393, "Walk in the Park"),
    "WitP - Opal 69": LocData(0x8755394, "Walk in the Park"),
    "WitP - Opal 70": LocData(0x8755395, "Walk in the Park"),
    "WitP - Opal 71": LocData(0x8755396, "Walk in the Park"),
    "WitP - Opal 72": LocData(0x8755397, "Walk in the Park"),
    "WitP - Opal 73": LocData(0x8755398, "Walk in the Park"),
    "WitP - Opal 74": LocData(0x8755399, "Walk in the Park"),
    "WitP - Opal 75": LocData(0x875539A, "Walk in the Park"),
    "WitP - Opal 76": LocData(0x875539B, "Walk in the Park"),
    "WitP - Opal 77": LocData(0x875539C, "Walk in the Park"),
    "WitP - Opal 78": LocData(0x875539D, "Walk in the Park"),
    "WitP - Opal 79": LocData(0x875539E, "Walk in the Park"),
    "WitP - Opal 80": LocData(0x875539F, "Walk in the Park"),
    "WitP - Opal 81": LocData(0x87553A0, "Walk in the Park"),
    "WitP - Opal 82": LocData(0x87553A1, "Walk in the Park"),
    "WitP - Opal 83": LocData(0x87553A2, "Walk in the Park"),
    "WitP - Opal 84": LocData(0x87553A3, "Walk in the Park"),
    "WitP - Opal 85": LocData(0x87553A4, "Walk in the Park"),
    "WitP - Opal 86": LocData(0x87553A5, "Walk in the Park"),
    "WitP - Opal 87": LocData(0x87553A6, "Walk in the Park"),
    "WitP - Opal 88": LocData(0x87553A7, "Walk in the Park"),
    "WitP - Opal 89": LocData(0x87553A8, "Walk in the Park"),
    "WitP - Opal 90": LocData(0x87553A9, "Walk in the Park"),
    "WitP - Opal 91": LocData(0x87553AA, "Walk in the Park"),
    "WitP - Opal 92": LocData(0x87553AB, "Walk in the Park"),
    "WitP - Opal 93": LocData(0x87553AC, "Walk in the Park"),
    "WitP - Opal 94": LocData(0x87553AD, "Walk in the Park"),
    "WitP - Opal 95": LocData(0x87553AE, "Walk in the Park"),
    "WitP - Opal 96": LocData(0x87553AF, "Walk in the Park"),
    "WitP - Opal 97": LocData(0x87553B0, "Walk in the Park"),
    "WitP - Opal 98": LocData(0x87553B1, "Walk in the Park"),
    "WitP - Opal 99": LocData(0x87553B2, "Walk in the Park"),
    "WitP - Opal 100": LocData(0x87553B3, "Walk in the Park"),
    "WitP - Opal 101": LocData(0x87553B4, "Walk in the Park"),
    "WitP - Opal 102": LocData(0x87553B5, "Walk in the Park"),
    "WitP - Opal 103": LocData(0x87553B6, "Walk in the Park"),
    "WitP - Opal 104": LocData(0x87553B7, "Walk in the Park"),
    "WitP - Opal 105": LocData(0x87553B8, "Walk in the Park"),
    "WitP - Opal 106": LocData(0x87553B9, "Walk in the Park"),
    "WitP - Opal 107": LocData(0x87553BA, "Walk in the Park"),
    "WitP - Opal 108": LocData(0x87553BB, "Walk in the Park"),
    "WitP - Opal 109": LocData(0x87553BC, "Walk in the Park"),
    "WitP - Opal 110": LocData(0x87553BD, "Walk in the Park"),
    "WitP - Opal 111": LocData(0x87553BE, "Walk in the Park"),
    "WitP - Opal 112": LocData(0x87553BF, "Walk in the Park"),
    "WitP - Opal 113": LocData(0x87553C0, "Walk in the Park"),
    "WitP - Opal 114": LocData(0x87553C1, "Walk in the Park"),
    "WitP - Opal 115": LocData(0x87553C2, "Walk in the Park"),
    "WitP - Opal 116": LocData(0x87553C3, "Walk in the Park"),
    "WitP - Opal 117": LocData(0x87553C4, "Walk in the Park"),
    "WitP - Opal 118": LocData(0x87553C5, "Walk in the Park"),
    "WitP - Opal 119": LocData(0x87553C6, "Walk in the Park"),
    "WitP - Opal 120": LocData(0x87553C7, "Walk in the Park"),
    "WitP - Opal 121": LocData(0x87553C8, "Walk in the Park"),
    "WitP - Opal 122": LocData(0x87553C9, "Walk in the Park"),
    "WitP - Opal 123": LocData(0x87553CA, "Walk in the Park"),
    "WitP - Opal 124": LocData(0x87553CB, "Walk in the Park"),
    "WitP - Opal 125": LocData(0x87553CC, "Walk in the Park"),
    "WitP - Opal 126": LocData(0x87553CD, "Walk in the Park"),
    "WitP - Opal 127": LocData(0x87553CE, "Walk in the Park"),
    "WitP - Opal 128": LocData(0x87553CF, "Walk in the Park"),
    "WitP - Opal 129": LocData(0x87553D0, "Walk in the Park"),
    "WitP - Opal 130": LocData(0x87553D1, "Walk in the Park"),
    "WitP - Opal 131": LocData(0x87553D2, "Walk in the Park"),
    "WitP - Opal 132": LocData(0x87553D3, "Walk in the Park"),
    "WitP - Opal 133": LocData(0x87553D4, "Walk in the Park"),
    "WitP - Opal 134": LocData(0x87553D5, "Walk in the Park"),
    "WitP - Opal 135": LocData(0x87553D6, "Walk in the Park"),
    "WitP - Opal 136": LocData(0x87553D7, "Walk in the Park"),
    "WitP - Opal 137": LocData(0x87553D8, "Walk in the Park"),
    "WitP - Opal 138": LocData(0x87553D9, "Walk in the Park"),
    "WitP - Opal 139": LocData(0x87553DA, "Walk in the Park"),
    "WitP - Opal 140": LocData(0x87553DB, "Walk in the Park"),
    "WitP - Opal 141": LocData(0x87553DC, "Walk in the Park"),
    "WitP - Opal 142": LocData(0x87553DD, "Walk in the Park"),
    "WitP - Opal 143": LocData(0x87553DE, "Walk in the Park"),
    "WitP - Opal 144": LocData(0x87553DF, "Walk in the Park"),
    "WitP - Opal 145": LocData(0x87553E0, "Walk in the Park"),
    "WitP - Opal 146": LocData(0x87553E1, "Walk in the Park"),
    "WitP - Opal 147": LocData(0x87553E2, "Walk in the Park"),
    "WitP - Opal 148": LocData(0x87553E3, "Walk in the Park"),
    "WitP - Opal 149": LocData(0x87553E4, "Walk in the Park"),
    "WitP - Opal 150": LocData(0x87553E5, "Walk in the Park"),
    "WitP - Opal 151": LocData(0x87553E6, "Walk in the Park"),
    "WitP - Opal 152": LocData(0x87553E7, "Walk in the Park"),
    "WitP - Opal 153": LocData(0x87553E8, "Walk in the Park"),
    "WitP - Opal 154": LocData(0x87553E9, "Walk in the Park"),
    "WitP - Opal 155": LocData(0x87553EA, "Walk in the Park"),
    "WitP - Opal 156": LocData(0x87553EB, "Walk in the Park"),
    "WitP - Opal 157": LocData(0x87553EC, "Walk in the Park"),
    "WitP - Opal 158": LocData(0x87553ED, "Walk in the Park"),
    "WitP - Opal 159": LocData(0x87553EE, "Walk in the Park"),
    "WitP - Opal 160": LocData(0x87553EF, "Walk in the Park"),
    "WitP - Opal 161": LocData(0x87553F0, "Walk in the Park"),
    "WitP - Opal 162": LocData(0x87553F1, "Walk in the Park"),
    "WitP - Opal 163": LocData(0x87553F2, "Walk in the Park"),
    "WitP - Opal 164": LocData(0x87553F3, "Walk in the Park"),
    "WitP - Opal 165": LocData(0x87553F4, "Walk in the Park"),
    "WitP - Opal 166": LocData(0x87553F5, "Walk in the Park"),
    "WitP - Opal 167": LocData(0x87553F6, "Walk in the Park"),
    "WitP - Opal 168": LocData(0x87553F7, "Walk in the Park"),
    "WitP - Opal 169": LocData(0x87553F8, "Walk in the Park"),
    "WitP - Opal 170": LocData(0x87553F9, "Walk in the Park"),
    "WitP - Opal 171": LocData(0x87553FA, "Walk in the Park"),
    "WitP - Opal 172": LocData(0x87553FB, "Walk in the Park"),
    "WitP - Opal 173": LocData(0x87553FC, "Walk in the Park"),
    "WitP - Opal 174": LocData(0x87553FD, "Walk in the Park"),
    "WitP - Opal 175": LocData(0x87553FE, "Walk in the Park"),
    "WitP - Opal 176": LocData(0x87553FF, "Walk in the Park"),
    "WitP - Opal 177": LocData(0x8755400, "Walk in the Park"),
    "WitP - Opal 178": LocData(0x8755401, "Walk in the Park"),
    "WitP - Opal 179": LocData(0x8755402, "Walk in the Park"),
    "WitP - Opal 180": LocData(0x8755403, "Walk in the Park"),
    "WitP - Opal 181": LocData(0x8755404, "Walk in the Park"),
    "WitP - Opal 182": LocData(0x8755405, "Walk in the Park"),
    "WitP - Opal 183": LocData(0x8755406, "Walk in the Park"),
    "WitP - Opal 184": LocData(0x8755407, "Walk in the Park"),
    "WitP - Opal 185": LocData(0x8755408, "Walk in the Park"),
    "WitP - Opal 186": LocData(0x8755409, "Walk in the Park"),
    "WitP - Opal 187": LocData(0x875540A, "Walk in the Park"),
    "WitP - Opal 188": LocData(0x875540B, "Walk in the Park"),
    "WitP - Opal 189": LocData(0x875540C, "Walk in the Park"),
    "WitP - Opal 190": LocData(0x875540D, "Walk in the Park"),
    "WitP - Opal 191": LocData(0x875540E, "Walk in the Park"),
    "WitP - Opal 192": LocData(0x875540F, "Walk in the Park"),
    "WitP - Opal 193": LocData(0x8755410, "Walk in the Park"),
    "WitP - Opal 194": LocData(0x8755411, "Walk in the Park"),
    "WitP - Opal 195": LocData(0x8755412, "Walk in the Park"),
    "WitP - Opal 196": LocData(0x8755413, "Walk in the Park"),
    "WitP - Opal 197": LocData(0x8755414, "Walk in the Park"),
    "WitP - Opal 198": LocData(0x8755415, "Walk in the Park"),
    "WitP - Opal 199": LocData(0x8755416, "Walk in the Park"),
    "WitP - Opal 200": LocData(0x8755417, "Walk in the Park"),
    "WitP - Opal 201": LocData(0x8755418, "Walk in the Park"),
    "WitP - Opal 202": LocData(0x8755419, "Walk in the Park"),
    "WitP - Opal 203": LocData(0x875541A, "Walk in the Park"),
    "WitP - Opal 204": LocData(0x875541B, "Walk in the Park"),
    "WitP - Opal 205": LocData(0x875541C, "Walk in the Park"),
    "WitP - Opal 206": LocData(0x875541D, "Walk in the Park"),
    "WitP - Opal 207": LocData(0x875541E, "Walk in the Park"),
    "WitP - Opal 208": LocData(0x875541F, "Walk in the Park"),
    "WitP - Opal 209": LocData(0x8755420, "Walk in the Park"),
    "WitP - Opal 210": LocData(0x8755421, "Walk in the Park"),
    "WitP - Opal 211": LocData(0x8755422, "Walk in the Park"),
    "WitP - Opal 212": LocData(0x8755423, "Walk in the Park"),
    "WitP - Opal 213": LocData(0x8755424, "Walk in the Park"),
    "WitP - Opal 214": LocData(0x8755425, "Walk in the Park"),
    "WitP - Opal 215": LocData(0x8755426, "Walk in the Park"),
    "WitP - Opal 216": LocData(0x8755427, "Walk in the Park"),
    "WitP - Opal 217": LocData(0x8755428, "Walk in the Park"),
    "WitP - Opal 218": LocData(0x8755429, "Walk in the Park"),
    "WitP - Opal 219": LocData(0x875542A, "Walk in the Park"),
    "WitP - Opal 220": LocData(0x875542B, "Walk in the Park"),
    "WitP - Opal 221": LocData(0x875542C, "Walk in the Park"),
    "WitP - Opal 222": LocData(0x875542D, "Walk in the Park"),
    "WitP - Opal 223": LocData(0x875542E, "Walk in the Park"),
    "WitP - Opal 224": LocData(0x875542F, "Walk in the Park"),
    "WitP - Opal 225": LocData(0x8755430, "Walk in the Park"),
    "WitP - Opal 226": LocData(0x8755431, "Walk in the Park"),
    "WitP - Opal 227": LocData(0x8755432, "Walk in the Park"),
    "WitP - Opal 228": LocData(0x8755433, "Walk in the Park"),
    "WitP - Opal 229": LocData(0x8755434, "Walk in the Park"),
    "WitP - Opal 230": LocData(0x8755435, "Walk in the Park"),
    "WitP - Opal 231": LocData(0x8755436, "Walk in the Park"),
    "WitP - Opal 232": LocData(0x8755437, "Walk in the Park"),
    "WitP - Opal 233": LocData(0x8755438, "Walk in the Park"),
    "WitP - Opal 234": LocData(0x8755439, "Walk in the Park"),
    "WitP - Opal 235": LocData(0x875543A, "Walk in the Park"),
    "WitP - Opal 236": LocData(0x875543B, "Walk in the Park"),
    "WitP - Opal 237": LocData(0x875543C, "Walk in the Park"),
    "WitP - Opal 238": LocData(0x875543D, "Walk in the Park"),
    "WitP - Opal 239": LocData(0x875543E, "Walk in the Park"),
    "WitP - Opal 240": LocData(0x875543F, "Walk in the Park"),
    "WitP - Opal 241": LocData(0x8755440, "Walk in the Park"),
    "WitP - Opal 242": LocData(0x8755441, "Walk in the Park"),
    "WitP - Opal 243": LocData(0x8755442, "Walk in the Park"),
    "WitP - Opal 244": LocData(0x8755443, "Walk in the Park"),
    "WitP - Opal 245": LocData(0x8755444, "Walk in the Park"),
    "WitP - Opal 246": LocData(0x8755445, "Walk in the Park"),
    "WitP - Opal 247": LocData(0x8755446, "Walk in the Park"),
    "WitP - Opal 248": LocData(0x8755447, "Walk in the Park"),
    "WitP - Opal 249": LocData(0x8755448, "Walk in the Park"),
    "WitP - Opal 250": LocData(0x8755449, "Walk in the Park"),
    "WitP - Opal 251": LocData(0x875544A, "Walk in the Park"),
    "WitP - Opal 252": LocData(0x875544B, "Walk in the Park"),
    "WitP - Opal 253": LocData(0x875544C, "Walk in the Park"),
    "WitP - Opal 254": LocData(0x875544D, "Walk in the Park"),
    "WitP - Opal 255": LocData(0x875544E, "Walk in the Park"),
    "WitP - Opal 256": LocData(0x875544F, "Walk in the Park"),
    "WitP - Opal 257": LocData(0x8755450, "Walk in the Park"),
    "WitP - Opal 258": LocData(0x8755451, "Walk in the Park"),
    "WitP - Opal 259": LocData(0x8755452, "Walk in the Park"),
    "WitP - Opal 260": LocData(0x8755453, "Walk in the Park"),
    "WitP - Opal 261": LocData(0x8755454, "Walk in the Park"),
    "WitP - Opal 262": LocData(0x8755455, "Walk in the Park"),
    "WitP - Opal 263": LocData(0x8755456, "Walk in the Park"),
    "WitP - Opal 264": LocData(0x8755457, "Walk in the Park"),
    "WitP - Opal 265": LocData(0x8755458, "Walk in the Park"),
    "WitP - Opal 266": LocData(0x8755459, "Walk in the Park"),
    "WitP - Opal 267": LocData(0x875545A, "Walk in the Park"),
    "WitP - Opal 268": LocData(0x875545B, "Walk in the Park"),
    "WitP - Opal 269": LocData(0x875545C, "Walk in the Park"),
    "WitP - Opal 270": LocData(0x875545D, "Walk in the Park"),
    "WitP - Opal 271": LocData(0x875545E, "Walk in the Park"),
    "WitP - Opal 272": LocData(0x875545F, "Walk in the Park"),
    "WitP - Opal 273": LocData(0x8755460, "Walk in the Park"),
    "WitP - Opal 274": LocData(0x8755461, "Walk in the Park"),
    "WitP - Opal 275": LocData(0x8755462, "Walk in the Park"),
    "WitP - Opal 276": LocData(0x8755463, "Walk in the Park"),
    "WitP - Opal 277": LocData(0x8755464, "Walk in the Park"),
    "WitP - Opal 278": LocData(0x8755465, "Walk in the Park"),
    "WitP - Opal 279": LocData(0x8755466, "Walk in the Park"),
    "WitP - Opal 280": LocData(0x8755467, "Walk in the Park"),
    "WitP - Opal 281": LocData(0x8755468, "Walk in the Park"),
    "WitP - Opal 282": LocData(0x8755469, "Walk in the Park"),
    "WitP - Opal 283": LocData(0x875546A, "Walk in the Park"),
    "WitP - Opal 284": LocData(0x875546B, "Walk in the Park"),
    "WitP - Opal 285": LocData(0x875546C, "Walk in the Park"),
    "WitP - Opal 286": LocData(0x875546D, "Walk in the Park"),
    "WitP - Opal 287": LocData(0x875546E, "Walk in the Park"),
    "WitP - Opal 288": LocData(0x875546F, "Walk in the Park"),
    "WitP - Opal 289": LocData(0x8755470, "Walk in the Park"),
    "WitP - Opal 290": LocData(0x8755471, "Walk in the Park"),
    "WitP - Opal 291": LocData(0x8755472, "Walk in the Park"),
    "WitP - Opal 292": LocData(0x8755473, "Walk in the Park"),
    "WitP - Opal 293": LocData(0x8755474, "Walk in the Park"),
    "WitP - Opal 294": LocData(0x8755475, "Walk in the Park"),
    "WitP - Opal 295": LocData(0x8755476, "Walk in the Park"),
    "WitP - Opal 296": LocData(0x8755477, "Walk in the Park"),
    "WitP - Opal 297": LocData(0x8755478, "Walk in the Park"),
    "WitP - Opal 298": LocData(0x8755479, "Walk in the Park"),
    "WitP - Opal 299": LocData(0x875547A, "Walk in the Park"),
    "WitP - Opal 300": LocData(0x875547B, "Walk in the Park"),
    "Ship Rex - Opal 1": LocData(0x8756350, "Ship Rex"),
    "Ship Rex - Opal 2": LocData(0x8756351, "Ship Rex"),
    "Ship Rex - Opal 3": LocData(0x8756352, "Ship Rex"),
    "Ship Rex - Opal 4": LocData(0x8756353, "Ship Rex"),
    "Ship Rex - Opal 5": LocData(0x8756354, "Ship Rex"),
    "Ship Rex - Opal 6": LocData(0x8756355, "Ship Rex"),
    "Ship Rex - Opal 7": LocData(0x8756356, "Ship Rex"),
    "Ship Rex - Opal 8": LocData(0x8756357, "Ship Rex"),
    "Ship Rex - Opal 9": LocData(0x8756358, "Ship Rex"),
    "Ship Rex - Opal 10": LocData(0x8756359, "Ship Rex"),
    "Ship Rex - Opal 11": LocData(0x875635A, "Ship Rex"),
    "Ship Rex - Opal 12": LocData(0x875635B, "Ship Rex"),
    "Ship Rex - Opal 13": LocData(0x875635C, "Ship Rex"),
    "Ship Rex - Opal 14": LocData(0x875635D, "Ship Rex"),
    "Ship Rex - Opal 15": LocData(0x875635E, "Ship Rex"),
    "Ship Rex - Opal 16": LocData(0x875635F, "Ship Rex"),
    "Ship Rex - Opal 17": LocData(0x8756360, "Ship Rex"),
    "Ship Rex - Opal 18": LocData(0x8756361, "Ship Rex"),
    "Ship Rex - Opal 19": LocData(0x8756362, "Ship Rex"),
    "Ship Rex - Opal 20": LocData(0x8756363, "Ship Rex"),
    "Ship Rex - Opal 21": LocData(0x8756364, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 22": LocData(0x8756365, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 23": LocData(0x8756366, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 24": LocData(0x8756367, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 25": LocData(0x8756368, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 26": LocData(0x8756369, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 27": LocData(0x875636A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 28": LocData(0x875636B, "Ship Rex"),
    "Ship Rex - Opal 29": LocData(0x875636C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 30": LocData(0x875636D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 31": LocData(0x875636E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 32": LocData(0x875636F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 33": LocData(0x8756370, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 34": LocData(0x8756371, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 35": LocData(0x8756372, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 36": LocData(0x8756373, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 37": LocData(0x8756374, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 38": LocData(0x8756375, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 39": LocData(0x8756376, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 40": LocData(0x8756377, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 41": LocData(0x8756378, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 42": LocData(0x8756379, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 43": LocData(0x875637A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 44": LocData(0x875637B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 45": LocData(0x875637C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 46": LocData(0x875637D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 47": LocData(0x875637E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 48": LocData(0x875637F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 49": LocData(0x8756380, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 50": LocData(0x8756381, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 51": LocData(0x8756382, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 52": LocData(0x8756383, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 53": LocData(0x8756384, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 54": LocData(0x8756385, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 55": LocData(0x8756386, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 56": LocData(0x8756387, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 57": LocData(0x8756388, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 58": LocData(0x8756389, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 59": LocData(0x875638A, "Ship Rex"),
    "Ship Rex - Opal 60": LocData(0x875638B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 61": LocData(0x875638C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 62": LocData(0x875638D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 63": LocData(0x875638E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 64": LocData(0x875638F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 65": LocData(0x8756390, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 66": LocData(0x8756391, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 67": LocData(0x8756392, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 68": LocData(0x8756393, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 69": LocData(0x8756394, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 70": LocData(0x8756395, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 71": LocData(0x8756396, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 72": LocData(0x8756397, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 73": LocData(0x8756398, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 74": LocData(0x8756399, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 75": LocData(0x875639A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 76": LocData(0x875639B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 77": LocData(0x875639C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 78": LocData(0x875639D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 79": LocData(0x875639E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 80": LocData(0x875639F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 81": LocData(0x87563A0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 82": LocData(0x87563A1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 83": LocData(0x87563A2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 84": LocData(0x87563A3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 85": LocData(0x87563A4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 86": LocData(0x87563A5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 87": LocData(0x87563A6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 88": LocData(0x87563A7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 89": LocData(0x87563A8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 90": LocData(0x87563A9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 91": LocData(0x87563AA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 92": LocData(0x87563AB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 93": LocData(0x87563AC, "Ship Rex"),
    "Ship Rex - Opal 94": LocData(0x87563AD, "Ship Rex"),
    "Ship Rex - Opal 95": LocData(0x87563AE, "Ship Rex"),
    "Ship Rex - Opal 96": LocData(0x87563AF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 97": LocData(0x87563B0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 98": LocData(0x87563B1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 99": LocData(0x87563B2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 100": LocData(0x87563B3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 101": LocData(0x87563B4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 102": LocData(0x87563B5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 103": LocData(0x87563B6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 104": LocData(0x87563B7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 105": LocData(0x87563B8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 106": LocData(0x87563B9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 107": LocData(0x87563BA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 108": LocData(0x87563BB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 109": LocData(0x87563BC, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 110": LocData(0x87563BD, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 111": LocData(0x87563BE, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 112": LocData(0x87563BF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 113": LocData(0x87563C0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 114": LocData(0x87563C1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 115": LocData(0x87563C2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 116": LocData(0x87563C3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 117": LocData(0x87563C4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 118": LocData(0x87563C5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 119": LocData(0x87563C6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 120": LocData(0x87563C7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 121": LocData(0x87563C8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 122": LocData(0x87563C9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 123": LocData(0x87563CA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 124": LocData(0x87563CB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 125": LocData(0x87563CC, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 126": LocData(0x87563CD, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 127": LocData(0x87563CE, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 128": LocData(0x87563CF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 129": LocData(0x87563D0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 130": LocData(0x87563D1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 131": LocData(0x87563D2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 132": LocData(0x87563D3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 133": LocData(0x87563D4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 134": LocData(0x87563D5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 135": LocData(0x87563D6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 136": LocData(0x87563D7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 137": LocData(0x87563D8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 138": LocData(0x87563D9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 139": LocData(0x87563DA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 140": LocData(0x87563DB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 141": LocData(0x87563DC, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 142": LocData(0x87563DD, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 143": LocData(0x87563DE, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 144": LocData(0x87563DF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 145": LocData(0x87563E0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 146": LocData(0x87563E1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 147": LocData(0x87563E2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 148": LocData(0x87563E3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 149": LocData(0x87563E4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 150": LocData(0x87563E5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 151": LocData(0x87563E6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 152": LocData(0x87563E7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 153": LocData(0x87563E8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 154": LocData(0x87563E9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 155": LocData(0x87563EA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 156": LocData(0x87563EB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 157": LocData(0x87563EC, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 158": LocData(0x87563ED, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 159": LocData(0x87563EE, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 160": LocData(0x87563EF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 161": LocData(0x87563F0, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 162": LocData(0x87563F1, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 163": LocData(0x87563F2, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 164": LocData(0x87563F3, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 165": LocData(0x87563F4, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 166": LocData(0x87563F5, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 167": LocData(0x87563F6, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 168": LocData(0x87563F7, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 169": LocData(0x87563F8, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 170": LocData(0x87563F9, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 171": LocData(0x87563FA, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 172": LocData(0x87563FB, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 173": LocData(0x87563FC, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 174": LocData(0x87563FD, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 175": LocData(0x87563FE, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 176": LocData(0x87563FF, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 177": LocData(0x8756400, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 178": LocData(0x8756401, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 179": LocData(0x8756402, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 180": LocData(0x8756403, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 181": LocData(0x8756404, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 182": LocData(0x8756405, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 183": LocData(0x8756406, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 184": LocData(0x8756407, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 185": LocData(0x8756408, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 186": LocData(0x8756409, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 187": LocData(0x875640A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 188": LocData(0x875640B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 189": LocData(0x875640C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 190": LocData(0x875640D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 191": LocData(0x875640E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 192": LocData(0x875640F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 193": LocData(0x8756410, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 194": LocData(0x8756411, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 195": LocData(0x8756412, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 196": LocData(0x8756413, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 197": LocData(0x8756414, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 198": LocData(0x8756415, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 199": LocData(0x8756416, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 200": LocData(0x8756417, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 201": LocData(0x8756418, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 202": LocData(0x8756419, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 203": LocData(0x875641A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 204": LocData(0x875641B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 205": LocData(0x875641C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 206": LocData(0x875641D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 207": LocData(0x875641E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 208": LocData(0x875641F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 209": LocData(0x8756420, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 210": LocData(0x8756421, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 211": LocData(0x8756422, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 212": LocData(0x8756423, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 213": LocData(0x8756424, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 214": LocData(0x8756425, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 215": LocData(0x8756426, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 216": LocData(0x8756427, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 217": LocData(0x8756428, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 218": LocData(0x8756429, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 219": LocData(0x875642A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 220": LocData(0x875642B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 221": LocData(0x875642C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 222": LocData(0x875642D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 223": LocData(0x875642E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 224": LocData(0x875642F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 225": LocData(0x8756430, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 226": LocData(0x8756431, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 227": LocData(0x8756432, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 228": LocData(0x8756433, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 229": LocData(0x8756434, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 230": LocData(0x8756435, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 231": LocData(0x8756436, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 232": LocData(0x8756437, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 233": LocData(0x8756438, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 234": LocData(0x8756439, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 235": LocData(0x875643A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 236": LocData(0x875643B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 237": LocData(0x875643C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 238": LocData(0x875643D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 239": LocData(0x875643E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 240": LocData(0x875643F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 241": LocData(0x8756440, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 242": LocData(0x8756441, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 243": LocData(0x8756442, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 244": LocData(0x8756443, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 245": LocData(0x8756444, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 246": LocData(0x8756445, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 247": LocData(0x8756446, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 248": LocData(0x8756447, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 249": LocData(0x8756448, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 250": LocData(0x8756449, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 251": LocData(0x875644A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 252": LocData(0x875644B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 253": LocData(0x875644C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 254": LocData(0x875644D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 255": LocData(0x875644E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 256": LocData(0x875644F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 257": LocData(0x8756450, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 258": LocData(0x8756451, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 259": LocData(0x8756452, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 260": LocData(0x8756453, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 261": LocData(0x8756454, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 262": LocData(0x8756455, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 263": LocData(0x8756456, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 264": LocData(0x8756457, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 265": LocData(0x8756458, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 266": LocData(0x8756459, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 267": LocData(0x875645A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 268": LocData(0x875645B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 269": LocData(0x875645C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 270": LocData(0x875645D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 271": LocData(0x875645E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 272": LocData(0x875645F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 273": LocData(0x8756460, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 274": LocData(0x8756461, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 275": LocData(0x8756462, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 276": LocData(0x8756463, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 277": LocData(0x8756464, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 278": LocData(0x8756465, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 279": LocData(0x8756466, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 280": LocData(0x8756467, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 281": LocData(0x8756468, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 282": LocData(0x8756469, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 283": LocData(0x875646A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 284": LocData(0x875646B, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 285": LocData(0x875646C, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 286": LocData(0x875646D, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 287": LocData(0x875646E, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 288": LocData(0x875646F, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 289": LocData(0x8756470, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 290": LocData(0x8756471, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 291": LocData(0x8756472, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 292": LocData(0x8756473, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 293": LocData(0x8756474, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 294": LocData(0x8756475, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 295": LocData(0x8756476, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 296": LocData(0x8756477, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 297": LocData(0x8756478, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 298": LocData(0x8756479, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 299": LocData(0x875647A, "Ship Rex - Beyond Gate"),
    "Ship Rex - Opal 300": LocData(0x875647B, "Ship Rex - Beyond Gate"),
    "BotRT - Opal 1": LocData(0x8758350, "Bridge on the River Ty"),
    "BotRT - Opal 2": LocData(0x8758351, "Bridge on the River Ty"),
    "BotRT - Opal 3": LocData(0x8758352, "Bridge on the River Ty"),
    "BotRT - Opal 4": LocData(0x8758353, "Bridge on the River Ty"),
    "BotRT - Opal 5": LocData(0x8758354, "Bridge on the River Ty"),
    "BotRT - Opal 6": LocData(0x8758355, "Bridge on the River Ty"),
    "BotRT - Opal 7": LocData(0x8758356, "Bridge on the River Ty"),
    "BotRT - Opal 8": LocData(0x8758357, "Bridge on the River Ty"),
    "BotRT - Opal 9": LocData(0x8758358, "Bridge on the River Ty"),
    "BotRT - Opal 10": LocData(0x8758359, "Bridge on the River Ty"),
    "BotRT - Opal 11": LocData(0x875835A, "Bridge on the River Ty"),
    "BotRT - Opal 12": LocData(0x875835B, "Bridge on the River Ty"),
    "BotRT - Opal 13": LocData(0x875835C, "Bridge on the River Ty"),
    "BotRT - Opal 14": LocData(0x875835D, "Bridge on the River Ty"),
    "BotRT - Opal 15": LocData(0x875835E, "Bridge on the River Ty"),
    "BotRT - Opal 16": LocData(0x875835F, "Bridge on the River Ty"),
    "BotRT - Opal 17": LocData(0x8758360, "Bridge on the River Ty"),
    "BotRT - Opal 18": LocData(0x8758361, "Bridge on the River Ty"),
    "BotRT - Opal 19": LocData(0x8758362, "Bridge on the River Ty"),
    "BotRT - Opal 20": LocData(0x8758363, "Bridge on the River Ty"),
    "BotRT - Opal 21": LocData(0x8758364, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 22": LocData(0x8758365, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 23": LocData(0x8758366, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 24": LocData(0x8758367, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 25": LocData(0x8758368, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 26": LocData(0x8758369, "Bridge on the River Ty"),
    "BotRT - Opal 27": LocData(0x875836A, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 28": LocData(0x875836B, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 29": LocData(0x875836C, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 30": LocData(0x875836D, "Bridge on the River Ty"),
    "BotRT - Opal 31": LocData(0x875836E, "Bridge on the River Ty"),
    "BotRT - Opal 32": LocData(0x875836F, "Bridge on the River Ty"),
    "BotRT - Opal 33": LocData(0x8758370, "Bridge on the River Ty"),
    "BotRT - Opal 34": LocData(0x8758371, "Bridge on the River Ty"),
    "BotRT - Opal 35": LocData(0x8758372, "Bridge on the River Ty"),
    "BotRT - Opal 36": LocData(0x8758373, "Bridge on the River Ty"),
    "BotRT - Opal 37": LocData(0x8758374, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 38": LocData(0x8758375, "Bridge on the River Ty"),
    "BotRT - Opal 39": LocData(0x8758376, "Bridge on the River Ty"),
    "BotRT - Opal 40": LocData(0x8758377, "Bridge on the River Ty"),
    "BotRT - Opal 41": LocData(0x8758378, "Bridge on the River Ty"),
    "BotRT - Opal 42": LocData(0x8758379, "Bridge on the River Ty"),
    "BotRT - Opal 43": LocData(0x875837A, "Bridge on the River Ty"),
    "BotRT - Opal 44": LocData(0x875837B, "Bridge on the River Ty"),
    "BotRT - Opal 45": LocData(0x875837C, "Bridge on the River Ty"),
    "BotRT - Opal 46": LocData(0x875837D, "Bridge on the River Ty"),
    "BotRT - Opal 47": LocData(0x875837E, "Bridge on the River Ty"),
    "BotRT - Opal 48": LocData(0x875837F, "Bridge on the River Ty"),
    "BotRT - Opal 49": LocData(0x8758380, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 50": LocData(0x8758381, "Bridge on the River Ty"),
    "BotRT - Opal 51": LocData(0x8758382, "Bridge on the River Ty"),
    "BotRT - Opal 52": LocData(0x8758383, "Bridge on the River Ty"),
    "BotRT - Opal 53": LocData(0x8758384, "Bridge on the River Ty"),
    "BotRT - Opal 54": LocData(0x8758385, "Bridge on the River Ty"),
    "BotRT - Opal 55": LocData(0x8758386, "Bridge on the River Ty"),
    "BotRT - Opal 56": LocData(0x8758387, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 57": LocData(0x8758388, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 58": LocData(0x8758389, "Bridge on the River Ty"),
    "BotRT - Opal 59": LocData(0x875838A, "Bridge on the River Ty"),
    "BotRT - Opal 60": LocData(0x875838B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 61": LocData(0x875838C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 62": LocData(0x875838D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 63": LocData(0x875838E, "Bridge on the River Ty"),
    "BotRT - Opal 64": LocData(0x875838F, "Bridge on the River Ty"),
    "BotRT - Opal 65": LocData(0x8758390, "Bridge on the River Ty"),
    "BotRT - Opal 66": LocData(0x8758391, "Bridge on the River Ty"),
    "BotRT - Opal 67": LocData(0x8758392, "Bridge on the River Ty"),
    "BotRT - Opal 68": LocData(0x8758393, "Bridge on the River Ty"),
    "BotRT - Opal 69": LocData(0x8758394, "Bridge on the River Ty"),
    "BotRT - Opal 70": LocData(0x8758395, "Bridge on the River Ty"),
    "BotRT - Opal 71": LocData(0x8758396, "Bridge on the River Ty"),
    "BotRT - Opal 72": LocData(0x8758397, "Bridge on the River Ty"),
    "BotRT - Opal 73": LocData(0x8758398, "Bridge on the River Ty"),
    "BotRT - Opal 74": LocData(0x8758399, "Bridge on the River Ty"),
    "BotRT - Opal 75": LocData(0x875839A, "Bridge on the River Ty"),
    "BotRT - Opal 76": LocData(0x875839B, "Bridge on the River Ty"),
    "BotRT - Opal 77": LocData(0x875839C, "Bridge on the River Ty"),
    "BotRT - Opal 78": LocData(0x875839D, "Bridge on the River Ty"),
    "BotRT - Opal 79": LocData(0x875839E, "Bridge on the River Ty"),
    "BotRT - Opal 80": LocData(0x875839F, "Bridge on the River Ty"),
    "BotRT - Opal 81": LocData(0x87583A0, "Bridge on the River Ty"),
    "BotRT - Opal 82": LocData(0x87583A1, "Bridge on the River Ty"),
    "BotRT - Opal 83": LocData(0x87583A2, "Bridge on the River Ty"),
    "BotRT - Opal 84": LocData(0x87583A3, "Bridge on the River Ty"),
    "BotRT - Opal 85": LocData(0x87583A4, "Bridge on the River Ty"),
    "BotRT - Opal 86": LocData(0x87583A5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 87": LocData(0x87583A6, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 88": LocData(0x87583A7, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 89": LocData(0x87583A8, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 90": LocData(0x87583A9, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 91": LocData(0x87583AA, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 92": LocData(0x87583AB, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 93": LocData(0x87583AC, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 94": LocData(0x87583AD, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 95": LocData(0x87583AE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 96": LocData(0x87583AF, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 97": LocData(0x87583B0, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 98": LocData(0x87583B1, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 99": LocData(0x87583B2, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 100": LocData(0x87583B3, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 101": LocData(0x87583B4, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 102": LocData(0x87583B5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 103": LocData(0x87583B6, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 104": LocData(0x87583B7, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 105": LocData(0x87583B8, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 106": LocData(0x87583B9, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 107": LocData(0x87583BA, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 108": LocData(0x87583BB, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 109": LocData(0x87583BC, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 110": LocData(0x87583BD, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 111": LocData(0x87583BE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 112": LocData(0x87583BF, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 113": LocData(0x87583C0, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 114": LocData(0x87583C1, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 115": LocData(0x87583C2, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 116": LocData(0x87583C3, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 117": LocData(0x87583C4, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 118": LocData(0x87583C5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 119": LocData(0x87583C6, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 120": LocData(0x87583C7, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 121": LocData(0x87583C8, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 122": LocData(0x87583C9, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 123": LocData(0x87583CA, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 124": LocData(0x87583CB, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 125": LocData(0x87583CC, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 126": LocData(0x87583CD, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 127": LocData(0x87583CE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 128": LocData(0x87583CF, "Bridge on the River Ty"),
    "BotRT - Opal 129": LocData(0x87583D0, "Bridge on the River Ty"),
    "BotRT - Opal 130": LocData(0x87583D1, "Bridge on the River Ty"),
    "BotRT - Opal 131": LocData(0x87583D2, "Bridge on the River Ty"),
    "BotRT - Opal 132": LocData(0x87583D3, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 133": LocData(0x87583D4, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 134": LocData(0x87583D5, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 135": LocData(0x87583D6, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 136": LocData(0x87583D7, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 137": LocData(0x87583D8, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 138": LocData(0x87583D9, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 139": LocData(0x87583DA, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 140": LocData(0x87583DB, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 141": LocData(0x87583DC, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 142": LocData(0x87583DD, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 143": LocData(0x87583DE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 144": LocData(0x87583DF, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 145": LocData(0x87583E0, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 146": LocData(0x87583E1, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 147": LocData(0x87583E2, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 148": LocData(0x87583E3, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 149": LocData(0x87583E4, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 150": LocData(0x87583E5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 151": LocData(0x87583E6, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 152": LocData(0x87583E7, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 153": LocData(0x87583E8, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 154": LocData(0x87583E9, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 155": LocData(0x87583EA, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 156": LocData(0x87583EB, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 157": LocData(0x87583EC, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 158": LocData(0x87583ED, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 159": LocData(0x87583EE, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 160": LocData(0x87583EF, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 161": LocData(0x87583F0, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 162": LocData(0x87583F1, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 163": LocData(0x87583F2, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 164": LocData(0x87583F3, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 165": LocData(0x87583F4, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 166": LocData(0x87583F5, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 167": LocData(0x87583F6, "Bridge on the River Ty"),
    "BotRT - Opal 168": LocData(0x87583F7, "Bridge on the River Ty"),
    "BotRT - Opal 169": LocData(0x87583F8, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 170": LocData(0x87583F9, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 171": LocData(0x87583FA, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 172": LocData(0x87583FB, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 173": LocData(0x87583FC, "Bridge on the River Ty - Beyond Broken Bridge Underwater"),
    "BotRT - Opal 174": LocData(0x87583FD, "Bridge on the River Ty"),
    "BotRT - Opal 175": LocData(0x87583FE, "Bridge on the River Ty"),
    "BotRT - Opal 176": LocData(0x87583FF, "Bridge on the River Ty"),
    "BotRT - Opal 177": LocData(0x8758400, "Bridge on the River Ty"),
    "BotRT - Opal 178": LocData(0x8758401, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 179": LocData(0x8758402, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 180": LocData(0x8758403, "Bridge on the River Ty - Underwater"),
    "BotRT - Opal 181": LocData(0x8758404, "Bridge on the River Ty"),
    "BotRT - Opal 182": LocData(0x8758405, "Bridge on the River Ty"),
    "BotRT - Opal 183": LocData(0x8758406, "Bridge on the River Ty"),
    "BotRT - Opal 184": LocData(0x8758407, "Bridge on the River Ty"),
    "BotRT - Opal 185": LocData(0x8758408, "Bridge on the River Ty"),
    "BotRT - Opal 186": LocData(0x8758409, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 187": LocData(0x875840A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 188": LocData(0x875840B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 189": LocData(0x875840C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 190": LocData(0x875840D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 191": LocData(0x875840E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 192": LocData(0x875840F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 193": LocData(0x8758410, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 194": LocData(0x8758411, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 195": LocData(0x8758412, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 196": LocData(0x8758413, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 197": LocData(0x8758414, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 198": LocData(0x8758415, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 199": LocData(0x8758416, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 200": LocData(0x8758417, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 201": LocData(0x8758418, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 202": LocData(0x8758419, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 203": LocData(0x875841A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 204": LocData(0x875841B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 205": LocData(0x875841C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 206": LocData(0x875841D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 207": LocData(0x875841E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 208": LocData(0x875841F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 209": LocData(0x8758420, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 210": LocData(0x8758421, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 211": LocData(0x8758422, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 212": LocData(0x8758423, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 213": LocData(0x8758424, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 214": LocData(0x8758425, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 215": LocData(0x8758426, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 216": LocData(0x8758427, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 217": LocData(0x8758428, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 218": LocData(0x8758429, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 219": LocData(0x875842A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 220": LocData(0x875842B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 221": LocData(0x875842C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 222": LocData(0x875842D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 223": LocData(0x875842E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 224": LocData(0x875842F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 225": LocData(0x8758430, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 226": LocData(0x8758431, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 227": LocData(0x8758432, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 228": LocData(0x8758433, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 229": LocData(0x8758434, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 230": LocData(0x8758435, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 231": LocData(0x8758436, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 232": LocData(0x8758437, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 233": LocData(0x8758438, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 234": LocData(0x8758439, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 235": LocData(0x875843A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 236": LocData(0x875843B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 237": LocData(0x875843C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 238": LocData(0x875843D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 239": LocData(0x875843E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 240": LocData(0x875843F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 241": LocData(0x8758440, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 242": LocData(0x8758441, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 243": LocData(0x8758442, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 244": LocData(0x8758443, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 245": LocData(0x8758444, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 246": LocData(0x8758445, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 247": LocData(0x8758446, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 248": LocData(0x8758447, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 249": LocData(0x8758448, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 250": LocData(0x8758449, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 251": LocData(0x875844A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 252": LocData(0x875844B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 253": LocData(0x875844C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 254": LocData(0x875844D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 255": LocData(0x875844E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 256": LocData(0x875844F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 257": LocData(0x8758450, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 258": LocData(0x8758451, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 259": LocData(0x8758452, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 260": LocData(0x8758453, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 261": LocData(0x8758454, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 262": LocData(0x8758455, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 263": LocData(0x8758456, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 264": LocData(0x8758457, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 265": LocData(0x8758458, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 266": LocData(0x8758459, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 267": LocData(0x875845A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 268": LocData(0x875845B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 269": LocData(0x875845C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 270": LocData(0x875845D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 271": LocData(0x875845E, "Bridge on the River Ty"),
    "BotRT - Opal 272": LocData(0x875845F, "Bridge on the River Ty"),
    "BotRT - Opal 273": LocData(0x8758460, "Bridge on the River Ty"),
    "BotRT - Opal 274": LocData(0x8758461, "Bridge on the River Ty"),
    "BotRT - Opal 275": LocData(0x8758462, "Bridge on the River Ty"),
    "BotRT - Opal 276": LocData(0x8758463, "Bridge on the River Ty"),
    "BotRT - Opal 277": LocData(0x8758464, "Bridge on the River Ty"),
    "BotRT - Opal 278": LocData(0x8758465, "Bridge on the River Ty"),
    "BotRT - Opal 279": LocData(0x8758466, "Bridge on the River Ty"),
    "BotRT - Opal 280": LocData(0x8758467, "Bridge on the River Ty"),
    "BotRT - Opal 281": LocData(0x8758468, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 282": LocData(0x8758469, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 283": LocData(0x875846A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 284": LocData(0x875846B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 285": LocData(0x875846C, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 286": LocData(0x875846D, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 287": LocData(0x875846E, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 288": LocData(0x875846F, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 289": LocData(0x8758470, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 290": LocData(0x8758471, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 291": LocData(0x8758472, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 292": LocData(0x8758473, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 293": LocData(0x8758474, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 294": LocData(0x8758475, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 295": LocData(0x8758476, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 296": LocData(0x8758477, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 297": LocData(0x8758478, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 298": LocData(0x8758479, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 299": LocData(0x875847A, "Bridge on the River Ty - Beyond Broken Bridge"),
    "BotRT - Opal 300": LocData(0x875847B, "Bridge on the River Ty - Beyond Broken Bridge"),
    "Snow Worries - Opal 1": LocData(0x8759350, "Snow Worries"),
    "Snow Worries - Opal 2": LocData(0x8759351, "Snow Worries"),
    "Snow Worries - Opal 3": LocData(0x8759352, "Snow Worries"),
    "Snow Worries - Opal 4": LocData(0x8759353, "Snow Worries"),
    "Snow Worries - Opal 5": LocData(0x8759354, "Snow Worries"),
    "Snow Worries - Opal 6": LocData(0x8759355, "Snow Worries"),
    "Snow Worries - Opal 7": LocData(0x8759356, "Snow Worries"),
    "Snow Worries - Opal 8": LocData(0x8759357, "Snow Worries"),
    "Snow Worries - Opal 9": LocData(0x8759358, "Snow Worries"),
    "Snow Worries - Opal 10": LocData(0x8759359, "Snow Worries"),
    "Snow Worries - Opal 11": LocData(0x875935A, "Snow Worries"),
    "Snow Worries - Opal 12": LocData(0x875935B, "Snow Worries"),
    "Snow Worries - Opal 13": LocData(0x875935C, "Snow Worries"),
    "Snow Worries - Opal 14": LocData(0x875935D, "Snow Worries"),
    "Snow Worries - Opal 15": LocData(0x875935E, "Snow Worries"),
    "Snow Worries - Opal 16": LocData(0x875935F, "Snow Worries"),
    "Snow Worries - Opal 17": LocData(0x8759360, "Snow Worries"),
    "Snow Worries - Opal 18": LocData(0x8759361, "Snow Worries"),
    "Snow Worries - Opal 19": LocData(0x8759362, "Snow Worries"),
    "Snow Worries - Opal 20": LocData(0x8759363, "Snow Worries"),
    "Snow Worries - Opal 21": LocData(0x8759364, "Snow Worries"),
    "Snow Worries - Opal 22": LocData(0x8759365, "Snow Worries"),
    "Snow Worries - Opal 23": LocData(0x8759366, "Snow Worries"),
    "Snow Worries - Opal 24": LocData(0x8759367, "Snow Worries"),
    "Snow Worries - Opal 25": LocData(0x8759368, "Snow Worries"),
    "Snow Worries - Opal 26": LocData(0x8759369, "Snow Worries"),
    "Snow Worries - Opal 27": LocData(0x875936A, "Snow Worries"),
    "Snow Worries - Opal 28": LocData(0x875936B, "Snow Worries"),
    "Snow Worries - Opal 29": LocData(0x875936C, "Snow Worries"),
    "Snow Worries - Opal 30": LocData(0x875936D, "Snow Worries"),
    "Snow Worries - Opal 31": LocData(0x875936E, "Snow Worries"),
    "Snow Worries - Opal 32": LocData(0x875936F, "Snow Worries"),
    "Snow Worries - Opal 33": LocData(0x8759370, "Snow Worries"),
    "Snow Worries - Opal 34": LocData(0x8759371, "Snow Worries"),
    "Snow Worries - Opal 35": LocData(0x8759372, "Snow Worries"),
    "Snow Worries - Opal 36": LocData(0x8759373, "Snow Worries"),
    "Snow Worries - Opal 37": LocData(0x8759374, "Snow Worries"),
    "Snow Worries - Opal 38": LocData(0x8759375, "Snow Worries"),
    "Snow Worries - Opal 39": LocData(0x8759376, "Snow Worries"),
    "Snow Worries - Opal 40": LocData(0x8759377, "Snow Worries"),
    "Snow Worries - Opal 41": LocData(0x8759378, "Snow Worries"),
    "Snow Worries - Opal 42": LocData(0x8759379, "Snow Worries"),
    "Snow Worries - Opal 43": LocData(0x875937A, "Snow Worries"),
    "Snow Worries - Opal 44": LocData(0x875937B, "Snow Worries"),
    "Snow Worries - Opal 45": LocData(0x875937C, "Snow Worries"),
    "Snow Worries - Opal 46": LocData(0x875937D, "Snow Worries"),
    "Snow Worries - Opal 47": LocData(0x875937E, "Snow Worries"),
    "Snow Worries - Opal 48": LocData(0x875937F, "Snow Worries"),
    "Snow Worries - Opal 49": LocData(0x8759380, "Snow Worries"),
    "Snow Worries - Opal 50": LocData(0x8759381, "Snow Worries"),
    "Snow Worries - Opal 51": LocData(0x8759382, "Snow Worries"),
    "Snow Worries - Opal 52": LocData(0x8759383, "Snow Worries"),
    "Snow Worries - Opal 53": LocData(0x8759384, "Snow Worries"),
    "Snow Worries - Opal 54": LocData(0x8759385, "Snow Worries"),
    "Snow Worries - Opal 55": LocData(0x8759386, "Snow Worries"),
    "Snow Worries - Opal 56": LocData(0x8759387, "Snow Worries"),
    "Snow Worries - Opal 57": LocData(0x8759388, "Snow Worries"),
    "Snow Worries - Opal 58": LocData(0x8759389, "Snow Worries"),
    "Snow Worries - Opal 59": LocData(0x875938A, "Snow Worries - Underwater"),
    "Snow Worries - Opal 60": LocData(0x875938B, "Snow Worries"),
    "Snow Worries - Opal 61": LocData(0x875938C, "Snow Worries"),
    "Snow Worries - Opal 62": LocData(0x875938D, "Snow Worries"),
    "Snow Worries - Opal 63": LocData(0x875938E, "Snow Worries"),
    "Snow Worries - Opal 64": LocData(0x875938F, "Snow Worries"),
    "Snow Worries - Opal 65": LocData(0x8759390, "Snow Worries"),
    "Snow Worries - Opal 66": LocData(0x8759391, "Snow Worries"),
    "Snow Worries - Opal 67": LocData(0x8759392, "Snow Worries"),
    "Snow Worries - Opal 68": LocData(0x8759393, "Snow Worries"),
    "Snow Worries - Opal 69": LocData(0x8759394, "Snow Worries"),
    "Snow Worries - Opal 70": LocData(0x8759395, "Snow Worries"),
    "Snow Worries - Opal 71": LocData(0x8759396, "Snow Worries"),
    "Snow Worries - Opal 72": LocData(0x8759397, "Snow Worries"),
    "Snow Worries - Opal 73": LocData(0x8759398, "Snow Worries"),
    "Snow Worries - Opal 74": LocData(0x8759399, "Snow Worries"),
    "Snow Worries - Opal 75": LocData(0x875939A, "Snow Worries"),
    "Snow Worries - Opal 76": LocData(0x875939B, "Snow Worries"),
    "Snow Worries - Opal 77": LocData(0x875939C, "Snow Worries"),
    "Snow Worries - Opal 78": LocData(0x875939D, "Snow Worries"),
    "Snow Worries - Opal 79": LocData(0x875939E, "Snow Worries"),
    "Snow Worries - Opal 80": LocData(0x875939F, "Snow Worries"),
    "Snow Worries - Opal 81": LocData(0x87593A0, "Snow Worries"),
    "Snow Worries - Opal 82": LocData(0x87593A1, "Snow Worries"),
    "Snow Worries - Opal 83": LocData(0x87593A2, "Snow Worries - Underwater"),
    "Snow Worries - Opal 84": LocData(0x87593A3, "Snow Worries"),
    "Snow Worries - Opal 85": LocData(0x87593A4, "Snow Worries"),
    "Snow Worries - Opal 86": LocData(0x87593A5, "Snow Worries"),
    "Snow Worries - Opal 87": LocData(0x87593A6, "Snow Worries"),
    "Snow Worries - Opal 88": LocData(0x87593A7, "Snow Worries"),
    "Snow Worries - Opal 89": LocData(0x87593A8, "Snow Worries"),
    "Snow Worries - Opal 90": LocData(0x87593A9, "Snow Worries"),
    "Snow Worries - Opal 91": LocData(0x87593AA, "Snow Worries - Underwater"),
    "Snow Worries - Opal 92": LocData(0x87593AB, "Snow Worries - Underwater"),
    "Snow Worries - Opal 93": LocData(0x87593AC, "Snow Worries - Underwater"),
    "Snow Worries - Opal 94": LocData(0x87593AD, "Snow Worries"),
    "Snow Worries - Opal 95": LocData(0x87593AE, "Snow Worries"),
    "Snow Worries - Opal 96": LocData(0x87593AF, "Snow Worries - Underwater"),
    "Snow Worries - Opal 97": LocData(0x87593B0, "Snow Worries - Underwater"),
    "Snow Worries - Opal 98": LocData(0x87593B1, "Snow Worries - Underwater"),
    "Snow Worries - Opal 99": LocData(0x87593B2, "Snow Worries - Underwater"),
    "Snow Worries - Opal 100": LocData(0x87593B3, "Snow Worries - Underwater"),
    "Snow Worries - Opal 101": LocData(0x87593B4, "Snow Worries - Underwater"),
    "Snow Worries - Opal 102": LocData(0x87593B5, "Snow Worries - Underwater"),
    "Snow Worries - Opal 103": LocData(0x87593B6, "Snow Worries"),
    "Snow Worries - Opal 104": LocData(0x87593B7, "Snow Worries - Underwater"),
    "Snow Worries - Opal 105": LocData(0x87593B8, "Snow Worries - Underwater"),
    "Snow Worries - Opal 106": LocData(0x87593B9, "Snow Worries - Underwater"),
    "Snow Worries - Opal 107": LocData(0x87593BA, "Snow Worries - Underwater"),
    "Snow Worries - Opal 108": LocData(0x87593BB, "Snow Worries"),
    "Snow Worries - Opal 109": LocData(0x87593BC, "Snow Worries"),
    "Snow Worries - Opal 110": LocData(0x87593BD, "Snow Worries"),
    "Snow Worries - Opal 111": LocData(0x87593BE, "Snow Worries"),
    "Snow Worries - Opal 112": LocData(0x87593BF, "Snow Worries"),
    "Snow Worries - Opal 113": LocData(0x87593C0, "Snow Worries"),
    "Snow Worries - Opal 114": LocData(0x87593C1, "Snow Worries"),
    "Snow Worries - Opal 115": LocData(0x87593C2, "Snow Worries"),
    "Snow Worries - Opal 116": LocData(0x87593C3, "Snow Worries"),
    "Snow Worries - Opal 117": LocData(0x87593C4, "Snow Worries"),
    "Snow Worries - Opal 118": LocData(0x87593C5, "Snow Worries"),
    "Snow Worries - Opal 119": LocData(0x87593C6, "Snow Worries"),
    "Snow Worries - Opal 120": LocData(0x87593C7, "Snow Worries"),
    "Snow Worries - Opal 121": LocData(0x87593C8, "Snow Worries"),
    "Snow Worries - Opal 122": LocData(0x87593C9, "Snow Worries"),
    "Snow Worries - Opal 123": LocData(0x87593CA, "Snow Worries"),
    "Snow Worries - Opal 124": LocData(0x87593CB, "Snow Worries"),
    "Snow Worries - Opal 125": LocData(0x87593CC, "Snow Worries - Underwater"),
    "Snow Worries - Opal 126": LocData(0x87593CD, "Snow Worries"),
    "Snow Worries - Opal 127": LocData(0x87593CE, "Snow Worries - Underwater"),
    "Snow Worries - Opal 128": LocData(0x87593CF, "Snow Worries - Underwater"),
    "Snow Worries - Opal 129": LocData(0x87593D0, "Snow Worries - Underwater"),
    "Snow Worries - Opal 130": LocData(0x87593D1, "Snow Worries"),
    "Snow Worries - Opal 131": LocData(0x87593D2, "Snow Worries"),
    "Snow Worries - Opal 132": LocData(0x87593D3, "Snow Worries"),
    "Snow Worries - Opal 133": LocData(0x87593D4, "Snow Worries"),
    "Snow Worries - Opal 134": LocData(0x87593D5, "Snow Worries"),
    "Snow Worries - Opal 135": LocData(0x87593D6, "Snow Worries - Underwater"),
    "Snow Worries - Opal 136": LocData(0x87593D7, "Snow Worries"),
    "Snow Worries - Opal 137": LocData(0x87593D8, "Snow Worries"),
    "Snow Worries - Opal 138": LocData(0x87593D9, "Snow Worries"),
    "Snow Worries - Opal 139": LocData(0x87593DA, "Snow Worries"),
    "Snow Worries - Opal 140": LocData(0x87593DB, "Snow Worries"),
    "Snow Worries - Opal 141": LocData(0x87593DC, "Snow Worries - Underwater"),
    "Snow Worries - Opal 142": LocData(0x87593DD, "Snow Worries - Underwater"),
    "Snow Worries - Opal 143": LocData(0x87593DE, "Snow Worries"),
    "Snow Worries - Opal 144": LocData(0x87593DF, "Snow Worries"),
    "Snow Worries - Opal 145": LocData(0x87593E0, "Snow Worries"),
    "Snow Worries - Opal 146": LocData(0x87593E1, "Snow Worries"),
    "Snow Worries - Opal 147": LocData(0x87593E2, "Snow Worries"),
    "Snow Worries - Opal 148": LocData(0x87593E3, "Snow Worries"),
    "Snow Worries - Opal 149": LocData(0x87593E4, "Snow Worries"),
    "Snow Worries - Opal 150": LocData(0x87593E5, "Snow Worries"),
    "Snow Worries - Opal 151": LocData(0x87593E6, "Snow Worries"),
    "Snow Worries - Opal 152": LocData(0x87593E7, "Snow Worries"),
    "Snow Worries - Opal 153": LocData(0x87593E8, "Snow Worries"),
    "Snow Worries - Opal 154": LocData(0x87593E9, "Snow Worries"),
    "Snow Worries - Opal 155": LocData(0x87593EA, "Snow Worries"),
    "Snow Worries - Opal 156": LocData(0x87593EB, "Snow Worries"),
    "Snow Worries - Opal 157": LocData(0x87593EC, "Snow Worries"),
    "Snow Worries - Opal 158": LocData(0x87593ED, "Snow Worries"),
    "Snow Worries - Opal 159": LocData(0x87593EE, "Snow Worries"),
    "Snow Worries - Opal 160": LocData(0x87593EF, "Snow Worries"),
    "Snow Worries - Opal 161": LocData(0x87593F0, "Snow Worries"),
    "Snow Worries - Opal 162": LocData(0x87593F1, "Snow Worries"),
    "Snow Worries - Opal 163": LocData(0x87593F2, "Snow Worries"),
    "Snow Worries - Opal 164": LocData(0x87593F3, "Snow Worries"),
    "Snow Worries - Opal 165": LocData(0x87593F4, "Snow Worries"),
    "Snow Worries - Opal 166": LocData(0x87593F5, "Snow Worries"),
    "Snow Worries - Opal 167": LocData(0x87593F6, "Snow Worries"),
    "Snow Worries - Opal 168": LocData(0x87593F7, "Snow Worries"),
    "Snow Worries - Opal 169": LocData(0x87593F8, "Snow Worries"),
    "Snow Worries - Opal 170": LocData(0x87593F9, "Snow Worries"),
    "Snow Worries - Opal 171": LocData(0x87593FA, "Snow Worries"),
    "Snow Worries - Opal 172": LocData(0x87593FB, "Snow Worries"),
    "Snow Worries - Opal 173": LocData(0x87593FC, "Snow Worries"),
    "Snow Worries - Opal 174": LocData(0x87593FD, "Snow Worries"),
    "Snow Worries - Opal 175": LocData(0x87593FE, "Snow Worries"),
    "Snow Worries - Opal 176": LocData(0x87593FF, "Snow Worries"),
    "Snow Worries - Opal 177": LocData(0x8759400, "Snow Worries - Underwater"),
    "Snow Worries - Opal 178": LocData(0x8759401, "Snow Worries - Underwater"),
    "Snow Worries - Opal 179": LocData(0x8759402, "Snow Worries - Underwater"),
    "Snow Worries - Opal 180": LocData(0x8759403, "Snow Worries - Underwater"),
    "Snow Worries - Opal 181": LocData(0x8759404, "Snow Worries"),
    "Snow Worries - Opal 182": LocData(0x8759405, "Snow Worries"),
    "Snow Worries - Opal 183": LocData(0x8759406, "Snow Worries"),
    "Snow Worries - Opal 184": LocData(0x8759407, "Snow Worries"),
    "Snow Worries - Opal 185": LocData(0x8759408, "Snow Worries"),
    "Snow Worries - Opal 186": LocData(0x8759409, "Snow Worries"),
    "Snow Worries - Opal 187": LocData(0x875940A, "Snow Worries"),
    "Snow Worries - Opal 188": LocData(0x875940B, "Snow Worries"),
    "Snow Worries - Opal 189": LocData(0x875940C, "Snow Worries"),
    "Snow Worries - Opal 190": LocData(0x875940D, "Snow Worries"),
    "Snow Worries - Opal 191": LocData(0x875940E, "Snow Worries"),
    "Snow Worries - Opal 192": LocData(0x875940F, "Snow Worries"),
    "Snow Worries - Opal 193": LocData(0x8759410, "Snow Worries"),
    "Snow Worries - Opal 194": LocData(0x8759411, "Snow Worries"),
    "Snow Worries - Opal 195": LocData(0x8759412, "Snow Worries"),
    "Snow Worries - Opal 196": LocData(0x8759413, "Snow Worries"),
    "Snow Worries - Opal 197": LocData(0x8759414, "Snow Worries"),
    "Snow Worries - Opal 198": LocData(0x8759415, "Snow Worries"),
    "Snow Worries - Opal 199": LocData(0x8759416, "Snow Worries"),
    "Snow Worries - Opal 200": LocData(0x8759417, "Snow Worries"),
    "Snow Worries - Opal 201": LocData(0x8759418, "Snow Worries"),
    "Snow Worries - Opal 202": LocData(0x8759419, "Snow Worries"),
    "Snow Worries - Opal 203": LocData(0x875941A, "Snow Worries"),
    "Snow Worries - Opal 204": LocData(0x875941B, "Snow Worries"),
    "Snow Worries - Opal 205": LocData(0x875941C, "Snow Worries - Underwater"),
    "Snow Worries - Opal 206": LocData(0x875941D, "Snow Worries - Underwater"),
    "Snow Worries - Opal 207": LocData(0x875941E, "Snow Worries - Underwater"),
    "Snow Worries - Opal 208": LocData(0x875941F, "Snow Worries - Underwater"),
    "Snow Worries - Opal 209": LocData(0x8759420, "Snow Worries"),
    "Snow Worries - Opal 210": LocData(0x8759421, "Snow Worries"),
    "Snow Worries - Opal 211": LocData(0x8759422, "Snow Worries"),
    "Snow Worries - Opal 212": LocData(0x8759423, "Snow Worries"),
    "Snow Worries - Opal 213": LocData(0x8759424, "Snow Worries"),
    "Snow Worries - Opal 214": LocData(0x8759425, "Snow Worries"),
    "Snow Worries - Opal 215": LocData(0x8759426, "Snow Worries"),
    "Snow Worries - Opal 216": LocData(0x8759427, "Snow Worries"),
    "Snow Worries - Opal 217": LocData(0x8759428, "Snow Worries"),
    "Snow Worries - Opal 218": LocData(0x8759429, "Snow Worries"),
    "Snow Worries - Opal 219": LocData(0x875942A, "Snow Worries"),
    "Snow Worries - Opal 220": LocData(0x875942B, "Snow Worries"),
    "Snow Worries - Opal 221": LocData(0x875942C, "Snow Worries"),
    "Snow Worries - Opal 222": LocData(0x875942D, "Snow Worries"),
    "Snow Worries - Opal 223": LocData(0x875942E, "Snow Worries"),
    "Snow Worries - Opal 224": LocData(0x875942F, "Snow Worries"),
    "Snow Worries - Opal 225": LocData(0x8759430, "Snow Worries"),
    "Snow Worries - Opal 226": LocData(0x8759431, "Snow Worries"),
    "Snow Worries - Opal 227": LocData(0x8759432, "Snow Worries"),
    "Snow Worries - Opal 228": LocData(0x8759433, "Snow Worries"),
    "Snow Worries - Opal 229": LocData(0x8759434, "Snow Worries"),
    "Snow Worries - Opal 230": LocData(0x8759435, "Snow Worries"),
    "Snow Worries - Opal 231": LocData(0x8759436, "Snow Worries"),
    "Snow Worries - Opal 232": LocData(0x8759437, "Snow Worries"),
    "Snow Worries - Opal 233": LocData(0x8759438, "Snow Worries"),
    "Snow Worries - Opal 234": LocData(0x8759439, "Snow Worries"),
    "Snow Worries - Opal 235": LocData(0x875943A, "Snow Worries"),
    "Snow Worries - Opal 236": LocData(0x875943B, "Snow Worries"),
    "Snow Worries - Opal 237": LocData(0x875943C, "Snow Worries"),
    "Snow Worries - Opal 238": LocData(0x875943D, "Snow Worries"),
    "Snow Worries - Opal 239": LocData(0x875943E, "Snow Worries"),
    "Snow Worries - Opal 240": LocData(0x875943F, "Snow Worries"),
    "Snow Worries - Opal 241": LocData(0x8759440, "Snow Worries"),
    "Snow Worries - Opal 242": LocData(0x8759441, "Snow Worries"),
    "Snow Worries - Opal 243": LocData(0x8759442, "Snow Worries"),
    "Snow Worries - Opal 244": LocData(0x8759443, "Snow Worries"),
    "Snow Worries - Opal 245": LocData(0x8759444, "Snow Worries"),
    "Snow Worries - Opal 246": LocData(0x8759445, "Snow Worries"),
    "Snow Worries - Opal 247": LocData(0x8759446, "Snow Worries"),
    "Snow Worries - Opal 248": LocData(0x8759447, "Snow Worries"),
    "Snow Worries - Opal 249": LocData(0x8759448, "Snow Worries"),
    "Snow Worries - Opal 250": LocData(0x8759449, "Snow Worries"),
    "Snow Worries - Opal 251": LocData(0x875944A, "Snow Worries"),
    "Snow Worries - Opal 252": LocData(0x875944B, "Snow Worries"),
    "Snow Worries - Opal 253": LocData(0x875944C, "Snow Worries"),
    "Snow Worries - Opal 254": LocData(0x875944D, "Snow Worries"),
    "Snow Worries - Opal 255": LocData(0x875944E, "Snow Worries"),
    "Snow Worries - Opal 256": LocData(0x875944F, "Snow Worries"),
    "Snow Worries - Opal 257": LocData(0x8759450, "Snow Worries"),
    "Snow Worries - Opal 258": LocData(0x8759451, "Snow Worries"),
    "Snow Worries - Opal 259": LocData(0x8759452, "Snow Worries"),
    "Snow Worries - Opal 260": LocData(0x8759453, "Snow Worries"),
    "Snow Worries - Opal 261": LocData(0x8759454, "Snow Worries"),
    "Snow Worries - Opal 262": LocData(0x8759455, "Snow Worries"),
    "Snow Worries - Opal 263": LocData(0x8759456, "Snow Worries"),
    "Snow Worries - Opal 264": LocData(0x8759457, "Snow Worries"),
    "Snow Worries - Opal 265": LocData(0x8759458, "Snow Worries"),
    "Snow Worries - Opal 266": LocData(0x8759459, "Snow Worries"),
    "Snow Worries - Opal 267": LocData(0x875945A, "Snow Worries"),
    "Snow Worries - Opal 268": LocData(0x875945B, "Snow Worries"),
    "Snow Worries - Opal 269": LocData(0x875945C, "Snow Worries"),
    "Snow Worries - Opal 270": LocData(0x875945D, "Snow Worries"),
    "Snow Worries - Opal 271": LocData(0x875945E, "Snow Worries"),
    "Snow Worries - Opal 272": LocData(0x875945F, "Snow Worries"),
    "Snow Worries - Opal 273": LocData(0x8759460, "Snow Worries"),
    "Snow Worries - Opal 274": LocData(0x8759461, "Snow Worries"),
    "Snow Worries - Opal 275": LocData(0x8759462, "Snow Worries"),
    "Snow Worries - Opal 276": LocData(0x8759463, "Snow Worries"),
    "Snow Worries - Opal 277": LocData(0x8759464, "Snow Worries"),
    "Snow Worries - Opal 278": LocData(0x8759465, "Snow Worries"),
    "Snow Worries - Opal 279": LocData(0x8759466, "Snow Worries"),
    "Snow Worries - Opal 280": LocData(0x8759467, "Snow Worries"),
    "Snow Worries - Opal 281": LocData(0x8759468, "Snow Worries"),
    "Snow Worries - Opal 282": LocData(0x8759469, "Snow Worries"),
    "Snow Worries - Opal 283": LocData(0x875946A, "Snow Worries"),
    "Snow Worries - Opal 284": LocData(0x875946B, "Snow Worries"),
    "Snow Worries - Opal 285": LocData(0x875946C, "Snow Worries"),
    "Snow Worries - Opal 286": LocData(0x875946D, "Snow Worries"),
    "Snow Worries - Opal 287": LocData(0x875946E, "Snow Worries"),
    "Snow Worries - Opal 288": LocData(0x875946F, "Snow Worries"),
    "Snow Worries - Opal 289": LocData(0x8759470, "Snow Worries"),
    "Snow Worries - Opal 290": LocData(0x8759471, "Snow Worries"),
    "Snow Worries - Opal 291": LocData(0x8759472, "Snow Worries"),
    "Snow Worries - Opal 292": LocData(0x8759473, "Snow Worries"),
    "Snow Worries - Opal 293": LocData(0x8759474, "Snow Worries"),
    "Snow Worries - Opal 294": LocData(0x8759475, "Snow Worries"),
    "Snow Worries - Opal 295": LocData(0x8759476, "Snow Worries"),
    "Snow Worries - Opal 296": LocData(0x8759477, "Snow Worries"),
    "Snow Worries - Opal 297": LocData(0x8759478, "Snow Worries"),
    "Snow Worries - Opal 298": LocData(0x8759479, "Snow Worries"),
    "Snow Worries - Opal 299": LocData(0x875947A, "Snow Worries"),
    "Snow Worries - Opal 300": LocData(0x875947B, "Snow Worries"),
    "Outback Safari - Opal 1": LocData(0x875A350, "Outback Safari"),
    "Outback Safari - Opal 2": LocData(0x875A351, "Outback Safari"),
    "Outback Safari - Opal 3": LocData(0x875A352, "Outback Safari"),
    "Outback Safari - Opal 4": LocData(0x875A353, "Outback Safari"),
    "Outback Safari - Opal 5": LocData(0x875A354, "Outback Safari"),
    "Outback Safari - Opal 6": LocData(0x875A355, "Outback Safari"),
    "Outback Safari - Opal 7": LocData(0x875A356, "Outback Safari"),
    "Outback Safari - Opal 8": LocData(0x875A357, "Outback Safari"),
    "Outback Safari - Opal 9": LocData(0x875A358, "Outback Safari"),
    "Outback Safari - Opal 10": LocData(0x875A359, "Outback Safari"),
    "Outback Safari - Opal 11": LocData(0x875A35A, "Outback Safari"),
    "Outback Safari - Opal 12": LocData(0x875A35B, "Outback Safari"),
    "Outback Safari - Opal 13": LocData(0x875A35C, "Outback Safari"),
    "Outback Safari - Opal 14": LocData(0x875A35D, "Outback Safari"),
    "Outback Safari - Opal 15": LocData(0x875A35E, "Outback Safari"),
    "Outback Safari - Opal 16": LocData(0x875A35F, "Outback Safari"),
    "Outback Safari - Opal 17": LocData(0x875A360, "Outback Safari"),
    "Outback Safari - Opal 18": LocData(0x875A361, "Outback Safari"),
    "Outback Safari - Opal 19": LocData(0x875A362, "Outback Safari"),
    "Outback Safari - Opal 20": LocData(0x875A363, "Outback Safari"),
    "Outback Safari - Opal 21": LocData(0x875A364, "Outback Safari"),
    "Outback Safari - Opal 22": LocData(0x875A365, "Outback Safari"),
    "Outback Safari - Opal 23": LocData(0x875A366, "Outback Safari"),
    "Outback Safari - Opal 24": LocData(0x875A367, "Outback Safari"),
    "Outback Safari - Opal 25": LocData(0x875A368, "Outback Safari"),
    "Outback Safari - Opal 26": LocData(0x875A369, "Outback Safari"),
    "Outback Safari - Opal 27": LocData(0x875A36A, "Outback Safari"),
    "Outback Safari - Opal 28": LocData(0x875A36B, "Outback Safari"),
    "Outback Safari - Opal 29": LocData(0x875A36C, "Outback Safari"),
    "Outback Safari - Opal 30": LocData(0x875A36D, "Outback Safari"),
    "Outback Safari - Opal 31": LocData(0x875A36E, "Outback Safari"),
    "Outback Safari - Opal 32": LocData(0x875A36F, "Outback Safari"),
    "Outback Safari - Opal 33": LocData(0x875A370, "Outback Safari"),
    "Outback Safari - Opal 34": LocData(0x875A371, "Outback Safari"),
    "Outback Safari - Opal 35": LocData(0x875A372, "Outback Safari"),
    "Outback Safari - Opal 36": LocData(0x875A373, "Outback Safari"),
    "Outback Safari - Opal 37": LocData(0x875A374, "Outback Safari"),
    "Outback Safari - Opal 38": LocData(0x875A375, "Outback Safari"),
    "Outback Safari - Opal 39": LocData(0x875A376, "Outback Safari"),
    "Outback Safari - Opal 40": LocData(0x875A377, "Outback Safari"),
    "Outback Safari - Opal 41": LocData(0x875A378, "Outback Safari"),
    "Outback Safari - Opal 42": LocData(0x875A379, "Outback Safari"),
    "Outback Safari - Opal 43": LocData(0x875A37A, "Outback Safari"),
    "Outback Safari - Opal 44": LocData(0x875A37B, "Outback Safari"),
    "Outback Safari - Opal 45": LocData(0x875A37C, "Outback Safari"),
    "Outback Safari - Opal 46": LocData(0x875A37D, "Outback Safari"),
    "Outback Safari - Opal 47": LocData(0x875A37E, "Outback Safari"),
    "Outback Safari - Opal 48": LocData(0x875A37F, "Outback Safari"),
    "Outback Safari - Opal 49": LocData(0x875A380, "Outback Safari"),
    "Outback Safari - Opal 50": LocData(0x875A381, "Outback Safari"),
    "Outback Safari - Opal 51": LocData(0x875A382, "Outback Safari"),
    "Outback Safari - Opal 52": LocData(0x875A383, "Outback Safari"),
    "Outback Safari - Opal 53": LocData(0x875A384, "Outback Safari"),
    "Outback Safari - Opal 54": LocData(0x875A385, "Outback Safari"),
    "Outback Safari - Opal 55": LocData(0x875A386, "Outback Safari"),
    "Outback Safari - Opal 56": LocData(0x875A387, "Outback Safari"),
    "Outback Safari - Opal 57": LocData(0x875A388, "Outback Safari"),
    "Outback Safari - Opal 58": LocData(0x875A389, "Outback Safari"),
    "Outback Safari - Opal 59": LocData(0x875A38A, "Outback Safari"),
    "Outback Safari - Opal 60": LocData(0x875A38B, "Outback Safari"),
    "Outback Safari - Opal 61": LocData(0x875A38C, "Outback Safari"),
    "Outback Safari - Opal 62": LocData(0x875A38D, "Outback Safari"),
    "Outback Safari - Opal 63": LocData(0x875A38E, "Outback Safari"),
    "Outback Safari - Opal 64": LocData(0x875A38F, "Outback Safari"),
    "Outback Safari - Opal 65": LocData(0x875A390, "Outback Safari"),
    "Outback Safari - Opal 66": LocData(0x875A391, "Outback Safari"),
    "Outback Safari - Opal 67": LocData(0x875A392, "Outback Safari"),
    "Outback Safari - Opal 68": LocData(0x875A393, "Outback Safari"),
    "Outback Safari - Opal 69": LocData(0x875A394, "Outback Safari"),
    "Outback Safari - Opal 70": LocData(0x875A395, "Outback Safari"),
    "Outback Safari - Opal 71": LocData(0x875A396, "Outback Safari"),
    "Outback Safari - Opal 72": LocData(0x875A397, "Outback Safari"),
    "Outback Safari - Opal 73": LocData(0x875A398, "Outback Safari"),
    "Outback Safari - Opal 74": LocData(0x875A399, "Outback Safari"),
    "Outback Safari - Opal 75": LocData(0x875A39A, "Outback Safari"),
    "Outback Safari - Opal 76": LocData(0x875A39B, "Outback Safari"),
    "Outback Safari - Opal 77": LocData(0x875A39C, "Outback Safari"),
    "Outback Safari - Opal 78": LocData(0x875A39D, "Outback Safari"),
    "Outback Safari - Opal 79": LocData(0x875A39E, "Outback Safari"),
    "Outback Safari - Opal 80": LocData(0x875A39F, "Outback Safari"),
    "Outback Safari - Opal 81": LocData(0x875A3A0, "Outback Safari"),
    "Outback Safari - Opal 82": LocData(0x875A3A1, "Outback Safari"),
    "Outback Safari - Opal 83": LocData(0x875A3A2, "Outback Safari"),
    "Outback Safari - Opal 84": LocData(0x875A3A3, "Outback Safari"),
    "Outback Safari - Opal 85": LocData(0x875A3A4, "Outback Safari"),
    "Outback Safari - Opal 86": LocData(0x875A3A5, "Outback Safari"),
    "Outback Safari - Opal 87": LocData(0x875A3A6, "Outback Safari"),
    "Outback Safari - Opal 88": LocData(0x875A3A7, "Outback Safari"),
    "Outback Safari - Opal 89": LocData(0x875A3A8, "Outback Safari"),
    "Outback Safari - Opal 90": LocData(0x875A3A9, "Outback Safari"),
    "Outback Safari - Opal 91": LocData(0x875A3AA, "Outback Safari"),
    "Outback Safari - Opal 92": LocData(0x875A3AB, "Outback Safari"),
    "Outback Safari - Opal 93": LocData(0x875A3AC, "Outback Safari"),
    "Outback Safari - Opal 94": LocData(0x875A3AD, "Outback Safari"),
    "Outback Safari - Opal 95": LocData(0x875A3AE, "Outback Safari"),
    "Outback Safari - Opal 96": LocData(0x875A3AF, "Outback Safari"),
    "Outback Safari - Opal 97": LocData(0x875A3B0, "Outback Safari"),
    "Outback Safari - Opal 98": LocData(0x875A3B1, "Outback Safari"),
    "Outback Safari - Opal 99": LocData(0x875A3B2, "Outback Safari"),
    "Outback Safari - Opal 100": LocData(0x875A3B3, "Outback Safari"),
    "Outback Safari - Opal 101": LocData(0x875A3B4, "Outback Safari"),
    "Outback Safari - Opal 102": LocData(0x875A3B5, "Outback Safari"),
    "Outback Safari - Opal 103": LocData(0x875A3B6, "Outback Safari"),
    "Outback Safari - Opal 104": LocData(0x875A3B7, "Outback Safari"),
    "Outback Safari - Opal 105": LocData(0x875A3B8, "Outback Safari"),
    "Outback Safari - Opal 106": LocData(0x875A3B9, "Outback Safari"),
    "Outback Safari - Opal 107": LocData(0x875A3BA, "Outback Safari"),
    "Outback Safari - Opal 108": LocData(0x875A3BB, "Outback Safari"),
    "Outback Safari - Opal 109": LocData(0x875A3BC, "Outback Safari"),
    "Outback Safari - Opal 110": LocData(0x875A3BD, "Outback Safari"),
    "Outback Safari - Opal 111": LocData(0x875A3BE, "Outback Safari"),
    "Outback Safari - Opal 112": LocData(0x875A3BF, "Outback Safari"),
    "Outback Safari - Opal 113": LocData(0x875A3C0, "Outback Safari"),
    "Outback Safari - Opal 114": LocData(0x875A3C1, "Outback Safari"),
    "Outback Safari - Opal 115": LocData(0x875A3C2, "Outback Safari"),
    "Outback Safari - Opal 116": LocData(0x875A3C3, "Outback Safari"),
    "Outback Safari - Opal 117": LocData(0x875A3C4, "Outback Safari"),
    "Outback Safari - Opal 118": LocData(0x875A3C5, "Outback Safari"),
    "Outback Safari - Opal 119": LocData(0x875A3C6, "Outback Safari"),
    "Outback Safari - Opal 120": LocData(0x875A3C7, "Outback Safari"),
    "Outback Safari - Opal 121": LocData(0x875A3C8, "Outback Safari"),
    "Outback Safari - Opal 122": LocData(0x875A3C9, "Outback Safari"),
    "Outback Safari - Opal 123": LocData(0x875A3CA, "Outback Safari"),
    "Outback Safari - Opal 124": LocData(0x875A3CB, "Outback Safari"),
    "Outback Safari - Opal 125": LocData(0x875A3CC, "Outback Safari"),
    "Outback Safari - Opal 126": LocData(0x875A3CD, "Outback Safari"),
    "Outback Safari - Opal 127": LocData(0x875A3CE, "Outback Safari"),
    "Outback Safari - Opal 128": LocData(0x875A3CF, "Outback Safari"),
    "Outback Safari - Opal 129": LocData(0x875A3D0, "Outback Safari"),
    "Outback Safari - Opal 130": LocData(0x875A3D1, "Outback Safari"),
    "Outback Safari - Opal 131": LocData(0x875A3D2, "Outback Safari"),
    "Outback Safari - Opal 132": LocData(0x875A3D3, "Outback Safari"),
    "Outback Safari - Opal 133": LocData(0x875A3D4, "Outback Safari"),
    "Outback Safari - Opal 134": LocData(0x875A3D5, "Outback Safari"),
    "Outback Safari - Opal 135": LocData(0x875A3D6, "Outback Safari"),
    "Outback Safari - Opal 136": LocData(0x875A3D7, "Outback Safari"),
    "Outback Safari - Opal 137": LocData(0x875A3D8, "Outback Safari"),
    "Outback Safari - Opal 138": LocData(0x875A3D9, "Outback Safari"),
    "Outback Safari - Opal 139": LocData(0x875A3DA, "Outback Safari"),
    "Outback Safari - Opal 140": LocData(0x875A3DB, "Outback Safari"),
    "Outback Safari - Opal 141": LocData(0x875A3DC, "Outback Safari"),
    "Outback Safari - Opal 142": LocData(0x875A3DD, "Outback Safari"),
    "Outback Safari - Opal 143": LocData(0x875A3DE, "Outback Safari"),
    "Outback Safari - Opal 144": LocData(0x875A3DF, "Outback Safari"),
    "Outback Safari - Opal 145": LocData(0x875A3E0, "Outback Safari"),
    "Outback Safari - Opal 146": LocData(0x875A3E1, "Outback Safari"),
    "Outback Safari - Opal 147": LocData(0x875A3E2, "Outback Safari"),
    "Outback Safari - Opal 148": LocData(0x875A3E3, "Outback Safari"),
    "Outback Safari - Opal 149": LocData(0x875A3E4, "Outback Safari"),
    "Outback Safari - Opal 150": LocData(0x875A3E5, "Outback Safari"),
    "Outback Safari - Opal 151": LocData(0x875A3E6, "Outback Safari"),
    "Outback Safari - Opal 152": LocData(0x875A3E7, "Outback Safari"),
    "Outback Safari - Opal 153": LocData(0x875A3E8, "Outback Safari"),
    "Outback Safari - Opal 154": LocData(0x875A3E9, "Outback Safari"),
    "Outback Safari - Opal 155": LocData(0x875A3EA, "Outback Safari"),
    "Outback Safari - Opal 156": LocData(0x875A3EB, "Outback Safari"),
    "Outback Safari - Opal 157": LocData(0x875A3EC, "Outback Safari"),
    "Outback Safari - Opal 158": LocData(0x875A3ED, "Outback Safari"),
    "Outback Safari - Opal 159": LocData(0x875A3EE, "Outback Safari"),
    "Outback Safari - Opal 160": LocData(0x875A3EF, "Outback Safari"),
    "Outback Safari - Opal 161": LocData(0x875A3F0, "Outback Safari"),
    "Outback Safari - Opal 162": LocData(0x875A3F1, "Outback Safari"),
    "Outback Safari - Opal 163": LocData(0x875A3F2, "Outback Safari"),
    "Outback Safari - Opal 164": LocData(0x875A3F3, "Outback Safari"),
    "Outback Safari - Opal 165": LocData(0x875A3F4, "Outback Safari"),
    "Outback Safari - Opal 166": LocData(0x875A3F5, "Outback Safari"),
    "Outback Safari - Opal 167": LocData(0x875A3F6, "Outback Safari"),
    "Outback Safari - Opal 168": LocData(0x875A3F7, "Outback Safari"),
    "Outback Safari - Opal 169": LocData(0x875A3F8, "Outback Safari"),
    "Outback Safari - Opal 170": LocData(0x875A3F9, "Outback Safari"),
    "Outback Safari - Opal 171": LocData(0x875A3FA, "Outback Safari"),
    "Outback Safari - Opal 172": LocData(0x875A3FB, "Outback Safari"),
    "Outback Safari - Opal 173": LocData(0x875A3FC, "Outback Safari"),
    "Outback Safari - Opal 174": LocData(0x875A3FD, "Outback Safari"),
    "Outback Safari - Opal 175": LocData(0x875A3FE, "Outback Safari"),
    "Outback Safari - Opal 176": LocData(0x875A3FF, "Outback Safari"),
    "Outback Safari - Opal 177": LocData(0x875A400, "Outback Safari"),
    "Outback Safari - Opal 178": LocData(0x875A401, "Outback Safari"),
    "Outback Safari - Opal 179": LocData(0x875A402, "Outback Safari"),
    "Outback Safari - Opal 180": LocData(0x875A403, "Outback Safari"),
    "Outback Safari - Opal 181": LocData(0x875A404, "Outback Safari"),
    "Outback Safari - Opal 182": LocData(0x875A405, "Outback Safari"),
    "Outback Safari - Opal 183": LocData(0x875A406, "Outback Safari"),
    "Outback Safari - Opal 184": LocData(0x875A407, "Outback Safari"),
    "Outback Safari - Opal 185": LocData(0x875A408, "Outback Safari"),
    "Outback Safari - Opal 186": LocData(0x875A409, "Outback Safari"),
    "Outback Safari - Opal 187": LocData(0x875A40A, "Outback Safari"),
    "Outback Safari - Opal 188": LocData(0x875A40B, "Outback Safari"),
    "Outback Safari - Opal 189": LocData(0x875A40C, "Outback Safari"),
    "Outback Safari - Opal 190": LocData(0x875A40D, "Outback Safari"),
    "Outback Safari - Opal 191": LocData(0x875A40E, "Outback Safari"),
    "Outback Safari - Opal 192": LocData(0x875A40F, "Outback Safari"),
    "Outback Safari - Opal 193": LocData(0x875A410, "Outback Safari"),
    "Outback Safari - Opal 194": LocData(0x875A411, "Outback Safari"),
    "Outback Safari - Opal 195": LocData(0x875A412, "Outback Safari"),
    "Outback Safari - Opal 196": LocData(0x875A413, "Outback Safari"),
    "Outback Safari - Opal 197": LocData(0x875A414, "Outback Safari"),
    "Outback Safari - Opal 198": LocData(0x875A415, "Outback Safari"),
    "Outback Safari - Opal 199": LocData(0x875A416, "Outback Safari"),
    "Outback Safari - Opal 200": LocData(0x875A417, "Outback Safari"),
    "Outback Safari - Opal 201": LocData(0x875A418, "Outback Safari"),
    "Outback Safari - Opal 202": LocData(0x875A419, "Outback Safari"),
    "Outback Safari - Opal 203": LocData(0x875A41A, "Outback Safari"),
    "Outback Safari - Opal 204": LocData(0x875A41B, "Outback Safari"),
    "Outback Safari - Opal 205": LocData(0x875A41C, "Outback Safari"),
    "Outback Safari - Opal 206": LocData(0x875A41D, "Outback Safari"),
    "Outback Safari - Opal 207": LocData(0x875A41E, "Outback Safari"),
    "Outback Safari - Opal 208": LocData(0x875A41F, "Outback Safari"),
    "Outback Safari - Opal 209": LocData(0x875A420, "Outback Safari"),
    "Outback Safari - Opal 210": LocData(0x875A421, "Outback Safari"),
    "Outback Safari - Opal 211": LocData(0x875A422, "Outback Safari"),
    "Outback Safari - Opal 212": LocData(0x875A423, "Outback Safari"),
    "Outback Safari - Opal 213": LocData(0x875A424, "Outback Safari"),
    "Outback Safari - Opal 214": LocData(0x875A425, "Outback Safari"),
    "Outback Safari - Opal 215": LocData(0x875A426, "Outback Safari"),
    "Outback Safari - Opal 216": LocData(0x875A427, "Outback Safari"),
    "Outback Safari - Opal 217": LocData(0x875A428, "Outback Safari"),
    "Outback Safari - Opal 218": LocData(0x875A429, "Outback Safari"),
    "Outback Safari - Opal 219": LocData(0x875A42A, "Outback Safari"),
    "Outback Safari - Opal 220": LocData(0x875A42B, "Outback Safari"),
    "Outback Safari - Opal 221": LocData(0x875A42C, "Outback Safari"),
    "Outback Safari - Opal 222": LocData(0x875A42D, "Outback Safari"),
    "Outback Safari - Opal 223": LocData(0x875A42E, "Outback Safari"),
    "Outback Safari - Opal 224": LocData(0x875A42F, "Outback Safari"),
    "Outback Safari - Opal 225": LocData(0x875A430, "Outback Safari"),
    "Outback Safari - Opal 226": LocData(0x875A431, "Outback Safari"),
    "Outback Safari - Opal 227": LocData(0x875A432, "Outback Safari"),
    "Outback Safari - Opal 228": LocData(0x875A433, "Outback Safari"),
    "Outback Safari - Opal 229": LocData(0x875A434, "Outback Safari"),
    "Outback Safari - Opal 230": LocData(0x875A435, "Outback Safari"),
    "Outback Safari - Opal 231": LocData(0x875A436, "Outback Safari"),
    "Outback Safari - Opal 232": LocData(0x875A437, "Outback Safari"),
    "Outback Safari - Opal 233": LocData(0x875A438, "Outback Safari"),
    "Outback Safari - Opal 234": LocData(0x875A439, "Outback Safari"),
    "Outback Safari - Opal 235": LocData(0x875A43A, "Outback Safari"),
    "Outback Safari - Opal 236": LocData(0x875A43B, "Outback Safari"),
    "Outback Safari - Opal 237": LocData(0x875A43C, "Outback Safari"),
    "Outback Safari - Opal 238": LocData(0x875A43D, "Outback Safari"),
    "Outback Safari - Opal 239": LocData(0x875A43E, "Outback Safari"),
    "Outback Safari - Opal 240": LocData(0x875A43F, "Outback Safari"),
    "Outback Safari - Opal 241": LocData(0x875A440, "Outback Safari"),
    "Outback Safari - Opal 242": LocData(0x875A441, "Outback Safari"),
    "Outback Safari - Opal 243": LocData(0x875A442, "Outback Safari"),
    "Outback Safari - Opal 244": LocData(0x875A443, "Outback Safari"),
    "Outback Safari - Opal 245": LocData(0x875A444, "Outback Safari"),
    "Outback Safari - Opal 246": LocData(0x875A445, "Outback Safari"),
    "Outback Safari - Opal 247": LocData(0x875A446, "Outback Safari"),
    "Outback Safari - Opal 248": LocData(0x875A447, "Outback Safari"),
    "Outback Safari - Opal 249": LocData(0x875A448, "Outback Safari"),
    "Outback Safari - Opal 250": LocData(0x875A449, "Outback Safari"),
    "Outback Safari - Opal 251": LocData(0x875A44A, "Outback Safari"),
    "Outback Safari - Opal 252": LocData(0x875A44B, "Outback Safari"),
    "Outback Safari - Opal 253": LocData(0x875A44C, "Outback Safari"),
    "Outback Safari - Opal 254": LocData(0x875A44D, "Outback Safari"),
    "Outback Safari - Opal 255": LocData(0x875A44E, "Outback Safari"),
    "Outback Safari - Opal 256": LocData(0x875A44F, "Outback Safari"),
    "Outback Safari - Opal 257": LocData(0x875A450, "Outback Safari"),
    "Outback Safari - Opal 258": LocData(0x875A451, "Outback Safari"),
    "Outback Safari - Opal 259": LocData(0x875A452, "Outback Safari"),
    "Outback Safari - Opal 260": LocData(0x875A453, "Outback Safari"),
    "Outback Safari - Opal 261": LocData(0x875A454, "Outback Safari"),
    "Outback Safari - Opal 262": LocData(0x875A455, "Outback Safari"),
    "Outback Safari - Opal 263": LocData(0x875A456, "Outback Safari"),
    "Outback Safari - Opal 264": LocData(0x875A457, "Outback Safari"),
    "Outback Safari - Opal 265": LocData(0x875A458, "Outback Safari"),
    "Outback Safari - Opal 266": LocData(0x875A459, "Outback Safari"),
    "Outback Safari - Opal 267": LocData(0x875A45A, "Outback Safari"),
    "Outback Safari - Opal 268": LocData(0x875A45B, "Outback Safari"),
    "Outback Safari - Opal 269": LocData(0x875A45C, "Outback Safari"),
    "Outback Safari - Opal 270": LocData(0x875A45D, "Outback Safari"),
    "Outback Safari - Opal 271": LocData(0x875A45E, "Outback Safari"),
    "Outback Safari - Opal 272": LocData(0x875A45F, "Outback Safari"),
    "Outback Safari - Opal 273": LocData(0x875A460, "Outback Safari"),
    "Outback Safari - Opal 274": LocData(0x875A461, "Outback Safari"),
    "Outback Safari - Opal 275": LocData(0x875A462, "Outback Safari"),
    "Outback Safari - Opal 276": LocData(0x875A463, "Outback Safari"),
    "Outback Safari - Opal 277": LocData(0x875A464, "Outback Safari"),
    "Outback Safari - Opal 278": LocData(0x875A465, "Outback Safari"),
    "Outback Safari - Opal 279": LocData(0x875A466, "Outback Safari"),
    "Outback Safari - Opal 280": LocData(0x875A467, "Outback Safari"),
    "Outback Safari - Opal 281": LocData(0x875A468, "Outback Safari"),
    "Outback Safari - Opal 282": LocData(0x875A469, "Outback Safari"),
    "Outback Safari - Opal 283": LocData(0x875A46A, "Outback Safari"),
    "Outback Safari - Opal 284": LocData(0x875A46B, "Outback Safari"),
    "Outback Safari - Opal 285": LocData(0x875A46C, "Outback Safari"),
    "Outback Safari - Opal 286": LocData(0x875A46D, "Outback Safari"),
    "Outback Safari - Opal 287": LocData(0x875A46E, "Outback Safari"),
    "Outback Safari - Opal 288": LocData(0x875A46F, "Outback Safari"),
    "Outback Safari - Opal 289": LocData(0x875A470, "Outback Safari"),
    "Outback Safari - Opal 290": LocData(0x875A471, "Outback Safari"),
    "Outback Safari - Opal 291": LocData(0x875A472, "Outback Safari"),
    "Outback Safari - Opal 292": LocData(0x875A473, "Outback Safari"),
    "Outback Safari - Opal 293": LocData(0x875A474, "Outback Safari"),
    "Outback Safari - Opal 294": LocData(0x875A475, "Outback Safari"),
    "Outback Safari - Opal 295": LocData(0x875A476, "Outback Safari"),
    "Outback Safari - Opal 296": LocData(0x875A477, "Outback Safari"),
    "Outback Safari - Opal 297": LocData(0x875A478, "Outback Safari"),
    "Outback Safari - Opal 298": LocData(0x875A479, "Outback Safari"),
    "Outback Safari - Opal 299": LocData(0x875A47A, "Outback Safari"),
    "Outback Safari - Opal 300": LocData(0x875A47B, "Outback Safari"),
    "LLPoF - Opal 1": LocData(0x875C350, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 2": LocData(0x875C351, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 3": LocData(0x875C352, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 4": LocData(0x875C353, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 5": LocData(0x875C354, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 6": LocData(0x875C355, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 7": LocData(0x875C356, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 8": LocData(0x875C357, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 9": LocData(0x875C358, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 10": LocData(0x875C359, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 11": LocData(0x875C35A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 12": LocData(0x875C35B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 13": LocData(0x875C35C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 14": LocData(0x875C35D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 15": LocData(0x875C35E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 16": LocData(0x875C35F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 17": LocData(0x875C360, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 18": LocData(0x875C361, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 19": LocData(0x875C362, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 20": LocData(0x875C363, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 21": LocData(0x875C364, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 22": LocData(0x875C365, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 23": LocData(0x875C366, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 24": LocData(0x875C367, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 25": LocData(0x875C368, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 26": LocData(0x875C369, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 27": LocData(0x875C36A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 28": LocData(0x875C36B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 29": LocData(0x875C36C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 30": LocData(0x875C36D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 31": LocData(0x875C36E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 32": LocData(0x875C36F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 33": LocData(0x875C370, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 34": LocData(0x875C371, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 35": LocData(0x875C372, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 36": LocData(0x875C373, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 37": LocData(0x875C374, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 38": LocData(0x875C375, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 39": LocData(0x875C376, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 40": LocData(0x875C377, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 41": LocData(0x875C378, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 42": LocData(0x875C379, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 43": LocData(0x875C37A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 44": LocData(0x875C37B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 45": LocData(0x875C37C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 46": LocData(0x875C37D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 47": LocData(0x875C37E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 48": LocData(0x875C37F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 49": LocData(0x875C380, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 50": LocData(0x875C381, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 51": LocData(0x875C382, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 52": LocData(0x875C383, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 53": LocData(0x875C384, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 54": LocData(0x875C385, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 55": LocData(0x875C386, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 56": LocData(0x875C387, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 57": LocData(0x875C388, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 58": LocData(0x875C389, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 59": LocData(0x875C38A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 60": LocData(0x875C38B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 61": LocData(0x875C38C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 62": LocData(0x875C38D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 63": LocData(0x875C38E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 64": LocData(0x875C38F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 65": LocData(0x875C390, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 66": LocData(0x875C391, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 67": LocData(0x875C392, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 68": LocData(0x875C393, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 69": LocData(0x875C394, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 70": LocData(0x875C395, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 71": LocData(0x875C396, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 72": LocData(0x875C397, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 73": LocData(0x875C398, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 74": LocData(0x875C399, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 75": LocData(0x875C39A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 76": LocData(0x875C39B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 77": LocData(0x875C39C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 78": LocData(0x875C39D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 79": LocData(0x875C39E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 80": LocData(0x875C39F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 81": LocData(0x875C3A0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 82": LocData(0x875C3A1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 83": LocData(0x875C3A2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 84": LocData(0x875C3A3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 85": LocData(0x875C3A4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 86": LocData(0x875C3A5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 87": LocData(0x875C3A6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 88": LocData(0x875C3A7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 89": LocData(0x875C3A8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 90": LocData(0x875C3A9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 91": LocData(0x875C3AA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 92": LocData(0x875C3AB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 93": LocData(0x875C3AC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 94": LocData(0x875C3AD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 95": LocData(0x875C3AE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 96": LocData(0x875C3AF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 97": LocData(0x875C3B0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 98": LocData(0x875C3B1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 99": LocData(0x875C3B2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 100": LocData(0x875C3B3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 101": LocData(0x875C3B4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 102": LocData(0x875C3B5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 103": LocData(0x875C3B6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 104": LocData(0x875C3B7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 105": LocData(0x875C3B8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 106": LocData(0x875C3B9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 107": LocData(0x875C3BA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 108": LocData(0x875C3BB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 109": LocData(0x875C3BC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 110": LocData(0x875C3BD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 111": LocData(0x875C3BE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 112": LocData(0x875C3BF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 113": LocData(0x875C3C0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 114": LocData(0x875C3C1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 115": LocData(0x875C3C2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 116": LocData(0x875C3C3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 117": LocData(0x875C3C4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 118": LocData(0x875C3C5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 119": LocData(0x875C3C6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 120": LocData(0x875C3C7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 121": LocData(0x875C3C8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 122": LocData(0x875C3C9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 123": LocData(0x875C3CA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 124": LocData(0x875C3CB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 125": LocData(0x875C3CC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 126": LocData(0x875C3CD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 127": LocData(0x875C3CE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 128": LocData(0x875C3CF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 129": LocData(0x875C3D0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 130": LocData(0x875C3D1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 131": LocData(0x875C3D2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 132": LocData(0x875C3D3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 133": LocData(0x875C3D4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 134": LocData(0x875C3D5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 135": LocData(0x875C3D6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 136": LocData(0x875C3D7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 137": LocData(0x875C3D8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 138": LocData(0x875C3D9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 139": LocData(0x875C3DA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 140": LocData(0x875C3DB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 141": LocData(0x875C3DC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 142": LocData(0x875C3DD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 143": LocData(0x875C3DE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 144": LocData(0x875C3DF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 145": LocData(0x875C3E0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 146": LocData(0x875C3E1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 147": LocData(0x875C3E2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 148": LocData(0x875C3E3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 149": LocData(0x875C3E4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 150": LocData(0x875C3E5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 151": LocData(0x875C3E6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 152": LocData(0x875C3E7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 153": LocData(0x875C3E8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 154": LocData(0x875C3E9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 155": LocData(0x875C3EA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 156": LocData(0x875C3EB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 157": LocData(0x875C3EC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 158": LocData(0x875C3ED, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 159": LocData(0x875C3EE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 160": LocData(0x875C3EF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 161": LocData(0x875C3F0, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 162": LocData(0x875C3F1, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 163": LocData(0x875C3F2, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 164": LocData(0x875C3F3, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 165": LocData(0x875C3F4, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 166": LocData(0x875C3F5, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 167": LocData(0x875C3F6, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 168": LocData(0x875C3F7, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 169": LocData(0x875C3F8, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 170": LocData(0x875C3F9, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 171": LocData(0x875C3FA, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 172": LocData(0x875C3FB, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 173": LocData(0x875C3FC, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 174": LocData(0x875C3FD, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 175": LocData(0x875C3FE, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 176": LocData(0x875C3FF, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 177": LocData(0x875C400, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 178": LocData(0x875C401, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 179": LocData(0x875C402, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 180": LocData(0x875C403, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 181": LocData(0x875C404, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 182": LocData(0x875C405, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 183": LocData(0x875C406, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 184": LocData(0x875C407, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 185": LocData(0x875C408, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 186": LocData(0x875C409, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 187": LocData(0x875C40A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 188": LocData(0x875C40B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 189": LocData(0x875C40C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 190": LocData(0x875C40D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 191": LocData(0x875C40E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 192": LocData(0x875C40F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 193": LocData(0x875C410, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 194": LocData(0x875C411, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 195": LocData(0x875C412, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 196": LocData(0x875C413, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 197": LocData(0x875C414, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 198": LocData(0x875C415, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 199": LocData(0x875C416, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 200": LocData(0x875C417, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 201": LocData(0x875C418, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 202": LocData(0x875C419, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 203": LocData(0x875C41A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 204": LocData(0x875C41B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 205": LocData(0x875C41C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 206": LocData(0x875C41D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 207": LocData(0x875C41E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 208": LocData(0x875C41F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 209": LocData(0x875C420, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 210": LocData(0x875C421, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 211": LocData(0x875C422, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 212": LocData(0x875C423, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 213": LocData(0x875C424, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 214": LocData(0x875C425, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 215": LocData(0x875C426, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 216": LocData(0x875C427, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 217": LocData(0x875C428, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 218": LocData(0x875C429, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 219": LocData(0x875C42A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 220": LocData(0x875C42B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 221": LocData(0x875C42C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 222": LocData(0x875C42D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 223": LocData(0x875C42E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 224": LocData(0x875C42F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 225": LocData(0x875C430, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 226": LocData(0x875C431, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 227": LocData(0x875C432, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 228": LocData(0x875C433, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 229": LocData(0x875C434, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 230": LocData(0x875C435, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 231": LocData(0x875C436, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 232": LocData(0x875C437, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 233": LocData(0x875C438, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 234": LocData(0x875C439, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 235": LocData(0x875C43A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 236": LocData(0x875C43B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 237": LocData(0x875C43C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 238": LocData(0x875C43D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 239": LocData(0x875C43E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 240": LocData(0x875C43F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 241": LocData(0x875C440, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 242": LocData(0x875C441, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 243": LocData(0x875C442, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 244": LocData(0x875C443, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 245": LocData(0x875C444, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 246": LocData(0x875C445, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 247": LocData(0x875C446, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 248": LocData(0x875C447, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 249": LocData(0x875C448, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 250": LocData(0x875C449, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 251": LocData(0x875C44A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 252": LocData(0x875C44B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 253": LocData(0x875C44C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 254": LocData(0x875C44D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 255": LocData(0x875C44E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 256": LocData(0x875C44F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 257": LocData(0x875C450, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 258": LocData(0x875C451, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 259": LocData(0x875C452, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 260": LocData(0x875C453, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 261": LocData(0x875C454, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 262": LocData(0x875C455, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 263": LocData(0x875C456, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 264": LocData(0x875C457, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 265": LocData(0x875C458, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 266": LocData(0x875C459, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 267": LocData(0x875C45A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 268": LocData(0x875C45B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 269": LocData(0x875C45C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 270": LocData(0x875C45D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 271": LocData(0x875C45E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 272": LocData(0x875C45F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 273": LocData(0x875C460, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 274": LocData(0x875C461, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 275": LocData(0x875C462, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 276": LocData(0x875C463, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 277": LocData(0x875C464, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 278": LocData(0x875C465, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 279": LocData(0x875C466, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 280": LocData(0x875C467, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 281": LocData(0x875C468, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 282": LocData(0x875C469, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 283": LocData(0x875C46A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 284": LocData(0x875C46B, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 285": LocData(0x875C46C, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 286": LocData(0x875C46D, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 287": LocData(0x875C46E, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 288": LocData(0x875C46F, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 289": LocData(0x875C470, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 290": LocData(0x875C471, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 291": LocData(0x875C472, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 292": LocData(0x875C473, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 293": LocData(0x875C474, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 294": LocData(0x875C475, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 295": LocData(0x875C476, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 296": LocData(0x875C477, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 297": LocData(0x875C478, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 298": LocData(0x875C479, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 299": LocData(0x875C47A, "Lyre, Lyre Pants on Fire"),
    "LLPoF - Opal 300": LocData(0x875C47B, "Lyre, Lyre Pants on Fire"),
    "BtBS - Opal 1": LocData(0x875D350, "Beyond the Black Stump"),
    "BtBS - Opal 2": LocData(0x875D351, "Beyond the Black Stump"),
    "BtBS - Opal 3": LocData(0x875D352, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 4": LocData(0x875D353, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 5": LocData(0x875D354, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 6": LocData(0x875D355, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 7": LocData(0x875D356, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 8": LocData(0x875D357, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 9": LocData(0x875D358, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 10": LocData(0x875D359, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 11": LocData(0x875D35A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 12": LocData(0x875D35B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 13": LocData(0x875D35C, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 14": LocData(0x875D35D, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 15": LocData(0x875D35E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 16": LocData(0x875D35F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 17": LocData(0x875D360, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 18": LocData(0x875D361, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 19": LocData(0x875D362, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 20": LocData(0x875D363, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 21": LocData(0x875D364, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 22": LocData(0x875D365, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 23": LocData(0x875D366, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 24": LocData(0x875D367, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 25": LocData(0x875D368, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 26": LocData(0x875D369, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 27": LocData(0x875D36A, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 28": LocData(0x875D36B, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 29": LocData(0x875D36C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 30": LocData(0x875D36D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 31": LocData(0x875D36E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 32": LocData(0x875D36F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 33": LocData(0x875D370, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 34": LocData(0x875D371, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 35": LocData(0x875D372, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 36": LocData(0x875D373, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 37": LocData(0x875D374, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 38": LocData(0x875D375, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 39": LocData(0x875D376, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 40": LocData(0x875D377, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 41": LocData(0x875D378, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 42": LocData(0x875D379, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 43": LocData(0x875D37A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 44": LocData(0x875D37B, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 45": LocData(0x875D37C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 46": LocData(0x875D37D, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 47": LocData(0x875D37E, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 48": LocData(0x875D37F, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 49": LocData(0x875D380, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 50": LocData(0x875D381, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 51": LocData(0x875D382, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 52": LocData(0x875D383, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 53": LocData(0x875D384, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 54": LocData(0x875D385, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 55": LocData(0x875D386, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 56": LocData(0x875D387, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 57": LocData(0x875D388, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 58": LocData(0x875D389, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 59": LocData(0x875D38A, "Beyond the Black Stump"),
    "BtBS - Opal 60": LocData(0x875D38B, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 61": LocData(0x875D38C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 62": LocData(0x875D38D, "Beyond the Black Stump"),
    "BtBS - Opal 63": LocData(0x875D38E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 64": LocData(0x875D38F, "Beyond the Black Stump"),
    "BtBS - Opal 65": LocData(0x875D390, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 66": LocData(0x875D391, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 67": LocData(0x875D392, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 68": LocData(0x875D393, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 69": LocData(0x875D394, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 70": LocData(0x875D395, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 71": LocData(0x875D396, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 72": LocData(0x875D397, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 73": LocData(0x875D398, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 74": LocData(0x875D399, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 75": LocData(0x875D39A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 76": LocData(0x875D39B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 77": LocData(0x875D39C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 78": LocData(0x875D39D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 79": LocData(0x875D39E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 80": LocData(0x875D39F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 81": LocData(0x875D3A0, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 82": LocData(0x875D3A1, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 83": LocData(0x875D3A2, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 84": LocData(0x875D3A3, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 85": LocData(0x875D3A4, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 86": LocData(0x875D3A5, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 87": LocData(0x875D3A6, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 88": LocData(0x875D3A7, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 89": LocData(0x875D3A8, "Beyond the Black Stump"),
    "BtBS - Opal 90": LocData(0x875D3A9, "Beyond the Black Stump"),
    "BtBS - Opal 91": LocData(0x875D3AA, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 92": LocData(0x875D3AB, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 93": LocData(0x875D3AC, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 94": LocData(0x875D3AD, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 95": LocData(0x875D3AE, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 96": LocData(0x875D3AF, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 97": LocData(0x875D3B0, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 98": LocData(0x875D3B1, "Beyond the Black Stump"),
    "BtBS - Opal 99": LocData(0x875D3B2, "Beyond the Black Stump"),
    "BtBS - Opal 100": LocData(0x875D3B3, "Beyond the Black Stump"),
    "BtBS - Opal 101": LocData(0x875D3B4, "Beyond the Black Stump"),
    "BtBS - Opal 102": LocData(0x875D3B5, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 103": LocData(0x875D3B6, "Beyond the Black Stump"),
    "BtBS - Opal 104": LocData(0x875D3B7, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 105": LocData(0x875D3B8, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 106": LocData(0x875D3B9, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 107": LocData(0x875D3BA, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 108": LocData(0x875D3BB, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 109": LocData(0x875D3BC, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 110": LocData(0x875D3BD, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 111": LocData(0x875D3BE, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 112": LocData(0x875D3BF, "Beyond the Black Stump"),
    "BtBS - Opal 113": LocData(0x875D3C0, "Beyond the Black Stump"),
    "BtBS - Opal 114": LocData(0x875D3C1, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 115": LocData(0x875D3C2, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 116": LocData(0x875D3C3, "Beyond the Black Stump"),
    "BtBS - Opal 117": LocData(0x875D3C4, "Beyond the Black Stump"),
    "BtBS - Opal 118": LocData(0x875D3C5, "Beyond the Black Stump"),
    "BtBS - Opal 119": LocData(0x875D3C6, "Beyond the Black Stump"),
    "BtBS - Opal 120": LocData(0x875D3C7, "Beyond the Black Stump"),
    "BtBS - Opal 121": LocData(0x875D3C8, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 122": LocData(0x875D3C9, "Beyond the Black Stump"),
    "BtBS - Opal 123": LocData(0x875D3CA, "Beyond the Black Stump"),
    "BtBS - Opal 124": LocData(0x875D3CB, "Beyond the Black Stump"),
    "BtBS - Opal 125": LocData(0x875D3CC, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 126": LocData(0x875D3CD, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 127": LocData(0x875D3CE, "Beyond the Black Stump - Glide Behind the Mountain"),
    "BtBS - Opal 128": LocData(0x875D3CF, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 129": LocData(0x875D3D0, "Beyond the Black Stump"),
    "BtBS - Opal 130": LocData(0x875D3D1, "Beyond the Black Stump"),
    "BtBS - Opal 131": LocData(0x875D3D2, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 132": LocData(0x875D3D3, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 133": LocData(0x875D3D4, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 134": LocData(0x875D3D5, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 135": LocData(0x875D3D6, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 136": LocData(0x875D3D7, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 137": LocData(0x875D3D8, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 138": LocData(0x875D3D9, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 139": LocData(0x875D3DA, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 140": LocData(0x875D3DB, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 141": LocData(0x875D3DC, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 142": LocData(0x875D3DD, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 143": LocData(0x875D3DE, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 144": LocData(0x875D3DF, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 145": LocData(0x875D3E0, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 146": LocData(0x875D3E1, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 147": LocData(0x875D3E2, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 148": LocData(0x875D3E3, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 149": LocData(0x875D3E4, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 150": LocData(0x875D3E5, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 151": LocData(0x875D3E6, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 152": LocData(0x875D3E7, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 153": LocData(0x875D3E8, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 154": LocData(0x875D3E9, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 155": LocData(0x875D3EA, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 156": LocData(0x875D3EB, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 157": LocData(0x875D3EC, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 158": LocData(0x875D3ED, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 159": LocData(0x875D3EE, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 160": LocData(0x875D3EF, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 161": LocData(0x875D3F0, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 162": LocData(0x875D3F1, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 163": LocData(0x875D3F2, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 164": LocData(0x875D3F3, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 165": LocData(0x875D3F4, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 166": LocData(0x875D3F5, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 167": LocData(0x875D3F6, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 168": LocData(0x875D3F7, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 169": LocData(0x875D3F8, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 170": LocData(0x875D3F9, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 171": LocData(0x875D3FA, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 172": LocData(0x875D3FB, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 173": LocData(0x875D3FC, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 174": LocData(0x875D3FD, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 175": LocData(0x875D3FE, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 176": LocData(0x875D3FF, "Beyond the Black Stump"),
    "BtBS - Opal 177": LocData(0x875D400, "Beyond the Black Stump"),
    "BtBS - Opal 178": LocData(0x875D401, "Beyond the Black Stump"),
    "BtBS - Opal 179": LocData(0x875D402, "Beyond the Black Stump"),
    "BtBS - Opal 180": LocData(0x875D403, "Beyond the Black Stump"),
    "BtBS - Opal 181": LocData(0x875D404, "Beyond the Black Stump"),
    "BtBS - Opal 182": LocData(0x875D405, "Beyond the Black Stump"),
    "BtBS - Opal 183": LocData(0x875D406, "Beyond the Black Stump"),
    "BtBS - Opal 184": LocData(0x875D407, "Beyond the Black Stump"),
    "BtBS - Opal 185": LocData(0x875D408, "Beyond the Black Stump"),
    "BtBS - Opal 186": LocData(0x875D409, "Beyond the Black Stump"),
    "BtBS - Opal 187": LocData(0x875D40A, "Beyond the Black Stump"),
    "BtBS - Opal 188": LocData(0x875D40B, "Beyond the Black Stump"),
    "BtBS - Opal 189": LocData(0x875D40C, "Beyond the Black Stump"),
    "BtBS - Opal 190": LocData(0x875D40D, "Beyond the Black Stump"),
    "BtBS - Opal 191": LocData(0x875D40E, "Beyond the Black Stump"),
    "BtBS - Opal 192": LocData(0x875D40F, "Beyond the Black Stump"),
    "BtBS - Opal 193": LocData(0x875D410, "Beyond the Black Stump"),
    "BtBS - Opal 194": LocData(0x875D411, "Beyond the Black Stump"),
    "BtBS - Opal 195": LocData(0x875D412, "Beyond the Black Stump"),
    "BtBS - Opal 196": LocData(0x875D413, "Beyond the Black Stump"),
    "BtBS - Opal 197": LocData(0x875D414, "Beyond the Black Stump"),
    "BtBS - Opal 198": LocData(0x875D415, "Beyond the Black Stump"),
    "BtBS - Opal 199": LocData(0x875D416, "Beyond the Black Stump"),
    "BtBS - Opal 200": LocData(0x875D417, "Beyond the Black Stump"),
    "BtBS - Opal 201": LocData(0x875D418, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 202": LocData(0x875D419, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 203": LocData(0x875D41A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 204": LocData(0x875D41B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 205": LocData(0x875D41C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 206": LocData(0x875D41D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 207": LocData(0x875D41E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 208": LocData(0x875D41F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 209": LocData(0x875D420, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 210": LocData(0x875D421, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 211": LocData(0x875D422, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 212": LocData(0x875D423, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 213": LocData(0x875D424, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 214": LocData(0x875D425, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 215": LocData(0x875D426, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 216": LocData(0x875D427, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 217": LocData(0x875D428, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 218": LocData(0x875D429, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 219": LocData(0x875D42A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 220": LocData(0x875D42B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 221": LocData(0x875D42C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 222": LocData(0x875D42D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 223": LocData(0x875D42E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 224": LocData(0x875D42F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 225": LocData(0x875D430, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 226": LocData(0x875D431, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 227": LocData(0x875D432, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 228": LocData(0x875D433, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 229": LocData(0x875D434, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 230": LocData(0x875D435, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 231": LocData(0x875D436, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 232": LocData(0x875D437, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 233": LocData(0x875D438, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 234": LocData(0x875D439, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 235": LocData(0x875D43A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 236": LocData(0x875D43B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 237": LocData(0x875D43C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 238": LocData(0x875D43D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 239": LocData(0x875D43E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 240": LocData(0x875D43F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 241": LocData(0x875D440, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 242": LocData(0x875D441, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 243": LocData(0x875D442, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 244": LocData(0x875D443, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 245": LocData(0x875D444, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 246": LocData(0x875D445, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 247": LocData(0x875D446, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 248": LocData(0x875D447, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 249": LocData(0x875D448, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 250": LocData(0x875D449, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 251": LocData(0x875D44A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 252": LocData(0x875D44B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 253": LocData(0x875D44C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 254": LocData(0x875D44D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 255": LocData(0x875D44E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 256": LocData(0x875D44F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 257": LocData(0x875D450, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 258": LocData(0x875D451, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 259": LocData(0x875D452, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 260": LocData(0x875D453, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 261": LocData(0x875D454, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 262": LocData(0x875D455, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 263": LocData(0x875D456, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 264": LocData(0x875D457, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 265": LocData(0x875D458, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 266": LocData(0x875D459, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 267": LocData(0x875D45A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 268": LocData(0x875D45B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 269": LocData(0x875D45C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 270": LocData(0x875D45D, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 271": LocData(0x875D45E, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 272": LocData(0x875D45F, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 273": LocData(0x875D460, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 274": LocData(0x875D461, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 275": LocData(0x875D462, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 276": LocData(0x875D463, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 277": LocData(0x875D464, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 278": LocData(0x875D465, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 279": LocData(0x875D466, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 280": LocData(0x875D467, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 281": LocData(0x875D468, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 282": LocData(0x875D469, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 283": LocData(0x875D46A, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 284": LocData(0x875D46B, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 285": LocData(0x875D46C, "Beyond the Black Stump - Upper Area"),
    "BtBS - Opal 286": LocData(0x875D46D, "Beyond the Black Stump"),
    "BtBS - Opal 287": LocData(0x875D46E, "Beyond the Black Stump"),
    "BtBS - Opal 288": LocData(0x875D46F, "Beyond the Black Stump"),
    "BtBS - Opal 289": LocData(0x875D470, "Beyond the Black Stump"),
    "BtBS - Opal 290": LocData(0x875D471, "Beyond the Black Stump"),
    "BtBS - Opal 291": LocData(0x875D472, "Beyond the Black Stump"),
    "BtBS - Opal 292": LocData(0x875D473, "Beyond the Black Stump"),
    "BtBS - Opal 293": LocData(0x875D474, "Beyond the Black Stump"),
    "BtBS - Opal 294": LocData(0x875D475, "Beyond the Black Stump"),
    "BtBS - Opal 295": LocData(0x875D476, "Beyond the Black Stump"),
    "BtBS - Opal 296": LocData(0x875D477, "Beyond the Black Stump"),
    "BtBS - Opal 297": LocData(0x875D478, "Beyond the Black Stump"),
    "BtBS - Opal 298": LocData(0x875D479, "Beyond the Black Stump"),
    "BtBS - Opal 299": LocData(0x875D47A, "Beyond the Black Stump"),
    "BtBS - Opal 300": LocData(0x875D47B, "Beyond the Black Stump"),
    "RMtS - Opal 1": LocData(0x875E350, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 2": LocData(0x875E351, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 3": LocData(0x875E352, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 4": LocData(0x875E353, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 5": LocData(0x875E354, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 6": LocData(0x875E355, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 7": LocData(0x875E356, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 8": LocData(0x875E357, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 9": LocData(0x875E358, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 10": LocData(0x875E359, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 11": LocData(0x875E35A, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 12": LocData(0x875E35B, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 13": LocData(0x875E35C, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 14": LocData(0x875E35D, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 15": LocData(0x875E35E, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 16": LocData(0x875E35F, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 17": LocData(0x875E360, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 18": LocData(0x875E361, "Rex Marks the Spot"),
    "RMtS - Opal 19": LocData(0x875E362, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 20": LocData(0x875E363, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 21": LocData(0x875E364, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 22": LocData(0x875E365, "Rex Marks the Spot"),
    "RMtS - Opal 23": LocData(0x875E366, "Rex Marks the Spot"),
    "RMtS - Opal 24": LocData(0x875E367, "Rex Marks the Spot"),
    "RMtS - Opal 25": LocData(0x875E368, "Rex Marks the Spot"),
    "RMtS - Opal 26": LocData(0x875E369, "Rex Marks the Spot"),
    "RMtS - Opal 27": LocData(0x875E36A, "Rex Marks the Spot"),
    "RMtS - Opal 28": LocData(0x875E36B, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 29": LocData(0x875E36C, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 30": LocData(0x875E36D, "Rex Marks the Spot"),
    "RMtS - Opal 31": LocData(0x875E36E, "Rex Marks the Spot"),
    "RMtS - Opal 32": LocData(0x875E36F, "Rex Marks the Spot"),
    "RMtS - Opal 33": LocData(0x875E370, "Rex Marks the Spot"),
    "RMtS - Opal 34": LocData(0x875E371, "Rex Marks the Spot"),
    "RMtS - Opal 35": LocData(0x875E372, "Rex Marks the Spot"),
    "RMtS - Opal 36": LocData(0x875E373, "Rex Marks the Spot"),
    "RMtS - Opal 37": LocData(0x875E374, "Rex Marks the Spot"),
    "RMtS - Opal 38": LocData(0x875E375, "Rex Marks the Spot"),
    "RMtS - Opal 39": LocData(0x875E376, "Rex Marks the Spot"),
    "RMtS - Opal 40": LocData(0x875E377, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 41": LocData(0x875E378, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 42": LocData(0x875E379, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 43": LocData(0x875E37A, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 44": LocData(0x875E37B, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 45": LocData(0x875E37C, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 46": LocData(0x875E37D, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 47": LocData(0x875E37E, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 48": LocData(0x875E37F, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 49": LocData(0x875E380, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 50": LocData(0x875E381, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 51": LocData(0x875E382, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 52": LocData(0x875E383, "Rex Marks the Spot"),
    "RMtS - Opal 53": LocData(0x875E384, "Rex Marks the Spot"),
    "RMtS - Opal 54": LocData(0x875E385, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 55": LocData(0x875E386, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 56": LocData(0x875E387, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 57": LocData(0x875E388, "Rex Marks the Spot"),
    "RMtS - Opal 58": LocData(0x875E389, "Rex Marks the Spot"),
    "RMtS - Opal 59": LocData(0x875E38A, "Rex Marks the Spot"),
    "RMtS - Opal 60": LocData(0x875E38B, "Rex Marks the Spot"),
    "RMtS - Opal 61": LocData(0x875E38C, "Rex Marks the Spot"),
    "RMtS - Opal 62": LocData(0x875E38D, "Rex Marks the Spot"),
    "RMtS - Opal 63": LocData(0x875E38E, "Rex Marks the Spot"),
    "RMtS - Opal 64": LocData(0x875E38F, "Rex Marks the Spot"),
    "RMtS - Opal 65": LocData(0x875E390, "Rex Marks the Spot"),
    "RMtS - Opal 66": LocData(0x875E391, "Rex Marks the Spot"),
    "RMtS - Opal 67": LocData(0x875E392, "Rex Marks the Spot"),
    "RMtS - Opal 68": LocData(0x875E393, "Rex Marks the Spot"),
    "RMtS - Opal 69": LocData(0x875E394, "Rex Marks the Spot"),
    "RMtS - Opal 70": LocData(0x875E395, "Rex Marks the Spot"),
    "RMtS - Opal 71": LocData(0x875E396, "Rex Marks the Spot"),
    "RMtS - Opal 72": LocData(0x875E397, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 73": LocData(0x875E398, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 74": LocData(0x875E399, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 75": LocData(0x875E39A, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 76": LocData(0x875E39B, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 77": LocData(0x875E39C, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 78": LocData(0x875E39D, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 79": LocData(0x875E39E, "Rex Marks the Spot - Underwater"),
    "RMtS - Opal 80": LocData(0x875E39F, "Rex Marks the Spot"),
    "RMtS - Opal 81": LocData(0x875E3A0, "Rex Marks the Spot"),
    "RMtS - Opal 82": LocData(0x875E3A1, "Rex Marks the Spot"),
    "RMtS - Opal 83": LocData(0x875E3A2, "Rex Marks the Spot"),
    "RMtS - Opal 84": LocData(0x875E3A3, "Rex Marks the Spot"),
    "RMtS - Opal 85": LocData(0x875E3A4, "Rex Marks the Spot"),
    "RMtS - Opal 86": LocData(0x875E3A5, "Rex Marks the Spot"),
    "RMtS - Opal 87": LocData(0x875E3A6, "Rex Marks the Spot"),
    "RMtS - Opal 88": LocData(0x875E3A7, "Rex Marks the Spot"),
    "RMtS - Opal 89": LocData(0x875E3A8, "Rex Marks the Spot"),
    "RMtS - Opal 90": LocData(0x875E3A9, "Rex Marks the Spot"),
    "RMtS - Opal 91": LocData(0x875E3AA, "Rex Marks the Spot"),
    "RMtS - Opal 92": LocData(0x875E3AB, "Rex Marks the Spot"),
    "RMtS - Opal 93": LocData(0x875E3AC, "Rex Marks the Spot"),
    "RMtS - Opal 94": LocData(0x875E3AD, "Rex Marks the Spot"),
    "RMtS - Opal 95": LocData(0x875E3AE, "Rex Marks the Spot"),
    "RMtS - Opal 96": LocData(0x875E3AF, "Rex Marks the Spot"),
    "RMtS - Opal 97": LocData(0x875E3B0, "Rex Marks the Spot"),
    "RMtS - Opal 98": LocData(0x875E3B1, "Rex Marks the Spot"),
    "RMtS - Opal 99": LocData(0x875E3B2, "Rex Marks the Spot"),
    "RMtS - Opal 100": LocData(0x875E3B3, "Rex Marks the Spot"),
    "RMtS - Opal 101": LocData(0x875E3B4, "Rex Marks the Spot"),
    "RMtS - Opal 102": LocData(0x875E3B5, "Rex Marks the Spot"),
    "RMtS - Opal 103": LocData(0x875E3B6, "Rex Marks the Spot"),
    "RMtS - Opal 104": LocData(0x875E3B7, "Rex Marks the Spot"),
    "RMtS - Opal 105": LocData(0x875E3B8, "Rex Marks the Spot"),
    "RMtS - Opal 106": LocData(0x875E3B9, "Rex Marks the Spot"),
    "RMtS - Opal 107": LocData(0x875E3BA, "Rex Marks the Spot"),
    "RMtS - Opal 108": LocData(0x875E3BB, "Rex Marks the Spot"),
    "RMtS - Opal 109": LocData(0x875E3BC, "Rex Marks the Spot"),
    "RMtS - Opal 110": LocData(0x875E3BD, "Rex Marks the Spot"),
    "RMtS - Opal 111": LocData(0x875E3BE, "Rex Marks the Spot"),
    "RMtS - Opal 112": LocData(0x875E3BF, "Rex Marks the Spot"),
    "RMtS - Opal 113": LocData(0x875E3C0, "Rex Marks the Spot"),
    "RMtS - Opal 114": LocData(0x875E3C1, "Rex Marks the Spot"),
    "RMtS - Opal 115": LocData(0x875E3C2, "Rex Marks the Spot"),
    "RMtS - Opal 116": LocData(0x875E3C3, "Rex Marks the Spot"),
    "RMtS - Opal 117": LocData(0x875E3C4, "Rex Marks the Spot"),
    "RMtS - Opal 118": LocData(0x875E3C5, "Rex Marks the Spot"),
    "RMtS - Opal 119": LocData(0x875E3C6, "Rex Marks the Spot"),
    "RMtS - Opal 120": LocData(0x875E3C7, "Rex Marks the Spot"),
    "RMtS - Opal 121": LocData(0x875E3C8, "Rex Marks the Spot"),
    "RMtS - Opal 122": LocData(0x875E3C9, "Rex Marks the Spot"),
    "RMtS - Opal 123": LocData(0x875E3CA, "Rex Marks the Spot"),
    "RMtS - Opal 124": LocData(0x875E3CB, "Rex Marks the Spot"),
    "RMtS - Opal 125": LocData(0x875E3CC, "Rex Marks the Spot"),
    "RMtS - Opal 126": LocData(0x875E3CD, "Rex Marks the Spot"),
    "RMtS - Opal 127": LocData(0x875E3CE, "Rex Marks the Spot"),
    "RMtS - Opal 128": LocData(0x875E3CF, "Rex Marks the Spot"),
    "RMtS - Opal 129": LocData(0x875E3D0, "Rex Marks the Spot"),
    "RMtS - Opal 130": LocData(0x875E3D1, "Rex Marks the Spot"),
    "RMtS - Opal 131": LocData(0x875E3D2, "Rex Marks the Spot"),
    "RMtS - Opal 132": LocData(0x875E3D3, "Rex Marks the Spot"),
    "RMtS - Opal 133": LocData(0x875E3D4, "Rex Marks the Spot"),
    "RMtS - Opal 134": LocData(0x875E3D5, "Rex Marks the Spot"),
    "RMtS - Opal 135": LocData(0x875E3D6, "Rex Marks the Spot"),
    "RMtS - Opal 136": LocData(0x875E3D7, "Rex Marks the Spot"),
    "RMtS - Opal 137": LocData(0x875E3D8, "Rex Marks the Spot"),
    "RMtS - Opal 138": LocData(0x875E3D9, "Rex Marks the Spot"),
    "RMtS - Opal 139": LocData(0x875E3DA, "Rex Marks the Spot"),
    "RMtS - Opal 140": LocData(0x875E3DB, "Rex Marks the Spot"),
    "RMtS - Opal 141": LocData(0x875E3DC, "Rex Marks the Spot"),
    "RMtS - Opal 142": LocData(0x875E3DD, "Rex Marks the Spot"),
    "RMtS - Opal 143": LocData(0x875E3DE, "Rex Marks the Spot"),
    "RMtS - Opal 144": LocData(0x875E3DF, "Rex Marks the Spot"),
    "RMtS - Opal 145": LocData(0x875E3E0, "Rex Marks the Spot"),
    "RMtS - Opal 146": LocData(0x875E3E1, "Rex Marks the Spot"),
    "RMtS - Opal 147": LocData(0x875E3E2, "Rex Marks the Spot"),
    "RMtS - Opal 148": LocData(0x875E3E3, "Rex Marks the Spot"),
    "RMtS - Opal 149": LocData(0x875E3E4, "Rex Marks the Spot"),
    "RMtS - Opal 150": LocData(0x875E3E5, "Rex Marks the Spot"),
    "RMtS - Opal 151": LocData(0x875E3E6, "Rex Marks the Spot"),
    "RMtS - Opal 152": LocData(0x875E3E7, "Rex Marks the Spot"),
    "RMtS - Opal 153": LocData(0x875E3E8, "Rex Marks the Spot"),
    "RMtS - Opal 154": LocData(0x875E3E9, "Rex Marks the Spot"),
    "RMtS - Opal 155": LocData(0x875E3EA, "Rex Marks the Spot"),
    "RMtS - Opal 156": LocData(0x875E3EB, "Rex Marks the Spot"),
    "RMtS - Opal 157": LocData(0x875E3EC, "Rex Marks the Spot"),
    "RMtS - Opal 158": LocData(0x875E3ED, "Rex Marks the Spot"),
    "RMtS - Opal 159": LocData(0x875E3EE, "Rex Marks the Spot"),
    "RMtS - Opal 160": LocData(0x875E3EF, "Rex Marks the Spot"),
    "RMtS - Opal 161": LocData(0x875E3F0, "Rex Marks the Spot"),
    "RMtS - Opal 162": LocData(0x875E3F1, "Rex Marks the Spot"),
    "RMtS - Opal 163": LocData(0x875E3F2, "Rex Marks the Spot"),
    "RMtS - Opal 164": LocData(0x875E3F3, "Rex Marks the Spot"),
    "RMtS - Opal 165": LocData(0x875E3F4, "Rex Marks the Spot"),
    "RMtS - Opal 166": LocData(0x875E3F5, "Rex Marks the Spot"),
    "RMtS - Opal 167": LocData(0x875E3F6, "Rex Marks the Spot"),
    "RMtS - Opal 168": LocData(0x875E3F7, "Rex Marks the Spot"),
    "RMtS - Opal 169": LocData(0x875E3F8, "Rex Marks the Spot"),
    "RMtS - Opal 170": LocData(0x875E3F9, "Rex Marks the Spot"),
    "RMtS - Opal 171": LocData(0x875E3FA, "Rex Marks the Spot"),
    "RMtS - Opal 172": LocData(0x875E3FB, "Rex Marks the Spot"),
    "RMtS - Opal 173": LocData(0x875E3FC, "Rex Marks the Spot"),
    "RMtS - Opal 174": LocData(0x875E3FD, "Rex Marks the Spot"),
    "RMtS - Opal 175": LocData(0x875E3FE, "Rex Marks the Spot"),
    "RMtS - Opal 176": LocData(0x875E3FF, "Rex Marks the Spot"),
    "RMtS - Opal 177": LocData(0x875E400, "Rex Marks the Spot"),
    "RMtS - Opal 178": LocData(0x875E401, "Rex Marks the Spot"),
    "RMtS - Opal 179": LocData(0x875E402, "Rex Marks the Spot"),
    "RMtS - Opal 180": LocData(0x875E403, "Rex Marks the Spot"),
    "RMtS - Opal 181": LocData(0x875E404, "Rex Marks the Spot"),
    "RMtS - Opal 182": LocData(0x875E405, "Rex Marks the Spot"),
    "RMtS - Opal 183": LocData(0x875E406, "Rex Marks the Spot"),
    "RMtS - Opal 184": LocData(0x875E407, "Rex Marks the Spot"),
    "RMtS - Opal 185": LocData(0x875E408, "Rex Marks the Spot"),
    "RMtS - Opal 186": LocData(0x875E409, "Rex Marks the Spot"),
    "RMtS - Opal 187": LocData(0x875E40A, "Rex Marks the Spot"),
    "RMtS - Opal 188": LocData(0x875E40B, "Rex Marks the Spot"),
    "RMtS - Opal 189": LocData(0x875E40C, "Rex Marks the Spot"),
    "RMtS - Opal 190": LocData(0x875E40D, "Rex Marks the Spot"),
    "RMtS - Opal 191": LocData(0x875E40E, "Rex Marks the Spot"),
    "RMtS - Opal 192": LocData(0x875E40F, "Rex Marks the Spot"),
    "RMtS - Opal 193": LocData(0x875E410, "Rex Marks the Spot"),
    "RMtS - Opal 194": LocData(0x875E411, "Rex Marks the Spot"),
    "RMtS - Opal 195": LocData(0x875E412, "Rex Marks the Spot"),
    "RMtS - Opal 196": LocData(0x875E413, "Rex Marks the Spot"),
    "RMtS - Opal 197": LocData(0x875E414, "Rex Marks the Spot"),
    "RMtS - Opal 198": LocData(0x875E415, "Rex Marks the Spot"),
    "RMtS - Opal 199": LocData(0x875E416, "Rex Marks the Spot"),
    "RMtS - Opal 200": LocData(0x875E417, "Rex Marks the Spot"),
    "RMtS - Opal 201": LocData(0x875E418, "Rex Marks the Spot"),
    "RMtS - Opal 202": LocData(0x875E419, "Rex Marks the Spot"),
    "RMtS - Opal 203": LocData(0x875E41A, "Rex Marks the Spot"),
    "RMtS - Opal 204": LocData(0x875E41B, "Rex Marks the Spot"),
    "RMtS - Opal 205": LocData(0x875E41C, "Rex Marks the Spot"),
    "RMtS - Opal 206": LocData(0x875E41D, "Rex Marks the Spot"),
    "RMtS - Opal 207": LocData(0x875E41E, "Rex Marks the Spot"),
    "RMtS - Opal 208": LocData(0x875E41F, "Rex Marks the Spot"),
    "RMtS - Opal 209": LocData(0x875E420, "Rex Marks the Spot"),
    "RMtS - Opal 210": LocData(0x875E421, "Rex Marks the Spot"),
    "RMtS - Opal 211": LocData(0x875E422, "Rex Marks the Spot"),
    "RMtS - Opal 212": LocData(0x875E423, "Rex Marks the Spot"),
    "RMtS - Opal 213": LocData(0x875E424, "Rex Marks the Spot"),
    "RMtS - Opal 214": LocData(0x875E425, "Rex Marks the Spot"),
    "RMtS - Opal 215": LocData(0x875E426, "Rex Marks the Spot"),
    "RMtS - Opal 216": LocData(0x875E427, "Rex Marks the Spot"),
    "RMtS - Opal 217": LocData(0x875E428, "Rex Marks the Spot"),
    "RMtS - Opal 218": LocData(0x875E429, "Rex Marks the Spot"),
    "RMtS - Opal 219": LocData(0x875E42A, "Rex Marks the Spot"),
    "RMtS - Opal 220": LocData(0x875E42B, "Rex Marks the Spot"),
    "RMtS - Opal 221": LocData(0x875E42C, "Rex Marks the Spot"),
    "RMtS - Opal 222": LocData(0x875E42D, "Rex Marks the Spot"),
    "RMtS - Opal 223": LocData(0x875E42E, "Rex Marks the Spot"),
    "RMtS - Opal 224": LocData(0x875E42F, "Rex Marks the Spot"),
    "RMtS - Opal 225": LocData(0x875E430, "Rex Marks the Spot"),
    "RMtS - Opal 226": LocData(0x875E431, "Rex Marks the Spot"),
    "RMtS - Opal 227": LocData(0x875E432, "Rex Marks the Spot"),
    "RMtS - Opal 228": LocData(0x875E433, "Rex Marks the Spot"),
    "RMtS - Opal 229": LocData(0x875E434, "Rex Marks the Spot"),
    "RMtS - Opal 230": LocData(0x875E435, "Rex Marks the Spot"),
    "RMtS - Opal 231": LocData(0x875E436, "Rex Marks the Spot"),
    "RMtS - Opal 232": LocData(0x875E437, "Rex Marks the Spot"),
    "RMtS - Opal 233": LocData(0x875E438, "Rex Marks the Spot"),
    "RMtS - Opal 234": LocData(0x875E439, "Rex Marks the Spot"),
    "RMtS - Opal 235": LocData(0x875E43A, "Rex Marks the Spot"),
    "RMtS - Opal 236": LocData(0x875E43B, "Rex Marks the Spot"),
    "RMtS - Opal 237": LocData(0x875E43C, "Rex Marks the Spot"),
    "RMtS - Opal 238": LocData(0x875E43D, "Rex Marks the Spot"),
    "RMtS - Opal 239": LocData(0x875E43E, "Rex Marks the Spot"),
    "RMtS - Opal 240": LocData(0x875E43F, "Rex Marks the Spot"),
    "RMtS - Opal 241": LocData(0x875E440, "Rex Marks the Spot"),
    "RMtS - Opal 242": LocData(0x875E441, "Rex Marks the Spot"),
    "RMtS - Opal 243": LocData(0x875E442, "Rex Marks the Spot"),
    "RMtS - Opal 244": LocData(0x875E443, "Rex Marks the Spot"),
    "RMtS - Opal 245": LocData(0x875E444, "Rex Marks the Spot"),
    "RMtS - Opal 246": LocData(0x875E445, "Rex Marks the Spot"),
    "RMtS - Opal 247": LocData(0x875E446, "Rex Marks the Spot"),
    "RMtS - Opal 248": LocData(0x875E447, "Rex Marks the Spot"),
    "RMtS - Opal 249": LocData(0x875E448, "Rex Marks the Spot"),
    "RMtS - Opal 250": LocData(0x875E449, "Rex Marks the Spot"),
    "RMtS - Opal 251": LocData(0x875E44A, "Rex Marks the Spot"),
    "RMtS - Opal 252": LocData(0x875E44B, "Rex Marks the Spot"),
    "RMtS - Opal 253": LocData(0x875E44C, "Rex Marks the Spot"),
    "RMtS - Opal 254": LocData(0x875E44D, "Rex Marks the Spot"),
    "RMtS - Opal 255": LocData(0x875E44E, "Rex Marks the Spot"),
    "RMtS - Opal 256": LocData(0x875E44F, "Rex Marks the Spot"),
    "RMtS - Opal 257": LocData(0x875E450, "Rex Marks the Spot"),
    "RMtS - Opal 258": LocData(0x875E451, "Rex Marks the Spot"),
    "RMtS - Opal 259": LocData(0x875E452, "Rex Marks the Spot"),
    "RMtS - Opal 260": LocData(0x875E453, "Rex Marks the Spot"),
    "RMtS - Opal 261": LocData(0x875E454, "Rex Marks the Spot"),
    "RMtS - Opal 262": LocData(0x875E455, "Rex Marks the Spot"),
    "RMtS - Opal 263": LocData(0x875E456, "Rex Marks the Spot"),
    "RMtS - Opal 264": LocData(0x875E457, "Rex Marks the Spot"),
    "RMtS - Opal 265": LocData(0x875E458, "Rex Marks the Spot"),
    "RMtS - Opal 266": LocData(0x875E459, "Rex Marks the Spot"),
    "RMtS - Opal 267": LocData(0x875E45A, "Rex Marks the Spot"),
    "RMtS - Opal 268": LocData(0x875E45B, "Rex Marks the Spot"),
    "RMtS - Opal 269": LocData(0x875E45C, "Rex Marks the Spot"),
    "RMtS - Opal 270": LocData(0x875E45D, "Rex Marks the Spot"),
    "RMtS - Opal 271": LocData(0x875E45E, "Rex Marks the Spot"),
    "RMtS - Opal 272": LocData(0x875E45F, "Rex Marks the Spot"),
    "RMtS - Opal 273": LocData(0x875E460, "Rex Marks the Spot"),
    "RMtS - Opal 274": LocData(0x875E461, "Rex Marks the Spot"),
    "RMtS - Opal 275": LocData(0x875E462, "Rex Marks the Spot"),
    "RMtS - Opal 276": LocData(0x875E463, "Rex Marks the Spot"),
    "RMtS - Opal 277": LocData(0x875E464, "Rex Marks the Spot"),
    "RMtS - Opal 278": LocData(0x875E465, "Rex Marks the Spot"),
    "RMtS - Opal 279": LocData(0x875E466, "Rex Marks the Spot"),
    "RMtS - Opal 280": LocData(0x875E467, "Rex Marks the Spot"),
    "RMtS - Opal 281": LocData(0x875E468, "Rex Marks the Spot"),
    "RMtS - Opal 282": LocData(0x875E469, "Rex Marks the Spot"),
    "RMtS - Opal 283": LocData(0x875E46A, "Rex Marks the Spot"),
    "RMtS - Opal 284": LocData(0x875E46B, "Rex Marks the Spot"),
    "RMtS - Opal 285": LocData(0x875E46C, "Rex Marks the Spot"),
    "RMtS - Opal 286": LocData(0x875E46D, "Rex Marks the Spot"),
    "RMtS - Opal 287": LocData(0x875E46E, "Rex Marks the Spot"),
    "RMtS - Opal 288": LocData(0x875E46F, "Rex Marks the Spot"),
    "RMtS - Opal 289": LocData(0x875E470, "Rex Marks the Spot"),
    "RMtS - Opal 290": LocData(0x875E471, "Rex Marks the Spot"),
    "RMtS - Opal 291": LocData(0x875E472, "Rex Marks the Spot"),
    "RMtS - Opal 292": LocData(0x875E473, "Rex Marks the Spot"),
    "RMtS - Opal 293": LocData(0x875E474, "Rex Marks the Spot"),
    "RMtS - Opal 294": LocData(0x875E475, "Rex Marks the Spot"),
    "RMtS - Opal 295": LocData(0x875E476, "Rex Marks the Spot"),
    "RMtS - Opal 296": LocData(0x875E477, "Rex Marks the Spot"),
    "RMtS - Opal 297": LocData(0x875E478, "Rex Marks the Spot"),
    "RMtS - Opal 298": LocData(0x875E479, "Rex Marks the Spot"),
    "RMtS - Opal 299": LocData(0x875E47A, "Rex Marks the Spot"),
    "RMtS - Opal 300": LocData(0x875E47B, "Rex Marks the Spot"),
}

time_attack_challenge_dict = {
    "Two Up - Time Attack Challenge":
        LocData(0x08750344, "Two Up"),
    "WitP - Time Attack Challenge":
        LocData(0x08750345, "Walk in the Park"),
    "Ship Rex - Time Attack Challenge":
        LocData(0x08750346, "Ship Rex - Beyond Gate"),
    "BotRT - Time Attack Challenge":
        LocData(0x08750348, "Bridge on the River Ty - Beyond Broken Bridge"),
    "Snow Worries - Time Attack Challenge":
        LocData(0x08750349, "Snow Worries"),
    "Outback Safari - Time Attack Challenge":
        LocData(0x0875034A, "Outback Safari"),
    "LLPoF - Time Attack Challenge":
        LocData(0x0875034C, "Lyre, Lyre Pants on Fire"),
    "BtBS - Time Attack Challenge":
        LocData(0x0875034D, "Beyond the Black Stump"),
    "RMtS - Time Attack Challenge":
        LocData(0x0875034E, "Rex Marks the Spot - Underwater"),
}

signposts_dict = {
    # On starting pillar
    "Rainbow Cliffs - Signpost 1":
        LocData(0x08750400, "Rainbow Cliffs"),
    # At start
    "Two Up - Signpost 1":
        LocData(0x08750401, "Two Up"),
    # At first thunder egg
    "Two Up - Signpost 2":
        LocData(0x08750402, "Two Up"),
    # Before purple crab
    "Two Up - Signpost 3":
        LocData(0x08750403, "Two Up"),
    # Near bunyip
    "Two Up - Signpost 4":
        LocData(0x08750404, "Two Up - Upper Area"),
    # At spy eggs
    "Two Up - Signpost 5":
        LocData(0x08750405, "Two Up"),
    # Before Glide The Gap
    "Two Up - Signpost 6":
        LocData(0x08750406, "Two Up"),
    # At pit with three crates near start
    "Two Up - Signpost 7":
        LocData(0x08750407, "Two Up"),
    # Before first frills
    "Two Up - Signpost 8":
        LocData(0x08750408, "Two Up"),
    # Before first bridge
    "Two Up - Signpost 9":
        LocData(0x08750409, "Two Up"),
    # After first bridge
    "Two Up - Signpost 10":
        LocData(0x0875040A, "Two Up"),
    # After Glide The Gap
    "Two Up - Signpost 11":
        LocData(0x0875040B, "Two Up - End Area"),
    # At mushrooms next to opal collector
    "Two Up - Signpost 12":
        LocData(0x0875040C, "Two Up - End Area"),
    # At second rang
    "Two Up - Signpost 13":
        LocData(0x0875040D, "Two Up"),
    # At first bilby
    "Two Up - Signpost 14":
        LocData(0x0875040E, "Two Up"),
    # At first dunny
    "Two Up - Signpost 15":
        LocData(0x0875040F, "Two Up"),
    # At start on path
    "WitP - Signpost 1":
        LocData(0x08750410, "Walk in the Park"),
    # After third log
    "WitP - Signpost 2":
        LocData(0x08750411, "Walk in the Park"),
    # Top of slide 1
    "WitP - Signpost 3":
        LocData(0x08750412, "Walk in the Park"),
    # Near Neddy
    "BotRT - Signpost 1":
        LocData(0x08750413, "Bridge on the River Ty - Beyond Broken Bridge"),
    # At start
    "BotRT - Signpost 2":
        LocData(0x08750414, "Bridge on the River Ty"),
    # At start on opal path
    "Snow Worries - Signpost 1":
        LocData(0x08750415, "Snow Worries"),
    # At bottom of main path pillars start of ice
    "Snow Worries - Signpost 2":
        LocData(0x08750416, "Snow Worries"),
    # At bottom of mountain steps (mill side)
    "Snow Worries - Signpost 3":
        LocData(0x08750417, "Snow Worries"),
    # Top of log climb
    "BtBS - Signpost 1":
        LocData(0x08750418, "Beyond the Black Stump - Upper Area"),
    # At end
    "Cass' Pass - Signpost 1":
        LocData(0x08750419, "Cass' Pass"),
}


extra_lives_dict = {
    # Side path next to Julius' lab
    "Rainbow Cliffs - Extra Life 1":
        LocData(0x08750420, "Rainbow Cliffs"),
    # In waterfall cave near Rang The Frills
    "Two Up - Extra Life 1":
        LocData(0x08750421, "Two Up"),
    # Underwater under barrier between upper area and bridge
    "Two Up - Extra Life 2":
        LocData(0x08750422, "Two Up"),
    # In bat cave
    "WitP - Extra Life 1":
        LocData(0x08750423, "Walk in the Park"),
    # In small rockpool near tunnel entry to ship wreck
    "Ship Rex - Extra Life 1":
        LocData(0x08750424, "Ship Rex - Beyond Gate"),
    # On pillars in quicksand
    "Ship Rex - Extra Life 2":
        LocData(0x08750425, "Ship Rex - Beyond Gate"),
    # On platforms on back of top of spire
    "Ship Rex - Extra Life 3":
        LocData(0x08750426, "Ship Rex - Beyond Gate"),
    # In metal shed in water towers area
    "Outback Safari - Extra Life 1":
        LocData(0x08750427, "Outback Safari"),
    # On spiral path up the mountain
    "Outback Safari - Extra Life 2":
        LocData(0x08750428, "Outback Safari"),
    # In metal shed on left path from start
    "Outback Safari - Extra Life 3":
        LocData(0x08750429, "Outback Safari"),
    # Top of lighthouse through underwater tunnel
    "Crikey's Cove - Extra Life 1":
        LocData(0x0875042A, "Crikey's Cove"),
    # Inside volcano
    "RMtS - Extra Life 1":
        LocData(0x0875042B, "Rex Marks the Spot"),
    # Underwater near big red button for platform cog
    "RMtS - Extra Life 2":
        LocData(0x0875042C, "Rex Marks the Spot"),
    # Before island with crest portal on left side underwater
    "Cass' Pass - Extra Life 1":
        LocData(0x0875042D, "Cass' Pass"),
    # Behind island with Crest portal at end underwater
    "Cass' Pass - Extra Life 2":
        LocData(0x0875042E, "Cass' Pass"),
    # Behind tree root at first waterfall
    "Cass' Pass - Extra Life 3":
        LocData(0x0875042F, "Cass' Pass"),
    # In corner under lower waterfall after slide
    "Cass' Pass - Extra Life 4":
        LocData(0x08750430, "Cass' Pass"),
    # On platforms before second button
    "Cass' Crest - Extra Life 1":
        LocData(0x08750431, "Cass' Crest"),
    # On platform to the left of path next to second dunny
    "Cass' Crest - Extra Life 2":
        LocData(0x08750432, "Cass' Crest"),
    # At the end around a corner
    "Cass' Crest - Extra Life 3":
        LocData(0x08750433, "Cass' Crest"),
    # Underwater at start under the path between where Shazza is and where Shadow is
    "Cass' Crest - Extra Life 4":
        LocData(0x08750434, "Cass' Crest"),
    # In hole past third gas jet
    "Cass' Crest - Extra Life 5":
        LocData(0x08750435, "Cass' Crest"),
}

conditional_items_dict = {
    "Attribute - Extra Health":
        LocData(0x08750313, "Rainbow Cliffs"),
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
    **elemental_rangs_dict,
    **scales_dict,
    **signposts_dict,
    **extra_lives_dict,
    **time_attack_challenge_dict,
    **opals_dict,
    **conditional_items_dict
}
