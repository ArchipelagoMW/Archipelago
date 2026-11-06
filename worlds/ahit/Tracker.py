from settings import Group, FilePath


# Basically copied from https://github.com/ArsonAssassin/DSAP/commit/62b0c4d87483977e86fdfba2229259ec581c4fdb
# TODO: Is there a way to make it only prompt when people want it to? Is that desirable over auto-prompt?
class AHITSettings(Group):
    class UTPoptrackerPath(FilePath):
        """Path to the user's AHIT Poptracker Pack."""
        description= "AHIT Poptracker Pack zip file"
        required = False
    ut_poptracker_path: UTPoptrackerPath | str = UTPoptrackerPath()


map_page_locations = [
    "locations/spaceship_overview.json",
    "locations/alpineskyline.json",
    "locations/basement.json",
    "locations/cruise.json",
    "locations/deadbirdstudio.json",
    # "locations/deathwish.json", # Has comments in the file, UT can't parse
    # "locations/mafiatown.json", # Has comments in the file
    "locations/nyakuza.json",
    # "locations/spaceship.json", # Has commnets in the file
    "locations/subcon.json",
    
    # "locations/entrances/chapter_time_rifts.json", # jsonc
    "locations/entrances/chapter1.json",
    # "locations/entrances/chapter2.json", # jsonc
    # "locations/entrances/chapter3.json", # jsonc
    # "locations/entrances/chapter4.json", # jsonc
    "locations/entrances/chapter5.json",
    # "locations/entrances/chapter6.json", # jsonc
    # "locations/entrances/chapter7.json", # jsonc
    "locations/entrances/spaceship_attic.json",
    "locations/entrances/spaceship_gallery.json",
    "locations/entrances/spaceship_lab.json"
]

# TODO: Deal with the abbreviated ones Em mentioned
tracker_name_mapping = {
    # Mafia Town
    "Welcome to Mafia Town/Time Piece" : 2000311771,
    "Welcome to Mafia Town/Umbrella" : 2000301002,
    "Barrel Battle/Time Piece" : 2000311958,
    "Mafia Geek/She Came from Outer Space" : 2000312262,
    "Mafia HQ/Time Piece" : 2000311326,
    "Mafia HQ/Hallway Brewing Crate" : 2000305387,
    "Mafia HQ/Freezer Chest" : 2000303241,
    "Mafia HQ/Secret Room" : 2000304979,
    "Mafia HQ/Bathroom Stall Chest" : 2000303243,
    "Beach Alcove/Cheating the Race" : 2000312318,
    "Mafia Geek/Heating Up Mafia Town" : 2000311481,
    "The Golden Vault/Time Piece" : 2000312250,
    "Bazaar/Time Rift" : 2000312465,
    "Sewers/Time Rift" : 2000312484,
    "Mafia of Cooks/Time Rift" : 2000311855,
    # "Mafia of Cooks/Pages" # TODO: Decide how to handle
    "Red Vault/Yarn" : 2000302848,
    "Dweller Boxes/Yarn" : 2000304462,
    "Old Man 2/Seaside Spaghetti" : 2000303833,
    "Ledge Chest/Yarn" : 2000303530,
    "Yellow Sphere Building Chest/Yarn" : 2000303535,
    "Beneath Scaffolding/Yarn" : 2000304456,
    "On Scaffolding/Yarn" : 2000304457,
    "Plaza Under Boxes/Yarn" : 2000304458,
    "Blue Vault/Brewing Crate" : 2000305572,
    "Small Boat/Yarn" : 2000304460,
    "Cargo Ship/Yarn" : 2000304459,
    "Beach Alcove/Yarn" : 2000304463,
    "Steel Beams/Wood Cage" : 2000304606,
    "Staircase Pon Cluster/Yarn" : 2000304611,
    "Blue Vault/Vault" : 2000302850,
    "Old Man/Yarn" : 2000303832,
    "Palm Tree/Yarn" : 2000304609,
    "Beach Patio/Freestanding" : 2000304610,
    "Steel Beams/Nest" : 2000304608,
    "Top of Ruined Tower/Yarn" : 2000304607,
    "Ice Hat Cage/Yarn" : 2000304831,
    "Hot Air Balloon/Yarn" : 2000304829,
    "Camera Badge/smile :)" : 2000302003,
    "Camera Badge 2/smile :)" : 2000302004,
    "Chest Beneath Aqueduct/Relic" : 2000303489,
    "Secret Cave/Relic" : 2000305220,
    "Crow Chest/Relic" : 2000303532,
    "Port/Relic" : 2000305219,
    "Docks Chest/Relic" : 2000303534,
    "Above Boats/Relic" : 2000305218,
    "Beach Patio/Slip Slide Chest" : 2000303529,
    "Green Vault/Token" : 2000302851,
    "Behind Faucet/Token" : 2000304214,
    "Hidden Buttons/Grab a beach ball" : 2000303483,
    "Clock Tower Chest/Token" : 2000303481,
    "Top of Lighthouse/Token" : 2000304213,
    "Mafia Geek Platform/Token" : 2000304212,
    "Mafia HQ/Behind HQ Chest" : 2000303486,

    # Battle of the Birds
    "Act Completion/Dead Bird Studio" : 2000311383,
    "Up the Ladder/Yarn" : 2000304874,
    "DJ Grooves Sign Chest/Yarn" : 2000303901,
    "Red Building Top/Yarn" : 2000305024,
    "Behind Water Tower/Yarn" : 2000305248,
    "Side of House/Yarn" : 2000305247,
    "Tightrope Chest/Relic" : 2000303898,
    "Teepee Chest/Relic" : 2000303899,
    "Conductor Chest/Token" : 2000303900,
    # "Act Completion/Time Piece" # Oh boy, is this unique? TODO: ??
    "Cafeteria/Yarn" : 2000305313,
    "Luggage Room Top/Yarn" : 2000305090,
    "Luggage Room Bottom/Yarn" : 2000305091,
    "Raven Suite/Room" : 2000305701,
    "Raven Suite/Top" : 2000305312,
    "Lounge Chest/Token" : 2000303963,
    # TODO: Verify these actually show up
    "Conductor Token: Cafeteria/" : 2001104767,
    "Conductor Token: Recreational Room/" : 2001104768,
    "Picture Perfect/Time Piece" : 2000311587,
    "Picture Perfect - Behind Badge Seller/Yarn" : 2000304307,
    "Picture Perfect - Hats Buy Building/Yarn" : 2000304530,
    "Picture Perfect - DJ Grooves Token: Cardboard Puppy/" : 2001203990,
    "Picture Perfect - DJ Grooves Token: Card Guessing Game/" : 2001203991,
    "Picture Perfect - DJ Grooves Token: Back Alley/" : 2001203992,
    "Picture Perfect - DJ Grooves Token: Cooking Show/" : 2001203993,
    "Picture Perfect - DJ Grooves Token: Pon Cluster/" : 2001203987,
    "Train Rush/Time Piece" : 2000312481,
    "Time Bonus: 1st Room/" : 2001305235,
    "Time Bonus: Falling Platform/" : 2001305189,
    "Time Bonus: Acid Crates/" : 2001305186,
    "Time Bonus: Balloon/" : 2001305239,
    "Time Bonus: Ring of Fire/" : 2001305237,
    "Time Bonus: Blue Panels/" : 2001305236,
    "Time Bonus: Sinking Lava Platform/" : 2001305234,
    "Time Bonus: Lava Panels 1/" : 2001305193,
    "Time Bonus: Lava Panels 2/" : 2001305190,
    "Time Bonus: Lava Panels 3/" : 2001305238,
    "The Big Parade/Time Piece" : 2000311157,
    # TODO: Figure out why the tokens don't show up. Probably the internal
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 1" : 2001400000,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 2" : 2001400001,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 3" : 2001400002,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 4" : 2001400003,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 5" : 2001400004,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 6" : 2001400005,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 7" : 2001400006,
    "The Big Parade - DJ Grooves Tokens (Internal)/Token 8" : 2001400007,
    "Act Completion/Award Ceremony" : 2000311488,
    # "Act Completion/Time Piece" # Yep, not unique... TODO: how?
    "Window Platform/Yarn" : 2000305432,
    "Cardboard Conductor/Yarn" : 2000305059,
    "Above Conductor Sign/Yarn" : 2000305057,
    "Logo Wall/Yarn" : 2000305207,
    "Disco Room/Yarn" : 2000305061,
    "Small Room/Token" : 2000304813,
    "Vent Pipe/Yarn" : 2000305430,
    "Tightrope/Yarn" : 2000305058,
    "Cameras/Yarn" : 2000305431,
    "Locked Room/Relic" : 2000305819,
    "The Owl Express/Time Rift" : 2000312807,
    "The Moon/Time Rift" : 2000312785,
    "Dead Bird Studio (Rift)/Time Piece" : 2000312577,
    # "Dead Bird Studio (Rift)/Pages" TODO: Decide how to handle this

    # Subcon Forest
    "Contractual Obligations/Time Piece" : 2000312317,
    "Snatcher/Contract - The Subcon Well" : 2000300200,
    "Cherry Bomb Bone Cage/Yarn" : 2000324761,
    "Subcon Well/Time Piece" : 2000311160,
    "Subcon Well/Hookshot Badge Chest" : 2000324114,
    "Subcon Well/Above Chest" : 2000324612,
    "Subcon Well/On Pipe" : 2000324311,
    "Subcon Well/Mushroom" : 2000325318,
    "Boss Arena/Toilet of Doom" : 2000311984,
    "Queen Vanessa's Manor/Time Piece" : 2000312017,
    "Queen Vanessa's Manor/Cellar" : 2000324841,
    "Queen Vanessa's Manor/Bedroom Chest" : 2000323808,
    "Queen Vanessa's Manor/Hall Chest" : 2000323896,
    "Queen Vanessa's Manor/Chandelier" : 2000325546,
    "Snatcher/Mail Delivery Service" : 2000312032,
    "Boss Arena/Your Contract has Expired" : 2000311390,
    "Pipe/Time Rift" : 2000313069,
    "Village/Time Rift" : 2000313056,
    "Sleepy Subcon/Time Rift" : 2000312086,
    # "Sleepy Subcon/Pages" TODO: decide how to handle
    # "Snatcher/Contracts" : TODO: decide how to handle
    "Tree Top Ice Cube/Yarn" : 2000325469,
    "Graveyard/Ice Cube" : 2000325077,
    "Graveyard/House Top" : 2000325471,
    "Ice Cube House/Relic" : 2000325469,
    "Snatcher Statue Chest/Yarn" : 2000323730,
    "Stump Platform Chest/Yarn" : 2000323729,
    "Giant Mushroom Climb/Don't Fall~" : 2000325470,
    "Swamp Gravestone/Yarn" : 2000326296,
    "Swamp Near Well/Token" : 2000324762,
    "Swamp Tree A/Yarn" : 2000324763,
    "Swamp Tree B/Yarn" : 2000324764,
    "Swamp Ice Wall/Yarn" : 2000324706,
    "Swamp Treehouse/Relic" : 2000325468,
    "Swamp Tree Chest/Yarn" : 2000323728,
    "Dweller Stump/Yarn" : 2000324767,
    "Dweller Floating Rocks/Token" : 2000324464,
    "Dweller Platforming Tree A/Yarn" : 2000324709,
    "Dweller/Platforming Tree B" : 2000324855,
    "Giant Time Piece/Relic" : 2000325473,
    "Gallows/Relic" : 2000325472,
    "Green and Purple Dweller Rocks/Yarn" : 2000325082,
    "Dweller/Shack" : 2000324463,
    "Tall Tree Hookshot Swing/Yarn" : 2000324766,
    "Burning House/Yarn" : 2000324710,
    "Burning Tree Climb/Yarn" : 2000325079,
    "Burning Stump Chest/Token" : 2000323731,
    "Burning Forest Treehouse/Relic" : 2000325467,
    "Spider Bone Cage A/Token" : 2000324462,
    "Spider Bone Cage B/Yarn" : 2000325080,
    "Infinite Yarn Bush/Yarn" : 2000325478,
    "Magnet Badge Bush/Badge" : 2000325479,
    "Triple Spider Bounce/Yarn" : 2000324765,
    "Noose Treehouse/Relic" : 2000324856,
    "Ice Cube Shack/Token" : 2000324465,
    "Long Tree Climb Chest/Yarn" : 2000323734,
    "Boss Arena Chest/Yarn" : 2000323735,
    "Queen Vanessa's Manor/Rooftop" : 2000325466,

    # Alpine Skyline
    "Goat Village/Below Hookpoint" : 2000334856,
    "Goat Village/Hidden Branch" : 2000334855,
    "Goat Refinery/Yarn" : 2000333635,
    "Bird House/Time Piece" : 2000311428,
    "Bird Pass Fork/Yarn" : 2000335911,
    "Yellow Band Hills/Yarn" : 2000335756,
    "Purrloined Village: Horned Stone/Token" : 2000335561,
    "Purrloined Village: Chest Reward/Token" : 2000334831,
    "Bird House/Triple Crow Chest" : 2000334758,
    "Bird House/Dweller Platforms Relic" : 2000336497,
    "Bird House/Brewing Crate House" : 2000336496,
    "Bird House/Hay Bale" : 2000335885,
    "Bird House/Alpine Crow Mini-Gauntlet" : 2000335886,
    "Bird House/Outer Edge" : 2000335492,
    "Lava Cake/Time Piece" : 2000312509,
    "Mystifying Time Mesa: Zipline/Token" : 2000337058,
    "Mystifying Time Mesa: Gate Puzzle/Relic" : 2000336052,
    "Ember Summit/Yarn" : 2000336311,
    "Lava Cake/Center Fence Cage" : 2000335448,
    "Lava Cake/Outer Island Chest" : 2000334291,
    "Lava Cake/Dweller Pillars" : 2000335417,
    "Lava Cake/Top Cake" : 2000335418,
    "The Twilight Bell/Time Piece" : 2000311540,
    "The Twilight Path/Token" : 2000334434,
    "The Twilight Bell/Wide Purple Platform" : 2000336478,
    "The Twilight Bell/Ice Platform" : 2000335826,
    "The Windmill/Time Piece" : 2000312263,
    "Goat Outpost Horn/Yarn" : 2000334760,
    "Windy Passage/Yarn" : 2000334776,
    "The Windmill/Inside Pon Cluster" : 2000336395,
    "The Windmill/Entrance" : 2000335783,
    "The Windmill/Dropdown" : 2000335815,
    "The Windmill/House Window" : 2000335389,
    "The Illness has Spread/Time Piece" : 2000312022,
    "The Twilight Bell (Rift)/Time Rift" : 2000312399,
    "Curly Tail Trail/Time Rift" : 2000313335,
    "Alpine Skyline (Rift)/Time Rift" : 2000311777,
    # "Alpine Skyline (Rift)/Pages" TODO: ???

    # The Arctic Cruise
    "Control Room/Bon Voyage!" : 2000311520,
    "Lamp Post Top/Relic" : 2000305321,
    "Mafia Cargo Ship/Token" : 2000304313,
    "Lost and Found/Ship Shape" : 2000311451,
    # "Lost and Found/Tasksanity Check" : TODO: ???
    "Post Captain Rescue/Time Piece" : 2000311437,
    "Reception Room/Suitcase" : 2000304045,
    "Reception Room/Under Desk" : 2000304047,
    "Lamp Post/Token" : 2000304048,
    "Iceberg Top/Token" : 2000304046,
    "Post Captain Rescue/Behind Iceberg" : 2000304049,
    "Balcony/Time Rift" : 2000312226,
    "Deep Sea/Time Rift" : 2000312434,
    # "Deep Sea/Pages (Starfish, Mini Castle, Urchins)" TODO: ???
    # "Deep Sea/Pages (Other)" TODO: ???
    "Toilet/Relic" : 2000305109,
    "Bar/Token" : 2000304251,
    "Dive Board Ledge/Token" : 2000304254,
    "Top Balcony/Token" : 2000304255,
    "Octopus Room/Relic" : 2000305253,
    "Octopus Room Top/Token" : 2000304249,
    "Laundry Room/Token" : 2000304250,
    "Ship Side/Token" : 2000304247,
    "Silver Ring/Relic" : 2000305252,

    # Nyakuza Metro
    "Nyakuza Metro Intro/Time Piece" : 2000311138,
    "Main Station Dining Area/Rift Token" : 2000304105,
    "Top of the Ramen Shop/Rift Token" : 2000304104,
    # "Main Station Thugs/Thug A" : TODO: ???
    # "Main Station Thugs/Thug B" : TODO: ???
    # "Main Station Thugs/Thug C" : TODO: ???
    "Yellow Overpass Station/Time Piece" : 2000311206,
    "Yellow Overpass Manhole/Time Piece" : 2000311387,
    "Yellow Overpass Station - Brewing Crate/Relic" : 2000305413,
    "Yellow Overpass Station/Yellow Metro Ticket" : 2000301014,
    # "Yellow Overpass Thug A/Scammed" : TODO: ???
    # "Yellow Overpass Thug B/Scammed" : TODO: ???
    # "Yellow Overpass Thug C/Scammed" : TODO: ???
    "Green Clean Station/Time Piece" : 2000311207,
    "Green Clean Manhole/Time Piece" : 2000311388,
    "Green Ticket Booth/Green Ticket" : 2000301015,
    # "Green Clean Thug A/Scammed" : TODO: ???
    # "Green Clean Thug B/Scammed" : TODO: ???
    "Bluefin Tunnel/Time Piece" : 2000311208,
    "Bluefin Tunnel - Cat Vacuum/Relic" : 2000305111,
    "Blue Ticket Booth/Blue Ticket" : 2000301016,
    # "Bluefin Tunnel Thug/Scammed" : TODO: ???
    "Pink Paw Station/Time Piece" : 2000311209,
    "Pink Paw Manhole/Time Piece" : 2000311389,
    "Pink Paw Station - Cat Vacuum/Rift Token" : 2000305110,
    "Pink Paw Station - Behind Fan/Rift Token" : 2000304106,
    "Pink Ticket Booth/Pink Ticket" : 2000301017,
    # "Pink Paw Station Thug/Scammed" : TODO:
    "Rush Hour/Time Piece" : 2000311210,
    "Rumbi Factory/Time Rift" : 2000312736
    # "Rumbi Factory/Pages" TODO: ???

    # TODO: Continue from uhh... check Em's stuff, make sure to add comma above as needed
    # Where is the finale? And Rumbi abuse?

}

# TODO: finish
# Entrance names are "<region name> -> <connected region name>" if not defined during Region.connect
# Entrance.connect also exists, which just uses an existing entrance name
# Looks like most of the entrance names are explicitly defined in create_regions and create_rift_connections
# Not sure how to map this cleanly since some have multiple entrances. Currently arbitrarily using first
# Also not sure how to deal with Can Complete - can I map to completion time piece?
# If the functionality is half-baked, could be worth just not including entrance tracking maps
poptracker_entrance_mapping = {
    # chapter_time_rifts
    # TODO: Deal with rifts that have multiple entrances
    "Time Rift - Sewers/Can Enter" : "Welcome to Mafia Town Portal - Entrance 3",
    # "Time Rift - Sewers/Can Complete"
    "Time Rift - Bazaar/Can Enter" : "Welcome to Mafia Town Portal - Entrance 10",
    # "Time Rift - Bazaar/Can Complete"
    "Time Rift - Mafia of Cooks/Can Enter" : "Welcome to Mafia Town Portal - Entrance 17",
    # "Time Rift - Mafia of Cooks/Can Complete"
    "Time Rift - The Owl Express/Can Enter" : "Murder on the Owl Express Portal - Entrance 23",
    # "Time Rift - The Owl Express/Can Complete"
    "Time Rift - The Moon/Can Enter" : "Picture Perfect Portal - Entrance 24",
    # "Time Rift - The Moon/Can Complete"
    "Time Rift - Dead Bird Studio/Can Enter" : "Dead Bird Studio Portal - Entrance 26",
    # "Time Rift - Dead Bird Studio/Can Complete"
    "Time Rift - Pipe/Can Enter" : "Contractual Obligations Portal - Entrance 28",
    # "Time Rift - Pipe/Can Complete"
    "Time Rift - Village/Can Enter" : "Contractual Obligations Portal - Entrance 33",
    # "Time Rift - Village/Can Complete"
    "Time Rift - Sleepy Subcon/Can Enter" : "Contractual Obligations Portal - Entrance 38",
    # "Time Rift - Sleepy Subcon/Can Complete"
    "Time Rift - Twilight Bell/Can Enter" : "Alpine Free Roam Portal - Entrance 43",
    # "Time Rift - Twilight Bell/Can Complete"
    "Time Rift - Curly Tail Trail/Can Enter" : "Alpine Free Roam Portal - Entrance 44",
    # "Time Rift - Curly Tail Trail/Can Complete"
    "Time Rift - Alpine Skyline/Can Enter" : "Alpine Free Roam Portal - Entrance 45",
    # "Time Rift - Alpine Skyline/Can Complete"
    "Time Rift - Balcony/Can Enter" : "Cruise Ship Portal - Entrance 48",
    # "Time Rift - Balcony/Can Complete"
    "Time Rift - Deep Sea/Can Enter" : "Bon Voyage! Portal - Entrance 49",
    # "Time Rift - Deep Sea/Can Complete"
    "Time Rift - Rumbi Factory/Can Enter" : "Nyakuza Free Roam Portal - Entrance 50",
    # "Time Rift - Rumbi Factory/Can Complete"

    "Act 1 - Welcome to Mafia Town/Can Enter" : "Mafia Town - Act 1",
    # "Act 1 - Welcome to Mafia Town/Can Complete" : 
    "Act 2 - Barrel Battle/Can Enter" : "Mafia Town - Act 2",
    # "Act 2 - Barrel Battle/Can Complete" : 
    "Act 3 - She Came from Outer Space/Can Enter" : "Mafia Town - Act 3",
    # "Act 3 - She Came from Outer Space/Can Complete" : 
    "Act 4 - Down with the Mafia!/Can Enter" : "Mafia Town - Act 4",
    # "Act 4 - Down with the Mafia!/Can Complete" : 
    "Act 5 - Cheating the Race/Can Enter" : "Mafia Town - Act 5",
    # "Act 5 - Cheating the Race/Can Complete" : 
    "Act 6 - Heating up Mafia Town/Can Enter" : "Mafia Town - Act 6",
    # "Act 6 - Heating up Mafia Town/Can Complete" : 
    "Act 7 - The Golden Vault/Can Enter" : "Mafia Town - Act 7"
    # "Act 7 - The Golden Vault/Can Complete" : 

    # TODO: continue with chapter2? Doesn't even seem to be working. Is it worth it?
}

# TODO: adjust or remove? Does this work with deathwish variant stuff?? It might be okay with auto-tabbing...
# map tabs for UT poptracker integration, mutually exclusive with map_page_layouts
map_page_groups = {
    "spaceship",
    "mafiatown",
    "deadbirdstudio",
    "murder_on_the_owl_express",
    "the_moon",
    "train_rush",
    "basement",
    "subcon",
    "alpine",
    "cruise",
    "nyakuza",
    "entrances"
    # "use_deathwish_variant"
}
