from BaseClasses import Location

class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

locGE_table = {
    "GE: Dino Piranha": 170000000,
    "GE: A Snack of Cosmic Proportions": 170000001,
    "GE: King Kaliente's Battle Fleet": 170000002,
    "GE: Luigi on the Roof": 170000003,
}
locHH_table = {
    "HH: Bee Mario Takes Flight": 170000006,
    "HH: Trouble on the Tower": 170000007,
    "HH: Big Bad Bugabooom": 170000008,
    "HH: Luigi in the Honeyhive Kingdom": 170000011,
}
locspecialstages_table ={
    "LDL: Surfing 101": 170000012,
    "FS: Painting the Planet Yellow": 170000013,
    "RG: Rolling in the Clouds": 170000028,
    "HS: Shrinking Satellite": 170000029,
    "BUB: Through the Poison Swamp": 170000043,
    "BB: The Floating Fortress": 170000044,
    "BB: The Secret of Buoy Base": 170000045,
    "GG: Grand Star Rescue": 170000047,
    "GG: Gateway's Purple coins": 170000048,
    "BF: Kingfin's Fearsome Waters": 170000067,
    "MS: Watch Your Step": 170000095,
    "RGT: Gizmos, Gears, and Gadgets": 170000096,
    "LDT: The Galaxy's Greatest Wave": 170000097,
    "BBT: The Electric Labyrinth": 170000098,
}
locbosses_table = {
    "BJ: Megaleg's Moon": 170000014,
    "B: The Firery Stronghold": 170000030,
    "BJ: Sinking the Airships": 170000045,
    "BJ: King Kaliente's Spicy Return": 170000067
    "B: The Fate of the Universe": 170000095,
}
locSJ_table = {
    "SJ: Pull Star Path": 170000015,
    "SJ: Kamella's Airship Attack": 170000016,
    "SJ: Tarantox's Tangled Web": 170000017,
    "SJ: Yoshi's Unexpected Apparence": 170000020,
}
locBR_table = {
    "BR: Battlerock Barrage": 170000021,
    "BR: Breaking into the Battlerock": 170000022,
    "BR: Topmaniac's Garbage dump": 170000023,
    "BR: Luigi under the Saucer" 170000027,
}
locBB_table = {
    "BB: Sunken Treasure": 170000031,
    "BB: Passing the Swim Test": 170000032,
    "BB: The Secret Undersea Cavern": 170000033
    "BB: Wall Jumping Water Falls": 170000036,
}
locG_table = {
    "G: Luigi and the Haunted Mansion": 170000037,
    "G: A Very Spooky Spirit": 170000038,
    "G: Beware of Bouldergeist": 170000039,
    "G: Matter Splatter Mansion": 170000042,
}
locGG_table = {
    "GG: Bunnies in the Wind": 170000108,
    "GG: The Dirty Tricks of Major Burrows", 170000109,
    "GG: Gusty Garden's Gravity Scramble": 170000110,
    "GG: The Golden Chomp": 170000113,
}
locFF_table = {
    "FF: The Frozen Peak of Baron Brr": 170000095,
    "FF: Freezeflame's Blistering Coore": 170000096,
    "FF: Hot and Cold Collide": 170000097,
    "FF: Conquring the Summit" 170000100,
}
locDDune = {
    "DDune: Soaring on the Desert Winds": 170000101,
    "DDune: Blasting through the Sand": 170000102,
    "DDune: Sunbaked Sand Castle": 170000103,
    "DDune: Bullet Bill on Your Back": 170000106,
    "DDune: Treasure of the Pyramid": 170000107,
} 
locGL_table = {
    "GL: Star Bunnies on the Hunt": 170000049,
    "GL: Cataquack to the skies": 170000050,
    "GL: When it Rains, it Pours": 170000051,
    "GL: The Bell on the Big Trees": 170000054,
 }
locSS_table = {
    "SS: Going After Guppy": 170000055,
    "SS: Faster Than a Speedrunning Penguin": 170000056,
    "SS: The Silver Stars of Sea Slide": 170000057,
    "SS: Hurry, He's Hungry": 170000060,
}
locTT_table = {
    "TT: Heavy Metal Mecha Boswer": 170000061,
    "TT: Mario (or Luigi) Meets Mario": 170000062,
    "TT: Bouncing Down Cake Lane": 170000063,
    "TT: The Flipswitch Chain": 170000064,
}
locDD_table = {
    "DD: The Underground Ghost Ship": 170000069,
    "DD: Bubble Blastoff": 170000070,
    "DD: Guppy and the Underground Lake": 170000071,
    "DD: Boo in Box": 170000074,
}
locDN_table = {
    "DN: Inflitrating the Dreadnought": 170000075,
    "DN: Dreanought's Colossal Cannons": 170000076,
    "DN: Revenge of the Topman Tribe": 170000077,
    "DN: Dreadnought's Garbage Dump": 170000080,
}
locMM_table = {
    "MM: The Sinking Lava Spire": 170000081,
    "MM: Through the Meteor Storm": 170000082,
    "MM: Fiery Dino Piranha": 170000083,
    "MM Burning Tide": 170000086,
}
locHL_table = {
    "SS: Rocky Road": 170000088,
    "SP: A Very Sticky Situation": 170000089,
    "DDR: Giant Eel Breakout": 170000090,
    "BM: Bigmouth's Gold Bait": 170000091,
    "SS: Choosing a Favorite Snack": 170000092,
    "BB: Racing the Spooky Speedster": 170000093,
    "SC: Star Bunnies in the Snow": 170000094,
}
location_table{**locGE_table,**locHH_table, \
               **locSJ_table,**locBR_table,**locBB_table, \
               **locGG_table,**locFF_table,**locDDune_table, \
               **locGL_table,**locSS_table,**locTT_table, \
               **locDD_table,**locDN_table,**locMM_table, \
               **locHL_table,**locspecialstages_table,**locbosses_table, \
} 