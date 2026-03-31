from typing import Dict
from collections import Counter
import struct
import math
from typing import TYPE_CHECKING
from logging import warning
if TYPE_CHECKING:
    from .. import EarthBoundWorld
    from ..Rom import LocalRom



class EarthBoundEnemy:
    def __init__(self, name: str, address: int, hp: int, pp: int, exp: int, money: int, speed: int, offense: int,
                 defense: int, level: int, guts: int, luck: int, is_scaled: bool, shield: str | None = None,
                 attack_extensions: int = 0):
        self.name = name
        self.address = address
        self.hp = hp
        self.pp = pp
        self.exp = exp
        self.money = money
        self.speed = speed
        self.offense = offense
        self.defense = defense
        self.level = level
        self.guts = guts
        self.luck = luck
        self.is_scaled = is_scaled
        self.shield = shield
        self.attack_extensions = attack_extensions


def initialize_enemies(world: "EarthBoundWorld") -> None:
    world.enemy_psi = {
        "Dept. Store Spook": ["freeze", "fire", "lifeup", "null"],
        "Dept. Store Spook (2)": ["null", "null", "freeze", "null"],
        "Black Antoid": ["null", "null", "null", "lifeup"],
        "Struttin' Evil Mushroom": ["null", "null", "null", "scatter_spores"],
        "Mobile Sprout": ["null", "null", "null", "lifeup"],
        "Tough Mobile Sprout": ["null", "null", "null", "lifeup"],
        "Mystical Record": ["null", "null", "lifeup", "null"],
        "Guardian Hieroglyph": ["hacking_cough", "thunder_minus", "flash", "thunder"],
        "Electro Swoosh": ["null", "electrical_shock", "electrical_shock", "null"],
        "Conducting Menace": ["flash_minus", "flash", "thunder_minus", "thunder"],
        "Conducting Spirit": ["flash_minus", "flash", "thunder_minus", "thunder"],
        "Ness's Nightmare": ["null", "special", "glorious_light", "null"],
        "Mr. Carpainter": ["crashing_boom_bang", "lifeup", "null", "null"],
        "Carbon Dog": ["flaming_fireball", "null", "null", "null"],
        "Thunder Mite": ["thunder_minus", "thunder_minus", "thunder", "thunder"],
        "Chomposaur": ["fire", "fire", "null", "null"],
        "Gigantic Ant": ["null", "poison_stinger", "null", "null"],
        "Shrooom!": ["null", "lifeup", "scatter_spores", "null"],
        "Plague Rat of Doom": ["poisonous_fangs", "null", "null", "null"],
        "Mondo Mole": ["lifeup", "null", "null", "null"],
        "Scalding Coffee Cup": ["scalding_espresso", "scalding_espresso", "scalding_espresso", "scalding_espresso"],
        "Arachnid!": ["null", "null", "null", "poison_stinger"],
        "Arachnid!!!": ["poison_stinger", "null", "null", "null"],
        "Slimy Little Pile": ["hacking_cough", "null", "null", "null"],
        "Even Slimier Little Pile": ["null", "null", "null", "hacking_cough"],
        "Kraken": ["breathe_fire", "null", "crashing_boom_bang", "null"],
        "Bionic Kraken": ["null", "crashing_boom_bang", "breathe_fire", "null"],  # Generate tornado?
        "Spinning Robo": ["null", "null", "stuffiness_beam", "null"],
        "Whirling Robo": ["null", "stuffiness_beam", "null", "null"],
        "Thirsty Coil Snake": ["poisonous_fangs", "null", "null", "null"],
        "Crazed Sign": ["null", "null", "paralysis", "null"],
        "Wooly Shambler": ["null", "null", "null", "flash"],
        "Wild 'n Wooly Shambler": ["null", "null", "null", "flash"],
        "Skelpion": ["null", "poison_stinger", "null", "thunder"],
        "Dread Skelpion": ["poison_stinger", "null", "thunder", "thunder"],
        "Ghost of Starman": ["starstorm_minus", "null", "null", "null"],
        "Smilin' Sphere": ["null", "fire", "null", "null"],
        "Uncontrollable Sphere": ["null", "fire", "fire", "null"],
        "Starman Deluxe": ["null", "null", "starstorm", "null"],
        "Final Starman": ["null", "null", "starstorm", "null"],
        "Urban Zombie": ["null", "null", "nauseous_breath", "null"],
        "Zombie Dog": ["null", "null", "null", "poisonous_fangs"],
        "Diamond Dog": ["null", "null", "null", "glorious_light"],
        "Trillionage Sprout": ["null", "null", "flash", "paralysis"],
        "Musica": ["electrical_shock", "null", "null", "electrical_shock"],
        "Desert Wolf": ["null", "null", "null", "poisonous_fangs"],
        "Master Belch": ["nauseous_breath", "nauseous_breath", "null", "null"],
        "Big Pile of Puke": ["null", "hacking_cough", "null", "nauseous_breath"],
        "Master Barf": ["nauseous_breath", "null", "null", "null"],
        "Kiss of Death": ["null", "null", "kiss_of_death", "null"],
        "French Kiss of Death": ["kiss_of_death", "kiss_of_death", "kiss_of_death", "kiss_of_death"],
        "Zap Eel": ["electrical_shock", "electrical_shock", "electrical_shock", "electrical_shock"],
        "Tangoo": ["null", "null", "poison_flute", "null"],
        "Squatter Demon": ["poisonous_fangs", "diamond_bite", "null", "null"],
        "Lesser Mook": ["freeze", "freeze", "null", "diamond_eyes"],
        "Mook Senior": ["freeze", "fire", "lifeup", "diamond_eyes"],
        "Smelly Ghost": ["null", "null", "lifeup", "null"],
        "Deadly Mouse": ["poisonous_fangs", "null", "null", "null"],
        "Care Free Bomb": ["throw_bomb_minus", "throw_bomb_minus", "throw_bomb_minus", "throw_bomb"],
        "Electro Specter": ["electrical_shock", "null", "electrical_shock", "null"],
        "Smilin' Sam": ["null", "null", "null", "lifeup"],
        "Manly Fish's Brother": ["null", "paralysis", "freeze", "healing"],
        "Thunder and Storm": ["crashing_boom_bang", "null", "null", "null"],
        "Cute Li'l UFO": ["null", "null", "null", "lifeup"],
        "Beautiful UFO": ["null", "null", "null", "lifeup"],
        "Evil Mani-Mani": ["null", "paralysis", "null", "null"],
        "Mr. Molecule": ["thunder", "flash", "fire", "freeze"],
        "Sentry Robot": ["null", "null", "null", "shoot_rocket"],
        "Psychic Psycho": ["fire", "fire", "fire", "fire"],
        "Major Psychic Psycho": ["fire", "null", "paralysis", "fire"],
        "Soul Consuming Flame": ["null", "breathe_fire", "flaming_fireball", "spray_fire"],
        "Demonic Petunia": ["null", "extinguishing_blast", "null", "paralyzing_pollen"],
        "Li'l UFO": ["null", "null", "stuffiness_beam", "null"],
        "Robo-Pump (2)": ["throw_bomb", "null", "null", "null"],
        "Ness's Nightmare (2)": ["special", "lifeup", "special", "null"],
        "Mr. Carpainter (2)": ["crashing_boom_bang", "null", "null", "null"],
        "Carbon Dog (2)": ["spray_fire", "null", "null", "null"],
        "Gigantic Ant (2)": ["paralysis", "null", "null", "null"],
        "Chomposaur (2)": ["null", "null", "fire", "fire"],
        "Guardian Digger (2)": ["null", "null", "null", "lifeup"],
        "Kraken (2)": ["flash", "breathe_fire", "null", "null"],  # tornado?
        "Starman Super (2)": ["null", "healing", "null", "null"],
        "Ghost of Starman (2)": ["null", "null", "starstorm", "null"],
        "Final Starman (2)": ["starstorm", "null", "healing", "null"],
        "Diamond Dog (2)": ["null", "null", "null", "diamond_bite"],
        "Trillionage Sprout (2)": ["null", "null", "diamond_eyes", "null"],
        "Master Belch (2)": ["nauseous_breath", "null", "null", "null"],
        "Master Barf (2)": ["null", "null", "nauseous_breath", "null"],
        "Boogey Tent (2)": ["null", "null", "flash", "null"],
        "Electro Specter (2)": ["null", "null", "electrical_shock", "null"],
        "Thunder and Storm (2)": ["summon_storm", "null", "crashing_boom_bang", "null"],
        "Evil Mani-Mani (2)": ["null", "null", "glorious_light", "null"],
        "Black Antoid (2)": ["lifeup", "lifeup", "lifeup", "lifeup"],
        "Giygas (2)": ["special", "special", "special", "special"],
        "Farm Zombie": ["null", "null", "nauseous_breath", "null"],
        "Criminal Caterpillar": ["fire", "fire", "fire", "fire"],
        "Evil Eye": ["null", "diamond_eyes", "paralysis", "null"],
        "Master Criminal Worm": ["fire", "fire", "fire", "fire"],
        "Giygas": ["giygas_phase2_thunder", "giygas_phase2_freeze", "giygas_phase2_flash", "null"],
        "Giygas (5)": ["giygas_phase3_thunder", "giygas_phase3_freeze", "giygas_phase3_flash", "null"],
        "Giygas (6)": ["giygas_phase4_thunder", "giygas_phase4_freeze", "giygas_phase4_flash", "null"],
        "Starman Junior": ["fire", "null", "freeze", "fire"],
        "Ultimate Octobot": ["null", "stuffiness_beam", "null", "stuffiness_beam"],
        "Mechanical Octobot": ["null", "null", "null", "stuffiness_beam"]
    }

    world.enemy_sprites = {
        "Insane Cultist": 0x0065,
        "Armored Frog": 0x0118,
        "Bad Buffalo": 0x0137,
        "Black Antoid": 0x013C,
        "Black Antoid (2)": 0x013C,
        "Red Antoid": 0x013C,
        "Ramblin' Evil Mushroom": 0x0123,
        "Struttin' Evil Mushroom": 0x0123,
        "Mobile Sprout": 0x013D,
        "Tough Mobile Sprout": 0x013D,
        "Enraged Fire Plug": 0x0117,
        "Mystical Record": 0x00C3,
        "Atomic Power Robot": 0x0132,
        "Nuclear Reactor Robot": 0x0132,
        "Guardian Hieroglyph": 0x0145,
        "Lethal Asp Hieroglyph": 0x0140,
        "Electro Swoosh": 0x0114,
        "Conducting Menace": 0x0144,
        "Conducting Spirit": 0x0144,
        "Evil Elemental": 0x0117,
        "Annoying Old Party Man": 0x0187,
        "Annoying Reveler": 0x0187,
        "Unassuming Local Guy": 0x0045,
        "New Age Retro Hippie": 0x0169,
        "Mighty Bear": 0x014B,
        "Mighty Bear Seven": 0x014B,
        "Putrid Moldyman": 0x011D,
        "Thunder Mite": 0x0144,
        "Cranky Lady": 0x0188,
        "Extra Cranky Lady": 0x0188,
        "Wetnosaur": 0x012A,
        "Chomposaur": 0x0138,
        "Gigantic Ant": 0x0139,
        "Scalding Coffee Cup": 0x00C3,
        "Loaded Dice": 0x00C3,
        "Slimy Little Pile": 0x013B,
        "Even Slimier Little Pile": 0x013B,
        "Arachnid!": 0x013A,
        "Arachnid!!!": 0x013A,
        "Bionic Kraken": 0x0132,
        "Spinning Robo": 0x0132,
        "Whirling Robo": 0x0132,
        "Hyper Spinning Robo": 0x0132,
        "Cop": 0x004A, 
        "Coil Snake": 0x011B,
        "Thirsty Coil Snake": 0x011B,
        "Mr. Batty": 0x0112,
        "Elder Batty": 0x0112,
        "Violent Roach": 0x013A,
        "Filthy Attack Roach": 0x013A,
        "Crazed Sign": 0x0135,
        "Wooly Shambler": 0x0132,
        "Wild 'n Wooly Shambler": 0x0132,
        "Skate Punk": 0x011C,
        "Skelpion": 0x013F, 
        "Dread Skelpion": 0x013F,
        "Starman": 0x012F,
        "Starman Super": 0x012F,
        "Ghost of Starman": 0x0132,
        "Smilin' Sphere": 0x012E,
        "Uncontrollable Sphere": 0x012E,
        "Petrified Royal Guard": 0x0142,
        "Final Starman": 0x0132,
        "Urban Zombie": 0x0134,
        "Zombie Possessor": 0x0131,
        "Zombie Dog": 0x016C,
        "Over Zealous Cop": 0x0182,
        "Territorial Oak": 0x0129,
        "Hostile Elder Oak": 0x0129,
        "Marauder Octobot": 0x0132,
        "Military Octobot": 0x0132,
        "Mechanical Octobot": 0x0132,
        "Ultimate Octobot": 0x0132,
        "Mad Duck": 0x011F,
        "Dali's Clock": 0x0146,
        "Musica": 0x00C3,
        "Desert Wolf": 0x014A,
        "Big Pile of Puke": 0x0148,
        "Kiss of Death": 0x0144,
        "French Kiss of Death": 0x0115,
        "Foppy": 0x0116,
        "Fobby": 0x0116,
        "Zap Eel": 0x012D,
        "Tangoo": 0x0144,
        "Squatter Demon": 0x0132,
        "Crested Booka": 0x0128,
        "Great Crested Booka": 0x0128,
        "Lesser Mook": 0x0132,
        "Mook Senior": 0x0132,
        "Smelly Ghost": 0x011D,
        "Stinky Ghost": 0x011D,
        "Attack Slug": 0x013C,
        "Pit Bull Slug": 0x013C,
        "Rowdy Mouse": 0x01A0,
        "Deadly Mouse": 0x01A0,
        "Care Free Bomb": 0x0115,
        "Handsome Tom": 0x011E,
        "Smilin' Sam": 0x011E,
        "Manly Fish": 0x0120,
        "Manly Fish's Brother": 0x0120,
        "Runaway Dog": 0x014A,
        "Trick or Trick Kid": 0x01BC,
        "Cave Boy": 0x0149,
        "Abstract Art": 0x012C,
        "Shattered Man": 0x0142,
        "Fierce Shattered Man": 0x0133,
        "Ego Orb": 0x0147,
        "Yes Man Junior": 0x011C,
        "Cute Li'l UFO": 0x0130,
        "Beautiful UFO": 0x0130,
        "Pogo Punk": 0x011C,
        "Tough Guy": 0x0186,
        "Mad Taxi": 0x0121,
        "Mr. Molecule": 0x0115,
        "Worthless Protoplasm": 0x00C3,
        "Sentry Robot": 0x0136,
        "Psychic Psycho": 0x0117,
        "Major Psychic Psycho": 0x0117,
        "Mole Playing Rough": 0x019F,
        "Gruff Goat": 0x0126,
        "Soul Consuming Flame": 0x0117,
        "Demonic Petunia": 0x0122,
        "Ranboob": 0x0124,
        "Li'l UFO": 0x0130,
        "High-class UFO": 0x0130,
        "Noose Man": 0x0143,
        "Robo-pump": 0x0117,
        "Plain Crocodile": 0x014C,
        "Strong Crocodile": 0x014C,
        "Hard Crocodile": 0x014C,
        "No Good Fly": 0x013E,
        "Mostly Bad Fly": 0x013E,
        "Spiteful Crow": 0x011A,
        "Farm Zombie": 0x0134,
        "Criminal Caterpillar": 0x01A1,
        "Evil Eye": 0x0132,
        "Master Criminal Worm": 0x01CD,
        "Loaded Dice 2": 0x00C3,
}

    world.enemies = {
        "Insane Cultist": EarthBoundEnemy("Insane Cultist", 0x1595e7, 94, 0, 353, 33, 8, 19, 25, 13, 20, 64, False),
        "Dept. Store Spook": EarthBoundEnemy("Dept. Store Spook", 0x159645, 610, 290, 24291, 1648, 19, 82, 135, 42, 24, 62, False, None, 2),
        "Armored Frog": EarthBoundEnemy("Armored Frog", 0x1596a3, 202, 0, 1566, 77, 7, 37, 108, 22, 5, 8, False),
        "Bad Buffalo": EarthBoundEnemy("Bad Buffalo", 0x159701, 341, 0, 4108, 172, 11, 64, 104, 34, 5, 5, False),
        "Black Antoid": EarthBoundEnemy("Black Antoid", 0x15975f, 34, 25, 37, 7, 4, 14, 13, 7, 3, 0, False),
        "Red Antoid": EarthBoundEnemy("Red Antoid", 0x1597bd, 112, 30, 1175, 35, 10, 29, 27, 20, 4, 0, False),
        "Ramblin' Evil Mushroom": EarthBoundEnemy("Ramblin' Evil Mushroom", 0x15981b, 60, 0, 95, 15, 5, 15, 10, 7, 5, 1, False),
        "Struttin' Evil Mushroom": EarthBoundEnemy("Struttin' Evil Mushroom", 0x159879, 157, 0, 1492, 95, 28, 29, 22, 17, 7, 1, False),
        "Mobile Sprout": EarthBoundEnemy("Mobile Sprout", 0x1598d7, 79, 9, 133, 13, 6, 17, 12, 10, 5, 1, False),
        "Tough Mobile Sprout": EarthBoundEnemy("Tough Mobile Sprout", 0x159935, 179, 13, 1865, 119, 18, 33, 27, 21, 6, 1, False),
        "Enraged Fire Plug": EarthBoundEnemy("Enraged Fire Plug", 0x159993, 309, 0, 4321, 346, 14, 60, 81, 32, 5, 4, False),
        "Mystical Record": EarthBoundEnemy("Mystical Record", 0x1599f1, 263, 35, 2736, 310, 20, 63, 78, 33, 12, 7, False),
        "Atomic Power Robot": EarthBoundEnemy("Atomic Power Robot", 0x159a4f, 594, 0, 26937, 730, 25, 119, 133, 56, 8, 12, False),
        "Nuclear Reactor Robot": EarthBoundEnemy("Nuclear Reactor Robot", 0x159aad, 798, 0, 53142, 820, 46, 142, 185, 64, 8, 12, False),
        "Guardian Hieroglyph": EarthBoundEnemy("Guardian Hieroglyph", 0x159b0b, 470, 126, 13064, 470, 20, 94, 106, 48, 20, 38, False),
        "Lethal Asp Hieroglyph": EarthBoundEnemy("Lethal Asp Hieroglyph", 0x159b69, 458, 0, 11321, 625, 21, 89, 94, 46, 5, 36, False),
        "Electro Swoosh": EarthBoundEnemy("Electro Swoosh", 0x159bc7, 543, 338, 17075, 791, 40, 140, 156, 62, 5, 10, False),
        "Conducting Menace": EarthBoundEnemy("Conducting Menace", 0x159c25, 445, 238, 14792, 574, 20, 107, 107, 52, 5, 8, False),
        "Conducting Spirit": EarthBoundEnemy("Conducting Spirit", 0x159c83, 587, 329, 30390, 804, 26, 130, 139, 59, 5, 8, False),
        "Evil Elemental": EarthBoundEnemy("Evil Elemental", 0x159ce1, 564, 0, 35737, 853, 30, 121, 136, 57, 7, 16, False),
        "Ness's Nightmare": EarthBoundEnemy("Ness's Nightmare", 0x159d3f, 1654, 882, 89004, 4442, 31, 172, 253, 71, 1, 80, False, "psi_1", 2),
        "Annoying Old Party Man": EarthBoundEnemy("Annoying Old Party Man", 0x159d9d, 99, 0, 130, 32, 6, 20, 25, 13, 50, 15, False),
        "Annoying Reveler": EarthBoundEnemy("Annoying Reveler", 0x159dfb, 288, 0, 2373, 268, 17, 58, 77, 31, 50, 15, False),
        "Unassuming Local Guy": EarthBoundEnemy("Unassuming Local Guy", 0x159e59, 73, 0, 146, 19, 5, 18, 13, 9, 1, 14, False),
        "New Age Retro Hippie": EarthBoundEnemy("New Age Retro Hippie", 0x159eb7, 87, 0, 160, 23, 5, 19, 14, 11, 10, 16, False),
        "Mr. Carpainter": EarthBoundEnemy("Mr. Carpainter", 0x159f15, 262, 70, 1412, 195, 8, 33, 45, 21, 13, 72, False, None, 2),
        "Carbon Dog": EarthBoundEnemy("Carbon Dog", 0x159f73, 1672, 0, 0, 0, 31, 159, 174, 70, 52, 53, False, None, 2),
        "Mighty Bear": EarthBoundEnemy("Mighty Bear", 0x159fd1, 167, 0, 609, 49, 7, 29, 31, 16, 1, 5, False),
        "Mighty Bear Seven": EarthBoundEnemy("Mighty Bear Seven", 0x15a02f, 367, 0, 8884, 440, 11, 85, 76, 42, 1, 4, False),
        "Putrid Moldyman": EarthBoundEnemy("Putrid Moldyman", 0x15a08d, 203, 0, 830, 53, 9, 36, 41, 21, 5, 17, False),
        "Thunder Mite": EarthBoundEnemy("Thunder Mite", 0x15a0eb, 293, 200, 10798, 430, 20, 85, 83, 43, 13, 8, False),
        "Cranky Lady": EarthBoundEnemy("Cranky Lady", 0x15a149, 95, 0, 200, 17, 6, 16, 18, 8, 3, 32, False),
        "Extra Cranky Lady": EarthBoundEnemy("Extra Cranky Lady", 0x15a1a7, 277, 0, 3651, 134, 17, 48, 70, 27, 5, 32, False),
        "Wetnosaur": EarthBoundEnemy("Wetnosaur", 0x15a263, 1030, 0, 33098, 745, 17, 126, 172, 59, 2, 16, False),
        "Chomposaur": EarthBoundEnemy("Chomposaur", 0x15a2c1, 1288, 320, 44378, 896, 17, 139, 183, 62, 3, 16, False, "phys_2", 2),
        "Titanic Ant": EarthBoundEnemy("Titanic Ant", 0x15a31f, 235, 102, 685, 150, 6, 19, 23, 13, 9, 72, False, None, 2),
        "Gigantic Ant": EarthBoundEnemy("Gigantic Ant", 0x15a37d, 308, 81, 3980, 304, 17, 54, 112, 30, 5, 6, False, None, 2),
        "Shrooom!": EarthBoundEnemy("Shrooom!", 0x15a3db, 1700, 112, 96323, 4086, 18, 95, 154, 48, 32, 72, False, None, 2),
        "Plague Rat of Doom": EarthBoundEnemy("Plague Rat of Doom", 0x15a439, 1827, 60, 115272, 4464, 19, 71, 180, 47, 250, 45, False, None, 2),
        "Mondo Mole": EarthBoundEnemy("Mondo Mole", 0x15a497, 498, 161, 5791, 400, 9, 37, 50, 23, 15, 36, False, None, 2),
        "Guardian Digger": EarthBoundEnemy("Guardian Digger", 0x15a4f5, 386, 110, 17301, 1467, 17, 59, 129, 32, 21, 55, False, "phys_2", 2),
        "Scalding Coffee Cup": EarthBoundEnemy("Scalding Coffee Cup", 0x15a553, 190, 0, 2462, 280, 23, 55, 20, 30, 5, 1, False),
        "Loaded Dice": EarthBoundEnemy("Loaded Dice", 0x15a5b1, 307, 0, 10672, 703, 77, 146, 113, 59, 75, 6, False, None),
        "Slimy Little Pile": EarthBoundEnemy("Slimy Little Pile", 0x15a60f, 224, 0, 1978, 124, 15, 42, 61, 24, 7, 38, False),
        "Even Slimier Little Pile": EarthBoundEnemy("Even Slimier Little Pile", 0x15a66d, 326, 0, 15075, 579, 22, 103, 101, 49, 9, 38, False),
        "Arachnid!": EarthBoundEnemy("Arachnid!", 0x15a6cb, 216, 0, 4933, 296, 23, 61, 30, 32, 3, 0, False),
        "Arachnid!!!": EarthBoundEnemy("Arachnid!!!", 0x15a729, 344, 0, 10449, 412, 20, 87, 86, 45, 4, 0, False),
        "Kraken": EarthBoundEnemy("Kraken", 0x15a787, 1097, 176, 79267, 3049, 21, 105, 166, 54, 1, 32, False, None, 2),
        "Bionic Kraken": EarthBoundEnemy("Bionic Kraken", 0x15a7e5, 900, 60, 50308, 960, 42, 155, 195, 70, 1, 32, False),
        "Spinning Robo": EarthBoundEnemy("Spinning Robo", 0x15a843, 113, 17, 297, 21, 7, 21, 22, 14, 5, 12, False),
        "Whirling Robo": EarthBoundEnemy("Whirling Robo", 0x15a8a1, 374, 36, 5782, 256, 18, 78, 90, 39, 5, 12, False),
        "Hyper Spinning Robo": EarthBoundEnemy("Hyper Spinning Robo", 0x15a8ff, 553, 83, 28866, 756, 28, 122, 130, 56, 5, 12, False),
        "Cop": EarthBoundEnemy("Cop", 0x15a95d, 75, 0, 86, 18, 5, 15, 18, 7, 7, 16, False),
        "Coil Snake": EarthBoundEnemy("Coil Snake", 0x15a9bb, 18, 0, 1, 4, 2, 3, 4, 1, 0, 6, False),
        "Thirsty Coil Snake": EarthBoundEnemy("Thirsty Coil Snake", 0x15aa19, 270, 0, 2786, 276, 18, 52, 80, 28, 5, 7, False),
        "Mr. Batty": EarthBoundEnemy("Mr. Batty", 0x15aa77, 86, 0, 304, 30, 29, 25, 5, 15, 4, 3, False),
        "Elder Batty": EarthBoundEnemy("Elder Batty", 0x15aad5, 294, 0, 4177, 371, 33, 66, 72, 35, 8, 4, False),
        "Violent Roach": EarthBoundEnemy("Violent Roach", 0x15ab33, 209, 0, 1757, 80, 35, 30, 26, 18, 9, 24, False),
        "Filthy Attack Roach": EarthBoundEnemy("Filthy Attack Roach", 0x15ab91, 399, 0, 10543, 432, 77, 84, 33, 42, 9, 24, False),
        "Crazed Sign": EarthBoundEnemy("Crazed Sign", 0x15abef, 295, 98, 3618, 244, 17, 64, 96, 34, 5, 11, False),
        "Wooly Shambler": EarthBoundEnemy("Wooly Shambler", 0x15ac4d, 391, 140, 5397, 458, 18, 81, 91, 40, 5, 63, False),
        "Wild 'n Wooly Shambler": EarthBoundEnemy("Wild 'n Wooly Shambler", 0x15acab, 722, 212, 33818, 906, 38, 144, 171, 65, 5, 63, False),
        "Skate Punk": EarthBoundEnemy("Skate Punk", 0x15ad09, 31, 0, 12, 17, 5, 7, 8, 3, 0, 13, False),
        "Skelpion": EarthBoundEnemy("Skelpion", 0x15ad67, 137, 21, 1823, 140, 37, 41, 23, 24, 80, 7, False),
        "Dread Skelpion": EarthBoundEnemy("Dread Skelpion", 0x15adc5, 214, 125, 9908, 609, 40, 82, 57, 41, 88, 8, False),
        "Starman": EarthBoundEnemy("Starman", 0x15ae23, 545, 155, 23396, 720, 24, 103, 126, 55, 25, 16, False, None, 2),
        "Starman Super": EarthBoundEnemy("Starman Super", 0x15ae81, 568, 310, 30145, 735, 24, 112, 129, 56, 25, 16, False, "psi_2", 1),
        "Ghost of Starman": EarthBoundEnemy("Ghost of Starman", 0x15aedf, 750, 462, 48695, 807, 46, 152, 170, 68, 43, 16, False, None, 2),
        "Smilin' Sphere": EarthBoundEnemy("Smilin' Sphere", 0x15af3d, 233, 60, 2218, 191, 17, 50, 65, 27, 5, 13, False),
        "Uncontrollable Sphere": EarthBoundEnemy("Uncontrollable Sphere", 0x15af9b, 577, 180, 20389, 796, 27, 116, 134, 56, 5, 15, False, "psi_1"),
        "Petrified Royal Guard": EarthBoundEnemy("Petrified Royal Guard", 0x15aff9, 573, 0, 19163, 628, 12, 106, 173, 53, 5, 5, False),
        "Guardian General": EarthBoundEnemy("Guardian General", 0x15b057, 831, 6, 95390, 3235, 21, 109, 214, 55, 1, 7, False, None, 2),
        "Starman Deluxe": EarthBoundEnemy("Starman Deluxe", 0x15b0b5, 1400, 418, 160524, 3827, 27, 143, 186, 65, 43, 21, False, "psi_2", 2),
        "Final Starman": EarthBoundEnemy("Final Starman", 0x15b113, 840, 860, 61929, 915, 47, 178, 187, 71, 25, 24, False, "psi_2", 2),
        "Urban Zombie": EarthBoundEnemy("Urban Zombie", 0x15b171, 171, 0, 700, 58, 10, 31, 24, 19, 15, 24, False),
        "Zombie Possessor": EarthBoundEnemy("Zombie Possessor", 0x15b1cf, 176, 0, 950, 81, 30, 28, 19, 17, 9, 6, False),
        "Zombie Dog": EarthBoundEnemy("Zombie Dog", 0x15b22d, 210, 0, 1354, 54, 30, 39, 51, 22, 10, 11, False),
        "Over Zealous Cop": EarthBoundEnemy("Over Zealous Cop", 0x15b2e9, 325, 0, 7448, 420, 18, 69, 75, 36, 7, 16, False),
        "Territorial Oak": EarthBoundEnemy("Territorial Oak", 0x15b347, 145, 41, 356, 29, 5, 26, 30, 15, 9, 4, False),
        "Hostile Elder Oak": EarthBoundEnemy("Hostile Elder Oak", 0x15b3a5, 609, 76, 17567, 690, 14, 134, 146, 59, 11, 5, False),
        "Diamond Dog": EarthBoundEnemy("Diamond Dog", 0x15b403, 3344, 154, 337738, 6968, 31, 167, 230, 70, 10, 47, False, "phys_2", 2),
        "Marauder Octobot": EarthBoundEnemy("Marauder Octobot", 0x15b461, 482, 0, 14475, 499, 23, 99, 121, 49, 8, 24, False),
        "Military Octobot": EarthBoundEnemy("Military Octobot", 0x15b4bf, 604, 0, 25607, 637, 26, 138, 147, 61, 8, 18, False),
        "Mechanical Octobot": EarthBoundEnemy("Mechanical Octobot", 0x15b51d, 768, 0, 41738, 744, 43, 147, 176, 66, 8, 24, False),
        "Ultimate Octobot": EarthBoundEnemy("Ultimate Octobot", 0x15b57b, 792, 0, 47876, 815, 44, 163, 181, 70, 8, 24, False),
        "Mad Duck": EarthBoundEnemy("Mad Duck", 0x15b5d9, 51, 0, 41, 12, 30, 12, 24, 8, 5, 1, False),
        "Dali's Clock": EarthBoundEnemy("Dali's Clock", 0x15b637, 296, 0, 2503, 314, 4, 65, 66, 34, 5, 4, False),
        "Trillionage Sprout": EarthBoundEnemy("Trillionage Sprout", 0x15b695, 1048, 240, 30303, 1358, 16, 54, 88, 29, 21, 71, False, None, 2),
        "Musica": EarthBoundEnemy("Musica", 0x15b6f3, 292, 0, 3748, 341, 21, 69, 85, 35, 20, 8, False),
        "Desert Wolf": EarthBoundEnemy("Desert Wolf", 0x15b751, 247, 0, 3740, 114, 33, 57, 67, 30, 2, 11, False),
        "Master Belch": EarthBoundEnemy("Master Belch", 0x15b7af, 650, 0, 12509, 664, 16, 50, 88, 27, 20, 61, False, None, 2),  # Real one
        "Big Pile of Puke": EarthBoundEnemy("Big Pile of Puke", 0x15b80d, 631, 0, 19659, 728, 16, 120, 158, 57, 26, 32, False),
        "Master Barf": EarthBoundEnemy("Master Barf", 0x15b86b, 1319, 0, 125056, 3536, 24, 136, 177, 60, 39, 64, False, None, 2),
        "Kiss of Death": EarthBoundEnemy("Kiss of Death", 0x15b8c9, 333, 0, 10354, 528, 19, 91, 100, 46, 7, 16, False),
        "French Kiss of Death": EarthBoundEnemy("French Kiss of Death", 0x15b927, 588, 0, 19210, 879, 30, 160, 160, 70, 7, 16, False),
        "Foppy": EarthBoundEnemy("Foppy", 0x15b985, 120, 10, 1311, 93, 1, 29, 9, 16, 5, 3, False),
        "Fobby": EarthBoundEnemy("Fobby", 0x15b9e3, 240, 19, 18348, 620, 5, 98, 84, 48, 5, 3, False),
        "Zap Eel": EarthBoundEnemy("Zap Eel", 0x15ba41, 370, 0, 12170, 611, 29, 97, 93, 48, 5, 8, False),
        "Tangoo": EarthBoundEnemy("Tangoo", 0x15ba9f, 371, 5, 14718, 572, 19, 96, 99, 48, 20, 16, False),
        "Boogey Tent": EarthBoundEnemy("Boogey Tent", 0x15bafd, 579, 56, 5500, 407, 10, 43, 69, 25, 16, 32, False, None, 2),
        "Squatter Demon": EarthBoundEnemy("Squatter Demon", 0x15bb5b, 774, 60, 48311, 897, 45, 158, 192, 69, 25, 32, False),
        "Crested Booka": EarthBoundEnemy("Crested Booka", 0x15bbb9, 265, 0, 3011, 130, 17, 53, 73, 28, 24, 37, False),
        "Great Crested Booka": EarthBoundEnemy("Great Crested Booka", 0x15bc17, 452, 0, 16365, 604, 20, 100, 110, 49, 28, 40, False),
        "Lesser Mook": EarthBoundEnemy("Lesser Mook", 0x15bc75, 401, 190, 7640, 467, 17, 76, 102, 39, 7, 16, False),
        "Mook Senior": EarthBoundEnemy("Mook Senior", 0x15bcd3, 501, 700, 21056, 715, 25, 108, 122, 54, 7, 16, False),
        "Smelly Ghost": EarthBoundEnemy("Smelly Ghost", 0x15bd31, 194, 50, 606, 71, 10, 35, 89, 21, 2, 9, False),
        "Stinky Ghost": EarthBoundEnemy("Stinky Ghost", 0x15bd8f, 444, 0, 13179, 541, 18, 90, 179, 46, 4, 7, False),
        "Everdred": EarthBoundEnemy("Everdred", 0x15bded, 182, 0, 986, 171, 6, 25, 35, 15, 10, 40, False, None, 2),
        "Attack Slug": EarthBoundEnemy("Attack Slug", 0x15be4b, 30, 6, 27, 6, 1, 9, 2, 5, 0, 3, False),
        "Pit Bull Slug": EarthBoundEnemy("Pit Bull Slug", 0x15bea9, 217, 11, 9994, 543, 2, 79, 77, 39, 5, 7, False),
        "Rowdy Mouse": EarthBoundEnemy("Rowdy Mouse", 0x15bf07, 36, 0, 34, 9, 5, 7, 20, 6, 225, 2, False),
        "Deadly Mouse": EarthBoundEnemy("Deadly Mouse", 0x15bf65, 416, 0, 9225, 406, 18, 63, 98, 38, 225, 13, False),
        "Care Free Bomb": EarthBoundEnemy("Care Free Bomb", 0x15bfc3, 504, 0, 14941, 641, 31, 135, 215, 60, 15, 8, False),
        "Electro Specter": EarthBoundEnemy("Electro Specter", 0x15c021, 3092, 80, 261637, 6564, 29, 148, 203, 67, 47, 56, False, "psi_2", 2),
        "Handsome Tom": EarthBoundEnemy("Handsome Tom", 0x15c07f, 133, 16, 520, 45, 11, 27, 25, 16, 5, 8, False),
        "Smilin' Sam": EarthBoundEnemy("Smilin' Sam", 0x15c0dd, 161, 55, 712, 48, 17, 34, 44, 20, 16, 16, False),
        "Manly Fish": EarthBoundEnemy("Manly Fish", 0x15c13b, 500, 0, 15826, 624, 22, 83, 114, 42, 9, 20, False),
        "Manly Fish's Brother": EarthBoundEnemy("Manly Fish's Brother", 0x15c199, 526, 210, 15970, 686, 24, 114, 123, 56, 11, 24, False),
        "Runaway Dog": EarthBoundEnemy("Runaway Dog", 0x15c1f7, 21, 0, 4, 3, 26, 4, 5, 2, 0, 1, False),
        "Trick or Trick Kid": EarthBoundEnemy("Trick or Trick Kid", 0x15c255, 142, 0, 570, 47, 7, 30, 37, 18, 12, 12, False),
        "Cave Boy": EarthBoundEnemy("Cave Boy", 0x15c2b3, 314, 0, 618, 17, 79, 21, 33, 14, 0, 80, False),
        "Abstract Art": EarthBoundEnemy("Abstract Art", 0x15c311, 301, 60, 4361, 255, 19, 67, 79, 35, 7, 7, False),
        "Shattered Man": EarthBoundEnemy("Shattered Man", 0x15c36f, 694, 0, 44690, 2630, 18, 104, 138, 51, 25, 38, False),
        "Fierce Shattered Man": EarthBoundEnemy("Fierce Shattered Man", 0x15c3cd, 516, 0, 17423, 577, 12, 101, 116, 50, 5, 4, False),
        "Ego Orb": EarthBoundEnemy("Ego Orb", 0x15c42b, 592, 0, 24180, 836, 17, 125, 140, 58, 1, 8, False),
        "Thunder and Storm": EarthBoundEnemy("Thunder and Storm", 0x15c489, 2065, 70, 129026, 4736, 21, 111, 178, 56, 35, 55, False, None, 2),
        "Yes Man Junior": EarthBoundEnemy("Yes Man Junior", 0x15c4e7, 33, 0, 13, 18, 4, 8, 9, 4, 0, 14, False),
        "Frankystein Mark II": EarthBoundEnemy("Frankystein Mark II", 0x15c545, 91, 0, 76, 31, 4, 15, 18, 7, 0, 40, False, None, 2),
        "Frank": EarthBoundEnemy("Frank", 0x15c5a3, 63, 0, 50, 48, 7, 12, 17, 6, 5, 32, False),
        "Cute Li'l UFO": EarthBoundEnemy("Cute Li'l UFO", 0x15c601, 162, 25, 1519, 110, 58, 49, 32, 27, 1, 70, False),
        "Beautiful UFO": EarthBoundEnemy("Beautiful UFO", 0x15c65f, 339, 15, 8257, 426, 59, 86, 87, 44, 1, 71, False),
        "Pogo Punk": EarthBoundEnemy("Pogo Punk", 0x15c6bd, 35, 0, 15, 18, 3, 8, 10, 4, 0, 15, False),
        "Tough Guy": EarthBoundEnemy("Tough Guy", 0x15c71b, 342, 0, 9310, 525, 18, 72, 92, 37, 20, 16, False),
        "Mad Taxi": EarthBoundEnemy("Mad Taxi", 0x15c779, 253, 0, 2336, 216, 38, 53, 68, 28, 5, 8, False),
        "Evil Mani-Mani": EarthBoundEnemy("Evil Mani-Mani", 0x15c7d7, 860, 88, 28139, 1852, 15, 86, 145, 45, 1, 80, False, None, 2),
        "Mr. Molecule": EarthBoundEnemy("Mr. Molecule", 0x15c835, 280, 21, 8708, 659, 18, 118, 97, 56, 5, 4, False),
        "Worthless Protoplasm": EarthBoundEnemy("Worthless Protoplasm", 0x15c893, 38, 0, 17, 11, 27, 11, 21, 7, 0, 1, False),
        "Sentry Robot": EarthBoundEnemy("Sentry Robot", 0x15c8f1, 372, 0, 5034, 392, 17, 77, 105, 39, 10, 4, False),
        # "Heavily Armed Pokey ": EarthBoundEnemy("Heavily Armed Pokey", 0x15c94f, 1746, 999, 0, 0, 51, 150, 274, 72, False), Unused
        "Psychic Psycho": EarthBoundEnemy("Psychic Psycho", 0x15c9ad, 591, 252, 30094, 682, 30, 124, 144, 58, 1, 24, False),
        "Major Psychic Psycho": EarthBoundEnemy("Major Psychic Psycho", 0x15ca0b, 618, 574, 39247, 862, 31, 145, 152, 65, 1, 24, False),
        "Mole Playing Rough": EarthBoundEnemy("Mole Playing Rough", 0x15ca69, 103, 0, 456, 36, 9, 22, 28, 14, 2, 8, False),
        "Gruff Goat": EarthBoundEnemy("Gruff Goat", 0x15cac7, 45, 0, 20, 9, 12, 8, 23, 7, 0, 16, False),
        "Clumsy Robot": EarthBoundEnemy("Clumsy Robot", 0x15cb25, 962, 0, 32378, 2081, 83, 88, 137, 46, 30, 49, False, "psi_1", 3),
        "Soul Consuming Flame": EarthBoundEnemy("Soul Consuming Flame", 0x15cb83, 602, 0, 37618, 768, 30, 131, 262, 59, 14, 8, False),
        "Demonic Petunia": EarthBoundEnemy("Demonic Petunia", 0x15cbe1, 478, 0, 15171, 724, 26, 102, 111, 50, 5, 9, False),
        "Ranboob": EarthBoundEnemy("Ranboob", 0x15cc3f, 232, 42, 2486, 158, 20, 41, 63, 24, 1, 9, False),
        "Li'l UFO": EarthBoundEnemy("Li'l UFO", 0x15cc9d, 82, 0, 223, 14, 53, 18, 17, 12, 13, 8, False),
        "High-class UFO": EarthBoundEnemy("High-class UFO", 0x15ccfb, 433, 72, 12385, 456, 60, 93, 103, 47, 15, 24, False, "phys_1"),
        "Noose Man": EarthBoundEnemy("Noose Man", 0x15cd59, 231, 0, 1990, 220, 18, 47, 52, 26, 5, 4, False),
        "Robo-pump": EarthBoundEnemy("Robo-pump", 0x15cdb7, 431, 0, 4797, 349, 19, 70, 113, 36, 5, 4, False, None, 2),
        "Plain Crocodile": EarthBoundEnemy("Plain Crocodile", 0x15ce15, 234, 0, 1928, 62, 10, 40, 55, 24, 1, 5, False),
        "Strong Crocodile": EarthBoundEnemy("Strong Crocodile", 0x15ce73, 417, 0, 10122, 495, 17, 85, 131, 43, 5, 6, False),
        "Hard Crocodile": EarthBoundEnemy("Hard Crocodile", 0x15ced1, 522, 0, 19484, 692, 23, 110, 128, 55, 10, 4, False),
        "No Good Fly": EarthBoundEnemy("No Good Fly", 0x15cf2f, 100, 0, 415, 26, 10, 23, 13, 15, 3, 0, False),
        "Mostly Bad Fly": EarthBoundEnemy("Mostly Bad Fly", 0x15cf8d, 141, 0, 1116, 84, 15, 32, 16, 19, 4, 0, False),
        "Spiteful Crow": EarthBoundEnemy("Spiteful Crow", 0x15cfeb, 24, 0, 3, 5, 77, 5, 3, 3, 0, 1, False),
        # "Master Belch": EarthBoundEnemy("Master Belch", 0x15d397, 650, 0, 12509, 664, 16, 50, 88, 27, False), Unused
        # "Insane Cultist (2)": EarthBoundEnemy("Insane Cultist", 0x15d3f5, 94, 0, 353, 33, 8, 19, 25, 13, False),
        "Dept. Store Spook (2)": EarthBoundEnemy("Dept. Store Spook (2)", 0x15d453, 610, 290, 24291, 1648, 19, 82, 135, 42, 24, 62, False),
        "Ness's Nightmare (2)": EarthBoundEnemy("Ness's Nightmare (2)", 0x15d4b1, 1654, 882, 89004, 4442, 31, 172, 253, 71, 1, 80, False),
        "Mr. Carpainter (2)": EarthBoundEnemy("Mr. Carpainter (2)", 0x15d50f, 262, 70, 1412, 195, 8, 33, 45, 21, 13, 72, False),
        "Carbon Dog (2)": EarthBoundEnemy("Carbon Dog (2)", 0x15d56d, 1672, 0, 0, 0, 31, 159, 174, 70, 52, 53, False),
        "Chomposaur (2)": EarthBoundEnemy("Chomposaur (2)", 0x15d5cb, 1288, 320, 44378, 896, 17, 139, 183, 62, 3, 16, False),
        "Titanic Ant (2)": EarthBoundEnemy("Titanic Ant (2)", 0x15d629, 235, 102, 685, 150, 6, 19, 23, 13, 9, 72, False),
        "Gigantic Ant (2)": EarthBoundEnemy("Gigantic Ant (2)", 0x15d687, 308, 81, 3980, 304, 17, 54, 112, 30, 5, 6, False),
        "Shrooom! (2)": EarthBoundEnemy("Shrooom! (2)", 0x15d6e5, 1700, 112, 96323, 4086, 18, 95, 154, 48, 32, 72, False),
        "Plague Rat of Doom (2)": EarthBoundEnemy("Plague Rat of Doom (2)", 0x15d743, 1827, 60, 115272, 4464, 19, 71, 180, 47, 250, 45, False),
        "Mondo Mole (2)": EarthBoundEnemy("Mondo Mole (2)", 0x15d7a1, 498, 161, 5791, 400, 9, 37, 50, 23, 15, 36, False),
        "Guardian Digger (2)": EarthBoundEnemy("Guardian Digger (2)", 0x15d7ff, 386, 110, 17301, 1467, 17, 59, 129, 32, 21, 55, False),
        "Kraken (2)": EarthBoundEnemy("Kraken (2)", 0x15d85d, 1097, 176, 79267, 3049, 21, 105, 166, 54, 1, 32, False),
        # "Bionic Kraken (2)": EarthBoundEnemy("Bionic Kraken", 0x15d8bb, 900, 60, 50308, 960, 42, 155, 195, 70, False),
        "Starman (2)": EarthBoundEnemy("Starman (2)", 0x15d919, 545, 155, 23396, 720, 24, 103, 126, 55, 25, 16, False),
        "Starman Super (2)": EarthBoundEnemy("Starman Super (2)", 0x15d977, 568, 310, 30145, 735, 24, 112, 129, 56, 25, 16, False),
        "Ghost of Starman (2)": EarthBoundEnemy("Ghost of Starman (2)", 0x15d9d5, 750, 462, 48695, 807, 46, 152, 170, 68, 43, 16, False),
        "Starman Deluxe (2)": EarthBoundEnemy("Starman Deluxe (2)", 0x15da33, 1400, 418, 160524, 3827, 27, 143, 186, 65, 43, 21, False),
        "Final Starman (2)": EarthBoundEnemy("Final Starman (2)", 0x15da91, 840, 860, 61929, 915, 47, 178, 187, 71, 25, 24, False),
        "Diamond Dog (2)": EarthBoundEnemy("Diamond Dog (2)", 0x15db4d, 3344, 154, 337738, 6968, 31, 167, 230, 70, 15, 24, False),
        "Trillionage Sprout (2)": EarthBoundEnemy("Trillionage Sprout (2)", 0x15dbab, 1048, 240, 30303, 1358, 16, 54, 88, 29, 21, 71, False),
        "Master Belch (2)": EarthBoundEnemy("Master Belch (2)", 0x15dc09, 650, 0, 12509, 664, 16, 50, 88, 27, 20, 61, False),
        "Master Barf (2)": EarthBoundEnemy("Master Barf (2)", 0x15dcc5, 1319, 0, 125056, 3536, 24, 136, 177, 60, 39, 64, False),
        "Loaded Dice 2": EarthBoundEnemy("Loaded Dice 2", 0x15dd23, 307, 0, 10672, 703, 77, 146, 113, 59, 75, 6, False),
        "Boogey Tent (2)": EarthBoundEnemy("Boogey Tent (2)", 0x15dddf, 579, 56, 5500, 407, 10, 43, 69, 25, 16, 32, False),
        "Everdred (2)": EarthBoundEnemy("Everdred (2)", 0x15de9b, 182, 0, 986, 171, 6, 25, 35, 15, 10, 40, False),
        "Electro Specter (2)": EarthBoundEnemy("Electro Specter (2)", 0x15def9, 3092, 80, 261637, 6564, 29, 148, 203, 67, 47, 56, False),
        "Thunder and Storm (2)": EarthBoundEnemy("Thunder and Storm (2)", 0x15df57, 2065, 70, 129026, 4736, 21, 111, 178, 56, 35, 55, False),
        "Frankystein Mark II (2)": EarthBoundEnemy("Frankystein Mark II (2)", 0x15dfb5, 91, 0, 76, 31, 4, 15, 18, 7, 0, 40, False),
        "Evil Mani-Mani (2)": EarthBoundEnemy("Evil Mani-Mani (2)", 0x15e013, 860, 88, 28139, 1852, 15, 86, 145, 45, 1, 80, False),
        # "Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e071, 1746, 999, 0, 0, 51, 150, 274, 72, False),
        "Clumsy Robot (2)": EarthBoundEnemy("Clumsy Robot (2)", 0x15e0cf, 962, 0, 32378, 2081, 83, 88, 137, 46, 30, 49, False),
        "Robo-pump (2)": EarthBoundEnemy("Robo-pump (2)", 0x15e12d, 431, 0, 4797, 349, 19, 70, 113, 36, 5, 4, False),
        "Guardian General (2)": EarthBoundEnemy("Guardian General (2)", 0x15e1e9, 831, 6, 95390, 3235, 21, 109, 214, 55, 1, 7, False),
        "Black Antoid (2)": EarthBoundEnemy("Black Antoid (2)", 0x15e247, 34, 25, 37, 7, 4, 14, 13, 7, 3, 0, False),  # Separate enemy used in the titanic ant fight
        "Runaway Dog (2)": EarthBoundEnemy("Runaway Dog", 0x15e303, 21, 0, 4, 3, 26, 4, 5, 73, 0, 1, False),
        # "Cave Boy (2)": EarthBoundEnemy("Cave Boy (2)", 0x15e361, 314, 0, 618, 17, 5, 21, 33, 11, False),
        "Tiny Li'l Ghost": EarthBoundEnemy("Tiny Li'l Ghost", 0x15e3bf, 90, 0, 1, 162, 100, 19, 7, 18, 25, 24, False),
        "Starman Junior": EarthBoundEnemy("Starman Junior", 0x15e41d, 200, 999, 16, 20, 1, 11, 10, 6, 0, 80, False),
        "Buzz Buzz": EarthBoundEnemy("Buzz Buzz", 0x15e47b, 2000, 999, 0, 0, 100, 40, 92, 20, 1, 80, False),
        "Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e4d9, 2000, 999, 70000, 0, 60, 145, 255, 80, 5, 255, False),
        # "Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e537, 1746, 999, 0, 0, 51, 150, 274, 72, False), Cutscene?
        "Giygas (2)": EarthBoundEnemy("Giygas (2)", 0x15e595, 9999, 999, 70000, 0, 80, 255, 255, 80, 5, 255, False),
        "Giygas (3)": EarthBoundEnemy("Giygas (3)", 0x15e5f3, 9999, 0, 0, 0, 80, 255, 255, 80, 5, 255, False),
        "Giygas": EarthBoundEnemy("Giygas", 0x15e651, 2000, 0, 0, 0, 80, 255, 255, 80, 5, 255, False),
        "Giygas (5)": EarthBoundEnemy("Giygas (5)", 0x15e6af, 9999, 0, 0, 0, 80, 255, 255, 80, 5, 255, False),
        "Farm Zombie": EarthBoundEnemy("Farm Zombie", 0x15e70d, 171, 0, 700, 58, 10, 31, 24, 19, 15, 24, False),
        "Criminal Caterpillar": EarthBoundEnemy("Criminal Caterpillar", 0x15e76b, 250, 168, 30384, 0, 134, 37, 16, 23, 0, 0, False),
        "Evil Eye": EarthBoundEnemy("Evil Eye", 0x15e7c9, 720, 400, 46376, 896, 38, 141, 162, 63, 25, 16, False),
        "Mini Barf": EarthBoundEnemy("Mini Barf", 0x15e885, 616, 0, 7521, 460, 10, 45, 71, 26, 19, 30, False),
        "Master Criminal Worm": EarthBoundEnemy("Master Criminal Worm", 0x15e8e3, 377, 300, 82570, 0, 136, 73, 40, 37, 0, 0, False),
        "Captain Strong": EarthBoundEnemy("Captain Strong", 0x15e941, 140, 0, 492, 159, 15, 20, 24, 13, 8, 18, False),
        "Giygas (6)": EarthBoundEnemy("Giygas (6)", 0x15e99f, 9999, 0, 0, 0, 80, 255, 127, 80, 5, 255, False),
        "Clumsy Robot (3)": EarthBoundEnemy("Clumsy Robot (3)", 0x15e9fd, 962, 0, 32378, 2081, 83, 88, 137, 46, 30, 49, False)
    }

    shuffled_enemies = {}
    for enemy in world.acting_enemy_list:
        shuffled_enemies[enemy] = world.enemies[world.acting_enemy_list[enemy]]

    flunkies = {
        "Titanic Ant": shuffled_enemies["Black Antoid (2)"],
        "Master Belch": shuffled_enemies["Slimy Little Pile"],
        "Trillionage Sprout": shuffled_enemies["Tough Mobile Sprout"],
        "Master Barf": shuffled_enemies["Even Slimier Little Pile"],
        "Starman Deluxe": [shuffled_enemies["Starman"], shuffled_enemies["Starman Super"]],
        "Carbon Dog": world.enemies[world.boss_list[27]],  # This should be the enemy that gets shuffled WITH carbon dog, right? Fix???
        "Skate Punk": [shuffled_enemies["Pogo Punk"], shuffled_enemies["Yes Man Junior"]],
        "Loaded Dice": [shuffled_enemies["Care Free Bomb"], shuffled_enemies["Beautiful UFO"], shuffled_enemies["High-class UFO"]],
        "Loaded Dice 2": [shuffled_enemies["Electro Swoosh"], shuffled_enemies["Fobby"], shuffled_enemies["Uncontrollable Sphere"]],
        "Starman Super": [shuffled_enemies["Starman"]]
    }

    world.regional_enemies = {"Northern Onett": {shuffled_enemies["Spiteful Crow"], shuffled_enemies["Runaway Dog"], shuffled_enemies["Coil Snake"]},
                              "Onett": {shuffled_enemies["Pogo Punk"], shuffled_enemies["Skate Punk"], shuffled_enemies["Yes Man Junior"], world.enemies[world.boss_list[0]], world.enemies[world.boss_list[1]]},
                              "Arcade": {shuffled_enemies["Pogo Punk"], shuffled_enemies["Skate Punk"], shuffled_enemies["Yes Man Junior"]},
                              "Giant Step": {shuffled_enemies["Attack Slug"], shuffled_enemies["Black Antoid"], shuffled_enemies["Rowdy Mouse"], world.enemies[world.boss_list[2]]},
                              "Twoson": {shuffled_enemies["Black Antoid"], shuffled_enemies["Cop"], world.enemies[world.boss_list[3]], shuffled_enemies["Ramblin' Evil Mushroom"],
                                         shuffled_enemies["Annoying Old Party Man"], shuffled_enemies["Cranky Lady"], shuffled_enemies["Mobile Sprout"], shuffled_enemies["New Age Retro Hippie"], shuffled_enemies["Unassuming Local Guy"],
                                         shuffled_enemies["Runaway Dog"]},
                              "Everdred's House": {world.enemies[world.boss_list[4]]},
                              "Peaceful Rest Valley": {shuffled_enemies["Li'l UFO"], shuffled_enemies["Mobile Sprout"], shuffled_enemies["Spinning Robo"], shuffled_enemies["Territorial Oak"]},
                              "Happy-Happy Village": {shuffled_enemies["Coil Snake"], shuffled_enemies["Insane Cultist"], shuffled_enemies["Spiteful Crow"], shuffled_enemies["Unassuming Local Guy"]},
                              "Happy-Happy HQ": {shuffled_enemies["Insane Cultist"], world.enemies[world.boss_list[5]]},
                              "Lilliput Steps": {shuffled_enemies["Mighty Bear"], shuffled_enemies["Mole Playing Rough"], shuffled_enemies["Mr. Batty"], world.enemies[world.boss_list[6]]},
                              "Threed": {shuffled_enemies["Coil Snake"], shuffled_enemies["Handsome Tom"], shuffled_enemies["Smilin' Sam"], shuffled_enemies["Trick or Trick Kid"],
                                         shuffled_enemies["Zombie Dog"], shuffled_enemies["Putrid Moldyman"], shuffled_enemies["Smelly Ghost"]},
                              "Threed Underground": {shuffled_enemies["No Good Fly"], shuffled_enemies["Urban Zombie"], shuffled_enemies["Zombie Possessor"], world.enemies[world.boss_list[8]], shuffled_enemies["Zombie Dog"]},
                              "Grapefruit Falls": {shuffled_enemies["Armored Frog"], shuffled_enemies["Black Antoid"], shuffled_enemies["Coil Snake"], shuffled_enemies["Farm Zombie"],
                                                   shuffled_enemies["Plain Crocodile"], shuffled_enemies["Red Antoid"], shuffled_enemies["Violent Roach"], shuffled_enemies["Mad Duck"], shuffled_enemies["Black Antoid (2)"]},
                              "Belch's Factory": {shuffled_enemies["Farm Zombie"], shuffled_enemies["Foppy"], shuffled_enemies["Mostly Bad Fly"], shuffled_enemies["Slimy Little Pile"], world.enemies[world.boss_list[9]]},
                              "Milky Well": {shuffled_enemies["Mad Duck"], shuffled_enemies["Ranboob"], shuffled_enemies["Struttin' Evil Mushroom"], shuffled_enemies["Tough Mobile Sprout"], world.enemies[world.boss_list[10]]},
                              "Dusty Dunes Desert": {shuffled_enemies["Bad Buffalo"], shuffled_enemies["Crested Booka"], shuffled_enemies["Criminal Caterpillar"], shuffled_enemies["Cute Li'l UFO"], shuffled_enemies["Desert Wolf"], shuffled_enemies["Mole Playing Rough"],
                                                     shuffled_enemies["Skelpion"], shuffled_enemies["Smilin' Sphere"]},
                              "Fourside": {shuffled_enemies["Annoying Reveler"], shuffled_enemies["Crazed Sign"], shuffled_enemies["Extra Cranky Lady"], shuffled_enemies["Mad Taxi"]},
                              "Moonside": {shuffled_enemies["Abstract Art"], shuffled_enemies["Dali's Clock"], shuffled_enemies["Enraged Fire Plug"], shuffled_enemies["Robo-pump"], world.enemies[world.boss_list[13]]},
                              "Gold Mine": {shuffled_enemies["Gigantic Ant"], shuffled_enemies["Mad Duck"], shuffled_enemies["Noose Man"], shuffled_enemies["Thirsty Coil Snake"], world.enemies[world.boss_list[11]]},
                              "Fourside Dept. Store": {shuffled_enemies["Musica"], shuffled_enemies["Mystical Record"], shuffled_enemies["Scalding Coffee Cup"], world.enemies[world.boss_list[12]]},
                              "Monkey Caves": {shuffled_enemies["Struttin' Evil Mushroom"], shuffled_enemies["Tough Mobile Sprout"]},
                              "Monotoli Building": {shuffled_enemies["Sentry Robot"], world.enemies[world.boss_list[14]]},
                              "Rainy Circle": {shuffled_enemies["Arachnid!"], shuffled_enemies["Elder Batty"], shuffled_enemies["Strong Crocodile"], world.enemies[world.boss_list[15]]},
                              "Andonuts Lab Area": {shuffled_enemies["Cave Boy"], shuffled_enemies["Mighty Bear Seven"]},
                              "Summers": {shuffled_enemies["Crazed Sign"], shuffled_enemies["Mad Taxi"], shuffled_enemies["Mole Playing Rough"], shuffled_enemies["Over Zealous Cop"], shuffled_enemies["Tough Guy"], world.enemies[world.boss_list[18]]},
                              "Summers Museum": {shuffled_enemies["Shattered Man"]},
                              "Magnet Hill": {shuffled_enemies["Deadly Mouse"], shuffled_enemies["Filthy Attack Roach"], shuffled_enemies["Stinky Ghost"], world.enemies[world.boss_list[16]]},
                              "Pink Cloud": {shuffled_enemies["Conducting Menace"], shuffled_enemies["Kiss of Death"], shuffled_enemies["Tangoo"], shuffled_enemies["Thunder Mite"], world.enemies[world.boss_list[17]]},
                              "Scaraba": {shuffled_enemies["Beautiful UFO"], shuffled_enemies["Dread Skelpion"], shuffled_enemies["Great Crested Booka"], shuffled_enemies["High-class UFO"], shuffled_enemies["Master Criminal Worm"]},
                              "Pyramid": {shuffled_enemies["Arachnid!!!"], shuffled_enemies["Fierce Shattered Man"], shuffled_enemies["Guardian Hieroglyph"], shuffled_enemies["Lethal Asp Hieroglyph"], shuffled_enemies["Petrified Royal Guard"],
                                          world.enemies[world.boss_list[19]]},
                              "Southern Scaraba": {shuffled_enemies["Beautiful UFO"], shuffled_enemies["High-class UFO"], shuffled_enemies["Marauder Octobot"]},
                              "Dungeon Man": {shuffled_enemies["Dali's Clock"], shuffled_enemies["Mystical Record"], shuffled_enemies["Lesser Mook"], shuffled_enemies["Mystical Record"], shuffled_enemies["Scalding Coffee Cup"], shuffled_enemies["Worthless Protoplasm"], shuffled_enemies["Cute Li'l UFO"]},
                              "Deep Darkness": {shuffled_enemies["Mole Playing Rough"]},
                              "Winters": {shuffled_enemies["Lesser Mook"], shuffled_enemies["Whirling Robo"], shuffled_enemies["Wooly Shambler"]},
                              "Deep Darkness Darkness": {shuffled_enemies["Big Pile of Puke"], shuffled_enemies["Demonic Petunia"], shuffled_enemies["Even Slimier Little Pile"], shuffled_enemies["Hard Crocodile"], shuffled_enemies["Hostile Elder Oak"],
                                                         shuffled_enemies["Manly Fish"], shuffled_enemies["Manly Fish's Brother"], shuffled_enemies["Pit Bull Slug"], shuffled_enemies["Zap Eel"], world.enemies[world.boss_list[20]]},
                              "Boogey Tent": {world.enemies[world.boss_list[7]]},
                              "Southern Winters": {shuffled_enemies["Lesser Mook"], shuffled_enemies["Whirling Robo"], shuffled_enemies["Wooly Shambler"]},
                              "Brickroad Maze": {shuffled_enemies["Rowdy Mouse"], shuffled_enemies["Worthless Protoplasm"], shuffled_enemies["Mad Duck"]},
                              "Stonehenge Base": {shuffled_enemies["Atomic Power Robot"], shuffled_enemies["Military Octobot"], shuffled_enemies["Mook Senior"], shuffled_enemies["Starman"], shuffled_enemies["Starman Super"], world.enemies[world.boss_list[21]]},
                              "Lumine Hall": {shuffled_enemies["Conducting Spirit"], shuffled_enemies["Fobby"], shuffled_enemies["Hyper Spinning Robo"], shuffled_enemies["Uncontrollable Sphere"], world.enemies[world.boss_list[22]]},
                              "Lost Underworld": {shuffled_enemies["Chomposaur"], shuffled_enemies["Ego Orb"], shuffled_enemies["Wetnosaur"]},
                              "Fire Spring": {shuffled_enemies["Evil Elemental"], shuffled_enemies["Major Psychic Psycho"], shuffled_enemies["Psychic Psycho"], shuffled_enemies["Soul Consuming Flame"], world.enemies[world.boss_list[23]]},
                              "Magicant": {shuffled_enemies["Care Free Bomb"], shuffled_enemies["Electro Swoosh"], shuffled_enemies["French Kiss of Death"], shuffled_enemies["Loaded Dice"], shuffled_enemies["Mr. Molecule"], shuffled_enemies["Loaded Dice 2"]},
                              "Sea of Eden": {world.enemies[world.boss_list[18]], world.enemies[world.boss_list[24]]},
                              "Cave of the Past": {shuffled_enemies["Bionic Kraken"], shuffled_enemies["Final Starman"], shuffled_enemies["Ghost of Starman"], shuffled_enemies["Nuclear Reactor Robot"], shuffled_enemies["Squatter Demon"],
                                                   shuffled_enemies["Ultimate Octobot"], shuffled_enemies["Wild 'n Wooly Shambler"]},
                              "Endgame": {world.enemies[world.boss_list[25]], world.enemies["Giygas (2)"], world.enemies[world.boss_list[28]], world.enemies["Giygas (3)"], world.enemies["Giygas (5)"], world.enemies["Giygas (6)"]},
                        
                              }

    if world.options.randomize_enemy_attacks:
        del flunkies["Loaded Dice 2"]
        del flunkies["Skate Punk"]
        del flunkies["Loaded Dice"]
        del flunkies["Starman Super"]

    for region in world.regional_enemies:
        enemy_list = world.regional_enemies[region]
        updated_list = set(enemy_list)
        for enemy in enemy_list:
            if enemy.name == "Carbon Dog":
                updated_list.add(world.enemies[world.boss_list[27]])
                for i in range(1, world.enemies[world.boss_list[27]].attack_extensions):
                    updated_list.add(world.enemies[f"{world.enemies[world.boss_list[27]].name} ({i + 1})"])
                # todo; option to not have in Giygas/Mine

            if enemy.name in flunkies:
                # Can I just always update instead of doing an add? Would probably need to make singulars a list of one item...
                if enemy.name in ["Starman Deluxe", "Skate Punk", "Loaded Dice", "Loaded Dice 2", "Starman Super"]:
                    updated_list.update(flunkies[enemy.name])
                else:
                    updated_list.add(flunkies[enemy.name])

            if enemy.attack_extensions > 1:
                for i in range(1, enemy.attack_extensions):
                    updated_list.add(world.enemies[f"{enemy.name} ({i + 1})"])
        world.regional_enemies[region] = updated_list


combat_regions = [
    "Northern Onett",
    "Onett",
    "Arcade",
    "Giant Step",
    "Twoson",
    "Happy-Happy Village",
    "Happy-Happy HQ"
    "Lilliput Steps",
    "Winters",
    "Threed",
    "Milky Well",
    "Dusty Dunes Desert",
    "Fourside",
    "Moonside",
    "Gold Mine",
    "Monkey Caves",
    "Monotoli Building",
    "Rainy Circle",
    "Summers",
    "Magnet Hill",
    "Pink Cloud",
    "Scaraba",
    "Pyramid",
    "Southern Scaraba",
    "Dungeon Man",
    "Deep Darkness",
    "Deep Darkness Darkness",
    "Stonehenge Base",
    "Lumine Hall",
    "Lost Underworld",
    "Fire Spring",
    "Magicant",
    "Cave of the Past",
    "Endgame",
    "Grapefruit Falls",
    "Peaceful Rest Valley",
    "Everdred's House",
    "Belch's Factory",
    "Southern Winters",
    "Brickroad Maze"
    "Summers Museum",
    "Fourside Dept. Store",
    "Threed Underground",
    "Boogey Tent"
]


levels = [
    1,  # north onett
    2,  # south onett
    3,  # giant step
    5,  # twoson
    7,  # everdred
    9,  # peaceful rest
    10,  # happy happy
    12,  # lilliput steps
    13,  # threed
    14,  # threed caverns
    15,  # grapefruit falls
    17,  # belch base
    18,  # milky well
    19,  # duty dunes
    21,  # fourside
    23,  # gold mine
    24,  # dept store
    25,  # monkey cabves
    26,  # monotoli building
    28,  # winters
    29,  # southern winters
    31,  # rainy circle
    32,  # summers
    33,  # museum
    35,  # Moonside
    36,  # magnet hill
    38,  # pink cloud
    39,  # scaraba
    42,  # pyramid
    43,  # scaraba south
    45,  # dungeon man
    47,  # deep darkness
    49,  # deep darkness swamp
    51,  # Happy-Happy HQ
    52,  # stonehenge
    54,  # Arcade
    56,  # lumine hall
    59,  # lost underworld
    61,  # fire spring
    63,  # magicant
    65,  # cave of the past
    68,  # Sea of Eden
    70,
    73,
    74,
    75]  # gigyas

spell_breaks: dict[str, dict[int, str]] = {
    "freeze": {8: "zeta", 12: "epsilon", 20: "delta", 25: "lambda", 40: "alpha", 65: "beta", 70: "gamma", 100: "omega"},
    "fire": {5: "zeta", 10: "epsilon", 20: "alpha", 50: "beta", 70: "gamma", 100: "omega"},  # zeta needs to do less damage
    "lifeup": {20: "alpha", 100: "beta"},
    "thunder": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "flash": {25: "alpha", 60: "beta", 70: "gamma", 100: "omega"},
    "special": {5: "zeta", 10: "epsilon", 30: "alpha", 65: "beta", 80: "gamma", 100: "omega"},
    "healing": {20: "alpha", 40: "beta", 60: "gamma", 100: "omega"},
    "starstorm": {5: "zeta", 12: "epsilon", 20: "delta", 45: "lambda", 70: "alpha", 100: "beta"},
    "diamond_eyes": {35: "alpha", 40: "beta", 100: "gamma"},
    "nauseous_breath": {25: "alpha", 100: "beta"},
    "poison_stinger": {25: "alpha", 100: "beta"},
    "kiss_of_death": {25: "alpha", 100: "beta"},
    "summon_storm": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "scalding_espresso": {5: "zeta", 10: "epsilon", 20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "extinguishing_blast": {5: "zeta", 10: "epsilon", 20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "spray_fire": {5: "zeta", 10: "epsilon", 20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "breathe_fire": {5: "zeta", 10: "epsilon", 20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "poisonous_fangs": {25: "alpha", 100: "beta"},
    "flaming_fireball": {5: "zeta", 10: "epsilon", 20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "glorious_light": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "poison_flute": {25: "alpha", 100: "beta"},
    "diamond_bite": {35: "alpha", 40: "beta", 100: "gamma"},
    "scatter_spores": {25: "alpha", 100: "beta"},
    "hacking_cough": {25: "alpha", 100: "beta"},
    "stuffiness_beam": {25: "alpha", 100: "beta"},
    "crashing_boom_bang": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "paralysis": {30: "lambda", 60: "alpha", 100: "omega"},
    "electrical_shock": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "giygas_phase2_thunder": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 100: "beta"},
    "giygas_phase3_thunder": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 100: "beta"},
    "giygas_phase4_thunder": {5: "zeta", 10: "epsilon", 15: "delta", 20: "lambda", 35: "alpha", 100: "beta"},
    "giygas_phase2_freeze": {8: "zeta", 12: "epsilon", 20: "delta", 25: "lambda", 100: "alpha"},
    "giygas_phase3_freeze": {8: "zeta", 12: "epsilon", 20: "delta", 25: "lambda", 100: "alpha"},
    "giygas_phase4_freeze": {8: "zeta", 12: "epsilon", 20: "delta", 25: "lambda", 100: "alpha"},
    "giygas_phase2_flash": {25: "alpha", 60: "beta", 100: "gamma"},
    "giygas_phase3_flash": {25: "alpha", 60: "beta", 100: "gamma"},
    "giygas_phase4_flash": {25: "alpha", 60: "beta", 100: "gamma"},
    "thunder_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 45: "alpha", 60: "beta", 100: "gamma", 200: "omega"},
    "starstorm_minus": {12: "zeta", 20: "epsilon", 45: "delta", 70: "lambda", 100: "alpha", 200: "beta"},
    "flash_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "blast": {10: "zeta", 20: "epsilon", 30: "alpha", 40: "beta", 50: "gamma", 100: "omega"},
    "missile": {5: "zeta", 12: "epsilon", 20: "alpha", 50: "beta", 73: "gamma", 100: "omega"},
    "throw_bomb": {10: "zeta", 20: "epsilon", 30: "alpha", 40: "beta", 50: "gamma", 100: "omega"},
    "throw_bomb_minus": {20: "zeta", 30: "epsilon", 40: "alpha", 50: "beta", 100: "gamma", 200: "omega"},
    "shoot_rocket": {5: "zeta", 12: "epsilon", 20: "alpha", 50: "beta", 73: "gamma", 100: "omega"},
    "paralyzing_pollen": {30: "lambda", 60: "alpha", 100: "omega"},

    "electrical_shock_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 45: "alpha", 60: "beta", 100: "gamma", 200: "omega"},
    "crashing_boom_bang_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 45: "alpha", 60: "beta", 100: "gamma", 200: "omega"},
    "giygas_phase2_thunder_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 100: "alpha", 200: "beta"},
    "giygas_phase3_thunder_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 100: "alpha", 200: "beta"},
    "giygas_phase4_thunder_minus": {10: "zeta", 15: "epsilon", 20: "delta", 35: "lambda", 100: "alpha", 200: "beta"},
    "thunder_minus_minus": {15: "zeta", 20: "epsilon", 35: "delta", 45: "lambda", 60: "alpha", 100: "beta", 200: "gamma", 300: "omega"},

    "starstorm_minus_minus": {20: "zeta", 45: "epsilon", 70: "delta", 100: "lambda", 200: "alpha", 300: "beta"},

    "giygas_phase2_flash_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "giygas_phase3_flash_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "giygas_phase4_flash_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "summon_storm_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "glorious_light_minus": {60: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "flash_minus_minus": {70: "alpha", 100: "beta", 200: "gamma", 300: "omega"},

    "fire_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "spray_fire_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "breathe_fire_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "scalding_espresso_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "flaming_fireball_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "extinguishing_blast_minus": {10: "zeta", 20: "epsilon", 50: "alpha", 70: "beta", 100: "gamma", 200: "omega"},

    "throw_bomb_minus_minus": {30: "zeta", 40: "epsilon", 50: "alpha", 100: "beta", 200: "gamma", 300: "omega"},

    "shoot_rocket_minus": {12: "zeta", 20: "epsilon", 50: "alpha", 73: "beta", 100: "gamma", 200: "omega"},

    "freeze_minus": {12: "zeta", 20: "epsilon", 25: "delta", 40: "lambda", 65: "alpha", 70: "beta", 100: "gamma", 200: "omega"},
    "giygas_phase2_freeze_minus": {12: "zeta", 20: "epsilon", 25: "delta", 100: "lambda", 200: "alpha"},
    "giygas_phase3_freeze_minus": {12: "zeta", 20: "epsilon", 25: "delta", 100: "lambda", 200: "alpha"},
    "giygas_phase4_freeze_minus": {12: "zeta", 20: "epsilon", 25: "delta", 100: "lambda", 200: "alpha"},

    "special_minus": {10: "zeta", 30: "epsilon", 65: "alpha", 80: "beta", 100: "gamma", 200: "omega"},
    "blast_minus": {20: "zeta", 30: "epsilon", 40: "alpha", 50: "beta", 100: "gamma", 200: "omega"},

}


def get_psi_levels(level: int, breaks: dict[str, dict[int, str]]):
  for top_level, psi_val in breaks.items():
    if level <= top_level:
      return psi_val
  return breaks[max(breaks)]


spell_elements = {
    "thunder": "thunder",
    "giygas_phase2_thunder": "thunder",
    "giygas_phase3_thunder": "thunder",
    "giygas_phase4_thunder": "thunder",
    "crashing_boom_bang": "thunder",
    "electrical_shock": "thunder",
    "thunder_minus": "thunder",

    "freeze": "freeze",
    "giygas_phase2_freeze": "freeze",
    "giygas_phase3_freeze": "freeze",
    "giygas_phase4_freeze": "freeze",

    "fire": "fire",
    "scalding_espresson": "fire",
    "extinguishing_blast": "fire",
    "spray_fire": "fire",
    "breathe_fire": "fire",
    "flaming_fireball": "fire",

    "flash": "flash",
    "summon_storm": "flash",
    "glorious_light": "flash",
    "giygas_phase2_flash": "flash",
    "giygas_phase3_flash": "flash",
    "giygas_phase4_flash": "flash",
    "flash_minus": "flash",

    "starstorm": "starstorm",
    "starstorm_minus": "starstorm",

    "special": "special",

    "blast": "explosive",
    "throw_bomb": "explosive",
    "throw_bomb_minus": "explosive"
}

spell_data = {
    "freeze": {
        "zeta": [0x62, 0x01, 0x37],
        "epsilon": [0x63, 0x01, 0x38],
        "delta": [0x64, 0x01, 0x39],
        "lambda": [0x65, 0x01, 0x3A],
        "alpha": [0x12, 0x00, 0x09],
        "beta": [0x13, 0x00, 0x0A],
        "gamma": [0x14, 0x00, 0x0B],
        "omega": [0x15, 0x00, 0x0C]
    },
    "fire": {
        "zeta": [0x60, 0x01, 0x35],
        "epsilon": [0x61, 0x01, 0x36],
        "alpha": [0x0E, 0x00, 0x05],
        "beta": [0x0F, 0x00, 0x06],
        "gamma": [0x10, 0x00, 0x07],
        "omega": [0x11, 0x00, 0x08]
    },
    "lifeup": {
        "alpha": [0x20, 0x00, 0x17],
        "beta": [0x21, 0x00, 0x18]
    },
    "flash": {
        "alpha": [0x1A, 0x00, 0x11],
        "beta": [0x1B, 0x00, 0x12],
        "gamma": [0x1C, 0x00, 0x13],
        "omega": [0x1D, 0x00, 0x14]
    },
    "thunder": {
        "zeta": [0x69, 0x01, 0x3E],
        "epsilon": [0x6A, 0x01, 0x3F],
        "delta": [0x6B, 0x01, 0x40],
        "lambda": [0x6C, 0x01, 0x41],
        "alpha": [0x16, 0x00, 0x0D],
        "beta": [0x17, 0x00, 0x0E],
        "gamma": [0x18, 0x00, 0x0F],
        "omega": [0x19, 0x00, 0x10]
    },
    "special": {
        "zeta": [0x66, 0x01, 0x3B],
        "epsilon": [0x67, 0x01, 0x3C],
        "alpha": [0x0A, 0x00, 0x01],
        "beta": [0x0B, 0x00, 0x02],
        "gamma": [0x0C, 0x00, 0x03],
        "omega": [0x0D, 0x00, 0x04]
    },
    "healing": {
        "alpha": [0x24, 0x00, 0x1B],
        "beta": [0x25, 0x00, 0x1C],
        "gamma": [0x26, 0x00, 0x1D],
        "omega": [0x27, 0x00, 0x1E]
    },
    "starstorm": {
        "zeta": [0x6D, 0x01, 0x42],
        "epsilon": [0x6E, 0x01, 0x43],
        "delta": [0x6F, 0x01, 0x44],
        "lambda": [0x70, 0x01, 0x45],
        "alpha": [0x1E, 0x00, 0x15],
        "beta": [0x1F, 0x00, 0x16]
    },
    "scatter_spores": {
        "alpha": [0x3F, 0x01, 0x00],
        "beta": [0xED, 0x00, 0x00],
    },
    "nauseous_breath": {
        "alpha": [0x4A, 0x00, 0x00],
        "beta": [0x47, 0x00, 0x00]
    },
    "diamond_eyes": {
        "alpha": [0x40, 0x01, 0x00],
        "beta": [0x41, 0x01, 0x00],
        "gamma": [0x44, 0x00, 0x00]
    },
    "glorious_light": {
        "alpha": [0x42, 0x01, 0x00],
        "beta": [0x43, 0x01, 0x00],
        "gamma": [0xC9, 0x00, 0x00],
        "omega": [0x44, 0x01, 0x00],
    },
    "flaming_fireball": {
        "zeta": [0x73, 0x01, 0x00],
        "epsilon": [0x74, 0x01, 0x00],
        "alpha": [0x47, 0x01, 0x00],
        "beta": [0x46, 0x01, 0x00],
        "gamma": [0x45, 0x01, 0x00],
        "omega": [0x68, 0x00, 0x00],
    },
    "breathe_fire": {
        "zeta": [0x71, 0x01, 0x00],
        "epsilon": [0x72, 0x01, 0x00],
        "alpha": [0x48, 0x01, 0x00],
        "beta": [0x49, 0x01, 0x00],
        "gamma": [0x5E, 0x00, 0x00],
        "omega": [0x4A, 0x01, 0x00],
    },
    "spray_fire": {
        "zeta": [0x75, 0x01, 0x00],
        "epsilon": [0x76, 0x01, 0x00],
        "alpha": [0x4B, 0x01, 0x00],
        "beta": [0x4C, 0x01, 0x00],
        "gamma": [0x4D, 0x01, 0x00],
        "omega": [0x5D, 0x00, 0x00],
    },
    "paralysis": {
        "lambda": [0x68, 0x01, 0x3D],
        "alpha": [0x38, 0x00, 0x2F],
        "omega": [0x39, 0x00, 0x30]
    },
    "poisonous_fangs": {
        "alpha": [0x4E, 0x01, 0x00],
        "beta": [0x64, 0x00, 0x00]
    },
    "poison_stinger": {
        "alpha": [0x4F, 0x01, 0x00],
        "beta": [0x48, 0x00, 0x00]
    },
    "crashing_boom_bang": {
        "zeta": [0x7D, 0x01, 0x00],
        "epsilon": [0x7E, 0x01, 0x00],
        "delta": [0x7F, 0x01, 0x00],
        "lambda": [0x80, 0x01, 0x00],
        "alpha": [0x50, 0x01, 0x00],
        "beta": [0x5C, 0x00, 0x00],
        "gamma": [0x51, 0x01, 0x00],
        "omega": [0x52, 0x01, 0x00]
    },

    "electrical_shock": {
        "zeta": [0x79, 0x01, 0x00],
        "epsilon": [0x7A, 0x01, 0x00],
        "delta": [0x7C, 0x01, 0x00],
        "lambda": [0x7B, 0x01, 0x00],
        "alpha": [0x53, 0x01, 0x00],
        "beta": [0xCA, 0x00, 0x00],
        "gamma": [0x54, 0x01, 0x00],
        "omega": [0x55, 0x01, 0x00]
    },

    "scalding_espresso": {
        "zeta": [0x77, 0x01, 0x00],
        "epsilon": [0x78, 0x01, 0x00],
        "alpha": [0x59, 0x00, 0x00],
        "beta": [0x56, 0x01, 0x00],
        "gamma": [0x57, 0x01, 0x00],
        "omega": [0x58, 0x01, 0x00]
    },
    "extinguishing_blast": {
        "zeta": [0x81, 0x01, 0x00],
        "epsilon": [0x82, 0x01, 0x00],
        "alpha": [0x59, 0x01, 0x00],
        "beta": [0x5A, 0x01, 0x00],
        "gamma": [0x5B, 0x00, 0x00],
        "omega": [0x5B, 0x01, 0x00]
    },

    "diamond_bite": {
        "alpha": [0x5C, 0x01, 0x00],
        "beta": [0x5D, 0x01, 0x00],
        "gamma": [0xE4, 0x00, 0x00]
    },
    "poison_flute": {
        "alpha": [0x5E, 0x01, 0x00],
        "beta": [0xCD, 0x00, 0x00]
    },
    "kiss_of_death": {
        "alpha": [0x5F, 0x01, 0x00],
        "beta": [0x49, 0x00, 0x00]
    },
    "stuffiness_beam": {
        "alpha": [0xF1, 0x00, 0x00],
        "beta": [0x45, 0x00, 0x00]
    },
    "hacking_cough": {
        "alpha": [0xD5, 0x00, 0x00],
        "beta": [0x57, 0x00, 0x00]
    },
    "giygas_phase2_thunder": {
        "zeta": [0x87, 0x01, 0x00],
        "epsilon": [0x86, 0x01, 0x00],
        "delta": [0x85, 0x01, 0x00],
        "lambda": [0x84, 0x01, 0x00],
        "alpha": [0x83, 0x01, 0x00],
        "beta": [0x12, 0x01, 0x00]
    },

    "giygas_phase3_thunder": {
        "zeta": [0x8C, 0x01, 0x00],
        "epsilon": [0x8B, 0x01, 0x00],
        "delta": [0x8A, 0x01, 0x00],
        "lambda": [0x89, 0x01, 0x00],
        "alpha": [0x88, 0x01, 0x00],
        "beta": [0x2E, 0x01, 0x00]
    },

    "giygas_phase4_thunder": {
        "zeta": [0x91, 0x01, 0x00],
        "epsilon": [0x90, 0x01, 0x00],
        "delta": [0x8F, 0x01, 0x00],
        "lambda": [0x8E, 0x01, 0x00],
        "alpha": [0x8D, 0x01, 0x00],
        "beta": [0x31, 0x01, 0x00]
    },


    "giygas_phase2_freeze": {
        "zeta": [0x92, 0x01, 0x00],
        "epsilon": [0x93, 0x01, 0x00],
        "delta": [0x94, 0x01, 0x00],
        "lambda": [0x95, 0x01, 0x00],
        "alpha": [0x2C, 0x01, 0x00]
    },

    "giygas_phase3_freeze": {
        "zeta": [0x96, 0x01, 0x00],
        "epsilon": [0x97, 0x01, 0x00],
        "delta": [0x98, 0x01, 0x00],
        "lambda": [0x99, 0x01, 0x00],
        "alpha": [0x2F, 0x01, 0x00]
    },

    "giygas_phase4_freeze": {
        "zeta": [0x9A, 0x01, 0x00],
        "epsilon": [0x9B, 0x01, 0x00],
        "delta": [0x9C, 0x01, 0x00],
        "lambda": [0x9D, 0x01, 0x00],
        "alpha": [0x32, 0x01, 0x00]
    },


    "giygas_phase2_flash": {
        "alpha": [0x9E, 0x01, 0x00],
        "beta": [0x9F, 0x01, 0x00],
        "gamma": [0x2D, 0x01, 0x00]
    },

    "giygas_phase3_flash": {
        "alpha": [0xA0, 0x01, 0x00],
        "beta": [0xA1, 0x01, 0x00],
        "gamma": [0x30, 0x01, 0x00]
    },

    "giygas_phase4_flash": {
        "alpha": [0xA2, 0x01, 0x00],
        "beta": [0xA3, 0x01, 0x00],
        "gamma": [0x33, 0x01, 0x00]
    },
    
    "explosion_damage": {
        "alpha": [0xA7, 0x00, 0x00],
        "beta": [0xA3, 0x01, 0x00],
        "gamma": [0x33, 0x01, 0x00]
    },
    "thunder_minus": {
        "zeta": [0x69, 0x01, 0x3E],
        "epsilon": [0x6A, 0x01, 0x3F],
        "delta": [0x6B, 0x01, 0x40],
        "lambda": [0x6C, 0x01, 0x41],
        "alpha": [0x16, 0x00, 0x0D],
        "beta": [0x17, 0x00, 0x0E],
        "gamma": [0x18, 0x00, 0x0F],
        "omega": [0x19, 0x00, 0x10]
    },

    "flash_minus": {
        "alpha": [0x1A, 0x00, 0x11],
        "beta": [0x1B, 0x00, 0x12],
        "gamma": [0x1C, 0x00, 0x13],
        "omega": [0x1D, 0x00, 0x14]
    },

    "starstorm_minus": {
        "zeta": [0x6D, 0x01, 0x42],
        "epsilon": [0x6E, 0x01, 0x43],
        "delta": [0x6F, 0x01, 0x44],
        "lambda": [0x70, 0x01, 0x45],
        "alpha": [0x1E, 0x00, 0x15],
        "beta": [0x1F, 0x00, 0x16]
    },
    "blast": {
        "zeta": [0xF7, 0x01, 0x58],
        "epsilon": [0xF8, 0x01, 0x59],
        "alpha": [0xA4, 0x01, 0x46],
        "beta": [0xA5, 0x01, 0x47],
        "gamma": [0xA6, 0x01, 0x48],
        "omega": [0xA7, 0x01, 0x48]
    },
    "missile": {
        "zeta": [0xF9, 0x01, 0x5A],
        "epsilon": [0xFA, 0x01, 0x5B],
        "alpha": [0xA8, 0x01, 0x4A],
        "beta": [0xA9, 0x01, 0x4B],
        "gamma": [0xAA, 0x01, 0x4C],
        "omega": [0xAB, 0x01, 0x4D]
    },
    "summon_storm": {
        "alpha": [0xF4, 0x01, 0x00],
        "beta": [0xF5, 0x01, 0x00],
        "gamma": [0x58, 0x00, 0x00],
        "omega": [0xF6, 0x01, 0x00]
    },
    "throw_bomb": {
        "zeta": [0xFC, 0x01, 0x00],
        "epsilon": [0xFB, 0x01, 0x00],
        "alpha": [0xFD, 0x01, 0x00],
        "beta": [0xFE, 0x01, 0x00],
        "gamma": [0xFF, 0x01, 0x00],
        "omega": [0x00, 0x02, 0x00]
    },

    "throw_bomb_minus": {
        "zeta": [0xFC, 0x01, 0x00],
        "epsilon": [0xFB, 0x01, 0x00],
        "alpha": [0xFD, 0x01, 0x00],
        "beta": [0xFE, 0x01, 0x00],
        "gamma": [0xFF, 0x01, 0x00],
        "omega": [0x00, 0x02, 0x00]
    },
    "shoot_rocket": {
        "zeta": [0x01, 0x02, 0x00],
        "epsilon": [0x02, 0x02, 0x00],
        "alpha": [0x03, 0x02, 0x00],
        "beta": [0x04, 0x02, 0x00],
        "gamma": [0x05, 0x02, 0x00],
        "omega": [0x06, 0x02, 0x00]
    },

    "paralyzing_pollen": {
        "lambda": [0x07, 0x02, 0x00],
        "alpha": [0xCB, 0x00, 0x00],
        "omega": [0x08, 0x02, 0x00]
    },


}

shield_table = {
    "disabled": 0x00,
    "phys_1": 0x03,
    "phys_2": 0x04,
    "psi_1": 0x01,
    "psi_2": 0x02
}


def assumed_player_speed_for_level(level: int) -> int:
    return 2 + 58 * (level - 1) / 80


def scale_enemy_speed(enemy: EarthBoundEnemy, new_level: int) -> int:
    normal_dodge_chance = (2 * enemy.speed - assumed_player_speed_for_level(enemy.level)) / 500

    enemy_scaled_speed = (normal_dodge_chance * 500 + assumed_player_speed_for_level(new_level)) / 2
    return enemy_scaled_speed


def scale_exp_2(base_exp: int, base_level: int, new_level: int, world: "EarthBoundWorld") -> int:
    base_scaled_exp = calculate_exp(base_level)
    scaled_exp = calculate_exp(new_level)
    new_exp = base_exp * scaled_exp / base_scaled_exp
    new_exp = max(new_exp, scaled_exp)  # maybe remove? if early scaled
    new_exp = math.ceil(new_exp * world.options.experience_modifier / 100)
    return new_exp


def calculate_exp(level: int) -> float:
    if level > 30:
        return 1000 * math.exp(0.05 * level)
    else:
        return 50 * math.exp(0.15 * level)
        # return 10 * math.exp(0.2 * level) if not boosted


def scale_shield(level: int, shield: str | None) -> str:
    if shield is not None:
        if level < 10:
            enemy_shield = "disabled"
        elif shield in ["phys_1", "phys_2"]:
            if level < 25:
                enemy_shield = "phys_1"
            else:
                enemy_shield = "phys_2"
        elif shield in ["psi_1", "psi_2"]:
            if level < 25:
                enemy_shield = "psi_1"
            else:
                enemy_shield = "psi_2"
        else:
            warning(f"Could not scale shield, found initial value of {shield}, this is probably a typo")
            enemy_shield = "disabled"
        return enemy_shield


guardian_text = [
    0xEEFAA0,
    0xEEFAA6,
    0xEEFAAD,
    0xEEFAB3,
    0xEEFABA,
    0xEEFAC0,
    0xEEFAC6,
    0xEEFACE
]

guardian_intro = {
    "Giant Step": 0x066699,
    "Lilliput Steps": 0x2F97CB,
    "Milky Well": 0x2F67C3,
    "Rainy Circle": 0x2EFAD6,
    "Magnet Hill": 0x083D4D,
    "Pink Cloud": 0x09D2E3,
    "Lumine Hall": 0x09E2A4,
    "Fire Spring": 0x2EFADF
}


def scale_enemies(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    additional_party_members = 0
    if world.options.auto_scale_party_members:
        if world.starting_character != "Ness":
            rom.write_bytes(0x15F5FB, bytearray([max(levels[world.scaled_area_order.index(world.Ness_region)] + world.random.randint(-3, 3), 1)]))

        if world.starting_character != "Paula":
            rom.write_bytes(0x15F60F, bytearray([max(levels[world.scaled_area_order.index(world.Paula_region)] + world.random.randint(-3, 3), 1)]))  # Paula starting level

        if world.starting_character != "Jeff":  
            rom.write_bytes(0x15F623, bytearray([max(levels[world.scaled_area_order.index(world.Jeff_region)] + world.random.randint(-3, 3), 1)]))  # Jeff starting level

        if world.starting_character != "Poo":
            rom.write_bytes(0x15F637, bytearray([max(levels[world.scaled_area_order.index(world.Poo_region)] + world.random.randint(-3, 3), 1)]))  # Poo starting level

    melody_number = 1
    has_badge = False
    c = Counter([world.Ness_region, world.Paula_region, world.Jeff_region, world.Poo_region])
    # for region, level in zip(world.scaled_area_order, levels):
    for region in world.scaled_area_order:
        level = world.area_levels[region]
        if world.options.easy_combat:
            level = max(1, int(level / 2))
        if region in ["Giant Step", "Lilliput Steps", "Milky Well",
                      "Rainy Circle", "Magnet Hill", "Pink Cloud",
                      "Lumine Hall", "Fire Spring"]:
            rom.write_bytes(guardian_intro[region], struct.pack("I", guardian_text[melody_number - 1]))
            melody_number += 1

        if region == world.Badge_region:
            has_badge = True

        additional_party_members += c[region]
        for enemy in world.regional_enemies[region]:
            if enemy.is_scaled is False:
                enemy_hp = int(enemy.hp * level / enemy.level)
                if not world.options.easy_combat:
                    enemy_hp = int(enemy_hp + (enemy_hp * (0.10 * (additional_party_members - 1))))
                enemy_pp = int(enemy.pp * level / enemy.level)
                enemy_exp = int(scale_exp_2(enemy.exp, enemy.level, level, world))
                enemy_money = min(65535, int((enemy.money * level / enemy.level) * world.options.money_drop_multiplier))
                enemy_speed = max(2, int(scale_enemy_speed(enemy, level)))
                enemy_offense = int(enemy.offense * level / enemy.level)
                enemy_defense = int(enemy.defense * level / enemy.level)
                enemy_level = int(enemy.level * level / enemy.level)
                enemy_shield = scale_shield(level, enemy.shield)
                rom.write_bytes(enemy.address + 33, enemy_hp.to_bytes(2, "little"))
                rom.write_bytes(enemy.address + 35, enemy_pp.to_bytes(2, "little"))
                rom.write_bytes(enemy.address + 37, enemy_exp.to_bytes(4, "little"))
                rom.write_bytes(enemy.address + 41, enemy_money.to_bytes(2, "little"))
                rom.write_bytes(enemy.address + 60, enemy_speed.to_bytes(1, "little"))
                rom.write_bytes(enemy.address + 56, enemy_offense.to_bytes(2, "little"))
                rom.write_bytes(enemy.address + 58, enemy_defense.to_bytes(2, "little"))
                rom.write_bytes(enemy.address + 54, enemy_level.to_bytes(1, "little"))
                if enemy.shield is not None:
                    rom.write_bytes(enemy.address + 89, shield_table[enemy_shield].to_bytes(1, "little"))
                
                if enemy.name in world.enemy_psi:
                    for index, spell in [(i, s) for i, s in enumerate(world.enemy_psi[enemy.name]) if s != "null"]:
                        if spell == "special":
                            spell = world.offensive_psi_slots[0].lower()

                        if spell in spell_elements:
                            element = spell_elements[spell]
                        else:
                            element = "None"
                        
                        if element == world.franklin_protection and not has_badge:
                            spell = f"{spell}_minus"
                        psi_level = get_psi_levels(level, spell_breaks[spell])
                        filtered_spell = spell.replace("_minus", "")
                        rom.write_bytes(enemy.address + 70 + (index * 2), bytearray(spell_data[filtered_spell][psi_level][0:2]))
                        rom.write_bytes(enemy.address + 80 + index, bytearray([spell_data[filtered_spell][psi_level][2]]))
                if world.options.shuffle_enemy_drops:
                    rom.write_bytes(enemy.address + 88, bytearray([world.random.choice(world.filler_drops)]))
                enemy.is_scaled = True
