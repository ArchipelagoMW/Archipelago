from typing import Optional, Tuple
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
    def __init__(self, index: int, item_type: IType, address: int, ic: ItemClassification = ItemClassification.filler):
        self.index = None if index is None else index + base_item_id
        self.type = item_type
        self.ic = ic
        self.address = address

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

    @staticmethod
    def get_item_info(item_id: int) -> tuple:
        for k, v in item_table.items():
            if v.index == item_id:
                return k, v


hand_type_table = {
    "Monster vial 1": ItemData(1, IType.USABLE, 0x09798b),
    "Monster vial 2": ItemData(2, IType.USABLE, 0x09798c),
    "Monster vial 3": ItemData(3, IType.USABLE, 0x09798d),
    "Shield rod": ItemData(4, IType.WEAPON1, 0x09798e),
    "Leather shield": ItemData(5, IType.SHIELD, 0x09798f),
    "Knight shield": ItemData(6, IType.SHIELD, 0x097990),
    "Iron shield": ItemData(7, IType.SHIELD, 0x097991),
    "AxeLord shield": ItemData(8, IType.SHIELD, 0x097992),
    "Herald shield": ItemData(9, IType.SHIELD, 0x097993),
    "Dark shield": ItemData(10, IType.SHIELD, 0x097994),
    "Goddess shield": ItemData(11, IType.SHIELD, 0x097995),
    "Shaman shield": ItemData(12, IType.SHIELD, 0x097996),
    "Medusa shield": ItemData(13, IType.SHIELD, 0x097997),
    "Skull shield": ItemData(14, IType.SHIELD, 0x097998),
    "Fire shield": ItemData(15, IType.SHIELD, 0x097999),
    "Alucard shield": ItemData(16, IType.SHIELD, 0x09799a),
    "Sword of dawn": ItemData(17, IType.WEAPON2, 0x09799b),
    "Basilard": ItemData(18, IType.WEAPON1, 0x09799c),
    "Short sword": ItemData(19, IType.WEAPON1, 0x09799d),
    "Combat knife": ItemData(20, IType.WEAPON1, 0x09799e),
    "Nunchaku": ItemData(21, IType.WEAPON2, 0x09799f),
    "Were bane": ItemData(22, IType.WEAPON1, 0x0979a0),
    "Rapier": ItemData(23, IType.WEAPON1, 0x0979a1),
    "Karma coin": ItemData(24, IType.USABLE, 0x0979a2),
    "Magic missile": ItemData(25, IType.USABLE, 0x0979a3),
    "Red rust": ItemData(26, IType.WEAPON2, 0x0979a4),
    "Takemitsu": ItemData(27, IType.WEAPON2, 0x0979a5),
    "Shotel": ItemData(28, IType.WEAPON1, 0x0979a6),
    "Orange": ItemData(29, IType.USABLE, 0x0979a7),
    "Apple": ItemData(30, IType.USABLE, 0x0979a8),
    "Banana": ItemData(31, IType.USABLE, 0x0979a9),
    "Grapes": ItemData(32, IType.USABLE, 0x0979aa),
    "Strawberry": ItemData(33, IType.USABLE, 0x0979ab),
    "Pineapple": ItemData(34, IType.USABLE, 0x0979ac),
    "Peanuts": ItemData(35, IType.USABLE, 0x0979ad),
    "Toadstool": ItemData(36, IType.USABLE, 0x0979ae),
    "Shiitake": ItemData(37, IType.USABLE, 0x0979af),
    "Cheesecake": ItemData(38, IType.USABLE, 0x0979b0),
    "Shortcake": ItemData(39, IType.USABLE, 0x0979b1),
    "Tart": ItemData(40, IType.USABLE, 0x0979b2),
    "Parfait": ItemData(41, IType.USABLE, 0x0979b3),
    "Pudding": ItemData(42, IType.USABLE, 0x0979b4),
    "Ice cream": ItemData(43, IType.USABLE, 0x0979b5),
    "Frankfurter": ItemData(44, IType.USABLE, 0x0979b6),
    "Hamburger": ItemData(45, IType.USABLE, 0x0979b7),
    "Pizza": ItemData(46, IType.USABLE, 0x0979b8),
    "Cheese": ItemData(47, IType.USABLE, 0x0979b9),
    "Ham and eggs": ItemData(48, IType.USABLE, 0x0979ba),
    "Omelette": ItemData(49, IType.USABLE, 0x0979bb),
    "Morning set": ItemData(50, IType.USABLE, 0x0979bc),
    "Lunch A": ItemData(51, IType.USABLE, 0x0979bd),
    "Lunch B": ItemData(52, IType.USABLE, 0x0979be),
    "Curry rice": ItemData(53, IType.USABLE, 0x0979bf),
    "Gyros plate": ItemData(54, IType.USABLE, 0x0979c0),
    "Spaghetti": ItemData(55, IType.USABLE, 0x0979c1),
    "Grape juice": ItemData(56, IType.USABLE, 0x0979c2),
    "Barley tea": ItemData(57, IType.USABLE, 0x0979c3),
    "Green tea": ItemData(58, IType.USABLE, 0x0979c4),
    "Natou": ItemData(59, IType.USABLE, 0x0979c5),
    "Ramen": ItemData(60, IType.USABLE, 0x0979c6),
    "Miso soup": ItemData(61, IType.USABLE, 0x0979c7),
    "Sushi": ItemData(62, IType.USABLE, 0x0979c8),
    "Pork bun": ItemData(63, IType.USABLE, 0x0979c9),
    "Red bean bun": ItemData(64, IType.USABLE, 0x0979ca),
    "Chinese bun": ItemData(65, IType.USABLE, 0x0979cb),
    "Dim sum set": ItemData(66, IType.USABLE, 0x0979cc),
    "Pot roast": ItemData(67, IType.USABLE, 0x0979cd),
    "Sirloin": ItemData(68, IType.USABLE, 0x0979ce),
    "Turkey": ItemData(69, IType.USABLE, 0x0979cf),
    "Meal ticket": ItemData(70, IType.USABLE, 0x0979d0),
    "Neutron bomb": ItemData(71, IType.USABLE, 0x0979d1),
    "Power of sire": ItemData(72, IType.USABLE, 0x0979d2),
    "Pentagram": ItemData(73, IType.USABLE, 0x0979d3),
    "Bat pentagram": ItemData(74, IType.USABLE, 0x0979d4),
    "Shuriken": ItemData(75, IType.USABLE, 0x0979d5),
    "Cross shuriken": ItemData(76, IType.USABLE, 0x0979d6),
    "Buffalo star": ItemData(77, IType.USABLE, 0x0979d7),
    "Flame star": ItemData(78, IType.USABLE, 0x0979d8),
    "TNT": ItemData(79, IType.USABLE, 0x0979d9),
    "Bwaka knife": ItemData(80, IType.USABLE, 0x0979da),
    "Boomerang": ItemData(81, IType.USABLE, 0x0979db),
    "Javelin": ItemData(82, IType.USABLE, 0x0979dc),
    "Tyrfing": ItemData(83, IType.WEAPON1, 0x0979dd),
    "Namakura": ItemData(84, IType.WEAPON2, 0x0979de),
    "Knuckle duster": ItemData(85, IType.WEAPON1, 0x0979df),
    "Gladius": ItemData(86, IType.WEAPON1, 0x0979e0),
    "Scimitar": ItemData(87, IType.WEAPON1, 0x0979e1),
    "Cutlass": ItemData(88, IType.WEAPON1, 0x0979e2),
    "Saber": ItemData(89, IType.WEAPON1, 0x0979e3),
    "Falchion": ItemData(90, IType.WEAPON1, 0x0979e4),
    "Broadsword": ItemData(91, IType.WEAPON1, 0x0979e5),
    "Bekatowa": ItemData(92, IType.WEAPON1, 0x0979e6),
    "Damascus sword": ItemData(93, IType.WEAPON1, 0x0979e7),
    "Hunter sword": ItemData(94, IType.WEAPON1, 0x0979e8),
    "Estoc": ItemData(95, IType.WEAPON2, 0x0979e9),
    "Bastard sword": ItemData(96, IType.WEAPON1, 0x0979ea),
    "Jewel knuckles": ItemData(97, IType.WEAPON1, 0x0979eb),
    "Claymore": ItemData(98, IType.WEAPON2, 0x0979ec),
    "Talwar": ItemData(99, IType.WEAPON1, 0x0979ed),
    "Katana": ItemData(100, IType.WEAPON2, 0x0979ee),
    "Flamberge": ItemData(101, IType.WEAPON2, 0x0979ef),
    "Iron fist": ItemData(102, IType.WEAPON1, 0x0979f0),
    "Zwei hander": ItemData(103, IType.WEAPON2, 0x0979f1),
    "Sword of hador": ItemData(104, IType.WEAPON1, 0x0979f2),
    "Luminus": ItemData(105, IType.WEAPON1, 0x0979f3),
    "Harper": ItemData(106, IType.WEAPON1, 0x0979f4),
    "Obsidian sword": ItemData(107, IType.WEAPON2, 0x0979f5),
    "Gram": ItemData(108, IType.WEAPON1, 0x0979f6),
    "Jewel sword": ItemData(109, IType.WEAPON1, 0x0979f7),
    "Mormegil": ItemData(110, IType.WEAPON1, 0x0979f8),
    "Firebrand": ItemData(111, IType.WEAPON1, 0x0979f9),
    "Thunderbrand": ItemData(112, IType.WEAPON1, 0x0979fa),
    "Icebrand": ItemData(113, IType.WEAPON1, 0x0979fb),
    "Stone sword": ItemData(114, IType.WEAPON1, 0x0979fc),
    "Holy sword": ItemData(115, IType.WEAPON1, 0x0979fd),
    "Terminus est": ItemData(116, IType.WEAPON1, 0x0979fe),
    "Marsil": ItemData(117, IType.WEAPON1, 0x0979ff),
    "Dark blade": ItemData(118, IType.WEAPON1, 0x097a00),
    "Heaven sword": ItemData(119, IType.WEAPON1, 0x097a01),
    "Fist of tulkas": ItemData(120, IType.WEAPON1, 0x097a02),
    "Gurthang": ItemData(121, IType.WEAPON1, 0x097a03),
    "Mourneblade": ItemData(122, IType.WEAPON1, 0x097a04),
    "Alucard sword": ItemData(123, IType.WEAPON1, 0x097a05),
    "Mablung Sword": ItemData(124, IType.WEAPON1, 0x097a06),
    "Badelaire": ItemData(125, IType.WEAPON1, 0x097a07),
    "Sword familiar": ItemData(126, IType.WEAPON1, 0x097a08),
    "Great sword": ItemData(127, IType.WEAPON2, 0x097a09),
    "Mace": ItemData(128, IType.WEAPON1, 0x097a0a),
    "Morningstar": ItemData(129, IType.WEAPON1, 0x097a0b),
    "Holy rod": ItemData(130, IType.WEAPON1, 0x097a0c),
    "Star flail": ItemData(131, IType.WEAPON1, 0x097a0d),
    "Moon rod": ItemData(132, IType.WEAPON1, 0x097a0e),
    "Chakram": ItemData(133, IType.WEAPON1, 0x097a0f),
    "Fire boomerang": ItemData(134, IType.USABLE, 0x097a10),
    "Iron ball": ItemData(135, IType.USABLE, 0x097a11),
    "Holbein dagger": ItemData(136, IType.WEAPON1, 0x097a12),
    "Blue knuckles": ItemData(137, IType.WEAPON1, 0x097a13),
    "Dynamite": ItemData(138, IType.USABLE, 0x097a14),
    "Osafune katana": ItemData(139, IType.WEAPON2, 0x097a15),
    "Masamune": ItemData(140, IType.WEAPON2, 0x097a16),
    "Muramasa": ItemData(141, IType.WEAPON2, 0x097a17),
    "Heart refresh": ItemData(142, IType.USABLE, 0x097a18),
    "Runesword": ItemData(143, IType.WEAPON1, 0x097a19),
    "Antivenom": ItemData(144, IType.USABLE, 0x097a1a),
    "Uncurse": ItemData(145, IType.USABLE, 0x097a1b),
    "Life apple": ItemData(146, IType.USABLE, 0x097a1c),
    "Hammer": ItemData(147, IType.USABLE, 0x097a1d),
    "Str. potion": ItemData(148, IType.USABLE, 0x097a1e),
    "Luck potion": ItemData(149, IType.USABLE, 0x097a1f),
    "Smart potion": ItemData(150, IType.USABLE, 0x097a20),
    "Attack potion": ItemData(151, IType.USABLE, 0x097a21),
    "Shield potion": ItemData(152, IType.USABLE, 0x097a22),
    "Resist fire": ItemData(153, IType.USABLE, 0x097a23),
    "Resist thunder": ItemData(154, IType.USABLE, 0x097a24),
    "Resist ice": ItemData(155, IType.USABLE, 0x097a25),
    "Resist stone": ItemData(156, IType.USABLE, 0x097a26),
    "Resist holy": ItemData(157, IType.USABLE, 0x097a27),
    "Resist dark": ItemData(158, IType.USABLE, 0x097a28),
    "Potion": ItemData(159, IType.USABLE, 0x097a29),
    "High potion": ItemData(160, IType.USABLE, 0x097a2a),
    "Elixir": ItemData(161, IType.USABLE, 0x097a2b),
    "Manna prism": ItemData(162, IType.USABLE, 0x097a2c),
    "Vorpal blade": ItemData(163, IType.WEAPON1, 0x097a2d),
    "Crissaegrim": ItemData(164, IType.WEAPON1, 0x097a2e),
    "Yasutsuna": ItemData(165, IType.WEAPON2, 0x097a2f),
    "Library card": ItemData(166, IType.USABLE, 0x097a30),
    "Alucart shield": ItemData(167, IType.SHIELD, 0x097a31),
    "Alucart sword": ItemData(168, IType.WEAPON1, 0x097a32)
}

chest_type_table = {
    "Cloth tunic": ItemData(170, IType.ARMOR, 0x097a34),
    "Hide cuirass": ItemData(171, IType.ARMOR, 0x097a35),
    "Bronze cuirass": ItemData(172, IType.ARMOR, 0x097a36),
    "Iron cuirass": ItemData(173, IType.ARMOR, 0x097a37),
    "Steel cuirass": ItemData(174, IType.ARMOR, 0x097a38),
    "Silver plate": ItemData(175, IType.ARMOR, 0x097a39),
    "Gold plate": ItemData(176, IType.ARMOR, 0x097a3a),
    "Platinum mail": ItemData(177, IType.ARMOR, 0x097a3b),
    "Diamond plate": ItemData(178, IType.ARMOR, 0x097a3c),
    "Fire mail": ItemData(179, IType.ARMOR, 0x097a3d),
    "Lightning mail": ItemData(180, IType.ARMOR, 0x097a3e),
    "Ice mail": ItemData(181, IType.ARMOR, 0x097a3f),
    "Mirror cuirass": ItemData(182, IType.ARMOR, 0x097a40),
    "Spike breaker": ItemData(183, IType.ARMOR, 0x097a41, ItemClassification.progression),
    "Alucard mail": ItemData(184, IType.ARMOR, 0x097a42),
    "Dark armor": ItemData(185, IType.ARMOR, 0x097a43),
    "Healing mail": ItemData(186, IType.ARMOR, 0x097a44),
    "Holy mail": ItemData(187, IType.ARMOR, 0x097a45),
    "Walk armor": ItemData(188, IType.ARMOR, 0x097a46),
    "Brilliant mail": ItemData(189, IType.ARMOR, 0x097a47),
    "Mojo mail": ItemData(190, IType.ARMOR, 0x097a48),
    "Fury plate": ItemData(191, IType.ARMOR, 0x097a49),
    "Dracula tunic": ItemData(192, IType.ARMOR, 0x097a4a),
    "God's Garb": ItemData(193, IType.ARMOR, 0x097a4b),
    "Axe Lord armor": ItemData(194, IType.ARMOR, 0x097a4c),
    "Alucart mail": ItemData(258, IType.ARMOR, 0x097a8c)
}

helmet_type_table = {
    "Sunglasses": ItemData(196, IType.HELMET, 0x097a4e),
    "Ballroom mask": ItemData(197, IType.HELMET, 0x097a4f),
    "Bandanna": ItemData(198, IType.HELMET, 0x097a50),
    "Felt hat": ItemData(199, IType.HELMET, 0x097a51),
    "Velvet hat": ItemData(200, IType.HELMET, 0x097a52),
    "Goggles": ItemData(201, IType.HELMET, 0x097a53),
    "Leather hat": ItemData(202, IType.HELMET, 0x097a54),
    "Holy glasses": ItemData(203, IType.HELMET, 0x097a55, ItemClassification.progression),
    "Steel helm": ItemData(204, IType.HELMET, 0x097a56),
    "Stone mask": ItemData(205, IType.HELMET, 0x097a57),
    "Circlet": ItemData(206, IType.HELMET, 0x097a58),
    "Gold circlet": ItemData(207, IType.HELMET, 0x097a59),
    "Ruby circlet": ItemData(208, IType.HELMET, 0x097a5a),
    "Opal circlet": ItemData(209, IType.HELMET, 0x097a5b),
    "Topaz circlet": ItemData(210, IType.HELMET, 0x097a5c),
    "Beryl circlet": ItemData(211, IType.HELMET, 0x097a5d),
    "Cat-eye circl.": ItemData(212, IType.HELMET, 0x097a5e),
    "Coral circlet": ItemData(213, IType.HELMET, 0x097a5f),
    "Dragon helm": ItemData(214, IType.HELMET, 0x097a60),
    "Silver crown": ItemData(215, IType.HELMET, 0x097a61),
    "Wizard hat": ItemData(216, IType.HELMET, 0x097a62)
}

cloak_type_table = {
    "Cloth cape": ItemData(218, IType.CLOAK, 0x097a64),
    "Reverse cloak": ItemData(219, IType.CLOAK, 0x097a65),
    "Elven cloak": ItemData(220, IType.CLOAK, 0x097a66),
    "Crystal cloak": ItemData(221, IType.CLOAK, 0x097a67),
    "Royal cloak": ItemData(222, IType.CLOAK, 0x097a68),
    "Blood cloak": ItemData(223, IType.CLOAK, 0x097a69),
    "Joseph's cloak": ItemData(224, IType.CLOAK, 0x097a6a),
    "Twilight cloak": ItemData(225, IType.CLOAK, 0x097a6b)
}

acc_type_table = {
    "Moonstone": ItemData(227, IType.ACCESSORY, 0x097a6d),
    "Sunstone": ItemData(228, IType.ACCESSORY, 0x097a6e),
    "Bloodstone": ItemData(229, IType.ACCESSORY, 0x097a6f),
    "Staurolite": ItemData(230, IType.ACCESSORY, 0x097a70),
    "Ring of pales": ItemData(231, IType.ACCESSORY, 0x097a71),
    "Zircon": ItemData(232, IType.ACCESSORY, 0x097a72),
    "Aquamarine": ItemData(233, IType.ACCESSORY, 0x097a73),
    "Turquoise": ItemData(234, IType.ACCESSORY, 0x097a74),
    "Onyx": ItemData(235, IType.ACCESSORY, 0x097a75),
    "Garnet": ItemData(236, IType.ACCESSORY, 0x097a76),
    "Opal": ItemData(237, IType.ACCESSORY, 0x097a77),
    "Diamond": ItemData(238, IType.ACCESSORY, 0x097a78),
    "Lapis lazuli": ItemData(239, IType.ACCESSORY, 0x097a79),
    "Ring of ares": ItemData(240, IType.ACCESSORY, 0x097a7a),
    "Gold ring": ItemData(241, IType.ACCESSORY, 0x097a7b, ItemClassification.progression),
    "Silver ring": ItemData(242, IType.ACCESSORY, 0x097a7C, ItemClassification.progression),
    "Ring of varda": ItemData(243, IType.ACCESSORY, 0x097a7d),
    "Ring of arcana": ItemData(244, IType.ACCESSORY, 0x097a7e),
    "Mystic pendant": ItemData(245, IType.ACCESSORY, 0x097a7f),
    "Heart broach": ItemData(246, IType.ACCESSORY, 0x097a80),
    "Necklace of j": ItemData(247, IType.ACCESSORY, 0x097a81),
    "Gauntlet": ItemData(248, IType.ACCESSORY, 0x097a82),
    "Ankh of life": ItemData(249, IType.ACCESSORY, 0x097a83),
    "Ring of feanor": ItemData(250, IType.ACCESSORY, 0x097a84),
    "Medal": ItemData(251, IType.ACCESSORY, 0x097a85),
    "Talisman": ItemData(252, IType.ACCESSORY, 0x097a86),
    "Duplicator": ItemData(253, IType.ACCESSORY, 0x097a87),
    "King's stone": ItemData(254, IType.ACCESSORY, 0x097a88),
    "Covenant stone": ItemData(255, IType.ACCESSORY, 0x097a89),
    "Nauglamir": ItemData(256, IType.ACCESSORY, 0x097a8a),
    "Secret boots": ItemData(257, IType.ACCESSORY, 0x097a8b)
}

vessel_table = {
    "Heart Vessel": ItemData(412, IType.POWERUP, 0x097ba8),
    "Life Vessel": ItemData(423, IType.POWERUP, 0x097ba0)
}

relic_table = {
    "Soul of bat": ItemData(300, IType.RELIC, 0x097964, ItemClassification.progression),
    "Fire of bat": ItemData(301, IType.RELIC, 0x097965),
    "Echo of bat": ItemData(302, IType.RELIC, 0x097966, ItemClassification.progression),
    "Force of echo": ItemData(303, IType.RELIC, 0x097967),
    "Soul of wolf": ItemData(304, IType.RELIC, 0x097968, ItemClassification.progression),
    "Power of wolf": ItemData(305, IType.RELIC, 0x097969),
    "Skill of wolf": ItemData(306, IType.RELIC, 0x09796a),
    "Form of mist": ItemData(307, IType.RELIC, 0x09796b, ItemClassification.progression),
    "Power of mist": ItemData(308, IType.RELIC, 0x09796c),
    "Gas cloud": ItemData(309, IType.RELIC, 0x09796d),
    "Cube of zoe": ItemData(310, IType.RELIC, 0x09796e, ItemClassification.progression),
    "Spirit orb": ItemData(311, IType.RELIC, 0x09796f),
    "Gravity boots": ItemData(312, IType.RELIC, 0x097970, ItemClassification.progression),
    "Leap stone": ItemData(313, IType.RELIC, 0x097971, ItemClassification.progression),
    "Holy symbol": ItemData(314, IType.RELIC, 0x097972, ItemClassification.progression),
    "Faerie scroll": ItemData(315, IType.RELIC, 0x097973),
    "Jewel of open": ItemData(316, IType.RELIC, 0x097974, ItemClassification.progression),
    "Merman statue": ItemData(317, IType.RELIC, 0x097975, ItemClassification.progression),
    "Bat card": ItemData(318, IType.RELIC, 0x097976),
    "Ghost card": ItemData(319, IType.RELIC, 0x097977),
    "Faerie card": ItemData(320, IType.RELIC, 0x097978),
    "Demon card": ItemData(321, IType.RELIC, 0x097979, ItemClassification.progression),
    "Sword card": ItemData(322, IType.RELIC, 0x09797a),
    "Heart of vlad": ItemData(325, IType.RELIC, 0x09797d, ItemClassification.progression),
    "Tooth of vlad": ItemData(326, IType.RELIC, 0x09797e, ItemClassification.progression),
    "Rib of vlad": ItemData(327, IType.RELIC, 0x09797f, ItemClassification.progression),
    "Ring of vlad": ItemData(328, IType.RELIC, 0x097980, ItemClassification.progression),
    "Eye of vlad": ItemData(329, IType.RELIC, 0x097981, ItemClassification.progression),
}

event_table = {
    "Victory": ItemData(350, IType.EVENT, 0x0, ItemClassification.progression),
    "Boss token": ItemData(351, IType.EVENT, 0x0, ItemClassification.progression),
    "Exploration token": ItemData(352, IType.EVENT, 0x0, ItemClassification.progression)
}

item_table = {
    **hand_type_table,
    **chest_type_table,
    **helmet_type_table,
    **cloak_type_table,
    **acc_type_table,
    **vessel_table,
    **relic_table,
    **event_table,
}


def get_item_data(item_id: int) -> ItemData:
    for k, v in item_table.items():
        data: ItemData = v
        if data.index == item_id:
            return data


def get_item_data_shop(item_id: int) -> Tuple:
    for k, v in item_table.items():
        data: ItemData = v
        if data.index == item_id + base_item_id:
            return k, data


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

