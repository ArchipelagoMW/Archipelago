from typing import Dict, List, NamedTuple, Optional, Union

from BaseClasses import MultiWorld
from worlds.generic.Rules import CollectionRule

from . import item_to_index, tier_1_opponents, yugioh06_difficulty
from .locations import special


class OpponentData(NamedTuple):
    id: int
    name: str
    campaign_info: List[str]
    tier: int
    column: int
    card_id: int = 0
    deck_name_id: int = 0
    deck_file: str = ""
    difficulty: int = 1
    additional_info: List[str] = []

    def tier(self, tier):
        self.tier = tier

    def column(self, column):
        self.column = column


challenge_opponents = [
    # Theme
    OpponentData(27, "Exarion Universe", [], 1, 1, 5452, 13001, "deck/theme_001.ydc\x00\x00\x00\x00", 0),
    OpponentData(28, "Stone Statue of the Aztecs", [], 4, 1, 4754, 13002, "deck/theme_002.ydc\x00\x00\x00\x00", 3),
    OpponentData(29, "Raging Flame Sprite", [], 1, 1, 6189, 13003, "deck/theme_003.ydc\x00\x00\x00\x00", 0),
    OpponentData(30, "Princess Pikeru", [], 1, 1, 6605, 13004, "deck/theme_004.ydc\x00\x00\x00\x00", 0),
    OpponentData(31, "Princess Curran", ["Quick-Finish"], 1, 1, 6606, 13005, "deck/theme_005.ydc\x00\x00\x00\x00", 0,
                 ["Has Back-row removal"]),
    OpponentData(32, "Gearfried the Iron Knight", ["Quick-Finish"], 2, 1, 5059, 13006,
                 "deck/theme_006.ydc\x00\x00\x00\x00", 1),
    OpponentData(33, "Zaborg the Thunder Monarch", [], 3, 1, 5965, 13007, "deck/theme_007.ydc\x00\x00\x00\x00", 2),
    OpponentData(34, "Kycoo the Ghost Destroyer", ["Quick-Finish"], 3, 1, 5248, 13008,
                 "deck/theme_008.ydc\x00\x00\x00\x00"),
    OpponentData(35, "Penguin Soldier", ["Quick-Finish"], 1, 1, 4608, 13009, "deck/theme_009.ydc\x00\x00\x00\x00", 0),
    OpponentData(36, "Green Gadget", [], 5, 1, 6151, 13010, "deck/theme_010.ydc\x00\x00\x00\x00", 5),
    OpponentData(37, "Guardian Sphinx", ["Quick-Finish"], 3, 1, 5422, 13011, "deck/theme_011.ydc\x00\x00\x00\x00", 3),
    OpponentData(38, "Cyber-Tech Alligator", [], 2, 1, 4790, 13012, "deck/theme_012.ydc\x00\x00\x00\x00", 1),
    OpponentData(39, "UFOroid Fighter", [], 3, 1, 6395, 13013, "deck/theme_013.ydc\x00\x00\x00\x00", 2),
    OpponentData(40, "Relinquished", [], 3, 1, 4737, 13014, "deck/theme_014.ydc\x00\x00\x00\x00", 2),
    OpponentData(41, "Manticore of Darkness", [], 2, 1, 5881, 13015, "deck/theme_015.ydc\x00\x00\x00\x00", 1),
    OpponentData(42, "Vampire Lord", [], 3, 1, 5410, 13016, "deck/theme_016.ydc\x00\x00\x00\x00", 2),
    OpponentData(43, "Gigantes", ["Quick-Finish"], 3, 1, 5831, 13017, "deck/theme_017.ydc\x00\x00\x00\x00", 2),
    OpponentData(44, "Insect Queen", ["Quick-Finish"], 2, 1, 4768, 13018, "deck/theme_018.ydc\x00\x00\x00\x00", 1),
    OpponentData(45, "Second Goblin", ["Quick-Finish"], 1, 1, 5587, 13019, "deck/theme_019.ydc\x00\x00\x00\x00", 0),
    OpponentData(46, "Toon Summoned Skull", [], 4, 1, 4735, 13020, "deck/theme_020.ydc\x00\x00\x00\x00", 3),
    OpponentData(47, "Iron Blacksmith Kotetsu", [], 2, 1, 5769, 13021, "deck/theme_021.ydc\x00\x00\x00\x00", 1),
    OpponentData(48, "Magician of Faith", [], 1, 1, 4434, 13022, "deck/theme_022.ydc\x00\x00\x00\x00", 0),
    OpponentData(49, "Mask of Darkness", [], 1, 1, 4108, 13023, "deck/theme_023.ydc\x00\x00\x00\x00", 0),
    OpponentData(50, "Dark Ruler Vandalgyon", [], 3, 1, 6410, 13024, "deck/theme_024.ydc\x00\x00\x00\x00", 2),
    OpponentData(51, "Aussa the Earth Charmer", ["Quick-Finish"], 2, 1, 6335, 13025,
                 "deck/theme_025.ydc\x00\x00\x00\x00", 1),
    OpponentData(52, "Exodia Necross", ["Quick-Finish"], 2, 1, 5701, 13026, "deck/theme_026.ydc\x00\x00\x00\x00", 1),
    OpponentData(53, "Dark Necrofear", [], 3, 1, 5222, 13027, "deck/theme_027.ydc\x00\x00\x00\x00", 2),
    OpponentData(54, "Demise, King of Armageddon", [], 4, 1, 6613, 13028, "deck/theme_028.ydc\x00\x00\x00\x00", 2),
    OpponentData(55, "Yamata Dragon", [], 3, 1, 5377, 13029, "deck/theme_029.ydc\x00\x00\x00\x00", 2),
    OpponentData(56, "Blue-Eyes Ultimate Dragon", [], 3, 1, 4386, 13030, "deck/theme_030.ydc\x00\x00\x00\x00", 2),
    OpponentData(57, "Wave-Motion Cannon", [], 4, 1, 5614, 13031, "deck/theme_031.ydc\x00\x00\x00\x00", 3,
                 ["Has Back-row removal"]),
    # Unused opponent
    # OpponentData(58, "Yata-Garasu", [], 1, 1, 5375, 13032, "deck/theme_031.ydc\x00\x00\x00\x00"),
    # Unused opponent
    # OpponentData(59, "Makyura the Destructor", [], 1, 1, 5285, 13033, "deck/theme_031.ydc\x00\x00\x00\x00"),
    OpponentData(60, "Morphing Jar", [], 5, 1, 4597, 13034, "deck/theme_034.ydc\x00\x00\x00\x00", 4),
    OpponentData(61, "Spirit Reaper", [], 2, 1, 5526, 13035, "deck/theme_035.ydc\x00\x00\x00\x00", 1),
    OpponentData(62, "Victory D.", [], 3, 1, 5868, 13036, "deck/theme_036.ydc\x00\x00\x00\x00", 2),
    OpponentData(63, "VWXYZ-Dragon Catapult Cannon", ["Quick-Finish"], 3, 1, 6484, 13037,
                 "deck/theme_037.ydc\x00\x00\x00\x00", 2),
    OpponentData(64, "XYZ-Dragon Cannon", [], 2, 1, 5556, 13038, "deck/theme_038.ydc\x00\x00\x00\x00", 1),
    OpponentData(65, "Uria, Lord of Searing Flames", [], 4, 1, 6563, 13039, "deck/theme_039.ydc\x00\x00\x00\x00", 3),
    OpponentData(66, "Hamon, Lord of Striking Thunder", [], 4, 1, 6564, 13040, "deck/theme_040.ydc\x00\x00\x00\x00", 3),
    OpponentData(67, "Raviel, Lord of Phantasms TD", [], 4, 1, 6565, 13041, "deck/theme_041.ydc\x00\x00\x00\x00", 3),
    OpponentData(68, "Ojama Trio", [], 1, 1, 5738, 13042, "deck/theme_042.ydc\x00\x00\x00\x00", 0),
    OpponentData(69, "People Running About", ["Quick-Finish"], 1, 1, 5578, 13043, "deck/theme_043.ydc\x00\x00\x00\x00",
                 0),
    OpponentData(70, "Cyber-Stein", [], 5, 1, 4426, 13044, "deck/theme_044.ydc\x00\x00\x00\x00", 4),
    OpponentData(71, "Winged Kuriboh LV10", [], 4, 1, 6406, 13045, "deck/theme_045.ydc\x00\x00\x00\x00", 3),
    OpponentData(72, "Blue-Eyes Shining Dragon", [], 3, 1, 6082, 13046, "deck/theme_046.ydc\x00\x00\x00\x00", 2),
    OpponentData(73, "Perfectly Ultimate Great Moth", ["Quick-Finish"], 3, 1, 4073, 13047,
                 "deck/theme_047.ydc\x00\x00\x00\x00", 2),
    OpponentData(74, "Gate Guardian", [], 4, 1, 4380, 13048, "deck/theme_048.ydc\x00\x00\x00\x00", 2),
    OpponentData(75, "Valkyrion the Magna Warrior", [], 3, 1, 5002, 13049, "deck/theme_049.ydc\x00\x00\x00\x00", 2),
    OpponentData(76, "Dark Sage", [], 4, 1, 5230, 13050, "deck/theme_050.ydc\x00\x00\x00\x00", 3),
    OpponentData(77, "Don Zaloog", [], 4, 1, 5426, 13051, "deck/theme_051.ydc\x00\x00\x00\x00", 3),
    OpponentData(78, "Blast Magician", ["Quick-Finish"], 2, 1, 6250, 13052, "deck/theme_052.ydc\x00\x00\x00\x00", 1),
    # Limited
    OpponentData(79, "Zombyra the Dark", [], 5, 1, 5245, 23000, "deck/limit_000.ydc\x00\x00\x00\x00", 5),
    OpponentData(80, "Goblin Attack Force", [], 4, 1, 5145, 23001, "deck/limit_001.ydc\x00\x00\x00\x00", 3),
    OpponentData(81, "Giant Kozaky", [], 4, 1, 6420, 23002, "deck/limit_002.ydc\x00\x00\x00\x00", 4),
    OpponentData(82, "Big Shield Gardna", ["Quick-Finish"], 2, 1, 4764, 23003, "deck/limit_003.ydc\x00\x00\x00\x00", 1),
    OpponentData(83, "Panther Warrior", [], 3, 1, 4751, 23004, "deck/limit_004.ydc\x00\x00\x00\x00", 2),
    OpponentData(84, "Silent Magician LV4", ["Quick-Finish"], 2, 1, 6167, 23005, "deck/limit_005.ydc\x00\x00\x00\x00",
                 1),
    OpponentData(85, "Summoned Skull", [], 4, 1, 4028, 23006, "deck/limit_006.ydc\x00\x00\x00\x00", 3),
    OpponentData(86, "Ancient Gear Golem", [], 5, 1, 6315, 23007, "deck/limit_007.ydc\x00\x00\x00\x00", 5),
    OpponentData(87, "Chaos Sorcerer", [], 5, 1, 5833, 23008, "deck/limit_008.ydc\x00\x00\x00\x00", 5),
    OpponentData(88, "Breaker the Magical Warrior", [], 5, 1, 5655, 23009, "deck/limit_009.ydc\x00\x00\x00\x00", 4),
    OpponentData(89, "Dark Magician of Chaos", [], 4, 1, 5880, 23010, "deck/limit_010.ydc\x00\x00\x00\x00", 3),
    OpponentData(90, "Stealth Bird", ["Quick-Finish"], 2, 1, 5882, 23011, "deck/limit_011.ydc\x00\x00\x00\x00", 1),
    OpponentData(91, "Rapid-Fire Magician", ["Quick-Finish"], 2, 1, 6500, 23012, "deck/limit_012.ydc\x00\x00\x00\x00",
                 1),
    OpponentData(92, "Morphing Jar #2", [], 5, 1, 4969, 23013, "deck/limit_013.ydc\x00\x00\x00\x00", 4),
    OpponentData(93, "Cyber Jar", [], 5, 1, 4913, 23014, "deck/limit_014.ydc\x00\x00\x00\x00", 4),
    # Unused/Broken
    # OpponentData(94, "Exodia the Forbidden One", [], 1, 1, 4027, 23015, "deck/limit_015.ydc\x00\x00\x00\x00"),
    OpponentData(94, "Dark Paladin", [], 4, 1, 5628, 23016, "deck/limit_016.ydc\x00\x00\x00\x00", 3),
    OpponentData(95, "F.G.D.", [], 5, 1, 5502, 23017, "deck/limit_017.ydc\x00\x00\x00\x00", 4),
    OpponentData(96, "Blue-Eyes Toon Dragon", ["Quick-Finish"], 2, 1, 4773, 23018, "deck/limit_018.ydc\x00\x00\x00\x00",
                 1),
    OpponentData(97, "Tsukuyomi", [], 3, 1, 5780, 23019, "deck/limit_019.ydc\x00\x00\x00\x00", 2),
    OpponentData(98, "Silent Swordsman LV3", ["Quick-Finish"], 2, 1, 6162, 23020, "deck/limit_020.ydc\x00\x00\x00\x00",
                 2),
    OpponentData(99, "Elemental Hero Flame Wingman", ["Quick-Finish"], 2, 1, 6344, 23021,
                 "deck/limit_021.ydc\x00\x00\x00\x00", 0),
    OpponentData(100, "Armed Dragon LV7", ["Quick-Finish"], 2, 1, 6107, 23022, "deck/limit_022.ydc\x00\x00\x00\x00", 0),
    OpponentData(101, "Alkana Knight Joker", ["Quick-Finish"], 1, 1, 6454, 23023, "deck/limit_023.ydc\x00\x00\x00\x00",
                 0),
    OpponentData(102, "Sorcerer of Dark Magic", [], 4, 1, 6086, 23024, "deck/limit_024.ydc\x00\x00\x00\x00", 3),
    OpponentData(103, "Shinato, King of a Higher Plane", [], 4, 1, 5697, 23025, "deck/limit_025.ydc\x00\x00\x00\x00",
                 3),
    OpponentData(104, "Ryu Kokki", [], 5, 1, 5902, 23026, "deck/limit_026.ydc\x00\x00\x00\x00", 4),
    OpponentData(105, "Cyber Dragon", [], 5, 1, 6390, 23027, "deck/limit_027.ydc\x00\x00\x00\x00", 4),
    OpponentData(106, "Dark Dreadroute", ["Quick-Finish"], 3, 1, 6405, 23028, "deck/limit_028.ydc\x00\x00\x00\x00", 2),
    OpponentData(107, "Ultimate Insect LV7", ["Quick-Finish"], 3, 1, 6319, 23029, "deck/limit_029.ydc\x00\x00\x00\x00",
                 2),
    OpponentData(108, "Thestalos the Firestorm Monarch", ["Quick-Finish"], 3, 1, 6190, 23030,
                 "deck/limit_030.ydc\x00\x00\x00\x00"),
    OpponentData(109, "Master of Oz", ["Quick-Finish"], 3, 1, 6127, 23031, "deck/limit_031.ydc\x00\x00\x00\x00", 2),
    OpponentData(110, "Orca Mega-Fortress of Darkness", ["Quick-Finish"], 3, 1, 5896, 23032,
                 "deck/limit_032.ydc\x00\x00\x00\x00", 2),
    OpponentData(111, "Airknight Parshath", ["Quick-Finish"], 4, 1, 5023, 23033, "deck/limit_033.ydc\x00\x00\x00\x00",
                 3),
    OpponentData(112, "Dark Scorpion Burglars", ["Quick-Finish"], 4, 1, 5425, 23034,
                 "deck/limit_034.ydc\x00\x00\x00\x00", 3),
    OpponentData(113, "Gilford the Lightning", [], 4, 1, 5451, 23035, "deck/limit_035.ydc\x00\x00\x00\x00", 3),
    OpponentData(114, "Embodiment of Apophis", [], 2, 1, 5234, 23036, "deck/limit_036.ydc\x00\x00\x00\x00", 1),
    OpponentData(115, "Great Maju Garzett", [], 5, 1, 5768, 23037, "deck/limit_037.ydc\x00\x00\x00\x00", 4),
    OpponentData(116, "Black Luster Soldier - Envoy of the Beginning", [], 5, 1, 5835, 23038,
                 "deck/limit_038.ydc\x00\x00\x00\x00", 4),
    OpponentData(117, "Red-Eyes B. Dragon", [], 4, 1, 4088, 23039, "deck/limit_039.ydc\x00\x00\x00\x00", 3),
    OpponentData(118, "Blue-Eyes White Dragon", [], 4, 1, 4007, 23040, "deck/limit_040.ydc\x00\x00\x00\x00", 3),
    OpponentData(119, "Dark Magician", [], 4, 1, 4041, 23041, "deck/limit_041.ydc\x00\x00\x00\x00", 3),
    OpponentData(0, "Starter", ["Quick-Finish"], 1, 1, 4064, 1510, "deck/SD0_STARTER.ydc\x00\x00", 0),
    OpponentData(10, "DRAGON'S ROAR", ["Quick-Finish"], 2, 1, 6292, 1511, "deck/SD1_DRAGON.ydc\x00\x00\x00", 1),
    OpponentData(11, "ZOMBIE MADNESS", ["Quick-Finish"], 2, 1, 6293, 1512, "deck/SD2_UNDEAD.ydc\x00\x00\x00", 1),
    OpponentData(12, "BLAZING DESTRUCTION", ["Quick-Finish"], 2, 1, 6368, 1513, "deck/SD3_FIRE.ydc\x00\x00\x00\x00\x00",
                 1,
                 ["Has Back-row removal"]),
    OpponentData(13, "FURY FROM THE DEEP", [], 2, 1, 6376, 1514,
                 "deck/SD4_UMI.ydc\x00\x00\x00\x00\x00\x00", 1, ["Has Back-row removal"]),
    OpponentData(15, "WARRIORS TRIUMPH", ["Quick-Finish"], 2, 1, 6456, 1515, "deck/SD5_SOLDIER.ydc\x00\x00", 1),
    OpponentData(16, "SPELLCASTERS JUDGEMENT", ["Quick-Finish"], 2, 1, 6530, 1516, "deck/SD6_MAGICIAN.ydc\x00", 1),
    OpponentData(17, "INVICIBLE FORTRESS", [], 2, 1, 6640, 1517, "deck/SD7_GANSEKI.ydc\x00\x00", 1),
    OpponentData(7, "Goblin King 2", ["Quick-Finish"], 3, 3, 5973, 8007, "deck/LV2_kingG2.ydc\x00\x00\x00", 2),
]


def get_opponents(multiworld: Optional[MultiWorld], player: Optional[int], randomize: bool = False) -> List[
    OpponentData]:
    opponents_table: List[OpponentData] = [
        # Tier 1
        OpponentData(0, "Kuriboh", [], 1, 1, 4064, 8000, "deck/LV1_kuriboh.ydc\x00\x00"),
        OpponentData(1, "Scapegoat", [], 1, 2, 4818, 8001, "deck/LV1_sukego.ydc\x00\x00\x00", 0,
                     ["Has Back-row removal"]),
        OpponentData(2, "Skull Servant", [], 1, 3, 4030, 8002, "deck/LV1_waito.ydc\x00\x00\x00\x00", 0,
                     ["Has Back-row removal"]),
        OpponentData(3, "Watapon", [], 1, 4, 6092, 8003, "deck/LV1_watapon.ydc\x00\x00", 0, ["Has Back-row removal"]),
        OpponentData(4, "White Magician Pikeru", [], 1, 5, 5975, 8004, "deck/LV1_pikeru.ydc\x00\x00\x00"),
        # Tier 2
        OpponentData(5, "Battery Man C", ["Quick-Finish"], 2, 1, 6428, 8005, "deck/LV2_denti.ydc\x00\x00\x00\x00", 1),
        OpponentData(6, "Ojama Yellow", [], 2, 2, 5811, 8006, "deck/LV2_ojama.ydc\x00\x00\x00\x00", 1,
                     ["Has Back-row removal"]),
        OpponentData(7, "Goblin King", ["Quick-Finish"], 2, 3, 5973, 8007, "deck/LV2_kingG.ydc\x00\x00\x00\x00", 1),
        OpponentData(8, "Des Frog", ["Quick-Finish"], 2, 4, 6424, 8008, "deck/LV2_kaeru.ydc\x00\x00\x00\x00", 1),
        OpponentData(9, "Water Dragon", ["Quick-Finish"], 2, 5, 6481, 8009, "deck/LV2_waterD.ydc\x00\x00\x00", 1),
        # Tier 3
        OpponentData(10, "Red-Eyes Darkness Dragon", ["Quick-Finish"], 3, 1, 6292, 8010, "deck/LV3_RedEyes.ydc\x00\x00",
                     2),
        OpponentData(11, "Vampire Genesis", ["Quick-Finish"], 3, 2, 6293, 8011, "deck/LV3_vamp.ydc\x00\x00\x00\x00\x00",
                     2),
        OpponentData(12, "Infernal Flame Emperor", [], 3, 3, 6368, 8012, "deck/LV3_flame.ydc\x00\x00\x00\x00", 2,
                     ["Has Back-row removal"]),
        OpponentData(13, "Ocean Dragon Lord - Neo-Daedalus", [], 3, 4, 6376, 8013, "deck/LV3_daidaros.ydc\x00", 2,
                     ["Has Back-row removal"]),
        OpponentData(14, "Helios Duo Megiste", ["Quick-Finish"], 3, 5, 6647, 8014, "deck/LV3_heriosu.ydc\x00\x00", 2),
        # Tier 4
        OpponentData(15, "Gilford the Legend", ["Quick-Finish"], 4, 1, 6456, 8015, "deck/LV4_gilfo.ydc\x00\x00\x00\x00",
                     3),
        OpponentData(16, "Dark Eradicator Warlock", ["Quick-Finish"], 4, 2, 6530, 8016, "deck/LV4_kuromadou.ydc", 3),
        OpponentData(17, "Guardian Exode", [], 4, 3, 6640, 8017, "deck/LV4_exodo.ydc\x00\x00\x00\x00", 3),
        OpponentData(18, "Goldd, Wu-Lord of Dark World", ["Quick-Finish"], 4, 4, 6505, 8018, "deck/LV4_ankokukai.ydc",
                     3),
        OpponentData(19, "Elemental Hero Erikshieler", ["Quick-Finish"], 4, 5, 6639, 8019,
                     "deck/LV4_Ehero.ydc\x00\x00\x00\x00", 3),
        # Tier 5
        OpponentData(20, "Raviel, Lord of Phantasms", [], 5, 1, 6565, 8020, "deck/LV5_ravieru.ydc\x00\x00", 4),
        OpponentData(21, "Horus the Black Flame Dragon LV8", [], 5, 2, 6100, 8021, "deck/LV5_horus.ydc\x00\x00\x00\x00",
                     4),
        OpponentData(22, "Stronghold", [], 5, 3, 6153, 8022, "deck/LV5_gadget.ydc\x00\x00\x00", 5),
        OpponentData(23, "Sacred Phoenix of Nephthys", [], 5, 4, 6236, 8023, "deck/LV5_nephthys.ydc\x00", 6),
        OpponentData(24, "Cyber End Dragon", ["Goal"], 5, 5, 6397, 8024, "deck/LV5_cyber.ydc\x00\x00\x00\x00", 7),
    ]
    world = multiworld.worlds[player]
    if not randomize:
        return opponents_table
    opponents = opponents_table + challenge_opponents
    start = world.random.choice([o for o in opponents if o.tier == 1 and len(o.additional_info) == 0])
    opponents.remove(start)
    goal = world.random.choice([o for o in opponents if "Goal" in o.campaign_info])
    opponents.remove(goal)
    world.random.shuffle(opponents)
    chosen_ones = opponents[:23]
    for item in (multiworld.precollected_items[player]):
        if item.name in tier_1_opponents:
            # convert item index to opponent index
            chosen_ones.insert(item_to_index[item.name] - item_to_index["Campaign Tier 1 Column 1"], start)
            break
    chosen_ones.append(goal)
    tier = 1
    column = 1
    recreation = []
    for opp in chosen_ones:
        recreation.append(OpponentData(opp.id, opp.name, opp.campaign_info, tier, column, opp.card_id,
                                       opp.deck_name_id, opp.deck_file, opp.difficulty))
        column += 1
        if column > 5:
            column = 1
            tier += 1

    return recreation


def get_opponent_locations(opponent: OpponentData) -> Dict[str, Optional[Union[str, int]]]:
    location = {opponent.name + " Beaten": "Tier " + str(opponent.tier) + " Beaten"}
    if opponent.tier > 4 and opponent.column != 5:
        name = "Campaign Tier 5: Column " + str(opponent.column) + " Win"
        # return a int instead so a item can be placed at this location later
        location[name] = special[name]
    for info in opponent.campaign_info:
        location[opponent.name + "-> " + info] = info
    return location


def get_opponent_condition(opponent: OpponentData, unlock_item: str, unlock_amount: int, player: int,
                           is_challenge: bool) -> CollectionRule:
    if is_challenge:
        return lambda state: (
            state.has(unlock_item, player, unlock_amount)
            and yugioh06_difficulty(state, player, opponent.difficulty)
            and state.has_all(opponent.additional_info, player)
        )
    else:
        return lambda state: (
            state.has_group(unlock_item, player, unlock_amount)
            and yugioh06_difficulty(state, player, opponent.difficulty)
            and state.has_all(opponent.additional_info, player)
        )
