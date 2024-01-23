from typing import Optional
from enum import Enum
from BaseClasses import ItemClassification, Item

base_item_id = 127000000
tile_id_offset = 0X80


class Type(Enum):
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
    def __init__(self, index: int, item_type: Type, ic: ItemClassification = ItemClassification.filler):
        self.index = None if index is None else index + base_item_id
        self.type = item_type
        self.ic = ic

    def get_item_id_no_offset(self):
        return self.index - base_item_id

    def get_item_id(self):
        if self.type == Type.RELIC:
            return self.index - base_item_id - 300
        if self.type == Type.POWERUP or self.type == Type.GOLD:
            return self.index - base_item_id - 400
        return self.index - base_item_id + tile_id_offset

    def get_item_type(self):
        return self.type


hand_type_table = {
    "Monster vial 1": ItemData(1, Type.USABLE),
    "Monster vial 2": ItemData(2, Type.USABLE),
    "Monster vial 3": ItemData(3, Type.USABLE),
    "Shield Rod": ItemData(4, Type.WEAPON1),
    "Leather shield": ItemData(5, Type.SHIELD),
    "Knight shield": ItemData(6, Type.SHIELD),
    "Iron shield": ItemData(7, Type.SHIELD),
    "AxeLord shield": ItemData(8, Type.SHIELD),
    "Herald Shield": ItemData(9, Type.SHIELD),
    "Dark shield": ItemData(10, Type.SHIELD),
    "Goddess shield": ItemData(11, Type.SHIELD),
    "Shaman shield": ItemData(12, Type.SHIELD),
    "Medusa shield": ItemData(13, Type.SHIELD),
    "Skull shield": ItemData(14, Type.SHIELD),
    "Fire shield": ItemData(15, Type.SHIELD),
    "Alucard shield": ItemData(16, Type.SHIELD),
    "Sword of dawn": ItemData(17, Type.WEAPON2),
    "Basilard": ItemData(18, Type.WEAPON1),
    "Short sword": ItemData(19, Type.WEAPON1),
    "Combat knife": ItemData(20, Type.WEAPON1),
    "Nunchaku": ItemData(21, Type.WEAPON2),
    "Were bane": ItemData(22, Type.WEAPON1),
    "Rapier": ItemData(23, Type.WEAPON1),
    "Karma coin": ItemData(24, Type.USABLE),
    "Magic missile": ItemData(25, Type.USABLE),
    "Red rust": ItemData(26, Type.WEAPON2),
    "Takemitsu": ItemData(27, Type.WEAPON2),
    "Shotel": ItemData(28, Type.WEAPON1),
    "Orange": ItemData(29, Type.USABLE),
    "Apple": ItemData(30, Type.USABLE),
    "Banana": ItemData(31, Type.USABLE),
    "Grapes": ItemData(32, Type.USABLE),
    "Strawberry": ItemData(33, Type.USABLE),
    "Pineapple": ItemData(34, Type.USABLE),
    "Peanuts": ItemData(35, Type.USABLE),
    "Toadstool": ItemData(36, Type.USABLE),
    "Shiitake": ItemData(37, Type.USABLE),
    "Cheesecake": ItemData(38, Type.USABLE),
    "Shortcake": ItemData(39, Type.USABLE),
    "Tart": ItemData(40, Type.USABLE),
    "Parfait": ItemData(41, Type.USABLE),
    "Pudding": ItemData(42, Type.USABLE),
    "Ice cream": ItemData(43, Type.USABLE),
    "Frankfurter": ItemData(44, Type.USABLE),
    "Hamburger": ItemData(45, Type.USABLE),
    "Pizza": ItemData(46, Type.USABLE),
    "Cheese": ItemData(47, Type.USABLE),
    "Ham and eggs": ItemData(48, Type.USABLE),
    "Omelette": ItemData(49, Type.USABLE),
    "Morning set": ItemData(50, Type.USABLE),
    "Lunch A": ItemData(51, Type.USABLE),
    "Lunch B": ItemData(52, Type.USABLE),
    "Curry rice": ItemData(53, Type.USABLE),
    "Gyros plate": ItemData(54, Type.USABLE),
    "Spaghetti": ItemData(55, Type.USABLE),
    "Grape juice": ItemData(56, Type.USABLE),
    "Barley tea": ItemData(57, Type.USABLE),
    "Green tea": ItemData(58, Type.USABLE),
    "Natou": ItemData(59, Type.USABLE),
    "Ramen": ItemData(60, Type.USABLE),
    "Miso soup": ItemData(61, Type.USABLE),
    "Sushi": ItemData(62, Type.USABLE),
    "Pork bun": ItemData(63, Type.USABLE),
    "Red bean bun": ItemData(64, Type.USABLE),
    "Chinese bun": ItemData(65, Type.USABLE),
    "Dim sum set": ItemData(66, Type.USABLE),
    "Pot roast": ItemData(67, Type.USABLE),
    "Sirloin": ItemData(68, Type.USABLE),
    "Turkey": ItemData(69, Type.USABLE),
    "Meal ticket": ItemData(70, Type.USABLE),
    "Neutron bomb": ItemData(71, Type.USABLE),
    "Power of sire": ItemData(72, Type.USABLE),
    "Pentagram": ItemData(73, Type.USABLE),
    "Bat pentagram": ItemData(74, Type.USABLE),
    "Shuriken": ItemData(75, Type.USABLE),
    "Cross shuriken": ItemData(76, Type.USABLE),
    "Buffalo star": ItemData(77, Type.USABLE),
    "Flame star": ItemData(78, Type.USABLE),
    "TNT": ItemData(79, Type.USABLE),
    "Bwaka knife": ItemData(80, Type.USABLE),
    "Boomerang": ItemData(81, Type.USABLE),
    "Javelin": ItemData(82, Type.USABLE),
    "Tyrfing": ItemData(83, Type.WEAPON1),
    "Namakura": ItemData(84, Type.WEAPON2),
    "Knuckle duster": ItemData(85, Type.WEAPON1),
    "Gladius": ItemData(86, Type.WEAPON1),
    "Scimitar": ItemData(87, Type.WEAPON1),
    "Cutlass": ItemData(88, Type.WEAPON1),
    "Saber": ItemData(89, Type.WEAPON1),
    "Falchion": ItemData(90, Type.WEAPON1),
    "Broadsword": ItemData(91, Type.WEAPON1),
    "Bekatowa": ItemData(92, Type.WEAPON1),
    "Damascus sword": ItemData(93, Type.WEAPON1),
    "Hunter sword": ItemData(94, Type.WEAPON1),
    "Estoc": ItemData(95, Type.WEAPON2),
    "Bastard sword": ItemData(96, Type.WEAPON1),
    "Jewel knuckles": ItemData(97, Type.WEAPON1),
    "Claymore": ItemData(98, Type.WEAPON2),
    "Talwar": ItemData(99, Type.WEAPON1),
    "Katana": ItemData(100, Type.WEAPON2),
    "Flamberge": ItemData(101, Type.WEAPON2),
    "Iron fist": ItemData(102, Type.WEAPON1),
    "Zwei hander": ItemData(103, Type.WEAPON2),
    "Sword of hador": ItemData(104, Type.WEAPON1),
    "Luminus": ItemData(105, Type.WEAPON1),
    "Harper": ItemData(106, Type.WEAPON1),
    "Obsidian sword": ItemData(107, Type.WEAPON2),
    "Gram": ItemData(108, Type.WEAPON1),
    "Jewel sword": ItemData(109, Type.WEAPON1),
    "Mormegil": ItemData(110, Type.WEAPON1),
    "Firebrand": ItemData(111, Type.WEAPON1),
    "Thunderbrand": ItemData(112, Type.WEAPON1),
    "Icebrand": ItemData(113, Type.WEAPON1),
    "Stone sword": ItemData(114, Type.WEAPON1),
    "Holy sword": ItemData(115, Type.WEAPON1),
    "Terminus est": ItemData(116, Type.WEAPON1),
    "Marsil": ItemData(117, Type.WEAPON1),
    "Dark blade": ItemData(118, Type.WEAPON1),
    "Heaven sword": ItemData(119, Type.WEAPON1),
    "Fist of tulkas": ItemData(120, Type.WEAPON1),
    "Gurthang": ItemData(121, Type.WEAPON1),
    "Mourneblade": ItemData(122, Type.WEAPON1),
    "Alucard sword": ItemData(123, Type.WEAPON1),
    "Mablung Sword": ItemData(124, Type.WEAPON1),
    "Badelaire": ItemData(125, Type.WEAPON1),
    "Sword familiar": ItemData(126, Type.WEAPON1),
    "Great sword": ItemData(127, Type.WEAPON2),
    "Mace": ItemData(128, Type.WEAPON1),
    "Morningstar": ItemData(129, Type.WEAPON1),
    "Holy rod": ItemData(130, Type.WEAPON1),
    "Star flail": ItemData(131, Type.WEAPON1),
    "Moon rod": ItemData(132, Type.WEAPON1),
    "Chakram": ItemData(133, Type.WEAPON1),
    "Fire boomerang": ItemData(134, Type.USABLE),
    "Iron ball": ItemData(135, Type.USABLE),
    "Holbein dagger": ItemData(136, Type.WEAPON1),
    "Blue knuckles": ItemData(137, Type.WEAPON1),
    "Dynamite": ItemData(138, Type.USABLE),
    "Osafune katana": ItemData(139, Type.WEAPON2),
    "Masamune": ItemData(140, Type.WEAPON2),
    "Muramasa": ItemData(141, Type.WEAPON2),
    "Heart refresh": ItemData(142, Type.USABLE),
    "Runesword": ItemData(143, Type.WEAPON1),
    "Antivenom": ItemData(144, Type.USABLE),
    "Uncurse": ItemData(145, Type.USABLE),
    "Life apple": ItemData(146, Type.USABLE),
    "Hammer": ItemData(147, Type.USABLE),
    "Str. potion": ItemData(148, Type.USABLE),
    "Luck potion": ItemData(149, Type.USABLE),
    "Smart potion": ItemData(150, Type.USABLE),
    "Attack potion": ItemData(151, Type.USABLE),
    "Shield potion": ItemData(152, Type.USABLE),
    "Resist fire": ItemData(153, Type.USABLE),
    "Resist thunder": ItemData(154, Type.USABLE),
    "Resist ice": ItemData(155, Type.USABLE),
    "Resist stone": ItemData(156, Type.USABLE),
    "Resist holy": ItemData(157, Type.USABLE),
    "Resist dark": ItemData(158, Type.USABLE),
    "Potion": ItemData(159, Type.USABLE),
    "High potion": ItemData(160, Type.USABLE),
    "Elixir": ItemData(161, Type.USABLE),
    "Manna prism": ItemData(162, Type.USABLE),
    "Vorpal blade": ItemData(163, Type.WEAPON1),
    "Crissaegrim": ItemData(164, Type.WEAPON1),
    "Yasutsuna": ItemData(165, Type.WEAPON2),
    "Library card": ItemData(166, Type.USABLE),
    "Alucart shield": ItemData(167, Type.SHIELD),
    "Alucart sword": ItemData(168, Type.WEAPON1)
}

chest_type_table = {
    "Cloth tunic": ItemData(170, Type.ARMOR),
    "Hide cuirass": ItemData(171, Type.ARMOR),
    "Bronze cuirass": ItemData(172, Type.ARMOR),
    "Iron cuirass": ItemData(173, Type.ARMOR),
    "Steel cuirass": ItemData(174, Type.ARMOR),
    "Silver plate": ItemData(175, Type.ARMOR),
    "Gold plate": ItemData(176, Type.ARMOR),
    "Platinum mail": ItemData(177, Type.ARMOR),
    "Diamond plate": ItemData(178, Type.ARMOR),
    "Fire mail": ItemData(179, Type.ARMOR),
    "Lightning mail": ItemData(180, Type.ARMOR),
    "Ice mail": ItemData(181, Type.ARMOR),
    "Mirror cuirass": ItemData(182, Type.ARMOR),
    "Spike breaker": ItemData(183, Type.ARMOR, ItemClassification.progression),
    "Alucard mail": ItemData(184, Type.ARMOR),
    "Dark armor": ItemData(185, Type.ARMOR),
    "Healing mail": ItemData(186, Type.ARMOR),
    "Holy mail": ItemData(187, Type.ARMOR),
    "Walk armor": ItemData(188, Type.ARMOR),
    "Brilliant mail": ItemData(189, Type.ARMOR),
    "Mojo mail": ItemData(190, Type.ARMOR),
    "Fury plate": ItemData(191, Type.ARMOR),
    "Dracula tunic": ItemData(192, Type.ARMOR),
    "God's Garb": ItemData(193, Type.ARMOR),
    "Axe Lord armor": ItemData(194, Type.ARMOR),
    "Alucart mail": ItemData(258, Type.ARMOR)
}

helmet_type_table = {
    "Sunglasses": ItemData(196, Type.HELMET),
    "Ballroom mask": ItemData(197, Type.HELMET),
    "Bandanna": ItemData(198, Type.HELMET),
    "Felt hat": ItemData(199, Type.HELMET),
    "Velvet hat": ItemData(200, Type.HELMET),
    "Goggles": ItemData(201, Type.HELMET),
    "Leather hat": ItemData(202, Type.HELMET),
    "Holy glasses": ItemData(203, Type.HELMET, ItemClassification.progression),
    "Steel helm": ItemData(204, Type.HELMET),
    "Stone mask": ItemData(205, Type.HELMET),
    "Circlet": ItemData(206, Type.HELMET),
    "Gold circlet": ItemData(207, Type.HELMET),
    "Ruby circlet": ItemData(208, Type.HELMET),
    "Opal circlet": ItemData(209, Type.HELMET),
    "Topaz circlet": ItemData(210, Type.HELMET),
    "Beryl circlet": ItemData(211, Type.HELMET),
    "Cat-eye circl.": ItemData(212, Type.HELMET),
    "Coral circlet": ItemData(213, Type.HELMET),
    "Dragon helm": ItemData(214, Type.HELMET),
    "Silver crown": ItemData(215, Type.HELMET),
    "Wizard hat": ItemData(216, Type.HELMET)
}

cloak_type_table = {
    "Cloth cape": ItemData(218, Type.CLOAK),
    "Reverse cloak": ItemData(219, Type.CLOAK),
    "Elven cloak": ItemData(220, Type.CLOAK),
    "Crystal cloak": ItemData(221, Type.CLOAK),
    "Royal cloak": ItemData(222, Type.CLOAK),
    "Blood cloak": ItemData(223, Type.CLOAK),
    "Joseph's cloak": ItemData(224, Type.CLOAK),
    "Twilight cloak": ItemData(225, Type.CLOAK)
}

acc_type_table = {
    "Moonstone": ItemData(227, Type.ACCESSORY),
    "Sunstone": ItemData(228, Type.ACCESSORY),
    "Bloodstone": ItemData(229, Type.ACCESSORY),
    "Staurolite": ItemData(230, Type.ACCESSORY),
    "Ring of pales": ItemData(231, Type.ACCESSORY),
    "Zircon": ItemData(232, Type.ACCESSORY),
    "Aquamarine": ItemData(233, Type.ACCESSORY),
    "Turquoise": ItemData(234, Type.ACCESSORY),
    "Onyx": ItemData(235, Type.ACCESSORY),
    "Garnet": ItemData(236, Type.ACCESSORY),
    "Opal": ItemData(237, Type.ACCESSORY),
    "Diamond": ItemData(238, Type.ACCESSORY),
    "Lapis lazuli": ItemData(239, Type.ACCESSORY),
    "Ring of ares": ItemData(240, Type.ACCESSORY),
    "Gold ring": ItemData(241, Type.ACCESSORY, ItemClassification.progression),
    "Silver ring": ItemData(242, Type.ACCESSORY, ItemClassification.progression),
    "Ring of varda": ItemData(243, Type.ACCESSORY),
    "Ring of arcana": ItemData(244, Type.ACCESSORY),
    "Mystic pendant": ItemData(245, Type.ACCESSORY),
    "Heart broach": ItemData(246, Type.ACCESSORY),
    "Necklace of j": ItemData(247, Type.ACCESSORY),
    "Gauntlet": ItemData(248, Type.ACCESSORY),
    "Ankh of life": ItemData(249, Type.ACCESSORY),
    "Ring of feanor": ItemData(250, Type.ACCESSORY),
    "Medal": ItemData(251, Type.ACCESSORY),
    "Talisman": ItemData(252, Type.ACCESSORY),
    "Duplicator": ItemData(253, Type.ACCESSORY),
    "King's stone": ItemData(254, Type.ACCESSORY),
    "Covenant stone": ItemData(255, Type.ACCESSORY),
    "Nauglamir": ItemData(256, Type.ACCESSORY),
    "Secret boots": ItemData(257, Type.ACCESSORY)
}

vessel_table = {
    "Heart Vessel": ItemData(412, Type.POWERUP),
    "Life Vessel": ItemData(423, Type.POWERUP)
}

relic_table = {
    "Soul of bat": ItemData(300, Type.RELIC, ItemClassification.progression),
    "Fire of bat": ItemData(301, Type.RELIC),
    "Echo of bat": ItemData(302, Type.RELIC, ItemClassification.progression),
    "Force of echo": ItemData(303, Type.RELIC),
    "Soul of wolf": ItemData(304, Type.RELIC, ItemClassification.progression),
    "Power of wolf": ItemData(305, Type.RELIC),
    "Skill of wolf": ItemData(306, Type.RELIC),
    "Form of mist": ItemData(307, Type.RELIC, ItemClassification.progression),
    "Power of mist": ItemData(308, Type.RELIC),
    "Gas cloud": ItemData(309, Type.RELIC),
    "Cube of zoe": ItemData(310, Type.RELIC, ItemClassification.progression),
    "Spirit orb": ItemData(311, Type.RELIC),
    "Gravity boots": ItemData(312, Type.RELIC, ItemClassification.progression),
    "Leap stone": ItemData(313, Type.RELIC, ItemClassification.progression),
    "Holy symbol": ItemData(314, Type.RELIC, ItemClassification.progression),
    "Faerie scroll": ItemData(315, Type.RELIC),
    "Jewel of open": ItemData(316, Type.RELIC, ItemClassification.progression),
    "Merman statue": ItemData(317, Type.RELIC, ItemClassification.progression),
    "Bat card": ItemData(318, Type.RELIC),
    "Ghost card": ItemData(319, Type.RELIC),
    "Faerie card": ItemData(320, Type.RELIC),
    "Demon card": ItemData(321, Type.RELIC, ItemClassification.progression),
    "Sword card": ItemData(322, Type.RELIC),
    "Heart of vlad": ItemData(325, Type.RELIC, ItemClassification.progression),
    "Tooth of vlad": ItemData(326, Type.RELIC, ItemClassification.progression),
    "Rib of vlad": ItemData(327, Type.RELIC, ItemClassification.progression),
    "Ring of vlad": ItemData(328, Type.RELIC, ItemClassification.progression),
    "Eye of vlad": ItemData(329, Type.RELIC, ItemClassification.progression),
}

event_table = {
    "Victory": ItemData(350, Type.EVENT, ItemClassification.progression),
    "Boss token": ItemData(351, Type.EVENT, ItemClassification.progression),
}

item_table = {
    **hand_type_table,
    **chest_type_table,
    **helmet_type_table,
    **acc_type_table,
    **vessel_table,
    **relic_table,
}


