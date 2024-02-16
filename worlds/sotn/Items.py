from typing import Optional
from enum import Enum
from BaseClasses import ItemClassification, Item

base_item_id = 127000000
tile_id_offset = 0X80


class IType(Enum):
    HEART = 0
    GOLD = 1
    SUBWEAPON = 2
    POWERUP = 3
    WEAPON1 = 4
    WEAPON2 = 5
    SHIELD = 6
    HELMET = 7
    ARMOR = 8
    CLOAK = 9
    ACCESSORY = 10
    USABLE = 11
    RELIC = 12
    EVENT = 13


def is_relic(item):
    if isinstance(item, SotnItem):
        if item.name in relic_table:
            return True
    return False


class SotnItem(Item):
    game: str = "Symphony of the Night"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)


class ItemData:
    def __init__(self, index: int, item_type: IType, ic: ItemClassification = ItemClassification.filler):
        self.index = None if index is None else index + base_item_id
        self.type = item_type
        self.ic = ic

    def get_item_id_no_offset(self):
        return self.index - base_item_id

    def get_item_id(self):
        if self.type == IType.RELIC:
            return self.index - base_item_id - 300
        if self.type == IType.POWERUP or self.type == IType.GOLD:
            return self.index - base_item_id - 400
        return self.index - base_item_id + tile_id_offset

    def get_item_type(self):
        return self.type

    def get_item_classification(self):
        return self.ic


hand_type_table = {
    "Monster vial 1": ItemData(1, IType.USABLE),
    "Monster vial 2": ItemData(2, IType.USABLE),
    "Monster vial 3": ItemData(3, IType.USABLE),
    "Shield rod": ItemData(4, IType.WEAPON1),
    "Leather shield": ItemData(5, IType.SHIELD),
    "Knight shield": ItemData(6, IType.SHIELD),
    "Iron shield": ItemData(7, IType.SHIELD),
    "AxeLord shield": ItemData(8, IType.SHIELD),
    "Herald shield": ItemData(9, IType.SHIELD),
    "Dark shield": ItemData(10, IType.SHIELD),
    "Goddess shield": ItemData(11, IType.SHIELD),
    "Shaman shield": ItemData(12, IType.SHIELD),
    "Medusa shield": ItemData(13, IType.SHIELD),
    "Skull shield": ItemData(14, IType.SHIELD),
    "Fire shield": ItemData(15, IType.SHIELD),
    "Alucard shield": ItemData(16, IType.SHIELD),
    "Sword of dawn": ItemData(17, IType.WEAPON2),
    "Basilard": ItemData(18, IType.WEAPON1),
    "Short sword": ItemData(19, IType.WEAPON1),
    "Combat knife": ItemData(20, IType.WEAPON1),
    "Nunchaku": ItemData(21, IType.WEAPON2),
    "Were bane": ItemData(22, IType.WEAPON1),
    "Rapier": ItemData(23, IType.WEAPON1),
    "Karma coin": ItemData(24, IType.USABLE),
    "Magic missile": ItemData(25, IType.USABLE),
    "Red rust": ItemData(26, IType.WEAPON2),
    "Takemitsu": ItemData(27, IType.WEAPON2),
    "Shotel": ItemData(28, IType.WEAPON1),
    "Orange": ItemData(29, IType.USABLE),
    "Apple": ItemData(30, IType.USABLE),
    "Banana": ItemData(31, IType.USABLE),
    "Grapes": ItemData(32, IType.USABLE),
    "Strawberry": ItemData(33, IType.USABLE),
    "Pineapple": ItemData(34, IType.USABLE),
    "Peanuts": ItemData(35, IType.USABLE),
    "Toadstool": ItemData(36, IType.USABLE),
    "Shiitake": ItemData(37, IType.USABLE),
    "Cheesecake": ItemData(38, IType.USABLE),
    "Shortcake": ItemData(39, IType.USABLE),
    "Tart": ItemData(40, IType.USABLE),
    "Parfait": ItemData(41, IType.USABLE),
    "Pudding": ItemData(42, IType.USABLE),
    "Ice cream": ItemData(43, IType.USABLE),
    "Frankfurter": ItemData(44, IType.USABLE),
    "Hamburger": ItemData(45, IType.USABLE),
    "Pizza": ItemData(46, IType.USABLE),
    "Cheese": ItemData(47, IType.USABLE),
    "Ham and eggs": ItemData(48, IType.USABLE),
    "Omelette": ItemData(49, IType.USABLE),
    "Morning set": ItemData(50, IType.USABLE),
    "Lunch A": ItemData(51, IType.USABLE),
    "Lunch B": ItemData(52, IType.USABLE),
    "Curry rice": ItemData(53, IType.USABLE),
    "Gyros plate": ItemData(54, IType.USABLE),
    "Spaghetti": ItemData(55, IType.USABLE),
    "Grape juice": ItemData(56, IType.USABLE),
    "Barley tea": ItemData(57, IType.USABLE),
    "Green tea": ItemData(58, IType.USABLE),
    "Natou": ItemData(59, IType.USABLE),
    "Ramen": ItemData(60, IType.USABLE),
    "Miso soup": ItemData(61, IType.USABLE),
    "Sushi": ItemData(62, IType.USABLE),
    "Pork bun": ItemData(63, IType.USABLE),
    "Red bean bun": ItemData(64, IType.USABLE),
    "Chinese bun": ItemData(65, IType.USABLE),
    "Dim sum set": ItemData(66, IType.USABLE),
    "Pot roast": ItemData(67, IType.USABLE),
    "Sirloin": ItemData(68, IType.USABLE),
    "Turkey": ItemData(69, IType.USABLE),
    "Meal ticket": ItemData(70, IType.USABLE),
    "Neutron bomb": ItemData(71, IType.USABLE),
    "Power of sire": ItemData(72, IType.USABLE),
    "Pentagram": ItemData(73, IType.USABLE),
    "Bat pentagram": ItemData(74, IType.USABLE),
    "Shuriken": ItemData(75, IType.USABLE),
    "Cross shuriken": ItemData(76, IType.USABLE),
    "Buffalo star": ItemData(77, IType.USABLE),
    "Flame star": ItemData(78, IType.USABLE),
    "TNT": ItemData(79, IType.USABLE),
    "Bwaka knife": ItemData(80, IType.USABLE),
    "Boomerang": ItemData(81, IType.USABLE),
    "Javelin": ItemData(82, IType.USABLE),
    "Tyrfing": ItemData(83, IType.WEAPON1),
    "Namakura": ItemData(84, IType.WEAPON2),
    "Knuckle duster": ItemData(85, IType.WEAPON1),
    "Gladius": ItemData(86, IType.WEAPON1),
    "Scimitar": ItemData(87, IType.WEAPON1),
    "Cutlass": ItemData(88, IType.WEAPON1),
    "Saber": ItemData(89, IType.WEAPON1),
    "Falchion": ItemData(90, IType.WEAPON1),
    "Broadsword": ItemData(91, IType.WEAPON1),
    "Bekatowa": ItemData(92, IType.WEAPON1),
    "Damascus sword": ItemData(93, IType.WEAPON1),
    "Hunter sword": ItemData(94, IType.WEAPON1),
    "Estoc": ItemData(95, IType.WEAPON2),
    "Bastard sword": ItemData(96, IType.WEAPON1),
    "Jewel knuckles": ItemData(97, IType.WEAPON1),
    "Claymore": ItemData(98, IType.WEAPON2),
    "Talwar": ItemData(99, IType.WEAPON1),
    "Katana": ItemData(100, IType.WEAPON2),
    "Flamberge": ItemData(101, IType.WEAPON2),
    "Iron fist": ItemData(102, IType.WEAPON1),
    "Zwei hander": ItemData(103, IType.WEAPON2),
    "Sword of hador": ItemData(104, IType.WEAPON1),
    "Luminus": ItemData(105, IType.WEAPON1),
    "Harper": ItemData(106, IType.WEAPON1),
    "Obsidian sword": ItemData(107, IType.WEAPON2),
    "Gram": ItemData(108, IType.WEAPON1),
    "Jewel sword": ItemData(109, IType.WEAPON1),
    "Mormegil": ItemData(110, IType.WEAPON1),
    "Firebrand": ItemData(111, IType.WEAPON1),
    "Thunderbrand": ItemData(112, IType.WEAPON1),
    "Icebrand": ItemData(113, IType.WEAPON1),
    "Stone sword": ItemData(114, IType.WEAPON1),
    "Holy sword": ItemData(115, IType.WEAPON1),
    "Terminus est": ItemData(116, IType.WEAPON1),
    "Marsil": ItemData(117, IType.WEAPON1),
    "Dark blade": ItemData(118, IType.WEAPON1),
    "Heaven sword": ItemData(119, IType.WEAPON1),
    "Fist of tulkas": ItemData(120, IType.WEAPON1),
    "Gurthang": ItemData(121, IType.WEAPON1),
    "Mourneblade": ItemData(122, IType.WEAPON1),
    "Alucard sword": ItemData(123, IType.WEAPON1),
    "Mablung Sword": ItemData(124, IType.WEAPON1),
    "Badelaire": ItemData(125, IType.WEAPON1),
    "Sword familiar": ItemData(126, IType.WEAPON1),
    "Great sword": ItemData(127, IType.WEAPON2),
    "Mace": ItemData(128, IType.WEAPON1),
    "Morningstar": ItemData(129, IType.WEAPON1),
    "Holy rod": ItemData(130, IType.WEAPON1),
    "Star flail": ItemData(131, IType.WEAPON1),
    "Moon rod": ItemData(132, IType.WEAPON1),
    "Chakram": ItemData(133, IType.WEAPON1),
    "Fire boomerang": ItemData(134, IType.USABLE),
    "Iron ball": ItemData(135, IType.USABLE),
    "Holbein dagger": ItemData(136, IType.WEAPON1),
    "Blue knuckles": ItemData(137, IType.WEAPON1),
    "Dynamite": ItemData(138, IType.USABLE),
    "Osafune katana": ItemData(139, IType.WEAPON2),
    "Masamune": ItemData(140, IType.WEAPON2),
    "Muramasa": ItemData(141, IType.WEAPON2),
    "Heart refresh": ItemData(142, IType.USABLE),
    "Runesword": ItemData(143, IType.WEAPON1),
    "Antivenom": ItemData(144, IType.USABLE),
    "Uncurse": ItemData(145, IType.USABLE),
    "Life apple": ItemData(146, IType.USABLE),
    "Hammer": ItemData(147, IType.USABLE),
    "Str. potion": ItemData(148, IType.USABLE),
    "Luck potion": ItemData(149, IType.USABLE),
    "Smart potion": ItemData(150, IType.USABLE),
    "Attack potion": ItemData(151, IType.USABLE),
    "Shield potion": ItemData(152, IType.USABLE),
    "Resist fire": ItemData(153, IType.USABLE),
    "Resist thunder": ItemData(154, IType.USABLE),
    "Resist ice": ItemData(155, IType.USABLE),
    "Resist stone": ItemData(156, IType.USABLE),
    "Resist holy": ItemData(157, IType.USABLE),
    "Resist dark": ItemData(158, IType.USABLE),
    "Potion": ItemData(159, IType.USABLE),
    "High potion": ItemData(160, IType.USABLE),
    "Elixir": ItemData(161, IType.USABLE),
    "Manna prism": ItemData(162, IType.USABLE),
    "Vorpal blade": ItemData(163, IType.WEAPON1),
    "Crissaegrim": ItemData(164, IType.WEAPON1),
    "Yasutsuna": ItemData(165, IType.WEAPON2),
    "Library card": ItemData(166, IType.USABLE),
    "Alucart shield": ItemData(167, IType.SHIELD),
    "Alucart sword": ItemData(168, IType.WEAPON1)
}

chest_type_table = {
    "Cloth tunic": ItemData(170, IType.ARMOR),
    "Hide cuirass": ItemData(171, IType.ARMOR),
    "Bronze cuirass": ItemData(172, IType.ARMOR),
    "Iron cuirass": ItemData(173, IType.ARMOR),
    "Steel cuirass": ItemData(174, IType.ARMOR),
    "Silver plate": ItemData(175, IType.ARMOR),
    "Gold plate": ItemData(176, IType.ARMOR),
    "Platinum mail": ItemData(177, IType.ARMOR),
    "Diamond plate": ItemData(178, IType.ARMOR),
    "Fire mail": ItemData(179, IType.ARMOR),
    "Lightning mail": ItemData(180, IType.ARMOR),
    "Ice mail": ItemData(181, IType.ARMOR),
    "Mirror cuirass": ItemData(182, IType.ARMOR),
    "Spike breaker": ItemData(183, IType.ARMOR, ItemClassification.progression),
    "Alucard mail": ItemData(184, IType.ARMOR),
    "Dark armor": ItemData(185, IType.ARMOR),
    "Healing mail": ItemData(186, IType.ARMOR),
    "Holy mail": ItemData(187, IType.ARMOR),
    "Walk armor": ItemData(188, IType.ARMOR),
    "Brilliant mail": ItemData(189, IType.ARMOR),
    "Mojo mail": ItemData(190, IType.ARMOR),
    "Fury plate": ItemData(191, IType.ARMOR),
    "Dracula tunic": ItemData(192, IType.ARMOR),
    "God's Garb": ItemData(193, IType.ARMOR),
    "Axe Lord armor": ItemData(194, IType.ARMOR),
    "Alucart mail": ItemData(258, IType.ARMOR)
}

helmet_type_table = {
    "Sunglasses": ItemData(196, IType.HELMET),
    "Ballroom mask": ItemData(197, IType.HELMET),
    "Bandanna": ItemData(198, IType.HELMET),
    "Felt hat": ItemData(199, IType.HELMET),
    "Velvet hat": ItemData(200, IType.HELMET),
    "Goggles": ItemData(201, IType.HELMET),
    "Leather hat": ItemData(202, IType.HELMET),
    "Holy glasses": ItemData(203, IType.HELMET, ItemClassification.progression),
    "Steel helm": ItemData(204, IType.HELMET),
    "Stone mask": ItemData(205, IType.HELMET),
    "Circlet": ItemData(206, IType.HELMET),
    "Gold circlet": ItemData(207, IType.HELMET),
    "Ruby circlet": ItemData(208, IType.HELMET),
    "Opal circlet": ItemData(209, IType.HELMET),
    "Topaz circlet": ItemData(210, IType.HELMET),
    "Beryl circlet": ItemData(211, IType.HELMET),
    "Cat-eye circl.": ItemData(212, IType.HELMET),
    "Coral circlet": ItemData(213, IType.HELMET),
    "Dragon helm": ItemData(214, IType.HELMET),
    "Silver crown": ItemData(215, IType.HELMET),
    "Wizard hat": ItemData(216, IType.HELMET)
}

cloak_type_table = {
    "Cloth cape": ItemData(218, IType.CLOAK),
    "Reverse cloak": ItemData(219, IType.CLOAK),
    "Elven cloak": ItemData(220, IType.CLOAK),
    "Crystal cloak": ItemData(221, IType.CLOAK),
    "Royal cloak": ItemData(222, IType.CLOAK),
    "Blood cloak": ItemData(223, IType.CLOAK),
    "Joseph's cloak": ItemData(224, IType.CLOAK),
    "Twilight cloak": ItemData(225, IType.CLOAK)
}

acc_type_table = {
    "Moonstone": ItemData(227, IType.ACCESSORY),
    "Sunstone": ItemData(228, IType.ACCESSORY),
    "Bloodstone": ItemData(229, IType.ACCESSORY),
    "Staurolite": ItemData(230, IType.ACCESSORY),
    "Ring of pales": ItemData(231, IType.ACCESSORY),
    "Zircon": ItemData(232, IType.ACCESSORY),
    "Aquamarine": ItemData(233, IType.ACCESSORY),
    "Turquoise": ItemData(234, IType.ACCESSORY),
    "Onyx": ItemData(235, IType.ACCESSORY),
    "Garnet": ItemData(236, IType.ACCESSORY),
    "Opal": ItemData(237, IType.ACCESSORY),
    "Diamond": ItemData(238, IType.ACCESSORY),
    "Lapis lazuli": ItemData(239, IType.ACCESSORY),
    "Ring of ares": ItemData(240, IType.ACCESSORY),
    "Gold ring": ItemData(241, IType.ACCESSORY, ItemClassification.progression),
    "Silver ring": ItemData(242, IType.ACCESSORY, ItemClassification.progression),
    "Ring of varda": ItemData(243, IType.ACCESSORY),
    "Ring of arcana": ItemData(244, IType.ACCESSORY),
    "Mystic pendant": ItemData(245, IType.ACCESSORY),
    "Heart broach": ItemData(246, IType.ACCESSORY),
    "Necklace of j": ItemData(247, IType.ACCESSORY),
    "Gauntlet": ItemData(248, IType.ACCESSORY),
    "Ankh of life": ItemData(249, IType.ACCESSORY),
    "Ring of feanor": ItemData(250, IType.ACCESSORY),
    "Medal": ItemData(251, IType.ACCESSORY),
    "Talisman": ItemData(252, IType.ACCESSORY),
    "Duplicator": ItemData(253, IType.ACCESSORY),
    "King's stone": ItemData(254, IType.ACCESSORY),
    "Covenant stone": ItemData(255, IType.ACCESSORY),
    "Nauglamir": ItemData(256, IType.ACCESSORY),
    "Secret boots": ItemData(257, IType.ACCESSORY)
}

vessel_table = {
    "Heart Vessel": ItemData(412, IType.POWERUP),
    "Life Vessel": ItemData(423, IType.POWERUP)
}

relic_table = {
    "Soul of bat": ItemData(300, IType.RELIC, ItemClassification.progression),
    "Fire of bat": ItemData(301, IType.RELIC, ItemClassification.filler),
    "Echo of bat": ItemData(302, IType.RELIC, ItemClassification.progression),
    "Force of echo": ItemData(303, IType.RELIC, ItemClassification.filler),
    "Soul of wolf": ItemData(304, IType.RELIC, ItemClassification.progression),
    "Power of wolf": ItemData(305, IType.RELIC, ItemClassification.filler),
    "Skill of wolf": ItemData(306, IType.RELIC, ItemClassification.filler),
    "Form of mist": ItemData(307, IType.RELIC, ItemClassification.progression),
    "Power of mist": ItemData(308, IType.RELIC, ItemClassification.filler),
    "Gas cloud": ItemData(309, IType.RELIC, ItemClassification.filler),
    "Cube of zoe": ItemData(310, IType.RELIC, ItemClassification.progression),
    "Spirit orb": ItemData(311, IType.RELIC, ItemClassification.filler),
    "Gravity boots": ItemData(312, IType.RELIC, ItemClassification.progression),
    "Leap stone": ItemData(313, IType.RELIC, ItemClassification.progression),
    "Holy symbol": ItemData(314, IType.RELIC, ItemClassification.progression),
    "Faerie scroll": ItemData(315, IType.RELIC, ItemClassification.filler),
    "Jewel of open": ItemData(316, IType.RELIC, ItemClassification.progression),
    "Merman statue": ItemData(317, IType.RELIC, ItemClassification.progression),
    "Bat card": ItemData(318, IType.RELIC, ItemClassification.filler),
    "Ghost card": ItemData(319, IType.RELIC, ItemClassification.filler),
    "Faerie card": ItemData(320, IType.RELIC, ItemClassification.filler),
    "Demon card": ItemData(321, IType.RELIC, ItemClassification.progression),
    "Sword card": ItemData(322, IType.RELIC, ItemClassification.filler),
    "Heart of vlad": ItemData(325, IType.RELIC, ItemClassification.progression),
    "Tooth of vlad": ItemData(326, IType.RELIC, ItemClassification.progression),
    "Rib of vlad": ItemData(327, IType.RELIC, ItemClassification.progression),
    "Ring of vlad": ItemData(328, IType.RELIC, ItemClassification.progression),
    "Eye of vlad": ItemData(329, IType.RELIC, ItemClassification.progression),
}

event_table = {
    "Victory": ItemData(350, IType.EVENT, ItemClassification.progression),
    "Boss token": ItemData(351, IType.EVENT, ItemClassification.progression),
}

item_table = {
    **hand_type_table,
    **chest_type_table,
    **helmet_type_table,
    **cloak_type_table,
    **acc_type_table,
    **vessel_table,
    **relic_table,
}


def get_item_data(item_id: int) -> ItemData:
    for k, v in item_table.items():
        data: ItemData = v
        if data.index == item_id:
            return data


vanilla_list = ["Monster vial 3", "Monster vial 3", "Monster vial 3", "Monster vial 3", "Shield rod", "Leather shield",
                "Knight shield", "Herald shield", "Goddess shield", "Shaman shield", "Alucard shield", "Sword of dawn",
                "Basilard", "Combat knife", "Nunchaku", "Karma coin", "Karma coin", "Karma coin", "Karma coin",
                "Karma coin", "Karma coin", "Magic missile", "Magic missile", "Magic missile", "Magic missile",
                "Magic missile", "Takemitsu", "Shotel", "Peanuts", "Peanuts", "Peanuts", "Peanuts", "Toadstool",
                "Toadstool", "Toadstool", "Shiitake", "Shiitake", "Shiitake", "Shiitake", "Shiitake", "Shiitake",
                "Shiitake", "Shiitake", "Shiitake", "Shiitake", "Shiitake", "Shiitake", "Frankfurter", "Frankfurter",
                "Cheese", "Grape juice", "Barley tea", "Green tea", "Green tea", "Pork bun", "Red bean bun",
                "Dim sum set", "Pot roast", "Pot roast", "Pot roast", "Pot roast", "Pot roast", "Pot roast",
                "Pot roast", "Pot roast", "Sirloin", "Turkey", "Turkey", "Turkey", "Turkey", "Meal ticket",
                "Meal ticket", "Meal ticket", "Meal ticket", "Meal ticket", "Meal ticket", "Meal ticket", "Meal ticket",
                "Meal ticket", "Meal ticket", "Neutron bomb", "Neutron bomb", "Power of sire", "Power of sire",
                "Power of sire", "Pentagram", "Pentagram", "Bat pentagram", "Shuriken", "Shuriken", "Shuriken",
                "Shuriken", "Shuriken", "Cross shuriken", "Cross shuriken", "Buffalo star", "Buffalo star", "TNT",
                "TNT", "TNT", "TNT", "Bwaka knife", "Bwaka knife", "Bwaka knife", "Boomerang", "Boomerang", "Javelin",
                "Tyrfing", "Knuckle duster", "Gladius", "Scimitar", "Cutlass", "Falchion", "Broadsword", "Bekatowa",
                "Estoc", "Bastard sword", "Jewel knuckles", "Claymore", "Talwar", "Katana", "Sword of hador", "Luminus",
                "Gram", "Jewel sword", "Mormegil", "Icebrand", "Holy sword", "Dark blade", "Alucard sword", "Badelaire",
                "Morningstar", "Holy rod", "Star flail", "Moon rod", "Fire boomerang", "Fire boomerang", "Iron ball",
                "Iron ball", "Iron ball", "Osafune katana", "Heart refresh", "Heart refresh", "Heart refresh",
                "Antivenom", "Antivenom", "Antivenom", "Antivenom", "Life apple", "Life apple", "Life apple",
                "Life apple", "Life apple", "Hammer", "Hammer", "Hammer", "Hammer", "Str. potion", "Str. potion",
                "Str. potion", "Luck potion", "Luck potion", "Luck potion", "Smart potion", "Smart potion",
                "Attack potion", "Attack potion", "Shield potion", "Shield potion", "Shield potion",
                "Shield potion", "Resist fire", "Resist fire", "Resist fire", "Resist fire", "Resist fire",
                "Resist thunder", "Resist thunder", "Resist thunder", "Resist thunder", "Resist ice", "Resist ice",
                "Resist ice", "Resist stone", "Resist stone", "Resist stone", "Resist holy", "Resist holy",
                "Resist dark", "Resist dark", "Resist dark", "Potion", "Potion", "Potion", "Potion", "Potion", "Potion",
                "Potion", "High potion", "High potion", "High potion", "High potion", "High potion", "Elixir", "Elixir",
                "Elixir", "Manna prism", "Manna prism", "Manna prism", "Manna prism", "Manna prism", "Library card",
                "Library card", "Library card", "Library card", "Library card", "Library card", "Library card",
                "Alucart shield", "Alucart sword", "Hide cuirass", "Bronze cuirass", "Silver plate", "Gold plate",
                "Platinum mail", "Fire mail", "Lightning mail", "Ice mail", "Mirror cuirass",
                "Alucard mail", "Healing mail", "Holy mail", "Walk armor", "Fury plate", "Dracula tunic",
                "Axe Lord armor", "Sunglasses", "Ballroom mask", "Bandanna", "Goggles", "Steel helm",
                "Stone mask", "Ruby circlet", "Topaz circlet", "Beryl circlet", "Cat-eye circl.", "Dragon helm",
                "Cloth cape", "Crystal cloak", "Royal cloak", "Blood cloak", "Twilight cloak",
                "Moonstone", "Sunstone", "Bloodstone", "Staurolite", "Zircon", "Zircon", "Zircon", "Zircon", "Zircon",
                "Zircon", "Zircon", "Zircon", "Zircon", "Aquamarine", "Aquamarine", "Aquamarine", "Turquoise",
                "Turquoise", "Turquoise", "Onyx", "Onyx", "Onyx", "Garnet", "Garnet", "Garnet", "Garnet", "Garnet",
                "Opal", "Opal", "Opal", "Opal", "Diamond", "Diamond", "Diamond", "Diamond", "Ring of ares",
                "Ring of arcana", "Mystic pendant", "Necklace of j", "Ankh of life", "Talisman",
                "Secret boots", "Alucart mail"
               ]

