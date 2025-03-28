from BaseClasses import Location, Region
from worlds.ty_the_tasmanian_tiger.options import Ty1Options


class Ty1Location(Location):
    game: str = "Ty the Tasmanian Tiger"


class LocData:
    def __init__(self, code: int, region: str,):
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
    # OPALS
    if options.opalsanity:
        create_locations_from_dict(opals_dict, reg, player)


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
        LocData(0x8750320, "Bli Bli Station Gate"),
    # Behind left-hand house in A-zone
    "Rainbow Scale 2":
        LocData(0x8750321, "Bli Bli Station Gate"),
    # In corner hidden behind Julius' lab
    "Rainbow Scale 3":
        LocData(0x8750322, "Rainbow Cliffs"),
    # Under Thunder Egg collector in B-zone
    "Rainbow Scale 4":
        LocData(0x8750323, "Pippy Beach"),
    # Just past flame logs in C-zone
    "Rainbow Scale 5":
        LocData(0x8750324, "Lake Burril"),
    # On small ledge on the side of starting pillar
    "Rainbow Scale 6":
        LocData(0x8750325, "Rainbow Cliffs"),
    # Inside waterfall cave
    "Rainbow Scale 7":
        LocData(0x8750326, "Rainbow Cliffs"),
    # Corner island next to waterfall cave
    "Rainbow Scale 8":
        LocData(0x8750327, "Rainbow Cliffs"),
    # Side of path between B-zone and Julius' lab 1
    "Rainbow Scale 9":
        LocData(0x8750328, "Rainbow Cliffs"),
    # Next to extra life
    "Rainbow Scale 10":
        LocData(0x8750329, "Rainbow Cliffs"),
    # Above water next to Julius' lab (pontoon scale)
    "Rainbow Scale 11":
        LocData(0x875032A, "Rainbow Cliffs"),
    # After pillar platforms leading up to C-zone
    "Rainbow Scale 12":
        LocData(0x875032B, "Rainbow Cliffs"),
    # In the water next to pillar platforms leading up to C-zone
    "Rainbow Scale 13":
        LocData(0x875032C, "Rainbow Cliffs"),
    # Behind rock at entrance to B-zone
    "Rainbow Scale 14":
        LocData(0x875032D, "Rainbow Cliffs"),
    # Inside starting pillar
    "Rainbow Scale 15":
        LocData(0x875032E, "Rainbow Cliffs"),
    # Underwater near Julius' lab
    "Rainbow Scale 16":
        LocData(0x875032F, "Rainbow Cliffs"),
    # On wooden platform in C-zone
    "Rainbow Scale 17":
        LocData(0x8750330, "Lake Burril"),
    # Under Thunder Egg collector in C-zone
    "Rainbow Scale 18":
        LocData(0x8750331, "Lake Burril"),
    # Just past ice wall in B-zone
    "Rainbow Scale 19":
        LocData(0x8750332, "Pippy Beach"),
    # Next to water wheel on wooden walkway at Julius' lab
    "Rainbow Scale 20":
        LocData(0x8750333, "Rainbow Cliffs"),
    # Underwater near waterfall cave
    "Rainbow Scale 21":
        LocData(0x8750334, "Rainbow Cliffs"),
    # Just past E-zone gate
    "Rainbow Scale 22":
        LocData(0x8750335, "Final Gauntlet"),
    # Hidden around corner in E-zone
    "Rainbow Scale 23":
        LocData(0x8750336, "Final Gauntlet"),
    # Floating in the air next to starting pillar
    "Rainbow Scale 24":
        LocData(0x8750337, "Rainbow Cliffs"),
    # Under Thunder Egg collector in A-zone
    "Rainbow Scale 25":
        LocData(0x8750338, "Rainbow Cliffs"),
}

opals_dict = {
    #Two Up
    "Two Up - Opal 1":
        LocData(0x8750350, "Two Up"),
    "Two Up - Opal 2":
        LocData(0x8750351, "Two Up"),
    "Two Up - Opal 3":
        LocData(0x8750352, "Two Up"),
    "Two Up - Opal 4":
        LocData(0x8750353, "Two Up"),
    "Two Up - Opal 5":
        LocData(0x8750354, "Two Up"),
    "Two Up - Opal 6":
        LocData(0x8750355, "Two Up"),
    "Two Up - Opal 7":
        LocData(0x8750356, "Two Up"),
    "Two Up - Opal 8":
        LocData(0x8750357, "Two Up"),
    "Two Up - Opal 9":
        LocData(0x8750358, "Two Up"),
    "Two Up - Opal 10":
        LocData(0x8750359, "Two Up"),
    "Two Up - Opal 11":
        LocData(0x875035A, "Two Up"),
    "Two Up - Opal 12":
        LocData(0x875035B, "Two Up"),
    "Two Up - Opal 13":
        LocData(0x875035C, "Two Up"),
    "Two Up - Opal 14":
        LocData(0x875035D, "Two Up"),
    "Two Up - Opal 15":
        LocData(0x875035E, "Two Up"),
    "Two Up - Opal 16":
        LocData(0x875035F, "Two Up"),
    "Two Up - Opal 17":
        LocData(0x8750360, "Two Up"),
    "Two Up - Opal 18":
        LocData(0x8750361, "Two Up"),
    "Two Up - Opal 19":
        LocData(0x8750362, "Two Up"),
    "Two Up - Opal 20":
        LocData(0x8750363, "Two Up"),
    "Two Up - Opal 21":
        LocData(0x8750364, "Two Up"),
    "Two Up - Opal 22":
        LocData(0x8750365, "Two Up"),
    "Two Up - Opal 23":
        LocData(0x8750366, "Two Up"),
    "Two Up - Opal 24":
        LocData(0x8750367, "Two Up"),
    "Two Up - Opal 25":
        LocData(0x8750368, "Two Up"),
    "Two Up - Opal 26":
        LocData(0x8750369, "Two Up"),
    "Two Up - Opal 27":
        LocData(0x875036A, "Two Up"),
    "Two Up - Opal 28":
        LocData(0x875036B, "Two Up"),
    "Two Up - Opal 29":
        LocData(0x875036C, "Two Up"),
    "Two Up - Opal 30":
        LocData(0x875036D, "Two Up"),
    "Two Up - Opal 31":
        LocData(0x875036E, "Two Up"),
    "Two Up - Opal 32":
        LocData(0x875036F, "Two Up"),
    "Two Up - Opal 33":
        LocData(0x8750370, "Two Up"),
    "Two Up - Opal 34":
        LocData(0x8750371, "Two Up"),
    "Two Up - Opal 35":
        LocData(0x8750372, "Two Up"),
    "Two Up - Opal 36":
        LocData(0x8750373, "Two Up"),
    "Two Up - Opal 37":
        LocData(0x8750374, "Two Up"),
    "Two Up - Opal 38":
        LocData(0x8750375, "Two Up"),
    "Two Up - Opal 39":
        LocData(0x8750376, "Two Up"),
    "Two Up - Opal 40":
        LocData(0x8750377, "Two Up"),
    "Two Up - Opal 41":
        LocData(0x8750378, "Two Up"),
    "Two Up - Opal 42":
        LocData(0x8750379, "Two Up"),
    "Two Up - Opal 43":
        LocData(0x875037A, "Two Up"),
    "Two Up - Opal 44":
        LocData(0x875037B, "Two Up"),
    "Two Up - Opal 45":
        LocData(0x875037C, "Two Up"),
    "Two Up - Opal 46":
        LocData(0x875037D, "Two Up"),
    "Two Up - Opal 47":
        LocData(0x875037E, "Two Up"),
    "Two Up - Opal 48":
        LocData(0x875037F, "Two Up"),
    "Two Up - Opal 49":
        LocData(0x8750380, "Two Up"),
    "Two Up - Opal 50":
        LocData(0x8750381, "Two Up"),
    "Two Up - Opal 51":
        LocData(0x8750382, "Two Up"),
    "Two Up - Opal 52":
        LocData(0x8750383, "Two Up"),
    "Two Up - Opal 53":
        LocData(0x8750384, "Two Up"),
    "Two Up - Opal 54":
        LocData(0x8750385, "Two Up"),
    "Two Up - Opal 55":
        LocData(0x8750386, "Two Up"),
    "Two Up - Opal 56":
        LocData(0x8750387, "Two Up"),
    "Two Up - Opal 57":
        LocData(0x8750388, "Two Up"),
    "Two Up - Opal 58":
        LocData(0x8750389, "Two Up"),
    "Two Up - Opal 59":
        LocData(0x875038A, "Two Up"),
    "Two Up - Opal 60":
        LocData(0x875038B, "Two Up"),
    "Two Up - Opal 61":
        LocData(0x875038C, "Two Up"),
    "Two Up - Opal 62":
        LocData(0x875038D, "Two Up"),
    "Two Up - Opal 63":
        LocData(0x875038E, "Two Up"),
    "Two Up - Opal 64":
        LocData(0x875038F, "Two Up"),
    "Two Up - Opal 65":
        LocData(0x8750390, "Two Up"),
    "Two Up - Opal 66":
        LocData(0x8750391, "Two Up"),
    "Two Up - Opal 67":
        LocData(0x8750392, "Two Up"),
    "Two Up - Opal 68":
        LocData(0x8750393, "Two Up"),
    "Two Up - Opal 69":
        LocData(0x8750394, "Two Up"),
    "Two Up - Opal 70":
        LocData(0x8750395, "Two Up"),
    "Two Up - Opal 71":
        LocData(0x8750396, "Two Up"),
    "Two Up - Opal 72":
        LocData(0x8750397, "Two Up"),
    "Two Up - Opal 73":
        LocData(0x8750398, "Two Up"),
    "Two Up - Opal 74":
        LocData(0x8750399, "Two Up"),
    "Two Up - Opal 75":
        LocData(0x875039A, "Two Up"),
    "Two Up - Opal 76":
        LocData(0x875039B, "Two Up"),
    "Two Up - Opal 77":
        LocData(0x875039C, "Two Up"),
    "Two Up - Opal 78":
        LocData(0x875039D, "Two Up"),
    "Two Up - Opal 79":
        LocData(0x875039E, "Two Up"),
    "Two Up - Opal 80":
        LocData(0x875039F, "Two Up"),
    "Two Up - Opal 81":
        LocData(0x87503A0, "Two Up"),
    "Two Up - Opal 82":
        LocData(0x87503A1, "Two Up"),
    "Two Up - Opal 83":
        LocData(0x87503A2, "Two Up"),
    "Two Up - Opal 84":
        LocData(0x87503A3, "Two Up"),
    "Two Up - Opal 85":
        LocData(0x87503A4, "Two Up"),
    "Two Up - Opal 86":
        LocData(0x87503A5, "Two Up"),
    "Two Up - Opal 87":
        LocData(0x87503A6, "Two Up"),
    "Two Up - Opal 88":
        LocData(0x87503A7, "Two Up"),
    "Two Up - Opal 89":
        LocData(0x87503A8, "Two Up"),
    "Two Up - Opal 90":
        LocData(0x87503A9, "Two Up"),
    "Two Up - Opal 91":
        LocData(0x87503AA, "Two Up"),
    "Two Up - Opal 92":
        LocData(0x87503AB, "Two Up"),
    "Two Up - Opal 93":
        LocData(0x87503AC, "Two Up"),
    "Two Up - Opal 94":
        LocData(0x87503AD, "Two Up"),
    "Two Up - Opal 95":
        LocData(0x87503AE, "Two Up"),
    "Two Up - Opal 96":
        LocData(0x87503AF, "Two Up"),
    "Two Up - Opal 97":
        LocData(0x87503B0, "Two Up"),
    "Two Up - Opal 98":
        LocData(0x87503B1, "Two Up"),
    "Two Up - Opal 99":
        LocData(0x87503B2, "Two Up"),
    "Two Up - Opal 100":
        LocData(0x87503B3, "Two Up"),
    "Two Up - Opal 101":
        LocData(0x87503B4, "Two Up"),
    "Two Up - Opal 102":
        LocData(0x87503B5, "Two Up"),
    "Two Up - Opal 103":
        LocData(0x87503B6, "Two Up"),
    "Two Up - Opal 104":
        LocData(0x87503B7, "Two Up"),
    "Two Up - Opal 105":
        LocData(0x87503B8, "Two Up"),
    "Two Up - Opal 106":
        LocData(0x87503B9, "Two Up"),
    "Two Up - Opal 107":
        LocData(0x87503BA, "Two Up"),
    "Two Up - Opal 108":
        LocData(0x87503BB, "Two Up"),
    "Two Up - Opal 109":
        LocData(0x87503BC, "Two Up"),
    "Two Up - Opal 110":
        LocData(0x87503BD, "Two Up"),
    "Two Up - Opal 111":
        LocData(0x87503BE, "Two Up"),
    "Two Up - Opal 112":
        LocData(0x87503BF, "Two Up"),
    "Two Up - Opal 113":
        LocData(0x87503C0, "Two Up"),
    "Two Up - Opal 114":
        LocData(0x87503C1, "Two Up"),
    "Two Up - Opal 115":
        LocData(0x87503C2, "Two Up"),
    "Two Up - Opal 116":
        LocData(0x87503C3, "Two Up"),
    "Two Up - Opal 117":
    LocData(0x87503C4, "Two Up - Upper Area"),
    "Two Up - Opal 118":
        LocData(0x87503C5, "Two Up - Upper Area"),
    "Two Up - Opal 119":
        LocData(0x87503C6, "Two Up - Upper Area"),
    "Two Up - Opal 120":
        LocData(0x87503C7, "Two Up - Upper Area"),
    "Two Up - Opal 121":
        LocData(0x87503C8, "Two Up - Upper Area"),
    "Two Up - Opal 122":
        LocData(0x87503C9, "Two Up - Upper Area"),
    "Two Up - Opal 123":
        LocData(0x87503CA, "Two Up - Upper Area"),
    "Two Up - Opal 124":
        LocData(0x87503CB, "Two Up - Upper Area"),
    "Two Up - Opal 125":
        LocData(0x87503CC, "Two Up - Upper Area"),
    "Two Up - Opal 126":
        LocData(0x87503CD, "Two Up - Upper Area"),
    "Two Up - Opal 127":
        LocData(0x87503CE, "Two Up - Upper Area"),
    "Two Up - Opal 128":
        LocData(0x87503CF, "Two Up - Upper Area"),
    "Two Up - Opal 129":
        LocData(0x87503D0, "Two Up - Upper Area"),
    "Two Up - Opal 130":
        LocData(0x87503D1, "Two Up - Upper Area"),
    "Two Up - Opal 131":
        LocData(0x87503D2, "Two Up"),
    "Two Up - Opal 132":
        LocData(0x87503D3, "Two Up"),
    "Two Up - Opal 133":
        LocData(0x87503D4, "Two Up"),
    "Two Up - Opal 134":
        LocData(0x87503D5, "Two Up"),
    "Two Up - Opal 135":
        LocData(0x87503D6, "Two Up"),
    "Two Up - Opal 136":
        LocData(0x87503D7, "Two Up"),
    "Two Up - Opal 137":
        LocData(0x87503D8, "Two Up"),
    "Two Up - Opal 138":
        LocData(0x87503D9, "Two Up"),
    "Two Up - Opal 139":
        LocData(0x87503DA, "Two Up"),
    "Two Up - Opal 140":
        LocData(0x87503DB, "Two Up"),
    "Two Up - Opal 141":
        LocData(0x87503DC, "Two Up"),
    "Two Up - Opal 142":
        LocData(0x87503DD, "Two Up"),
    "Two Up - Opal 143":
        LocData(0x87503DE, "Two Up"),
    "Two Up - Opal 144":
        LocData(0x87503DF, "Two Up"),
    "Two Up - Opal 145":
        LocData(0x87503E0, "Two Up"),
    "Two Up - Opal 146":
        LocData(0x87503E1, "Two Up"),
    "Two Up - Opal 147":
        LocData(0x87503E2, "Two Up"),
    "Two Up - Opal 148":
        LocData(0x87503E3, "Two Up"),
    "Two Up - Opal 149":
        LocData(0x87503E4, "Two Up"),
    "Two Up - Opal 150":
        LocData(0x87503E5, "Two Up"),
    "Two Up - Opal 151":
        LocData(0x87503E6, "Two Up"),
    "Two Up - Opal 152":
        LocData(0x87503E7, "Two Up"),
    "Two Up - Opal 153":
        LocData(0x87503E8, "Two Up"),
    "Two Up - Opal 154":
        LocData(0x87503E9, "Two Up"),
    "Two Up - Opal 155":
        LocData(0x87503EA, "Two Up"),
    "Two Up - Opal 156":
        LocData(0x87503EB, "Two Up"),
    "Two Up - Opal 157":
        LocData(0x87503EC, "Two Up"),
    "Two Up - Opal 158":
        LocData(0x87503ED, "Two Up - Upper Area"),
    "Two Up - Opal 159":
        LocData(0x87503EE, "Two Up - Upper Area"),
    "Two Up - Opal 160":
        LocData(0x87503EF, "Two Up - Upper Area"),
    "Two Up - Opal 161":
        LocData(0x87503F0, "Two Up - Upper Area"),
    "Two Up - Opal 162":
        LocData(0x87503F1, "Two Up - Upper Area"),
    "Two Up - Opal 163":
        LocData(0x87503F2, "Two Up - Upper Area"),
    "Two Up - Opal 164":
        LocData(0x87503F3, "Two Up - Upper Area"),
    "Two Up - Opal 165":
        LocData(0x87503F4, "Two Up - Upper Area"),
    "Two Up - Opal 166":
        LocData(0x87503F5, "Two Up - Upper Area"),
    "Two Up - Opal 167":
        LocData(0x87503F6, "Two Up - Upper Area"),
    "Two Up - Opal 168":
        LocData(0x87503F7, "Two Up"),
    "Two Up - Opal 169":
        LocData(0x87503F8, "Two Up"),
    "Two Up - Opal 170":
        LocData(0x87503F9, "Two Up"),
    "Two Up - Opal 171":
        LocData(0x87503FA, "Two Up"),
    "Two Up - Opal 172":
        LocData(0x87503FB, "Two Up"),
    "Two Up - Opal 173":
        LocData(0x87503FC, "Two Up"),
    "Two Up - Opal 174":
        LocData(0x87503FD, "Two Up"),
    "Two Up - Opal 175":
        LocData(0x87503FE, "Two Up"),
    "Two Up - Opal 176":
        LocData(0x87503FF, "Two Up"),
    "Two Up - Opal 177":
        LocData(0x8750400, "Two Up"),
    "Two Up - Opal 178":
        LocData(0x8750401, "Two Up"),
    "Two Up - Opal 179":
        LocData(0x8750402, "Two Up"),
    "Two Up - Opal 180":
        LocData(0x8750403, "Two Up"),
    "Two Up - Opal 181":
        LocData(0x8750404, "Two Up"),
    "Two Up - Opal 182":
        LocData(0x8750405, "Two Up"),
    "Two Up - Opal 183":
        LocData(0x8750406, "Two Up"),
    "Two Up - Opal 184":
        LocData(0x8750407, "Two Up"),
    "Two Up - Opal 185":
        LocData(0x8750408, "Two Up"),
    "Two Up - Opal 186":
        LocData(0x8750409, "Two Up"),
    "Two Up - Opal 187":
        LocData(0x875040A, "Two Up"),
    "Two Up - Opal 188":
        LocData(0x875040B, "Two Up"),
    "Two Up - Opal 189":
        LocData(0x875040C, "Two Up"),
    "Two Up - Opal 190":
        LocData(0x875040D, "Two Up"),
    "Two Up - Opal 191":
        LocData(0x875040E, "Two Up"),
    "Two Up - Opal 192":
        LocData(0x875040F, "Two Up"),
    "Two Up - Opal 193":
        LocData(0x8750410, "Two Up"),
    "Two Up - Opal 194":
        LocData(0x8750411, "Two Up"),
    "Two Up - Opal 195":
        LocData(0x8750412, "Two Up"),
    "Two Up - Opal 196":
        LocData(0x8750413, "Two Up"),
    "Two Up - Opal 197":
        LocData(0x8750414, "Two Up"),
    "Two Up - Opal 198":
        LocData(0x8750415, "Two Up"),
    "Two Up - Opal 199":
        LocData(0x8750416, "Two Up"),
    "Two Up - Opal 200":
        LocData(0x8750417, "Two Up"),
    "Two Up - Opal 201":
        LocData(0x8750418, "Two Up"),
    "Two Up - Opal 202":
        LocData(0x8750419, "Two Up"),
    "Two Up - Opal 203":
        LocData(0x875041A, "Two Up"),
    "Two Up - Opal 204":
        LocData(0x875041B, "Two Up"),
    "Two Up - Opal 205":
        LocData(0x875041C, "Two Up"),
    "Two Up - Opal 206":
        LocData(0x875041D, "Two Up"),
    "Two Up - Opal 207":
        LocData(0x875041E, "Two Up"),
    "Two Up - Opal 208":
        LocData(0x875041F, "Two Up"),
    "Two Up - Opal 209":
        LocData(0x8750420, "Two Up"),
    "Two Up - Opal 210":
        LocData(0x8750421, "Two Up"),
    "Two Up - Opal 211":
        LocData(0x8750422, "Two Up"),
    "Two Up - Opal 212":
        LocData(0x8750423, "Two Up"),
    "Two Up - Opal 213":
        LocData(0x8750424, "Two Up"),
    "Two Up - Opal 214":
        LocData(0x8750425, "Two Up"),
    "Two Up - Opal 215":
        LocData(0x8750426, "Two Up"),
    "Two Up - Opal 216":
        LocData(0x8750427, "Two Up"),
    "Two Up - Opal 217":
        LocData(0x8750428, "Two Up"),
    "Two Up - Opal 218":
        LocData(0x8750429, "Two Up"),
    "Two Up - Opal 219":
        LocData(0x875042A, "Two Up"),
    "Two Up - Opal 220":
        LocData(0x875042B, "Two Up"),
    "Two Up - Opal 221":
        LocData(0x875042C, "Two Up"),
    "Two Up - Opal 222":
        LocData(0x875042D, "Two Up"),
    "Two Up - Opal 223":
        LocData(0x875042E, "Two Up"),
    "Two Up - Opal 224":
        LocData(0x875042F, "Two Up"),
    "Two Up - Opal 225":
        LocData(0x8750430, "Two Up"),
    "Two Up - Opal 226":
        LocData(0x8750431, "Two Up"),
    "Two Up - Opal 227":
        LocData(0x8750432, "Two Up"),
    "Two Up - Opal 228":
        LocData(0x8750433, "Two Up"),
    "Two Up - Opal 229":
        LocData(0x8750434, "Two Up"),
    "Two Up - Opal 230":
        LocData(0x8750435, "Two Up"),
    "Two Up - Opal 231":
        LocData(0x8750436, "Two Up"),
    "Two Up - Opal 232":
        LocData(0x8750437, "Two Up"),
    "Two Up - Opal 233":
        LocData(0x8750438, "Two Up"),
    "Two Up - Opal 234":
        LocData(0x8750439, "Two Up"),
    "Two Up - Opal 235":
        LocData(0x875043A, "Two Up"),
    "Two Up - Opal 236":
        LocData(0x875043B, "Two Up"),
    "Two Up - Opal 237":
        LocData(0x875043C, "Two Up"),
    "Two Up - Opal 238":
        LocData(0x875043D, "Two Up"),
    "Two Up - Opal 239":
        LocData(0x875043E, "Two Up"),
    "Two Up - Opal 240":
        LocData(0x875043F, "Two Up"),
    "Two Up - Opal 241":
        LocData(0x8750440, "Two Up"),
    "Two Up - Opal 242":
        LocData(0x8750441, "Two Up"),
    "Two Up - Opal 243":
        LocData(0x8750442, "Two Up"),
    "Two Up - Opal 244":
        LocData(0x8750443, "Two Up"),
    "Two Up - Opal 245":
        LocData(0x8750444, "Two Up"),
    "Two Up - Opal 246":
        LocData(0x8750445, "Two Up"),
    "Two Up - Opal 247":
        LocData(0x8750446, "Two Up"),
    "Two Up - Opal 248":
        LocData(0x8750447, "Two Up"),
    "Two Up - Opal 249":
        LocData(0x8750448, "Two Up"),
    "Two Up - Opal 250":
        LocData(0x8750449, "Two Up"),
    "Two Up - Opal 251":
        LocData(0x875044A, "Two Up"),
    "Two Up - Opal 252":
        LocData(0x875044B, "Two Up"),
    "Two Up - Opal 253":
        LocData(0x875044C, "Two Up"),
    "Two Up - Opal 254":
        LocData(0x875044D, "Two Up"),
    "Two Up - Opal 255":
        LocData(0x875044E, "Two Up"),
    "Two Up - Opal 256":
        LocData(0x875044F, "Two Up"),
    "Two Up - Opal 257":
        LocData(0x8750450, "Two Up"),
    "Two Up - Opal 258":
        LocData(0x8750451, "Two Up"),
    "Two Up - Opal 259":
        LocData(0x8750452, "Two Up"),
    "Two Up - Opal 260":
        LocData(0x8750453, "Two Up"),
    "Two Up - Opal 261":
        LocData(0x8750454, "Two Up"),
    "Two Up - Opal 262":
        LocData(0x8750455, "Two Up"),
    "Two Up - Opal 263":
        LocData(0x8750456, "Two Up"),
    "Two Up - Opal 264":
        LocData(0x8750457, "Two Up"),
    "Two Up - Opal 265":
        LocData(0x8750458, "Two Up"),
    "Two Up - Opal 266":
        LocData(0x8750459, "Two Up"),
    "Two Up - Opal 267":
        LocData(0x875045A, "Two Up"),
    "Two Up - Opal 268":
        LocData(0x875045B, "Two Up"),
    "Two Up - Opal 269":
        LocData(0x875045C, "Two Up"),
    "Two Up - Opal 270":
        LocData(0x875045D, "Two Up"),
    "Two Up - Opal 271":
        LocData(0x875045E, "Two Up"),
    "Two Up - Opal 272":
        LocData(0x875045F, "Two Up"),
    "Two Up - Opal 273":
        LocData(0x8750460, "Two Up"),
    "Two Up - Opal 274":
        LocData(0x8750461, "Two Up"),
    "Two Up - Opal 275":
        LocData(0x8750462, "Two Up"),
    "Two Up - Opal 276":
        LocData(0x8750463, "Two Up"),
    "Two Up - Opal 277":
        LocData(0x8750464, "Two Up"),
    "Two Up - Opal 278":
        LocData(0x8750465, "Two Up"),
    "Two Up - Opal 279":
        LocData(0x8750466, "Two Up"),
    "Two Up - Opal 280":
        LocData(0x8750467, "Two Up"),
    "Two Up - Opal 281":
        LocData(0x8750468, "Two Up"),
    "Two Up - Opal 282":
        LocData(0x8750469, "Two Up"),
    "Two Up - Opal 283":
        LocData(0x875046A, "Two Up"),
    "Two Up - Opal 284":
        LocData(0x875046B, "Two Up"),
    "Two Up - Opal 285":
        LocData(0x875046C, "Two Up"),
    "Two Up - Opal 286":
        LocData(0x875046D, "Two Up"),
    "Two Up - Opal 287":
        LocData(0x875046E, "Two Up"),
    "Two Up - Opal 288":
        LocData(0x875046F, "Two Up"),
    "Two Up - Opal 289":
        LocData(0x8750470, "Two Up"),
    "Two Up - Opal 290":
        LocData(0x8750471, "Two Up"),
    "Two Up - Opal 291":
        LocData(0x8750472, "Two Up"),
    "Two Up - Opal 292":
        LocData(0x8750473, "Two Up"),
    "Two Up - Opal 293":
        LocData(0x8750474, "Two Up"),
    "Two Up - Opal 294":
        LocData(0x8750475, "Two Up"),
    "Two Up - Opal 295":
        LocData(0x8750476, "Two Up"),
    "Two Up - Opal 296":
        LocData(0x8750477, "Two Up"),
    "Two Up - Opal 297":
        LocData(0x8750478, "Two Up"),
    "Two Up - Opal 298":
        LocData(0x8750479, "Two Up"),
    "Two Up - Opal 299":
        LocData(0x875047A, "Two Up"),
    "Two Up - Opal 300":
        LocData(0x875047B, "Two Up"),

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
