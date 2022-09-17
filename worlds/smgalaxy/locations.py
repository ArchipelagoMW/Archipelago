from BaseClasses import Location

class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

locGE_table = {
    "GE: Dino Piranha": 170000000,
    "GE: A Snack of Cosmic Proportions": 170000001,
    "GE: King Kaliente's Battle Fleet": 170000002,
    "GE: Luigi on the Roof": 170000003,
    "GE: Dino Piranha Speed Run": 170000004,
    "GE: Purple Coin Omelet": 170000005,
}
locHH_table = {
    "HH: Bee Mario Takes Flight": 170000006,
    "HH: Trouble on the Tower": 170000007,
    "HH: Big Bad Bugabooom": 170000008,
    "HH: Luigi in the Honeyhive Kingdom": 170000011,
    "HH: Honeyhive Cosmic Mario Race": 170000009,
    "HH: Honeyhive's Purple Coins": 170000010,
}

locspecialstages_table = {
    "LDL: Surfing 101": 170000012,
    "FS: Painting the Planet Yellow": 170000013,
    "RG: Rolling in the Clouds": 170000027,
    "HS: Shrinking Satellite": 170000028,
    "BUB: Through the Poison Swamp": 170000042,
    "BB: The Floating Fortress": 170000043,
    "BB: The Secret of Buoy Base": 170000044,
    "GG: Grand Star Rescue": 170000045,
    "GG: Gateway's Purple coins": 170000046,
    "BF: Kingfin's Fearsome Waters": 170000065,
    "MS: Watch Your Step": 170000095,
    "RGT: Gizmos, Gears, and Gadgets": 170000096,
    "LDT: The Galaxy's Greatest Wave": 170000097,
    "BBT: The Electric Labyrinth": 170000098,
}

locbosses_table = {
    "BJ: Megaleg's Moon": 170000014,
    "B: The Firery Stronghold": 170000029,
    "BJ: Sinking the Airships": 170000045,
    "BJ: King Kaliente's Spicy Return": 170000066,
    "B:  Darkness on the Horizon": 170000095,
}

locSJ_table = {
    "SJ: Pull Star Path": 170000015,
    "SJ: Kamella's Airship Attack": 170000016,
    "SJ: Tarantox's Tangled Web": 170000017,
    "SJ: Yoshi's Unexpected Apparence": 170000020,
    "SJ: Pull Star Path Speed Run": 170000018,
    "SJ: Purple Coin Spacewalk": 170000019,
}
locBR_table = {
    "BR: Battlerock Barrage": 170000021,
    "BR: Breaking into the Battlerock": 170000022,
    "BR: Topmaniac's Garbage dump": 170000023,
    "BR: Topmanic's Dardevil Run": 170000024,
    "BR: Purple Coins on the Battlerock": 170000025,
    "BR: Luigi under the Saucer": 170000026,
}
locBB_table = {
    "BB: Sunken Treasure": 170000030,
    "BB: Passing the Swim Test": 170000031,
    "BB: The Secret Undersea Cavern": 170000032,
    "BB: Fast Foes on the Cyclone Stone": 170000033,
    "BB: Beachcombing for Purple Coins": 170000034,
    "BB: Wall Jumping Water Falls": 170000035,
}
locG_table = {
    "G: Luigi and the Haunted Mansion": 170000036,
    "G: A Very Spooky Spirit": 170000037,
    "G: Beware of Bouldergeist": 170000038,
    "G: Bouldergeist's Daredevil Run": 170000039,
    "G: Purple Coins in the Bone Pen": 170000040,
    "G: Matter Splatter Mansion": 170000041,
}
locGG_table = {
    "GG: Bunnies in the Wind": 170000108,
    "GG: The Dirty Tricks of Major Burrows": 170000109,
    "GG: Gusty Garden's Gravity Scramble": 170000110,
    "GG: Major Burrows's Daredevil Run": 170000111,
    "GG: Purple Coins on the Puzzle Cube": 170000112,
    "GG: The Golden Chomp": 170000113,
}
locFF_table = {
    "FF: The Frozen Peak of Baron Brr": 170000095,
    "FF: Freezeflame's Blistering Coore": 170000096,
    "FF: Hot and Cold Collide": 170000097,
    "FF: Conquring the Summit": 170000100,
    "FF: Frosty Cosmic Mario race": 170000098,
    "FF: Purple Coins on the Summit": 170000099,
}
locDDune_table = {
    "DDune: Soaring on the Desert Winds": 170000101,
    "DDune: Blasting through the Sand": 170000102,
    "DDune: Sunbaked Sand Castle": 170000103,
    "DDune: Purple Coin in the Desert": 170000105,
    "DDune: Bullet Bill on Your Back": 170000106,
    "DDune: Bullet Bill on Your Back": 170000106,
    "DDune: Treasure of the Pyramid": 170000107,
} 
locGL_table = {
    "GL: Star Bunnies on the Hunt": 170000047,
    "GL: Cataquack to the skies": 170000048,
    "GL: When it Rains, it Pours": 170000049,
    "GL: Cosmic Mario Forest Race": 170000050,
    "GL: Purple Coins in the Woods": 170000051,
    "GL: The Bell on the Big Trees": 170000052,
 }
locSS_table = {
    "SS: Going After Guppy": 170000053,
    "SS: Faster Than a Speedrunning Penguin": 170000054,
    "SS: The Silver Stars of Sea Slide": 170000055,
    "SS: Underwater Cosmic Mario Race": 170000056,
    "SS: Purple Coins by the Seaside": 170000057,
    "SS: Hurry, He's Hungry": 170000058,
}
locTT_table = {
    "TT: Heavy Metal Mecha Boswer": 170000059,
    "TT: Mario (or Luigi) Meets Mario": 170000060,
    "TT: Bouncing Down Cake Lane": 170000061,
    "TT: The Flipswitch Chain": 170000062,
    "TT: Fast Foes of Toy Time": 170000063,
    "TT: Luigi's Purple Coins": 170000064, 
}
locDD_table = {
    "DD: The Underground Ghost Ship": 170000067,
    "DD: Bubble Blastoff": 170000068,
    "DD: Guppy and the Underground Lake": 170000069,
    "DD: Ghost Ship Daredevil Run": 170000070,
    "DD: Plunder the Purple Coins": 170000071,
    "DD: Boo in Box": 170000072,
}
locDN_table = {
    "DN: Inflitrating the Dreadnought": 170000073,
    "DN: Dreanought's Colossal Cannons": 170000074,
    "DN: Revenge of the Topman Tribe": 170000075,
    "DN: Topman Tribe Speed Run": 170000076,
    "DN: Battlestation's Purple Coins": 170000077,
    "DN: Dreadnought's Garbage Dump": 170000078,
}
locMM_table = {
    "MM: The Sinking Lava Spire": 170000079,
    "MM: Through the Meteor Storm": 170000080,
    "MM: Fiery Dino Piranha": 170000081,
    "MM: Lava Spire Daredevil Run": 170000082,
    "MM: Red-Hot Purple Coins": 170000083,
    "MM Burning Tide": 170000084,
}
locHL_table = {
    "SS: Rocky Road": 170000085,
    "SP: A Very Sticky Situation": 170000086,
    "DDR: Giant Eel Breakout": 170000087,
    "BM: Bigmouth's Gold Bait": 170000088,
    "SS: Choosing a Favorite Snack": 170000089,
    "BB: Racing the Spooky Speedster": 170000090,
    "SC: Star Bunnies in the Snow": 170000091,
}
location_table = { **locGE_table,**locHH_table, \
               **locSJ_table,**locBR_table,**locBB_table, \
               **locGG_table,**locFF_table,**locDDune_table, \
               **locGL_table,**locSS_table,**locTT_table, \
               **locDD_table,**locDN_table,**locMM_table, \
               **locHL_table,**locspecialstages_table,**locbosses_table
}
