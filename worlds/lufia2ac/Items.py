from enum import auto, Enum
from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

start_id: int = 0xAC0000


class ItemType(Enum):
    BLUE_CHEST = auto()
    BOSS = auto()
    CAPSULE_MONSTER = auto()
    ENEMY_DROP = auto()
    ENTRANCE_CHEST = auto()
    IRIS_TREASURE = auto()
    PARTY_MEMBER = auto()
    RED_CHEST = auto()
    RED_CHEST_PATCH = auto()


class ItemData(NamedTuple):
    code: int
    type: ItemType
    classification: ItemClassification


class L2ACItem(Item):
    game: str = "Lufia II Ancient Cave"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)


l2ac_item_table: Dict[str, ItemData] = {
    # 0x0000: "No equip"
    # ----- CONSUMABLE -----
    "Charred newt": ItemData(0x0001, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Potion": ItemData(0x0002, ItemType.RED_CHEST, ItemClassification.useful),
    "Hi-Potion": ItemData(0x0003, ItemType.RED_CHEST, ItemClassification.useful),
    "Ex-Potion": ItemData(0x0004, ItemType.RED_CHEST, ItemClassification.useful),
    "Magic jar": ItemData(0x0005, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Hi-Magic": ItemData(0x0006, ItemType.RED_CHEST, ItemClassification.useful),
    "Ex-Magic": ItemData(0x0007, ItemType.RED_CHEST, ItemClassification.useful),
    "Regain": ItemData(0x0008, ItemType.RED_CHEST, ItemClassification.useful),
    "Miracle": ItemData(0x0009, ItemType.RED_CHEST, ItemClassification.useful),
    "Antidote": ItemData(0x000A, ItemType.RED_CHEST, ItemClassification.useful),
    "Awake": ItemData(0x000B, ItemType.RED_CHEST, ItemClassification.useful),
    "Shriek": ItemData(0x000C, ItemType.RED_CHEST, ItemClassification.useful),
    "Mystery pin": ItemData(0x000D, ItemType.RED_CHEST, ItemClassification.useful),
    "Power gourd": ItemData(0x000E, ItemType.RED_CHEST, ItemClassification.useful),
    "Mind gourd": ItemData(0x000F, ItemType.RED_CHEST, ItemClassification.useful),
    "Magic guard": ItemData(0x0010, ItemType.RED_CHEST, ItemClassification.useful),
    "Life potion": ItemData(0x0011, ItemType.RED_CHEST, ItemClassification.useful),
    "Spell potion": ItemData(0x0012, ItemType.RED_CHEST, ItemClassification.useful),
    "Power potion": ItemData(0x0013, ItemType.RED_CHEST, ItemClassification.useful),
    "Speed potion": ItemData(0x0014, ItemType.RED_CHEST, ItemClassification.useful),
    "Mind potion": ItemData(0x0015, ItemType.RED_CHEST, ItemClassification.useful),
    "Brave": ItemData(0x0016, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0017: "Pear cider"
    "Sour cider": ItemData(0x0018, ItemType.ENEMY_DROP, ItemClassification.useful),
    # 0x0019: "Lime cider"
    # 0x001A: "Plum cider"
    # 0x001B: "Apple cider"
    "Sleep ball": ItemData(0x001C, ItemType.RED_CHEST, ItemClassification.useful),
    "Confuse ball": ItemData(0x001D, ItemType.RED_CHEST, ItemClassification.useful),
    "Freeze ball": ItemData(0x001E, ItemType.RED_CHEST, ItemClassification.useful),
    "Smoke ball": ItemData(0x001F, ItemType.RED_CHEST, ItemClassification.useful),
    "Ice ball": ItemData(0x0020, ItemType.RED_CHEST, ItemClassification.useful),
    "Fire ball": ItemData(0x0021, ItemType.RED_CHEST, ItemClassification.useful),
    "Terror ball": ItemData(0x0022, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0023: "Ear pick"
    "Boomerang": ItemData(0x0024, ItemType.RED_CHEST, ItemClassification.useful),
    "Big boomer": ItemData(0x0025, ItemType.RED_CHEST, ItemClassification.useful),
    "Ex-boomer": ItemData(0x0026, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0027: "Dragon tooth"
    # 0x0028: "Green tea"
    # 0x0029: "Escape"
    # 0x002A: "Warp"
    # 0x002B: "Dragon egg"
    "Curselifter": ItemData(0x002C, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x002D: "Providence"
    "Secret fruit": ItemData(0x002E, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Holy fruit": ItemData(0x002F, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Breeze fruit": ItemData(0x0030, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Charm fruit": ItemData(0x0031, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Dark fruit": ItemData(0x0032, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Earth fruit": ItemData(0x0033, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Flame fruit": ItemData(0x0034, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Magic fruit": ItemData(0x0035, ItemType.RED_CHEST, ItemClassification.useful),
    # ----- WEAPON -----
    # 0x0036: "Dual blade"
    "Frypan": ItemData(0x0037, ItemType.RED_CHEST, ItemClassification.useful),
    "Knife": ItemData(0x0038, ItemType.RED_CHEST, ItemClassification.useful),
    "Small knife": ItemData(0x0039, ItemType.RED_CHEST, ItemClassification.useful),
    "Rapier": ItemData(0x003A, ItemType.RED_CHEST, ItemClassification.useful),
    "Battle knife": ItemData(0x003B, ItemType.RED_CHEST, ItemClassification.useful),
    "Dagger": ItemData(0x003C, ItemType.RED_CHEST, ItemClassification.useful),
    "Insect crush": ItemData(0x003D, ItemType.RED_CHEST, ItemClassification.useful),
    "Long knife": ItemData(0x003E, ItemType.RED_CHEST, ItemClassification.useful),
    "Short sword": ItemData(0x003F, ItemType.RED_CHEST, ItemClassification.useful),
    "Light knife": ItemData(0x0040, ItemType.RED_CHEST, ItemClassification.useful),
    "Kukri": ItemData(0x0041, ItemType.RED_CHEST, ItemClassification.useful),
    "Gladius": ItemData(0x0042, ItemType.RED_CHEST, ItemClassification.useful),
    "Cold rapier": ItemData(0x0043, ItemType.RED_CHEST, ItemClassification.useful),
    "Scimitar": ItemData(0x0044, ItemType.RED_CHEST, ItemClassification.useful),
    "Deadly sword": ItemData(0x0045, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0046: "Deadly sword" (uncursed)
    "SuhrCustom11": ItemData(0x0047, ItemType.RED_CHEST, ItemClassification.useful),
    "Bronze sword": ItemData(0x0048, ItemType.RED_CHEST, ItemClassification.useful),
    "Fire dagger": ItemData(0x0049, ItemType.RED_CHEST, ItemClassification.useful),
    "War rapier": ItemData(0x004A, ItemType.RED_CHEST, ItemClassification.useful),
    "Long sword": ItemData(0x004B, ItemType.RED_CHEST, ItemClassification.useful),
    "Beserk blade": ItemData(0x004C, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x004D: "Beserk blade" (uncursed)
    "Multi sword": ItemData(0x004E, ItemType.RED_CHEST, ItemClassification.useful),
    "Rockbreaker": ItemData(0x004F, ItemType.RED_CHEST, ItemClassification.useful),
    "Broadsword": ItemData(0x0050, ItemType.RED_CHEST, ItemClassification.useful),
    "Estok": ItemData(0x0051, ItemType.RED_CHEST, ItemClassification.useful),
    "Silvo rapier": ItemData(0x0052, ItemType.RED_CHEST, ItemClassification.useful),
    "Burn sword": ItemData(0x0053, ItemType.RED_CHEST, ItemClassification.useful),
    "Dekar blade": ItemData(0x0054, ItemType.RED_CHEST, ItemClassification.useful),
    "Crazy blade": ItemData(0x0055, ItemType.RED_CHEST, ItemClassification.useful),
    "Deadly sword (fake)": ItemData(0x0056, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0057: "Deadly sword" (fake, uncursed)
    "Luck rapier": ItemData(0x0058, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0059: "Luck rapier" (uncursed)
    "Aqua sword": ItemData(0x005A, ItemType.RED_CHEST, ItemClassification.useful),
    "Red saber": ItemData(0x005B, ItemType.RED_CHEST, ItemClassification.useful),
    "Lucky blade": ItemData(0x005C, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x005D: "Lucky blade" (uncursed)
    "Mist rapier": ItemData(0x005E, ItemType.RED_CHEST, ItemClassification.useful),
    "Boom sword": ItemData(0x005F, ItemType.RED_CHEST, ItemClassification.useful),
    "Freeze sword": ItemData(0x0060, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver sword": ItemData(0x0061, ItemType.RED_CHEST, ItemClassification.useful),
    "Flying blow": ItemData(0x0062, ItemType.RED_CHEST, ItemClassification.useful),
    "Super sword": ItemData(0x0063, ItemType.RED_CHEST, ItemClassification.useful),
    "Buster sword": ItemData(0x0064, ItemType.RED_CHEST, ItemClassification.useful),
    "Rune rapier": ItemData(0x0065, ItemType.RED_CHEST, ItemClassification.useful),
    "Old sword": ItemData(0x0066, ItemType.RED_CHEST, ItemClassification.useful),
    "Lizard blow": ItemData(0x0067, ItemType.RED_CHEST, ItemClassification.useful),
    "Zirco sword": ItemData(0x0068, ItemType.RED_CHEST, ItemClassification.useful),
    "Sizzle sword": ItemData(0x4069, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Blaze sword": ItemData(0x406A, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Myth blade": ItemData(0x006B, ItemType.RED_CHEST, ItemClassification.useful),
    "Gades blade": ItemData(0x406C, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Sky sword": ItemData(0x406D, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Snow sword": ItemData(0x406E, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Fry sword": ItemData(0x406F, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x0070: "Egg sword"
    "Franshiska": ItemData(0x0071, ItemType.RED_CHEST, ItemClassification.useful),
    "Thunder ax": ItemData(0x0072, ItemType.RED_CHEST, ItemClassification.useful),
    "Hand ax": ItemData(0x0073, ItemType.RED_CHEST, ItemClassification.useful),
    "Bronze ax": ItemData(0x0074, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0075: "Flying ax"
    "Rainy ax": ItemData(0x0076, ItemType.RED_CHEST, ItemClassification.useful),
    "Great ax": ItemData(0x0077, ItemType.RED_CHEST, ItemClassification.useful),
    "Zirco ax": ItemData(0x0078, ItemType.RED_CHEST, ItemClassification.useful),
    "Mega ax": ItemData(0x4079, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Mace": ItemData(0x007A, ItemType.RED_CHEST, ItemClassification.useful),
    "Rod": ItemData(0x007B, ItemType.RED_CHEST, ItemClassification.useful),
    "Staff": ItemData(0x007C, ItemType.RED_CHEST, ItemClassification.useful),
    "Deadly rod": ItemData(0x007D, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x007E: "Deadly rod" (uncursed)
    "Sleep rod": ItemData(0x007F, ItemType.RED_CHEST, ItemClassification.useful),
    "Long staff": ItemData(0x0080, ItemType.RED_CHEST, ItemClassification.useful),
    "Holy staff": ItemData(0x0081, ItemType.RED_CHEST, ItemClassification.useful),
    "Morning star": ItemData(0x0082, ItemType.RED_CHEST, ItemClassification.useful),
    "Pounder rod": ItemData(0x0083, ItemType.RED_CHEST, ItemClassification.useful),
    "Crystal wand": ItemData(0x0084, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver rod": ItemData(0x0085, ItemType.RED_CHEST, ItemClassification.useful),
    "Zirco rod": ItemData(0x0086, ItemType.RED_CHEST, ItemClassification.useful),
    "Zirco flail": ItemData(0x0087, ItemType.RED_CHEST, ItemClassification.useful),
    "Spark staff": ItemData(0x4088, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Whip": ItemData(0x0089, ItemType.RED_CHEST, ItemClassification.useful),
    "Wire": ItemData(0x008A, ItemType.RED_CHEST, ItemClassification.useful),
    "Chain": ItemData(0x008B, ItemType.RED_CHEST, ItemClassification.useful),
    "Aqua whip": ItemData(0x008C, ItemType.RED_CHEST, ItemClassification.useful),
    "Cutter whip": ItemData(0x008D, ItemType.RED_CHEST, ItemClassification.useful),
    "Royal whip": ItemData(0x008E, ItemType.RED_CHEST, ItemClassification.useful),
    "Holy whip": ItemData(0x008F, ItemType.RED_CHEST, ItemClassification.useful),
    "Zirco whip": ItemData(0x0090, ItemType.RED_CHEST, ItemClassification.useful),
    "Air whip": ItemData(0x4091, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Fatal pick": ItemData(0x0092, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0093: "Fatal pick" (uncursed)
    "Spear": ItemData(0x0094, ItemType.RED_CHEST, ItemClassification.useful),
    "Trident": ItemData(0x0095, ItemType.RED_CHEST, ItemClassification.useful),
    "Halberd": ItemData(0x0096, ItemType.RED_CHEST, ItemClassification.useful),
    "Heavy lance": ItemData(0x0097, ItemType.RED_CHEST, ItemClassification.useful),
    "Water spear": ItemData(0x4098, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Dragon spear": ItemData(0x4099, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Vice pliers": ItemData(0x009A, ItemType.RED_CHEST, ItemClassification.useful),
    "Coma hit": ItemData(0x009B, ItemType.RED_CHEST, ItemClassification.useful),
    "Figgoru": ItemData(0x009C, ItemType.RED_CHEST, ItemClassification.useful),
    "Superdriver": ItemData(0x009D, ItemType.RED_CHEST, ItemClassification.useful),
    "Stun gun": ItemData(0x009E, ItemType.RED_CHEST, ItemClassification.useful),
    "Battledriver": ItemData(0x009F, ItemType.RED_CHEST, ItemClassification.useful),
    "Launcher": ItemData(0x00A0, ItemType.RED_CHEST, ItemClassification.useful),
    "Freeze bow": ItemData(0x00A1, ItemType.RED_CHEST, ItemClassification.useful),
    "Cursed bow": ItemData(0x00A2, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x00A3: "Arty's bow" (uncursed)
    # ----- ARMOR -----
    "Apron": ItemData(0x00A4, ItemType.RED_CHEST, ItemClassification.useful),
    "Dress": ItemData(0x00A5, ItemType.RED_CHEST, ItemClassification.useful),
    "Cloth": ItemData(0x00A6, ItemType.RED_CHEST, ItemClassification.useful),
    "Lab-coat": ItemData(0x00A7, ItemType.RED_CHEST, ItemClassification.useful),
    "Hide armor": ItemData(0x00A8, ItemType.RED_CHEST, ItemClassification.useful),
    "Frock": ItemData(0x00A9, ItemType.RED_CHEST, ItemClassification.useful),
    "Robe": ItemData(0x00AA, ItemType.RED_CHEST, ItemClassification.useful),
    "Cloth armor": ItemData(0x00AB, ItemType.RED_CHEST, ItemClassification.useful),
    "Coat": ItemData(0x00AC, ItemType.RED_CHEST, ItemClassification.useful),
    "Tough hide": ItemData(0x00AD, ItemType.RED_CHEST, ItemClassification.useful),
    "Light dress": ItemData(0x00AE, ItemType.RED_CHEST, ItemClassification.useful),
    "Light armor": ItemData(0x00AF, ItemType.RED_CHEST, ItemClassification.useful),
    "Camu armor": ItemData(0x00B0, ItemType.RED_CHEST, ItemClassification.useful),
    "Baggy": ItemData(0x00B1, ItemType.RED_CHEST, ItemClassification.useful),
    "Tight dress": ItemData(0x00B2, ItemType.RED_CHEST, ItemClassification.useful),
    "Chainmail": ItemData(0x00B3, ItemType.RED_CHEST, ItemClassification.useful),
    "Holy wings": ItemData(0x00B4, ItemType.RED_CHEST, ItemClassification.useful),
    "Ironmail": ItemData(0x00B5, ItemType.RED_CHEST, ItemClassification.useful),
    "Toga": ItemData(0x00B6, ItemType.RED_CHEST, ItemClassification.useful),
    "Chain armor": ItemData(0x00B7, ItemType.RED_CHEST, ItemClassification.useful),
    "Thick cloth": ItemData(0x00B8, ItemType.RED_CHEST, ItemClassification.useful),
    "Stone plate": ItemData(0x00B9, ItemType.RED_CHEST, ItemClassification.useful),
    "Long robe": ItemData(0x00BA, ItemType.RED_CHEST, ItemClassification.useful),
    "Plated cloth": ItemData(0x00BB, ItemType.RED_CHEST, ItemClassification.useful),
    "Iron plate": ItemData(0x00BC, ItemType.RED_CHEST, ItemClassification.useful),
    "Metal mail": ItemData(0x00BD, ItemType.RED_CHEST, ItemClassification.useful),
    "Silk toga": ItemData(0x00BE, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver armor": ItemData(0x00BF, ItemType.RED_CHEST, ItemClassification.useful),
    "Light jacket": ItemData(0x00C0, ItemType.RED_CHEST, ItemClassification.useful),
    "Metal coat": ItemData(0x00C1, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver mail": ItemData(0x00C2, ItemType.RED_CHEST, ItemClassification.useful),
    "Power jacket": ItemData(0x00C3, ItemType.RED_CHEST, ItemClassification.useful),
    "Quilted silk": ItemData(0x00C4, ItemType.RED_CHEST, ItemClassification.useful),
    "Metal armor": ItemData(0x00C5, ItemType.RED_CHEST, ItemClassification.useful),
    "Power cape": ItemData(0x00C6, ItemType.RED_CHEST, ItemClassification.useful),
    "Magic bikini": ItemData(0x00C7, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver robe": ItemData(0x00C8, ItemType.RED_CHEST, ItemClassification.useful),
    "Evening gown": ItemData(0x00C9, ItemType.RED_CHEST, ItemClassification.useful),
    "Plate armor": ItemData(0x00CA, ItemType.RED_CHEST, ItemClassification.useful),
    "Plati plate": ItemData(0x00CB, ItemType.RED_CHEST, ItemClassification.useful),
    "Silk robe": ItemData(0x00CC, ItemType.RED_CHEST, ItemClassification.useful),
    "Revive armor": ItemData(0x00CD, ItemType.RED_CHEST, ItemClassification.useful),
    "Crystal mail": ItemData(0x00CE, ItemType.RED_CHEST, ItemClassification.useful),
    "Crystal robe": ItemData(0x00CF, ItemType.RED_CHEST, ItemClassification.useful),
    "Heal armor": ItemData(0x00D0, ItemType.RED_CHEST, ItemClassification.useful),
    "Metal jacket": ItemData(0x00D1, ItemType.RED_CHEST, ItemClassification.useful),
    "Deadly armor": ItemData(0x00D2, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x00D3: "Deadly armor" (uncursed)
    "Eron dress": ItemData(0x00D4, ItemType.RED_CHEST, ItemClassification.useful),
    "Bright armor": ItemData(0x00D5, ItemType.RED_CHEST, ItemClassification.useful),
    "Bright cloth": ItemData(0x00D6, ItemType.RED_CHEST, ItemClassification.useful),
    "Power robe": ItemData(0x00D7, ItemType.RED_CHEST, ItemClassification.useful),
    "Magic scale": ItemData(0x00D8, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x00D9: "Holy robe"
    "Ghostclothes": ItemData(0x00DA, ItemType.RED_CHEST, ItemClassification.useful),
    "Royal dress": ItemData(0x00DB, ItemType.RED_CHEST, ItemClassification.useful),
    "Full mail": ItemData(0x00DC, ItemType.RED_CHEST, ItemClassification.useful),
    "Old armor": ItemData(0x00DD, ItemType.RED_CHEST, ItemClassification.useful),
    "Zircon plate": ItemData(0x00DE, ItemType.RED_CHEST, ItemClassification.useful),
    "Zircon armor": ItemData(0x00DF, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Mirak plate": ItemData(0x40E0, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Ruse armor": ItemData(0x40E1, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x00E2: "Pearl armor"
    # ----- SHIELD -----
    "Chop board": ItemData(0x00E3, ItemType.RED_CHEST, ItemClassification.useful),
    "Small shield": ItemData(0x00E4, ItemType.RED_CHEST, ItemClassification.useful),
    "Hide shield": ItemData(0x00E5, ItemType.RED_CHEST, ItemClassification.useful),
    "Buckler": ItemData(0x00E6, ItemType.RED_CHEST, ItemClassification.useful),
    "Mini shield": ItemData(0x00E7, ItemType.RED_CHEST, ItemClassification.useful),
    "Wood shield": ItemData(0x00E8, ItemType.RED_CHEST, ItemClassification.useful),
    "Bracelet": ItemData(0x00E9, ItemType.RED_CHEST, ItemClassification.useful),
    "Power brace": ItemData(0x00EA, ItemType.RED_CHEST, ItemClassification.useful),
    "Kite shield": ItemData(0x00EB, ItemType.RED_CHEST, ItemClassification.useful),
    "Tough gloves": ItemData(0x00EC, ItemType.RED_CHEST, ItemClassification.useful),
    "Brone shield": ItemData(0x00ED, ItemType.RED_CHEST, ItemClassification.useful),
    "Anger brace": ItemData(0x00EE, ItemType.RED_CHEST, ItemClassification.useful),
    "Block shield": ItemData(0x00EF, ItemType.RED_CHEST, ItemClassification.useful),
    "Tecto gloves": ItemData(0x00F0, ItemType.RED_CHEST, ItemClassification.useful),
    "Round shield": ItemData(0x00F1, ItemType.RED_CHEST, ItemClassification.useful),
    "Pearl brace": ItemData(0x00F2, ItemType.RED_CHEST, ItemClassification.useful),
    "Fayza shield": ItemData(0x00F3, ItemType.RED_CHEST, ItemClassification.useful),
    "Big shield": ItemData(0x00F4, ItemType.RED_CHEST, ItemClassification.useful),
    "Tall shield": ItemData(0x00F5, ItemType.RED_CHEST, ItemClassification.useful),
    "Silvo shield": ItemData(0x00F6, ItemType.RED_CHEST, ItemClassification.useful),
    "Spike shield": ItemData(0x00F7, ItemType.RED_CHEST, ItemClassification.useful),
    "Slash shield": ItemData(0x00F8, ItemType.RED_CHEST, ItemClassification.useful),
    "Mage shield": ItemData(0x00F9, ItemType.RED_CHEST, ItemClassification.useful),
    "Tuff buckler": ItemData(0x00FA, ItemType.RED_CHEST, ItemClassification.useful),
    "Tect buckler": ItemData(0x00FB, ItemType.RED_CHEST, ItemClassification.useful),
    "Gold gloves": ItemData(0x00FC, ItemType.RED_CHEST, ItemClassification.useful),
    "Gold shield": ItemData(0x00FD, ItemType.RED_CHEST, ItemClassification.useful),
    "Plati gloves": ItemData(0x00FE, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Plati shield": ItemData(0x00FF, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Gauntlet": ItemData(0x0100, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Rune gloves": ItemData(0x0101, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Holy shield": ItemData(0x0102, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Zirco gloves": ItemData(0x0103, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Zirco shield": ItemData(0x0104, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Old shield": ItemData(0x0105, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Flame shield": ItemData(0x4106, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Water gaunt": ItemData(0x4107, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Bolt shield": ItemData(0x4108, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Cryst shield": ItemData(0x4109, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x010A: "Mega shield"
    "Dark mirror": ItemData(0x410B, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x010C: "Dark mirror" (uncursed)
    "Apron shield": ItemData(0x410D, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x010E: "Pearl shield"
    # ----- HEADGEAR -----
    "Pot": ItemData(0x010F, ItemType.RED_CHEST, ItemClassification.useful),
    "Beret": ItemData(0x0110, ItemType.RED_CHEST, ItemClassification.useful),
    "Cap": ItemData(0x0111, ItemType.RED_CHEST, ItemClassification.useful),
    "Cloth helmet": ItemData(0x0112, ItemType.RED_CHEST, ItemClassification.useful),
    "Hairband": ItemData(0x0113, ItemType.RED_CHEST, ItemClassification.useful),
    "Headband": ItemData(0x0114, ItemType.RED_CHEST, ItemClassification.useful),
    "Hide helmet": ItemData(0x0115, ItemType.RED_CHEST, ItemClassification.useful),
    "Jet helm": ItemData(0x0116, ItemType.RED_CHEST, ItemClassification.useful),
    "Red beret": ItemData(0x0117, ItemType.RED_CHEST, ItemClassification.useful),
    "Glass cap": ItemData(0x0118, ItemType.RED_CHEST, ItemClassification.useful),
    "Wood helmet": ItemData(0x0119, ItemType.RED_CHEST, ItemClassification.useful),
    "Blue beret": ItemData(0x011A, ItemType.RED_CHEST, ItemClassification.useful),
    "Brone helmet": ItemData(0x011B, ItemType.RED_CHEST, ItemClassification.useful),
    "Stone helmet": ItemData(0x011C, ItemType.RED_CHEST, ItemClassification.useful),
    "Cloche": ItemData(0x011D, ItemType.RED_CHEST, ItemClassification.useful),
    "Fury helmet": ItemData(0x011E, ItemType.RED_CHEST, ItemClassification.useful),
    "Iron helmet": ItemData(0x011F, ItemType.RED_CHEST, ItemClassification.useful),
    "Tight helmet": ItemData(0x0120, ItemType.RED_CHEST, ItemClassification.useful),
    "Turban": ItemData(0x0121, ItemType.RED_CHEST, ItemClassification.useful),
    "Plate cap": ItemData(0x0122, ItemType.RED_CHEST, ItemClassification.useful),
    "Roomy helmet": ItemData(0x0123, ItemType.RED_CHEST, ItemClassification.useful),
    "Tight turban": ItemData(0x0124, ItemType.RED_CHEST, ItemClassification.useful),
    "Glass cloche": ItemData(0x0125, ItemType.RED_CHEST, ItemClassification.useful),
    "Plate helmet": ItemData(0x0126, ItemType.RED_CHEST, ItemClassification.useful),
    "Rock helmet": ItemData(0x0127, ItemType.RED_CHEST, ItemClassification.useful),
    "Jute helmet": ItemData(0x0128, ItemType.RED_CHEST, ItemClassification.useful),
    "Shade hat": ItemData(0x0129, ItemType.RED_CHEST, ItemClassification.useful),
    "Metal cloche": ItemData(0x012A, ItemType.RED_CHEST, ItemClassification.useful),
    "SilverHelmet": ItemData(0x012B, ItemType.RED_CHEST, ItemClassification.useful),
    "Fury ribbon": ItemData(0x012C, ItemType.RED_CHEST, ItemClassification.useful),
    "Silver hat": ItemData(0x012D, ItemType.RED_CHEST, ItemClassification.useful),
    "Eron hat": ItemData(0x012E, ItemType.RED_CHEST, ItemClassification.useful),
    "Circlet": ItemData(0x012F, ItemType.RED_CHEST, ItemClassification.useful),
    "Golden helm": ItemData(0x0130, ItemType.RED_CHEST, ItemClassification.useful),
    "Gold band": ItemData(0x0131, ItemType.RED_CHEST, ItemClassification.useful),
    "Plati band": ItemData(0x0132, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Plati helm": ItemData(0x0133, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Crysto beret": ItemData(0x0134, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Crysto helm": ItemData(0x0135, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Holy cap": ItemData(0x0136, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Safety hat": ItemData(0x0137, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Zirco band": ItemData(0x0138, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Zirco helmet": ItemData(0x0139, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Old helmet": ItemData(0x013A, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Agony helm": ItemData(0x413B, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Boom turban": ItemData(0x413C, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Aqua helm": ItemData(0x413D, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Ice hairband": ItemData(0x413E, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x013F: "Legend helm"
    "Hairpin": ItemData(0x4140, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Brill helm": ItemData(0x0141, ItemType.ENTRANCE_CHEST, ItemClassification.useful),
    # 0x0142: "Pearl helmet"
    # ----- RING -----
    "Ear jewel": ItemData(0x0143, ItemType.RED_CHEST, ItemClassification.useful),
    "Glass brace": ItemData(0x0144, ItemType.RED_CHEST, ItemClassification.useful),
    "Glass ring": ItemData(0x0145, ItemType.RED_CHEST, ItemClassification.useful),
    "Earring": ItemData(0x4146, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Speedy ring": ItemData(0x0147, ItemType.RED_CHEST, ItemClassification.useful),
    "Power ring": ItemData(0x0148, ItemType.RED_CHEST, ItemClassification.useful),
    "Muscle ring": ItemData(0x0149, ItemType.RED_CHEST, ItemClassification.useful),
    "Protect ring": ItemData(0x014A, ItemType.RED_CHEST, ItemClassification.useful),
    "Mind ring": ItemData(0x014B, ItemType.RED_CHEST, ItemClassification.useful),
    "Witch ring": ItemData(0x014C, ItemType.RED_CHEST, ItemClassification.useful),
    "Fire ring": ItemData(0x014D, ItemType.RED_CHEST, ItemClassification.useful),
    "Water ring": ItemData(0x014E, ItemType.RED_CHEST, ItemClassification.useful),
    "Ice ring": ItemData(0x014F, ItemType.RED_CHEST, ItemClassification.useful),
    "Thunder ring": ItemData(0x0150, ItemType.RED_CHEST, ItemClassification.useful),
    "Fury ring": ItemData(0x0151, ItemType.RED_CHEST, ItemClassification.useful),
    "Mystery ring": ItemData(0x0152, ItemType.RED_CHEST, ItemClassification.useful),
    "Sonic ring": ItemData(0x0153, ItemType.RED_CHEST, ItemClassification.useful),
    "Hipower ring": ItemData(0x0154, ItemType.RED_CHEST, ItemClassification.useful),
    "Trick ring": ItemData(0x0155, ItemType.RED_CHEST, ItemClassification.useful),
    "Fake ring": ItemData(0x0156, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x0157: "S-fire ring"
    # 0x0158: "S-water ring"
    # 0x0159: "S-ice ring"
    # 0x015A: "S-thun ring"
    "S-power ring": ItemData(0x015B, ItemType.RED_CHEST, ItemClassification.useful),
    "S-mind ring": ItemData(0x015C, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "S-pro ring": ItemData(0x015D, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "S-witch ring": ItemData(0x015E, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Undead ring": ItemData(0x015F, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Rocket ring": ItemData(0x0160, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Ghost ring": ItemData(0x0161, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Angry ring": ItemData(0x0162, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "S-myst ring": ItemData(0x0163, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Dia ring": ItemData(0x4164, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Sea ring": ItemData(0x4165, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Dragon ring": ItemData(0x0166, ItemType.ENTRANCE_CHEST, ItemClassification.useful),
    "Engage ring": ItemData(0x4167, ItemType.BLUE_CHEST, ItemClassification.useful),
    # 0x0168: "Egg ring"
    # ----- ROCK -----
    "Horse rock": ItemData(0x0169, ItemType.RED_CHEST, ItemClassification.useful),
    "Eagle rock": ItemData(0x016A, ItemType.RED_CHEST, ItemClassification.useful),
    "Lion fang": ItemData(0x016B, ItemType.RED_CHEST, ItemClassification.useful),
    "Bee rock": ItemData(0x016C, ItemType.RED_CHEST, ItemClassification.useful),
    "Snake rock": ItemData(0x016D, ItemType.RED_CHEST, ItemClassification.useful),
    "Cancer rock": ItemData(0x016E, ItemType.RED_CHEST, ItemClassification.useful),
    "Pumkin jewel": ItemData(0x016F, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Uni jewel": ItemData(0x0170, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Mysto jewel": ItemData(0x0171, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Samu jewel": ItemData(0x0172, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Bat rock": ItemData(0x0173, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Hidora rock": ItemData(0x0174, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Flame jewel": ItemData(0x0175, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Water jewel": ItemData(0x4176, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Thundo jewel": ItemData(0x4177, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Earth jewel": ItemData(0x4178, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Twist jewel": ItemData(0x4179, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Gloom jewel": ItemData(0x417A, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Tidal jewel": ItemData(0x417B, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Magma rock": ItemData(0x017C, ItemType.ENEMY_DROP, ItemClassification.useful),
    "Evil jewel": ItemData(0x017D, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    # 0x017E: "Evil jewel" (uncursed)
    "Gorgon rock": ItemData(0x017F, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Song rock": ItemData(0x0180, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Kraken rock": ItemData(0x0181, ItemType.RED_CHEST_PATCH, ItemClassification.useful),
    "Catfish jwl.": ItemData(0x4182, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Camu jewel": ItemData(0x4183, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Spido jewel": ItemData(0x4184, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Gorgan rock": ItemData(0x4185, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Light jewel": ItemData(0x0186, ItemType.ENTRANCE_CHEST, ItemClassification.useful),
    "Black eye": ItemData(0x4187, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Silver eye": ItemData(0x4188, ItemType.BLUE_CHEST, ItemClassification.useful),
    "Gold eye": ItemData(0x4189, ItemType.BLUE_CHEST, ItemClassification.useful),
    # ----- OTHER -----
    # 0x018A: "1 coin"
    # 0x018B: "10 coin set"
    # 0x018C: "50 coin set"
    # 0x018D: "100 coin set"
    # 0x018E: "Flame charm"
    # 0x018F: "Zap charm"
    # 0x0190: "Magic lamp"
    # 0x0191: "Statue"
    # 0x0192: "Rage knife"
    # 0x0193: "Fortune whip"
    # 0x0194: "Dragon blade"
    # 0x0195: "Bunny ring"
    # 0x0196: "Bunny ears"
    # 0x0197: "Bunnylady"
    # 0x0198: "Bunny sword"
    # 0x0199: "Bunnysuit"
    # 0x019A: "Seethru cape"
    # 0x019B: "Seethru silk"
    "Iris sword": ItemData(0x039C, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris shield": ItemData(0x039D, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris helmet": ItemData(0x039E, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris armor": ItemData(0x039F, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris ring": ItemData(0x03A0, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris jewel": ItemData(0x03A1, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris staff": ItemData(0x03A2, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris pot": ItemData(0x03A3, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    "Iris tiara": ItemData(0x03A4, ItemType.IRIS_TREASURE, ItemClassification.progression_skip_balancing),
    # 0x01A5: "Power jelly"
    # 0x01A6: "Jewel sonar"
    # 0x01A7: "Hook"
    # 0x01A8: "Bomb"
    # 0x01A9: "Arrow"
    # 0x01AA: "Fire arrow"
    # 0x01AB: "Hammer"
    # 0x01AC: "Treas. sword"
    # 0x01AD: "Door key"
    # 0x01AE: "Shrine key"
    # 0x01AF: "Sky key"
    # 0x01B0: "Lake key"
    # 0x01B1: "Ruby key"
    "Selan": ItemData(0x01B2, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Wind key"
    "Guy": ItemData(0x01B3, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Cloud key"
    "Arty": ItemData(0x01B4, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Light key"
    "Dekar": ItemData(0x01B5, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Sword key"
    "Tia": ItemData(0x01B6, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Tree key"
    "Lexis": ItemData(0x01B7, ItemType.PARTY_MEMBER, ItemClassification.progression),  # replaces "Flower key"
    "JELZE": ItemData(0x01B8, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Magma key"
    "FLASH": ItemData(0x01B9, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Heart key"
    "GUSTO": ItemData(0x01BA, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Ghost key"
    "ZEPPY": ItemData(0x01BB, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Trial key"
    "DARBI": ItemData(0x01BC, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Dankirk key"
    "SULLY": ItemData(0x01BD, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Basement key"
    "BLAZE": ItemData(0x01BE, ItemType.CAPSULE_MONSTER, ItemClassification.progression),  # replaces "Narcysus key"
    # 0x01BF: "Truth key"
    # 0x01C0: "Mermaid jade"
    # 0x01C1: "Engine"
    "Ancient key": ItemData(0x01C2, ItemType.BOSS, ItemClassification.progression_skip_balancing),
    # 0x01C3: "Pretty flwr."
    # 0x01C4: "Glass angel"
    # 0x01C5: "VIP card"
    # 0x01C6: "Key26"
    # 0x01C7: "Key27"
    # 0x01C8: "Key28"
    # 0x01C9: "Key29"
    # 0x01CA: "AP item"  # replaces "Key30"
    # 0x01CB: "SOLD OUT"  # replaces "Crown"
    # 0x01CC: "Ruby apple"
    # 0x01CD: "PURIFIA"
    # 0x01CE: "Tag ring"
    # 0x01CF: "Tag ring" (uncursed)
    # 0x01D0: "RAN-RAN step"
    # 0x01D1: "Tag candy"
    # 0x01D2: "Last"
    # ----- SPELL -----
    "Flash": ItemData(0x8000, ItemType.RED_CHEST, ItemClassification.useful),
    "Bolt": ItemData(0x8001, ItemType.RED_CHEST, ItemClassification.useful),
    "Thunder": ItemData(0x8002, ItemType.RED_CHEST, ItemClassification.useful),
    "Spark": ItemData(0x8003, ItemType.RED_CHEST, ItemClassification.useful),
    "Fireball": ItemData(0x8004, ItemType.RED_CHEST, ItemClassification.useful),
    "Firebird": ItemData(0x8005, ItemType.RED_CHEST, ItemClassification.useful),
    "Droplet": ItemData(0x8006, ItemType.RED_CHEST, ItemClassification.useful),
    "Vortex": ItemData(0x8007, ItemType.RED_CHEST, ItemClassification.useful),
    "Dragon": ItemData(0x8008, ItemType.RED_CHEST, ItemClassification.useful),
    "Gale": ItemData(0x8009, ItemType.RED_CHEST, ItemClassification.useful),
    "Blizzard": ItemData(0x800A, ItemType.RED_CHEST, ItemClassification.useful),
    "Ice Valk": ItemData(0x800B, ItemType.RED_CHEST, ItemClassification.useful),
    "Perish": ItemData(0x800C, ItemType.RED_CHEST, ItemClassification.useful),
    "Destroy": ItemData(0x800D, ItemType.RED_CHEST, ItemClassification.useful),
    "Drowsy": ItemData(0x800E, ItemType.RED_CHEST, ItemClassification.useful),
    "Coma": ItemData(0x800F, ItemType.RED_CHEST, ItemClassification.useful),
    "Dread": ItemData(0x8010, ItemType.RED_CHEST, ItemClassification.useful),
    "Deflect": ItemData(0x8011, ItemType.RED_CHEST, ItemClassification.useful),
    "Absorb": ItemData(0x8012, ItemType.RED_CHEST, ItemClassification.useful),
    "Fake": ItemData(0x8013, ItemType.RED_CHEST, ItemClassification.useful),
    "Trick": ItemData(0x8014, ItemType.RED_CHEST, ItemClassification.useful),
    "Confuse": ItemData(0x8015, ItemType.RED_CHEST, ItemClassification.useful),
    "Bravery": ItemData(0x8016, ItemType.RED_CHEST, ItemClassification.useful),
    "Courage": ItemData(0x8017, ItemType.RED_CHEST, ItemClassification.useful),
    "Mirror": ItemData(0x8018, ItemType.RED_CHEST, ItemClassification.useful),
    "Strong": ItemData(0x8019, ItemType.RED_CHEST, ItemClassification.useful),
    "Stronger": ItemData(0x801A, ItemType.RED_CHEST, ItemClassification.useful),
    "Champion": ItemData(0x801B, ItemType.RED_CHEST, ItemClassification.useful),
    "Poison": ItemData(0x801C, ItemType.RED_CHEST, ItemClassification.useful),
    "Rally": ItemData(0x801D, ItemType.RED_CHEST, ItemClassification.useful),
    "Valor": ItemData(0x801E, ItemType.RED_CHEST, ItemClassification.useful),
    "Fry": ItemData(0x801F, ItemType.RED_CHEST, ItemClassification.useful),
    "Zap": ItemData(0x8020, ItemType.RED_CHEST, ItemClassification.useful),
    "Shield": ItemData(0x8021, ItemType.RED_CHEST, ItemClassification.useful),
    "Waken": ItemData(0x8022, ItemType.RED_CHEST, ItemClassification.useful),
    # 0x8023: "Release"
    # 0x8024: "Warp"
    # 0x8025: "Escape"
    # 0x8026: "Reset"
    # 0x8027: "Light"
}

l2ac_item_name_to_id: Dict[str, int] = {name: (start_id + data.code) for name, data in l2ac_item_table.items()}
