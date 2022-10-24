from BaseClasses import Location

class SM64Location(Location):
    game: str = "Super Mario 64"

#Bob-omb Battlefield
locBoB_table = {
    "BoB: Big Bob-Omb on the Summit": 3626000,
    "BoB: Footrace with Koopa The Quick": 3626001,
    "BoB: Shoot to the Island in the Sky": 3626002,
    "BoB: Find the 8 Red Coins": 3626003,
    "BoB: Mario Wings to the Sky": 3626004,
    "BoB: Behind Chain Chomp's Gate": 3626005,
    "BoB: Bob-omb Buddy": 3626200,
}

#Whomp's Fortress
locWhomp_table = {
    "WF: Chip Off Whomp's Block": 3626007,
    "WF: To the Top of the Fortress": 3626008,
    "WF: Shoot into the Wild Blue": 3626009,
    "WF: Red Coins on the Floating Isle": 3626010,
    "WF: Fall onto the Caged Island": 3626011,
    "WF: Blast Away the Wall": 3626012,
    "WF: Bob-omb Buddy": 3626201,
}

#Jolly Roger Bay
locJRB_table = {
    "JRB: Plunder in the Sunken Ship": 3626014,
    "JRB: Can the Eel Come Out to Play?": 3626015,
    "JRB: Treasure of the Ocean Cave": 3626016,
    "JRB: Red Coins on the Ship Afloat": 3626017,
    "JRB: Blast to the Stone Pillar": 3626018,
    "JRB: Through the Jet Stream": 3626019,
    "JRB: Bob-omb Buddy": 3626202,
}


#Cool, Cool Mountain
locCCM_table = {
    "CCM: Slip Slidin' Away": 3626021,
    "CCM: Li'l Penguin Lost": 3626022,
    "CCM: Big Penguin Race": 3626023,
    "CCM: Frosty Slide for 8 Red Coins": 3626024,
    "CCM: Snowman's Lost His Head": 3626025,
    "CCM: Wall Kicks Will Work": 3626026,
    "CCM: Bob-omb Buddy": 3626203,
    "CCM: 1Up Block Near Snowman": 3626215,
    "CCM: 1Up Block Ice Pillar": 3626216,
    "CCM: 1Up Block Secret Slide": 3626217
}

#Big Boo's Haunt
locBBH_table = {
    "BBH: Go on a Ghost Hunt": 3626028,
    "BBH: Ride Big Boo's Merry-Go-Round": 3626029,
    "BBH: Secret of the Haunted Books": 3626030,
    "BBH: Seek the 8 Red Coins": 3626031,
    "BBH: Big Boo's Balcony": 3626032,
    "BBH: Eye to Eye in the Secret Room": 3626033,
    "BBH: 1Up Block Top of Mansion": 3626218
}

#Hazy Maze Cave
locHMC_table = {
    "HMC: Swimming Beast in the Cavern": 3626035,
    "HMC: Elevate for 8 Red Coins": 3626036,
    "HMC: Metal-Head Mario Can Move!": 3626037,
    "HMC: Navigating the Toxic Maze": 3626038,
    "HMC: A-Maze-Ing Emergency Exit": 3626039,
    "HMC: Watch for Rolling Rocks": 3626040,
    "HMC: 1Up Block above Pit": 3626219,
    "HMC: 1Up Block Past Rolling Rocks": 3626220,
}

#Lethal Lava Land
locLLL_table = {
    "LLL: Boil the Big Bully": 3626042,
    "LLL: Bully the Bullies": 3626043,
    "LLL: 8-Coin Puzzle with 15 Pieces": 3626044,
    "LLL: Red-Hot Log Rolling": 3626045,
    "LLL: Hot-Foot-It into the Volcano": 3626046,
    "LLL: Elevator Tour in the Volcano": 3626047
}

#Shifting Sand Land
locSSL_table = {
    "SSL: In the Talons of the Big Bird": 3626049,
    "SSL: Shining Atop the Pyramid": 3626050,
    "SSL: Inside the Ancient Pyramid": 3626051,
    "SSL: Stand Tall on the Four Pillars": 3626052,
    "SSL: Free Flying for 8 Red Coins": 3626053,
    "SSL: Pyramid Puzzle": 3626054,
    "SSL: Bob-omb Buddy": 3626207,
    "SSL: 1Up Block Outside Pyramid": 3626221,
    "SSL: 1Up Block Pyramid Left Path": 3626222,
    "SSL: 1Up Block Pyramid Back": 3626223
}

#Dire, Dire Docks
locDDD_table = {
    "DDD: Board Bowser's Sub": 3626056,
    "DDD: Chests in the Current": 3626057,
    "DDD: Pole-Jumping for Red Coins": 3626058,
    "DDD: Through the Jet Stream": 3626059,
    "DDD: The Manta Ray's Reward": 3626060,
    "DDD: Collect the Caps...": 3626061
}

#Snowman's Land
locSL_table = {
    "SL: Snowman's Big Head": 3626063,
    "SL: Chill with the Bully": 3626064,
    "SL: In the Deep Freeze": 3626065,
    "SL: Whirl from the Freezing Pond": 3626066,
    "SL: Shell Shreddin' for Red Coins": 3626067,
    "SL: Into the Igloo": 3626068,
    "SL: Bob-omb Buddy": 3626209,
    "SL: 1Up Block Near Moneybags": 3626224,
    "SL: 1Up Block inside Igloo": 3626225
}

#Wet-Dry World
locWDW_table = {
    "WDW: Shocking Arrow Lifts!": 3626070,
    "WDW: Top o' the Town": 3626071,
    "WDW: Secrets in the Shallows & Sky": 3626072,
    "WDW: Express Elevator--Hurry Up!": 3626073,
    "WDW: Go to Town for Red Coins": 3626074,
    "WDW: Quick Race Through Downtown!": 3626075,
    "WDW: Bob-omb Buddy": 3626210,
    "WDW: 1Up Block in Downtown": 3626226
}

#Tall, Tall Mountain
locTTM_table = {
    "TTM: Scale the Mountain": 3626077,
    "TTM: Mystery of the Monkey Cage": 3626078,
    "TTM: Scary 'Shrooms, Red Coins": 3626079,
    "TTM: Mysterious Mountainside": 3626080,
    "TTM: Breathtaking View from Bridge": 3626081,
    "TTM: Blast to the Lonely Mushroom": 3626082,
    "TTM: Bob-omb Buddy": 3626211,
    "TTM: 1Up Block on Red Mushroom": 3626227
}

#Tiny-Huge Island
locTHI_table = {
    "THI: Pluck the Piranha Flower": 3626084,
    "THI: The Tip Top of the Huge Island": 3626085,
    "THI: Rematch with Koopa the Quick": 3626086,
    "THI: Five Itty Bitty Secrets": 3626087,
    "THI: Wiggler's Red Coins": 3626088,
    "THI: Make Wiggler Squirm": 3626089,
    "THI: Bob-omb Buddy": 3626212,
    "THI: 1Up Block THI Small near Start": 3626228,
    "THI: 1Up Block THI Large near Start": 3626229,
    "THI: 1Up Block Windy Area": 3626230
}

#Tick Tock Clock
locTTC_table = {
    "TTC: Roll into the Cage": 3626091,
    "TTC: The Pit and the Pendulums": 3626092,
    "TTC: Get a Hand": 3626093,
    "TTC: Stomp on the Thwomp": 3626094,
    "TTC: Timed Jumps on Moving Bars": 3626095,
    "TTC: Stop Time for Red Coins": 3626096,
    "TTC: 1Up Block Midway Up": 3626231,
    "TTC: 1Up Block at the Top": 3626232
}

#Rainbow Ride
locRR_table = {
    "RR: Cruiser Crossing the Rainbow": 3626098,
    "RR: The Big House in the Sky": 3626099,
    "RR: Coins Amassed in a Maze": 3626100,
    "RR: Swingin' in the Breeze": 3626101,
    "RR: Tricky Triangles!": 3626102,
    "RR: Somewhere Over the Rainbow": 3626103,
    "RR: Bob-omb Buddy": 3626214,
    "RR: 1Up Block Top of Red Coin Maze": 3626233,
    "RR: 1Up Block Under Fly Guy": 3626234,
    "RR: 1Up Block On House in the Sky": 3626235
}

loc100Coin_table = {
        "BoB: 100 Coins": 3626006,
        "WF: 100 Coins": 3626013,
        "JRB: 100 Coins": 3626020,
        "CCM: 100 Coins": 3626027,
        "BBH: 100 Coins": 3626034,
        "HMC: 100 Coins": 3626041,
        "LLL: 100 Coins": 3626048,
        "SSL: 100 Coins": 3626055,
        "DDD: 100 Coins": 3626062,
        "SL: 100 Coins": 3626069,
        "WDW: 100 Coins": 3626076,
        "TTM: 100 Coins": 3626083,
        "THI: 100 Coins": 3626090,
        "TTC: 100 Coins": 3626097,
        "RR: 100 Coins": 3626104
}

locPSS_table = {
    "The Princess's Secret Slide Block": 3626126,
    "The Princess's Secret Slide Fast": 3626127,
}

locSA_table = {
    "The Secret Aquarium": 3626161
}

locBitDW_table = {
    "Bowser in the Dark World Red Coins": 3626105,
    "Bowser in the Dark World Key": 3626178,
    "Bowser in the Dark World 1Up Block on Tower": 3626236,
    "Bowser in the Dark World 1Up Block near Goombas": 3626237
}

locTotWC_table = {
    "Tower of the Wing Cap Switch": 3626181,
    "Tower of the Wing Cap Red Coins": 3626140
}

locCotMC_table = {
    "Cavern of the Metal Cap Switch": 3626182,
    "Cavern of the Metal Cap Red Coins": 3626133,
    "Cavern of the Metal Cap 1Up Block": 3626241
}

locVCutM_table = {
    "Vanish Cap Under the Moat Switch": 3626183,
    "Vanish Cap Under the Moat Red Coins": 3626147,
    "Vanish Cap Under the Moat 1Up Block": 3626242
}

locBitFS_table = {
    "Bowser in the Fire Sea Red Coins": 3626112,
    "Bowser in the Fire Sea Key": 3626179,
    "Bowser in the Fire Sea 1Up Block Swaying Stairs": 3626238,
    "Bowser in the Fire Sea 1Up Block Near Poles": 3626239
}

locWMotR_table = {
    "Wing Mario Over the Rainbow Red Coins": 3626154,
    "Wing Mario Over the Rainbow 1Up Block": 3626243
}

locBitS_table = {
    "Bowser in the Sky Red Coins": 3626119,
    "Bowser in the Sky 1Up Block": 3626240
}

#Secret Stars found inside the Castle
locSS_table = {
    "Toad (Basement)": 3626168,
    "Toad (Second Floor)": 3626169,
    "Toad (Third Floor)": 3626170,
    "MIPS 1": 3626171,
    "MIPS 2": 3626172
}

# Correspond to 3626000 + course index * 7 + star index, then secret stars, then keys, then 100 Coin Stars
location_table = {**locBoB_table,**locWhomp_table,**locJRB_table,**locCCM_table,**locBBH_table, \
                  **locHMC_table,**locLLL_table,**locSSL_table,**locDDD_table,**locSL_table, \
                  **locWDW_table,**locTTM_table,**locTHI_table,**locTTC_table,**locRR_table, \
                  **loc100Coin_table,**locPSS_table,**locSA_table,**locBitDW_table,**locTotWC_table, \
                  **locCotMC_table, **locVCutM_table, **locBitFS_table, **locWMotR_table, **locBitS_table, \
                  **locSS_table}
