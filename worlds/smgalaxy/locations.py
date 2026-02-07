from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, Region


def purplecoinstar(multiworld, player):
    return multiworld.enable_purple_coin_stars[player].value < 2

def maingameonly(multiworld, player):
    return multiworld.enable_purple_coin_stars[player].value == 1

class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMGLocation, self).__init__(player, name, address=location_table[name], parent=parent)
        self.code = location_table[name]

class SMGLocationData(NamedTuple):
    location_groups: list[str] # type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    game_address: Optional[int] = 0  #

# good egg galaxy

locGE_table: dict[str, SMGLocationData] = {
    "GE: Dino Piranha": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 17000000),
    "GE: A Snack of Cosmic Proportions": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 17000001),
    "GE: King Kaliente's Battle Fleet": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 17000002),
    "GE: Luigi on the Roof": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 17000003),
    "GE: Dino Piranha Speed Run": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 17000004),
}

locHH_table: dict[str, SMGLocationData]  = {
    "HH: Bee Mario Takes Flight": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 17000006),
    "HH: Trouble on the Tower": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 17000007),
    "HH: Big Bad Bugabooom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 17000008),
    "HH: Luigi in the Honeyhive Kingdom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 17000009),
    "HH: Honeyhive Cosmic Mario Race": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 170000010)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    "LDL: Surfing 101": SMGLocationData(["Loopdeloop Galaxy", "Power Star"], "Loopdeloop", 170000012),
    "FS: Painting the Planet Yellow": SMGLocationData(["Flipswitch Galaxy", "Power Star"], "Flipswitch", 170000013),
    "RG: Rolling in the Clouds": SMGLocationData(["Rolling Green Galaxy", "Power Star"], "Rolling Green", 170000014),
    "HS: Shrinking Satellite": SMGLocationData(["Hurry-Scurry Galaxy", "Power Star"], "Hurry-Scurry", 170000015),
    "BUB: Through the Poison Swamp": SMGLocationData(["Bubble Breeze Galaxy", "Power Star"], "Bubble Breeze", 170000016),
    "HC: Scaling the Sticky Wall": SMGLocationData(["Honeyclimb Galaxy", "Power Star"], "Honeyclimb", 170000118),
    "BB: The Floating Fortress": SMGLocationData(["Buoy Base Galaxy", "Power Star"], "Buoy Base", 170000017),
    "BB: The Secret of Buoy Base": SMGLocationData(["Buoy Base Galaxy", "Power Star"], "Buoy Base", 170000018),
  # TO DO ADD BACK WHEN MORE THEN ONE CHECK IN FIRST LEVEL , REQUIRES GOAL FOR REVIST
  # "GG: Grand Star Rescue": SMGLocationData(["Gateway Galaxy", "Power Star"], "Gateway Galaxy", 170000019),
    "BF: Kingfin's Fearsome Waters": SMGLocationData(["Bonefin Galaxy", "Power Star"], "Bonefin", 170000021),
    "MS: Watch Your Step": SMGLocationData(["Matter Splatter Galaxy", "Power Star"], "Matter Splatter", 170000022),
    "RGT: Gizmos, Gears, and Gadgets": SMGLocationData(["Rolling Gizmo Galaxy", "Power Star"], "Rolling Gizmo", 170000023),
    "LDT: The Galaxy's Greatest Wave": SMGLocationData(["Loopdeeswoop Galaxy", "Power Star"], "Loopdeeswoop", 170000024),
    "BBT: The Electric Labyrinth": SMGLocationData(["Bubble Blast Galaxy", "Power Star"], "Bubble Blast", 170000025)
}

locbosses_table: dict[str, SMGLocationData]  = {
    "BJ: Megaleg's Moon": SMGLocationData(["Bowser Jr.'s Robot Reactor", "Power Star"], "Bowser Jr.'s Robot Reactor", 170000026),
    "B: The Fiery Stronghold": SMGLocationData(["Bowser's Star Reactor", "Power Star"], "Bowser's Star Reactor", 170000027),
    "BJ: Sinking the Airships": SMGLocationData(["Bowser Jr.'s Airship Armada", "Power Star"], "Bowser Jr.'s Airship Armada", 170000028),
    "BJ: King Kaliente's Spicy Return": SMGLocationData(["Bowser Jr.'s Lava Reactor", "Power Star"], "Bowser Jr.'s Lava Reactor", 170000029),
    "B: Darkness on the Horizon": SMGLocationData(["Bowser's Dark Matter Plant", "Power Star"], "Bowser's Dark Matter Plant", 170000030),
    "B: The Fate of the Universe": SMGLocationData(["Bowser's Galaxy Reactor", "Power Star"], "Bowser's Galaxy Reactor", 170000120)
}

locSJ_table: dict[str, SMGLocationData]  = {
    "SJ: Pull Star Path": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000031),
    "SJ: Kamella's Airship Attack": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000032),
    "SJ: Tarantox's Tangled Web": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000033),
    "SJ: Yoshi's Unexpected Apparence": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000034),
    "SJ: Pull Star Path Speed Run": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000035)
}

locBR_table: dict[str, SMGLocationData]  = {
    "BR: Battlerock Barrage": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000037),
    "BR: Breaking into the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000038),
    "BR: Topmaniac and Topman Tribe": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000119),
    "BR: Battlerock's Garbage dump": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000039),
    "BR: Topmanic's Dardevil Run": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000040),
    "BR: Luigi under the Saucer": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 170000042)
}

locBB_table: dict[str, SMGLocationData]  = {
    "BB: Sunken Treasure": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], "Beach Bowl", 170000043),
    "BB: Passing the Swim Test": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], "Beach Bowl", 170000044),
    "BB: The Secret Undersea Cavern": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], "Beach Bowl", 170000045),
    "BB: Fast Foes on the Cyclone Stone": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], "Beach Bowl", 170000046),
    "BB: Wall Jumping Up Waterfalls": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], "Beach Bowl", 170000048)
}

locG_table: dict[str, SMGLocationData]  = {
    "G: Luigi and the Haunted Mansion": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly Bowl", 170000049),
    "G: A Very Spooky Spirit": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly Bowl", 170000050),
    "G: Beware of Bouldergeist": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly Bowl", 170000051),
    "G: Bouldergeist's Daredevil Run": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly Bowl", 170000052),
    "G: Matter Splatter Mansion": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly Bowl", 170000054)
}

locGG_table: dict[str, SMGLocationData]  = {
    "GG: Bunnies in the Wind": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000055),
    "GG: The Dirty Tricks of Major Burrows": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000056),
    "GG: Gusty Garden's Gravity Scramble": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000057),
    "GG: Major Burrows's Daredevil Run": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000058),
    "GG: The Golden Chomp": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000060)
}

locFF_table: dict[str, SMGLocationData]  = {
    "FF: The Frozen Peak of Baron Brr": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000061),
    "FF: Freezeflame's Blistering Coore": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000062),
    "FF: Hot and Cold Collide": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000063),
    "FF: Conquring the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000064),
    "FF: Frosty Cosmic Mario race": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000065)
}

locDDune_table: dict[str, SMGLocationData]  = {
    "DDune: Soaring on the Desert Winds": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000067),
    "DDune: Blasting through the Sand": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000068),
    "DDune: Sunbaked Sand Castle": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000069),
    "DDune: Sandblast Speed Run": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000071),
    "DDune: Bullet Bill on Your Back": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000072),
    "DDune: Treasure of the Pyramid": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000073)
} 

locGL_table: dict[str, SMGLocationData]  = {
    "GL: Star Bunnies on the Hunt": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000074),
    "GL: Cataquack to the skies": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000075),
    "GL: When it Rains, it Pours": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000076),
    "GL: Cosmic Mario Forest Race": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000077),
    "GL: The Bell on the Big Trees": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000079)
}

locSS_table: dict[str, SMGLocationData]  = {
    "SS: Going After Guppy": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000080),
    "SS: Faster Than a Speedrunning Penguin": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000081),
    "SS: The Silver Stars of Sea Slide": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000082),
    "SS: Underwater Cosmic Mario Race": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000083),
    "SS: Hurry, He's Hungry": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000085)
}

locTT_table: dict[str, SMGLocationData]  = {
    "TT: Heavy Metal Mecha Boswer": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000086),
    "TT: Mario (or Luigi) Meets Mario": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000087),
    "TT: Bouncing Down Cake Lane": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000088),
    "TT: The Flipswitch Chain": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000089),
    "TT: Fast Foes of Toy Time": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000090)
}

locDD_table: dict[str, SMGLocationData]  = {
    "DD: The Underground Ghost Ship": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000092),
    "DD: Bubble Blastoff": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000093),
    "DD: Guppy and the Underground Lake": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000094),
    "DD: Ghost Ship Daredevil Run": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000095),
    "DD: Boo in Box": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000097)
}

locDN_table: dict[str, SMGLocationData]  = {
    "DN: Inflitrating the Dreadnought": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000098),
    "DN: Dreadnought's Colossal Cannons": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000099),
    "DN: Revenge of the Topman Tribe": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000100),
    "DN: Topman Tribe Speed Run": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000101),
    "DN: Dreadnought's Garbage Dump": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000103)
}

locMM_table: dict[str, SMGLocationData]  = {
    "MM: The Sinking Lava Spire": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000104),
    "MM: Through the Meteor Storm": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000105),
    "MM: Fiery Dino Piranha": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000106),
    "MM: Lava Spire Daredevil Run": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000107),
    "MM Burning Tide": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000109)
}

locHL_table: dict[str, SMGLocationData]  = {
    "SS: Rocky Road": SMGLocationData(["Sweet Sweet Galaxy", "Power Star"], "Sweet Sweet", 170000110),
    "SP: A Very Sticky Situation": SMGLocationData(["Sling Pod Galaxy", "Power Star"], "Sling Pod", 170000111),
    "DDR: Giant Eel Breakout": SMGLocationData(["Drip Drop Galaxy", "Power Star"], "Drip Drop", 170000112),
    "BM: Bigmouth's Gold Bait": SMGLocationData(["Bigmouth Galaxy", "Power Star"], "Bigmouth", 170000113),
    "Sandy Spiral: Choosing a Favorite Snack": SMGLocationData(["Sand Spiral Galaxy", "Power Star"], "Sand Spiral", 170000114),
    "Bone's Boneyard: Racing the Spooky Speedster": SMGLocationData(["Boo's Boneyard Galaxy", "Power Star"], "Boo's Boneyard", 170000115),
    "SC: Star Bunnies in the Snow": SMGLocationData(["Snow Cap Galaxy", "Power Star"], "Snow Cap", 170000116)
}

locPC_table: dict[str, SMGLocationData]  = {
    "TT: Luigi's Purple Coins": SMGLocationData(["Toy Time Galaxy", "Power Star"], "Toy Time", 170000091),
    "DN: Battlestation's Purple Coins": SMGLocationData(["Dreadnought Galaxy", "Power Star"], "Dreadnought", 170000102),
    "MM: Red-Hot Purple Coins": SMGLocationData(["Melty Molten Galaxy", "Power Star"], "Melty Molten", 170000108),
    "DD: Plunder the Purple Coins": SMGLocationData(["Deep Dark Galaxy", "Power Star"], "Deep Dark", 170000096),
    "SS: Purple Coins by the Seaside": SMGLocationData(["Sea Slide Galaxy", "Power Star"], "Sea Slide", 170000084),
    "GE: Purple Coin Omelet": SMGLocationData(["Good Egg Galaxy", "Power Star"], "Good Egg", 170000005),
    "GG: Gateway's Purple coins": SMGLocationData(["Gateway Galaxy", "Power Star"], "Gateway Garden", 170000020),
    "BR: Purple Coins on the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star"], "Battlerock", 17000004),
    "SJ: Purple Coin Spacewalk": SMGLocationData(["Space Junk Galaxy", "Power Star"], "Space Junk", 170000036),
    "GG: Purple Coins on the Puzzle Cube": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], "Gusty Garden", 170000059),
    "BB: Beachcombing for Purple Coins": SMGLocationData(["Bubble Breeze Galaxy", "Power Star"], "Bubble Breeze", 170000047),
    "FF: Purple Coins on the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star"], "Freezeflame", 170000066),
    "G: Purple Coins in the Bone Pen": SMGLocationData(["Ghostly Galaxy", "Power Star"], "Ghostly", 170000053),
    "GL: Purple Coins in the Woods": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], "Gold Leaf", 170000078),
    "DDune: Purple Coin in the Desert": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], "Dusty Dune", 170000070),
    "HH: The Honeyhive's Purple Coins": SMGLocationData(["Honeyhive Galaxy", "Power Star"], "Honeyhive", 170000011)
}

location_table = { **locGE_table, **locHH_table, 
                   **locSJ_table, **locBR_table, **locBB_table, 
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table, 
                   **locGL_table, **locSS_table, **locTT_table, 
                   **locDD_table, **locDN_table, **locMM_table, 
                   **locHL_table, **locspecialstages_table, **locbosses_table, 
                   **locPC_table,
}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: SMGLocationData.code for name, data in location_table.items() if data.code is not None}