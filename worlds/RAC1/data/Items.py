from dataclasses import dataclass
from typing import Mapping, Sequence

from BaseClasses import Item
from worlds.RAC1 import Options


@dataclass
class ItemData(Item):
    item_id: int
    name: str
    pool: str
    quantity: int = 1


HELI_PACK = ItemData(2, "Heli Pack", "Packs")
THRUSTER_PACK = ItemData(3, "Thruster Pack", "Packs")
HYDRO_PACK = ItemData(4, "Hydro Pack", "Packs")
SONIC_SUMMONER = ItemData(5, "Sonic Summoner", "Helmets")
O2_MASK = ItemData(6, "O2 Mask", "Helmets")
PILOTS_HELMET = ItemData(7, "Pilots Helmet", "Helmets")
# WRENCH = ItemData(8, "Wrench", "?")
SUCK_CANNON = ItemData(9, "Suck cannon", "Weapons")
BOMB_GLOVE = ItemData(10, "Bomb glove", "Weapons")
DEVASTATOR = ItemData(11, "Devastator", "Weapons")
SWINGSHOT = ItemData(12, "Swingshot", "Gadgets")
VISIBOMB = ItemData(13, "Visibomb", "Weapons")
TAUNTER = ItemData(14, "Taunter", "Weapons")
BLASTER = ItemData(15, "Blaster", "Weapons")
PYROCITOR = ItemData(16, "Pyrocitor", "Weapons")
MINE_GLOVE = ItemData(17, "Mine glove", "Weapons")
WALLOPER = ItemData(18, "Walloper", "Weapons")
TESLA_CLAW = ItemData(19, "Tesla claw", "Weapons")
GLOVE_OF_DOOM = ItemData(20, "Glove of doom", "Weapons")
MORPH_O_RAY = ItemData(21, "Morph-o-ray", "Weapons")
HYDRODISPLACER = ItemData(22, "Hydrodisplacer", "Gadgets")
RYNO = ItemData(23, "RYNO", "Weapons")
DRONE_DEVICE = ItemData(24, "Drone device", "Weapons")
DECOY_GLOVE = ItemData(25, "Decoy glove", "Weapons")
TRESPASSER = ItemData(26, "Trespasser", "Gadgets")
METAL_DETECTOR = ItemData(27, "Metal Detector", "Gadgets")
MAGNEBOOTS = ItemData(28, "Magneboots", "Boots")
GRINDBOOTS = ItemData(29, "Grindboots", "Boots")
HOVERBOARD = ItemData(30, "Hoverboard", "ExtraItems")
HOLOGUISE = ItemData(31, "Hologuise", "Gadgets")
PDA = ItemData(32, "PDA", "Gadgets")
MAP_O_MATIC = ItemData(33, "Map-o-Matic", "ExtraItems")
BOLT_GRABBER = ItemData(34, "Bolt Grabber", "ExtraItems")
PERSUADER = ItemData(35, "Persuader", "ExtraItems")

ZOOMERATOR = ItemData(48, "Zoomerator", "ExtraItems")
RARITANIUM = ItemData(49, "Raritanium", "ExtraItems")
CODEBOT = ItemData(50, "Codebot", "ExtraItems")
PREMIUM_NANOTECH = ItemData(52, "Premium nanotech", "ExtraItems")
ULTRA_NANOTECH = ItemData(53, "Ultra nanotech", "ExtraItems")

GOLDEN_SUCK_CANNON = ItemData(309, "Golden Suck Cannon", "GoldenWeapons")
GOLDEN_BOMB_GLOVE = ItemData(310, "Golden Bomb glove", "GoldenWeapons")
GOLDEN_DEVASTATOR = ItemData(311, "Golden Devastator", "GoldenWeapons")
GOLDEN_BLASTER = ItemData(315, "Golden Blaster", "GoldenWeapons")
GOLDEN_PYROCITOR = ItemData(316, "Golden Pyrocitor", "GoldenWeapons")
GOLDEN_MINE_GLOVE = ItemData(317, "Golden Mine glove", "GoldenWeapons")
GOLDEN_TESLA_CLAW = ItemData(319, "Golden Tesla claw", "GoldenWeapons")
GOLDEN_GLOVE_OF_DOOM = ItemData(320, "Golden Glove of doom", "GoldenWeapons")
GOLDEN_MORPH_O_RAY = ItemData(321, "Golden Morph-o-ray", "GoldenWeapons")
GOLDEN_DECOY_GLOVE = ItemData(325, "Golden Decoy glove", "GoldenWeapons")

PROGRESSIVE_PACK = ItemData(80, "Progressive Pack", "Packs")
PROGRESSIVE_HELMET = ItemData(81, "Progressive Helmet", "Helmets")
PROGRESSIVE_SUCK = ItemData(82, "Progressive Suck Cannon", "Weapons")
PROGRESSIVE_BOMB = ItemData(83, "Progressive Bomb glove", "Weapons")
PROGRESSIVE_DEVASTATOR = ItemData(84, "Progressive Devastator", "Weapons")
PROGRESSIVE_BLASTER = ItemData(85, "Progressive Blaster", "Weapons")
PROGRESSIVE_PYROCITOR = ItemData(86, "Progressive Pyrocitor", "Weapons")
PROGRESSIVE_MINE = ItemData(87, "Progressive Mine glove", "Weapons")
PROGRESSIVE_TESLA = ItemData(88, "Progressive Tesla claw", "Weapons")
PROGRESSIVE_DOOM = ItemData(89, "Progressive Glove of doom", "Weapons")
PROGRESSIVE_MORPH = ItemData(90, "Progressive Morph-o-ray", "Weapons")
PROGRESSIVE_DECOY = ItemData(91, "Progressive Decoy glove", "Weapons")
PROGRESSIVE_BOOT = ItemData(92, "Progressive Boots", "Boots")
PROGRESSIVE_HOVERBOARD = ItemData(93, "Progressive Hoverboard", "ExtraItems")
PROGRESSIVE_TRADE = ItemData(94, "Progressive Raritanium", "ExtraItems")
PROGRESSIVE_NANOTECH = ItemData(95, "Progressive Nanotech", "ExtraItems")

NOVALIS_INFOBOT = ItemData(101, "Novalis", "Infobots")
ARIDIA_INFOBOT = ItemData(102, "Aridia", "Infobots")
KERWAN_INFOBOT = ItemData(103, "Kerwan", "Infobots")
EUDORA_INFOBOT = ItemData(104, "Eudora", "Infobots")
RILGAR_INFOBOT = ItemData(105, "Rilgar", "Infobots")
BLARG_INFOBOT = ItemData(106, "Blarg", "Infobots")
UMBRIS_INFOBOT = ItemData(107, "Umbris", "Infobots")
BATALIA_INFOBOT = ItemData(108, "Batalia", "Infobots")
GASPAR_INFOBOT = ItemData(109, "Gaspar", "Infobots")
ORXON_INFOBOT = ItemData(110, "Orxon", "Infobots")
POKITARU_INFOBOT = ItemData(111, "Pokitaru", "Infobots")
HOVEN_INFOBOT = ItemData(112, "Hoven", "Infobots")
GEMLIK_INFOBOT = ItemData(113, "Gemlik", "Infobots")
OLTANIS_INFOBOT = ItemData(114, "Oltanis", "Infobots")
QUARTU_INFOBOT = ItemData(115, "Quartu", "Infobots")
KALEBO_INFOBOT = ItemData(116, "Kalebo III", "Infobots")
FLEET_INFOBOT = ItemData(117, "Drek's Fleet", "Infobots")
VELDIN_INFOBOT = ItemData(118, "Veldin", "Infobots")

TAKE_AIM = ItemData(200, "Take Aim: Skill Point", "Skillpoint")
SWING_IT = ItemData(201, "Swing it!: Skill Point", "Skillpoint")
TRANSPORTED = ItemData(202, "Transported: Skill Point", "Skillpoint")
STRIKE_A_POSE = ItemData(203, "Strike a pose: Skill Point", "Skillpoint")
BLIMPY = ItemData(204, "Blimpy: Skill Point", "Skillpoint")
QWARKTASTIC = ItemData(205, "Qwarktastic: Skill Point", "Skillpoint")
ANY_TEN = ItemData(206, "Any Ten: Skill Point", "Skillpoint")
TRICKY = ItemData(207, "Tricky: Skill Point", "Skillpoint")
CLUCK_CLUCK = ItemData(208, "Cluck, Cluck: Skill Point", "Skillpoint")
SPEEDY = ItemData(209, "Speedy: Skill Point", "Skillpoint")
GIRL_TROUBLE = ItemData(210, "Girl Trouble: Skill Point", "Skillpoint")
JUMPER = ItemData(211, "Jumper: Skill Point", "Skillpoint")
ACCURACY_COUNTS = ItemData(212, "Accuracy Counts: Skill Point", "Skillpoint")
EAT_LEAD = ItemData(213, "Eat Lead: Skill Point", "Skillpoint")
DESTROYED = ItemData(214, "Destroyed: Skill Point", "Skillpoint")
GUNNER = ItemData(215, "Gunner: Skill Point", "Skillpoint")
SNIPER = ItemData(216, "Sniper: Skill Point", "Skillpoint")
HEY_OVER_HERE = ItemData(217, "Hey, Over Here!: Skill Point", "Skillpoint")
ALIEN_INVASION = ItemData(218, "Alien Invasion: Skill Point", "Skillpoint")
BURIED_TREASURE = ItemData(219, "Buried Treasure: Skill Point", "Skillpoint")
PEST_CONTROL = ItemData(220, "Pest Control: Skill Point", "Skillpoint")
WHIRLYBIRDS = ItemData(221, "Whirlybirds: Skill Point", "Skillpoint")
SITTING_DUCKS = ItemData(222, "Sitting Ducks: Skill Point", "Skillpoint")
SHATTERED_GLASS = ItemData(223, "Shattered Glass: Skill Point", "Skillpoint")
BLAST_EM = ItemData(224, "Blast Em!: Skill Point", "Skillpoint")
HEAVY_TRAFFIC = ItemData(225, "Heavy Traffic: Skill Point", "Skillpoint")
MAGICIAN = ItemData(226, "Magician: Skill Point", "Skillpoint")
SNEAKY = ItemData(227, "Sneaky: Skill Point", "Skillpoint")
CAREFUL_CRUISE = ItemData(228, "Careful Cruise: Skill Point", "Skillpoint")
GOING_COMMANDO = ItemData(229, "Going Commando: Skill Point", "Skillpoint")


@dataclass
class CollectableData(ItemData):
    max_capacity: int = 0x7F


# Collectables
GOLD_BOLT = ItemData(261, "Generic Gold Bolt", "GoldBolts")
GOLD_BOLT_1 = ItemData(262, "1 Gold Bolt", "GoldBolts", 1)
GOLD_BOLT_2 = ItemData(263, "2 Gold Bolts", "GoldBolts", 2)
GOLD_BOLT_3 = ItemData(264, "3 Gold Bolts", "GoldBolts", 3)
GOLD_BOLT_4 = ItemData(265, "4 Gold Bolts", "GoldBolts", 4)
GOLD_BOLT_5 = ItemData(266, "5 Gold Bolts", "GoldBolts", 5)
GOLD_BOLT_6 = ItemData(267, "6 Gold Bolts", "GoldBolts", 6)
GOLD_BOLT_7 = ItemData(268, "7 Gold Bolts", "GoldBolts", 7)
GOLD_BOLT_8 = ItemData(269, "8 Gold Bolts", "GoldBolts", 8)
GOLD_BOLT_9 = ItemData(270, "9 Gold Bolts", "GoldBolts", 9)
GOLD_BOLT_10 = ItemData(271, "10 Gold Bolts", "GoldBolts", 10)
GOLD_BOLT_11 = ItemData(272, "11 Gold Bolts", "GoldBolts", 11)
GOLD_BOLT_12 = ItemData(273, "12 Gold Bolts", "GoldBolts", 12)
GOLD_BOLT_13 = ItemData(274, "13 Gold Bolts", "GoldBolts", 13)
GOLD_BOLT_14 = ItemData(275, "14 Gold Bolts", "GoldBolts", 14)
GOLD_BOLT_15 = ItemData(276, "15 Gold Bolts", "GoldBolts", 15)
GOLD_BOLT_16 = ItemData(277, "16 Gold Bolts", "GoldBolts", 16)
GOLD_BOLT_17 = ItemData(278, "17 Gold Bolts", "GoldBolts", 17)
GOLD_BOLT_18 = ItemData(279, "18 Gold Bolts", "GoldBolts", 18)
GOLD_BOLT_19 = ItemData(280, "19 Gold Bolts", "GoldBolts", 19)
GOLD_BOLT_20 = ItemData(281, "20 Gold Bolts", "GoldBolts", 20)
GOLD_BOLT_21 = ItemData(282, "21 Gold Bolts", "GoldBolts", 21)
GOLD_BOLT_22 = ItemData(283, "22 Gold Bolts", "GoldBolts", 22)
GOLD_BOLT_23 = ItemData(284, "23 Gold Bolts", "GoldBolts", 23)
GOLD_BOLT_24 = ItemData(285, "24 Gold Bolts", "GoldBolts", 24)
GOLD_BOLT_25 = ItemData(286, "25 Gold Bolts", "GoldBolts", 25)
GOLD_BOLT_26 = ItemData(287, "26 Gold Bolts", "GoldBolts", 26)
GOLD_BOLT_27 = ItemData(288, "27 Gold Bolts", "GoldBolts", 27)
GOLD_BOLT_28 = ItemData(289, "28 Gold Bolts", "GoldBolts", 28)
GOLD_BOLT_29 = ItemData(290, "29 Gold Bolts", "GoldBolts", 29)
GOLD_BOLT_30 = ItemData(291, "30 Gold Bolts", "GoldBolts", 30)
GOLD_BOLT_31 = ItemData(292, "31 Gold Bolts", "GoldBolts", 31)
GOLD_BOLT_32 = ItemData(293, "32 Gold Bolts", "GoldBolts", 32)
GOLD_BOLT_33 = ItemData(294, "33 Gold Bolts", "GoldBolts", 33)
GOLD_BOLT_34 = ItemData(295, "34 Gold Bolts", "GoldBolts", 34)
GOLD_BOLT_35 = ItemData(296, "35 Gold Bolts", "GoldBolts", 35)
GOLD_BOLT_36 = ItemData(297, "36 Gold Bolts", "GoldBolts", 36)
GOLD_BOLT_37 = ItemData(298, "37 Gold Bolts", "GoldBolts", 37)
GOLD_BOLT_38 = ItemData(299, "38 Gold Bolts", "GoldBolts", 38)
GOLD_BOLT_39 = ItemData(300, "39 Gold Bolts", "GoldBolts", 39)
GOLD_BOLT_40 = ItemData(301, "40 Gold Bolts", "GoldBolts", 40)

BOLT_PACK = ItemData(302, "Generic Bolt Pack", "Filler")
BOLT_PACK_0 = ItemData(400, "Nothing", "Filler", 0)
BOLT_PACK_1 = ItemData(401, "A single bolt", "Filler", 1)
BOLT_PACK_2 = ItemData(402, "10 bolts", "Filler", 10)
BOLT_PACK_3 = ItemData(403, "100 bolts", "Filler", 100)
BOLT_PACK_4 = ItemData(404, "250 bolts", "Filler", 250)
BOLT_PACK_5 = ItemData(405, "500 bolts", "Filler", 500)
BOLT_PACK_6 = ItemData(406, "750 bolts", "Filler", 750)
BOLT_PACK_7 = ItemData(407, "1,000 bolts", "Filler", 1000)
BOLT_PACK_8 = ItemData(408, "2,000 bolts", "Filler", 2000)
BOLT_PACK_9 = ItemData(409, "3,000 bolts", "Filler", 3000)
BOLT_PACK_10 = ItemData(410, "4,000 bolts", "Filler", 4000)
BOLT_PACK_11 = ItemData(411, "5,000 bolts", "Filler", 5000)
BOLT_PACK_12 = ItemData(412, "6,000 bolts", "Filler", 6000)
BOLT_PACK_13 = ItemData(413, "7,000 bolts", "Filler", 7000)
BOLT_PACK_14 = ItemData(414, "8,000 bolts", "Filler", 8000)
BOLT_PACK_15 = ItemData(415, "9,000 bolts", "Filler", 9000)
BOLT_PACK_16 = ItemData(416, "10,000 bolts", "Filler", 10000)
BOLT_PACK_17 = ItemData(417, "12,500 bolts", "Filler", 12500)
BOLT_PACK_18 = ItemData(418, "15,000 bolts", "Filler", 15000)
BOLT_PACK_19 = ItemData(419, "17,500 bolts", "Filler", 17500)
BOLT_PACK_20 = ItemData(420, "20,000 bolts", "Filler", 20000)
BOLT_PACK_21 = ItemData(421, "25,000 bolts", "Filler", 25000)
BOLT_PACK_22 = ItemData(422, "30,000 bolts", "Filler", 30000)
BOLT_PACK_23 = ItemData(423, "40,000 bolts", "Filler", 40000)
BOLT_PACK_24 = ItemData(424, "50,000 bolts", "Filler", 50000)
BOLT_PACK_25 = ItemData(425, "75,000 bolts", "Filler", 75000)
BOLT_PACK_26 = ItemData(426, "100,000 bolts", "Filler", 100000)

WEAPONS: Sequence[ItemData] = [
    TAUNTER,
    VISIBOMB,
    WALLOPER,
    RYNO,
    DRONE_DEVICE,
]

NON_PROGRESSIVE_WEAPONS: Sequence[ItemData] = [
    SUCK_CANNON,
    BOMB_GLOVE,
    DEVASTATOR,
    BLASTER,
    PYROCITOR,
    MINE_GLOVE,
    TESLA_CLAW,
    GLOVE_OF_DOOM,
    MORPH_O_RAY,
    DECOY_GLOVE,
]

PROGRESSIVE_WEAPONS: Sequence[ItemData] = [
    PROGRESSIVE_SUCK,
    PROGRESSIVE_BOMB,
    PROGRESSIVE_DEVASTATOR,
    PROGRESSIVE_BLASTER,
    PROGRESSIVE_PYROCITOR,
    PROGRESSIVE_MINE,
    PROGRESSIVE_TESLA,
    PROGRESSIVE_DOOM,
    PROGRESSIVE_MORPH,
    PROGRESSIVE_DECOY,
]

GOLDEN_WEAPONS: Sequence[ItemData] = [
    GOLDEN_SUCK_CANNON,
    GOLDEN_BOMB_GLOVE,
    GOLDEN_DEVASTATOR,
    GOLDEN_BLASTER,
    GOLDEN_PYROCITOR,
    GOLDEN_MINE_GLOVE,
    GOLDEN_TESLA_CLAW,
    GOLDEN_GLOVE_OF_DOOM,
    GOLDEN_MORPH_O_RAY,
    GOLDEN_DECOY_GLOVE,
]

PROGRESSIVE_GOLDEN_WEAPONS: Sequence[ItemData] = [
    GOLDEN_SUCK_CANNON,
    GOLDEN_BOMB_GLOVE,
    GOLDEN_DEVASTATOR,
    GOLDEN_BLASTER,
    GOLDEN_PYROCITOR,
    GOLDEN_MINE_GLOVE,
    GOLDEN_TESLA_CLAW,
    GOLDEN_GLOVE_OF_DOOM,
    GOLDEN_MORPH_O_RAY,
    GOLDEN_DECOY_GLOVE,
]

GADGETS: Sequence[ItemData] = [
    HYDRODISPLACER,
    TRESPASSER,
    METAL_DETECTOR,
    HOLOGUISE,
    PDA,
    SWINGSHOT,
]

PACKS: Sequence[ItemData] = [
    HELI_PACK,
    THRUSTER_PACK,
    HYDRO_PACK,
]

PROGRESSIVE_PACKS: Sequence[ItemData] = [
    *[PROGRESSIVE_PACK] * 3,
]

HELMETS: Sequence[ItemData] = [
    SONIC_SUMMONER,
    O2_MASK,
    PILOTS_HELMET,
]

PROGRESSIVE_HELMETS: Sequence[ItemData] = [
    *[PROGRESSIVE_HELMET] * 3,
]

BOOTS: Sequence[ItemData] = [
    MAGNEBOOTS,
    GRINDBOOTS,
]

PROGRESSIVE_BOOTS: Sequence[ItemData] = [
    *[PROGRESSIVE_BOOT] * 2,
]

EXTRA_ITEMS: Sequence[ItemData] = [
    MAP_O_MATIC,
    BOLT_GRABBER,
    CODEBOT,
]

NON_PROGRESSIVE_HOVERBOARDS: Sequence[ItemData] = [
    HOVERBOARD,
    ZOOMERATOR,
]

PROGRESSIVE_HOVERBOARDS: Sequence[ItemData] = [
    *[PROGRESSIVE_HOVERBOARD] * 2,
]

NON_PROGRESSIVE_TRADES: Sequence[ItemData] = [
    PERSUADER,
    RARITANIUM,
]

PROGRESSIVE_TRADES: Sequence[ItemData] = [
    *[PROGRESSIVE_TRADE] * 2,
]

NON_PROGRESSIVE_NANOTECHS: Sequence[ItemData] = [
    PREMIUM_NANOTECH,
    ULTRA_NANOTECH,
]

PROGRESSIVE_NANOTECHS: Sequence[ItemData] = [
    *[PROGRESSIVE_NANOTECH] * 2,
]

GOLD_BOLTS: Sequence[ItemData] = [
    GOLD_BOLT,
    GOLD_BOLT_1,
    GOLD_BOLT_2,
    GOLD_BOLT_3,
    GOLD_BOLT_4,
    GOLD_BOLT_5,
    GOLD_BOLT_6,
    GOLD_BOLT_7,
    GOLD_BOLT_8,
    GOLD_BOLT_9,
    GOLD_BOLT_10,
    GOLD_BOLT_11,
    GOLD_BOLT_12,
    GOLD_BOLT_13,
    GOLD_BOLT_14,
    GOLD_BOLT_15,
    GOLD_BOLT_16,
    GOLD_BOLT_17,
    GOLD_BOLT_18,
    GOLD_BOLT_19,
    GOLD_BOLT_20,
    GOLD_BOLT_21,
    GOLD_BOLT_22,
    GOLD_BOLT_23,
    GOLD_BOLT_24,
    GOLD_BOLT_25,
    GOLD_BOLT_26,
    GOLD_BOLT_27,
    GOLD_BOLT_28,
    GOLD_BOLT_29,
    GOLD_BOLT_30,
    GOLD_BOLT_31,
    GOLD_BOLT_32,
    GOLD_BOLT_33,
    GOLD_BOLT_34,
    GOLD_BOLT_35,
    GOLD_BOLT_36,
    GOLD_BOLT_37,
    GOLD_BOLT_38,
    GOLD_BOLT_39,
    GOLD_BOLT_40,
]

BOLT_PACKS: Sequence[ItemData] = [
    BOLT_PACK,
    BOLT_PACK_0,
    BOLT_PACK_1,
    BOLT_PACK_2,
    BOLT_PACK_3,
    BOLT_PACK_4,
    BOLT_PACK_5,
    BOLT_PACK_6,
    BOLT_PACK_7,
    BOLT_PACK_8,
    BOLT_PACK_9,
    BOLT_PACK_10,
    BOLT_PACK_11,
    BOLT_PACK_12,
    BOLT_PACK_13,
    BOLT_PACK_14,
    BOLT_PACK_15,
    BOLT_PACK_16,
    BOLT_PACK_17,
    BOLT_PACK_18,
    BOLT_PACK_19,
    BOLT_PACK_20,
    BOLT_PACK_21,
    BOLT_PACK_22,
    BOLT_PACK_23,
    BOLT_PACK_24,
    BOLT_PACK_25,
    BOLT_PACK_26,
]

PLANETS: Sequence[ItemData] = [
    NOVALIS_INFOBOT,
    ARIDIA_INFOBOT,
    KERWAN_INFOBOT,
    EUDORA_INFOBOT,
    RILGAR_INFOBOT,
    BLARG_INFOBOT,
    UMBRIS_INFOBOT,
    BATALIA_INFOBOT,
    GASPAR_INFOBOT,
    ORXON_INFOBOT,
    POKITARU_INFOBOT,
    HOVEN_INFOBOT,
    GEMLIK_INFOBOT,
    OLTANIS_INFOBOT,
    QUARTU_INFOBOT,
    KALEBO_INFOBOT,
    FLEET_INFOBOT,
    VELDIN_INFOBOT,
]

STARTING_PLANETS: Sequence[ItemData] = [
    NOVALIS_INFOBOT,
    KERWAN_INFOBOT,
    BLARG_INFOBOT,
    BATALIA_INFOBOT,
    ORXON_INFOBOT,
]

SKILLPOINTS: Sequence[ItemData] = [
    TAKE_AIM,
    SWING_IT,
    TRANSPORTED,
    STRIKE_A_POSE,
    BLIMPY,
    QWARKTASTIC,
    ANY_TEN,
    TRICKY,
    CLUCK_CLUCK,
    SPEEDY,
    GIRL_TROUBLE,
    JUMPER,
    ACCURACY_COUNTS,
    EAT_LEAD,
    DESTROYED,
    GUNNER,
    SNIPER,
    HEY_OVER_HERE,
    ALIEN_INVASION,
    BURIED_TREASURE,
    PEST_CONTROL,
    WHIRLYBIRDS,
    SITTING_DUCKS,
    SHATTERED_GLASS,
    BLAST_EM,
    HEAVY_TRAFFIC,
    MAGICIAN,
    SNEAKY,
    CAREFUL_CRUISE,
    GOING_COMMANDO,
]

ALL: Sequence[ItemData] = [*WEAPONS, *NON_PROGRESSIVE_WEAPONS, *PROGRESSIVE_WEAPONS, *GOLDEN_WEAPONS,
                           *GADGETS, *PACKS, *PROGRESSIVE_PACKS, *HELMETS, *PROGRESSIVE_HELMETS, *BOOTS,
                           *PROGRESSIVE_BOOTS, *EXTRA_ITEMS, *NON_PROGRESSIVE_HOVERBOARDS, *PROGRESSIVE_HOVERBOARDS,
                           *NON_PROGRESSIVE_TRADES, *PROGRESSIVE_TRADES, *NON_PROGRESSIVE_NANOTECHS,
                           *PROGRESSIVE_NANOTECHS, *GOLD_BOLTS, *PLANETS, *SKILLPOINTS, *BOLT_PACKS]

ITEM_POOL: Sequence[ItemData] = [*PLANETS, *WEAPONS, *GADGETS, *EXTRA_ITEMS]  # *SKILLPOINTS

STARTING_WEAPONS: Sequence[ItemData] = [*WEAPONS, *NON_PROGRESSIVE_WEAPONS, *PROGRESSIVE_WEAPONS,
                                        *PROGRESSIVE_GOLDEN_WEAPONS]
ALL_WEAPONS: Sequence[ItemData] = [*STARTING_WEAPONS, *GOLDEN_WEAPONS]
ALL_PACKS: Sequence[ItemData] = [*PACKS, *PROGRESSIVE_PACKS]
ALL_HELMETS: Sequence[ItemData] = [*HELMETS, *PROGRESSIVE_HELMETS]
ALL_BOOTS: Sequence[ItemData] = [*BOOTS, *PROGRESSIVE_BOOTS]
ALL_EXTRA_ITEMS: Sequence[ItemData] = [*EXTRA_ITEMS, *NON_PROGRESSIVE_HOVERBOARDS, *PROGRESSIVE_HOVERBOARDS,
                                       *NON_PROGRESSIVE_TRADES, *PROGRESSIVE_TRADES, *NON_PROGRESSIVE_NANOTECHS,
                                       *PROGRESSIVE_NANOTECHS]
ALL_HOVERBOARD: Sequence[ItemData] = [*NON_PROGRESSIVE_HOVERBOARDS, *PROGRESSIVE_HOVERBOARDS]
ALL_TRADE: Sequence[ItemData] = [*NON_PROGRESSIVE_TRADES, *PROGRESSIVE_TRADES]
ALL_NANOTECH: Sequence[ItemData] = [*NON_PROGRESSIVE_NANOTECHS, *PROGRESSIVE_NANOTECHS]
ALL_STARTING: Sequence[ItemData] = [*STARTING_WEAPONS, *GADGETS]

SUCK_GROUP: Sequence[ItemData] = [SUCK_CANNON, GOLDEN_SUCK_CANNON, PROGRESSIVE_SUCK]
BOMB_GROUP: Sequence[ItemData] = [BOMB_GLOVE, GOLDEN_BOMB_GLOVE, PROGRESSIVE_BOMB]
DEVASTATOR_GROUP: Sequence[ItemData] = [DEVASTATOR, GOLDEN_DEVASTATOR, PROGRESSIVE_DEVASTATOR]
BLASTER_GROUP: Sequence[ItemData] = [BLASTER, GOLDEN_BLASTER, PROGRESSIVE_BLASTER]
PYROCITOR_GROUP: Sequence[ItemData] = [PYROCITOR, GOLDEN_PYROCITOR, PROGRESSIVE_PYROCITOR]
MINE_GROUP: Sequence[ItemData] = [MINE_GLOVE, GOLDEN_MINE_GLOVE, PROGRESSIVE_MINE]
TESLA_GROUP: Sequence[ItemData] = [TESLA_CLAW, GOLDEN_TESLA_CLAW, PROGRESSIVE_TESLA]
DOOM_GROUP: Sequence[ItemData] = [GLOVE_OF_DOOM, GOLDEN_GLOVE_OF_DOOM, PROGRESSIVE_DOOM]
MORPH_GROUP: Sequence[ItemData] = [MORPH_O_RAY, GOLDEN_MORPH_O_RAY, PROGRESSIVE_MORPH]
DECOY_GROUP: Sequence[ItemData] = [DECOY_GLOVE, GOLDEN_DECOY_GLOVE, PROGRESSIVE_DECOY]

PROG: dict[str, Mapping[str, int]] = {
    HELI_PACK.name: {HELI_PACK.name: 1},
    THRUSTER_PACK.name: {THRUSTER_PACK.name: 1},
    HYDRO_PACK.name: {HYDRO_PACK.name: 1},
    SONIC_SUMMONER.name: {SONIC_SUMMONER.name: 1, PROGRESSIVE_HELMET.name: 2},
    O2_MASK.name: {O2_MASK.name: 1, PROGRESSIVE_HELMET.name: 1},
    PILOTS_HELMET.name: {PILOTS_HELMET.name: 1, PROGRESSIVE_HELMET.name: 3},
    SUCK_CANNON.name: {SUCK_CANNON.name: 1},
    GOLDEN_SUCK_CANNON.name: {SUCK_CANNON.name: 1, GOLDEN_SUCK_CANNON.name: 1},
    BOMB_GLOVE.name: {BOMB_GLOVE.name: 1},
    GOLDEN_BOMB_GLOVE.name: {BOMB_GLOVE.name: 1, GOLDEN_BOMB_GLOVE.name: 1},
    DEVASTATOR.name: {DEVASTATOR.name: 1},
    GOLDEN_DEVASTATOR.name: {DEVASTATOR.name: 1, GOLDEN_DEVASTATOR.name: 1},
    BLASTER.name: {BLASTER.name: 1},
    GOLDEN_BLASTER.name: {BLASTER.name: 1, GOLDEN_BLASTER.name: 1},
    PYROCITOR.name: {PYROCITOR.name: 1},
    GOLDEN_PYROCITOR.name: {PYROCITOR.name: 1, GOLDEN_PYROCITOR.name: 1},
    MINE_GLOVE.name: {MINE_GLOVE.name: 1},
    GOLDEN_MINE_GLOVE.name: {MINE_GLOVE.name: 1, GOLDEN_MINE_GLOVE.name: 1},
    TESLA_CLAW.name: {TESLA_CLAW.name: 1},
    GOLDEN_TESLA_CLAW.name: {TESLA_CLAW.name: 1, GOLDEN_TESLA_CLAW.name: 1},
    GLOVE_OF_DOOM.name: {GLOVE_OF_DOOM.name: 1},
    GOLDEN_GLOVE_OF_DOOM.name: {GLOVE_OF_DOOM.name: 1, GOLDEN_GLOVE_OF_DOOM.name: 1},
    MORPH_O_RAY.name: {MORPH_O_RAY.name: 1},
    GOLDEN_MORPH_O_RAY.name: {MORPH_O_RAY.name: 1, GOLDEN_MORPH_O_RAY.name: 1},
    DECOY_GLOVE.name: {DECOY_GLOVE.name: 1},
    GOLDEN_DECOY_GLOVE.name: {DECOY_GLOVE.name: 1, GOLDEN_DECOY_GLOVE.name: 1},
    MAGNEBOOTS.name: {MAGNEBOOTS.name: 1, PROGRESSIVE_BOOT.name: 2},
    GRINDBOOTS.name: {GRINDBOOTS.name: 1, PROGRESSIVE_BOOT.name: 1},
    HOVERBOARD.name: {HOVERBOARD.name: 1, PROGRESSIVE_HOVERBOARD.name: 1},
    ZOOMERATOR.name: {ZOOMERATOR.name: 1, PROGRESSIVE_HOVERBOARD.name: 2},
    PERSUADER.name: {PERSUADER.name: 1, PROGRESSIVE_TRADE.name: 1},
    RARITANIUM.name: {RARITANIUM.name: 1, PROGRESSIVE_TRADE.name: 2},
    PREMIUM_NANOTECH.name: {PREMIUM_NANOTECH.name: 1, PROGRESSIVE_NANOTECH.name: 1},
    ULTRA_NANOTECH.name: {ULTRA_NANOTECH.name: 1, PROGRESSIVE_NANOTECH.name: 2},
}


def get_bolt_pack(options: Options) -> str:
    lookup: dict[int, str] = {
        BOLT_PACK_0.quantity: BOLT_PACK_0.name,
        BOLT_PACK_1.quantity: BOLT_PACK_1.name,
        BOLT_PACK_2.quantity: BOLT_PACK_2.name,
        BOLT_PACK_3.quantity: BOLT_PACK_3.name,
        BOLT_PACK_4.quantity: BOLT_PACK_4.name,
        BOLT_PACK_5.quantity: BOLT_PACK_5.name,
        BOLT_PACK_6.quantity: BOLT_PACK_6.name,
        BOLT_PACK_7.quantity: BOLT_PACK_7.name,
        BOLT_PACK_8.quantity: BOLT_PACK_8.name,
        BOLT_PACK_9.quantity: BOLT_PACK_9.name,
        BOLT_PACK_10.quantity: BOLT_PACK_10.name,
        BOLT_PACK_11.quantity: BOLT_PACK_11.name,
        BOLT_PACK_12.quantity: BOLT_PACK_12.name,
        BOLT_PACK_13.quantity: BOLT_PACK_13.name,
        BOLT_PACK_14.quantity: BOLT_PACK_14.name,
        BOLT_PACK_15.quantity: BOLT_PACK_15.name,
        BOLT_PACK_16.quantity: BOLT_PACK_16.name,
        BOLT_PACK_17.quantity: BOLT_PACK_17.name,
        BOLT_PACK_18.quantity: BOLT_PACK_18.name,
        BOLT_PACK_19.quantity: BOLT_PACK_19.name,
        BOLT_PACK_20.quantity: BOLT_PACK_20.name,
        BOLT_PACK_21.quantity: BOLT_PACK_21.name,
        BOLT_PACK_22.quantity: BOLT_PACK_22.name,
        BOLT_PACK_23.quantity: BOLT_PACK_23.name,
        BOLT_PACK_24.quantity: BOLT_PACK_24.name,
        BOLT_PACK_25.quantity: BOLT_PACK_25.name,
        BOLT_PACK_26.quantity: BOLT_PACK_26.name,
    }
    return lookup[options.pack_size_bolts.value]


def get_gold_bolts(options: Options) -> str:
    lookup: dict[int, str] = {}
    for gold_bolt in GOLD_BOLTS:
        if gold_bolt.name.startswith("Generic"):
            continue
        lookup.update({gold_bolt.quantity: gold_bolt.name})
    return lookup[options.pack_size_gold_bolts.value]


def progression_rules(world):
    match world.options.progressive_weapons.value:
        case Options.GoldenWeaponProgression.option_normal:
            PROG[SUCK_CANNON.name] = {SUCK_CANNON.name: 1, GOLDEN_SUCK_CANNON.name: 1}
            PROG[GOLDEN_SUCK_CANNON.name] = {GOLDEN_SUCK_CANNON.name: 1}
            PROG[BOMB_GLOVE.name] = {BOMB_GLOVE.name: 1, GOLDEN_BOMB_GLOVE.name: 1}
            PROG[GOLDEN_BOMB_GLOVE.name] = {GOLDEN_BOMB_GLOVE.name: 1}
            PROG[DEVASTATOR.name] = {DEVASTATOR.name: 1, GOLDEN_DEVASTATOR.name: 1}
            PROG[GOLDEN_DEVASTATOR.name] = {GOLDEN_DEVASTATOR.name: 1}
            PROG[BLASTER.name] = {BLASTER.name: 1, GOLDEN_BLASTER.name: 1}
            PROG[GOLDEN_BLASTER.name] = {GOLDEN_BLASTER.name: 1}
            PROG[PYROCITOR.name] = {PYROCITOR.name: 1, GOLDEN_PYROCITOR.name: 1}
            PROG[GOLDEN_PYROCITOR.name] = {GOLDEN_PYROCITOR.name: 1}
            PROG[MINE_GLOVE.name] = {MINE_GLOVE.name: 1, GOLDEN_MINE_GLOVE.name: 1}
            PROG[GOLDEN_MINE_GLOVE.name] = {GOLDEN_MINE_GLOVE.name: 1}
            PROG[TESLA_CLAW.name] = {TESLA_CLAW.name: 1, GOLDEN_TESLA_CLAW.name: 1}
            PROG[GOLDEN_TESLA_CLAW.name] = {GOLDEN_TESLA_CLAW.name: 1}
            PROG[GLOVE_OF_DOOM.name] = {GLOVE_OF_DOOM.name: 1, GOLDEN_GLOVE_OF_DOOM.name: 1}
            PROG[GOLDEN_GLOVE_OF_DOOM.name] = {GOLDEN_GLOVE_OF_DOOM.name: 1}
            PROG[MORPH_O_RAY.name] = {MORPH_O_RAY.name: 1, GOLDEN_MORPH_O_RAY.name: 1}
            PROG[GOLDEN_MORPH_O_RAY.name] = {GOLDEN_MORPH_O_RAY.name: 1}
            PROG[DECOY_GLOVE.name] = {DECOY_GLOVE.name: 1, GOLDEN_DECOY_GLOVE.name: 1}
            PROG[GOLDEN_DECOY_GLOVE.name] = {GOLDEN_DECOY_GLOVE.name: 1}
        case Options.GoldenWeaponProgression.option_progressive:
            PROG[SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 1}
            PROG[GOLDEN_SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 2}
            PROG[BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 1}
            PROG[GOLDEN_BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 2}
            PROG[DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 1}
            PROG[GOLDEN_DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 2}
            PROG[BLASTER.name] = {PROGRESSIVE_BLASTER.name: 1}
            PROG[GOLDEN_BLASTER.name] = {PROGRESSIVE_BLASTER.name: 2}
            PROG[PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 1}
            PROG[GOLDEN_PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 2}
            PROG[MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 1}
            PROG[GOLDEN_MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 2}
            PROG[TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 1}
            PROG[GOLDEN_TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 2}
            PROG[GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 1}
            PROG[GOLDEN_GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 2}
            PROG[MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 1}
            PROG[GOLDEN_MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 2}
            PROG[DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 1}
            PROG[GOLDEN_DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 2}
        case Options.GoldenWeaponProgression.option_progressive_reversed:
            world.orders["progressive_suck_cannon_order"].reverse()
            PROG[SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 1}
            PROG[GOLDEN_SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 1}
            world.orders["progressive_bomb_glove_order"].reverse()
            PROG[BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 1}
            PROG[GOLDEN_BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 1}
            world.orders["progressive_devastator_order"].reverse()
            PROG[DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 1}
            PROG[GOLDEN_DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 1}
            world.orders["progressive_blaster_order"].reverse()
            PROG[BLASTER.name] = {PROGRESSIVE_BLASTER.name: 1}
            PROG[GOLDEN_BLASTER.name] = {PROGRESSIVE_BLASTER.name: 1}
            world.orders["progressive_pyrocitor_order"].reverse()
            PROG[PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 1}
            PROG[GOLDEN_PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 1}
            world.orders["progressive_mine_glove_order"].reverse()
            PROG[MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 1}
            PROG[GOLDEN_MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 1}
            world.orders["progressive_tesla_claw_order"].reverse()
            PROG[TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 1}
            PROG[GOLDEN_TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 1}
            world.orders["progressive_glove_of_doom_order"].reverse()
            PROG[GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 1}
            PROG[GOLDEN_GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 1}
            world.orders["progressive_morph_o_ray_order"].reverse()
            PROG[MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 1}
            PROG[GOLDEN_MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 1}
            world.orders["progressive_decoy_glove_order"].reverse()
            PROG[DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 1}
            PROG[GOLDEN_DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 1}
        case Options.GoldenWeaponProgression.option_progressive_random:
            world.random.shuffle(world.orders["progressive_suck_cannon_order"])
            PROG[SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 1}
            PROG[GOLDEN_SUCK_CANNON.name] = {PROGRESSIVE_SUCK.name: 1 + world.orders[
                "progressive_suck_cannon_order"].index(GOLDEN_SUCK_CANNON.item_id)}
            world.random.shuffle(world.orders["progressive_bomb_glove_order"])
            PROG[BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 1}
            PROG[GOLDEN_BOMB_GLOVE.name] = {PROGRESSIVE_BOMB.name: 1 + world.orders[
                "progressive_bomb_glove_order"].index(GOLDEN_BOMB_GLOVE.item_id)}
            world.random.shuffle(world.orders["progressive_devastator_order"])
            PROG[DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 1}
            PROG[GOLDEN_DEVASTATOR.name] = {PROGRESSIVE_DEVASTATOR.name: 1 + world.orders[
                "progressive_devastator_order"].index(GOLDEN_DEVASTATOR.item_id)}
            world.random.shuffle(world.orders["progressive_blaster_order"])
            PROG[BLASTER.name] = {PROGRESSIVE_BLASTER.name: 1}
            PROG[GOLDEN_BLASTER.name] = {PROGRESSIVE_BLASTER.name: 1 + world.orders[
                "progressive_blaster_order"].index(GOLDEN_BLASTER.item_id)}
            world.random.shuffle(world.orders["progressive_pyrocitor_order"])
            PROG[PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 1}
            PROG[GOLDEN_PYROCITOR.name] = {PROGRESSIVE_PYROCITOR.name: 1 + world.orders[
                "progressive_pyrocitor_order"].index(GOLDEN_PYROCITOR.item_id)}
            world.random.shuffle(world.orders["progressive_mine_glove_order"])
            PROG[MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 1}
            PROG[GOLDEN_MINE_GLOVE.name] = {PROGRESSIVE_MINE.name: 1 + world.orders[
                "progressive_mine_glove_order"].index(GOLDEN_MINE_GLOVE.item_id)}
            world.random.shuffle(world.orders["progressive_tesla_claw_order"])
            PROG[TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 1}
            PROG[GOLDEN_TESLA_CLAW.name] = {PROGRESSIVE_TESLA.name: 1 + world.orders[
                "progressive_tesla_claw_order"].index(TESLA_CLAW.item_id)}
            world.random.shuffle(world.orders["progressive_glove_of_doom_order"])
            PROG[GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 1}
            PROG[GOLDEN_GLOVE_OF_DOOM.name] = {PROGRESSIVE_DOOM.name: 1 + world.orders[
                "progressive_glove_of_doom_order"].index(GOLDEN_GLOVE_OF_DOOM.item_id)}
            world.random.shuffle(world.orders["progressive_morph_o_ray_order"])
            PROG[MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 1}
            PROG[GOLDEN_MORPH_O_RAY.name] = {PROGRESSIVE_MORPH.name: 1 + world.orders[
                "progressive_morph_o_ray_order"].index(GOLDEN_MORPH_O_RAY.item_id)}
            world.random.shuffle(world.orders["progressive_decoy_glove_order"])
            PROG[DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 1}
            PROG[GOLDEN_DECOY_GLOVE.name] = {PROGRESSIVE_DECOY.name: 1 + world.orders[
                "progressive_decoy_glove_order"].index(GOLDEN_DECOY_GLOVE.item_id)}
        case _:
            pass

    match world.options.progressive_packs.value:
        case Options.ProgressiveOptions.option_progressive:
            PROG[HELI_PACK.name] = {PROGRESSIVE_PACK.name: 1}
            PROG[THRUSTER_PACK.name] = {PROGRESSIVE_PACK.name: 2}
            PROG[HYDRO_PACK.name] = {PROGRESSIVE_PACK.name: 3}
        case Options.ProgressiveOptions.option_progressive_reversed:
            world.orders["progressive_packs_order"].reverse()
            PROG[HELI_PACK.name] = {PROGRESSIVE_PACK.name: 3}
            PROG[THRUSTER_PACK.name] = {PROGRESSIVE_PACK.name: 2}
            PROG[HYDRO_PACK.name] = {PROGRESSIVE_PACK.name: 1}
        case Options.ProgressiveOptions.option_progressive_random:
            world.random.shuffle(world.orders["progressive_packs_order"])
            PROG[HELI_PACK.name] = {
                PROGRESSIVE_PACK.name: 1 + world.orders["progressive_packs_order"].index(HELI_PACK.item_id)}
            PROG[THRUSTER_PACK.name] = {
                PROGRESSIVE_PACK.name: 1 + world.orders["progressive_packs_order"].index(THRUSTER_PACK.item_id)}
            PROG[HYDRO_PACK.name] = {
                PROGRESSIVE_PACK.name: 1 + world.orders["progressive_packs_order"].index(HYDRO_PACK.item_id)}
        case _:
            pass

    match world.options.progressive_helmets.value:
        case Options.ProgressiveOptions.option_progressive:
            PROG[O2_MASK.name] = {PROGRESSIVE_HELMET.name: 1}
            if world.options.shuffle_helmets.value <= Options.ItemOptions.option_random_same:
                PROG[SONIC_SUMMONER.name] = {PROGRESSIVE_HELMET.name: 3}
                PROG[PILOTS_HELMET.name] = {PROGRESSIVE_HELMET.name: 2}
                world.orders["progressive_helmets_order"] = [O2_MASK.item_id, PILOTS_HELMET.item_id,
                                                             SONIC_SUMMONER.item_id]
            else:
                PROG[SONIC_SUMMONER.name] = {PROGRESSIVE_HELMET.name: 2}
                PROG[PILOTS_HELMET.name] = {PROGRESSIVE_HELMET.name: 3}
        case Options.ProgressiveOptions.option_progressive_reversed:
            world.orders["progressive_helmets_order"].reverse()
            PROG[O2_MASK.name] = {PROGRESSIVE_HELMET.name: 3}
            PROG[SONIC_SUMMONER.name] = {PROGRESSIVE_HELMET.name: 2}
            PROG[PILOTS_HELMET.name] = {PROGRESSIVE_HELMET.name: 1}
        case Options.ProgressiveOptions.option_progressive_random:
            world.random.shuffle(world.orders["progressive_helmets_order"])
            PROG[O2_MASK.name] = {
                PROGRESSIVE_HELMET.name: 1 + world.orders["progressive_helmets_order"].index(O2_MASK.item_id)}
            PROG[SONIC_SUMMONER.name] = {
                PROGRESSIVE_HELMET.name: 1 + world.orders["progressive_helmets_order"].index(SONIC_SUMMONER.item_id)}
            PROG[PILOTS_HELMET.name] = {
                PROGRESSIVE_HELMET.name: 1 + world.orders["progressive_helmets_order"].index(PILOTS_HELMET.item_id)}
            if (world.options.shuffle_helmets.value <= Options.ItemOptions.option_random_same and
                    PROG[PILOTS_HELMET.name].values() == 3):
                temp = PROG[PILOTS_HELMET.name]
                PROG[PILOTS_HELMET.name] = PROG[SONIC_SUMMONER.name]
                PROG[SONIC_SUMMONER.name] = temp
                if world.orders["progressive_helmets_order"].index(O2_MASK.item_id) == 0:
                    world.orders["progressive_helmets_order"] = [O2_MASK.item_id, PILOTS_HELMET.item_id,
                                                                 SONIC_SUMMONER.item_id]
                else:
                    world.orders["progressive_helmets_order"] = [PILOTS_HELMET.item_id, O2_MASK.item_id,
                                                                 SONIC_SUMMONER.item_id]

        case _:
            pass

    match world.options.progressive_boots.value:
        case Options.ProgressiveOptions.option_progressive:
            PROG[GRINDBOOTS.name] = {PROGRESSIVE_BOOT.name: 1}
            PROG[MAGNEBOOTS.name] = {PROGRESSIVE_BOOT.name: 2}
        case Options.ProgressiveOptions.option_progressive_reversed:
            world.orders["progressive_boots_order"].reverse()
            PROG[GRINDBOOTS.name] = {PROGRESSIVE_BOOT.name: 2}
            PROG[MAGNEBOOTS.name] = {PROGRESSIVE_BOOT.name: 1}
        case Options.ProgressiveOptions.option_progressive_random:
            world.random.shuffle(world.orders["progressive_boots_order"])
            PROG[GRINDBOOTS.name] = {
                PROGRESSIVE_BOOT.name: 1 + world.orders["progressive_boots_order"].index(GRINDBOOTS.item_id)}
            PROG[MAGNEBOOTS.name] = {
                PROGRESSIVE_BOOT.name: 1 + world.orders["progressive_boots_order"].index(MAGNEBOOTS.item_id)}
        case _:
            pass

    if world.options.shuffle_extra_items.value == Options.ItemOptions.option_vanilla:
        PROG[HOVERBOARD.name] = {HOVERBOARD.name: 1, PROGRESSIVE_HOVERBOARD.name: 1}
        PROG[ZOOMERATOR.name] = {ZOOMERATOR.name: 1, PROGRESSIVE_HOVERBOARD.name: 2}
    else:
        match world.options.progressive_hoverboard.value:
            case Options.ProgressiveOptions.option_progressive:
                PROG[HOVERBOARD.name] = {PROGRESSIVE_HOVERBOARD.name: 1}
                PROG[ZOOMERATOR.name] = {PROGRESSIVE_HOVERBOARD.name: 2}
            case Options.ProgressiveOptions.option_progressive_reversed:
                world.orders["progressive_hoverboard_order"].reverse()
                PROG[HOVERBOARD.name] = {PROGRESSIVE_HOVERBOARD.name: 2}
                PROG[ZOOMERATOR.name] = {PROGRESSIVE_HOVERBOARD.name: 1}
            case Options.ProgressiveOptions.option_progressive_random:
                world.random.shuffle(world.orders["progressive_hoverboard_order"])
                PROG[HOVERBOARD.name] = {
                    PROGRESSIVE_HOVERBOARD.name: 1 + world.orders["progressive_hoverboard_order"].index(HOVERBOARD.item_id)}
                PROG[ZOOMERATOR.name] = {
                    PROGRESSIVE_HOVERBOARD.name: 1 + world.orders["progressive_hoverboard_order"].index(ZOOMERATOR.item_id)}
            case _:
                pass
    if world.options.shuffle_extra_items.value == Options.ItemOptions.option_vanilla:
        PROG[RARITANIUM.name] = {RARITANIUM.name: 1, PROGRESSIVE_TRADE.name: 1}
        PROG[PERSUADER.name] = {PERSUADER.name: 1, PROGRESSIVE_TRADE.name: 2}
    else:
        match world.options.progressive_raritanium.value:
            case Options.ProgressiveOptions.option_progressive:
                PROG[RARITANIUM.name] = {PROGRESSIVE_TRADE.name: 1}
                PROG[PERSUADER.name] = {PROGRESSIVE_TRADE.name: 2}
            case Options.ProgressiveOptions.option_progressive_reversed:
                world.orders["progressive_raritanium_order"].reverse()
                PROG[RARITANIUM.name] = {PROGRESSIVE_TRADE.name: 2}
                PROG[PERSUADER.name] = {PROGRESSIVE_TRADE.name: 1}
            case Options.ProgressiveOptions.option_progressive_random:
                world.random.shuffle(world.orders["progressive_raritanium_order"])
                PROG[RARITANIUM.name] = {
                    PROGRESSIVE_TRADE.name: 1 + world.orders["progressive_raritanium_order"].index(RARITANIUM.item_id)}
                PROG[PERSUADER.name] = {
                    PROGRESSIVE_TRADE.name: 1 + world.orders["progressive_raritanium_order"].index(PERSUADER.item_id)}
            case _:
                pass

    match world.options.progressive_nanotech.value:
        case Options.ProgressiveOptions.option_progressive:
            PROG[PREMIUM_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 1}
            PROG[ULTRA_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 2}
        case Options.ProgressiveOptions.option_progressive_reversed:
            world.orders["progressive_nanotech_order"].reverse()
            PROG[PREMIUM_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 2}
            PROG[ULTRA_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 1}
        case Options.ProgressiveOptions.option_progressive_random:
            world.random.shuffle(world.orders["progressive_nanotech_order"])
            PROG[PREMIUM_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 1 + world.orders[
                "progressive_nanotech_order"].index(PREMIUM_NANOTECH.item_id)}
            PROG[ULTRA_NANOTECH.name] = {PROGRESSIVE_NANOTECH.name: 1 + world.orders[
                "progressive_nanotech_order"].index(ULTRA_NANOTECH.item_id)}
        case _:
            pass
    return


def get_pool(options) -> Sequence[ItemData]:
    pool = []
    for item in ITEM_POOL:
        pool += [item]
    if options.progressive_weapons.value > Options.GoldenWeaponProgression.option_normal:
        for item in PROGRESSIVE_WEAPONS:
            pool += [item, item]
    else:
        for item in NON_PROGRESSIVE_WEAPONS:
            pool += [item]
        for item in GOLDEN_WEAPONS:
            pool += [item]
    if options.progressive_packs.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_PACKS:
            pool += [item]
    else:
        for item in PACKS:
            pool += [item]
    if options.progressive_helmets.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_HELMETS:
            pool += [item]
    else:
        for item in HELMETS:
            pool += [item]
    if options.progressive_boots.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_BOOTS:
            pool += [item]
    else:
        for item in BOOTS:
            pool += [item]
    if options.progressive_hoverboard.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_HOVERBOARDS:
            pool += [item]
    else:
        for item in NON_PROGRESSIVE_HOVERBOARDS:
            pool += [item]
    if options.progressive_raritanium.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_TRADES:
            pool += [item]
    else:
        for item in NON_PROGRESSIVE_TRADES:
            pool += [item]
    if options.progressive_nanotech.value > Options.ProgressiveOptions.option_vanilla:
        for item in PROGRESSIVE_NANOTECHS:
            pool += [item]
    else:
        for item in NON_PROGRESSIVE_NANOTECHS:
            pool += [item]
    lookup: dict[int, tuple[ItemData, int]] = {
        1: (GOLD_BOLT_1, 40),
        2: (GOLD_BOLT_2, 30),
        3: (GOLD_BOLT_3, 20),
        4: (GOLD_BOLT_4, 15),
        5: (GOLD_BOLT_5, 12),
        6: (GOLD_BOLT_6, 10),
        7: (GOLD_BOLT_7, 9),
        8: (GOLD_BOLT_8, 8),
        9: (GOLD_BOLT_9, 7),
        10: (GOLD_BOLT_10, 6),
        11: (GOLD_BOLT_11, 5),
        12: (GOLD_BOLT_12, 5),
        13: (GOLD_BOLT_13, 5),
        14: (GOLD_BOLT_14, 4),
        15: (GOLD_BOLT_15, 4),
        16: (GOLD_BOLT_16, 4),
        17: (GOLD_BOLT_17, 4),
        18: (GOLD_BOLT_18, 4),
        19: (GOLD_BOLT_19, 4),
        20: (GOLD_BOLT_20, 3),
        21: (GOLD_BOLT_21, 3),
        22: (GOLD_BOLT_22, 3),
        23: (GOLD_BOLT_23, 3),
        24: (GOLD_BOLT_24, 3),
        25: (GOLD_BOLT_25, 3),
        26: (GOLD_BOLT_26, 3),
        27: (GOLD_BOLT_27, 3),
        28: (GOLD_BOLT_28, 3),
        29: (GOLD_BOLT_29, 3),
        30: (GOLD_BOLT_30, 2),
        31: (GOLD_BOLT_31, 2),
        32: (GOLD_BOLT_32, 2),
        33: (GOLD_BOLT_33, 2),
        34: (GOLD_BOLT_34, 2),
        35: (GOLD_BOLT_35, 2),
        36: (GOLD_BOLT_36, 2),
        37: (GOLD_BOLT_37, 2),
        38: (GOLD_BOLT_38, 2),
        39: (GOLD_BOLT_39, 2),
        40: (GOLD_BOLT_40, 1),
    }
    for _ in range(lookup[options.pack_size_gold_bolts.value][1]):
        pool += [lookup[options.pack_size_gold_bolts.value][0]]
    return pool


def get_starting_planets(options) -> Sequence[ItemData]:
    planets: Sequence[ItemData] = []
    for item in STARTING_PLANETS:
        planets += [item]
    if options.shuffle_infobots.value >= Options.ShuffleInfobots.option_unrestricted:
        planets += [ARIDIA_INFOBOT]
        if options.shuffle_helmets.value >= Options.ShuffleHelmets.option_unrestricted:
            planets += [GASPAR_INFOBOT]
        if options.shuffle_gold_bolts.value:
            planets += [HOVEN_INFOBOT]
    return planets


def from_id(item_id: int) -> ItemData:
    matching = [item for item in ALL if item.item_id == item_id]
    if len(matching) == 0:
        raise ValueError(f"No item data for item id '{item_id}'")
    assert len(matching) < 2, f"{len(matching)} item data found with id '{item_id}'. Items are: {matching}"
    return matching[0]


def from_name(item_name: str) -> ItemData:
    matching = [item for item in ALL if item.name == item_name]
    if len(matching) == 0:
        raise ValueError(f"No item data for '{item_name}'")
    # if item_name != GOLD_BOLT.name:
    #     assert len(matching) < 2, f"Multiple item data with name '{item_name}'. Please report."
    return matching[0]


def get_item_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {
        "Weapons": {w.name for w in ALL_WEAPONS},
        "Gadgets": {g.name for g in GADGETS},
        "Packs": {p.name for p in ALL_PACKS},
        "Helmets": {h.name for h in ALL_HELMETS},
        "Boots": {b.name for b in ALL_BOOTS},
        "ExtraItems": {e.name for e in ALL_EXTRA_ITEMS},
        "GoldBolts": {c.name for c in GOLD_BOLTS},
        "Infobots": {i.name for i in PLANETS},
        "Skillpoints": {s.name for s in SKILLPOINTS},
    }
    return groups


def check_progressive_item(options, item) -> str:
    new_item = item
    match from_name(item).pool:
        case SUCK_CANNON.pool | GOLDEN_SUCK_CANNON.pool:
            if options.progressive_weapons.value > Options.GoldenWeaponProgression.option_normal:
                match item:
                    case SUCK_CANNON.name:
                        new_item = PROGRESSIVE_SUCK.name
                    case GOLDEN_SUCK_CANNON.name:
                        new_item = PROGRESSIVE_SUCK.name
                    case BOMB_GLOVE.name:
                        new_item = PROGRESSIVE_BOMB.name
                    case GOLDEN_BOMB_GLOVE.name:
                        new_item = PROGRESSIVE_BOMB.name
                    case DEVASTATOR.name:
                        new_item = PROGRESSIVE_DEVASTATOR.name
                    case GOLDEN_DEVASTATOR.name:
                        new_item = PROGRESSIVE_DEVASTATOR.name
                    case BLASTER.name:
                        new_item = PROGRESSIVE_BLASTER.name
                    case GOLDEN_BLASTER.name:
                        new_item = PROGRESSIVE_BLASTER.name
                    case PYROCITOR.name:
                        new_item = PROGRESSIVE_PYROCITOR.name
                    case GOLDEN_PYROCITOR.name:
                        new_item = PROGRESSIVE_PYROCITOR.name
                    case MINE_GLOVE.name:
                        new_item = PROGRESSIVE_MINE.name
                    case GOLDEN_MINE_GLOVE.name:
                        new_item = PROGRESSIVE_MINE.name
                    case TESLA_CLAW.name:
                        new_item = PROGRESSIVE_TESLA.name
                    case GOLDEN_TESLA_CLAW.name:
                        new_item = PROGRESSIVE_TESLA.name
                    case GLOVE_OF_DOOM.name:
                        new_item = PROGRESSIVE_DOOM.name
                    case GOLDEN_GLOVE_OF_DOOM.name:
                        new_item = PROGRESSIVE_DOOM.name
                    case MORPH_O_RAY.name:
                        new_item = PROGRESSIVE_MORPH.name
                    case GOLDEN_MORPH_O_RAY.name:
                        new_item = PROGRESSIVE_MORPH.name
                    case DECOY_GLOVE.name:
                        new_item = PROGRESSIVE_DECOY.name
                    case GOLDEN_DECOY_GLOVE.name:
                        new_item = PROGRESSIVE_DECOY.name
        case HELI_PACK.pool:
            if options.progressive_packs.value:
                new_item = PROGRESSIVE_PACK.name
        case O2_MASK.pool:
            if options.progressive_helmets.value:
                new_item = PROGRESSIVE_HELMET.name
        case GRINDBOOTS.pool:
            if options.progressive_boots.value:
                new_item = PROGRESSIVE_BOOT.name
        case HOVERBOARD.pool:
            match item:
                case HOVERBOARD.name | ZOOMERATOR.name:
                    if options.progressive_hoverboard.value:
                        new_item = PROGRESSIVE_HOVERBOARD.name
                case RARITANIUM.name | PERSUADER.name:
                    if options.progressive_raritanium.value:
                        new_item = PROGRESSIVE_TRADE.name
                case PREMIUM_NANOTECH.name | ULTRA_NANOTECH.name:
                    if options.progressive_nanotech.value:
                        new_item = PROGRESSIVE_NANOTECH.name
    return new_item
