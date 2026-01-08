from typing import Dict
import typing
from itertools import chain
from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    itemName: str
    progression: ItemClassification
    itemID: int = 0x00
    player: int = 0


class FFTAItem(Item):
    itemName: str
    progression: ItemClassification
    itemID: int = 0x00
    player: int = 0
    game: str = "Final Fantasy Tactics Advance"


WeaponSwords: typing.List[ItemData] = [

    # Swords
    ItemData('Shortsword', ItemClassification.useful, 0x01),
    ItemData('Silver Sword', ItemClassification.useful, 0x02),
    ItemData('Buster Sword', ItemClassification.useful, 0x03),
    ItemData('Burglar Sword', ItemClassification.useful, 0x04),
    ItemData('Gale Sword', ItemClassification.useful, 0x05),
    ItemData('Blood Sword', ItemClassification.useful, 0x06),
    ItemData('Restorer', ItemClassification.useful, 0x07),
    ItemData('Vitanova', ItemClassification.useful, 0x08),
    ItemData('Mythril Sword', ItemClassification.useful, 0x09),
    ItemData('Victor Sword', ItemClassification.useful, 0x0A),
    ItemData('Onion Sword', ItemClassification.useful, 0x0B),
    ItemData('Chirijiraden', ItemClassification.useful, 0x0C),
    ItemData('Laglace Sword', ItemClassification.useful, 0x0D),
]


WeaponBlades: typing.List[ItemData] = [
    ItemData('Sweep Blade', ItemClassification.useful, 0x0E),
    ItemData('Shadow Blade', ItemClassification.useful, 0x0F),
    ItemData('Sun Blade', ItemClassification.useful, 0x10),
    ItemData("Atmos Blade", ItemClassification.useful, 0x11),
    ItemData("Flametongue", ItemClassification.useful, 0x12),
    ItemData("Air Blade", ItemClassification.useful, 0x13),
    ItemData("Icebrand", ItemClassification.useful, 0x14),
    ItemData("Kwigon Blade", ItemClassification.useful, 0x15),
    ItemData("Ogun Blade", ItemClassification.useful,  0x16),
    ItemData("Pearl Blade", ItemClassification.useful, 0x17),
    ItemData("Paraiba Blade", ItemClassification.useful, 0x18),
    ItemData("Venus Blade", ItemClassification.useful, 0x19),
    ItemData("Materia Blade", ItemClassification.useful, 0x1A),
    ItemData("Mythril Blade", ItemClassification.useful, 0x1B),
    ItemData("Ebon Blade", ItemClassification.useful,  0x1C),
    ItemData("Adaman Blade", ItemClassification.useful, 0x1D),
    ItemData("Ayvuir Red", ItemClassification.useful,  0x1E),
    ItemData("Ayvuir Blue", ItemClassification.useful, 0x1F),
]

WeaponSabers: typing.List[ItemData] = [
    ItemData("Blue Saber", ItemClassification.useful, 0x20),
    ItemData("Shamshir", ItemClassification.useful, 0x21),
    ItemData("Aqua Saber", ItemClassification.useful, 0x22),
    ItemData("Harpe", ItemClassification.useful, 0x23),
    ItemData("Manganese", ItemClassification.useful, 0x24),
    ItemData("Mythril Saber", ItemClassification.useful, 0x25),
    ItemData("Tulwar", ItemClassification.useful, 0x26),
    ItemData("Soul Saber", ItemClassification.useful, 0x27),
]

WeaponKnightswords: typing.List[ItemData] = [
    ItemData("Defender", ItemClassification.useful, 0x28),
    ItemData("Apocalypse", ItemClassification.useful, 0x29),
    ItemData("Lionheart", ItemClassification.useful, 0x2A),
    ItemData("Ragnarok", ItemClassification.useful, 0x2B),
    ItemData("Lohengrin", ItemClassification.useful, 0x2C),
    ItemData("Save The Queen", ItemClassification.useful, 0x2D),
    ItemData("Arch Sword", ItemClassification.useful, 0x2E),
    ItemData("Excalibur", ItemClassification.useful, 0x2F),
    ItemData("Mythril Brand", ItemClassification.useful, 0x30),
    ItemData("Excalibur 2", ItemClassification.useful, 0x31),
    ItemData("Nagrarok", ItemClassification.useful, 0x32),
    ItemData("Sequence", ItemClassification.useful, 0x33),
]

WeaponGreatswords: typing.List[ItemData] = [
    ItemData("Barong", ItemClassification.useful, 0x34),
    ItemData("Ancient Sword", ItemClassification.useful, 0x35),
    ItemData("Diamond Sword", ItemClassification.useful, 0x36),
    ItemData("Hardedge", ItemClassification.useful, 0x37),
    ItemData("Vigilante", ItemClassification.useful, 0x38),
    ItemData("Zankplus", ItemClassification.useful, 0x39),
    ItemData("Master Sword", ItemClassification.useful, 0x3A),
    ItemData("Oblige", ItemClassification.useful, 0x3B),
    ItemData("Iceprism", ItemClassification.useful, 0x3C),
    ItemData("Lurebreaker", ItemClassification.useful, 0x3D),
]


WeaponBroadswords: typing.List[ItemData] = [
    ItemData("Samson Sword", ItemClassification.useful, 0x3E),
    ItemData("Falchion", ItemClassification.useful, 0x3F),
    ItemData("Predator", ItemClassification.useful, 0x40),
    ItemData("Striborg", ItemClassification.useful, 0x41),
    ItemData("El Cid Sword", ItemClassification.useful, 0x42),
    ItemData("Claymore", ItemClassification.useful, 0x43),
    ItemData("Vajra", ItemClassification.useful, 0x44),
    ItemData("Tabarise", ItemClassification.useful, 0x45),
    ItemData("Rhomphaia", ItemClassification.useful, 0x46),
    ItemData("Beastsword", ItemClassification.useful, 0x47),
    ItemData("Eclipse", ItemClassification.useful, 0x48),
    ItemData("Estreledge", ItemClassification.useful, 0x49),
]

WeaponKnives: typing.List[ItemData] = [
    ItemData("Jack Knife", ItemClassification.useful, 0x4A),
    ItemData("Kris Knife", ItemClassification.useful, 0x4B),
    ItemData("Khukuri", ItemClassification.useful, 0x4C),
    ItemData("Kard", ItemClassification.useful, 0x4D),
    ItemData("Scramasax", ItemClassification.useful, 0x4E),
    ItemData("Rondell Dagger", ItemClassification.useful, 0x4F),
    ItemData("Jambiya", ItemClassification.useful, 0x50),
    ItemData("Zorlin Shape", ItemClassification.useful, 0x51),
    ItemData("Sword Breaker", ItemClassification.useful, 0x52),
    ItemData("Orichalcum", ItemClassification.useful, 0x53),
    ItemData("Cinquedea", ItemClassification.useful, 0x54),
    ItemData("Mythril Knife", ItemClassification.useful, 0x55),
    ItemData("Tonberrian", ItemClassification.useful, 0x56),
    ItemData("Tiptaptwo", ItemClassification.useful, 0x57),

]


WeaponRapiers: typing.List[ItemData] = [
    ItemData("Stinger", ItemClassification.useful, 0x58),
    ItemData("Estoc", ItemClassification.useful, 0x59),
    ItemData("Fleuret", ItemClassification.useful, 0x5A),
    ItemData("Scarlette", ItemClassification.useful, 0x5B),
    ItemData("Flamberge", ItemClassification.useful, 0x5C),
    ItemData("Silver Rapier", ItemClassification.useful, 0x5D),
    ItemData("Djinn Flyssa", ItemClassification.useful, 0x5E),
    ItemData("Joyeuse", ItemClassification.useful, 0x5F),
    ItemData("Mage Masher", ItemClassification.useful, 0x60),
    ItemData("Colichemarde", ItemClassification.useful, 0x61),
    ItemData("Gupti Aga", ItemClassification.useful, 0x62),
    ItemData("Madu", ItemClassification.useful, 0x63),
    ItemData("Epeprism", ItemClassification.useful, 0x64),
    ItemData("Mythril Rapier", ItemClassification.useful, 0x65),
    ItemData("Last Letter", ItemClassification.useful, 0x66),
    ItemData("Diabolique", ItemClassification.useful, 0x67),
    ItemData("Femme Fatale", ItemClassification.useful, 0x68),
    ItemData("Aerial Hole", ItemClassification.useful, 0x69)
]

WeaponKatanas: typing.List[ItemData] = [
    ItemData("Ninja Knife", ItemClassification.useful, 0x6A),
    ItemData("Murasame", ItemClassification.useful, 0x6B),
    ItemData("Ashura", ItemClassification.useful, 0x6C),
    ItemData("Osafune", ItemClassification.useful, 0x6D),
    ItemData("Petalchaser", ItemClassification.useful, 0x6E),
    ItemData("Kotetsu", ItemClassification.useful, 0x6F),
    ItemData("Kikuichimonji", ItemClassification.useful, 0x70),
    ItemData("Heaven's Cloud", ItemClassification.useful, 0x71),
    ItemData("Nosada", ItemClassification.useful, 0x72),
    ItemData("Masamune", ItemClassification.useful, 0x73),
    ItemData("Zanmato", ItemClassification.useful, 0x74),
    ItemData("Mythril Epee", ItemClassification.useful, 0x75),
    ItemData("Masamune 100", ItemClassification.useful, 0x76),
    ItemData("Charfire", ItemClassification.useful, 0x77),
    ItemData("Silkmoon", ItemClassification.useful, 0x78)
]

WeaponStaves: typing.List[ItemData] = [
    ItemData("White Staff", ItemClassification.useful, 0x79),
    ItemData("Guard Staff", ItemClassification.useful, 0x7A),
    ItemData("Judge Staff", ItemClassification.useful, 0x7B),
    ItemData("Cure Staff", ItemClassification.useful, 0x7C),
    ItemData("Pure Staff", ItemClassification.useful, 0x7D),
    ItemData("Bless Staff", ItemClassification.useful, 0x7E),
    ItemData("Snake Staff", ItemClassification.useful, 0x7F),
    ItemData("Spring Staff", ItemClassification.useful, 0x80),
    ItemData("Garnet Staff", ItemClassification.useful, 0x81),
    ItemData("Cheer Staff", ItemClassification.useful, 0x82),
    ItemData("Nirvana Staff", ItemClassification.useful, 0x83),
    ItemData("Mythril Staff", ItemClassification.useful, 0x84),
    ItemData("Power Staff", ItemClassification.useful, 0x85),
    ItemData("Dream Watcher", ItemClassification.useful, 0x86)
]

WeaponRods: typing.List[ItemData] = [
    ItemData("Rod", ItemClassification.useful, 0x87),
    ItemData("Firewheel Rod", ItemClassification.useful, 0x88),
    ItemData("Thunder Rod", ItemClassification.useful, 0x89),
    ItemData("Sleet Rod", ItemClassification.useful, 0x8A),
    ItemData("Terre Rod", ItemClassification.useful, 0x8B),
    ItemData("Force Rod", ItemClassification.useful, 0x8C),
    ItemData("Flame Rod", ItemClassification.useful, 0x8D),
    ItemData("Thor Rod", ItemClassification.useful, 0x8E),
    ItemData("Chill Rod", ItemClassification.useful, 0x8F),
    ItemData("Stardust Rod", ItemClassification.useful, 0x90),
    ItemData("Princess Rod", ItemClassification.useful, 0x91),
    ItemData("Mythril Rod", ItemClassification.useful, 0x92),
    ItemData("Heretic Rod", ItemClassification.useful, 0x93),
    ItemData("Sapere Aude", ItemClassification.useful, 0x94)
]

WeaponMaces: typing.List[ItemData] = [
    ItemData("Battle Mace", ItemClassification.useful, 0x95),
    ItemData("Energy Mace", ItemClassification.useful, 0x96),
    ItemData("Druid Mace", ItemClassification.useful, 0x97),
    ItemData("Sage Crosier", ItemClassification.useful, 0x98),
    ItemData("Morning Star", ItemClassification.useful, 0x99),
    ItemData("Mandragora", ItemClassification.useful, 0x9A),
    ItemData("Life Crosier", ItemClassification.useful, 0x9B),
    ItemData("Lotus Mace", ItemClassification.useful, 0x9C),
    ItemData("Scorpion Tail", ItemClassification.useful, 0x9D),
    ItemData("Zeus Mace", ItemClassification.useful, 0x9E),
    ItemData("Mythril Mace", ItemClassification.useful, 0x9F),
    ItemData("Cactus Stick", ItemClassification.useful, 0xA0),
    ItemData("Vesper", ItemClassification.useful, 0xA1)

]

WeaponBows: typing.List[ItemData] = [
    ItemData("Longbow", ItemClassification.useful, 0xA2),
    ItemData("Char Bow", ItemClassification.useful, 0xA3),
    ItemData("Thorn Bow", ItemClassification.useful, 0xA4),
    ItemData("Nail Bow", ItemClassification.useful, 0xA5),
    ItemData("Silver Bow", ItemClassification.useful, 0xA6),
    ItemData("Artemis Bow", ItemClassification.useful, 0xA7),
    ItemData("Yoichi Bow", ItemClassification.useful, 0xA8),
    ItemData("Target Bow", ItemClassification.useful, 0xA9),
    ItemData("Perseus Bow", ItemClassification.useful, 0xAA),
    ItemData("Mythril Bow", ItemClassification.useful, 0xAB),
    ItemData("Crescent Bow", ItemClassification.useful, 0xAC),
    ItemData("Malbow", ItemClassification.useful, 0xAD)
]

WeaponGreatBows: typing.List[ItemData] = [
    ItemData("Windslash Bow", ItemClassification.useful, 0xAE),
    ItemData("Ranger Bow", ItemClassification.useful, 0xAF),
    ItemData("Cranequin", ItemClassification.useful, 0xB0),
    ItemData("Twin Bow", ItemClassification.useful, 0xB1),
    ItemData("Hunt Bow", ItemClassification.useful, 0xB2),
    ItemData("Fey Bow", ItemClassification.useful, 0xB3),
    ItemData("Hades Bow", ItemClassification.useful, 0xB4),
    ItemData("Nike Bow", ItemClassification.useful, 0xB5),
    ItemData("Master Bow", ItemClassification.useful, 0xB6),
    ItemData("Max's Oathbow", ItemClassification.useful, 0xB7),
    ItemData("Seventh Heaven", ItemClassification.useful, 0xB8),
    ItemData("Mythril Shot", ItemClassification.useful, 0xB9),
    ItemData("Marduk Bow", ItemClassification.useful, 0xBA),
    ItemData("Gastra Bow", ItemClassification.useful, 0xBB),
    ItemData("Arbalest", ItemClassification.useful, 0xBC)
]

WeaponSpears: typing.List[ItemData] = [
    ItemData("Javelin", ItemClassification.useful, 0xBD),
    ItemData("Lava Spear", ItemClassification.useful, 0xBE),
    ItemData("Gae Bolg", ItemClassification.useful, 0xBF),
    ItemData("Ice Lance", ItemClassification.useful, 0xC0),
    ItemData("Partisan", ItemClassification.useful, 0xC1),
    ItemData("Kain's Lance", ItemClassification.useful, 0xC2),
    ItemData("Trident", ItemClassification.useful, 0xC3),
    ItemData("Dragon Whisker", ItemClassification.useful, 0xC4),
    ItemData("Mythril Spear", ItemClassification.useful, 0xC5),
    ItemData("Odin Lance", ItemClassification.useful, 0xC6),
    ItemData("Beast Spear", ItemClassification.useful, 0xC7),
    ItemData("Bangaa Spike", ItemClassification.useful, 0xC8)
]

WeaponInstruments: typing.List[ItemData] = [
    ItemData("Demon Bell", ItemClassification.useful, 0xC9),
    ItemData("Glass Bell", ItemClassification.useful, 0xCA),
    ItemData("War Trumpet", ItemClassification.useful, 0xCB),
    ItemData("Conch Shell", ItemClassification.useful, 0xCC),
    ItemData("Earth Bell", ItemClassification.useful, 0xCD),
    ItemData("Black Quena", ItemClassification.useful, 0xCE),
    ItemData("Satyr Flute", ItemClassification.useful, 0xCF),
    ItemData("Fairy Harp", ItemClassification.useful, 0xD0),
    ItemData("Aona Flute", ItemClassification.useful, 0xD1),
    ItemData("Heal Chime", ItemClassification.useful, 0xD2),
    ItemData("Blood Strings", ItemClassification.useful, 0xD3),
    ItemData("Mythril Bell", ItemClassification.useful, 0xD4),
    ItemData("Dark Fiddle", ItemClassification.useful, 0xD5),
    ItemData("Fell Castanets", ItemClassification.useful, 0xD6)
]

WeaponKnuckles: typing.List[ItemData] = [
    ItemData("Hard Knuckles", ItemClassification.useful, 0xD7),
    ItemData("Rising Sun", ItemClassification.useful, 0xD8),
    ItemData("Sick Knuckles", ItemClassification.useful, 0xD9),
    ItemData("Dream Claws", ItemClassification.useful, 0xDA),
    ItemData("Kaiser Knuckles", ItemClassification.useful, 0xDB),
    ItemData("Cat Claws", ItemClassification.useful, 0xDC),
    ItemData("Survivor", ItemClassification.useful, 0xDD),
    ItemData("White Fangs", ItemClassification.useful, 0xDE),
    ItemData("Godhand", ItemClassification.useful, 0xDF),
    ItemData("Tiger Fangs", ItemClassification.useful, 0xE0),
    ItemData("Death Claws", ItemClassification.useful, 0xE1),
    ItemData("Mythril Claws", ItemClassification.useful, 0xE2),
    ItemData("Greaseburst", ItemClassification.useful, 0xE3),
    ItemData("Magic Hands", ItemClassification.useful, 0xE4)
]

WeaponSouls: typing.List[ItemData] = [
    ItemData("Goblin Soul", ItemClassification.useful, 0xE5),
    ItemData("Flan Soul", ItemClassification.useful, 0xE6),
    ItemData("Bomb Soul", ItemClassification.useful, 0xE7),
    ItemData("Dragon Soul", ItemClassification.useful, 0xE8),
    ItemData("Lamia Soul", ItemClassification.useful, 0xE9),
    ItemData("Bug Soul", ItemClassification.useful, 0xEA),
    ItemData("Panther Soul", ItemClassification.useful, 0xEB),
    ItemData("Malboro Soul", ItemClassification.useful, 0xEC),
    ItemData("Eye Soul", ItemClassification.useful, 0xED),
    ItemData("Mythril Soul", ItemClassification.useful, 0xEE),
    ItemData("Dread Soul", ItemClassification.useful, 0xEF),
    ItemData("Rukavi Soul", ItemClassification.useful, 0xF0)
]

WeaponGuns: typing.List[ItemData] = [
    ItemData("Aiot Gun", ItemClassification.useful, 0xF1),
    ItemData("Silver Cannon", ItemClassification.useful, 0xF2),
    ItemData("Riot Gun", ItemClassification.useful, 0xF3),
    ItemData("Chaos Rifle", ItemClassification.useful, 0xF4),
    ItemData("Lost Gun", ItemClassification.useful, 0xF5),
    ItemData("Peacemaker", ItemClassification.useful, 0xF6),
    ItemData("Giot Gun", ItemClassification.useful, 0xF7),
    ItemData("Longbarrel", ItemClassification.useful, 0xF8),
    ItemData("Outsider", ItemClassification.useful, 0xF9),
    ItemData("Mythril Gun", ItemClassification.useful, 0xFA),
    ItemData("Bindsnipe", ItemClassification.useful, 0xFB),
    ItemData("Calling Gun", ItemClassification.useful, 0xFC)
]


EquipShields: typing.List[ItemData] = [
    ItemData("Bronze Shield", ItemClassification.useful, 0xFD),
    ItemData("Round Shield", ItemClassification.useful, 0xFE),
    ItemData("Opal Shield", ItemClassification.useful, 0xFF),
    ItemData("Ice Shield", ItemClassification.useful, 0x100),
    ItemData("Flame Shield", ItemClassification.useful, 0x101),
    ItemData("Aegis Shield", ItemClassification.useful, 0x102),
    ItemData("Genji Shield", ItemClassification.useful, 0x103),
    ItemData("Sacri Shield", ItemClassification.useful, 0x104),
    ItemData("Shijin Shield", ItemClassification.useful, 0x105),
    ItemData("Chocobo Shield", ItemClassification.useful, 0x106),
    ItemData("La Seraphica", ItemClassification.useful, 0x107),
    ItemData("Reverie Shield", ItemClassification.useful, 0x108)
]

EquipHelmets: typing.List[ItemData] = [
    ItemData("Bronze Helm", ItemClassification.useful, 0x109),
    ItemData("Iron Helm", ItemClassification.useful, 0x10A),
    ItemData("Opal Helm", ItemClassification.useful, 0x10B),
    ItemData("Cross Helm", ItemClassification.useful, 0x10C),
    ItemData("Diamond Helm", ItemClassification.useful, 0x10D),
    ItemData("Genji Helm", ItemClassification.useful, 0x10E),
    ItemData("Parade Helm", ItemClassification.useful, 0x10F),
    ItemData("Hanya Helm", ItemClassification.useful, 0x110),
    ItemData("Bangaa Helm", ItemClassification.useful, 0x111)
]

EquipFemale: typing.List[ItemData] = [
    ItemData("Cachusha", ItemClassification.useful, 0x112),
    ItemData("Barette", ItemClassification.useful, 0x113),
    ItemData("Ribbon", ItemClassification.useful, 0x114),
    ItemData("Tiara", ItemClassification.useful, 0x11F),
    ItemData("Minerva Plate", ItemClassification.useful, 0x137),
    ItemData("Rubber Suit", ItemClassification.useful, 0x13C)
]

EquipHats: typing.List[ItemData] = [
    ItemData("Feather Cap", ItemClassification.useful, 0x115),
    ItemData("Circlet", ItemClassification.useful, 0x116),
    ItemData("Green Beret", ItemClassification.useful, 0x117),
    ItemData("Headband", ItemClassification.useful, 0x118),
    ItemData("Wizard Hat", ItemClassification.useful, 0x119),
    ItemData("Gold Hairpin", ItemClassification.useful, 0x11A),
    ItemData("Thief Hat", ItemClassification.useful, 0x11B),
    ItemData("Black Hat", ItemClassification.useful, 0x11C),
    ItemData("White Hat", ItemClassification.useful, 0x11D),
    ItemData("Acacia Hat", ItemClassification.useful, 0x11E)
]

EquipArmor: typing.List[ItemData] = [
    ItemData("Cuirass", ItemClassification.useful, 0x120),
    ItemData("Bronze Armor", ItemClassification.useful, 0x121),
    ItemData("Iron Armor", ItemClassification.useful, 0x122),
    ItemData("Platemail", ItemClassification.useful, 0x123),
    ItemData("Gold Armor", ItemClassification.useful, 0x124),
    ItemData("Diamond Armor", ItemClassification.useful, 0x125),
    ItemData("Opal Armor", ItemClassification.useful, 0x126),
    ItemData("Carabini", ItemClassification.useful, 0x127),
    ItemData("Mirror Mail", ItemClassification.useful, 0x128),
    ItemData("Dragon Mail", ItemClassification.useful, 0x129),
    ItemData("Genji Armor", ItemClassification.useful, 0x12A),
    ItemData("Maximillian", ItemClassification.useful, 0x12B),
    ItemData("Adaman Armor", ItemClassification.useful, 0x12C),
    ItemData("Materia Armor", ItemClassification.useful, 0x12D),
    ItemData("Peytral", ItemClassification.useful, 0x12E)
]

EquipClothing: typing.List[ItemData] = [
    ItemData("Leather Garb", ItemClassification.useful, 0x12F),
    ItemData("Chain Plate", ItemClassification.useful, 0x130),
    ItemData("Adaman Vest", ItemClassification.useful, 0x131),
    ItemData("Survival Vest", ItemClassification.useful, 0x132),
    ItemData("Brigandine", ItemClassification.useful, 0x133),
    ItemData("Judo Uniform", ItemClassification.useful, 0x134),
    ItemData("Power Sash", ItemClassification.useful, 0x135),
    ItemData("Gaia Gear", ItemClassification.useful, 0x136),
    ItemData("Ninja Gear", ItemClassification.useful, 0x138),
    ItemData("Dark Gear", ItemClassification.useful, 0x139),
    ItemData("Wygar", ItemClassification.useful, 0x13A),
    ItemData("Mirage Vest", ItemClassification.useful, 0x13B),
    ItemData("Bone Plate", ItemClassification.useful, 0x13D),
    ItemData("Onlyone", ItemClassification.useful, 0x13E),
    ItemData("Brint Set", ItemClassification.useful, 0x13F),
    ItemData("Galmia Set", ItemClassification.useful, 0x140),
    ItemData("Judge Coat", ItemClassification.useful, 0x141),
    ItemData("Temple Cloth", ItemClassification.useful, 0x142)
]

EquipRobes: typing.List[ItemData] = [
    ItemData("Hempen Robe", ItemClassification.useful, 0x143),
    ItemData("Silken Robe", ItemClassification.useful, 0x144),
    ItemData("Magus Robe", ItemClassification.useful, 0x145),
    ItemData("Mistle Robe", ItemClassification.useful, 0x146),
    ItemData("Blaze Robe", ItemClassification.useful, 0x147),
    ItemData("Thunder Robe", ItemClassification.useful, 0x148),
    ItemData("Flurry Robe", ItemClassification.useful, 0x149),
    ItemData("White Robe", ItemClassification.useful, 0x14A),
    ItemData("Black Robe", ItemClassification.useful, 0x14B),
    ItemData("Light Robe", ItemClassification.useful, 0x14C),
    ItemData("Lordly Robe", ItemClassification.useful, 0x14D),
    ItemData("Silver Coat", ItemClassification.useful, 0x14E),
    ItemData("Red Robe", ItemClassification.useful, 0x14F),
    ItemData("Sage Robe", ItemClassification.useful, 0x150),
    ItemData("Magic Robe", ItemClassification.useful, 0x151),
    ItemData("Reaper Cloak", ItemClassification.useful, 0x152)
]

EquipShoes: typing.List[ItemData] = [
    ItemData("Battle Boots", ItemClassification.useful, 0x153),
    ItemData("Spiked Boots", ItemClassification.useful, 0x154),
    ItemData("Dash Boots", ItemClassification.useful, 0x155),
    ItemData("Red Boots", ItemClassification.useful, 0x156),
    ItemData("Feather Boots", ItemClassification.useful, 0x157),
    ItemData("Germinas", ItemClassification.useful, 0x158),
    ItemData("Galmia Shoes", ItemClassification.useful, 0x159),
    ItemData("Fairy Shoes", ItemClassification.useful, 0x15A),
    ItemData("Caligula", ItemClassification.useful, 0x15B),
    ItemData("Ninja Tabi", ItemClassification.useful, 0x15C)
]

EquipGloves: typing.List[ItemData] = [
    ItemData("Gauntlets", ItemClassification.useful, 0x15D),
    ItemData("Thief Armlets", ItemClassification.useful, 0x15E),
    ItemData("Bracers", ItemClassification.useful, 0x15F),
    ItemData("Genji Armlets", ItemClassification.useful, 0x160),
    ItemData("Fire Mitts", ItemClassification.useful, 0x161),
    ItemData("Bone Armlets", ItemClassification.useful, 0x162)
]

EquipRings: typing.List[ItemData] = [
    ItemData("Fortune Ring", ItemClassification.useful, 0x163),
    ItemData("Magic Ring", ItemClassification.useful, 0x164),
    ItemData("Angel Ring", ItemClassification.useful, 0x165),
    ItemData("Scarab", ItemClassification.useful, 0x166),
    ItemData("Ruby Earring", ItemClassification.useful, 0x167),
    ItemData("Star Armlet", ItemClassification.useful, 0x168),
    ItemData("Mindu Gem", ItemClassification.useful, 0x169)
]

Consumables: typing.List[ItemData] = [
    ItemData("Potion", ItemClassification.filler, 0x16A),
    ItemData("Hi-Potion", ItemClassification.filler, 0x16B),
    ItemData("X-Potion", ItemClassification.filler, 0x16C),
    ItemData("Ether", ItemClassification.filler, 0x16D),
    ItemData("Elixir", ItemClassification.filler, 0x16E),
    ItemData("Antidote", ItemClassification.filler, 0x16F),
    ItemData("Eye Drops", ItemClassification.filler, 0x170),
    ItemData("Echo Screen", ItemClassification.filler, 0x171),
    ItemData("Maiden's Kiss", ItemClassification.filler, 0x172),
    ItemData("Soft", ItemClassification.filler, 0x173),
    ItemData("Holy Water", ItemClassification.filler, 0x174),
    ItemData("Bandage", ItemClassification.filler, 0x175),
    ItemData("Cureall", ItemClassification.filler, 0x176),
    ItemData("Phoenix Down", ItemClassification.filler, 0x177),
]


MissionUnlockItems: typing.List[ItemData] = [
    ItemData('Magic Trophy', ItemClassification.progression, 0x178),
    ItemData('Fight Trophy', ItemClassification.progression, 0x179),

    ItemData('Magic Medal', ItemClassification.progression, 0x17e),
    ItemData('Ancient Medal', ItemClassification.progression, 0x17f),

    ItemData('Choco Bread', ItemClassification.progression, 0x1ac),
    ItemData('Choco Gratin', ItemClassification.progression, 0x1ad),

    ItemData('Black Thread', ItemClassification.progression, 0x19a),
    ItemData('White Thread', ItemClassification.progression, 0x19b),

    ItemData('Thunderstone', ItemClassification.progression, 0x189),
    ItemData('Stormstone', ItemClassification.progression, 0x18a),

    ItemData('Ahriman Eye', ItemClassification.progression, 0x18c),
    ItemData('Ahriman Wing', ItemClassification.progression, 0x1a0),

    ItemData('Magic Cloth', ItemClassification.progression, 0x19d),
    ItemData('Magic Cotton', ItemClassification.progression, 0x19e),

    ItemData('Adaman Alloy', ItemClassification.progression, 0x196),
    ItemData('Mysidia Alloy', ItemClassification.progression, 0x197),

    ItemData("Elda's Cup", ItemClassification.progression, 0x17b),
    ItemData('Gold Vessel', ItemClassification.progression, 0x17d),

    ItemData('Kiddy Bread', ItemClassification.progression, 0x1ae),
    ItemData('Grownup Bread', ItemClassification.progression, 0x1af),

    ItemData('Danbukwood', ItemClassification.progression, 0x1c2),
    ItemData('Moonwood', ItemClassification.progression, 0x1c3),

    ItemData('Dragon Bone', ItemClassification.progression, 0x1e4),
    ItemData('Animal Bone', ItemClassification.progression, 0x1e5),

    ItemData('Magic Fruit', ItemClassification.progression, 0x1f1),
    ItemData('Power Fruit', ItemClassification.progression, 0x1f2),

    # Gate 15 items
    ItemData('Malboro Wine', ItemClassification.progression, 0x1b0),
    ItemData('Gedegg Soup', ItemClassification.progression, 0x1b1),

    ItemData('Encyclopedia', ItemClassification.progression, 0x1ba),
    ItemData('Dictionary', ItemClassification.progression, 0x1bb),

    ItemData('Rat Tail', ItemClassification.progression, 0x1c0),
    ItemData('Rabbit Tail', ItemClassification.progression, 0x1c1),

    ItemData('Stasis Rope', ItemClassification.progression, 0x1dd),
    ItemData('Mythril Pick', ItemClassification.progression, 0x1de),

    ItemData('Clock Gear', ItemClassification.progression, 0x1e8),
    ItemData('Gun Gear', ItemClassification.progression, 0x1e9),

    ItemData('Blood Shawl', ItemClassification.progression, 0x19f),
    ItemData('Blood Apple', ItemClassification.progression, 0x1f0),

    ItemData('Eldagusto', ItemClassification.progression, 0x1aa),
    ItemData('Cyril Ice', ItemClassification.progression, 0x1ab),

    ItemData('Crystal', ItemClassification.progression, 0x1c8),
    ItemData('Trichord', ItemClassification.progression, 0x1cb),

    ItemData('Tranquil Box', ItemClassification.progression, 0x1da),
    ItemData('Flower Vase', ItemClassification.progression, 0x1e3),

    ItemData("Cat's Tears", ItemClassification.progression, 0x187),
    ItemData("Dame's Blush", ItemClassification.progression, 0x188),

    ItemData('Homework', ItemClassification.progression, 0x1b9),
    ItemData('Friend Badge', ItemClassification.progression, 0x1b5),

    ItemData('Love Potion', ItemClassification.progression, 0x1e0),
    ItemData('Tonberry Lamp', ItemClassification.progression, 0x1e1),

    ItemData("Runba's Tale", ItemClassification.progression, 0x1b6),
    ItemData("The Hero Gaol", ItemClassification.progression, 0x1b7),

    ItemData('Mind Ceffyl', ItemClassification.progression, 0x1d4),
    ItemData('Body Ceffyl', ItemClassification.progression, 0x1d5),

    ItemData('Ancient Bills', ItemClassification.progression, 0x1f5),
    ItemData('Ancient Coins', ItemClassification.progression, 0x1f6),

    ItemData('Blue Rose', ItemClassification.progression, 0x1ee),
    ItemData('White Flowers', ItemClassification.progression, 0x1ef),

    ItemData('Gysahl Greens', ItemClassification.progression, 0x1a6),
    ItemData('Chocobo Egg', ItemClassification.progression, 0x1a7),

    ItemData('Delta Fang', ItemClassification.progression, 0x186),
    ItemData('Esteroth', ItemClassification.progression, 0x18b),

    ItemData('Moon Bloom', ItemClassification.progression, 0x1ec),
    ItemData('Telaq Flowers', ItemClassification.progression, 0x1ed)
]

TotemaUnlockItems: typing.List[ItemData] = [
    ItemData('Fire Sigil', ItemClassification.progression, 0x1d0),
    ItemData('Water Sigil', ItemClassification.progression, 0x1d1),
    ItemData('Wind Sigil', ItemClassification.progression, 0x1d2),
    ItemData('Earth Sigil', ItemClassification.progression, 0x1d3),
    ItemData('Old Statue', ItemClassification.progression, 0x1c9)
]

ProgressiveItems: typing.List[ItemData] = [
    ItemData('Progressive Path 1', ItemClassification.progression, 0x300),
    ItemData('Progressive Path 2', ItemClassification.progression, 0x301),
    ItemData('Progressive Path 3', ItemClassification.progression, 0x302),
    ItemData('Progressive Dispatch', ItemClassification.progression, 0x303),
    ItemData('Progressive Shop', ItemClassification.progression, 0x3FF),
]

# Ability items? maybe do job unlock items first
AbilityItems: typing.List[ItemData] = [
    #ItemData('Ability: Sheep Count', ItemClassification.useful, 0x1b8),
    #ItemData('Ability: 100% Wool', ItemClassification.useful, 0x1b9),
    #ItemData('Ability: Cuisine', ItemClassification.useful, 0x1ba),
    #ItemData('Ability: Tail Wag', ItemClassification.useful, 0x1bb)
]

JobUnlockDict = {
    0x55: 0x521AAC,  # Soldier
    0x65: 0x521AE0,  # Paladin
    0x0D: 0x521B14,  # Fighter
    0x7D: [0x521B48, 0x522230],  # Thief
    0x05: 0x521B7C,  # Ninja
    0x2A: [0x521BB0, 0x521E54, 0x522090],  # White Mage
    0x3C: [0x521BE4, 0x521E88, 0x5222CC],  # Black Mage
    0x6B: [0x521C18, 0x521EF0],  # Illusionist
    0x45: 0x521C4C,  # Blue Mage
    0x5F: [0x521C80, 0x5220f8],  # Archer
    0x2C: 0x521CB4,  # Hunter
    0x56: 0x521CE8,  # Warrior
    0x58: 0x521D1C,  # Dragoon
    0x0C: 0x521D50,  # Defender
    0x19: 0x521D84,  # Gladiator
    0x1A: 0x521DB8,  # White Monk
    0x41: 0x521DEC,  # Bishop
    0x1D: 0x521E20,  # Templar
    0x4E: [0x521EF0, 0x522300],  # Time Mage
    0x32: 0x521F24,  # Alchemist
    0x2B: 0x521F58,  # Beastmaster
    0x25: 0x521F8C,  # Morpher
    0x3B: 0x521FC0,  # Sage
    0x57: 0x521FF4,  # Fencer
    0x73: 0x522028,   # Elementalist
    0x17: 0x52205C,   # Red Mage
    0x0B: 0x5220C4,  # Summoner
    0x60: 0x52212C,  # Assassin
    0x61: 0x522160,  # Sniper
    0x48: 0x522194,  # Animist
    0x3D: 0x5221C8,  # Mog Knight
    0x4F: 0x5221FC,   # Gunner
    0x50: 0x522264,  # Juggler
    0x64: 0x522298  # Gadgeteer
}

JobUnlocks: typing.List[ItemData] = [

    ItemData('Job Unlock: Soldier', ItemClassification.useful, 0x1cc),  # Rusty sword
    ItemData('Job Unlock: Paladin', ItemClassification.useful, 0x1dc),  # Snake shield
    ItemData('Job Unlock: Fighter', ItemClassification.useful, 0x184),  # Badge
    ItemData('Job Unlock: Thief', ItemClassification.useful, 0x1f4),  # Stolen Gil
    ItemData('Job Unlock: Ninja', ItemClassification.useful, 0x17c),  # Ogma's Seal
    ItemData('Job Unlock: White Mage', ItemClassification.useful, 0x1a1),  # Fairy wing
    ItemData('Job Unlock: Black Mage', ItemClassification.useful, 0x1b3),  # Magic Vellum
    ItemData('Job Unlock: Illusionist', ItemClassification.useful, 0x1e2),  # Stilpool scroll
    ItemData('Job Unlock: Blue Mage', ItemClassification.useful, 0x1bc),  # Monster guide
    ItemData('Job Unlock: Archer', ItemClassification.useful, 0x1d6),  # Feather badge
    ItemData('Job Unlock: Hunter', ItemClassification.useful, 0x1a3),  # Panther hide
    ItemData('Job Unlock: Warrior', ItemClassification.useful, 0x1cd),  # Broken sword
    ItemData('Job Unlock: Dragoon', ItemClassification.useful, 0x1cf),  # Rusty spear
    ItemData('Job Unlock: Defender', ItemClassification.useful, 0x183),  # Master brave
    ItemData('Job Unlock: Gladiator', ItemClassification.useful, 0x190),  # Silvril
    ItemData('Job Unlock: White Monk', ItemClassification.useful, 0x191),  # Materite
    ItemData('Job Unlock: Bishop', ItemClassification.useful, 0x1b8),  # Edaroya tome
    ItemData('Job Unlock: Templar', ItemClassification.useful, 0x194),  # Spiritstone
    ItemData('Job Unlock: Time Mage', ItemClassification.useful, 0x1c5),  # Clock post
    ItemData('Job Unlock: Alchemist', ItemClassification.useful, 0x1a9),  # Life water
    ItemData('Job Unlock: Beastmaster', ItemClassification.useful, 0x1a2),  # Bombshell
    ItemData('Job Unlock: Morpher', ItemClassification.useful, 0x19c),  # Chocobo skin
    ItemData('Job Unlock: Sage', ItemClassification.useful, 0x1b2),  # Ancient text
    ItemData('Job Unlock: Fencer', ItemClassification.useful, 0x1ce),  # Bent sword
    ItemData('Job Unlock: Elementalist', ItemClassification.useful, 0x1ea),  # Sprinkler
    ItemData('Job Unlock: Red Mage', ItemClassification.useful, 0x18e),  # Topaz armring
    ItemData('Job Unlock: Summoner', ItemClassification.useful, 0x182),  # Friend pin
    ItemData('Job Unlock: Assassin', ItemClassification.useful, 0x1d7),  # Insignia
    ItemData('Job Unlock: Sniper', ItemClassification.useful, 0x1d8),  # Ally Finder
    ItemData('Job Unlock: Animist', ItemClassification.useful, 0x1bf),  # Stuffed bear
    ItemData('Job Unlock: Mog Knight', ItemClassification.useful, 0x1b4),  # Justice badge
    ItemData('Job Unlock: Gunner', ItemClassification.useful, 0x1c6),  # Fountain pen
    ItemData('Job Unlock: Juggler', ItemClassification.useful, 0x1c7),  # Ear plugs
    ItemData('Job Unlock: Gadgeteer', ItemClassification.useful, 0x1db),  # Loaded dice
]

LawCards: typing.List[ItemData] = [
    #ItemData('Law Card: none', ItemClassification.useful, 0x200),
    ItemData('Law Card: Skills', ItemClassification.useful, 0x201),
    ItemData('Law Card: Techniques', ItemClassification.useful, 0x202),
    ItemData('Law Card: Color Magic', ItemClassification.useful, 0x203),
    ItemData('Law Card: Chivalry', ItemClassification.useful, 0x204),
    ItemData('Law Card: Prayer', ItemClassification.useful, 0x205),
    ItemData('Law Card: Defend', ItemClassification.useful, 0x206),
    ItemData('Law Card: Elementals', ItemClassification.useful, 0x207),
    ItemData('Law Card: Hunt', ItemClassification.useful, 0x208),
    ItemData('Law Card: Charge', ItemClassification.useful, 0x209),
    ItemData('Law Card: Time Magic', ItemClassification.useful, 0x20a),
    ItemData('Law Card: Aim', ItemClassification.useful, 0x20b),
    ItemData('Law Card: Sharpshoot', ItemClassification.useful, 0x20c),
    ItemData('Law Card: Gunmanship', ItemClassification.useful, 0x20d),
    ItemData('Law Card: Steal', ItemClassification.useful, 0x20e),
    ItemData('Law Card: Corner', ItemClassification.useful, 0x20f),
    ItemData('Law Card: Control', ItemClassification.useful, 0x210),
    ItemData('Law Card: Morph', ItemClassification.useful, 0x211),
    ItemData('Law Card: Call', ItemClassification.useful, 0x212),
    ItemData('Law Card: Summon', ItemClassification.useful, 0x213),
    ItemData('Law Card: Items', ItemClassification.useful, 0x214),
    ItemData('Law Card: Fire', ItemClassification.useful, 0x215),
    ItemData('Law Card: Ice', ItemClassification.useful, 0x216),
    ItemData('Law Card: Lightning', ItemClassification.useful, 0x217),
    ItemData('Law Card: Holy', ItemClassification.useful, 0x218),
    ItemData('Law Card: Wind', ItemClassification.useful, 0x219),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x21a),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x21b),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x21c),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x21d),
    ItemData('Law Card: Ganging Up', ItemClassification.useful, 0x21e),
    #ItemData('Law Card: Full HP [dummy]', ItemClassification.useful, 0x21f),
    #ItemData('Law Card: HP > 1/2 [dummy]', ItemClassification.useful, 0x220),
    ItemData('Law Card: Copycat', ItemClassification.useful, 0x221),
    ItemData('Law Card: Fight', ItemClassification.useful, 0x222),
    ItemData('Law Card: Target Area', ItemClassification.useful, 0x223),
    ItemData('Law Card: Target All', ItemClassification.useful, 0x224),
    ItemData('Law Card: Swords', ItemClassification.useful, 0x225),
    ItemData('Law Card: Blades', ItemClassification.useful, 0x226),
    ItemData('Law Card: Sabers', ItemClassification.useful, 0x227),
    ItemData('Law Card: Knightswords', ItemClassification.useful, 0x228),
    ItemData('Law Card: Greatswords', ItemClassification.useful, 0x229),
    ItemData('Law Card: Broadswords', ItemClassification.useful, 0x22a),
    ItemData('Law Card: Knives', ItemClassification.useful, 0x22b),
    ItemData('Law Card: Rapiers', ItemClassification.useful, 0x22c),
    ItemData('Law Card: Katanas', ItemClassification.useful, 0x22d),
    ItemData('Law Card: Spears', ItemClassification.useful, 0x22e),
    ItemData('Law Card: Instruments', ItemClassification.useful, 0x22f),
    ItemData('Law Card: Knuckles', ItemClassification.useful, 0x230),
    ItemData('Law Card: Soul', ItemClassification.useful, 0x231),
    ItemData('Law Card: Missile', ItemClassification.useful, 0x232),
    #ItemData('Law Card: Dark [dummy]', ItemClassification.useful, 0x233),
    #ItemData('Law Card: Staves [dummy]', ItemClassification.useful, 0x234),
    #ItemData('Law Card: Rods [dummy]', ItemClassification.useful, 0x235),
    #ItemData('Law Card: Maces [dummy]', ItemClassification.useful, 0x236),
    #ItemData('Law Card: Bare Hands [dummy]', ItemClassification.useful, 0x237),
    #ItemData('Law Card: Damage > 100 [dummy]', ItemClassification.useful, 0x238),
    #ItemData('Law Card: Heal < 50 [dummy]', ItemClassification.useful, 0x239),
    #ItemData('Law Card: Heal < 100 [dummy]', ItemClassification.useful, 0x23a),
    #ItemData('Law Card: Heal > 50 [dummy]', ItemClassification.useful, 0x23b),
    #ItemData('Law Card: Heal > 100 [dummy]', ItemClassification.useful, 0x23c),
    ItemData('Law Card: Healing', ItemClassification.useful, 0x23d),
    ItemData('Law Card: Petrify', ItemClassification.useful, 0x23e),
    ItemData('Law Card: Frog', ItemClassification.useful, 0x23f),
    ItemData('Law Card: Poison', ItemClassification.useful, 0x240),
    ItemData('Law Card: Confuse', ItemClassification.useful, 0x241),
    ItemData('Law Card: Berserk', ItemClassification.useful, 0x242),
    ItemData('Law Card: Silence', ItemClassification.useful, 0x243),
    ItemData('Law Card: Charm', ItemClassification.useful, 0x244),
    ItemData('Law Card: Bind', ItemClassification.useful, 0x245),
    ItemData('Law Card: Addle', ItemClassification.useful, 0x246),
    ItemData('Law Card: Slow', ItemClassification.useful, 0x247),
    ItemData('Law Card: Stop', ItemClassification.useful, 0x248),
    ItemData('Law Card: Status', ItemClassification.useful, 0x249),
    ItemData('Law Card: Shell', ItemClassification.useful, 0x24a),
    ItemData('Law Card: Protect', ItemClassification.useful, 0x24b),
    ItemData('Law Card: Haste', ItemClassification.useful, 0x24c),
    ItemData('Law Card: Dmg2: Human', ItemClassification.useful, 0x24d),
    ItemData('Law Card: Dmg2: Bangaa', ItemClassification.useful, 0x24e),
    ItemData('Law Card: Dmg2: Nu Mou', ItemClassification.useful, 0x24f),
    ItemData('Law Card: Dmg2: Viera', ItemClassification.useful, 0x250),
    ItemData('Law Card: Dmg2: moogle', ItemClassification.useful, 0x251),
    ItemData('Law Card: Dmg2: Animal', ItemClassification.useful, 0x252),
    ItemData('Law Card: Law Cards', ItemClassification.useful, 0x253),
    ItemData('Law Card: NoClr Magic', ItemClassification.useful, 0x254),
    #ItemData('Law Card: (not used) [dummy]', ItemClassification.useful, 0x255),
    ItemData('Law Card: Skills antilaw', ItemClassification.useful, 0x256),
    ItemData('Law Card: Techniques antilaw', ItemClassification.useful, 0x257),
    ItemData('Law Card: Color Magic antilaw', ItemClassification.useful, 0x258),
    ItemData('Law Card: Chivalry antilaw', ItemClassification.useful, 0x259),
    ItemData('Law Card: Prayer antilaw', ItemClassification.useful, 0x25a),
    ItemData('Law Card: Defend antilaw', ItemClassification.useful, 0x25b),
    ItemData('Law Card: Elementals antilaw', ItemClassification.useful, 0x25c),
    ItemData('Law Card: Hunt antilaw', ItemClassification.useful, 0x25d),
    ItemData('Law Card: Charge antilaw', ItemClassification.useful, 0x25e),
    ItemData('Law Card: Time Magic antilaw', ItemClassification.useful, 0x25f),
    ItemData('Law Card: Aim antilaw', ItemClassification.useful, 0x260),
    ItemData('Law Card: Sharpshoot antilaw', ItemClassification.useful, 0x261),
    ItemData('Law Card: Gunmanship antilaw', ItemClassification.useful, 0x262),
    ItemData('Law Card: Steal antilaw', ItemClassification.useful, 0x263),
    ItemData('Law Card: Corner antilaw', ItemClassification.useful, 0x264),
    ItemData('Law Card: Control antilaw', ItemClassification.useful, 0x265),
    ItemData('Law Card: Morph antilaw', ItemClassification.useful, 0x266),
    ItemData('Law Card: Call antilaw', ItemClassification.useful, 0x267),
    ItemData('Law Card: Summon antilaw', ItemClassification.useful, 0x268),
    ItemData('Law Card: Items antilaw', ItemClassification.useful, 0x269),
    ItemData('Law Card: Fire antilaw', ItemClassification.useful, 0x26a),
    ItemData('Law Card: Ice antilaw', ItemClassification.useful, 0x26b),
    ItemData('Law Card: Lightning antilaw', ItemClassification.useful, 0x26c),
    ItemData('Law Card: Holy antilaw', ItemClassification.useful, 0x26d),
    ItemData('Law Card: Wind antilaw', ItemClassification.useful, 0x26e),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x26f),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x270),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x271),
    #ItemData('Law Card: xxxx [dummy]', ItemClassification.useful, 0x272),
    ItemData('Law Card: Ganging Up antilaw', ItemClassification.useful, 0x273),
    #ItemData('Law Card: Full HP [dummy]', ItemClassification.useful, 0x274),
    #ItemData('Law Card: HP > 1/2 [dummy]', ItemClassification.useful, 0x275),
    ItemData('Law Card: Copycat antilaw', ItemClassification.useful, 0x276),
    ItemData('Law Card: Fight antilaw', ItemClassification.useful, 0x277),
    ItemData('Law Card: Target Area antilaw', ItemClassification.useful, 0x278),
    ItemData('Law Card: Target All antilaw', ItemClassification.useful, 0x279),
    ItemData('Law Card: Swords antilaw', ItemClassification.useful, 0x27a),
    ItemData('Law Card: Blades antilaw', ItemClassification.useful, 0x27b),
    ItemData('Law Card: Sabers antilaw', ItemClassification.useful, 0x27c),
    ItemData('Law Card: Knightswords antilaw', ItemClassification.useful, 0x27d),
    ItemData('Law Card: Greatswords antilaw', ItemClassification.useful, 0x27e),
    ItemData('Law Card: Broadswords antilaw', ItemClassification.useful, 0x27f),
    ItemData('Law Card: Knives antilaw', ItemClassification.useful, 0x280),
    ItemData('Law Card: Rapiers antilaw', ItemClassification.useful, 0x281),
    ItemData('Law Card: Katanas antilaw', ItemClassification.useful, 0x282),
    ItemData('Law Card: Spears antilaw', ItemClassification.useful, 0x283),
    ItemData('Law Card: Instruments antilaw', ItemClassification.useful, 0x284),
    ItemData('Law Card: Knuckles antilaw', ItemClassification.useful, 0x285),
    ItemData('Law Card: Soul antilaw', ItemClassification.useful, 0x286),
    #ItemData('Law Card: Missile [dummy]', ItemClassification.useful, 0x287),
    #ItemData('Law Card: Dark [dummy]', ItemClassification.useful, 0x288),
    #ItemData('Law Card: Staves [dummy]', ItemClassification.useful, 0x289),
    #ItemData('Law Card: Rods [dummy]', ItemClassification.useful, 0x28a),
    #ItemData('Law Card: Maces [dummy]', ItemClassification.useful, 0x28b),
    #ItemData('Law Card: Bare Hands [dummy]', ItemClassification.useful, 0x28c),
    #ItemData('Law Card: Damage > 100 [dummy]', ItemClassification.useful, 0x28d),
    #ItemData('Law Card: Heal < 50 [dummy]', ItemClassification.useful, 0x28e),
    #ItemData('Law Card: Heal < 100 [dummy]', ItemClassification.useful, 0x28f),
    #ItemData('Law Card: Heal > 50 [dummy]', ItemClassification.useful, 0x290),
    #ItemData('Law Card: Heal > 100 [dummy]', ItemClassification.useful, 0x291),
    ItemData('Law Card: Healing antilaw', ItemClassification.useful, 0x292),
    ItemData('Law Card: Petrify antilaw', ItemClassification.useful, 0x293),
    ItemData('Law Card: Frog antilaw', ItemClassification.useful, 0x294),
    ItemData('Law Card: Poison antilaw', ItemClassification.useful, 0x295),
    ItemData('Law Card: Confuse antilaw', ItemClassification.useful, 0x296),
    ItemData('Law Card: Berserk antilaw', ItemClassification.useful, 0x297),
    ItemData('Law Card: Silence antilaw', ItemClassification.useful, 0x298),
    ItemData('Law Card: Charm antilaw', ItemClassification.useful, 0x299),
    ItemData('Law Card: Bind antilaw', ItemClassification.useful, 0x29a),
    ItemData('Law Card: Addle antilaw', ItemClassification.useful, 0x29b),
    ItemData('Law Card: Slow antilaw', ItemClassification.useful, 0x29c),
    ItemData('Law Card: Stop antilaw', ItemClassification.useful, 0x29d),
    ItemData('Law Card: Status antilaw', ItemClassification.useful, 0x29e),
    ItemData('Law Card: Shell antilaw', ItemClassification.useful, 0x29f),
    ItemData('Law Card: Protect antilaw', ItemClassification.useful, 0x2a0),
    ItemData('Law Card: Haste antilaw', ItemClassification.useful, 0x2a1),
    ItemData('Law Card: Dmg2: Human antilaw', ItemClassification.useful, 0x2a2),
    ItemData('Law Card: Dmg2: Bangaa antilaw', ItemClassification.useful, 0x2a3),
    ItemData('Law Card: Dmg2: Nu Mou antilaw', ItemClassification.useful, 0x2a4),
    ItemData('Law Card: Dmg2: Viera antilaw', ItemClassification.useful, 0x2a5),
    ItemData('Law Card: Dmg2: Moogle antilaw', ItemClassification.useful, 0x2a6),
    ItemData('Law Card: Dmg2: Animal antilaw', ItemClassification.useful, 0x2a7),
    ItemData('Law Card: Law Cards antilaw', ItemClassification.useful, 0x2a8),
    ItemData('Law Card: NoClr Magic antilaw', ItemClassification.useful, 0x2a9),
    #ItemData('Law Card: (not used) [dummy]', ItemClassification.useful, 0x2aa),
    ItemData('Law Card: R1 Antilaw', ItemClassification.useful, 0x2ab),
    ItemData('Law Card: R2 Antilaw', ItemClassification.useful, 0x2ac),
    ItemData('Law Card: R3 Antilaw', ItemClassification.useful, 0x2ad),
    ItemData('Law Card: R4 Antilaw', ItemClassification.useful, 0x2ae),
    ItemData('Law Card: R5 Antilaw', ItemClassification.useful, 0x2af),
    ItemData('Law Card: R6 Antilaw', ItemClassification.useful, 0x2b0),
    ItemData('Law Card: Allmighty antilaw', ItemClassification.useful, 0x2b1),
    #ItemData('Law Card: random card', ItemClassification.useful, 0x2ff),
]

TrapItems: typing.List[ItemData] = [
    ItemData('Roulette Trap', ItemClassification.trap, 0x11111),
]

AllItems: typing.List[ItemData] = list(chain(WeaponSwords, WeaponBlades, WeaponSabers, WeaponKnightswords,
                                             WeaponGreatswords, WeaponBroadswords, WeaponKnives, WeaponRapiers,
                                             WeaponKatanas, WeaponStaves, WeaponRods, WeaponMaces, WeaponBows,
                                             WeaponGreatBows, WeaponSpears, WeaponInstruments, WeaponKnuckles,
                                             WeaponSouls, WeaponGuns, EquipShields, EquipHelmets, EquipGloves,
                                             EquipHats, EquipArmor, EquipRings, EquipClothing, EquipRobes, EquipShoes,
                                             MissionUnlockItems, JobUnlocks, TotemaUnlockItems, Consumables,
                                             ProgressiveItems, LawCards, EquipFemale))

SoldierWeapons: typing.List[ItemData] = WeaponSwords + WeaponGreatswords
PaladinWeapons: typing.List[ItemData] = WeaponGreatswords + WeaponKnightswords

WarriorWeapons: typing.List[ItemData] = WeaponSwords + WeaponBroadswords
DefenderWeapons: typing.List[ItemData] = WeaponBroadswords + WeaponKnightswords
DragoonWeapons: typing.List[ItemData] = WeaponSpears + WeaponSwords
TemplarWeapons: typing.List[ItemData] = WeaponKnightswords + WeaponSpears

AssassinWeapons: typing.List[ItemData] = WeaponKatanas + WeaponGreatBows

AllWeapons = list(chain(WeaponSwords, WeaponBlades, WeaponSabers, WeaponKnightswords,
                        WeaponGreatswords, WeaponBroadswords, WeaponKnives, WeaponRapiers,
                        WeaponKatanas, WeaponStaves, WeaponRods, WeaponMaces, WeaponBows,
                        WeaponGreatBows, WeaponSpears, WeaponInstruments, WeaponKnuckles,
                        WeaponSouls, WeaponGuns))

AllOtherEquipment = list(chain(EquipShields, EquipHelmets, EquipGloves, EquipHats, EquipArmor,
                               EquipRings, EquipClothing, EquipRobes, EquipShoes))

AllBuyableItems = list(chain(AllWeapons, AllOtherEquipment, Consumables))

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in AllItems}
items_by_id: typing.Dict[int, ItemData] = {item.itemID: item for item in AllItems}


def create_item_label_to_code_map() -> Dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    offset = 41234532
    label_to_code_map: Dict[str, int] = {}
    for item in AllItems:
        label_to_code_map[item.itemName] = item.itemID + offset

    return label_to_code_map


ShopItem = typing.Tuple[str, typing.Union[str, int]]

VanillaShopTier0: typing.List[str] = [
    "Bronze Helm",
    "Feather Cap",
    "Green Beret",
    "Cuirass",
    "Bronze Armor",
    "Leather Garb",
    "Chain Plate",
    "Hempen Robe",
    "Shortsword",
    "Silver Sword",
    "Sweep Blade",
    "Barong",
    "Falchion",
    "Jack Knife",
    "Scramasax",
    "Jambiya",
    "Stinger",
    "Fleuret",
    "Scarlette",
    "White Staff",
    "Guard Staff",
    "Judge Staff",
    "Rod",
    "Longbow",
    "Char Bow",
    "Thorn Bow",
    "Demon Bell",
    "Glass Bell",
    "War Trumpet",
    "Hard Knuckles",
    "Rising Sun",
    "Aiot Gun",
    "Bronze Shield",
    "Battle Boots",
    "Gauntlets",
    "Potion",
    "Hi-Potion",
    "X-Potion",
    "Antidote",
    "Eye Drops",
    "Echo Screen",
    "Maiden's Kiss",
    "Soft",
    "Holy Water",
    "Bandage",
    "Phoenix Down",
]

VanillaShopTier1: typing.List[str] = [
    "Iron Helm",
    "Iron Armor",
    "Adaman Vest",
    "Survival Vest",
    "Silken Robe",
    "Buster Sword",
    "Shadow Blade",
    "Sun Blade",
    "Atmos Blade",
    "Blue Saber",
    "Shamshir",
    "Apocalypse",
    "Lionheart",
    "Ragnarok",
    "Ancient Sword",
    "Samson Sword",
    "Estoc",
    "Flamberge",
    "Ninja Knife",
    "Murasame",
    "Ashura",
    "Osafune",
    "Kotetsu",
    "Pure Staff",
    "Bless Staff",
    "Firewheel Rod",
    "Thunder Rod",
    "Sleet Rod",
    "Terre Rod",
    "Battle Mace",
    "Energy Mace",
    "Druid Mace",
    "Sage Crosier",
    "Silver Bow",
    "Windslash Bow",
    "Ranger Bow",
    "Cranequin",
    "Javelin",
    "Lava Spear",
    "Ice Lance",
    "Partisan",
    "Conch Shell",
    "Earth Bell",
    "Black Quena",
    "Satyr Flute",
    "Sick Knuckles",
    "Dream Claws",
    "Kaiser Knuckles",
    "Silver Cannon",
    "Round Shield",
]

VanillaShopTier2: typing.List[str] = [
    "Opal Helm",
    "Circlet",
    "Headband",
    "Platemail",
    "Gold Armor",
    "Brigandine",
    "Judo Uniform",
    "Power Sash",
    "Magus Robe",
    "Mistle Robe",
    "Burglar Sword",
    "Flametongue",
    "Air Blade",
    "Icebrand",
    "Kwigon Blade",
    "Ogun Blade",
    "Paraiba Blade",
    "Aqua Saber",
    "Defender",
    "Lohengrin",
    "Predator",
    "Striborg",
    "Kris Knife",
    "Khukuri",
    "Kard",
    "Rondell Dagger",
    "Mage Masher",
    "Kikuichimonji",
    "Heaven's Cloud",
    "Cure Staff",
    "Garnet Staff",
    "Force Rod",
    "Nail Bow",
    "Twin Bow",
    "Gae Bolg",
    "Dragon Whisker",
    "Riot Gun",
    "Chaos Rifle",
    "Opal Shield",
    "Spiked Boots",
    "Dash Boots",
    "Fortune Ring",
    "Scarab",
]

itemGroups: typing.Dict[str, typing.List[str]] = {
    "vanillashoptier0": VanillaShopTier0,
    "vanillashoptier1": VanillaShopTier1,
    "vanillashoptier2": VanillaShopTier2,
    "all": [x.itemName for x in AllBuyableItems],
    "weapons": [x.itemName for x in AllWeapons],
    "otherequipment": [x.itemName for x in AllOtherEquipment],
    "swords": [x.itemName for x in WeaponSwords],
    "blades": [x.itemName for x in WeaponBlades],
    "sabers": [x.itemName for x in WeaponSabers],
    "knightswords": [x.itemName for x in WeaponKnightswords],
    "greatswords": [x.itemName for x in WeaponGreatswords],
    "broadswords": [x.itemName for x in WeaponBroadswords],
    "knives": [x.itemName for x in WeaponKnives],
    "rapiers": [x.itemName for x in WeaponRapiers],
    "katanas": [x.itemName for x in WeaponKatanas],
    "staves": [x.itemName for x in WeaponStaves],
    "rods": [x.itemName for x in WeaponRods],
    "maces": [x.itemName for x in WeaponMaces],
    "bows": [x.itemName for x in WeaponBows],
    "greatbows": [x.itemName for x in WeaponGreatBows],
    "spears": [x.itemName for x in WeaponSpears],
    "instruments": [x.itemName for x in WeaponInstruments],
    "knuckles": [x.itemName for x in WeaponKnuckles],
    "souls": [x.itemName for x in WeaponSouls],
    "guns": [x.itemName for x in WeaponGuns],
    "shields": [x.itemName for x in EquipShields],
    "helmets": [x.itemName for x in EquipHelmets],
    "gloves": [x.itemName for x in EquipGloves],
    "hats": [x.itemName for x in EquipHats],
    "armor": [x.itemName for x in EquipArmor],
    "rings": [x.itemName for x in EquipRings],
    "clothing": [x.itemName for x in EquipClothing],
    "robes": [x.itemName for x in EquipRobes],
    "shoes": [x.itemName for x in EquipShoes],
    "consumables": [x.itemName for x in Consumables],
}
