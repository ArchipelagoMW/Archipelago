from typing import Callable, Dict, NamedTuple, Optional
from BaseClasses import Location, Region

from.Constants.Names import region_names as regname

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
    default_access: Optional[dict[str, int]] = {}

# good egg galaxy

locGE_table: dict[str, SMGLocationData] = {
    "GE: Dino Piranha": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000000),
    "GE: A Snack of Cosmic Proportions": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000001),
    "GE: King Kaliente's Battle Fleet": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000002),
    "GE: Luigi on the Roof": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000003),
    "GE: Dino Piranha Speed Run": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000004),
}

locHH_table: dict[str, SMGLocationData]  = {
    "HH: Bee Mario Takes Flight": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000006),
    "HH: Trouble on the Tower": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000007),
    "HH: Big Bad Bugabooom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000008),
    "HH: Luigi in the Honeyhive Kingdom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000009),
    "HH: Honeyhive Cosmic Mario Race": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 170000010)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    "LDL: Surfing 101": SMGLocationData(["Loopdeloop Galaxy", "Power Star"], regname.LOOPDEELOOP, 170000012),
    "FS: Painting the Planet Yellow": SMGLocationData(["Flipswitch Galaxy", "Power Star"], regname.FLIPSWITCH, 170000013),
    "RG: Rolling in the Clouds": SMGLocationData(["Rolling Green Galaxy", "Power Star"], regname.ROLLINGGREEN, 170000014),
    "HS: Shrinking Satellite": SMGLocationData(["Hurry-Scurry Galaxy", "Power Star"], regname.HURRYSCUR, 170000015),
    "BUB: Through the Poison Swamp": SMGLocationData(["Bubble Breeze Galaxy", "Power Star"], regname.BUBBLEBREEZE, 170000016),
    "HC: Scaling the Sticky Wall": SMGLocationData(["Honeyclimb Galaxy", "Power Star"], regname.HONEYCLIMB, 170000118),
    "BB: The Floating Fortress": SMGLocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000017),
    "BB: The Secret of Buoy Base": SMGLocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000018),
  # TO DO ADD BACK WHEN MORE THEN ONE CHECK IN FIRST LEVEL , REQUIRES GOAL FOR REVIST
    "GG: Grand Star Rescue": SMGLocationData([regname.GATEWAY, "Power Star"], regname.GATEWAY, 170000019),
    "BF: Kingfin's Fearsome Waters": SMGLocationData(["Bonefin Galaxy", "Power Star"], regname.BONEFIN, 170000021),
    "MS: Watch Your Step": SMGLocationData(["Matter Splatter Galaxy", "Power Star"], regname.MATTER, 170000022),
    "RGT: Gizmos, Gears, and Gadgets": SMGLocationData(["Rolling Gizmo Galaxy", "Power Star"], regname.ROLLINGGIZ, 170000023),
    "LDT: The Galaxy's Greatest Wave": SMGLocationData(["Loopdeeswoop Galaxy", "Power Star"], regname.LOOPDEESWOOP, 170000024),
    "BBT: The Electric Labyrinth": SMGLocationData(["Bubble Blast Galaxy", "Power Star"], regname.BUBBLEBLAST, 170000025)
}

locbosses_table: dict[str, SMGLocationData]  = {
    "BJ: Megaleg's Moon": SMGLocationData([regname.BOWJR1, "Power Star"], regname.BOWJR1, 170000026),
    "B: The Fiery Stronghold": SMGLocationData([regname.BOWSER1, "Power Star"], regname.BOWSER1, 170000027),
    "BJ: Sinking the Airships": SMGLocationData([regname.BOWJR2, "Power Star"], regname.BOWJR2, 170000028),
    "BJ: King Kaliente's Spicy Return": SMGLocationData([regname.BOWJR3, "Power Star"], regname.BOWJR3, 170000029),
    "B: Darkness on the Horizon": SMGLocationData([regname.BOWSER2, "Power Star"], regname.BOWSER2, 170000030),
    "B: The Fate of the Universe": SMGLocationData([regname.BOWSER3, "Power Star"], regname.BOWSER3, 170000120)
}

locSJ_table: dict[str, SMGLocationData]  = {
    "SJ: Pull Star Path": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000031),
    "SJ: Kamella's Airship Attack": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000032),
    "SJ: Tarantox's Tangled Web": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000033),
    "SJ: Yoshi's Unexpected Apparence": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000034),
    "SJ: Pull Star Path Speed Run": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000035)
}

locBR_table: dict[str, SMGLocationData]  = {
    "BR: Battlerock Barrage": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000037),
    "BR: Breaking into the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000038),
    "BR: Topmaniac and Topman Tribe": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000119),
    "BR: Battlerock's Garbage dump": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000039),
    "BR: Topmanic's Dardevil Run": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000040),
    "BR: Luigi under the Saucer": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000042)
}

locBB_table: dict[str, SMGLocationData]  = {
    "BB: Sunken Treasure": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000043),
    "BB: Passing the Swim Test": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000044),
    "BB: The Secret Undersea Cavern": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000045),
    "BB: Fast Foes on the Cyclone Stone": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000046),
    "BB: Wall Jumping Up Waterfalls": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000048)
}

locG_table: dict[str, SMGLocationData]  = {
    "G: Luigi and the Haunted Mansion": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000049),
    "G: A Very Spooky Spirit": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000050),
    "G: Beware of Bouldergeist": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000051),
    "G: Bouldergeist's Daredevil Run": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000052),
    "G: Matter Splatter Mansion": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000054)
}

locGG_table: dict[str, SMGLocationData]  = {
    "GG: Bunnies in the Wind": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000055),
    "GG: The Dirty Tricks of Major Burrows": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000056),
    "GG: Gusty Garden's Gravity Scramble": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000057),
    "GG: Major Burrows's Daredevil Run": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000058),
    "GG: The Golden Chomp": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000060)
}

locFF_table: dict[str, SMGLocationData]  = {
    "FF: The Frozen Peak of Baron Brr": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000061),
    "FF: Freezeflame's Blistering Coore": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000062),
    "FF: Hot and Cold Collide": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000063),
    "FF: Conquring the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000064),
    "FF: Frosty Cosmic Mario race": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000065)
}

locDDune_table: dict[str, SMGLocationData]  = {
    "DDune: Soaring on the Desert Winds": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000067),
    "DDune: Blasting through the Sand": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000068),
    "DDune: Sunbaked Sand Castle": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000069),
    "DDune: Sandblast Speed Run": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000071),
    "DDune: Bullet Bill on Your Back": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000072),
    "DDune: Treasure of the Pyramid": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000073)
} 

locGL_table: dict[str, SMGLocationData]  = {
    "GL: Star Bunnies on the Hunt": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000074),
    "GL: Cataquack to the skies": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000075),
    "GL: When it Rains, it Pours": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000076),
    "GL: Cosmic Mario Forest Race": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000077),
    "GL: The Bell on the Big Trees": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000079)
}

locSS_table: dict[str, SMGLocationData]  = {
    "SS: Going After Guppy": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000080),
    "SS: Faster Than a Speedrunning Penguin": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000081),
    "SS: The Silver Stars of Sea Slide": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000082),
    "SS: Underwater Cosmic Mario Race": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000083),
    "SS: Hurry, He's Hungry": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000085)
}

locTT_table: dict[str, SMGLocationData]  = {
    "TT: Heavy Metal Mecha Boswer": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000086),
    "TT: Mario (or Luigi) Meets Mario": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000087),
    "TT: Bouncing Down Cake Lane": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000088),
    "TT: The Flipswitch Chain": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000089),
    "TT: Fast Foes of Toy Time": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000090)
}

locDD_table: dict[str, SMGLocationData]  = {
    "DD: The Underground Ghost Ship": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000092),
    "DD: Bubble Blastoff": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000093),
    "DD: Guppy and the Underground Lake": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000094),
    "DD: Ghost Ship Daredevil Run": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000095),
    "DD: Boo in Box": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000097)
}

locDN_table: dict[str, SMGLocationData]  = {
    "DN: Inflitrating the Dreadnought": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000098),
    "DN: Dreadnought's Colossal Cannons": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000099),
    "DN: Revenge of the Topman Tribe": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000100),
    "DN: Topman Tribe Speed Run": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000101),
    "DN: Dreadnought's Garbage Dump": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000103)
}

locMM_table: dict[str, SMGLocationData]  = {
    "MM: The Sinking Lava Spire": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000104),
    "MM: Through the Meteor Storm": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000105),
    "MM: Fiery Dino Piranha": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000106),
    "MM: Lava Spire Daredevil Run": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000107),
    "MM Burning Tide": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000109)
}

locHL_table: dict[str, SMGLocationData]  = {
    "SS: Rocky Road": SMGLocationData(["Sweet Sweet Galaxy", "Power Star"], regname.SWEETSWEET, 170000110),
    "SP: A Very Sticky Situation": SMGLocationData(["Sling Pod Galaxy", "Power Star"], regname.SLINGPOD, 170000111),
    "DDR: Giant Eel Breakout": SMGLocationData(["Drip Drop Galaxy", "Power Star"], regname.DRIPDROP, 170000112),
    "BM: Bigmouth's Gold Bait": SMGLocationData(["Bigmouth Galaxy", "Power Star"], regname.BIGMOUTH, 170000113),
    "Sandy Spiral: Choosing a Favorite Snack": SMGLocationData(["Sand Spiral Galaxy", "Power Star"], regname.SANDSPIRAL, 170000114),
    "Bone's Boneyard: Racing the Spooky Speedster": SMGLocationData(["Boo's Boneyard Galaxy", "Power Star"], regname.BOOBONE, 170000115),
    "SC: Star Bunnies in the Snow": SMGLocationData(["Snow Cap Galaxy", "Power Star"], regname.SNOWCAP, 170000116)
}

locPC_table: dict[str, SMGLocationData]  = {
    "TT: Luigi's Purple Coins": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000091),
    "DN: Battlestation's Purple Coins": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000102),
    "MM: Red-Hot Purple Coins": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000108),
    "DD: Plunder the Purple Coins": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000096),
    "SS: Purple Coins by the Seaside": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000084),
    "GE: Purple Coin Omelet": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 170000005),
    "GG: Gateway's Purple coins": SMGLocationData([regname.GATEWAY, "Power Star"], regname.GATEWAY, 170000020),
    "BR: Purple Coins on the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 17000004),
    "SJ: Purple Coin Spacewalk": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000036),
    "GG: Purple Coins on the Puzzle Cube": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000059),
    "BB: Beachcombing for Purple Coins": SMGLocationData(["Bubble Breeze Galaxy", "Power Star"], regname.BUBBLEBREEZE, 170000047),
    "FF: Purple Coins on the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000066),
    "G: Purple Coins in the Bone Pen": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000053),
    "GL: Purple Coins in the Woods": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000078),
    "DDune: Purple Coin in the Desert": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000070),
    "HH: The Honeyhive's Purple Coins": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 170000011)
}

base_stars_locations = {**locGE_table, **locHH_table,
                   **locSJ_table, **locBR_table, **locBB_table,
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table,
                   **locGL_table, **locSS_table, **locTT_table,
                   **locDD_table, **locDN_table, **locMM_table,
                   **locHL_table, **locspecialstages_table, **locbosses_table}

location_table = { **locGE_table, **locHH_table, 
                   **locSJ_table, **locBR_table, **locBB_table, 
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table, 
                   **locGL_table, **locSS_table, **locTT_table, 
                   **locDD_table, **locDN_table, **locMM_table, 
                   **locHL_table, **locspecialstages_table, **locbosses_table, 
                   **locPC_table,
}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in location_table.items() if data.code is not None}