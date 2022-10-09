from BaseClasses import Location

class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

locGE_table = {
    "GE: Dino Piranha": 170000000,
    "GE: A Snack of Cosmic Proportions": 170000001,
    "GE: King Kaliente's Battle Fleet": 170000002,
    "GE: Luigi on the Roof": 170000003,
    "GE: Dino Piranha Speed Run": 170000004,
}
locHH_table = {
    "HH: Bee Mario Takes Flight": 170000006,
    "HH: Trouble on the Tower": 170000007,
    "HH: Big Bad Bugabooom": 170000008,
    "HH: Luigi in the Honeyhive Kingdom": 17000009,
    "HH: Honeyhive Cosmic Mario Race": 170000010,
}

locspecialstages_table = {
    "LDL: Surfing 101": 170000012,
    "FS: Painting the Planet Yellow": 170000013,
    "RG: Rolling in the Clouds": 170000014,
    "HS: Shrinking Satellite": 170000015,
    "BUB: Through the Poison Swamp": 170000016,
    "BB: The Floating Fortress": 170000017,
    "BB: The Secret of Buoy Base": 170000018,
    "GG: Grand Star Rescue": 170000019,
    "BF: Kingfin's Fearsome Waters": 170000021,
    "MS: Watch Your Step": 170000022,
    "RGT: Gizmos, Gears, and Gadgets": 170000023,
    "LDT: The Galaxy's Greatest Wave": 170000024,
    "BBT: The Electric Labyrinth": 170000025,
}

locbosses_table = {
    "BJ: Megaleg's Moon": 170000026,
    "B: The Firery Stronghold": 170000027,
    "BJ: Sinking the Airships": 170000028,
    "BJ: King Kaliente's Spicy Return": 170000029,
    "B:  Darkness on the Horizon": 170000030,
}

locSJ_table = {
    "SJ: Pull Star Path": 170000031,
    "SJ: Kamella's Airship Attack": 170000032,
    "SJ: Tarantox's Tangled Web": 170000033,
    "SJ: Yoshi's Unexpected Apparence": 170000034,
    "SJ: Pull Star Path Speed Run": 170000035,
}
locBR_table = {
    "BR: Battlerock Barrage": 170000037,
    "BR: Breaking into the Battlerock": 170000038,
    "BR: Topmaniac's Garbage dump": 170000039,
    "BR: Topmanic's Dardevil Run": 170000040,
    "BR: Luigi under the Saucer": 170000042,
}
locBB_table = {
    "BB: Sunken Treasure": 170000043,
    "BB: Passing the Swim Test": 170000044,
    "BB: The Secret Undersea Cavern": 170000045,
    "BB: Fast Foes on the Cyclone Stone": 170000046,
    "BB: Wall Jumping Water Falls": 170000048,
}
locG_table = {
    "G: Luigi and the Haunted Mansion": 170000049,
    "G: A Very Spooky Spirit": 170000050,
    "G: Beware of Bouldergeist": 170000051,
    "G: Bouldergeist's Daredevil Run": 170000052,
    "G: Matter Splatter Mansion": 170000054,
}
locGG_table = {
    "GG: Bunnies in the Wind": 170000055,
    "GG: The Dirty Tricks of Major Burrows": 170000056,
    "GG: Gusty Garden's Gravity Scramble": 170000057,
    "GG: Major Burrows's Daredevil Run": 170000058,
    "GG: The Golden Chomp": 170000060,
}
locFF_table = {
    "FF: The Frozen Peak of Baron Brr": 170000061,
    "FF: Freezeflame's Blistering Coore": 170000062,
    "FF: Hot and Cold Collide": 170000063,
    "FF: Conquring the Summit": 170000064,
    "FF: Frosty Cosmic Mario race": 170000065,
}
locDDune_table = {
    "DDune: Soaring on the Desert Winds": 170000067,
    "DDune: Blasting through the Sand": 170000068,
    "DDune: Sunbaked Sand Castle": 170000069,

    "DDune: Bullet Bill on Your Back": 170000071,
    "DDune: Bullet Bill on Your Back": 170000072,
    "DDune: Treasure of the Pyramid": 170000073,
} 
locGL_table = {
    "GL: Star Bunnies on the Hunt": 170000074,
    "GL: Cataquack to the skies": 170000075,
    "GL: When it Rains, it Pours": 170000076,
    "GL: Cosmic Mario Forest Race": 170000077,
    "GL: The Bell on the Big Trees": 170000079,
 }
locSS_table = {
    "SS: Going After Guppy": 170000080,
    "SS: Faster Than a Speedrunning Penguin": 170000081,
    "SS: The Silver Stars of Sea Slide": 170000082,
    "SS: Underwater Cosmic Mario Race": 170000083,
    "SS: Hurry, He's Hungry": 170000085,
}
locTT_table = {
    "TT: Heavy Metal Mecha Boswer": 170000086,
    "TT: Mario (or Luigi) Meets Mario": 170000087,
    "TT: Bouncing Down Cake Lane": 170000088,
    "TT: The Flipswitch Chain": 170000089,
    "TT: Fast Foes of Toy Time": 170000090,
}
locDD_table = {
    "DD: The Underground Ghost Ship": 170000092,
    "DD: Bubble Blastoff": 170000093,
    "DD: Guppy and the Underground Lake": 170000094,
    "DD: Ghost Ship Daredevil Run": 170000095,
    "DD: Boo in Box": 170000097,
}
locDN_table = {
    "DN: Inflitrating the Dreadnought": 170000098,
    "DN: Dreanought's Colossal Cannons": 170000099,
    "DN: Revenge of the Topman Tribe": 170000100,
    "DN: Topman Tribe Speed Run": 170000101,
    "DN: Dreadnought's Garbage Dump": 170000103,
}
locMM_table = {
    "MM: The Sinking Lava Spire": 170000104,
    "MM: Through the Meteor Storm": 170000105,
    "MM: Fiery Dino Piranha": 170000106,
    "MM: Lava Spire Daredevil Run": 170000107,
    "MM Burning Tide": 170000109,
}
locHL_table = {
    "SS: Rocky Road": 170000110,
    "SP: A Very Sticky Situation": 170000111,
    "DDR: Giant Eel Breakout": 170000112,
    "BM: Bigmouth's Gold Bait": 170000113,
    "SS: Choosing a Favorite Snack": 170000114,
    "BB: Racing the Spooky Speedster": 170000115,
    "SC: Star Bunnies in the Snow": 170000116,
}
locPC_table = {
    "TT: Luigi's Purple Coins": 170000091, 
    "DN: Battlestation's Purple Coins": 170000102,
    "MM: Red-Hot Purple Coins": 170000108,
    "DD: Plunder the Purple Coins": 170000096,
    "SS: Purple Coins by the Seaside": 170000084,
    "GE: Purple Coin Omelet": 170000005,
    "GG: Gateway's Purple coins": 170000020,
    "BR: Purple Coins on the Battlerock": 170000041,
    "SJ: Purple Coin Spacewalk": 170000036,
    "GG: Purple Coins on the Puzzle Cube": 170000059,
    "BB: Beachcombing for Purple Coins": 170000047,
    "FF: Purple Coins on the Summit": 170000066,
    "G: Purple Coins in the Bone Pen": 170000053,
    "GL: Purple Coins in the Woods": 170000078,
    "DDune: Purple Coin in the Desert": 170000070,
    "HH: The Honeyhive's Purple Coins": 170000011,
}
location_table = { **locGE_table,**locHH_table, \
                   **locSJ_table,**locBR_table,**locBB_table, \
                   **locGG_table,**locFF_table,**locDDune_table, \
                   **locGL_table,**locSS_table,**locTT_table, \
                   **locDD_table,**locDN_table,**locMM_table, \
                   **locPC_table,**locHL_table,**locspecialstages_table,**locbosses_table
}
