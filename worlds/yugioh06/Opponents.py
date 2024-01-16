from typing import NamedTuple, Callable, List, Optional, Tuple

from BaseClasses import CollectionState, MultiWorld
from worlds.yugioh06.Locations import special


class OpponentData(NamedTuple):
    id: int
    name: str
    campaignInfo: List[str]
    tier: int
    column: int
    card_id: int = 0
    deck_name_id: int = 0
    deck_file: str = ''
    rule: Callable[[CollectionState], bool] = lambda state: True


def get_opponents(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[OpponentData, ...]:
    opponents_table: List[OpponentData] = [
        # Tier 1
        OpponentData(0, "Kuriboh", [], 1, 1, 4064, 8000, "deck/LV1_kuriboh.ydc  "),
        OpponentData(1, "Scapegoat", [], 1, 2, 4818, 8001, "deck/LV1_sukego.ydc   "),
        OpponentData(2, "Skull Servant", [], 1, 3, 4030, 8002, "deck/LV1_waito.ydc    "),
        OpponentData(3, "Watapon", [], 1, 4, 6092, 8003, "deck/LV1_watapon.ydc  "),
        OpponentData(4, "White Magician Pikeru", [], 1, 5, 5975, 8004, "deck/LV1_pikeru.ydc   "),
        # Tier 2
        OpponentData(5, "Battery Man C", ["Quick-Finish"], 2, 1, 6428, 8005, "deck/LV2_denti.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData(6, "Ojama Yellow", [], 2, 2, 5811, 8006, "deck/LV2_ojama.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData(7, "Goblin King", ["Quick-Finish"], 2, 3, 5973, 8007, "deck/LV2_kingG.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData(8, "Des Frog", ["Quick-Finish"], 2, 4, 6424, 8008, "deck/LV2_kaeru.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData(9, "Water Dragon", ["Quick-Finish"], 2, 5, 6481, 8009, "deck/LV2_waterD.ydc   ",
                     lambda state: state.yugioh06_difficulty(player, 1)),
        # Tier 3
        OpponentData(10, "Red-Eyes Darkness Dragon", ["Quick-Finish"], 3, 1, 6292, 8010, "deck/LV3_RedEyes.ydc  ",
                     lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData(11, "Vampire Genesis", ["Quick-Finish"], 3, 2, 6293, 8011, "deck/LV3_vamp.ydc     ",
                     lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData(12, "Infernal Flame Emperor", [], 3, 3, 6368, 8012, "deck/LV3_flame.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData(13, "Ocean Dragon Lord - Neo-Daedalus", [], 3, 4, 6376, 8013, "deck/LV3_daidaros.ydc ",
                     lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData(14, "Helios Duo Megiste", ["Quick-Finish"], 3, 5, 6647, 8014, "deck/LV3_heriosu.ydc  ",
                     lambda state: state.yugioh06_difficulty(player, 2)),
        # Tier 4
        OpponentData(15, "Gilford the Legend", ["Quick-Finish"], 4, 1, 6456, 8015, "deck/LV4_gilfo.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData(16, "Dark Eradicator Warlock", ["Quick-Finish"], 4, 2, 6530, 8016, "deck/LV4_kuromadou.ydc",
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData(17, "Guardian Exode", [], 4, 3, 6640, 8017, "deck/LV4_exodo.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData(18, "Goldd, Wu-Lord of Dark World", ["Quick-Finish"], 4, 4, 6505, 8018, "deck/LV4_ankokukai.ydc",
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData(19, "Elemental Hero Erikshieler", ["Quick-Finish"], 4, 5, 6639, 8019, "deck/LV4_Ehero.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 3)),
        # Tier 5
        OpponentData(20, "Raviel, Lord of Phantasms", [], 5, 1, 6565, 8020, "deck/LV5_ravieru.ydc  ",
                     lambda state: state.yugioh06_difficulty(player, 4)),
        OpponentData(21, "Horus the Black Flame Dragon LV8", [], 5, 2, 6100, 8021, "deck/LV5_horus.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 4)),
        OpponentData(22, "Stronghold", [], 5, 3, 6153, 8022, "deck/LV5_gadget.ydc   ",
                     lambda state: state.yugioh06_difficulty(player, 5)),
        OpponentData(23, "Sacred Phoenix of Nephthys", [], 5, 4, 6236, 8023, "deck/LV5_nephthys.ydc ",
                     lambda state: state.yugioh06_difficulty(player, 6)),
        OpponentData(24, "Cyber End Dragon", ["Goal"], 5, 5, 6397, 8024, "deck/LV5_cyber.ydc    ",
                     lambda state: state.yugioh06_difficulty(player, 7)),
    ]
    return tuple(opponents_table)


def get_other_opponents(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[OpponentData, ...]:
    opponents_table: List[OpponentData] = [
        OpponentData(27, "Exarion Universe", [], 1, 1, 5452, 13001, "deck/theme_001.ydc\x00\x00\x00\x00"),
        OpponentData(28, "Stone Statue of the Aztecs", [], 1, 1, 4754, 13002, "deck/theme_002.ydc\x00\x00\x00\x00"),
        OpponentData(29, "Raging Flame Sprite", [], 1, 1, 6189, 13003, "deck/theme_003.ydc\x00\x00\x00\x00"),
        OpponentData(30, "Princess Pikeru", [], 1, 1, 6605, 13004, "deck/theme_004.ydc\x00\x00\x00\x00"),
        OpponentData(31, "Princess Curran", [], 1, 1, 6606, 13005, "deck/theme_005.ydc\x00\x00\x00\x00"),
        OpponentData(32, "Gearfried the Iron Knight", [], 1, 1, 5059, 13006, "deck/theme_006.ydc\x00\x00\x00\x00"),
        OpponentData(33, "Zaborg the Thunder Monarch", [], 1, 1, 5965, 13007, "deck/theme_007.ydc\x00\x00\x00\x00"),
        OpponentData(34, "Kycoo the Ghost Destroyer", [], 1, 1, 5248, 13008, "deck/theme_008.ydc\x00\x00\x00\x00"),
        OpponentData(35, "Penguin Soldier", [], 1, 1, 4608, 13009, "deck/theme_009.ydc\x00\x00\x00\x00"),
        OpponentData(36, "Green Gadget", [], 1, 1, 6151, 13010, "deck/theme_010.ydc\x00\x00\x00\x00"),
        OpponentData(37, "Guardian Sphinx", [], 1, 1, 5422, 13011, "deck/theme_011.ydc\x00\x00\x00\x00"),
        OpponentData(38, "Cyber-Tech Alligator", [], 1, 1, 4790, 13012, "deck/theme_012.ydc\x00\x00\x00\x00"),
        OpponentData(39, "UFOroid Fighter", [], 1, 1, 6395, 13013, "deck/theme_013.ydc\x00\x00\x00\x00"),
        OpponentData(40, "Relinquished", [], 1, 1, 4737, 13014, "deck/theme_014.ydc\x00\x00\x00\x00"),
        OpponentData(41, "Manticore of Darkness", [], 1, 1, 5881, 13015, "deck/theme_015.ydc\x00\x00\x00\x00"),
        OpponentData(42, "Vampire Lord", [], 1, 1, 5410, 13016, "deck/theme_016.ydc\x00\x00\x00\x00"),
        OpponentData(43, "Gigantes", [], 1, 1, 5831, 13017, "deck/theme_017.ydc\x00\x00\x00\x00"),
        OpponentData(44, "Insect Queen", [], 1, 1, 4768, 13018, "deck/theme_018.ydc\x00\x00\x00\x00"),
        OpponentData(45, "Second Goblin", [], 1, 1, 5587, 13019, "deck/theme_019.ydc\x00\x00\x00\x00"),
        OpponentData(46, "Toon Summoned Skull", [], 1, 1, 4735, 13020, "deck/theme_020.ydc\x00\x00\x00\x00"),
        OpponentData(47, "Iron Blacksmith Kotetsu", [], 1, 1, 5769, 13021, "deck/theme_021.ydc\x00\x00\x00\x00"),
        OpponentData(48, "Magician of Faith", [], 1, 1, 4434, 13021, "deck/theme_022.ydc\x00\x00\x00\x00"),
        OpponentData(49, "Mask of Darkness", [], 1, 1, 4108, 13021, "deck/theme_023.ydc\x00\x00\x00\x00"),
        OpponentData(50, "Dark Ruler Vandalgyon", [], 1, 1, 6410, 13021, "deck/theme_024.ydc\x00\x00\x00\x00"),
        OpponentData(51, "Aussa the Earth Charmer", [], 1, 1, 6335, 13025, "deck/theme_025.ydc\x00\x00\x00\x00"),
    ]
    return opponents_table


def get_opponent_locations(opponent: OpponentData) -> dict[str, str]:
    location = {}
    location[opponent.name + " Beaten"] = "Tier " + str(opponent.tier) + " Beaten"
    if opponent.tier > 4 and opponent.column != 5:
        name = "Campaign Tier 5: Column " + str(opponent.column) + " Win"
        location[name] = special[name]
    for info in opponent.campaignInfo:
        location[opponent.name + "-> " + info] = info
    return location
