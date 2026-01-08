from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DarkSoulsRemasteredArchipelagoOptions:
    pass


class DarkSoulsRemasteredGame(Game):
    name = "Dark Souls: Remastered"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = DarkSoulsRemasteredArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Create a new CLASS character.  Gift: GIFT  Gender: GENDER",
                data={
                    "CLASS": (self.classes, 1),
                    "GIFT": (self.gifts, 1),
                    "GENDER": (self.genders, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Defeat one of the following Bosses: BOSSES",
                data={
                    "BOSSES": (self.bosses, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat MINIBOSS",
                data={
                    "MINIBOSS": (self.minibosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat one of the following Minibosses: MINIBOSSES",
                data={
                    "MINIBOSSES": (self.minibosses, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Enter the following Area: AREA",
                data={
                    "AREA": (self.areas, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Light the following Bonfire: BONFIRE",
                data={
                    "BONFIRE": (self.bonfires, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Light one of the following Bonfires: BONFIRES",
                data={
                    "BONFIRES": (self.bonfires, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Fully kindle the following Bonfire: BONFIRE",
                data={
                    "BONFIRE": (self.bonfires, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Navigate between the 2 following Bonfires without resting: BONFIRES",
                data={
                    "BONFIRES": (self.bonfires, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Starting at BONFIRE, navigate to the following area without resting: AREA",
                data={
                    "BONFIRE": (self.bonfires, 1),
                    "AREA": (self.areas, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Trade in the following Ember: EMBER",
                data={
                    "EMBER": (self.embers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Upgrade the Estus Flask to have +COUNT potency",
                data={
                    "COUNT": (self.flask_potency_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain and cast one of the following Miracles: MIRACLES",
                data={
                    "MIRACLES": (self.miracles, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain and cast one of the following Pyromancies: PYROMANCIES",
                data={
                    "PYROMANCIES": (self.pyromancies, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain and cast one of the following Sorceries: SORCERIES",
                data={
                    "SORCERIES": (self.sorceries, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain one of the following Weapons: WEAPONS",
                data={
                    "WEAPONS": (self.weapons_melee, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Fully upgrade one of the following Weapons: WEAPONS  Allowed Upgrade Paths: PATHS",
                data={
                    "WEAPONS": (self.weapons_melee, 3),
                    "PATHS": (self.weapon_upgrade_paths, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat a boss with one of the following Weapons: WEAPONS",
                data={
                    "WEAPONS": (self.weapons_melee, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain one of the following Ranged Weapons: RANGED_WEAPONS",
                data={
                    "RANGED_WEAPONS": (self.weapons_ranged, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill an enemy with one of the following Ranged Weapons: RANGED_WEAPONS",
                data={
                    "RANGED_WEAPONS": (self.weapons_ranged, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain one of the following Caster Items: ITEMS",
                data={
                    "ITEMS": (self.caster_items, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain one of the following Shields: SHIELDS",
                data={
                    "SHIELDS": (self.shields, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat a boss while wielding one of the following Shields: SHIELDS",
                data={
                    "SHIELDS": (self.shields, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Ascend of the following Boss Soul Item: ITEMS",
                data={
                    "ITEMS": (self.boss_soul_items, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect one of the following Helms: HELMS",
                data={
                    "HELMS": (self.armor_helms, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect one of the following pieces of Chest Armor: ARMORS",
                data={
                    "ARMORS": (self.armor_chest_armors, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect one of the following Gauntlets: GAUNTLETS",
                data={
                    "GAUNTLETS": (self.armor_gauntlets, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect one of the following pieces of Leg Armor: LEGS",
                data={
                    "LEGS": (self.armor_leg_armors, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Acquire one of the following Rings: RINGS",
                data={
                    "RINGS": (self.rings, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Acquire one of the following Keys: KEYS",
                data={
                    "KEYS": (self.keys, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Level LEVEL",
                data={
                    "LEVEL": (self.level_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def classes() -> List[str]:
        return [
            "Warrior",
            "Knight",
            "Wanderer",
            "Thief",
            "Bandit",
            "Hunter",
            "Sorcerer",
            "Pyromancer",
            "Cleric",
            "Deprived",
        ]

    @staticmethod
    def gifts() -> List[str]:
        return [
            "None",
            "None",
            "Goddess's Blessing",
            "Black Firebomb",
            "Twin Humanities",
            "Binoculars",
            "Pendant",
            "Master Key",
            "Tiny Being's Ring",
            "Old Witch's Ring",
        ]

    @staticmethod
    def genders() -> List[str]:
        return [
            "Female",
            "Male",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Artorias the Abysswalker",
            "Asylum Demon",
            "Bell Gargoyle",
            "Black Dragon Kalameet",
            "Capra Demon",
            "Ceaseless Discharge",
            "Centipede Demon",
            "Chaos Witch Quelaag",
            "Crossbreed Priscilla",
            "Dark Sun Gwyndolin",
            "Demon Firesage",
            "Four Kings",
            "Gaping Dragon",
            "Great Grey Wolf Sif",
            "Gwyn Lord of Cinder",
            "Iron Golem",
            "Manus, Father of the Abyss",
            "Moonlight Butterfly",
            "Nito",
            "Ornstein and Smough",
            "Pinwheel",
            "Sanctuary Guardian",
            "Seath the Scaleless",
            "Stray Demon",
            "Taurus Demon",
            "The Bed of Chaos",
        ]

    @staticmethod
    def minibosses() -> List[str]:
        return [
            "Black Hydra",
            "Black Phantom",
            "Butcher",
            "Fang Boar",
            "Giant Cat",
            "Giant Rat",
            "Golden Crystal Golem",
            "Havel The Rock",
            "Hydra",
            "Mass of Souls",
            "Ricard the Archer",
            "The Berenike Knights",
            "The Black Knight",
            "The Bridge Wyvern",
            "The Channeler",
            "Titanite Demon",
            "Undead Dragon",
        ]

    @staticmethod
    def areas() -> List[str]:
        return [
            "Anor Londo",
            "Battle of Stoicism",
            "Blighttown",
            "Chasm of the Abyss",
            "Crystal Cave",
            "Darkroot Basin",
            "Darkroot Garden",
            "Demon Ruins",
            "Depths",
            "Firelink Shrine",
            "Kiln of The First Flame",
            "Lost Izalith",
            "New Londo Ruins",
            "Northern Undead Asylum",
            "Oolacile Sanctuary",
            "Oolacile Township",
            "Quelaag's Domain",
            "Royal Woods",
            "Sanctuary Garden",
            "Sen's Fortress",
            "The Abyss",
            "The Catacombs",
            "The Duke's Archives",
            "The Valley of Drakes",
            "Tomb of Giants",
            "Undead Burg",
            "Undead Parish",
        ]

    @staticmethod
    def bonfires() -> List[str]:
        return [
            "Undead Asylum (Courtyard)",
            "Undead Asylum (After Boss)",
            "Firelink Shrine",
            "Undead Burg (Below Bridge)",
            "Undead Burg (After Bridge)",
            "Undead Parish",
            "Darkroot Garden",
            "Darkroot Basin",
            "Depths",
            "Blighttown (Catwalk)",
            "Blighttown (Swamp)",
            "Quelaag's Domain",
            "The Great Hollow",
            "Ash Lake (After Tree)",
            "Ash Lake (Stone Dragon)",
            "Demon Ruins (Entrance)",
            "Demon Ruins (Staircase)",
            "Demon Ruins (Catacombs)",
            "Lost Izalith (Lava Pits)",
            "Lost Izalith (Illusory Wall)",
            "Lost Izalith (Heart of Chaos)",
            "Sen's Fortress",
            "Anor Londo (Entrance)",
            "Anor Londo (Darkmoon Tomb)",
            "Anor Londo (Residence)",
            "Anor Londo (Princess Chamber)",
            "Painted World of Ariamis",
            "The Duke's Archives (Seath)",
            "The Duke's Archives (Prison Cell)",
            "The Duke's Archives (Balcony)",
            "Crystal Cave",
            "Catacombs (Entrance)",
            "Catacombs (Illusory Wall)",
            "Catacombs (Blacksmith)",
            "Tomb of Giants (Patches)",
            "Tomb of Giants (Midway)",
            "Tomb of Giants (Nito)",
            "The Abyss",
            "Sanctuary Garden",
            "Oolacile Sanctuary",
            "Oolacile Township (Artorias)",
            "Oolacile Township (Dungeon)",
            "Chasm of the Abyss",
        ]

    @staticmethod
    def miracles() -> List[str]:
        return [
            "Bountiful Sunlight",
            "Darkmoon Blade",
            "Emit Force",
            "Force",
            "Gravelord Greatsword Dance",
            "Gravelord Sword Dance",
            "Great Heal Excerpt",
            "Great Heal",
            "Great Lightning Spear",
            "Great Magic Barrier",
            "Heal",
            "Homeward",
            "Karmic Justice",
            "Lightning Spear",
            "Magic Barrier",
            "Replenishment",
            "Seek Guidance",
            "Soothing Sunlight",
            "Sunlight Blade",
            "Sunlight Spear",
            "Tranquil Walk of Peace",
            "Vow of Silence",
            "Wrath of the Gods",
        ]

    @staticmethod
    def pyromancies() -> List[str]:
        return [
            "Acid Surge",
            "Black Flame",
            "Chaos Fire Whip",
            "Chaos Storm",
            "Combustion",
            "Fire Orb",
            "Fire Surge",
            "Fire Tempest",
            "Fire Whip",
            "Fireball",
            "Firestorm",
            "Flash Sweat",
            "Great Chaos Fireball",
            "Great Combustion",
            "Great Fireball",
            "Iron Flesh",
            "Poison Mist",
            "Power Within",
            "Toxic Mist",
            "Undead Rapport",
        ]

    @staticmethod
    def sorceries() -> List[str]:
        return [
            "Aural Decoy",
            "Cast Light",
            "Chameleon",
            "Crystal Magic Weapon",
            "Crystal Soul Spear",
            "Dark Bead",
            "Dark Fog",
            "Dark Orb",
            "Fall Control",
            "Great Heavy Soul Arrow",
            "Great Magic Weapon",
            "Great Soul Arrow",
            "Heavy Soul Arrow",
            "Hidden Body",
            "Hidden Weapon",
            "Homing Crystal Soulmass",
            "Homing Soulmass",
            "Hush",
            "Magic Shield",
            "Magic Weapon",
            "Pursuers",
            "Remedy",
            "Repair",
            "Resist Curse",
            "Soul Arrow",
            "Soul Spear",
            "Strong Magic Shield",
            "White Dragon Breath",
        ]

    @staticmethod
    def weapons_melee() -> List[str]:
        return [
            "Astora's Straight Sword",
            "Balder Side Sword",
            "Bandit's Knife",
            "Barbed Straight Sword",
            "Bastard Sword",
            "Battle Axe",
            "Black Knight Greataxe",
            "Black Knight Greatsword",
            "Black Knight Halberd",
            "Black Knight Sword",
            "Blacksmith Giant Hammer",
            "Blacksmith Hammer",
            "Broadsword",
            "Broken Straight Sword",
            "Butcher Knife",
            "Caestus",
            "Channeler's Trident",
            "Claws",
            "Claymore",
            "Club",
            "Crescent Axe",
            "Crystal Greatsword",
            "Crystal Straight Sword",
            "Dagger",
            "Dark Hand",
            "Dark Silver Tracer",
            "Darksword",
            "Demon Great Machete",
            "Demon's Great Hammer",
            "Demon's Greataxe",
            "Demon's Spear",
            "Dragon Greatsword",
            "Dragon King Greataxe",
            "Dragon Tooth",
            "Drake Sword",
            "Estoc",
            "Falchion",
            "Flamberge",
            "Four-pronged Plow",
            "Gargoyle Tail Axe",
            "Gargoyle's Halberd",
            "Ghost Blade",
            "Giant's Halberd",
            "Gold Tracer",
            "Grant",
            "Gravelord Sword",
            "Great Club",
            "Great Scythe",
            "Greataxe",
            "Greatsword",
            "Guardian Tail",
            "Halberd",
            "Hammer of Vamos",
            "Hand Axe",
            "Iaito",
            "Jagged Ghost Blade",
            "Large Club",
            "Longsword",
            "Lucerne",
            "Mace",
            "Mail Breaker",
            "Man-Serpent Greatsword",
            "Moonlight Greatsword",
            "Morning Star",
            "Murakumo",
            "Notched Whip",
            "Obsidian Greatsword",
            "Painting Guardian Sword",
            "Parrying Dagger",
            "Partizan",
            "Pickaxe",
            "Pike",
            "Priscilla's Dagger",
            "Rapier",
            "Reinforced Club",
            "Ricard's Rapier",
            "Scimitar",
            "Scythe",
            "Server",
            "Shortsword",
            "Shotel",
            "Silver Knight Spear",
            "Silver Knight Straight Sword",
            "Spear",
            "Stone Greataxe",
            "Stone Greatsword",
            "Straight Sword Hilt",
            "Sunlight Straight Sword",
            "Titanite Catch Pole",
            "Uchigatana",
            "Velka's Rapier",
            "Warpick",
            "Washing Pole",
            "Whip",
            "Winged Spear",
            "Zweihander",
        ]

    @staticmethod
    def weapons_ranged() -> List[str]:
        return [
            "Avelyn",
            "Black Bow of Pharis",
            "Composite Bow",
            "Dragonslayer Greatbow",
            "Gough's Greatbow",
            "Heavy Crossbow",
            "Light Crossbow",
            "Longbow",
            "Short Bow",
            "Sniper Crossbow",
        ]

    @staticmethod
    def flames() -> List[str]:
        return [
            "Ascended Pyromancy Flame",
            "Pyromancy Flame",
        ]

    @staticmethod
    def catalysts() -> List[str]:
        return [
            "Beatrice's Catalyst",
            "Demon's Catalyst",
            "Izalith Catalyst",
            "Logan's Catalyst",
            "Oolacile Catalyst",
            "Oolacile Ivory Catalyst",
            "Sorcerer's Catalyst",
            "Tin Banishment Catalyst",
            "Tin Crystallization Catalyst",
        ]

    @staticmethod
    def talismans() -> List[str]:
        return [
            "Canvas Talisman",
            "Darkmoon Talisman",
            "Gwynevere's Talisman",
            "Ivory Talisman",
            "Sunlight Talisman",
            "Talisman",
            "Thorolund Talisman",
            "Velka's Talisman",
        ]

    def caster_items(self) -> List[str]:
        return sorted(
            self.flames() + self.catalysts() + self.talismans()
        )

    @staticmethod
    def shields() -> List[str]:
        return [
            "Balder Shield",
            "Black Iron Greatshield",
            "Black Knight Shield",
            "Bloodshield",
            "Bonewheel Shield",
            "Buckler",
            "Caduceus Kite Shield",
            "Caduceus Round Shield",
            "Cleansing Greatshield",
            "Cracked Round Shield",
            "Crest Shield",
            "Crystal Shield",
            "Dragon Crest Shield",
            "Eagle Shield",
            "East-West Shield",
            "Effigy Shield",
            "Gargoyle's Shield",
            "Giant Shield",
            "Grass Crest Shield",
            "Havel's Greatshield",
            "Heater Shield",
            "Hollow Soldier Shield",
            "Iron Round Shield",
            "Knight Shield",
            "Large Leather Shield",
            "Leather Shield",
            "Pierce Shield",
            "Plank Shield",
            "Red & White Round Shield",
            "Sanctus",
            "Silver Knight Shield",
            "Small Leather Shield",
            "Spider Shield",
            "Spiked Shield",
            "Stone Greatshield",
            "Sunlight Shield",
            "Target Shield",
            "Tower Kite Shield",
            "Tower Shield",
            "Warrior's Round Shield",
            "Wooden Shield",
        ]

    @staticmethod
    def boss_soul_items() -> List[str]:
        return [
            "Abyss Greatsword",
            "Chaos Blade",
            "Crystal Ring Shield",
            "Cursed Greatsword of Artorias",
            "Darkmoon Bow",
            "Dragon Bone Fist",
            "Dragonslayer Spear",
            "Golem Axe",
            "Great Lord Greatsword",
            "Greatshield of Artorias",
            "Greatsword of Artorias",
            "Lifehunt Scythe",
            "Manus Catalyst",
            "Moonlight Butterfly Horn",
            "Quelaag's Furysword",
            "Smough's Hammer",
            "Tin Darkmoon Catalyst",
        ]

    @staticmethod
    def armor_helms() -> List[str]:
        return [
            "Balder Helm",
            "Big Hat",
            "Black Iron Helm",
            "Black Knight Helm",
            "Black Sorcerer Hat",
            "Bloated Head",
            "Bloated Sorcerer Head",
            "Brass Helm",
            "Brigand Hood",
            "Catarina Helm",
            "Chain Helm",
            "Cleric Helm",
            "Crown of Dusk",
            "Crown of the Dark Sun",
            "Crown of the Great Lord",
            "Crystalline Helm",
            "Dark Mask",
            "Dingy Hood",
            "Eastern Helm",
            "Elite Knight Helm",
            "Fang Boar Helm",
            "Gargoyle Helm",
            "Giant Helm",
            "Gold-Hemmed Black Hood",
            "Golem Helm",
            "Gough's Helm",
            "Guardian Helm",
            "Havel's Helm",
            "Helm of Artorias",
            "Helm of Favor",
            "Helm of Thorns",
            "Helm of the Wise",
            "Hollow Soldier Helm",
            "Hollow Thief's Hood",
            "Hollow Warrior Helm",
            "Iron Helm",
            "Knight Helm",
            "Maiden Hood",
            "Mask of Velka",
            "Mask of the Child",
            "Mask of the Father",
            "Mask of the Mother",
            "Mask of the Sealer",
            "Ornstein's Helm",
            "Painting Guardian Hood",
            "Paladin Helm",
            "Pharis's Hat",
            "Porcelain Mask",
            "Priest's Hat",
            "Royal Helm",
            "Sack",
            "Shadow Mask",
            "Silver Knight Helm",
            "Six-Eyed Helm of the Channelers",
            "Smough's Helm",
            "Snickering Top Hat",
            "Sorcerer Hat",
            "Standard Helm",
            "Steel Helm",
            "Stone Helm",
            "Sunlight Maggot",
            "Symbol of Avarice",
            "Tattered Cloth Hood",
            "Thief Mask",
            "Wanderer Hood",
            "Witch Hat",
            "Xanthous Crown",
        ]

    @staticmethod
    def armor_chest_armors() -> List[str]:
        return [
            "Antiquated Dress",
            "Armor of Artorias",
            "Armor of Thorns",
            "Armor of the Glorious",
            "Armor of the Sun",
            "Balder Armor",
            "Black Cleric Robe",
            "Black Iron Armor",
            "Black Knight Armor",
            "Black Leather Armor",
            "Black Sorcerer Cloak",
            "Brass Armor",
            "Brigand Armor",
            "Catarina Armor",
            "Chain Armor",
            "Chester's Long Coat",
            "Cleric Armor",
            "Crimson Robe",
            "Crystalline Armor",
            "Dark Armor",
            "Dingy Robe",
            "Eastern Armor",
            "Elite Knight Armor",
            "Embraced Armor of Favor",
            "Giant Armor",
            "Gold-Hemmed Black Cloak",
            "Golem Armor",
            "Gough's Armor",
            "Guardian Armor",
            "Hard Leather Armor",
            "Havel's Armor",
            "Hollow Soldier Armor",
            "Hollow Thief's Leather Armor",
            "Hollow Warrior Armor",
            "Holy Robe",
            "Knight Armor",
            "Leather Armor",
            "Lord's Blade Robe",
            "Maiden Robe",
            "Moonlight Robe",
            "Ornstein's Armor",
            "Painting Guardian Robe",
            "Paladin Armor",
            "Robe of the Channelers",
            "Robe of the Great Lord",
            "Sage Robe",
            "Shadow Garb",
            "Silver Knight Armor",
            "Smough's Armor",
            "Sorcerer Cloak",
            "Steel Armor",
            "Stone Armor",
            "Tattered Cloth Robe",
            "Wanderer Coat",
            "Witch Cloak",
            "Xanthous Overcoat",
        ]

    @staticmethod
    def armor_gauntlets() -> List[str]:
        return [
            "Antiquated Gloves",
            "Balder Gauntlets",
            "Black Iron Gauntlets",
            "Black Knight Gauntlets",
            "Black Leather Gloves",
            "Black Manchette",
            "Black Sorcerer Gauntlets",
            "Bracelet of the Great Lord",
            "Brass Gauntlets",
            "Brigand Gauntlets",
            "Catarina Gauntlets",
            "Chester's Gloves",
            "Crimson Gloves",
            "Crystalline Gauntlets",
            "Dark Gauntlets",
            "Dingy Gloves",
            "Eastern Gauntlets",
            "Elite Knight Gauntlets",
            "Gauntlets of Artorias",
            "Gauntlets of Favor",
            "Gauntlets of Thorns",
            "Gauntlets of the Channelers",
            "Gauntlets of the Vanquisher",
            "Giant Gauntlets",
            "Gold-Hemmed Black Gloves",
            "Golem Gauntlets",
            "Gough's Gauntlets",
            "Guardian Gauntlets",
            "Hard Leather Gauntlets",
            "Havel's Gauntlets",
            "Iron Bracelet",
            "Knight Gauntlets",
            "Leather Gauntlets",
            "Leather Gloves",
            "Lord's Blade Gloves",
            "Maiden Gloves",
            "Moonlight Gloves",
            "Orntein's Gauntlets",
            "Painting Guardian Gloves",
            "Paladin Gauntlets",
            "Shadow Gauntlets",
            "Silver Knight Gauntlets",
            "Smough's Gauntlets",
            "Sorcerer Gauntlets",
            "Steel Gauntlets",
            "Stone Gauntlets",
            "Tattered Cloth Manchette",
            "Travelling Gloves",
            "Wanderer Manchette",
            "Witch Gloves",
            "Xanthous Gloves",
        ]

    @staticmethod
    def armor_leg_armors() -> List[str]:
        return [
            "Anklet of the Great Lord",
            "Antiquated Skirt",
            "Balder Leggings",
            "Black Iron Leggings",
            "Black Knight Leggings",
            "Black Leather Boots",
            "Black Sorcerer Boots",
            "Black Tights",
            "Blood-Stained Skirt",
            "Boots of the Explorer",
            "Brass Leggings",
            "Brigand Trousers",
            "Catarina Leggings",
            "Chain Leggings",
            "Chester's Trousers",
            "Crimson Waistcloth",
            "Crystalline Leggings",
            "Dark Leggings",
            "Eastern Leggings",
            "Elite Knight Leggings",
            "Giant Leggings",
            "Gold-Hemmed Black Skirt",
            "Golem Leggings",
            "Gough's Leggings",
            "Guardian Leggings",
            "Hard Leather Boots",
            "Havel's Leggings",
            "Heavy Boots",
            "Hollow Soldier Waistcloth",
            "Hollow Thief's Tights",
            "Hollow Warrior Waistcloth",
            "Holy Trousers",
            "Iron Leggings",
            "Knight Leggings",
            "Leather Boots",
            "Leggings of Artorias",
            "Leggings of Favor",
            "Leggings of Thorns",
            "Lord's Blade Waistcloth",
            "Maiden Skirt",
            "Moonlight Waistcloth",
            "Ornstein's Leggings",
            "Painting Guardian Waistcloth",
            "Paladin Leggings",
            "Shadow Leggings",
            "Silver Knight Leggings",
            "Smough's Leggings",
            "Sorcerer Boots",
            "Steel Leggings",
            "Stone Leggings",
            "Travelling Boots",
            "Waistcloth of the Channelers",
            "Wanderer Boots",
            "Witch Skirt",
            "Xanthous Waistcloth",
        ]

    @staticmethod
    def rings() -> List[str]:
        return [
            "Bellowing Dragoncrest Ring",
            "Bloodbite Ring",
            "Blue Tearstone Ring",
            "Calamity Ring",
            "Cat Covenant Ring",
            "Cloranthy Ring",
            "Covenant of Artorias",
            "Covetous Gold Serpent Ring",
            "Covetous Silver Serpent Ring",
            "Cursebite Ring",
            "Dark Wood Grain Ring",
            "Darkmoon Blade Covenant Ring",
            "Darkmoon Seance Ring",
            "Dusk Crown Ring",
            "East Wood Grain Ring",
            "Flame Stoneplate Ring",
            "Havel's Ring",
            "Hawk Ring",
            "Hornet Ring",
            "Leo Ring",
            "Lingering Dragoncrest Ring",
            "Old Witch's Ring",
            "Orange Charred Ring",
            "Poisonbite Ring",
            "Rare Ring of Sacrifice",
            "Red Tearstone Ring",
            "Ring of Favor and Protection",
            "Ring of Fog",
            "Ring of Sacrifice",
            "Ring of Steel Protection",
            "Ring of the Evil Eye",
            "Ring of the Sun Princess",
            "Ring of the Sun's Firstborn",
            "Rusted Iron Ring",
            "Slumbering Dragoncrest Ring",
            "Speckled Stoneplate Ring",
            "Spell Stoneplate Ring",
            "Thunder Stoneplate Ring",
            "Tiny Being's Ring",
            "White Seance Ring",
            "Wolf Ring",
        ]

    @staticmethod
    def weapon_upgrade_paths() -> List[str]:
        return [
            "Chaos",
            "Crystal",
            "Divine",
            "Enchanted",
            "Fire",
            "Lightning",
            "Magic",
            "Occult",
            "Raw",
            "Regular",
            "Unique",
        ]

    @staticmethod
    def embers() -> List[str]:
        return [
            "Chaos Flame Ember",
            "Crystal Ember",
            "Dark Ember",
            "Divine Ember",
            "Enchanted Ember",
            "Large Divine Ember",
            "Large Ember",
            "Large Flame Ember",
            "Large Magic Ember",
            "Very Large Ember",
        ]

    @staticmethod
    def keys() -> List[str]:
        return [
            "Annex Key",
            "Archive Prison Extra Key",
            "Archive Tower Cell Key",
            "Archive Tower Giant Cell Key",
            "Archive Tower Giant Door Key",
            "Basement Key",
            "Big Pilgrim's Key",
            "Blighttown Key",
            "Broken Pendant",
            "Cage Key",
            "Crest Key",
            "Crest of Artorias",
            "Dungeon Cell Key",
            "Key to Depths",
            "Key to New Londo Ruins",
            "Key to the Seal",
            "Master Key",
            "Mystery Key",
            "Peculiar Doll",
            "Residence Key",
            "Sewer Chamber Key",
            "Undead Asylum F2 East Key",
            "Undead Asylum F2 West Key",
            "Watchtower Basement Key",
        ]

    @staticmethod
    def level_range() -> range:
        return range(20, 71)

    @staticmethod
    def flask_potency_range() -> range:
        return range(1, 8)


# Archipelago Options
# ...
