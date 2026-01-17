from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class FF12OpenWorldItem(Item):
    game: str = "Final Fantasy 12 Open World"


class FF12OpenWorldItemData(NamedTuple):
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    category: str = ""
    weight: int = 0
    amount: int = 1
    duplicateAmount: int = 1


item_data_table: Dict[str, FF12OpenWorldItemData] = {
    "Potion": FF12OpenWorldItemData(
        code=1,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Hi-Potion": FF12OpenWorldItemData(
        code=2,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "X-Potion": FF12OpenWorldItemData(
        code=3,
        classification=ItemClassification.filler,
        category="Item",
        weight=68
    ),
    "Ether": FF12OpenWorldItemData(
        code=4,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Hi-Ether": FF12OpenWorldItemData(
        code=5,
        classification=ItemClassification.filler,
        category="Item",
        weight=34
    ),
    "Elixir": FF12OpenWorldItemData(
        code=6,
        classification=ItemClassification.filler,
        category="Item",
        weight=12
    ),
    "Phoenix Down": FF12OpenWorldItemData(
        code=7,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Gold Needle": FF12OpenWorldItemData(
        code=8,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Echo Herbs": FF12OpenWorldItemData(
        code=9,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Antidote": FF12OpenWorldItemData(
        code=10,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Eye Drops": FF12OpenWorldItemData(
        code=11,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Prince's Kiss": FF12OpenWorldItemData(
        code=12,
        classification=ItemClassification.filler,
        category="Item",
        weight=280
    ),
    "Handkerchief": FF12OpenWorldItemData(
        code=13,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Chronos Tear": FF12OpenWorldItemData(
        code=14,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Nu Khai Sand": FF12OpenWorldItemData(
        code=15,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Serum": FF12OpenWorldItemData(
        code=16,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Remedy": FF12OpenWorldItemData(
        code=17,
        classification=ItemClassification.filler,
        category="Item",
        weight=68
    ),
    "Soleil Fang": FF12OpenWorldItemData(
        code=18,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Rime Fang": FF12OpenWorldItemData(
        code=19,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Lightning Fang": FF12OpenWorldItemData(
        code=20,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Bacchus's Wine": FF12OpenWorldItemData(
        code=21,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Megalixir": FF12OpenWorldItemData(
        code=22,
        classification=ItemClassification.filler,
        category="Item",
        weight=2
    ),
    "Baltoro Seed": FF12OpenWorldItemData(
        code=23,
        classification=ItemClassification.filler,
        category="Item",
        weight=2
    ),
    "Domaine Calvados": FF12OpenWorldItemData(
        code=24,
        classification=ItemClassification.filler,
        category="Item",
        weight=12
    ),
    "Dark Energy": FF12OpenWorldItemData(
        code=25,
        classification=ItemClassification.filler,
        category="Item",
        weight=2
    ),
    "Meteorite A": FF12OpenWorldItemData(
        code=26,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Meteorite B": FF12OpenWorldItemData(
        code=27,
        classification=ItemClassification.filler,
        category="Item",
        weight=68
    ),
    "Meteorite C": FF12OpenWorldItemData(
        code=28,
        classification=ItemClassification.filler,
        category="Item",
        weight=34
    ),
    "Meteorite D": FF12OpenWorldItemData(
        code=29,
        classification=ItemClassification.filler,
        category="Item",
        weight=2
    ),
    "Reverse Mote": FF12OpenWorldItemData(
        code=43,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Dark Mote": FF12OpenWorldItemData(
        code=44,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Aero Mote": FF12OpenWorldItemData(
        code=45,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Aquara Mote": FF12OpenWorldItemData(
        code=46,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Bio Mote": FF12OpenWorldItemData(
        code=47,
        classification=ItemClassification.filler,
        category="Item",
        weight=68
    ),
    "Shock Mote": FF12OpenWorldItemData(
        code=48,
        classification=ItemClassification.filler,
        category="Item",
        weight=34
    ),
    "Holy Mote": FF12OpenWorldItemData(
        code=49,
        classification=ItemClassification.filler,
        category="Item",
        weight=24
    ),
    "Scathe Mote": FF12OpenWorldItemData(
        code=50,
        classification=ItemClassification.filler,
        category="Item",
        weight=24
    ),
    "Balance Mote": FF12OpenWorldItemData(
        code=51,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Gravity Mote": FF12OpenWorldItemData(
        code=52,
        classification=ItemClassification.filler,
        category="Item",
        weight=138
    ),
    "Cura Mote": FF12OpenWorldItemData(
        code=53,
        classification=ItemClassification.filler,
        category="Item",
        weight=68
    ),
    "Dispel Mote": FF12OpenWorldItemData(
        code=54,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Aeroga Mote": FF12OpenWorldItemData(
        code=55,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Warp Mote": FF12OpenWorldItemData(
        code=56,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Bubble Mote": FF12OpenWorldItemData(
        code=57,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Hastega Mote": FF12OpenWorldItemData(
        code=58,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Reflectga Mote": FF12OpenWorldItemData(
        code=59,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Vanishga Mote": FF12OpenWorldItemData(
        code=60,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Float Mote": FF12OpenWorldItemData(
        code=61,
        classification=ItemClassification.filler,
        category="Item",
        weight=98
    ),
    "Eksir Berries": FF12OpenWorldItemData(
        code=62,
        classification=ItemClassification.filler,
        category="Item",
        weight=400
    ),
    "Dark Matter": FF12OpenWorldItemData(
        code=63,
        classification=ItemClassification.filler,
        category="Item",
        weight=12
    ),
    "Knot of Rust": FF12OpenWorldItemData(
        code=64,
        classification=ItemClassification.filler,
        category="Item",
        weight=196
    ),
    "Broadsword": FF12OpenWorldItemData(
        code=4098,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Longsword": FF12OpenWorldItemData(
        code=4099,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Iron Sword": FF12OpenWorldItemData(
        code=4100,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Zwill Blade": FF12OpenWorldItemData(
        code=4101,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Ancient Sword": FF12OpenWorldItemData(
        code=4102,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Blood Sword": FF12OpenWorldItemData(
        code=4103,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Lohengrin": FF12OpenWorldItemData(
        code=4104,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Flametongue": FF12OpenWorldItemData(
        code=4105,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Demonsbane": FF12OpenWorldItemData(
        code=4106,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Icebrand": FF12OpenWorldItemData(
        code=4107,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Platinum Sword": FF12OpenWorldItemData(
        code=4108,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Bastard Sword": FF12OpenWorldItemData(
        code=4109,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Diamond Sword": FF12OpenWorldItemData(
        code=4110,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Runeblade": FF12OpenWorldItemData(
        code=4111,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Deathbringer": FF12OpenWorldItemData(
        code=4112,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Stoneblade": FF12OpenWorldItemData(
        code=4113,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Durandal": FF12OpenWorldItemData(
        code=4114,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Claymore": FF12OpenWorldItemData(
        code=4115,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Defender": FF12OpenWorldItemData(
        code=4116,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Save the Queen": FF12OpenWorldItemData(
        code=4117,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Ragnarok": FF12OpenWorldItemData(
        code=4118,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Ultima Blade": FF12OpenWorldItemData(
        code=4119,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Excalibur": FF12OpenWorldItemData(
        code=4120,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Tournesol": FF12OpenWorldItemData(
        code=4121,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Kotetsu": FF12OpenWorldItemData(
        code=4122,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Osafune": FF12OpenWorldItemData(
        code=4123,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Kogarasumaru": FF12OpenWorldItemData(
        code=4124,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Magoroku": FF12OpenWorldItemData(
        code=4125,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Murasame": FF12OpenWorldItemData(
        code=4126,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Kiku-ichimonji": FF12OpenWorldItemData(
        code=4127,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Yakei": FF12OpenWorldItemData(
        code=4128,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Ame-no-Murakumo": FF12OpenWorldItemData(
        code=4129,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Muramasa": FF12OpenWorldItemData(
        code=4130,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Masamune": FF12OpenWorldItemData(
        code=4131,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Ashura": FF12OpenWorldItemData(
        code=4132,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Sakura-saezuri": FF12OpenWorldItemData(
        code=4133,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Kagenui": FF12OpenWorldItemData(
        code=4134,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Koga Blade": FF12OpenWorldItemData(
        code=4135,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Iga Blade": FF12OpenWorldItemData(
        code=4136,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Orochi": FF12OpenWorldItemData(
        code=4137,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Yagyu Darkblade": FF12OpenWorldItemData(
        code=4138,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Javelin": FF12OpenWorldItemData(
        code=4139,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Spear": FF12OpenWorldItemData(
        code=4140,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Partisan": FF12OpenWorldItemData(
        code=4141,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Heavy Lance": FF12OpenWorldItemData(
        code=4142,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Storm Spear": FF12OpenWorldItemData(
        code=4143,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Obelisk": FF12OpenWorldItemData(
        code=4144,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Halberd": FF12OpenWorldItemData(
        code=4145,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Trident": FF12OpenWorldItemData(
        code=4146,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Holy Lance": FF12OpenWorldItemData(
        code=4147,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Gungnir": FF12OpenWorldItemData(
        code=4148,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Dragon Whisker": FF12OpenWorldItemData(
        code=4149,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Zodiac Spear": FF12OpenWorldItemData(
        code=4150,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Oaken Pole": FF12OpenWorldItemData(
        code=4151,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Cypress Pole": FF12OpenWorldItemData(
        code=4152,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Battle Bamboo": FF12OpenWorldItemData(
        code=4153,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Musk Stick": FF12OpenWorldItemData(
        code=4154,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Iron Pole": FF12OpenWorldItemData(
        code=4155,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Six-fluted Pole": FF12OpenWorldItemData(
        code=4156,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Gokuu Pole": FF12OpenWorldItemData(
        code=4157,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Zephyr Pole": FF12OpenWorldItemData(
        code=4158,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Ivory Pole": FF12OpenWorldItemData(
        code=4159,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Sweep": FF12OpenWorldItemData(
        code=4160,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Eight-fluted Pole": FF12OpenWorldItemData(
        code=4161,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Whale Whisker": FF12OpenWorldItemData(
        code=4162,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Shortbow": FF12OpenWorldItemData(
        code=4163,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Silver Bow": FF12OpenWorldItemData(
        code=4164,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Aevis Killer": FF12OpenWorldItemData(
        code=4165,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Killer Bow": FF12OpenWorldItemData(
        code=4166,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Longbow": FF12OpenWorldItemData(
        code=4167,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Elfin Bow": FF12OpenWorldItemData(
        code=4168,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Loxley Bow": FF12OpenWorldItemData(
        code=4169,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Giant Stonebow": FF12OpenWorldItemData(
        code=4170,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Burning Bow": FF12OpenWorldItemData(
        code=4171,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Traitor's Bow": FF12OpenWorldItemData(
        code=4172,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Yoichi Bow": FF12OpenWorldItemData(
        code=4173,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Perseus Bow": FF12OpenWorldItemData(
        code=4174,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Artemis Bow": FF12OpenWorldItemData(
        code=4175,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Sagittarius": FF12OpenWorldItemData(
        code=4176,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Bowgun": FF12OpenWorldItemData(
        code=4177,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Crossbow": FF12OpenWorldItemData(
        code=4178,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Paramina Crossbow": FF12OpenWorldItemData(
        code=4179,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Recurve Crossbow": FF12OpenWorldItemData(
        code=4180,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Hunting Crossbow": FF12OpenWorldItemData(
        code=4181,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Penetrator Crossbow": FF12OpenWorldItemData(
        code=4182,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Gastrophetes": FF12OpenWorldItemData(
        code=4183,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Altair": FF12OpenWorldItemData(
        code=4184,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Capella": FF12OpenWorldItemData(
        code=4185,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Vega": FF12OpenWorldItemData(
        code=4186,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Sirius": FF12OpenWorldItemData(
        code=4187,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Betelgeuse": FF12OpenWorldItemData(
        code=4188,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Ras Algethi": FF12OpenWorldItemData(
        code=4189,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Aldebaran": FF12OpenWorldItemData(
        code=4190,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Spica": FF12OpenWorldItemData(
        code=4191,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Antares": FF12OpenWorldItemData(
        code=4192,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Arcturus": FF12OpenWorldItemData(
        code=4193,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Fomalhaut": FF12OpenWorldItemData(
        code=4194,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Handaxe": FF12OpenWorldItemData(
        code=4195,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Broadaxe": FF12OpenWorldItemData(
        code=4196,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Slasher": FF12OpenWorldItemData(
        code=4197,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Hammerhead": FF12OpenWorldItemData(
        code=4198,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Francisca": FF12OpenWorldItemData(
        code=4199,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Greataxe": FF12OpenWorldItemData(
        code=4200,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Golden Axe": FF12OpenWorldItemData(
        code=4201,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Iron Hammer": FF12OpenWorldItemData(
        code=4202,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "War Hammer": FF12OpenWorldItemData(
        code=4203,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Sledgehammer": FF12OpenWorldItemData(
        code=4204,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Morning Star": FF12OpenWorldItemData(
        code=4205,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Scorpion Tail": FF12OpenWorldItemData(
        code=4206,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Dagger": FF12OpenWorldItemData(
        code=4207,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Mage Masher": FF12OpenWorldItemData(
        code=4208,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Assassin's Dagger": FF12OpenWorldItemData(
        code=4209,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Chopper": FF12OpenWorldItemData(
        code=4210,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Main Gauche": FF12OpenWorldItemData(
        code=4211,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Gladius": FF12OpenWorldItemData(
        code=4212,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Avenger": FF12OpenWorldItemData(
        code=4213,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Orichalcum Dirk": FF12OpenWorldItemData(
        code=4214,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Platinum Dagger": FF12OpenWorldItemData(
        code=4215,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Zwill Crossblade": FF12OpenWorldItemData(
        code=4216,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Shikari Nagasa": FF12OpenWorldItemData(
        code=4217,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Rod": FF12OpenWorldItemData(
        code=4218,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Serpent Rod": FF12OpenWorldItemData(
        code=4219,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Healing Rod": FF12OpenWorldItemData(
        code=4220,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Gaia Rod": FF12OpenWorldItemData(
        code=4221,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Power Rod": FF12OpenWorldItemData(
        code=4222,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Empyrean Rod": FF12OpenWorldItemData(
        code=4223,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Holy Rod": FF12OpenWorldItemData(
        code=4224,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Rod of Faith": FF12OpenWorldItemData(
        code=4225,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Oak Staff": FF12OpenWorldItemData(
        code=4226,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Cherry Staff": FF12OpenWorldItemData(
        code=4227,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Wizard's Staff": FF12OpenWorldItemData(
        code=4228,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Flame Staff": FF12OpenWorldItemData(
        code=4229,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Storm Staff": FF12OpenWorldItemData(
        code=4230,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Glacial Staff": FF12OpenWorldItemData(
        code=4231,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Golden Staff": FF12OpenWorldItemData(
        code=4232,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Judicer's Staff": FF12OpenWorldItemData(
        code=4233,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Cloud Staff": FF12OpenWorldItemData(
        code=4234,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Staff of the Magi": FF12OpenWorldItemData(
        code=4235,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Mace": FF12OpenWorldItemData(
        code=4236,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Bronze Mace": FF12OpenWorldItemData(
        code=4237,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Bhuj": FF12OpenWorldItemData(
        code=4238,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Miter": FF12OpenWorldItemData(
        code=4239,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Thorned Mace": FF12OpenWorldItemData(
        code=4240,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Chaos Mace": FF12OpenWorldItemData(
        code=4241,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Doom Mace": FF12OpenWorldItemData(
        code=4242,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Zeus Mace": FF12OpenWorldItemData(
        code=4243,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Grand Mace": FF12OpenWorldItemData(
        code=4244,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Gilt Measure": FF12OpenWorldItemData(
        code=4245,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Arc Scale": FF12OpenWorldItemData(
        code=4246,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Multiscale": FF12OpenWorldItemData(
        code=4247,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Cross Scale": FF12OpenWorldItemData(
        code=4248,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Caliper": FF12OpenWorldItemData(
        code=4249,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Euclid's Sextant": FF12OpenWorldItemData(
        code=4250,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Hornito": FF12OpenWorldItemData(
        code=4251,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Fumarole": FF12OpenWorldItemData(
        code=4252,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Tumulus": FF12OpenWorldItemData(
        code=4253,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Caldera": FF12OpenWorldItemData(
        code=4254,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Volcano": FF12OpenWorldItemData(
        code=4255,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Bonebreaker": FF12OpenWorldItemData(
        code=4256,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Mythril Sword": FF12OpenWorldItemData(
        code=4257,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Mythril Blade": FF12OpenWorldItemData(
        code=4265,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Kumbha": FF12OpenWorldItemData(
        code=4267,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Mesa": FF12OpenWorldItemData(
        code=4268,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Mina": FF12OpenWorldItemData(
        code=4269,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Wyrmhero Blade": FF12OpenWorldItemData(
        code=4270,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Vrsabha": FF12OpenWorldItemData(
        code=4271,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Bone of Byblos": FF12OpenWorldItemData(
        code=4272,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Tula": FF12OpenWorldItemData(
        code=4273,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Great Trango": FF12OpenWorldItemData(
        code=4274,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Seitengrat": FF12OpenWorldItemData(
        code=4275,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=1
    ),
    "Karkata": FF12OpenWorldItemData(
        code=4289,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Excalipur": FF12OpenWorldItemData(
        code=4290,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Simha": FF12OpenWorldItemData(
        code=4291,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Makara": FF12OpenWorldItemData(
        code=4292,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Vrscika": FF12OpenWorldItemData(
        code=4293,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=6
    ),
    "Mithuna": FF12OpenWorldItemData(
        code=4294,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Kanya": FF12OpenWorldItemData(
        code=4295,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Dhanusha": FF12OpenWorldItemData(
        code=4296,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Gendarme": FF12OpenWorldItemData(
        code=4297,
        classification=ItemClassification.filler,
        category="Armor",
        weight=1
    ),
    "Leather Shield": FF12OpenWorldItemData(
        code=4298,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Buckler": FF12OpenWorldItemData(
        code=4299,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Bronze Shield": FF12OpenWorldItemData(
        code=4300,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Round Shield": FF12OpenWorldItemData(
        code=4301,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Shell Shield": FF12OpenWorldItemData(
        code=4302,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Golden Shield": FF12OpenWorldItemData(
        code=4303,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Ice Shield": FF12OpenWorldItemData(
        code=4304,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Flame Shield": FF12OpenWorldItemData(
        code=4305,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Diamond Shield": FF12OpenWorldItemData(
        code=4306,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Platinum Shield": FF12OpenWorldItemData(
        code=4307,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Dragon Shield": FF12OpenWorldItemData(
        code=4308,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Crystal Shield": FF12OpenWorldItemData(
        code=4309,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Genji Shield": FF12OpenWorldItemData(
        code=4310,
        classification=ItemClassification.filler,
        category="Armor",
        weight=6
    ),
    "Kaiser Shield": FF12OpenWorldItemData(
        code=4311,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Aegis Shield": FF12OpenWorldItemData(
        code=4312,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Demon Shield": FF12OpenWorldItemData(
        code=4313,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Venetian Shield": FF12OpenWorldItemData(
        code=4314,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Zodiac Escutcheon": FF12OpenWorldItemData(
        code=4315,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Ensanguined Shield": FF12OpenWorldItemData(
        code=4316,
        classification=ItemClassification.filler,
        category="Armor",
        weight=6
    ),
    "Leather Cap": FF12OpenWorldItemData(
        code=4317,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Headgear": FF12OpenWorldItemData(
        code=4318,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Headguard": FF12OpenWorldItemData(
        code=4319,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Leather Headgear": FF12OpenWorldItemData(
        code=4320,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Horned Hat": FF12OpenWorldItemData(
        code=4321,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Balaclava": FF12OpenWorldItemData(
        code=4322,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Soldier's Cap": FF12OpenWorldItemData(
        code=4323,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Green Beret": FF12OpenWorldItemData(
        code=4324,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Red Cap": FF12OpenWorldItemData(
        code=4325,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Headband": FF12OpenWorldItemData(
        code=4326,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Pirate Hat": FF12OpenWorldItemData(
        code=4327,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Goggle Mask": FF12OpenWorldItemData(
        code=4328,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Adamant Hat": FF12OpenWorldItemData(
        code=4329,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Officer's Hat": FF12OpenWorldItemData(
        code=4330,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Chakra Band": FF12OpenWorldItemData(
        code=4331,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Thief's Cap": FF12OpenWorldItemData(
        code=4332,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Gigas Hat": FF12OpenWorldItemData(
        code=4333,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Chaperon": FF12OpenWorldItemData(
        code=4334,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Crown of Laurels": FF12OpenWorldItemData(
        code=4335,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Renewing Morion": FF12OpenWorldItemData(
        code=4336,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Dueling Mask": FF12OpenWorldItemData(
        code=4337,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Cotton Cap": FF12OpenWorldItemData(
        code=4338,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Magick Curch": FF12OpenWorldItemData(
        code=4339,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Pointy Hat": FF12OpenWorldItemData(
        code=4340,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Topkapi Hat": FF12OpenWorldItemData(
        code=4341,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Calot Hat": FF12OpenWorldItemData(
        code=4342,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Wizard's Hat": FF12OpenWorldItemData(
        code=4343,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Lambent Hat": FF12OpenWorldItemData(
        code=4344,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Feathered Cap": FF12OpenWorldItemData(
        code=4345,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Mage's Hat": FF12OpenWorldItemData(
        code=4346,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Lamia's Tiara": FF12OpenWorldItemData(
        code=4347,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Sorcerer's Hat": FF12OpenWorldItemData(
        code=4348,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Black Cowl": FF12OpenWorldItemData(
        code=4349,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Astrakhan Hat": FF12OpenWorldItemData(
        code=4350,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Gaia Hat": FF12OpenWorldItemData(
        code=4351,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Hypnocrown": FF12OpenWorldItemData(
        code=4352,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Gold Hairpin": FF12OpenWorldItemData(
        code=4353,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Celebrant's Miter": FF12OpenWorldItemData(
        code=4354,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Black Mask": FF12OpenWorldItemData(
        code=4355,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "White Mask": FF12OpenWorldItemData(
        code=4356,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Golden Skullcap": FF12OpenWorldItemData(
        code=4357,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Circlet": FF12OpenWorldItemData(
        code=4358,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Leather Helm": FF12OpenWorldItemData(
        code=4359,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Bronze Helm": FF12OpenWorldItemData(
        code=4360,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Sallet": FF12OpenWorldItemData(
        code=4361,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Iron Helm": FF12OpenWorldItemData(
        code=4362,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Barbut": FF12OpenWorldItemData(
        code=4363,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Winged Helm": FF12OpenWorldItemData(
        code=4364,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Golden Helm": FF12OpenWorldItemData(
        code=4365,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Burgonet": FF12OpenWorldItemData(
        code=4366,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Close Helmet": FF12OpenWorldItemData(
        code=4367,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Bone Helm": FF12OpenWorldItemData(
        code=4368,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Diamond Helm": FF12OpenWorldItemData(
        code=4369,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Steel Mask": FF12OpenWorldItemData(
        code=4370,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Platinum Helm": FF12OpenWorldItemData(
        code=4371,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Giant's Helmet": FF12OpenWorldItemData(
        code=4372,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Dragon Helm": FF12OpenWorldItemData(
        code=4373,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Genji Helm": FF12OpenWorldItemData(
        code=4374,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Magepower Shishak": FF12OpenWorldItemData(
        code=4375,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Grand Helm": FF12OpenWorldItemData(
        code=4376,
        classification=ItemClassification.filler,
        category="Armor",
        weight=6
    ),
    "Leather Clothing": FF12OpenWorldItemData(
        code=4377,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Chromed Leathers": FF12OpenWorldItemData(
        code=4378,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Leather Breastplate": FF12OpenWorldItemData(
        code=4379,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Bronze Chestplate": FF12OpenWorldItemData(
        code=4380,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Ringmail": FF12OpenWorldItemData(
        code=4381,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Windbreaker": FF12OpenWorldItemData(
        code=4382,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Heavy Coat": FF12OpenWorldItemData(
        code=4383,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Survival Vest": FF12OpenWorldItemData(
        code=4384,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Brigandine": FF12OpenWorldItemData(
        code=4385,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Jujitsu Gi": FF12OpenWorldItemData(
        code=4386,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Viking Coat": FF12OpenWorldItemData(
        code=4387,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Metal Jerkin": FF12OpenWorldItemData(
        code=4388,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Adamant Vest": FF12OpenWorldItemData(
        code=4389,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Barrel Coat": FF12OpenWorldItemData(
        code=4390,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Power Vest": FF12OpenWorldItemData(
        code=4391,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Ninja Gear": FF12OpenWorldItemData(
        code=4392,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Gigas Chestplate": FF12OpenWorldItemData(
        code=4393,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Minerva Bustier": FF12OpenWorldItemData(
        code=4394,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Rubber Suit": FF12OpenWorldItemData(
        code=4395,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Mirage Vest": FF12OpenWorldItemData(
        code=4396,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Brave Suit": FF12OpenWorldItemData(
        code=4397,
        classification=ItemClassification.filler,
        category="Armor",
        weight=6
    ),
    "Cotton Shirt": FF12OpenWorldItemData(
        code=4398,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Light Woven Shirt": FF12OpenWorldItemData(
        code=4399,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Silken Shirt": FF12OpenWorldItemData(
        code=4400,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Kilimweave Shirt": FF12OpenWorldItemData(
        code=4401,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Shepherd's Bolero": FF12OpenWorldItemData(
        code=4402,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Wizard's Robes": FF12OpenWorldItemData(
        code=4403,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Chanter's Djellaba": FF12OpenWorldItemData(
        code=4404,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Traveler's Vestment": FF12OpenWorldItemData(
        code=4405,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Mage's Habit": FF12OpenWorldItemData(
        code=4406,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Enchanter's Habit": FF12OpenWorldItemData(
        code=4407,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Sorcerer's Habit": FF12OpenWorldItemData(
        code=4408,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Black Garb": FF12OpenWorldItemData(
        code=4409,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Carmagnole": FF12OpenWorldItemData(
        code=4410,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Maduin Gear": FF12OpenWorldItemData(
        code=4411,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Jade Gown": FF12OpenWorldItemData(
        code=4412,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Gaia Gear": FF12OpenWorldItemData(
        code=4413,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Cleric's Robes": FF12OpenWorldItemData(
        code=4414,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "White Robes": FF12OpenWorldItemData(
        code=4415,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Black Robes": FF12OpenWorldItemData(
        code=4416,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Glimmering Robes": FF12OpenWorldItemData(
        code=4417,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Lordly Robes": FF12OpenWorldItemData(
        code=4418,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Leather Armor": FF12OpenWorldItemData(
        code=4419,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Bronze Armor": FF12OpenWorldItemData(
        code=4420,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Scale Armor": FF12OpenWorldItemData(
        code=4421,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Iron Armor": FF12OpenWorldItemData(
        code=4422,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Linen Cuirass": FF12OpenWorldItemData(
        code=4423,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Chainmail": FF12OpenWorldItemData(
        code=4424,
        classification=ItemClassification.filler,
        category="Armor",
        weight=5
    ),
    "Golden Armor": FF12OpenWorldItemData(
        code=4425,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Shielded Armor": FF12OpenWorldItemData(
        code=4426,
        classification=ItemClassification.filler,
        category="Armor",
        weight=49
    ),
    "Demon Mail": FF12OpenWorldItemData(
        code=4427,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Bone Mail": FF12OpenWorldItemData(
        code=4428,
        classification=ItemClassification.filler,
        category="Armor",
        weight=34
    ),
    "Diamond Armor": FF12OpenWorldItemData(
        code=4429,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Mirror Mail": FF12OpenWorldItemData(
        code=4430,
        classification=ItemClassification.filler,
        category="Armor",
        weight=24
    ),
    "Platinum Armor": FF12OpenWorldItemData(
        code=4431,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Carabineer Mail": FF12OpenWorldItemData(
        code=4432,
        classification=ItemClassification.filler,
        category="Armor",
        weight=17
    ),
    "Dragon Mail": FF12OpenWorldItemData(
        code=4433,
        classification=ItemClassification.filler,
        category="Armor",
        weight=12
    ),
    "Genji Armor": FF12OpenWorldItemData(
        code=4434,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Maximillian": FF12OpenWorldItemData(
        code=4435,
        classification=ItemClassification.filler,
        category="Armor",
        weight=9
    ),
    "Grand Armor": FF12OpenWorldItemData(
        code=4436,
        classification=ItemClassification.filler,
        category="Armor",
        weight=6
    ),
    "Opal Ring": FF12OpenWorldItemData(
        code=4437,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=12
    ),
    "Ruby Ring": FF12OpenWorldItemData(
        code=4438,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=34
    ),
    "Tourmaline Ring": FF12OpenWorldItemData(
        code=4439,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Sage's Ring": FF12OpenWorldItemData(
        code=4440,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Ring of Renewal": FF12OpenWorldItemData(
        code=4441,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=34
    ),
    "Agate Ring": FF12OpenWorldItemData(
        code=4442,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Bangle": FF12OpenWorldItemData(
        code=4443,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=140
    ),
    "Orrachea Armlet": FF12OpenWorldItemData(
        code=4444,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=140
    ),
    "Power Armlet": FF12OpenWorldItemData(
        code=4445,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Argyle Armlet": FF12OpenWorldItemData(
        code=4446,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Diamond Armlet": FF12OpenWorldItemData(
        code=4447,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Amber Armlet": FF12OpenWorldItemData(
        code=4448,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Berserker Bracers": FF12OpenWorldItemData(
        code=4449,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=17
    ),
    "Magick Gloves": FF12OpenWorldItemData(
        code=4450,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Thief's Cuffs": FF12OpenWorldItemData(
        code=4451,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=24
    ),
    "Blazer Gloves": FF12OpenWorldItemData(
        code=4452,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Genji Gloves": FF12OpenWorldItemData(
        code=4453,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=6
    ),
    "Gauntlets": FF12OpenWorldItemData(
        code=4454,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Turtleshell Choker": FF12OpenWorldItemData(
        code=4455,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=34
    ),
    "Nihopalaoa": FF12OpenWorldItemData(
        code=4456,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=9
    ),
    "Embroidered Tippet": FF12OpenWorldItemData(
        code=4457,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=17
    ),
    "Leather Gorget": FF12OpenWorldItemData(
        code=4458,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Jade Collar": FF12OpenWorldItemData(
        code=4459,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Steel Gorget": FF12OpenWorldItemData(
        code=4460,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Rose Corsage": FF12OpenWorldItemData(
        code=4461,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Pheasant Netsuke": FF12OpenWorldItemData(
        code=4462,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=34
    ),
    "Indigo Pendant": FF12OpenWorldItemData(
        code=4463,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=34
    ),
    "Golden Amulet": FF12OpenWorldItemData(
        code=4464,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=17
    ),
    "Bowline Sash": FF12OpenWorldItemData(
        code=4465,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Firefly": FF12OpenWorldItemData(
        code=4466,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=140
    ),
    "Sash": FF12OpenWorldItemData(
        code=4467,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Bubble Belt": FF12OpenWorldItemData(
        code=4468,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=17
    ),
    "Cameo Belt": FF12OpenWorldItemData(
        code=4469,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Nishijin Belt": FF12OpenWorldItemData(
        code=4470,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Black Belt": FF12OpenWorldItemData(
        code=4471,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Battle Harness": FF12OpenWorldItemData(
        code=4472,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Germinas Boots": FF12OpenWorldItemData(
        code=4473,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=24
    ),
    "Hermes Sandals": FF12OpenWorldItemData(
        code=4474,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=17
    ),
    "Gillie Boots": FF12OpenWorldItemData(
        code=4475,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=69
    ),
    "Steel Poleyns": FF12OpenWorldItemData(
        code=4476,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Winged Boots": FF12OpenWorldItemData(
        code=4477,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Quasimodo Boots": FF12OpenWorldItemData(
        code=4478,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=98
    ),
    "Cat-ear Hood": FF12OpenWorldItemData(
        code=4480,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=24
    ),
    "Fuzzy Miter": FF12OpenWorldItemData(
        code=4481,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=49
    ),
    "Ribbon": FF12OpenWorldItemData(
        code=4482,
        classification=ItemClassification.filler,
        category="Accessory",
        weight=6
    ),
    "Onion Arrows": FF12OpenWorldItemData(
        code=4485,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Parallel Arrows": FF12OpenWorldItemData(
        code=4486,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Fiery Arrows": FF12OpenWorldItemData(
        code=4487,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Bamboo Arrows": FF12OpenWorldItemData(
        code=4488,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Lightning Arrows": FF12OpenWorldItemData(
        code=4489,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Assassin's Arrows": FF12OpenWorldItemData(
        code=4490,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Icecloud Arrows": FF12OpenWorldItemData(
        code=4491,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Artemis Arrows": FF12OpenWorldItemData(
        code=4492,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Onion Bolts": FF12OpenWorldItemData(
        code=4493,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Long Bolts": FF12OpenWorldItemData(
        code=4494,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Stone Bolts": FF12OpenWorldItemData(
        code=4495,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Lead Bolts": FF12OpenWorldItemData(
        code=4496,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Black Bolts": FF12OpenWorldItemData(
        code=4497,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Time Bolts": FF12OpenWorldItemData(
        code=4498,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Sapping Bolts": FF12OpenWorldItemData(
        code=4499,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Grand Bolts": FF12OpenWorldItemData(
        code=4500,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Onion Shot": FF12OpenWorldItemData(
        code=4501,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Silent Shot": FF12OpenWorldItemData(
        code=4502,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Aqua Shot": FF12OpenWorldItemData(
        code=4503,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Wyrmfire Shot": FF12OpenWorldItemData(
        code=4504,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Mud Shot": FF12OpenWorldItemData(
        code=4505,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=5
    ),
    "Windslicer Shot": FF12OpenWorldItemData(
        code=4506,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Dark Shot": FF12OpenWorldItemData(
        code=4507,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Stone Shot": FF12OpenWorldItemData(
        code=4508,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Onion Bombs": FF12OpenWorldItemData(
        code=4509,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=49
    ),
    "Poison Bombs": FF12OpenWorldItemData(
        code=4510,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Stun Bombs": FF12OpenWorldItemData(
        code=4511,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Oil Bombs": FF12OpenWorldItemData(
        code=4512,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=24
    ),
    "Chaos Bombs": FF12OpenWorldItemData(
        code=4513,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=17
    ),
    "Stink Bombs": FF12OpenWorldItemData(
        code=4514,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=34
    ),
    "Water Bombs": FF12OpenWorldItemData(
        code=4515,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=12
    ),
    "Castellanos": FF12OpenWorldItemData(
        code=4516,
        classification=ItemClassification.filler,
        category="Weapon",
        weight=9
    ),
    "Cure": FF12OpenWorldItemData(
        code=12289,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blindna": FF12OpenWorldItemData(
        code=12290,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Vox": FF12OpenWorldItemData(
        code=12291,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Poisona": FF12OpenWorldItemData(
        code=12292,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Cura": FF12OpenWorldItemData(
        code=12293,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Raise": FF12OpenWorldItemData(
        code=12294,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Curaga": FF12OpenWorldItemData(
        code=12295,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Stona": FF12OpenWorldItemData(
        code=12296,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Regen": FF12OpenWorldItemData(
        code=12297,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Cleanse": FF12OpenWorldItemData(
        code=12298,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Esuna": FF12OpenWorldItemData(
        code=12299,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Curaja": FF12OpenWorldItemData(
        code=12300,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Dispel": FF12OpenWorldItemData(
        code=12301,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Dispelga": FF12OpenWorldItemData(
        code=12302,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Renew": FF12OpenWorldItemData(
        code=12303,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Arise": FF12OpenWorldItemData(
        code=12304,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Esunaga": FF12OpenWorldItemData(
        code=12305,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Holy": FF12OpenWorldItemData(
        code=12306,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Fire": FF12OpenWorldItemData(
        code=12307,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Thunder": FF12OpenWorldItemData(
        code=12308,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blizzard": FF12OpenWorldItemData(
        code=12309,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Aqua": FF12OpenWorldItemData(
        code=12310,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Aero": FF12OpenWorldItemData(
        code=12311,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Fira": FF12OpenWorldItemData(
        code=12312,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Thundara": FF12OpenWorldItemData(
        code=12313,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blizzara": FF12OpenWorldItemData(
        code=12314,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Bio": FF12OpenWorldItemData(
        code=12315,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Aeroga": FF12OpenWorldItemData(
        code=12316,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Firaga": FF12OpenWorldItemData(
        code=12317,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Thundaga": FF12OpenWorldItemData(
        code=12318,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blizzaga": FF12OpenWorldItemData(
        code=12319,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Shock": FF12OpenWorldItemData(
        code=12320,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Scourge": FF12OpenWorldItemData(
        code=12321,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Flare": FF12OpenWorldItemData(
        code=12322,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Ardor": FF12OpenWorldItemData(
        code=12323,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Scathe": FF12OpenWorldItemData(
        code=12324,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Haste": FF12OpenWorldItemData(
        code=12325,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Float": FF12OpenWorldItemData(
        code=12326,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Hastega": FF12OpenWorldItemData(
        code=12327,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Slow": FF12OpenWorldItemData(
        code=12328,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Immobilize": FF12OpenWorldItemData(
        code=12329,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Disable": FF12OpenWorldItemData(
        code=12330,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Bleed": FF12OpenWorldItemData(
        code=12331,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Break": FF12OpenWorldItemData(
        code=12332,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Stop": FF12OpenWorldItemData(
        code=12333,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Slowga": FF12OpenWorldItemData(
        code=12334,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Countdown": FF12OpenWorldItemData(
        code=12335,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Reflect": FF12OpenWorldItemData(
        code=12336,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Reflectga": FF12OpenWorldItemData(
        code=12337,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Balance": FF12OpenWorldItemData(
        code=12338,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Warp": FF12OpenWorldItemData(
        code=12339,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Protect": FF12OpenWorldItemData(
        code=12340,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Shell": FF12OpenWorldItemData(
        code=12341,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Bravery": FF12OpenWorldItemData(
        code=12342,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Faith": FF12OpenWorldItemData(
        code=12343,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Protectga": FF12OpenWorldItemData(
        code=12344,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Shellga": FF12OpenWorldItemData(
        code=12345,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blind": FF12OpenWorldItemData(
        code=12346,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Oil": FF12OpenWorldItemData(
        code=12347,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Poison": FF12OpenWorldItemData(
        code=12348,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Silence": FF12OpenWorldItemData(
        code=12349,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Sleep": FF12OpenWorldItemData(
        code=12350,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Blindga": FF12OpenWorldItemData(
        code=12351,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Toxify": FF12OpenWorldItemData(
        code=12352,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Silencega": FF12OpenWorldItemData(
        code=12353,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Sleepga": FF12OpenWorldItemData(
        code=12354,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Reverse": FF12OpenWorldItemData(
        code=12355,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Berserk": FF12OpenWorldItemData(
        code=12356,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Death": FF12OpenWorldItemData(
        code=12357,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Confuse": FF12OpenWorldItemData(
        code=12358,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Decoy": FF12OpenWorldItemData(
        code=12359,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Vanish": FF12OpenWorldItemData(
        code=12360,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Vanishga": FF12OpenWorldItemData(
        code=12361,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Drain": FF12OpenWorldItemData(
        code=12362,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Syphon": FF12OpenWorldItemData(
        code=12363,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Bubble": FF12OpenWorldItemData(
        code=12364,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Dark": FF12OpenWorldItemData(
        code=12365,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Darkra": FF12OpenWorldItemData(
        code=12366,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Darkga": FF12OpenWorldItemData(
        code=12367,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Gravity": FF12OpenWorldItemData(
        code=12368,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Graviga": FF12OpenWorldItemData(
        code=12369,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "First Aid": FF12OpenWorldItemData(
        code=16385,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Shades of Black": FF12OpenWorldItemData(
        code=16386,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Horology": FF12OpenWorldItemData(
        code=16387,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Stamp": FF12OpenWorldItemData(
        code=16388,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Achilles": FF12OpenWorldItemData(
        code=16389,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Charge": FF12OpenWorldItemData(
        code=16390,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Infuse": FF12OpenWorldItemData(
        code=16391,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Souleater": FF12OpenWorldItemData(
        code=16392,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Wither": FF12OpenWorldItemData(
        code=16393,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Addle": FF12OpenWorldItemData(
        code=16394,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Bonecrusher": FF12OpenWorldItemData(
        code=16395,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Steal": FF12OpenWorldItemData(
        code=16396,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Telekinesis": FF12OpenWorldItemData(
        code=16397,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Expose": FF12OpenWorldItemData(
        code=16398,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Shear": FF12OpenWorldItemData(
        code=16399,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Charm": FF12OpenWorldItemData(
        code=16400,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Revive": FF12OpenWorldItemData(
        code=16401,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Sight Unseeing": FF12OpenWorldItemData(
        code=16402,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Numerology": FF12OpenWorldItemData(
        code=16403,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Libra": FF12OpenWorldItemData(
        code=16404,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Poach": FF12OpenWorldItemData(
        code=16405,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "1000 Needles": FF12OpenWorldItemData(
        code=16406,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Traveler": FF12OpenWorldItemData(
        code=16407,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Gil Toss": FF12OpenWorldItemData(
        code=16408,
        classification=ItemClassification.useful,
        category="Ability"
    ),
    "Teleport Stone": FF12OpenWorldItemData(
        code=8193,
        classification=ItemClassification.filler,
        category="Item",
        weight=400
    ),
    "Earth Stone": FF12OpenWorldItemData(
        code=8225,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wind Stone": FF12OpenWorldItemData(
        code=8226,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Water Stone": FF12OpenWorldItemData(
        code=8227,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Fire Stone": FF12OpenWorldItemData(
        code=8228,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ice Stone": FF12OpenWorldItemData(
        code=8229,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Storm Stone": FF12OpenWorldItemData(
        code=8230,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Holy Stone": FF12OpenWorldItemData(
        code=8231,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Dark Stone": FF12OpenWorldItemData(
        code=8232,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Earth Magicite": FF12OpenWorldItemData(
        code=8233,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wind Magicite": FF12OpenWorldItemData(
        code=8234,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Water Magicite": FF12OpenWorldItemData(
        code=8235,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Fire Magicite": FF12OpenWorldItemData(
        code=8236,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ice Magicite": FF12OpenWorldItemData(
        code=8237,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Storm Magicite": FF12OpenWorldItemData(
        code=8238,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Holy Magicite": FF12OpenWorldItemData(
        code=8239,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Dark Magicite": FF12OpenWorldItemData(
        code=8240,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Earth Crystal": FF12OpenWorldItemData(
        code=8241,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wind Crystal": FF12OpenWorldItemData(
        code=8242,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Water Crystal": FF12OpenWorldItemData(
        code=8243,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Fire Crystal": FF12OpenWorldItemData(
        code=8244,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ice Crystal": FF12OpenWorldItemData(
        code=8245,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Storm Crystal": FF12OpenWorldItemData(
        code=8246,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Holy Crystal": FF12OpenWorldItemData(
        code=8247,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Dark Crystal": FF12OpenWorldItemData(
        code=8248,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Aries Gem": FF12OpenWorldItemData(
        code=8249,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Taurus Gem": FF12OpenWorldItemData(
        code=8250,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Gemini Gem": FF12OpenWorldItemData(
        code=8251,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Cancer Gem": FF12OpenWorldItemData(
        code=8252,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Leo Gem": FF12OpenWorldItemData(
        code=8253,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Virgo Gem": FF12OpenWorldItemData(
        code=8254,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Libra Gem": FF12OpenWorldItemData(
        code=8255,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Scorpio Gem": FF12OpenWorldItemData(
        code=8256,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sagittarius Gem": FF12OpenWorldItemData(
        code=8257,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Capricorn Gem": FF12OpenWorldItemData(
        code=8258,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Aquarius Gem": FF12OpenWorldItemData(
        code=8259,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Pisces Gem": FF12OpenWorldItemData(
        code=8260,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Salamand Halcyon": FF12OpenWorldItemData(
        code=8261,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Mardu Halcyon": FF12OpenWorldItemData(
        code=8262,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Leshach Halcyon": FF12OpenWorldItemData(
        code=8263,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Gnoma Halcyon": FF12OpenWorldItemData(
        code=8264,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Undin Halcyon": FF12OpenWorldItemData(
        code=8265,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sylphi Halcyon": FF12OpenWorldItemData(
        code=8266,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Diakon Halcyon": FF12OpenWorldItemData(
        code=8267,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Leamonde Halcyon": FF12OpenWorldItemData(
        code=8268,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Arcana": FF12OpenWorldItemData(
        code=8269,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "High Arcana": FF12OpenWorldItemData(
        code=8270,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Turtle Shell": FF12OpenWorldItemData(
        code=8271,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Aged Turtle Shell": FF12OpenWorldItemData(
        code=8272,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ancient Turtle Shell": FF12OpenWorldItemData(
        code=8273,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Molting": FF12OpenWorldItemData(
        code=8274,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Iron Carapace": FF12OpenWorldItemData(
        code=8275,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wyrm Carapace": FF12OpenWorldItemData(
        code=8276,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Insect Husk": FF12OpenWorldItemData(
        code=8277,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Battlewyrm Carapace": FF12OpenWorldItemData(
        code=8278,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Destrier Barding": FF12OpenWorldItemData(
        code=8279,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Charger Barding": FF12OpenWorldItemData(
        code=8280,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Fish Scale": FF12OpenWorldItemData(
        code=8281,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Yensa Scale": FF12OpenWorldItemData(
        code=8282,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ichthon Scale": FF12OpenWorldItemData(
        code=8283,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ring Wyrm Scale": FF12OpenWorldItemData(
        code=8284,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Drab Wool": FF12OpenWorldItemData(
        code=8285,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Braid Wool": FF12OpenWorldItemData(
        code=8286,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Fine Wool": FF12OpenWorldItemData(
        code=8287,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Blood Wool": FF12OpenWorldItemData(
        code=8288,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Rat Pelt": FF12OpenWorldItemData(
        code=8289,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Snake Skin": FF12OpenWorldItemData(
        code=8290,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tyrant Hide": FF12OpenWorldItemData(
        code=8291,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Quality Hide": FF12OpenWorldItemData(
        code=8292,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Beastlord Hide": FF12OpenWorldItemData(
        code=8293,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tanned Hide": FF12OpenWorldItemData(
        code=8294,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tanned Giantskin": FF12OpenWorldItemData(
        code=8295,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tanned Tyrant Hide": FF12OpenWorldItemData(
        code=8296,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Prime Tanned Hide": FF12OpenWorldItemData(
        code=8297,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wolf Pelt": FF12OpenWorldItemData(
        code=8298,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Coeurl Pelt": FF12OpenWorldItemData(
        code=8299,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Quality Pelt": FF12OpenWorldItemData(
        code=8300,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Prime Pelt": FF12OpenWorldItemData(
        code=8301,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Small Feather": FF12OpenWorldItemData(
        code=8302,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Large Feather": FF12OpenWorldItemData(
        code=8303,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Chocobo Feather": FF12OpenWorldItemData(
        code=8304,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Giant Feather": FF12OpenWorldItemData(
        code=8305,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bundle of Feathers": FF12OpenWorldItemData(
        code=8306,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Windslicer Pinion": FF12OpenWorldItemData(
        code=8307,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Horn": FF12OpenWorldItemData(
        code=8308,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Pointed Horn": FF12OpenWorldItemData(
        code=8309,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Solid Horn": FF12OpenWorldItemData(
        code=8310,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bat Fang": FF12OpenWorldItemData(
        code=8311,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Crooked Fang": FF12OpenWorldItemData(
        code=8312,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Spiral Incisor": FF12OpenWorldItemData(
        code=8313,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wyvern Fang": FF12OpenWorldItemData(
        code=8314,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Cactus Fruit": FF12OpenWorldItemData(
        code=8315,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Succulent Fruit": FF12OpenWorldItemData(
        code=8316,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Screamroot": FF12OpenWorldItemData(
        code=8317,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Malboro Vine": FF12OpenWorldItemData(
        code=8318,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Malboro Fruit": FF12OpenWorldItemData(
        code=8319,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Malboro Flower": FF12OpenWorldItemData(
        code=8320,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bone Fragment": FF12OpenWorldItemData(
        code=8321,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sturdy Bone": FF12OpenWorldItemData(
        code=8322,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Blood-darkened Bone": FF12OpenWorldItemData(
        code=8323,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Lumber": FF12OpenWorldItemData(
        code=8324,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Quality Lumber": FF12OpenWorldItemData(
        code=8325,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Solid Stone": FF12OpenWorldItemData(
        code=8326,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Quality Stone": FF12OpenWorldItemData(
        code=8327,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Iron Scraps": FF12OpenWorldItemData(
        code=8328,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Iron Ore": FF12OpenWorldItemData(
        code=8329,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Green Liquid": FF12OpenWorldItemData(
        code=8330,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Yellow Liquid": FF12OpenWorldItemData(
        code=8331,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Silver Liquid": FF12OpenWorldItemData(
        code=8332,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Glass Jewel": FF12OpenWorldItemData(
        code=8333,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sky Jewel": FF12OpenWorldItemData(
        code=8334,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Demon Eyeball": FF12OpenWorldItemData(
        code=8335,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Demon Feather": FF12OpenWorldItemData(
        code=8336,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Demon Tail": FF12OpenWorldItemData(
        code=8337,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Grimoire Togail": FF12OpenWorldItemData(
        code=8338,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Grimoire Aidhed": FF12OpenWorldItemData(
        code=8339,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bomb Ashes": FF12OpenWorldItemData(
        code=8340,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bomb Shell": FF12OpenWorldItemData(
        code=8341,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Book of Orgain": FF12OpenWorldItemData(
        code=8342,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Book of Orgain-Cent": FF12OpenWorldItemData(
        code=8343,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Book of Orgain-Mille": FF12OpenWorldItemData(
        code=8344,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Foul Flesh": FF12OpenWorldItemData(
        code=8345,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Festering Flesh": FF12OpenWorldItemData(
        code=8346,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Maggoty Flesh": FF12OpenWorldItemData(
        code=8347,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Forbidden Flesh": FF12OpenWorldItemData(
        code=8348,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Feystone": FF12OpenWorldItemData(
        code=8349,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Pebble": FF12OpenWorldItemData(
        code=8350,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Broken Sword": FF12OpenWorldItemData(
        code=8351,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Broken Greataxe": FF12OpenWorldItemData(
        code=8352,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Broken Spear": FF12OpenWorldItemData(
        code=8353,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bent Staff": FF12OpenWorldItemData(
        code=8354,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Moon Ring": FF12OpenWorldItemData(
        code=8355,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bundle of Needles": FF12OpenWorldItemData(
        code=8356,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Coeurl Whisker": FF12OpenWorldItemData(
        code=8357,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Mallet": FF12OpenWorldItemData(
        code=8358,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tattered Garment": FF12OpenWorldItemData(
        code=8359,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Split Armor": FF12OpenWorldItemData(
        code=8360,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Chimera Head": FF12OpenWorldItemData(
        code=8361,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Rat Tail": FF12OpenWorldItemData(
        code=8362,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Slaven Harness": FF12OpenWorldItemData(
        code=8363,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Blood-stained Necklace": FF12OpenWorldItemData(
        code=8364,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Destrier Mane": FF12OpenWorldItemData(
        code=8365,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wargod's Band": FF12OpenWorldItemData(
        code=8366,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Soul of Thamasa": FF12OpenWorldItemData(
        code=8367,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Beastlord Horn": FF12OpenWorldItemData(
        code=8368,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Vampyr Fang": FF12OpenWorldItemData(
        code=8369,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Great Serpent's Fang": FF12OpenWorldItemData(
        code=8370,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Death's-Head": FF12OpenWorldItemData(
        code=8371,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ancient Bone": FF12OpenWorldItemData(
        code=8372,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wyrm Bone": FF12OpenWorldItemData(
        code=8373,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tyrant Bone": FF12OpenWorldItemData(
        code=8374,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Mirror Scale": FF12OpenWorldItemData(
        code=8375,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Emperor Scale": FF12OpenWorldItemData(
        code=8376,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Mythril": FF12OpenWorldItemData(
        code=8377,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Adamantite": FF12OpenWorldItemData(
        code=8378,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Scarletite": FF12OpenWorldItemData(
        code=8379,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Damascus Steel": FF12OpenWorldItemData(
        code=8380,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Orichalcum": FF12OpenWorldItemData(
        code=8381,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Mystletainn": FF12OpenWorldItemData(
        code=8382,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Einherjarium": FF12OpenWorldItemData(
        code=8383,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Electrum": FF12OpenWorldItemData(
        code=8384,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Dorsal Fin": FF12OpenWorldItemData(
        code=8385,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Yensa Fin": FF12OpenWorldItemData(
        code=8386,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ring Wyrm Liver": FF12OpenWorldItemData(
        code=8387,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Eye of the Hawk": FF12OpenWorldItemData(
        code=8388,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Serpent Eye": FF12OpenWorldItemData(
        code=8389,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ambrosia": FF12OpenWorldItemData(
        code=8390,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Foul Liquid": FF12OpenWorldItemData(
        code=8391,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Putrid Liquid": FF12OpenWorldItemData(
        code=8392,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Caramel": FF12OpenWorldItemData(
        code=8393,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Slime Oil": FF12OpenWorldItemData(
        code=8394,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Unpurified Ether": FF12OpenWorldItemData(
        code=8395,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Demon Drink": FF12OpenWorldItemData(
        code=8396,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Death Powder": FF12OpenWorldItemData(
        code=8397,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Soul Powder": FF12OpenWorldItemData(
        code=8398,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Zombie Powder": FF12OpenWorldItemData(
        code=8399,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Snowfly": FF12OpenWorldItemData(
        code=8400,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Corpse Fly": FF12OpenWorldItemData(
        code=8401,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bat Wing": FF12OpenWorldItemData(
        code=8402,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wyvern Wing": FF12OpenWorldItemData(
        code=8403,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Bomb Fragment": FF12OpenWorldItemData(
        code=8404,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Throat Wolf Blood": FF12OpenWorldItemData(
        code=8405,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Frogspawn": FF12OpenWorldItemData(
        code=8406,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Frog Oil": FF12OpenWorldItemData(
        code=8407,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Behemoth Steak": FF12OpenWorldItemData(
        code=8408,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Gysahl Greens": FF12OpenWorldItemData(
        code=8409,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "White Incense": FF12OpenWorldItemData(
        code=8410,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Antarctic Wind": FF12OpenWorldItemData(
        code=8411,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Arctic Wind": FF12OpenWorldItemData(
        code=8412,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Wrath of the Gods": FF12OpenWorldItemData(
        code=8413,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Charged Gizzard": FF12OpenWorldItemData(
        code=8414,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Lifewick": FF12OpenWorldItemData(
        code=8415,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Ketu Board": FF12OpenWorldItemData(
        code=8416,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Magick Lamp": FF12OpenWorldItemData(
        code=8417,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Hell-Gate's Flame": FF12OpenWorldItemData(
        code=8418,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sickle-Blade": FF12OpenWorldItemData(
        code=8419,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Stardust": FF12OpenWorldItemData(
        code=8420,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Moondust": FF12OpenWorldItemData(
        code=8421,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Rainbow Egg": FF12OpenWorldItemData(
        code=8422,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Four-leaf Clover": FF12OpenWorldItemData(
        code=8423,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Gimble Stalk": FF12OpenWorldItemData(
        code=8424,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Onion": FF12OpenWorldItemData(
        code=8425,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Jack-o'-Lantern": FF12OpenWorldItemData(
        code=8426,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Tomato Stalk": FF12OpenWorldItemData(
        code=8427,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Demon's Sigh": FF12OpenWorldItemData(
        code=8428,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Omega Badge": FF12OpenWorldItemData(
        code=8429,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Empyreal Soul": FF12OpenWorldItemData(
        code=8430,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Serpentarius": FF12OpenWorldItemData(
        code=8431,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Gemsteel": FF12OpenWorldItemData(
        code=8432,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Centurio Hero's Badge": FF12OpenWorldItemData(
        code=8433,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Horakhty's Flame": FF12OpenWorldItemData(
        code=8434,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Phobos Glaze": FF12OpenWorldItemData(
        code=8435,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Deimos Clay": FF12OpenWorldItemData(
        code=8436,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Godslayer's Badge": FF12OpenWorldItemData(
        code=8437,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Lu Shang's Badge": FF12OpenWorldItemData(
        code=8438,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Empty Bottle": FF12OpenWorldItemData(
        code=8449,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Common Fish": FF12OpenWorldItemData(
        code=8450,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Delicious Fish": FF12OpenWorldItemData(
        code=8451,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Nebra Succulent": FF12OpenWorldItemData(
        code=8452,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Peach Tuft": FF12OpenWorldItemData(
        code=8453,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Green Tuft": FF12OpenWorldItemData(
        code=8454,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Orange Tuft": FF12OpenWorldItemData(
        code=8455,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Brown Tuft": FF12OpenWorldItemData(
        code=8456,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "White Tuft": FF12OpenWorldItemData(
        code=8457,
        classification=ItemClassification.filler,
        category="Loot",
        weight=10
    ),
    "Sandalwood Chop": FF12OpenWorldItemData(
        code=8467,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Pinewood Chop": FF12OpenWorldItemData(
        code=8468,
        classification=ItemClassification.progression_skip_balancing,
        category="Key",
        duplicateAmount=28
    ),
    "Black Orb": FF12OpenWorldItemData(
        code=8471,
        classification=ItemClassification.progression_skip_balancing,
        category="Key",
        duplicateAmount=24
    ),
    "Systems Access Key": FF12OpenWorldItemData(
        code=8473,
        classification=ItemClassification.progression_skip_balancing,
        category="Key",
        duplicateAmount=3
    ),
    "Writ of Transit": FF12OpenWorldItemData(
        code=32881,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Clan Primer": FF12OpenWorldItemData(
        code=32882,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Cactus Flower": FF12OpenWorldItemData(
        code=32884,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Tube Fuse": FF12OpenWorldItemData(
        code=32885,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Sword of the Order": FF12OpenWorldItemData(
        code=32886,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "No. 1 Brig Key": FF12OpenWorldItemData(
        code=32887,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Dawn Shard": FF12OpenWorldItemData(
        code=32889,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Shadestone": FF12OpenWorldItemData(
        code=32890,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Sunstone": FF12OpenWorldItemData(
        code=32891,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Ring of the Toad": FF12OpenWorldItemData(
        code=32893,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Silent Urn": FF12OpenWorldItemData(
        code=32894,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Site 3 Key": FF12OpenWorldItemData(
        code=32895,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Site 11 Key": FF12OpenWorldItemData(
        code=32896,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Crescent Stone": FF12OpenWorldItemData(
        code=32897,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Medallion of Bravery": FF12OpenWorldItemData(
        code=32898,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Medallion of Might": FF12OpenWorldItemData(
        code=32899,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Medallion of Love": FF12OpenWorldItemData(
        code=32900,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Lusterless Medallion": FF12OpenWorldItemData(
        code=32901,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Stone of the Condemner": FF12OpenWorldItemData(
        code=32902,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Errmonea Leaf": FF12OpenWorldItemData(
        code=32903,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Rabbit's Tail": FF12OpenWorldItemData(
        code=32904,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Ann's Letter": FF12OpenWorldItemData(
        code=32905,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Manufacted Nethicite": FF12OpenWorldItemData(
        code=32906,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Rusted Scrap of Armor": FF12OpenWorldItemData(
        code=32907,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Sword of Kings": FF12OpenWorldItemData(
        code=32908,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Treaty-Blade": FF12OpenWorldItemData(
        code=32909,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Dusty Letter": FF12OpenWorldItemData(
        code=32910,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Serpentwyne Must": FF12OpenWorldItemData(
        code=32911,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Dull Fragment": FF12OpenWorldItemData(
        code=32912,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Blackened Fragment": FF12OpenWorldItemData(
        code=32913,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Grimy Fragment": FF12OpenWorldItemData(
        code=32914,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Stolen Articles": FF12OpenWorldItemData(
        code=32915,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Barheim Key": FF12OpenWorldItemData(
        code=32916,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Merchant's Armband": FF12OpenWorldItemData(
        code=32921,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Pilika's Diary": FF12OpenWorldItemData(
        code=32922,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Ring of the Light": FF12OpenWorldItemData(
        code=32923,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Viera Rucksack": FF12OpenWorldItemData(
        code=32924,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Lab Access Card": FF12OpenWorldItemData(
        code=32927,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Moonsilver Medallion": FF12OpenWorldItemData(
        code=32932,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Goddess's Magicite": FF12OpenWorldItemData(
        code=32941,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Broken Key": FF12OpenWorldItemData(
        code=32943,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Sluice Gate Key": FF12OpenWorldItemData(
        code=32944,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Wind Globe": FF12OpenWorldItemData(
        code=32946,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Windvane": FF12OpenWorldItemData(
        code=32947,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Dragon Scale": FF12OpenWorldItemData(
        code=32949,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Ageworn Key": FF12OpenWorldItemData(
        code=32950,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Soul Ward Key": FF12OpenWorldItemData(
        code=32951,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Lente's Tear": FF12OpenWorldItemData(
        code=32952,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Shelled Trophy": FF12OpenWorldItemData(
        code=32953,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fur-scaled Trophy": FF12OpenWorldItemData(
        code=32954,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Bony Trophy": FF12OpenWorldItemData(
        code=32955,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Fanged Trophy": FF12OpenWorldItemData(
        code=32956,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Hide-covered Trophy": FF12OpenWorldItemData(
        code=32957,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Maned Trophy": FF12OpenWorldItemData(
        code=32958,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Fell Trophy": FF12OpenWorldItemData(
        code=32959,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Accursed Trophy": FF12OpenWorldItemData(
        code=32960,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Beaked Trophy": FF12OpenWorldItemData(
        code=32961,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Maverick Trophy": FF12OpenWorldItemData(
        code=32962,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Soulless Trophy": FF12OpenWorldItemData(
        code=32963,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Leathern Trophy": FF12OpenWorldItemData(
        code=32964,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Sickle Trophy": FF12OpenWorldItemData(
        code=32965,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Vengeful Trophy": FF12OpenWorldItemData(
        code=32966,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Gravesoil Trophy": FF12OpenWorldItemData(
        code=32967,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Metallic Trophy": FF12OpenWorldItemData(
        code=32968,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Slimy Trophy": FF12OpenWorldItemData(
        code=32969,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Scythe Trophy": FF12OpenWorldItemData(
        code=32970,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Feathered Trophy": FF12OpenWorldItemData(
        code=32971,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Skull Trophy": FF12OpenWorldItemData(
        code=32972,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Mind Trophy": FF12OpenWorldItemData(
        code=32973,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Eternal Trophy": FF12OpenWorldItemData(
        code=32974,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Clawed Trophy": FF12OpenWorldItemData(
        code=32975,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Odiferous Trophy": FF12OpenWorldItemData(
        code=32976,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Whiskered Trophy": FF12OpenWorldItemData(
        code=32977,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Frigid Trophy": FF12OpenWorldItemData(
        code=32978,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Ensanguined Trophy": FF12OpenWorldItemData(
        code=32979,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Cruel Trophy": FF12OpenWorldItemData(
        code=32980,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Adamantine Trophy": FF12OpenWorldItemData(
        code=32981,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Reptilian Trophy": FF12OpenWorldItemData(
        code=32982,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Vile Trophy": FF12OpenWorldItemData(
        code=32983,
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Rainstone": FF12OpenWorldItemData(
        code=32993,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Rabanastre Aeropass": FF12OpenWorldItemData(
        code=32994,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Nalbina Aeropass": FF12OpenWorldItemData(
        code=32995,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Bhujerba Aeropass": FF12OpenWorldItemData(
        code=32996,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Archades Aeropass": FF12OpenWorldItemData(
        code=32997,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Balfonheim Aeropass": FF12OpenWorldItemData(
        code=32998,
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Belias": FF12OpenWorldItemData(
        code=49171,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Mateus": FF12OpenWorldItemData(
        code=49172,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Adrammelech": FF12OpenWorldItemData(
        code=49173,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Hashmal": FF12OpenWorldItemData(
        code=49174,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Cuchulainn": FF12OpenWorldItemData(
        code=49175,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Famfrit": FF12OpenWorldItemData(
        code=49176,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Zalera": FF12OpenWorldItemData(
        code=49177,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Shemhazai": FF12OpenWorldItemData(
        code=49178,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Chaos": FF12OpenWorldItemData(
        code=49179,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Zeromus": FF12OpenWorldItemData(
        code=49180,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Exodus": FF12OpenWorldItemData(
        code=49181,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Ultima": FF12OpenWorldItemData(
        code=49182,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Zodiark": FF12OpenWorldItemData(
        code=49183,
        classification=ItemClassification.progression,
        category="Esper"
    ),
    "Second Board": FF12OpenWorldItemData(
        code=49184,
        classification=ItemClassification.progression,
        category="Board"
    ),
    "1 Gil": FF12OpenWorldItemData(
        code=98305,
        classification=ItemClassification.filler,
        category="Gil",
        weight=250,
        duplicateAmount=0
    ),
    "500 Gil": FF12OpenWorldItemData(
        code=98306,
        classification=ItemClassification.filler,
        category="Gil",
        weight=900,
        amount=500,
        duplicateAmount=0
    ),
    "1000 Gil": FF12OpenWorldItemData(
        code=98307,
        classification=ItemClassification.filler,
        category="Gil",
        weight=1150,
        amount=1000,
        duplicateAmount=0
    ),
    "5000 Gil": FF12OpenWorldItemData(
        code=98308,
        classification=ItemClassification.filler,
        category="Gil",
        weight=800,
        amount=5000,
        duplicateAmount=0
    ),
    "10000 Gil": FF12OpenWorldItemData(
        code=98309,
        classification=ItemClassification.filler,
        category="Gil",
        weight=500,
        amount=10000,
        duplicateAmount=0
    ),
    "25000 Gil": FF12OpenWorldItemData(
        code=98310,
        classification=ItemClassification.filler,
        category="Gil",
        weight=200,
        amount=25000,
        duplicateAmount=0
    ),
}

item_table = {name: data.code for name, data in item_data_table.items()}
inv_item_table = {data.code: name for name, data in item_data_table.items()}

filler_items = [name for name, data in item_data_table.items()
                if data.classification == ItemClassification.filler and data.weight > 0]
filler_weights = [item_data_table[name].weight for name in filler_items]
